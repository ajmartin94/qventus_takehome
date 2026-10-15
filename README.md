# AI-assisted OR case booking

Prototype for the Qventus AI Solution Architect challenge. The agent turns OR case requests (fax, email, call, chat) into complete, compliant bookings: the language model interprets and communicates, deterministic code decides, and the coordinator confirms every commit.

- [Problem statement](docs/problem_statement.md)
- [Booking flow diagrams](docs/diagrams/booking_flow.md)
- [Implementation plan](docs/implementation_plan.md)

## Status

Built through Phase 1 of the [build order](docs/implementation_plan.md#71-phases): the skeleton (ports, composition root, audit, layering check) and the simulated hospital (Northwind fixtures and the mock scheduling system).

## Setup

Python 3.11+.

```bash
uv venv
uv pip install -e ".[dev]"
```

## Run

```bash
.venv/Scripts/or-booking ports
```

```bash
.venv/Scripts/or-booking availability
```

```bash
.venv/Scripts/or-booking schedule
```

`ports` shows which adapter backs each port. `availability` sends scenario D1's availability query (Dr. Patel, robotic knee, 112/135 minutes, week of Nov 2) to the scheduling service; its options take any other surgeon, procedure, length or dates. `schedule` prints the simulated hospital's week, rooms by day. The simulated hospital itself is described in [fixtures/README.md](fixtures/README.md).

## Test

```bash
.venv/Scripts/python -m pytest
```

The layering contracts in `pyproject.toml` run inside the test suite, and also on their own with `lint-imports`.
