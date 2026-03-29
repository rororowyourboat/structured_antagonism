"""Socratic Elenchus (Euthyphro) — OGS game structure.

Encodes the Platonic dialogue as a two-player pursuit-evasion game
with cross-timestep temporal iteration (.loop() / corecursive operator).
This is the "pursuit-evasion antagonism" class in the structured
antagonism taxonomy.

The key structural properties:
1. Asymmetric observation — Socrates sees the full commitment store
   history; Euthyphro sees only the current commitment state.
2. Accumulating state — the commitment store grows across turns via
   .loop() (covariant, cross-timestep), not .feedback().
3. Pursuit-evasion dynamics — Socrates engineers aporia by targeting
   specific prior commitments; Euthyphro tries to maintain coherence.

This distinguishes elenchus from GANs (.feedback(), symmetric, stateless
per-step) and from the AI co-scientist (.loop().loop(), hierarchical).

OGS Game Theory Decomposition:
    Players: Euthyphro (respondent/evader), Socrates (questioner/pursuer)
    State: Commitment store (accumulating, append-only when enforced)

    Composition:
        euthyphro_arm = euthyphro_view >> euthyphro_decision
        socrates_arm = socrates_view >> socrates_decision
        round = (euthyphro_arm | socrates_arm) >> commitment_update
        elenchus = round.corecursive([commitment_store -> views])

    Terminal condition: aporia — commitment store becomes circular or
    internally inconsistent (Definition N collapses into already-refuted
    Definition M).

    Failure mode: sophistry — commitment store grows without bound
    without reaching inconsistency. Evader escapes by shifting ground
    or retracting commitments (violation of monotonicity).

References:
    - Plato, Euthyphro (Stephanus 2a-16a)
    - annotations.json in this directory for commitment store trace
    - Research journal Entry 7-8: taxonomy and formal definition of sophistry
"""

from ogs.dsl.compile import compile_to_ir
from ogs.dsl.composition import (
    CorecursiveLoop,
    Flow,
    ParallelComposition,
    SequentialComposition,
)
from ogs.dsl.games import CovariantFunction, DecisionGame
from ogs.dsl.pattern import Pattern, PatternInput, TerminalCondition
from ogs.dsl.types import CompositionType, InputType, Signature, port
from ogs.ir.models import PatternIR

# ======================================================================
# Observation Projections — asymmetric views of shared state
# ======================================================================

# Euthyphro sees only the current commitment state (local view)
euthyphro_view = CovariantFunction(
    name="Euthyphro View",
    signature=Signature(
        x=(port("Commitment Store"),),
        y=(port("Current Commitments"),),
    ),
    logic=(
        "Projects the full commitment store into the respondent's "
        "local view: the current active commitments without the full "
        "history of how they were established or which were retracted."
    ),
    tags={"role": "projection", "player": "euthyphro"},
)

# Socrates sees the full commitment history (global view)
socrates_view = CovariantFunction(
    name="Socrates View",
    signature=Signature(
        x=(port("Commitment Store"),),
        y=(port("Commitment History"), port("Current Commitments")),
    ),
    logic=(
        "Projects the full commitment store into the questioner's "
        "global view: the complete history of commitments including "
        "which were added, which were retracted, and the dependency "
        "chain between definitions. This asymmetric access enables "
        "the pursuer to target specific prior commitments."
    ),
    tags={"role": "projection", "player": "socrates"},
)

# ======================================================================
# Decision Games — the two players
# ======================================================================

euthyphro_decision = DecisionGame(
    name="Euthyphro",
    signature=Signature(
        x=(port("Current Commitments"), port("Refutation")),
        y=(port("Proposed Definition"),),
        r=(port("Refutation"),),
        s=(port("Euthyphro Response Quality"),),
    ),
    logic=(
        "The respondent observes their current commitments and the "
        "latest refutation from Socrates. They propose a new or "
        "revised definition of piety, attempting to maintain coherence "
        "across all accumulated commitments. Strategy: evade "
        "inconsistency by finding definitions compatible with all "
        "prior concessions."
    ),
    tags={"role": "respondent", "class": "pursuit_evasion"},
)

socrates_decision = DecisionGame(
    name="Socrates",
    signature=Signature(
        x=(port("Commitment History"), port("Current Commitments"),
           port("Proposed Definition")),
        y=(port("Refutation"),),
        r=(port("Euthyphro Response Quality"),),
        s=(port("Socratic Strategy Signal"),),
    ),
    logic=(
        "The questioner observes the full commitment history, the "
        "current active commitments, and the latest proposed definition. "
        "Produces a refutation by identifying: (a) internal contradiction "
        "with prior commitments, (b) conflation of attribute with essence, "
        "(c) circularity with a previously refuted definition, or "
        "(d) methodological error. Strategy: navigate the commitment "
        "space toward inconsistency — engineer aporia."
    ),
    tags={"role": "questioner", "class": "pursuit_evasion"},
)

# ======================================================================
# State Update — commitment store mechanism
# ======================================================================

