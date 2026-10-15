# The Human Side of OR Scheduling in US Hospitals and Surgeon Practices: Roles, Daily Work, Mental Model, Tools, Frustrations

Research date: 2026-10-14. This file covers the people doing the work. The formal booking stages, booking form fields, block release numbers, KPIs and economics are in `../OR scheduling assistant research/workflow_and_data.md` and `stakeholders_and_value.md`, and are not repeated here.

**Source labels:** **[JP]** job posting or job description; **[R]** anonymous employee review (anecdotal); **[F]** practitioner forum post (anecdotal); **[T]** trade press; **[V]** vendor marketing (self-interested, unverified); **[PR]** peer-reviewed; **[S]** only a search-result snippet was available because the full page was blocked or 404. Treat [S] items as weaker evidence and re-check before quoting them.

**Method caveats:**
- Reddit (old.reddit.com) could not be fetched, and the search index returned no Reddit threads. AllNurses, Becker's and ScienceDirect returned HTTP 403 to direct fetches, so those items come from search snippets.
- The best first-person material is therefore Payscale employee reviews (2020) and AllNurses snippets (c. 2013–2015).
- Practitioner wording is paraphrased to respect copyright limits, with one short direct quote. The URLs lead to the verbatim text.

---

## 1. What distinct scheduling roles exist, how do they hand off, and which one is the "surgical scheduling coordinator"?

### Takeaway
At least six human roles touch one OR case:
1. The surgeon-practice surgical coordinator or surgery scheduler, who books the case and also handles prior authorization, clearances and patient instructions.
2. The hospital central OR scheduler, who validates and places the case and confirms back to the office.
3. The OR desk or control-desk scheduler, working with the charge nurse and the anesthesia-in-charge (the "board runners"), who own today's schedule and add-ons.
4. The anesthesia scheduling coordinator, who assigns anesthesiologists and CRNAs to rooms.
5. The ASC scheduler, who does the hospital-side job at a smaller scale and with more personal negotiation.
6. The perioperative business manager, who owns block allocation and utilization reporting.

"Surgical scheduling coordinator" is used on both sides of the practice–hospital line. In practice it most often names the practice-side (or clinic-side) person who books with the hospital and also does authorization and patient prep.

### Cited Findings
**Surgeon practice / clinic-side surgical coordinator ("surgery scheduler")**
- Duke Health's "Surgery Scheduler" job description (revised 03/24/2025) is a clinic-based role with these duties:
  - verify surgical postings (patient, procedure, diagnosis, site), enter referrals and orders, and resolve discrepancies with providers before scheduling
  - schedule surgeries in Epic or other systems and "secure operating room times with hospitals and surgical centers"
  - manage pre-op and post-op appointments, clearances and follow-ups
  - give patients pre-op and post-op instructions with verbal and written confirmation
  - verify benefits, obtain prior authorizations and tell patients their out-of-pocket costs
  - submit billing sheets daily for surgical coding
  - coordinate patient needs with anesthesia

  Requirements are a high school diploma, an associate's degree preferred, two years of clinical or coding/billing experience, and Epic experience preferred. The role has no supervisory responsibility. — [Duke DUHS Job Description 4655 [JP], rev. 2025](https://forms.hr.duke.edu/descriptions/duhs/select.php?ID=4655)
