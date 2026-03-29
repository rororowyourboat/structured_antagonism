# Research Journal: Structured Antagonism as Compositional Game Theory

*A record of the intellectual development, design decisions, and open questions driving this project.*

**Notation:** This journal uses `.feedback()` and `.loop()` as shorthand for GDS composition operators. In the OGS API: `.feedback()` = `FeedbackLoop` (contravariant, within-timestep); `.loop()` = `CorecursiveLoop` (covariant, cross-timestep, wraps GDS `TemporalLoop`). The GDS IR uses `is_temporal` for corecursive wirings. See `models/` for actual API usage.

---

## Entry 1: The Core Observation

**Date:** 2026-03-29

### What we noticed

There is a recurring architectural pattern across multiple domains:

**A generative process + an evaluative process operating under different objectives, coupled into a feedback loop.**

The quality improvement comes not from either component alone but from the tension at their interface. This pattern is load-bearing in:

- **Game theory** — GANs are a minimax game between generator and discriminator. Convergence produces outputs neither process could generate alone. Failure (mode collapse) occurs when evaluator and generator collapse into the same information channel.
- **Evolutionary biology** — Competitive coevolution (Red Queen hypothesis) drives open-ended complexity through arms race dynamics. The evaluator must access orthogonal information or the system cycles without progress.
- **Argumentation theory** — Dung's abstract argumentation frameworks (1995) define stable extensions as fixed-point concepts: sets of arguments that survive all attacks and are internally consistent.
- **Multi-agent AI** — Google's AI Co-Scientist and DeepMind's AlphaEvolve use specialized agent coalitions locked in iterative competition. Hypotheses compete in Elo-based tournaments.
- **Ancient philosophy** — Socratic elenchus (as recorded in the Platonic dialogues) is a structured adversarial process where a questioner systematically probes a respondent's commitments until contradiction (aporia) is reached.

A common failure mode appears across these systems: the adversarial process degenerates because the evaluator has no independent leverage on truth. GAN mode collapse and LLM sycophancy are instances of this — both involve evaluator-generator information channels collapsing. *(Note: Entry 7 shows these are not "structurally identical" in the compositional sense — GANs use `.feedback()` while multi-agent debate uses `.loop()`. The shared pattern is the information asymmetry failure, not the composition topology.)*

### The question this raises

These systems clearly share something structural. But *what exactly* do they share, and can we make that precise enough to prove properties about it? And where the structural details diverge, does that divergence predict different behavior?

---

## Entry 2: The Formal Substrate

**Date:** 2026-03-29

### The key invariant

All productive antagonistic systems share:

1. **Two or more agents with different objective functions** — not different implementations of the same objective, but genuinely different optimization targets.
2. **A feedback topology** — outputs of one agent feed inputs of another, closing a loop.
3. **An information asymmetry condition** — the evaluator must have access to signals orthogonal to the generator's information channel. Without this, the system collapses into cycling (mode collapse) or consensus around the wrong answer (sycophancy).
4. **A convergence criterion** — some notion of "stable output" that the loop can terminate at (Nash equilibrium, stable extension, aporia, validated hypothesis).

### What varies across instances

| Property | Elenchus | GAN | AI Co-Scientist |
|----------|----------|-----|-----------------|
| Composition operator | `.loop()` (corecursive) | `.feedback()` (contravariant) | `.loop().loop()` (nested corecursive) |
| Signal type | Natural language | Scalar gradient | Structured hypothesis |
| State | Commitment store | Model parameters | Hypothesis population |
| Convergence | Aporia (inconsistency) | Nash equilibrium | Elo-stable ranking |
| Failure mode | Sophistry | Mode collapse | Sycophantic consensus |

The topology is the same for elenchus and GANs. The co-scientist is strictly deeper — the meta-review closes a loop over the entire inner pipeline, accumulating information about the *distribution* of failures rather than individual failures.

### The claim worth proving

**Systems with deeper feedback nesting have richer fixed-point structure than single-loop systems, but are harder to certify convergent.**

This is testable if we can encode all three systems in a common formal vocabulary and compare their structural properties computationally.

---

## Entry 3: Why GDS-Core

**Date:** 2026-03-29

### The framework

GDS-Core (Generalized Dynamical Systems) is a compositional specification framework built on the Open Games formalism (Ghani, Hedges et al.). It provides:

- **`OpenGame` with `Signature(x, y, r, s)`** — four-channel blocks where `x` = observations (covariant forward), `y` = choices (covariant forward), `r` = utilities (contravariant backward), `s` = coutilities (contravariant backward).
- **Composition operators** — `>>` sequential, `|` parallel, `.feedback()` (within-timestep contravariant), `.loop()` (cross-timestep covariant).
- **Compilation** — game trees compile to flat `SystemIR` for topological analysis.
- **Verification** — pluggable checks (G-001..G-006 generic, T-001..T-006 type, S-001..S-007 structural) that certify properties of composed systems.

### Why it fits

A two-player antagonistic system is literally two `DecisionGame` blocks composed with `.feedback()`. The composition operators distinguish the topologies we care about:

- **Elenchus** = `(Interlocutor >> Socrates).feedback()`
- **GAN** = `(Generator >> Discriminator).feedback()`
- **AI Co-Scientist** = `(Gen >> Reflect >> Rank >> Evolve).feedback(via=MetaReview)`

The first two are topologically identical in GDS terms — same composition tree, different types on the wires. The third has strictly deeper nesting. This is a structural fact that GDS makes visible and verifiable.

### The encoding

**Socratic Elenchus (Euthyphro):**

```python
interlocutor = DecisionGame(
    name="Euthyphro",
    signature=Signature(
        x=(port("Commitment Store"),),       # observes accumulated commitments
        y=(port("Proposed Definition"),),     # proposes/revises definition
        r=(port("Refutation"),),              # receives Socratic challenge
        s=(port("Updated Commitments"),),     # sends updated commitment state
    ),
)

socrates = DecisionGame(
    name="Socrates",
    signature=Signature(
        x=(port("Proposed Definition"),),     # observes the proposal
        y=(port("Refutation"),),              # produces counterexample
        r=(port("Updated Commitments"),),     # receives commitment updates
        s=(port("Next Question"),),           # sends the next probe
    ),
)

elenchus = (interlocutor >> socrates).feedback(...)
```

The commitment store is the state variable that accumulates and eventually becomes inconsistent — aporia is a detectable terminal condition in which no valid `y` exists.

