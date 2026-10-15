# Problem Statement: AI-Assisted OR Case Booking

*Qventus AI Solution Architect Tech Challenge. Chosen workflow: Operating Room Scheduling.*

**North star:** every OR case request becomes a complete, compliant booking in the right slot, quickly, and the coordinator spends their time only on the requests that need human judgment.

## 1. Outcomes

### Customer outcomes

| Outcome | Why it matters to the hospital | How booking contributes |
|---|---|---|
| Grow surgical volume in existing OR capacity | A staffed OR minute costs about $57.71 (FY2022), and an added elective case is worth roughly $4,000–5,000 in contribution margin | Released and open time gets booked sooner, cases land in the owner's block first, and durations fit the slot |
| Reduce avoidable delays and day-of cancellations | Cancellations waste staffed time and patient trust. A fifth to a third of them are hospital-side: equipment, implants, beds, scheduling errors | Bookings carry the right procedure, side, equipment, implant and authorization details, so downstream teams act on correct information from the start |
| Zero booking-originated safety errors | In one study of 17,000+ surgeries, wrong side was 36% of booking errors, and most were caught only in pre-op holding or the OR | Patient identity, laterality and procedure codes come from lookups and are confirmed before anything is committed |
| Give coordinators time back for judgment | Coordinators re-key requests into several systems and chase missing fields; one source reports 40+ messages per case | The agent handles intake, validation and option-finding; the coordinator handles exceptions |
| Faster, more predictable access for surgeons' offices | Offices phone and fax to find time, and independent surgeons take cases elsewhere when booking is hard | Request-to-confirmation time drops, and the office gets a confirmation plus a list of what is still needed |

### What this project moves directly, and what it enables

This project **stops at the point of booking**. Within that scope it moves these measures directly:

- time from request received to confirmed booking
- coordinator touches per request
- share of bookings that are complete and valid on first pass
- hard-rule violations (target: zero)
- share of requests that would qualify for straight-through booking
- correct routing of urgent, clinical and other-owner-block requests to the right human
- readiness items created with an owner and a deadline at the moment of booking

It **enables, but does not deliver or measure**, the downstream outcomes: released-time fill rate, prime-time utilization, day-of cancellations caused by booking errors, share of cases ready 72 hours out, and overtime. Section 5 explains the link and treats it as a hypothesis.

## 2. The problem

A hospital's central OR scheduling coordinator turns a constant stream of requests into bookings. Requests arrive by fax, phone, email, EHR case request and web portal, and they range from complete to unusable. Before a case can go on the schedule it has to meet a strict standard: complete data, safe identifiers, and the hospital's rules on block ownership, room capability, surgeon privileges, cutoffs and authorization. The scheduling system of record has to stay deterministic and auditable, because an error in patient, side, procedure or duration becomes a safety event, a cancellation or idle OR time.

Today the coordinator is the human integration layer between messy inputs and that strict system. They re-key requests, chase missing fields, search block, released and open time across screens, and re-send every change by phone and fax. Most of that work is language work, which current AI handles well. Choosing a feasible slot is constraint satisfaction, which deterministic code handles better; the best models solve only about half of calendar-scheduling benchmark tasks.

> **How might we** let an AI agent handle the language work at the edges of booking (reading any request, asking for exactly what is missing, turning intent into a structured search, explaining the options, and packaging the result for the people downstream) while a deterministic engine decides what is feasible and the coordinator stays in control of what gets booked?

## 3. Who we are designing for

- **Primary user: the hospital central OR scheduling coordinator.** A rules-and-capacity specialist who validates requests, sizes cases, places them against block ownership and room capability, and confirms back to the office. The agent is their teammate, working on top of the hospital's scheduling system of record.
- **Counterparty: the surgeon's office surgical coordinator.** Submits requests, answers clarifying questions, and receives confirmations and outstanding-item lists. They are also a natural second user of the same capability, with narrower permissions.
- **Downstream readers of every booking:** OR desk, charge nurse and anesthesiologist in charge (AIC), anesthesia scheduling, pre-admission testing (PAT), sterile processing (SPD), implant vendors, bed management, and the patient.

