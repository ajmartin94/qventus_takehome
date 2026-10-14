# Qventus: AI Solution Architect Tech Challenge

Take-home assessment for the **Forward Deployed AI Solutions Architect** role.

- **Received:** 2026-10-08, from Chiara Lombardi (clombardi@qventus.com)
- **Questions:** Chiara Lombardi or AJ Modi (amodi@qventus.com)
- **Panel presentation:** Fri 2026-10-16, 11:00am–12:00pm ET (10:00–11:00am CT)
- **Submit by email:** 24 hours before the panel, so **Thu 2026-10-15, 11:00am ET (10:00am CT)**
- **Suggested time:** ~4–6 hours. Don't go beyond that. They care about approach and reasoning, not production polish.

---

## Context

Qventus is building AI assistants to help hospitals streamline operations so clinicians and staff can focus on patient care. These assistants support workflows like patient admissions, operating room scheduling, and pharmacy refills.

As a **Forward Deployed Solutions Architect**, you'll need to structure modular conversational logic, apply prompt engineering, integrate with backend systems, and design for scalability.

This challenge is designed to see **how you architect and implement solutions**, not to test for UI polish. **Be explicit on where AI assistants were used.**

---

## Part 1: Pick a Workflow (Your Scenario)

Choose **one** of the following (or propose a similar workflow you think fits):

1. **Patient Admission & Bed Assignment**: Nurse admits a patient and finds a bed, with escalation if none are available.
2. **Operating Room Scheduling**: Coordinator checks availability and books an operating room.
3. **Pharmacy Refill & Escalation**: Physician assistant requests a medication refill, with escalation if approval is needed.

Make appropriate assumptions.

---

## Part 2: Core Design

- Outline the **high-level flow** for your chosen scenario (happy path + at least one alternate/failure path).
- Illustrate the flow using a **conversation modeling technique** of your choice (state machine, decision tree, or graph-based approach).
- Identify the **key intents** and **entities** your system needs to capture.

---

## Part 3: Prototype Implementation

Build a **lightweight prototype** in any framework or stack you prefer (LangChain, Rasa, Dialogflow, Amazon Lex, Python, etc.). Picking something you are familiar with is preferred for detailed discussion (only if you believe it is the right choice). You can pick any modality (chat, voice). The prototype should demonstrate how your assistant can:

- Recognize and route user intent(s)
- Capture the necessary information (entities/slots)
- Interact with a backend system (this can be a stub or simulated API call, e.g., returning `{available: true, bed_id: 103}`)

We're especially interested in how you **structure** the solution (e.g., modular prompts, separation of logic and integrations).

**Optional / Bonus:** Show how you would handle multi-turn clarifications, or extend the design with retrieval-augmented generation (RAG), embeddings, or vector search for policies/guidelines.

---

## Part 4: Optimization & Scalability (Written)

In 1–2 pages (bullets are fine), describe how you would:

- Monitor and improve performance over time (logging, testing, evaluation loops)
- Scale the architecture to support multiple workflows
- Leverage RAG/vector databases for external knowledge
- Ensure robustness against ambiguous or incomplete inputs

---

## Submission Guidelines

**Deliverables:**

- Short **flow diagram or outline** (image, PDF, or text)
- **Prototype code** (GitHub repo, zip, or Colab notebook)
- **Written notes** (1–2 pages) on optimization & scalability

---

## Evaluation Criteria

1. **Architectural Thinking**: Is the system modular, extensible, and practical?
2. **Prompt Engineering & Technical Depth**: Are prompts and logic thoughtfully designed?
3. **Implementation**: Does the prototype demonstrate core functionality?
4. **Conversation Modeling**: Is the flow structured clearly using state machines, decision trees, or graphs?
5. **Scalability & Optimization**: Are strategies for improvement realistic?
6. **Clarity**: Is documentation concise and easy to follow?
