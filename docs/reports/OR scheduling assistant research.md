# Turn TimeFinder into a trustworthy booking conversation

The scenario that fits both the take-home rubric and Qventus's real product line is a chat version of TimeFinder with write-back. A central OR scheduling coordinator asks in plain language for time for a named surgeon and procedure. The assistant searches block, released and open time and knows who owns each minute. It sizes the case from the surgeon's own history plus turnover and filters rooms by capability. It books only after a structured read-back, and it returns a case number together with the readiness items that are still open. Qventus already sells every underlying piece: open-time search, block-release nudges, a clinic booking assistant with a 22-minute median turnaround, a Document Assistant that reads faxes, and bi-directional EHR write-back. It has not announced a chat interface for OR case booking. This research found no conversational OR-booking agent from LeanTaaS or Epic either, though LeanTaaS markets workflow assistants and a generative-AI "Autopilot." The table stakes are availability search that knows block ownership, deterministic handling of patient identity, procedure codes and laterality, explicit confirmation before every write, and a clear split between a case that is *booked* and one that is *ready*. Constraints fall into three tiers:

- **Hard blockers:** room, surgeon and equipment conflicts; missing privileges; another owner's unreleased block; missing laterality.
- **Gates that are hard on the day of surgery but soft at booking:** H&P, consent, prior authorization, loaner trays.
- **Soft preferences:** utilization, sequencing, prime time.

Public Epic interfaces expose surgical cases as read-only, so the backend has to be a mocked scheduling service with hold-and-confirm semantics. The economics rest on OR minutes that cost $57.71 each in FY2022 and an added elective case worth about $4,000–5,000 in contribution margin. Nearly every outcome figure in this market, though, is vendor-reported and uncontrolled. The recommended scenario books a robotic right total knee arthroplasty. Its alternate path is a request that lands in another service's unreleased robotic block. Its failure and escalation paths are an urgent case routed to the anesthesia-in-charge (AIC) and a slot lost to a race at commit.

## Table stakes start with knowing who owns each OR minute

### Qventus sells every piece except the conversation

Qventus's perioperative business is built on making OR time easy to trade. Its 2021 Perioperative Solution had three parts:

- machine learning that predicts **up to a month ahead** which blocks will go unused, with behavioral nudges to get them released;
- outreach that offers open time to the surgeons most likely to use it;
- **TimeFinder**, a reservation-style view where employed and community surgeons and their schedulers see open time and colleagues' block time, then submit case requests without an EHR login. TimeFinder replaced a separately faxed request form.

