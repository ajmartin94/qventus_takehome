# Constraints on OR Case Scheduling at US Hospitals and on Deploying an AI Conversational Scheduling Assistant

Research date: 2026-10-14. Scope: US hospitals. Sources are a mix of primary (regulation text, Epic's open.epic, hospital policy PDFs, peer-reviewed papers) and secondary (law-firm alerts, trade press, vendor blogs); secondary sources are flagged where it matters. Dates on regulatory items are given because several changed in 2025-2026.

---

## Q1. Block ownership, release, and open-time rules

### Takeaway
Most US hospitals run block scheduling: a surgeon or service "owns" recurring room-days, must release unused time manually (typically 48-72 hours ahead), and loses it automatically at a service-specific cutoff (commonly 0-14 days). Block holders who stay below roughly 75% utilization can have blocks cut. Released time becomes "open time," usually first-come, first-served. An assistant has to know who owns a slot and whether it has been released before it offers that slot to anyone else.

### Cited Findings
- University of Toledo Medical Center: block utilization = (elective case time + turnover time) / total block hours x 100. Goal is 75%, with turnover counted — [UToledo policy 3364-100-53-27](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- HonorHealth (AZ): blocks under 75% utilization "may be adjusted, reduced, or eliminated" by the designated committee. Suggested auto-release periods differ by specialty, from 0 working days (neuro, trauma) to 5 working days (ENT, general, OB/GYN, plastics). Numbers come from the search-engine summary because the PDF's compressed text could not be extracted directly — [HonorHealth Surgery Block Scheduling Policy (2023)](https://www.honorhealth.com/sites/default/files/2023-03/surgery-block-scheduling-policy.pdf)
- St. Charles (Redmond, OR): unused block auto-releases 7 calendar days before the date of procedure, after which the time is open to other providers or the room is closed depending on resources. **Robotics blocks release at 14 days** — [St. Charles Surgical/Procedural Block Management Policy 9579 (2024)](https://WWW.STCHARLESHEALTHCARE.ORG/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgicalProceduralBlockManagementRedmond-Policy9579.pdf)
- AORN business guidance: a surgeon who won't use some or all of a block should tell the scheduler 72 hours ahead so the time can be offered to someone else — [AORN Outpatient Surgery, "Ready to Tackle Block Time" (2017)](https://www.aorn.org/outpatient-surgery/article/2017-July-business-advisor-ready-to-tackle-block-time)
- ASC guidance: release unused block at least 48 hours ahead, 72 hours ideally — [HST Pathways](https://hstpathways.com/?p=259049)
- Hospitals often build in automatic release that triggers 72 hours before the day — [Rowan research summary, "Specialty acuity should be a consideration while assessing OR block time metrics"](https://www.researchwithrowan.com/en/publications/specialty-acuity-should-be-a-consideration-while-assessing-operat/)
- Releasing early can increase usable capacity. Inova reported +20% released OR minutes, 46% of released time backfilled with new cases, and +8% case volume for its top 10 requestors — [Becker's, "Inside Inova's 46% release fill rate"](https://www.beckershospitalreview.com/hospital-management-administration/inside-inovas-46-release-fill-rate-turning-open-or-time-into-more-cases/) (case report, not a benchmark)
- "Release" means scheduling a new case into another service's under-used allocated time — [Stanford FSI, "How to Release Allocated OR Time to Increase Efficiency"](https://healthpolicy.fsi.stanford.edu/node/24044)
- Dexter's practitioner guidance: OR **allocation**, not day-of-surgery decisions, is the main driver of OR efficiency. Day-of decisions barely matter when there is no over-utilized time — [Dexter, AORN Outpatient Surgery, "Drawing up a winning schedule" (2005)](https://www.aorn.org/outpatient-surgery/article/2005-April-drawing-up-winning-schedule)
- Separate add-on/day-of-surgery blocks can sit mostly unused. One capstone found only 15% of minutes allocated to such blocks went to add-on cases — [Georgia Tech ISyE capstone](https://capstone.isye.gatech.edu/node/5890)
- Henderson Hospital (surfaced in search; exact source URL not verified): blocks must be released at least 48 hours ahead, and 30 days before planned vacations — see Gaps.
- UI Health Care reportedly lengthened auto-release from 3 to 7 to 14 days because short-notice released time was hard to fill (search summary; attribution to a specific article not verified) — see Gaps.

### Inferences
- **The prototype should model these block states:** owned and unreleased; owned and manually released; auto-released (past the cutoff); open/unblocked; plus a specialty-reserved pool (e.g., robot, hybrid). When a coordinator for Surgeon B asks about a date, the assistant must not book into Surgeon A's unreleased block. It can offer "request release from block owner" as an escalation path.
- Release cutoffs depend on the service and the room. Store them as configuration per service/room (e.g., neuro 0 days, general 5 days, robotics 14 days), not as a single global constant.
- The block-utilization rule (75%) is a soft, slow-moving metric. Showing a surgeon's block utilization when you suggest they use their own block first is a credible value-add, but it is not a booking blocker.

### Gaps
- No primary national standard sets release windows; they are local policy. The Henderson Hospital and UI Health Care details came from search summaries whose source URLs I could not confirm.
- I could not read the HonorHealth PDF directly. Its specialty release table is quoted from a search summary.

---

## Q2. Room capabilities, shared equipment, instrument trays / sterile processing, implant vendor reps

### Takeaway
Rooms are not interchangeable. Robotic, hybrid, cysto, and similar rooms have fixed equipment, dedicated block allocations, and specialty-trained staff. Loaner instrument and implant sets usually must reach Sterile Processing **at least 48 hours** before the case, and first-time sets need more time. Vendor reps must be credentialed and tied to a specific case. Each of these is a resource the assistant has to check, or explicitly flag as unchecked, before it confirms a booking.

### Cited Findings
- Hybrid OR at Ulm: weekly blocks split among orthopedic trauma, vascular/cardiac, and neurosurgery. Spare hours are requested through a coordinator, and dedicated staff work with the robotic imaging system daily — [Siemens AXIOM Innovations, "The Multidisciplinary Hybrid OR" (2013)](https://marketing.webassets.siemens-healthineers.com/1800000001354483/4a04cfd2ef26/AX-AXIOM_Innovations_Dec_2013_The_Multidisciplinary_Hybrid_OR_1800000001354483.pdf)
- A neurosurgical hybrid-OR study (1,865 cases) proposed a scoring scale to rank which cases most need the hybrid room — [Sun et al., via NGDC](https://ngdc.cncb.ac.cn/openlb/publication/OLB-PM-40100554)
- AORN education on robotic scheduling covers block-release criteria and open-time management for robotic rooms — [AORN, "Maximizing Robotic Utilization with Scheduling Best Practices"](https://aorn.org/details/scheduling-robotic-surgery-in-OR)
- Robotics blocks auto-release at 14 days, against 7 days for other blocks — [St. Charles Policy 9579](https://WWW.STCHARLESHEALTHCARE.ORG/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgicalProceduralBlockManagementRedmond-Policy9579.pdf)
- Loaner trays: check-in on arrival **48 hours before the procedure** — [University of Toledo SP1-4 Loaner Trays](https://www.utoledo.edu/policies/utmc/sterile_processing/pdfs/SP1-4-loaner-trays.pdf)
- Loaner sets must reach Sterile Processing at least 48 hours ahead, and **first-time vendor sets need 3 business days**. Vendors must train SPD staff on decontamination, inspection, assembly, and sterilization of their sets — [UTMB policy](https://www.utmb.edu/policies_and_procedures/20038472)
- 48-hour allowance for reprocessing — [Ohio State Wexner loaner policy](https://wexnermedical.osu.edu/-/media/files/wexnermedical/utility/footer-pages/vendor-interaction/osu-loaner-policy.pdf)
- IAHCSMM Orthopedic Council recommends that loaner programs define request timing and pre-/post-procedure processing times. Reps tag each tray with **surgeon, date, and procedure** — [Infection Control Today, "Challenges Associated with Loaner Instrumentation"](https://www.infectioncontroltoday.com/view/challenges-associated-loaner-instrumentation)
- The vendor must provide a verified inventory at delivery or is responsible for missing items — [Denver Health, Management of Loaner and Consignment Instruments and Implants](https://denverhealth.org/-/media/files/about/for-vendors/2023/management-of-loaner-and-consignment-instruments-and-implants)
- Instrument trays should not exceed 25 lb (described as an AAMI/AORN national recommendation) — [Becker's ASC, Loaner Instrumentation Checklist](https://www.beckersasc.com/asc-accreditation-and-patient-safety/loaner-instrumentation-checklist-10-steps-to-follow/)
- Reps bringing trays must show ID and log into the facility's tracking system — [University of Toledo SP1-4](https://www.utoledo.edu/policies/utmc/sterile_processing/pdfs/SP1-4-loaner-trays.pdf)
- CMS CoP requires OR suites to have a call-in system, cardiac monitor, resuscitator, defibrillator, aspirator, and tracheotomy set, plus adequate equipment for sterilization — [42 CFR 482.51(b)](https://www.law.cornell.edu/cfr/text/42/482.51)

### Inferences
- **Hard constraints for the prototype:** (1) the case's required room capability (robot, fluoroscopy/C-arm, hybrid imaging, laminar flow for implants, cysto table, microscope) must be satisfied by the room; (2) a shared mobile asset (C-arm, robot, microscope, laser) cannot be double-allocated to overlapping times; (3) if a loaner/implant set is needed and the case is under 48 hours out (or under 3 business days for a first-time set), the assistant must not confirm as "ready". It should either flag "requires SPD/vendor confirmation" or escalate.
- Instrument trays owned by the hospital also turn over (decontaminate, assemble, sterilize). When several same-procedure cases fall on one day, tray count is a real constraint. Model it as inventory per tray type per day.
- Vendor rep scheduling is a soft-to-hard constraint. Many implant cases cannot proceed without the rep, so the assistant should collect "rep required? which company?" at booking and send a notification task. It should not assume availability.

### Gaps
- I did not find a public, primary source for typical in-house SPD turnaround times (hours per tray cycle) or for laminar-flow room requirements for arthroplasty. These are facility-specific; treat any number used in the prototype as illustrative.
- I could not verify the AAMI ST79 text directly (paywalled). The 48-hour rule is documented as common hospital policy, not as a quoted national standard.
- Vendor rep credentialing systems (e.g., third-party credentialing platforms) are widely used, but I did not retrieve a citable source on specific requirements.

---

## Q3. Staffing, surgeon availability, and concurrent / overlapping surgery

### Takeaway
Every room-hour also needs people: at minimum an RN circulator (AORN's position: one per patient), a scrub (RN, LPN, or surgical tech), and anesthesia coverage. When an anesthesiologist medically directs CRNAs, the ratio is capped at **1:4 concurrent cases** for Medicare billing (TEFRA). Surgeons may run overlapping rooms only if their critical portions do not overlap, and the patient must be informed. Truly concurrent surgery, with critical portions overlapping, is considered inappropriate by the ACS. Surgical privileges must match the procedure.

### Cited Findings
- CMS CoP: the OR must be supervised by an experienced RN or MD/DO. A qualified RN may circulate. LPNs and surgical techs may scrub under RN supervision, and may assist with circulating where state law and medical staff policy allow, provided an RN is immediately available — [42 CFR 482.51(a)](https://www.law.cornell.edu/cfr/text/42/482.51)
- CMS CoP: surgical privileges are delineated per practitioner by competency, and **a roster of each practitioner's surgical privileges must be kept** by the surgical service — [42 CFR 482.51(a)(4)](https://www.law.cornell.edu/cfr/text/42/482.51)
- AORN position (2014; endorsed by ANA): every patient undergoing a surgical or invasive procedure should at minimum have an RN in the circulating role, in any setting — [ANA, "One Perioperative Registered Nurse Circulator"](https://nursingworld.org/practice-policy/nursing-excellence/official-position-statements/id/one-perioperative-registered-nurse-circulator)
- AORN Safe Staffing and On-Call position statement (revised 2021): the staffing plan **begins when the procedure is scheduled** and runs through the postoperative phase. It includes sample staffing formulas — [AORN position statement (2021)](https://www.aorn.org/docs/default-source/guidelines-resources/position-statements/personnel-staffing/posstat-staffingoncall-0721.pdf)
- TEFRA (1982) and the 1998 HCFA/CMS final rule: an anesthesiologist may medically direct and bill **at most four concurrent cases** (modifier QK). Seven requirements apply, including the pre-anesthesia exam, participation in the most demanding parts (e.g., induction and emergence), and staying physically present. Failing the requirements converts billing to medical supervision (QZ) — [Coronis Health, TEFRA medical direction documentation guidelines](https://www.coronishealth.com/archive-guidelines-anesthesiologist-hcfa-final-rule-tefra-1198/)
- ACS: **concurrent** surgery, where critical or key portions of two operations overlap, is inappropriate. **Overlapping** surgery is acceptable when the critical portions of the first operation are complete, or when another attending is assigned to be immediately available in the first room. The patient must be informed in both cases — [AAHKS summary of ACS updated statement on concurrent surgeries](https://www.aahks.org/acs-updates-statement-on-concurrent-surgeries/)
- For Medicare teaching-setting billing of overlapping operations, CMS requires the surgeon's presence for the critical or key portions of both operations — [AAHKS/ACS summary](https://www.aahks.org/acs-updates-statement-on-concurrent-surgeries/); see also [COPIC, "Ask ECRI: Overlapping Surgeries"](https://www.copic.com/?p=2573)
- OR capacity depends on trained staff, and robotic and endoscopic case growth strains specialty staffing — [University of Twente LNMB OR planning course slides](https://www.utwente.nl/choir/en/education/PhDstudents/LNMB_ORinHealthcare_coursePhDs/College%202%20(operating%20room%20scheduling).pdf)

### Inferences
- **Hard:** (1) a surgeon cannot be booked into two rooms whose critical portions overlap. Since a scheduler rarely knows critical-portion timing, the safe prototype rule is "no overlapping booked times for the same surgeon unless the case is flagged as an approved overlapping/flip-room pattern"; (2) the surgeon must hold privileges for the procedure, checked against the privileges roster; (3) a room cannot run without a circulator and anesthesia coverage. Anesthesia coverage per anesthesiologist is capped at 1:4 medically directed rooms. Local practice is often 1:2 or 1:3, so make it configurable.
- Specialty teams (cardiac pump, robotic-trained scrub, neuro-monitoring, pediatric anesthesia) are hard resource constraints on certain case types. The assistant should check them or, more realistically, mark them "pending staffing confirmation" and route the case to the charge nurse or anesthesia scheduler.
- "Flip rooms" (one surgeon, two rooms) is a legitimate pattern that the assistant should neither block outright nor create without authorization.

### Gaps
- I did not retrieve ASA's own current statement on medical direction ratios. Claims about typical real-world ratios (2:1 vs 3:1) and a figure that TEFRA requirements were unmet in 35% of 2:1 and 99% of 3:1 scenarios appeared only in secondary sources with unclear attribution, so they are excluded.
- State-specific CRNA supervision rules (opt-out states) and state concurrent-surgery laws were not researched in depth.

---

## Q4. Time constraints: prime time, turnover, case duration, overtime cost

### Takeaway
A booking has to fit case duration plus turnover inside staffed hours. Running past the scheduled end means over-utilized time, which costs roughly $36-37 per OR minute (2005-2014 California data; likely higher now) plus overtime labor. Turnover averages about 25-45 minutes depending on setting and definition. Case duration is uncertain, and that uncertainty matters as much as the mean.

### Cited Findings
- Mean cost of 1 OR minute: **$37.45 inpatient, $36.14 ambulatory** (California, FY2005-2014). Direct costs were 54.6% and 59.1% of total, with wages and benefits the largest component — [Childers & Maggard-Gibbons, JAMA Surgery 2018 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/5875376)
- A 2026 JAMA Surgery update (Ashrafi, Maggard-Gibbons, Childers) says the earlier estimates are likely obsolete because of COVID-19, inflation, and consolidation. The updated per-minute figure was not visible in what I retrieved — [JAMA Surg 2026, DOI 10.1001/jamasurg.2026.2355 (index listing)](https://www.citedrive.com/en/discovery/costs-charges-and-revenue-of-hospital-operating-rooms-in-california/)
- Turnover: Advocate Health (2025) reported average turnover of **43 min in the OR and 31 min in the ASC**, and cited a 2012 survey of 134 hospitals with a range of 15-40 min and a **median of 28.5 min** — [Advocate Health nursing conference poster (2025)](https://institutionalrepository.aah.org/nursing_conference/2025/quality/26)
- Definitions of turnover and start times vary among anesthesiologists, nurses, and surgeons — [UCSF, OR start times and turnover times](https://open-proposals.ucsf.edu/sites/default/files/chv/cw-projects-2024/1677821080/or_start_times_and_turnover_times.pdf)
- Dexter: decisions to reduce over-utilized OR time rely on **mean** case durations, while decisions to reduce patient and surgeon waiting rely on quantifying **uncertainty** in durations — [Dexter et al., Anesthesiology 2007 (UIowa PDF)](https://user.engineering.uiowa.edu/~csl/publications/pdf/2007%20Dexter%20Anethesiologist%20Decisionmaking%20Anesthesia.pdf)
- Utilization formulas count turnover time against block hours, so turnover is a scheduling quantity, not overhead — [UToledo policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)

### Inferences
- Model each case as `[start, start + predicted_duration + turnover)` in the room, and check it against the room's staffed hours (e.g., 07:30-15:30 prime time; local values vary). A booking that would push past staffed end time is a **soft** constraint with escalation: it may still be allowed with charge nurse/anesthesia approval, and the assistant should state the projected overrun in minutes.
- Use the surgeon-specific historical duration for the procedure (the EHR typically supplies it) rather than an LLM estimate. Show it with a range (e.g., P50/P80) so the coordinator sees the overrun risk.
- Prime-time hours (e.g., 07:30-15:30) are commonly cited but are local configuration. I found no single national standard.

### Gaps
- I found no authoritative US-wide source for a standard "prime time" window or overtime pay multipliers for OR staff. Treat 07:30-15:30 as illustrative.
- The 2026 updated OR cost-per-minute figure was not retrieved.

---

## Q5. Downstream capacity (PACU / inpatient / ICU beds) and case sequencing rules

### Takeaway
An OR slot is useless if there is no PACU, ICU, or inpatient bed afterwards. Elective schedules that ignore downstream beds cause PACU boarding and delays. Sequencing rules (latex-allergic patients first, contaminated cases typically last, children and insulin-dependent diabetics often early) are real but facility-specific and sometimes conflict.

### Cited Findings
- OR schedules are typically built around surgeon and staff preferences, while the effect on post-op beds is overlooked. That causes PACU boarding (patients held overnight in PACU when ICU is full). Smoothing daily bed occupancy via integer programming and simulation reduced boarding — [Price et al., Production and Operations Management 2011 (RTI)](https://www.rti.org/publication/reducing-boarding-post-anesthesia-care-unit)
- A constraint-programming re-sequencing of an elective pre-schedule suggested **20-30% reductions in expected peak PACU census** on most days — [Lyons, Begen & Bell, Analytics 2023 (DOI 10.3390/analytics2030036)](https://citedrive.com/en/discovery/surgery-scheduling-and-perioperative-care-smoothing-and-visualizing-elective-surgery-and-recovery-patient-flow)
- Heavy early-week elective volume consumes inpatient beds and delays add-on cases. Proposed fixes include spreading electives across the week and moving cases to outpatient or extended recovery — [Harvard D3 forum, "Smoothing OR flow"](https://d3.harvard.edu/platform-mhcdsolutions/submission/smoothing-or-flow/index.html); [Becker's, strategies to decrease boarding (citing Health Affairs)](https://www.beckershospitalreview.com/patient-experience/9-strategies-to-decrease-ed-boarding-at-hospitals/)
- Latex allergy should be noted on the OR schedule, and the patient booked as **first case of the day if possible**. Otherwise the room needs extended ventilation time to clear airborne latex proteins (Canadian ORNAC-based standard; US practice is similar but I found no US primary source) — [CPSBC/Northern Health, Latex Allergy standard](https://www.cpsbc.ca/files/pdf/NH-AS-Latex-Allergy.pdf)
- Highest-risk latex sensitization groups include patients with repeated surgeries (e.g., spina bifida), urogenital anomalies, and insulin-treated diabetics — [Latex Allergy in Children, PMC review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10779698/)

### Inferences
- **Prototype model:** each case carries `post_op_destination` (home same-day / PACU-only / inpatient floor / ICU / step-down). A booking that requires an ICU bed post-op on a day when ICU is projected full should trigger a **soft-to-hard** escalation ("requires bed management approval"), not a silent booking.
- Sequencing flags: `latex_allergy` → prefer first case; `contaminated/isolation (e.g., MRSA, C. diff, TB)` → typically last or followed by terminal clean; `pediatric` and `insulin-dependent diabetic / NPO-sensitive` → prefer early. Treat these as **soft preferences with policy overrides**, and surface them when they conflict (latex-allergic and contaminated means "first" and "last" pull opposite ways, so escalate).
- The assistant can surface these rules ("this patient has a latex allergy; first-case slot available Tues 7:30 in OR 4") as part of offering alternatives. That shows clinical-operational awareness without making clinical decisions.

### Gaps
- No primary source found for "contaminated/isolation cases last," or for pediatric/diabetic-first rules. These are widespread practice but local. A US hospital policy PDF would be needed for citation.
- AORN's current guidance on latex-safe environments, which may make "first case" unnecessary in fully latex-free ORs, was not retrieved.

---

## Q6. Add-on / emergent cases, bumping, cancellations, and day-of-surgery decisions

### Takeaway
Elective schedules are routinely disrupted by add-on and emergent cases (often triaged by urgency class) and by day-of-surgery cancellations. Published cancellation rates range from about 2% to 24%, with many studies in the 6-13% range, mostly from non-US settings. Dexter's ordered priorities for day-of changes are: (1) patient safety, completing scheduled cases unless unsafe; (2) reduce over-utilized time; (3) reduce waiting; (4) personal preferences.

### Cited Findings
- Dexter's four ordered priorities for day-of-surgery decisions: (i) perform all scheduled cases unless there is a patient safety concern, (ii) reduce over-utilized OR time, (iii) reduce patient and surgeon waiting, (iv) satisfy personal and professional priorities — [Dexter et al., Anesthesiology 2007](https://user.engineering.uiowa.edu/~csl/publications/pdf/2007%20Dexter%20Anethesiologist%20Decisionmaking%20Anesthesia.pdf); [Dexter, "Making management decisions on the day of surgery" (UIowa repository)](https://iro.uiowa.edu/esploro/outputs/journalArticle/Making-management-decisions-on-the-day/9983806376902771)
- Day-of-surgery cancellation: 7.3% in one study. The literature review cited reported rates from **1.96% to 24%** — [Bahrain Medical Bulletin (2018)](https://bahrainmedicalbulletin.com/MAR_2018/MAR2018_CANCELLATION.pdf). Other single-center studies (Iran, Nigeria) ranged from 0.46% to 20.2% — [JIMC, Northern Iran report](https://publish.kne-publishing.com/index.php/JIMC/article/view/17712); [Annals of Health Research, Nigeria audit](https://doaj.org/article/a819b2350c1b4fc28d77b233cc107c59)
- Dedicated add-on blocks can be badly under-used (15% of minutes used in one study) — [Georgia Tech ISyE capstone](https://capstone.isye.gatech.edu/node/5890)

### Inferences
- **Failure paths for the prototype:** (a) requested slot taken (race, see Q12); (b) slot exists but owned by another block, so offer a release request; (c) no capacity in window, so offer alternates (other rooms with the capability, other days, a waitlist); (d) add-on/urgent request, so the assistant should **not** decide who gets bumped. Bumping an elective case is a charge nurse / anesthesia / OR director decision and is a clear escalation point; (e) cancellation, which must release the room, equipment, tray, rep, and bed holds and notify downstream.
- Urgency classes (e.g., emergent within 1 hr, urgent within 4-6 hrs, add-on within 24 hrs) are widely used, but I found no single citable US standard. Model them as configurable categories with the escalation owner per category.
- Because cancellations are common, the assistant should tell the coordinator about known cancellation-risk signals (missing H&P, consent, prior auth, labs; see Q7) at booking time. That is a high-value, low-risk nudge.

### Gaps
- No US-national day-of-surgery cancellation rate retrieved. Most cited figures are international single-center studies.
- No citable US standard for add-on urgency classes or bumping policy. These are local (e.g., NSQIP or hospital-specific classifications).

---

## Q7. Pre-operative readiness: H&P / PAT, informed consent, privileges, prior authorization

### Takeaway
Several readiness items are set by regulation: an H&P within 30 days before (updated within 24 hours after admission), signed informed consent in the chart before surgery, and a privileged surgeon. Payer prior authorization is legally separate from scheduling but a frequent cause of cancellation. Medicare requires it for specific outpatient services. Since January 1, 2026, CMS-0057-F makes Medicare Advantage, Medicaid, CHIP, and Marketplace payers decide in **72 hours (expedited) / 7 calendar days (standard)**.

### Cited Findings
- H&P must be completed and documented **no more than 30 days before or 24 hours after admission/registration**, but before surgery. If done within the 30 days prior, an **update** is required within 24 hours after admission and before surgery. Medical staff may define outpatient procedures where an assessment replaces a full H&P — [42 CFR 482.51(b)(1)](https://www.law.cornell.edu/cfr/text/42/482.51)
- A properly executed **informed consent** form must be in the chart before surgery, except in emergencies — [42 CFR 482.51(b)(2)](https://www.law.cornell.edu/cfr/text/42/482.51)
- An **operating room register** must be complete and up to date — [42 CFR 482.51(b)](https://www.law.cornell.edu/cfr/text/42/482.51)
- Medicare hospital outpatient department (OPD) prior authorization (since July 2020, expanded 2021 and 2023) covers blepharoplasty, botulinum toxin injections, panniculectomy, rhinoplasty, vein ablation (2020); implanted spinal neurostimulators and cervical fusion with disc removal (2021); facet joint interventions (2023) — [CMS, Prior Authorization for Certain OPD Services](https://www.cms.gov/data-research/monitoring-programs/medicare-fee-service-compliance-programs/prior-authorization-pre-claim-review-initiatives/prior-authorization-certain-hospital-outpatient-department-opd-services)
- CMS-0057-F (Interoperability and Prior Authorization final rule): from **January 1, 2026**, impacted payers (MA, Medicaid, CHIP, FFE QHPs; not traditional Medicare or commercial employer plans) must decide expedited requests in 72 hours and standard requests in 7 calendar days, and give specific denial reasons. FHIR Prior Authorization APIs are due **January 1, 2027** — [ASPR CMS Solutions summary](https://asprcmsolutions.com/insights/cms-0057-f-prior-authorization-api-deadline-2026/); [Virginia DMAS Medicaid bulletin](https://vamedicaid.dmas.virginia.gov/vamed/download-pdf-bulletin/22237) (secondary; verify against CMS fact sheet)

### Inferences
- **Readiness checks the assistant should surface at booking**, as status rather than blockers, because most can be completed after the slot is reserved: H&P date vs surgery date (more than 30 days means a new H&P is needed); consent on file; prior auth status (required / submitted / approved / denied), with lead time for a 7-day standard decision; PAT/anesthesia pre-op clinic visit scheduled; required labs/imaging/clearances (cardiology, medical); implant/loaner/rep confirmed.
- **Hard at day of surgery, soft at booking:** H&P and consent do not need to exist when the case is booked, but they must exist before surgery. The prototype should book while creating follow-up tasks, and should never claim the case is "cleared".
- If the case is under 7 calendar days out and prior auth is not approved for an impacted payer, flag scheduling risk: the payer's standard decision window may not close in time.

### Gaps
- I did not verify whether the CMS OPD prior-auth list changed after 2023, beyond CMS's statement that changes go through notice-and-comment rulemaking. Check the CMS lookup tool.
- Commercial payer prior auth rules vary and are not covered by CMS-0057-F. State "gold-card" laws were not researched.

---

## Q8. HIPAA: minimum necessary, BAAs with LLM vendors, PHI in prompts/logs, audit controls

### Takeaway
An LLM vendor that receives, processes, or retains PHI (prompts, outputs, logs) for a hospital or for Qventus is a business associate (or subcontractor BA) and needs a BAA. The "conduit" exception does not cover cloud or LLM services that persist data. Audit controls (45 CFR 164.312(b)) are a required Security Rule standard. A major Security Rule overhaul was proposed in January 2025 but is **not final**: the 2026 Unified Agenda projects July 2027.

### Cited Findings
- HHS/OCR cloud computing guidance: a cloud service provider that creates, receives, maintains, or transmits ePHI is a business associate **even if the data is encrypted and the CSP lacks the key** ("no-view" services). The conduit exception covers only transient transmission, not persistent storage — [Hunton, "HHS Releases Guidance on HIPAA and Cloud Computing"](https://www.hunton.com/privacy-and-cybersecurity-law-blog/hhs-releases-guidance-hipaa-cloud-computing); [Crowell client alert](https://www.crowell.com/en/insights/client-alerts/the-office-of-civil-rights-issues-demanding-hipaa-guidance-to-cloud-services-providers)
- CSPs that handle ePHI as subcontractors of a business associate are themselves business associates and need BAAs. The guidance permits offshore storage if the risk is addressed — [Hunton summary](https://www.hunton.com/privacy-and-cybersecurity-law-blog/hhs-releases-guidance-hipaa-cloud-computing)
- Standard consumer LLM endpoints do not come with a BAA. Enterprise tiers of major providers (e.g., OpenAI Enterprise, Anthropic enterprise, Azure OpenAI, Amazon Bedrock) are reported to support BAAs. BAAs should address model training/fine-tuning restrictions, retention and deletion, breach notification timing, and subcontractor flow-down — [Medcurity, HIPAA Compliance for Generative AI](https://medcurity.com/hipaa-compliance-generative-ai/); [Respan, HIPAA BAA LLM engineering (May 2026)](https://www.respan.ai/resources/hipaa-baa-llm-engineering) (vendor/secondary sources; confirm current terms directly with each vendor)
- A BAA is necessary but not sufficient. The deployer remains responsible for audit logging, access control, encryption, and keeping PHI out of system prompts, eval datasets, and logs — [Promise Legal, HIPAA and AI for health tech founders](https://blog.promise.legal/hipaa-ai-compliance-health-tech/) (secondary)
- Audit controls, 45 CFR 164.312(b): mechanisms to **record and examine activity** in systems containing ePHI. It is a required standard — [AFS Law, Proposed changes to the HIPAA Security Rule](https://www.afslaw.com/perspectives/health-care-counsel-blog/proposed-changes-the-hipaa-security-rule-what-regulated)
- HIPAA Security Rule NPRM: announced December 27, 2024 and published January 6, 2025 (comments closed March 7, 2025). It would make all implementation specifications mandatory, require annual compliance audits, and set intervals for written risk analysis, vulnerability scanning, and pen testing. The 2026 Unified Agenda lists it as a **long-term action, with final action projected July 2027**. A coalition of 100+ organizations led by CHIME urged withdrawal (Dec 8, 2025) — [McDermott, "Final action on HIPAA Security Rule modifications now projected for July 2027"](https://www.mcdermottlaw.com/?p=50371417); [Paubox](https://www.paubox.com/blog/hhs-pushes-final-hipaa-security-rule-update-to-2027); [Orrick, Jan 2025](https://www.orrick.com/en/Insights/2025/01/Proposed-HIPAA-Security-Rule-Update-What-It-Means-for-Cybersecurity-in-Health-Care)

### Inferences
- **Minimum necessary for the prototype:** the scheduling task needs patient identity (name, DOB, MRN), procedure, laterality, surgeon, payer/auth status, and a few safety flags (latex allergy, isolation, implant). It does not need the full chart, notes, or diagnoses beyond what booking requires. Design tool calls to return only those fields. Reference patients by internal ID in LLM context where possible, and resolve display names in the UI layer.
- **Logs:** conversation transcripts that include PHI are ePHI and need the same protection, retention policy, and access controls. Redact or tokenize PHI before sending traces to third-party observability tools that lack a BAA.
- **Audit trail:** every state-changing action (hold, book, modify, cancel) should record who (authenticated coordinator), what (before/after), when, via which channel (assistant vs direct EHR), and the confirmation step. This serves both 164.312(b) and the CMS "operating room register" expectation.
- Qventus would be a business associate of the hospital, and its LLM provider a subcontractor BA. The prototype write-up should state this chain explicitly.

### Gaps
- I did not retrieve OCR's primary cloud-computing guidance page directly (summaries only), or any OCR guidance specific to generative AI or LLM prompts. To my knowledge none exists as of this date, but I did not confirm that.
- No result discussed how the minimum-necessary standard (45 CFR 164.502(b)) applies to LLM context windows. The inference above is mine.

---

## Q9. CMS Conditions of Participation and Joint Commission Universal Protocol: booking accuracy

### Takeaway
Wrong-site, wrong-procedure, and wrong-patient prevention begins at scheduling. Universal Protocol pre-procedure verification includes checking patient, procedure, site, and laterality **at the time of scheduling**, with "right," "left," and "bilateral" spelled out. A conversational assistant that garbles laterality or procedure is creating exactly the discrepancy the Protocol is built to catch.

### Cited Findings
- The Universal Protocol has three parts: pre-procedure verification, site marking, and time-out. Its goal is correct patient, correct procedure, correct site. The 2009 revision (after the 2007 Wrong Site Surgery Summit) required verification at multiple points, including preadmission testing, and expects use of a standardized checklist — [OR Manager, Joint Commission Universal Protocol (2009)](https://www.ormanager.com/wp-content/uploads/pdfx/ORMVol24No8JCuniversalProtocol09.pdf); [ASC Quality Collaboration, Universal Protocol and Time Out Policy template (2024)](https://ascquality.org/wp-content/uploads/2024/10/Universal-Protocol-and-Time-Out-Policy.docx)
- Hospital policy example: the surgery-scheduling clerk verifies the operative procedure, including site-specific identification, **at the time of scheduling** — [Floyd Health, PCS-03-003 Wrong Site Surgery](https://www.floyd.org/Documents%20Medical%20Staff/PCS-03-003%20Wrong%20Site%20Surgery.pdf)
- UP policies seen in search list the scheduler's required data as: patient full legal name (correctly spelled), DOB, procedure name **with site and laterality**, performing physician, and implants/special equipment. "Right," "left," or "bilateral" are written out, not abbreviated (from a hospital/ASC UP policy among [Floyd](https://www.floyd.org/Documents%20Medical%20Staff/PCS-03-003%20Wrong%20Site%20Surgery.pdf) and [ASC Quality Collaboration](https://ascquality.org/wp-content/uploads/2024/10/Universal-Protocol-and-Time-Out-Policy.docx); exact document not pinned down)
- Consent forms, imaging, medical records, and surgical site / laterality / spinal **level** must agree. Discrepancies are resolved before proceeding — [PSMF, Wrong Site Surgery](https://psmf.org/?p=197131)
- Site marking applies where more than one location is possible (limbs, digits, lesions, spinal levels, organs) — [Floyd Health policy](https://www.floyd.org/Documents%20Medical%20Staff/PCS-03-003%20Wrong%20Site%20Surgery.pdf)
- CMS CoP for surgical services: services must follow accepted standards of practice. The OR register must be complete and current. Consent and H&P are prerequisites (see Q7) — [42 CFR 482.51](https://www.law.cornell.edu/cfr/text/42/482.51)

### Inferences
- **Hard constraints for the prototype:**
  1. Never infer or default laterality. If the procedure is lateral (knee, hip, shoulder, eye, hernia, digit, breast, kidney, etc.) and laterality isn't stated, the assistant must ask.
  2. Spell out laterality in full in all summaries and confirmations. Use "Left," never "L" or "lt".
  3. For spine, capture level(s).
  4. Read back patient (name + DOB + MRN), procedure, laterality/level, surgeon, date/time, and room in a structured confirmation card before committing.
  5. If the procedure text conflicts with the order or referral on file (e.g., the order says right, the coordinator says left), stop and escalate. Do not "pick one".
- The assistant should source procedure descriptions and codes from the EHR's procedure master or the surgeon's order (tool lookup), never from free LLM generation (see Q12).

### Gaps
- I did not access the current Joint Commission UP standard text (UP.01.01.01 and following) directly. Note that the Joint Commission restructured its hospital accreditation manual in 2025-2026 ("Accreditation 360"), so standard numbering may have changed. Not verified here.
- No quantitative data found on the share of wrong-site events that originate in scheduling errors.

---

## Q10. Device status, decision-support transparency, nondiscrimination, state AI laws, and 2025-2026 AI governance guidance

### Takeaway
A pure scheduling assistant falls under the Cures Act's **administrative-support exclusion** from the FDA device definition, which explicitly names "appointment schedules." It does not have to clear the CDS criteria, provided it does not recommend diagnosis or treatment. ONC HTI-1 decision-support transparency rules bind certified EHR developers (e.g., Epic), not a third-party scheduling chatbot, and HTI-5 (proposed late 2025 / Jan 2026) would remove the "AI model card" source-attribute requirements. The Joint Commission/CHAI guidance (Sept 2025) is non-binding but explicitly covers scheduling tools. Texas and California disclosure laws mostly target patient-facing or clinical AI.

### Cited Findings
- **FDA / statute:** FD&C Act §520(o)(1)(A) [21 U.S.C. 360j(o)(1)(A)] excludes from the device definition software intended "for administrative support of a health care facility," including financial records, **appointment schedules**, billing, and inventory management — [21 U.S.C. 360j (LII)](https://www.law.cornell.edu/uscode/text/21/360j)
- FDA's guidance on Cures Act §3060 software changes (final, Sept 2019) implements these exclusions — [FDA guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/changes-existing-medical-software-policies-resulting-section-3060-21st-century-cures-act)
- **FDA CDS guidance revised January 6, 2026**, superseding the 2022 version. FDA now says it will exercise enforcement discretion for single-recommendation CDS when only one option is clinically appropriate. Image and signal analysis stays regulated. The guidance was issued without public comment — [Covington, "5 key takeaways from FDA's revised CDS guidance" (Jan 2026)](https://www.cov.com/en/news-and-insights/insights/2026/01/5-key-takeaways-from-fdas-revised-clinical-decision-support-cds-software-guidance); [FDA Law Blog (Jan 2026)](https://www.thefdalawblog.com/2026/01/a-busy-day-in-the-cdrh-neighborhood-updates-to-the-cds-and-general-wellness-guidance-documents/). One source mentioned a further revision on Jan 29, 2026, which I could not confirm.
- **ONC/ASTP HTI-1** decision support interventions criterion (§170.315(b)(11)) requires certified developers to supply source attributes ("AI model cards") for predictive DSIs. **HTI-5 proposed rule** (covered January 2026) would remove the source-attribute and risk-management requirements, retire the legacy CDS criterion (a)(9), and eliminate 34 of 60 certification criteria, including the §170.315(d) privacy and security criteria — [Covington blog, Jan 15, 2026](https://www.covingtonblogs.com/2026/01/15/hhs-proposes-changes-to-the-health-it-certification-program-and-information-blocking-regulations-in-hti-5-proposed-rule/); [Drummond Group](https://www.drummondgroup.com/blog/how-the-hti-5-proposed-rule-affects-certification/); [Reed Smith](https://www.reedsmith.com/our-insights/blogs/health-industry-washington-watch/102m1ob/hti-5-proposal-signals-health-it-deregulation-and-fhir-first-interoperability-and/). **Final status not confirmed.**
- **Joint Commission + CHAI, "Responsible Use of AI in Healthcare" (Sept 17, 2025):** non-binding and high-level. It applies to clinical, administrative, and operational AI, **explicitly including scheduling**. Its seven elements: (1) AI policies and governance; (2) patient privacy and transparency (disclose AI use); (3) data security and data-use protections (vendor agreements restricting data use and re-identification, audit rights); (4) ongoing quality monitoring, including human-in-the-loop review and validation of vendor tools; (5) voluntary, blinded AI safety-event reporting (e.g., to PSOs); (6) risk and bias assessment; (7) education and training. Playbooks and a voluntary certification are forthcoming — [Polsinelli](https://www.polsinelli.com/publications/tjc-chai-release-guidance-responsible-ai-use-healthcare); [Parker Poe (Nov 2025)](https://parkerpoe.com/news/2025/11/new-national-guidance-lays-out-responsible-use-of)
- **Section 1557 (45 CFR 92.210):** covered entities must not discriminate through "patient care decision support tools," must make reasonable efforts to identify tools that use race, color, national origin, sex, age, or disability inputs, and must mitigate the risk. Compliance deadline May 1, 2025. The definition covers tools that "support clinical decision-making" — [Health Affairs Forefront](https://www.healthaffairs.org/content/forefront/section-1557-rule-mandates-identification-and-mitigation-discriminatory-clinical); [AMN Section 1557 readiness workshop](https://prod.amnhealthcare.com/siteassets/language-services/section-1557-compliance-materials/section-1557-readiness-workshop---may-and-july-requirements.pdf). Current enforcement posture under the present administration not confirmed.
- **California AB 3030** (effective Jan 1, 2025): generative-AI **patient communications** with clinical information need a prominent AI disclaimer and instructions for reaching a human. Exempt if a licensed provider reads and reviews the message before it is sent — [Arent Fox Schiff](https://www.afslaw.com/perspectives/alerts/california-requires-disclaimers-health-care-providers-ai-generated-patient-communications)
- **Texas:** SB 1188 (effective Sept 1, 2025) lets practitioners use AI for diagnosis/treatment if they personally review AI output and disclose AI use to patients. TRAIGA / HB 149 (effective Jan 1, 2026) requires providers to disclose AI use in services or treatment. AG enforcement carries penalties of $10,000-$200,000 per violation — [Bass Berry](https://bassberry.com/news/texas-illinois-and-colorado-legislative-developments-impact-healthcare-ai-and-other-industries-while-u-s-congress-fails-to-pass-moratorium/); [Akerman, "New Year, New AI Rules" (Jan 2026)](https://www.akerman.com/en/perspectives/hrx-new-year-new-ai-rules-healthcare-ai-laws-now-in-effect.html)
- **Colorado:** the original AI Act, already delayed to June 30, 2026, was **repealed and replaced by SB 26-189** (signed May 14, 2026). The new law is narrower and transparency-focused around automated decision-making technology, takes effect **January 1, 2027**, and lists health care services among consequential decisions — [Mayer Brown (May 2026)](https://www.mayerbrown.com/insights/publications/2026/05/colorado-enacts-new-admt-law-replacing-colorado-ai-act); [Goodwin (June 2026)](https://www.goodwinlaw.com/en/insights/publications/2026/06/alerts-technology-fs-colorado-enacts-law-repealing-replacing-landmark-ai-act)

### Inferences
- **Device status:** an assistant that checks availability and books cases is administrative support and not a device. Scope creep changes that. If it starts recommending *which procedure*, *whether the patient is fit for surgery*, or *clinical urgency/triage*, it moves toward CDS or device territory. The design should say explicitly: the assistant never makes clinical determinations, never assigns urgency class, and never decides who is bumped.
- **HTI-1/HTI-5:** a Qventus assistant sold to hospitals is not certified health IT, so HTI-1 DSI source-attribute obligations do not apply directly. Publishing a lightweight "model card" (intended use, out-of-scope uses, known failure modes) still aligns with the TJC/CHAI guidance and is cheap credibility.
- **Disclosure:** an internal staff-facing tool (coordinator-facing) mostly falls outside AB 3030 (patient communications) and the Texas patient-disclosure provisions. If the prototype ever sends patient-facing messages (e.g., date confirmations with pre-op instructions), disclaimers or human review apply in CA, and AI-use disclosure in TX.
- **Section 1557:** a scheduling assistant probably isn't a "patient care decision support tool," since it supports operational rather than clinical decisions. If it prioritizes waitlists or alternate slots using age, disability, or language, though, it would be prudent to show non-discriminatory logic. This is my inference and not legal advice.
- **TJC/CHAI alignment for the write-up:** governance owner, human confirmation before writes, monitoring metrics (booking-error rate, escalation rate, override rate), AI-incident reporting path, and staff training.

### Gaps
- Whether HTI-5 has been finalized as of Oct 2026 was not confirmed.
- Whether the FDA CDS guidance had a second revision (Jan 29, 2026) was not confirmed.
- Section 1557 §92.210's current enforcement status (possible rescission or non-enforcement) was not confirmed.
- HHS's broader AI strategy and any 2025-2026 OCR AI guidance were not researched in depth.
- Other states with health-AI laws (e.g., Illinois, Utah) were not researched.

---

## Q11. EHR integration and write-back: Epic OpTime APIs, HL7 v2 SIU, FHIR Appointment

### Takeaway
Epic publicly documents an **outbound-only** HL7v2 "Outgoing Surgical Case Scheduling" interface (new, rescheduled, updated, and canceled cases) and an **inbound** "Surgical Case Tracking" interface (case events and timestamps). There is no public inbound surgical-case booking interface. Epic's public FHIR scheduling services are described as "prototypes" oriented to ambulatory (Cadence) appointments. A realistic integration therefore reads OR schedule data via feeds and APIs, and writes either a **case request** for a human to finalize or through a site-specific, Epic-approved integration. It does not assume open FHIR write access to OpTime.

### Cited Findings
- Epic open.epic HL7v2 scheduling interfaces, **outgoing**: "Outgoing Surgical Case Scheduling" sends case scheduling information to external systems for new, rescheduled, updated, and canceled cases. "Outgoing Appointment Scheduling" notes that surgical case schedules require the surgical case interface. **Incoming**: "Incoming Appointment Scheduling" (new, rescheduled, updated, canceled appointments; no-shows); "Incoming Surgical Case Tracking" (real-time case events and timestamps for the case log, integrated with e.g. Amazon, ARTISIGHT, TeleTracking); "Incoming Schedule Query"; "Incoming External Appointments". **No public inbound surgical-case scheduling interface is listed** — [open.epic, Scheduling HL7v2](https://open.epic.com/Scheduling/HL7v2)
- Epic open.epic FHIR scheduling: "These prototype services demonstrate scheduling an appointment using FHIR." No surgical/OpTime specifics given — [open.epic, Scheduling FHIR](https://open.epic.com/Scheduling/FHIR)
- Epic FHIR booking uses STU3 `Appointment/$find` and `$book` operations, which work only after the health system has built scheduling rules in Cadence (ambulatory). Many Epic scheduling endpoints are proprietary, so workflows mix FHIR and non-FHIR calls — [Nirmitee, FHIR scheduling across Epic/Oracle/athena](https://nirmitee.io/blog/fhir-scheduling-api-appointment-slot-epic-oracle-athenahealth/); [Mindbowser, Epic scheduling API guide](https://www.mindbowser.com/epic-scheduling-api-guide/) (secondary vendor blogs)
- HL7 v2 SIU event codes: S12 new appointment, S14 modification, S26 cancellation (and others), carried with SCH/PID/PV1/AIL/AIP segments. Epic routes them through its Bridges interface engine — [Mindbowser, Referral loops in Epic](https://www.mindbowser.com/referral-loops-in-epic-ehr/); SIU S12-S22 field requirements (v2.5.1) in a non-Epic implementation — [Infor docs](https://docs.infor.com/mscm/2025.x/en-us/mscmolh/mscmag/cpr1537939813847.html)
- Real-world example of two-way OR integration difficulty: a two-way QGenda–OpTime feed was "set up" but "not live yet (in process)" — [University of Colorado I&E award submission (QGenda)](https://www.cu.edu/print/controller/i-e-awards/past-submissions/cu-ie-submission-qgenda). Maastricht UMC used an HL7 SIU interface for real-time surgical-schedule sync between Epic and SAP — [Nordic case study](https://www.nordicglobal.com/hubfs/Maastricht%20UMC+%20-%20Case%20Study.pdf)
- OpTime handles block time assignment, preference cards, and staff allocation within Epic — [Folio3, Epic OpTime overview](https://digitalhealth.folio3.com/blog/epic-optime-features-uses-benefits/) (secondary)

### Inferences
- **Source of truth is the EHR (OpTime)**, not the assistant. The prototype should treat its own availability view as a cache with a freshness timestamp, and re-validate against the source immediately before any write.
- **Realistic write patterns, ranked by feasibility:** (1) the assistant prepares a fully structured **case request** that a coordinator submits in OpTime (zero write integration; human-in-the-loop by construction); (2) the assistant writes via a site-approved Epic integration (private APIs or an Epic-approved app; needs per-customer Epic analyst work); (3) an internal scheduling layer that Qventus owns, with outbound sync. For a take-home prototype, a mock "EHR scheduling service" with explicit `hold`, `book`, and `cancel` endpoints and an outbound SIU-like event stream is a defensible abstraction. The write-up should say real write-back is site- and vendor-dependent.
- Outbound SIU feeds are eventually consistent: the assistant's view can lag the EHR by seconds to minutes. That is one reason to re-check at commit time.
- Latency budget: a chat turn that calls several tools (patient lookup, availability, equipment, staffing) should run them in parallel and stream partial results. EHR API latencies vary by site. I found no published Epic latency SLAs.

### Gaps
- Epic's technical specs for surgical interfaces, including whether OpTime accepts inbound case requests via HL7 (e.g., SRM/SRR) or private APIs, require an open.epic/Epic login and were not accessible.
- Other EHRs (Oracle Health/Cerner SurgiNet, MEDITECH) were not researched.
- No published Epic API latency or rate-limit numbers were found.

---

## Q12. Concurrency, idempotency, LLM-specific risks, human-in-the-loop, role-based access

### Takeaway
The main technical risks are (a) two coordinators (or a coordinator and an add-on) claiming the same room-time, (b) duplicate bookings from retries, and (c) an LLM fabricating or mutating clinical identifiers. Benchmark evidence shows LLMs reproduce exact CPT codes from descriptions **under 50%** of the time (GPT-4: 49.8% CPT, 33.9% ICD-10-CM in 2024). Identifiers must therefore come from deterministic lookups, never from model generation, and every write needs explicit human confirmation.

### Cited Findings
- NEJM AI (Soroush et al., April 2024; DOI 10.1056/AIdbp2300040): across 27,000+ codes from a year of Mount Sinai care, all models tested (GPT-4, GPT-3.5, Gemini-pro, Llama-2-70b) were **below 50% exact-match** accuracy. GPT-4 scored about 45.9% ICD-9-CM, 33.9% ICD-10-CM, and 49.8% CPT. Errors included imprecise and **fabricated** codes, and the authors concluded models are not ready to automate coding without human oversight — [Healthcare IT News](https://www.healthcareitnews.com/news/llms-are-not-ready-automate-clinical-coding-says-mount-sinai-study); [Mount Sinai press release](https://mountsinai.org/about/newsroom/2024/despite-ai-advancements-human-oversight-remains-essential). (2024 model generation; current models likely better but not re-benchmarked here.)
- TJC/CHAI guidance calls for "human in the loop" review, ongoing monitoring of vendor tools, and AI incident reporting — [Parker Poe](https://parkerpoe.com/news/2025/11/new-national-guidance-lays-out-responsible-use-of)
- Texas SB 1188 requires practitioners to personally review AI-generated content before clinical decisions. This applies to clinical rather than scheduling use, but it shows the regulatory direction — [Bass Berry](https://bassberry.com/news/texas-illinois-and-colorado-legislative-developments-impact-healthcare-ai-and-other-industries-while-u-s-congress-fails-to-pass-moratorium/)
- AORN: the staffing plan begins when the procedure is scheduled, so a booking change propagates to staffing — [AORN Safe Staffing position statement (2021)](https://www.aorn.org/docs/default-source/guidelines-resources/position-statements/personnel-staffing/posstat-staffingoncall-0721.pdf)
- The proposed HIPAA Security Rule would require mandatory controls across all implementation specifications. Commentary suggests these would extend to AI tools, such as revoking AI tool access on termination (vendor commentary, not rule text) — [Varonis, Decoding Proposed HIPAA Security Rule changes](https://www.varonis.com/blog/hipaa-nprm)

### Inferences
These are design inferences, mostly standard distributed-systems and LLM-safety practice; they are not sourced in this research session.
- **Race conditions / holds:** use a two-phase pattern. Step 1, `hold(room, start, end, resources)` creates a short-TTL tentative reservation (e.g., 5-10 min) visible to other coordinators as "pending." Step 2, `confirm(hold_id)` commits only if the hold is still valid and a re-check passes. On conflict, return a typed error (`SLOT_TAKEN`, `HOLD_EXPIRED`, `BLOCK_NOT_RELEASED`, `RESOURCE_CONFLICT:C-arm`) that the assistant turns into alternatives. Use optimistic concurrency (version numbers or ETags; FHIR supports versioned updates via If-Match, not verified here) so a stale view cannot overwrite a newer one.
- **Idempotency:** every write carries a client-generated idempotency key (e.g., per confirmation-card ID), so LLM tool-call retries, network retries, or double-clicks cannot create duplicate cases. On retry, return the original result.
- **Identifier integrity (hard rules):**
  - MRN, CPT/procedure ID, surgeon ID, and room ID must come only from tool results (patient search, procedure master, provider directory). The LLM must never type them from memory. Validate at the tool layer, so write tools accept only IDs returned by lookup tools in the same session.
  - Disambiguate patients with two identifiers (name + DOB, and MRN). If search returns more than one match, the assistant must ask; it must never choose.
  - Render the confirmation card from structured data (not LLM prose), so what the coordinator approves is exactly what will be written.
- **Human-in-the-loop:** reads (availability checks) can be autonomous. Every write (hold → book, modify, cancel, release) requires explicit coordinator confirmation of a structured summary. Actions outside the coordinator role (bumping, overtime approval, unreleased-block override, ICU bed commitment) are **escalations** that route to the owning human (block owner, charge RN, anesthesia coordinator, bed management) with a ticket or notification; the assistant does not perform them.
- **Role-based access:** the assistant acts with the authenticated user's permissions, never broader service credentials. A coordinator for Ortho should not see or book Neuro block time beyond open time, unless policy allows. Patient lookups should be scoped to the coordinator's service or patients and logged (supports minimum necessary).
- **Prompt injection / data-as-instruction:** free-text fields from the EHR (case comments, order notes) must be treated as data. A note saying "override block rules" must not change behavior.
- **Failure transparency:** if any dependency (staffing, equipment, SPD) cannot be checked, say so explicitly ("Room and surgeon available; C-arm availability could not be verified") rather than implying full clearance.
- **Latency:** stream intermediate status, parallelize lookups, and cache static reference data (rooms, capabilities, block templates), but never cache live slot availability past its freshness window.

### Gaps
- No published empirical data were found on double-booking or race-condition rates in OR scheduling systems.
- No recent (2025-2026) benchmark of LLM CPT accuracy with tool/RAG grounding was retrieved. The 2024 NEJM AI study tested ungrounded generation.

---

## Q13. Hard vs. soft constraint classification

### Takeaway
Hard constraints are those whose violation causes a physical impossibility (double-booked room, surgeon, or equipment), a patient-safety/regulatory breach (wrong patient, site, or laterality; unprivileged surgeon; no circulator or anesthesia), or an unauthorized action (booking into someone's unreleased block, PHI exposure). Soft constraints are optimization targets and local preferences (utilization, prime time, sequencing preferences, PACU smoothing). Several items are **hard at day of surgery but soft at booking time**, such as H&P, consent, prior auth, and loaner trays.

### Cited Findings
- Dexter's ordered priorities put patient safety first, then over-utilized time, then waiting, then preferences. That ordering maps directly onto hard (safety) versus soft (efficiency, preference) — [Dexter et al., Anesthesiology 2007](https://user.engineering.uiowa.edu/~csl/publications/pdf/2007%20Dexter%20Anethesiologist%20Decisionmaking%20Anesthesia.pdf)
- Regulatory hard requirements: privileges roster, RN supervision and circulating, H&P timing, consent before surgery, OR register — [42 CFR 482.51](https://www.law.cornell.edu/cfr/text/42/482.51); verification of procedure, site, and laterality starting at scheduling — [Floyd Health UP policy](https://www.floyd.org/Documents%20Medical%20Staff/PCS-03-003%20Wrong%20Site%20Surgery.pdf); concurrent critical portions inappropriate — [ACS via AAHKS](https://www.aahks.org/acs-updates-statement-on-concurrent-surgeries/); max 4 medically directed concurrent anesthesia cases — [Coronis TEFRA guide](https://www.coronishealth.com/archive-guidelines-anesthesiologist-hcfa-final-rule-tefra-1198/)
- Policy-level (local, enforceable but adjustable) items: block release windows, 75% utilization thresholds — [UToledo](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf), [HonorHealth](https://www.honorhealth.com/sites/default/files/2023-03/surgery-block-scheduling-policy.pdf), [St. Charles](https://WWW.STCHARLESHEALTHCARE.ORG/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgicalProceduralBlockManagementRedmond-Policy9579.pdf); 48-hour loaner delivery — [UTMB](https://www.utmb.edu/policies_and_procedures/20038472)

### Inferences
Proposed classification for the prototype (my synthesis):

| Constraint | Class | Assistant behavior |
|---|---|---|
| Room double-booking (case + turnover overlap) | **Hard** | Never book; offer alternates |
| Surgeon in two rooms with overlapping booked time (no approved flip-room pattern) | **Hard** | Block; escalate if flip-room requested |
| Shared equipment (robot, C-arm, microscope, hybrid imaging) over-allocated | **Hard** | Block; offer alternate times/rooms |
| Room lacks required capability (robot, fluoro, laminar flow, cysto) | **Hard** | Filter out room |
| Surgeon not privileged for procedure | **Hard** | Block; escalate to medical staff office |
| Patient identity ambiguous / not confirmed by 2 identifiers | **Hard** | Ask; never guess |
| Laterality / spinal level missing or conflicting with order | **Hard** | Ask or escalate; spell out in full |
| Procedure or CPT not resolved from master or order | **Hard** | Lookup only; no generation |
| Booking into another owner's unreleased block | **Hard (policy)** | Offer "request release" escalation |
| Write without explicit human confirmation | **Hard (product)** | Always show structured confirmation |
| PHI to non-BAA service / unaudited write | **Hard (compliance)** | Architectural |
| Anesthesia coverage > configured ratio (≤1:4 medical direction) | **Hard (escalate)** | Flag; route to anesthesia scheduler |
| No RN circulator / required specialty team for date | **Hard (escalate)** | Mark pending staffing; route to charge RN |
| Loaner/implant set < 48 h (or < 3 business days if first-time) | **Hard-at-DOS / soft-at-booking** | Book with risk flag + SPD/vendor task, or escalate |
| H&P > 30 days old at DOS, consent missing | **Hard-at-DOS / soft-at-booking** | Book + readiness task |
| Prior auth not approved | **Hard-at-DOS (financial) / soft-at-booking** | Book + flag window vs 72h/7-day payer clocks |
| Post-op ICU/inpatient bed availability | **Soft → escalate** | Flag; route to bed management |
| Runs past staffed hours / prime time (overtime) | **Soft → escalate** | State projected overrun; needs approval |
| Latex-first, contaminated-last, pediatric/diabetic-early | **Soft (policy preference)** | Prefer; surface conflicts |
| Block utilization ≥ 75%, fill own block first | **Soft (metric)** | Prefer owner's block; show utilization |
| PACU peak smoothing, day-of-week leveling | **Soft (optimization)** | Optional ranking factor |
| Surgeon/patient preferred date or time | **Soft (preference)** | Rank alternates |
| Bumping elective for add-on/emergent | **Not the assistant's decision** | Always escalate to OR charge / anesthesia |

### Gaps
- The classification is a synthesis, not a published standard. Individual hospitals may treat some soft items as hard (e.g., some forbid booking without prior auth, or require consent before booking).
- Thresholds (ratios, release windows, staffed hours) vary by site and should be configuration, not constants.
