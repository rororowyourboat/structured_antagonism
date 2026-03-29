# Analysis Plan — Design Instrument

*Generates a tool-neutral, methodologically rigorous data science analysis plan.*

---

## Full Version

```
ROLE: Senior data scientist and methodologist. Produce an emoji-free, tool-neutral ANALYSIS PLAN that describes ONLY the analytical approach — what to investigate, what to measure, and what constitutes evidence. Exclude tool/library choices (no pandas, sklearn, R packages), infrastructure details, team assignments, timelines, and code. No filler.

INPUTS (use provided; otherwise infer sensible defaults and flag under Assumptions):
- Project: <PROJECT_NAME>
- Question: <RESEARCH_QUESTION or BUSINESS_QUESTION>
- Data sources: <DATA_SOURCES>
- Stakeholder context: <WHO_WILL_ACT_ON_RESULTS>
- Constraints (regulatory/ethical/resource): <CONSTRAINTS>

OUTPUT FORMAT (Markdown, exact sections):

# <PROJECT_NAME> — Analysis Plan

## 1. Problem Statement (What & Why)
- One-sentence definition of what this analysis aims to determine.
- Objectives (3–5 specific, measurable analytical goals).
- Non-Questions (what this analysis explicitly does NOT attempt to answer).
- Decision context: what action will be taken based on results, and by whom.

## 2. Constructs & Variables
- Core constructs (abstract concepts being investigated — e.g., "customer engagement," "treatment effect," "system reliability").
- Operationalization: how each construct maps to observable, measurable variables. For each variable:
  - Name, definition, unit of measurement.
  - Type: continuous, categorical, ordinal, binary, time-series, text, etc.
  - Role: outcome/response, predictor/feature, confounder, mediator, moderator, instrumental.
- Variable relationships: hypothesized causal or associational structure (directed, undirected, confounded).

## 3. Population & Sampling
- Target population: who/what the analysis aims to generalize to.
- Study population: who/what is actually represented in the available data.
- Sampling mechanism: how data was collected (random, convenience, stratified, census, observational, experimental).
- Known selection biases: systematic differences between target and study population.
- Unit of analysis: individual observation, aggregated group, time period, etc.
- Inclusion/exclusion criteria (applied before any analysis).

## 4. Data Characterization
- For each data source:
  - Name, origin, collection period, refresh frequency.
  - Grain: what one row represents.
  - Volume: approximate row/column count.
  - Known quality issues: missingness patterns, measurement error, truncation, censoring, duplication.
  - Joining logic: how this source links to others (keys, temporal alignment, fuzzy matching).
- Data freshness requirements: how stale can data be before conclusions are invalid?
- Privacy/sensitivity classification per field (PII, PHI, financial, etc.).

## 5. Analysis Design
- Analysis type: exploratory (hypothesis-generating), confirmatory (hypothesis-testing), predictive (forecasting), causal (effect estimation), or descriptive (summarization).
- For each analytical objective (from Section 1):
  - Method class: the family of approaches (e.g., "regression," "survival analysis," "clustering," "A/B test," "time series decomposition") — no specific implementations.
  - Assumptions required by this method class (e.g., linearity, independence, normality, stationarity, exchangeability).
  - How assumptions will be checked (diagnostic procedures, not tools).
  - Primary metric(s): what quantity answers the question (e.g., "coefficient estimate," "classification accuracy," "hazard ratio").
  - Decision threshold: what value of the primary metric constitutes an actionable result.
  - Comparison/baseline: what the result is compared against (null hypothesis, naive model, prior period, control group).

## 6. Validation Strategy
- Holdout/splitting strategy: how data is partitioned for training vs. evaluation (temporal split, k-fold, leave-one-out, etc.).
- Leakage prevention: what information must be excluded from features to prevent train-test contamination.
- Multiple comparison correction: if testing multiple hypotheses, how to control false discovery rate.
- Sensitivity analysis plan: what parameters or assumptions to vary and what constitutes robustness.
- Pre-registration: which analytical choices are committed to before seeing results vs. which are exploratory.

## 7. Threat Model (Validity)
- Internal validity threats: confounders, reverse causality, selection bias, survivorship bias, measurement error, missing data mechanism (MCAR/MAR/MNAR).
- External validity threats: population mismatch, temporal drift, domain shift, Simpson's paradox potential.
- Statistical validity threats: multiple testing, p-hacking, overfitting, specification searching, garden of forking paths.
- For each identified threat: severity (high/medium/low) and planned mitigation.

## 8. Metrics & Success Criteria
- Primary metrics: the quantities that directly answer the research question.
- Secondary metrics: supporting evidence (e.g., model diagnostics, calibration, fairness measures).
- Guardrail metrics: quantities that must NOT degrade (e.g., "latency must stay below X," "no subgroup accuracy below Y").
- Minimum detectable effect / required precision: what effect size or confidence width is needed for the result to be actionable.
- Go/no-go criteria: under what conditions the analysis is considered conclusive vs. inconclusive.

## 9. Reporting & Communication
- Primary audience and their statistical literacy level.
- Key deliverable format: report, dashboard, presentation, decision memo, automated alert.
- What must be communicated: point estimates, uncertainty bounds, caveats, limitations.
- What must NOT be communicated: misleading precision, causal claims from correlational evidence, results without context.
- Shelf life: how long are these results valid before the analysis should be refreshed?

## 10. Assumptions & Open Questions
- Assumptions made (with which section they affect).
- Open questions to resolve before analysis begins, with priority.

STYLE RULES
- Short, testable bullets; avoid narrative prose.
- Describe WHAT to analyze and WHY; never WHICH TOOL to use or HOW to code it.
- No emojis, no team/process language, no timelines/estimates/library names.
- Every metric must have a decision threshold or "why measure it" justification.
- Every method choice must list its assumptions and how they'll be checked.
```

