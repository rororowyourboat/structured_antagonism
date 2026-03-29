# The Map is Not the Territory, But You Still Need a Good Map

*Reflections on building tools at the boundary of math, software, and understanding*

---

There is a confusion that keeps showing up in complex technical projects, and I've started to think it isn't accidental. It's structural. It's what happens when you try to build software for domains that are themselves still being understood.

The confusion is this: **we collapse layers that need to be kept separate.** Infrastructure gets tangled with models. Authoring gets tangled with visualization. Domain experts get conflated with protocol designers. The person building the theory gets tangled up with the person consuming its outputs. And when these concerns collapse into each other, the tools become brittle, the understanding becomes shallow, and the practices become unreliable.

I want to try to articulate what I think is actually going on — using our work on MSML and compositional game theory as the grounding example — and then step back and say something more general about what data, knowledge, and representation actually are, and why getting this right matters.

---

## Four People in the Room

When we work on something like MSML — a mathematical specification and modeling library for complex systems — there are roughly four kinds of people involved, and they need radically different things from the same underlying reality.

**The domain experts** are the ones who invented the formalisms in the first place. The dynamical systems theorist. The game theorist. The software architect who understands compositional structure. These people work at the frontier of their disciplines, and their job is to get the deep theory right — not to make it usable, but to make it true. They think in proofs, in category theory, in structural invariants that hold regardless of any particular application. Their knowledge is powerful precisely because it is general and often deliberately impractical.

**The protocol designer** is someone different, and this distinction matters enormously. The protocol designer is not necessarily the one who invented open games or dynamical systems theory — but they understand enough of both to wire them together into something coherent and operational. In our work, this is the person building the block diagram algebra, the wiring logic, the type system — authoring the grammar that others will write in. They are translators: taking formal knowledge from multiple domain experts and distilling it into a protocol that is precise enough to be implemented and expressive enough to be useful. They face in two directions at once, and the tension is productive. This role is often underappreciated because it doesn't look like pure research and it doesn't look like pure engineering — but it is the hinge on which everything else turns.

**The modeler** picks up the protocol and uses it to describe a specific system — a market mechanism, a coalition formation protocol, a resource exchange game. They are not inventing the algebra; they are writing in it. They need expressive power and clarity. They need to be able to say "this agent observes this, decides this, produces that" without having to re-derive the underlying category theory every time they sit down to work. The cleaner the protocol designer's work, the more the modeler can focus on their actual problem rather than fighting the tooling.

**The business stakeholder or consumer of insights** doesn't care about the algebra at all. They have a question: is this mechanism incentive-compatible? Where does the system break down? What happens when I change this parameter? They need a view — a semantically rich, carefully curated window into the model's outputs that is legible to them and actionable for their decisions.

These four people are deeply interconnected. The modeler's work is only as good as the protocol the protocol designer built. The protocol is only as sound as the domain theory it draws from. The stakeholder's insight is only as trustworthy as the modeler's fidelity to the real system. But here is the critical point: **if we don't enforce clean separations between their concerns, we cannot build reliable tools for any of them.** The modeler shouldn't have to understand the compiler internals. The stakeholder shouldn't have to read the Pydantic schemas. The protocol designer shouldn't have to re-derive the category theory every time they want to add a new block type. And the domain expert shouldn't have to think about dashboard UI when refining the algebra.

Each of these is a different kind of knowledge. Conflating them doesn't make anyone smarter — it makes everyone slower.

This is not just good software engineering hygiene. It reflects something deeper about the structure of knowledge itself.

---



## Data, Representation, and the Problem of Views

Let's step back. The world is messy. Reality is dense, continuous, and doesn't come pre-labeled. The first act of any modeling discipline is **capture** — deciding what to record, and in what form. But capture is never innocent. To capture anything, you need a schema: a prior belief about what kinds of things exist, what properties they have, and how they relate. Your ontology precedes your data.

This is the first layer: **raw data shaped by a schema**, which is itself shaped by the questions you're trying to answer.

From that captured data, you build a **base representation** — a structured model that holds enough information to answer the questions multiple stakeholders might ask. This base representation is the hardest thing to get right, because it faces pressure from two directions simultaneously. It must be rich enough to support multiple views. But it cannot be infinitely expressive, because then it becomes equivalent to the original messy world you were trying to escape. A model that captures everything is not a model. It is just a copy — and a worse one at that.

The art is in the **principled lossyness**. You decide what to include not arbitrarily but based on what downstream views will need. In our work, this is the SystemIR — the intermediate representation that flattens the compositional structure into something serializable, analyzable, and projectable. It is not the full richness of the open game formalism. It is the right cross-section of it.

From the base representation, you generate **views**. And here is where most confusion lives: views are not summaries. They are not simplifications in a pejorative sense. They are **semantic commitments**. A view for the modeler shows wiring diagrams and type flows. A view for the protocol author shows structural invariants and composition laws. A view for the business stakeholder shows equilibrium outcomes and sensitivity analyses. Each view is answering a different question about the same underlying reality. Each view hides things deliberately. **What a view hides is as important as what it shows.**

