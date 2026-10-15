# Where Conversational and Agentic AI Adds Value in OR Scheduling (and Where a GUI or Plain Automation Wins)

Scope: product and interaction design, not engineering mechanics. Engineering patterns (tool calling, state machines, RAG, eval, τ-bench reliability) are in `../OR scheduling assistant research/ai_techniques.md` and are only cross-referenced here. Qventus product claims (PCC, Document Assistant, write-back) are in `../OR scheduling assistant research/qventus_and_market.md`.

Evidence labels used throughout:
- **[Peer-reviewed]**: journal or conference paper.
- **[Preprint]**: arXiv or medRxiv, not peer reviewed.
- **[Opinion]**: practitioner essay, including Nielsen and NN/g conceptual pieces.
- **[Vendor]**: company-reported claim.
- **[Trade press]**: health-system executive interview or news report.
- **[Survey]**: survey data.
- **[Regulation]**: law, ruling, or legal commentary on one.
- **[Classic]**: pre-2018 foundational HCI work, cited from background knowledge and not re-fetched in this round.

---

## Q1. What do UX research and HCI sources say about when conversational interfaces beat GUIs, and when they fall short?

### Takeaway
The evidence does not support "chat replaces GUI," and it does not support "chat is a gimmick" either. Conversation wins when the user can state an outcome more easily than they can navigate to it: retrieval, filtering, comparison, and multi-constraint "find me X" requests. GUIs and direct manipulation win for overview, precise edits, verification, and anything the user needs to feel confident about. The studies converge on hybrids, with language for stating intent and structured or visual UI for inspecting, choosing, and correcting.

### Cited Findings

