# Annotation Methodology: Euthyphro Commitment Store

*Schema, methodology, and failure modes for annotating the Platonic dialogue as a pursuit-evasion game.*

---

## The Core Distinction

The schema encodes a three-way distinction that most annotation efforts collapse into two:

- **Assertion** — a speaker says P, but has not been held to P and could retract it without logical cost
- **Commitment** — a speaker has conceded P in a way that Socrates can subsequently invoke as binding; retraction requires explicit acknowledgment of inconsistency
- **Presupposition** — P is implicit in what the speaker said; neither party has surfaced it, but it is available for Socratic exploitation

The GDS encoding cares about this because the game's asymmetry is precisely that Socrates accumulates the commitment store without adding to his own, while Euthyphro's store grows until it cycles. Conflating assertion with commitment loses the asymmetry. Ignoring presupposition misses half of what Socrates is actually doing.

---

## Terminal Condition: Circularity, Not Inconsistency

The Euthyphro does not end in flat inconsistency (P and not-P in the store). It ends in **circularity**: Definition 5 reduces to Definition 3, which was already shown to give an attribute (pathos) rather than an essence (ousia). The store is not contradictory — it is exhausted. Every new definition either contradicts a prior commitment or reduces to an already-refuted one.

Socrates states this explicitly (Stephanus 15b-c): *"the argument comes round to the same point."*

In GDS terms, the exit condition is: **the commitment store trajectory enters a cycle** — the latest definition maps onto a prior one already marked as refuted or attribute-only. This is detectable as a property of the store's history, which is why Socrates needs the full commitment history (asymmetric observation).

Sophistry (the failure mode) is specifically unbounded growth without cycle — the evader's counter-strategy is to ensure the trajectory never revisits a prior definition.

---

## Schema (v2.0)

```json
{
  "dialogue": "Euthyphro",
  "schema_version": "2.0",
  "translation_base": "Jowett (Gutenberg #1642)",
  "translation_secondary": "Grube/Cooper (Hackett)",
  "normalization_rules": "see section below",

  "game_type": "mixed_motivation",
  "objective_structure": {
    "shared": ["find the truth about piety"],
    "conflicting": {
      "euthyphro": "appear knowledgeable (reputation)",
      "socrates": "expose inconsistency in definitions (elenctic method)"
    },
    "note": "Evasion = Euthyphro prioritizing reputation over inquiry. Socratic persistence = Socrates prioritizing exposure over social comfort."
  },

  "state_ownership": {
    "character_state": {
      "euthyphro": "beliefs, current definition, goal prioritization",
      "socrates": "strategy, question target, elenctic method"
    },
    "world_state": {
      "owner": "Dialogue Logic (no agency — CovariantFunction in GDS)",
      "contents": "commitment store, refutation history, consistency status",
      "write_rule": "Speech acts from both players trigger writes. Conditionals enter on ratification, discharge on antecedent concession, retract on antecedent retraction."
    }
  },

  "definition_map": [
    {
      "id": "D1",
      "stephanus": "5d-6e",
      "content": "Piety is prosecuting wrongdoers (example, not definition)",
      "refutation_type": "methodological",
      "refutation_summary": "An example is not a definition — no eidos given",
      "reduces_to": null,
      "status": "refuted"
    },
    {
      "id": "D2",
      "stephanus": "6e-8a",
      "content": "Piety is what is dear to the gods",
      "refutation_type": "internal_contradiction",
      "refutation_summary": "Gods disagree — same act is both pious and impious",
      "reduces_to": null,
      "status": "refuted"
    },
    {
      "id": "D3",
      "stephanus": "9e-11b",
      "content": "Piety is what all the gods love",
      "refutation_type": "essence_vs_attribute",
      "refutation_summary": "God-lovedness is a pathos (attribute), not the ousia (essence) — the Euthyphro dilemma",
      "reduces_to": null,
      "status": "refuted"
    },
    {
      "id": "D4",
      "stephanus": "12d-14b",
      "content": "Piety is that part of justice concerned with care (therapeia) of the gods",
      "refutation_type": "definitional_collapse",
      "refutation_summary": "Care normally improves its object; gods cannot be improved; therapeia is inapplicable",
      "reduces_to": null,
      "status": "refuted"
    },
    {
      "id": "D5",
      "stephanus": "14b-15c",
      "content": "Piety is knowledge of sacrifice (giving) and prayer (asking)",
      "refutation_type": "circular_regression",
      "refutation_summary": "Giving what pleases the gods = what the gods love = D3 (already refuted as attribute not essence)",
      "reduces_to": "D3",
      "status": "refuted_by_cycle"
    }
  ],

  "terminal_condition": {
    "type": "cycle",
    "cycle_closes_at": "D5",
    "cycle_closes_to": "D3",
    "mechanism": "D5 reduces to 'what the gods love' which is D3, already shown to give attribute not essence. The discharged conditional from turn 6 (if god-love defines piety then we have attribute not essence) makes the cycle mechanically detectable.",
    "stephanus": "15b-c"
  },

  "turns": [
    {
      "turn_id": "integer, 1-indexed",
      "stephanus": "string — Stephanus range e.g. '5d-6e'",
      "speaker": "Socrates | Euthyphro",
      "text_jowett": "string — verbatim Jowett passage",
      "text_grube": "string — corresponding Grube passage, or null",
      "translation_divergence": {
        "flagged": "boolean",
        "note": "string — philosophically significant divergence, or null"
      },
      "speech_act": {
        "primary": "propose | challenge | concede | retract | clarify | evade | question",
        "secondary": "optional second act if the turn does both, or null",
        "note": "string — brief justification for classification"
      },
      "commitment_delta": {
        "added": [
          {
            "holder": "Socrates | Euthyphro",
            "proposition": "string — normalized propositional form",
            "type": "commitment | assertion | presupposition | conditional_commitment",
            "antecedent": "string — for conditional_commitment only, or null",
            "consequent": "string — for conditional_commitment only, or null",
            "antecedent_status": "string — e.g. 'conceded at turn 6', or null",
            "discharged": "boolean — true if antecedent conceded and consequent active, or null",
            "source": "explicit | extracted | implicit",
            "available_to": "both | socrates_only | euthyphro_only",
            "confidence": "high | medium | low",
            "note": "string — justification, especially for medium/low"
          }
        ],
        "removed": [
          {
            "holder": "Socrates | Euthyphro",
            "proposition": "string — must match prior store exactly",
            "removal_type": "retraction | superseded | refuted | discharged",
            "note": "string"
          }
        ],
        "suspended": [
          {
            "holder": "Socrates | Euthyphro",
            "proposition": "string",
            "reason": "string — why suspended rather than removed or retained"
          }
        ]
      },
      "commitment_store": {
        "socrates": ["list of active propositions"],
        "euthyphro": ["list of active propositions"],
        "dialogue": ["list of world-state propositions (discharged conditionals, refutation records)"]
      },
      "cycle_signal": {
        "flagged": "boolean",
        "current_definition": "string — definition ID e.g. 'D5'",
        "maps_to": "string — prior definition ID e.g. 'D3'",
        "via": "string — the chain of reductions",
        "discharged_conditional": "string — the conditional that makes the cycle mechanically detectable"
      },
      "annotation_confidence": "high | medium | low",
      "annotation_notes": "string — uncertain, contested, or requiring cross-check"
    }
  ]
}
```