In multi-stakeholder systems, this means there is no single "correct" view. A view optimized for one stakeholder will actively mislead another. The mathematician's block diagram is not a better version of the stakeholder's dashboard — it is a different projection entirely, faithful to a different set of questions.

This is not a new idea. It's Borges' map that is the size of the territory — useless precisely because it hides nothing. It's the physicist's point particle — wrong in a way that is exactly right for the purpose. It's what philosophers of science call **model-relative truth**: a claim is true or false only relative to a model, and a model is adequate or inadequate only relative to a purpose.

---

## Tools as Epistemic Instruments

Here is the thing armchair philosophy can't give you: the feeling of the rubber hitting the road.

Building MSML has taught us things about compositional game theory that no amount of pure theory would have surfaced as quickly. When you try to compile an open game into a flat IR, you discover immediately that "state exists between games, not within them" is not just a theoretical nicety — it is a hard constraint that shapes every architectural decision downstream. When you try to build a validation pipeline that compares a canvas diagram against a code implementation, you discover that the gap between intention and implementation is not where you expected it to be. When you try to give a modeler a clean DSL, you discover that the concepts your mathematician considers primitive are actually composite — and vice versa.

**Building tools forces ontological commitment.** You cannot ship a vague concept. You cannot compile an ambiguity. The act of implementation is itself a form of philosophical inquiry, and it tends to be a faster and more humbling one than sitting with a blank page.

There is a real risk here though, and I want to name it honestly. If you overindex on building, you lose the altitude needed to see the pattern. You mistake the specific bug for the structural flaw. You optimize the local solution without noticing you're climbing the wrong hill. The learnings from making things work need to be periodically brought back up to the level of synthesis — written down, talked through, abstracted — or they evaporate into tribal knowledge and forgotten commit messages.

The balance is between **action and synthesis**. Neither is sufficient alone. Pure synthesis without implementation is speculation. Pure implementation without synthesis is archaeology — you learn a lot, but only after the fact and only by digging.

---

## What This Means in Practice

If I had to distill this into a principle, it would be:

> **Separate the concern of holding knowledge from the concern of showing it. Separate the concern of authoring a model from the concern of using it. Build the base representation to serve multiple projections, not one.**

In practice, this means resisting the temptation to build "the view" and instead building the representation from which views can be derived. It means investing in the schema and the ontology before optimizing the dashboard. It means being explicit about what each layer owns, and what crosses the boundary only through well-defined interfaces.

And it means building — deliberately, reflectively, with one eye on the structure you're discovering and one eye on the tools you're making — because the domain will teach you things that the domain alone, unimplemented, never could.

---

---

## The Formal Substrate of Antagonism

Everything above explains why separation matters — why layers must be kept distinct, why views must be projected from a base representation, why building forces ontological commitment. But there is a second structural claim running through this work that deserves its own treatment: **the claim that adversarial processes produce quality that no single-perspective process can match.**

This is not a metaphor. It is a recurring architectural invariant across multiple formal domains.

### The Core Invariant

The pattern is:

**A generative process + an evaluative process operating under different objectives, coupled into a feedback loop.**

The quality improvement comes not from either component alone but from the *tension at their interface*. The generator proposes; the evaluator constrains; the generator adapts; the evaluator sharpens. When the coupling is right, this loop converges on outputs that neither process could have produced in isolation.

This pattern appears, with different vocabulary, in at least six well-established traditions.

### Game Theory: Minimax as the Formal Root

The most rigorous grounding is in zero-sum and non-zero-sum game theory. The generator-discriminator structure in GANs is literally a minimax problem:

*min_G max_D V(D, G)*

Goodfellow's original GAN paper (2014) frames this explicitly as a two-player game where Nash equilibrium, if reached, corresponds to the generator perfectly modeling the target distribution. Two networks with antagonistic loss functions, locked in productive opposition.

But the formal framing immediately reveals a problem: convergence to Nash equilibrium in GANs is not guaranteed. In practice you get mode collapse, oscillation, and vanishing gradients. The theory is sound, but clean convergence requires additional structure — which is exactly the role SA's epistemic sequencing and halt gates play.

### Coevolution: The Biological Analog

In evolutionary biology, the formal equivalent is competitive coevolution — the Red Queen hypothesis — where predator and prey (or host and parasite) drive each other's adaptation. Each agent's fitness landscape is non-stationary because it depends on the current state of the other population. This produces an arms race dynamic and, under certain conditions, drives open-ended complexity.

The coevolution literature distinguishes cooperative from competitive coevolution and has studied extensively when competitive coevolution produces genuine improvement versus when it cycles without progress. The key formal condition for *productive* structured antagonism is: **the evaluator must have access to a broader or orthogonal information channel than the generator.** If they share the same model of the world, you collapse into cycling.