**GAN:**

```python
generator = DecisionGame(
    name="Generator",
    signature=Signature(
        x=(port("Noise"),),
        y=(port("Sample"),),
        r=(port("Discriminator Signal"),),
        s=(port("Updated Params"),),
    ),
)

discriminator = DecisionGame(
    name="Discriminator",
    signature=Signature(
        x=(port("Sample"),),
        y=(port("Real or Fake"),),
        r=(port("Generator Params"),),
        s=(port("Updated Params"),),
    ),
)

gan = (generator >> discriminator).feedback(...)
```

**AI Co-Scientist:**

```python
gen     = CovariantFunction(name="Generation", ...)
reflect = CovariantFunction(name="Reflection", ...)
rank    = CovariantFunction(name="Ranking", ...)
evolve  = CovariantFunction(name="Evolution", ...)
meta    = DecisionGame(name="Meta-Review", ...)

inner = gen >> reflect >> rank >> evolve
system = inner.feedback(via=meta)
```

### What compilation reveals

Once all three compile to `SystemIR`, we can compare:

- **Loop depth** — number of nested feedback loops
- **Signature compatibility** — what types flow across the antagonism boundary
- **Fixed-point structure** — what the stable state looks like in each system
- **Convergence conditions** — structural properties that determine whether the system terminates or cycles

---

## Entry 4: The Semantic Web Move

**Date:** 2026-03-29

### The insight

Rather than writing procedural Python to compare `SystemIR` objects, we can export all three models to RDF via `gds-owl` and make the comparison *declarative*.

`gds-owl` exports any `GDSSpec` or `SystemIR` to a full RDF graph with four ontology layers:

- **Layer 0:** Composition algebra — Block hierarchy, interfaces, ports, token-based type matching
- **Layer 1:** Specification framework — GDSSpec, TypeDef, Space, Entity, StateVariable, SpecWiring
- **Layer 2:** SystemIR — BlockIR, WiringIR, HierarchyNodeIR (flat topology)
- **Layer 3:** Verification — Findings, severity, check IDs

It also provides:

- **SPARQL templates** — pre-built queries for blocks-by-role, dependency paths, entity-update maps, wiring topology
- **SHACL shapes** — 13 structural validators
- **Full round-trip** at R1 fidelity (structure preserved, behavior functions lossy)

### Why semantic web over plain Python

Three reasons:

**1. Declarative cross-model queries.** Merge all three systems into a single RDF graph and query across them:

```sparql
# Which systems have nested feedback loops?
SELECT ?system ?inner ?outer WHERE {
  ?system gds-ir:hasWiringIR ?outer .
  ?outer gds-ir:isFeedback true .
  ?inner_block gds-ir:hasWiringIR ?inner .
  ?inner gds-ir:isFeedback true .
  ?system gds-ir:hasBlockIR ?inner_block .
}
```

```sparql
# What role distribution does each system have?
SELECT ?system (COUNT(?boundary) AS ?exogenous)
              (COUNT(?policy) AS ?decisions)
              (COUNT(?mechanism) AS ?updates) WHERE {
  ?system gds-core:hasBlock ?block .
  OPTIONAL { ?block a gds-core:BoundaryAction . BIND(?block AS ?boundary) }
  OPTIONAL { ?block a gds-core:Policy . BIND(?block AS ?policy) }
  OPTIONAL { ?block a gds-core:Mechanism . BIND(?block AS ?mechanism) }
} GROUP BY ?system
```

**2. Custom SHACL shapes for antagonism properties.** Define what "productive antagonism" looks like structurally:

```turtle
sa:ProductiveAntagonismShape a sh:NodeShape ;
    sh:targetClass gds-ir:SystemIR ;
    sh:property [
        sh:path gds-ir:hasWiringIR ;
        sh:qualifiedValueShape [
            sh:property [
                sh:path gds-ir:isFeedback ;
                sh:hasValue true
            ]
        ] ;
        sh:qualifiedMinCount 1 ;
        sh:message "System must have at least one feedback wiring"
    ] .
```

**3. AIF interoperability.** The Argument Interchange Format (AIF) is itself an OWL ontology — the standard vocabulary for computational argumentation. It defines classes for:

- `I-node` — information (claims, premises)
- `RA-node` — inference (support relations)
- `CA-node` — conflict (attack relations)
- `PA-node` — preference (defeat relations)

Dung's argumentation frameworks have a direct AIF encoding. If we encode Euthyphro's commitment store in a way compatible with *both* GDS-OWL and AIF, we get:

- **The dialogue as a game** (GDS-OWL) — blocks, feedback, state variables, verification
- **The dialogue as an argument** (AIF) — attack relations, support relations, stable extensions
- **Cross-ontology queries** — "in this game, which feedback cycles correspond to unresolved attacks in the argumentation framework?"

This is the connection between game theory and argumentation theory made *computationally traversable*, not just asserted in prose.

### What this means for the comparison

The `compare.py` script becomes very clean:

1. Load three GDS specs (elenchus, GAN, co-scientist)
2. Export each to RDF via `gds-owl`
3. Merge into a single graph
4. Run SPARQL queries for structural comparison
5. Run SHACL shapes for antagonism-specific validation
6. Report structural differences and shared invariants

### The honest limitation

gds-owl exports *structure* (topology, wiring, roles, types) but not *behavior* (logic functions, constraints). `TypeDef.constraint` is R3 lossy. So the comparison is topological — we can prove two systems have identical feedback structure but we cannot reason in SPARQL about what the signals *mean*.

For our purposes this is sufficient. The claim is structural: same topology, different types on the wires. Structure is exactly what the RDF graph captures.

---

## Entry 5: The Hard Problem — Euthyphro Annotation

**Date:** 2026-03-29

### What needs to happen

Before we can encode the Socratic elenchus as a GDS game, we need to extract the commitment store from the dialogue text. The commitment store is implicit in the Platonic dialogues — reconstructed by a reader from what each interlocutor has conceded at each step.

Euthyphro is the right starting text:
- Short (~20 pages)
- Single topic (the nature of piety)
- Clean terminus in aporia
- Well-studied in the argumentation theory literature

### The annotation task

For each dialogue turn, extract:
- **Speaker** (Socrates or Euthyphro)
- **Speech act type** (propose, challenge, concede, retract, clarify)
- **Commitment store delta** — what was added to or removed from each speaker's commitments
- **Cumulative commitment store** — the full set of commitments at that point

