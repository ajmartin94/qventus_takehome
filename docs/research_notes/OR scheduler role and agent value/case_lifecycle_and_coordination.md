# Surgical Case Lifecycle After Booking: Changes, Coordination Traffic, Day-of Execution, and the Communication Network (US hospitals)

Research date: 2026-10-14. This file covers what happens to a case after it is booked: changes, chasing, readiness, schedule close, day-of execution, and who talks to whom. It does not repeat the booking stages, booking fields, block release rules or KPIs in `../OR scheduling assistant research/workflow_and_data.md` and `stakeholders_and_value.md`. Those files are cross-referenced where they apply.

**Evidence labels:**
- [PR] peer-reviewed
- [P] hospital policy (primary document, full text read)
- [A] academic poster or non-peer-reviewed QI project
- [T] trade press or consultant
- [V] vendor claim
- [Intl] non-US setting
- (snippet) means the item came from a search-result summary, not a full-text read, and is weaker evidence.

Main anchors read in full:
- Dexter et al. 2012 and 2014, *Anesthesia & Analgesia* (abstracts)
- Moss & Xiao 2004, *JONA*, an observational study of OR charge nurse communication
- St. Charles Bend Surgery and Procedural Schedule Management Policy #3899 (v12, reviewed 08/2023)
- Albany Medical Center day-of-surgery cancellation poster (2022–2023)
- The Qventus Southern Health System case study (2025)
- The LeanTaaS preoperative readiness blog (Aug 2026)
- The AORN preference card article (Dec 2023)

---

## 1. Post-booking changes: how often are cases rescheduled, modified, cancelled or moved, and what triggers it?

### Takeaway
The OR schedule is not stable after booking. In audit-log data from a US academic hospital, about half of ORs had their last case scheduled or changed within 2 working days of surgery, and about a quarter of OR-days had at least one add-on [PR]. Reported cancellation rates depend on the window measured:
- About 1–2% for same-day outpatient cancellations at well-run centers
- About 12% of all scheduled cases in the VA
- 15–18% for cancellations within 72 hours, or for some specialties such as total joint arthroplasty (TJA)

Triggers split into four groups:
- **Patient:** not fit, no-show, did not follow instructions, declined
- **Work-up and medical:** clearance or labs incomplete, condition changed
- **Payer:** prior auth denied or late, often within 3 days of surgery
- **Facility:** equipment or implants unavailable, no bed, scheduling error, no OR time, bumped by an emergency

Inpatients and late-scheduled cases make up a disproportionate share of cancelled time.

