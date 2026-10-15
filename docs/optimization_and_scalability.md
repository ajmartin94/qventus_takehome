# Optimization and Scalability

What we would do next to improve the OR booking agent, grouped by the four areas in the assignment.

## Monitor and improve performance over time

- Integrate tracing into the product's core tracing solution (OpenTelemetry?) and make metrics available for monitoring in standard dashboards. 
- Track product metrics: request-to-confirmation time, coordinator touches per request, first-pass completeness, own-block share and routing rates, etc.
- Track model metrics: extraction accuracy per field and channel (coordinator corrections drive feedback loop for labeled data), refusal and fallback rates, latency and cost per completed booking, conversation routing deviations, tool sequence (if applicable, etc.
- Alarm on any non-zero safety-gate count: a commit without confirmation, an identifier not from a lookup, a booking against the surgeon's order, or an urgent or clinical request booked, etc. 
- Build a generated eval set with seed cases across channel, input condition, request type and service line, giving scenarios with known answers. Ideally, would seed with real submission data cleansed of PII and PHI and signoff with SMEs.
- Grade deterministically (task success, routing, field precision and recall, pass^3, safety gates at 100%) where possible, and use a model judge where needed (tone, for example).
- Gate every prompt or model change on the suite, with prompt versions and hashes in the traces.
- Turn each coordinator correction and hand-off in production into a new eval scenario. Sample cases with no corrections to supplement.
- Tune effort per prompt against the eval suite, keeping the lowest setting that holds quality.
- Move prompts (especially the phrasing) to a smaller model once it matches quality on the suite.
- Run a "shadow-mode" that simulates the Agent running completely autonomously and compare verdicts with coordinators' decisions, potentially switching to autonomous operation for specific request types. 

## Scale the architecture to support multiple workflows

- Package the shared layers (ports and adapters, policy engine, interpretation layer, state-machine engine) so each workflow imports them.
- Add a workflow by writing only its transition table, handlers, domain module, intents, fields and scenarios.
- Put an intake router in front that decides which workflow each input belongs to.
- Onboard a hospital by writing adapters to its systems and loading its policies, with no change to the agent's code.
- Build a process to turn prose-only policies into structured rules through model-assisted extraction that a person reviews and signs off.
- Build out session storage or integrate with existing session storage solution in order to scale with user load (PostGreSQL or similar). Additionally, ensure that long-wait replies are handled gracefully and can survive system interruption. 
- Feed inputs through queues from the fax server, email gateway and HL7 SIU feed, with idempotent commits making retries safe.

## Leverage RAG/vector databases for external knowledge

- Onboard hospitals with their own policy documentation. Create embedding vector stores via chunking by section, and model enrichment with supervision. 
- Enables the solutuion to answer coordinators' policy questions with citations, such as "When does a robotic block release?" and explain each decision by quoting the policy passage behind the rule that made it.
- Using the retrieval as enforcement of the workflow can be tricky, so this would need a lot of testing. It would make the most sense to pair this with a structured rule embedding process for a hospital's onboarding and policy change management to ensure that specific policy rules are translated into testable parts of their Agent's workflow and then supplement steps in the conversation with retrieved information.
- Measure retrieval recall@k on its own question set before measuring answer quality.

## Ensure robustness against ambiguous or incomplete inputs

- Already have a place for routing when there are gaps in the request, but user experience improvements (more communication channel options, easy one-click responses sent on behalf of the coordinator, etc) would impact user outcomes. 
- Add field-level OCR and transcription confidence, so low-confidence values get a question even when they parse.
- Show the evidence snippet from the source document beside each value on the confirmation card.
- Use the hospital's master patient index data to supplement and/or challenge incoming data from the input, in order to answer questions not completely answered on the incoming request. Narrow patient searches with match scores to ensure the correct patient is being retrieved. 
- Build out a robust eval suite to ensure coverage of challenging and/or ambiguous inputs. Add a model-played coordinator in to test free-form replies to clarifying questions. Add eval cases with instructions hidden in faxes and emails, to keep checking that document text can't steer the flow. Add eval cases with varied documentation quality, misspellings, incomplete patient data, etc. 
