# Data Science Domain

SA instruments for planning, auditing, and synthesizing data science analyses.

## The Three Instruments

| Instrument | Purpose | Input | Output |
|-----------|---------|-------|--------|
| [Analysis Plan](analysis-plan.md) | Generate a structured, tool-neutral analysis plan | Research/business question + data sources | Methodological plan with constructs, variables, methods, validation, threats |
| [Plan Audit](plan-audit.md) | Adversarially review a plan for methodological gaps | An analysis plan | Audit summary + prioritized drill-down plan with artifacts |
| [Plan Synthesize](plan-synthesize.md) | Interrogate, validate, and produce an executable analysis design | An analysis plan (+ optional answers) | Questionnaire, clarifications, or final low-level analysis design |

## The Loop

```
Research Question
       │
       ▼
  Analysis Plan  ──▶  Plan Audit  ──▶  Plan Synthesize
       │                  │                    │
       │            Gaps found?          Complete &
       │                  │              compatible?
       │                  ▼                    │
       │           Fix & re-plan          Yes: Final Design
       │                                  No:  Clarify & loop
       ▼
  (iterate until sound)
```

## Epistemic Dependency Chain

Each layer depends on the ones before it. Skipping ahead creates rework.

```
Layer 1: Problem & Constructs   → What question? What concepts? What populations?
Layer 2: Data & Measurement     → What data exists? How measured? What quality? What biases?
Layer 3: Analysis & Flows       → What methods? In what order? What decision points?
Layer 4: Validity & Constraints → What threats? What corrections? What confidence?
Layer 5: Reporting & Evolution  → How communicated? What shelf life? What follow-up?
```

**You can't choose a method without knowing the data.** You can't assess validity without knowing the method. You can't write a reporting contract without knowing the confidence levels. Each layer consumes the outputs of the previous one.

## When to Use Each

**Analysis Plan** — When you have a research or business question and need to define what to analyze and why, before anyone opens a notebook. Use this to force clarity on constructs, variables, and evidence standards before method selection begins.

**Plan Audit** — When you have a plan and want to stress-test it for methodological gaps: unmeasured confounders, leakage risks, assumption violations, population mismatches, missing baselines. Use this before investing in execution.

**Plan Synthesize** — When you want to go from a high-level analysis plan to a fully specified, executable design through structured Q&A. Validates that method assumptions are compatible with data properties, conclusions don't exceed confidence levels, and causal claims have credible identification strategies.

## Four People

| Role | In this domain | What they need from this instrument |
|------|---------------|-------------------------------------|
| Domain expert | Statistician / ML theorist | Formal rigor: assumptions stated, diagnostics planned, threats enumerated |
| Protocol designer | Analysis framework designer | Clear method specification: inputs, outputs, decision points, fallbacks |
| Modeler | Data scientist applying the framework | Actionable plan: what to build, in what order, what to check |
| Consumer | Decision-maker acting on results | Trustworthy output: conclusions matched to evidence, caveats explicit |

## Principles Emphasized

This domain most strongly exercises:
- **Ontology First** — constructs and variables defined before any method is discussed
- **Principled Lossyness** — what to analyze and why, never which library to use
- **Halt on Uncertainty** — if data quality is insufficient or assumptions fail, stop and surface it
- **Cross-Layer Validation** — method assumptions checked against data properties, conclusions checked against confidence levels, causal claims checked against identification strategy

## Key Anti-Patterns This Prevents

| Anti-Pattern | How SA Prevents It |
|-------------|-------------------|
| Jumping to methods before defining the question | Section 1 (Problem) must be complete before Section 5 (Analysis Design) |
| Choosing methods that don't match the data | Compatibility matrix checks method assumptions against data properties |
| Causal claims from correlational evidence | Reporting contract explicitly forbids causal language without identification strategy |
| P-hacking / multiple comparison problems | Pre-registration boundary separates committed from exploratory choices |
| Leakage between train and test | Feature boundary rules document what's known at decision time |
| Over-precise conclusions | Decision thresholds and minimum detectable effects force honest precision |
| Results that expire silently | Shelf life and drift monitoring define when results are no longer valid |

## PSuU Connection

The data science instruments directly implement the PSuU methodology:

| PSuU Step | Analysis Plan Section |
|-----------|----------------------|
| 1. System goals identification | Section 1: Problem Statement (objectives) |
| 2. Control parameter identification | Section 5: Analysis Design (method choices, thresholds) |
| 3. Environmental parameter identification | Section 4: Data Characterization (properties you can't control) |
| 4. Metric identification | Section 8: Metrics & Success Criteria |
| 5. Simulation | Section 6: Validation Strategy (sensitivity analysis, cross-validation) |
| 6. Optimal parameter selection | Section 5: Decision thresholds + Section 8: Go/no-go criteria |