---

## Schema Design Decisions

### Why `suspended` in addition to `added` and `removed`?

Some propositions are neither active nor retracted — they are deferred. When Euthyphro introduces a new definition, his previous definition is not formally retracted (he never says "I was wrong"); it is displaced. The GDS encoding distinguishes a superseded commitment from a retracted one: a retracted commitment cannot be invoked later; a superseded one arguably can — and Socrates sometimes does invoke earlier concessions.

### Why `source: explicit | extracted | implicit`?

This is where the philosophical judgment lives.
- **Explicit**: speaker states P in first-person assertoric form
- **Extracted**: Socrates draws P out through questioning and speaker ratifies (says yes)
- **Implicit**: P follows from what was conceded but neither party has surfaced it — a presupposition available for later exploitation

The GDS encoding needs this because the game's information structure depends on what each player *knows they have committed to*.

### Why `confidence` on individual propositions?

Some commitment inferences are uncontroversial; some are genuinely contested in the scholarly literature. Low-confidence propositions are candidates for cross-checking against Grube and annotation notes.

### Why `conditional_commitment` as a fourth type?

Socrates introduces conditional propositions ("if piety is what pleases the gods, then...") and Euthyphro ratifies them by engaging with the consequent. A ratified conditional is the mechanism by which Socrates constructs the cycle — the Euthyphro dilemma ("is the pious loved because it is pious, or pious because it is loved?") is a conditional that, once Euthyphro picks a horn, binds everything downstream.

The Dialogue entity's write rule for conditionals:

1. **Entry:** Conditional enters the store when the speaker ratifies it (engages with consequent without rejecting antecedent). Type: `conditional_commitment`, `discharged: false`.
2. **Discharge:** Conditional discharges to full commitment when the antecedent is independently conceded. `discharged: true`, consequent becomes active.
3. **Retraction:** Conditional is retracted if the antecedent is retracted. `removal_type: discharged`.

This follows the natural deduction discharge rule: conditional introduction followed by modus ponens when the antecedent is established. Without this, the cycle graph cannot close mechanically — the link between "piety causes god-love" and "god-love cannot define piety" would require inference rather than store lookup.

### Why `definition_map` as a top-level object?

The five definitions and their refutation types form a directed graph (D5 → D3 via `reduces_to`). This graph is the cycle that constitutes aporia. Making it a first-class object rather than something reconstructed by traversing turns means:

- The Dialogue entity can detect cycles by checking `reduces_to` pointers
- The annotation can be validated: does the `reduces_to` chain actually form a cycle?
- The GDS encoding can use the definition map as the exit condition's formal target

### Why `available_to` on each commitment?

