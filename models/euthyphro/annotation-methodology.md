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

## Schema (v3.0)

```json
{
  "dialogue": "Euthyphro",
  "schema_version": "3.0",
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
      "socrates": "strategy, question target, elenctic method, knowledge of derivations"
    },
    "world_state": {
      "owner": "Dialogue Logic (no agency — CovariantFunction in GDS)",
      "contents": "commitment store, derivation records, refutation history, consistency status",
      "write_rules": {
        "commitment": "Written when a speaker ratifies under questioning (question + affirmative response)",
        "assertion": "Written when a speaker volunteers without being bound",
        "presupposition": "Written when the annotator identifies an implicit assumption neither party has surfaced",
        "conditional_commitment": "Written when a speaker ratifies an if/then structure as a unit (antecedent + consequent conceded together)",
        "derivation": "Written when a speaker performs explicit reasoning from premises already in store, in monologue, without interruption or objection from the other party. The write trigger is monologue + silence, not question + ratification."
      }
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
    "mechanism": "D5 reduces to 'what the gods love' which is D3. The derivation record from 10a-11b (piety and god-lovedness have different causal structures, so D3 gives attribute not essence) was never objected to and remains invocable. Socrates invokes it at 15b-c to close the cycle.",
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
            "id": "string — stable identifier e.g. 'C-12.3' (commitment, section 12, item 3)",
            "holder": "Socrates | Euthyphro | Dialogue",
            "proposition": "string — normalized propositional form",
            "type": "commitment | assertion | presupposition | conditional_commitment | derivation",

            "_if_conditional_commitment": {
              "antecedent": "string — the if-clause",
              "consequent": "string — the then-clause",
              "antecedent_status": "string — e.g. 'conceded at T71'",
              "discharged": "boolean — true if antecedent conceded",
              "ratified_by": "Socrates | Euthyphro | null"
            },

            "_if_derivation": {
              "premises": ["list of commitment IDs — e.g. 'C-12.1', 'C-12.2', 'C-12.3'"],
              "conclusion": "string — what the premises jointly entail",
              "derived_by": "Socrates | Euthyphro",
              "presented_at": "string — stephanus reference",
              "objected_to": "boolean — false means the other party did not block",
              "ratified_by": "Socrates | Euthyphro | null — null if silence, name if explicit agreement",
              "invocable_at": ["list of stephanus references where this derivation is later used"]
            },

            "source": "explicit | extracted | implicit | derived",
            "available_to": "both | socrates_only | euthyphro_only",
            "confidence": "high | medium | low",
            "note": "string — justification, especially for medium/low"
          }
        ],
        "removed": [
          {
            "holder": "Socrates | Euthyphro | Dialogue",
            "proposition": "string — must match prior store exactly",
            "removal_type": "retraction | superseded | refuted",
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
        "socrates": ["list of active commitment IDs"],
        "euthyphro": ["list of active commitment IDs"],
        "dialogue": ["list of world-state entries: derivation records, conditional statuses, refutation records"]
      },
      "cycle_signal": {
        "flagged": "boolean",
        "current_definition": "string — definition ID e.g. 'D5'",
        "maps_to": "string — prior definition ID e.g. 'D3'",
        "via": "string — the chain of reductions",
        "closing_derivation": "string — the derivation ID that makes the cycle mechanically detectable"
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

### The five-type taxonomy

The schema distinguishes five types of store entry. Each has a distinct write condition for the Dialogue entity:

| Type | Write condition | Example |
|------|----------------|---------|
| `commitment` | Speaker ratifies under questioning (question + affirmative response) | Euthyphro: "Yes" to "Is piety loved because it is pious?" (T129) |
| `assertion` | Speaker volunteers without being bound | Euthyphro: "Piety is doing as I am doing" (T41) |
| `presupposition` | Annotator identifies implicit assumption neither party has surfaced | "Divine punishment is paradigmatic of piety" (implicit in T41's Zeus/Kronos appeal) |
| `conditional_commitment` | Speaker ratifies an if/then structure as a unit | "If the gods disagree about justice, the same act is both dear and hateful" (Section 9) |
| `derivation` | Speaker performs explicit reasoning from premises already in store, in monologue, without objection | Socrates' argument at T132-T138 deriving that D3 gives attribute not essence |

**The derivation/conditional distinction is critical.** The Euthyphro dilemma (Section 12) was initially analyzed as a conditional commitment. Working through the text turn by turn showed it is actually a derivation: Euthyphro concedes three independent premises under questioning, and Socrates derives the conclusion in monologue. The conditional structure lives in Socrates' argument, not in Euthyphro's store.

- `conditional_commitment`: one speech act ratifying an if/then structure (Section 9 pattern: "if gods disagree, then same act is both pious and impious")
- `derivation`: multiple independent commitments + logical derivation performed by one party (Section 12 pattern: three premises → conclusion that D3 gives attribute not essence)

### Why `conditional_commitment`?

For cases where a speaker ratifies an if/then structure as a unit — not derived from separate premises. The Dialogue entity's write rule:

1. **Entry:** Conditional enters when speaker engages with the consequent without rejecting the antecedent. `discharged: false`.
2. **Discharge:** Conditional discharges when the antecedent is independently conceded. `discharged: true`, consequent becomes active.
3. **Retraction:** Conditional is retracted if the antecedent is retracted.

### Why `derivation`?

For cases where a speaker derives a conclusion from premises already in the store, in monologue, without interruption or objection. The write trigger is **monologue + silence**, not question + ratification. This is where Socrates functions as a partial GM: he performs reasoning about the store that Euthyphro did not perform and may not have tracked.

Key fields:
- `premises`: list of commitment IDs the derivation depends on
- `derived_by`: who performed the reasoning
- `objected_to`: false means the other party did not block the derivation
- `ratified_by`: null (silence) vs named (explicit agreement) — null is the more common case and is what makes the derivation `available_to: socrates_only`
- `invocable_at`: where the derivation is later used (the cycle-closing move at 15b-c)

The `objected_to` field replaces the earlier `discharged` concept for derivations. A derivation is not "discharged" (it has no antecedent) — it is *unopposed*. Euthyphro's failure to object at T132-T138 is itself a speech act: silence under a Socratic derivation is a form of passive ratification.

### Why `definition_map` as a top-level object?

The five definitions and their refutation types form a directed graph (D5 → D3 via `reduces_to`). This graph is the cycle that constitutes aporia. Making it a first-class object rather than something reconstructed by traversing turns means:

- The Dialogue entity can detect cycles by checking `reduces_to` pointers
- The annotation can be validated: does the `reduces_to` chain actually form a cycle?
- The GDS encoding can use the definition map as the exit condition's formal target

### Why `available_to` on each commitment?

Captures the information asymmetry at the commitment level. Most commitments are `available_to: "both"`. But presuppositions extracted by Socrates' questioning may be `available_to: "socrates_only"` — Euthyphro ratified the proposition without realizing he committed to it. This is the mechanism by which Socrates functions as a partial GM: he tracks commitments that the interlocutor does not know are in the store.

### Why `dialogue` in the commitment store alongside `socrates` and `euthyphro`?

The three-entity model requires world-state to be tracked separately from character-state. The `dialogue` store holds derivation records, conditional commitment statuses, and refutation records — propositions that are properties of the argument structure, not of either player's beliefs. This is what the Dialogue entity (the CovariantFunction in GDS) writes. Derivations are the primary content of the dialogue store: they capture Socrates' reasoning about the commitment store, not commitments that either player made.

### Why `cycle_signal` instead of `aporia_signal`?

The terminal condition is circularity (trajectory enters a cycle), not flat inconsistency (P and not-P). The cycle signal names: the current definition ID, the prior definition it maps to, the chain of reductions, and the `closing_derivation` — the derivation record ID that makes the cycle mechanically detectable. At 15b-c, Socrates invokes the Section 12 derivation (D3 gives attribute not essence) against D5 (which reduces to D3), closing the cycle.

### Why normalized propositional form?

The `commitment_store` at each turn must be a stable list diffable programmatically. If turn 7 adds "Piety is what pleases the gods" and turn 12 removes it, those strings must match exactly. Normalization rules are defined below.

---

## Normalization Rules

Define before annotating turn 1. Do not deviate.

1. **Third-person propositional form.** Not "I believe piety is X" but "Piety is X."
2. **Consistent entity naming.** Use: "piety", "the gods", "Euthyphro's father". Not: "it", "they", "him".
3. **Strip indexicals and dialogue context.** Not "what I am doing now" but "prosecuting one's father for wrongdoing is an instance of piety."
4. **Preserve semantic distinctions.** "Piety is what is dear to the gods" and "Piety is what all the gods love" are DIFFERENT propositions. The first is about individual gods; the second requires unanimity. Do not normalize to equivalence — Socrates exploits this exact distinction.
5. **Conditionals stay conditional until discharged; derivations reference premise IDs.** "If the gods disagree, the same act is both dear and hateful" stays conditional as `type: "conditional_commitment"` until `discharged: true`. Derivations are normalized as conclusions with `premises` pointing to commitment IDs — the derivation's proposition is the conclusion, not the argument.
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