### Approach options

1. **Manual** — careful philological work, high fidelity, slow (days)
2. **LLM first pass + manual verification** — faster, good enough if we verify carefully
3. **Treat annotation as a research question** — formalize the extraction methodology itself

Option 2 is the practical choice. The LLM can extract a reasonable first draft of commitment stores per turn; we then verify against the Greek text and existing scholarly commentary.

### Output format

```json
{
  "dialogue": "Euthyphro",
  "turns": [
    {
      "turn": 1,
      "speaker": "Socrates",
      "text": "...",
      "speech_act": "question",
      "commitment_delta": {
        "added": ["Euthyphro claims to know what piety is"],
        "removed": []
      },
      "commitment_store": {
        "socrates": [],
        "euthyphro": ["Claims to know what piety is"]
      }
    }
  ]
}
```

This annotation is itself a contribution — a machine-readable commitment-store trace of a canonical philosophical text does not exist in this form.

---

## Entry 6: Research Plan

**Date:** 2026-03-29

### Sequencing

The project has five phases, each producing a self-contained artifact:

**Phase 1: Scaffold**
- Set up `pyproject.toml` with `gds-framework`, `gds-games`, `gds-owl`, `gds-viz` from PyPI
- Validate that the packages work together
- Artifact: working project skeleton with imports verified

**Phase 2: GAN Model**
- Encode the GAN generator-discriminator system as an OGS Pattern
- Compile to PatternIR → SystemIR
- Export to RDF via gds-owl
- Run verification checks
- Artifact: `models/gan/model.py` + exported Turtle file + verification report
- *Why first:* Most well-understood system. Validates our approach before harder work.

**Phase 3: Euthyphro Annotations**
- Extract commitment stores per dialogue turn (LLM first pass + manual verification)
- Formalize as structured JSON
- Artifact: `models/euthyphro/annotations.json`
- *Bottleneck:* This is genuine philological work. A few days of careful effort.

**Phase 4: Euthyphro Model**
- Encode the annotated dialogue as an OGS Pattern
- Map commitment store to Entity state variables
- Define aporia as a terminal condition (commitment store inconsistency)
- Explore AIF bridge — encode the same dialogue as an argumentation graph
- Export to RDF, merge with GAN graph
- Artifact: `models/euthyphro/model.py` + `models/euthyphro/aif.py`

**Phase 5: AI Co-Scientist Model + Taxonomy**
- Encode the hierarchical multi-agent system as an OGS Pattern
- Nested composition: `inner.loop(hypothesis_population).feedback(via=MetaReview)`
- Export to RDF, merge all three into single graph
- Write SPARQL queries for structural comparison (operator type, loop depth, state dynamics)
- Write SHACL shapes for each antagonism class
- Validate taxonomy: do the composition trees differ as predicted? Do structural differences correspond to different convergence/failure properties?
- Artifact: `models/co_scientist/model.py` + `models/compare.py` + SPARQL/SHACL files + taxonomy analysis

### Repo structure (target state)

```
structured-antagonism/
├── README.md                           # Philosophy + project overview
├── docs/
│   ├── philosophy.md                   # Source essay + formal substrate
│   ├── manifesto.md                    # SA manifesto
│   ├── anatomy.md                      # Prompt architecture patterns
│   ├── construction-guide.md           # Building SA instruments
│   ├── psuu.md                         # PSuU methodology
│   └── research-journal.md             # This document
├── domains/                            # SA prompt instruments
│   ├── software-systems/
│   ├── data-science/
│   └── research/
├── meta/
│   ├── principles.md                   # 10 principles expanded
│   └── anti-patterns.md               # 10 failure modes
├── models/                             # GDS/OGS formal encodings
│   ├── euthyphro/
│   │   ├── annotations.json            # Commitment store per turn
│   │   ├── model.py                    # OGS game spec
│   │   └── aif.py                      # AIF argumentation graph
│   ├── gan/
│   │   └── model.py                    # OGS game spec
│   ├── co_scientist/
│   │   └── model.py                    # OGS game spec
│   └── compare.py                      # Merge → SPARQL → report
├── ontology/
│   ├── antagonism_shapes.ttl           # Custom SHACL for SA properties
│   └── queries/
│       ├── loop_depth.sparql
│       ├── role_topology.sparql
│       └── feedback_structure.sparql
└── pyproject.toml                      # gds-framework, gds-games, gds-owl, gds-viz
```

### The contribution (revised after Entry 7)

If this works, the project produces:

1. **A formal taxonomy** of antagonistic systems classified by GDS composition topology (`.feedback()` vs `.loop()` vs `.loop().feedback()`)
2. **A structural result** linking composition topology to convergence dynamics and failure modes — the topology predicts whether the system fails via mode collapse, sophistry, or sycophantic consensus
3. **A machine-readable annotation** of a canonical Platonic dialogue with commitment stores, treated as a contribution in its own right with explicit interpretive methodology
4. **A computational demonstration** that elenchus and GANs are *not* topologically equivalent — they use different GDS operators, reflecting the pursuit-evasion vs. minimax distinction
5. **Custom SHACL shapes** defining structural properties of each antagonism class
6. **A clear open problem** — formalizing the information asymmetry condition that determines whether a system in any class converges or degenerates

This sits at the intersection of compositional game theory, computational argumentation, and AI systems design — territory that is currently fragmented across fields that have not yet synthesized.

---

## Entry 7: The Asymmetry Problem — Self-Audit

**Date:** 2026-03-29

### The critique

An honest review of the project surfaced a blind spot that restructures the central claim.

The project originally claimed that Socratic elenchus and GANs have "identical feedback topology" — same GDS composition tree, different types on the wires. But this claim conflates two structurally different relationships to game state:

- In a **GAN**, both players are peers. The generator produces a sample; the discriminator classifies it; the gradient feeds back. Neither player accumulates a record. Each training step is relatively independent — the feedback is *within-timestep*.

- In **Socratic elenchus**, the relationship is asymmetric. Socrates is not evaluating a proposal against ground truth (like a discriminator). He is *searching the commitment space for inconsistency*. His strategy is a function of the *entire commitment history* — he chooses questions that target specific earlier concessions to engineer contradiction. The commitment store *accumulates across turns* and constrains all future moves.

This is pursuit-evasion, not minimax. And it maps to a different GDS operator.

### Where the topology diverges

