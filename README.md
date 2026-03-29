# Structured Antagonism

**A thinking methodology for reasoning about complex domains where ambiguity is dangerous and assumptions are expensive.**

---

Structured Antagonism (SA) is the discipline of reasoning adversarially against your own assumptions, within a structure that makes the adversarial process productive rather than destructive.

It emerged from a specific observation: the best system design prompts don't work because they tell an AI what to write. They work because they **constrain the space of acceptable reasoning** — encoding structural properties of good thinking directly into the prompt's architecture. The same properties that make a design review rigorous, a research plan sound, or a data analysis trustworthy.

SA is not a prompt engineering framework. Prompts are one implementation surface. The principles apply equally to writing design docs, structuring research plans, running architecture reviews, or building decision frameworks for any domain where multiple stakeholders need different views of the same underlying reality.

## The Problem SA Solves

Complex domains have a recurring failure mode: **layers collapse into each other.** Infrastructure gets tangled with models. Authoring gets tangled with visualization. The person building the theory gets conflated with the person consuming its outputs. When these concerns collapse, the tools become brittle, the understanding becomes shallow, and the practices become unreliable.

Most planning and specification artifacts fail not because any single section is wrong, but because:

- Sections contradict each other silently
- Scope creep hides inside ambiguity
- Later steps proceed before earlier ones are sound
- Vague verbs ("explore options," "assess feasibility") never resolve into commitments
- A view optimized for one stakeholder actively misleads another

SA prevents these failures by making them structurally impossible.

## The Ten Principles

1. **Ontology First** — Define what exists before describing what happens. You don't get to discuss behavior until you've committed to entities, relationships, and identity rules.

2. **Separate, Then Project** — Build the base representation first; derive views from it. Never build "the view" — build the thing from which all views can be projected.

3. **Principled Lossyness** — Every view hides things deliberately. A model that captures everything is not a model — it's a worse copy of reality. Name what you're hiding and why.

4. **Scope by Exclusion** — Non-goals and boundaries are first-class outputs, not afterthoughts. What you exclude defines the system as much as what you include.

5. **Audit Before Synthesis** — Treat every input as a hypothesis to be stress-tested, not a draft to be polished. Diagnose before prescribing.

6. **Epistemic Sequencing** — Establish dependency chains between layers. Domain before contracts. Contracts before flows. Flows before SLOs. Don't let later steps proceed until earlier ones are sound.

7. **Artifact Closure** — Every step produces a named artifact with a verifiable "done when" condition. You cannot ship a vague concept. You cannot compile an ambiguity.

8. **Halt on Uncertainty** — If the foundation is unsound, stop and surface it. Never paper over gaps with confident-sounding prose. The system should prefer silence over confabulation.

9. **Cross-Layer Validation** — Internal coherence within a section is necessary but not sufficient. Sections must be coherent with each other. Build compatibility matrices, not just checklists.

10. **Stakeholder-Aware Views** — The same system looks different to different people. A mathematician's block diagram is not a better version of a stakeholder's dashboard — it's a different projection entirely. Build for multiple projections, not consensus on a single narrative.

## The Underlying Structure

There is a formal invariant beneath SA that appears across multiple domains:

**A generative process + an evaluative process operating under different objectives, coupled into a feedback loop.**

Quality improvement comes not from either component alone but from the tension at their interface. SA's Design → Audit → Synthesize loop is a specific instantiation of this pattern, with structural safeguards (epistemic sequencing, halt gates, role separation) that address the known failure modes.

This pattern is load-bearing in:

- **Game theory** — GANs are literally a minimax game between generator and discriminator. When convergence works, the adversarial tension drives the generator to model the target distribution. When it fails (mode collapse), the evaluator and generator have collapsed into the same information channel.

- **Evolutionary biology** — Competitive coevolution (the Red Queen hypothesis) drives open-ended complexity through arms race dynamics. The key condition: the evaluator must have access to orthogonal information. If predator and prey share the same model of the world, they cycle without progress.

- **Argumentation theory** — Dung's abstract argumentation frameworks (1995) define stable extensions as fixed-point concepts: sets of arguments that are internally consistent and defend against all attacks. SA's halt gates are the procedural encoding of this — the system refuses to produce output until a stable extension is reached.