**The paradigm framing (opinion, but widely cited)**
- Jakob Nielsen, May 2023: AI is the third UI paradigm, called "intent-based outcome specification."
  - The user says what they want, not how to do it, so the locus of control moves to the computer. **[Opinion]**
  - Nielsen calls current chatbot-style interfaces seriously flawed and sees them as an intermediate step, not the end state.
  - — [Nielsen, "AI Is First New UI Paradigm in 60 Years" (Substack, 2023)](https://jakobnielsenphd.substack.com/p/ai-is-first-new-ui-paradigm-in-60?open=false); [UX Tigers mirror](https://www.uxtigers.com/post/ai-new-ui-paradigm/)
- Nielsen, 2023, "The Articulation Barrier." **[Opinion]**
  - Prompt-driven UIs require users to write their intent in prose. That speeds up skilled users but excludes less articulate ones.
  - He extrapolates from literacy data that roughly half the population in rich countries is low-literacy. He admits he found no direct studies of writing or prompting skill.
  - GUIs "show" what is possible. Chat makes the user recall and articulate it.
  - Remedies from his follow-up piece: prompt builders, parametrization, related-prompt suggestions, and prompt rewrite.
  - — [Nielsen, "The Articulation Barrier" (Substack)](https://jakobnielsenphd.substack.com/p/prompt-driven-ai-ux-hurts-usability); [Nielsen, "Prompt Augmentation"](https://jakobnielsenphd.substack.com/p/prompt-augmentation)
- Nielsen, March 26, 2026, "Intent by Discovery." **[Opinion]**
  - A usable intent has three parts: (1) desired outcome, (2) constraints, and (3) a **delegation boundary** stating what the system may do itself versus only prepare.
  - The user's role moves from operator to supervisor. The GUI is demoted rather than removed: it becomes the place to inspect, negotiate, and correct AI work, and direct manipulation stays for fine edits and overrides.
  - Recommended practices:
    - Ask the fewest targeted clarifying questions that prevent the most serious mistakes.
    - Give long-running tasks a "run contract" (time window, cost cap, definition of done, hard limits).
    - Use **progressive delegation**: start with draft-and-confirm and widen authority as reliability is shown.
    - Scale friction to stakes and reversibility.
    - Show plan previews and post-action summaries that say what can still be undone.
  - New metrics he proposes: intent capture, clarification quality, evaluability, and trust calibration, in place of click efficiency.
  - — [Nielsen, "Intent by Discovery: Designing the AI User Experience" (Mar 26, 2026)](https://jakobnielsenphd.substack.com/p/intent-ux?open=false)
- NN/g (Kate Moran and Sarah Gibbons), March 22, 2024, "Generative UI and Outcome-Oriented Design." **[Opinion]**
  - Designers will set goals and constraints (what must, should, or should never appear) instead of designing every screen.
  - Caveat: interfaces that keep changing force users to relearn them. Designers must weigh tailoring against consistency.
  - — [NN/g, Generative UI and Outcome-Oriented Design (2024)](https://www.nngroup.com/articles/generative-ui/)
- NN/g, service-design piece on AI agents: with agents, the user specifies a desired result instead of performing every step. **[Opinion]** — [NN/g, How Service Design Will Evolve with AI Agents](https://www.nngroup.com/articles/service-design-evolve-ai-agents/)
- NN/g study guide, as summarized in search results, says chat-generated UI elements (inline controls) can gather context and reduce typing and memory load. It also says hybrid prompt-plus-GUI interfaces improve usability. **[Opinion]** — [NN/g, Designing AI Products and Features: Study Guide](https://www.nngroup.com/articles/designing-ai-study-guide/)

**Empirical comparisons**
- **DirectGPT, CHI 2024** (Masson et al.). **[Peer-reviewed]**
  - Design: a direct-manipulation layer over an LLM (select the object, then apply a command) compared with plain ChatGPT for editing text, code, and vector images.
  - Results: participants were about **50% faster** and used **50% fewer and 72% shorter prompts**. Subjective ratings were equal or better.
  - The gap was small for code and large for text and images.
  - The authors attribute prompt-only problems to the same "semantic and articulatory distance" that motivated direct manipulation in the 1980s.
  - — [ACM DL, DirectGPT (CHI 2024)](https://dl.acm.org/doi/fullHtml/10.1145/3613904.3642462); [arXiv 2310.03691](https://arxiv.org/abs/2310.03691)
- **Chatbot vs dashboard for industrial decision tasks** (Figliè et al., arXiv 2605.31224, May 29, 2026; sessions ran Mar to Jun 2025). **[Preprint]**
  - Design: N=20, mostly CS students, within-subjects. A GPT-4o chatbot was compared with a performance dashboard.
  - Low-complexity information retrieval:
    - The chatbot had lower workload (NASA-TLX, p=.0089) and was faster (p=.0209).
    - Accuracy was identical.
  - High-complexity problem solving: the chatbot was faster and more accurate on one of the two tasks (p=.0368 and p=.0301, Hedges' g=1.03) and showed no difference on the other.
  - Preferences:
    - 12 participants rated the chatbot more useful against 2 for the dashboard.
    - Respondents preferred the chatbot when speed (15 vs 3) or a direct answer (14 vs 2) mattered.
    - **When confidence was the criterion, all 18 decisive responses favored the dashboard.**
  - Qualitative themes:
    - "Conversational compression" helps only when the request is clear.
    - Reliance was calibrated through auditability, and the dashboard was seen as more verifiable.
    - Participants spontaneously used hybrid workflows.
  - The authors recommend hybrids in which conversational agents "reduce avoidable interaction costs." The study has a small sample and an order confound.
  - — [arXiv 2605.31224](https://arxiv.org/html/2605.31224)
- **Generative Interfaces for Language Models** (Chen, Zhang et al., Stanford, arXiv 2508.19227v2, Oct 7, 2025). **[Preprint]**
  - Design: the LLM generates a task-specific interactive UI instead of a text reply.
  - Win rates against chat:
    - 84% against Claude 3.7 chat and 69% against GPT-4o chat.
    - In a real-user study (76 participants, 380 queries), 50.8% wins, 8.2% ties, and 41.1% losses.
  - Generated UI was strongest for:
    - Data analysis and visualization (93.8%).
    - **Business strategy and operations (87.5%)**.
    - Detailed, interactive, information-dense queries.
  - It was weakest for simple "how-to" questions, where extra controls added load, and for math-heavy explanation (50%).
  - Generation could take minutes.
  - — [arXiv 2508.19227v2](https://arxiv.org/html/2508.19227v2)
- **Visualization survey** (arXiv 2601.14943, 2026). **[Preprint]** GUI interaction (buttons, sliders, selection) suits fine-grained changes that are tedious to describe. Natural-language interaction suits changes that are easy to describe. — [arXiv 2601.14943](https://arxiv.org/pdf/2601.14943)

**Human-AI interaction guidelines**
- **Amershi et al., "Guidelines for Human-AI Interaction," CHI 2019 (Microsoft).** **[Peer-reviewed]**
  - 18 guidelines, grouped by phase: initially, during interaction, when wrong, and over time.
  - The authors validated them with 49 design practitioners against 20 AI products.
  - Guidelines most relevant here (list from background knowledge of the paper):
    - G1, make clear what the system can do.
    - G2, make clear how well it can do it.
    - G9, support efficient correction.
    - G10, scope services when in doubt.
    - G11, make clear why the system did what it did.
    - G16, convey the consequences of user actions.
    - G17, provide global controls.
  - — [Microsoft Research project page](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/); [paper PDF](https://research.microsoft.com/%7Ehorvitz/Guidelines_Human_AI_Interaction.pdf)
- **[Classic] works that frame the same debate:**
  - Shneiderman and Maes (1997), "Direct manipulation vs. interface agents." — [ACM Interactions](https://dl.acm.org/doi/10.1145/267505.267514)
  - Horvitz (1999), "Principles of mixed-initiative user interfaces," which weighs the expected value of acting, asking, or doing nothing, given uncertainty about the user's goals. — [CHI 1999](https://dl.acm.org/doi/10.1145/302979.303030)
  - Shneiderman (2020), human-centered AI: high automation and high human control are separate axes and can both be high. — [IJHCI 2020](https://doi.org/10.1080/10447318.2020.1741118)

### Inferences
- In OR scheduling, the coordinator's question "Dr. Patel needs 180 min with the robot, sometime in the next 3 weeks, not Fridays" is a perfect conversational input. The answer should come back as **structured option cards or a mini-grid** the coordinator can scan, compare, and click. It should not come back as a paragraph. This hybrid pattern is what DirectGPT, Figliè, and the GenUI study all support.
- The schedule board itself (rooms × time, blocks, utilization) is an overview and verification surface. Figliè found confidence went entirely to the dashboard, and NN/g warns that shifting generated layouts force users to relearn them. Together those argue for keeping the grid **stable and conventional** and attaching AI to it, rather than regenerating it.
- Nielsen's three-part intent (outcome, constraints, delegation boundary) maps directly onto a booking request:
  - **Outcome:** a booked case.
  - **Constraints:** surgeon, duration, equipment, patient window, and policy.
  - **Delegation boundary:** hold versus book versus notify the office.
  - The assistant should make the delegation boundary explicit in its UI.
- The articulation barrier matters less for expert coordinators, who know the domain vocabulary, than for occasional users such as surgeon-office staff. For occasional users, suggested prompts and parametrized cards matter more.

### Gaps
- I found no NN/g usability-test data on agentic or chat UIs in enterprise scheduling. NN/g's work here is mostly conceptual.
- NN/g's "AI Chat Is Not (Always) the Answer" and "Less Chat, More Answer" surfaced only as titles in listings. I could not retrieve or verify their content.
- I found no controlled study comparing chat with a calendar or grid GUI specifically for scheduling or resource-allocation tasks. The closest evidence is the dashboard-vs-chatbot preprint above.

---

## Q2. What are the documented strengths and weaknesses of LLM agents in operational work?

### Takeaway
Documented strengths:
- Turning messy, unstructured inputs (faxes, referral packets, calls) into structured data.
- Running high-volume, repetitive multi-party conversations, such as payer and patient calls.
- Compressing retrieval and summarization.

Documented weaknesses:
- **Reliability and policy adherence** (covered in the prior notes via τ-bench).
- **Constraint satisfaction and planning.** LLMs alone are poor schedulers.
- **Verifiability and overreliance.**
- **Latency.**
- **Failure on accents and speech differences in voice.**

The design implication: the LLM should understand and communicate, and deterministic code or solvers should decide what is feasible.

### Cited Findings

**Strengths**
- **Unstructured document intake.**
  - A 2026 preprint built an open-weight LLM pipeline on a single consumer GPU and tested it on 200 *synthetic* colorectal-cancer fax referral packets.
  - Results: 98.9% exact extraction for labs, 100% for diagnoses, and 92.9% for procedures. The authors report zero fabricated facts across 11,993 items. Median time was 90 s per packet.
  - The data is synthetic, so real-world confirmation is needed. **[Preprint]**
  - — [medRxiv/Sciety record 10.64898/2026.10.03.26364667](https://sciety.org/articles/activity/10.64898/2026.10.03.26364667)
- **Older referral-document work.** A 2023 arXiv paper on referral understanding found that adding domain rules to a transformer greatly improved precision and F1. It also found pure rules break because every practice has its own format. **[Preprint]** — [arXiv 2309.13184](https://arxiv.org/html/2309.13184v1)
- **High-volume repetitive calls to other parties.** Infinitus voice agents call payers for benefits verification. Cencora reports:
  - offsetting the work of 100+ FTEs;
  - about 4x faster benefits-verification turnaround;
  - absorbing 10x reverification-season spikes.
  - **[Vendor]** — [Infinitus case study: Cencora](https://infinitus.ai/case-studies/cencora-patient-services/)
- **Payer-side call length.** A large US payer cut benefits-verification call length by more than a third. **[Vendor]** — [Infinitus case study: leading US payor](https://infinitus.ai/case-studies/leading-us-payor)
- **Calls to offices on staff's behalf.** Pair Team, a Medicaid medical group, used an AI agent to call physician offices and book appointments. That freed community health workers' time. The source is descriptive, with no outcome metrics. I reached it via search summary only because the article page was blocked by a CAPTCHA. **[Peer-reviewed commentary, not verified directly]** — [PMC12162835, "How generative AI voice agents will transform medicine"](https://pmc.ncbi.nlm.nih.gov/articles/PMC12162835/)
- **Retrieval compression.** The chatbot lowered workload and time for direct retrieval, filtering, comparison, and calculation (see Q1). **[Preprint]** — [arXiv 2605.31224](https://arxiv.org/html/2605.31224)

**Weaknesses**
- **Planning and constraint satisfaction.** NATURAL PLAN, Google DeepMind 2024, covers trip planning, meeting planning, and **calendar scheduling**, with tool outputs supplied in context. **[Preprint]**
  - Trip planning: GPT-4 solved 31.1% and Gemini 1.5 Pro 34.8%.
  - Calendar scheduling: even in the best long-context setting, Gemini 1.5 Pro reached only about 50%.
  - — [arXiv 2406.04520](https://arxiv.org/pdf/2406.04520)
- **Policy adherence and repeat reliability.** τ-bench found under 50% task success and pass^8 below 25%. See the prior notes. — [Sierra blog](https://sierra.ai/blog/benchmarking-ai-agents)
- **Verification and trust calibration.**
  - Users trusted the dashboard over the chatbot when confidence mattered (18 of 18 decisive responses). **[Preprint]** — [arXiv 2605.31224](https://arxiv.org/html/2605.31224)
  - Fluent natural-language explanations raise perceived credibility. Users without domain-specific ways to verify cannot easily check them. **[Preprint]** — [arXiv 2606.24370](https://arxiv.org/pdf/2606.24370)
  - A 2025 position paper argues that measuring and mitigating overreliance must become central to LLM deployment. **[Preprint]** — [arXiv 2509.08010](https://web3.arxiv.org/pdf/2509.08010)
  - An AIES paper identifies frictionless interfaces, and organizations that treat AI as authoritative, as drivers of overreliance. **[Peer-reviewed]** — [AAAI/AIES](https://ojs.aaai.org/index.php/AIES/article/download/43225/50785/47331)
- **Ironies of automation.** **[Classic]** Bainbridge (1983): automating the routine leaves humans with the hardest, rarest cases and erodes the skills needed to handle them. — [Automatica 1983](https://doi.org/10.1016/0005-1098(83)90046-8)
- **Latency.** Generated interfaces can take minutes to refine. **[Preprint]** — [arXiv 2508.19227v2](https://arxiv.org/html/2508.19227v2)
- **Voice failure modes.** In a UK example from late 2025, as reported secondhand, a patient could not get a voice booking system to understand their regional accent or speech impediment and gave up. **[Trade press, aggregator]** — [AI Healthcare 360](https://aihealthcare360.org/operations/ai-voice-agents-no-show-reduction/)
- **Needless complexity.** Generated or rich UIs added load for simple queries, where some users preferred plain chat. **[Preprint]** — [arXiv 2508.19227v2](https://arxiv.org/html/2508.19227v2)
- **When to use agents.** Anthropic recommends the simplest solution that works. Workflows (predefined code paths) suit well-defined tasks. Agents suit open-ended problems where the number of steps cannot be predicted, and they bring higher cost and compounding errors. **[Opinion, vendor engineering guidance, Dec 2024]** — [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)

### Inferences
- For OR scheduling, the LLM's comparative advantage is at the **edges**:
  - **Ingest:** fax, email, clinic note, or voicemail into a structured case request.
  - **Communicate:** ask an office for a missing H&P, draft a block-release nudge, call a patient.
  - **Summarize:** what is at risk for tomorrow.
- The **middle** (feasibility, conflicts, block rules, the time-slot search itself) belongs to deterministic code or an optimizer. NATURAL PLAN's calendar results are direct evidence that an LLM should not be the scheduler of record.
- "Chat fatigue" is a real design risk even without a clean study behind it. A coordinator booking 30+ cases a day will not type a conversation per case. High-frequency work should be **zero-chat**: auto-extracted, pre-filled, and approved with one click. Conversation should be reserved for exceptions.

### Gaps
- I found no rigorous study quantifying verbosity or "chat fatigue" in operational enterprise tools. Treat this as practitioner consensus, not evidence.
- I found no peer-reviewed evaluation of LLM extraction on *real* (not synthetic) surgical booking faxes.
- I found no published calendar-scheduling accuracy for GPT-4 in NATURAL PLAN's zero-shot setting. The snippets did not include that table.

---

## Q3. What is the evidence from healthcare operations (scheduling call centers, patient access, prior auth, referral intake, care coordination, ambient tools)?

### Takeaway
Deployment numbers are mostly vendor-reported or come from executive interviews. The common pattern among credible reports:
- The agent handles the **high-volume, rule-bound path end to end**: prior-auth approvals, reminders, routine scheduling calls, payer benefits checks.
- **Exceptions go to people**: denials, clinical questions, failed understanding.

The strongest *peer-reviewed* evidence of staff relief comes from **ambient scribes**, which work in the background with human review. That evidence does not come from chat interfaces.

### Cited Findings
- **MUSC Health with Notable agents (2025).** **[Trade press, executive interview]**
  - About **40% of prior authorizations** are completed with no human involvement. A task that took about 30 min of manual work takes the agent about 1 min.
  - The agent works in the payer portal. If the auth is approved, it writes the code into Epic so the patient can be scheduled. **Denials route to a person.**
  - Digital check-in roughly doubled, to nearly half of patients.
  - Mammogram care-gap outreach scheduled 129 mammograms by the next morning, and more than 2,000 in total.
  - — [Becker's Hospital Review](https://www.beckershospitalreview.com/ai/prior-authorizations-patient-check-ins-musc-healths-ai-agents.html)
- **Patient-access voice agents (secondary aggregator reporting; primary sources not verified).** **[Trade press, aggregator]**
  - Tampa General:
    - Scheduled appointments rose 21% within two weeks.
    - Call abandonment fell from 34% to 14.9%.
    - Wait times fell from 6.2 to 2.4 min.
  - Catholic Health: 54% call containment on day one, rising to 64%.
  - WellSpan "Ana": more than 160k calls per month.
  - MUSC "Emily": 25% of patient calls, more than 2.2M calls since 2024.
  - The aggregator notes that published results cover call handling and cost, not no-shows or access.
  - — [AI Healthcare 360](https://aihealthcare360.org/operations/ai-voice-agents-no-show-reduction/); [CloudTalk statistics roundup](https://www.cloudtalk.io/blog/healthcare-ai-voice-agent-statistic/)
- **Automated reminder calls.** Adding automated calls to SMS reminders cut no-shows from 11.3% to 9.6% across more than 244k patients. These were automated reminder calls, not a conversational agent, and the figure was seen only via a secondary roundup. **[Peer-reviewed per secondary source: NEJM Catalyst 2025]** — [CloudTalk statistics roundup](https://www.cloudtalk.io/blog/healthcare-ai-voice-agent-statistic/)
- **Infinitus (payer calls).** See Q2.
  - Infinitus also markets to **ambulatory surgery centers** and health systems, which is directly relevant to perioperative benefits verification and prior auth.
  - The company claims its agent is "10% more accurate than manual callers" without published methodology.
  - **[Vendor]** — [Infinitus ASC solutions](https://infinitus.ai/solutions/ambulatory-surgery-centers); [Infinitus success stories](https://www.infinitus.ai/success-stories)
- **Hippocratic AI.**
  - University Hospitals (Cleveland) started with pharmacy-related patient outreach and reported "promising early results" but no metrics. Planned expansion covers screening calls, education, and appointment support. **[Vendor press release, Sep 2025]** — [BusinessWire](https://secure.businesswire.com/news/home/20250910841321/en/University-Hospitals-and-Hippocratic-AI-Collaborate-to-Advance-Patient-Outcomes-Through-Safe-Patient-Facing-AI)
  - NVIDIA's case study reports 100,000 patients contacted in one day during an emergency. That is a throughput figure, not an outcome. **[Vendor]** — [NVIDIA case study](https://www.nvidia.com/en-eu/case-studies/hippocratic-ai/)
- **Qventus Perioperative Care Coordination** (Jan 2025): AI teammates make and receive calls, send SMS, read chart notes, and act on follow-ups in the EHR. Qventus claims "up to 40%" fewer cancellations. **[Vendor]** See the prior notes. — [Qventus PCC launch](https://www.qventus.com/company/newsroom/qventus-launches-perioperative-care-coordination-solution-to-alleviate-the-administrative-burden-on-clinicians-reduce-unnecessary-surgery-cancellations-and-optimize-patients-pre-and-post-surgery/)
- **Epic Emmie, Art, and Penny** (UGM Aug 2025). Emmie handles *patient-side* scheduling. See the prior notes.
- **Ambient AI scribes: the strongest peer-reviewed staff-relief signal.**
  - Olson et al., JAMA Network Open, October 2025: 263 ambulatory clinicians, six health systems, 30 days.
  - Results:
    - Burnout fell from **51.9% to 38.8%** (OR 0.26).
    - Cognitive task load fell 2.64 points on a 10-point scale.
    - After-hours documentation fell 0.90 h.
    - Focused attention on patients rose.
  - Pre-post design with no control group. The vendor (Abridge) facilitated data collection but had no role in analysis. **[Peer-reviewed]**
  - — [Yale news](https://medicine.yale.edu/news-article/ai-scribes-reduce-physician-burnout-return-focus-to-the-patient/); [Newswise](https://www.newswise.com/articles/study-ai-scribes-lower-physician-burnout-lend-patients-more-undivided-attention)
- A separate multisite JAMA study (2026, five academic centers) reportedly found about 16 min saved per 8 h of patient care, concentrated among heavy users. This was seen only via a secondary news summary. **[Peer-reviewed per secondary source]** — [Textbook of Digital Health news](https://www.textbookofdigitalhealth.com/news/2026-05-18-jama-scribe-study.html)
- **Prior-auth burden context.** Physicians and staff spend about 13 h per week on prior authorizations (AMA 2024 survey, cited secondhand). **[Survey, secondhand]** — [Moxo blog citing AMA](https://www.moxo.com/blog/agentic-ai-in-healthcare)

### Inferences
- Healthcare deployments that report results share a design: **asymmetric automation**.
  - The agent closes the happy path automatically: approved auth, confirmed appointment, reached voicemail and left the message.
  - The agent hands off the unhappy path with context attached: denial, ambiguity, clinical content, a patient in distress.
  - MUSC's "approved goes to Epic, denied goes to a person" rule is a template for OR use. For example: "office sent all required docs, so mark ready; something is missing, so the agent chases it; still missing at T-72h, so escalate to the coordinator."
- The ambient-scribe result suggests the biggest relief comes from AI that **removes work without demanding attention** (background capture plus a review step), not from a new conversational surface. An OR scheduling assistant should therefore get most of its value from background agents (intake, chasing, monitoring) and use chat as the command and exception surface.
- Throughput metrics (calls handled, containment) dominate vendor reporting. For OR scheduling, the take-home should pair them with **outcome metrics**: time-to-book, touches per case, cases with incomplete pre-op at T-72h, day-of cancellations, and released-time fill rate.

### Gaps
- I found no peer-reviewed controlled evaluation of a conversational or voice agent in a hospital scheduling call center, or of agentic prior auth or referral intake. All deployment numbers above are vendor, executive, or aggregator reported.
- I found no published outcome data from Qventus PCC calls (for example, reach rate, escalation rate, or patient satisfaction with AI calls).
- I could not verify the primary sources for Tampa General, Catholic Health, WellSpan, or the NEJM Catalyst reminder study within budget.

---

## Q4. How do agents chase information, contact other parties, and close loops, and what design principles make that trustworthy?

### Takeaway
Agents that act for staff in multi-party loops are trustworthy when:
- autonomy is a **deliberate, per-action design choice**, not a byproduct of model capability;
- friction scales with **stakes, reversibility, and external visibility**;
- every outbound action is **disclosed, consented where required, logged, and reversible**;
- humans see **a worklist of open loops**, not a chat transcript.

Regulation already constrains outbound AI voice and AI-generated patient messages.

### Cited Findings
- **Levels of autonomy** (Feng, McDonald, Zhang, University of Washington / Knight First Amendment Institute, arXiv 2506.12469, Jun 2025). **[Preprint/working paper]**
  - Five levels, defined by the user's role:
    - L1 Operator: the user decides and the agent executes.
    - L2 Collaborator: they plan and execute jointly.
    - L3 Consultant: the agent leads and consults the user for expertise or preferences.
    - L4 Approver: the agent engages the user only in risky or pre-specified cases.
    - L5 Observer: the agent is fully autonomous and the user monitors.
  - Autonomy is a design choice separate from capability: a capable agent can still be configured at a low level. The authors propose third-party "autonomy certificates."
  - — [Knight Columbia](https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1); [arXiv 2506.12469](https://arxiv.org/html/2506.12469v1)
- **Levels of automation by function.** **[Classic]** Parasuraman, Sheridan and Wickens (2000) assign automation levels separately to information acquisition, analysis, decision selection, and action implementation. — [IEEE SMC-A 2000](https://ieeexplore.ieee.org/document/844354)
- **Progressive delegation** (Nielsen, Mar 2026). **[Opinion]**
  - Start at draft and confirm, then widen authority as reliability is shown. Leave external and high-stakes actions for last.
  - Use quick approval for low-risk actions and deliberate checks for high-risk ones.
  - Show plan previews and post-action summaries with undo information.
  - Use run contracts for long-running tasks.
  - — [Nielsen, Intent by Discovery](https://jakobnielsenphd.substack.com/p/intent-ux?open=false)
- **Amershi et al. 2019:** G1/G2 (capabilities and limits), G9 (efficient correction), G11 (explain why), G16 (consequences), G17 (global controls). **[Peer-reviewed]** — [Microsoft Research](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/)
- **Regulation of outbound AI contact.**
  - **FCC Declaratory Ruling (Feb 8, 2024, unanimous):** AI-generated voices count as "artificial or prerecorded voice" under the TCPA. Such calls generally require prior express consent unless an exemption applies. **[Regulation]** — [Hunton](https://huntonak.com/privacy-and-information-security-law/fcc-issues-declaratory-ruling-that-tcpa-applies-to-ai-generated-voice-calls); [Wiley](https://wiley.law/alert-FCC-Extends-Regulatory-Reach-Over-AI-Announces-TCPA-Restrictions-Cover-AI-Generated-Voices-in-Outbound-Calls)
  - **California AB 3030 (effective Jan 1, 2025):** generative-AI patient communications about clinical information must include an AI disclaimer and instructions for reaching a human.
    - Audio: the disclaimer is spoken at the start and end.
    - Chat: it is displayed throughout.
    - Exempt if a licensed provider reads and reviews the message.
    - **[Regulation]** — [Arent Fox Schiff](https://www.afslaw.com/perspectives/alerts/california-requires-disclaimers-health-care-providers-ai-generated-patient); [Duane Morris](https://www.duanemorris.com/alerts/california_passes_novel_law_governing_generative_ai_healthcare_1224.html)
- **The escalation pattern in practice:** MUSC/Notable automate approvals and route denials to staff (Q3). **[Trade press]** — [Becker's](https://www.beckershospitalreview.com/ai/prior-authorizations-patient-check-ins-musc-healths-ai-agents.html)
- **Human-oversight research.** Recent arXiv work frames the problem as "overseeing agents without constant oversight," meaning designs that let humans supervise many agent actions without watching each one. Only the title and abstract were seen. **[Preprint]** — [arXiv 2602.16844](https://arxiv.org/pdf/2602.16844); [arXiv 2605.16278](https://arxiv.org/pdf/2605.16278)

### Inferences
- **Proposed delegation tiers for OR scheduling actions** (synthesis), keyed on reversibility, blast radius, and whether the action is visible outside the hospital:

| Tier | Agent may | Examples in OR scheduling |
|---|---|---|
| T0 Inform | Read, summarize, flag | "3 cases tomorrow lack H&P"; block utilization summary; policy lookup with citation |
| T1 Draft | Prepare an action for one-click approval | Pre-filled case request from a fax; block-release nudge email to a surgeon's office; proposed slot options |
| T2 Act and notify (with undo) | Execute low-risk, reversible, internal actions; post a summary | Place a tentative hold on released time; create follow-up tasks; send a templated "missing document" request to a known office contact |
| T3 Act autonomously in a bounded loop | Run a multi-step outbound loop within a run contract (who, what, how many attempts, deadline), then escalate | Chase a missing H&P: fax or portal message, then a call on day 2, then escalate to the coordinator at T-72h; patient pre-op reminder calls with AB 3030/TCPA-compliant disclosure |
| Never autonomous | Recommend only | Bumping or resequencing booked cases; accepting add-ons that displace others; anything clinical (clearance decisions); overriding block policy |

- The **open-loop worklist** is the right primary UI for agentic chasing. Each row shows the item, the party, the last attempt, the next step, the due time, and the escalation owner. It works like a GUI ticket queue. Chat is the place to ask "why is this stuck?" or say "call them again now."
- Outbound messages to surgeon offices and patients should carry **the hospital's identity, an AI disclosure, and a path to a human**, both for trust and for compliance with AB 3030 and the TCPA.
- Autonomy should be **configurable per site and per action type** (Feng et al.: autonomy is a design choice). That fits Qventus's forward-deployed model: start each customer at T1, then promote action types to T2 or T3 as the measured error rate permits.

### Gaps
- I found no study measuring which autonomy tier hospital operations staff *prefer* for specific scheduling actions.
- I found no published error, escalation, or complaint rates for AI outbound calls to surgeon offices or patients in perioperative workflows.
- Whether TCPA consent applies to hospital-to-patient pre-op calls depends on exemptions (for example, healthcare-related calls). That was not researched in depth and needs legal confirmation.

---

## Q5. How do clinicians and staff feel about AI in hospital operations (trust, desired autonomy, burnout relief, reasons for rejection)?

### Takeaway
Clinicians are broadly positive about AI for **administrative** work, and more so than for clinical work. Adoption is rising fast. Trust depends on concrete conditions:
- a feedback channel;
- privacy;
- **EHR integration**;
- oversight and clear liability;
- tools that **support rather than replace** staff.

Staff reject tools that add work, sit outside the workflow, remove human connection, or leave accountability unclear.

### Cited Findings
- **AMA physician survey, 2024 data, published Feb 2025.** **[Survey]**
  - AI use rose from 38% in 2023 to 66% in 2024.
  - **57%** see reducing administrative burden through automation as AI's biggest opportunity.
  - Top conditions for adoption:
    - a designated **feedback channel (88%)**;
    - **data privacy assurances (87%)**;
    - **EHR integration (84%)**.
  - 47% ranked increased oversight as the top regulatory action for trust.
  - — [AMA Physician AI Sentiment Report (PDF)](https://www.ama-assn.org/system/files/physician-ai-sentiment-report.pdf); [HC Innovation Group](https://www.hcinnovationgroup.com/analytics-ai/artifical-intelligence-machine-learning/news/55268048/ama-survey-physicians-warm-up-to-using-ai-in-practice)
- **AMA 2026 follow-up, via news coverage.** **[Survey, secondhand]**
  - 81% of physicians use AI, averaging 2.3 use cases.
  - Clear **liability frameworks** now rank as the top trust-building regulatory action.
  - — [HC Innovation Group](https://www.hcinnovationgroup.com/analytics-ai/artifical-intelligence-machine-learning/news/55363445/ama-survey-ai-usage-among-doctors-doubles-since-2023)
- **Philips Future Health Index 2025, US.** **[Survey, vendor-sponsored]**
  - **85%** of US healthcare professionals say AI can reduce their administrative burden.
  - Patients accept AI for administrative tasks such as scheduling and registration more readily than for clinical use.
  - More than 75% of professionals lose clinical time to incomplete or inaccessible data.
  - — [Philips US press release](https://www.usa.philips.com/about/news-and-insights/press-release/philips-future-health-index-2025-report-highlights-significant-trust-gap-in); [Philips blog](https://www.philips.com/a-w/about/news/archive/blogs/innovation-matters/2025/building-trust-in-healthcare-ai-five-key-insights-from-the-2025-future-health-index); [Healthcare in Europe](https://healthcare-in-europe.com/en/news/medical-ai-trust-gap-patients.html)
- **Nurses** (2025 systematic review of 37 studies): **[Peer-reviewed]**
  - moderate concern about safety and errors;
  - more optimism among younger staff;
  - a consistent preference for AI that **supports rather than replaces** staff;
  - trust hinges on transparency;
  - concerns about deskilling and overreliance on automated alerts.
  - — [PMC12507812](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12507812/); [PMC12311186](https://pmc.ncbi.nlm.nih.gov/articles/PMC12311186/)
- **American Nurse 2025-2026 Trends Survey** (more than 1,000 nurses): **[Survey]**
  - the top concern about AI is loss of human connection;
  - other concerns are privacy and **accountability when an algorithm is wrong**.
  - — [American Nurse](https://www.myamericannurse.com/2025-2026-trends-survey/)
- **Burnout relief:** see the ambient-scribe results in Q3 (burnout 51.9% to 38.8%). **[Peer-reviewed]**

### Inferences
- For OR schedulers (non-clinical staff), the most relevant acceptance drivers are, by analogy:
  - **in-EHR or in-workflow integration** (no new window to babysit);
  - **a visible feedback and correction path**;
  - **clear accountability for who booked what**, meaning audit trails that attribute agent actions;
  - tools framed as removing drudgery (chasing, re-keying) rather than replacing the coordinator's judgment.
- Coordinators' relationships with surgeon offices are part of their job value. Agent outreach should be **in the coordinator's name or team's name, with the coordinator copied**, and the coordinator should be able to take over any thread. That speaks to the "loss of human connection" and accountability concerns.

### Gaps
- I found no survey of **OR schedulers or perioperative business staff** specifically, covering their attitudes to AI agents, desired autonomy, or burnout. The available surveys are of physicians and nurses.
- I found no study of *why* hospital staff abandoned specific operational AI tools such as scheduling or capacity tools. The reasons above are inferred from general clinician and nurse surveys.

---

## Q6. Synthesis: a framework for choosing conversation or agent versus GUI versus plain automation, mapped to OR scheduling tasks

### Takeaway
Choose the modality **per task, not per product**:
- **Plain automation (no UI)** for deterministic, high-frequency, rule-bound work.
- **Background agents with an exceptions worklist** for multi-party chasing and unstructured intake.
- **Conversation** for stating ambiguous, multi-constraint intent, asking ad hoc questions, and handling exceptions.
- **GUI** for overview, comparison, verification, and precise manipulation.

The winning pattern is "**say it, see it, approve it**": language in, structured cards or a grid out, and an explicit commit with undo.

### Cited Findings
- **Conversation lowers effort for retrieval, filtering, and comparison. A dashboard wins on confidence and verification.** **[Preprint]** — [arXiv 2605.31224](https://arxiv.org/html/2605.31224)
- **Direct manipulation over LLM output beat chat-only:** about 50% faster, 72% shorter prompts. **[Peer-reviewed]** — [DirectGPT, CHI 2024](https://dl.acm.org/doi/fullHtml/10.1145/3613904.3642462)
- **Generated structured UIs beat chat** for information-dense and business-operations queries (87.5%). Chat is fine for simple how-to questions. **[Preprint]** — [arXiv 2508.19227v2](https://arxiv.org/html/2508.19227v2)
- **GUI for fine-grained changes, natural language for easily described ones.** **[Preprint]** — [arXiv 2601.14943](https://arxiv.org/pdf/2601.14943)
- **A usable intent includes a delegation boundary. Friction should scale with stakes and reversibility.** **[Opinion]** — [Nielsen, Mar 2026](https://jakobnielsenphd.substack.com/p/intent-ux?open=false)
- **Workflows over agents when steps are predictable.** **[Opinion, vendor guidance]** — [Anthropic, Building effective agents (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents)
- **LLMs alone are weak at calendar scheduling and constraint planning**, so a solver should decide feasibility. **[Preprint]** — [NATURAL PLAN](https://arxiv.org/pdf/2406.04520)
- **Asymmetric automation in production:** happy path automated, exceptions to humans. **[Trade press]** — [Becker's, MUSC/Notable](https://www.beckershospitalreview.com/ai/prior-authorizations-patient-check-ins-musc-healths-ai-agents.html)
- **Background AI with human review produced the strongest peer-reviewed staff-relief result.** **[Peer-reviewed]** — [Yale news on Olson et al. 2025](https://medicine.yale.edu/news-article/ai-scribes-reduce-physician-burnout-return-focus-to-the-patient/)

### Inferences

**Modality decision signals** (synthesis of the findings above)

| Signal | Points to conversation or agent | Points to GUI | Points to plain automation (no UI) |
|---|---|---|---|
| Intent clarity | Ambiguous, varies case to case, many optional constraints | User knows exactly what to click | Fully specified by rules |
| Input form | Unstructured (fax, email, voicemail, free text) | Already structured | Structured, machine-to-machine (HL7/FHIR) |
| Frequency × variability | Low frequency, high variability | High frequency, user needs speed through repetition | High frequency, low variability |
| Parties and elapsed time | Multi-party, spans hours or days, needs follow-up | Single user, single sitting | System to system |
| Output need | An answer, a draft, a summary | Overview, comparison, spatial or temporal layout (schedule grid) | A state change only |
| Precision | Coarse ("sometime next 3 weeks, not Fridays") | Fine-grained (drag a case 15 min, reorder rooms) | Exact by rule |
| Verification need | Low or moderate (draft gets reviewed) | High; user must feel confident | Validated by code |
| Context of use | Mobile, hands busy, between cases (voice or SMS) | At a desk with large screens | n/a |
| Stakes and reversibility | Reversible, internal | Irreversible or high blast radius: human decides in GUI with AI recommendations | Low stakes, reversible |

**Mapping to OR scheduling tasks**

| Task | Best primary modality | Role of AI | Role of GUI | Delegation tier (see Q4) |
|---|---|---|---|---|
| Intake of booking request (fax, email, clinic EHR order) | Background agent | Extract to structured case request; flag missing or conflicting fields | Side-by-side source document and extracted fields for one-click confirm or correct | T1 → T2 |
| Find time for a case ("180 min, robot, next 3 weeks, not Fri") | Conversation in, cards out | Parse constraints; call solver; explain trade-offs | Ranked slot cards and mini-grid; click to hold | T1 (hold may be T2) |
| View and manage the daily or weekly schedule, block utilization | GUI (grid or board) | Inline annotations ("at-risk", "released"), "explain this" on hover | Primary surface; drag-and-drop for precise moves | T0 |
| Precise reschedule or room swap | GUI direct manipulation | Validate the move live (conflicts, equipment) | Primary | Human |
| Chase missing pre-op items (H&P, consent, clearance, implant or vendor tray, prior auth) | Background agent with worklist | Multi-channel outreach with run contract; parse replies; escalate at deadline | Open-loop worklist with status, next step, owner | T2 → T3 |
| Block release and open-time marketing to surgeon offices | Agent-drafted, human-approved (later auto) | Identify likely unused block; draft nudge; match released time to best-fit surgeons | Approve and send queue; utilization view | T1 → T2 |
| Add-on or urgent case that displaces others | GUI decision with AI options | Generate options with impact (who moves, overtime minutes) | Compare options side by side; human commits | Never autonomous |
| "What's at risk for tomorrow?" or shift handoff | Conversation or summary | Summarize across systems with links to records | Linked worklist and grid | T0 |
| Policy question ("can Dr Y book outside block within 72h?") | Conversation (RAG with citation) | Answer with source excerpt | Link to policy | T0 |
| Routine confirmations, reminders, status sync to EHR | Plain automation | None needed, or templated messages | Exceptions only | Automated |
| Patient pre-op calls (instructions, arrival time, NPO reminders) | Voice or SMS agent | Conversational outreach with AI disclosure and human fallback; log outcomes | Coordinator or PAT dashboard of reach and escalations | T3 within compliance limits |

**Design principles to state in the take-home** (synthesis)
1. **Conversation is the command line, not the workspace.** The grid and the worklist remain the workspaces. Chat issues intents and handles exceptions.
2. **Say it, see it, approve it.** Natural-language intent goes in. Structured, verifiable artifacts (cards, diffs, previews) come out. An explicit commit follows, with undo and an audit entry.
3. **Zero-chat for the happy path.** If a coordinator has to converse to book a routine, complete request, the design has failed. Pre-fill it and make approval one click.
4. **The LLM interprets and communicates. Code decides.** Feasibility, conflicts, and policy come from deterministic services or a solver. The LLM explains their output.
5. **Agents own loops, humans own judgment.** Agents chase, remind, and reconcile within run contracts. Humans decide displacements, exceptions, and anything clinical.
6. **Autonomy is a dial per action type, per site.** Start at draft and approve, and promote action types on measured accuracy (progressive delegation).
7. **Make agent work legible.** Show who was contacted, when, what they said, what happens next, and who is accountable. Disclose AI to outside parties and keep a path to a human.
8. **Measure outcomes, not conversations.** Time-to-book, touches per case, pre-op completeness at T-72h, day-of cancellations, released-time fill rate, and override and correction rates. Not message counts or containment.

### Gaps
- The framework is a synthesis. I found no study that validates it end to end in perioperative scheduling, so it should be presented as a hypothesis to test in a pilot.
- No time-motion data was found on how coordinators split their time across the tasks in the mapping table, so I could not weight which modality would deliver the most value. The prior notes also flag this gap.