commitment_update = CovariantFunction(
    name="Commitment Update",
    signature=Signature(
        x=(port("Proposed Definition"), port("Refutation"),
           port("Commitment Store")),
        y=(port("Commitment Store"),),
    ),
    logic=(
        "Updates the commitment store with the new definition and "
        "refutation. The store is append-only (monotonic): new "
        "commitments are added, refuted definitions are marked as "
        "refuted but not removed. This monotonicity is the enforcement "
        "mechanism that prevents sophistry — the evader cannot retract "
        "prior concessions."
    ),
    tags={"role": "mechanism", "class": "pursuit_evasion"},
)


# ======================================================================
# Composition — build the game tree
# ======================================================================


def build_game() -> CorecursiveLoop:
    """Build the Socratic elenchus as a corecursive (temporal) loop.

    Structure:
        euthyphro_arm = euthyphro_view >> euthyphro_decision
        socrates_arm = socrates_view >> socrates_decision
        round = euthyphro_arm >> socrates_arm >> commitment_update
        elenchus = round.corecursive([commitment_store -> views])

    The commitment store accumulates across turns. Each turn adds
    a definition and a refutation. The loop terminates when the
    store becomes inconsistent (aporia) or circular.
    """
    # Euthyphro's arm: view projection >> decision
    euthyphro_arm = SequentialComposition(
        name="Euthyphro Arm",
        first=euthyphro_view,
        second=euthyphro_decision,
        wiring=[
            Flow(
                source_game=euthyphro_view,
                source_port="Current Commitments",
                target_game=euthyphro_decision,
                target_port="Current Commitments",
            ),
        ],
    )

    # Socrates' arm: view projection >> decision
    socrates_arm = SequentialComposition(
        name="Socrates Arm",
        first=socrates_view,
        second=socrates_decision,
        wiring=[
            Flow(
                source_game=socrates_view,
                source_port="Commitment History",
                target_game=socrates_decision,
                target_port="Commitment History",
            ),
            Flow(
                source_game=socrates_view,
                source_port="Current Commitments",
                target_game=socrates_decision,
                target_port="Current Commitments",
            ),
        ],
    )

    # Euthyphro proposes, then Socrates refutes
    dialogue_exchange = SequentialComposition(
        name="Dialogue Exchange",
        first=euthyphro_arm,
        second=socrates_arm,
        wiring=[
            Flow(
                source_game=euthyphro_decision,
                source_port="Proposed Definition",
                target_game=socrates_decision,
                target_port="Proposed Definition",
            ),
        ],
    )

    # Update commitment store with both the proposal and refutation
    dialogue_round = SequentialComposition(
        name="Dialogue Round",
        first=dialogue_exchange,
        second=commitment_update,
        wiring=[
            Flow(
                source_game=euthyphro_decision,
                source_port="Proposed Definition",
                target_game=commitment_update,
                target_port="Proposed Definition",
            ),
            Flow(
                source_game=socrates_decision,
                source_port="Refutation",
                target_game=commitment_update,
                target_port="Refutation",
            ),
        ],
    )

    # Temporal loop: updated commitment store feeds back to both views
    return CorecursiveLoop(
        name="Socratic Elenchus",
        inner=dialogue_round,
        corecursive_wiring=[
            Flow(
                source_game=commitment_update,
                source_port="Commitment Store",
                target_game=euthyphro_view,
                target_port="Commitment Store",
            ),
            Flow(
                source_game=commitment_update,
                source_port="Commitment Store",
                target_game=socrates_view,
                target_port="Commitment Store",
            ),
        ],
        exit_condition="Commitment store becomes circular or internally inconsistent (aporia)",
    )


# ======================================================================
# Pattern — top-level specification with metadata
# ======================================================================


def build_pattern() -> Pattern:
    """Build the complete OGS Pattern for the Socratic elenchus."""
    return Pattern(
        name="Socratic Elenchus (Euthyphro)",
        game=build_game(),
        inputs=[
            PatternInput(
                name="Initial Question",
                input_type=InputType.EXTERNAL_WORLD,
                schema_hint="'What is piety?' — the definitional question",
                target_game="Euthyphro",
                flow_label="Refutation",
            ),
        ],
        composition_type=CompositionType.CORECURSIVE,
        terminal_conditions=[
            TerminalCondition(
                name="Aporia",
                actions={
                    "Euthyphro": "Propose definition",
                    "Socrates": "Show circularity with prior refuted definition",
                },
                outcome=(
                    "The commitment store becomes circular: Definition N "
                    "collapses into already-refuted Definition M. No "
                    "consistent definition survives. The interlocutor "
                    "departs without resolution."
                ),
                description=(
                    "Convergence: pursuit succeeds — the commitment "
                    "space has been navigated to inconsistency."
                ),
                payoff_description="Circular commitment store — D5 reduces to D3",
            ),
            TerminalCondition(
                name="Sophistry",
                actions={
                    "Euthyphro": "Shift ground or retract commitments",
                    "Socrates": "Unable to close contradiction",
                },
                outcome=(
                    "The commitment store grows without bound without "
                    "reaching inconsistency. The evader escapes by "
                    "redefining terms or retracting prior concessions."
                ),
                description=(
                    "Failure mode: pursuit fails — monotonicity of "
                    "commitment store is violated, or evader's strategy "
                    "space is too large to navigate."
                ),
                payoff_description="Unbounded store, no inconsistency",
            ),
        ],
        source="dsl",
    )


def build_ir() -> PatternIR:
    """Compile the Pattern to OGS PatternIR."""
    return compile_to_ir(build_pattern())
