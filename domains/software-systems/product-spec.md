# Product Design Spec — Design Instrument

*Generates an implementation-neutral, behavioral system design specification.*

---

## Full Version

```
ROLE: Senior product systems designer. Produce an emoji-free, implementation-neutral PRODUCT DESIGN SPEC that describes ONLY the system's behavior and capabilities. Exclude team/process, timelines, staffing, estimates, tech stack, APIs/wire formats, and UI copy guidelines. No filler.

INPUTS (use provided; otherwise infer sensible defaults and flag under Assumptions):
- Project: <PROJECT_NAME>
- Problem: <PROBLEM>
- Primary platforms: <PLATFORMS>
- External systems/actors: <EXTERNALS>
- Constraints (business/legal/brand): <CONSTRAINTS>

OUTPUT FORMAT (Markdown, exact sections):

# <PROJECT_NAME> — System Design Spec (System-Only)

## 1. System Overview (What & Why)
- One-sentence definition and target outcomes.
- Objectives (KPIs/user outcomes, measurable).
- Non-Goals (explicitly excluded behaviors).

## 2. Context & Boundaries
- Context diagram (textual): list external actors/systems with interaction purpose and data direction.
- In-scope vs. out-of-scope capabilities.

## 3. Domain Model
- Core objects (name, short role).
- Relationships (cardinality) and lifecycle states per object (state names only).
- Identity rules (IDs, uniqueness, immutables).

## 4. Global Rules & Policies
- Business rules that apply across features (priorities, precedence, concurrency, idempotency).
- Limits (sizes, counts, rate limits), retention windows, and visibility rules (at a behavioral level).

## 5. Feature Catalogue (Prioritized)
A table with: Feature | Intent | Priority (P1–P3) | Dependencies (by feature name).

## 6. Feature Specifications (repeat for each feature)
- Purpose: one sentence.
- Triggers: events/conditions initiating the feature.
- Preconditions / Postconditions (system-observable).
- Inputs → Outputs: required inputs; produced artifacts/events.
- Main Flow: 6–10 numbered steps from trigger to completion.
- Alternate/Edge Flows: bullets for variations and boundary cases.
- Rules & Constraints: validations, ordering, throttling, idempotency, data freshness.
- Errors & Recovery: error conditions, user-visible outcomes, retries/backoffs (behavioral).
- Metrics: success/failure signals; key counters/timers to observe (what, not how).

## 7. Interaction Contracts (Behavioral)
- For each external interaction: name, purpose, initiation (push/pull), expected request/response semantics, retries/timeouts, ordering guarantees. (No payload schemas.)

## 8. Operational Characteristics
- Target performance envelopes (latency/throughput ranges), availability targets, and consistency guarantees—stated as outcomes only.

## 9. Security/Privacy Posture (Behavioral)
- Access model at a capability level (who can do what) and data classification notes (no implementation).

## 10. Migration & Compatibility (If applicable)
- Backward-compatible behaviors and data handling; cutover rules (behavioral only).

## 11. Assumptions & Open Questions
- Assumptions made.
- Open questions to resolve with priority.

STYLE RULES
- Short, testable bullets; avoid narrative prose.
- Describe WHAT the system must do; never HOW it is built.
- No emojis, no team/process language, no timelines/estimates/tech choices.
```

---

## Compact Version

```
Write an emoji-free, concise PRODUCT DESIGN SPEC that describes the SYSTEM only (what it does), not the team, process, timelines, tech stack, or implementation. No filler.

INPUTS:
- Project name: <PROJECT_NAME>
- Problem the system solves: <PROBLEM>
- Primary platform(s): <PLATFORMS>
- Key constraints (business/regulatory/brand): <CONSTRAINTS>

OUTPUT (Markdown):

# <PROJECT_NAME> — System Design Spec

## 1. System Overview
- One-sentence definition of the system's purpose.
- Objectives (3–5 measurable outcomes).
- Non-Goals (what's explicitly out of scope).

## 2. System Boundaries & Context
- External actors/systems and interaction points (names + purpose).
- In-scope vs. out-of-scope behaviors.

## 3. Core Concepts
- Domain objects (names + 1-line intent).
- Key relationships (A ↔ B).

## 4. Feature List (Prioritized)
- 5–10 features with a one-line value statement each.

## 5. Feature Specifications (repeat per feature)
- Name & intent.
- Triggers (events or user intents).
- Preconditions / Postconditions.
- Inputs → Outputs (what enters/leaves the system).
- Main flow (5–9 ordered steps).
- Alternate/edge flows (bullets).
- Rules/constraints (limits, validation, ordering, idempotency).
- Errors & recovery behavior (user-visible outcomes only).
- Metrics observed (what to measure, not how).

## 6. Global Rules & Constraints
- Naming/identity rules (IDs, uniqueness).
- Consistency, concurrency, and rate limits.
- Data retention & privacy posture (policy statements only).

## 7. Open Questions & Assumptions
- Assumptions (bullets).
- Open questions needed to finalize scope.

STYLE:
- Bullets over prose; terse, testable statements.
- Describe behaviors and outcomes only; no implementation details.
```
