"""Structured Antagonism Design-Audit-Synthesize Loop — OGS game structure.

Encodes SA's own core methodology as a compositional game. The Designer
generates a specification; the Auditor stress-tests it for gaps,
ambiguities, and contradictions; the Synthesizer either produces the
final artifact or halts with questions.

This is a self-referential test: the methodology classifying itself.
The predicted class is pursuit-evasion antagonism (.loop()) with
asymmetric observation and enforced commitment (halt gates).

OGS Game Theory Decomposition:
    Players: Designer (generator), Auditor (evaluator)
    World-state: Spec Store (accumulating findings, halt gates)

    Composition:
        designer_arm = designer_view >> designer
        auditor_arm = auditor_view >> auditor
        round = designer_arm >> auditor_arm >> spec_update
        sa_loop = round.corecursive([spec_store -> views])

    Terminal condition: spec is complete AND compatible (all halt
    gates pass). Halts if gaps remain — prefers silence over
    confabulation.

    Failure mode: sophistry — the loop produces ever-expanding
    specifications without converging, or the audit is too shallow
    (symmetric observation), or halt gates are overridden
    (commitment violation).

References:
    - Research journal Entry 8: SA maps onto the taxonomy
    - docs/manifesto.md: the SA methodology
    - meta/principles.md: the ten principles
"""

from ogs.dsl.compile import compile_to_ir
from ogs.dsl.composition import (
    CorecursiveLoop,
    Flow,
    SequentialComposition,
)
from ogs.dsl.games import CovariantFunction, DecisionGame
from ogs.dsl.pattern import Pattern, PatternInput, TerminalCondition
from ogs.dsl.types import CompositionType, InputType, Signature, port
from ogs.ir.models import PatternIR

# ======================================================================
# Observation Projections — asymmetric views of shared state
# ======================================================================

designer_view = CovariantFunction(
    name="Designer View",
    signature=Signature(
        x=(port("Spec Store"),),
        y=(port("Current Spec State"),),
    ),
    logic=(
        "Projects the spec store into the designer's view: the current "
        "state of the specification without the full audit history. "
        "The designer sees what the spec contains but not the structural "
        "analysis of its gaps and contradictions."
    ),
    tags={"role": "projection", "player": "designer"},
)

auditor_view = CovariantFunction(
    name="Auditor View",
    signature=Signature(
        x=(port("Spec Store"),),
        y=(port("Spec History"), port("Current Spec State"),
           port("Prior Findings")),
    ),
    logic=(
        "Projects the spec store into the auditor's view: the full "
        "history of spec revisions, the current state, AND all prior "
        "audit findings. This asymmetric access enables the auditor "
        "to detect cross-layer contradictions and track whether "
        "previously identified gaps have been addressed."
    ),
    tags={"role": "projection", "player": "auditor"},
)

# ======================================================================
# Decision Games — the two players
# ======================================================================

designer = DecisionGame(
    name="Designer",
    signature=Signature(
        x=(port("Current Spec State"), port("Audit Findings")),
        y=(port("Revised Spec"),),
        r=(port("Audit Findings"),),
        s=(port("Design Quality Signal"),),
    ),
    logic=(
        "The designer receives the current spec state and the latest "
        "audit findings. Produces a revised specification that addresses "
        "identified gaps, resolves ambiguities, and attempts to satisfy "
        "all halt gate conditions. Strategy: ontology first, then "
        "boundaries, then behaviors, then views — epistemic sequencing."
    ),
    tags={"role": "generator", "class": "pursuit_evasion"},
)

auditor = DecisionGame(
    name="Auditor",
    signature=Signature(
        x=(port("Spec History"), port("Current Spec State"),
           port("Prior Findings"), port("Revised Spec")),
        y=(port("Audit Findings"),),
        r=(port("Design Quality Signal"),),
        s=(port("Audit Strategy Signal"),),
    ),
    logic=(
        "The auditor receives the full spec history, current state, "
        "prior findings, AND the latest revision. Produces structured "
        "findings: gaps, ambiguities, contradictions, unstated "
        "assumptions. Checks cross-layer compatibility. Does NOT "
        "prescribe solutions — only diagnoses. Audit before synthesis."
    ),
    tags={"role": "evaluator", "class": "pursuit_evasion"},
)

# ======================================================================
# State Update — spec store mechanism
# ======================================================================

spec_update = CovariantFunction(
    name="Spec Update",
    signature=Signature(
        x=(port("Revised Spec"), port("Audit Findings"),
           port("Spec Store")),
        y=(port("Spec Store"),),
    ),
    logic=(
        "Updates the spec store with the revised specification and "
        "audit findings. The store is append-only: new spec sections "
        "are added, findings accumulate, halt gate decisions are "
        "recorded. Addressed findings are marked resolved but not "
        "deleted. This monotonicity is the Halt on Uncertainty "
        "principle made structural — once a gap is surfaced, it "
        "cannot be papered over."
    ),
    tags={"role": "mechanism", "class": "pursuit_evasion"},
)


