# How OR Settings, Room Types, and Surgical Specialties Change Case Scheduling (US hospitals)

Scope note: these notes add to the earlier round in `../OR scheduling assistant research/` (`constraints.md`, `workflow_and_data.md`). That round already covered generic booking fields, block release horizons, urgency class examples (UTMC Class X/1A/1B/1C), loaner-tray lead times (48 h, or 3 business days for first-time sets), staffing ratios, latex-first sequencing, and the OR cost per minute. Those are referenced here, not repeated. Research ran 2026-10-14. Source dates appear inline where known. Several URL attributions come from search-result sets that could not be opened (PubMed blocked the fetch). Those are marked "(attribution from search results; verify)".

---

## Q1. Settings: hospital main OR vs HOPD vs ASC vs procedural areas (endoscopy, cath lab, IR, L&D)

### Takeaway
The setting mostly changes **who is eligible** and **how predictable the day is**, not the basic booking mechanics.
- **ASCs** take only patients and procedures that Medicare and the facility consider safe to discharge the same day (ASA/BMI/OSA screens). They run shorter, more uniform cases with faster turnover and almost no emergencies.
- **Main hospital ORs** absorb the inpatient, high-acuity, and emergent mix.
- **Procedural areas** (cath lab, IR, endoscopy) run their own schedules. These are slot-based and often in separate EHR modules, with their own emergency-preemption patterns (e.g., STEMI).
- The site-of-service boundary is moving fast. CMS began phasing out the Inpatient-Only list in 2026 and added hundreds of codes to the ASC list, so eligibility rules are configuration that changes every year.