- **Multi-agent AI** — Google's AI Co-Scientist and DeepMind's AlphaEvolve use specialized agent coalitions (generation, reflection, ranking, evolution) locked in iterative competition. Hypotheses compete in Elo-based tournaments. The more compute spent on adversarial evaluation, the better the outputs.

The synthesis gap — the open theoretical question — is precisely *when* adversarial processes converge to genuine quality versus confident consensus around the wrong answer. GAN mode collapse and LLM sycophancy are the same failure mode at different abstraction levels. SA's structural safeguards (role separation, cross-layer validation, halt on uncertainty) are designed to prevent this degeneration.

## Intellectual Roots

SA draws from six sources:

- **"The Map is Not the Territory, But You Still Need a Good Map"** — An essay on building tools at the boundary of math, software, and understanding. Introduces the concept of "four people in the room" (domain expert, protocol designer, modeler, stakeholder) who need radically different things from the same underlying reality. Also grounds the formal substrate of antagonism across game theory, coevolution, argumentation theory, and multi-agent AI. ([Read it](docs/philosophy.md))

- **Parameter Selection Under Uncertainty (PSuU)** — BlockScience's methodology for configuring complex ecosystems: Goals → Parameters → Metrics → Simulation → Selection. Each step depends on the previous. Trade-offs are explicit objects, not hidden compromises. ([Read it](docs/psuu.md))

- **Compositional game theory and MSML** — The practical experience of building tools that force ontological commitment. "Building tools forces ontological commitment. You cannot ship a vague concept. You cannot compile an ambiguity."

- **Minimax game theory and GANs** — The formal grounding for adversarial quality improvement. Goodfellow (2014) showed that generator-discriminator tension, when properly structured, converges on outputs neither process could produce alone. The failure modes (mode collapse, vanishing gradients) map directly to SA's failure modes (sycophancy, layer collapse).

- **Competitive coevolution** — The Red Queen hypothesis and the evolutionary computation literature on when arms races produce genuine improvement versus cycling. The formal condition — evaluator must access orthogonal information — is why SA enforces role separation between designer, auditor, and synthesizer.

- **Abstract argumentation frameworks** — Dung (1995) and the dialectical logic tradition from Aristotle through Hegel. Stable extensions as fixed-point concepts provide the formal analogue of SA's convergence criterion: the output must survive all attacks and be internally consistent.

## Reading Order

**Start here:** [The Manifesto](docs/manifesto.md) — what SA is, the epistemic core, the ten principles, the core loop.

**The source essay:** [The Map is Not the Territory](docs/philosophy.md) — the original essay on separation of concerns, stakeholder views, and building tools at the boundary of math and software. Includes the formal substrate of antagonism across game theory, coevolution, argumentation theory, and multi-agent AI.

**The methodology roots:** [Parameter Selection Under Uncertainty](docs/psuu.md) — BlockScience's PSuU framework that provides the backbone for epistemic sequencing.

**The principles in depth:** [Ten Principles](meta/principles.md) with expanded examples and counter-examples. [Anti-Patterns](meta/anti-patterns.md) — the ten failure modes SA prevents.

**Prompt architecture:** [Anatomy of an SA Prompt](docs/anatomy.md) — dissecting which principle each structural choice embodies. [Construction Guide](docs/construction-guide.md) — how to build SA instruments for a new domain.

**Working prompts:** The [`domains/`](domains/) directory contains complete Design → Audit → Synthesize prompt loops for [software systems](domains/software-systems/), [data science](domains/data-science/), and [research](domains/research/) (stub).

## The Core Loop

Every SA workflow follows the same three-phase loop:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   DESIGN    │────▶│    AUDIT     │────▶│   SYNTHESIZE    │
│             │     │              │     │                 │
│ Ontology    │     │ Gaps?        │     │ Complete?       │
│ Boundaries  │     │ Ambiguities? │     │ Compatible?     │
│ Behaviors   │     │ Contradictions│    │ Cross-validated?│
│ Views       │     │ Assumptions? │     │                 │
└─────────────┘     └──────┬───────┘     └────────┬────────┘
                           │                      │
                           │ If unsound            │ If gaps remain
                           ▼                      ▼
                    ┌──────────────┐        ┌──────────────┐
                    │  HALT & ASK  │        │  HALT & ASK  │
                    └──────────────┘        └──────────────┘
