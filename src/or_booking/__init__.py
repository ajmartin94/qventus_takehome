"""AI-assisted OR case booking: a ports-and-adapters prototype.

Layers (see docs/implementation_plan.md, Section 2.1):

- `domain`: pure logic and models; no I/O, no model calls.
- `ports`: typed interfaces the core needs from the outside world.
- `adapters`: implementations of the ports (mocks and stubs today).
- `orchestrator` and `interpretation`: the conversation state machine and the
  language-model boundary; they depend on the domain and on ports only.
- `channels`: the CLI (and later a Streamlit view).
- `app`: the composition root, the only place adapters are chosen.
"""
