# Stakeholders, Pain Points, KPIs and Economic Value in US Hospital OR Scheduling

Source-type labels used throughout: **[PR]** peer-reviewed; **[V]** vendor claim (self-reported, not independently verified); **[T]** trade press; **[C]** consultant/advisory firm; **[H]** hospital policy or form; **[A]** academic, not peer-reviewed (project page, DNP capstone). Dates are publication date or data year, as stated. Research cutoff: Oct 2026.

Caveat on method: several vendor PDFs (Qventus case studies) could not be text-extracted in full; their figures come from search-index excerpts of those PDFs and should be re-checked against the PDF before quoting in a deliverable.

---

## 1. Who are the stakeholders and what jobs do they need done?

### Takeaway
Booking one OR case is a multi-party coordination job. The surgeon office scheduler originates the request, the central OR scheduling coordinator turns it into a valid slot, and anesthesia, pre-admission testing (PAT), sterile processing (SPD) and the day-of OR board consume the booking's information. Leaders (perioperative director, CFO/COO) care about the aggregate: utilization, case volume, contribution margin. A chat assistant mainly changes the coordinator's and office scheduler's work. Downstream stakeholders benefit only if the booking it produces is complete and accurate.

### Cited Findings
- A single case booking needs, at minimum: patient name, surgeon and assisting personnel, procedure description or billing code with site/side, diagnosis codes, proposed anesthesia, insurance approval and patient consent. Faxes, paper forms, phone calls, email, Excel sheets and whiteboards are common tools "even [at] very large hospitals and ASCs" — [LeanTaaS, "6 Communication Problems in Surgery Scheduling" [V], undated](https://surgical-clinics.leantaas.com/?p=3084)
- A "fully engaged surgery scheduler may exchange 40-plus messages" per case with case assistants, OR managers, vendors, anesthesia, authorization teams, physical therapists and others. The role is repetitive and manual, which hurts satisfaction, productivity and retention — [Becker's Spine Review, "7 common causes of inefficient orthopedic and spine case scheduling" [T, likely vendor-authored contributed piece], date not retrieved](https://www.beckersspine.com/orthopedic-spine-practices-improving-profits/7-common-causes-of-inefficient-orthopedic-and-spine-case-scheduling/)
- Hospitals still accept case requests through several channels. HonorHealth (AZ) offers an online request form but also a fax form (revised 2025), and clinical orders and documentation "will need to be faxed upon submission of case request" — [HonorHealth scheduling overview [H], 2021](https://www.honorhealth.com/sites/default/files/2021-09/scheduling-overview.pdf); [HonorHealth surgery scheduling fax request form [H], Oct 2025](https://www.honorhealth.com/sites/default/files/2025-10/surgery-scheduling-fax-request-form.pdf)
- Stony Brook Medicine encourages faxing bookings and also takes phone calls — [Stony Brook "Scheduling: Booking Procedure" [H], undated](https://www.stonybrookmedicine.edu/node/658)
- At The Christ Hospital (Cincinnati), urgent next-day cases are booked by calling the OR bookers, and a case "will not be scheduled until the Surgery Reservation Packet is received" with all required information — [Christ Hospital surgery scheduling information sheet [H], 2018](https://www.thechristhospital.com/OrderForms/2018/Surgery%20scheduling%20information%20sheet.pdf)
- Emory's OR scheduling form states that if the form is not complete, "case will not be scheduled" — [Emory Healthcare OR scheduling form [H], May 2026](https://www.emoryhealthcare.org/-/media/Project/EH/Emory/ui/pdfs/south/wrp-or-scheduling-form-05-2026.pdf)
- When no duration is provided, St. Luke's (Boise) scheduling system averages the surgeon's previous case times — [St. Luke's surgery scheduling guidelines [H], undated](https://stlukesonline.org/en/for-providers/surgery-scheduling/)
- In Qventus's Banner Health deployment, the surgeon's scheduler receives block-release "nudges." Schedulers use a "TimeFinder" tool to search open slots by day, time, room type, equipment and procedure duration and book "with just a few clicks." Unused slots are offered by email to the surgeon most likely to need them, then to the next candidate — [Qventus Banner Health customer story [V], ©2025](https://qventus.com/resources/customer-successes/banner-health)
- About one third of same-day cancellations at Tulane (2009 data) came from hospital-side problems such as "scheduling errors leading to missing equipment or beds." More than 30% came from patients not arriving at the correct time. These are the failure points for SPD/equipment, bed management and patient communication — [Advisory Board Daily Briefing [T], May 2012, summarizing Tulane study](https://www.advisory.com/daily-briefing/2012/05/09/same-day-surgery-cancellations-cost-hospitals-millions); [FierceHealthcare [T], 2012](https://www.fiercehealthcare.com/healthcare/hospitals-lose-millions-from-cancelled-surgeries)
- OR leaders are judged on surgical volume and margin. Becker's (2020) reports the OR accounts for "up to 65% of hospital profit margin," citing Surgical Directions — [Becker's Hospital Review [T/C], 2020](https://www.beckershospitalreview.com/strategy/how-to-rebuild-surgical-revenue-after-covid-19-even-if-you-just-lost-60-of-your-or-volume.html)

### Inferences
**Stakeholder value map.** Jobs-to-be-done and the "what changes" column are synthesis. Evidence for each pain is in Section 2.

| Stakeholder | Job-to-be-done | Pains today (see §2 for evidence) | What a chat booking assistant could change | KPIs that would show value |
|---|---|---|---|---|
| **Surgeon office scheduler** (clinic side; often owns the surgeon's block) | Get the patient a date the surgeon and patient accept. Submit a complete request once. | Fax/phone/portal requests. Phone tag over missing fields. No visibility into open time outside own block. Block-release requests arrive as nudges/emails. | Self-serve availability check ("Dr. X needs 180 min, robot, next 3 weeks"). Required-field validation at intake. Instant hold or confirmation. Release unused block in one turn. | Time from decision-to-operate to confirmed date. Requests returned for missing info (%). Touches per case. Release lead time (days). |
| **Central OR scheduling coordinator** (primary user in this take-home) | Turn requests into valid, conflict-free bookings. Fill released and open time. Keep the schedule accurate. | Searching several views for open time. 40+ messages per case. Re-keying fax content into the EHR. Chasing incomplete info. Manual tracking across email, spreadsheets and phone. | Natural-language availability search across blocks, released time, rooms and equipment. Pre-filled booking from the request. Completeness checklist. Conflict checks (room, equipment, surgeon double-booking). Audit trail. | Time-to-book (min per case). Touches/calls per case. Bookings per FTE per day. Rework rate (edits after booking). Scheduler overtime and turnover. |
| **Perioperative services director / OR manager** | Maximize productive use of staffed OR time. Allocate blocks fairly. Grow volume. | Block hoarding and late release. Released time going unfilled. Utilization metric disputes (raw vs adjusted). Inaccurate durations causing overruns. | Data on released time and how fast it is picked up. Better-fit case placement. Structured data feeding block reviews. | Block utilization (adjusted). Prime-time utilization. Released-time pickup (fill) rate. Cases per OR per month. Overtime minutes. |
| **Surgeon** | Operate on own patients promptly, at preferred times, with right equipment and team. | Cannot find time outside own block. Losing block for low utilization. Day-of delays from missing equipment. | Faster access to open or released time. Robot and equipment availability visible at booking. | Lead time to surgery. Cases booked outside own block. On-time starts. Same-day cancellations. |
| **Anesthesia** | Staff rooms and plan anesthesia type. Flag high-risk patients for pre-op evaluation. | Late add-ons. Missing anesthesia type or comorbidity info at booking. Overruns into overtime. | Anesthesia type and risk flags captured at booking. Earlier visibility of case mix. | Late-room / overtime minutes. Same-day cancellations for medical reasons. |
| **Charge nurse / OR board runner** | Run the day's board: start on time, turn rooms, handle add-ons. | Schedule that doesn't match reality (durations, equipment). Day-of surprises. | More accurate durations and equipment requirements at booking. Fewer day-of changes. | First-case on-time starts. Turnover time. Day-of schedule changes. |
| **Sterile processing (SPD)** | Have the right trays and implants ready on time. | Late or incomplete equipment and instrument info. Vendor implant trays not requested. | Equipment and implant fields required at booking. Earlier lead time. | Delays or cancellations attributed to equipment. Flash/immediate-use sterilization events. |
| **Pre-admission testing (PAT) nurse** | Get the patient medically cleared before the day of surgery. | Learning of cases too late. Missing contact info and history. | Automatic PAT referral or risk triage at booking. Captures lead time. | % of cases with PAT complete by T-72h. Cancellations for incomplete workup. |
| **Patient** | Get a surgery date quickly, with clear instructions, and not be cancelled. | Waiting for callbacks. Day-of cancellation. Wrong arrival time. | Faster confirmation. Fewer errors driving cancellation. (Patients don't use the coordinator-facing assistant directly.) | Days from decision to surgery. Same-day cancellation rate. Patient-side no-shows. |
| **CFO / COO** | Grow surgical contribution margin without adding ORs or staff. | Paying for staffed but idle OR minutes. Volume leaking to competitors. Scheduler labor. | More cases in existing capacity. Fewer wasted minutes. Lower scheduling labor per case. | Incremental cases/month × contribution margin per case. Cost of idle staffed minutes. ROI and payback period. |

- The assistant's direct users are the coordinator and the office scheduler. Every other stakeholder benefits through the booking: complete data, correct duration and equipment, and earlier lead time. The prototype's metrics should therefore cover both workflow speed (time-to-book, touches) and booking quality (completeness, conflict-free, later cancellation).
- Block-release behavior belongs to the surgeon and the office scheduler, not the central coordinator. An assistant that only books, without exposing released time, captures only part of the value.

### Gaps
- No time-motion study or survey of what share of a central OR scheduler's day goes to finding time versus chasing info versus data entry. Peer-reviewed studies of scheduler burnout or turnover were not found either. The "40+ messages" figure is from a trade or vendor piece of unknown date.
- No quantitative US data found for SPD-attributed delays or PAT completion rates linked to booking quality.

---

## 2. What pain points are documented (with evidence)?

### Takeaway
The best-documented pains are (a) unused and late-released block time, (b) inaccurate case-duration estimates (EHR averages land within ±10% of actual only about a third of the time), (c) incomplete requests that stall bookings or cause later cancellation, and (d) fax/phone intake with phone tag. Hard numbers on scheduler time per booking and burnout are largely missing from the public literature. Most "pain" evidence comes from hospital forms, trade press and vendor material.

### Cited Findings
**Block hoarding / late release**
- Providence reports a 30% reduction in "unused and unreleased block time" after adopting LeanTaaS iQueue (since 2023). Backfill of released slots was 34% "with improving numbers month over month" — [Becker's Hospital Review, "A matter of OR minutes" [T reporting V outcome], ~2024–25; page could not be fetched, figures from search excerpt](https://www.beckershospitalreview.com/finance/a-matter-of-or-minutes-health-systems-notch-big-financial-wins-with-ai.html)
- Banner Health's baseline (Qventus): utilization "falling short of patient demand," difficulty finding available OR time, manual scheduling processes and "significant amounts of unused, unreleased block time" — [Qventus Banner Health [V], ©2025](https://qventus.com/resources/customer-successes/banner-health)
- Release-window practice varies widely. Some ASCs release 24 hours to 1 week ahead — [Becker's, Q&A with Dawn McLane, Health Inventures [T], undated](https://www.beckershospitalreview.com/care-coordination/how-to-ensure-maximum-operating-room-utilization-qaa-with-dawn-q-mclane-of-health-inventures/). Loma Linda moved outlying elective sites to a 21-day release after finding surgeons could not backfill time released at 14 days. Silver Cross Hospital moved to 28-day proactive release during a renovation — [Becker's, "3 health system leaders on why block utilization doesn't tell the full story" [T], ~2024–25; attribution from search excerpt](https://www.beckershospitalreview.com/or/3-health-system-leaders-on-why-block-utilization-doesnt-tell-the-full-story-and-what-grew-surgical-volume-7/)
- Counterpoint from OR-management science: a 2005 review summarized that when OR time is released matters much less than having the correct OR allocations in the first place — [Dexter et al., University of Iowa repository [PR], ~2005; mapping of finding to this record is from search excerpt](https://iro.uiowa.edu/esploro/outputs/journalArticle/Operating-room-efficiency-and-scheduling/9983806265302771)

**Inaccurate case durations**
- In 46,986 surgeries, the institution's standard estimate placed 32% of cases within ±10% of actual duration. A surgeon-specific ML model raised that to 39% — [Bartek et al., J Am Coll Surg 2019 [PR]](https://pmc.ncbi.nlm.nih.gov/articles/PMC7077507)
- An AI model predicted 48% of cases within ±20% of actual duration, versus 17% for the EHR system's estimate — [OR Manager brief [T, summarizing a study], Dec 4 2024](https://ormanager.com/briefs/study-ai-improves-surgical-case-length-predictions)
- A prospectively deployed ML model at MD Anderson (33,815 cases) produced 11.2% fewer underpredicted cases and 5.9% more cases within 20% of actual than human schedulers. Its advantage over schedulers was smaller than its advantage over raw EHR estimates — [MD Anderson, "Development and implementation of a machine learning model…" [PR], ~2020s](https://mdanderson.elsevierpure.com/en/publications/development-and-implementation-of-a-machine-learning-model-for-pr/)
- In 326 orthopedic cases at a Level 1 trauma center (WVU), Epic's predicted time was "correct" (within 30%) 77.9% of the time versus 48.2% for surgeon predictions. Multi-procedure cases showed significantly larger discrepancies — [WVU poster/abstract [A], ~2025](https://health.wvu.edu/media/18934/42-vincent-melemai-21925.pdf)
- Most EHRs estimate duration by averaging a handful of recent cases, excluding outliers and ignoring complexity and time of day — [Apella blog [V], undated](https://apella.io/blog/what-hospitals-get-wrong-about-or-scheduling)

**Incomplete booking info → stalled bookings and cancellations**
- Paper request forms faxed to an ASC scheduling office were sometimes left partly blank, which required "a series of back-and-forth phone calls." The fix was a digital form with required fields. Separately, an Illinois ASC stopped taking schedule requests by phone because of mis-speaking, mis-hearing and forgetting — [Becker's ASC/Spine scheduling articles and LeanTaaS [T/V], undated; exact article attribution from search excerpt](https://www.beckershospitalreview.com/asc-turnarounds/8-points-about-scheduling-cases-in-an-asc.html); [LeanTaaS [V]](https://surgical-clinics.leantaas.com/?p=3084)
- Hospitals refuse to schedule incomplete requests (Emory 2026, Christ Hospital 2018). See Section 1 citations.
- In non-US peer-reviewed studies, "incomplete medical work-up" was the most common cause of day-of cancellation (32%) in 1,716 open-heart cases. In a 10,000-case series (5.84% day-of cancellations), the most common avoidable causes were poor patient preparation, scheduling error and poor surgical decision — [search excerpts of international studies [PR], dates unverified](https://bmchealthservres.biomedcentral.com/articles/10.1186/s12913-016-1475-6/tables/2); [PAFMJ [PR]](https://pafmj.org/PAFMJ/article/download/7315/3525/55018)

**Fax/phone intake, phone tag, scheduler workload**
- Schedulers "spend hours tracking changes across emails, spreadsheets, and phone calls" — [LeanTaaS-associated blog via purpose.jobs [V], undated](https://www.purpose.jobs/blog/3-ways-leantaas-helps-clinicians)
- Phone calls and faxes leave staff "playing phone tag with physician offices" — [One Mnet Health marketing page [V], undated](https://onemnethealth.com/?p=88902)
- HonorHealth lists "less time spent scheduling" as a benefit of its online request form, with no figure attached — [HonorHealth [H], 2021](https://www.honorhealth.com/sites/default/files/2021-09/scheduling-overview.pdf)

**Patient access / backlog / leakage**
- At one large US health system, 15% of surgical cases were cancelled within 72 hours of surgery, and only about 50% of those were rescheduled and performed within 90 days. That is an estimated $35M/yr opportunity at an assumed $5,000 contribution margin per case — [Qventus eBook "$35M Problem: Surgical Leakage" [V], Feb 2026](https://www.qventus.com/wp-content/uploads/2026/02/Qventus-eBook-35MProblem-SurgicalLeakage-1.pdf)

### Inferences
- Duration accuracy is a booking-time problem. The coordinator accepts or overrides the default duration when booking. An assistant that shows the surgeon's historical distribution (median and variance) and flags multi-procedure cases could improve accuracy without its own ML model.
- Incomplete info is the most addressable failure for a chat assistant. Required-field enforcement is the proven fix for paper/fax forms, and a conversational agent can do it while asking only for what is missing.
- About a third of the Tulane cancellations (missing equipment or beds from scheduling errors) are hospital-process failures that better booking data could prevent.

### Gaps
- No peer-reviewed US data (2018–2026) found on hours per week schedulers spend on phone tag, or on scheduler turnover rates.
- No recent US peer-reviewed estimate of surgical backlog or wait time attributable to scheduling friction (as opposed to capacity limits).

---

## 3. What KPIs matter, how are they computed, and what are typical benchmarks?

### Takeaway
The core leadership KPIs are block utilization (ideally adjusted, i.e. counting turnover), prime-time utilization, released-time pickup or fill rate, first-case on-time starts, turnover time, same-day cancellation rate and cases per OR. Common targets are 70% initially and 75–80% long term for block utilization, and 80% for prime time. Released-time fill rates of 34–50% are reported in vendor deployments. Public benchmark medians are mostly dated (2010–2012), and definitions vary a lot, so any metric used in the prototype should state its definition.

### Cited Findings
**Block and prime-time utilization**
- Targets: start with a 70% block utilization goal and move toward 75–80%. Set a prime-time utilization goal of 80%, with prime time typically 7:30 am–3:30 pm, Mon–Fri — [Impact Advisors [C], undated (~2020s)](https://impact-advisors.com/article/surgical-block-utilization)
- In the McKesson OR Benchmarks Collaborative (Jan–Apr 2010 data), about 79–80% of available time was blocked. Prime-time (7a–3p) utilization figures of 75.3%, 93.9% and 100% appear for different (unlabeled) percentile columns — [OR Manager, Jan 2012 [T]](https://www.ormanager.com/wp-content/uploads/2012/01/0112_ORM_5.Benchmark_r.pdf)
- **Raw vs adjusted utilization:** raw counts procedure (in-room) time only. Adjusted adds setup and cleanup (turnover) time and is preferred in practice. Example: a tonsillectomy surgeon with 15-minute setup and cleanup gets 50% raw block utilization. A neurosurgeon doing one long case gets 100%. Both get 100% adjusted — [OR Manager Vol 20 No 11, citing Dexter, Mazzei, Blasco [T], ~2004](https://www.ormanager.com/wp-content/uploads/pdfx/001/ORMVol20No11blockTime.pdf)
- Utilization alone is a noisy basis for allocating block time to low-caseload surgeons. With 3 months of data, 95% CIs for average utilization were wider than 10 percentage points for surgeons averaging ≤83% raw utilization. Allocation should rest on OR efficiency instead — [Dexter et al., Anesthesiology 2003 [PR]](https://healthpolicy.fsi.stanford.edu/publications/operating_room_utilization_alone_is_not_an_accurate_metric_for_the_allocation_of_operating_room_block_time_to_individual_surgeons_with_low_caseloads); [Wachtel & Dexter, Anesth Analg 2008 [PR]](https://iro.uiowa.edu/esploro/outputs/journalArticle/Tactical-increases-in-operating-room-block/9983806391202771)

**Released time pickup / fill rate**
- Inova: 46% release fill rate, 20% increase in released OR minutes and a 3-point prime-time utilization gain in the first year (LeanTaaS iQueue) — [Becker's [T, vendor-linked], ~2024–25](https://www.beckershospitalreview.com/hospital-management-administration/inside-inovas-46-release-fill-rate-turning-open-or-time-into-more-cases/)
- Providence: backfill of released slots at 34% — [Becker's [T/V]](https://www.beckershospitalreview.com/finance/a-matter-of-or-minutes-health-systems-notch-big-financial-wins-with-ai.html)
- Qventus claims a "50% utilization of early released block" rate as a benchmark — [Qventus Perioperative Solution Brief [V], Oct 2024](https://qventus.com/wp-content/uploads/2024/10/Qventus_Solution-Brief_Perioperative.pdf)

**First-case on-time starts (FCOTS) and turnover**
- FCOTS median 64.3%, 90th percentile 88.3%, 95th percentile 91.4% (McKesson collaborative) — [OR Manager, Jan 2012 [T]](https://www.ormanager.com/wp-content/uploads/2012/01/0112_ORM_5.Benchmark_r.pdf). Dated.
- Definition example: on time if the case starts before or within 5 minutes of the scheduled start. Turnover usually 15–40 min — [LeanTaaS, "5 of the Most Important OR Performance Metrics" [V], undated](https://surgical-clinics.leantaas.com/5-of-the-most-important-operating-room-performance-metrics/)
- Median turnover of 32 minutes (setup plus cleanup) reported in a benchmarking survey — [Relias Media [T], date not retrieved, likely pre-2018](https://reliasmedia.com/articles/51280-here-are-study-results-how-do-you-measure-up)
- Room turnover (patient out to next patient in) was about 36 min at one academic center. Patient-to-patient turnover (end of surgery to end of next induction) was about 1 hour. Definitions are not interchangeable — [UCSF Open Proposals OR start/turnover document [A], 2024 project file; finding attribution from search excerpt](https://open-proposals.ucsf.edu/sites/default/files/chv/cw-projects-2024/1677821080/or_start_times_and_turnover_times.pdf)

**Same-day cancellation rate**
- 6.7% of 4,876 elective outpatient cases at Tulane were cancelled (2009 data) — [Advisory Board [T], 2012](https://www.advisory.com/daily-briefing/2012/05/09/same-day-surgery-cancellations-cost-hospitals-millions)
- A Maryland hospital QI project cites "up to 20%" of ambulatory cases cancelled nationwide. Its own site rate ranged 5.1%–9.7% (Aug–Dec 2022) — [UMaryland DNP project [A, not peer-reviewed], 2023](https://archive.hshsl.umaryland.edu/entities/publication/4bcf1e9a-0a93-4baa-b1de-3e7373cb6189)
- 15% of cases cancelled within 72 hours at one large system — [Qventus eBook [V], Feb 2026](https://www.qventus.com/wp-content/uploads/2026/02/Qventus-eBook-35MProblem-SurgicalLeakage-1.pdf)

**Case duration accuracy**: see Section 2 (32% within ±10% institutional baseline; 17% within ±20% for one EHR).

**Cases per OR per month**
- Qventus claims "up to 3+ cases added per OR per month" — [Qventus Solution Brief [V], Oct 2024](https://qventus.com/wp-content/uploads/2024/10/Qventus_Solution-Brief_Perioperative.pdf)

**Workflow KPIs (time-to-book, touches/case, lead time)**
- Qventus says HonorHealth schedulers "book OR time in seconds" with a digital booking interface (no baseline given) — [Qventus HonorHealth case study [V], Dec 2024](https://qventus.com/wp-content/uploads/2024/12/Qventus-HonorHealth-Case-Study-122024.pdf)
- 89% of OR requests submitted through Qventus at Banner were accepted — [Qventus Banner [V], ©2025](https://qventus.com/resources/customer-successes/banner-health)
- 40+ messages per case — [Becker's Spine [T/V]](https://www.beckersspine.com/orthopedic-spine-practices-improving-profits/7-common-causes-of-inefficient-orthopedic-and-spine-case-scheduling/)

### Inferences
- **Block utilization formula (common form):** (minutes of cases performed in the block, including turnover if adjusted) ÷ (allocated block minutes − minutes released by the deadline, depending on policy). Whether released minutes leave the denominator varies by institution. That rule decides whether surgeons have any incentive to release, so the prototype should state it explicitly.
- **Released-time pickup rate:** released minutes later filled by booked cases ÷ total released minutes. Reported values: Providence 34%, Inova 46%, Qventus target 50%.
- No public benchmark exists for time-to-book or touches per case, so a prototype can define its own: median minutes from request receipt to confirmed booking, number of messages or calls per case, and % of bookings complete at first submission. These are the most direct measures of a chat assistant's value.
- KPI hierarchy for the take-home: **leading/workflow** (time-to-book, touches, first-pass completeness, availability-search time) → **operational** (released-time pickup, prime-time utilization, duration accuracy, same-day cancellations from booking errors) → **financial** (incremental cases × contribution margin, idle staffed minutes × cost per minute).

### Gaps
- No current (2018–2026) public national median for block utilization, FCOTS or turnover was found. Benchmarks sit in subscription datasets (Vizient, AORN Syntegrity, Surgical Directions, LeanTaaS and Qventus customer data).
- No published US benchmark for scheduling lead time or touches per case was found.

---

## 4. What is the economic value (cost and revenue per OR minute, revenue share, value per case, cost of cancellation)?

### Takeaway
The newest peer-reviewed benchmark puts the cost of an OR minute at **$57.71 (California, FY2022)**, up from **$36–37 (FY2014)**. Revenue is **~$66/min** and charges **~$295/min**. Much of the folk "$36–$100+/min" range comes from mixing cost, revenue and charges. An added elective case is worth roughly **$4,000–5,000 in contribution margin** (consultant and vendor figures). Day-of cancellations cost **~$1,300–6,000 per case** in opportunity cost (2009 data). Recent claims put surgery at ~40% of hospital revenue and up to 65% of hospital margin.

### Cited Findings
**Cost / revenue per OR minute (peer-reviewed)**
- **$36–37 per OR minute** (California, FY2014; 302 hospitals). Of this, $20–21 is direct cost ($14 wages and benefits, $2.50–3.50 surgical supplies, ~$3 other). The remaining $14–16 is indirect cost — [Childers & Maggard-Gibbons, "Understanding Costs of Care in the Operating Room," JAMA Surgery 2018 [PR]](https://pubmed.ncbi.nlm.nih.gov/29490366/); [PMC full text](https://pmc.ncbi.nlm.nih.gov/articles/5875376); [MedicalResearch.com author interview [T], 2018](https://medicalresearch.com/labor-costs-account-for-largest-percentage-of-operating-room-expenses/)
- **$57.71 per OR minute (SD $24.09) in FY2022**, up 54% from FY2014 (5.24%/yr; 95% CI 4.63–5.82%). Direct costs are 56.6% ($32.56), and wages and benefits are about two-thirds of direct cost. **Revenue $66.31/min (SD $31.30); charges $295.09/min (SD $148.23).** Sample: 278 California hospitals, FY2014–2022. The authors call earlier estimates likely obsolete after COVID-19, inflation and consolidation — [Ashrafi, Maggard-Gibbons, Childers, "Costs, Charges, and Revenue of Hospital Operating Rooms in California," JAMA Surgery 2026, DOI 10.1001/jamasurg.2026.2355 [PR]](https://www.citedrive.com/en/discovery/costs-charges-and-revenue-of-hospital-operating-rooms-in-california/)

**OR share of hospital revenue / margin**
- ORs generate "an estimated 40% of hospital revenue" — [UChicago Booth Healthcare Management Analytics Lab project page [A], undated](https://hdsi.uchicago.edu/project/a-strategic-plan-for-optimizing-the-surgical-case-mix/)
- The OR accounts for "up to 65% of hospital profit margin" — [Becker's Hospital Review citing Surgical Directions [T/C], 2020](https://www.beckershospitalreview.com/strategy/how-to-rebuild-surgical-revenue-after-covid-19-even-if-you-just-lost-60-of-your-or-volume.html)

**Value per added case**
- Average contribution margin for an elective outpatient procedure: **$4,090/case** (Surgical Directions proprietary benchmark) — [Becker's [T/C], 2020](https://www.beckershospitalreview.com/strategy/how-to-rebuild-surgical-revenue-after-covid-19-even-if-you-just-lost-60-of-your-or-volume.html)
- Qventus uses an assumed **$5,000 contribution margin per case** — [Qventus eBook [V], Feb 2026](https://www.qventus.com/wp-content/uploads/2026/02/Qventus-eBook-35MProblem-SurgicalLeakage-1.pdf)
- Midwest AMC (Qventus): **391 cases added per month** on average and **$18.3M annualized contribution margin**. 39 hrs/month of block time released through nudges — [Qventus Midwest AMC case study [V], Jun 2025](https://www.qventus.com/wp-content/uploads/2025/06/Qventus-Midwest-AMC-CaseStudy.pdf)
- Case mix matters: in one Stanford analysis of 2,848 elective cases, contribution margin per OR hour was negative for 26% of cases — [Stanford Health Care publication [PR?], date not retrieved; attribution from search excerpt](https://stanfordhealthcare.org/publications/307/307429.html)

**Cost of a day-of-surgery cancellation**
- Tulane (2009 data): 327 of 4,876 elective outpatient cases cancelled (6.7%), costing nearly $1M, mostly in opportunity cost because slots could not be refilled. Cost per cancelled case by specialty: neurosurgery $5,962, urology $4,758, ENT $4,623, thoracic $4,208, ophthalmology $2,927, orthopedics $2,779, general surgery $1,965, pediatrics $1,325 — [Advisory Board [T], May 2012](https://www.advisory.com/daily-briefing/2012/05/09/same-day-surgery-cancellations-cost-hospitals-millions); [FierceHealthcare [T], 2012](https://www.fiercehealthcare.com/healthcare/hospitals-lose-millions-from-cancelled-surgeries)
- At one large system, 15% of cases were cancelled within 72 hours and about 50% were rescheduled within 90 days, putting **~$35M/yr** at risk at $5,000 CM per case — [Qventus eBook [V], Feb 2026](https://www.qventus.com/wp-content/uploads/2026/02/Qventus-eBook-35MProblem-SurgicalLeakage-1.pdf)

**Vendor ROI claims**
- HonorHealth (Qventus, perioperative): **224 incremental cases/month**, 210 additional robotic cases, **9.6x ROI**. Systemwide: $69M savings and 4% case-volume increase (includes inpatient products) — [Qventus HonorHealth case study [V], Dec 2024](https://qventus.com/wp-content/uploads/2024/12/Qventus-HonorHealth-Case-Study-122024.pdf); [2025 version](https://www.qventus.com/wp-content/uploads/2025/07/Qventus-Honor-Heath-Case-Study-2025.pdf)
- Banner Health (Qventus): **369 hours/month** of block released early, **+6.3% prime-time utilization**, 13 robotic cases/month added, **7x ROI**. "Results after the first six months have far exceeded our expectations" — [Qventus [V], ©2025](https://qventus.com/resources/customer-successes/banner-health)
- Qventus claims breakeven within 3 months of go-live — [Qventus Solution Brief [V], Oct 2024](https://qventus.com/wp-content/uploads/2024/10/Qventus_Solution-Brief_Perioperative.pdf)
- LeanTaaS iQueue: MultiCare +12.4% prime-time utilization — [LeanTaaS blog [V]](https://leantaas.com/blog/beyond-surgical-block-time-utilization-a-holistic-approach-to-optimizing-the-or/). Lee Health: surgeons released 840,000 OR minutes, alongside +6% case volume and +5% staffed-room utilization — [purpose.jobs/LeanTaaS blog [V]](https://www.purpose.jobs/blog/3-ways-leantaas-helps-clinicians)

### Inferences
- **The "$36–$100+/min" range** mixes measures: $36–37 is FY2014 cost, $57.71 FY2022 cost, $66 FY2022 revenue, $295 charges. Quote cost per minute for waste and revenue or contribution margin per case for growth. Never quote charges as value.
- **Sanity check on vendor math:** $18.3M ÷ (391 × 12 cases) ≈ $3,900 per added case, consistent with the $4,090 Surgical Directions benchmark.
- **Illustrative model** (assumptions stated; for the take-home's value slide):
  - A 20-OR hospital × 480 prime-time min/day × 250 days = 2.4M prime-time minutes/yr. A 1-point prime-time utilization gain ≈ 24,000 min ≈ **$1.4M of staffed cost put to productive use** ($57.71/min) or ≈ **$1.6M revenue** ($66.31/min).
  - +1 case per OR per month = 240 cases/yr × $4,090–5,000 CM ≈ **$1.0–1.2M/yr**. At Qventus's claimed "3+ cases/OR/month," ≈ $2.9–3.6M/yr (vendor-claim-based).
  - Released-time fill: Banner's 369 released hours/month × the 46% fill rate Inova reported ≈ 170 hrs/month refilled. Those are different systems, so the combination is illustrative only.
  - Cancellations: if 1 point of same-day cancellations (on 10,000 cases/yr = 100 cases) is booking-error-driven and avoidable, at $2,000–4,000 opportunity cost each (Tulane range, 2009 dollars) that is ≈ $0.2–0.4M/yr.
- Scheduler labor savings are likely small next to OR-minute value. Faster booking matters mainly because it fills released time sooner and with better-fit cases.

### Gaps
- The commonly cited "$100+/min" figure was not traced to a primary 2018–2026 source.
- One search excerpt cited a national average of $46.04/min, and an unnamed review cited $5,000–8,000 per cancelled case and $10–20 per wasted minute. Their primary sources could not be verified, so they are excluded from findings.
- No US peer-reviewed cancellation-cost study from 2018–2026 was found. Tulane (2009 data) remains the most-cited.
- No current, source-verified figure for the commonly cited "OR = 60–70% of hospital revenue." Verified figures are ~40% of revenue (UChicago) and up to 65% of margin (Becker's/Surgical Directions 2020).
- No 2018–2026 US source was found for OR overtime or staffing cost per overtime hour.

---

## 5. What evidence exists on scheduler time per booking, and on the impact of digital/automated scheduling?

### Takeaway
No peer-reviewed US time-and-motion study of OR case booking time was found. Evidence that digital or automated scheduling helps comes almost entirely from vendor case studies (Qventus, LeanTaaS): +3 to +12 points of prime-time utilization, 34–50% release fill rates, and hundreds of cases added per month at large systems. Peer-reviewed evidence is stronger for one sub-problem, ML duration prediction, where gains are modest (about +7 points of cases within ±10%). Measuring time-to-book and touches per case in a prototype pilot would fill a real gap.

### Cited Findings
- **Booking time:** the only figures are qualitative: "book OR time in seconds" — [Qventus HonorHealth [V], Dec 2024](https://qventus.com/wp-content/uploads/2024/12/Qventus-HonorHealth-Case-Study-122024.pdf); "with just a few clicks" — [Qventus Banner [V], ©2025](https://qventus.com/resources/customer-successes/banner-health); "less time spent scheduling" — [HonorHealth online form [H], 2021](https://www.honorhealth.com/sites/default/files/2021-09/scheduling-overview.pdf)
- **Coordination load:** 40+ messages per case — [Becker's Spine [T/V]](https://www.beckersspine.com/orthopedic-spine-practices-improving-profits/7-common-causes-of-inefficient-orthopedic-and-spine-case-scheduling/); "hours tracking changes across emails, spreadsheets, and phone calls" — [LeanTaaS-associated blog [V]](https://www.purpose.jobs/blog/3-ways-leantaas-helps-clinicians)
- **Digital intake:** required-field digital forms replaced faxed paper forms that were often incomplete. An Illinois ASC stopped phone requests entirely — [Becker's ASC [T]](https://www.beckershospitalreview.com/asc-turnarounds/8-points-about-scheduling-cases-in-an-asc.html); [LeanTaaS [V]](https://surgical-clinics.leantaas.com/?p=3084)
- **Automated block release and outreach (vendor):** Banner +6.3% prime time, 369 hrs/month released early, 89% of requests accepted [V, ©2025]. HonorHealth 224 cases/month added, 9.6x ROI [V, Dec 2024]. Midwest AMC 391 cases/month, $18.3M CM; it had previously used LeanTaaS iQueue without desired results [V, Jun 2025]. Inova 46% fill rate, +3 points prime time [T/V]. Providence −30% unused/unreleased block, 34% backfill [T/V]. MultiCare +12.4% prime time [V] — sources as cited in §4.
- **ML case duration (peer-reviewed):** +7 points within ±10% (32%→39%) — [Bartek et al., JACS 2019 [PR]](https://pmc.ncbi.nlm.nih.gov/articles/PMC7077507). Deployed model: 11.2% fewer underpredictions vs schedulers — [MD Anderson [PR]](https://mdanderson.elsevierpure.com/en/publications/development-and-implementation-of-a-machine-learning-model-for-pr/). AI 48% vs EHR 17% within ±20% — [OR Manager [T], Dec 2024](https://ormanager.com/briefs/study-ai-improves-surgical-case-length-predictions)
- **Caution from OR-management science:** release timing matters less than correct allocation, and utilization is a noisy metric for low-volume surgeons — [Dexter et al. [PR], 2003–2008](https://healthpolicy.fsi.stanford.edu/publications/operating_room_utilization_alone_is_not_an_accurate_metric_for_the_allocation_of_operating_room_block_time_to_individual_surgeons_with_low_caseloads)

### Inferences
- The vendor results bundle several interventions: predictive release nudges, outreach, a digital booking UI and analytics. None isolates the effect of a conversational booking interface. A chat assistant's claim should rest on workflow metrics it can directly move (time-to-book, touches, first-pass completeness, time-to-fill released slots), with utilization and margin as downstream hypotheses.
- Suggested pilot measurement design for the take-home: baseline 2–4 weeks of coordinator bookings (timestamp request received → booking confirmed; count of outbound calls and messages per case; % of requests needing follow-up), then the same with the assistant. Track same-day cancellations and day-of changes attributed to booking errors as a lagging quality guardrail.
- Peer-reviewed duration-ML gains are modest, so the assistant should treat duration as a suggested default with variance shown, not a precise prediction.

### Gaps
- No peer-reviewed or independent (non-vendor) controlled study of digital OR booking or block-release tools on utilization or volume was found in this bounded search. All before/after figures are self-reported, uncontrolled and from vendor or partner sources.
- No source quantified minutes per booking, calls per booking, or scheduler FTEs per OR for US hospitals.
- Peer-reviewed AORN Journal or Anesthesia & Analgesia studies of electronic case-request systems may exist but did not surface in this bounded search.
