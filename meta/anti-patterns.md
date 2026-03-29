# Anti-Patterns

*What Structured Antagonism prevents — and why these failures are so common*

---

## 1. The Premature Feature Spec

**What it looks like:** Detailed feature specifications written before the domain model exists. Flows reference entities that haven't been defined, use terms that haven't been committed to, and assume relationships that haven't been established.

**Why it happens:** Features feel like progress. Domain modeling feels like overhead. The team wants to show something concrete to stakeholders, so they skip to the interesting part.

**What goes wrong:** Every feature spec is a coin flip on undefined terms. When the domain model is eventually forced into existence (by implementation), half the feature specs need rewriting because they assumed the wrong ontology.

**SA principle violated:** Ontology First (P1), Epistemic Sequencing (P6)

---

## 2. The Universal Document

**What it looks like:** A single artifact that tries to serve every stakeholder — engineering, product, security, compliance, executives. It contains API schemas next to user stories next to threat models next to one-page summaries.

**Why it happens:** Creating multiple documents feels like duplication. "Why can't we just have one source of truth?"

**What goes wrong:** Every reader wades through 80% irrelevant content to find the 20% they need. The document becomes too long to maintain, so it drifts from reality. Worse: sections optimized for one audience actively mislead another. The engineer reads the executive summary and thinks the scope is smaller than it is. The exec reads the technical detail and thinks the complexity is greater than it is.

**SA principle violated:** Stakeholder-Aware Views (P10), Separate Then Project (P2), Principled Lossyness (P3)

---

## 3. The Vague Plan

**What it looks like:** A list of steps like "Research caching options," "Explore authentication approaches," "Assess scaling strategies." No artifacts named. No completion criteria. No way to tell when a step is done.

**Why it happens:** Specificity feels like commitment, and commitment feels risky before you've done the research. So the plan stays vague to keep options open.

**What goes wrong:** The plan never resolves. "Research caching options" runs for two weeks and produces a Slack conversation, three bookmarks, and a vague preference. No artifact exists that can be reviewed, challenged, or built upon. The step ends when someone gets bored, not when it's done.

**SA principle violated:** Artifact Closure (P7)

---

## 4. The Polished Contradiction

**What it looks like:** A beautifully written spec where each section is internally coherent, well-structured, and detailed — but sections contradict each other. The domain model defines three states; a feature flow references four. The API spec promises consistency; the architecture section describes eventual consistency. The retention policy says 30 days; the audit section requires 7 years.

**Why it happens:** Sections are written by different people, or at different times, or with different assumptions. Each section is reviewed in isolation. No one checks sections against each other.

**What goes wrong:** The contradictions surface during implementation, when fixing them is expensive. Or worse: they surface in production, when fixing them is an incident.

**SA principle violated:** Cross-Layer Validation (P9)

---

## 5. The Confident Guess

**What it looks like:** A spec or plan that proceeds confidently through areas of genuine uncertainty. Assumptions are unstated. Ambiguities are resolved by picking whatever seems reasonable. Gaps are filled with plausible-sounding defaults.

**Why it happens:** Uncertainty feels like incompetence. Admitting "I don't know" feels like the plan is failing. And with LLMs, the temptation is even stronger — the model will produce fluent, confident text regardless of whether the underlying reasoning is sound.

**What goes wrong:** The output looks authoritative but is built on sand. Downstream decisions trust the confident prose and inherit the unstated assumptions. When the assumptions turn out to be wrong, the blast radius includes everything built on them.

**SA principle violated:** Halt on Uncertainty (P8)

---

## 6. The Scope Ghost

**What it looks like:** A spec that describes what the system does but never states what it doesn't do. Boundaries are implied but never explicit. Edge cases are unaddressed. The question "does it handle X?" has no clear answer.

**Why it happens:** Stating non-goals feels negative, defensive, or premature. "We'll figure out the boundaries as we go."

**What goes wrong:** Stakeholders fill the gaps with their own assumptions. Engineering fills them with their own interpretations. Six months later, three people have three different understandings of what's in scope — and all of them feel betrayed when the system doesn't do what they assumed.

**SA principle violated:** Scope by Exclusion (P4)

---

## 7. The Skip-Ahead

**What it looks like:** A team that jumps to choosing a database before defining the data model. A data scientist who picks a statistical test before examining the data distribution. A researcher who designs the protocol before articulating the hypothesis.

**Why it happens:** Later steps feel more concrete and more fun. Earlier steps feel abstract and ungrateful. And often there's pressure to "show progress" in terms of implementation decisions rather than foundational ones.

**What goes wrong:** The later decision constrains the earlier one in ways that weren't intentional. The database choice forces a data model shape. The statistical test assumes a distribution. The protocol assumes a hypothesis. When the foundation is eventually examined, it turns out to be incompatible with the decisions already made — and the rework is expensive.

**SA principle violated:** Epistemic Sequencing (P6)

---

## 8. The Synthetic Unanimity

**What it looks like:** A single narrative that claims to represent "the team's view" or "the system's purpose" — erasing the real tensions between stakeholder perspectives. Trade-offs are hidden. Competing priorities are merged into bland compromise language.

**Why it happens:** Consensus feels like progress. Disagreement feels like dysfunction. The path of least resistance is to find language that everyone can nod at, even if it means different things to different people.

**What goes wrong:** The disagreement doesn't go away — it goes underground. It resurfaces during implementation as "interpretation differences" that are actually unresolved conflicts. The bland consensus language provides no guidance when real trade-offs must be made.

**SA principle violated:** Stakeholder-Aware Views (P10), Principled Lossyness (P3)

---

## 9. The Improvement Reflex

**What it looks like:** Receiving a draft or input and immediately starting to improve it — adding detail, refactoring structure, polishing prose — without first diagnosing what's actually wrong.

**Why it happens:** Improvement feels productive. Diagnosis feels slow. The draft is right there, and it's so tempting to just start making it better.

**What goes wrong:** You improve the wrong things. You polish a section that's internally beautiful but contradicts three others. You add detail to a feature that shouldn't exist. You refactor the structure of a spec that has the right structure but the wrong content.

**SA principle violated:** Audit Before Synthesis (P5)

---

## 10. The Infinite Model

**What it looks like:** A specification or model that tries to capture every possible detail, every edge case, every stakeholder concern. Nothing is excluded. Nothing is simplified. The document grows without bound.

**Why it happens:** Thoroughness is rewarded. Excluding something feels like cutting corners. "What if someone needs this detail later?"

**What goes wrong:** The model becomes Borges' map — the same size as the territory, and therefore useless. No one reads it. No one maintains it. It drifts from reality within weeks. The attempt to hide nothing means nothing is foregrounded — the critical insights drown in the noise.

**SA principle violated:** Principled Lossyness (P3), Separate Then Project (P2)