### Cited Findings
**How much the schedule churns close to the day of surgery**
- Dexter, Shi & Epstein (2012) rebuilt each date's OR schedule from timestamped scheduling-transaction audit tables over 17 consecutive 4-week periods. Findings:
  - 24.1% ± 0.3% of OR-date combinations had at least one add-on case.
  - For 22.3% ± 0.4% of OR-dates, the most recent case addition came 1 working day before surgery.
  - 51.5% ± 0.5% of ORs had their last case scheduled or changed within 2 working days of surgery.
  - Once allocated time was full, the median lead time for each additional case was 2.2 ± 0.2 workdays.
  - Additional cases made up 11.1% ± 1.7% of the total.
  - The authors say anesthesia groups should coordinate with the scheduling office during the final 2 workdays because changes are so frequent.
  — [Dexter et al., *Anesth Analg* 2012;115:1188–95 [PR]](https://iro.uiowa.edu/esploro/outputs/journalArticle/Descriptive-study-of-case-scheduling-and/9983806274002771)
- Dexter et al. (2014) on cancelled OR time:
  - At a 21-facility nonacademic system, inpatients were 16.2% of scheduled minutes but about 49% of cancelled minutes (57% in hospitals only).
  - At an academic hospital, inpatients were 22.3% of scheduled minutes but 70% ± 2% of cancelled minutes.
  - About 54% of inpatient cancelled minutes came from cases scheduled within 1 workday before surgery.
  - Outpatient cancelled minutes were 1.6%, against 8.1% for inpatients.
  - Outpatients can reach a cancellation rate of about 2% or lower with a phone-based preoperative evaluation.
  — [Dexter et al., *Anesth Analg* 2014;118:1072–80 [PR]](https://iro.uiowa.edu/esploro/outputs/journalArticle/Relative-influence-on-total-cancelled-operating/9983806374002771)
- At one inpatient site, cases cancelled after 7 AM the day before, or at any time on the day of surgery, accounted for 22.6% ± 0.5% of scheduled minutes (snippet). — [Dexter group, Univ. of Iowa repository [PR] (snippet)](https://iro.uiowa.edu/esploro/outputs/journalArticle/Management-implications-for-the-perioperative-surgical/9983806387502771)
- Moving cases to other ORs when a room ran late cut tardiness by 50–70% for the moved cases. Suite-wide tardiness fell only 6–9% because few cases were moved (snippet). — [Dexter group, "Reducing tardiness from scheduled start times" [PR] (snippet)](https://iro.uiowa.edu/esploro/outputs/journalArticle/Reducing-tardiness-from-scheduled-start-times/9983806372702771)

**Cancellation rates and reasons (US)**
- VA, 2006 data from 123 facilities: 40,988 of 329,784 scheduled cases (12.4%) were cancelled. Reasons:
  - Patient: 35%
  - Work-up or change in medical condition: 28%
  - Facility: 20%
  - Surgeon: 8%
  - Anesthesia: 1%
  - Miscellaneous: 8%

  (snippet; abstract summary). — [Argo et al., *Am J Surg* 2009;198:600–6 [PR]](https://aemqa.stanfordhealthcare.org/publications/414/414224.html)
- The VA facility-side cancellation codes include broken or unavailable equipment, unavailable implants, no ICU or hospital bed, scheduling errors, non-surgical staff shortages, lack of OR time, and emergency cases displacing elective ones. Patient-side codes include refusal or no consent, transportation problems, and inadequate preoperative instructions. — [Table adapted from Argo 2009, via PMC4184311](https://pmc.ncbi.nlm.nih.gov/articles/PMC4184311/table/T7)
- Albany Medical Center (main campus, adult elective outpatients, July 2022–Dec 2023):
  - 194 day-of-surgery cancellations out of 17,353 cases, a 1.1% rate.
  - 71% were patient-related. Within those: 44% not fit for surgery, 11% no-show, 9% patient cancelled, 14% did not follow preoperative instructions (anticoagulant or NPO).
  - 22 cancellations had no reason recorded.
  - The authors concluded that few cancellations are preventable.
  — [Carpenter et al., Albany Med poster, 2026 [A]](https://www.amc.edu/wp-content/uploads/sites/3/2026/06/Outlook-Day-of-Surgery-Cancellations-for-Albany-Medical-Center-Main-Campus-A-Retrospective-Investigation.pdf)
- Olson & Dhakal (2015) studied 14,893 elective patients at an academic tertiary hospital. The overall day-of-surgery cancellation rate was 1.23%. By type of preoperative assessment:
  - Comprehensive assessment: 0.48%
  - Nurse telephone screening: 0.60%
  - No structured assessment: 2.02%

  — [cited in LeanTaaS blog, Aug 2026 [V citing PR]](https://leantaas.com/blog/preoperative-readiness/)
- Abate et al. (2020, systematic review) put the global day-of-surgery cancellation rate at about 18% (95% CI 16–20%). — [cited in LeanTaaS blog [V citing PR]](https://leantaas.com/blog/preoperative-readiness/)
- At one large US health system, 15% of cases were cancelled within 72 hours of surgery, and only about 50% of those were performed within 90 days. — [Qventus eBook, Feb 2026 [V]; see stakeholders_and_value.md](https://www.qventus.com/wp-content/uploads/2026/02/Qventus-eBook-35MProblem-SurgicalLeakage-1.pdf)
- That contrasts with a University of Iowa study in which 90% of cancelled cases later had the same or a similar procedure at the same hospital (snippet). — [Rescheduling of previously cancelled surgical cases [PR] (snippet)](https://iro.uiowa.edu/esploro/outputs/journalArticle/Rescheduling-of-previously-cancelled-surgical-cases/9983806379402771)

**Prior authorization as a trigger**
- ISASS 2016 survey of spine surgeons (n=115 of 571):
  - Surgeons estimated that 24.6% of cases were denied during pre-authorization.
  - 58.5% of denials arrived no more than 3 days before surgery.
  - Surgeons perceived OR time as unfilled 19% of the time.
  - 84.3% named insurance denial as the top reason for unfilled OR time.
  — [ISASS press release [T]](https://www.isass.org/wp-content/uploads/2016/04/PreAuth-Survey-Press-Release.pdf); [Healio 2016](https://www.healio.com/news/orthopedics/20160920/survey-of-surgeons-perceptions-preauthorization-delays-negatively-impact-care-workflow)
- Single institution, AAOS 2026 abstract: 105 of 584 scheduled primary TJA cases (17.9%) were cancelled in a 50-day window. Insurance issues (authorization delays and denials) caused 38 of the 105 (36.2%), the most common reason. — [AAOS 2026 abstract [A]](https://index.mirasmart.com/AAOS2026/PDFfiles/AAOS2026-005559.pdf)
- AAHKS 2023 survey (n=353, 13% response rate): 95% of members saw prior authorization increase over the past 5 years, and 96% said it delays access to care at least sometimes. — [AAHKS survey [PR]](https://profiles.wustl.edu/en/publications/prior-authorization-in-total-joint-arthroplasty-a-survey-of-the-a/)
- St. Charles Bend policy on prior authorization:
  - An approved or pending prior-authorization number for facility charges is required to schedule within 14 days of surgery, and the case must fall inside the authorization's valid date range.
  - "If resource needs change requiring updated authorization, the case will be removed from schedule until prior authorization is supplied."
  - Any case that needs a Supply Chain "Fast Track" item is not scheduled until the item is approved.
  — [St. Charles Policy #3899, reviewed 08/2023 [P]](http://www.stcharleshealthcare.org/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgeryProceduralScheduleManagementBend-Policy3899.pdf)
- HonorHealth's form tells offices that changing location, patient class or CPT means contacting the insurer and updating the authorization (see workflow_and_data.md). — [HonorHealth form [P]](https://www.honorhealth.com/sites/default/files/2025-10/surgery-scheduling-fax-request-form.pdf)

**Modifications and booking errors**
- Wu (2012): the booking error rate was 0.86% across more than 17,000 surgeries. Wrong side made up 36% of errors and wrong approach (e.g., laparoscopic vs open) 17%. Most errors were caught in the holding area or the OR (secondary summary). — [Patient Safety Solutions, Oct 2012 [T summarizing PR]](https://www.patientsafetysolutions.com/docs/October_30_2012_Surgical_Scheduling_Errors.htm)
- Elective cases at St. Charles cannot be booked past the end of the block. Overflow cases "will be moved to the providers next available block time." — [St. Charles #3899 [P]](http://www.stcharleshealthcare.org/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgeryProceduralScheduleManagementBend-Policy3899.pdf)

**International comparison**
- [Intl] Ibri Regional Hospital, Oman (2014): 1,235 of 4,814 elective cases (26%) were cancelled. 63% were patient no-shows; only 2% were OR-related. — [Sultan Qaboos Univ Med J 2016 [PR]](https://pmc.ncbi.nlm.nih.gov/articles/PMC4996291)

### Inferences
- Change activity peaks in the last 2 workdays and the last 72 hours. This is the same window that holds schedule close (UTMC 2:00 PM day before; St. Charles 5:00 PM two business days before), chart deadlines (UTMC 72h), implant deadlines (48h) and late prior-auth denials (58.5% within 3 days, per ISASS). An agent's highest-value time window is T-5 to T-0 days, not the booking moment.
- Each change sets off a fan-out of notifications. A CPT, location or class change re-triggers prior auth, and may also change duration, trays and implants, bed type and PAT pathway. A date change re-triggers patient instructions, PAT timing, the vendor rep and loaner delivery. This is inferred from the policies above. No source measured fan-out per change.
- Facility-side cancellation causes (about 20% in the VA) and late payer denials are the most process-addressable. Patient-fitness causes are addressed by earlier readiness work (Section 3), not by scheduling.

### Gaps
- No US study found that reports a rate of reschedules per case (date moved but not cancelled), or how often procedure, duration, surgeon or equipment are changed after booking. Dexter's audit-table method could produce these rates, but published abstracts report only additions and cancellations.
- A search summary attributed a figure of "9.7% of scheduled hours and 9.7% of cases cancelled from 7 AM the working day before" to a Dexter-group study. The source paper could not be verified, so the figure is not used above.
- The full Argo 2009 VA ranked-reason table (e.g., no-show %, bed %, implant %) was not accessible.

---

## 2. The coordination network: parties, channels and touches per case

### Takeaway
A single elective case links roughly 10–15 parties:
- Surgeon and the surgeon's office scheduler
- Central OR scheduling
- Payer and financial clearance
- PAT nurses and outside clearance physicians (cardiology, PCP)
- Anesthesia (AIC)
- OR charge nurse / OR desk and OR clerk
- SPD and equipment managers
- Vendor rep and purchasing / supply chain
- Bed management, pre-op holding and PACU
- Floor nurses, for inpatients
- The patient and family

Before the day of surgery, communication is phone, fax and the EHR. On the day, it is mostly face to face and by phone at the OR desk.

The best-measured node is the OR charge nurse:
- 32–74 communication episodes per hour
- 69% face to face
- Dominated by equipment coordination (39%) and patient-preparedness checks (26%), not by scheduling

No source gives a validated "touches per case" count.

### Cited Findings
**The OR desk / charge nurse hub (the best quantitative data)**
- Moss & Xiao observed charge nurses at 4 OR suites in 3 mid-Atlantic tertiary hospitals over 17 days (about 100 hours, mostly 6 AM–noon).
  - **Volume:** 2,074 communication episodes, ranging from 32 to 74 per hour. The largest suite had the highest rate.
  - **Who:** OR nurses 39%, OR technicians 14%, OR clerks 12%, surgeons 11%, equipment managers 9%. Other targets included anesthesia, the ambulatory surgery unit, floor nurses, pre-op holding and (at one suite) bed control.
  - **Why:**
    - Coordinate equipment: 39%
    - Coordinate patient preparedness: 26%
    - Staffing: 19%
    - Room assignment: 11%
    - Schedule or reschedule surgery: 6%
  - **How:** face to face 69%, telephone 18%, intercom 7%. 85% of communication with floor nurses and 86% with pre-op holding was by telephone.
  - **Duration:** mean 40 seconds, median 20 seconds or less; 93% lasted 1 minute or less. Scheduling, rescheduling and room-assignment conversations ran longer because they "often involved negotiation."
  - **Asynchronous channels:** email and voicemail were never used for OR coordination. Wireless phones were considered unreliable at 2 of the 4 suites.
  - **Trauma suite contrast:** in a trauma OR suite, scheduling and rescheduling made up more than 32% of episodes.
  - **Authors' conclusion:** short status queries about preparedness and equipment "may be fulfilled by automated status displays and short messages."
  — [Moss & Xiao, *JONA* 2004;34(2) [PR]](https://www.interruptions.net/literature/Moss-JONA04.pdf)
- Before the patient enters the room, someone must confirm several things: financial forms, admission assessment and diagnostic tests are complete, and the surgeon and anesthesiologist have examined the patient. The authors say an electronic patient-status display "would eliminate a great deal of the communication related to patient preparedness." — [Moss & Xiao 2004 [PR]](https://www.interruptions.net/literature/Moss-JONA04.pdf)
- [Intl, Toronto] In-room team communication: of 421 procedurally relevant communication events across 48 procedures, 129 (about 30%) were failures. By failure type: occasion/timing 45.7%, content 35.7%, purpose 24.0%, audience 20.9%. 36.4% of failures had visible effects such as delay, inefficiency or tension. — [Lingard et al., *Qual Saf Health Care* 2004 [PR]](https://qualitysafety.bmj.com/content/13/5/330)

**Surgeon office ↔ facility (pre-day-of)**
- A practice administrator describes the routine: after faxing a case, office staff call the OR scheduler to confirm that the case is on the schedule, insurance is verified, equipment is available, and the sales rep has been notified. Offices "cannot see the care coordination workflow status" for each case (snippet). — [Whitman Partners, "Challenges coordinating surgical care" [T]](https://whitmanpartners.com/challenges-coordinating-surgical-care/)
- Illegible or incomplete faxes, or forms with sections left blank, led to "a series of back-and-forth phone calls" to get case information, plus more calls to confirm the schedule (2007). — [Relias Media / Same-Day Surgery 2007 [T]](https://reliasmedia.com/articles/101595-connect-to-physician-offices-through-internet)
- At UTMC, offices may not fax next-day add-ons, cancellations or changes. They must phone them in and then send an updated form, and every cancellation needs a reason (see workflow_and_data.md). — [UTMC Policy 3364-100-53-27, 5/2026 [P]](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)

**Vendor reps, purchasing and SPD (implants and loaners)**
- UTMB loaner policy:
  - The surgeon's office should tell the OR and Purchasing about loaner needs "at the time the procedure is scheduled."
  - Loaner trays are due in SPD at least 48 hours before the case.
  - First-time vendor sets need 3 business days.
  - Trays are tagged with date, surgeon and procedure.
  (snippet). — [UTMB policy [P] (snippet)](https://www.utmb.edu/policies_and_procedures/20038472)
- HealthTrust: sets "are supposed to be delivered at a minimum of 24 hours in advance… but often that's not the case." The result can be "significant delays in the operating room and sometimes cancelled procedures" (snippet). — [HealthTrust, The Source [T]](https://healthtrustpg.com/thesource/clinical-connection/quality-improvement/reducing-unnecessary-cost-risk-in-the-or/)
- St. Charles policy on vendor items:
  - It is the physician's or office's responsibility to contact the vendor rep for Supply-Chain-approved items.
  - Cases needing extra lead time are "subject to delay pending physician consultation" if supplies are not obtained.
  - For add-ons, the provider communicates supply needs to the vendor.
  — [St. Charles #3899 [P]](http://www.stcharleshealthcare.org/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgeryProceduralScheduleManagementBend-Policy3899.pdf)

**PAT ↔ outside offices ↔ patient**
- Qventus describes Southern Health System's baseline as "endless hours spent faxing, making unanswered phone calls, and manually combing through patient charts." Reported results:
  - PAT capacity rose from 1.8 to 2.8 screenings per hour.
  - Cancellations fell from about 4.9% to about 3.5%.
  - Each fax took about 3 minutes less, a 60% cut in processing time.
  — [Qventus Southern Health System case study, 2025 [V]](https://www.qventus.com/wp-content/uploads/2025/09/Qventus-Southern-health-system-PCC-Case-Study.pdf)
- Qventus said in 2021 that its predictions removed more than 10,000 hours of back-and-forth phone calls for OR schedulers (snippet). — [Qventus 2021 announcement [V] (snippet)](https://jotup.co/node/1727538)
- LeanTaaS says readiness gaps arise when teams don't know who owns the next step. It claims its Patient Outreach Assistant saved an average of 52.8 nursing hours per month. — [LeanTaaS blog, Aug 2026 [V]](https://leantaas.com/blog/preoperative-readiness/)

### Inferences
- A conversational agent mainly fits the **pre-day-of** network (office ↔ scheduling ↔ PAT ↔ payer ↔ vendor ↔ patient). That network is asynchronous, fax-heavy and slow-latency. The **day-of** network (charge nurse ↔ OR staff) is synchronous, sub-minute and face to face. There an agent is better used as a status source that cuts queries (Moss) than as a chat participant.
- Most queries at the hub are short status checks. In Moss, 39% were about equipment and 26% about patient preparedness, at a median of 20 seconds or less. "Is the patient in holding? Is the tray sterile? Did anesthesia see the patient?" are status lookups that a tracking or agent layer can answer.
- A plausible touch count per elective implant case, assembled from the policies above and not measured, is about 10–20 discrete messages or calls:
  - Office books
  - Scheduler validates
  - Auth request and response
  - PAT call(s)
  - Outside records request(s)
  - Vendor and purchasing notice
  - Loaner delivery check
  - Day-before confirmation to office and patient
  - Day-of status checks

### Gaps
- No peer-reviewed or credible source gives a measured number of touches, calls or messages per surgical case, or scheduler minutes per change.
- No data was found on Vocera or secure-chat volume for OR charge nurses or schedulers. Moss (2004) predates smartphones and secure messaging, so channel shares will have moved toward secure chat and EHR in-basket since then.
- The detailed implant-rep workflow (who confirms rep attendance, how bill-only implants are reconciled) was not documented in sources found.

---

## 3. Pre-op readiness tracking: how are H&P, consent, labs, clearances, prior auth and implants tracked, and what happens when they're not ready 48–72 hours out?

### Takeaway
Hospitals set hard deadlines:
- Chart documents at T-72h (UTMC)
- Financial clearance by noon the day before (UTMC)
- Implants and loaners in SPD at T-48h (UTMC, UTMB)
- Prior auth number required to book within 14 days (St. Charles)

The penalty for missing a deadline is removal, deferral or cancellation. Tracking is fragmented across the PAT nurse, the scheduler, the office and SPD. The interventions with reported results are proactive outreach and chart review at about 48–72 hours (phone, email or AI) with escalation to the scheduler. They report roughly 25–53% fewer preventable late cancellations, mostly in self-reported QI and vendor data.

### Cited Findings
- UTMC: chart documentation is due to pre-admission 72 hours before elective cases, otherwise cases "may be removed from the schedule or postponed." Financial clearance is due by 12:00 PM the day before "or the case may be deferred." Vendor implants must be in SPD 48 hours ahead "or the procedure may be subject to cancellation." — [UTMC Policy, 5/2026 [P]](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf) (detail in workflow_and_data.md)
- St. Charles requires approved or pending prior auth to book within 14 days. A resource change that needs new authorization removes the case from the schedule until authorization is supplied. — [St. Charles #3899 [P]](http://www.stcharleshealthcare.org/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgeryProceduralScheduleManagementBend-Policy3899.pdf)
- The readiness items one vendor lists as tracked:
  - Labs and clearances
  - Medication changes (anticoagulants, diabetes drugs, GLP-1 agents)
  - NPO instructions and skin prep
  - Illness screening
  - Arrival time and location, driver, and overnight caregiver
  - Documentation completeness and patient comprehension

  Gaps "surface at check-in" when no one owns the next step. — [LeanTaaS, Aug 2026 [V]](https://leantaas.com/blog/preoperative-readiness/)
- Haufler & Harrington (2011, ASC): scripted nurse calls 3 business days before surgery, focused on no-show, NPO and transportation, cut daily cancellations by 53%. — [cited in LeanTaaS [V citing PR]](https://leantaas.com/blog/preoperative-readiness/)
- Kaiser Permanente Sacramento (2025):
  - PACU/pre-op teams added outreach 72 hours before surgery by email or phone covering fasting, medications and cancellation steps.
  - Preventable same-day cancellations fell from 27 to 13 in a 13-week pilot (52%).
  - The project also improved "communication between pre-op nurses and OR schedulers to ensure timely updates" (snippet).
  — [KP NCAL Nursing Annual Report 2025 [A] (snippet)](https://nursingncal.kaiserpermanente.org/annual-report-2025/new-knowledge-innovation-improvements/reducing-same-day-surgical-cancellations-a-pre-op-pacu-process-improvement-initiative/)
- Kaiser Folsom ambulatory surgery nurses did targeted chart reviews ("shallow dives") 48 hours before surgery to resolve pending labs, medication adjustments and comorbidity management. The target was a 30% cut in same-day cancellations; no final result was found (snippet). — [KP NCAL Nursing Annual Report 2025 [A] (snippet)](https://nursingncal.kaiserpermanente.org/annual-report-2025/exemplary-professional-practice/preop-phone-calls-reduce-same-day-surgery-cancellations-and-enhance-patient-experience/)
- NYU Langone Orthopedic Hospital: a daily OR huddle plus scheduling software reportedly cut day-of cancellations from about 10% to under 1% (snippet). — [OR Manager, March 2018 [T] (snippet)](https://www.nxtbook.com/accessintelligence/ORManager/or-manager-march-2018/index.php?startid=24)
- OHSU: more than 50% reduction in targeted late cancellations. It moved to a "coordinated case planning" model with AI-enabled outreach and human escalation. Before the change, preparation was concentrated close to the day of surgery, leaving little time to fix missed instructions, transport or illness issues (snippet; conference/sponsored). — [Becker's session, Sept 2026 [T/V]](https://conferences.beckershospitalreview.com/transform-hospital-operations-sept-2026/session/4262232/50-percent-+-reduction-in-late-cancellations-how-ohsu-scaled-coordinated-case-planning-to-prepare-patients-earlier)
- Qventus PCC components [V]:
  - PAT Assist: prioritizes PAT calls and handles prep, follow-up, medical-record requests and EHR notes
  - Continuous risk determination from EHR, chart review and conversations
  - AI patient concierge by voice, text and email
  - Intelligent document management for faxed, scanned and emailed records

  One stated goal was to "reduce 72-hour surgery cancellations." — [Qventus SHS case study 2025 [V]](https://www.qventus.com/wp-content/uploads/2025/09/Qventus-Southern-health-system-PCC-Case-Study.pdf)
- At an academic hospital, in-person preoperative clinic visits did not lower outpatient cancelled minutes (0.0% ± 0.1% per 10% more visits, P=0.58). Phone-based evaluation reached a rate of about 2% or lower. — [Dexter et al. 2014 [PR]](https://iro.uiowa.edu/esploro/outputs/journalArticle/Relative-influence-on-total-cancelled-operating/9983806374002771)

### Inferences
- Readiness is a checklist with an owner and a due date per item, and the escalation path at T-72h and T-48h is "chase, then escalate to the scheduler or surgeon, then defer or remove." An agent that holds this per-case checklist can:
  - Send reminders to the right owner, such as an office for a missing H&P, cardiology for a clearance letter, or the vendor for a loaner
  - Answer "what's still open on Mrs. X's case?"
  - Raise at-risk cases to the scheduler before the 72h line

  This matches what vendors are already building ([V] Qventus, LeanTaaS).
- Patient-facing readiness items (NPO, anticoagulants, ride, illness) cause many day-of cancellations: 14% of patient-related cancellations at Albany were instruction failures. They suit automated outreach. Clinical judgments (fit or not fit, clearance adequacy) still need a nurse or anesthesiologist.

### Gaps
- No public Epic or Oracle "surgical readiness" work-queue specification was found showing which readiness flags exist natively.
- No US data was found on what share of cases are not ready at T-72h, or how many of those are rescued versus deferred.

---

## 4. Day-before and day-of: schedule close, confirmation, OR desk decisions, add-ons and bumping, delays, flip rooms, room moves and day-of communications

### Takeaway
The schedule "closes" 1–2 business days before surgery (UTMC 2:00 PM day before; St. Charles 5:00 PM two business days before). Case sequence is confirmed with offices, and later requests become add-ons. The add-on route goes through the charge RN, with the anesthesiologist-in-charge (AIC) deciding urgency and final sequence.

On the day, the charge RN and AIC watch for late rooms and apply explicit rules. For example, start an elective case only if two-thirds can finish before the block ends and the overrun is under 45 minutes; otherwise move it to the add-on queue or reschedule. Bumps require the surgeon who needs the room to tell the bumped surgeon directly, and disputes go provider-to-provider, then to the AIC, then to leadership. Day-of communication is mostly face to face and by phone at the OR desk.

### Cited Findings
**St. Charles Bend Policy #3899 (v12, reviewed 08/17/2023) [P]**
- **Close and sequence:**
  - Elective scheduling closes at 5:00 PM two business days before surgery, and case-sequence confirmation is due by then.
  - Sequencing rules: same-day discharge first; history of malignant hyperthermia first case; isolation last; group by patient type, age, anesthesia type and laterality.
- **Add-ons:**
  - Requests after close or on the day are "called to the department Charge RN," and the provider or APP submits the request electronically.
  - Authorization or documentation of medical necessity is required.
  - Requests are accepted based on acuity and resources, and urgency questions go to the AIC or the on-call anesthesiologist.
  - Add-ons are not accepted more than 24 hours ahead.
  - Start order depends on acuity and the order of request.
- **Urgency classes:** emergency access within 60 minutes; emergent trauma within 15 minutes; urgent within 24 hours. ED and bedded inpatients count as urgent.
- **Bumping:** the first available suite is used. If none is free, the charge nurse may consult the AIC and providers about bumping. "It is the responsibility of the provider with the emergency case to communicate with the provider being 'bumped.'" The AIC owns final case sequence, or the on-call trauma surgeon if the AIC is unavailable.
- **Running late:** "Throughout the day the OR Charge RN and Anesthesiologist in Charge (AIC) will monitor the daily schedule for late rooms."
  - A late room may start an elective case if two-thirds of it can be completed before end of block and the overrun is under 45 minutes.
  - Otherwise the case goes to the add-on queue "or will be rescheduled into the next available date/time."
  - Holds are prioritized by OR efficiency "and dependent on surgeon-to-surgeon communication."
- **Disputes:** add-on order disputes go provider-to-provider, then to the AIC, then to the perioperative manager on call or Administrator on Duty out of hours.
- **Capacity limits:** 7 anesthetizing locations from 17:30 to 19:00, and 5 overnight and on weekends.

— [St. Charles #3899](http://www.stcharleshealthcare.org/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgeryProceduralScheduleManagementBend-Policy3899.pdf)

**Other policies**
- UTMC [P]: the schedule closes at 2:00 PM the day before. Scheduling confirms case order and start time with the surgeon or office the day before. Start times after the first case are "estimates only." Add-ons need AIC/board runner approval with the OR supervisor. The OR Director/Manager notifies surgeons of delays (see workflow_and_data.md). — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Hendrick Health: requests for procedures that will not finish by 19:00 need approval from the on-call anesthesiologist. If an emergency cannot fit, the surgeon who needs the room tells the bumped surgeon in person, and disputes go to the Chief of Surgery (snippet). — [Hendrick Health policy [P] (snippet)](https://www.hendrickhealth.org/documents/content/Scheduling-of-Patients-for-Surgery-4-9164.pdf)
- St. Charles Redmond: if no suite is open, the charge nurse may consult on-call anesthesia and surgeons about bumping. Providers bump their own partner or specialty first (snippet). — [St. Charles Redmond Policy 2212 [P] (snippet)](https://WWW.STCHARLESHEALTHCARE.ORG/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgeryProceduralScheduleManagementRedmond-Policy2212.pdf)
- OR Manager framework: emergencies take the first available room, and elective add-ons go to the end of the day. Urgency classes escalate over time; for example, a Class B case (4 hours) becomes Class A (1 hour) and bumps in after 3 hours of waiting (snippet). — [OR Manager, "Managing urgent cases" [T] (snippet)](https://www.ormanager.com/wp-content/uploads/pdfx/ORMVol26No7ManagingUrgentCases.pdf)

**Delays, room moves, flip rooms**
- Moving late-running cases to other ORs cut tardiness by 50–70% for the moved cases but only 6–9% suite-wide, because few cases were moved (snippet). — [Dexter group [PR] (snippet)](https://iro.uiowa.edu/esploro/outputs/journalArticle/Reducing-tardiness-from-scheduled-start-times/9983806372702771)
- An ACHE 2025 poster found that first-case delays were driven mainly by completing consent and site marking and by the surgical briefing (snippet). — [ACHE 2025 poster 18 [A] (snippet)](https://www.ache.org/-/media/ache/learning-center/research/2025-poster-presentation-posters/poster-18.pdf)
- In an anesthesia consultancy's review of 6 clients over 2 months, flip-room days averaged 14% of days, with wide variation (snippet). — [Becker's ASC [T] (snippet)](https://beckersasc.com/anesthesia/how-flip-rooms-affect-anesthesia-practice-productivity-4-things-to-know.html)
- LeanTaaS says flip rooms improve surgeon efficiency but generally lower overall utilization and use twice the resources of a single room. — [LeanTaaS blog [V] (snippet)](https://leantaas.com/blog/or-flip-rooms-are-nothing-to-flip-out-about)

**Day-of communication channels**
- At the OR desk, communication was 69% face to face, 18% telephone and 7% intercom. Contact with pre-op holding and floor nurses was mostly by phone (86% and 85%). Email and voicemail were never used, and wireless phones were unreliable at 2 of 4 suites (2004 data). — [Moss & Xiao 2004 [PR]](https://www.interruptions.net/literature/Moss-JONA04.pdf)
- Family updates: Gordon et al. (2015) evaluated a secure web service that sends perioperative updates to the patient's designated contacts by SMS or email (snippet). — [Patient Safety in Surgery 2015 [PR] (snippet)](https://pssjournal.biomedcentral.com/track/pdf/10.1186/s13037-015-0070-9)
- In a 2024 feasibility study of an SMS/web perioperative messenger for families, 99% of 173 messages were read on mobile devices. Staff named "no additional workload" as a key requirement (snippet; setting not verified). — [Digital Health 2024 [PR] (snippet)](https://doi.org/10.1177/20552076241288760)

### Inferences
- Day-of decisions are rule-based but negotiated: two-thirds-of-case and 45-minute rules, urgency clocks, "bump your own partner first," and surgeon-to-surgeon calls. An agent can do several things here:
  - Compute the options, such as which room finishes first, whether the case can start under the two-thirds rule, and which cases are candidates to bump.
  - Draft and route the notifications to the bumped surgeon, office, patient, family and PACU.
  - Keep the add-on queue visible and ordered.

  The AIC and charge RN keep the decision. Policies explicitly name them as owners.
- The most common day-of question from offices and families, "Is my case on and when?", is answered by the OR desk by phone today. Start times after the first case are "estimates only" (UTMC). A real-time, agent-answerable case status (on time, delayed X minutes, moved to OR 7, bumped) is the obvious automation target.

### Gaps
- No US data was found on how many cases per day are moved between rooms or resequenced, or how many add-ons per day a typical OR desk processes. The closest figure is Dexter's 24.1% of OR-dates with at least one add-on.
- No published data was found on Vocera, secure-chat or text volume for OR charge nurses or AICs, or on how status boards (Epic OpTime status board, whiteboards) are used for day-of changes.
- No structured description was found of the "next-day confirmation call" to patients (who makes it, the script, the no-answer rate).

---

## 5. Preference cards and case picking: dependence on schedule accuracy and what goes wrong

### Takeaway
SPD and the OR build case carts and room setups from the surgeon's preference card for the booked procedure. Card accuracy and booking accuracy (procedure, side, approach, surgeon, implant vendor) together decide whether the right trays and supplies arrive. Errors show up as:
- Opened-but-unused supplies (about 26% of opened single-use sterile items per one survey)
- Missing or broken instruments (tray defects in about 5% of cases in one large US study; over 50% of affected cases delayed in an observational study)
- Loaners or devices missing from the card, which in one example cancelled the case

Equipment coordination is already the single biggest purpose of charge nurse communication (39%).

### Cited Findings
- Preference cards list items from the surgeon and procedure down to individual tray instruments, and formats vary (EMR, paper, separate lists). Outdated cards cause wasted opened supplies, delays while staff gather missing items, and safety concerns. Staff are told to notify the charge nurse or the preference-card owner when a card needs updating. In the article's example, a skin-graft "mesher" was a loaner that was not on the card and was unavailable, so the patient had to return the next day. — [AORN, "Why Do I Need Preference Cards?", 12/20/2023 [T]](https://aorn.org/article/why-do-i-need-preference-cards)
- In an AORN survey commissioned by Owens & Minor, 40% of perioperative leaders named inaccurate preference cards as the main reason supplies are picked for a case but not used. Updates are largely reactive (snippet). — [Owens & Minor [V-sponsored survey] (snippet)](https://www.owens-minor.com/?p=1020984)
- A 2022 survey estimated that 26% of single-use sterile supplies opened for surgery were unused (snippet). — [Medline SCO Fall/Winter 2024 [V/T] (snippet)](https://publications.medline.com/pub-sco-fawi-2024issue-9-sco-fall-winter-2024-issue-9/0609259001730912126/p16)
- Stanford (JAMIA): an algorithm flagged likely-inaccurate card quantities, and nurses revised 309 cards across 8 services. Direct supply cost per case fell 8.38% in the intervention group and rose 13.21% in the control group (snippet). — [Stanford / JAMIA doi:10.1093/jamia/ocaa275 [PR] (snippet)](https://stanfordhealthcare.org/publications/804/804134.html)
- OR-reported tray defects, July 2016–Dec 2017: 3,900 defects, mostly from tray assembly, affected about 5% of 41,799 surgical cases. Missing instruments were the most common assembly defect (17.6%). Root causes included production pressure and inconsistent instrument naming (snippet). — [BMJ Quality & Safety 2021;30:271 [PR] (snippet)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7979531)
- Direct observation in 7 pediatric ORs (2021):
  - 236 instrument errors affected 147 cases. Missing instruments were the most common (n=160), followed by broken instruments (n=44).
  - Errors occurred in 42.7% of inpatient cases and 22.3% of outpatient cases.
  - Over 50% of affected cases were delayed, by an average of 10.16 minutes.
  - Estimated lost charges were $6.75–9.42M per year.
  (snippet). — [BMC Surgery 2024 [PR] (snippet)](https://link.springer.com/article/10.1186/s12893-024-02407-1)
- In an Aesculap/Ascendco benchmark survey of more than 100 SPD and OR leaders, 58% reported surgery delays tied to instrument sets that were missing, incomplete or not ready (snippet). — [HPN Online [V-sponsored survey] (snippet)](https://www.hpnonline.com/sterile-processing/news/55330330/benchmark-report-identifies-fundamental-risks-in-sterile-processing-operations)
- St. Charles adds turnover times automatically by procedure card, and case durations come from EHR provider-specific averages. The booked procedure therefore also drives duration and turnover. — [St. Charles #3899 [P]](http://www.stcharleshealthcare.org/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgeryProceduralScheduleManagementBend-Policy3899.pdf)
- Booking errors (0.86% of more than 17,000 cases; 36% wrong side, 17% wrong approach) are mostly caught in holding or the OR. By then the case cart has already been picked for the wrong variant. — [Patient Safety Solutions summarizing Wu 2012 [T]](https://www.patientsafetysolutions.com/docs/October_30_2012_Surgical_Scheduling_Errors.htm)
- In Moss & Xiao, equipment coordination was the top purpose of charge nurse communication (39%), and 51% of communication with OR technicians concerned equipment. — [Moss & Xiao 2004 [PR]](https://www.interruptions.net/literature/Moss-JONA04.pdf)

### Inferences
- The scheduling-to-SPD failure chain runs like this. A late change to procedure, approach, side, surgeon or date leaves the picked cart wrong or stale. The loaner or implant is not ordered or not delivered in time, or there is a sterilization crunch (immediate-use sterilization risk). The result is a delay or cancellation. Every procedure, surgeon or date change after carts are picked (often the evening or night before) should therefore trigger an SPD and vendor notification. An agent can enforce this.
- An agent could cross-check the booked CPT or procedure text, laterality and approach against the consent and H&P, and the preference card's loaner and implant items against vendor confirmations, at T-72h and T-48h.

### Gaps
- No study was found that measures case-cart or picking errors caused specifically by late schedule changes, as opposed to card inaccuracy or tray assembly.
- No public data was found on when case carts are typically picked relative to surgery (e.g., evening before vs night shift) in US hospitals.

---

## 6. Where time and frustration concentrate, and what is most amenable to automation or a conversational agent

### Takeaway
The work and failures concentrate in four places:
1. **The final 2 workdays / 72 hours:** schedule churn, add-ons, late prior-auth denials, readiness deadlines and implant deadlines.
2. **Chasing missing information:** faxes, unanswered calls, outside records, clearances, prior auth.
3. **Status queries:** "Is my case on? Is the tray ready? Is the patient in holding?" These are high-volume, short and interrupt-driven.
4. **Propagating changes** to every downstream party: SPD, vendor, anesthesia, PAT, patient, bed and PACU.

The best fits for a conversational agent are chasing, status answering, change propagation and structured add-on and change intake. Day-of bumping and sequencing decisions should stay with the AIC and charge RN, with the agent supplying decision support and notification drafting.

### Cited Findings
- 51.5% of ORs have their last case scheduled or changed within 2 working days of surgery. The authors say anesthesia should coordinate with the scheduling office in those final days. — [Dexter et al. 2012 [PR]](https://iro.uiowa.edu/esploro/outputs/journalArticle/Descriptive-study-of-case-scheduling-and/9983806274002771)
- 58.5% of prior-auth denials arrive within 3 days of surgery (surgeon estimates). — [ISASS 2016 [T]](https://www.isass.org/wp-content/uploads/2016/04/PreAuth-Survey-Press-Release.pdf)
- Charge nurses handle up to 74 communication episodes per hour. Most are short status or equipment queries that the authors say could be met by "automated status displays and short messages." — [Moss & Xiao 2004 [PR]](https://www.interruptions.net/literature/Moss-JONA04.pdf)
- Surgeon office staff spend many hours on the phone confirming case status, insurance, equipment and rep notification, and they lack visibility into case status (snippet). — [Whitman Partners [T]](https://whitmanpartners.com/challenges-coordinating-surgical-care/)
- PAT work is dominated by faxing, unanswered calls and chart review. Automating it raised nurse capacity about 50% and cut cancellations about 25%, from about 4.9% to about 3.5%. — [Qventus SHS 2025 [V]](https://www.qventus.com/wp-content/uploads/2025/09/Qventus-Southern-health-system-PCC-Case-Study.pdf)
- Proactive 72-hour outreach (52% fewer preventable same-day cancellations, KP Sacramento [A]) and 3-business-day scripted calls (53%, Haufler & Harrington via LeanTaaS) show that readiness chasing is where measured gains appear. — [KP NCAL 2025](https://nursingncal.kaiserpermanente.org/annual-report-2025/new-knowledge-innovation-improvements/reducing-same-day-surgical-cancellations-a-pre-op-pacu-process-improvement-initiative/); [LeanTaaS](https://leantaas.com/blog/preoperative-readiness/)
- AI outreach with human escalation reportedly cut targeted late cancellations by more than 50% at OHSU (sponsored). — [Becker's session 2026 [T/V]](https://conferences.beckershospitalreview.com/transform-hospital-operations-sept-2026/session/4262232/50-percent-+-reduction-in-late-cancellations-how-ohsu-scaled-coordinated-case-planning-to-prepare-patients-earlier)
- Policies assign final day-of authority to the AIC, the Medical Director or the operational leader. Bump communication is explicitly surgeon-to-surgeon. — [St. Charles #3899 [P]](http://www.stcharleshealthcare.org/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgeryProceduralScheduleManagementBend-Policy3899.pdf); [UTMC [P]](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)

### Inferences

**Lifecycle map with the owner and the failure point at each stage.** The map combines the sources above with workflow_and_data.md.

| Stage | Who | Typical failure | Agent opportunity |
|---|---|---|---|
| T-30 to T-14 d: booked | Office → scheduling | Incomplete request; auth pending | Completeness check; open readiness checklist |
| T-14 to T-5 d: auth, PAT, vendor | Office, payer, PAT, vendor, purchasing | Auth late or denied; records and clearances not received; loaner not requested | Chase owners; track status; escalate |
| T-5 to T-2 d: block release / close | Scheduling, anesthesia | 51.5% of ORs still changing; add-ons; inpatient late adds | Propagate changes to SPD, vendor, anesthesia, PAT and patient; confirm sequence |
| T-72 to T-48 h: readiness deadlines | PAT, SPD, financial clearance | Chart not ready; implants not in SPD; auth denied late | At-risk list for the scheduler; patient instruction outreach |
| T-1 d: confirmation | Scheduling → office and patient | Wrong arrival time; patient not told; case cart picked for the wrong variant | Automated confirmations; answer "is my case on?" |
| Day of | Charge RN, AIC, OR desk | Late rooms, add-ons, bumps, missing instruments, first-case delays (consent, site marking) | Real-time status answers; bump and move options; notification drafts |

**Most amenable to a conversational agent**
- Answering status questions for offices, patients and staff
- Chasing missing items with the named owner and deadline
- Fanning out change notifications
- Structured intake of change, cancel and add-on requests with a mandatory reason
- Day-before confirmations

**Moderately amenable (decision support with a human in the loop)**
- Add-on placement and late-room options under explicit rules (two-thirds of case, 45 minutes, urgency clock)
- Flagging booking/consent/H&P mismatches

**Least amenable**
- Clinical fitness and clearance judgments
- Surgeon-to-surgeon bump negotiation
- AIC prioritization of emergencies

### Gaps
- No time-and-motion study of US OR schedulers was found (minutes per booking versus per change, chase or status call), so the claim that most burden comes after booking is supported by indirect evidence: Dexter's churn data, Moss's communication data, and vendor PAT data. It is not measured directly.
- No independent (non-vendor) evaluation of a conversational or AI agent in OR scheduling or readiness was found. The OHSU, Qventus and LeanTaaS results are self-reported.
