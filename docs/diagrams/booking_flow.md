# Booking Flow

Five views of the same system:

1. **Intake and routing:** every kind of input and where it goes.
2. **Booking core:** the shared steps every schedule change runs through.
3. **Conversation state machine:** the states a request moves through and what moves it.
4. **Sequence, new request:** who calls whom when a faxed request becomes a booking.
5. **Sequence, bumped case:** who calls whom when a booked case is displaced and re-booked.

Inputs fall into five groups (see the [problem statement](../problem_statement.md#4-what-comes-in)): new cases, requests about an existing case, hospital or system events, continuations of an open request, and requests that route straight to a human.

**Color legend:** purple = language model (interprets, communicates) · blue = deterministic rules (decide) · green = scheduling service and lookups (act) · orange = human decision · gray dashed = waiting, downstream or not yet supported · dark blue = entry into the booking core.

Where a diagram routes something to a person (the AIC and OR desk for urgent requests, the surgeon's office for clinical questions, the block owner for a release request), that destination is the simulated hospital's **default policy**, not a fixed rule of the agent. The only fixed rules are the flow's own: every commit passes through confirmation and a commit-time re-check, model output enters a case only through lookup and validation, and every step is recorded.

## 1. Intake and routing

Requests from people and events from the hospital or system enter separately. Anything that changes the schedule goes to the booking core through one of its entries. Everything else is answered read-only or routed to a human.

```mermaid
flowchart LR
    REQ(["Request from a person<br/>fax · email · call · portal · chat"]):::input
    EVT(["Event from the<br/>hospital or system"]):::input
    EXTRACT["Extract intent<br/>and fields"]:::llm
    MATCH{"Matches an open draft<br/>or a booked case?"}:::logic
    INTENT{"What is it?"}:::logic
    CASEQ{"What about<br/>the case?"}:::logic
    EVTYPE{"Event type?"}:::logic
    TASKS["One re-booking task<br/>per displaced case"]:::logic

    C_REPLY[["Core: late reply<br/>or duplicate"]]:::core
    C_NEW[["Core: new case"]]:::core
    C_EXIST[["Core: existing case"]]:::core
    C_DISP[["Core: displaced case"]]:::core
    C_WL[["Core: waitlist match"]]:::core

    AVAIL(["Show open time<br/>read-only"]):::svc
    ESC(["Escalate to AIC / OR desk<br/>no booking"]):::human
    DECLINE(["Decline and route<br/>clinical question"]):::human
    STATUS(["Answer status and<br/>open items, read-only"]):::svc
    CANCEL(["Capture reason, confirm, release slot<br/>emits a time-opened event"]):::logic
    FOLLOW(["Readiness follow-up<br/>downstream"]):::out

    REQ --> EXTRACT --> MATCH
    MATCH -- "open draft" --> C_REPLY
    MATCH -- "no match" --> INTENT
    MATCH -- "booked case" --> CASEQ
    INTENT -- "new elective case" --> C_NEW
    INTENT -- "availability only" --> AVAIL
    INTENT -- "urgent / add-on" --> ESC
    INTENT -- "clinical" --> DECLINE
    CASEQ -- "modify / reschedule" --> C_EXIST
    CASEQ -- "status" --> STATUS
    CASEQ -- "cancel" --> CANCEL
    CASEQ -- "readiness update" --> FOLLOW
    EVT --> EVTYPE
    EVTYPE -- "bump / room down /<br/>surgeon out" --> TASKS --> C_DISP
    EVTYPE -- "time opened" --> C_WL

    classDef input fill:#f1f5f9,stroke:#475569,color:#0f172a
    classDef llm fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef logic fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef svc fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef human fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef out fill:#f8fafc,stroke:#94a3b8,color:#475569,stroke-dasharray: 4 3
    classDef core fill:#1e3a8a,stroke:#1e3a8a,color:#ffffff
```

## 2. Booking core

All four entries converge on the same validation, search, confirmation and commit steps. New cases enter through lookups. Existing and displaced cases enter through an impact check that works out what the change breaks, and skip intake because the case is already known.

```mermaid
flowchart TD
    IN_NEW[["New case"]]:::core
    IN_REPLY[["Late reply or duplicate"]]:::core
    IN_EXIST[["Existing or displaced case"]]:::core
    IN_WL[["Waitlist match"]]:::core

    RESOLVE["Resolve patient, surgeon, procedure<br/>lookups only"]:::svc
    MERGE["Merge into the open draft"]:::logic
    LOAD["Load the booked case"]:::svc
    IMPACT["Work out what the change affects<br/>auth dates · H&P window · loaner tray · PAT"]:::logic
    MATCHWL["Match waitlisted cases<br/>to the opened time"]:::logic

    VALIDATE{"Complete and valid?"}:::logic
    CLARIFY["Ask for exactly what is<br/>missing or conflicting"]:::llm
    PARKED(["Draft parked, waiting for reply<br/>resumes as a late reply"]):::out
    HANDOFF(["Hand off to coordinator"]):::human
    PROFILE{"Service-line profile"}:::logic
    STUB(["Not supported yet<br/>route to human"]):::out
    SIZE["Size case<br/>surgeon P50 / P80 + room turnover"]:::logic
    SEARCH["Search own block,<br/>released and open time"]:::svc
    OPTIONS["Rank options and<br/>explain trade-offs"]:::llm
    PICK{"Coordinator decides"}:::human
    WAITLIST(["Waitlist, re-offered when time opens,<br/>or draft a release request to the owner"]):::llm
    CONFIRM["Confirmation card<br/>shows what changes"]:::logic
    COMMIT["Hold, re-check, commit<br/>with idempotency key"]:::svc
    DONE(["Booked or updated: case number,<br/>readiness list, draft notifications"]):::logic
    FOLLOW(["Readiness follow-up<br/>downstream"]):::out

    %% Forward path first, so the layout reads top to bottom; loop-backs last
    IN_NEW --> RESOLVE --> VALIDATE
    IN_REPLY --> MERGE --> VALIDATE
    IN_EXIST --> LOAD --> IMPACT --> VALIDATE
    IN_WL --> MATCHWL --> OPTIONS
    VALIDATE -- "valid, needs slot" --> PROFILE
    PROFILE -- "standard" --> SIZE --> SEARCH --> OPTIONS --> PICK
    PICK -- "option chosen" --> CONFIRM
    CONFIRM -- "confirmed" --> COMMIT
    COMMIT -- "success" --> DONE
    DONE -.-> FOLLOW
    PICK -- "other owner's block or no fit" --> WAITLIST
    PROFILE -- "cardiac / tandem / emergency" --> STUB
    VALIDATE -- "valid, keeps slot" --> CONFIRM
    VALIDATE -- "gaps" --> CLARIFY
    CLARIFY -- "answered in chat" --> RESOLVE
    CLARIFY -. "asked by fax / email" .-> PARKED
    CLARIFY -. "3 failed attempts" .-> HANDOFF
    VALIDATE -- "hard rule fails" --> HANDOFF
    CONFIRM -- "correction" --> VALIDATE
    COMMIT -- "slot taken" --> SEARCH

    classDef llm fill:#ede9fe,stroke:#7c3aed,color:#2e1065
    classDef logic fill:#dbeafe,stroke:#2563eb,color:#172554
    classDef svc fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef human fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef out fill:#f8fafc,stroke:#94a3b8,color:#475569,stroke-dasharray: 4 3
    classDef core fill:#1e3a8a,stroke:#1e3a8a,color:#ffffff
```

## 3. Conversation state machine

Each request or re-booking task is one instance of this machine. Requests from people and events from the system enter at different points but share the same core states. `AwaitingReply` lets a request survive across channels and hours. `RoutedOut` covers escalation to the AIC or OR desk, declining clinical questions, and sending readiness updates downstream.

```mermaid
stateDiagram-v2
    direction TB
    [*] --> Intake: request from a person
    [*] --> EventReceived: system event
    Intake --> Matching: parsed
    Matching --> Collecting: new case or reply
    Matching --> CaseLoaded: modify or reschedule
    Matching --> Cancelling: cancel
    Matching --> Answered: status or availability
    Matching --> RoutedOut: urgent, clinical, readiness
    EventReceived --> CaseLoaded: case displaced
    EventReceived --> Presenting: time opened
    CaseLoaded --> Collecting: impact assessed
    Collecting --> Clarifying: gap or conflict
    Clarifying --> Collecting: answered
    Clarifying --> AwaitingReply: asked by fax or email
    AwaitingReply --> Collecting: reply arrives
    AwaitingReply --> HandedOff: no reply by deadline
    Clarifying --> HandedOff: 3 failed attempts
    Collecting --> HandedOff: hard rule fails
    Collecting --> Searching: needs a slot
    Collecting --> Confirming: keeps current slot
    Searching --> Presenting: options found
    Searching --> Waitlisted: no valid option
    Presenting --> Waitlisted: other owner's block
    Presenting --> Confirming: option selected
    Confirming --> Collecting: correction
    Confirming --> Committing: confirmed
    Committing --> Searching: slot taken
    Committing --> Booked: committed
    Cancelling --> Cancelled: confirmed

    classDef human fill:#ffedd5,stroke:#ea580c,color:#431407
    classDef done fill:#dcfce7,stroke:#16a34a,color:#052e16
    classDef waiting fill:#f8fafc,stroke:#94a3b8,color:#475569
    class RoutedOut, HandedOff human
    class Booked, Cancelled, Answered done
    class AwaitingReply, Waitlisted waiting
```

## 4. Sequence: a faxed request becomes a booking

The language model only interprets and phrases. The orchestrator owns every rule and renders the confirmation card from validated state, so the card never comes from model prose.

```mermaid
sequenceDiagram
    autonumber
    actor F as Surgeon office
    actor C as Coordinator
    participant A as Agent (LLM)
    participant O as Orchestrator
    participant S as Scheduling service
    F->>A: fax: robotic right TKA,<br/>Dr. Patel, Maria Gomez, no DOB
    A->>O: extracted fields + confidence
    O->>S: look up surgeon, procedure, patient
    S-->>O: robot required,<br/>2 patients named Maria Gomez
    O->>S: estimate duration
    S-->>O: P50 112 min, P80 135 min
    O->>S: search: robot room, 142 min
    S-->>O: 3 slots + block ownership
    O-->>A: ranked options,<br/>open question: which patient
    A-->>C: option cards,<br/>asks for patient DOB
    C->>A: DOB 3/12/1958, take Tuesday
    A->>O: DOB, slot 1
    O->>S: look up patient (name + DOB)
    S-->>O: one match (MRN)
    O-->>C: confirmation card<br/>from validated state
    C->>O: confirm
    O->>S: hold, re-check, commit<br/>(idempotency key)
    alt slot still free
        S-->>O: case ID, Scheduled
        O->>O: build readiness list
        O-->>A: booking + readiness items
        A-->>C: case number, readiness list,<br/>draft office confirmation
    else slot taken
        S-->>O: SLOT_TAKEN
        O->>S: search again
        O-->>A: next options
        A-->>C: slot just taken,<br/>here are the next options
    end
```

## 5. Sequence: a bumped case is re-booked

The bump itself is a human decision, and the surgeon taking the room tells the bumped surgeon directly. The agent's work starts after that: it already knows the case, so it skips intake and goes straight to what the new date has to respect.

```mermaid
sequenceDiagram
    autonumber
    actor D as OR desk / AIC
    actor C as Coordinator
    participant A as Agent (LLM)
    participant O as Orchestrator
    participant S as Scheduling service
    D->>S: bump case 4417 for an emergency
    Note over D,C: surgeon taking the room<br/>calls the bumped surgeon
    S-->>O: event: case 4417 displaced
    O->>S: load case 4417
    S-->>O: case + readiness items
    O->>O: impact check: H&P valid to Nov 19,<br/>auth to Nov 30, tray due 48 h before
    O->>S: search before Nov 19,<br/>surgeon's own block first
    S-->>O: 2 slots
    O-->>A: re-booking task + constraints
    A-->>C: case 4417 bumped,<br/>2 options before H&P expires
    C->>A: take Thursday
    A->>O: slot 2
    O-->>C: confirmation card: new date,<br/>tray and PAT dates that move
    C->>O: confirm
    O->>S: hold, re-check, update 4417<br/>(idempotency key)
    S-->>O: 4417 rescheduled
    O->>O: recompute readiness list
    O-->>A: updated case + notifications needed
    A-->>C: drafts for approval: office and patient,<br/>SPD and vendor tray change
```
