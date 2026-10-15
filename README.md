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

## Test

```bash
.venv/Scripts/python -m pytest
```

The layering contracts in `pyproject.toml` run inside the test suite, and also on their own with `lint-imports`.
