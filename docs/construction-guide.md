# Construction Guide

*How to build Structured Antagonism instruments for any domain*

---

## What You're Building

An SA instrument is not a prompt template. It is a **reasoning constraint** — a structure that forces the producer (human or AI) to think in a specific epistemic order, commit to specific artifacts, and halt when the foundation is unsound.

Every SA instrument has the same deep structure, regardless of domain:

1. A **role** that establishes the perspective and constraints
2. An **ontological commitment phase** that forces definition before action
3. **Layered sections** that follow an epistemic dependency chain
4. **Artifact closures** with verifiable "done when" conditions
5. **Halt gates** that prevent progression on shaky ground
6. **Cross-layer compatibility checks** at the synthesis stage

This guide walks through building each of these for a new domain.

## Step 1: Identify the Four People

Before writing anything, identify the domain's equivalent of the four people in the room:

| Role | Function | What they need |
|------|----------|---------------|
| Domain expert | Gets the deep theory right | Formal precision, structural invariants |
| Protocol designer | Translates theory into operational structure | Expressiveness + correctness |
| Modeler | Uses the structure to describe a specific instance | Clarity, expressiveness, ergonomics |
| Consumer | Needs actionable answers to specific questions | Legible views, actionable signals |

**Example for data science:**
- Domain expert = Statistician / ML theorist
- Protocol designer = The person defining the analysis framework (what kinds of analyses, what validation methods, what standards of evidence)
- Modeler = The data scientist applying the framework to a specific dataset and question
- Consumer = The decision-maker who needs to act on the analysis

**Example for research:**
- Domain expert = Methodologist (the person who understands experimental design theory)
- Protocol designer = The person defining the study protocol
- Modeler = The researcher executing the study within the protocol
- Consumer = The reader, reviewer, or policy-maker who needs to trust the results

Identifying these four roles tells you what views your instrument needs to support and what separations it needs to enforce.

## Step 2: Define the Ontological Core

Every domain has a set of **primitive objects** that must be defined before anything else can be discussed. These are the things that *exist* in the domain — not the things that *happen*.

Ask: What are the nouns of this domain? What are their identity rules? What relationships exist between them? What lifecycle states do they pass through?

| Domain | Example primitives |
|--------|-------------------|
| Software systems | Entities, relationships, identity rules, lifecycle states |
| Data science | Variables, datasets, populations, hypotheses, metrics |
| Research | Constructs, measures, conditions, participants, outcomes |
| Decision-making | Options, criteria, constraints, stakeholders, trade-offs |

**The test:** If someone can discuss behavior/features/methods without having committed to these primitives, your ontological phase is too weak. Tighten it until skipping it is impossible.

## Step 3: Establish the Epistemic Dependency Chain

Identify the layers of your domain and their dependency order. Each layer should depend on the ones before it, and it should be *impossible* to meaningfully fill out a later layer without having completed the earlier ones.

**The general pattern:**

```
Layer 1: Domain & Semantics     — What exists? What do terms mean?
Layer 2: Data & Contracts       — What is captured? What are the interfaces?
Layer 3: Behavior & Flows       — What happens? In what order? Under what conditions?
Layer 4: Quality & Constraints  — How well must it work? What are the boundaries?
Layer 5: Lifecycle & Evolution   — How does it change over time? What's the exit strategy?
```

**For data science, this becomes:**

```
Layer 1: Problem & Constructs   — What question? What constructs? What populations?
Layer 2: Data & Measurement     — What data? How measured? What quality? What biases?
Layer 3: Analysis & Flows       — What methods? In what order? What decision points?
Layer 4: Validity & Constraints — What threats to validity? What confidence thresholds?
Layer 5: Reporting & Evolution  — How communicated? What follow-up? What shelf life?
```

**For research:**

```
Layer 1: Question & Constructs  — What hypothesis? What constructs? What's the theory?
Layer 2: Measurement & Design   — How measured? What design? What controls?
Layer 3: Procedure & Flows      — What protocol? What sequence? What decision rules?
Layer 4: Validity & Power       — What threats? What power? What sensitivity?
Layer 5: Reporting & Replication — How reported? How replicated? What archival?
```

**The test:** Try to fill out Layer 3 without Layer 1. If you can do it without feeling lost, your dependency chain is too loose.

## Step 4: Build the Three Instruments

Every SA domain needs three instruments that form a loop:

### Instrument 1: The Design Prompt

This is the generative instrument. It forces the production of a structured artifact that follows the epistemic dependency chain.

**Structure:**

```
ROLE: [Perspective and constraints]

INPUTS: [What the user provides — and what to infer if missing]

OUTPUT FORMAT:
  Section 1: [Ontological core — entities, relationships, identity]
  Section 2: [Boundaries — in-scope, out-of-scope, non-goals]
  Section 3: [Layer 1 content]
  Section 4: [Layer 2 content]
  ...
  Section N: [Assumptions & open questions]

STYLE RULES:
  - [Principled lossyness — what to exclude and why]
  - [Artifact format — bullets, tables, testable statements]
  - [Audience constraint — who this view is for]
```

**Key design choices:**
- The ROLE must constrain perspective. "Senior systems architect" is different from "independent reviewer" — same domain, different adversarial stance.
- INPUTS should have sensible defaults with explicit flagging when assumptions are made.
- Each section must be a view — serving a specific audience or answering a specific kind of question.
- STYLE RULES enforce principled lossyness: "describe WHAT, never HOW" or "state behavioral outcomes, not implementation mechanisms."

