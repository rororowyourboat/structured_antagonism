# Cross-Domain Mappings: The Taxonomy Beyond Its Training Set

*If the three-axis taxonomy (operator class, observation symmetry, commitment enforcement) is a genuine structural classification, it should correctly classify systems from domains we did not design it around.*

---

## The Antagonism Precondition

Before the three-axis taxonomy applies, a system must satisfy the **antagonism precondition** — the formal criterion that distinguishes structured antagonism from mere feedback.

A system exhibits structured antagonism when:

1. **Two or more agents with distinct objective functions.** The system contains identifiable agents that optimize different things. This rules out single-controller systems (thermostats, homeostasis) where one agent regulates a passive plant.

2. **No Pareto-dominant joint strategy.** There is no point in the joint strategy space where all agents simultaneously achieve their optima. At least one dimension of one agent's objectives is structurally in tension with another's. This rules out mutualistic systems (mycorrhizal networks, symbiosis) where cooperative equilibria are Pareto-dominant — both agents can be at their optimum simultaneously.

3. **The tension is mediated by the system's feedback topology.** The agents' outputs are coupled through the wiring such that one agent's optimization pressure constrains the other's strategy space. The opposition is structural, not incidental.

Condition 2 is the key discriminant. It is the standard game-theoretic criterion for a non-trivially mixed game: the payoff matrix has no cell where all players are simultaneously maximized. Mixed-motivation systems (like the elenchus, where Socrates and Euthyphro share the truth-seeking objective but conflict on reputation/exposure) satisfy condition 2 because the tension on the conflicting dimension is sufficient — Pareto dominance requires *all* dimensions, and one dimension of conflict is enough to prevent it.

**Boundary cases:**

| System | Condition 1 | Condition 2 | Condition 3 | Antagonistic? |
|--------|:---:|:---:|:---:|:---:|
| GAN | Two agents | No Pareto point (fool vs detect) | Gradient feedback | Yes |
| Elenchus | Two agents | No Pareto point (reputation conflict) | Commitment loop | Yes |
| Thermostat | One agent (controller + passive plant) | N/A | N/A | **No** |
| Homeostasis | One agent (hypothalamus + passive body) | N/A | N/A | **No** |
| Mycorrhizal mutualism | Two agents | Pareto-dominant (both benefit) | Cooperative exchange | **No** |

---

## The Test

The taxonomy was developed from three systems: GANs, Socratic elenchus, and AI Co-Scientist. A real structural result should predict the class of systems from domains where the adversarial feedback structure is well-characterized independently — and should also correctly *exclude* systems that have feedback topology but lack antagonism.

For each candidate domain, we ask:
1. Does it satisfy the antagonism precondition?
2. What is the operator class? (`.feedback()` vs `.loop()` vs nested)
3. Is observation symmetric or asymmetric?
4. Is there commitment enforcement (monotonic state)?
5. What is the known failure mode? Does the taxonomy predict it?

---

## Class 1: Symmetric Antagonism (`.feedback()`)

### Robust Control / H-infinity

**Domain:** Control theory. A controller optimizes system behavior against a worst-case disturbance. In H-infinity control, the controller and the disturbance are modeled as adversaries in a minimax game — the controller minimizes the worst-case effect of the disturbance.

**Mapping:**
- **Generator:** Disturbance (nature, adversary) — produces perturbations
- **Evaluator:** Controller — produces corrections
- **Feedback:** Error signal (within-timestep, contravariant)
- **Operator:** `.feedback()` — the error signal is a within-step scalar, not accumulating state
- **Observation:** Symmetric — both controller and disturbance "observe" the plant output
- **Commitment enforcement:** N/A — no accumulating store

**Known failure mode:** **Gain instability** — the controller overreacts to disturbances, amplifying rather than dampening them. This is the control-theoretic analogue of mode collapse: the feedback signal loses its corrective property when the controller and disturbance are too tightly coupled.

**Taxonomy prediction:** Symmetric antagonism → mode collapse analogue. **Correct.**

**GDS encoding:** This is already in gds-core as the PID controller example. The plant is a `Mechanism`, the controller is a `Policy`, the error signal is a `.feedback()` wiring. The H-infinity extension adds a `BoundaryAction` (disturbance) with adversarial objective.

### Adversarial Training in ML

**Domain:** Machine learning. A classifier is trained against adversarial perturbations. At each step, an attacker generates a perturbation; the classifier updates to resist it.