---

## Compact Version

```
Write an emoji-free, concise ANALYSIS PLAN that describes WHAT to analyze and WHY, not which tools to use or how to code it. No filler.

INPUTS:
- Project name: <PROJECT_NAME>
- Question the analysis answers: <QUESTION>
- Available data sources: <DATA_SOURCES>
- Key constraints (regulatory/ethical/resource): <CONSTRAINTS>

OUTPUT (Markdown):

# <PROJECT_NAME> — Analysis Plan

## 1. Problem Statement
- One-sentence definition of what this analysis determines.
- Objectives (3–5 measurable analytical goals).
- Non-Questions (what this analysis explicitly does NOT answer).

## 2. Constructs & Variables
- Core constructs (abstract concepts → measurable variables).
- Variable roles: outcome, predictor, confounder, moderator.
- Hypothesized relationships (directed/undirected).

## 3. Population & Sampling
- Target vs. study population.
- Sampling mechanism and known biases.
- Unit of analysis and inclusion/exclusion criteria.

## 4. Data Characterization
- Per source: grain, volume, quality issues, joining logic.
- Freshness requirements and sensitivity classification.

## 5. Analysis Design
- Analysis type (exploratory/confirmatory/predictive/causal/descriptive).
- Per objective: method class, assumptions, how checked, primary metric, decision threshold.

## 6. Validation Strategy
- Splitting strategy and leakage prevention.
- Multiple comparison correction and sensitivity analysis plan.

## 7. Threat Model
- Internal, external, and statistical validity threats.
- Per threat: severity and mitigation.

## 8. Success Criteria
- Primary, secondary, and guardrail metrics.
- Minimum detectable effect and go/no-go criteria.

## 9. Reporting
- Audience, deliverable format, shelf life.
- What to communicate and what NOT to communicate.

## 10. Assumptions & Open Questions

STYLE:
- Bullets over prose; terse, testable statements.
- Describe analysis approach and rationale only; no tool/library names.
```
