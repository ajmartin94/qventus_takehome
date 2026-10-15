# Demo transcripts

Each demo scenario in `scenarios/demo/`, run end to end and written out: the input, the conversation with its cards and state trace, what the model returned, every port call, the drafted messages and the checks that held.

Replay transcripts use the scripted model, so they are deterministic; a test fails if they drift from the code. Live transcripts are snapshots of runs with the real model reading and interpreting every turn, so their wording is the model's and varies between runs.

Regenerate with `or-booking transcripts` (add `--live d1` to refresh a live snapshot; that spends API credit).

| Scenario | Title | Ends in | Replay | Live |
|---|---|---|---|---|
| [D1](d1_faxed_request.md) | Faxed request with two patients named Maria Gomez | Booked | pass | [live run](live/d1_faxed_request.md) |
| [D2](d2_other_owners_block.md) | The coordinator wants Wednesday, which sits in other owners' unreleased blocks | Waitlisted | pass | - |
| [D3](d3_slot_taken.md) | Another coordinator takes the slot between search and pick | Booked | pass | - |
| [D4](d4_urgent.md) | "This needs a room tonight": urgent requests go to the anesthesiologist in charge and the OR desk | RoutedOut | pass | - |
| [D5](d5_clinical_question.md) | A clinical question goes to the surgeon's office, not the scheduling agent | RoutedOut | pass | - |
| [D6](d6_side_conflict.md) | The email says left knee; the surgeon's order says right | Booked | pass | - |
| [D7](d7_cardiac_stub.md) | A cardiac case selects the OR-plus-ICU-bed strategy, a stub, and routes to a person | RoutedOut | pass | - |