# ======================================================================
# Composition — build the game tree
# ======================================================================


def build_game() -> CorecursiveLoop:
    """Build the SA Design-Audit-Synthesize loop.

    Structure:
        designer_arm = designer_view >> designer
        auditor_arm = auditor_view >> auditor
        round = designer_arm >> auditor_arm >> spec_update
        sa_loop = round.corecursive([spec_store -> views])
    """
    designer_arm = SequentialComposition(
        name="Designer Arm",
        first=designer_view,
        second=designer,
        wiring=[
            Flow(
                source_game=designer_view,
                source_port="Current Spec State",
                target_game=designer,
                target_port="Current Spec State",
            ),
        ],
    )

    auditor_arm = SequentialComposition(
        name="Auditor Arm",
        first=auditor_view,
        second=auditor,
        wiring=[
            Flow(
                source_game=auditor_view,
                source_port="Spec History",
                target_game=auditor,
                target_port="Spec History",
            ),
            Flow(
                source_game=auditor_view,
                source_port="Current Spec State",
                target_game=auditor,
                target_port="Current Spec State",
            ),
            Flow(
                source_game=auditor_view,
                source_port="Prior Findings",
                target_game=auditor,
                target_port="Prior Findings",
            ),
        ],
    )

    design_then_audit = SequentialComposition(
        name="Design Then Audit",
        first=designer_arm,
        second=auditor_arm,
        wiring=[
            Flow(
                source_game=designer,
                source_port="Revised Spec",
                target_game=auditor,
                target_port="Revised Spec",
            ),
        ],
    )

    full_round = SequentialComposition(
        name="SA Round",
        first=design_then_audit,
        second=spec_update,
        wiring=[
            Flow(
                source_game=designer,
                source_port="Revised Spec",
                target_game=spec_update,
                target_port="Revised Spec",
            ),
            Flow(
                source_game=auditor,
                source_port="Audit Findings",
                target_game=spec_update,
                target_port="Audit Findings",
            ),
        ],
    )

    return CorecursiveLoop(
        name="SA Design-Audit-Synthesize Loop",
        inner=full_round,
        corecursive_wiring=[
            Flow(
                source_game=spec_update,
                source_port="Spec Store",
                target_game=designer_view,
                target_port="Spec Store",
            ),
            Flow(
                source_game=spec_update,
                source_port="Spec Store",
                target_game=auditor_view,
                target_port="Spec Store",
            ),
        ],
        exit_condition="Spec is complete AND compatible — all halt gates pass, compatibility matrix has no contradictions",
    )


# ======================================================================
# Pattern — top-level specification
# ======================================================================


def build_pattern() -> Pattern:
    """Build the complete OGS Pattern for the SA loop."""
    return Pattern(
        name="SA Design-Audit-Synthesize Loop",
        game=build_game(),
        inputs=[
            PatternInput(
                name="Initial Requirements",
                input_type=InputType.EXTERNAL_WORLD,
                schema_hint="Domain description, stakeholder needs, constraints",
                target_game="Designer",
                flow_label="Audit Findings",
            ),
        ],
        composition_type=CompositionType.CORECURSIVE,
        terminal_conditions=[
            TerminalCondition(
                name="Complete and Compatible",
                actions={
                    "Designer": "Produce spec with all sections filled",
                    "Auditor": "Confirm no gaps, no contradictions",
                },
                outcome=(
                    "Spec is complete (all layers have content) and "
                    "compatible (cross-layer validation passes). "
                    "Halt gates are clear. Final artifact produced."
                ),
                description="Convergence: all halt gates pass",
                payoff_description="Sound specification ready for implementation",
            ),
            TerminalCondition(
                name="Sophistry",
                actions={
                    "Designer": "Expand spec without addressing findings",
                    "Auditor": "Produce shallow findings or override halt gates",
                },
                outcome=(
                    "Spec grows without converging. Findings accumulate "
                    "but are not addressed. The loop produces ever-expanding "
                    "documentation without reaching soundness."
                ),
                description=(
                    "Failure mode: the spec store grows monotonically "
                    "but the trajectory never reaches a state where all "
                    "halt gates pass simultaneously."
                ),
                payoff_description="Unbounded spec growth, no convergence",
            ),
        ],
        source="dsl",
    )


def build_ir() -> PatternIR:
    """Compile the Pattern to OGS PatternIR."""
    return compile_to_ir(build_pattern())
