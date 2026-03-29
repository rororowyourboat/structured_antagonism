# Anatomy of an SA Prompt

*Dissecting the structural patterns in the three software design prompts*

---

This document walks through the three existing software design prompts and annotates exactly which SA principle each structural choice embodies. If you want to understand *why* the prompts are built the way they are, this is where to look.

The prompts themselves are in [`domains/software-systems/`](../domains/software-systems/).

---

## Prompt 1: Product Design Spec (The Design Instrument)

### The Role Declaration

```
ROLE: Senior product systems designer. Produce an emoji-free,
implementation-neutral PRODUCT DESIGN SPEC that describes ONLY
the system's behavior and capabilities.
```

**Principles at work:**
- **Principled Lossyness (P3):** "implementation-neutral" and "behavior and capabilities" are explicit exclusions. The prompt names what it's hiding (implementation) and why (this is a behavioral view, not an engineering view).
- **Stakeholder-Aware Views (P10):** The role is "product systems designer" — not engineer, not architect, not PM. This constrains the perspective to behavioral description, which serves the protocol designer and modeler without burdening them with implementation concerns.

### The Exclusion List

```
Exclude team/process, timelines, staffing, estimates,
tech stack, APIs/wire formats, and UI copy guidelines.
```

**Principles at work:**
- **Scope by Exclusion (P4):** This is the most aggressive non-goal declaration in any of the three prompts. Seven categories explicitly excluded. Each exclusion is a boundary that prevents scope creep from a specific direction.
- **Principled Lossyness (P3):** These exclusions aren't arbitrary — they represent concerns that belong to different stakeholders (PM owns timelines, engineering owns tech stack, design owns UI copy). The prompt enforces the separation.

### Section 1: System Overview

```
- One-sentence definition and target outcomes.
- Objectives (KPIs/user outcomes, measurable).
- Non-Goals (explicitly excluded behaviors).
```

**Principles at work:**
- **Ontology First (P1):** Before any feature is discussed, the system must be defined in one sentence. This forces ontological commitment at the highest level.
- **Scope by Exclusion (P4):** Non-Goals appear in the very first section — not at the end as an afterthought, but as a foundational constraint. You define what the system *is not* before you define what it *does*.

### Section 3: Domain Model

```
- Core objects (name, short role).
- Relationships (cardinality) and lifecycle states per object.
- Identity rules (IDs, uniqueness, immutables).
```

**Principles at work:**
- **Ontology First (P1):** This is the ontological core. Objects, relationships, lifecycles, identity rules — all defined before any behavior is described. This section answers "what exists?" and must be answered before "what happens?" (the feature specs in Section 6).
- **Epistemic Sequencing (P6):** Section 3 (Domain Model) comes before Section 6 (Feature Specifications). You cannot meaningfully describe feature flows without knowing what objects exist, how they relate, and what states they can be in.

### Section 5: Feature Catalogue

```
A table with: Feature | Intent | Priority (P1–P3) | Dependencies (by feature name).
```

**Principles at work:**
- **Epistemic Sequencing (P6):** The catalogue comes before the detailed specs. This forces a complete inventory before deep dives — preventing the common failure mode of specifying three features in detail while forgetting the fourth that makes them all coherent.
- **Cross-Layer Validation (P9):** The Dependencies column makes inter-feature dependencies explicit. This is a lightweight compatibility check — forcing the author to consider how features interact before specifying each one in isolation.

### Section 6: Feature Specifications

```
- Triggers: events/conditions initiating the feature.
- Preconditions / Postconditions (system-observable).
- Inputs → Outputs: required inputs; produced artifacts/events.
- Main Flow: 6–10 numbered steps from trigger to completion.
- Errors & Recovery: error conditions, user-visible outcomes.
- Metrics: success/failure signals (what, not how).
```

**Principles at work:**
- **Artifact Closure (P7):** Each feature spec is a complete artifact with clear structure. Triggers, pre/postconditions, flows, errors, metrics — nothing is left vague.
- **Principled Lossyness (P3):** "Metrics: what, not how" — the prompt explicitly separates the *measurement concern* from the *instrumentation concern*. You define what to observe, not how to observe it.
- **Separate, Then Project (P2):** The spec format is a view of the system optimized for builders. The same underlying behavior appears differently in Section 2 (context diagrams for boundary thinkers) and Section 9 (security posture for compliance).

### Style Rules

```
- Short, testable bullets; avoid narrative prose.
- Describe WHAT the system must do; never HOW it is built.
```

**Principles at work:**
- **Artifact Closure (P7):** "Testable bullets" — every statement should be verifiable. This is the artifact closure principle applied at the sentence level.
- **Principled Lossyness (P3):** "WHAT, never HOW" — the single most important style rule, repeated as a constraint to prevent the natural drift toward implementation.

---

## Prompt 2: Spec Audit (The Audit Instrument)

### The Role Shift

```
ROLE: Senior Systems Architect (independent reviewer).
```

**Principles at work:**
- **Audit Before Synthesis (P5):** The role explicitly changes from "designer" to "independent reviewer." This is not the same person polishing their own work — it is a different perspective, adversarially positioned.

### The Task Structure

```
TASK: First, audit the design at a high level. Then produce
a concise, prioritized drill-down plan.
```

**Principles at work:**
- **Audit Before Synthesis (P5):** "First audit, then plan." The sequencing is explicit. You diagnose before you prescribe. The prompt does not allow jumping to solutions.

### Audit Summary