The job title "surgical scheduling coordinator" is used on both the hospital and office side. This problem statement centers the hospital side because block rules, room capability and history-based sizing are the core of the OR scheduling problem; the office side's heaviest work (prior authorization, patient preparation) belongs to adjacent workflows.

## 4. What comes in

Inputs vary along four independent dimensions. A solution has to handle any combination.

| Dimension | Variants |
|---|---|
| **Who sends it** | Surgeon's office coordinator; the surgeon directly; hospital teams (OR desk, anesthesia, bed management, PAT); the scheduling system itself (auto-release, room or equipment closures) |
| **How it arrives** | Fax (scanned image or PDF); phone call or voicemail (transcript); email, often with attachments; EHR case request (structured but often incomplete); web portal or form; secure chat or text; the coordinator typing or saying what they need |
| **What it asks for** | See request types below |
| **What condition it is in** | Complete; incomplete; conflicting (the side in the request differs from the surgeon's order); ambiguous (two patients match, surgeon name partial); illegible; duplicate (the same request faxed and phoned in); stale (H&P out of window, authorization expired) |

### Request types

| Group | Request type | Example | Typical source |
|---|---|---|---|
| New case | New elective case | "Robotic right total knee for Dr. Patel, next three weeks" | Office, any channel |
| New case | Duplicate of a request already received | The same case faxed and also phoned in | Office |
| New case | Availability check, no case yet | "What robot time is open next week?" | Coordinator, office |
| New case | Waitlist or first-available | "Tell me if Wednesday opens up" | Office |
| New case | Request another owner to release block time | "Can Urology give up Wednesday?" | Coordinator |
| Existing case | Re-book a bumped case | Displaced by an emergency on the day of surgery | OR desk, AIC |
| Existing case | Modify a booked case | Change date, procedure, side, duration, equipment, surgeon, patient class or site | Office, surgeon |
| Existing case | Reschedule after postponement | Authorization denied, patient not optimized, patient asked to move | Office, PAT, financial clearance |
| Existing case | Cancel | Requires a reason | Office, patient |
| Existing case | Status inquiry | "Is the Gomez case on? What's still open?" | Office, OR desk |
| Existing case | Readiness update | Authorization approved, H&P uploaded, tray confirmed | Office, payer, vendor |
| Hospital or system event | Room, equipment or staffing change | Robot down, staffing shortage, surgeon out; one event can displace several cases | Perioperative leadership, system |
| Hospital or system event | Time opens and a waitlisted case fits | A release or cancellation frees Wednesday | Scheduling system |
| Continuation | Late reply to an open question | The office faxes the missing date of birth hours later | Office, any channel |
| Routed to a human | Add-on, urgent or emergent | "This needs a room tonight" | Surgeon, OR desk |
| Routed to a human | Clinical question | "Is she fit for general anesthesia?" | Anyone |

Changes and re-bookings are a large share of the traffic, not an edge case. In audit data from a US academic hospital, 51.5% of ORs had their last case added or changed within two working days of surgery. A solution that only handles new requests misses much of the real work.

Three other properties of the input stream shape the problem. Not every input comes from a person: hospital and system events create work on their own, and one event can displace several cases at once. A request can stay open across channels and hours, because the answer to a clarifying question may arrive later by fax. And readiness updates arrive in the same queue even though they belong to the follow-up work after booking, so they have to be recognized and routed.

## 5. Why booking quality is where downstream outcomes start

### The standard a booking must meet

A request is bookable only when it passes two layers of checks:

1. **Completeness:** every field the procedure and site require is present (patient, surgeon, procedure, laterality, duration, anesthesia type, patient class, equipment, implants and vendor, authorization status, and more).
2. **Validity:** the request passes the hospital's rules. The hard rules are: no room, surgeon or equipment conflicts; the room has the required capability; the surgeon is privileged for the procedure; no booking into another owner's unreleased block; two patient identifiers confirmed; laterality spelled out and consistent with the order; procedure codes resolved from the master list; nothing committed without confirmation. Requests after the schedule closes, and urgent cases, route to humans.

### How booking quality flows downstream

Everyone downstream acts on the booking as written. An error introduced at booking is copied by each team that reads it, not corrected.

| Booking attribute | Downstream effect | Outcome it supports | Evidence |
|---|---|---|---|
| Correct patient, procedure, side and approach | Right preference card, case cart, consent and site marking; no day-of correction | Safety; fewer delays | 0.86% booking error rate, 36% of errors wrong side, mostly caught in holding or the OR |
| Duration from the surgeon's history, plus room-type turnover | Fewer overruns and fewer idle gaps | Utilization; less overtime | Standard estimates land within 10% of actual only 32% of the time; Epic's prediction was within 30% for 77.9% of cases vs 48.2% for surgeon estimates |
| Equipment, implants and vendor captured at booking | Loaner trays requested before the 48-hour (or 3-business-day) SPD deadline | Fewer equipment delays and cancellations | Facility causes, including equipment, implants and scheduling errors, were 20% of VA cancellations |
| Procedure code, site, patient class and date consistent with the authorization | The authorization matches what is booked; no late denial from a mismatch | Fewer late cancellations | Insurance was the top cancellation cause (36.2%) in one total-joint series; 58.5% of spine denials arrived within 3 days of surgery |
| Readiness items created with an owner and a deadline | Follow-up starts at booking, not at check-in | Fewer late cancellations | Outreach 48–72 hours out roughly halved preventable late cancellations (quality-improvement and vendor reports) |
| Fast booking; owner's block before open time | Released and open time filled before it goes idle; block utilization credited correctly | Volume; utilization | Released-time fill rates of 34–46% reported (vendor-linked) |

The booking's final output is therefore more than a case number. It is the case number plus a **readiness list** of open items (authorization, H&P window, implant tray deadline, vendor rep), each with an owner and a due date, and a confirmation to the office. This is where the project stops: it creates the list and hands it off. Chasing those items is the next tier of value (Section 6).

**Caveats.** Booking quality is necessary but not sufficient. The largest cancellation categories are patient-related (35% in VA data) and medical work-up (28%), which a booking cannot fix, though a good booking starts the clock on fixing them. No published study isolates the effect of a booking interface on utilization; vendor case studies bundle booking with nudges, outreach and analytics. We treat the downstream outcomes as hypotheses and measure the leading indicators in Section 1.

## 6. The spectrum of agent value

The agent's role is a dial, not a single feature. Each tier adds autonomy on top of the one below, and the underlying capability is the same; what changes is where the human approval sits.

| Tier | The agent | The coordinator | Value | How we measure it |
|---|---|---|---|---|
| **1. Clean intake** | Turns any input into a structured, validated draft; asks for exactly what is missing; flags conflicts and duplicates | Makes every slot decision and commits | Less re-keying and chasing; complete on first pass | Touch time; first-pass completeness |
| **2. Decision support** | Runs the deterministic search and returns ranked, valid options with the trade-offs laid out: block ownership and release time, fit at typical and long durations, room capability, readiness risk, utilization effect | Picks an option and confirms | Better slot choices, made faster | Time to book; own-block-first rate; overrun risk |
| **3. Straight-through booking** | Books requests that pass every eligibility check without a human; packages the rest as exceptions with options laid out | Handles exceptions: other owners' blocks, duration overrides, add-ons, conflicts, anything political | Coordinator capacity freed for judgment; faster fill | Straight-through rate; zero incorrect auto-books |
| **4. Closing the loop after booking** | Chases readiness items, pushes changes to every affected team, re-offers displaced cases | Judges exceptions | Fewer late cancellations; changes reach everyone | Share of cases ready 72 hours out |

Tiers 1–3 sit within this project's scope. Tier 4 is downstream of booking.

Three notes on the tiers:

- **Bumps are not part of elective booking.** A routine elective booking never displaces another case. Displacement only comes up for urgent and emergent requests, and the hospital's policy decides who chooses. In most hospitals, and in this design's defaults, that is the AIC, with the agent listing the affected cases.
- **Tier 3 eligibility is deterministic and set by the hospital.** The hospital's autonomy policy defines when a request qualifies. A sensible default: all required fields are present and resolved through lookups, nothing conflicts with the surgeon's order, the procedure uses a fully supported booking strategy, the slot is in the requesting surgeon's own block or open time, there are no resource conflicts, the schedule has not closed, the duration is not overridden, and the request is not a duplicate. Everything else goes to the coordinator.
- **Autonomy is promoted, not assumed.** Each hospital sets the tiers in its policy, per request type. Running Tier 3 in shadow mode first, and measuring agreement with the coordinator's actual decisions, is how a hospital would earn the confidence to switch it on.

## 7. Scope

The problem runs from the moment a request arrives to a confirmed booking with its readiness list handed off.

**In scope**
- Every request type in Section 4 that ends in a booking decision (new cases, waitlist, modifications, re-bookings, reschedules, cancellations), plus routing urgent and add-on requests to the right human and answering status questions
- Inputs from any channel and in any condition
- The variation between kinds of surgery and settings. Most service lines differ only in parameters (durations, equipment, specialized staff, vendor lead times, turnover, release rules). A few differ in how booking works: cardiac and transplant cases need an ICU bed reserved with the room; cataract lists and flip rooms run parallel rooms; trauma, transplant and emergent C-sections preempt electives; and eligibility differs across surgery center, hospital outpatient department and main OR
- Both sides of the request: the hospital coordinator as primary user, the surgeon's office as counterparty
- Tiers 1–3 of agent value

**Out of scope (downstream of booking)**
- Chasing readiness items, prior authorization and patient outreach (Tier 4)
- Day-of board management, late-room decisions and anesthesia staffing
- Block allocation and block-release prediction

## 8. Boundaries: what the flow guarantees and what the hospital decides

The agent itself guarantees only what its conversation flow guarantees, at any hospital:

- **Nothing is committed without a confirmation step and a commit-time re-check.** Who confirms is the hospital's choice: the coordinator, or an automatic approver if the hospital's autonomy policy allows straight-through booking.
- **The model proposes; the flow decides.** Model output becomes part of a case only after lookup and validation, so identifiers always come from the hospital's systems, and text in a fax or message can't steer the flow.
- **Every step is recorded.**

Everything else is hospital policy, and the agent follows whatever policy it is given. The defaults in this design come from the hospitals in the research:

- Urgent, emergent and after-close requests go to the AIC and the OR desk; the agent doesn't book them or assign an urgency class.
- Bumping a scheduled case is the AIC's decision; the agent may list the affected cases.
- Clinical questions, such as fitness for surgery, go to the surgeon's office. Keeping clinical judgment out of the agent also keeps it an administrative tool rather than a regulated medical device, so a hospital would need a strong reason to change this default.
- A request for another owner's unreleased block becomes a release request the coordinator sends, because those favors are negotiated between people.
- Patients are identified by two identifiers and the side is always stated, following the Joint Commission's Universal Protocol.

## 9. Assumptions and open questions

**Assumptions**
- A US hospital running an Epic-like system of record. Public EHR interfaces expose surgical cases read-only, so bookings must go through a hospital-approved scheduling interface or a case-request queue that a human finalizes.
- Hospital rules (release horizons, cutoffs, readiness deadlines, routing, autonomy) vary by hospital and are read from each hospital's own systems and policies. The examples in this document come from public hospital policies.

**Open questions**
- How much straight-through autonomy would a hospital accept, and for which request types?
- How accurate is extraction on real faxes and call transcripts?
- Which persona would Qventus deploy first, given that its Clinic Scheduler Assistant already serves surgeons' offices?

---

*Evidence and sources: [OR scheduling assistant research](reports/OR%20scheduling%20assistant%20research.md) and [OR scheduler role and agent value](reports/OR%20scheduler%20role%20and%20agent%20value.md).*
