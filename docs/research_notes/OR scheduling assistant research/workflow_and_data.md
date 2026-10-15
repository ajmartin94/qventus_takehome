# OR Case Scheduling Workflow, Booking Data, and System Integrations (US hospitals)

Research date: 2026-10-14. Primary anchors: the University of Toledo Medical Center (UTMC) Surgical Services policy, effective 5/2026 (full text read); the HonorHealth (Jan 2025), Emory WRP (May 2026), and Saint Alphonsus booking request forms (full text read); the Epic OR Capacity page; the HL7 FHIR R4 spec; Oracle Millennium API docs. Some items come only from search-result summaries. Those are marked "(snippet)" and are weaker evidence.

---

## 1. What are the step-by-step stages of booking an elective case, and who performs each step?

### Takeaway
An elective case moves through these stages: the surgeon decides; the surgeon's office scheduler submits a case request (Epic Case Request, a portal, or a faxed form during downtime); the central surgery scheduling office validates it, assigns a length, and places it into the surgeon's block or open time; insurance authorization and financial clearance follow; then pre-admission testing and chart completion; the schedule closes the day before (often 2:00 PM) with case order confirmed to the office; and the OR desk and anesthesia-in-charge manage the day of surgery. Add-ons and urgent cases go around the scheduling office to the anesthesia-in-charge and OR desk.

