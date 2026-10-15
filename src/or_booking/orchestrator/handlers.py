"""One handler per state (Section 6.1): call the domain and the ports, then pick the next edge.

`enter_<state>` runs when a request enters a state. States that wait for input also have
`input_<state>`, which receives the interpreted message. Handlers never move a request
themselves; they return a step and the engine moves it along the transition table.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, Any

from or_booking.domain.errors import BookingError, HoldExpired
from or_booking.domain.impact import change_impact
from or_booking.domain.matching import MatchKind, MatchResult
from or_booking.domain.models import (
    AuthorizationRef,
    BookedCase,
    BookingField,
    CaseDraft,
    CaseUpdate,
    Channel,
    Contact,
    FieldValue,
    ImplantRequest,
    Issue,
    IssueKind,
    Laterality,
    Ownership,
    Patient,
    Payer,
    Procedure,
    ResolvedBy,
    SourceKind,
    Stage,
    Surgeon,
    SurgicalOrder,
    Unsupported,
)
from or_booking.domain.policy import Facts, HospitalPolicies, RouteAction, Situation, applicable_requirements, case_facts, route_for
from or_booking.domain.ranking import rank_options, requested_day_status
from or_booking.domain.readiness import after, booking_gates, readiness_list, readiness_risks
from or_booking.domain.sizing import override, size_case
from or_booking.domain.straight_through import StraightThroughInputs, evaluate
from or_booking.domain.strategies import select_strategy
from or_booking.domain.validation import (
    build_booking_request,
    matching_order,
    next_issue,
    parse_date_window,
    patient_lookup_keys,
    qualify_booking,
    qualify_query,
    query_inputs,
    resolve_patient,
)
from or_booking.interpretation.schemas import Intent, TurnInterpretation
from or_booking.orchestrator import cards
from or_booking.orchestrator.context import STAY, Go, Step, TurnOutput
from or_booking.orchestrator.router import route_intake
from or_booking.orchestrator.session import Session, SessionKind
from or_booking.orchestrator.states import State
from or_booking.ports.document_ingest import InboundDocument
from or_booking.ports.outbox import OutboundMessage

if TYPE_CHECKING:
    from or_booking.orchestrator.engine import Orchestrator

F = BookingField
QUERY_FIELDS = {F.SURGEON, F.PROCEDURE, F.DATE_WINDOW}
CONFIRMATION_FIELDS = [
    F.PATIENT_NAME, F.PATIENT_DOB, F.SURGEON, F.PROCEDURE, F.LATERALITY, F.DIAGNOSIS,
    F.ANESTHESIA_TYPE, F.PATIENT_CLASS, F.IMPLANTS, F.AUTHORIZATION,
]  # fmt: skip


class Handlers:
    def __init__(self, engine: Orchestrator) -> None:
        self.o = engine
        self.ports = engine.ports
        self.repo = engine.repo

    def enter(self, s: Session, out: TurnOutput) -> Step:
        return getattr(self, f"enter_{s.state.name.lower()}")(s, out)

    def input(self, s: Session, interp: TurnInterpretation, out: TurnOutput) -> Step:
        return getattr(self, f"input_{s.state.name.lower()}")(s, interp, out)

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def now(self) -> datetime:
        return self.ports.clock.now()

    def today(self) -> date:
        return self.now().date()

    def policies(self) -> HospitalPolicies:
        return self.ports.policy_store.policies()

    def surgeon(self, s: Session) -> Surgeon:
        return self.ports.directory.get_surgeon(s.draft.resolved(F.SURGEON) or "")

    def procedure(self, s: Session) -> Procedure:
        return self.ports.directory.get_procedure(s.draft.resolved(F.PROCEDURE) or "")

    def decide(self, s: Session, name: str, detail: dict[str, Any]) -> None:
        self.o.record_decision(s, name, detail)

    def route(self, s: Session, situation: Situation, reason: str) -> bool:
        """Apply the hospital's routing policy. True if the agent carries on with the request."""
        route = route_for(self.policies(), situation)
        s.route, s.route_reason = route, reason
        self.decide(s, "route", {"situation": situation.value, "action": route.action.value, "route_to": route.route_to})
        return route.agent_continues or route.action is RouteAction.AGENT_PROCEEDS

    def identify_patient(self, draft: CaseDraft) -> CaseDraft:
        """The draft with the patient resolved, if name and date of birth identify exactly one."""
        name, dob = patient_lookup_keys(draft, self.today())
        if not name or dob is None:
            return draft
        return resolve_patient(draft, self.ports.directory.find_patients(name, dob), self.today()).draft

    def records(self, s: Session) -> tuple[Patient | None, list[SurgicalOrder], Payer | None]:
        mrn = s.draft.resolved(F.PATIENT_NAME)
        if mrn is None:
            return None, [], None
        patient = self.ports.directory.get_patient(mrn)
        payer = self.ports.directory.get_payer(patient.payer_id) if patient.payer_id else None
        return patient, self.ports.directory.orders_for_patient(mrn), payer

    def facts(self, s: Session, procedure: Procedure) -> Facts:
        draft = self.identify_patient(s.draft)
        mrn = draft.resolved(F.PATIENT_NAME)
        patient = self.ports.directory.get_patient(mrn) if mrn else None
        payer = self.ports.directory.get_payer(patient.payer_id) if patient and patient.payer_id else None
        orders = self.ports.directory.orders_for_patient(mrn) if mrn else []
        order = matching_order(orders, s.draft.resolved(F.SURGEON) or "", procedure.id)
        return case_facts(
            procedure=procedure,
            payer=payer,
            authorization=order.authorization if order else None,
            patient=patient,
            loaner_first_time=s.draft.loaner_first_time,
            urgency=s.draft.stated_urgency,
        )

    def display(self, s: Session) -> dict[BookingField, str]:
        """How each resolved value reads on a card."""
        d, shown = s.draft, {}
        if d.resolved(F.SURGEON):
            shown[F.SURGEON] = self.surgeon(s).display_name
        if d.resolved(F.PROCEDURE):
            procedure = self.procedure(s)
            shown[F.PROCEDURE] = f"{procedure.name} ({procedure.id}, CPT {procedure.cpt})"
            if d.resolved(F.IMPLANTS) and procedure.implant:
                i = procedure.implant
                extras = [x for x, on in (("loaner set", i.loaner_set), ("rep attending", i.rep_attends)) if on]
                shown[F.IMPLANTS] = ", ".join([f"{i.system} ({i.vendor_name})", *extras])
        if mrn := d.resolved(F.PATIENT_NAME):
            shown[F.PATIENT_NAME] = f"{self.ports.directory.get_patient(mrn).name} (MRN {mrn})"
        if d.resolved(F.DIAGNOSIS):
            fv = d.get(F.DIAGNOSIS)
            shown[F.DIAGNOSIS] = f"{fv.value} ({fv.stated})" if fv and fv.stated != fv.value else d.resolved(F.DIAGNOSIS)
        for field in (F.ANESTHESIA_TYPE, F.PATIENT_CLASS, F.LATERALITY):
            if value := d.resolved(field):
                shown[field] = value.replace("_", " ")
        if window := d.resolved(F.DATE_WINDOW):
            start, end = (date.fromisoformat(x) for x in window.split("/"))
            shown[F.DATE_WINDOW] = f"{cards.day_label(start)} to {cards.day_label(end)}"
        return shown

    def draft_message(
        self, s: Session, role: str, recipient: Contact | None, subject: str, body: str, channel: Channel | None = None
    ) -> None:
        channel = channel or (Channel.FAX if recipient and recipient.fax else Channel.EMAIL)
        record = self.ports.outbox.draft(
            OutboundMessage(request_id=s.request_id, recipient_role=role, recipient=recipient, channel=channel, subject=subject, body=body)
        )
        s.drafts.append(f"{record.draft_id}: {subject} (to {recipient.name if recipient else role}, {channel.value}, draft)")

    def requester(self, s: Session) -> Contact | None:
        if s.requester:
            return s.requester
        return self.surgeon(s).office if s.draft.resolved(F.SURGEON) else None

    # ------------------------------------------------------------------
    # Intake and matching
    # ------------------------------------------------------------------

    def enter_intake(self, s: Session, out: TurnOutput) -> Step:
        incoming = out.incoming
        if isinstance(incoming, InboundDocument):
            extracted = self.o.interpreter.extract_document(incoming)
            if extracted is None:
                s.intent = Intent.UNCLEAR
                out.say("I couldn't read this document reliably; a person should look at it.")
            else:
                s.intent = extracted.intent
                self.o.apply_mentions(s, extracted.mentions, SourceKind.DOCUMENT)
                if extracted.stated_urgency != "none":
                    s.draft = s.draft.model_copy(update={"stated_urgency": extracted.stated_urgency})
                s.requester = extracted.sender or (Contact(name=incoming.sender) if incoming.sender else None)
        else:
            interp = self.o.interpret(s, str(incoming))
            s.intent = interp.intent if interp else Intent.UNCLEAR
            if interp:
                self.o.apply(s, interp, SourceKind.COORDINATOR)
        return Go(State.MATCHING)

    def enter_matching(self, s: Session, out: TurnOutput) -> Step:
        return route_intake(self, s)

    def answer_status(self, s: Session, match: MatchResult) -> Step:
        s.kind = SessionKind.INQUIRY
        if match.kind is MatchKind.BOOKED_CASE and match.case_id:
            case = self.ports.scheduling.get_case(match.case_id)
            s.case_id = case.case_id
            s.answer = [("Answer", f"Case {case.case_id}"), *self.case_rows(case)]
            s.readiness = self.case_readiness(case)
            still_open = sum(i.status.value != "done" for i in s.readiness)
            s.summary = (
                f"{case.case_id} is {case.status.value}: {cards.day_label(case.start)}, {case.room_id}, "
                f"{cards.time_label(case.start)}-{cards.time_label(case.end)}. {still_open} readiness items still open."
            )
        elif match.kind in (MatchKind.CONTINUATION, MatchKind.DUPLICATE) and match.request_id:
            other = self.repo.load(match.request_id)
            waiting_on = other.last_question if other and other.last_question else "nothing from the office"
            s.answer = [("Answer", f"Request {match.request_id}"), ("Status", f"Not booked yet ({other.state.value if other else '?'})"),
                        ("Waiting on", waiting_on)]  # fmt: skip
            s.summary = f"Not booked yet: request {match.request_id} is waiting on {waiting_on}."
        else:
            s.answer = [("Answer", "No match"), ("Reason", match.reason)]
            s.summary = "No booked case or open request matches."
        return Go(State.ANSWERED)

    def answer_availability(self, s: Session) -> Step:
        s.kind = SessionKind.INQUIRY
        if not self.qualify_query(s):
            s.summary = "To check open time I need " + ", ".join(i.field.value.replace("_", " ") for i in s.issues) + "."
            s.answer = [("Answer", "Open time")]
            return Go(State.ANSWERED)
        procedure = self.procedure(s)
        s.sizing = self.size(s, procedure)
        plan = select_strategy(procedure, self.surgeon(s)).plan(query_inputs(s.draft), s.sizing.minutes)
        if isinstance(plan, Unsupported):
            s.summary, s.answer = plan.reason, [("Answer", "Open time")]
            return Go(State.ANSWERED)
        result = self.ports.scheduling.search_availability(plan)
        ranked = rank_options(result.options, s.sizing.minutes, self.today(), limit=5)
        s.summary = f"{len(result.options)} windows fit a {s.sizing.minutes.typical}-minute case (read-only; nothing held)."
        s.answer = [("Answer", "Open time"), *((f"Option {r.rank}", cards.option_line(r)) for r in ranked)]
        return Go(State.ANSWERED)

    def case_rows(self, case: BookedCase) -> list[tuple[str, str]]:
        procedure = self.ports.directory.get_procedure(case.procedure_id)
        patient = self.ports.directory.get_patient(case.patient_mrn) if case.patient_mrn else None
        return [
            ("Case", case.case_id),
            ("Status", case.status.value),
            ("When", f"{cards.day_label(case.start)}, {cards.time_label(case.start)}-{cards.time_label(case.end)}"),
            ("Room", case.room_id),
            ("Patient", f"{patient.name} (MRN {patient.mrn})" if patient else "-"),
            ("Surgeon", self.ports.directory.get_surgeon(case.surgeon_id).display_name),
            ("Procedure", procedure.name + (f", {case.laterality.value}" if case.laterality else "")),
        ]

    def case_readiness(self, case: BookedCase) -> list:
        procedure = self.ports.directory.get_procedure(case.procedure_id)
        patient = self.ports.directory.get_patient(case.patient_mrn) if case.patient_mrn else None
        payer = self.ports.directory.get_payer(patient.payer_id) if patient and patient.payer_id else None
        orders = self.ports.directory.orders_for_patient(patient.mrn) if patient else []
        order = matching_order(orders, case.surgeon_id, case.procedure_id)
        facts = case_facts(procedure=procedure, payer=payer, authorization=order.authorization if order else None, patient=patient)
        return readiness_list(self.policies(), facts, case.start, self.now())

    # ------------------------------------------------------------------
    # Events and booked cases
    # ------------------------------------------------------------------

    def enter_event_received(self, s: Session, out: TurnOutput) -> Step:
        if s.ranked:  # time opened, and the waitlisted request now has options (the engine checked)
            out.say(f"Time opened for the waitlisted request {s.parent_request_id}.")
            return Go(State.PRESENTING)
        return Go(State.CASE_LOADED)

    def enter_case_loaded(self, s: Session, out: TurnOutput) -> Step:
        case = self.ports.scheduling.get_case(s.case_id or "")
        s.draft = self.prefill_from_case(s.draft, case)
        needs_slot = s.event is not None or s.draft.get(F.DATE_WINDOW) is not None or s.draft.get(F.PREFERENCES) is not None
        if s.event is not None:
            out.say(f"Case {case.case_id} was displaced ({s.event.type.value.replace('_', ' ')}). Finding a new slot.")
        change = f"moving {case.case_id} to a new date" if needs_slot else f"changing the details of {case.case_id}"
        impact = change_impact(case, self.case_readiness(case), change)
        out.say(f"{impact.reason}; check {', '.join(impact.would_need)} by hand.")
        if needs_slot:
            s.kind = SessionKind.RESCHEDULE
            return Go(State.COLLECTING)
        s.kind = SessionKind.UPDATE
        return Go(State.COMPLETING)

    def prefill_from_case(self, draft: CaseDraft, case: BookedCase) -> CaseDraft:
        """Identity comes from the booked case; other fields only where the request didn't state a change."""
        patient = self.ports.directory.get_patient(case.patient_mrn) if case.patient_mrn else None
        surgeon = self.ports.directory.get_surgeon(case.surgeon_id)
        procedure = self.ports.directory.get_procedure(case.procedure_id)
        identity = {
            F.SURGEON: (surgeon.id, surgeon.display_name),
            F.PROCEDURE: (procedure.id, procedure.name),
        }
        if patient:
            identity[F.PATIENT_NAME] = (patient.mrn, patient.name)
            identity[F.PATIENT_DOB] = (patient.dob.isoformat(), patient.dob.isoformat())
        details = {
            F.LATERALITY: case.laterality.value if case.laterality else None,
            F.DIAGNOSIS: case.diagnosis_code,
            F.ANESTHESIA_TYPE: case.anesthesia_type.value if case.anesthesia_type else None,
            F.PATIENT_CLASS: case.patient_class.value if case.patient_class else None,
            F.IMPLANTS: case.implants[0].vendor_id if case.implants else None,
        }

        def from_case(value: str, stated: str) -> FieldValue:
            return FieldValue.proposed(value, SourceKind.BOOKED_CASE, evidence=case.case_id, stated=stated).resolve(
                value, ResolvedBy.LOOKUP, ref=case.case_id
            )

        for field, (value, stated) in identity.items():
            draft = draft.set(field, from_case(value, stated))
        for field, value in details.items():
            if value is not None and draft.get(field) is None:
                draft = draft.set(field, from_case(value, value))
        if draft.get(F.DIAGNOSIS) is None and patient:  # fixture cases may lack a code: take the order's
            order = matching_order(self.ports.directory.orders_for_patient(patient.mrn), surgeon.id, procedure.id)
            if order:
                draft = draft.set(F.DIAGNOSIS, from_case(order.diagnosis.code, order.diagnosis.description))
        return draft

    # ------------------------------------------------------------------
    # Finding time
    # ------------------------------------------------------------------

    def qualify_query(self, s: Session) -> bool:
        d = s.draft
        surgeons = self._lookup(d, F.SURGEON, self.ports.directory.find_surgeons, self.ports.directory.get_surgeon)
        procedures = self._lookup(d, F.PROCEDURE, self.ports.directory.find_procedures, self.ports.directory.get_procedure)
        q = qualify_query(d, surgeons=surgeons, procedures=procedures, today=self.today())
        s.draft, s.issues = q.draft, q.issues
        return q.ready

    @staticmethod
    def _lookup(draft: CaseDraft, field: BookingField, find, get) -> list:
        fv = draft.get(field)
        if fv is None:
            return []
        return [get(fv.value)] if fv.is_resolved else find(fv.stated)

    def enter_collecting(self, s: Session, out: TurnOutput) -> Step:
        if self.qualify_query(s):
            return Go(State.SEARCHING)
        hard = [i for i in s.issues if i.hard]
        if hard:
            s.route, s.route_reason = None, hard[0].detail
            return Go(State.HANDED_OFF)
        return Go(State.CLARIFYING)

    def size(self, s: Session, procedure: Procedure):
        history = self.ports.duration_history
        estimate = size_case(
            history.surgeon_durations(s.draft.resolved(F.SURGEON) or "", procedure.id),
            history.procedure_durations(procedure.id),
            procedure.default_minutes,
        )
        return override(estimate, s.draft.duration_override) if s.draft.duration_override else estimate

    def enter_searching(self, s: Session, out: TurnOutput) -> Step:
        surgeon, procedure = self.surgeon(s), self.procedure(s)
        s.sizing = self.size(s, procedure)
        plan = select_strategy(procedure, surgeon, s.draft.stated_urgency).plan(query_inputs(s.draft), s.sizing.minutes)
        if isinstance(plan, Unsupported):
            self.route(s, Situation.UNSUPPORTED_BOOKING_STRATEGY, f"{plan.capability}: {plan.reason}")
            return Go(State.ROUTED_OUT)
        try:
            result = self.ports.scheduling.search_availability(plan)
        except BookingError as err:
            s.route_reason = f"The scheduling system refused the search ({err.code}): {err.message}"
            return Go(State.WAITLISTED)
        s.availability = result
        facts = self.facts(s, procedure)
        policies = self.policies()
        risks = {o.option_id: readiness_risks(readiness_list(policies, facts, o.start, self.now())) for o in result.options}
        s.ranked = rank_options(result.options, s.sizing.minutes, self.today(), risks)
        if not s.ranked:
            closed = f"; the schedule has closed for {', '.join(cards.day_label(d) for d in result.closed_dates)}" if result.closed_dates else ""
            held = f"; {len(result.held)} windows sit in other owners' unreleased blocks" if result.held else ""
            s.route_reason = f"No bookable time fits a {s.sizing.minutes.typical}-minute case in those dates{closed}{held}"
            return Go(State.WAITLISTED)
        return Go(State.PRESENTING)

    def enter_presenting(self, s: Session, out: TurnOutput) -> Step:
        procedure, surgeon = self.procedure(s), self.surgeon(s)
        side = s.draft.get(F.LATERALITY)
        sizing = s.sizing
        assert sizing is not None
        title = f"{surgeon.display_name}: {procedure.name}" + (f", {side.stated}" if side else "")
        still_needed = self.booking_preview(s, procedure)
        out.card(
            cards.OptionsCard(
                title=title,
                sizing=f"{sizing.minutes.typical} min typical, {sizing.minutes.long} min long. {sizing.note}",
                options=[cards.option_card(r, sizing) for r in s.ranked],
                still_needed=still_needed,
            )
        )
        facts = {
            "options": [c.model_dump() for c in (cards.option_card(r, sizing) for r in s.ranked)],
            "still_needed": still_needed,
        }
        out.say(self.o.interpreter.phrase("explain_options", facts, fallback=self._options_line(s, still_needed)))
        return STAY

    def _options_line(self, s: Session, still_needed: list[str]) -> str:
        first = s.ranked[0]
        parts = [f"{len(s.ranked)} option{'s' if len(s.ranked) > 1 else ''}."]
        if first.counts_toward_block:
            over = f", but runs {first.overrun_minutes} min past at the long length" if first.overrun_minutes else ""
            parts.append(f"Option 1 is in the surgeon's own block{over}.")
        if still_needed:
            parts.append("Still needed to book: " + "; ".join(still_needed) + ".")
        return " ".join(parts)

    def booking_preview(self, s: Session, procedure: Procedure) -> list[str]:
        """What the booking will still need, shown with the options so it can come back in the same reply."""
        name, dob = patient_lookup_keys(s.draft, self.today())
        needed = []
        if name:
            preview = resolve_patient(s.draft, self.ports.directory.find_patients(name, dob), self.today())
            needed += [_preview(i) for i in preview.issues]
        facts = case_facts(procedure=procedure)
        for rule in applicable_requirements(self.policies(), facts):
            needed += [_preview_missing(f) for f in rule.require if s.draft.get(f) is None and not (f is F.PATIENT_DOB and needed)]
        return list(dict.fromkeys(needed))

    def input_presenting(self, s: Session, interp: TurnInterpretation, out: TurnOutput) -> Step:
        given = interp.mentions + interp.corrections
        self.o.apply_mentions(s, [m for m in given if m.field not in QUERY_FIELDS], SourceKind.COORDINATOR)
        if interp.intent is Intent.SELECT_OPTION and interp.selected_option and 1 <= interp.selected_option <= len(s.ranked):
            s.selected_option_id = s.ranked[interp.selected_option - 1].option.option_id
            return Go(State.HOLDING)
        if interp.intent is Intent.REQUEST_WAITLIST:
            s.route_reason = s.route_reason or "Waiting for time that isn't bookable now"
            return Go(State.WAITLISTED)
        days = [w.start for m in given if m.field is F.DATE_WINDOW and (w := parse_date_window(m.value, self.today())) and w.start == w.end]
        if days or interp.intent is Intent.REQUEST_RELEASE:
            return self._requested_day(s, days[0] if days else None, out)
        if any(m.field in {F.SURGEON, F.PROCEDURE, F.DATE_WINDOW} for m in given):
            out.say("A different surgeon, procedure or date range needs a new search; start a new request for that.")
        elif given:
            out.say("Noted: " + ", ".join(cards.FIELD_LABELS[m.field].lower() for m in given) + ".")
        else:
            out.say("Pick an option by number, ask for a different day, or say 'waitlist'.")
        return STAY

    def _requested_day(self, s: Session, day: date | None, out: TurnOutput) -> Step:
        if day is None or s.availability is None:
            out.say("Which day would you like?")
            return STAY
        status = requested_day_status(day, s.availability)
        label = cards.day_label(day)
        if status.status == "bookable":
            number = next(r.rank for r in s.ranked if r.option.date == day) if any(r.option.date == day for r in s.ranked) else None
            out.say(f"{label} is option {number} above." if number else f"{label} has time, but it ranks below the options shown.")
            return STAY
        if status.status == "schedule_closed":
            self.route(s, Situation.ADD_ON_AFTER_CLOSE, f"Schedule for {label} has closed")
            out.say(f"The schedule for {label} has closed; add-ons go to {', '.join(_roles(s.route.route_to))} per policy.")
            return STAY
        if status.status == "no_fit":
            out.say(f"Nothing on {label} fits a {s.sizing.minutes.typical if s.sizing else '?'}-minute case.")
            return STAY
        blocks = "; ".join(
            f"{w.room_id} is {w.block_owner_name}'s block, releases {cards.day_label(w.releases_at)} {cards.time_label(w.releases_at)}"
            for w in status.held
            if w.releases_at
        )
        continues = self.route(s, Situation.OTHER_OWNER_UNRELEASED_BLOCK, f"{label} requested: {blocks}")
        for w in status.held:
            owner = self.ports.directory.get_surgeon(w.block_owner_id) if w.block_owner_id and w.block_owner_id.startswith("S-") else None
            window = f"{cards.time_label(w.start)}-{cards.time_label(w.end)}"
            body = f"Would you release {window} on {label} in {w.room_id} for {self.surgeon(s).display_name} ({self.procedure(s).name})?"
            if w.releases_at:
                body += f" It releases automatically {cards.day_label(w.releases_at)} {cards.time_label(w.releases_at)} otherwise."
            recipient = owner.office if owner else Contact(name=w.block_owner_name or "block owner")
            self.draft_message(s, "block_owner", recipient, f"Release request: {label}, {w.room_id}, {window}", body)
        out.say(f"{label} isn't bookable: {blocks}. I've drafted a release request for you to send.")
        if continues:
            out.say(f"Pick one of the options above, or say 'waitlist' to wait for {label}.")
            return STAY
        return Go(State.WAITLISTED)

    # ------------------------------------------------------------------
    # Booking it
    # ------------------------------------------------------------------

    def enter_holding(self, s: Session, out: TurnOutput) -> Step:
        if s.selected_option_id is None:
            return Go(State.SEARCHING)
        try:
            s.hold = self.ports.scheduling.place_hold(s.selected_option_id, s.request_id)
        except BookingError as err:
            out.say(f"That slot is no longer available ({err.code}): {err.message} Searching again.")
            s.selected_option_id, s.hold = None, None
            return Go(State.SEARCHING)
        return Go(State.COMPLETING)

    def enter_completing(self, s: Session, out: TurnOutput) -> Step:
        procedure = self.procedure(s)
        name, dob = patient_lookup_keys(s.draft, self.today())
        candidates = self.ports.directory.find_patients(name, dob) if name else []
        found = resolve_patient(s.draft, candidates, self.today())
        s.draft = found.draft
        patient, orders, payer = self.records(s)
        surgery_date = s.hold.start.date() if s.hold else self.ports.scheduling.get_case(s.case_id or "").date
        identity = frozenset({F.PATIENT_NAME, F.PATIENT_DOB}) if found.issues else frozenset()
        booking = qualify_booking(
            s.draft, procedure=procedure, patient=patient, orders=orders, payer=payer,
            policies=self.policies(), surgery_date=surgery_date, today=self.today(), already_raised=identity,
        )  # fmt: skip
        s.draft = booking.draft
        s.issues = found.issues + booking.issues
        if s.issues:
            return Go(State.CLARIFYING)

        order = matching_order(orders, s.draft.resolved(F.SURGEON) or "", procedure.id)
        facts = case_facts(procedure=procedure, payer=payer, authorization=order.authorization if order else None, patient=patient)
        gate_applies = any(g.applies for g in booking_gates(self.policies(), facts, surgery_date, self.today()))
        authorization = AuthorizationRef(status=order.authorization.status, number=order.authorization.number) if gate_applies and order else None
        if s.kind is SessionKind.UPDATE:
            side = s.draft.resolved(F.LATERALITY)
            s.case_update = CaseUpdate(
                case_id=s.case_id or "",
                laterality=Laterality(side) if side else None,
                diagnosis_code=s.draft.resolved(F.DIAGNOSIS) or "",
                anesthesia_type=s.draft.resolved(F.ANESTHESIA_TYPE),
                patient_class=s.draft.resolved(F.PATIENT_CLASS),
                implants=[ImplantRequest(system=i.system, vendor_id=i.vendor_id, loaner_set=i.loaner_set, rep_attending=i.rep_attends)]
                if (i := procedure.implant)
                else [],
                updated_by=s.coordinator_id,
                idempotency_key=s.request_id,
            )
        else:
            assert s.hold is not None and s.sizing is not None
            s.booking_request = build_booking_request(
                s.draft, option_id=s.hold.option_id, procedure=procedure, scheduled_minutes=s.sizing.minutes.typical,
                booked_by=s.coordinator_id, idempotency_key=s.request_id, requested_by=self.requester(s), authorization=authorization,
            )  # fmt: skip
        return Go(State.CONFIRMING)

    def enter_clarifying(self, s: Session, out: TurnOutput) -> Step:
        issue = next_issue(s.issues)
        assert issue is not None
        key = issue.field.value
        s.attempts[key] = s.attempts.get(key, 0) + 1
        limit = self.o.max_clarifications
        if s.attempts[key] > limit:
            situation = (
                Situation.UNRESOLVABLE_CONFLICT if issue.kind is IssueKind.CONFLICTS_WITH_ORDER else Situation.CLARIFICATION_ATTEMPTS_EXHAUSTED
            )
            self.route(s, situation, f"Asked {limit} times without an answer that resolves it: {issue.detail}")
            return Go(State.HANDED_OFF)
        s.open_question = issue
        stated = s.draft.get(issue.field)
        facts = {"field": issue.field.value, "kind": issue.kind.value, "detail": issue.detail, "candidate_count": issue.candidate_count,
                 "stated": stated.stated if stated else None}  # fmt: skip
        s.last_question = self.o.interpreter.phrase("ask_clarification", facts, fallback=question_text(issue, stated))
        out.say(s.last_question)
        if s.interactive:
            return STAY
        recipient = self.requester(s)
        same_channel = s.draft.channel if s.draft.channel in (Channel.FAX, Channel.EMAIL) else None  # answer the way it came in
        self.draft_message(s, "requester", recipient, f"Question about your surgery request {s.request_id}", s.last_question, same_channel)
        rule = self.policies().routing_for(Situation.CLARIFICATION_UNANSWERED)
        s.reply_deadline = after(self.now(), rule.reply_deadline) if rule and rule.reply_deadline else None
        return Go(State.AWAITING_REPLY)

    def input_clarifying(self, s: Session, interp: TurnInterpretation, out: TurnOutput) -> Step:
        self.o.apply(s, interp, SourceKind.COORDINATOR)
        question, s.open_question = s.open_question, None
        if question is None or question.stage is Stage.QUERY:
            return Go(State.COLLECTING)
        return Go(State.COMPLETING)

    def enter_awaiting_reply(self, s: Session, out: TurnOutput) -> Step:
        self.release_hold(s)
        recipient = self.requester(s)
        deadline = f" until {cards.day_label(s.reply_deadline)} {cards.time_label(s.reply_deadline)}" if s.reply_deadline else ""
        out.say(f"Asked {recipient.name if recipient else 'the requester'}; parked{deadline}. A reply on any channel resumes it.")
        return STAY

    def input_awaiting_reply(self, s: Session, interp: TurnInterpretation, out: TurnOutput) -> Step:
        self.o.apply(s, interp, SourceKind.COORDINATOR)
        s.open_question = None
        return Go(State.COLLECTING)

    def enter_confirming(self, s: Session, out: TurnOutput) -> Step:
        option = next((r.option for r in s.ranked if r.option.option_id == s.selected_option_id), None)
        s.verdict = evaluate(
            self.policies().autonomy_for("straight_through_booking"),
            StraightThroughInputs(
                issues=s.issues,
                order_conflict=False,
                strategy_supported=True,
                ownership=option.ownership if option else Ownership.OWN_BLOCK,
                resource_conflict=False,
                schedule_closed=False,
                duration_overridden=s.draft.duration_override is not None,
                duplicate=False,
            ),
        )
        out.card(self.confirmation_card(s))
        if s.verdict.would_act:
            out.say("Approved automatically under the hospital's straight-through booking policy.")
            return Go(State.COMMITTING)
        out.say("Ready to book. Say 'confirm', or tell me what to change.")
        return STAY

    def confirmation_card(self, s: Session) -> cards.ConfirmationCard:
        if s.kind is SessionKind.UPDATE:
            case = self.ports.scheduling.get_case(s.case_id or "")
            slot = f"{case.case_id} stays at {cards.day_label(case.start)}, {case.room_id}, {cards.time_label(case.start)}-{cards.time_label(case.end)}"
        else:
            assert s.hold is not None and s.sizing is not None
            end = s.hold.end
            slot = f"{cards.day_label(s.hold.start)}, {s.hold.room_id}, {cards.time_label(s.hold.start)}-{cards.time_label(end)} ({s.sizing.minutes.typical} min booked; long length {s.sizing.minutes.long})"
            if s.kind is SessionKind.RESCHEDULE:
                slot = f"Move {s.case_id} to {slot}"
        verdict = s.verdict
        if verdict is None or verdict.mode.value == "disabled":
            st = "Straight-through booking: not enabled"
        elif verdict.eligible:
            st = f"Straight-through ({verdict.mode.value}): would qualify" + (" (not acted on)" if not verdict.would_act else "")
        else:
            st = f"Straight-through ({verdict.mode.value}): wouldn't qualify ({', '.join(c.value for c in verdict.failed)})"
        return cards.ConfirmationCard(
            title=f"Confirm booking for {s.request_id}",
            slot=slot,
            rows=cards.field_rows(s.draft, self.display(s), CONFIRMATION_FIELDS),
            hold_expires=cards.time_label(s.hold.expires_at) if s.hold else None,
            straight_through=st,
        )

    def input_confirming(self, s: Session, interp: TurnInterpretation, out: TurnOutput) -> Step:
        if interp.intent is Intent.CONFIRM:
            return Go(State.COMMITTING)
        if interp.mentions or interp.corrections:
            self.o.apply(s, interp, SourceKind.COORDINATOR)
            return Go(State.COMPLETING)
        out.say("Say 'confirm' to book, or tell me what to change.")
        return STAY

    def enter_committing(self, s: Session, out: TurnOutput) -> Step:
        scheduling = self.ports.scheduling
        try:
            if s.kind is SessionKind.UPDATE:
                assert s.case_update is not None
                case = scheduling.update_case(s.case_update)
            elif s.kind is SessionKind.RESCHEDULE:
                assert s.hold is not None
                case = scheduling.reschedule_case(s.case_id or "", s.hold.hold_id, s.request_id)
            else:
                assert s.hold is not None and s.booking_request is not None
                case = scheduling.confirm_booking(s.hold.hold_id, s.booking_request)
        except HoldExpired:
            out.say("The hold expired before the booking was committed; holding the same slot again.")
            s.hold = None
            return Go(State.HOLDING)
        except BookingError as err:
            out.say(f"The scheduling system didn't accept the booking ({err.code}): {err.message}")
            s.hold = None
            return Go(State.HOLDING)
        s.case_id, s.hold = case.case_id, None
        return Go(State.BOOKED)

    # ------------------------------------------------------------------
    # Endings
    # ------------------------------------------------------------------

    def enter_booked(self, s: Session, out: TurnOutput) -> Step:
        case = self.ports.scheduling.get_case(s.case_id or "")
        s.readiness = self.case_readiness(case)
        receipt = self.ports.readiness_handoff.hand_off(case.case_id, s.readiness)
        verb = {SessionKind.RESCHEDULE: "Rescheduled", SessionKind.UPDATE: "Updated"}.get(s.kind, "Booked")
        rows = self.case_rows(case)
        recipient = self.requester(s)
        body = "\n".join(f"{k}: {v}" for k, v in rows) + "\n\nStill needed:\n" + "\n".join(
            f"- {i.item} ({i.owner})" + (f", due {cards.day_label(i.due)} {cards.time_label(i.due)}" if i.due else "")
            + (f", dated {cards.day_label(i.valid_from)} or later" if i.valid_from else "")
            for i in s.readiness
            if i.status.value != "done"
        )
        self.draft_message(s, "surgeons_office", recipient, f"{verb}: case {case.case_id}, {cards.day_label(case.start)}", body)
        out.card(cards.OutcomeCard(title=f"{verb} {case.case_id}", rows=rows, readiness=s.readiness, drafts=s.drafts))
        facts = {"outcome": verb.lower(), "case": dict(rows), "open_readiness_items": sum(i.status.value != "done" for i in s.readiness),
                 "handoff": receipt.destination, "drafts": s.drafts}  # fmt: skip
        fallback = (
            f"{verb} {case.case_id}: {cards.day_label(case.start)}, {case.room_id}, {cards.time_label(case.start)}-{cards.time_label(case.end)}. "
            f"Readiness list handed off ({facts['open_readiness_items']} items open); confirmation drafted for {recipient.name if recipient else 'the office'}."
        )
        out.say(self.o.interpreter.phrase("summarize_outcome", facts, fallback=fallback))
        return STAY

    def enter_cancelling(self, s: Session, out: TurnOutput) -> Step:
        case = self.ports.scheduling.get_case(s.case_id or "")
        out.card(cards.AnswerCard(title=f"Cancel {case.case_id}?", rows=self.case_rows(case)))
        out.say(f"Cancel {case.case_id} ({s.cancel_reason})? Say 'confirm'." if s.cancel_reason else f"What's the reason for cancelling {case.case_id}?")
        return STAY

    def input_cancelling(self, s: Session, interp: TurnInterpretation, out: TurnOutput) -> Step:
        if interp.cancel_reason:
            s.cancel_reason = interp.cancel_reason
        if interp.intent is Intent.CONFIRM and s.cancel_reason:
            self.ports.scheduling.cancel_case(s.case_id or "", s.cancel_reason)
            return Go(State.CANCELLED)
        out.say("I need a reason before cancelling." if not s.cancel_reason else f"Cancel {s.case_id} ({s.cancel_reason})? Say 'confirm'.")
        return STAY

    def enter_cancelled(self, s: Session, out: TurnOutput) -> Step:
        case = self.ports.scheduling.get_case(s.case_id or "")
        rows = self.case_rows(case) + [("Reason", s.cancel_reason or "")]
        self.draft_message(s, "surgeons_office", self.requester(s), f"Cancelled: case {case.case_id}", "\n".join(f"{k}: {v}" for k, v in rows))
        out.card(cards.OutcomeCard(title=f"Cancelled {case.case_id}", rows=rows, drafts=s.drafts))
        out.say(f"Cancelled {case.case_id}. The time is back in the pool; notice drafted for the office.")
        return STAY

    def enter_answered(self, s: Session, out: TurnOutput) -> Step:
        out.say(s.summary or "")
        out.card(cards.AnswerCard(title=dict(s.answer).get("Answer", "Answer"), rows=[r for r in s.answer if r[0] != "Answer"], readiness=s.readiness))
        return STAY

    def release_hold(self, s: Session) -> None:
        """A request that ends or parks gives its hold back rather than letting it run out."""
        if s.hold is not None:
            try:
                self.ports.scheduling.release_hold(s.hold.hold_id)
            except BookingError:
                pass
            s.hold, s.selected_option_id = None, None

    def enter_waitlisted(self, s: Session, out: TurnOutput) -> Step:
        self.release_hold(s)
        rows = [("Request", s.request_id), ("Why", s.route_reason or "No bookable time")]
        if window := self.display(s).get(F.DATE_WINDOW):
            rows.append(("Dates wanted", window))
        out.card(cards.AnswerCard(title="Waitlisted", rows=rows + [("Drafts", d) for d in s.drafts]))
        out.say("Waitlisted. When matching time opens, the request comes back with options.")
        return STAY

    def enter_routed_out(self, s: Session, out: TurnOutput) -> Step:
        return self._hand_over(s, out, "Routed")

    def enter_handed_off(self, s: Session, out: TurnOutput) -> Step:
        return self._hand_over(s, out, "Handed off")

    def _hand_over(self, s: Session, out: TurnOutput, verb: str) -> Step:
        self.release_hold(s)
        route = s.route
        route_to = route.route_to if route else ["coordinator"]
        fields = handoff_values(s, self.display(s), route.handoff_fields if route else ["request_summary", "contact"])
        for role in route_to:
            self.draft_message(s, role, None, f"{verb}: request {s.request_id}", "\n".join(f"{k}: {v}" for k, v in fields))
        out.card(
            cards.HandoffCard(
                title=f"{verb} to {', '.join(_roles(route_to))}",
                route_to=route_to,
                action=route.action.value if route else "hand_off",
                reason=s.route_reason or "",
                policy=route.source if route else "the agent's own rule: a person takes over",
                fields=fields,
            )
        )
        out.say(f"{verb} to {', '.join(_roles(route_to))}: {s.route_reason or 'per policy'}. Nothing was booked.")
        return STAY