Captures the information asymmetry at the commitment level. Most commitments are `available_to: "both"`. But presuppositions extracted by Socrates' questioning may be `available_to: "socrates_only"` — Euthyphro ratified the proposition without realizing he committed to it. This is the mechanism by which Socrates functions as a partial GM: he tracks commitments that the interlocutor does not know are in the store.

### Why `dialogue` in the commitment store alongside `socrates` and `euthyphro`?

The three-entity model requires world-state to be tracked separately from character-state. The `dialogue` store holds discharged conditionals, refutation records, and the consistency status — propositions that are properties of the argument structure, not of either player's beliefs. This is what the Dialogue entity (the CovariantFunction in GDS) writes.

### Why `cycle_signal` instead of `aporia_signal`?

The terminal condition is circularity (trajectory enters a cycle), not flat inconsistency (P and not-P). The cycle signal names: the current definition ID, the prior definition it maps to, the chain of reductions, and the discharged conditional that makes the cycle mechanically detectable.

### Why normalized propositional form?

The `commitment_store` at each turn must be a stable list diffable programmatically. If turn 7 adds "Piety is what pleases the gods" and turn 12 removes it, those strings must match exactly. Normalization rules are defined below.

---

## Normalization Rules

Define before annotating turn 1. Do not deviate.

1. **Third-person propositional form.** Not "I believe piety is X" but "Piety is X."
2. **Consistent entity naming.** Use: "piety", "the gods", "Euthyphro's father". Not: "it", "they", "him".
3. **Strip indexicals and dialogue context.** Not "what I am doing now" but "prosecuting one's father for wrongdoing is an instance of piety."
4. **Preserve semantic distinctions.** "Piety is what is dear to the gods" and "Piety is what all the gods love" are DIFFERENT propositions. The first is about individual gods; the second requires unanimity. Do not normalize to equivalence — Socrates exploits this exact distinction.
5. **Conditionals stay conditional until discharged.** "If the gods disagree, the same act is both dear and hateful" stays conditional in the store as `type: "conditional_commitment"` with explicit `antecedent` and `consequent` fields. Do not flatten to "the same act is both dear and hateful" until `discharged: true`. When discharged, the consequent enters the store as a full commitment.
6. **Mark scope explicitly.** "Care (therapeia) of X normally improves X" has universal scope. "The gods cannot be improved" is a specific claim about gods. Keep them separate.

---

## Methodology

### Phase A: Preparation

1. Read the full dialogue once without annotating. Map the five definitions and each refutation's structure.
2. Finalize normalization rules (above).
3. Decide turn segmentation: **each speaker change** as the atomic unit. Multi-act turns use `speech_act.secondary`. Very long turns (e.g., Socrates' extended argument at 10a-11b) are one turn with detailed notes.

### Phase B: LLM-Assisted Structural Extraction

Use the LLM for:
- Segmenting turns and assigning Stephanus numbers
- Identifying `speech_act.primary` candidates (flagging for review)
- Flagging Jowett/Grube divergences
- Producing candidate propositions per turn (raw, not normalized)

Do NOT use the LLM for:
- Deciding commitment vs assertion vs presupposition
- Populating `commitment_store` at any turn
- Deciding `removal_type`
- Any judgment that requires interpreting what is *conceded* vs merely *said*

### Phase C: Human Annotation Pass

For each turn:
1. Read Jowett. Read Grube if flagged. Note divergence.
2. Classify speech act.
3. Decide what was added/removed/suspended from whose store, and why.
4. Write normalized propositions.
5. Update cumulative store.
6. Flag cycle signals.

Do this in a single sitting per dialogue section if possible.

### Phase D: Consistency Audit

After full pass:
1. Verify every `removed` proposition matches an exact string in a prior `commitment_store`
2. Verify `commitment_store` at each turn is the cumulative result of all deltas
3. Identify all `low` confidence annotations for cross-checking
4. Verify the cycle signal at the terminal turn correctly names the cycle (Definition 5 → Definition 3 → attribute-not-essence refutation)

---

## Failure Modes

### 1. Conflating what Euthyphro said with what he committed to

Not everything Euthyphro says enters his commitment store. Only what he has conceded under questioning, or asserted in a way Socrates can bind him to, is a commitment. When uncertain, mark `assertion` with `confidence: low`.

### 2. Ignoring asymmetric commitment extraction

Socrates asks questions; he rarely asserts. But his questions carry presuppositions that Euthyphro ratifies by answering without objection. Watch for this especially in later refutations where Socrates' questions get architecturally complex.

### 3. Normalizing propositions too aggressively

"Piety is what is dear to the gods" and "Piety is what all the gods love" are DIFFERENT propositions. Normalize for syntactic consistency, not semantic equivalence. When in doubt, keep distinct.

### 4. Marking retraction when the text shows evasion

Euthyphro almost never explicitly retracts. He shifts, qualifies, evades. Evasion means the prior commitment may still be active and available for Socratic reinvocation. Mark as `suspended`, not `removed`.

### 5. Letting GDS encoding goals bias annotation

The annotation should be capable of falsifying the GDS model. If the commitment store is messier than the model expects, that is a finding.

### 6. Inconsistent Stephanus referencing

Cite the range of each turn, not just the start. Be consistent.