- Orthopedic practice postings bundle the same work: verify benefits and obtain authorization for every procedure, maintain the surgeon's schedule, and liaise with implant vendors — [Orthopaedic Specialty Group careers [JP], undated](https://osgpc.com/surgical-coordinator-careers/). Another adds confirming the insurer and getting prior authorization (or routing it), documenting informed consent, making pre-procedure calls, and reviewing discharge instructions — [Florida OrthoCare posting [JP], undated](https://florthocare.com/jobs/orhtopedic-surgical-coordinator/)
- At a children's hospital, a "Scheduling Coordinator II (Surgery & Procedures)" handles complex multi-surgeon cases and also confirms the insurer and obtains surgical authorizations — [CHKD Norfolk via CareerBuilder [JP][S]](https://www.careerbuilder.com/job-details/scheduling-coordinator-ii-surgery-procedures-norfolk-va--7e817a24-1cdd-475b-a2a4-95a6617fac01)
- Historical origin of the role (Portland, OR orthopedic group): before a formal surgery scheduling department existed, medical assistants on the clinic floor booked surgery alongside their other duties. As surgeons and caseload grew, inefficiencies followed, and the director of operations described the process as fragile — [Becker's ASC Q&A with Ken Takenaka, Orthopedic + Fracture Specialists [T][S], c. 2025](https://www.beckersasc.com/hospital-management-administration/from-backlog-to-booked-how-one-orthopedic-practice-accelerated-surgical-case-velocity/)

**Hospital central OR scheduler / perioperative scheduling office**
- University of Michigan "Surgery Scheduler": uses the EMR to create and maintain the surgical schedule, weighing surgeon availability, procedure complexity, OR capacity and turnaround times, and maintains waitlists — [UMich careers [JP][S], posting now 404](https://careers.umich.edu/node/271053)
- An Epic OpTime-based posting (Hermiston, OR) books and maintains cases in OpTime and related Epic modules, and works with surgeons' offices to confirm details such as CPT codes and estimated times — [ZipRecruiter Epic OpTime listings [JP][S], 2026](https://www.ziprecruiter.com/Jobs/Epic-Optime)
- Rush's "Perioperative Scheduler" is the go-between for patients, department staff and OR teams. It requires a high school diploma, and Epic experience is a plus rather than a requirement — [Rush posting [JP][S]](https://rush.fxrecruiter.com/jobs/details/united-states/il/chicago/work-type/perioperative-scheduler/13158)
- Centralized model: one team schedules electives for several hospitals in a region, and each hospital keeps a local staffer for urgent, emergent and same-day add-on cases. Central teams have increasingly worked remotely, which the vendor links to satisfaction and retention — [LeanTaaS blog, S. Fernandez [V], Mar 9 2022](https://leantaas.com/blog/centralized-surgical-scheduling-an-innovative-model-to-streamline-health-systems-address-case-backlogs/)

**OR desk / control desk / charge nurse / anesthesia-in-charge ("board runner")**
- Allegheny General Hospital's (AHN/Highmark) "Operating Room Scheduling Coordinator" duties:
  - assists the OR charge nurse at the OR control desk and maintains add-ons and cancellations for the current day's schedule
  - joins the daily OR huddle for final approval of the next-day schedule
  - drafts the OR schedule with surgeons' offices, perioperative management, anesthesiologists and surgeons
  - distributes the schedule so staff, equipment and supplies are ready
  - calls inpatient floors to arrange patient transport, and checks in vendors

  — [AHN posting via zapply [JP][S], 2026](https://zapply.jobs/jobs/c12f5790-9336-4d9c-88d8-d8d805fc7601/)
- Beth Israel Lahey "Perioperative Ops Assistant": takes add-on and next-day bookings that arrive after 5 pm and enters them into the hospital's PIMS system, enters staff assignments for the next-day schedule, and tells PACU about changes — [BILH posting [JP][S]](https://jobs.bilh.org/jobs/perioperative-ops-assistant-boston-ma-jr98421/)
- Who runs the board varies by facility, according to anecdotal AllNurses OR threads (c. 2013–2015):
  - At one hospital, a charge RN, charge anesthesiologist and charge CRNA jointly move resources and fit add-ons into rooms.
  - At another, a "charge triad" of nurse, anesthesia and surgeon leads decides, and nothing is decided unless the AIC (anesthesia-in-charge) and NIC (nurse-in-charge) agree.
  - Some hospitals rotated scrub techs into running the board, which RNs opposed because the charge nurse is the escalation point when something goes wrong.

  — [AllNurses "Who Runs Your Operating Room?" [F][S]](https://allnurses.com/who-runs-your-operating-room-t560689/); [AllNurses "Surgical Techs Running O.R. Board?" [F][S]](https://allnurses.com/surgical-techs-running-o-r-t751911/)

**Anesthesia scheduling coordinator**
- Brigham and Women's "Sr. Anesthesia Scheduling Coordinator" builds the daily anesthesia staff schedule (attendings, CRNAs, fellows, residents, SRNAs) for more than 250 clinicians across 43 main ORs plus procedural and off-site locations. They triage all same-day OR and personnel changes with the Associate Clinical Director, the Floor Leader and division team leaders — [Handshake posting [JP][S]](https://app.joinhandshake.com/jobs/4872728/share_preview)
- Johns Hopkins "Clinical Scheduling Specialist" runs the CRNA daily schedule in QGenda: 85 CRNAs across 75 anesthetizing locations per day. The schedule is generated quarterly, with room assignments made weekly — [JHH via dejobs [JP][S]](https://spinalcord.dejobs.org/baltimore-md/clinical-scheduling-specialist/F3C6DB597005440E8063E87FA75B45D7/job)
- University of Florida: an anesthesia admin role talks daily with the AOD (anesthesiologist on duty) about which faculty, residents, CRNAs, CAAs and fellows are available for clinical assignments — [UF posting [JP][S]](https://explore.jobs.ufl.edu/en-us/job/535494/administrative-specialist-i)

**ASC scheduler**
- At an Illinois orthopedic ASC (Becker's ASC; an older article, likely c. 2010–2012):
  - The center does not accept scheduling requests by phone.
  - It emails surgeons about voluntary block releases.
  - Blocks release at 72 hours, and as that deadline nears the scheduler calls surgeons to ask whether they will add cases.
  - When a request needs a block-holder to start earlier or later, the administrator or business office manager calls that surgeon to ask a favor.

  — [Becker's ASC "8 Points About Scheduling Cases in an ASC" [T]](https://www.beckersasc.com/asc-news/8-points-about-scheduling-cases-in-an-asc/)
- A CarePlus Management analysis found anesthesia scheduling was the most common concern among the ASC leaders it spoke with. Finding coverage when a provider cancels on the day of service is a particular problem — [Becker's ASC [T][S]](https://beckersasc.com/anesthesia/anesthesia-scheduling-is-a-major-pain-point-for-ascs-4-takeaways.html)

**Perioperative business manager (block allocation)**
- Perioperative business operations manager postings describe:
  - evaluating block utilization and recommending improvements
  - working with surgeons and clinic offices to make fuller use of block assignments
  - supporting decisions on access, block allocation and utilization
  - producing statistical, financial and benchmark reports for perioperative leaders and physicians
  - serving as administrative liaison to a perioperative block subcommittee

  These snippets come from several postings and are not attributed line by line — [Texas Health [JP][S]](https://jobs.texashealth.org/job/21828996/manager-perioperative-business-operations-arlington-tx); [Phoenix Children's [JP][S]](https://careers.phoenixchildrens.com/Positions/Posting/389091); [Hackensack Meridian [JP][S]](https://careers-hackensackmeridianhealth.icims.com/jobs/180704/mgr.-periop-business-information---full-time---day/job)

**Handoff evidence**
- A Hospital for Special Surgery (HSS, New York) scheduling posting prepares the daily OR schedule, checks it for accuracy and completeness, and sends surgery confirmation back to physician offices — [ZipRecruiter NY Surgery Scheduler Coordinator listings [JP][S]](https://www.ziprecruiter.com/Jobs/Surgery-Scheduler-Coordinator/--in-New-York)
- Indeed listed 1,528 "Surgical Scheduling Coordinator" jobs on June 1, 2026 — [Indeed [JP][S]](https://www.indeed.com/q-Surgical-Scheduling-Coordinator-jobs.html)

### Inferences
- **Handoff chain** (assembled from the postings above):
  1. The practice coordinator collects the decision, orders, authorization and clearances, then submits a case request.
  2. The central scheduler validates the request, places it, and sends confirmation back to the office.
  3. The next-day huddle finalizes the schedule. It includes the scheduling coordinator, perioperative management and anesthesia.
  4. The anesthesia scheduler maps providers to rooms against the posted schedule.
  5. The OR desk, charge nurse and AIC own same-day changes and add-ons, and an after-hours ops assistant books cases that arrive after 5 pm.
  6. The business manager looks backward at block utilization and pushes surgeon offices to use or release time.

  Each handoff is a re-read of the same case, often in a different system.
- **Who the "surgical scheduling coordinator" in the prompt is:** most likely the surgeon-side coordinator (practice or academic clinic) or the hospital central scheduler. The title covers both. Duke's "Surgery Scheduler" sits in the clinic but books OR time with hospitals; AHN's "OR Scheduling Coordinator" sits at the hospital control desk. For a Qventus-style hospital product, both are users: the office scheduler requests time (Qventus's Banner deployment sends block-release nudges to the surgeon's scheduler, per the prior notes), and the central scheduler approves it. The design should state which persona the agent serves first.
- The practice-side role is a generalist: scheduler, authorization specialist, patient educator, billing-sheet submitter, implant-rep liaison. The hospital-side role is a specialist in rules and capacity. An agent for the practice side has to deal with insurance and patient prep. An agent for the hospital side has to deal with rules, room capabilities and the board.

### Gaps
- No source gave a clean RACI or org chart for a typical hospital scheduling office (headcount, supervisor ratio, reporting line to the perioperative director).
- The OR Manager feature "Surgical scheduling: Taking an important role to the next level" (J. Mathias, Mar 2011) is behind a paywall. Its teaser line advertises an OR scheduler job at $33,000 — [Periop Leader/OR Manager [T]](https://www.periopleader.com/surgical-scheduling-taking-an-important-role-to-the-next-level/). Content not retrieved.

---

## 2. What does a day look like for each role (volume, calls/faxes/in-baskets, interruptions, end-of-day close, next-day confirmations)?

### Takeaway
No US time-and-motion study of OR schedulers was found. The day can be reconstructed from postings, vendor descriptions and anecdotes.

- **Practice coordinator:** a high-volume, interrupt-driven queue of calls, faxes, portals and EHR messages covering perhaps 8–15 cases a week per busy surgeon. Often one coordinator serves several surgeons. Each case carries dozens of data elements and touchpoints, plus 48-hour confirmations and payer hold time.
- **Hospital scheduler:** the day runs in phases. Today's add-ons and cancellations come first; new requests and changes run through the day; the next-day schedule is finalized at a huddle and confirmed to offices. Bookings after 5 pm go to an after-hours desk.
- **Anesthesia scheduler:** the day is a rolling rebuild of provider-to-room assignments as the OR schedule changes.

### Cited Findings
**Volume and load (practice side)**
- A busy orthopedic surgeon does 8–15 cases a week, and the dedicated coordinator confirms each case about 48 hours out — [Staffing for Doctors, Orthopedic Surgical Coordinator [V], updated Jul 2026](https://www.staffingfordoctors.com/practice-types/orthopedics/roles/surgical-coordinator)
- AAOS census: full-time orthopaedists average about 32 procedures a month (about 7–8 a week) and part-timers about 7 — [AAOS Orthopaedic Practice in the US (2018 census) [T]](https://www.aaos.org/globalassets/quality-and-practice-resources/census/2018-census.pdf). In 2017 AAOE data, average surgical cases per orthopedic physician rose from 443 (2014) to 503 (2017) — [AAOE Benchmarking 2017 insights [T][S]](https://cdn.ymaws.com/www.aaoe.net/resource/resmgr/benchmarking/aaoe_benchmarking_medres.pdf)
- Orthopedic practice employees per physician rose from 6.4 to 8.3 in the period ending 2024 — [AAOE benchmarking whitepaper [T][S]](https://assets.noviams.com/novi-file-uploads/aaoe/Leveraging_Benchmarking_Data_Whitepaper.pdf)
- Coverage ratios in employee reviews (2020, anecdotal): one reviewer is the only scheduler for four doctors and never gets help; another office has 11 doctors and one full-time scheduler — [Payscale Surgery Scheduler reviews [R][S]](https://www.payscale.com/research/US/Job=Surgery_Scheduler/Reviews/Page-5)
- Per-case burden:
  - A fax or email booking carries about 70 pieces of information, which the scheduler tracks and keeps current up to surgery day — [PreferredMD blog [V], Nov 24 2022](https://preferredmd.io/blog/what_do_physicians_expect_from_surgical_scheduling)
  - A single case may need 5–10 micro-tasks that never show up in reports — [Surgimate "Where Surgical Scheduling Loses Time" [V][S]](https://www.surgimate.com/blog/where-surgical-scheduling-loses-time-even-when-everything-looks-fine/)
  - The prior notes record the "40-plus messages per case" Becker's Spine figure.
- Status chasing: Surgimate claims coordinators spend up to 40% of the day checking whether cases are ready (calling payers, messaging colleagues, digging through files) and calls this a vigilance tax. The figure is unsourced — [Surgimate "The Operational Visibility Gap" [V], Apr 2026 (year inferred)](https://www.surgimate.com/blog/the-operational-visibility-gap/)
- Payer phone time: benefits verification and prior authorization calls can keep staff on hold for up to two hours, longer if the call drops — [PreferredMD [V], 2022](https://preferredmd.io/blog/what_do_physicians_expect_from_surgical_scheduling)
- AMA's 2024 survey, as cited by an orthopedic RCM vendor: physicians' practices handle about 39 prior authorization requests a week, taking about 13 hours of physician and staff time — [Strategic Practice Solutions [V] citing AMA 2024](https://spsrcm.com/orthopedic-prior-authorizations/)

**Rhythm of the day (hospital side)**
- Day-of: the control-desk scheduler tracks today's add-ons and cancellations alongside the charge nurse, calls floors to arrange transport, and checks in vendors — [AHN OR Scheduling Coordinator [JP][S]](https://zapply.jobs/jobs/c12f5790-9336-4d9c-88d8-d8d805fc7601/)
- Afternoon close: a daily OR huddle gives final approval to the next-day schedule — [AHN [JP][S]](https://zapply.jobs/jobs/c12f5790-9336-4d9c-88d8-d8d805fc7601/). The scheduling office then confirms scheduled surgeries to physician offices — [HSS via ZipRecruiter [JP][S]](https://www.ziprecruiter.com/Jobs/Surgery-Scheduler-Coordinator/--in-New-York)
- After hours: add-ons and next-day bookings after 5 pm go to a perioperative ops assistant who enters them in PIMS and notifies PACU — [BILH [JP][S]](https://jobs.bilh.org/jobs/perioperative-ops-assistant-boston-ma-jr98421/)
- Churn up to the last minute: in an anesthesia-literature descriptive study using OR system audit timestamps, at least half of ORs had their last case scheduled or changed within 2 working days of surgery — [PubMed 23011558 [PR], c. 2012](https://pubmed.ncbi.nlm.nih.gov/23011558/)
- Add-ons are getting more frequent. Becker's Spine reports more last-minute add-ons (referrals within 48 hours of the surgery date), with friction when the case lacks a complete medical record for clearance — [Becker's Spine [T][S], recent](https://www.beckersspine.com/spine/spine-orthopedic-leaders-tackle-top-friction-points/)

**Charge nurse / board runner day (anecdotal)**
- A first-person AllNurses account: the OR charge nurse plans add-on cases with the anesthesia charge while handling staff breaks and trauma pages, and may have to hold a room open for an incoming emergency — [AllNurses "A Day in the Life of an OR Charge Nurse" [F][S], c. 2013](https://allnurses.com/a-day-life-or-charge-t481164/)
- Another thread notes that juggling surgeon cancellations, add-ons and late anesthesia is hard to do while also circulating — [AllNurses [F][S]; which of the returned threads this came from was not verified](https://allnurses.com/calling-charge-nurses-t595139/)

**Anesthesia scheduler day**
- Requests, swaps and approvals arrive by email from about 85 providers, and the schedule is constantly fluid. Coordinators handle call-outs and secure emergency coverage — [anesthesia scheduling postings, Somnia/others [JP][S]; line-level attribution not verified](https://careers-somniainc.icims.com/jobs/2059/scheduling-coordinator/job)
- Assignments weigh provider specialty, benefit time, special-request cases, staff swaps, evening and late cases, and post-call, late-call and on-call status — [BWH [JP][S]](https://app.joinhandshake.com/jobs/4872728/share_preview)

### Inferences
- **Practice coordinator:** combining the vendor's 8–15 cases a week per busy surgeon with Payscale ratios of one coordinator to 4–11 doctors, one coordinator may carry roughly 30–100+ active cases in various stages of readiness at once. This is an estimate from unrelated sources, not a measured figure. Their day is mostly queue management: what is missing on which case, and who to chase.
- **Hospital scheduler:** the day has a predictable shape. Today's fires come in the morning, requests and changes run through midday, and the next-day freeze comes in the afternoon (2 pm close at UTMC per the prior notes, then a huddle). After hours is a handoff. An agent's highest-value moments are likely the afternoon close (is tomorrow complete?) and the 48–72 hour window (is the case actually ready?).
- Much of the interruption load is status and confirmation traffic (is it booked, what time, is auth done) that an agent could answer without a human.

### Gaps
- No time-and-motion study of US OR schedulers or practice surgical coordinators was found: calls per day, cases per FTE per day, and share of time on phone versus EHR are unmeasured.
- No hospital-side volume per scheduler (cases booked per scheduler per day) was found in any posting.
- A search summary described a Memphis anesthesia scheduling posting: about 70 anesthesiologists and CRNAs across five hospitals, a day-by-day resource calendar plus confirmation sheets, and a preference for candidates who know care-team ratio and site-logistics scheduling. The URL could not be pinned down, so this is left uncited.

---

## 3. How do experienced schedulers think when slotting a case ("Tetris"), what tribal knowledge do they rely on, how long does training take, and what is turnover like?

### Takeaway
Experienced schedulers carry a private model of each surgeon:
- whether their posted times are realistic (and how much to pad)
- whether they start late
- how they like cases sequenced
- what equipment, implants and staff they need

They also know which rooms have which capabilities, which rooms are closed, and who can be asked for a favor without overdrawing goodwill. Vendors say basic proficiency takes days to weeks and real mastery takes years. Turnover is described as a chronic problem, but no hard turnover rate for schedulers was found.

### Cited Findings
**What goes into the mental model**
- Surgeon-time padding: at one surgery center, a QA study found a group of surgeons who consistently underestimated case times, so schedulers were told to add time to those surgeons' cases. Habitually late surgeons can be scheduled later in the day ahead of time. Allowing surgeons to add cases at the start of the day rather than the end keeps clinic hours moving. These Becker's ASC/Spine scheduling-tips articles are older (c. 2010–2012) — [Becker's Spine "8 Tips for Scheduling at Orthopedic Surgery Centers" [T][S]](https://www.beckersspine.com/orthopedic-spine-practices-improving-profits/8-tips-for-scheduling-at-orthopedic-surgery-centers/); [Becker's ASC "8 Points About Scheduling Cases in an ASC" [T]](https://www.beckersasc.com/asc-news/8-points-about-scheduling-cases-in-an-asc/)
- The favor economy: when a request needs another block-holder to shift, leadership calls that surgeon to ask a favor. If the surgeon declines, they try other block holders or alternative days. The business office manager called it a bit of negotiating and said they take care not to ask any one surgeon for too many favors. Surgeons who release block time get extra attention from staff — [Becker's ASC "8 Points" [T], older](https://www.beckersasc.com/asc-news/8-points-about-scheduling-cases-in-an-asc/)
- Per-surgeon preferences: schedulers must learn each surgeon's preferences for sequencing, equipment and staffing. Experienced surgeons latch onto a great scheduler and dread their scheduler's vacations, and communicating accurately under pressure takes years — [LeanTaaS "Your Surgery Scheduler: One of Your Most Overlooked Assets" [V][S], undated](https://surgical-clinics.leantaas.com/your-surgery-scheduler-one-of-your-most-overlooked-assets/)
- Rules and capacity held in memory: central schedulers must memorize scheduling guidelines, search OR schedules by hand across several EHR locations, and check each provider's credentialing and availability. After a capacity tool went in, CHI Health Lakeside staff no longer had to remember room closures — [LeanTaaS centralized scheduling blog [V], Mar 2022](https://leantaas.com/blog/centralized-surgical-scheduling-an-innovative-model-to-streamline-health-systems-address-case-backlogs/)
- Factors a hospital scheduler is formally told to weigh: surgeon availability, procedure complexity, OR capacity, appropriate turnaround times — [UMich [JP][S]](https://careers.umich.edu/node/271053)
- Equipment and implants (ortho): send size estimates to the implant rep, confirm trays are at the facility, and coordinate specialty equipment (Mako, ROSA, navigation, custom guides) — [Staffing for Doctors [V], 2026](https://www.staffingfordoctors.com/practice-types/orthopedics/roles/surgical-coordinator)
- Anesthesia-side mental model: provider specialty, benefit time, special-request cases, swaps, late cases and call status — [BWH [JP][S]](https://app.joinhandshake.com/jobs/4872728/share_preview)
- Tribal knowledge as a known risk: a vendor positions its platform as removing reliance on tribal knowledge while cutting phone calls, and describes surgeon preference records so teams do not depend on one person's memory — [LeanTaaS iQueue for Surgical Clinics [V][S]](https://surgical-clinics.leantaas.com/)
- Surgimate says cases often live in folders, on sticky notes, or in one coordinator's mental Rolodex — [Surgimate [V], 2026](https://www.surgimate.com/blog/the-operational-visibility-gap/)
- Academic view: surgeon preferences are hard to manage by hand because the problem is complex — [ScienceDirect, OR scheduling with surgeons' preferences [PR][S], 2021](https://www.sciencedirect.com/science/article/abs/pii/S0360835221002102)

**Training time and turnover**
- A vendor says newly trained schedulers may not be up to speed for several days or weeks. Software that knows individual surgeon preferences would let anyone on staff schedule — [LeanTaaS iQueue for Surgical Clinics [V][S]](https://surgical-clinics.leantaas.com/7-best-surgery-scheduling-practices/)
- Many facilities struggle with staff turnover, so new hires need repeated training. Training on phone-based insurance verification means a mentor and new hire may wait an hour or more on hold before training can even start — [PreferredMD [V], 2022](https://preferredmd.io/blog/what_do_physicians_expect_from_surgical_scheduling)
- Electronic scheduling forms reduced workload and retraining needs. At one Chicago-area hospital, cancellations fell from about 12% to under 1% of cases after a scheduling form was introduced — [OR Manager, Feb 2013 (old, single site) [T][S]](https://healthnautica.com/eorders/eOrdersSurginORManagerFeb2013.pdf)
- Pay and seniority signals that suggest turnover risk:
  - Job postings run about $18–$40/hr — [ZipRecruiter perioperative scheduler [JP][S], 2026](https://www.ziprecruiter.com/Jobs/Perioperative-Scheduler). An Epic OpTime scheduler posting sample was $22.93–$35.88/hr — [ZipRecruiter [JP][S]](https://www.ziprecruiter.com/Jobs/Epic-Optime)
  - One guide puts pay at $18–21/hr — [Desmedcar [V][S]](https://desmedcar.com/what-is-a-remote-surgical-scheduler/)
  - Entry requirement is typically a high school diploma plus 1–2 years of healthcare office experience — [Duke [JP]](https://forms.hr.duke.edu/descriptions/duhs/select.php?ID=4655); [Rush [JP][S]](https://rush.fxrecruiter.com/jobs/details/united-states/il/chicago/work-type/perioperative-scheduler/13158)
  - Payscale reviewers (2020) complain that pay is below market and raises are hard to get — [Payscale [R]](https://www.payscale.com/research/US/Job=Surgery_Scheduler/Reviews/Page-2)
- General hospital context: 2025 hospital-wide turnover was 18.3% (NSI report, cited secondhand by a vendor). This is not scheduler-specific — [ShiftMed citing NSI 2025 [V][S]](https://www.shiftmed.com/insights/knowledge-center/flexible-scheduling-reduces-nurse-turnover-roi/)

### Inferences
- The "Tetris" is really four overlaid puzzles:
  - **Time:** padding surgeon-specific estimates, plus turnover.
  - **Space and equipment:** which room has the robot or C-arm, which room is closed, whether trays are available.
  - **People:** anesthesia coverage and ratios, specialty teams, surgeon lateness.
  - **Politics:** block ownership, a ledger of favors owed, keeping high-volume surgeons happy.

  The first three can be modeled from data. The fourth depends on relationships, and an agent should surface it (for example, "this requires Dr. X to shift; Dr. X has accommodated 3 requests this month") rather than act on it.
- Much tribal knowledge consists of facts that are knowable but unwritten: personal padding factors, room closures, preference cards. That makes it a strong target for an agent that reads historical case durations, room capability tables and preference cards and explains its reasoning in the scheduler's terms.
- Low pay, a high-school entry bar and multi-year mastery together suggest the job loses institutional knowledge whenever a senior scheduler leaves. Surgeons dreading their scheduler's vacations is a signal of single-person dependency. This is an inference; no turnover statistic supports it directly.

### Gaps
- No credible figure was found for time-to-proficiency, such as "6 months to independence." The only claims are vendor statements ("days or weeks" for basics, "years" for excellence).
- No scheduler-specific turnover or vacancy rate was found from MGMA, AAOE, AORN or HR surveys.
- No firsthand practitioner description (Reddit, AllNurses) of the slotting thought process was retrievable. Reddit was not reachable.

---

## 4. What tools and channels do schedulers juggle, and where do they re-key information?

### Takeaway
Schedulers work across:
- a hospital perioperative system (Epic OpTime, or a home-grown PIMS)
- the practice's own EHR or practice management system (athena, NextGen, ModMed, eCW), sometimes Epic
- payer portals and phone lines
- fax, still the default channel for orders, clearances and downtime requests
- email and phone
- spreadsheets, paper calendars and sticky notes
- anesthesia staffing tools (QGenda)
- whiteboards on the OR floor

The same case details are typed into several of these. One reviewer described entering each surgery in four places.

### Cited Findings
- Re-keying in a reviewer's words (2020, ophthalmology/cataract practice, Pueblo CO): "wasting more than 5-10 minutes putting surgeries in 4 different places" — [Payscale Surgery Scheduler reviews [R], Jun 2020](https://www.payscale.com/research/US/Job=Surgery_Scheduler/Reviews/Page-2)
- Root cause of duplicate entry: when a clinic schedules at a separate surgical facility, the information sits in the EMR, the clinic practice management system, the surgical center's practice management system and scanning software. Because these are disconnected, the same data is duplicated, and paper requests are faxed or mailed — [US patent "Coordinated processing and scheduling for surgical procedures" (12502075) [S]](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12502075)
- Fax, email and phone are the main communication channels in private practices, and spreadsheets are used for credentialing tracking. One change, such as a new date, can mean calling and faxing or emailing every party, reconfirming with the patient, and coordinating with vendors and the facility — [PreferredMD [V], 2022](https://preferredmd.io/blog/what_do_physicians_expect_from_surgical_scheduling)
- Central scheduling: coordination with clinic schedulers still relies on phone, fax and email, which the vendor says produces unmanageable call volumes and fragmented information. Schedulers search OR schedules across several EHR locations — [LeanTaaS [V], 2022](https://leantaas.com/blog/centralized-surgical-scheduling-an-innovative-model-to-streamline-health-systems-address-case-backlogs/)
- Clearances may sit in a fax queue, and cases are tracked across folders, sticky notes and paper or digital calendars — [Surgimate [V], 2026](https://www.surgimate.com/blog/the-operational-visibility-gap/). Readiness items (authorizations, clearances, labs, patient prep) are tracked across separate systems and rely on manual reminders — [Surgimate "Three Moments When Surgical Coordination Usually Fails" [V], Dec 2025 (year inferred)](https://www.surgimate.com/blog/the-three-moments-when-surgical-coordination-usually-fails/)
- Most practice coordinator work is described as phone, fax, portal and EHR coordination — [Staffing for Doctors blog [V][S]](https://www.staffingfordoctors.com/blog/what-does-a-surgical-coordinator-do-virtual)
- Hospital systems named in postings:
  - Epic OpTime — [ZipRecruiter [JP][S]](https://www.ziprecruiter.com/Jobs/Epic-Optime)
  - A PIMS system at BILH — [BILH [JP][S]](https://jobs.bilh.org/jobs/perioperative-ops-assistant-boston-ma-jr98421/)
  - Entering patient charges and post-case data into Epic — [Velvetjobs surgery scheduler JD [JP][S]](https://www.velvetjobs.com/job-descriptions/surgery-scheduler)
  - QGenda for anesthesia staffing — [JHH [JP][S]](https://spinalcord.dejobs.org/baltimore-md/clinical-scheduling-specialist/F3C6DB597005440E8063E87FA75B45D7/job)
  - Note from prior notes: UTMC keeps scheduling transactions in Athena and intraoperative documentation in Epic.
- ASC side: anesthesia schedules are still faxed or emailed to anesthesia providers, which a vendor offers to replace. Practices can request time through a form that needs no login. Integrations with athenaOne and NextGen are listed — [HST Pathways Case Coordination [V][S]](https://www.hstpathways.com/products/hst-case-coordination/)
- Payer channels: some carriers have web portals for prior authorization; others still need fax — [Nisos Technologies surgery scheduling guide [V][S]](https://nisostech.com/surgery-scheduling-guide/index.html)
- Whiteboards persist on the OR floor. A 2024 qualitative study interviewed 11 anesthesia clinical directors at US academic medical centers about the whiteboard used to run perioperative operations, using constructivist grounded theory. Its title frames it as running complex systems with simple tools — [ScienceDirect, "A qualitative exploration of operating room whiteboards" [PR][S], 2024](https://www.sciencedirect.com/science/article/pii/S2950553424000108)
- Electronic submission versus call-in: at Woman's Hospital, electronic case submission averaged 3 min 6 s per case with all required details, 12% faster than the phone workflow measured by the OR scheduling team — [LeanTaaS iQueue case study booklet [V][S], Oct 2023](https://leantaas.com/wp-content/uploads/2023/10/iQueue-for-OR-Case-Study-Booklet.pdf)

### Inferences
- Common re-key points (inferred from the sources above):
  1. Surgeon's note or verbal decision → practice EHR surgery order.
  2. Practice EHR → hospital case request (EpicCare Link, a portal, or a faxed form re-typed by the hospital scheduler).
  3. Case → payer portal or phone for authorization, then the authorization number is copied back to the case.
  4. Case → implant rep email or text.
  5. Case → patient instruction letter or call.
  6. Hospital schedule → anesthesia staffing tool (QGenda) and whiteboard.
  7. Any change → repeat 2–6.

  An agent that writes once and fans out (or at least pre-fills and diffs) addresses the re-keying directly.
- Fax persists because it is the lowest common denominator across independent practices, payers and hospitals. An agent design should assume some inputs arrive as faxed PDFs or images, not structured data.

### Gaps
- No source specifically described schedulers' use of secure chat (Vocera, TigerConnect, Teams, Epic Secure Chat). It is likely used on the OR floor and between the desk and the charge nurse, but this is unverified.
- No source measured time spent re-keying beyond the single Payscale anecdote.
- How often EpicCare Link is actually used by independent offices, versus fax, was not found.

---

## 5. What are the most common frustrations and failure modes, in practitioners' own words?

### Takeaway
Practitioners and their vendors describe the same cluster of frustrations:
- workload and understaffing (one scheduler for many surgeons, production quotas)
- poor communication and decisions made by people who do not do the job
- duplicate entry
- payer hold times and authorization mismatches
- missing intake information that has to be chased later
- last-minute add-ons with incomplete records
- surgeons who underestimate times or run late
- day-of anesthesia gaps

Blame and invisibility come through as feeling unvalued and being reprimanded over quotas. No direct source was found of schedulers being blamed for cancellations.

### Cited Findings
**Practitioner voice (anonymous reviews, 2020; all paraphrased except the quote in Section 4)**
- A cataract-practice scheduler (Pueblo, Jun 2020) said:
  - the work had tripled and everything felt rushed, with no communication
  - they felt expected to produce surgeries like a machine as one person
  - they were reprimanded for missing a daily surgery quota
  - surgeries had to be entered in four different places

  — [Payscale [R]](https://www.payscale.com/research/US/Job=Surgery_Scheduler/Reviews/Page-2)
- An office-based scheduler (Cincinnati, Jun 2020) said that as the only scheduler in the specialty, the doctors piled on more work with no extra pay and no overtime — [Payscale [R]](https://www.payscale.com/research/US/Job=Surgery_Scheduler/Reviews/Page-2)
- A Memphis reviewer (Jul 2020) cited lack of communication and not feeling paid or valued, while saying the job was stressful but rewarding when patients came out of surgery feeling better — [Payscale [R]](https://www.payscale.com/research/US/Job=Surgery_Scheduler/Reviews/Page-2)
- Other reviews describe a high-stress job, decisions made by people who do not do the work, and being the only scheduler for four doctors without help — [Payscale reviews, page 5 [R][S]](https://www.payscale.com/research/US/Job=Surgery_Scheduler/Reviews/Page-5)
- A remote-scheduler career guide says the stress comes from schedules, phone calls, paperwork and serving multiple customers with different priorities — [Desmedcar [V][S]](https://desmedcar.com/what-is-a-remote-surgical-scheduler/)

**Failure modes (documented mechanisms)**
- Missing intake information: coordinators spend extra time gathering information that could have been captured on day one, such as authorization requirements, patient preferences, facility constraints, incomplete orders, unclear diagnosis or CPT, and no owner for the next step. Authorizations can sit unsubmitted, and the team may not find out until days before surgery — [Surgimate [V], 2025](https://www.surgimate.com/blog/the-three-moments-when-surgical-coordination-usually-fails/)
- Communication breakdowns: changes not shared across teams, different teams holding outdated versions of the same information, and no feedback loop. This spans schedulers, surgeons, facilities, reps, anesthesia and clinic staff — [Surgimate [V], 2025](https://www.surgimate.com/blog/the-three-moments-when-surgical-coordination-usually-fails/)
- Early warning signs that coordination is slipping: orders piling up without a surgery date, and cancellations rising inside 72 hours — [Surgimate "Early Warning Signs" [V][S]](https://www.surgimate.com/blog/early-warning-signs-that-surgical-coordination-is-slipping/)
- Authorization mismatch: carriers have tightened retroactive fixes. An example is a knee arthroscopy authorized for one meniscal CPT code that needs a different code once the surgeon finds both menisci torn — [Strategic Practice Solutions [V]](https://spsrcm.com/orthopedic-prior-authorizations/). Common denial causes are missing documentation, outdated clinical notes, wrong CPT codes and payer form errors — [AnnexMed [V][S]](https://annexmed.com/prior-authorization-challenges-in-orthopedic-practices)
- Payer phone time: hold times run up to two hours, and an error means calling back — [PreferredMD [V], 2022](https://preferredmd.io/blog/what_do_physicians_expect_from_surgical_scheduling)
- Double-booked physicians (staff schedule the same slot separately), lost documents, patients arriving unprepared, and missed credentialing expirations — [PreferredMD [V], 2022](https://preferredmd.io/blog/what_do_physicians_expect_from_surgical_scheduling)
- Day-of cancellations from missing clearance or labs: the coordinator chases CBC, CMP, INR and type and screen so cases are not cancelled on the day — [Staffing for Doctors [V], 2026](https://www.staffingfordoctors.com/practice-types/orthopedics/roles/surgical-coordinator)
- Add-ons within 48 hours that lack a complete medical record for clearance — [Becker's Spine [T][S]](https://www.beckersspine.com/spine/spine-orthopedic-leaders-tackle-top-friction-points/)
- Surgeon behavior: underestimated case times, and late surgeons whose delays cascade to following cases and strain nursing and anesthesia staffing. If the surgeon warns the center early, the patient is not brought into pre-op too soon — [Becker's Spine/ASC tips [T][S], older](https://www.beckersspine.com/orthopedic-spine-practices-improving-profits/8-tips-for-scheduling-at-orthopedic-surgery-centers/)
- Anesthesia gaps: day-of provider cancellations at ASCs are hard to cover — [Becker's ASC/CarePlus [T][S]](https://beckersasc.com/anesthesia/anesthesia-scheduling-is-a-major-pain-point-for-ascs-4-takeaways.html). Rotating through coverage providers to cut per-case cost leads to cancellations, coverage gaps and surgeon frustration — [Becker's ASC [T][S]](https://www.beckersasc.com/anesthesia/the-hidden-asc-anesthesia-drain/). The US is projected to be 6,300 anesthesiologists short by 2036 — [Becker's ASC, Gavin Baker of Krewe Anesthesia [T][S]](https://www.beckersasc.com/anesthesia/the-invaluable-give-and-take-of-anesthesia-scheduling/)
- Day-of board friction: charge nurses juggle surgeon cancellations, add-ons and late anesthesia while also running staff relief and trauma pages — [AllNurses [F][S]](https://allnurses.com/a-day-life-or-charge-t481164/)
- Schedulers are described as often undervalued and underestimated, and were especially stretched after COVID surges — [LeanTaaS [V], 2022](https://leantaas.com/blog/centralized-surgical-scheduling-an-innovative-model-to-streamline-health-systems-address-case-backlogs/)

### Inferences
- The frustrations fall into three groups:
  1. **Chasing:** missing info, payer holds, clearances in fax queues.
  2. **Re-keying and re-broadcasting:** one change means N calls and faxes.
  3. **Absorbing other people's variance:** surgeons' time estimates and lateness, add-ons, anesthesia call-outs.

  An agent can take on groups 1 and 2 most directly. Group 3 is where it should advise, not decide.
- The emotional tone (one person for many surgeons, quotas, feeling unvalued) suggests positioning the agent as the scheduler's assistant that removes chasing and duplicate entry. An agent that bypasses the scheduler, or reports on their speed, is likely to meet resistance. This is an inference.

### Gaps
- No firsthand source was found in which schedulers describe being blamed for cancellations, although it is widely assumed. Reddit and AllNurses threads that might contain it could not be fetched.
- No source described vendor and implant rep frustrations from the scheduler's side beyond "liaise with vendors" and "confirm trays."
- Most failure-mode material is vendor-authored ([V]). Independent quantification (for example, the share of a coordinator's time spent chasing) is missing.

---

## 6. What does the surgeon-practice side look like, from "we'll operate" to "patient arrives"?

### Takeaway
The practice coordinator runs a checklist of roughly 10 steps over 2–6 weeks:
1. Capture the decision and orders.
2. Verify benefits and obtain prior authorization (procedure and implants).
3. Counsel the patient on cost.
4. Book OR time at the hospital or ASC.
5. Arrange medical clearance (PCP or cardiology) and pre-op labs and EKG within the H&P window.
6. Coordinate implants, trays, reps and special equipment.
7. Coordinate anesthesia needs.
8. Send pre-op instructions and consent.
9. Confirm 48 hours out.
10. Handle post-op follow-up and billing sheets.

Each step can reset when the date, CPT code or site changes.

### Cited Findings
- **Vendor checklist (ortho):**
  1. decision to operate
  2. book the hospital or ASC block, with the H&P inside its 30-day window
  3. schedule pre-op clearance and confirm it is uploaded to the chart
  4. chase labs (CBC, CMP, INR, type and screen)
  5. secure prior authorization for the procedure and implants
  6. send size estimates to the implant rep, confirm trays are at the facility, and coordinate Mako, ROSA, navigation or custom guides
  7. send pre-op instructions and coordinate anesthesia
  8. confirm 48 hours out
  9. manage post-op follow-up

  — [Staffing for Doctors [V], updated Jul 2026](https://www.staffingfordoctors.com/practice-types/orthopedics/roles/surgical-coordinator)
- **Academic clinic version:** verify the posting, enter referrals and orders, resolve discrepancies with providers, schedule in Epic and secure OR time with hospitals or ASCs, manage pre-op and post-op ancillary and diagnostic appointments and clearances, give verbal and written confirmation, verify benefits and obtain authorization, notify patients of out-of-pocket costs, submit daily billing sheets, log clearances and lab results, coordinate with anesthesia — [Duke [JP], 2025](https://forms.hr.duke.edu/descriptions/duhs/select.php?ID=4655)
- **Patient-facing steps:** document informed consent, make pre-procedure calls, review discharge instructions and schedule follow-up — [Florida OrthoCare [JP]](https://florthocare.com/jobs/orhtopedic-surgical-coordinator/). Verify insurance eligibility and notify patients of copays and out-of-pocket costs — [Goodkind Group surgical coordinator [JP][S]](https://jobs.recorder.com/job/d4ec07f0-9b75-4a46-8089-8fa07202c28f/surgical-coordinator). Respond to patient questions during the perioperative period to keep them informed and calm — [Duke NC Orthopaedic Clinic Surgery Scheduler [JP][S]](https://careers.duke.edu/job/Durham-Surgery-Scheduler-NC-Orthopaedic-Clinic-NC-27707/1327148500)
- **Authorization workflow** as described by an RCM vendor:
  1. Confirm eligibility and benefits, and flag out-of-pocket costs.
  2. Submit with complete documentation.
  3. Track the approval number, dates and units.
  4. Watch expiration dates.
  5. Work with billing on denials.

  — [Strategic Practice Solutions [V]](https://spsrcm.com/orthopedic-prior-authorizations/)
- **Practice–hospital interface:** coordinators book OR or ASC time with the hospital and arrange PCP or cardiology clearance — [Staffing for Doctors [V]](https://www.staffingfordoctors.com/practice-types/orthopedics/roles/surgical-coordinator). Hospital schedulers in turn confirm CPT codes and estimated times with surgeons' offices — [ZipRecruiter Epic OpTime [JP][S]](https://www.ziprecruiter.com/Jobs/Epic-Optime) — and send confirmation back to physician offices — [HSS via ZipRecruiter [JP][S]](https://www.ziprecruiter.com/Jobs/Surgery-Scheduler-Coordinator/--in-New-York)
- **The block-release pull from the hospital:** as release deadlines near, facility schedulers call surgeons' offices to ask whether they plan to add cases — [Becker's ASC "8 Points" [T], older](https://www.beckersasc.com/asc-news/8-points-about-scheduling-cases-in-an-asc/). (Qventus's Banner block-release nudges to the surgeon's scheduler are covered in the prior notes.)
- **Change cascade:** one date change means calling and faxing or emailing every party, reconfirming with the patient, and re-coordinating vendors and the facility — [PreferredMD [V], 2022](https://preferredmd.io/blog/what_do_physicians_expect_from_surgical_scheduling). Changing location, patient class or CPT requires updating the authorization with the insurer (HonorHealth form; see prior notes).
- **Lead-time pressure:** the case-scheduling audit data in the anesthesia literature (last changes within 2 working days for at least half of ORs) shows that readiness work collides with schedule churn late in the cycle — [PubMed 23011558 [PR], c. 2012](https://pubmed.ncbi.nlm.nih.gov/23011558/)

### Inferences
- The practice coordinator works on a dependency graph, not a calendar. The OR slot is one node. Authorization (tied to CPT and site), clearance and labs (tied to a date window relative to surgery), implants (tied to the date and facility) and patient instructions (tied to the date and arrival time) all hang off it. A change to date, CPT or facility invalidates downstream nodes. A good agent should track readiness per case, explain what a proposed change would invalidate before the human commits to it, and pre-draft the re-notifications.
- Most practice–hospital friction sits at three seams:
  1. **Intake completeness:** the hospital rejects incomplete forms; prior notes cite Emory's "case will not be scheduled."
  2. **Duration and equipment truth:** the office's estimate versus the hospital's history-based time.
  3. **Late readiness:** clearance and authorization not done by the 48–72 hour mark.

  These are the natural checkpoints for an agent spanning both sides.

### Gaps
- No source quantified elapsed time from decision to surgery date, or how long each checklist step takes, for US practices.
- No firsthand practice-coordinator narrative (for example, an AAOE or MGMA member story) was retrievable. AAOE member content and Becker's full texts were blocked.
- No data was found on how many independent practices use EpicCare Link versus fax to submit hospital case requests.