# ---------------------------------------------------------------------------
# Wording the code owns: fallbacks for questions, previews and handoffs
# ---------------------------------------------------------------------------

_ROLE_NAMES = {
    "anesthesiologist_in_charge": "the anesthesiologist in charge",
    "or_desk": "the OR desk",
    "surgeons_office": "the surgeon's office",
    "coordinator": "the scheduling coordinator",
    "readiness_worklist": "the readiness worklist",
    "block_owner": "the block owner",
}


def _roles(route_to: list[str]) -> list[str]:
    return [_ROLE_NAMES.get(r, r.replace("_", " ")) for r in route_to]


def question_text(issue: Issue, stated: FieldValue | None) -> str:
    label = cards.FIELD_LABELS[issue.field].lower()
    words = f" '{stated.stated}'" if stated else ""
    if issue.kind is IssueKind.AMBIGUOUS and issue.field is F.PATIENT_DOB:
        return "More than one patient matches that name. What is the patient's date of birth?"
    if issue.kind is IssueKind.AMBIGUOUS:
        return f"More than one {label} matches{words}. Which one is it?"
    if issue.kind is IssueKind.CONFLICTS_WITH_ORDER:
        return f"{issue.detail}. Which is correct?"
    if issue.kind is IssueKind.GATED:
        return f"{issue.detail}. Is there an authorization number?"
    if issue.kind is IssueKind.NOT_FOUND and issue.field is F.DIAGNOSIS:
        return "There's no surgical order on file for this patient and procedure. Can the office send it?"
    if issue.kind is IssueKind.NOT_FOUND:
        return f"I couldn't find the {label}{words}. Could you check it?"
    if issue.kind is IssueKind.INVALID:
        return f"I couldn't read the {label}{words}. Could you restate it?"
    return {
        F.SURGEON: "Which surgeon is operating?",
        F.PROCEDURE: "Which procedure is it?",
        F.DATE_WINDOW: "Which dates should I look at?",
        F.PATIENT_NAME: "What is the patient's name?",
        F.PATIENT_DOB: "What is the patient's date of birth?",
        F.LATERALITY: "Which side: left, right or bilateral?",
    }.get(issue.field, f"What is the {label}?")