In GDS, `.feedback()` and `.loop()` are different composition operators with different formal properties:

- **`.feedback()`** — contravariant, within-timestep. The backward channel (r/s) carries a signal that influences the current step. The GAN discriminator's gradient is `.feedback()`.

- **`.loop()`** — covariant, cross-timestep. The forward channel (x/y) carries state that persists and accumulates. The elenchus commitment store is `.loop()`.

This means the three systems under study use *different composition operators*:

```python
# GAN — within-timestep feedback, symmetric players
gan = (generator >> discriminator).feedback(gradient_signal)

# Elenchus — cross-timestep accumulation, asymmetric observation
elenchus = (euthyphro >> socrates).loop(commitment_store)

# Co-Scientist — nested: temporal loop with inner feedback
inner = gen >> reflect >> rank >> evolve
co_scientist = inner.loop(hypothesis_population).feedback(via=meta_review)
```

Three different composition trees. Not "the same topology with different types on the wires."

### The revised taxonomy

The structural result is now a *classification* of antagonistic systems by composition topology, not a proof of topological equivalence:

| Class | GDS Operator | State dynamics | Convergence criterion | Failure mode |
|-------|-------------|----------------|----------------------|-------------|
| **Symmetric antagonism** | `.feedback()` | Stateless per-step | Nash equilibrium | Mode collapse |
| **Pursuit-evasion antagonism** | `.loop()` | Accumulating state | Aporia (inconsistency) | Sophistry |
| **Hierarchical antagonism** | `.loop().loop()` | Population + meta-signal | Elo-stable ranking | Sycophantic consensus |

The failure modes are *associated with* the composition topology, but as Entry 8 clarifies, they depend on the full three-axis combination (operator class, observation symmetry, commitment enforcement), not operator class alone:

- **Mode collapse** occurs in `.feedback()` systems when the evaluator and generator share the same information channel — specifically when observation is symmetric (both players see the same signals). The operator class creates the precondition; the observation symmetry determines whether the failure manifests.
- **Sophistry** occurs in `.loop()` systems when commitment enforcement fails — the evader retracts or shifts ground, violating monotonicity. The operator class creates accumulating state; the enforcement mechanism determines whether that state converges or cycles.
- **Sycophantic consensus** occurs in nested `.loop()` systems when the outer loop signal is too weak relative to the inner loop — agents converge on locally popular answers. The nesting creates the hierarchical structure; the relative signal strength (an observation asymmetry property) determines whether the outer loop has genuine leverage.

### What this means for the research plan

The claim to test is no longer "these systems share a topology." It is: **different classes of antagonistic systems have different composition topologies in GDS, and the three-axis combination (operator, observation, enforcement) determines convergence dynamics and failure modes.**

This is a stronger result. It also has a clear falsification condition: if the composition trees don't differ (all three systems reduce to the same operator), the taxonomy is trivial. If they differ but the structural differences don't predict convergence behavior, the taxonomy is uninformative.

### Updated encodings

The Entry 3 pseudocode needs revision:

**Elenchus (revised):**

```python
euthyphro = DecisionGame(
    name="Euthyphro",
    signature=Signature(
        x=(port("Commitment Store"),),        # full accumulated state
        y=(port("Proposed Definition"),),      # current proposal
        r=(port("Refutation"),),               # Socratic challenge
        s=(port("Updated Commitments"),),      # state delta
    ),
)

socrates = DecisionGame(
    name="Socrates",
    signature=Signature(
        x=(port("Commitment Store"),           # ALSO sees full history
           port("Proposed Definition"),),       # plus current proposal
        y=(port("Refutation"),),               # engineered challenge
        r=(port("Updated Commitments"),),      # commitment delta
        s=(port("Next Question"),),            # probe targeting specific prior commitment
    ),
)

# Cross-timestep loop, not within-timestep feedback
elenchus = (euthyphro >> socrates).loop(
    [Wiring("Socrates", "Updated Commitments",
            "Euthyphro", "Commitment Store",
            direction=FlowDirection.COVARIANT)],
    exit_condition="commitment_store_inconsistent",
)
```

Key differences from Entry 3:
1. Socrates' `x` channel includes the full commitment store, not just the current proposal — asymmetric observation
2. The composition uses `.loop()` (covariant, cross-timestep), not `.feedback()` (contravariant, within-timestep)
3. The exit condition is commitment store inconsistency (aporia), not a Nash equilibrium

### Remaining gaps

**Information asymmetry is still the hard problem.** The composition algebra captures *that* there is feedback but not *what information it carries*. The orthogonality condition ("evaluator must access signals orthogonal to the generator's channel") would need to live as a property annotation on the wiring — metadata describing the information channel's characteristics — not something the type system enforces. This is an honest limitation and a clear target for extending the framework.

**The AIF bridge is harder than originally planned.** Static Dung frameworks don't capture dialogue dynamics. We would need Walton & Krabbe's dialogue game protocols or Hamblin's commitment store formalism — dynamic extensions that track commitment evolution over time. This is a separate research question, not a Phase 4 sub-task. Flagging it as such.

**The Euthyphro annotation is doing philosophical work.** Different interpretations of what Euthyphro has committed to at each step are not minor variations — they produce structurally different games. If the annotation is contested, the formal encoding inherits that contestation silently. This argues for treating the annotation as a contribution in its own right, with explicit methodology and documented interpretive choices, rather than a preprocessing step.

---

## Entry 8: Sharpening the Taxonomy — Three Questions Resolved

**Date:** 2026-03-29

### Question 1: Is the co-scientist `.loop().feedback()` or `.loop().loop()`?

In GDS, `FeedbackLoop` connects `backward_out → backward_in` (within-timestep, contravariant). `TemporalLoop` connects `forward_out → forward_in` (cross-timestep, covariant).

The question is whether the meta-review operates on the *current round's outputs* (within-step feedback) or on the *accumulated distribution across rounds* (temporal signal). In the actual AI co-scientist paper, the meta-review aggregates across the Elo history — it reasons about the trajectory of the hypothesis population, not just the current batch. That is a temporal signal. The co-scientist is `.loop().loop()`.

This means the taxonomy is not three fixed classes. It is an **open lattice** generated by operator combinations:

