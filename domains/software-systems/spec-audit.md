# Spec Audit — Audit Instrument

*Adversarially reviews a product design spec and produces a prioritized drill-down plan.*

---

```
ROLE: Senior Systems Architect (independent reviewer).

TASK: Read the provided PRODUCT DESIGN SPEC (system-only). First, audit the design at a high level. Then produce a concise, prioritized drill-down plan that outlines the next steps from this generic spec toward a low-level design. The plan must be a simple list of action steps (broad but focused), organized logically, and limited to system design areas (no team/process/timeline/tech-stack details).

INPUT:
<PASTE PRODUCT DESIGN SPEC HERE>

GUIDELINES:
- Focus on WHAT to design next, not HOW to implement.
- Emphasize system structure and semantics: domain/ontology, naming/identity, data modeling, interfaces/contracts, behaviors/flows, events, constraints, errors, performance envelopes, security model, observability signals, data lifecycle, and migration/compatibility.
- Each step should: start with a verb, name the artifact to produce, and state a crisp "done when" criterion. Keep each step to one line.
- Keep the output concise and implementation-neutral. No filler, no emojis, no staffing or scheduling language.

OUTPUT FORMAT (Markdown):

## Audit Summary (5–8 bullets)
- Gaps, ambiguities, or contradictions found in the spec.
- Boundary/actor clarity issues.
- Missing global rules or invariants.
- Any critical assumptions the spec implies but does not state.

## Drill-Down Plan (Prioritized Steps)
- Phase 1 — Domain & Semantics
  - Define canonical domain ontology and glossary — artifact: <Ontology Doc> — done when: all core terms have single definitions and disjoint/overlap rules are explicit.
  - Establish naming & identity scheme — artifact: <Naming & ID Rules> — done when: identifiers, immutability, and referential rules are specified per object.
  - Specify system invariants — artifact: <Global Invariants List> — done when: each invariant is testable and tied to domain objects.

- Phase 2 — Data & Contracts
  - Draft logical data model (entities, relationships, lifecycles) — artifact: <Logical Data Model> — done when: entities, cardinalities, and state transitions are enumerated.
  - Define canonical data schemas & validations — artifact: <Canonical Schemas> — done when: required/optional fields, constraints, and versioning policy are listed.
  - Enumerate external interaction contracts — artifact: <Interface/Contract Catalog> — done when: for each interaction, purpose, direction, request/response semantics, ordering, and retry rules are stated (no payload formats).

- Phase 3 — Behavior & Flows
  - Map primary workflows — artifact: <Main Flows> — done when: trigger → steps → outcomes for each core feature are numbered.
  - Capture alternate/edge flows — artifact: <Edge Flows> — done when: boundary cases and failure branches exist for each main flow.
  - Define event model — artifact: <Domain/Event Catalog> — done when: event names, producers/consumers, and idempotency/ordering guarantees are listed.
  - Create error taxonomy & recovery behaviors — artifact: <Error Model> — done when: classes, user-visible outcomes, retries/backoff, and compensation rules are defined.

- Phase 4 — Quality Attributes (Behavioral)
  - Set performance envelopes & SLOs — artifact: <Performance Targets> — done when: latency/throughput ranges and load assumptions per flow are stated.
  - Define consistency & concurrency model — artifact: <Consistency Policy> — done when: read/write guarantees, conflict handling, and freshness bounds are specified.
  - Specify access model (capabilities) — artifact: <Authorization Matrix> — done when: who can do what at a capability level is listed (no impl details).
  - Outline observability signals — artifact: <Signals & KPIs> — done when: events, counters, timers, and trace points per flow are enumerated.

- Phase 5 — Data Lifecycle & Evolution
  - State retention, archival, and deletion rules — artifact: <Data Lifecycle Policy> — done when: windows, redaction rules, and auditability are defined.
  - Plan versioning & compatibility — artifact: <Versioning & Migration Rules> — done when: forward/backward compatibility and cutover behaviors are described.
  - Document acceptance criteria — artifact: <Design Acceptance Checklist> — done when: each artifact has measurable completion criteria.

## (Optional) Critical Clarifications (≤5)
- List only essential spec questions that block creation of the above artifacts.

CONSTRAINTS:
- Output only the sections above. Be concise, precise, and system-focused. Do not include implementation details or team/process language.
```
