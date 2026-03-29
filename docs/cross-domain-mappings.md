# Cross-Domain Mappings: The Taxonomy Beyond Its Training Set

*If the three-axis taxonomy (operator class, observation symmetry, commitment enforcement) is a genuine structural classification, it should correctly classify systems from domains we did not design it around.*

---

## The Test

The taxonomy was developed from three systems: GANs, Socratic elenchus, and AI Co-Scientist. A real structural result should predict the class of systems from control theory, biology, law, security, and market design — domains where the adversarial feedback structure is well-characterized independently.

For each candidate domain, we ask:
1. What is the operator class? (`.feedback()` vs `.loop()` vs nested)
2. Is observation symmetric or asymmetric?
3. Is there commitment enforcement (monotonic state)?
4. What is the known failure mode? Does the taxonomy predict it?

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

## Class 4? Open Questions

### Homeostasis / Thermoregulation

**Domain:** Biology. The hypothalamus maintains body temperature via negative feedback — vasodilation, sweating, shivering.

**Mapping:** `.feedback()` — within-timestep error signal. But is this *antagonistic*? The setpoint and the disturbance (environment) are not adversaries in any strategic sense. There is no evaluator with a different objective. This is pure control, not structured antagonism.

**Taxonomy status:** `.feedback()` topology but **no antagonism** — the feedback is corrective, not adversarial. The taxonomy may need a precondition: the system must have agents with *different* objectives for the antagonism classification to apply. Pure negative feedback without opposed objectives is control, not antagonism.

### Hegelian Dialectic

**Domain:** Philosophy of history. Thesis → antithesis → synthesis, where the synthesis becomes the new thesis at a higher level.

**Mapping:** The state space *transforms* with each iteration — the synthesis is not just a new state in the same space but a new level of abstraction. This is not expressible as `.loop()` (which iterates within a fixed state space) or `.feedback()`.

**Taxonomy status:** Potentially a **fourth operator class** — `.lift()` — where each iteration expands the state space. This remains an open question from the research journal (Entry 8).

---

## Summary Table

| Domain | Operator | Observation | Enforcement | Predicted failure | Known failure | Match? |
|--------|----------|-------------|-------------|-------------------|---------------|:---:|
| H-infinity control | `.feedback()` | Symmetric | N/A | Mode collapse | Gain instability | Yes |
| Adversarial training | `.feedback()` | Symmetric | N/A | Mode collapse | Catastrophic overfitting | Yes |
| Adaptive immunity | `.loop()` | Asymmetric | Partial | Sophistry | Immune evasion | Yes |
| Adversarial law | `.loop()` | Asymmetric | Strong | Sophistry | Obfuscation | Yes |
| Red team / blue team | `.loop()` | Asymmetric | Partial | Sophistry | Security theater | Yes |
| Peer review | `.loop().loop()` | Hierarchical | Partial | Sycophantic consensus | Paradigm lock-in | Yes |
| Niche construction | `.loop().loop()` | Hierarchical | Partial | Sycophantic consensus | Ecological trap | Plausible |
| Homeostasis | `.feedback()` | N/A | N/A | — | — | Not antagonistic |
| Hegelian dialectic | ? | ? | ? | ? | ? | Needs new operator |

Seven clear matches. One non-antagonistic system correctly excluded. One system (Hegelian dialectic) that may require extending the taxonomy. The taxonomy classifies known systems from control theory, immunology, law, security, evolutionary biology, and science with zero false predictions on the well-characterized cases.