| Composition | Operators | Example | Notes |
|-------------|-----------|---------|-------|
| `.feedback()` | Contravariant within-step | GAN | Symmetric |
| `.loop()` | Covariant cross-step | Elenchus | Accumulating, pursuit-evasion |
| `.loop().loop()` | Nested covariant | AI co-scientist | Temporal at both levels |
| `.loop().feedback()` | Temporal + within-step | SA's Design→Audit→Synthesize? | Hybrid |
| `.feedback().feedback()` | Nested within-step | ? | Unclear if meaningfully distinct |

Whether this lattice is bounded or generative — whether deeper nesting produces genuinely new classes or collapses — is an empirical question the GDS encoding can answer. If `.loop().loop().loop()` behaves like `.loop().loop()`, the lattice has a fixed point. If not, it is open-ended and corresponds to increasing hierarchical depth.

### Question 2: Sophistry as a formal trajectory property

Sophistry in a `.loop()` system is a trajectory where **the commitment store grows without bound without ever reaching inconsistency.** The evader's strategy is to keep the store in a region where no inconsistency is derivable — expanding the surface area faster than the pursuer can close contradictions.

In GDS terms:

- **Productive elenchus:** Finite trajectory. Commitment store reaches inconsistency. `TemporalLoop.exit_condition` fires. Loop terminates.
- **Sophistry:** Unbounded trajectory. Store grows monotonically. Exit condition never fires. The formal signature is: `|store(t)| → ∞` while `inconsistency(store(t)) = false ∀ t`.
- **Commitment violation:** Store shrinks (retractions). The `Mechanism` update rule is not monotonic. Loop integrity is violated — the interlocutor escapes by denying earlier concessions.

This surfaces the **commitment enforcement problem.** In the GDS encoding, the commitment store is a state variable updated by a `Mechanism`. Nothing in the composition algebra *prevents* the interlocutor from retracting. The enforcement must be a constraint on the `Mechanism`'s update rule: the update must be monotonic (append-only).

This can be expressed as:
- A custom GDS verification check: `SA-COMMIT-001: Mechanism updates to commitment store entity must be append-only`
- A SHACL shape on the RDF export validating monotonicity
- A TypeDef constraint on the commitment store state variable

The commitment enforcement is load-bearing for the `.loop()` class in a way that has no analogue in `.feedback()`. In a GAN, the generator cannot "retract" previous samples — the gradient signal is a scalar, not a store. In elenchus, the interlocutor *can* retract, and preventing that retraction is what makes the loop productive. **Commitment enforcement is the mechanism that converts cycling into convergence in `.loop()` systems.**

### Question 3: Asymmetric observation of shared state

GDS *does* support asymmetric observation. Each player's `x` (forward_in) is a tuple of Ports. Two players composed in parallel (`|`) before sequential composition (`>>`) can have different forward_in ports even when they share the same upstream state.

The asymmetry lives in the *wiring*, not the state. A `Policy` or `ControlAction` block upstream projects the shared state differently for each player:

```python
# Upstream projection blocks
euthyphro_view = Policy(
    name="Euthyphro View",
    interface=Interface(
        forward_in=(port("Commitment Store"),),
        forward_out=(port("Current Commitments"),),     # projection: active set only
    ),
)

socrates_view = Policy(
    name="Socrates View",
    interface=Interface(
        forward_in=(port("Commitment Store"),),
        forward_out=(port("Commitment Store History"),   # full trajectory
                     port("Current Commitments"),),      # plus active set
    ),
)

# Each player sees a different projection of the same state
euthyphro = DecisionGame(
    name="Euthyphro",
    signature=Signature(
        x=(port("Current Commitments"),),               # limited view
        ...
    ),
)

socrates = DecisionGame(
    name="Socrates",
    signature=Signature(
        x=(port("Commitment Store History"),             # full history
           port("Current Commitments"),),                # plus current
        ...
    ),
)

# Compose with asymmetric projection
euthyphro_arm = euthyphro_view >> euthyphro
socrates_arm = socrates_view >> socrates
round = (euthyphro_arm | socrates_arm) >> commitment_update
elenchus = round.loop(commitment_store_wiring, exit_condition="aporia")
```

This means the information asymmetry condition *is partially capturable in GDS topology.* Not the content of the information, but the structural fact that one player's `x` channel is a strict superset of the other's. In the compiled `SystemIR`, this shows up as different wiring fan-out from the shared state entity — queryable in SPARQL:

```sparql
# Which players observe a strict superset of another player's inputs?
SELECT ?observer ?observed WHERE {
  ?observer gds-ir:hasForwardIn ?obs_ports .
  ?observed gds-ir:hasForwardIn ?obsd_ports .
  # obs_ports is a strict superset of obsd_ports
  FILTER(?observer != ?observed)
  FILTER(
    # All ports observed by ?observed are also observed by ?observer
    NOT EXISTS {
      ?obsd_ports gds-ir:hasPort ?p .
      FILTER NOT EXISTS { ?obs_ports gds-ir:hasPort ?p }
    }
  )
}
```

This is significant. The information asymmetry condition was identified in Entry 7 as "the hard problem that topology cannot capture." It turns out that the *structural component* — who observes a superset of whom — is topological and is capturable. What remains uncapturable is the *semantic component* — whether the additional information is orthogonal to the generator's model, which depends on content, not structure.

### What this means for the taxonomy

The taxonomy now has three axes, not one:

1. **Operator class:** `.feedback()` vs `.loop()` vs nested combinations — determines state dynamics
2. **Observation symmetry:** symmetric vs asymmetric `x` channels — determines information advantage
3. **Commitment enforcement:** whether the state update `Mechanism` is monotonic — determines whether the loop converges or cycles

The failure modes correspond to degradation along each axis:

| Axis | Healthy | Degraded | Failure mode |
|------|---------|----------|-------------|
| Operator class | Matches domain dynamics | Mismatched (using `.feedback()` for accumulating state) | Wrong convergence criterion |
| Observation symmetry | Evaluator observes superset | Symmetric observation | Mode collapse / sycophancy |
| Commitment enforcement | Monotonic store | Retractions allowed | Sophistry / cycling |

### The normative application

This surfaces the connection back to SA as a methodology. SA's Design → Audit → Synthesize loop is itself an instance of structured antagonism with specific choices on all three axes:

- **Operator:** `.loop()` — the spec accumulates across phases, each phase builds on the previous
- **Observation:** Asymmetric — the Auditor sees the full design output plus structural properties (gaps, contradictions) that the Designer did not surface
- **Commitment:** Enforced — the Halt on Uncertainty principle is commitment enforcement. Once a gap is surfaced, it cannot be papered over. The methodology is monotonic: findings accumulate, they are not retracted