([Qventus, Oct 2021](https://www.qventus.com/company/newsroom/qventus-introduces-new-perioperative-solution-to-increase-prime-time-utilization-and-grow-case-volume/)).

Today these ship as "AI teammates" in the Surgical Growth Solution. TimeFinder now predicts case length from each surgeon's history. The Capacity Assistant prompts block release weeks ahead. The Strategic Marketing Assistant and Robotics Optimizer market time to best-fit surgeons ([Qventus Erlanger blog](https://www.qventus.com/resources/blog/how-erlanger-adds-220-surgical-cases-per-month-with-ai-powered-surgical-operations/)). The May 2025 release added three more pieces ([Qventus, May 2025](https://www.qventus.com/company/newsroom/qventus-ai-teammates-transform-the-perioperative-care-journey-driving-strategic-surgical-growth-and-winning-several-new-clients-and-enterprise-wide-expansions/)):

- a **Clinic Scheduler Assistant** embedded in independent surgeons' clinic EMRs, with a **22-minute median booking turnaround**;
- a **Document Assistant** that digitizes perioperative scheduling faxes, claimed to save **~60 OR-scheduler hours per month**;
- **enhanced bi-directional write-back**, claimed to save **~100 hours per scheduler per month**.

At Banner Health, schedulers use TimeFinder to search open slots by day, time, room type, equipment and procedure duration, and book in a few clicks ([Qventus Banner Health](https://qventus.com/resources/customer-successes/banner-health)). Those search dimensions are a good minimum filter set for the prototype.

The company is well funded and leans hard into agents. It raised a **$105M Series D led by KKR** in January 2025 ([Business Wire](https://www.businesswire.com/news/home/20250113993134/en/Qventus-Announces-$105-Million-Investment-Series-D-Led-by-KKR)). It says it serves 150+ hospital facilities and co-develops assistants with Allina and HonorHealth through its AI Solution Factory. It positions itself as a layer that acts on top of the EHR, not a replacement for it ([HonorHealth release, Sept 2026](https://finance.yahoo.com/healthcare/articles/honorhealth-selects-qventus-ai-solution-130000232.html)). Its conversational features (voice calls, SMS, chat and EHR follow-ups) are documented for Perioperative Care Coordination and the patient concierge, not for OR case booking ([Qventus Allina release](https://www.qventus.com/company/newsroom/qventus-announces-allina-health-as-its-inaugural-ai-solution-factory-client/)).

The competitive field explains why a conversational booking layer is interesting.

- **LeanTaaS iQueue for Operating Rooms** is the closest rival. It reports 550+ hospitals and 5.7k+ ORs and offers block release and request workflows plus open-time matching, but it describes most of its workflows as read-only alongside the EHR ([LeanTaaS](https://leantaas.com/products/operating-rooms/)). It billed its 2023 iQueue Autopilot as a generative-AI layer across its OR, infusion and inpatient products ([LeanTaaS](https://leantaas.com/press-releases/leantaas-announces-iqueue-autopilot-first-ever-generative-ai-hospital-operations-solution/)). Its June 2025 iQueue for Surgical Clinics reaches into the surgeon's office ([LeanTaaS](https://leantaas.com/press-releases/leantaas-launches-iqueue-for-surgical-clinics-delivering-the-industrys-first-end-to-end-surgical-coordination-platform/)).
- **Epic's OR Capacity** suite includes an OR Marketplace, self-service release, Predictive Block Reminders, EpicCare Link for outside offices, and case-length estimates with a confidence score. Epic reports, as a vendor, about three more cases per OR per month from the Marketplace ([Epic](https://www.epic.com/software/or-capacity/)).
- **Epic's AI agents** (Art, Emmie and Penny) target clinicians, patients and revenue cycle. Emmie's scheduling is patient-side appointments, not OR cases ([Healthcare IT News](https://www.healthcareitnews.com/news/epic-unveils-ai-agents-showcases-new-foundational-models)). Epic's Agent Factory, previewed at HIMSS26, is the platform risk to watch ([Digital Health News](https://www.digitalhealthnews.com/epic-unveils-agent-factory-expands-ai-tools-at-himss26)).
- **Apella and Opmed** compete on prediction and day-of execution, not booking. Examples are Apella's pilot claims of 69 fewer delayed minutes per OR per day ([GlobeNewswire](https://www.globenewswire.com/news-release/2025/08/21/3137285/0/en/Apella-Launches-Scheduling-Optimization-Becoming-the-First-Ambient-AI-OR-Platform-to-Unify-Real-Time-Management-Capacity-Planning-and-Performance-Improvement.html)) and Opmed's Mayo validation, which halved duration error from 1.13 h to 0.56 h ([HIT Consultant](https://hitconsultant.net/2026/06/18/opmed-mayo-clinic-cardiovascular-ai-scheduling/)).

No productized chat agent for OR schedulers surfaced. That is an inference from absence of evidence, not a confirmed market gap. Framing the prototype as "conversational TimeFinder plus write-back" uses Qventus's own vocabulary, and the coordinator persona matches the OR schedulers its releases name as users.

### A booking passes through five teams before the patient reaches the OR

An elective case moves through five stages.

1. **Request.** The surgeon's office scheduler submits a case request, normally electronically. HonorHealth labels its fax version a downtime form and states that it is a booking request, not a pre-op order ([HonorHealth form](https://www.honorhealth.com/sites/default/files/2025-10/surgery-scheduling-fax-request-form.pdf)).
2. **Placement.** The central scheduling office checks the surgeon's privileges, assigns case time from the surgeon's own historical times, and places the case in block or open time. Extensions need approval from the AIC ([UTMC policy 3364-100-53-27](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)).
3. **Confirmation.** Saint Alphonsus issues the **case number at confirmation**, along with the date, time and who scheduled it ([Saint Alphonsus form](https://saintalphonsus.org/sites/default/files/hg_features/mercury_standard_layout/9939b69fdb35876f43bc892c7805e777.pdf)).
4. **Readiness.** At UTMC, financial clearance is due by **noon the day before**, the pre-op evaluation falls 3–30 business days out, chart documentation is due **72 hours** ahead, and vendor implants must reach sterile processing (SPD) **48 hours** ahead. Each of these can postpone the case ([UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)).
5. **Close and day of surgery.** The schedule closes at **2:00 PM the day before**. Later cases become add-ons that need AIC approval, and day-of cases go through the AIC and the OR desk lead (same source).

Two implications follow. The take-home's "surgical scheduling coordinator" is best modeled as the central scheduler who validates and places cases, often acting on office requests. And a booking is not atomic: a case can be scheduled while authorization, workup or implants are still pending. Surgimate makes the same point to its practice customers: a booked case is not a ready case ([Surgimate](https://www.surgimate.com/blog/the-three-moments-when-surgical-coordination-usually-fails/)).

### Eight capabilities separate a credible assistant from a demo

| Capability | What the assistant must do | Evidence |
|---|---|---|
| Availability search that knows block ownership | Label each window as own block, another owner's unreleased block (with release time), released, open, or closed. Prefer the surgeon's own block, because open-time cases do not count toward block utilization. | [UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf); [St. Charles](https://WWW.STCHARLESHEALTHCARE.ORG/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgicalProceduralBlockManagementRedmond-Policy9579.pdf) |
| Case sizing with provenance | Default to the surgeon's historical time for the procedure, add turnover, show where the number came from, and flag overrides that need approval. | [Salem Health](https://salemhealth.org/common-ground-home/common-ground-post/accurate-case-scheduling); [Epic](https://www.epic.com/software/or-capacity/) |
| Capability and resource filtering | Filter rooms by robot, fluoro or other capability. Do not double-allocate shared equipment. | [Qventus Banner](https://qventus.com/resources/customer-successes/banner-health) |
| Staged required-field capture | Ask only for what the current step needs. Capture laterality per procedure line. Never submit an incomplete booking. | [Emory form](https://www.emoryhealthcare.org/-/media/Project/EH/Emory/ui/pdfs/south/wrp-or-scheduling-form-05-2026.pdf) |
| Identity and laterality integrity | Use two patient identifiers, spell laterality out in full, and take codes only from lookups. | [Floyd Health UP policy](https://www.floyd.org/Documents%20Medical%20Staff/PCS-03-003%20Wrong%20Site%20Surgery.pdf) |
| Confirm before commit | Show a structured read-back card, then return a case number, status and who booked it. | [Saint Alphonsus](https://saintalphonsus.org/sites/default/files/hg_features/mercury_standard_layout/9939b69fdb35876f43bc892c7805e777.pdf) |
| Readiness checklist on the booking | List authorization status, PAT, H&P window and the implant/SPD deadline as open items. | [HonorHealth form](https://www.honorhealth.com/sites/default/files/2025-10/surgery-scheduling-fax-request-form.pdf); [UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf) |
| Policy-routed escalation | Send add-ons after the cutoff and urgent cases to the AIC or OR desk, and unreleased-block requests to the block owner. | [UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf) |

Duration needs particular care because the defaults are only moderately accurate. In a WVU orthopedic sample of 326 cases, Epic's prediction was within 30% of actual **77.9%** of the time, against **48.2%** for surgeon estimates, and multi-procedure cases had larger errors ([WVU poster](https://health.wvu.edu/media/18934/42-vincent-melemai-21925.pdf)). The required contiguous time is in-room duration plus turnover; UTMC targets turnover at 30 minutes in the main OR ([UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)).

On intents, a production assistant would also need status lookup, modify/reschedule and cancel (with a mandatory reason). For a 4–6 hour prototype, the true table stakes are:

- check availability;
- book with confirmation;
- clarification and correction;
- escalation, covering urgent cases, add-ons and handoff to a human;
- a waitlist or release-request action for the alternate path.

## Constraints sort into hard blockers, day-of-surgery gates and soft preferences

### Operational rules are local configuration, not constants

Block rules vary widely between hospitals:

- **UTMC** caps blocks at 80% of prime hours and keeps 20% as open time. Blocks auto-cut off at 7:00 AM five business days before surgery, voluntary release must come 14 days ahead, and the utilization goal is 75% ([UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)). The same policy also contains a conflicting second release rule. That inconsistency is itself a reason to treat release rules as editable configuration.
- **St. Charles** auto-releases at 7 calendar days, but **14 days for robotics blocks** ([St. Charles Policy 9579](https://WWW.STCHARLESHEALTHCARE.ORG/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgicalProceduralBlockManagementRedmond-Policy9579.pdf)).
- **HonorHealth** sets release times by specialty, from 0 to 5 working days ([HonorHealth block policy](https://www.honorhealth.com/sites/default/files/2023-03/surgery-block-scheduling-policy.pdf)).
- **Loma Linda** moved outlying elective sites to 21 days because time released later could not be backfilled ([Becker's](https://www.beckershospitalreview.com/or/3-health-system-leaders-on-why-block-utilization-doesnt-tell-the-full-story-and-what-grew-surgical-volume-7/)).

Rooms and equipment are not interchangeable. Loaner instrument sets must reach SPD at least 48 hours ahead, and **first-time vendor sets need 3 business days** ([UTMB](https://www.utmb.edu/policies_and_procedures/20038472)).

People are hard constraints too:

- CMS requires an RN supervising the OR and limits who may scrub and circulate ([42 CFR 482.51](https://www.law.cornell.edu/cfr/text/42/482.51)).
- AORN's position is one RN circulator per patient ([ANA/AORN](https://nursingworld.org/practice-policy/nursing-excellence/official-position-statements/id/one-perioperative-registered-nurse-circulator)).
- An anesthesiologist may medically direct at most **four concurrent cases** for Medicare billing ([Coronis/TEFRA](https://www.coronishealth.com/archive-guidelines-anesthesiologist-hcfa-final-rule-tefra-1198/)).
- The ACS considers truly concurrent surgery inappropriate. Overlapping surgery is acceptable when critical portions don't overlap and the patient is told ([AAHKS summary of ACS](https://www.aahks.org/acs-updates-statement-on-concurrent-surgeries/)).
- AORN says the staffing plan begins when the procedure is scheduled ([AORN](https://www.aorn.org/docs/default-source/guidelines-resources/position-statements/personnel-staffing/posstat-staffingoncall-0721.pdf)), so every booking spreads into staffing.

Downstream capacity matters as well. Schedules that ignore post-op beds cause PACU boarding ([Price et al.](https://www.rti.org/publication/reducing-boarding-post-anesthesia-care-unit)), and re-sequencing an elective schedule was projected to cut expected peak PACU census by **20–30%** on most days ([Lyons et al.](https://citedrive.com/en/discovery/surgery-scheduling-and-perioperative-care-smoothing-and-visualizing-elective-surgery-and-recovery-patient-flow)). Sequencing preferences, such as booking latex-allergic patients as the first case, are real but rest on facility standards; the clearest source found is Canadian ([Northern Health/CPSBC](https://www.cpsbc.ca/files/pdf/NH-AS-Latex-Allergy.pdf)).

Dexter's ordered priorities for day-of decisions are patient safety, then reducing over-utilized time, then reducing waiting, then personal preferences ([Dexter et al., 2007](https://user.engineering.uiowa.edu/~csl/publications/pdf/2007%20Dexter%20Anethesiologist%20Decisionmaking%20Anesthesia.pdf)). That ordering is the most defensible basis for separating hard constraints from soft ones.

### Regulation makes booking accuracy a safety duty and keeps the assistant administrative

**CMS surgical-services rules.** The Conditions of Participation require a roster of each practitioner's surgical privileges. They require an H&P no more than 30 days before or 24 hours after admission, with an update if it was done earlier, plus signed informed consent before surgery and a complete OR register ([42 CFR 482.51](https://www.law.cornell.edu/cfr/text/42/482.51)).

**Universal Protocol.** Verification of patient, procedure, site and laterality starts at scheduling. One hospital policy has the scheduling clerk verify the procedure, including site-specific identification, when the case is scheduled ([Floyd Health](https://www.floyd.org/Documents%20Medical%20Staff/PCS-03-003%20Wrong%20Site%20Surgery.pdf)). An assistant that garbles laterality creates exactly the discrepancy the Protocol exists to catch.

**HIPAA.**

- HHS cloud guidance treats a provider that stores ePHI as a business associate even when the data is encrypted and the provider holds no key ([Hunton](https://www.hunton.com/privacy-and-cybersecurity-law-blog/hhs-releases-guidance-hipaa-cloud-computing)). An LLM vendor that retains prompts or logs therefore needs a BAA, giving the chain hospital → Qventus → LLM provider.
- Enterprise LLM tiers reportedly support BAAs; consumer endpoints do not ([Medcurity](https://medcurity.com/hipaa-compliance-generative-ai/)).
- Audit controls under 45 CFR 164.312(b) are a required standard ([AFS Law](https://www.afslaw.com/perspectives/health-care-counsel-blog/proposed-changes-the-hipaa-security-rule-what-regulated)).
- The proposed Security Rule overhaul is not final. Final action is now projected for **July 2027** ([McDermott](https://www.mcdermottlaw.com/?p=50371417)).

**Device status.** The Cures Act excludes software for administrative support, explicitly including **appointment schedules**, from the FDA device definition ([21 U.S.C. 360j](https://www.law.cornell.edu/uscode/text/21/360j)). That holds only while the assistant stays out of clinical calls such as assigning urgency class, judging fitness for surgery, or choosing procedures. FDA revised its CDS guidance in January 2026 ([Covington](https://www.cov.com/en/news-and-insights/insights/2026/01/5-key-takeaways-from-fdas-revised-clinical-decision-support-cds-software-guidance)), which moves that boundary.

**Governance guidance.** The Joint Commission and CHAI guidance of September 2025 is non-binding, but it explicitly covers scheduling tools. It asks for governance, disclosure, monitoring with human-in-the-loop review, and AI safety-event reporting ([Parker Poe](https://parkerpoe.com/news/2025/11/new-national-guidance-lays-out-responsible-use-of)). ONC's HTI-1 source-attribute ("model card") duties bind certified EHR developers, not a third-party assistant. HTI-5 proposes removing them, and its final status is unconfirmed ([Covington](https://www.covingtonblogs.com/2026/01/15/hhs-proposes-changes-to-the-health-it-certification-program-and-information-blocking-regulations-in-hti-5-proposed-rule/)).

**State AI laws.** These mostly reach patient-facing output, so a staff-facing assistant largely sits outside them until it sends patient confirmations.

- California AB 3030 covers generative-AI patient communications ([Arent Fox Schiff](https://www.afslaw.com/perspectives/alerts/california-requires-disclaimers-health-care-providers-ai-generated-patient-communications)).
- Texas TRAIGA has required disclosure of AI use in services since January 2026 ([Akerman](https://www.akerman.com/en/perspectives/hrx-new-year-new-ai-rules-healthcare-ai-laws-now-in-effect.html)).
- Colorado's replacement law, SB 26-189, takes effect January 1, 2027 ([Mayer Brown](https://www.mayerbrown.com/insights/publications/2026/05/colorado-enacts-new-admt-law-replacing-colorado-ai-act)).

**Prior authorization.** Since January 1, 2026, CMS-0057-F requires Medicare Advantage, Medicaid, CHIP and Marketplace payers to decide in **72 hours (expedited) or 7 calendar days (standard)** ([ASPR CMS Solutions](https://asprcmsolutions.com/insights/cms-0057-f-prior-authorization-api-deadline-2026/)). Booking date and authorization clock therefore interact.

### Public EHR interfaces let an assistant read the OR schedule, not write it

Epic's public catalog lists an **outbound-only** "Outgoing Surgical Case Scheduling" HL7v2 interface and an inbound case-*tracking* interface. It lists no public inbound surgical-case scheduling interface ([open.epic HL7v2](https://open.epic.com/Scheduling/HL7v2)). Epic calls its FHIR scheduling services prototypes ([open.epic FHIR](https://open.epic.com/Scheduling/FHIR)). Epic-on-FHIR surgery resources such as "Appointment.Search (Scheduled Surgeries)" appear as read and search only ([Vital](https://vital.io/help/en/articles/15863078-epic-on-fhir-application)). One developer guide reports proprietary endpoints that return HTTP 200 with an error, such as slot already taken, in the body ([Mindbowser](https://www.mindbowser.com/epic-scheduling-api-guide/)). Oracle's Millennium Appointment create requires exactly one Slot reference for a booked status ([Oracle](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/op-appointment-post.html)). Real two-way OR integrations take time: a University of Colorado two-way QGenda–OpTime feed was set up but not yet live ([CU](https://www.cu.edu/print/controller/i-e-awards/past-submissions/cu-ie-submission-qgenda)).

The realistic write paths, in order of feasibility, are:

1. a structured case request that a human finalizes in the EHR;
2. a site-approved Epic integration;
3. a Qventus-owned scheduling layer with outbound sync.

For the take-home, that justifies a mocked scheduling service with explicit hold, confirm and cancel calls, typed errors, re-validation at commit, and an outbound event stream modeled on HL7 SIU S12/S14/S15 ([Rhapsody](https://rhapsody.health/resources/hl7-siu-message/)). FHIR Appointment statuses (proposed, pending, booked, waitlist, cancelled) give a standard vocabulary for case state ([HL7 FHIR R4](https://hl7.org/fhir/R4/appointment.html)). The research notes rest the read-only conclusion on Epic's "prototype" language plus a third-party API listing, not on Epic's login-gated specs. It is strong but not certain.

### Language models follow written policy unreliably and invent codes

On τ-bench, a set of airline and retail booking tasks with policy documents, GPT-4o completed fewer than half the tasks. Its **pass^8 fell below 25%** in retail, and agents often failed to follow written policies ([Sierra](https://sierra.ai/blog/benchmarking-ai-agents)). On clinical coding, GPT-4 reproduced exact **CPT codes only 49.8%** of the time and ICD-10-CM codes 33.9%, sometimes fabricating codes ([Healthcare IT News on NEJM AI](https://www.healthcareitnews.com/news/llms-are-not-ready-automate-clinical-coding-says-mount-sinai-study)). These are 2024-generation models without tool grounding, so current models are likely better, but the design lesson holds.

Two framework details matter here:

- **Structured outputs** guarantee that responses match the schema, not that they are accurate. Claude's strict schemas cannot enforce numeric minimums or maximums, so range checks belong in code ([Claude docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)).
- **LangGraph interrupts** re-run the node from the start on resume, so any side effect before an approval pause must be idempotent ([LangGraph](https://docs.langchain.com/oss/python/langgraph/interrupts)).

The consequences for the design are:

- hard rules live in code, not in the prompt;
- write tools accept only IDs returned by lookup tools;
- the confirmation card is rendered from structured state, not from LLM prose;
- every write carries an idempotency key;
- free-text EHR notes are treated as data, never as instructions;
- conversation logs are treated as ePHI.

### How each constraint should behave

The classification below is a synthesis, not a published standard. Individual hospitals harden some soft items; some refuse to book without prior authorization, for example.

| Constraint | Class | Assistant behavior | Basis |
|---|---|---|---|
| Room double-booked (case plus turnover overlap) | Hard | Never book; offer alternatives | [UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf) |
| Surgeon in overlapping rooms without an approved flip pattern | Hard | Block; escalate flip-room requests | [ACS via AAHKS](https://www.aahks.org/acs-updates-statement-on-concurrent-surgeries/) |
| Room lacks required capability; shared robot or C-arm over-allocated | Hard | Filter out; offer other times or rooms | [St. Charles](https://WWW.STCHARLESHEALTHCARE.ORG/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgicalProceduralBlockManagementRedmond-Policy9579.pdf) |
| Surgeon not privileged for the procedure | Hard | Block; route to medical staff office | [42 CFR 482.51](https://www.law.cornell.edu/cfr/text/42/482.51) |
| Patient identity not confirmed by two identifiers | Hard | Ask; never pick among matches | [Floyd Health](https://www.floyd.org/Documents%20Medical%20Staff/PCS-03-003%20Wrong%20Site%20Surgery.pdf) |
| Laterality or spinal level missing, or in conflict with the order | Hard | Ask or escalate; spell out in full | [Floyd Health](https://www.floyd.org/Documents%20Medical%20Staff/PCS-03-003%20Wrong%20Site%20Surgery.pdf) |
| Procedure or CPT not resolved from the master list | Hard | Lookup only, never generated | [NEJM AI via HIT News](https://www.healthcareitnews.com/news/llms-are-not-ready-automate-clinical-coding-says-mount-sinai-study) |
| Slot in another owner's unreleased block | Hard (local policy) | Show release time; offer waitlist or release request | [UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf) |
| Write without explicit confirmation | Hard (product) | Structured read-back card every time | [TJC/CHAI via Parker Poe](https://parkerpoe.com/news/2025/11/new-national-guidance-lays-out-responsible-use-of) |
| PHI sent to a non-BAA service; unaudited write | Hard (compliance) | Architectural control | [Hunton](https://www.hunton.com/privacy-and-cybersecurity-law-blog/hhs-releases-guidance-hipaa-cloud-computing) |
| Day-before cutoff passed, or urgent/emergent case | Hard routing | Convert to add-on or escalate to AIC/OR desk; never auto-book | [UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf) |
| Anesthesia ratio or specialty staffing exceeded | Hard, escalate | Mark pending; route to anesthesia scheduler or charge RN | [Coronis/TEFRA](https://www.coronishealth.com/archive-guidelines-anesthesiologist-hcfa-final-rule-tefra-1198/) |
| Loaner/implant set inside 48 h (3 business days if first-time) | Hard on day of surgery, soft at booking | Book with risk flag and SPD/vendor task, or escalate | [UTMB](https://www.utmb.edu/policies_and_procedures/20038472) |
| H&P older than 30 days, consent missing | Hard on day of surgery, soft at booking | Book and create readiness task | [42 CFR 482.51](https://www.law.cornell.edu/cfr/text/42/482.51) |
| Prior authorization not approved | Hard on day of surgery (financial), soft at booking | Book and flag payer decision clock | [ASPR CMS Solutions](https://asprcmsolutions.com/insights/cms-0057-f-prior-authorization-api-deadline-2026/) |
| Post-op ICU or inpatient bed | Soft, escalate | Flag; route to bed management | [Price et al.](https://www.rti.org/publication/reducing-boarding-post-anesthesia-care-unit) |
| Case runs past staffed hours | Soft, escalate | State overrun minutes; require approval | [JAMA Surg 2026](https://www.citedrive.com/en/discovery/costs-charges-and-revenue-of-hospital-operating-rooms-in-california/) |
| Latex-first and similar sequencing rules | Soft (policy preference) | Prefer; surface conflicts | [CPSBC](https://www.cpsbc.ca/files/pdf/NH-AS-Latex-Allergy.pdf) |
| Fill own block before open time; utilization | Soft (metric) | Rank own block first; show utilization | [UTMC](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf) |
| Bumping an elective case for an add-on | Not the assistant's decision | Always escalate | [Dexter et al.](https://user.engineering.uiowa.edu/~csl/publications/pdf/2007%20Dexter%20Anethesiologist%20Decisionmaking%20Anesthesia.pdf) |

## Value reaches two users directly but pays out in $57.71 OR minutes

Only two people talk to the assistant: the central coordinator and, in a clinic-facing variant, the surgeon's office scheduler. Everyone else benefits through the quality of the booking it produces. The pains are well documented in kind but poorly quantified:

- **Coordination load.** One trade piece describes a fully engaged scheduler exchanging more than 40 messages per case with assistants, OR managers, vendors, anesthesia and authorization teams ([Becker's Spine Review](https://www.beckersspine.com/orthopedic-spine-practices-improving-profits/7-common-causes-of-inefficient-orthopedic-and-spine-case-scheduling/)).
- **Paper and phone channels.** Faxes, paper forms, phone calls and spreadsheets persist even at large hospitals ([LeanTaaS](https://surgical-clinics.leantaas.com/?p=3084)). Stony Brook still invites faxed bookings ([Stony Brook](https://www.stonybrookmedicine.edu/node/658)). Qventus describes Erlanger's clinic schedulers before deployment as spending hours on calls and faxes while independent surgeons took cases to competitors ([Qventus Erlanger blog](https://www.qventus.com/resources/blog/how-erlanger-adds-220-surgical-cases-per-month-with-ai-powered-surgical-operations/)).
- **Inaccurate durations.** Across 46,986 surgeries, the institutional estimate landed within ±10% of actual for only **32%** of cases ([Bartek et al., JACS 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC7077507)).
- **Cancellations from booking errors.** At Tulane, 6.7% of elective outpatient cases were cancelled on the day, and about a third of those stemmed from hospital-side problems such as scheduling errors that left equipment or beds missing ([Advisory Board](https://www.advisory.com/daily-briefing/2012/05/09/same-day-surgery-cancellations-cost-hospitals-millions)).

| Stakeholder | Pain today | What the assistant changes | KPIs that show it |
|---|---|---|---|
| Central OR scheduling coordinator (primary user) | Searches several views for time; 40+ messages per case; re-keys faxed requests; chases missing fields | One plain-language search across own, released and open time with equipment filters; pre-filled booking; targeted prompts for missing fields; conflict checks; audit trail | Minutes from request to confirmed booking; touches per case; first-pass completeness; edits after booking |
| Surgeon office or clinic scheduler (requester) | Hunts for time outside own block by phone and fax; requests bounced for missing data | Self-serve availability and instant holds (the Clinic Scheduler Assistant analog) | Lead time from decision to date; % of requests returned; release lead time |
| Surgeon | Can't see time outside own block; risks losing block at low utilization | Released and open time visible; robot availability at booking | Lead time to surgery; cases booked outside own block |
| Perioperative director / OR manager | Late release; released time left unfilled; overruns from bad durations | Faster pickup of released time; durations with provenance; structured booking data for block reviews | Released-time pickup rate; prime-time utilization; overtime minutes; cases per OR per month |
| Anesthesia, AIC, OR desk | Late add-ons; missing anesthesia type; day-of surprises | Anesthesia type and safety flags captured at booking; urgent cases arrive as structured handoffs | First-case on-time starts; day-of changes; overtime |
| SPD, PAT, bed management | Learn about implants, workups and beds too late | Readiness checklist and notification tasks created at booking | % of cases PAT-complete by T-72h; equipment-related delays; cancellations |
| CFO / COO | Paying for idle staffed minutes; volume leaking to competitors | More cases in existing capacity; fewer cancellations caused by booking errors | Incremental cases × contribution margin; idle minutes × cost per minute; ROI and payback |
| Patient (indirect) | Waits for callbacks; day-of cancellation | Faster, more accurate confirmation | Days to surgery; same-day cancellation rate |

### KPIs should run from workflow speed to margin, with definitions stated

The KPIs fall into three tiers.

**Workflow (leading).** These are time-to-book, touches per case and first-pass completeness. No public benchmark exists for them, so the prototype must define its own. Qventus's 22-minute median clinic booking turnaround is the closest anchor ([Qventus, May 2025](https://www.qventus.com/company/newsroom/qventus-ai-teammates-transform-the-perioperative-care-journey-driving-strategic-surgical-growth-and-winning-several-new-clients-and-enterprise-wide-expansions/)).

**Operational.**

- *Block and prime-time utilization.* Consultants suggest starting at 70% block utilization, moving to 75–80%, with an 80% prime-time goal over roughly 7:30–3:30 ([Impact Advisors](https://impact-advisors.com/article/surgical-block-utilization)). Whether utilization is "adjusted" to include turnover changes the result a lot: a tonsillectomy surgeon can score 50% raw and 100% adjusted ([OR Manager](https://www.ormanager.com/wp-content/uploads/pdfx/001/ORMVol20No11blockTime.pdf)). Utilization is also a noisy basis for judging low-volume surgeons ([Dexter et al., 2003](https://healthpolicy.fsi.stanford.edu/publications/operating_room_utilization_alone_is_not_an_accurate_metric_for_the_allocation_of_operating_room_block_time_to_individual_surgeons_with_low_caseloads)).
- *Released-time pickup rate.* Inova reports **46%** ([Becker's](https://www.beckershospitalreview.com/hospital-management-administration/inside-inovas-46-release-fill-rate-turning-open-or-time-into-more-cases/)) and Providence **34%** ([Becker's](https://www.beckershospitalreview.com/finance/a-matter-of-or-minutes-health-systems-notch-big-financial-wins-with-ai.html)). Qventus benchmarks 50% use of early-released block ([Qventus Solution Brief](https://qventus.com/wp-content/uploads/2024/10/Qventus_Solution-Brief_Perioperative.pdf)).
- *Duration accuracy* and *same-day cancellations attributable to booking errors.*

**Financial.** Incremental cases times contribution margin, plus idle staffed minutes times cost per minute.

### The economics favor filling time over saving keystrokes

The newest peer-reviewed benchmark puts the cost of an OR minute at **$57.71 in FY2022**, up 54% from FY2014. Revenue is **$66.31** per minute and charges are **$295.09**, based on 278 California hospitals ([Ashrafi, Maggard-Gibbons & Childers, JAMA Surgery 2026](https://www.citedrive.com/en/discovery/costs-charges-and-revenue-of-hospital-operating-rooms-in-california/)). The widely quoted $36–37 figure is FY2014 cost ([Childers & Maggard-Gibbons, 2018](https://pmc.ncbi.nlm.nih.gov/articles/5875376)), and charges should never be presented as value.

An added elective case is worth about **$4,090** in contribution margin by Surgical Directions' benchmark ([Becker's](https://www.beckershospitalreview.com/strategy/how-to-rebuild-surgical-revenue-after-covid-19-even-if-you-just-lost-60-of-your-or-volume.html)). Qventus assumes **$5,000** ([Qventus eBook](https://www.qventus.com/wp-content/uploads/2026/02/Qventus-eBook-35MProblem-SurgicalLeakage-1.pdf)). Its own Midwest AMC figures, 391 added cases per month and $18.3M annualized margin, work out to roughly $3,900 per case, which is consistent ([Qventus Midwest AMC](https://www.qventus.com/wp-content/uploads/2025/06/Qventus-Midwest-AMC-CaseStudy.pdf)). Case mix still matters: one Stanford analysis found negative contribution margin per OR hour for 26% of elective cases ([Stanford Health Care](https://stanfordhealthcare.org/publications/307/307429.html)).

Tulane's day-of cancellations cost **$1,325–$5,962 per case** by specialty, in 2009 dollars ([Advisory Board](https://www.advisory.com/daily-briefing/2012/05/09/same-day-surgery-cancellations-cost-hospitals-millions)). At the system level, the OR is credited with about 40% of hospital revenue ([UChicago](https://hdsi.uchicago.edu/project/a-strategic-plan-for-optimizing-the-surgical-case-mix/)) and up to 65% of margin ([Becker's](https://www.beckershospitalreview.com/strategy/how-to-rebuild-surgical-revenue-after-covid-19-even-if-you-just-lost-60-of-your-or-volume.html)).

An illustrative model for a value slide, using a 20-OR hospital with 480 prime-time minutes per room per day over 250 days (2.4M minutes a year):

- **One point of prime-time utilization** is 24,000 minutes. That is about **$1.4M** of staffed cost put to productive use, or **$1.6M** of revenue.
- **One extra case per OR per month** is 240 cases a year, worth **$1.0–1.2M** in contribution margin.
- **Scheduler time** is small by comparison. One OR hour carries about $3,460 of staffed cost, so the assistant's real economic lever is filling released time sooner and with better-fit cases, not saving scheduler minutes.

### Every outcome claim in this market is vendor-reported

The evidence base is thin, and the write-up should say so.

- Qventus reports **+220 cases per month** at Erlanger, where **98 surgeons booked directly from a nudge** in six months. Its 5x ROI figure there is a projection, not a realized result ([Business Wire](https://businesswire.com/news/home/20260203913068/en/Erlanger-Health-System-Achieves-Strong-Results-in-Robotic-Access-and-OR-Capacity-with-Qventus-On-Track-to-Deliver-5x-Annualized-ROI)).
- At Banner: **369 hours per month** of block released early, **+6.3%** prime-time utilization and 7x ROI ([Qventus Banner](https://qventus.com/resources/customer-successes/banner-health)).
- Across its 2025 perioperative clients: 135K block-release hours and 10x average ROI ([Qventus, Sept 2025](https://www.qventus.com/company/newsroom/qventus-drives-next-wave-of-healthcare-ai-innovation-with-debut-of-ai-solution-factory-and-releases-new-roi-outcomes-from-health-systems/)).

All of these are uncontrolled before/after or year-over-year comparisons, and all bundle nudges, outreach, a booking UI and analytics. None isolates the effect of a conversational interface. OR-management research adds a caution: when time is released matters much less than getting block allocation right in the first place ([Dexter, AORN](https://www.aorn.org/outpatient-surgery/article/2005-April-drawing-up-winning-schedule)).

The honest claim for a chat assistant is narrow: it moves workflow metrics directly, and utilization and margin are downstream hypotheses. A pilot design would capture 2–4 weeks of baseline timestamps (request received to booking confirmed), calls and messages per case, and the share of requests needing follow-up. It would then repeat the measurement with the assistant, tracking same-day cancellations from booking errors as a lagging guardrail. The research found no peer-reviewed US time-and-motion study of OR booking, so such a pilot would fill a real gap.

## The best stretch goals mirror assistants Qventus already sells

The strongest stretch goals reuse the extractor, validators and tool layer the core flow already needs, and tie directly to a named Qventus product. Machine-learning components belong behind the same tool interfaces as swappable stubs, because the peer-reviewed gains are real but modest. A randomized trial at Memorial Sloan Kettering cut duration MAE by **16.5%** (59.3 to 49.5 minutes) and next-patient wait time by **67%** ([Strömblad et al., JAMA Surgery 2021](https://jamanetwork.com/journals/jamasurgery/article-abstract/2775620)). A scoping review, however, found only one RCT among 14 studies and only one external validation, and noted that models predicted a day ahead while scheduling needs predictions weeks ahead ([Spence et al., BJS Open 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10630142/)). Cancellation-risk models reach AUCs around 0.72–0.83. At one cutoff, a 24-hour model had an NPV of 0.96 but a **PPV of only 0.21**, so acting on its flags automatically would be wrong four times in five ([Mahidol repository](https://repository.li.mahidol.ac.th/items/62c8d49e-c07b-4f18-a65e-9d06b68100a0/full)). Block-release prediction is backed only by vendor content, including Qventus's own ([Qventus blog](https://qventus.com/3-ways-machine-learning-can-optimize-your-operating-room-utilization/)).

| Stretch goal | Qventus or market anchor | Build or describe | Why it earns its place |
|---|---|---|---|
| Fax or email booking request parsed into the same slot schema | Document Assistant (~60 scheduler hours/month); Premier Southern reported 60% less manual time per fax ([Qventus, Sept 2025](https://www.qventus.com/company/newsroom/qventus-drives-next-wave-of-healthcare-ai-innovation-with-debut-of-ai-solution-factory-and-releases-new-roi-outcomes-from-health-systems/)) | Build | Reuses the extractor and validators; dramatizes the phone-and-fax pain |
| Policy Q&A with section citations | Rubric credit for RAG; Contextual Retrieval cut retrieval failures 49% with hybrid search and 67% with reranking ([Anthropic](https://www.anthropic.com/news/contextual-retrieval)) | Build small | Hard rules run in code, and the same rules exist as cited chunks so the assistant can explain a refusal |
| Duration range (P50/P80) with provenance and an override flag | TimeFinder predicts length from surgeon history; Epic shows a confidence score ([Epic](https://www.epic.com/software/or-capacity/)) | Build (stub) | Cheap; shows awareness of uncertainty and that overrun risk is a soft constraint |
| Waitlist, notify-on-release and request-release flow | Capacity Assistant and Strategic Marketing Assistant; Epic Marketplace notifications | Build simple | Turns the alternate path into a released-time fill story |
| Readiness checklist with payer clock and tray deadlines | Perioperative Care Coordination's 72-hour cancellation focus ([Qventus PCC](https://www.qventus.com/company/newsroom/qventus-launches-perioperative-care-coordination-solution-to-alleviate-the-administrative-burden-on-clinicians-reduce-unnecessary-surgery-cancellations-and-optimize-patients-pre-and-post-surgery/)); CMS-0057-F | Build simple | Makes "booked is not ready" visible |
| Scenario eval harness with pass^k and a 100% safety gate | τ-bench and τ²-bench ([arXiv 2506.07982](https://arxiv.org/pdf/2506.07982)); CareConnect's 680-scenario benchmark | Build | Demonstrates reliability rather than one lucky demo |
| Tracing and audit log (OpenTelemetry / Langfuse) | 45 CFR 164.312(b); TJC/CHAI monitoring ([Langfuse](https://langfuse.com/resources/engineering/opentelemetry-languages)) | Build cheap | Serves compliance and debugging in one move |
| Modify and cancel, with re-authorization flag and mandatory reason | HonorHealth re-auth rule; UTMC cancellation-reason rule | Build if time | Completes the case lifecycle |
| Clinic-side persona with scoped permissions | Clinic Scheduler Assistant; West Tennessee's 61 independent-surgeon cases in 100 days ([Qventus, May 2025](https://www.qventus.com/company/newsroom/qventus-ai-teammates-transform-the-perioperative-care-journey-driving-strategic-surgical-growth-and-winning-several-new-clients-and-enterprise-wide-expansions/)) | Describe, or a second persona | Same engine, different role-based access |
| ML duration model, block-release prediction, CP-SAT schedule optimization, cancellation-risk model | Strömblad RCT; Qventus block prediction; OR literature | Describe | Needs real data; evidence is modest or vendor-only |
| Real EHR write-back via case-request queue or site-approved interface, plus SIU events | Qventus enhanced write-back; [open.epic](https://open.epic.com/Scheduling/HL7v2) | Describe | Site- and vendor-dependent |
| Voice channel or patient-facing confirmations | PCC voice capabilities | Describe | Triggers AB 3030 and TRAIGA disclosure duties |

The eval harness deserves priority over most features. τ-bench's pass^k measures the probability that an agent succeeds on *every* one of k trials, and that score dropped sharply with k for all agents tested ([arXiv 2406.12045](https://arxiv.org/pdf/2406.12045)). Amazon's τ²-Bench-Verified found original tasks misaligned with their own policies, a reminder that eval labels need auditing too ([GitHub](https://github.com/amazon-agi/tau2-bench-verified)). The closest academic analog is CareConnect, a 2026 preprint on an appointment-logistics agent built from function calling, RAG and layered deterministic guardrails. It reported **91.8% task completion**, **96.0% safety compliance** and $0.0324 per appointment, on its authors' own benchmark rather than a live deployment ([arXiv 2607.05055](https://arxiv.org/pdf/2607.05055)). Those metric categories (completion, safety compliance, latency, cost) are a ready-made results table for the write-up.

## Recommendations: book a robotic right knee and route around an unreleased block

*Everything in this section is a recommendation synthesized from the evidence above, not a reported finding.*

### Recommended framing

The user is a central OR scheduling coordinator at a fictional two-campus US health system that runs an Epic-like system of record. She acts on a request phoned or faxed in by Dr. Priya Patel's orthopedic office. The case is a **robotic-assisted right total knee arthroplasty**, chosen because it exercises every table-stakes capability in one realistic request:

- laterality (Universal Protocol);
- a capability-constrained room (robot), echoing Qventus's robotics emphasis;
- duration from surgeon history;
- block ownership with the 14-day robotics release rule seen at St. Charles;
- an implant vendor tray (SPD deadline);
- prior authorization.

Freeze the simulated clock at **Wednesday, October 14, 2026, 09:00** so tests are deterministic, and target the week of **Monday, November 2**. The synthetic data should cover:

- eight rooms, two of them robot-capable;
- two weeks of block templates;
- five surgeons with privilege lists;
- about ten procedures in a master list with default equipment;
- a history CSV of case durations;
- two patients named "Maria Gomez" with different dates of birth, to force disambiguation;
- three to five short policy documents (block release, add-ons and urgent cases, robot room eligibility, implant and loaner rules, pre-op readiness).

If time is short, a non-robotic knee arthroscopy keeps the same flow with one fewer constraint.

### The happy path in six turns

| Turn | Coordinator | Assistant and system behavior |
|---|---|---|
| 1 | "Can you find time next week for Dr. Patel, robotic right total knee?" | Routes to `check_availability`. Resolves the surgeon (one match) and the procedure from the master list (robot required). Records laterality as **Right**. Estimates duration from 14 prior cases: P50 112 min, P80 135 min, plus 30 min turnover, shown with provenance. |
| 2 | (none) | Returns three ranked options: Tue Nov 3, OR 5, Patel's own robotic block, 12:30–15:00 free (fits at P50; at P80 it would run 15 min past block end, flagged as a soft overrun). Wed Nov 4, OR 6, Urology robotics block, **auto-releases Wed Oct 21 07:00**, not bookable now. Thu Nov 5, OR 6, open time 07:30–10:30, fits. Notes that the own-block option counts toward Patel's utilization. |
| 3 | "Take Tuesday." | Asks only for booking-stage fields: patient, anesthesia type, patient class, diagnosis. Patient search on name alone returns two matches, so it asks for date of birth. |
| 4 | "DOB 3/12/1958, general plus block, outpatient." | Resolves the MRN and pulls the diagnosis from the surgeon's order. Renders a structured confirmation card from validated state: patient (name, DOB, MRN), procedure with **Right** spelled out, surgeon, room, date and time, duration and source, implant vendor tray required. |
| 5 | "Confirm." | Places a hold, re-checks availability and resource conflicts, then confirms with an idempotency key. Returns case number, status Scheduled, and who booked it. |
| 6 | (none) | Attaches the readiness checklist: prior auth **pending** (for a Medicare Advantage payer, submit by about Oct 26 to clear a 7-day standard decision before the noon Nov 2 financial-clearance cutoff); H&P must be dated on or after Oct 4; chart due by Oct 31 12:30; loaner tray in SPD by Nov 1 12:30 (by Oct 29 if it is a first-time set); vendor rep task created. Emits notifications to the office, PAT and SPD. |

### Alternate and failure paths

| Path | Trigger | Assistant behavior | Escalation owner |
|---|---|---|---|
| **Alternate (required): unreleased block** | Coordinator says the patient can only do Wednesday | Refuses to book into Urology's block (`BLOCK_NOT_RELEASED`), shows the Oct 21 release time, and offers Patel's next own robotic block, Thursday open time, notify-on-release, or a release request to the block owner | Urology office scheduler / block owner |
| **Failure: race at commit** | A second coordinator takes the Tuesday window between search and confirm (a demo toggle) | Commit-time re-check returns `SLOT_TAKEN`. The assistant re-queries and re-offers. The idempotency key prevents a duplicate case on retry. | None |
| **Failure and escalation: urgent or add-on** | "Dr. Patel's partner needs a room tonight for an open tibia fracture," or a next-day request after the 2:00 PM close | Does not book, does not assign an urgency class, and does not decide who gets bumped. Creates a structured handoff (surgeon, procedure, laterality, requested timing, contact) and tells the coordinator to call the OR desk | AIC / OR desk lead |
| **Failure: identity or laterality** | Two patient matches, missing laterality, or the coordinator says left while the order says right | Asks; never chooses. Stops on conflict with the order. After 2–3 failed attempts, hands off with the draft case and transcript | Human scheduler |
| Optional: not privileged | Surgeon lacks robotic privileges | `NOT_PRIVILEGED`: blocks and routes | Medical staff office |
| Optional: tray deadline | Booking falls inside 48 h of a case needing a loaner set | Books with a risk flag, or escalates per policy | SPD / vendor |

### Candidate intents and entities

| Intent | Example utterance | Prototype status |
|---|---|---|
| `check_availability` | "Two and a half hours for Patel next week, robot room" | Core |
| `book_case` (select option, supply fields, confirm) | "Take the Tuesday slot" | Core |
| `provide_or_correct_info` | "Sorry, it's the right knee, not left" | Core |
| `request_waitlist_or_release` | "Tell me if Wednesday opens up" | Core (alternate path) |
| `escalate_urgent_or_add_on` | "This needs to go tonight" | Core (escalation path) |
| `handoff_to_human` | "Get me the OR desk" | Core |
| `out_of_scope_clinical` | "Is she fit for general anesthesia?" | Core (decline and route) |
| `policy_question` | "When do robotic blocks release?" | Stretch (RAG) |
| `get_case_status` | "Is the Gomez case confirmed?" | Stretch (cheap) |
| `modify_case` / `cancel_case` | "Move it to Thursday" / "Cancel, patient declined" | Stretch |

| Stage | Entities | Handling rule |
|---|---|---|
| Needed to search | Surgeon; procedure (free text mapped to a master ID); laterality; duration (defaults to surgeon history); date window and time of day; campus; room capability (robot, fluoro); patient class | Surgeon and procedure resolve only via lookup tools; ambiguous names return candidates for the user to pick |
| Needed to book | Patient (name plus DOB, resolved to MRN); diagnosis (from order); anesthesia type; admission type; selected `slot_id`; implants and vendor | Write tools accept only IDs returned earlier in the session |
| Conditional | Assistant or co-surgeon; additional procedure lines; spinal level; bed type; latex allergy; isolation; interpreter; authorization status and number; PAT type; urgency (captured, never assigned); change or cancel reason; case number | Laterality is per procedure line; any change to CPT, location or class flags re-authorization |

### Architecture and mock API shape

Use the workflow pattern rather than a free-roaming agent, consistent with Anthropic's advice to prefer predefined code paths and add complexity only when needed ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents)), and with Rasa CALM's split, where the LLM emits commands and flows execute the business logic ([Rasa](https://rasa.com/docs/learn/concepts/calm/)).

- **One extraction call per turn.** A strict-schema call returns intent, slots, corrections and ambiguities.
- **A deterministic state machine** (route → collect → validate → search → present → confirm → commit, with clarify, policy-QA and escalate side states) owns every rule.
- **Escalation counters per slot.** After 2–3 failed attempts on a slot, the flow escalates, mirroring Dialogflow CX's per-slot reprompt events ([Google Cloud](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-dialogflow-cx-v3/latest/Google-Cloud-Dialogflow-CX-V3-Form-Parameter-FillBehavior)).
- **Mock scheduling service.** It exposes `lookup_surgeon`, `lookup_procedure`, `lookup_patient`, `estimate_duration`, `search_availability` (returns opaque `slot_id`s with ownership state and release time), `place_hold` (short TTL), `confirm_booking` (idempotency key, re-check), `get_case`, `cancel_case`, `join_waitlist`, `request_block_release`, `create_escalation` and `search_policy`.
- **Typed errors.** These include `SLOT_TAKEN`, `HOLD_EXPIRED`, `BLOCK_NOT_RELEASED`, `RESOURCE_CONFLICT`, `PAST_CUTOFF`, `NOT_PRIVILEGED` and `MISSING_REQUIRED_FIELD`. The dialogue layer turns each into an alternative or an escalation.
- **Integration seam.** The service should emit SIU-style events and keep FHIR-like case statuses, so the write-up can show exactly where a real Epic case-request queue or site-approved interface would plug in.

### What to measure in the demo

Report the following, defining each metric in the write-up:

- time-to-book and turns-to-book on the happy path;
- first-pass completeness;
- per-field slot accuracy;
- escalation correctness on the urgent path;
- pass^k over 15–25 scripted and simulated scenarios.

Hold two safety metrics at 100%: zero commits without confirmation and zero bookings that violate a hard rule. Then translate the workflow gains into the hospital-level model above, stating plainly that utilization and margin are downstream hypotheses, not demonstrated effects.

## Conclusion

The chat interface is not where this prototype stands out. Qventus's CEO said in September 2026 that "building an agent is easy" and that operationalizing it is the hard part ([HonorHealth release](https://finance.yahoo.com/healthcare/articles/honorhealth-selects-qventus-ai-solution-130000232.html)). The evidence here says the same thing. What distinguishes a credible OR booking assistant is three things a generic agent gets wrong: it knows who owns a minute and when that changes, it refuses to let a model invent identifiers or laterality, and it states openly that a booked case is not yet a ready one. Each comes from a hospital policy, a federal rule or a measured LLM failure mode, and each can be shown in a few hours with a mocked backend.

The research also shifts how to argue value. Vendor case studies credit block-release and booking tools with hundreds of added cases, but none isolates the booking interface. The economics show that scheduler minutes are trivial next to an OR hour that costs about $3,460 to staff. The persuasive pitch to Qventus is therefore not "this saves coordinators time." It is a system that books correctly, escalates the right things to the right human, and measures its own reliability. That same system becomes the fastest way to put released time back to work, which is the outcome Qventus's whole perioperative line is built to sell.