**Mapping:**
- **Generator:** Adversarial perturbation generator (PGD, FGSM)
- **Evaluator:** Classifier
- **Feedback:** Gradient of adversarial loss (within-timestep)
- **Operator:** `.feedback()` — same structure as GAN

**Known failure mode:** **Catastrophic overfitting** — the classifier learns to resist a narrow class of perturbations while remaining vulnerable to others. This is mode collapse: the adversary and classifier share the same perturbation distribution.

**Taxonomy prediction:** Symmetric antagonism → mode collapse. **Correct.**

---

## Class 2: Pursuit-Evasion Antagonism (`.loop()`)

### Adaptive Immunity

**Domain:** Immunology. The adaptive immune system maintains a memory of encountered pathogens (via memory T-cells and B-cells). When a new pathogen is encountered, the immune system searches its repertoire for a match, and if none is found, generates new antibodies through somatic hypermutation and clonal selection.

**Mapping:**
- **Pursuer:** Immune system — accumulates memory of pathogen signatures
- **Evader:** Pathogen population — mutates to escape immune recognition
- **State:** Immune memory (accumulating, cross-timestep)
- **Operator:** `.loop()` — immune memory persists and grows across encounters
- **Observation:** Asymmetric — the immune system "sees" the pathogen's surface antigens; the pathogen does not "see" the immune memory
- **Commitment enforcement:** Partial — immune memory is mostly persistent (memory cells are long-lived) but can wane (immunosenescence)

**Known failure mode:** **Immune evasion** — the pathogen mutates fast enough that the immune system's accumulated memory becomes irrelevant. The evader's strategy space grows faster than the pursuer can navigate. This is **sophistry**: unbounded store growth without convergence.

**Taxonomy prediction:** Pursuit-evasion → sophistry. **Correct.**

**Note:** Antigenic sin (the immune system preferentially recalls old responses rather than generating new ones) is a *commitment enforcement pathology* — the store's monotonicity actively hurts when the pathogen has changed enough that old commitments are misleading.

### Adversarial Law (Common Law)

**Domain:** Legal systems. Prosecution and defense present opposing arguments to a judge/jury. Legal precedent (case law) accumulates over time and constrains future arguments.

**Mapping:**
- **Pursuer:** Prosecution — builds a case by extracting admissions, establishing facts
- **Evader:** Defense — attempts to maintain consistency while undermining the prosecution's narrative
- **State:** Legal record (testimony, exhibits, stipulations) — accumulating, append-only (testimony cannot be un-given)
- **World-state owner:** The court record (maintained by the court reporter, not by either party)
- **Operator:** `.loop()` — the record accumulates across examination rounds
- **Observation:** Asymmetric — prosecution may have evidence not yet disclosed; discovery rules partially equalize this
- **Commitment enforcement:** Strong — sworn testimony is a commitment; perjury penalties enforce monotonicity

**Known failure mode:** **Obfuscation** — the defense buries relevant facts in irrelevant testimony, expanding the record without convergence. This is sophistry in the formal sense: the store grows without reaching a verdict-forcing state.

**Taxonomy prediction:** Pursuit-evasion → sophistry. **Correct.**

**Structural parallel to Euthyphro:** The three-entity model maps directly. Prosecution = Socrates (pursuer), Defense = Euthyphro (evader), Court Record = Dialogue entity (world-state). The terminal condition is a verdict (the jury finds the record sufficient to decide) rather than aporia (the record becomes circular). But both are store-trajectory conditions.

### Red Team / Blue Team (Security)

**Domain:** Cybersecurity. Red team (attackers) probe a system for vulnerabilities. Blue team (defenders) patches and hardens.