### Cited Findings
**Stage 1: Surgeon office creates the case request**
- HonorHealth's form says: "This is not a Preoperative order. This is only a case booking request." Bold fields are required "to avoid scheduling delays." The form records Scheduler Name and Contact Number, which identify the office scheduler as the requester. It is labeled a "Downtime Form", so electronic entry is the normal route (revised Jan 2025). — [HonorHealth Surgery Scheduling Request Form](https://www.honorhealth.com/sites/default/files/2025-10/surgery-scheduling-fax-request-form.pdf)
- Saint Alphonsus: "Scheduling of procedure cannot be initiated without this basic information." It captures "Office Scheduler Name / Ph / Fax" and asks for a demographics form and an insurance referral form (PCP-to-specialist) where required. — [Saint Alphonsus Booking Request Form](https://saintalphonsus.org/sites/default/files/hg_features/mercury_standard_layout/9939b69fdb35876f43bc892c7805e777.pdf)
- Emory WRP (May 2026): "MANDATORY - All Highlighted areas. If not complete, case will not be scheduled." For multi-surgeon cases, each surgeon must complete a form and the forms must be sent together. Otherwise "it will look like two different cases and be posted as two different cases," and there may not be enough time left on the schedule for the second procedure. — [Emory WRP OR Scheduling Form](https://www.emoryhealthcare.org/-/media/Project/EH/Emory/ui/pdfs/south/wrp-or-scheduling-form-05-2026.pdf)
- Epic's "Case Request" is the module for electronic OR time requests (Salem Health) (snippet). — [Salem Health](https://salemhealth.org/common-ground-home/common-ground-post/inpatient-case-request-went-live-in-epic-oct-21)
- At Catholic Health (Buffalo, 2020), outside surgeons either enter the Case Request and PreOp orders in Epic themselves or have office staff do it. Staff entries require the surgeon's co-signature. Surgeons doing more than 10 cases a year had to use Epic (snippet). — [Catholic Health Epic and Surgical Scheduling](https://medstaff.chsbuffalo.org/wp-content/uploads/2020/03/Epic-and-Surgical-Scheduling-3.26.2020-003.pdf)
- EpicCare Link lets independent surgeon offices "view, request, and manage OR time." The OR Marketplace lets "surgeons and staff browse and request OR time as it becomes available." A Community Health Network quote says offices "no longer need to call surgery schedulers" to check availability. — [Epic OR Capacity](https://www.epic.com/software/or-capacity/)

**Stage 2: Central surgery scheduling office validates and places the case** (UTMC policy, 5/2026)
- The Surgery Scheduling Office is open Mon–Fri 0700–1630, excluding holidays. — [UTMC Policy 3364-100-53-27](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Only credentialed surgeons may schedule. Privileges are verified when a surgeon new to the department first schedules, or when "a surgeon attempts to schedule a case outside of his credentialed surgical specialty." If the surgeon is not privileged, the primary surgeon must find a privileged surgeon or the case is cancelled. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Case time is assigned at scheduling "based on historical case time specific to the assigned surgeon." Extensions are allowed for difficulty but "need approval by AIC" (anesthesia in charge). — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Block surgeons schedule through "a standardized scheduling form." "All scheduling transactions including cancellations, rescheduling, and equipment or supply requests must be uploaded into Athena." Intraoperative documentation is in Epic. Scheduling and documentation can therefore live in different systems. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Saint Alphonsus has a "Confirmation (completed by surgery scheduler)" block with Date, Time, Case #, and Scheduled By. The case number is issued at confirmation. — [Saint Alphonsus form](https://saintalphonsus.org/sites/default/files/hg_features/mercury_standard_layout/9939b69fdb35876f43bc892c7805e777.pdf)

**Stage 3: Authorization and financial clearance**
- HonorHealth: "If you are making changes to the Location, Patient Class or CPT code please contact the patient's insurance company and update the authorization." Authorization Status options are N/A, Pending, and Authorized (Number). The form collects primary and secondary insurance, Group/ID/Claim #, and Date of Injury. — [HonorHealth form](https://www.honorhealth.com/sites/default/files/2025-10/surgery-scheduling-fax-request-form.pdf)
- UTMC: "Financial clearance for elective procedures must be obtained by 12:00 PM the day prior to surgery or the case may be deferred." — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)

**Stage 4: Pre-admission testing (PAT) and chart readiness**
- UTMC: the pre-op health evaluation is done 3–30 business days before surgery. Test results are valid up to 30 days. The H&P must be within 30 days and updated on the day of surgery. All chart documentation is due to the pre-admission office 72 hours before elective cases. Cases "may be removed from the schedule or postponed" if incomplete. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- UTMC: non-facility vendor equipment and implants must be in Sterile Processing at least 48 hours before the scheduled start "or the procedure may be subject to cancellation." The attending surgeon coordinates vendor resources. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Saint Alphonsus Pre-Surgical Screening (PSS) options are a phone call (usually 2–3 days before), an on-site PSS visit (within 7 days, includes diagnostic orders), or an NP visit (Boise only). The surgeon's office tells the patient about the PSS appointment. — [Saint Alphonsus form](https://saintalphonsus.org/sites/default/files/hg_features/mercury_standard_layout/9939b69fdb35876f43bc892c7805e777.pdf)
- Some Epic sites require pre-op orders with the case request. One tip sheet warns that a missing pre-op order "may result in case delays and case cancellations" (snippet). — [Catholic Health](https://medstaff.chsbuffalo.org/wp-content/uploads/2020/03/Epic-and-Surgical-Scheduling-3.26.2020-003.pdf)

**Stage 5: Day-before close and confirmation**
- UTMC: the schedule closes at 2:00 PM the day before surgery, and later additions are add-ons. "Surgery Scheduling will confirm case order and expected surgery start time with the surgeon and/or office day prior to surgery." Start times after the first case "are estimates only." — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- UTMC: offices "may not fax notice of next day add-on cases, cancellations, or other changes." These must be phoned in, followed by an updated form. "All cancellations must be accompanied by a reason." — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)

**Stage 6: Day of surgery (OR desk, AIC, OR supervisor)**
- UTMC: day-of-surgery cases are scheduled "through Anesthesia in charge and OR desk lead." The OR Director/Manager runs the daily schedule and notifies surgeons of delays. A "Bumped Case" is moved because of an emergency. Cancellation requires agreement between surgeon and anesthesiologist. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)

### Inferences
- Roles for the prototype:
  - **Office scheduler (requester):** creates and changes requests and owns authorization.
  - **Central OR scheduling coordinator:** validates, places the case, assigns length, and issues the Case #.
  - **Anesthesia-in-charge / board runner plus OR desk lead or charge nurse:** approve add-ons, extensions, and day-of changes.
  - **PAT nurses:** own readiness.
  - **SSEC / OR committee:** owns block allocation.

  The take-home's "surgical scheduling coordinator" maps best to the central OR scheduling coordinator, possibly acting for offices.
- A booking is not a single atomic event. A case can be "scheduled" with readiness items still open (authorization pending, PAT not done, implants not delivered, H&P outdated), and those items can later cause deferral or removal. A credible assistant should return a booked case together with its outstanding readiness checklist.
- Time-based cutoffs change the workflow path. Before the 2:00 PM day-before close, the case is a normal booking. After it, the case is an add-on that needs AIC approval. Same-day urgent cases skip scheduling entirely.

### Gaps
- No public Epic OpTime tip sheet was found that shows the exact Case Request → scheduler work queue → "Scheduled" status transitions. Epic's internal status names (e.g., "Requested", "Pending", "Scheduled") were not confirmed from a primary source.
- No source gave standard lead times by case type (e.g., "book at least N days ahead"). UTMC defines elective cases only as "usually scheduled greater 72 hours in advance."

---

## 2. What fields are on a typical surgical case request / booking (posting) sheet?

### Takeaway
Four real US forms (2025–2026) share a core set of fields:
- Patient identity and contact details
- Location/site
- Surgeon(s)
- Requested date/time
- Case length
- Patient class/admission type
- Diagnosis (ICD-10)
- Procedure (CPT plus "permit"/consent wording) with laterality per line
- Anesthesia type
- Special needs (instruments, equipment, implants, vendor)
- Insurance and authorization status

Many forms add C-arm, bed type, frozen section, MRSA/latex/interpreter flags, PAT type, and an acuity or delay-risk field. Blood products and positioning are usually free text or missing.

### Cited Findings
**HonorHealth Surgery Scheduling Request Form (rev. Jan 2025)** — [source](https://www.honorhealth.com/sites/default/files/2025-10/surgery-scheduling-fax-request-form.pdf)
- New Case / Existing Case; Today's Date; Scheduler Name; Contact Number.
- Patient: First, MI, Last, Address, DOB, SSN (if available), Sex, Home/Cell phone, Email.
- Location (choose one): campus × room type, e.g., "SHEA IP OR", "OSBORN CATH", "TEMPE ENDO", "FOUR PEAKS OR", "JCL OP".
- Primary Surgeon; Assist; Second Surgeon; Date of Service; Start Time; Procedure Length.
- Admission Type: Outpatient / Pre-Inpatient / Short Stay Admit (23 Hour Observation) / Inpatient (Currently Admitted). Also Length of Stay (days) and Preoperative Medical Evaluation Y/N.
- Diagnosis; ICD-10 code(s); CPT code(s); Procedure (Permit to Read), which is the consent wording.
- Anesthesia Type: General / Local / MAC / Spinal / Conscious / Block / None / Other. Anesthesia Provider (named groups, N/A, Other).
- Special Needs Inst/Equip/Implants/Vendor (free text).
- Primary and secondary insurance, Group#/ID#/Claim#, Date of Injury, Authorization Status (N/A / Pending / Authorized (Number)).

**Saint Alphonsus Surgery Scheduling Booking Request Form** — [source](https://saintalphonsus.org/sites/default/files/hg_features/mercury_standard_layout/9939b69fdb35876f43bc892c7805e777.pdf)
- Location: Boise / Nampa / Ontario × Main, Day Surgery, CVOR, Surgery Center, Endoscopy.
- Patient: Name, DOB (mm-dd-yyyy), Gender, MRSA Hx (Yes/No/Active), Latex Allergy (Y/N), Interpreter (Y/N + language).
- Patient Type (must check one): Outpatient / Outpatient with 23 hour observation / Inpatient (to be admitted).
- Surgery Date/Time Request and preferred dates/times; PSS type.
- Primary Surgeon, Assistant, 2nd Surgeon, Scrub request.
- ICD-10, Procedure, CPT code(s), Modifier, Left/Right/Bilateral.
- "Estimated Duration (min) (skin to skin)".
- Anesthesia: General / MAC / Spinal / Epidural / Block / Choice.
- Special Requests: Wound Vac / Mesh / Other; Specialty Trays/Implants; "Custom order/Special order implants: Vendor notified / OR notified / N/A".
- ICU bed anticipated Y/N; Frozen Section Y/N; COVID testing.
- Scheduler confirmation: Date, Time, Case #, Scheduled By.

**Emory WRP OR Surgery Scheduling Request (May 2026)** — [source](https://www.emoryhealthcare.org/-/media/Project/EH/Emory/ui/pdfs/south/wrp-or-scheduling-form-05-2026.pdf)
- Patient name "must match that on their license/passport"; DOB; gender; address; phones.
- Date of Service, Time, Surgeon, Outpatient / Inpatient / Surgical Admit.
- Additional Surgeon (different specialty); Assisting Surgeon (same specialty).
- ICD-10; repeating CPT rows (primary, secondary…), each with description and Laterality Left/Right/Bil/N/A.
- Expected Surgery Length; Fluoro/C-Arm Needed Y/N.
- Free text: "Positioning / Request for Instruments and Equipment / Anesthesia Type / Acuity (Time-Based)".
- Hospital bed: ICU / Non-ICU / No bed.
- "Effect of Short-Term Delay on Outcome": Minimum / Moderate / High Risk to Patient.
- In-person PAT needed + date/time; Desired Date/Time; Billing type (Partially/Fully Cosmetic/Other); Physician signature.
- Multi-surgeon Y/N and "Total Length of the Case for All Surgeons Times Combined."

**Other forms (snippets)**
- Children's Minnesota asks for CPT and ICD-10 and whether vendor reps are needed, with vendor information. — [Children's MN surgery request form](https://www.childrensmn.org/references/MR/or/opreport/surgery-request-form.pdf)
- St. Francis Medical Center has a booking form with a separate special-equipment section listing implants and vendor. — [St. Francis booking form](https://WWW.STFRANCISMEDICALCENTER.COM/wp-content/uploads/2022/08/02-Fillable-Booking-Form-and-Special-Equip_Surgery-Services-06.22.22.pdf)

**Epic case length field**
- Salem Health's scheduling sheet and Epic Case Request ask: "Use Surgeon's average time? Yes/No If no, length requested?" — [Salem Health, 2021](https://salemhealth.org/common-ground-home/common-ground-post/accurate-case-scheduling)

**Downstream items the booking feeds (UTMC time-out checklist)**
- Consent, site marking, case duration, anticipated blood loss, imaging displayed, "Equipment/devices/implants in the OR", and ABO/crossmatch for transplants. These are captured or verified later, not necessarily at booking. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)

### Inferences
**Proposed slot schema for the prototype** (synthesized from the forms above, not a standard).

Required to check availability:
- surgeon
- procedure (name or CPT)
- estimated duration (or "use surgeon average")
- location/site (or "any")
- date or date range (or time-of-day preference)
- patient class

Required to book:
- patient identifiers (name + DOB or MRN)
- procedure lines (CPT + description + laterality + modifier)
- diagnosis (ICD-10)
- anesthesia type
- admission type / patient class
- requested date and start time
- room/site
- duration (estimate in minutes, with source: surgeon estimate vs historical)

Conditional or optional:
- assistant/co-surgeon (and multi-surgeon total length)
- C-arm/fluoro, robot
- special trays, implants + vendor + vendor-notified flag
- positioning
- bed (ICU/non-ICU/none) and frozen section
- blood products / type & screen
- isolation (MRSA Hx), latex allergy, interpreter/language
- PAT type
- authorization status + number
- acuity / delay-risk
- notes

- Laterality must be per procedure line, not per case (Emory, Saint Alphonsus). Multi-procedure cases need a repeating structure.
- "Duration" is ambiguous across forms: "Procedure Length" (HonorHealth), "skin to skin" (Saint Alphonsus), and "Expected Surgery Length" (Emory). The assistant should state which definition it uses (in-room vs incision-to-close) and add setup/turnover.
- Changing location, patient class, or CPT has insurance consequences (re-authorization), so the assistant should flag these on modify.

### Gaps
- No public form fetched had a structured blood-products field (type & screen, crossmatch units). Blood appears only in the UTMC time-out ("anticipated blood loss", ABO/crossmatch for transplant).
- No form had a structured positioning picklist (supine/prone/lateral/lithotomy/beach chair). Emory uses free text.
- Consent status is not a booking-form field. HonorHealth captures only the "Permit to Read" wording, and UTMC requires a signed consent before the procedure.

---

## 3. How do block scheduling, block release, open time, add-ons, and urgent/emergent classes work?

### Takeaway
Most prime-time OR hours (about 80%) are allocated as blocks to surgeons, groups, or services, with about 20% held as first-come-first-served open time. Unused block time auto-releases to open time at a fixed horizon. Published horizons range from 24 hours to 21 days, and 5 business days or 7 calendar days are common. Release may be tiered by specialty or utilization. Blocks are kept or lost on about 75% utilization. Add-ons after the day-before cutoff need anesthesia approval, and urgent/emergent cases follow hospital-defined classes with start-time targets from 15 minutes to 24 hours.

### Cited Findings
**Block, open, and release definitions (UTMC 5/2026)** — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Block Time is "Surgical time reserved for a designated surgeon, group, or service within a defined cut-off period... only the designated surgeon, group or service may schedule."
- Open Time is "available... on a first-come, first-serve basis. A goal is to keep 20% of total OR minutes available as Open Time." Total block assignments "will not exceed 80% of prime block hours (07:30–1500)."
- Block shapes: 2.5h or 4.5h half-days (07:30–12:00 or 12:30–15:00), 7.5h (07:30–15:00), and 9.5h (07:30–17:00).
- "Automatic Block cutoff applies at 7:00 AM 5 business days prior to scheduled surgery date." A release table in the same policy says "Unscheduled block time of release at 1500" on the prior same weekday. This is an internal inconsistency in the source.
- Surgeon self-release "must occur 14 days prior to scheduled block to prevent negative utilization time."
- Released time becomes open time, first-come-first-served. Block time "cannot be designated to another colleague (unless... group block)." A surgeon who releases time and then wants it back competes first-come-first-served.
- Designated block time should be used before booking open time, and "Cases scheduled in open time will not count toward a surgeon's monthly utilization."
- Block holders may schedule "up to 100% of the approved hours of block time." Gaps between cases may not exceed 90 minutes.
- Block Utilization = block minutes used ÷ block minutes available, including turnover. The goal is ≥75%:
  - 65–74% = potential concern
  - 36–64% = warning (two consecutive months leads to reduction)
  - ≤35% for two quarters = automatic adjustment
  - Two-room block holders need 65%
- Flip room eligibility requires ≥75% utilization, more than 250 cases a year or 5 cases per 8-hour block, and an average case of 60–90 minutes.
- Concurrent surgery is not supported. Overlapping surgery requires a designated back-up surgeon and patient consent.

**Release horizons at other hospitals**
- St. Charles (OR): unused blocks auto-release 7 calendar days before (14 days for robotics). Manual release is allowed ≥30 calendar days out, capped at 5 manual releases per block per rolling 6 months (snippet). — [St. Charles Redmond Policy 9579 (2024)](https://WWW.STCHARLESHEALTHCARE.ORG/sites/default/files/Documents/Surgery%20Scheduling/2024/SurgicalProceduralBlockManagementRedmond-Policy9579.pdf)
- At St. Charles Bend, auto-release does not apply to add-on rooms for designated trauma or heart blocks (snippet). — [St. Charles Bend Policy 3653](https://stcharleshealthcare.org/sites/default/files/Documents/Surgery%20Scheduling/SurgicalProceduralBlockManagementBend-Policy3653.pdf)
- Hendrick Medical Center (2020, reviewed 2023): the release horizon is tiered by utilization, e.g., 5 working days at >80% and 24-hour release at 90%. Blocks below 50% can be reduced (snippet). — [Hendrick Block Scheduling 4.6651](https://www.hendrickhealth.org/documents/medical%20staff%20services/Block-Scheduling-4.6651.pdf)
- HonorHealth (2022): 80% block / 20% open target and 75% required utilization. Release times are set per specialty by committee, ranging from 0 to 5 working days, with orthopedic trauma released at 7 a.m. on the day of surgery (snippet). — [HonorHealth Block Policy](https://www.honorhealth.com/sites/default/files/2023-03/surgery-block-scheduling-policy.pdf)
- Loma Linda moved auto-release to 21 days at its all-elective outlying sites after reviewing data with nine surgical chairs (snippet). — [Becker's](https://www.beckershospitalreview.com/or/3-health-system-leaders-on-why-block-utilization-doesnt-tell-the-full-story-and-what-grew-surgical-volume-7/)
- OR Manager (July 2010): some facilities use a standard 5-day release, and no release time is suggested when block utilization consistently exceeds 85% (snippet). — [OR Manager](https://www.ormanager.com/wp-content/uploads/pdfx/ORMVol26No7BlockSchedulingPolicies.pdf)
- A vendor/consultant source recommends releasing unused block at least 48 hours ahead, with 72 hours ideal. This is advice, not a hospital policy (snippet). — [HST Pathways](https://www.hstpathways.com/blog/10-tips-to-improve-or-utilization-through-block-time/)
- A 2014 simulation found that block release gives only a minor benefit for services already at or above 80% utilization (snippet). — [Weiss & Taaffe, WSC 2014](https://informs-sim.org/wsc14papers/includes/files/103.pdf)
- Epic supports self-service release ("directly release OR time if a surgeon doesn't plan to use it"), AI "Predictive Block Reminders" sent to office staff weeks ahead, monthly block-owner notifications, and suggested block allocations. Epic reports OR Marketplace averages of "3 more cases per OR per month", "60% more OR time freed up", and "5.5 additional days of lead time" (vendor-reported). — [Epic OR Capacity](https://www.epic.com/software/or-capacity/)

**Add-ons (UTMC)** — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Add-on cases are "scheduled after schedule closes at 2:00 PM previous day" and need approval from the AIC/board runner with the OR supervisor.
- "First Available Room (FAR)" cases before the day of surgery go through the scheduling office until 2:00 PM the day before. Day-of cases go through the AIC and OR desk lead.

**Urgent/emergent classes**
- UTMC (5/2026): "Elective Case... usually scheduled greater 72 hours in advance." — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- UTMC urgent and emergent classes:
  - Class X (Emergent): OR staffed and accepting the patient within 15 minutes
  - Class 1A: within 1 hour
  - Class 1B: within 2–3 hours
  - Class 1C: within 6 hours
  - Long Bone Fracture: within 24 hours

  The surgeon documents the class and communicates it to the AIC, and the class can be reclassified. The on-call team response is 30 minutes. Elective surgery is not scheduled on holidays. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- OR Manager (2010) gives other examples. A Michigan hospital uses Class A (life/limb/sight, within 1 hour), Class B (within 4 hours), and Class C (non-life-threatening). Another hospital uses 30–60 minutes, under 2 hours, and under 24 hours (snippet). — [OR Manager Managing Urgent Cases](https://www.ormanager.com/wp-content/uploads/pdfx/ORMVol26No7ManagingUrgentCases.pdf)
- NCEPOD (UK) "Urgent" cases are "generally performed within hours of decision to operate" (snippet). — [NCEPOD Classification](https://ncepod.org.uk/classification.html)

### Inferences
- For "check availability", the assistant needs to know a time window's ownership state, not just whether it is free:
  - (a) inside the requesting surgeon's own block
  - (b) another owner's block, not yet released (unavailable, but shows the release date/time)
  - (c) released block (now open)
  - (d) open/unblocked time (first-come-first-served)
  - (e) closed or holiday

  Also needed: the release rule for the window (e.g., "auto-releases at 07:00 on 2026-10-21, 5 business days prior") and whether the date is past the add-on cutoff.
- A strong alternate path: the requested date falls in another surgeon's unreleased block. The assistant offers (1) the surgeon's own next block day, (2) open time on other dates, (3) a waitlist or notification when the block releases (Epic's OR Marketplace notifications).
- Urgent/emergent requests are a separate path, not a normal booking. The assistant should detect acuity and route to the AIC/OR desk with a class (e.g., X/1A/1B/1C) rather than "book" into elective time.
- Booking into open time doesn't count toward block utilization at UTMC, so a coordinator would prefer the surgeon's block when one fits. That is a useful ranking rule.

### Gaps
- I found no American College of Surgeons (ACS) standard for emergency case classes. The "ACS emergency classification" in the brief could not be verified. Classes appear to be hospital-defined (UTMC, OR Manager examples) or come from non-US frameworks (NCEPOD, WSES TACS).
- No primary source confirmed a "72-hour auto-release" policy at a named US hospital. 72 hours appears in consultant/vendor advice and as UTMC's definition of an elective case.

---

## 4. How is case duration estimated, and how are turnover times factored in?

### Takeaway
At booking, the EHR's surgeon-specific historical average for the procedure is the default (Epic: "last ten similar cases" at Salem Health). The surgeon can override it for complex cases, which may need approval. EHR estimates beat surgeon guesses in published comparisons, and Epic now shows a predicted length with a confidence score. Turnover (about 20–30 minutes) is a separate allowance between cases and is counted in utilization metrics.

### Cited Findings
- UTMC: case time is assigned "based on historical case time specific to the assigned surgeon." It can be extended "depending on the degree of difficulty... (needs approval by AIC)." — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Salem Health (2021): schedulers use the surgeon's average time, "which Epic calculates from the surgeon's last ten similar cases." Surgeons answer "Use Surgeon's average time? Yes/No If no, length requested?" for complex cases. — [Salem Health](https://salemhealth.org/common-ground-home/common-ground-post/accurate-case-scheduling)
- Epic Case Length Estimation shows expected procedure lengths "with a confidence score" so staff can decide whether to adjust, and built-in analytics track estimate accuracy. — [Epic OR Capacity](https://www.epic.com/software/or-capacity/)
- WVU orthopedics (326 cases, level 1 trauma center): counting a prediction as correct within 30% of actual, Epic-generated predictions were correct 77.9% of the time and surgeon predictions 48.2%. Surgeons underestimated more, and multi-procedure cases had larger discrepancies. This is a poster-style document (snippet). — [WVU poster](https://health.wvu.edu/media/18934/42-vincent-melemai-21925.pdf)
- JACS (2019) machine learning: surgeon-specific models improved accuracy (within 10%) from 30% (surgeon estimate) to 39% (snippet). — [HospiMedica summary](https://mobile.hospimedica.com/surgical-techniques/articles/294778842/machine-learning-approach-predicts-surgery-duration.html)
- A preprint using 170,748 cases treated EMR historical averages by surgeon or procedure as the baseline and linked low accuracy to rescheduling and cancellations (snippet). — [medRxiv 2020](https://www.medrxiv.org/content/10.1101/2020.06.10.20127910v2.full-text)
- Dexter et al. (Can J Anesth 2005, 58,291 cases) recommend monitoring each service's bias in scheduled durations. For services that consistently underestimate, they suggest statistical estimates instead of the surgeon's (snippet). — [Univ. of Iowa record](https://iro.uiowa.edu/esploro/outputs/journalArticle/Validity-and-usefulness-of-a-method/9983806247602771)
- Turnover (UTMC) is "The time from when one patient leaves the operating room until the next patient arrives... when a surgeon is available and scheduled to follow immediately." Targets are 30 minutes for the main OR and 20 minutes for the surgery center, on 85% of cases. On-time first-case start target is 85%. OR utilization includes turnover: (elective hours in block including prep, induction, and emergence + turnover) ÷ available hours. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Forms define duration differently: "Procedure Length" (HonorHealth), "Estimated Duration (min) (skin to skin)" (Saint Alphonsus), and "Expected Surgery Length" plus a multi-surgeon combined total (Emory). — [HonorHealth](https://www.honorhealth.com/sites/default/files/2025-10/surgery-scheduling-fax-request-form.pdf); [Saint Alphonsus](https://saintalphonsus.org/sites/default/files/hg_features/mercury_standard_layout/9939b69fdb35876f43bc892c7805e777.pdf); [Emory](https://www.emoryhealthcare.org/-/media/Project/EH/Emory/ui/pdfs/south/wrp-or-scheduling-form-05-2026.pdf)
- A review found that combined interventions can cut average turnover by about 7 minutes per case, with small efficiency gains compared with allocating OR time and scheduling cases well (snippet). — [Univ. of Iowa (Dexter) record](https://iro.uiowa.edu/esploro/outputs/journalArticle/Operating-room-efficiency-and-scheduling/9983806265302771)

### Inferences
- The assistant should show the duration and its provenance, e.g.: "Booked 135 min = Dr. X's median of last 10 lap choles (105 min in-room) + 30 min turnover. Surgeon estimate was 90 min." It should also let the coordinator override, flagging that extensions may need AIC approval.
- When checking fit, required contiguous time = estimated in-room duration + turnover. The block must have that much contiguous time without creating a gap over 90 minutes (UTMC rule).
- For multi-procedure or multi-surgeon cases, sum the lines and warn about lower estimate accuracy.

### Gaps
- No primary documentation was found on how Epic OpTime configures setup and cleanup minutes on top of procedure length. Whether the "case length" field includes turnover varies by site build.
- The Epic default sample size ("last 10 similar cases") comes from one hospital's 2021 article and may be site-configurable.

---

## 5. What systems hold the data, and how do integrations work (Epic OpTime/Cadence, Oracle Health, Meditech, HL7 v2 SIU, FHIR, Epic APIs)?

### Takeaway
The surgical case of record lives in the EHR's perioperative module (Epic OpTime; Oracle Health SurgiNet; Meditech's surgical module). Outbound integration is mainly HL7 v2 SIU messages (S12 new booking, S13 reschedule, S14 modify, S15 cancel, S26 no-show, plus resource and slot events). Over FHIR R4, Epic exposes scheduled surgeries as read and search only ("Appointment.Read/Search (Scheduled Surgeries)", "Procedure.Read/Search (Surgeries)"). Epic's FHIR booking services are described as prototypes, and most real scheduling writes go through proprietary interfaces. A prototype should therefore mock a scheduling service and not assume FHIR write access to OR cases.

### Cited Findings
**EHR modules**
- Epic OR Capacity tools include OR Marketplace, self-service block release, Predictive Block Reminders, EpicCare Link for independent surgeons, Case Length Estimation with a confidence score, Advanced Block Analytics (utilization, "unused gap time", suggested allocations), and OR Staffing Analysis. — [Epic OR Capacity](https://www.epic.com/software/or-capacity/)
- Epic's "Case Request" is the module for electronic OR time requests (snippet). — [Salem Health](https://salemhealth.org/common-ground-home/common-ground-post/inpatient-case-request-went-live-in-epic-oct-21)
- UTMC enters scheduling transactions into "Athena" and documents intraop delays in Epic. Some hospitals split scheduling and periop documentation across vendors. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)

**HL7 v2 SIU**
- There are 14 SIU trigger events, all sharing one structure:
  - S12 new appointment booking
  - S13 rescheduling
  - S14 modification
  - S15 cancellation
  - S16 discontinuation
  - S17 deletion
  - S18 addition of service/resource
  - S19 modification of service/resource
  - S20 cancellation of service/resource
  - S21 discontinuation of service/resource
  - S22 deletion of service/resource
  - S23 "blocked schedule time slot(s)"
  - S24 "opened ('un-blocked') schedule time slot(s)"
  - S26 patient did not show

  — [Rhapsody](https://rhapsody.health/resources/hl7-siu-message/)
- SIU structure: MSH, SCH (schedule activity, required), NTE, and a Patient group (PID, PV1, PV2, OBX, DG1). It also has repeating Resource groups led by RGS, containing AIS (service, e.g., the procedure), AIG (general resource, e.g., equipment), AIL (location resource, e.g., OR room), and AIP (personnel, e.g., surgeon or anesthesiologist), each with NTE. — [Rhapsody](https://rhapsody.health/resources/hl7-siu-message/)
- Receivers often take only a subset. Kyruus consumes S12/S13/S14/S15/S26, does not support SIU for check-in or room transfer, and asks senders to filter by provider population (snippet). — [Kyruus Academy](https://academy.kyruus.com/technical-kickoff-series/1792849)

**FHIR R4 Scheduling module**
- Appointment.status values: proposed, pending, booked, arrived, fulfilled, cancelled, noshow, entered-in-error, checked-in, waitlist. Only proposed or cancelled appointments may lack start/end.
- Appointment workflow: discover the Schedule, optionally check Slots ("a slot being available doesn't guarantee booking"), create the Appointment as "proposed" with participants at "needs-action", then participants reply with AppointmentResponse and the overall status is updated.
- Appointment elements: basedOn → ServiceRequest; slot; participant actors (Patient, Practitioner, PractitionerRole, Device, HealthcareService, Location, RelatedPerson) with status accepted, declined, tentative, or needs-action; serviceType; appointmentType; reasonCode; priority (0–9); minutesDuration; requestedPeriod; supportingInformation.

  — [HL7 FHIR R4 Appointment](https://hl7.org/fhir/R4/appointment.html)
- Slot.status values: busy, free, busy-unavailable, busy-tentative, entered-in-error. A Slot has one Schedule plus start/end, serviceType, specialty, appointmentType, overbooked, and comment. Slots "do not provide any information about appointments." — [HL7 FHIR R4 Slot](https://hl7.org/fhir/R4/slot.html)

**Epic FHIR / API reality**
- open.epic Scheduling: "These prototype services demonstrate scheduling an appointment using FHIR." It covers "scheduled appointments and procedures" in general, with no OR/OpTime specifics, and also points to HL7 v2 and "Other" scheduling interfaces. — [open.epic Scheduling](https://open.epic.com/Scheduling/FHIR)
- Epic on FHIR app listings include "Appointment.Read (Scheduled Surgeries)", "Appointment.Search (Scheduled Surgeries)", "Procedure.Read (Surgeries)", "Procedure.Search (Surgeries)", "ServiceRequest.Read/Search (Order Procedure)", "Location.Read", "Practitioner.Read", "Coverage.Read/Search", "Flag.Read/Search" (Infection, Isolation), and "Consent.Read/Search (Document)". All surgery-related entries are read or search; no surgery create or update is listed. — [Vital Epic on FHIR app article](https://vital.io/help/en/articles/15863078-epic-on-fhir-application)
- A developer guide says "many Epic scheduling endpoints remain proprietary and older," so workflows mix FHIR and non-FHIR calls. Epic sometimes returns HTTP 200 OK with an error in the body, e.g., slot already taken (snippet). — [Mindbowser Epic Scheduling API guide](https://www.mindbowser.com/epic-scheduling-api-guide/)
- An Epic connector vendor lists the FHIR Appointment $book operation under STU3, not R4 (snippet). — [OutSystems Epic Connector](https://www.outsystems.com/forge/component-overview/16374/epic-connector)

**Oracle Health (Cerner) Millennium**
- POST /Appointment (R4): status must be proposed or booked. For booked, "Appointment.slot must be a list containing exactly one reference to the Slot," and the single participant must be the patient with status accepted. requestedPeriod.start and requestedPeriod.end are required (snippet). — [Oracle Millennium API: Create an appointment](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/op-appointment-post.html)
- Another variant requires a slot with status free and says participant.type must not be set (snippet). — [Oracle Millennium API variant](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfdap/op-appointment-post.html)
- A third-party guide says Oracle documents no hold operation, so treat a slot as reserved only after create succeeds, then read back the Appointment (snippet). — [Nirmitee](https://nirmitee.io/blog/fhir-scheduling-api-appointment-slot-epic-oracle-athenahealth/)

### Inferences
- A realistic prototype architecture: the chat assistant calls a mocked "OR Scheduling Service" with tools such as `search_or_availability`, `get_block_schedule`, `create_case_request`, `get_case`, `update_case`, `cancel_case`, and `release_block`. The mock represents what the EHR's proprietary periop scheduling API would do. Booking writes into a production Epic OR schedule would realistically go through a case request work queue or proprietary or vendor-partner interfaces, not public FHIR R4. A downstream SIU^S12 or S14 notifies other systems.
- FHIR mapping for the mock's data model:
  - Case → Appointment (+ Procedure for the performed surgery, ServiceRequest for the surgeon's order/request)
  - OR room → Location
  - Surgeon/anesthesia → Practitioner
  - C-arm/robot → Device
  - Block/open time → Schedule + Slot (status free / busy / busy-unavailable for another owner's block)
  - Booking state → Appointment.status (proposed → pending → booked; cancelled; waitlist)
- Failure modes worth modeling from the integration evidence:
  - race condition / slot taken (Epic 200-with-error; Oracle has no hold)
  - read-back confirmation after a write
  - write rejected because the surgeon isn't privileged or required fields are missing

### Gaps
- No primary Epic (fhir.epic.com) page was retrieved confirming the exact search parameters for "Appointment.Search (Scheduled Surgeries)", or whether any Epic write API exists for OpTime cases. The read-only conclusion rests on a third-party app's API list plus Epic's "prototype" language.
- No source found for Oracle SurgiNet-specific surgical case APIs, or for Meditech (Expanse) surgical scheduling interfaces.
- HL7 v2 SRM/SRR (placer-to-filler scheduling request/response, S01–S11) and SIU S25 were not verified in this session.
- Qventus's own integration patterns (e.g., how its OR products read block and schedule data from the EHR) were out of scope and not researched here.

---

## 6. What does a realistic "check availability" query return, and what does a realistic "book case" response include?

### Takeaway
No public source specifies these payloads. Realistic shapes can be assembled from the cited fields and policies. Availability results should be room/date windows with an ownership state (own block / other's block plus release time / released / open), contiguous free minutes, and constraints (cutoff, equipment). A booking result should include a case number, status (requested/pending vs scheduled/booked), scheduled room, start and duration with provenance, and an outstanding-readiness checklist and conflicts. Alternate and failure paths come straight from policy rules.

### Cited Findings
- Confirmation data a real scheduler returns: "Date, Time, Case #, Scheduled By." — [Saint Alphonsus form](https://saintalphonsus.org/sites/default/files/hg_features/mercury_standard_layout/9939b69fdb35876f43bc892c7805e777.pdf)
- Ownership and time-state concepts: block, surgeon-released block, automatically released block, open time (first-come-first-served), add-on after 2:00 PM day-before close, FAR, bumped case. — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Epic exposes availability to offices as browsable open OR time with notifications when time opens. — [Epic OR Capacity](https://www.epic.com/software/or-capacity/)
- Booking states in the standards: FHIR Appointment status (proposed, pending, booked, waitlist, cancelled…) and participant status (needs-action/accepted). — [FHIR R4 Appointment](https://hl7.org/fhir/R4/appointment.html). Oracle create accepts proposed or booked. — [Oracle Millennium API](https://docs.oracle.com/en/industries/health/millennium-platform-apis/mfrap/op-appointment-post.html)
- Conditions that block or defer a case:
  - missing mandatory fields: "case will not be scheduled" — [Emory](https://www.emoryhealthcare.org/-/media/Project/EH/Emory/ui/pdfs/south/wrp-or-scheduling-form-05-2026.pdf)
  - surgeon not privileged for the procedure
  - financial clearance not done by noon the day prior
  - PAT or chart incomplete 72 hours before
  - vendor implants not in SPD 48 hours before

  — [UTMC Policy](https://www.utoledo.edu/policies/utmc/administrative/pdfs/3364-100-53-27.pdf)
- Authorization status (N/A / Pending / Authorized #) is tracked on the request and must be updated if location, patient class, or CPT changes. — [HonorHealth form](https://www.honorhealth.com/sites/default/files/2025-10/surgery-scheduling-fax-request-form.pdf)

### Inferences
**Illustrative "check availability" result (synthesized):**
```
Request: Dr. Patel (Ortho), CPT 29881 knee arthroscopy L, est. 75 min (surgeon median of last 10 = 68 min in-room) + 30 min turnover = 105 min needed; Main OR; week of 2026-11-02
Results:
1. Tue 2026-11-03, OR 7, 07:30-15:00 | Block: Patel (own block) | booked 3 cases / 270 min | free contiguous: 12:45-15:00 (135 min) | fits | counts toward block utilization
2. Wed 2026-11-04, OR 3, 07:30-15:00 | Block: Ortho Sports group (not Patel) | auto-releases Wed 2026-10-28 07:00 (5 business days) | free 210 min | NOT bookable until release (offer waitlist/notify)
3. Thu 2026-11-05, OR 11 | Open time (FCFS) | free 07:30-10:30 (180 min) | fits | needs C-arm: 1 of 2 available
Notes: Mon 2026-11-02 after cutoff? No. Holiday? No.
```
Fields: date, site, room, time window, owner type (own_block/other_block/released/open/closed), owner name, release_at, scheduled minutes, free contiguous minutes, fits (bool), constraint flags (equipment, cutoff, room capability e.g. robot/fluoro-capable).

**Illustrative "book case" result (synthesized):**
```
Case #: SC-2026-104882 | Status: Scheduled (Booked) [or "Pending - awaiting scheduler review"]
Patient: J. Doe, DOB 1961-04-02, MRN 00012345 | Class: Outpatient
Procedure: 29881 Arthroscopy, knee, meniscectomy - LEFT | Dx: M23.222
Surgeon: Patel | Anesthesia: General + block | Room: Main OR 7 | 2026-11-03 12:45, 75 min + 30 turnover (est. source: surgeon historical median)
Equipment: arthroscopy tower; implants: none; vendor: none
Readiness: Auth PENDING (payer: Aetna) - due by 2026-11-02 12:00 for financial clearance; PAT phone screen not yet scheduled; H&P must be dated >= 2026-10-04
Conflicts: none | Notifications: surgeon office, PAT, SPD (SIU^S12 sent)
```

**Alternate and failure paths to prototype (each traceable to a cited rule):**
1. Requested date is in another owner's unreleased block. Show the release date/time and offer own-block dates, open time, or waitlist/notify on release.
2. Not enough contiguous minutes (duration + turnover). Offer a different room or day, or a shorter case only if the surgeon overrides the estimate (needs AIC approval).
3. Request is after the 2:00 PM day-before cutoff. Convert to an add-on request routed to the AIC/OR desk, not auto-booked.
4. Request is urgent/emergent (Class X/1A–1C). Don't book. Escalate with acuity class and target time.
5. Missing required fields (laterality, CPT, patient class, anesthesia type). Ask for them and do not submit.
6. Surgeon not privileged for the procedure or specialty. Block and route to credentialing / alternate surgeon.
7. Slot taken between check and book (race). Re-query and re-offer, and verify by read-back.
8. Equipment or vendor conflict (only one C-arm or robot, or implants need 48 hours in SPD). Warn or offer another time.
9. Modify or cancel. Cancel requires a reason; changing CPT, location, or class triggers re-authorization.
10. Multi-surgeon case. Combine lines into one case with total length.

**Intents a credible assistant must handle (table stakes):**
- check_availability (by surgeon/date range/site/room/duration)
- book_case (create request → scheduled)
- get_case_status
- modify/reschedule_case
- cancel_case (reason required)
- release_block / view block schedule
- request_add_on or urgent case (escalation)
- waitlist / notify-when-open
- explain_duration (estimate provenance)
- list readiness gaps

**Entities/slots:**
- patient (name, DOB, MRN)
- surgeon, assistant/co-surgeon
- procedure (name, CPT, modifier, laterality), diagnosis (ICD-10)
- duration (minutes + source)
- anesthesia type, patient class/admission type
- date / date range / time-of-day preference, site/location, room
- equipment (C-arm, robot, microscope), implants/vendor, trays, positioning
- bed type (ICU/non-ICU/none), frozen section, blood products
- isolation/MRSA, latex allergy, interpreter
- authorization status/number, PAT type
- acuity/urgency class
- case number (for modify/cancel), cancel/change reason

### Gaps
- No public example of an actual Epic OpTime or SurgiNet availability-search screen or API payload was found. The examples above are synthesized from policy and form fields and should be labeled illustrative.
- The exact internal case statuses (e.g., Epic's case request vs scheduled case states) were not confirmed from vendor documentation.
