"""The orchestrator: runs the conversation state machine one turn at a time (Section 6.3).

A turn:
1. load the request's session, or create one
2. interpret the message or extract the document (one model call)
3. apply the result to the draft as proposed values
4. run the machine until it reaches a state that waits: handlers call the domain and the
   ports, and values become resolved only through lookups and validation
5. build the reply: cards from state, plus at most one model-phrased line
6. save the session; every transition, model call and port call is in the audit log

States that don't wait run straight through, so one message can move a request
through several states before the agent replies.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from or_booking.domain.models import CaseDraft, Channel, SourceKind, Unsupported
from or_booking.domain.policy import Situation
from or_booking.domain.ranking import rank_options
from or_booking.domain.strategies import select_strategy
from or_booking.domain.validation import query_inputs
from or_booking.interpretation.interpreter import Interpreter
from or_booking.interpretation.schemas import Mention, OptionLine, TurnContext, TurnInterpretation
from or_booking.observability import request_context
from or_booking.orchestrator import cards
from or_booking.orchestrator.context import Go, Merge, Ports, Step, TurnOutput, TurnResult
from or_booking.orchestrator.handlers import Handlers
from or_booking.orchestrator.router import situation_for
from or_booking.orchestrator.session import Session, SessionKind, SessionRepository, TranscriptEntry
from or_booking.orchestrator.states import WAITING, State
from or_booking.orchestrator.transitions import transition
from or_booking.ports.audit_log import AuditEntry, AuditKind
from or_booking.ports.event_source import EventType, ScheduleEvent

_MAX_STEPS = 40  # a turn that moves this many times has a loop; fail loudly


class Orchestrator:
    def __init__(self, ports: Ports, interpreter: Interpreter, *, max_clarifications: int = 3, coordinator_id: str = "C-0042") -> None:
        self.ports = ports
        self.interpreter = interpreter
        self.max_clarifications = max_clarifications
        self.coordinator_id = coordinator_id
        self.repo = SessionRepository(ports.store)
        self.handlers = Handlers(self)

    # ------------------------------------------------------------------
    # Entry points
    # ------------------------------------------------------------------

    def receive_document(self, document_id: str, *, interactive: bool = True) -> TurnResult:
        """A fax, email or call transcript starts a request, or continues an open one."""
        document = self.ports.document_ingest.get_document(document_id)
        session = self._new_session(document.channel, interactive=interactive, source_document=document_id)
        self._transcript(session, "requester", f"[{document.channel.value} {document.document_id}]\n{document.text}", document.channel)
        return self._start(session, TurnOutput(incoming=document), State.INTAKE)

    def receive_message(self, text: str) -> TurnResult:
        """The coordinator types a new request."""
        session = self._new_session(Channel.CHAT, interactive=True)
        self._transcript(session, "coordinator", text, Channel.CHAT)
        return self._start(session, TurnOutput(incoming=text), State.INTAKE)

    def reply(self, request_id: str, text: str) -> TurnResult:
        """The coordinator answers a request that is waiting for input."""
        session = self._load(request_id)
        out = TurnOutput()
        self._transcript(session, "coordinator", text, Channel.CHAT)
        with request_context(session.request_id):
            if session.state not in WAITING:
                out.say(f"{session.request_id} is {session.state.value}; it isn't waiting for input.")
                return self._finish(session, out)
            interp = self.interpret(session, text)
            if interp is None:
                out.say("I couldn't interpret that. Could you say it another way?")
                return self._finish(session, out)
            situation = situation_for(interp.intent, interp.stated_urgency)
            if situation is not None:  # can't move this request; say who handles it
                route = self.handlers.policies().routing_for(situation)
                who = ", ".join(route.route_to) if route else "the coordinator"
                out.say(f"Per policy, {situation.value.replace('_', ' ')} goes to {who}; this request stays as it is.")
                self.record_decision(session, "route_noted", {"situation": situation.value})
                return self._finish(session, out)
            step = self.handlers.input(session, interp, out)
            return self._run(session, out, step)

    def process_events(self) -> list[TurnResult]:
        """Hospital and system events: each displaced case becomes a re-booking task; opened time re-offers waitlisted requests."""
        results = []
        for event in self.ports.event_source.poll():
            if event.type is EventType.TIME_OPENED:
                results += [r for w in self.repo.all() if w.state is State.WAITLISTED and (r := self._reoffer(w, event))]
            else:
                for case_id in event.case_ids:
                    session = self._new_session(Channel.CHAT, interactive=True, kind=SessionKind.RESCHEDULE, case_id=case_id, event=event)
                    results.append(self._start(session, TurnOutput(), State.EVENT_RECEIVED))
        return results

    def tick(self) -> list[TurnResult]:
        """Timers: a parked request past its reply deadline goes to a person."""
        results = []
        for session in self.repo.open():
            if session.state is State.AWAITING_REPLY and session.reply_deadline and self.ports.clock.now() >= session.reply_deadline:
                with request_context(session.request_id):
                    self.handlers.route(session, Situation.CLARIFICATION_UNANSWERED, f"No reply by {session.reply_deadline:%a %b %d %H:%M}")
                    results.append(self._run(session, TurnOutput(), Go(State.HANDED_OFF)))
        return results

    def session(self, request_id: str) -> Session:
        return self._load(request_id)

    def sessions(self) -> list[Session]:
        return self.repo.all()

    # ------------------------------------------------------------------
    # Interpretation
    # ------------------------------------------------------------------

    def interpret(self, session: Session, text: str) -> TurnInterpretation | None:
        return self.interpreter.interpret_turn(self.context(session), text)

    def context(self, session: Session) -> TurnContext:
        return TurnContext(
            state=session.state.value,
            filled={f.value: fv.stated for f, fv in session.draft.fields.items()},
            open_question=session.last_question if session.state is State.CLARIFYING else None,
            options=[OptionLine(number=r.rank, summary=cards.option_line(r)) for r in session.ranked]
            if session.state is State.PRESENTING
            else [],
        )

    def apply(self, session: Session, interp: TurnInterpretation, source: SourceKind) -> None:
        self.apply_mentions(session, interp.mentions + interp.corrections, source)
        if interp.stated_urgency != "none":
            session.draft = session.draft.model_copy(update={"stated_urgency": interp.stated_urgency})
        if interp.cancel_reason:
            session.cancel_reason = interp.cancel_reason

    def apply_mentions(self, session: Session, mentions: list[Mention], source: SourceKind) -> None:
        """Model output enters a draft only here, and only as proposed values."""
        for m in mentions:
            session.draft = session.draft.propose(m.field, m.value, source, m.evidence)

    # ------------------------------------------------------------------
    # The machine
    # ------------------------------------------------------------------

    def _start(self, session: Session, out: TurnOutput, entry: State) -> TurnResult:
        with request_context(session.request_id):
            return self._run(session, out, Go(entry))

    def _run(self, session: Session, out: TurnOutput, step: Step) -> TurnResult:
        for _ in range(_MAX_STEPS):
            if isinstance(step, Merge):
                return self._merge(session, out, step.request_id)
            if not isinstance(step, Go):
                return self._finish(session, out)
            self._move(session, step.target, out)
            step = self.handlers.enter(session, out)
        raise RuntimeError(f"{session.request_id} moved {_MAX_STEPS} times in one turn: {out.trace}")

    def _move(self, session: Session, target: State, out: TurnOutput) -> None:
        edge = transition(session.state, target)  # anything off the table is a programming error
        self.ports.audit_log.record(
            AuditEntry(
                at=self.ports.clock.now(),
                request_id=session.request_id,
                kind=AuditKind.TRANSITION,
                name=f"{edge.source.value} -> {edge.target.value}",
                detail={"label": edge.label},
            )
        )
        session.state = target
        session.path.append(target)
        out.trace.append(target)

    def _merge(self, provisional: Session, out: TurnOutput, request_id: str) -> TurnResult:
        """A reply to an open request: its values go to that request, and it resumes if it was parked."""
        target = self._load(request_id)
        source = SourceKind.DOCUMENT if provisional.source_document else SourceKind.COORDINATOR
        for field, fv in provisional.draft.fields.items():
            if target.draft.get(field) is None or not target.draft.get(field).is_resolved:
                target.draft = target.draft.propose(field, fv.value, source, fv.evidence)
        target.transcript += provisional.transcript
        self.record_decision(target, "merged", {"from": provisional.request_id, "trace": [s.value for s in out.trace]})
        merged = TurnOutput(incoming=out.incoming)
        merged.say(f"Matched to open request {target.request_id}.")
        with request_context(target.request_id):
            if target.state is State.AWAITING_REPLY:
                target.open_question = None
                return self._run(target, merged, Go(State.COLLECTING))
            merged.say(f"{target.request_id} is {target.state.value}; the new details are recorded on it.")
            return self._finish(target, merged)

    def _reoffer(self, waitlisted: Session, event: ScheduleEvent) -> TurnResult | None:
        """Opened time: if a waitlisted request now has options, offer them as a new task."""
        try:
            procedure = self.handlers.procedure(waitlisted)
            plan = select_strategy(procedure, self.handlers.surgeon(waitlisted)).plan(
                query_inputs(waitlisted.draft), self.handlers.size(waitlisted, procedure).minutes
            )
        except ValueError:
            return None
        if isinstance(plan, Unsupported):
            return None
        result = self.ports.scheduling.search_availability(plan)
        ranked = rank_options(result.options, plan.case_minutes, self.ports.clock.now().date())
        if not ranked:
            return None
        session = self._new_session(
            waitlisted.draft.channel, interactive=True, parent_request_id=waitlisted.request_id, event=event, requester=waitlisted.requester
        )
        session.draft = waitlisted.draft.model_copy(update={"request_id": session.request_id})
        session.sizing, session.availability, session.ranked = self.handlers.size(waitlisted, procedure), result, ranked
        return self._start(session, TurnOutput(), State.EVENT_RECEIVED)

    def _finish(self, session: Session, out: TurnOutput) -> TurnResult:
        reply = out.reply()
        if reply.message or reply.cards:
            text = reply.message + "".join(f"\n[{c.kind}: {c.title}]" for c in reply.cards)
            self._transcript(session, "agent", text.strip(), Channel.CHAT)
        session.updated_at = self.ports.clock.now()
        self.repo.save(session)
        return TurnResult(
            request_id=session.request_id,
            state=session.state,
            trace=out.trace,
            reply=reply,
            waiting=session.state in WAITING,
        )

    # ------------------------------------------------------------------

    def record_decision(self, session: Session, name: str, detail: dict[str, Any]) -> None:
        self.ports.audit_log.record(
            AuditEntry(at=self.ports.clock.now(), request_id=session.request_id, kind=AuditKind.DECISION, name=name, detail=detail)
        )

    def _new_session(self, channel: Channel, *, interactive: bool, **fields: Any) -> Session:
        now: datetime = self.ports.clock.now()
        request_id = self.repo.next_request_id()
        return Session(
            request_id=request_id,
            interactive=interactive,
            coordinator_id=self.coordinator_id,
            draft=CaseDraft(request_id=request_id, channel=channel),
            created_at=now,
            updated_at=now,
            **fields,
        )

    def _load(self, request_id: str) -> Session:
        session = self.repo.load(request_id)
        if session is None:
            raise KeyError(f"No request {request_id}")
        return session

    def _transcript(self, session: Session, speaker: str, text: str, channel: Channel) -> None:
        session.transcript.append(TranscriptEntry(at=self.ports.clock.now(), speaker=speaker, text=text, channel=channel.value))