```

The halt gates are not failure states. They are the methodology working correctly — surfacing uncertainty rather than burying it.

## Current Research Direction

The philosophy and prompt instruments above are the first layer. The active research direction is to make the structural claims *computationally verifiable* by encoding specific instances of structured antagonism in the GDS-Core compositional game theory framework and comparing them via semantic web technologies.

The three systems under study:

- **Socratic elenchus** (Euthyphro) — pursuit-evasion antagonism with accumulating commitment store, encoded as `CorecursiveLoop` (cross-timestep temporal iteration)
- **GANs** — symmetric antagonism with within-timestep gradient feedback, encoded as `FeedbackLoop` (contravariant)
- **AI Co-Scientist** — hierarchical antagonism with nested temporal loops (`CorecursiveLoop` inside `CorecursiveLoop`)

The claim to test: different classes of antagonistic systems have different composition topologies in GDS, and the three-axis combination (operator class, observation symmetry, commitment enforcement) determines convergence dynamics and failure modes.

All three models are compiled, verified (63/64 checks passed), and structurally compared via SPARQL on a merged RDF graph. The Euthyphro dialogue is annotated with a five-type commitment store taxonomy (commitment, assertion, presupposition, conditional_commitment, derivation) across 232 speaker-change turns.

See the [research journal](docs/research-journal.md) for the full development of this direction.

## References

### Primary Sources

- Plato, *Euthyphro*. Benjamin Jowett translation (Project Gutenberg #1642). [`references/euthyphro.txt`](references/euthyphro.txt)

### Formal Frameworks

- Goodfellow, I. et al. (2014). "Generative Adversarial Networks." *arXiv:1406.2661*.
- Ghani, N., Hedges, J., Winschel, V., & Zahn, P. (2018). "Compositional Game Theory." *arXiv:1603.04641*.
- Dung, P. M. (1995). "On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning, Logic Programming, and n-Person Games." *Artificial Intelligence*, 77(2), 321-357.
- Zargham, M. & Shorish, J. (2022). "Generalized Dynamical Systems." Working paper, BlockScience.

### Multi-Agent AI Systems

- Gottweis, J. et al. (2025). "Towards an AI Co-Scientist." Google DeepMind.
- AlphaEvolve (2025). Google DeepMind.
- Leibo, J. Z. et al. (2021). "Scalable Evaluation of Multi-Agent Reinforcement Learning with Melting Pot." *ICML 2021*.

### Euthyphro Scholarship

- Ebrey, D. (2017). "Identity and Explanation in the *Euthyphro*." *Oxford Studies in Ancient Philosophy*, 52, 77-105. [`references/ebrey_2017_identity_and_explanation.pdf`](references/ebrey_2017_identity_and_explanation.pdf)
- Sharvy, R. (1972). "Euthyphro 9d-11b: Analysis and Definition in Plato and Others." *Nous*, 6, 119-137.
- Judson, L. (2010). "Carried Away in the *Euthyphro*." In D. Charles (ed.), *Definition in Greek Philosophy*, Oxford, 31-61.
- Wolfsdorf, D. (2005). "'Euthyphro' 10a2-11b1: A Study in Platonic Metaphysics and its Reception since 1960." *Apeiron*, 38, 1-71.
- Evans, M. (2012). "Lessons from *Euthyphro* 10a-11b." *Oxford Studies in Ancient Philosophy*, 42, 1-38.

### Argumentation Theory

- Walton, D. & Krabbe, E. (1995). *Commitment in Dialogue*. SUNY Press.
- Hamblin, C. L. (1970). *Fallacies*. Methuen.

## License

MIT

## Contributing

This is an open methodology. If you build SA instruments for a new domain, open a PR. The [construction guide](docs/construction-guide.md) tells you how.