**Mapping:**
- **Pursuer:** Red team — searches for vulnerabilities, accumulates attack knowledge
- **Evader:** Blue team — patches known vulnerabilities, tries to stay ahead
- **State:** Vulnerability database / patch history (accumulating)
- **Operator:** `.loop()` — knowledge accumulates across engagement rounds
- **Observation:** Asymmetric — red team often discovers vulnerabilities the blue team doesn't know about (zero-days)
- **Commitment enforcement:** Partial — patches are commitments (you can't un-patch), but the attack surface changes

**Known failure mode:** **Security theater** — blue team patches known vulnerabilities but the system's attack surface expands faster than patches can cover. The store grows (more patches, more advisories) without convergence (system never becomes secure).

**Taxonomy prediction:** Pursuit-evasion → sophistry. **Correct.**

---

## Class 3: Hierarchical Antagonism (nested `.loop()`)

### Peer Review / Scientific Method

**Domain:** Science. Researchers generate hypotheses (papers). Reviewers critique them. Editors/meta-reviewers aggregate across reviews. The literature accumulates.

**Mapping:**
- **Inner loop:** Author → Reviewer → Revision (hypothesis generation + critique within a paper)
- **Outer loop:** Meta-review / editorial board — reasons about patterns across submissions, identifies systematic weaknesses, shifts acceptance criteria
- **Operator:** `.loop().loop()` — inner loop iterates within a submission; outer loop accumulates across the literature
- **Observation:** Hierarchical — editors see patterns across submissions that individual reviewers do not
- **Commitment enforcement:** Partial — published results are commitments (retractions are rare and costly), but the literature is not strictly monotonic (paradigm shifts retract entire frameworks)

**Known failure mode:** **Paradigm lock-in** — the field converges on a locally popular framework because the outer loop (editorial norms) is too aligned with the inner loop (reviewer preferences). New approaches are filtered out before they reach the meta-review level. This is **sycophantic consensus**: inner-loop agents agree on answers the outer loop reinforces rather than challenges.

**Taxonomy prediction:** Hierarchical → sycophantic consensus. **Correct.**

### Evolutionary Arms Races with Niche Construction

**Domain:** Evolutionary biology. Predator-prey dynamics where the environment itself changes in response to population dynamics (niche construction).

**Mapping:**
- **Inner loop:** Predator-prey coevolution within a generation (fitness evaluation)
- **Outer loop:** Niche construction — organisms modify the environment (beaver dams, coral reefs), which changes the selection pressures for the next generation
- **Operator:** `.loop().loop()` — inner loop is within-generation selection; outer loop is cross-generation environmental modification
- **Observation:** Hierarchical — niche effects are visible at the population level but not to individual organisms

**Known failure mode:** **Ecological trap** — organisms optimize for an environment they have constructed, but the construction makes the environment fragile to external shocks. The inner loop converges (predator-prey equilibrium) but the outer loop has created a brittle niche. This is a form of sycophantic consensus: the inner-loop "agreement" (ecological stability) masks vulnerability that only the outer loop could detect.

**Taxonomy prediction:** Hierarchical → sycophantic consensus analogue. **Plausible.**

---

## Correctly Excluded Systems

### Homeostasis / Thermoregulation

**Domain:** Biology. The hypothalamus maintains body temperature via negative feedback.

**Why excluded:** Fails condition 1 (one agent — the hypothalamus regulates a passive body). The disturbance (environment) is not an agent with an objective function. `.feedback()` topology without antagonism is pure control.

### Mutualistic Coevolution (Mycorrhizal Networks)

**Domain:** Ecology. Fungi and plant roots exchange nutrients — fungi provide phosphorus, plants provide carbon. Both benefit.

**Why excluded:** Fails condition 2 (Pareto-dominant joint strategy exists). Both organisms can be at their optimum simultaneously. The exchange is cooperative, not constraining — neither agent's optimization pressure degrades the other's position. `.loop()` topology (nutrient exchange accumulates across seasons) but no structural tension.

**Note:** This is the critical test case for condition 2. Mycorrhizal networks have information asymmetry (each party has private knowledge of its resource state), accumulating state, and `.loop()` topology. Without the Pareto dominance criterion, the taxonomy would incorrectly classify this as pursuit-evasion. Condition 2 is what prevents the taxonomy from being "any feedback system."

---

## Enforcement Pathologies: Antigenic Original Sin

The adaptive immunity mapping surfaced a failure mode — **antigenic original sin** — where the commitment store's monotonicity actively hurts. When a pathogen mutates sufficiently, the immune system's stored memory (old antibodies) is no longer relevant, but the store's monotonicity means old responses are preferentially recalled over new ones.

This is not a gap in the taxonomy. It is a pathology *within* the `.loop()` class's enforcement axis. The taxonomy predicts that `.loop()` systems are vulnerable to enforcement-related failures. Antigenic sin is a *specific* enforcement failure: the store is monotonic, but the evader has changed enough that old commitments are misleading.

The analogue in the elenchus: Socrates invokes an early concession that Euthyphro made about a different definition, but the conceptual landscape has shifted enough that the old concession doesn't bind in the way Socrates assumes. This doesn't happen in the Euthyphro (the definitions are genuinely related — D5 reduces to D3 legitimately). But in a longer or less focused dialogue, it could.

The analogue in adversarial law: a prosecution invokes a witness's early testimony that was accurate at the time but has been superseded by new evidence. The store's monotonicity (testimony cannot be un-given) creates a misleading record.

These are all enforcement pathologies of the same structural type: **the store's monotonicity becomes counterproductive when the evader has changed faster than the store's relevance decays.** The taxonomy predicts the vulnerability class; the specific pathology depends on the domain.

---

## The `.lift()` Hypothesis

### What `.lift()` would describe

The current three-operator vocabulary (`.feedback()`, `.loop()`, nested `.loop()`) assumes a **fixed state space**. The commitment store grows but the space of possible propositions is fixed. GAN parameters update but the model architecture is fixed. The hypothesis population evolves but the evaluation criteria are fixed.

A `.lift()` operator would describe systems where **the evaluation criteria themselves change as a result of the process** — where each iteration transforms the state space rather than iterating within it.

### Candidate instances

| Domain | Inner operation | Lift operation | What changes |
|--------|---------------|---------------|-------------|
| Scientific paradigm shifts | Normal science (`.loop()`) | Paradigm shift | What counts as a good theory |
| Constitutional amendment | Ordinary legislation (`.loop()`) | Amendment | The rules for making rules |
| Developmental biology | Gene expression (`.loop()`) | Cell differentiation | The regulatory state space |
| Meta-learning (MAML) | Parameter update (`.loop()`) | Learning algorithm update | The optimization procedure itself |

### Is `.lift()` encodable in GDS?

The question is whether `.lift()` requires a genuinely new primitive or whether it is expressible as a composition of existing operators.

**Argument for new primitive:** GDS `CorecursiveLoop` iterates within a fixed `Interface` — the forward_in and forward_out types are set at composition time. A true `.lift()` would require an operator where the output type of iteration N is *different from* the input type of iteration N+1. This is a type-level change, not a value-level change, and GDS's type system does not support it.

**Argument for existing composition:** `.lift()` could be modeled as `.loop()` with a state variable whose *interpretation* changes across iterations, even if its type stays the same. A string-typed "current paradigm" variable can hold "Newtonian mechanics" at iteration N and "general relativity" at iteration N+1 without requiring a type change. The lift is in the semantics, not the syntax.

**Assessment:** The second argument is formally correct but philosophically unsatisfying. The whole point of `.lift()` is that the rules change — and representing rule changes as value changes in a fixed-type variable hides the structural transformation in the data. This is analogous to encoding a programming language in a string field rather than defining its grammar — technically possible, but it loses the structure the formalism should capture.

This remains an open question. If `.lift()` cannot be captured without a new GDS primitive, it is a limitation the research program has surfaced in the framework.

---

## Summary

### What the taxonomy predicts correctly (7/7)

| Domain | Operator | Predicted failure | Known failure | Match |
|--------|----------|-------------------|---------------|:---:|
| H-infinity control | `.feedback()` | Mode collapse | Gain instability | Yes |
| Adversarial training | `.feedback()` | Mode collapse | Catastrophic overfitting | Yes |
| Adaptive immunity | `.loop()` | Sophistry | Immune evasion | Yes |
| Adversarial law | `.loop()` | Sophistry | Obfuscation | Yes |
| Red team / blue team | `.loop()` | Sophistry | Security theater | Yes |
| Peer review | `.loop().loop()` | Sycophantic consensus | Paradigm lock-in | Yes |
| Niche construction | `.loop().loop()` | Sycophantic consensus | Ecological trap | Plausible |

### What the taxonomy correctly excludes (2)

| System | Topology | Why excluded |
|--------|----------|-------------|
| Homeostasis | `.feedback()` | Fails condition 1 (single agent) |
| Mycorrhizal mutualism | `.loop()` | Fails condition 2 (Pareto-dominant) |

### What the taxonomy cannot yet classify (1)

| System | Issue | Status |
|--------|-------|--------|
| Hegelian dialectic | State space transforms per iteration | Needs `.lift()` operator — open question |

### Falsifiability

The taxonomy would be falsified by a system that:
1. Satisfies the antagonism precondition
2. Has a well-characterized failure mode
3. Is classified by the three axes into a class whose predicted failure mode does not match the observed one

No such system has been found. This is either because the taxonomy captures a genuine structural pattern, or because the three axes are loose enough that classification can be adjusted post-hoc. The test for the latter is to find a system where the axis assignment is unambiguous but the prediction fails. Candidate stress tests: adversarial debate protocols (where the failure mode may be neither mode collapse nor sophistry nor sycophancy), and competitive multi-agent reinforcement learning (where the failure mode may depend on training dynamics not captured by topology).
