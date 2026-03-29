# The Ten Principles of Structured Antagonism

*Expanded with examples and counter-examples*

---

## 1. Ontology First

**Define what exists before describing what happens.**

You don't get to discuss features until you've committed to entities, relationships, lifecycles, and identity rules. The schema shapes what you can capture. The capture shapes what you can model. Get the ontology wrong and everything downstream inherits the error silently.

**In practice:**
- In a software spec: define domain objects before feature flows
- In a data science plan: define variables, populations, and constructs before choosing methods
- In a research design: define constructs and their operationalizations before designing procedures

**Counter-example:** A feature spec that says "users can share content with groups" without having defined what a User is, what Content is, what a Group is, what "sharing" means (copy? reference? delegation?), or what the relationship between User and Group is. Every downstream decision about permissions, notifications, and storage depends on these definitions — and without them, each decision is a coin flip.

**The test:** Can someone describe a behavior without having defined the objects involved? If yes, the ontological phase is too weak.

---

## 2. Separate, Then Project

**Build the base representation first; derive views from it. Never build "the view."**

The temptation is always to jump to the output format — the dashboard, the report, the diagram. But if you build the view without building the representation it projects from, you get a view that cannot be reprojected, cannot serve a different audience, and cannot evolve when requirements change.

**In practice:**
- In a software spec: build the domain model, then derive context diagrams, feature specs, and security posture as different projections
- In a data science plan: build the analytical framework, then derive the technical plan, the stakeholder summary, and the validation report
- In a research design: build the theoretical model, then derive the protocol, the IRB application, and the results template

**Counter-example:** A dashboard designed directly from stakeholder requests, without an underlying data model. When a second stakeholder needs a different view, the team discovers the dashboard can't be reprojected — it was built as "the view," not as a projection from a base.

**The test:** Can you derive at least two meaningfully different views from your base representation? If not, you may have built a view, not a representation.

---

## 3. Principled Lossyness

**Every view hides things deliberately. Name what you're hiding and why.**

A model that captures everything is not a model — it is a worse copy of reality. A spec that includes every possible detail is not thorough — it is unnavigable. The art is in what you choose to exclude, and the discipline is in making that choice explicit.

**In practice:**
- Implementation-neutral specs hide tech stack choices because the behavioral audience doesn't need them
- Executive summaries hide methodology because the decision-making audience needs conclusions, not procedures
- Data dictionaries hide business context because the engineering audience needs schemas, not narratives

**Counter-example:** A 200-page spec that includes behavioral requirements, API schemas, database ERDs, deployment topology, and team structure in a single document. No single reader needs all of it. Every reader must wade through the rest to find what they need. The document hides nothing — and is therefore useless to everyone.

**The test:** For each section, can you name who it's for and what it deliberately excludes? If not, the view isn't principled — it's just incomplete.

---

## 4. Scope by Exclusion

**Non-goals and boundaries are first-class outputs, not afterthoughts.**

Scope creep doesn't announce itself. It hides in ambiguity — in the features no one explicitly excluded, in the use cases no one explicitly said "not this." Forcing explicit non-goals is adversarial scoping: it makes the author confront boundaries rather than leaving them undefined.

**In practice:**
- "This system does NOT handle payment processing" is more useful than "this system handles order management" — the second leaves payment ambiguous
- "This analysis does NOT attempt causal inference" prevents downstream misinterpretation of correlational results
- "This study does NOT generalize beyond the sampled population" prevents overgeneralization of findings

**Counter-example:** A spec for a "messaging system" that never states whether it handles file attachments, read receipts, message editing, or message deletion. Six months later, stakeholders disagree about what was promised — because the boundaries were never drawn.

**The test:** Can someone read your artifact and *still* be confused about whether X is in scope? If yes, X needs to be in the non-goals list.

---

## 5. Audit Before Synthesis

**Treat every input as a hypothesis to be stress-tested, not a draft to be polished.**

The natural instinct is to improve — to take what's there and make it better. But improvement without diagnosis is cosmetic. You might polish a section that is internally beautiful but contradicts three other sections. You might add detail to a feature that shouldn't exist at all.

**In practice:**
- Before refining a spec, first list its gaps, ambiguities, contradictions, and unstated assumptions
- Before improving an analysis plan, first check whether the method matches the data, the data matches the question, and the conclusions are supportable
- Before revising a research design, first check whether the design can actually test the stated hypothesis

**Counter-example:** A code reviewer who "improves" a function by refactoring it — without noticing that the function is called with the wrong arguments from three different callsites. The improvement makes the wrong code prettier.

**The test:** Does your process have a diagnostic step that runs *before* any generative step? If not, you're polishing before diagnosing.

---

## 6. Epistemic Sequencing

**Establish dependency chains between layers. Don't let later steps proceed until earlier ones are sound.**

Domain & Semantics → Data & Contracts → Behavior & Flows → Quality Attributes → Lifecycle & Evolution. This is not organizational preference — it is epistemic necessity. Each layer consumes the outputs of the previous one. Skipping ahead doesn't save time — it creates rework when the skipped layer turns out to have been wrong.

