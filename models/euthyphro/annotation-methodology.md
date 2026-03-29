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

## Schema (v1.0)

```json
{
  "dialogue": "Euthyphro",
  "schema_version": "1.1",
  "translation_base": "Jowett (Gutenberg #1642)",
  "translation_secondary": "Grube/Cooper (Hackett)",
  "normalization_rules": "see section below",
  "terminal_condition": "commitment store trajectory enters a cycle",
  "game_type": "mixed_motivation",
  "objectives": {
    "euthyphro": ["appear knowledgeable", "find the truth about piety"],
    "socrates": ["expose inconsistency in definitions", "find the truth about piety"]
  },
  "state_ownership": {
    "character_state": {
      "euthyphro": "beliefs, current definition, goal prioritization",
      "socrates": "strategy, question target, elenctic method"
    },
    "world_state": "commitment store, refutation history, consistency status — owned by dialogue logic, not by either player"
  },
  "turns": [
    {
      "turn_id": "integer, 1-indexed",
      "stephanus": "string — Stephanus reference e.g. '5d-6e'",
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
            "type": "commitment | assertion | presupposition",
            "source": "explicit | extracted | implicit",
            "confidence": "high | medium | low",
            "note": "string — justification, especially for medium/low"
          }
        ],
        "removed": [
          {
            "holder": "Socrates | Euthyphro",
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
        "socrates": ["list of active propositions"],
        "euthyphro": ["list of active propositions"]
      },
      "cycle_signal": {
        "flagged": "boolean",
        "current_definition": "string — if flagged, the current definition",
        "maps_to": "string — the prior definition it reduces to",
        "refutation_of_prior": "string — how the prior was already refuted"
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

### Why `cycle_signal` instead of `aporia_signal`?

The terminal condition is circularity (trajectory enters a cycle), not flat inconsistency (P and not-P). The cycle signal must name: the current definition, the prior definition it maps to, and the refutation that already applied to that prior definition.

### Why normalized propositional form?

The `commitment_store` at each turn must be a stable list diffable programmatically. If turn 7 adds "Piety is what pleases the gods" and turn 12 removes it, those strings must match exactly. Normalization rules are defined below.

---

## Normalization Rules

Define before annotating turn 1. Do not deviate.

1. **Third-person propositional form.** Not "I believe piety is X" but "Piety is X."
2. **Consistent entity naming.** Use: "piety", "the gods", "Euthyphro's father". Not: "it", "they", "him".
3. **Strip indexicals and dialogue context.** Not "what I am doing now" but "prosecuting one's father for wrongdoing is an instance of piety."
4. **Preserve semantic distinctions.** "Piety is what is dear to the gods" and "Piety is what all the gods love" are DIFFERENT propositions. The first is about individual gods; the second requires unanimity. Do not normalize to equivalence — Socrates exploits this exact distinction.
5. **Conditionals stay conditional.** "If the gods disagree, the same act is both dear and hateful" stays conditional. Do not flatten to "the same act is both dear and hateful."
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