### Cited Findings
**ASC regulatory eligibility (CMS)**
- Through CY2025, the 42 CFR 416.166 test for an ASC covered procedure was:
  - separately paid under OPPS;
  - no significant safety risk in an ASC;
  - no expected need for "active medical monitoring and care at midnight following the procedure" (no overnight stay).

  General exclusions cover procedures that generally cause extensive blood loss, require major or prolonged entry into body cavities, directly involve major blood vessels, or are generally emergent or life-threatening — [eCFR 42 CFR 416.166](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-416/subpart-F/section-416.166); [Cornell LII 416.166](https://www.law.cornell.edu/cfr/text/42/416.166); [AAO-HNS position statement summary](https://entnet.org/resource/position-statement-ambulatory-procedures)
- From 1 January 2026, covered procedures must meet a new paragraph (b)(2). I did not retrieve its text (see Gaps) — [eCFR 42 CFR 416.166](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-416/subpart-F/section-416.166)

**CY2026 OPPS/ASC final rule: site-of-service shift**
- Total knee arthroplasty came off the Inpatient-Only (IPO) list in 2018 and total hip in 2020 — [MedBridge (2026)](https://www.medbridge.com/blog/the-inpatient-only-list-is-almost-gone-what-the-proposed-2027-outpatient-rule-means-for-where-you-operate)
- For CY2026, CMS began a three-year IPO phase-out, removing 285 procedures that are mostly musculoskeletal (CPT 27000 series) — [AAHKS summary of CY2026 OPPS/ASC final rules (Jan 2026)](https://www.aahks.org/wp-content/uploads/2026/01/AAHKS-Summary-2026-Medicare-OPPS-ASC-Final-Rules.pdf). Optum reports 271 IPO removals instead — [Optum/AAPC 2026 presentation](https://www.optumcoding.com/upload/docs/OPPS_ASC_2026_AAPC%20presentation.pdf). The counts conflict.
- CY2026 ASC Covered Procedures List additions (counts vary by source; about 560 total per McDermott+):
  - 271 IPO-removed codes
  - about 289 other surgical codes
  - 168 orthopedic codes, including revision total hip and knee arthroplasty
  - spine fusion codes CPT 22630 and 22633
  - six cardiac ablation codes

  — [Becker's ASC (2026)](https://www.beckersasc.com/legal-regulatory-issues/the-procedures-that-shifted-to-the-outpatient-model-in-2026/); [McDermott+ (2025/2026)](https://www.mcdermottplus.com/?p=159014)
- Proposed for CY2027 (not confirmed final at retrieval): remove 637 more procedures from the IPO list, with the remaining 801 in CY2028, and add 618 procedures to the ASC list — [MedBridge (2026)](https://www.medbridge.com/blog/the-inpatient-only-list-is-almost-gone-what-the-proposed-2027-outpatient-rule-means-for-where-you-operate)

**ASC patient selection: facility and payer level, no single national rule**
- Blue Shield of California's ASC medical policy treats ASA III or higher as high anesthetic risk but allows some ASA III patients by exception, depending on procedure and clinical information. It also lists BMI over 40 with hemodynamic or respiratory problems (e.g., severe OSA) as high risk — [Blue Shield CA medical policy](https://blueshieldca.com/content/dam/bsca/en/provider/docs/medical-policies/Ambulatory-Surg-Center.pdf)
- ASPS (2021): ASA 1-3 patients can be considered for ambulatory surgery. Setting should depend on ASA class, procedure type, and anesthesia type — [ASPS Principle: Patient Selection (2021)](https://www.plasticsurgery.org/documents/Health-Policy/Principles/principle-2021-patient-selection.pdf)
- AANA: many facilities set a BMI cutoff in policy, and candidacy depends on comorbidities, procedure, and anesthetic. Class 3 obesity (BMI 40 or above) carries more perioperative airway and cardiac risk — [AANA, Patient Selection: Elevated BMI](https://www.aana.com/file-download/patient-selection-criteria-clinical-considerations-for-elevated-bmi)
- In a study of 3,444 total joint patients, BMI over 40 was the most common ASC ineligibility factor (32.6%), ahead of comorbidity severity and untreated sleep apnea — [Becker's ASC, "4 key points on patient selection for TJR in ASCs" (date not captured)](https://beckersasc.com/orthopedics-tjr/4-key-points-on-appropriate-patient-selection-for-total-joint-replacement-in-ascs.html)

**Throughput differences by setting**
- Munnich & Parente (Health Affairs 2014; CDC data, about 52,000 visits at 437 facilities): ASC procedures took **31.8 fewer minutes** than hospital procedures, 25% of mean procedure time — [UMN Experts record](https://experts.umn.edu/en/publications/procedures-take-less-time-at-ambulatory-surgery-centers-keeping-c-2/); [Becker's ASC](https://www.beckersasc.com/asc-news/ascs-reduce-procedure-times-25-compared-to-hospitals/)
- A Medicare-based study found total perioperative time **39% shorter** in freestanding ASCs than in hospital-based settings. The authors note it is unclear how much is efficiency and how much is patient selection — [PMC3792562](https://pmc.ncbi.nlm.nih.gov/articles/PMC3792562)
- The earlier round found turnover of 43 min in the OR vs 31 min in the ASC (Advocate Health 2025) — see `constraints.md` Q4.

**Procedural areas (cath lab, IR, endoscopy)**
- A US cath lab redesign set aside 1-2 of 4 labs for urgent and emergent work, varying by weekday. Before the change, STEMI patients went to the first open room and other inpatients were squeezed into gaps or pushed to the next day. Afterwards electives stopped being bumped, and average urgent waits fell by **75%** in the first six months — [Cath Lab Digest/HMP, "Doing More with Less Overtime" (date not captured)](https://hmpgloballearningnetwork.com/site/cathlab/articles/doing-more-less-overtime-improving-patient-flow-through-cath-lab)
- Epic's cardiology module (Cupid) supports creating an emergent STEMI case and placing it on the schedule board. The cath lab schedule therefore sits in a different module from OpTime — [University of Iowa Epic support, Cupid](https://epicsupport.sites.uiowa.edu/epic-resources/cupid)
- IR at Stony Brook covers emergent arterial embolization, TIPS, and abscess drainage, and schedules about **8-10 outpatient electives per day** — [Stony Brook Medicine IR](https://www.stonybrookmedicine.edu/node/1307)
- At University of Iowa IR, emergent GI or trauma bleeds go through an on-call pager, and routine cases go through a weekday nurse coordinator — [UIowa Vascular & IR](https://gme.medicine.uiowa.edu/radiology/node/686)
- Endoscopy add-on workflow (Niagara Health, Canada, 2025): it first asks whether the case is elective or STAT. Urgent add-ons go to the endoscopy scheduler and onto a separate "Urgent List" — [Niagara Health procedure](https://niagarahealth.on.ca/files/Perioperative-ScheduleEmergencyAppointment-ENDO2025-03-141141Approved.pdf)

### Inferences
- **Setting is best modeled as an eligibility gate plus a parameter set, not separate scheduling logic.** An `asc` site profile would carry:
  - a procedure allow-list (from the CMS CPL, updated each year);
  - patient-selection rules (ASA ceiling, BMI ceiling, OSA/STOP-BANG, anticoagulation, distance-to-hospital and similar facility rules);
  - "no overnight" and "no ICU destination" constraints;
  - shorter default turnover;
  - no emergency reserve.

  A `main_or` profile would carry an emergency reserve, inpatient and ICU destinations, and a heavier add-on rate. HOPD sits between them.
- **Agent value:** a "where should this case go?" check at booking. For example: "TKA, ASA III, BMI 42, untreated OSA, which fails ASC criteria at this facility, so offer HOPD/main OR slots." This is a deterministic rules check that the LLM explains. It should never be a clinical judgment by the LLM; the anesthesia-approved criteria are configuration.
- Because the CPL and IPO lists change every year (CY2026, and proposed CY2027 and 2028), the eligibility list must be data with an effective date, not hard-coded.
- **Procedural areas** (cath, IR, endoscopy) usually run on fixed-length slot templates in their own EHR modules (Cupid, Radiant for IR, and so on), often under moderate sedation instead of an anesthesia team. They share the OR's urgency and preemption problem. For a take-home, treat them as stubbed profiles with an "emergent preemption" behavior (STEMI → next available lab). Do not build them out.

### Gaps
- The new 42 CFR 416.166(b)(2) criteria (effective 1/1/2026) were not retrieved. CY2027 final-rule figures were not confirmed; the CY2027 final rule is typically released in early November.
- I found no ASCA or ASA primary document giving a national ASA-class or BMI ceiling for ASCs. These are facility and anesthesia policies.
- I found no US source comparing HOPD with main-OR scheduling practice directly (block structure, release horizons), and no sourced, typical slot lengths for endoscopy (e.g., colonoscopy) or cath lab cases.
- No source was found for how L&D ORs are scheduled day to day (see Q4 for the emergent C-section standard).

---

## Q2. Room types and capability constraints (robotic, hybrid, cardiac, neuro, cysto, ortho/laminar flow, trauma, C-section)

### Takeaway
Rooms differ in four ways that matter for booking:
1. **Fixed capability.** Imaging, robot, laminar flow, cysto table, microscope, perfusion setup.
2. **Longer non-operative time.** Robotic turnover runs about 67-72 min in single-center studies, against roughly 30-45 min generally. Setup and docking add time within the case.
3. **Multi-service sharing.** Hybrid ORs and robots are split among cardiac, vascular, neuro, urology, and other services, with stricter release rules.
4. **Protected status.** Trauma and OB rooms are held open, not booked.

Points 1-3 are parameters on a generic "room capability + shared asset" model. Point 4 is different logic.

### Cited Findings
**Robotic rooms**
- Setup and docking: median setup 22 min (range 9-50) and median docking 10 min (range 2-70) in 96 patients. Experienced dockers took 8 min vs 17.5 min for inexperienced ones (2010) — [Université de Genève archive (2010)](https://archive-ouverte.unige.ch/unige:21022)
- da Vinci Xi learning curve: draping and docking times flattened after about 21 and 18 cases, then averaged about **5 min draping and 7 min docking** (2020) — [PMC7674320 (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7674320) (attribution from search results; verify)
- Hugo RAS vs da Vinci Xi (German prospective study): total non-operative time (setup, docking, undocking, cleanup) was **94.3 vs 81.6 min**. The gap faded after 10-15 cases per scrub nurse — [PMC12413327](https://pmc.ncbi.nlm.nih.gov/articles/PMC12413327) (attribution from search results; verify)
- Robotic **turnover** studies:
  - 2022 human-factors study, 40 observed turnovers: median **67 min**, of which instrument setup was 25.5 min and cleaning 25 min. Interventions (dashboard, role clarity, standardized cleaning) cut about 26 min.
  - 2020 study, 20 turnovers: mean **72 min**, of which cleaning was about 27 min (38%).

  — [PubMed 35220451 (2022)](https://www.pubmed.ncbi.nlm.nih.gov/35220451/); [PubMed 31933120 (2020)](https://www.pubmed.ncbi.nlm.nih.gov/31933120/) (attribution from search results; fetch blocked; verify)
- From the earlier round: robotics blocks auto-release at **14 days** vs 7 for other blocks at St. Charles (2024), and AORN offers robotic scheduling and block-release education — see `constraints.md` Q2.

**Hybrid ORs (fixed angiography/CT plus a full OR)**
- TAVR is best done in a hybrid room with fluoroscopy, DynaCT, and echo guidance, with a surgeon on standby and a heart-lung machine available. EVAR is now commonly done in hybrid rooms — [ACC, "Clinical Advances With Hybrid Surgical Technologies" (2015)](https://acc.org/latest-in-cardiology/articles/2015/04/27/11/05/clinical-advances-with-hybrid-surgical-technologies)
- One surgeon's hybrid OR ran at **80-90% capacity**, with TAVR alone taking a bit over one day per week, which "takes a lot of planning and smart scheduling" — [DotMed HealthCare Business News (Mar 2013)](https://www.dotmed.com/news/story/20488?p_begin=2)
- A Montreal (MUHC) technology assessment found cath labs already had capacity for TAVI and mitral procedures. It projected that a vascular hybrid OR would be about **65%** occupied by vascular cases — [INAHTA/MUHC brief report](https://database.inahta.org/article/13283)
- EVAR in a hybrid suite (51 cases) vs a mobile C-arm OR (58 cases): no difference in complications or mortality, with a trend toward less fluoroscopy time — [Stanford Health Care publication](https://aemqa.stanfordhealthcare.org/publications/377/377815.html)
- A 2018 Bridgeport Hospital poster identified hybrid-OR turnover time as the lever for TAVR throughput — [Bridgeport Hospital poster (2018)](https://scholar.bridgeporthospital.org/poster_presentations/47)
- From the earlier round: Ulm's hybrid OR splits weekly blocks among ortho trauma, vascular/cardiac, and neurosurgery, and a neurosurgical hybrid-OR scoring scale ranks which cases most need the room — see `constraints.md` Q2.

**Trauma-designated rooms**
- An AAST document lists "an adequately staffed and equipped operating room with immediate (15 minutes) availability" as a Level I requirement (edition not stated) — [AAST document](https://www.aast.org/asset/EBB2EE64%2D6F1C%2D4205%2DA99321D990FE6388); secondary summary at [American Trauma Society, Trauma Center Levels](https://www.traumacenters.org/page/TraumaCenterLevels)
- The ACS 2022 *Resources for Optimal Care of the Injured Patient* has standards **3.1 Operating Room Availability**, **3.2 Additional Operating Room**, **3.3 Operating Room for Orthopaedic Trauma Care**, and **4.4 Trauma Surgeon Presence in Operating Room**. I did not retrieve the exact wording. The ACS says the 2022 standards stand alone and replace earlier editions — [2022 ACS standards manual (Louisiana LERN copy)](https://lern.la.gov/wp-content/uploads/2022_vrc_injured-patient-standardsmanual_revised_dec-2022.pdf); [ACS 2022 standards FAQ](https://ww2.facs.org/quality-programs/trauma/quality/verification-review-and-consultation-program/trauma-verification-qas/vrc-2022-standards-qas)
- From the earlier round: St. Charles Bend exempts designated trauma and heart add-on rooms from block auto-release, and HonorHealth releases orthopedic-trauma block time at 07:00 on the day of surgery — see `workflow_and_data.md` Q3.

**L&D / C-section rooms**
- The 30-minute "decision-to-incision" expectation for emergent cesarean comes from ACOG's *Guidelines for Perinatal Care* (consensus; the 5th edition is cited), which notes no data link timing to outcome. Commentators argue it should not be applied universally — [OBG Management (Chauhan)](https://cdn.mdedge.com/files/s3fs-public/issues/articles/media_5b919b0_OBGManagement_ChauhanS_October20.PDF); [OBG Management (2017)](https://cdn.mdedge.com/files/s3fs-public/Document/September-2017/1910OBGM_Article4.pdf); [The Hospitalist/MDedge commentary](https://mdedge.com/content/there-no-gold-standard-decision-incision-time)

### Inferences
- **Generic room model (parameters):**
  - `room.capabilities` = {robot_platform: da Vinci Xi / Mako / ROSA / none, fixed_imaging: hybrid_angio / CT / none, mobile_c_arm_compatible, laminar_flow, cysto_table, neuro_microscope_navigation, perfusion_ready, pediatric_equipped, bariatric_table_rated_kg}
  - `room.default_turnover_min` by room type, e.g., a higher default for robotic rooms based on the 67-72 min studies
  - `room.block_release_days`, e.g., 14 for robotic rooms
  - `room.owner_services`, a multi-service list for hybrid and robotic rooms
- **Shared mobile assets** (robots on carts, C-arms, microscopes, lasers, navigation towers) are resources with their own calendars, which `constraints.md` already covers. A fixed robot or hybrid suite is a **room capability**. A mobile robot is a **shared asset**. The booking logic should treat both as "capability needed → candidate rooms/assets."
- **Trauma and OB rooms are not bookable inventory.** They are held capacity with a response-time SLA (about 15 min for trauma at Level I; about 30 min decision-to-incision for emergent C-section). The agent should never offer them for elective booking. When they get used, that consumes reserve and may trigger displacement of electives in other rooms (see Q4). This is different logic.
- Robotic setup and docking time, and the learning-curve effect, argue for **team-specific** non-operative time parameters ("this scrub team has fewer than 15 robotic cases → add buffer"), but that is a refinement for later.

### Gaps
- I found no sourced numbers for laminar-flow requirements for arthroplasty rooms (it is ventilation design guidance, ASHRAE 170 / FGI, which I did not retrieve), cysto room turnover, or neuro microscope/navigation setup time.
- The exact ACS 2022 standard 3.1-3.3 text was not retrieved. The 15-minute figure comes from AAST and secondary sources, edition unclear.
- No recent (2020 or later) US multi-service hybrid-OR block allocation study was found. The utilization figures above date from 2013-2018.
- No source on bariatric OR table weight ratings or bariatric equipment booking was retrieved.

---

## Q3. Service-line scheduling profiles (ortho, cardiac, neuro/spine, general/bariatric, transplant, OB/GYN, urology, ENT, ophthalmology, pediatrics, vascular, plastics, trauma/ACS)

### Takeaway
Service lines differ along the same handful of dimensions:
- duration mean and variability
- special staff (perfusion, neuromonitoring, vendor reps, robotic teams, pediatric anesthesia)
- equipment and implant lead time
- downstream bed type
- urgency mix
- sequencing rules
- block shape: full-day long cases vs many short cases, with tandem or flip rooms

Most of these are **parameter differences**. Three service-line behaviors are **logic differences**:
1. **Cardiac** couples the OR booking to ICU-bed and perfusion availability, and cancellations follow from them.
2. **Ophthalmology and other high-volume short-case lines** run tandem or two-room throughput.
3. **Transplant, trauma, and emergent OB** arrive unscheduled and displace electives.

Pediatric sequencing (youngest or diabetic first) is a rules-engine configuration, not a new module.

### Cited Findings
**Duration variability (cross-specialty)**
- Iowa, 61,353 cases: process variability (duration prediction error) differed significantly across 11 groups of specialty and urgency. Absolute percentage error exceeded the overall median of 22% for **57% of urgent spine** cases vs **42% of elective spine** cases — [Univ. of Iowa repository (Dexter group)](https://iro.uiowa.edu/esploro/outputs/journalArticle/Influence-of-procedure-classification-on-process/9983983624902771)
- Pediatrics (UCLA, more than 40,000 scheduled cases): the SD of case time was about **30% of the median** (95% CI 25.8-34.7%), and relative variability (CV) was largest for **short** cases — [eScholarship, "The nature and sources of variability in pediatric surgical case duration"](https://escholarship.org/uc/item/2nw3r72h)
- One academic-hospital dataset fit elective durations by specialty to log-normal distributions. A search tool applied CV = sqrt(e^σ² − 1) to the reported σ² values; these CVs are **derived, not reported by the paper, and unverified**:
  - Colorectal ≈ 0.84
  - Hepato-pancreato-biliary ≈ 0.61
  - Breast & endocrine ≈ 0.49
  - Cardiac surgical unit ≈ 0.34

  The hospital's country was not verified — [arXiv 1809.07822, "Analysis of uncertainty in the surgical department"](https://arxiv.org/pdf/1809.07822)
- Large between-facility differences in means and CVs of durations mean that pooled specialty CVs can mislead — [Univ. of Iowa repository](https://iro.uiowa.edu/esploro/outputs/journalArticle/Estimating-surgical-case-durations-and-making/9983806276302771)

**Orthopedics (joints, spine)**
- THA (ACS NSQIP, 131,361 patients): mean operating time fell from **118.3 min (2006) to 89.6 min (2016)**. Times of 120-179 min raised major-complication risk 1.4×, and 180 min or more raised it 2.1× — [Bone & Joint Journal 2019;101-B(6)](https://boneandjoint.org.uk/Article/10.1302/0301-620X.101B6.BJJ-2018-1400.R1) (attribution from search results; verify)
- Spinal fusion (NSQIP 2008-2016, 67,775 cases), mean operative time with ortho vs neuro surgeons in parentheses:

  | Procedure | Mean operative time (min) | Ortho vs neuro |
  |---|---|---|
  | 2-3 level lumbar fusion | ~124-134 | 124 vs 134 |
  | 4 or more levels lumbar fusion | ~176-189 | |
  | ACDF | ~71-77 | |
  | 3-6 level posterior cervical fusion | ~138-157 | |

  — [International Journal of Spine Surgery 16(2):291](https://www.ijssurgery.com/content/16/2/291.full.pdf) (attribution from search results; verify)
- Adult spinal deformity (multicenter, 544 patients): mean operative time **378 min**. The strongest predictor of duration was **institution or surgeon**, and a combined anterior-posterior approach added 139 min — [Duke repository](https://dukespace.lib.duke.edu/items/6a2ad177-04a9-4106-a62b-4370f91b62b6/full) or [eScholarship](https://escholarship.org/uc/item/0f90d92n) (exact attribution between these two results unclear; verify)
- Joint replacement continues to migrate to outpatient and ASC settings (IPO removal: TKA 2018, THA 2020, 2026 phase-out). ASC eligibility hinges on BMI over 40, comorbidities, and OSA — see Q1 sources.
- From the earlier round: loaner implant sets need 48 h (3 business days if first-time), and vendor reps are tied to a specific case — see `constraints.md` Q2.

**Neurosurgery / spine: neuromonitoring (IONM)**
- Hospitals often contract out IONM. A University of New Mexico RFP (2019) sought vendors to supply certified IONM technicians, equipment, and remote physician interpretation to supplement permanent staff — [UNM HSC RFP P409-19](https://hsc.unm.edu/health/about/bids-proposals/doc/2019/p409-19-neuromonitoring-services.pdf)
- Some IONM vendors handle "100%" of IONM scheduling and setup, and vendor coordinators schedule cases with the hospital and surgeon scheduling offices. IONM is therefore an external resource that needs its own confirmation step — [NuVasive Clinical Services NCS Operations Coordinator posting](https://jobs.dukecapitalpartners.duke.edu/companies/nuvasive/jobs/48489353-ncs-operations-coordinator); [CSA job listing describing vendor model](https://careers.csahq.org/job/intraoperative-neuromonitorist/81277953)

**Cardiac surgery**
- A London (Barts) audit found **16.6%** of cardiac cases were cancelled on the day, with urgent cases cancelled more often than elective ones. Reason categories included lack of ITU beds and nurses, lack of perfusionist, scheduling error (overruns or overbooking), and "emergency intervened" (UK) — [STS abstract (Jasionowska)](https://www.sts.org/sites/default/files/documents/Thurs%20A_1210_ABSTRACT%20The%20Cancellation_Jasionowska.pdf)
- UK cardiothoracic modelling reports a **12-15%** operation cancellation rate, with the ICU believed to be the system constraint — [Bahou et al., Strathclyde (2017)](https://strathprints.strath.ac.uk/60718/1/Bahou_HMS2017_Modelling_the_critical_care_pathway_for_cardiothoracic_surgery.pdf)
- Pediatric cardiac ICUs often run at or near capacity, which leads to cancelled electives. Electives are typically scheduled on surgeon and patient preference without regard to CICU capacity. Scheduling patients with an expected 1-2 day stay early in the week (Mon/Tue) reduced CICU census variation and annual cancellations — [Frontiers in Health Services (2021)](https://www.frontiersin.org/articles/10.3389/frhs.2021.787358)
- A dynamic admission policy that considers waiting time and expected ICU length of stay improved equity at small efficiency cost (cardiothoracic OR + ICU queuing/simulation) — [Oxford Brookes RADAR](https://radar.brookes.ac.uk/radar/items/ad81c6be-f2fe-46ad-9503-08a9b407e15d/1)
- TAVR runs in hybrid rooms or cath labs with a standby surgeon and heart-lung machine — see Q2 ([ACC 2015](https://acc.org/latest-in-cardiology/articles/2015/04/27/11/05/clinical-advances-with-hybrid-surgical-technologies))

**Transplant**
- Auckland City Hospital (NZ): acute liver transplants need an OR and team immediately. The usual workaround is to pull an elective list and move it later, which in a full schedule causes a "**domino effect**" of cascading cancellations. Near-100% utilization leaves no buffer — [University of Auckland ResearchSpace](https://researchspace.auckland.ac.nz/handle/2292/31941)
- Transplant subspecialties impose extra block constraints: a subspecialty can be assigned to a block only if an appropriate team is available that day and shift — [arXiv 2607.25482 (2026)](https://arxiv.org/pdf/2607.25482)

**Ophthalmology (cataract)**
- Trade and consultant benchmarks:
  - Two identically equipped and staffed rooms "in tandem," with the surgeon moving between them, reach **5-6 cataract cases per hour**.
  - Many surgeons do **3-4 per hour in one room** (24-32 a day).
  - Surgeons doing fewer than 3 per hour should not get two rooms.
  - Lens selection and paperwork should be done before surgery day.

  — [Becker's ASC, "11 Ways to Improve Efficiency... in Ophthalmology" (older, date not captured)](https://www.beckersasc.com/news-analysis-asc/business-financial-benchmarking/11-ways-to-improve-efficiency-quality-and-profitability-in-ophthalmology.html)

**Pediatrics**
- ACS Children's Surgery Verification:
  - Level I is staffed 24/7 with pediatric specialists, including **pediatric anesthesiologists**, and needs a Level IV NICU.
  - Level II needs a pediatric anesthesiologist and a Level III or higher NICU.
  - Level III relies on general anesthesiologists with pediatric expertise.

  — [Clinician.com summary](https://www.clinician.com/articles/119023-3-levels-of-care-urged-for-peds-surgery); [UC Davis news](https://health.ucdavis.edu/publish/news/newsroom/14217)
- The ACS Level III pre-review questionnaire (2021) asks whether a pediatric anesthesiologist, or an anesthesiologist with pediatric expertise, gives or directly oversees general anesthesia for **all patients 2 years or younger**. This is a case-to-anesthesiologist matching constraint driven by age — [ACS 2021 CSV PRQ Level III](https://ww2.facs.org/media/cmsc0eno/2021_re_csv_prqs_level_iii_v02.pdf)
- List order (UK hospital guidance): the youngest child usually goes first, but this is not rigid. Type of operation, biopsy lab cutoffs, and infection status (MRSA) can override it, and a true anesthetic drug allergy means going first — [Cambridge University Hospitals, paediatric list orders](https://www.cuh.nhs.uk/patient-information/paediatric-surgery-list-orders-information-for-parents-and-carers/)
- Children with type 1 diabetes should be first on the morning list (Australian guideline) — [Sydney Children's Hospitals Network policy](https://resources.schn.health.nsw.gov.au/policies/policies/pdf/2013-7048.pdf)
- In a 1,820-patient pediatric study, fasting times were shorter for **first scheduled** patients. Later surgery time, younger age, and longer clear-fluid fasting were each independently associated with complications (non-US) — [J Anesth Analg Crit Care (Feb 2024)](https://doaj.org/article/cdb5fe5431fe4a21b44102bd35bb85f7)

**Interventional cardiology / IR / endoscopy** — see Q1 (procedural areas).

### Inferences

**Service-line profile matrix (synthesis).** Cited items point to the sources above. Items marked "(unsourced heuristic)" are common domain knowledge I could not cite this round; validate them with the client.

| Service line | Duration and variability | Special staff and equipment | Downstream bed | Urgency mix | Sequencing and block shape | Logic vs params |
|---|---|---|---|---|---|---|
| Ortho: joints | THA about 90 min (2016 NSQIP mean); fairly predictable | Implants/loaners (48 h), vendor rep, often Mako robot; ASC eligibility (BMI, OSA) | Same-day, observation, or floor | Mostly elective | Full-day blocks, often flip rooms for high-volume surgeons (UTMC flip-room criteria in earlier notes) | **Params** (best candidate for the fully built profile) |
| Ortho: spine | 71 min (ACDF) to 378 min (deformity); surgeon/institution is the top predictor; urgent spine much less predictable | IONM tech (often an external vendor), navigation/O-arm, implants, rep | Floor; ICU for deformity | Elective plus urgent (cord compression) | Long cases, often one or two per day | **Params** plus an external-resource confirmation step |
| Ortho: trauma | Variable | C-arm, fracture tables (unsourced heuristic) | Floor | Urgent; "long bone fracture within 24 h" class (UTMC) | Dedicated ortho trauma room (ACS 2022 std 3.3); block released day-of (HonorHealth) | **Logic:** held/released-day-of capacity |
| Cardiac (CABG/valve) | Lower relative variability than colorectal in one dataset (derived CV ≈ 0.34) but long | Perfusionist and pump, cardiac anesthesia; TAVR needs hybrid/cath plus standby pump | **ICU bed required** | Elective, urgent, emergent; urgent cases cancel more | Typically one or two cases per room per day (unsourced heuristic); spread ICU-heavy cases across the week (Mon/Tue short-stay result) | **Logic:** joint OR + perfusion + ICU-bed reservation; ICU census drives cancellations |
| Neurosurgery (cranial) | Long, variable (unsourced heuristic) | Microscope, navigation, IONM; hybrid OR for some | ICU or step-down | Elective plus emergent (bleeds) | Hybrid-OR priority scoring (earlier notes) | **Params** plus asset/IONM confirmation |
| General / colorectal / bariatric | High variability (derived colorectal CV ≈ 0.84) | Bariatric table, beds, and stretchers (unsourced heuristic); robot often | Floor | Large add-on/acute-care component | Standard blocks | **Params**; acute care surgery is in the emergency stream |
| Transplant | Long, unscheduled start | Team availability by day/shift; donor-organ-driven timing | ICU | Unscheduled, effectively emergent | Displaces electives ("domino effect") | **Logic:** unscheduled arrival plus displacement |
| OB/GYN | Scheduled C-sections and GYN are predictable; emergent C-section has a 30-min target | L&D OR, neonatal team (unsourced heuristic) | Postpartum or NICU | Mixed; labor-driven | L&D rooms held; GYN often in the main OR or ASC | **Logic** for L&D emergent; **params** for elective GYN |
| Urology | Many short cysto cases plus robotic prostatectomy (unsourced heuristic) | Cysto table/fluoro, laser, robot | Mostly same-day | Mostly elective plus stones/obstruction urgent | Short-case blocks | **Params** |
| ENT | Many short cases (T&A, tubes), especially pediatric (unsourced heuristic) | Microscope, navigation for sinus | Same-day | Elective; airway emergencies are rare | Short-case blocks | **Params** |
| Ophthalmology | Very short; 3-4/hr in one room, 5-6/hr two-room tandem | Phaco, microscope; lens chosen pre-day | Same-day | Elective; ASC-heavy | **Tandem/two-room** model; dozens of cases a day | **Logic:** parallel-room throughput (or params if modeled as a generic "flip room" pattern) |
| Pediatrics (cross-cutting) | High relative variability for short cases (SD about 30% of median) | Pediatric anesthesiologist for 2 years or younger at ACS-verified centers; child life (unsourced) | Same-day, floor, PICU/NICU | Mixed | Youngest/diabetic first, allergy first, MRSA later | **Params** in a generic sequencing-rules engine plus an age-based anesthesiologist matching constraint |
| Vascular | Variable; EVAR suits hybrid | Hybrid or C-arm, endografts/implants, rep | Floor or ICU | Elective plus emergent (ruptured AAA, ischemia) (unsourced heuristic) | Shares hybrid with cardiac and neuro | **Params** plus shared-room arbitration |
| Plastics | Variable; much cosmetic work in ASCs or office suites (unsourced heuristic) | Implants | Same-day | Elective; self-pay cosmetic has different pre-op/financial clearance (unsourced) | Standard | **Params** |
| Trauma / acute care surgery | Highly variable | Held trauma OR (Level I about 15 min) | ICU or floor | Emergent | Not booked; consumes reserve | **Logic:** reserve and preempt |

- **Design implication:** a `SchedulingProfile` per service line that is mostly data:
  - duration source (surgeon-procedure history with P50/P80) and a variability flag
  - required room capabilities
  - required staff roles (perfusion, IONM, robotic-trained, pediatric anesthesia for age 2 or under)
  - external resources needing confirmation (vendor rep, IONM vendor, loaner set lead time)
  - default post-op destination and its bed type
  - pre-op checklist items
  - sequencing preferences
  - default block shape

  Plus a small set of pluggable **behaviors**: `standard_booking`, `bed_coupled_booking`, `tandem_room_booking`, `reserve_and_preempt`, `unscheduled_arrival`.
- **For the take-home:** fully build **orthopedic joints**. It exercises the most generic constraint types (implant/loaner lead time, vendor rep, robot capability, ASC vs HOPD eligibility, post-op destination, flip rooms) without event-driven logic. Stub **cardiac** (show the ICU-bed coupling hook), **ophthalmology** (tandem rooms), **pediatrics** (sequencing rules), and **trauma/transplant/OB** (reserve-and-preempt routed to humans).

### Gaps
- No sourced US numbers were retrieved for typical CABG or valve operative times (STS database), cranial neurosurgery, bariatric, urology, ENT, plastics, or vascular case durations. All of those table entries are heuristics.
- No source was found for bariatric equipment booking (table weight ratings, bariatric beds), urology cysto room specifics, ENT, plastics, child life scheduling, or perfusionist staffing ratios as a scheduling constraint. Perfusion appears only as a cancellation category (Barts audit).
- The sequencing evidence (youngest-first, diabetic-first) comes from UK and Australian hospitals. No US primary policy was retrieved, though it is widely practiced.
- AAOS, STS, and AAP society scheduling guidance was not found. These societies mostly publish clinical, not scheduling, guidance.
- Several duration statistics are attributed from search-result sets without opening the paper (THA, spine fusion, ASD). Verify before quoting numbers in an interview.

---

## Q4. Urgency classes, add-ons, held-open rooms, and how emergent cases displace electives

### Takeaway
Earlier notes established that urgency classes are hospital-defined (e.g., UTMC Class X = 15 min, 1A = 1 h, 1B = 2-3 h, 1C = 6 h, long-bone fracture = 24 h) and that Dexter's priorities govern day-of decisions. This round adds the structural options hospitals use to protect elective schedules:
- **dedicated emergency/urgent rooms or labs** (Mayo; cath lab 1-2 of 4 labs reserved);
- **held trauma and OB rooms** with response-time standards;
- **reservation-planning** models that cap how many electives to accept given expected emergency demand.

When those buffers are absent, emergencies such as transplants cause cascading elective cancellations. Displacement is a human decision (charge nurse, anesthesia in charge, OR director). The agent's job is to route, inform, and re-offer, not to choose who gets bumped.

### Cited Findings
- Mayo Clinic: the old schedule had "no way to easily insert the inevitable emergency cases without severely disrupting elective cases," and cases got bumped past 5 p.m. A simulation compared dedicated elective rooms, dedicated non-elective rooms, and versatile rooms — [The Hospitalist, "Changed surgical culture focuses on patients, needs"](https://community.the-hospitalist.org/content/novel-or-scheduling-and-staffing-boosts-efficiency); [Winter Simulation Conference 2014](https://informs-sim.org/wsc14papers/includes/files/122.pdf)
- Reservation planning: a classic model decides how many extra elective requests to accept on a day given random emergency demand — [Gerchak, Gupta & Henig, Management Science 1996](https://pubsonline.informs.org/doi/10.1287/mnsc.42.3.321) (pre-2018, foundational)
- A robust-optimization paper argues the question is not just how much slack to add but **where in the day** to place it — [arXiv 2608.03931 (2026)](https://arxiv.org/pdf/2608.03931)
- Cath lab: reserving 1-2 of 4 labs for urgent and emergent work cut urgent waits by 75% and stopped elective bumping — [Cath Lab Digest/HMP](https://hmpgloballearningnetwork.com/site/cathlab/articles/doing-more-less-overtime-improving-patient-flow-through-cath-lab)
- Transplant: emergencies in a fully booked system set off a "domino effect" of cancellations — [University of Auckland](https://researchspace.auckland.ac.nz/handle/2292/31941)
- Cardiac: "emergency intervened" is a named day-of cancellation category, and urgent cardiac cases are cancelled more often than electives — [STS abstract (Barts)](https://www.sts.org/sites/default/files/documents/Thurs%20A_1210_ABSTRACT%20The%20Cancellation_Jasionowska.pdf)
- Trauma OR availability (Level I about 15 min) and emergent C-section (about 30 min decision-to-incision) are response-time standards — see Q2 sources.
- Urgent cases have worse duration predictability than electives (urgent spine 57% vs elective spine 42% above the median error) — [Univ. of Iowa repository](https://iro.uiowa.edu/esploro/outputs/journalArticle/Influence-of-procedure-classification-on-process/9983983624902771)

### Inferences
- **Separate the elective-booking path from the urgent/emergent path.**
  - The elective path is a constraint-satisfying slot search, which is the main agent use case.
  - The urgent/emergent path is a **triage and notify** workflow. It captures the class, procedure, surgeon, patient readiness, and required capabilities; it then pages or notifies the AIC/OR desk, shows which rooms could take the case and which elective cases might be affected, and records the human decision.
- Parameters per facility: urgency class definitions and SLAs, whether dedicated emergency rooms exist and how many by weekday, the add-on cutoff time, and who approves bumps.
- **Logic that differs:** an "unscheduled arrival with preemption" module. It covers trauma, transplant, emergent OB, and STEMI (cath lab). It reads elective schedules and computes displacement options but does not write without human confirmation.
- When an elective is bumped, the agent can add value by **re-offering** the displaced case: finding the next slots that satisfy all its constraints, notifying the surgeon's office, and releasing or re-holding the tray, rep, and bed.

### Gaps
- No US national standard for urgency classes, as the earlier round also found (ACS NSQIP has emergency flags, not class SLAs).
- No source was found quantifying how often electives are bumped by emergencies in US hospitals, or typical add-on volumes by service line.
- No source covered organ-offer timing specifics (e.g., typical hours from offer to incision) for transplant OR planning.

---

## Q5. Which differences are "different parameters" vs "different scheduling logic"?

### Takeaway
Most variation across settings, rooms, and service lines can be expressed as **data on a common constraint model**: capabilities, resources and roles, lead times, duration distributions, turnover, bed destination, eligibility rules, sequencing preferences, and release horizons. Genuinely different **logic** arises in about four places:
1. **Reserve-and-preempt / unscheduled arrival:** trauma, transplant, emergent OB, STEMI. These need a triage and displacement workflow, not a slot search.
2. **Downstream-capacity-coupled booking:** cardiac, ICU-heavy neuro and transplant. The OR slot and ICU bed must be reserved together, with census smoothing across the week.
3. **Parallel-room throughput:** ophthalmology tandem rooms, flip rooms.
4. **Site-of-service eligibility gating:** ASC vs HOPD vs main OR.

Points 3 and 4 can be built as generic, configurable components, so only points 1 and 2 truly need separate modules.

### Cited Findings
- Duration predictability differs by specialty **and** urgency, and surgeon/institution is the strongest predictor for complex spine. Duration modeling should be per surgeon-procedure, with variability as a parameter — [Univ. of Iowa repository](https://iro.uiowa.edu/esploro/outputs/journalArticle/Influence-of-procedure-classification-on-process/9983983624902771); [Duke repository (ASD)](https://dukespace.lib.duke.edu/items/6a2ad177-04a9-4106-a62b-4370f91b62b6/full)
- Downstream ICU capacity is a binding constraint for cardiac, and smoothing by weekday reduces cancellations. This is logic beyond a single-slot check — [Frontiers in Health Services (2021)](https://www.frontiersin.org/articles/10.3389/frhs.2021.787358); [Bahou et al. (2017)](https://strathprints.strath.ac.uk/60718/1/Bahou_HMS2017_Modelling_the_critical_care_pathway_for_cardiothoracic_surgery.pdf)
- Protected emergency capacity (dedicated rooms or labs) is a structural choice that changes which rooms the elective logic can see — [Cath Lab Digest/HMP](https://hmpgloballearningnetwork.com/site/cathlab/articles/doing-more-less-overtime-improving-patient-flow-through-cath-lab); [WSC 2014 (Mayo)](https://informs-sim.org/wsc14papers/includes/files/122.pdf)
- Hybrid block/open scheduling has been formalized as a mixed-integer model on real data (Rome, 2025). Allocation policy is a tunable layer separate from case booking — [Springer Operations Research Forum (2025)](https://link.springer.com/article/10.1007/s43069-025-00432-1)
- Tandem two-room cataract scheduling is reserved for surgeons above a throughput threshold (about 3 or more per hour), so it is an eligibility parameter on top of a parallel-room pattern — [Becker's ASC](https://www.beckersasc.com/news-analysis-asc/business-financial-benchmarking/11-ways-to-improve-efficiency-quality-and-profitability-in-ophthalmology.html)
- ASC eligibility is defined by regulation (416.166) plus facility rules (ASA, BMI, OSA), and the code lists change every year — see Q1 sources.

### Inferences

**Proposed split for the candidate's architecture:**

| Concern | Data/config (same engine) | Different logic (separate module/strategy) |
|---|---|---|
| Duration | Surgeon-procedure P50/P80, specialty fallback, urgency inflation factor | — |
| Turnover | Per room type (e.g., robotic about 60-70 min by default), per site | — |
| Room fit | Capability flags on rooms; required capabilities on procedure/profile | — |
| Shared assets | Asset calendars (robot cart, C-arm, microscope, IONM machine) | — |
| Special staff | Required role list (perfusion, IONM, robotic scrub, peds anesthesia for age 2 or under); "confirm with" routing | — |
| External vendors | Rep/IONM/loaner lead-time rules (48 h, 3 business days) | — |
| Pre-op | Checklist per profile (e.g., ASC: anesthesia screen; cardiac: cardiology clearance/echo; peds: fasting instructions) | — |
| Block rules | Release horizons per room or service (7 vs 14 days robotic; day-of for ortho trauma) | Block **allocation** optimization is a separate tactical layer, out of scope |
| Sequencing | Rule list with priorities (latex first, youngest/diabetic first, MRSA later) | Generic rules engine; conflicts escalate |
| Site of service | Eligibility rules (CPL list with effective date, ASA/BMI/OSA thresholds) | Generic gate component |
| Parallel rooms | Surgeon eligibility for flip/tandem (threshold), room pairs | `tandem_room_booking` strategy (could stay generic) |
| Downstream beds | Default post-op destination per profile | `bed_coupled_booking`: atomic OR + ICU hold, weekday smoothing (**cardiac, transplant, ICU neuro**) |
| Emergencies | Urgency class SLAs, reserved room counts by weekday, approver roles | `reserve_and_preempt` / `unscheduled_arrival`: triage, show displacement options, human decides (**trauma, transplant, emergent OB, STEMI**) |

- **Interview framing:** "One booking engine, many profiles. A profile is a config bundle plus a behavior strategy. 90% of service-line differences are config. The few that change control flow (bed-coupled, reserve-and-preempt) are separate strategies behind the same agent interface, and the high-stakes ones route to humans by design."
- **Profile interface sketch** (for stubs):
  - `eligible(case, site) -> pass/fail + reasons`
  - `required_resources(case) -> {room_caps, assets, roles, external_confirmations, lead_times}`
  - `duration(case) -> distribution`
  - `sequencing_prefs(case) -> soft rules`
  - `post_op(case) -> bed_type`
  - `booking_strategy -> standard | bed_coupled | tandem | reserve_and_preempt`
- **Recommended "fully built" profile:** orthopedic total joints in HOPD/main OR with an ASC eligibility gate. It is high volume, high revenue, elective, and rich in deterministic constraints (implants, rep, robot, loaner 48 h, post-op destination, flip rooms). Stub the others with the same interface, each returning a clear "not supported in prototype; route to X" message.

### Gaps
- No published taxonomy maps service lines to scheduling-logic classes. The split above is my synthesis from the cited constraints, not an industry standard.
- I did not verify how Epic OpTime represents service-line-specific booking rules (e.g., procedure-level required equipment and staff roles, or case-request templates per specialty). That would confirm which items already exist as EHR data versus agent-side config.
- No vendor (Intuitive, Stryker) robotic program scheduling guidance was retrieved.