### Instrument 2: The Audit Prompt

This is the adversarial instrument. It takes the output of Instrument 1 and stress-tests it.

**Structure:**

```
ROLE: [Independent reviewer — different perspective from Instrument 1]

TASK: Audit the provided [artifact]. First diagnose, then plan.

INPUT: [The artifact from Instrument 1]

OUTPUT FORMAT:
  Audit Summary:
    - Gaps found
    - Ambiguities found
    - Contradictions found
    - Unstated assumptions surfaced

  Drill-Down Plan:
    Phase 1: [Layer 1 artifacts — with done-when criteria]
    Phase 2: [Layer 2 artifacts — with done-when criteria]
    ...

  Critical Clarifications: [Questions that block progress]
```

**Key design choices:**
- The ROLE must be adversarial but constructive — "independent reviewer," not "critic."
- The audit summary forces diagnosis before prescription.
- Every drill-down step must have: a verb, a named artifact, and a "done when" condition.
- Critical clarifications are halt gates — they block progress until answered.

### Instrument 3: The Synthesis Prompt

This is the conditional instrument. It either produces the final artifact or halts and asks for more.

**Structure:**

```
ROLE: [Auditor and synthesizer — both perspectives]

WORKFLOW:
  A) If answers NOT provided:
     → Produce breadth questionnaire organized by layers
     → Each question has: ID, purpose, prompt, options, dependencies, done-when
     → STOP and wait

  B) If answers PROVIDED:
     1) Consistency & completeness audit
        → Build dependency map across sections
        → Check for contradictions, undefined terms, unreachable states
     2) If ANY gap or incompatibility:
        → Output final clarification questions ONLY (no artifact)
        → STOP and wait
     3) If COMPLETE and COMPATIBLE:
        → Output final artifact
        → Include compatibility matrix (section X ↔ section Y)

QUALITY BAR:
  - If uncertain, do not guess — ask
  - Each section must align with all others
  - Contradictions are not allowed
```

**Key design choices:**
- The conditional workflow is the most important structural move. It literally refuses to produce output on shaky ground.
- The compatibility matrix at the end catches cross-layer contradictions.
- The question format includes dependency tracking — answering one question changes constraints on others.
- "If uncertain, do not guess — ask" is the quality bar that makes everything else work.

## Step 5: Define the Compatibility Matrix

For Instrument 3, define which sections must be checked against each other. This is domain-specific:

**Software systems:**
| Check | Against |
|-------|---------|
| Ontology | Contracts |
| Flows | SLOs |
| Consistency model | APIs |
| Lifecycle | Observability |

**Data science:**
| Check | Against |
|-------|---------|
| Constructs | Measurements |
| Analysis methods | Data properties |
| Validity threats | Method choices |
| Conclusions | Confidence levels |

**Research:**
| Check | Against |
|-------|---------|
| Hypotheses | Measures |
| Design | Power analysis |
| Protocol | Ethics constraints |
| Analysis plan | Pre-registration |

## Step 6: Write the Anti-Pattern Guards

Every instrument should include explicit style rules that prevent common failure modes:

| Anti-pattern | Guard |
|-------------|-------|
| Conflating layers | "Describe WHAT, never HOW" |
| Vague steps | "Each step must name an artifact and a done-when condition" |
| Scope creep | "Include Non-Goals as a first-class section" |
| Premature action | "If gaps exist, output clarifications ONLY — no artifact" |
| Stakeholder confusion | "This view is for [audience] — exclude [other concerns]" |
| Confabulation | "If uncertain, do not guess — ask" |

## Validation Checklist

Before considering an SA instrument complete, verify:

- [ ] Can someone fill out Layer 3 without having done Layer 1? If yes, tighten the dependency chain.
- [ ] Does every step produce a named artifact with a "done when"? If not, the step is a wish, not a step.
- [ ] Are there explicit non-goals? If not, scope is undefined.
- [ ] Does the synthesis instrument have halt gates? If not, it will produce output on unsound foundations.
- [ ] Is there a compatibility matrix? If not, cross-layer contradictions will hide.
- [ ] Are the style rules enforcing principled lossyness? If not, views will bleed into each other.
- [ ] Can you identify all four people? If not, the views may not serve the right audiences.

## Example: Building a Data Science SA Instrument

See [`domains/data-science/`](../domains/data-science/) for the complete implementation. Here's the thinking that produced it:

1. **Four people:** Statistician (domain expert), analysis framework designer (protocol designer), data scientist (modeler), decision-maker (consumer).

2. **Ontological core:** Variables, datasets, populations, hypotheses, metrics, assumptions.

3. **Dependency chain:** Problem → Data → Methods → Validity → Reporting.

4. **Design instrument:** Forces definition of the question and constructs before any method is discussed. Excludes tool/library choices (principled lossyness for the "what not how" layer).

5. **Audit instrument:** Treats the analysis plan as a hypothesis. Checks for: confounded variables, selection bias, multiple comparison problems, leakage, unstated assumptions about data distributions.

6. **Synthesis instrument:** Conditional on whether validity threats have been addressed. Produces the final analysis plan only when the method choices are compatible with the data properties, the confidence levels are compatible with the conclusions, and the reporting format serves the decision-maker.