**In practice:**
- You cannot define API contracts without a domain model (what entities exist to be exposed?)
- You cannot set SLOs without knowing the flows (what operations need latency guarantees?)
- You cannot choose a statistical test without knowing the data distribution (what assumptions does the test require?)

**Counter-example:** A team that sets "99.9% uptime" as an SLO before defining what operations the system performs. Three months later, they discover that one critical operation involves a third-party API with 99% uptime — making the 99.9% target impossible regardless of their own engineering.

**The test:** Try to fill out Layer N without having completed Layer N-1. If you can do it without feeling lost, the dependency chain is too loose.

---

## 7. Artifact Closure

**Every step produces a named artifact with a verifiable "done when" condition.**

"Explore options" is not a step — it is a wish. "Research best practices" is not a step — it is an activity. A step must produce something concrete, and there must be a way to know when it's done. Without this, planning degenerates into a list of good intentions.

**In practice:**
- "Define canonical domain ontology — artifact: Ontology Doc — done when: all core terms have single definitions and disjoint/overlap rules are explicit"
- "Specify data quality requirements — artifact: DQ Checklist — done when: each variable has completeness, accuracy, and freshness thresholds"
- "Design experimental protocol — artifact: Protocol Doc — done when: every step from recruitment to data collection is numbered and each has materials listed"

**Counter-example:** A project plan with the step "Investigate caching strategies." When is this done? When someone feels like they've investigated enough? When they've read three blog posts? When they've benchmarked four options? The step has no closure condition, so it either runs forever or ends arbitrarily.

**The test:** For each step in your plan, can a different person verify whether it's done? If not, the step needs a sharper "done when."

---

## 8. Halt on Uncertainty

**If the foundation is unsound, stop and surface it. Never paper over gaps.**

The instinct to keep going is strong. The gap is small, the deadline is near, the rest of the work is ready. But proceeding on unsound foundations doesn't save the work — it delays the discovery of the problem while increasing the cost of fixing it.

**In practice:**
- If the spec is ambiguous about a critical boundary, don't guess — stop and ask
- If two answers are inconsistent, don't pick the more convenient one — stop and reconcile
- If the data doesn't match the assumptions of the planned analysis, don't proceed anyway — stop and either change the analysis or investigate the data

**Counter-example:** An analysis that assumes normal distribution, applies a t-test, and reports the p-value — without checking whether the data is actually normally distributed. The analyst knew the assumption might not hold, but proceeding was easier than stopping. The resulting p-value is meaningless, but it looks precise.

**The test:** Does your process have explicit halt gates — points where the workflow stops if conditions aren't met? If not, it will produce output on unsound foundations.

---

## 9. Cross-Layer Validation

**Internal coherence within a section is necessary but not sufficient. Sections must be coherent with each other.**

The most dangerous errors are not within sections — they are between sections. An ontology that defines three entity types and an API spec that exposes four. A flow that assumes eventually-consistent reads and an SLO that promises read-your-writes. A retention policy that deletes data after 30 days and an audit requirement that preserves it for 7 years.

**In practice:**
- Check ontology against contracts: does every exposed entity exist in the domain model?
- Check flows against SLOs: can the flow complete within the stated latency envelope?
- Check consistency model against APIs: do the API guarantees match the consistency guarantees?
- Check analysis methods against data properties: does the method's assumptions hold for this data?
- Check conclusions against confidence levels: does the stated confidence support the strength of the conclusion?

**Counter-example:** A spec where Section 3 (Domain Model) defines a "Project" entity with states {draft, active, archived} and Section 6 (Feature Specs) includes a flow for "deleting a project." The flow references a state ("deleted") that doesn't exist in the domain model. Each section is internally coherent. Together, they contradict.

**The test:** Build a compatibility matrix: for each pair of related sections, what invariant must hold between them? If you can't state the invariant, the relationship is unchecked.

---

## 10. Stakeholder-Aware Views

**The same system looks different to different people. Build for projection, not for consensus on a single narrative.**

A view for the modeler shows wiring diagrams and type flows. A view for the business stakeholder shows equilibrium outcomes and sensitivity analyses. Each is answering a different question about the same underlying reality. A view optimized for one stakeholder will actively mislead another.

**In practice:**
- A context diagram serves boundary thinkers (what's in, what's out, what touches what)
- A feature spec serves builders (triggers, flows, error handling)
- A security posture serves compliance (who can do what, what data is sensitive)
- An executive summary serves decision-makers (outcomes, trade-offs, risks)

**Counter-example:** A single "technical design document" shared between the engineering team, the product team, the security team, and the executive sponsor. The engineers need API schemas. The PM needs user stories. The security team needs threat models. The exec needs a one-page summary. No single document serves all of them — and the attempt to do so serves none of them.

**The test:** For each section of your artifact, can you name a specific person or role who is its primary audience? If a section doesn't have a clear audience, it may be a view without a viewer — or a misplaced detail that belongs in a different projection.