This is why GAN mode collapse and sycophancy in LLM debate systems are the same failure mode at different levels of abstraction. In both cases, the adversarial process degenerates because the evaluator has no independent leverage on truth.

### Dialectical Logic and Argumentation Theory

There is a formal tradition here that most computational work ignores. It runs from Aristotle through Hegel's dialectic through Dung's abstract argumentation frameworks (1995). Dung's framework defines:

- An **argumentation framework** as a directed graph of arguments with attack relations.
- **Admissible** and **stable** extensions as fixed-point concepts — sets of arguments that are internally consistent and defend themselves against all attacks.
- Convergence to a stable extension as the formal analogue of "structured antagonism produces a stable, defensible output."

This is the deepest formal grounding for SA's core loop. The Design phase proposes arguments. The Audit phase attacks them. The Synthesis phase finds the stable extension — the set of claims that survive all attacks and are mutually compatible. When no stable extension exists (i.e., contradictions remain), the system halts. This is exactly what SA's halt gates encode.

### Multi-Agent AI: The Generation-Verification-Reflection Loop

The generation-verification-reflection loop is emerging as a central architectural motif in robust AI systems:

- **Generation** is sampling from a distribution (learned or prompted).
- **Verification** is applying a scoring function with *different coverage* — ideally a formally verifiable signal (type checker, execution result, logical entailment) rather than another copy of the same model.
- **Reflection** is a structured gradient signal that biases the next generation step.

Google's AI Co-Scientist (Gottweis et al., 2025) instantiates this with a coalition of specialized agents — Generation, Reflection, Ranking, Evolution, Proximity, and Meta-review — where hypotheses compete in an Elo-based tournament system. AlphaEvolve (DeepMind, 2025) does the same for code optimization: generate candidates, score against metrics, regenerate from the best.

The theoretical requirement for convergence is that the verification function provides *non-trivial information not already encoded in the generator*. This is analogous to the PAC-learning condition that the error signal must have complexity not already in the hypothesis class.

Current multi-agent LLM systems take three paradigms: cooperative, debate, and competitive. The debate paradigm — agents presenting and defending viewpoints, critiquing alternatives — maps directly onto SA's audit phase. But the theory is currently weak on precisely *when* structured debate produces genuine quality improvement versus confident consensus around the wrong answer. The sycophancy problem in LLM debate (agents converging to agreement because agreement is implicitly rewarded) is the analogue of Nash equilibria that are Pareto-dominated.

### The Synthesis Gap

Here is the intellectual map of what is not yet resolved:

**When does antagonism improve quality versus cycle?** The formal condition requires the evaluator to have access to signals orthogonal to the generator's information channel. This is partially formalizable via information theory — mutual information between the critic's signal and ground truth, conditioned on the generator's prior.

**What is the right coupling strength?** Too tight (same model critiquing itself) and you get sycophancy. Too loose (completely independent critics with no shared world model) and the critique is noise. There should be an optimal coupling coefficient — directly analogous to the temperature parameter in simulated annealing and the prey-predator coupling constants in ecological models.

**Does the loop converge, and to what?** For GANs, convergence to Nash equilibrium requires convexity conditions that rarely hold in practice. For LLM debate, the formal convergence theory barely exists. Empirical proxies like Elo ratings are used, but the theoretical foundation is incomplete.

**Role separation as the key design variable.** The AI co-scientist's specialization of agents (Generation, Reflection, Ranking, Evolution, Meta-review) is not arbitrary — each agent carries a different inductive bias about what counts as quality. This is the analogue of maintaining population diversity in evolutionary computation to prevent premature convergence. SA's three-instrument loop (Design, Audit, Synthesize) enforces the same structural separation through distinct roles and adversarial stances.

### What This Means for SA

SA can now be understood not just as a methodology for structured reasoning but as a specific instantiation of this cross-domain pattern, with design choices that address the known failure modes:

- **Epistemic sequencing** prevents the generator and evaluator from sharing the same degraded information — each phase operates on the outputs of the previous phase, not on the same ambiguous inputs.
- **Role separation** (designer vs. independent reviewer vs. synthesizer) ensures the evaluator has a genuinely different perspective from the generator, preventing the sycophancy/mode-collapse failure.
- **Halt gates** are the mechanism that prevents the loop from producing confident output on unsound foundations — the formal equivalent of refusing to declare a Nash equilibrium when the game hasn't converged.
- **Cross-layer validation** is the compatibility check that catches contradictions between sections, directly analogous to checking admissibility conditions in Dung's argumentation framework.
- **Principled lossyness** ensures each view carries a different inductive bias, maintaining the population diversity that prevents premature convergence to a single (and possibly wrong) perspective.

The antagonism in structured antagonism is not a metaphor for rigor. It is a load-bearing architectural feature — the same feature that makes GANs generative, coevolution adaptive, and debate epistemically productive. The structure ensures that the antagonism converges rather than cycles.

---

*These reflections come out of ongoing work on MSML, open games, and compositional game theory at Coophive/Arkhai. The ideas are still developing — which is, I think, part of the point.*