def _preview(issue: Issue) -> str:
    if issue.kind is IssueKind.AMBIGUOUS and issue.field is F.PATIENT_DOB:
        return f"patient's date of birth ({issue.candidate_count} patients match the name)"
    return f"{cards.FIELD_LABELS[issue.field].lower()} ({issue.detail})"


def _preview_missing(field: BookingField) -> str:
    return {F.PATIENT_DOB: "patient's date of birth"}.get(field, cards.FIELD_LABELS[field].lower())


def handoff_values(s: Session, shown: dict[BookingField, str], names: list[str]) -> list[tuple[str, str]]:
    def stated(field: BookingField) -> str:
        if field in shown:
            return shown[field]
        fv = s.draft.get(field)
        return fv.stated if fv else "not stated"

    first_message = next((t.text for t in s.transcript if t.speaker != "agent"), "")
    contact = s.requester
    values = {
        "patient": stated(F.PATIENT_NAME) + (f", DOB {s.draft.get(F.PATIENT_DOB).stated}" if s.draft.get(F.PATIENT_DOB) else ""),
        "surgeon": stated(F.SURGEON),
        "procedure": stated(F.PROCEDURE),
        "laterality": stated(F.LATERALITY),
        "stated_urgency": s.draft.stated_urgency,
        "requested_timing": stated(F.DATE_WINDOW),
        "requested_date": stated(F.DATE_WINDOW),
        "contact": ", ".join(x for x in (contact.name, contact.phone, contact.fax) if x) if contact else "not stated",
        "question": first_message,
        "reason": s.route_reason or "",
        "request_summary": first_message,
        "case_number": s.case_id or "not stated",
        "update": first_message,
        "attempts": str(max(s.attempts.values(), default=0)),
    }
    if s.open_question:
        values |= {"field": s.open_question.field.value, "question": s.last_question or s.open_question.detail}
    return [(name.replace("_", " ").capitalize(), values.get(name, "see request")) for name in names]