SA is a `.loop()` system with asymmetric observation and enforced commitment. Its failure mode (when the methodology breaks down) is sophistry — the loop produces ever-expanding specifications without converging, or the audit is too shallow (symmetric observation), or the halt gates are overridden (commitment violation).

This is the direct path from the formal taxonomy back to the methodology: **the composition topology prescribes the instrument design.** Given a convergence target, the taxonomy tells you which operator class, observation structure, and commitment mechanism to build.

---

## Open Questions (revised)

- **Is the operator lattice bounded?** Does `.loop().loop().loop()` collapse to `.loop().loop()`, or does each additional nesting level produce meaningfully different convergence dynamics?
- **Can commitment enforcement be expressed as a GDS verification check?** The check would need to inspect the `Mechanism` update rule for monotonicity — but update rules are behavior, not topology. This may require extending the framework.
- **What generates a fourth axis?** The three axes (operator, observation, commitment) were discovered by examining three systems. Are there antagonistic systems that vary on an axis not yet identified?
- **Does the Hegelian case require a new operator?** Aufhebung transforms the state space itself. If `.loop()` can only iterate within a fixed state space, Hegelian dialectic may require an operator that *lifts* — expanding the state space with each iteration. This would be a genuinely new GDS primitive.
- **Is the taxonomy predictive?** The strong claim is that knowing the composition topology, observation structure, and commitment mechanism is *sufficient* to predict the convergence dynamics and failure modes. The weak claim is that it is *necessary but not sufficient* — the information content (semantics) still matters. Which claim holds?

---

## Entry 10: Prior Art — Fan/Toni (2016) and the Gap This Project Occupies

**Date:** 2026-03-29

### The closest prior work

Fan & Toni, "On the Interplay between Games, Argumentation and Dialogues" (AAMAS 2016, pp. 260-268) establishes three formal results connecting game theory, argumentation, and dialogues:

1. **Static equivalence (Theorem 3.1, 3.2):** By mapping a two-player normal-form game into an Assumption-Based Argumentation (ABA) framework, computing dominant solutions and Nash equilibria is provably equivalent to computing admissible sets of arguments. The payoff matrix becomes ABA rules; strategies become assumptions; preferences over outcomes become contraries.

2. **Dynamic equivalence under incomplete information (Theorem 4.1):** When agents have private payoff functions and must exchange information to find Nash equilibria, constructing a successful ABA dialogue is equivalent to computing the equilibrium. A dialogue δ constructed with the thorough strategy is successful iff the claim pair is a dominant solution / Nash equilibrium.

3. **Mechanism design on dialogues (Theorem 5.1, Corollary 6.1):** By treating the dialogue itself as a game and using reverse game theory, agents using specific utility definitions are incentivized to be truthful and disclose relevant information, guaranteeing convergence to Nash equilibria even when payoffs are private.

### The precise distinction

The distinction between Fan/Toni's result and ours can be stated exactly:

- **Fan/Toni:** equilibrium ↔ admissible extension (output equivalence between solution concepts)
- **This project:** `.feedback()` / `.loop()` / nested `.loop()` composition topology ↔ convergence dynamics ↔ failure modes (process topology equivalence)

These are formally independent. Fan/Toni's result would be a *consequence* of ours if ours holds — if two systems share feedback topology, their fixed points should have equivalent structure — but their result does not imply ours. They prove the endpoints are equivalent; we claim the paths to those endpoints are the same shape.

Fan/Toni's paper is exclusively about two-player normal-form games. It does not address feedback topology, repeated games, or iterative processes. The equivalence it establishes is between static objects (a solution concept and a set-theoretic property), not between dynamic processes. Theorem 4.1 does establish a dynamic result — dialogues converge to equilibria — but the dialogue is a specific ABA protocol, not an arbitrary feedback process. The result says "this specific protocol computes equilibria," not "any process with this topology converges."

### The commitment-store asymmetry as a contribution not in Fan/Toni

Fan/Toni model agents as symmetric with respect to dialogue history. Each agent has a private ABA framework, and the dialogue constructs a joint framework incrementally. There is no entity tracking the cumulative history of concessions in a way that is asymmetrically accessible.

The Euthyphro annotation introduces exactly this: a three-entity model where the Dialogue entity owns the commitment store as world-state, Socrates has full trajectory access (via `Socrates View`), and Euthyphro only observes the current state (via `Euthyphro View`). This asymmetry is what makes aporia-as-cycle detectable — it requires comparing the current definition against a refutation history that one party has tracked and the other has not. Socrates can invoke D-12.1 at T225 because he performed the derivation and tracked it; Euthyphro needs to be reminded ("Have you forgotten?").

This asymmetric world-state structure is absent from Fan/Toni, from the broader ABA dialogue literature, and from the existing argumentation-game equivalence results generally. It is a structural contribution of this project.

### Position in the literature

The existing literature establishes three pairwise bridges:

| Bridge | Result | Level |
|--------|--------|-------|
| Game theory ↔ Argumentation | Fan/Toni 2016; Grossi 2013 | Solution concepts / proof procedures |
| Game theory ↔ Biology | Evolutionary game theory (ESS, replicator equations) | Fitness dynamics |
| Argumentation ↔ Biology | *None found* | — |

What does not exist:
- A unified taxonomy classifying game-theoretic, argumentation, and biological systems by *feedback topology*
- Any cross-domain comparison that includes Socratic elenchus, GANs, and biological coevolution as instances of the same formal class
- Any framework that predicts failure modes (mode collapse, sophistry, sycophantic consensus) as structurally equivalent across domains
- Any connection between the argumentation-game equivalence and the Open Games / compositional game theory framework (GDS-Core)

This project occupies the gap: a topology-level classification rather than a solution-concept-level equivalence, using compositional game theory (OGS/GDS) as the formal vocabulary rather than ABA or classical game theory.

---

## Entry 11: The Orthogonal Evaluator Model — When Does Antagonism Produce Genuine Improvement?

**Date:** 2026-03-29

### The problem

The taxonomy classifies antagonistic systems by composition topology and predicts failure modes. But it does not answer the harder question: **when does adversarial process converge to genuine quality versus confident consensus around the wrong answer?**

This is the synthesis gap named in Entry 2. The taxonomy tells you *what kind* of system you have. It does not tell you whether that system will produce a good result.

### Three non-equivalent definitions of "genuine improvement"