```
- Gaps, ambiguities, or contradictions found in the spec.
- Boundary/actor clarity issues.
- Missing global rules or invariants.
- Any critical assumptions the spec implies but does not state.
```

**Principles at work:**
- **Audit Before Synthesis (P5):** Four categories of problems — gaps, ambiguities, contradictions, assumptions. This is a diagnostic taxonomy. It forces the reviewer to categorize what's wrong rather than just saying "needs work."
- **Cross-Layer Validation (P9):** "Contradictions" as a category means the reviewer must check sections against each other, not just within themselves.

### The Drill-Down Plan

```
Phase 1 — Domain & Semantics
  - Define canonical domain ontology — artifact: <Ontology Doc>
    — done when: all core terms have single definitions
  - Establish naming & identity scheme — artifact: <Naming & ID Rules>
    — done when: identifiers and referential rules are specified
```

**Principles at work:**
- **Epistemic Sequencing (P6):** The five phases follow the dependency chain: Domain → Data → Behavior → Quality → Lifecycle. Each phase depends on the previous.
- **Artifact Closure (P7):** Every step has three components: a verb ("Define"), a named artifact ("<Ontology Doc>"), and a "done when" condition. This is the most rigorous expression of artifact closure in any of the three prompts. No step is a vague verb.

### Critical Clarifications

```
- List only essential spec questions that block creation
  of the above artifacts.
```

**Principles at work:**
- **Halt on Uncertainty (P8):** These are halt gates. They block progress. The word "block" is explicit — these aren't nice-to-haves, they are dependencies that prevent the drill-down plan from executing.

---

## Prompt 3: Spec Synthesize (The Synthesis Instrument)

### The Conditional Workflow

```
A) If ANSWERS are NOT provided:
   → Produce breadth questionnaire → STOP

B) If ANSWERS ARE provided:
   1) Consistency & completeness audit
   2) If ANY incompatibility → Final clarification questions → STOP
   3) If COMPLETE & COMPATIBLE → Final spec
```

**Principles at work:**
- **Halt on Uncertainty (P8):** This is the most sophisticated structural move across all three prompts. There are two halt gates: one for missing information, one for inconsistent information. Only when both are cleared does the prompt produce output. The prompt literally *refuses* to generate a spec on unsound foundations.
- **Audit Before Synthesis (P5):** Even in the synthesis instrument, there's an audit step (B.1) before the synthesis (B.3). The adversarial stance persists to the very end.

### The Question Format

```
- ID: Q-<phase>-<number>
- Purpose: why this decision matters
- Prompt: the question
- Options: 3–7 clear options with implications
- Dependencies: affected sections
- Acceptance Criteria ("Done when…")
- Expected Answer Format
```

**Principles at work:**
- **Artifact Closure (P7):** Each question is itself an artifact — with ID, purpose, options, and acceptance criteria. Even the *questions* have "done when" conditions.
- **Cross-Layer Validation (P9):** The Dependencies field makes explicit that answering one question changes the constraints on others. This is systems thinking applied to the act of planning itself.
- **Epistemic Sequencing (P6):** Questions are organized by phase (Q-DS for Domain & Semantics, Q-DC for Data & Contracts), reinforcing the dependency chain even in the questioning process.

### The Consistency Audit

```
Build a dependency map across sections
(ontology ↔ data model ↔ contracts ↔ flows ↔
 error taxonomy ↔ consistency model ↔ access model ↔ lifecycle).
Validate every declared invariant against flows and data.
Check for undefined terms, conflicting cardinalities,
unreachable states, and incompatible SLO envelopes.
```

**Principles at work:**
- **Cross-Layer Validation (P9):** This is the full expression of the principle. Eight sections checked against each other. Not "review each section" but "check each section against every other section it touches." The dependency map is explicit.

### The Compatibility Matrix

```
Table mapping cross-section compatibility
(ontology↔contracts, flows↔SLOs, consistency↔APIs,
 lifecycle↔observability), noting constraints/invariants
```

**Principles at work:**
- **Cross-Layer Validation (P9):** The capstone. A literal matrix that maps which sections must be compatible with which, and what constraints or invariants govern their relationship. This is the single most powerful structural element across all three prompts.

### The Quality Bar

```
- If uncertain, do not guess — ask for Final Clarifications instead.
```

**Principles at work:**
- **Halt on Uncertainty (P8):** The most transferable principle, stated as a single sentence. This one line encodes epistemic humility structurally: the system would rather pause and surface uncertainty than produce a confident-looking but unsound output.

---

## Summary: Principle Distribution

| Principle | Prompt 1 (Design) | Prompt 2 (Audit) | Prompt 3 (Synthesize) |
|-----------|-------------------|-------------------|-----------------------|
| Ontology First | Primary driver | Reinforced in Phase 1 | Verified in audit |
| Separate, Then Project | Section structure | — | View projections |
| Principled Lossyness | Role + style rules | — | Constraint exclusions |
| Scope by Exclusion | Non-Goals section | Out-of-scope audit | — |
| Audit Before Synthesis | — | Primary driver | Embedded in workflow |
| Epistemic Sequencing | Section order | Phase order | Question organization |
| Artifact Closure | Feature spec format | Done-when criteria | Question format |
| Halt on Uncertainty | — | Critical clarifications | Conditional workflow |
| Cross-Layer Validation | Feature dependencies | Contradiction audit | Compatibility matrix |
| Stakeholder-Aware Views | Multiple section types | — | Final spec views |

Each prompt emphasizes different principles while maintaining all of them. The three together form a complete system — no single prompt carries all ten principles at full strength, but the loop does.
