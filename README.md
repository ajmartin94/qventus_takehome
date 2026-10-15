# AI-assisted OR case booking

Prototype for the Qventus AI Solution Architect challenge. The agent turns OR case requests (fax, email, call, chat) into complete, compliant bookings: the language model interprets and communicates, deterministic code decides, and the coordinator confirms every commit.

- [Problem statement](docs/problem_statement.md)
- [Booking flow diagrams](docs/diagrams/booking_flow.md)
- [Implementation plan](docs/implementation_plan.md)

## Status

Built through Phase 4 of the [build order](docs/implementation_plan.md#71-phases):

- **Phase 0, skeleton:** ports, composition root, audit, layering check.
- **Phase 1, simulated hospital:** Northwind fixtures and the mock scheduling system.
- **Phase 2, domain core** (`src/or_booking/domain/`): policy evaluation for the four rule types, qualification of the availability query and the booking request, sizing, ranking, readiness with business days, booking strategies (standard built, three stubs), request matching and the Tier 3 shadow check.
- **Phase 3, orchestrator in replay mode** (`src/or_booking/orchestrator/`, `src/or_booking/interpretation/`): the conversation state machine, with one handler per state; the transition table, which also generates the documented state diagram; sessions; policy routing; cards; versioned prompts; a scripted model for offline replay; and scenario replay from the CLI.
- **Phase 4, the real model** (`src/or_booking/adapters/llm_anthropic.py`): Claude Opus 5.5 through the Anthropic SDK, with schema-constrained structured outputs, effort set per prompt, cached system prompts, refusal and stop-reason handling, and server-side refusal fallbacks. The prompts were tuned against live runs. D1 runs end to end with the real model reading the fax.

Alternate and failure-path scenarios come next (Phase 5).

## Setup

Python 3.11+.

```bash
uv venv
uv pip install -e ".[dev]"
```

## Live model

Live runs need an Anthropic API key. Copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY` (`.env` is gitignored; a key already in your environment takes precedence). Without `--live`, everything runs offline with the scripted model.

```bash
.venv/Scripts/or-booking replay d1 --live
```

```bash
.venv/Scripts/or-booking chat --live
```

A live D1 run makes 5 model calls (about 13k input and 1.4k output tokens). In `chat --live` you can type freely, or add `--scenario d1` to start from the faxed request.

## Run

Replay scenario D1 end to end with no network: a faxed request with two patients named Maria Gomez becomes a booking.

```bash
.venv/Scripts/or-booking replay d1
```

Step through the same conversation yourself (press Enter to send each scripted coordinator turn; `/help` lists commands such as `/schedule`, `/drafts` and `/audit`):

```bash
.venv/Scripts/or-booking chat --scenario d1
```

Look at the simulated hospital directly:

```bash
.venv/Scripts/or-booking schedule
```

```bash
.venv/Scripts/or-booking availability
```

```bash
.venv/Scripts/or-booking ports
```

`schedule` prints the week, rooms by day. `availability` sends D1's availability query (Dr. Patel, robotic knee, 112/135 minutes, week of Nov 2) straight to the scheduling service. `ports` shows which adapter backs each port. The simulated hospital is described in [fixtures/README.md](fixtures/README.md); scenarios live in `scenarios/demo/`.

## Test

```bash
.venv/Scripts/python -m pytest
```

The suite runs offline. Tests that call the real model are marked `live` and run only when asked for:

```bash
OR_BOOKING_LIVE=1 .venv/Scripts/python -m pytest -m live
```

The suite includes the golden replay of every demo scenario, a flow for every transition in the state machine (a test fails if a transition has none), contract tests per port, and the layering contracts from `pyproject.toml` (also runnable on their own with `lint-imports`).