1. **Convergence to a fixed point** — the system reaches a stable state (Nash equilibrium, stable extension, aporia). Measurable, but does not distinguish genuine improvement from cycling around a wrong answer. Fan/Toni (2016) proved this for ABA dialogues.

2. **Reduction of exploitable inconsistency** — the commitment store shrinks toward coherence, or the hypothesis space narrows toward consistency. This is what the elenchus measures: the trajectory moves toward a state where no consistent definition survives. Quality is measured by whether the inconsistencies surfaced are genuine (productive) or manufactured (sophistic).

3. **Approach to ground truth** — the output gets closer to something independently verifiable. This is what GAN training claims when it converges (`p_g → p_data`), but it requires an external reference that most real multi-agent systems do not have.

**Definition 2 is the one the project's formal apparatus can operationalize.** Definition 1 is already proved by Fan/Toni. Definition 3 requires external ground truth not available in most domains. Definition 2 — reduction of exploitable inconsistency — is what the commitment store annotation tracks and what the topology predicts.

### The Orthogonal Evaluator Model (OEM)

The key structural insight from the existing work: genuine improvement requires the evaluator to have access to signals orthogonal to the generator's information channel. When that condition fails, you get mode collapse or sycophancy. When it holds, you get productive antagonism.

This suggests a model where the orthogonality condition is the central variable — not a background assumption but a tuneable parameter.

**Three components:**

1. **Generator G** — proposes hypotheses, definitions, solutions. In the elenchus: Euthyphro. In GANs: the generator network. In peer review: the submitting author.

2. **Evaluator E** — assesses proposals against a scoring function. The critical variable is `ρ(E, T)` — the correlation between E's scoring function and ground truth T. When `ρ = 1`, E perfectly tracks truth. When `ρ = 0`, E's signal is orthogonal noise. When `ρ = -1`, E is adversarial with no truth-tracking.

3. **Shared information channel I** — the overlap between G's hypothesis space and E's evaluation criteria. When `|I|` is large (they share the same model of the world), E mirrors G and you get sycophancy. When `|I|` is small (E has genuinely independent signal), you get productive tension.

**The convergence condition:**

Genuine improvement (definition 2: reduction of exploitable inconsistency) occurs when:

- `ρ(E, T) > ρ(G, T)` — the evaluator has better access to truth than the generator
- `|I|` is bounded below a threshold — the shared channel is not so large that E collapses into G's distribution

**Failure mode mapping:**

| Condition | Result |
|-----------|--------|
| `ρ(E,T)` high, `|I|` small | Productive antagonism — evaluator has independent leverage |
| `|I|` → max | Sycophancy / mode collapse — evaluator mirrors generator |
| `ρ(E,T)` low, `ρ(G,E)` high | Sophistry — generator tracks evaluator instead of truth |
| `ρ(E,T) ≈ ρ(G,T)`, both low | Cycling — neither has truth access, no convergence |

### Mapping to existing models

| System | `ρ(E,T)` | `|I|` | Prediction | Observed |
|--------|----------|-------|------------|----------|
| Euthyphro (productive) | High — logical consistency is truth-tracking | Small — Socrates has trajectory, Euthyphro doesn't | Productive | Aporia (genuine) |
| GAN (productive) | High — discriminator has real data | Small — discriminator sees real samples, generator sees noise | Productive | Nash equilibrium |
| GAN (mode collapse) | Degrades over training | Grows — generator learns discriminator's distribution | Sycophancy | Mode collapse |
| Sophist vs Socrates | Low — sophist tracks questioner, not truth | Large — sophist reads evaluator | Sophistry | Unbounded growth |
| Peer review (productive) | Medium — reviewer has domain expertise | Small — reviewer has different perspective from author | Productive | Published, improved |
| Peer review (paradigm lock-in) | Degrades — reviewers share paradigm | Large — all reviewers trained on same literature | Sycophantic consensus | Paradigm lock-in |

### How this resolves the "hard problem"

The information asymmetry condition — identified in Entry 7 as "the hard problem that topology cannot capture" — is now parameterized:

- **`|I|`** is the structural component. It is partially capturable in GDS topology: if the evaluator's `x` channel observes ports not present in the generator's `x` channel (as detected by our SPARQL observation asymmetry query), that is evidence of small `|I|`. The asymmetric projection blocks in the Euthyphro and SA loop models encode this structurally.

- **`ρ(E,T)`** is the semantic component. It cannot be captured by topology alone — it depends on whether the evaluator's signal is actually truth-tracking, which is a content question. This is the genuinely irreducible limitation: topology tells you the structure permits productive antagonism, but not whether the evaluator is actually competent.

The synthesis gap is now formally statable: **what is the minimum `ρ(E,T)` required for productive antagonism, and how does it depend on `|I|`?** This is analogous to PAC-learning's sample complexity question: how much signal does the evaluator need to drive genuine improvement? The answer likely depends on the complexity of the generator's hypothesis space — a richer generator requires a more truth-tracking evaluator.

### GDS encoding path

`ρ(E,T)` and `|I|` can be encoded as `ParameterDef` entries on the `GDSSpec`, annotating the wiring between evaluator and generator. The productive antagonism condition becomes a custom verification check:

```python
@gds_check(check_id="SA-OEM-001", severity="warning")
def check_orthogonal_evaluator(system: SystemIR) -> list[Finding]:
    """Productive antagonism requires evaluator's observation ports
    to include tokens not present in generator's observation ports."""
    # Extract forward_in tokens for decision-type blocks
    # Check that evaluator's tokens are a strict superset
    # If symmetric: warn "sycophancy risk — shared information channel"
    ...
```

This would run on any GDS model and flag systems where the evaluator and generator share the same observation channels — a structural precondition for sycophancy.

### The fourth model confirms the theory

The SA Design-Audit-Synthesize loop, classified as `pursuit_evasion` alongside the Euthyphro, has:
- `ρ(E,T)` high — the Auditor checks structural properties (gaps, contradictions) that are independently verifiable
- `|I|` small — the Auditor observes 4 channels (Spec History + Current Spec State + Prior Findings + Revised Spec) while the Designer observes 2 (Current Spec State + Audit Findings)
- Prediction: productive antagonism
- Observed: the methodology works when applied correctly; fails (sophistry) when audit is shallow (`ρ(E,T)` drops) or halt gates are overridden (`|I|` grows because auditor defers to designer)

