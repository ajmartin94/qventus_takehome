# AI/ML and Conversational-AI Techniques for an OR Scheduling Assistant

Research date: 2026-10-14. Scope: OR-domain ML (to inform stretch goals and "future work") and LLM-assistant engineering patterns (to inform the architecture of a 4-6 hour chat prototype that checks OR availability and books a case). Sources are dated where possible. Vendor-reported numbers are labeled as such.

## Q1. OR-domain ML: case duration, block release, demand, optimization, cancellation, released-time matching. What is realistic to stub in a prototype?

### Takeaway
ML case-duration models beat surgeon estimates and EHR historical averages, but only modestly: typically about 13-20% lower RMSE/MAE. One RCT showed a 16.5% MAE reduction and a 67% cut in patient wait time. Block-release prediction and released-time matching are mostly vendor territory, including Qventus's own products, and have little peer-reviewed evidence. Cancellation models reach AUCs of about 0.72-0.83 but have low PPV. OR scheduling optimization is a mature operations-research field (MIP, CP, heuristics; NP-hard). A prototype should stub all of these behind clean tool interfaces: historical medians plus rules plus greedy slot search. ML and optimization belong in "future work".

### Cited Findings

**Case duration prediction**
- Bartek et al. (2019) used data from more than 45,000 surgeries by 92 surgeons over 4 years and built specialty-level and surgeon-specific models. The share of cases predicted within ±10% rose from 32% with the institutional standard to 39% with the surgeon-specific ML model. Surgeon-specific models beat service-level models, and accuracy passed 50% for the top third of surgeons. — [UW Medicine newsroom](https://newsroom.uw.edu/news-releases/how-much-time-surgery-researchers-create-model); [EM-Consulte abstract](https://www.em-consulte.com/article/1320284/improving-operating-room-efficiency-machine-learni)
  - Citation note: the brief names this paper as *JAMA Surgery*, but search results place it in the *Journal of the American College of Surgeons* (2019). The UW press release gives the baseline as 30% (surgeon estimate) rather than 32%. — [UW Medicine newsroom](https://newsroom.uw.edu/news-releases/how-much-time-surgery-researchers-create-model)
  - The scoping review below reports Bartek's MAPE as 26% (ML) vs 30% (standard). — [Spence et al., BJS Open 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10630142/)
- **RCT evidence (Strömblad et al., JAMA Surgery 2021;156(4):315-321, Memorial Sloan Kettering):** colorectal and gynecology cases from Apr-Jun 2018 were randomized; 683 were analyzed (356 control, 327 ML). Results:
  - MAE fell from 59.3 to 49.5 min (−9.8 min, a 16.5% improvement, P=.03).
  - Wait time for the to-follow patient fell from 49.4 to 16.3 min (−67%).
  - Presurgical length of stay fell from 173.3 to 148.1 min.
  - Turnover time changed by only 1.5 min.
  - Limitations: single center, small arm. — [JAMA Surgery abstract](https://jamanetwork.com/journals/jamasurgery/article-abstract/2775620)
- **Scoping review (Spence et al., BJS Open, Nov 2023; searches to July 2023):** 14 studies, 11 from the USA, only 1 RCT.
  - Tree-based models (XGBoost, CatBoost, gradient boosting) were best in 9 of 14. Deep learning helped mainly in datasets with more than 50k records.
  - Reported gains vs standard: RMSE 43.4 vs 49.8 min (Ng 2017); RMSE 80.2 vs 100.4 (Zhao 2019); mean absolute difference 20.0 vs 27.0 min (Tuwatananurak 2019); CRPS 13.8 vs 37.0 min (Jiao 2022); RMSE about 38-39 vs 46.3 min (Miller 2022).
  - Common inputs: primary surgeon, historical average duration, procedure type, surgeon experience, scheduled duration, BMI, age, ASA, comorbidities, anesthesia type. Using more than about 1,500 variables gave no clear accuracy gain.
  - Only 1 study externally validated its model. Evidence quality was judged low.
  - Models predicted retrospectively or one day ahead, while real scheduling needs predictions **weeks** in advance.
  - Implementation barriers: data quality, EHR interoperability, accountability. — [Spence et al., BJS Open 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10630142/)
- **Systematic review (Bellini et al., J Med Syst, Feb 2024):** 22 studies (Feb 2019 - Sep 2023). AI had significant impact on case-duration prediction, PACU resource allocation and cancellation detection. XGBoost, random forest and neural networks were the effective methods. The review flags data access and privacy limitations. — [PMC10867065](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10867065/)
- A second PRISMA systematic review screened 608 records and included 21 studies, with similar conclusions: duration prediction, cancellation detection and PACU allocation. I could not confirm its publication date. — [PMC11929973](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11929973/)

**Block release / unused block prediction**
- Qventus (blog by David Atashroo, MD) says its models use historical EHR data to predict, up to about one month ahead, which blocks or partial blocks will go unused. When confidence is high, it nudges surgeons to release early. It argues that standard auto-release policies fire only a few days before the block, too late to backfill. These are vendor claims. — [Qventus blog](https://qventus.com/3-ways-machine-learning-can-optimize-your-operating-room-utilization/); [Qventus block utilization blog](https://www.qventus.com/resources/blog/block-time-utilization-in-operating-rooms-how-to-identify-areas-of-improvement-and-increase-utilization/)
- A secondary blog attributes a 30% case-length-estimate improvement (about 40 h/yr less wasted OR time) at the University of Arkansas for Medical Sciences to a vendor tool. I could not find the primary source, so treat it as unverified. — [Simbo.ai blog](https://www.simbo.ai/blog/?p=55427)
- The closest peer-reviewed work found is an ambulatory surgery center study. It predicted a composite outcome: the case finishes by block end and the patient leaves PACU by shift end. Ensemble ML was compared against logistic regression. — [PMC9172889](https://pmc.ncbi.nlm.nih.gov/articles/PMC9172889)

**Matching released time to waitlisted cases / surgeons**
- Qventus (June 2025 release) describes ML "personalized to surgeon preferences and behavior patterns" that matches open OR slots with the right surgeons, replacing first-come-first-served. It reports an average 11X ROI. These are vendor-reported figures. — [BusinessWire, Jun 17 2025](https://www.businesswire.com/news/home/20250617272367/en)

**Cancellation risk prediction**
- Day-of-surgery cancellation models report AUCs of roughly 0.72-0.83:
  - Urology, West China (RF): AUC 0.72. — [PMC7914093](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7914093/)
  - Urology with social-determinants data: AUC 0.80 (95% CI 0.70-0.89), sensitivity 81%, specificity 55% at a 0.4 cutoff. — [PMC12712017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12712017/)
  - Pediatric (Cincinnati Children's), gradient-boosted: AUC 0.781 and 0.740 at two campuses, and 0.725 and 0.735 when trained on one site and tested on the other. — [AHRQ R21 final report 2019](https://healthit.ahrq.gov/sites/default/files/docs/citation/r21hs024983-pratap-final-report-2019.pdf)
  - Orthopedics national gradient-boosted model: AUC 0.833. This is a conference abstract, not peer-reviewed. — [AAOS 2026 abstract](https://index.mirasmart.com/AAOS2026/PDFfiles/AAOS2026-003124.pdf)
- PPV problem: a 24-hour cancellation score (logistic regression) had AUC 0.79 in development and 0.73 in validation. At its cutoff, NPV was 0.96 but **PPV was only 0.21**. — [Mahidol repository](https://repository.li.mahidol.ac.th/items/62c8d49e-c07b-4f18-a65e-9d06b68100a0/full)

**Schedule optimization (operations research)**
- Classic and recent surveys:
  - Cardoen, Demeulemeester & Beliën (2010, *EJOR*) is the foundational literature review.
  - Samudra et al. (2016, *J Scheduling*).
  - A 2018 *J Comb Optim* survey classifies work by decision level, uncertainty, model and solution method. It finds mathematical programming and heuristics dominate.
  - A 2025 *Operational Research* review finds no single dominant research trend.
  - [J Comb Optim 2018](https://link.springer.com/10.1007/s10878-018-0322-6); [Operational Research 2025](https://ideas.repec.org/a/spr/operea/v25y2025i1d10.1007_s12351-024-00884-z.html); [Samudra et al. record](https://scholarhub.vn/publication/Scheduling-operating-rooms-achievements-challenges-and-pitfalls/6759d646-c137-4fbf-af67-d6797d91348c)
- Wang, Meskens & Duvivier (2015, *EJOR* 247:401-413) directly compare MIP and constraint programming (CP) for daily operating-theatre scheduling. Another MILP-vs-CP study on benchmark instances found MILP faster. Hybrid approaches combine them: CP inside branch-and-price, or ILP for small instances plus a genetic algorithm for large ones. OR scheduling is NP-hard, so exact methods are typically paired with heuristics. — [Wang et al. record](https://libsearch.um.ac.ir/fum/handle/fum/2084739?show=full); [SUNY MIP+CP paper](https://researchconnect.suny.edu/en/publications/using-mixed-integer-programming-and-constraint-programming-for-op/); [UNAB record](https://repositorio.unab.cl/items/452bb05b-5123-44cb-9b15-b8cbd33aec6e/full); [UTS comprehensive review](https://opus.lib.uts.edu.au/handle/10453/145725)

### Inferences

**Prototype vs future work**

| Technique | 4-6 h prototype (realistic) | Future-work section |
|---|---|---|
| Case duration | `estimate_duration(cpt, surgeon_id)` returns the surgeon+procedure historical median (P50) and P80 from a synthetic CSV, falling back to the procedure-level median, and shows the surgeon's requested minutes side by side. Flag when the request is below P50 by more than X%. | Gradient-boosted (XGBoost/LightGBM) quantile regression on surgeon, procedure, patient (ASA/BMI), anesthesia type. Cite Strömblad's RCT as the evidence bar. Note the "weeks-ahead horizon" and external-validation gaps from Spence 2023. |
| Block release | Rule-based `release_candidates()`: blocks less than N% booked at T-14 days, or past the policy auto-release threshold (from the RAG policy doc). | ML predicting unused block about 30 days out, with nudges to surgeons. This is Qventus's own product thesis, so it is worth naming explicitly. |
| Released-time to waitlist matching | Greedy filter: waitlisted cases whose estimated duration plus turnover fits the gap, whose surgeon is credentialed or has privileges in the room, and whose equipment matches. Rank by wait time or priority. | Learned ranking from surgeon preference and behavior, or a CP/MIP assignment. |
| Slot search / optimization | Deterministic first-fit or best-fit search over room-day gaps with hard constraints: room capability (e.g., robot), surgeon availability, duration+turnover ≤ gap, block ownership. Return the top 3 options. | MIP/CP formulation (e.g., OR-Tools CP-SAT, my suggestion, not sourced) minimizing overtime and idle time under duration uncertainty, using stochastic durations from the duration model. |
| Cancellation risk | A rule-based risk flag (e.g., missing pre-op clearance, prior no-shows in synthetic data). Surface it as advisory only. | Gradient-boosted classifier. Discuss low PPV and cross-site AUC drop, and use it to prioritize outreach rather than auto-bump cases. |
| Demand forecasting | Out of scope. At most, a static "utilization by service" summary. | Time-series forecasting of case volume by service for block allocation (see Gaps). |

- The strongest grounded narrative for a Qventus reviewer: ML improves estimates only incrementally, about 15-20%, so the assistant should **show ranges and the data provenance** of every estimate ("historical median of 23 cases for Dr. X") rather than present a point prediction as truth.
- All ML components should sit behind the same tool interfaces the LLM calls. That makes them swappable stubs, which demonstrates the "separation of logic and integrations" grading criterion.

### Gaps
- **Demand forecasting:** no sources retrieved specifically on surgical demand forecasting for block allocation. I found no peer-reviewed accuracy figures.
- **Block-release prediction:** no peer-reviewed study with accuracy metrics (e.g., AUC for "block will go unused") was found. The evidence is vendor content only.
- **Waitlist matching:** no peer-reviewed evaluation of ML matching released time to waitlisted cases was found.
- **Bartek full text:** the full text (journal volume/pages, MAE in minutes) was not retrieved. Only the press release, the abstract page and the Spence review summary were.
- **MIP vs CP:** I did not retrieve quantitative results (solve times, objective gaps) from Wang et al. 2015.

## Q2. Conversational AI patterns for transactional workflows (intent + slot filling, state machines/graphs, confirmation, clarification, guardrails, deterministic validation, escalation)

### Takeaway
Production-grade transactional assistants converge on one design. The LLM handles **understanding (intent + slot extraction) and phrasing**. A **deterministic state machine/flow** owns business logic, validation and side effects. Commits happen only after an explicit confirmation checkpoint. Several sources point the same way:
- Rasa CALM (LLM emits commands, flows execute).
- Dialogflow CX (pages and forms, escalating reprompts).
- LangGraph `interrupt()` (approve/reject before tool execution).
- Anthropic's "workflows before agents" guidance.

Schema-constrained outputs guarantee shape, not truth, so entity values must still be validated in code against directories and lookup tables.

### Cited Findings

**General architecture guidance**
- Anthropic, "Building effective agents" (Dec 19, 2024):
  - Distinguishes **workflows** (LLMs and tools orchestrated through predefined code paths) from **agents** (LLMs dynamically directing their own process).
  - Recommends finding the simplest solution and adding complexity only when needed.
  - Names five patterns: prompt chaining (with programmatic checks between steps), routing (classify, then specialized prompt), parallelization (sectioning/voting), orchestrator-workers, and evaluator-optimizer.
  - Advises starting with LLM APIs directly. Frameworks can obscure prompts and responses and tempt unnecessary complexity.
  - Advises investing in the "agent-computer interface": clear tool descriptions, examples, edge cases and boundaries between similar tools.
  - Advises **poka-yoke** tool arguments that make mistakes hard. Its example is requiring absolute file paths.
  - Recommends human checkpoints, stopping conditions (max iterations) and sandboxed testing.
  - Notes that customer support suits agents because success is measurable by resolution.
  - [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)

**Flows / state machines**
- **Rasa CALM:**
  - An LLM "command generator" reads each message in context and emits internal commands: start, stop or resume a flow; trigger a pattern flow; call a custom action; answer from the knowledge base via RAG.
  - A dialogue manager executes those commands deterministically. **Business logic lives in flows, not in the LLM**, and the LLM does not decide steps on the fly.
  - Built-in "conversation patterns" handle topic changes, corrections and clarifications.
  - Rasa argues ReAct-style agents make inconsistent decisions when business logic is embedded in prompts.
  - An optional rephraser makes templated responses fluent.
  - Related paper: arXiv 2402.12234 (2024).
  - [Rasa docs](https://rasa.com/docs/learn/concepts/calm/)
- **Dialogflow CX forms:**
  - Each form parameter has a "fill behavior": an initial prompt fulfillment plus reprompt event handlers.
  - Handled events are `sys.no-match-1..6`, `sys.no-match-default`, `sys.no-input-1..6`, `sys.no-input-default` and `sys.invalid-parameter`. Each successive failure can trigger a different reprompt or **transition to another page or flow**, which is an escalation path.
  - Fulfillments can call webhooks, for example to load data from a database.
  - [Google Cloud Dialogflow CX FillBehavior reference](https://docs.cloud.google.com/ruby/docs/reference/google-cloud-dialogflow-cx-v3/latest/Google-Cloud-Dialogflow-CX-V3-Form-Parameter-FillBehavior)
- **LangGraph human-in-the-loop (`interrupt()`):**
  - Calling `interrupt(payload)` inside a node pauses the graph, persists state via a **checkpointer** and requires a `thread_id`. The caller resumes with `Command(resume=value)`, which becomes `interrupt()`'s return value.
  - Documented patterns:
    - approve/reject before a critical action, routing with `Command(goto=...)`;
    - review-and-edit of generated content;
    - interrupts inside tools, so every call to a sensitive tool requires approval and the reviewer can edit arguments;
    - input-validation loops: one interrupt per node run, re-prompt stored in state, loop back via a conditional edge (no `while True` inside a node).
  - Caveats:
    - On resume, **the node re-executes from the start**, so side effects before `interrupt()` must be idempotent or moved after it or into a separate node.
    - Don't wrap `interrupt()` in a bare try/except.
    - Interrupts are matched to resume values by position.
    - `interrupt_before`/`interrupt_after` are for debugging only.
  - `response_schema` validation of resume values requires `langgraph>=1.2.12`.
  - [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/interrupts)

**Structured outputs / strict tool use (slot extraction)**
- Claude structured outputs:
  - **What it is:** JSON outputs via `output_config.format` with `type: "json_schema"`, and strict tool use via `strict: true`. The API compiles the schema into a grammar that constrains decoding ("schema-compliant by construction"). It is GA, with no beta header for `output_config.format`; the older `output_format` is deprecated and needs the `structured-outputs-2025-11-13` header.
  - **Unsupported schema features:** numeric `minimum`/`maximum`, string `minLength`/`maxLength`, recursive schemas and regex lookarounds.
  - **Limits:** 20 strict tools per request, 24 optional parameters and 16 union-type parameters across all strict schemas.
  - **Caching and latency:** first-request grammar compilation latency, with compiled grammars cached for 24 h.
  - **Not guaranteed:** enum casing; refusals and `max_tokens` truncation can break the schema.
  - **The guarantee covers schema compliance, not factual accuracy.** A value can match its type and still be wrong.
  - [Claude docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

**Policy-following failures of tool-calling agents (why deterministic guards matter)**
- In τ-bench (Sierra, 2024: retail and airline booking/modification domains with policy docs):
  - GPT-4o succeeded on fewer than 50% of tasks, and **pass^8 fell below 25%** in retail.
  - Main failure modes: inconsistent rule-following, long-horizon planning, and focusing on the relevant information when facts conflict.
  - "Function-calling agents often fail to follow the rules in policy documents."
  - [Sierra blog](https://sierra.ai/blog/benchmarking-ai-agents); [arXiv 2406.12045](https://arxiv.org/pdf/2406.12045)

### Inferences

**Recommended prototype architecture (synthesized from the above)**

1. **State graph** (LangGraph `StateGraph` or a plain Python FSM) with explicit states: `GREETING/ROUTE → COLLECT_SLOTS → VALIDATE → SEARCH_AVAILABILITY → PRESENT_OPTIONS → CONFIRM → COMMIT → DONE`, plus side states `CLARIFY`, `POLICY_QA` (RAG), `ESCALATE`.
   - Intent routing uses Anthropic's "routing" pattern.
   - Intents: `check_availability`, `book_case`, `policy_question`, `modify/cancel` (stretch), `out_of_scope`.
2. **LLM as NLU only:** one strict-schema extraction call per turn returns `{intent, slots: {surgeon_name, procedure_text/cpt, date_window, duration_min, room_requirements, patient_ref}, corrections, confidence/ambiguities}`.
   - This mirrors CALM's "LLM emits commands" idea.
   - Keep business rules out of the prompt.
3. **Deterministic validators** (pure functions, unit-testable):
   - surgeon directory fuzzy match (return candidates if more than 1, so the LLM can ask "Dr. Lee in Ortho or Dr. Lee in Urology?");
   - CPT lookup table (code ↔ description, default duration, equipment);
   - date normalization to ISO;
   - **range checks in code**, since Claude strict schemas can't enforce numeric min/max (e.g., duration 15-720 min);
   - block ownership and policy checks.
   - Invalid → a `CLARIFY` state with a targeted question.
4. **Poka-yoke tool signatures:**
   - `book_case` accepts only `surgeon_id`, `cpt_code`, `room_id` and `slot_id` returned by earlier lookup/search tools, never free text. It also takes an **idempotency key** (the LangGraph re-execution caveat).
   - `search_availability` returns opaque `slot_id`s.
5. **Confirmation-before-commit:**
   - The `CONFIRM` node renders a deterministic summary (template, not LLM-generated values) and calls `interrupt()`. Only an explicit "yes" routes to `COMMIT`; "change X" routes back to `COLLECT_SLOTS`.
   - Re-check availability inside `COMMIT` to avoid races.
6. **Escalation:** a reprompt counter per slot, mirroring Dialogflow's `no-match-N`. After 2-3 failures, policy conflicts or out-of-scope clinical questions, go to `ESCALATE` with a handoff summary (structured case draft plus transcript) for a human scheduler.
7. **Guardrails:**
   - Scope restriction (no clinical advice).
   - PHI minimization (use patient MRN placeholders in synthetic data).
   - Output check that every slot value in the confirmation came from validated state, not from LLM text.
   - Max-turn / max-tool-call stopping conditions.

**Prompt modularity:** separate prompt files for the router/extractor, clarification question generation, the policy-QA (RAG) answerer, and the response rephraser (CALM-style). Version them in the repo so regression evals can pin prompt versions.

**Prototype vs future:**
- Prototype: the graph, a single extractor, validators, the confirmation interrupt, an escalation stub and an in-memory checkpointer.
- Future: persistent checkpointer (Postgres), modify/cancel flows, multi-case batch booking, voice channel, EHR write-back (e.g., Epic/HL7 scheduling APIs, not researched here).

### Gaps
- **OpenAI Structured Outputs:** the announcement page returned 403, so OpenAI's schema-adherence eval figures are not verified here. (Recollection: 100% on their complex-schema eval vs <40% for gpt-4-0613, Aug 2024. Verify before citing.)
- **Dialogflow CX semantics:** the main docs page (pages as states, `$page.params.status = "FINAL"` completion condition, webhook-driven `sys.invalid-parameter`) returned 404/redirect issues. Only the API reference for FillBehavior was confirmed.
- **Rasa CALM benchmarks:** no quantitative comparison of CALM-style vs ReAct-style agents on task success was retrieved; Rasa's claim is qualitative.
- **Escalation thresholds:** no sources on optimal reprompt counts or escalation thresholds for healthcare scheduling bots.

## Q3. RAG for scheduling policies (block release rules, procedure requirements): chunking, embeddings, hybrid search, citations

### Takeaway
For a small policy corpus (a few documents), Anthropic's own guidance says to skip RAG and put the whole corpus in a cached prompt; the threshold is under about 200k tokens. Because the grading rubric explicitly values RAG, the defensible move is a small **hybrid (BM25 + embedding) retriever over section-chunked policies with metadata and citations**. Contextual Retrieval and reranking are a documented, measurable upgrade path.

### Cited Findings
- **Anthropic Contextual Retrieval (Sep 19, 2024):**
  - Prepend a short LLM-generated, chunk-specific context to each chunk before both embedding and BM25 indexing.
  - Results, measured as top-20 retrieval failure rate from a 5.7% baseline:
    - contextual embeddings: −35% (to 3.7%);
    - contextual embeddings + contextual BM25 (i.e., hybrid): **−49%** (to 2.9%);
    - plus reranking: **−67%** (to 1.9%).
  - Chunk size, boundaries and overlap matter. Gemini and Voyage embeddings performed best in their tests. Passing 20 chunks beat 5 or 10. Domain-specific contextualizer prompts may help. Always run evals on your own data.
  - **For knowledge bases under 200k tokens (about 500 pages), skip RAG and include everything in the prompt.** Prompt caching cuts latency by more than 2x and cost by up to 90%.
  - [Anthropic](https://www.anthropic.com/news/contextual-retrieval)
- Rasa CALM routes knowledge questions to a RAG "answer from knowledge base" command, separate from transactional flows. This shows policy QA as its own route rather than mixed into booking logic. — [Rasa docs](https://rasa.com/docs/learn/concepts/calm/)
- τ-bench shows tool-calling agents often fail to follow rules written in policy documents. This argues for turning hard policies (e.g., the block release deadline) into **code-level checks**, and using RAG for explanation and soft guidance. — [Sierra blog](https://sierra.ai/blog/benchmarking-ai-agents)

### Inferences

**Prototype design**
- Write 3-5 synthetic policy markdown docs: block release policy (auto-release at T-72h/T-7d by service), add-on/urgent case policy, robot room eligibility, procedure equipment/implant vendor requirements, pre-op clearance requirements.
- Chunk by heading/section, one rule per chunk. Store metadata `{doc_id, section_id, title, effective_date, service_line}`.
- Index with BM25 (`rank_bm25`) plus embeddings (any small embedding model; local `sentence-transformers` avoids API keys) in an in-memory store (numpy/FAISS/Chroma). Combine with reciprocal rank fusion (my suggestion; RRF itself was not sourced here).
- The answer prompt requires citing `[doc_id §section_id]` for each claim. Answer "not found in policy" when the top score is below threshold.

**Dual use of policies**
- Hard rules (e.g., "robotic cases only in OR 5-7", "block auto-releases 72h prior") are encoded as validators in code and used for decisions.
- The same rules exist as RAG chunks so the assistant can **explain** a decision with a citation.
- This dual representation is a strong talking point for "separation of logic and integrations".

**Future work**
- Contextual Retrieval preprocessing, a reranker, policy versioning by effective date, an eval set of policy Q→expected section pairs (recall@k), and document ingestion from PDFs.

### Gaps
- **Citations APIs:** I did not retrieve docs for Anthropic's Citations API or OpenAI file search citations, so native-citation features are not verified here.
- **Embedding benchmarks:** no current (2025-2026) embedding-model benchmark comparisons (e.g., MTEB leaderboard) were retrieved.
- **Clinical RAG evidence:** no healthcare-policy-specific RAG evaluations were retrieved.

## Q4. Evaluation and monitoring for task-oriented LLM agents

### Takeaway
The state of the art for transactional agents is **simulated-user, end-state-checked evaluation with repeated trials** (τ-bench pass^k, τ²-bench dual-control). Success is judged by the final database state plus natural-language assertions, and reliability across k runs is reported, not just a single-run success. Observability is converging on OpenTelemetry GenAI conventions, which Langfuse ingests natively. A prototype can implement a scaled-down τ-bench-style harness in an hour or two.

### Cited Findings
- **τ-bench (Sierra, 2024):** an LLM-simulated user interacts with the agent. The task is scored by comparing the **final database state** to the expected state. **pass^k** is the probability that the agent succeeds in **all** k independent trials, a reliability metric stricter than pass@k. pass^k dropped sharply with k for all 12 agents tested, e.g., GPT-4o's pass^8 was below 25% in retail. — [arXiv 2406.12045](https://arxiv.org/pdf/2406.12045); [Sierra blog](https://sierra.ai/blog/benchmarking-ai-agents)
- **τ²-bench (Barres et al., 2025, arXiv 2506.07982):**
  - Adds a telecom domain with **dual control**: the user has tools the agent can't call.
  - Tasks are either "policy-violation" (the agent must refuse) or "mutation" (the agent must act correctly).
  - Success requires both the final DB state and NL assertions to hold.
  - A No-User ablation separates reasoning errors from communication and collaboration errors.
  - Amazon's τ²-Bench-Verified fixed tasks whose expected actions didn't align with the policies or DB. **Eval sets themselves need auditing.**
  - One source says the framework was rebranded τ³-bench (v1.0.0, March 2026). Unconfirmed.
  - [arXiv 2506.07982](https://arxiv.org/pdf/2506.07982); [tau2-bench-verified](https://github.com/amazon-agi/tau2-bench-verified); [Layer3 explainer, Sep 2026](https://www.layer3labs.io/guides/tau-bench-explained)
- **Simulator noise:** commentary notes the user simulator is stochastic, so pass^k variance mixes agent and simulator inconsistency. — [beancount.io research log, Jun 2026](https://beancount.io/bean-labs/research-logs/2026/06/12/tau-bench-tool-agent-user-interaction-real-world-domains)
- **CareConnect (healthcare logistics agent, arXiv 2607.05055, Jul 2026):**
  - Evaluated on a **680-scenario** benchmark covering end-to-end workflows, multi-turn interactions and edge cases.
  - Reported 91.8% task completion, a 2.2 s median latency, **96.0% safety compliance** on a safety-critical subset and $0.0324 per appointment.
  - A useful template for metric categories (task completion, safety compliance, latency, cost).
  - [arXiv 2607.05055](https://arxiv.org/pdf/2607.05055)
- **Observability:**
  - Langfuse renders spans that carry OpenTelemetry `gen_ai.*` attributes as LLM generations, with model, token and cost data. `session.id`/`user.id` attributes group conversations. Its tracing is OTel-based to reduce lock-in. — [Langfuse docs](https://langfuse.com/resources/engineering/opentelemetry-languages)
  - Secondary guides describe GenAI agent spans (`invoke_agent`, `create_agent`) and attributes like `gen_ai.request.model` and `gen_ai.agent.name`. Spec stability varies by version. Verify against opentelemetry.io. — [traeai guide](https://learn.traeai.com/t/ai-engineering/phases/14-agent-engineering/23-otel-genai-conventions.html)
- Anthropic recommends extensive testing in sandboxed environments, and measuring success by resolution where possible. — [Anthropic](https://www.anthropic.com/engineering/building-effective-agents)

### Inferences

**Prototype eval harness (fits in 1-2 h)**
- **Scenarios:** 15-25 YAML scenarios, each with a user persona/script, ground-truth slots, the expected final booking-DB state (or "no booking + escalation" / "refusal"), and the expected tool-call sequence.
- **Categories (mirroring τ²-bench task types):**
  - happy path;
  - missing slots (multi-turn clarification);
  - ambiguous surgeon name;
  - invalid CPT;
  - user correction mid-flow;
  - policy violation (book into a released or other-service block), where the expected outcome is refusal or escalation;
  - no availability (offer alternatives);
  - user declines at confirmation (no commit);
  - out-of-scope clinical question.
- **Metrics:**
  - (a) task success = final DB state matches;
  - (b) **slot accuracy** per field (extracted vs gold);
  - (c) tool-call accuracy (correct tool + args; no `book_case` without a prior confirmation event);
  - (d) turns-to-completion;
  - (e) **pass^k** with k=3-5 at temperature > 0;
  - (f) safety: zero commits without confirmation, zero bookings violating hard rules. This should be a hard gate at 100%.
- **User simulator:** an LLM with the scenario persona, or scripted turns for determinism in CI. Keep both: scripted for regression, simulated for robustness.
- **LLM-as-judge:** only for soft qualities (clarifying-question quality, tone, citation faithfulness for policy QA). Use rubric prompts with a pass/fail output, never as the arbiter of booking correctness, which is checked deterministically.
- **Regression:** run on every prompt/version change (pytest), and store results per prompt version.
- **Observability:**
  - Log a structured trace per turn: state transition, extracted slots, validator results, tool calls and latency/tokens. Tag each trace with a session ID.
  - Langfuse/OTel export is a cheap stretch (a decorator/callback). LangSmith is the LangGraph-native alternative.
  - Human feedback: a thumbs-up/down plus a "scheduler corrected X" event feeding back into the eval set.
- **Future work:** larger synthetic suites generated from templates, an audit of eval-set labels (the τ²-Verified lesson), online monitoring dashboards (escalation rate, confirmation-reject rate, slot correction rate) and drift alerts.

### Gaps
- **LangSmith:** docs were not retrieved, so specific LangSmith features (datasets, online evaluators) are not verified here.
- **LLM-as-judge reliability:** no sources were retrieved on LLM-as-judge biases (position or verbosity bias, agreement with humans) for task-oriented dialogue.
- **OTel GenAI spec:** the official spec version and stability status were not confirmed from opentelemetry.io directly.
- **Healthcare benchmarks:** no healthcare-scheduling-specific public benchmark analogous to τ-bench was found, apart from CareConnect's self-built set.

## Q5. Published examples / case studies of LLM agents for healthcare scheduling or operations (2023-2026), including failures and risks

### Takeaway
Peer-reviewed evidence of LLM agents doing OR booking in live use is essentially absent. The closest academic analog is the CareConnect appointment-logistics agent, a July 2026 preprint evaluated on a self-built benchmark, which uses the same architecture recommended above (function calling + RAG + layered deterministic guardrails). Qventus publicly markets "AI teammates" for surgical scheduling, but its outcome numbers are vendor-reported. General agent benchmarks document inconsistent policy-following, the main risk for booking workflows.

### Cited Findings
- **CareConnect (American University of Beirut; arXiv 2607.05055, Jul 2026):**
  - A "safety-first" conversational agent for healthcare logistics combining LLM function calling, RAG and **layered deterministic safety guardrails**.
  - Eight tools: booking, modification, cancellation and facility lookup. Strict scope constraints prohibit medical advice or diagnosis.
  - Results: 91.8% task completion, 96.0% safety compliance and $0.0324 per appointment, on the authors' own 680-scenario benchmark (not a live deployment).
  - Code: github.com/Hadi-Hsn/CareConnect.
  - [arXiv 2607.05055](https://arxiv.org/pdf/2607.05055)
- **Qventus surgical AI products (vendor-reported, 2025):**
  - "Clinic Scheduler Assistant" works inside surgeon-clinic EMRs; one health system books cases with a **22-minute median turnaround** (May 2025).
  - "Document Assistant" digitizes, categorizes and summarizes perioperative faxes, saving about 60 h of OR-scheduler time per month.
  - "Robotics Assistant" claims more than 10% incremental robotic volume.
  - ML matches open OR slots to surgeons (June 2025).
  - West Tennessee Healthcare reported 4x annualized ROI and 61 added cases in its first 100 days.
  - Jan 2025: $105M Series D led by KKR.
  - [BusinessWire May 2025](https://www.businesswire.com/news/home/20250515873225/en); [BusinessWire Jun 2025](https://www.businesswire.com/news/home/20250617272367/en); [Qventus blog](https://www.qventus.com/resources/blog/how-qventus-ai-teammates-drive-strategic-surgical-growth-and-transform-the-perioperative-care-journey/); [Qventus ViVE 2025](https://www.qventus.com/resources/resource-library/qventus-at-vive-2025/)
- **Allina Health** selected Qventus to automate OR scheduling with ML and reported 50+ added robotic cases in Q4 2024, a $5.8M "Qventus-affected" contribution margin (vendor or trade-press reporting). — [Healthcare IT News](https://www.healthcareitnews.com/news/perioperative-it-brings-major-efficiencies-allina-health)
- **Failure and risk evidence (general-domain booking agents):**
  - τ-bench airline and retail booking agents (2024) succeeded on under 50% of tasks.
  - Reliability collapses over repeated trials (pass^8 below 25%).
  - Agents often fail to follow policy-document rules.
  - [Sierra blog](https://sierra.ai/blog/benchmarking-ai-agents)
- **Benchmark reliability:** τ²-Bench-Verified found original benchmark tasks misaligned with stated policies or DB contents. Evaluation artifacts are themselves a failure source. — [GitHub amazon-agi/tau2-bench-verified](https://github.com/amazon-agi/tau2-bench-verified)
- **Cancellation-model PPV:** at an NPV of 0.96 the PPV was only 0.21. Acting automatically on predictions (e.g., overbooking or bumping cases) would be wrong about 4 in 5 times at that threshold. This is a risk argument for keeping ML advisory, with a human in the loop. — [Mahidol repository](https://repository.li.mahidol.ac.th/items/62c8d49e-c07b-4f18-a65e-9d06b68100a0/full)

### Inferences
- The take-home's architecture can be framed as aligned with both the academic analog (CareConnect: tools + RAG + deterministic guardrails + scenario benchmark) and Qventus's product direction (scheduler assistants, slot matching, document intake).
- A credible stretch goal: a mini "Document Assistant" path where a pasted booking-request fax/email text is extracted into the same slot schema, reusing the extractor. It is cheap to demo because it reuses the validators.
- Risk framing for the write-up:
  - inconsistent policy adherence (τ-bench), so encode hard rules in code;
  - hallucinated entities, so use directory/CPT validation and ID-only commit tools;
  - unintended commits, so use confirmation interrupts and idempotency;
  - over-trusting ML estimates, so show ranges and provenance and keep them advisory;
  - PHI exposure, so use synthetic data, log redaction and minimum-necessary prompts;
  - vendor-claim inflation, so measure with your own eval harness.

### Gaps
- **Peer-reviewed deployments:** no peer-reviewed or NEJM AI/JAMIA publication was found describing a live LLM agent for **OR** case booking, or reporting its failure rates. The search was bounded and did not exhaustively cover NEJM AI, JAMIA or Health Affairs.
- **Independent Qventus evaluation:** no independent evaluation of Qventus's AI teammates was found. All figures are vendor-reported.
- **Incident reports:** no incident reports (e.g., wrong bookings or PHI leaks) from LLM scheduling agents in healthcare were found. That absence likely reflects reporting gaps rather than a lack of incidents.
- **Swarm and Evolutionary Computation 2025:** the Brunel paper on LLMs for healthcare resource management (DOI 10.1016/j.swevo.2025.101859) surfaced only as a repository record. Its method and results were not reviewed. — [Brunel repository](https://bura.brunel.ac.uk/handle/2438/31214)
