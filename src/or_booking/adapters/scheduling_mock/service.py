"""Mock OR scheduling system over fixtures/scheduling.

Plays the hospital's scheduling system of record well enough to be believable, and
enforces what that system would: block ownership and release, schedule close, room
capability, turnover, shared equipment, privileges, holds with a time limit and
idempotent confirms. It answers with options or the port's typed errors; the agent
never checks any of these rules itself.

Availability works per room and day: prime time is split into ownership segments
(blocks, with early releases cut out, and open time between them), booked cases and
active holds are subtracted with their turnover, and each remaining free stretch inside
one segment is an option if the typical case length plus turnover fits.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Literal

from or_booking.adapters.fixture_data import EhrRecords, FixtureError, load_ehr
from or_booking.adapters.scheduling_mock.records import (
    WEEKDAYS,
    BlockTemplate,
    FixtureCase,
    RoomRecord,
    SchedulingRecords,
    load_scheduling,
)
from or_booking.domain.errors import (
    BlockNotReleased,
    HoldExpired,
    MissingRequiredField,
    NotFound,
    NotPrivileged,
    PastCutoff,
    RequestRejected,
    ResourceConflict,
    SlotTaken,
)
from or_booking.domain.models import (
    AvailabilityQuery,
    AvailabilityResult,
    BookedCase,
    BookingRequest,
    CaseStatus,
    CaseUpdate,
    DateWindow,
    Hold,
    Ownership,
    Procedure,
    SlotOption,
    Surgeon,
)
from or_booking.ports.clock import Clock
from or_booking.ports.scheduling import RoomDay, ScheduledCase, ScheduleSegment, ScheduleView

Span = tuple[datetime, datetime]


def _at(d: date, t: time) -> datetime:
    return datetime.combine(d, t)


def _mins(n: int) -> timedelta:
    return timedelta(minutes=n)


def _overlaps(spans: list[Span], start: datetime, end: datetime) -> bool:
    return any(s < end and start < e for s, e in spans)


@dataclass(frozen=True)
class _Segment:
    start: datetime
    end: datetime
    block: BlockTemplate | None
    owner_name: str | None
    released_at: datetime | None
    releases_at: datetime | None  # the block's automatic release time

    def ownership_for(self, surgeon_id: str) -> Ownership:
        if self.block is None:
            return Ownership.OPEN
        if self.released_at is not None:
            return Ownership.RELEASED
        return Ownership.OWN_BLOCK if self.block.owner == surgeon_id else Ownership.HELD_BY_OTHER


@dataclass(frozen=True)
class _Issued:
    """An option the service has offered, with the query context it was computed for."""

    option: SlotOption
    surgeon_id: str
    procedure_id: str
    minutes: int


@dataclass
class _HoldState:
    hold: Hold
    surgeon_id: str
    procedure_id: str
    assets: list[str]
    status: Literal["active", "released", "consumed", "expired"] = "active"


class MockSchedulingService:
    def __init__(self, records: SchedulingRecords, ehr: EhrRecords, clock: Clock) -> None:
        _validate(records, ehr)
        self._s = records
        self._ehr = ehr
        self._clock = clock
        self._cases: dict[str, BookedCase] = {c.case_id: _to_booked(c) for c in records.booked.cases}
        self._holds: dict[str, _HoldState] = {}
        self._issued: dict[str, _Issued] = {}
        self._by_key: dict[str, str] = {}
        self._next_case = 5001
        self._next_hold = 1

    @classmethod
    def from_fixtures(cls, fixtures_dir: Path, clock: Clock) -> MockSchedulingService:
        return cls(load_scheduling(fixtures_dir), load_ehr(fixtures_dir), clock)

    # ------------------------------------------------------------------
    # Port: availability
    # ------------------------------------------------------------------

    def search_availability(self, query: AvailabilityQuery) -> AvailabilityResult:
        surgeon, procedure = self._surgeon(query.surgeon_id), self._procedure(query.procedure_id)
        if procedure.id not in surgeon.privileges:
            raise NotPrivileged(surgeon.id, procedure.id)
        rooms = [r for r in self._s.rooms.values() if set(procedure.room_capabilities) <= set(r.capabilities)]
        today = self._clock.now().date()
        options: list[SlotOption] = []
        held: list[SlotOption] = []
        closed: list[date] = []

        for d in query.window.days():
            if d < today or not self._operating(d) or WEEKDAYS[d.weekday()] in query.preferences.avoid_weekdays:
                continue
            if self._closed(d):
                closed.append(d)
                continue
            for room in rooms:
                for option in self._options(room, d, surgeon.id, procedure, query.case_minutes.typical):
                    self._issued[option.option_id] = _Issued(option, surgeon.id, procedure.id, query.case_minutes.typical)
                    (options if option.bookable else held).append(option)

        preferred = query.preferences.preferred_room_ids
        options.sort(key=lambda o: (o.room_id not in preferred, o.start, o.room_id))
        held.sort(key=lambda o: (o.start, o.room_id))
        return AvailabilityResult(query=query, options=options, held=held, closed_dates=closed)

    # ------------------------------------------------------------------
    # Port: holds and bookings
    # ------------------------------------------------------------------

    def place_hold(self, option_id: str, request_id: str) -> Hold:
        issued = self._issued.get(option_id)
        if issued is None:
            raise NotFound("option", option_id)
        option, d = issued.option, issued.option.date
        if self._closed(d):
            raise PastCutoff(d, self._close_time(d))
        for state in self._active_holds():  # one hold per request: a new pick replaces the old one
            if state.hold.request_id == request_id:
                state.status = "released"

        segment = self._segment_at(option.room_id, option.start)
        if segment.ownership_for(issued.surgeon_id) is Ownership.HELD_BY_OTHER:
            assert segment.block is not None
            raise BlockNotReleased(option_id, segment.block.owner, segment.owner_name or "", segment.releases_at)

        room = self._s.rooms[option.room_id]
        start = option.start
        end = start + _mins(issued.minutes)
        if _overlaps(self._occupied(room.id, d), start, end + _mins(room.turnover_minutes)):
            raise SlotTaken(option_id, "Another case or hold now covers that time.")
        procedure = self._procedure(issued.procedure_id)
        assets = self._assets_for(procedure, room.id, start, end + _mins(room.turnover_minutes))
        if assets is None:
            raise ResourceConflict(" and ".join(procedure.shared_assets), "No unit is free for that time.")

        hold = Hold(
            hold_id=f"H-{self._next_hold:04d}",
            option_id=option_id,
            request_id=request_id,
            room_id=room.id,
            start=start,
            end=end,
            expires_at=self._clock.now() + _mins(self._s.location.hold_minutes),
        )
        self._next_hold += 1
        self._holds[hold.hold_id] = _HoldState(hold, issued.surgeon_id, procedure.id, assets)
        return hold

    def release_hold(self, hold_id: str) -> None:
        state = self._holds.get(hold_id)
        if state is None:
            raise NotFound("hold", hold_id)
        if state.status == "active":
            state.status = "released"

    def confirm_booking(self, hold_id: str, request: BookingRequest) -> BookedCase:
        if request.idempotency_key in self._by_key:  # a retry: same case, never a second one
            return self._cases[self._by_key[request.idempotency_key]]
        state = self._live_hold(hold_id)
        hold = state.hold
        if request.option_id != hold.option_id:
            raise RequestRejected(f"Hold {hold_id} is for {hold.option_id}, not {request.option_id}.")
        if (request.surgeon_id, request.procedure_id) != (state.surgeon_id, state.procedure_id):
            raise RequestRejected(f"Hold {hold_id} was placed for a different surgeon or procedure.")

        surgeon, procedure = self._surgeon(request.surgeon_id), self._procedure(request.procedure_id)
        if procedure.id not in surgeon.privileges:
            raise NotPrivileged(surgeon.id, procedure.id)
        missing = []
        if not request.patient_mrn:
            missing.append("patient_mrn")
        if procedure.laterality == "required" and request.laterality is None:
            missing.append("laterality")
        if missing:
            raise MissingRequiredField(missing)
        if request.patient_mrn not in self._ehr.patients:
            raise NotFound("patient", request.patient_mrn)
        d = hold.start.date()
        if self._closed(d):
            raise PastCutoff(d, self._close_time(d))

        # The booked length may differ from the held one (a duration override): re-check that span.
        room = self._s.rooms[hold.room_id]
        end = hold.start + _mins(request.scheduled_minutes)
        span_end = end + _mins(room.turnover_minutes)
        if _overlaps(self._occupied(room.id, d, ignore_hold=hold_id), hold.start, span_end):
            raise ResourceConflict(room.id, f"A {request.scheduled_minutes}-minute case would overlap the next case.")
        assets = self._assets_for(procedure, room.id, hold.start, span_end, ignore_hold=hold_id)
        if assets is None:
            raise ResourceConflict(" and ".join(procedure.shared_assets), "Not free for the booked length.")

        case = BookedCase(
            case_id=f"C-{self._next_case}",
            status=CaseStatus.BOOKED,
            surgeon_id=surgeon.id,
            procedure_id=procedure.id,
            room_id=room.id,
            start=hold.start,
            end=end,
            patient_mrn=request.patient_mrn,
            laterality=request.laterality,
            diagnosis_code=request.diagnosis_code,
            anesthesia_type=request.anesthesia_type,
            patient_class=request.patient_class,
            implants=request.implants,
            assets=assets,
            requested_by=request.requested_by,
            booked_by=request.booked_by,
            idempotency_key=request.idempotency_key,
        )
        self._next_case += 1
        self._cases[case.case_id] = case
        self._by_key[request.idempotency_key] = case.case_id
        state.status = "consumed"
        return case

    def get_case(self, case_id: str) -> BookedCase:
        if case_id not in self._cases:
            raise NotFound("case", case_id)
        return self._cases[case_id]

    def find_cases(self, *, patient_mrn: str | None = None, surgeon_id: str | None = None) -> list[BookedCase]:
        return sorted(
            (
                c
                for c in self._cases.values()
                if (patient_mrn is None or c.patient_mrn == patient_mrn)
                and (surgeon_id is None or c.surgeon_id == surgeon_id)
            ),
            key=lambda c: (c.start, c.room_id),
        )

    def cancel_case(self, case_id: str, reason: str) -> BookedCase:
        case = self.get_case(case_id)
        if case.status is not CaseStatus.CANCELLED:
            case = case.model_copy(update={"status": CaseStatus.CANCELLED, "cancel_reason": reason})
            self._cases[case_id] = case
        return case

    def reschedule_case(self, case_id: str, hold_id: str, idempotency_key: str) -> BookedCase:
        if idempotency_key in self._by_key:
            return self._cases[self._by_key[idempotency_key]]
        case = self.get_case(case_id)
        state = self._live_hold(hold_id)
        hold = state.hold
        if (state.surgeon_id, state.procedure_id) != (case.surgeon_id, case.procedure_id):
            raise RequestRejected(f"Hold {hold_id} was placed for a different surgeon or procedure than {case_id}.")
        room = self._s.rooms[hold.room_id]
        end = hold.start + (case.end - case.start)
        span_end = end + _mins(room.turnover_minutes)
        if _overlaps(self._occupied(room.id, hold.start.date(), ignore_hold=hold_id, ignore_case=case_id), hold.start, span_end):
            raise ResourceConflict(room.id, "The case's length doesn't fit at the held time.")
        procedure = self._procedure(case.procedure_id)
        assets = self._assets_for(procedure, room.id, hold.start, span_end, ignore_hold=hold_id, ignore_case=case_id)
        if assets is None:
            raise ResourceConflict(" and ".join(procedure.shared_assets), "Not free at the held time.")
        moved = case.model_copy(update={"room_id": room.id, "start": hold.start, "end": end, "assets": assets})
        self._cases[case_id] = moved
        self._by_key[idempotency_key] = case_id
        state.status = "consumed"
        return moved

    def update_case(self, update: CaseUpdate) -> BookedCase:
        if update.idempotency_key in self._by_key:
            return self._cases[self._by_key[update.idempotency_key]]
        case = self.get_case(update.case_id)
        if self._procedure(case.procedure_id).laterality == "required" and update.laterality is None:
            raise MissingRequiredField(["laterality"])
        changed = case.model_copy(
            update={
                "laterality": update.laterality,
                "diagnosis_code": update.diagnosis_code,
                "anesthesia_type": update.anesthesia_type,
                "patient_class": update.patient_class,
                "implants": update.implants,
            }
        )
        self._cases[case.case_id] = changed
        self._by_key[update.idempotency_key] = case.case_id
        return changed

    # ------------------------------------------------------------------
    # Port: schedule view
    # ------------------------------------------------------------------

    def get_schedule(self, window: DateWindow) -> ScheduleView:
        filled = self._s.booked.schedule_filled_through
        room_days = []
        for d in window.days():
            if not self._operating(d):
                continue
            for room in self._s.rooms.values():
                segments = [
                    ScheduleSegment(
                        start=s.start,
                        end=s.end,
                        state="open" if s.block is None else ("released" if s.released_at else "held"),
                        owner_id=s.block.owner if s.block else None,
                        owner_name=s.owner_name,
                        releases_at=s.releases_at if s.block and not s.released_at else None,
                        released_at=s.released_at,
                        filler=bool(s.block and s.block.filler),
                    )
                    for s in self._segments(room.id, d)
                ]
                cases = [
                    ScheduledCase(
                        case_id=c.case_id,
                        status=c.status,
                        surgeon_id=c.surgeon_id,
                        procedure_id=c.procedure_id,
                        patient_mrn=c.patient_mrn,
                        start=c.start,
                        end=c.end,
                    )
                    for c in self.find_cases()
                    if c.room_id == room.id and c.date == d and c.status is CaseStatus.BOOKED
                ]
                room_days.append(
                    RoomDay(
                        room_id=room.id,
                        date=d,
                        schedule_closed=self._closed(d),
                        fully_booked=bool(filled and d <= filled),
                        segments=segments,
                        cases=cases,
                    )
                )
        return ScheduleView(window=window, room_days=room_days)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _surgeon(self, surgeon_id: str) -> Surgeon:
        if surgeon_id not in self._ehr.surgeons:
            raise NotFound("surgeon", surgeon_id)
        return self._ehr.surgeons[surgeon_id]

    def _procedure(self, procedure_id: str) -> Procedure:
        if procedure_id not in self._ehr.procedures:
            raise NotFound("procedure", procedure_id)
        return self._ehr.procedures[procedure_id]

    def _owner_name(self, owner: str) -> str:
        if owner in self._ehr.surgeons:
            return self._ehr.surgeons[owner].display_name
        return self._s.blocks.groups[owner]

    def _operating(self, d: date) -> bool:
        return WEEKDAYS[d.weekday()] in self._s.location.operating_days

    def _prime(self, d: date) -> Span:
        prime = self._s.location.prime_time
        return _at(d, prime.start), _at(d, prime.end)

    def _close_time(self, d: date) -> datetime:
        rule = self._s.location.schedule_close
        day, steps = d, 0
        while steps < rule.business_days_before:
            day -= timedelta(days=1)
            steps += day.weekday() < 5
        return _at(day, rule.at)

    def _closed(self, d: date) -> bool:
        return self._clock.now() >= self._close_time(d)

    def _segments(self, room_id: str, d: date) -> list[_Segment]:
        """Prime time split by owner: blocks (with early releases cut out) and open time between them."""
        now = self._clock.now()
        pieces: list[_Segment] = []
        for block in self._s.blocks.blocks:
            if block.room != room_id or block.weekday != WEEKDAYS[d.weekday()]:
                continue
            name = self._owner_name(block.owner)
            auto = _at(d - timedelta(days=block.release.days_before), block.release.at)
            auto_released = auto if now >= auto else None
            cursor, block_end = _at(d, block.start), _at(d, block.end)
            early = sorted(
                (e for e in self._s.blocks.early_releases if e.block == block.id and e.date == d and e.released_at <= now),
                key=lambda e: e.start,
            )
            for e in early:
                if _at(d, e.start) > cursor:
                    pieces.append(_Segment(cursor, _at(d, e.start), block, name, auto_released, auto))
                pieces.append(_Segment(_at(d, e.start), _at(d, e.end), block, name, e.released_at, auto))
                cursor = _at(d, e.end)
            if cursor < block_end:
                pieces.append(_Segment(cursor, block_end, block, name, auto_released, auto))

        prime_start, prime_end = self._prime(d)
        segments: list[_Segment] = []
        cursor = prime_start
        for piece in sorted(pieces, key=lambda p: p.start):
            if piece.start > cursor:
                segments.append(_Segment(cursor, piece.start, None, None, None, None))
            segments.append(piece)
            cursor = max(cursor, piece.end)
        if cursor < prime_end:
            segments.append(_Segment(cursor, prime_end, None, None, None, None))
        return segments

    def _segment_at(self, room_id: str, at: datetime) -> _Segment:
        return next(s for s in self._segments(room_id, at.date()) if s.start <= at < s.end)

    def _active_holds(self) -> list[_HoldState]:
        now = self._clock.now()
        return [h for h in self._holds.values() if h.status == "active" and now < h.hold.expires_at]

    def _live_hold(self, hold_id: str) -> _HoldState:
        state = self._holds.get(hold_id)
        if state is None:
            raise NotFound("hold", hold_id)
        if state.status in ("released", "consumed"):
            raise RequestRejected(f"Hold {hold_id} was already {state.status}.")
        if state.status == "expired" or self._clock.now() >= state.hold.expires_at:
            state.status = "expired"
            raise HoldExpired(hold_id, state.hold.expires_at)
        return state

    def _turnover(self, room_id: str) -> timedelta:
        return _mins(self._s.rooms[room_id].turnover_minutes)

    def _occupied(self, room_id: str, d: date, *, ignore_hold: str | None = None, ignore_case: str | None = None) -> list[Span]:
        filled = self._s.booked.schedule_filled_through
        if filled and d <= filled:
            return [self._prime(d)]
        turnover = self._turnover(room_id)
        busy = [(s.start, s.end) for s in self._segments(room_id, d) if s.block and s.block.filler]
        busy += [
            (c.start, c.end + turnover)
            for c in self._cases.values()
            if c.room_id == room_id and c.date == d and c.status is CaseStatus.BOOKED and c.case_id != ignore_case
        ]
        busy += [
            (h.hold.start, h.hold.end + turnover)
            for h in self._active_holds()
            if h.hold.room_id == room_id and h.hold.start.date() == d and h.hold.hold_id != ignore_hold
        ]
        return busy

    def _free(self, room_id: str, d: date) -> list[Span]:
        prime_start, prime_end = self._prime(d)
        free: list[Span] = []
        cursor = prime_start
        for s, e in sorted(self._occupied(room_id, d)):
            if s > cursor:
                free.append((cursor, min(s, prime_end)))
            cursor = max(cursor, e)
        if cursor < prime_end:
            free.append((cursor, prime_end))
        return [(s, e) for s, e in free if e > s]

    def _options(self, room: RoomRecord, d: date, surgeon_id: str, procedure: Procedure, minutes: int) -> Iterator[SlotOption]:
        need = _mins(minutes + room.turnover_minutes)
        segments = self._segments(room.id, d)
        for free_start, free_end in self._free(room.id, d):
            for seg in segments:
                start, end = max(free_start, seg.start), min(free_end, seg.end)
                if end - start < need or self._assets_for(procedure, room.id, start, start + need) is None:
                    continue
                ownership = seg.ownership_for(surgeon_id)
                yield SlotOption(
                    option_id=f"OPT-{room.id.replace('-', '')}-{start:%Y%m%d-%H%M}",
                    room_id=room.id,
                    start=start,
                    end=end,
                    turnover_minutes=room.turnover_minutes,
                    ownership=ownership,
                    block_owner_id=seg.block.owner if seg.block else None,
                    block_owner_name=seg.owner_name,
                    released_at=seg.released_at,
                    releases_at=seg.releases_at if ownership is Ownership.HELD_BY_OTHER else None,
                )

    def _assets_for(
        self,
        procedure: Procedure,
        room_id: str,
        start: datetime,
        end: datetime,
        *,
        ignore_hold: str | None = None,
        ignore_case: str | None = None,
    ) -> list[str] | None:
        """One free unit of each shared asset type the procedure needs, or None if any type has none free."""
        chosen = []
        for asset_type in procedure.shared_assets:
            units = [a.id for a in self._s.assets.values() if a.type == asset_type and room_id in a.rooms]
            free = next((u for u in units if not self._asset_busy(u, start, end, ignore_hold, ignore_case)), None)
            if free is None:
                return None
            chosen.append(free)
        return chosen

    def _asset_busy(self, asset_id: str, start: datetime, end: datetime, ignore_hold: str | None, ignore_case: str | None) -> bool:
        spans = [
            (c.start, c.end + self._turnover(c.room_id))
            for c in self._cases.values()
            if asset_id in c.assets and c.status is CaseStatus.BOOKED and c.case_id != ignore_case
        ]
        spans += [
            (h.hold.start, h.hold.end + self._turnover(h.hold.room_id))
            for h in self._active_holds()
            if asset_id in h.assets and h.hold.hold_id != ignore_hold
        ]
        return _overlaps(spans, start, end)


def _to_booked(c: FixtureCase) -> BookedCase:
    return BookedCase(
        case_id=c.case_id,
        status=CaseStatus.BOOKED,
        surgeon_id=c.surgeon_id,
        procedure_id=c.procedure_id,
        room_id=c.room_id,
        start=_at(c.date, c.start),
        end=_at(c.date, c.end),
        patient_mrn=c.patient_mrn,
        laterality=c.laterality,
        diagnosis_code=c.diagnosis_code,
        anesthesia_type=c.anesthesia_type,
        patient_class=c.patient_class,
        implants=c.implants,
        assets=c.assets,
    )


def _validate(s: SchedulingRecords, ehr: EhrRecords) -> None:
    """The scheduling system's own guarantees, checked on the fixture data at startup."""
    problems: list[str] = []
    prime = s.location.prime_time
    owners = set(ehr.surgeons) | set(s.blocks.groups)
    blocks = {b.id: b for b in s.blocks.blocks}

    for b in s.blocks.blocks:
        if b.room not in s.rooms:
            problems.append(f"block {b.id}: unknown room {b.room}")
        if b.owner not in owners:
            problems.append(f"block {b.id}: unknown owner {b.owner}")
        if not prime.start <= b.start < b.end <= prime.end:
            problems.append(f"block {b.id}: outside prime time")
    for i, a in enumerate(s.blocks.blocks):
        for b in s.blocks.blocks[i + 1 :]:
            if (a.room, a.weekday) == (b.room, b.weekday) and a.start < b.end and b.start < a.end:
                problems.append(f"blocks {a.id} and {b.id} overlap")
    for e in s.blocks.early_releases:
        block = blocks.get(e.block)
        if block is None:
            problems.append(f"early release of unknown block {e.block}")
        elif WEEKDAYS[e.date.weekday()] != block.weekday or not block.start <= e.start < e.end <= block.end:
            problems.append(f"early release of {e.block} on {e.date} is outside the block")

    spans: dict[tuple[str, date], list[tuple[datetime, datetime, str]]] = {}
    asset_spans: dict[str, list[tuple[datetime, datetime, str]]] = {}
    for c in s.booked.cases:
        room = s.rooms.get(c.room_id)
        procedure = ehr.procedures.get(c.procedure_id)
        surgeon = ehr.surgeons.get(c.surgeon_id)
        if room is None or procedure is None or surgeon is None:
            problems.append(f"case {c.case_id}: unknown room, procedure or surgeon")
            continue
        if c.procedure_id not in surgeon.privileges:
            problems.append(f"case {c.case_id}: {c.surgeon_id} not privileged for {c.procedure_id}")
        if not set(procedure.room_capabilities) <= set(room.capabilities):
            problems.append(f"case {c.case_id}: {c.room_id} can't host {c.procedure_id}")
        if c.patient_mrn and c.patient_mrn not in ehr.patients:
            problems.append(f"case {c.case_id}: unknown patient {c.patient_mrn}")
        asset_types = sorted(s.assets[a].type for a in c.assets if a in s.assets)
        if len(asset_types) != len(c.assets) or asset_types != sorted(procedure.shared_assets):
            problems.append(f"case {c.case_id}: assets {c.assets} don't match {procedure.shared_assets}")
        if any(c.room_id not in s.assets[a].rooms for a in c.assets if a in s.assets):
            problems.append(f"case {c.case_id}: an asset can't be used in {c.room_id}")
        start, end = _at(c.date, c.start), _at(c.date, c.end) + _mins(room.turnover_minutes)
        spans.setdefault((c.room_id, c.date), []).append((start, end, c.case_id))
        for a in c.assets:
            asset_spans.setdefault(a, []).append((start, end, c.case_id))
    for group in [*spans.values(), *asset_spans.values()]:
        group.sort()
        for (_, end_a, id_a), (start_b, _, id_b) in zip(group, group[1:]):
            if start_b < end_a:
                problems.append(f"cases {id_a} and {id_b} overlap (including turnover)")
    if problems:
        raise FixtureError("scheduling fixtures are inconsistent:\n  " + "\n  ".join(problems))