SA and the Euthyphro are not just topologically equivalent — they are equivalent on the OEM parameters too. The methodology was designed, unknowingly, to maximize `ρ(E,T)` (independent structural review) and minimize `|I|` (role separation between designer and auditor). The ten principles are engineering choices that tune the OEM parameters toward productive antagonism.

---

## Known Limitations of the Formalism

### Terminal conditions are strings, not computable predicates (F-006)

GDS `TemporalLoop.exit_condition` and OGS `CorecursiveLoop.exit_condition` accept a free-form string description, not a computable predicate. The claim that a system "converges" or "reaches aporia" is asserted *outside* the formal system — GDS can verify structural properties of the composition (wiring correctness, type matching, acyclicity) but cannot verify that a loop terminates.

This means our convergence claims (Nash equilibrium for GAN, aporia for elenchus, Elo stability for co-scientist) are external to the formalism. The taxonomy classifies systems by *structural preconditions for convergence*, not by convergence itself. Making convergence computable would require extending GDS with state predicates — a significant framework addition.

### Naming mismatch between IR layers (F-004)

The GDS SystemIR uses `is_temporal` for corecursive wirings. The OGS IR uses `is_corecursive`. The RDF export via `gds-owl` uses `isTemporal` (from the GDS layer). These refer to the same property but the naming is inconsistent across layers. This is a `gds-owl` framework issue, not a modeling error. SPARQL queries should use `isTemporal`; Python code working with PatternIR should use `is_corecursive`.

### S-005 false positive for environment-sourced utility (F-001/F-002)

OGS check S-005 requires every `DecisionGame` to have an incoming contravariant flow from another game. In the GAN topology, the Discriminator's utility signal (Ground Truth Label) comes from the external environment (training data), not from another player. S-005 produces a warning (not an error) for this topology. The signal is provided via `PatternInput`, which S-005 does not inspect. This is documented in `models/gan/artifacts/verification.txt`.

---

## Entry 9: Leibo, Social Generalization, and Commitment Store Ownership

**Date:** 2026-03-29

### Source

Leibo's work on evaluating multi-agent AI systems (Melting Pot, Concordia) and the distinction between Small Worlds (enumerated states, Nash equilibrium) and Large Worlds (unknown unknowns, evolutionary dynamics).

### What this changes

**1. The elenchus is mixed-motivation, not zero-sum.**

The taxonomy of strategic situations distinguishes pure conflict, pure common interest, and mixed motivation. The Socratic elenchus is mixed-motivation: Euthyphro wants to appear knowledgeable *and* find the truth; Socrates wants to expose inconsistency *and* find the truth. They share one objective and conflict on another. This means an evasion by Euthyphro is not a competitive move in a zero-sum sense — it is a mixed-motivation agent prioritizing one objective (reputation) over another (inquiry). The annotation schema should encode this as `game_type: "mixed_motivation"` with explicit objective decomposition per player.

**2. Observation asymmetry is social generalization.**

Leibo's key metric — generalization to strangers — maps onto the Socratic asymmetry. Socrates is a domain-general evaluator: his elenctic method works on any interlocutor, any topic. He extracts commitments from whoever is in front of him using a substrate-independent strategy. Euthyphro is hyper-specialized: his responses are contingent on his specific beliefs about piety. In multi-agent evaluation terms, Socrates generalizes; Euthyphro overfits to his own training distribution.

**3. Sophistry is formally analogous to "Graduate Student Gradient Descent."**

The failure mode where researchers repeatedly adjust a model based on test results, destroying generalization validity. Sophistry is structurally identical: the respondent adjusts their definition based on each refutation, producing a trajectory that tracks the critic's objections rather than converging on the nature of the thing. Both are **overfitting to the evaluator** — and both are detectable as trajectories where the store grows without convergence (in ML terms: training loss decreases but test loss does not).

**4. Commitment store ownership: world-state, not character-state.**

The Concordia architecture uses a Game Master (GM) / Player split: the GM owns world-state and resolves consequences of actions; players own character-state (beliefs, goals, memories). Applied to the elenchus:

- **Euthyphro** (character-state): beliefs about piety, goal to appear knowledgeable, current definition
- **Socrates** (character-state): elenctic strategy, question selection, goal to expose inconsistency
- **Dialogue Logic** (world-state): commitment store, refutation history, consistency status

The commitment store is *world-state*. Neither Socrates nor Euthyphro owns it. Socrates acts as a *partial GM* by invoking the store ("Were we not saying that...?"), but he doesn't own it any more than a player who remembers the board state owns the board. The annotator — who reconstructs the store from the text — is functioning as the post-hoc GM.

In GDS terms, this means three entities:

```python
euthyphro_state = entity("Euthyphro",
    beliefs=state_var(BeliefSet),
    current_definition=state_var(Definition))
socrates_state = entity("Socrates",
    strategy=state_var(Strategy),
    question_target=state_var(CommitmentRef))
dialogue_state = entity("Dialogue",
    commitment_store=state_var(CommitmentStore),
    refutation_history=state_var(RefutationHistory),
    consistency_status=state_var(ConsistencyStatus))
```

The `Commitment Update` mechanism in the current model is already structurally this — it's a `CovariantFunction` with no agency, updating world-state based on both players' outputs. But it should be made explicit that this is world-state owned by the dialogue logic.

### LLM bias mitigation for annotation extraction

When using an LLM for Phase B (structural extraction), the LLM has read the Euthyphro, read the secondary literature, and has implicit views about the commitment stores. This is a detectable bias, not an uncontrolled one.

**Protocol: dual-pass with divergence detection.**

1. **Context-minimal pass:** Give the LLM only the raw Jowett text. No schema, no mention of commitment stores or GDS. Ask: "Segment this dialogue into turns. For each turn, identify the speaker, classify the speech act, and list what the speaker asserts or concedes." This produces a naive extraction.

2. **Schema-informed pass:** Give the LLM the full annotation schema and the raw text. Ask it to populate the schema, flagging `confidence: low` wherever uncertain.

3. **Divergence detection:** Diff the two passes. Divergences indicate one of:
   - The LLM's training data is supplying a scholarly interpretation the text doesn't support (contamination)
   - The schema is forcing a distinction the naive reading doesn't surface (schema doing useful work)
   - The text is genuinely ambiguous (flag for manual review)

This treats the LLM's prior knowledge as detectable bias. Convergence between passes increases confidence. Divergence is the signal for human judgment.
