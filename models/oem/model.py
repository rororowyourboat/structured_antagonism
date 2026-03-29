"""Orthogonal Evaluator Model (OEM) — parameterized GDS specification.

Encodes the conditions for productive antagonism as a GDS spec with
two key parameters:

    ρ(E,T) — evaluator's correlation with ground truth
    |I|    — shared information channel between generator and evaluator

The productive antagonism condition:
    ρ(E,T) > ρ(G,T) AND |I| < threshold

This is a GDS *specification* (GDSSpec), not just an OGS game tree.
It uses the full GDS vocabulary: TypeDef, Entity, StateVariable,
ParameterDef, BoundaryAction, Policy, Mechanism — plus a custom
verification check that flags sycophancy risk from observation symmetry.

References:
    - Research journal Entry 11: OEM formulation
    - Research journal Entry 7-8: three-axis taxonomy
"""

from gds import (
    BoundaryAction,
    GDSSpec,
    Mechanism,
    Policy,
    compile_system,
    interface,
    port,
    verify,
)
from gds.blocks.composition import TemporalLoop, Wiring
from gds.ir.models import FlowDirection
from gds.parameters import ParameterDef
from gds.state import Entity, StateVariable
from gds.types.typedef import TypeDef
from gds.verification.findings import Finding, Severity


# ======================================================================
# Type definitions
# ======================================================================

Probability = TypeDef(
    name="Probability",
    python_type=float,
    constraint=lambda x: 0.0 <= x <= 1.0,
    description="Probability or correlation value in [0, 1]",
)

ChannelSize = TypeDef(
    name="ChannelSize",
    python_type=float,
    constraint=lambda x: x >= 0.0,
    description="Size of shared information channel (non-negative)",
)

Quality = TypeDef(
    name="Quality",
    python_type=float,
    description="Quality score of generated output",
)

Inconsistency = TypeDef(
    name="Inconsistency",
    python_type=float,
    constraint=lambda x: x >= 0.0,
    description="Measure of exploitable inconsistency in the store (non-negative, 0 = fully consistent)",
)


# ======================================================================
# State entities
# ======================================================================

generator_state = Entity(
    name="Generator",
    variables={
        "hypothesis": StateVariable(
            name="hypothesis",
            typedef=Quality,
            symbol="h",
            description="Current hypothesis/proposal quality",
        ),
        "truth_correlation": StateVariable(
            name="truth_correlation",
            typedef=Probability,
            symbol="ρ_G",
            description="Generator's correlation with ground truth — ρ(G,T)",
        ),
    },
)

evaluator_state = Entity(
    name="Evaluator",
    variables={
        "scoring_accuracy": StateVariable(
            name="scoring_accuracy",
            typedef=Probability,
            symbol="ρ_E",
            description="Evaluator's correlation with ground truth — ρ(E,T)",
        ),
    },
)

store_state = Entity(
    name="Store",
    variables={
        "inconsistency": StateVariable(
            name="inconsistency",
            typedef=Inconsistency,
            symbol="ε",
            description="Current exploitable inconsistency in the commitment store",
        ),
        "size": StateVariable(
            name="size",
            typedef=ChannelSize,
            symbol="n",
            description="Number of entries in the store",
        ),
    },
)


# ======================================================================
# Parameters — the OEM's tuneable variables
# ======================================================================

rho_et = ParameterDef(
    name="rho_evaluator_truth",
    typedef=Probability,
    description=(
        "ρ(E,T) — evaluator's correlation with ground truth. "
        "High values (→1) mean the evaluator tracks truth; "
        "low values (→0) mean the evaluator's signal is noise."
    ),
)

rho_gt = ParameterDef(
    name="rho_generator_truth",
    typedef=Probability,
    description=(
        "ρ(G,T) — generator's correlation with ground truth. "
        "Productive antagonism requires ρ(E,T) > ρ(G,T)."
    ),
)

channel_overlap = ParameterDef(
    name="channel_overlap",
    typedef=ChannelSize,
    description=(
        "|I| — size of shared information channel between generator "
        "and evaluator. Small |I| means independent signals (productive). "
        "Large |I| means evaluator mirrors generator (sycophancy risk)."
    ),
)

channel_threshold = ParameterDef(
    name="channel_threshold",
    typedef=ChannelSize,
    description=(
        "Maximum |I| for productive antagonism. When channel_overlap > "
        "channel_threshold, the system is at risk of sycophancy."
    ),
)


# ======================================================================
# Blocks — the OEM's composition
# ======================================================================

# Exogenous inputs
truth_signal = BoundaryAction(
    name="Truth Signal",
    interface=interface(forward_out=["Ground Truth"]),
)

noise = BoundaryAction(
    name="Noise",
    interface=interface(forward_out=["Random Seed"]),
)

# Generator: produces hypotheses
generator_policy = Policy(
    name="Generator Policy",
    interface=interface(
        forward_in=["Store State", "Random Seed"],
        forward_out=["Hypothesis"],
    ),
)

# Evaluator: scores hypotheses — has ADDITIONAL observation channel
evaluator_policy = Policy(
    name="Evaluator Policy",
    interface=interface(
        forward_in=["Hypothesis", "Store State", "Store History", "Ground Truth"],
        forward_out=["Evaluation Signal"],
    ),
)

# Store update: world-state mechanism
store_mechanism = Mechanism(
    name="Store Update",
    interface=interface(
        forward_in=["Hypothesis", "Evaluation Signal"],
        forward_out=["Store State", "Store History"],
    ),
    updates=[
        ("Store", "inconsistency"),
        ("Store", "size"),
    ],
)


# ======================================================================
# Composition
# ======================================================================


def build_system():
    """Build the OEM as a GDS composition.

    Structure:
        (truth | noise) >> generator >> evaluator >> store_update
        .loop([store_state -> generator, store_state + history -> evaluator])

    The evaluator observes a STRICT SUPERSET of the generator:
        Generator sees: Store State + Random Seed
        Evaluator sees: Hypothesis + Store State + Store History + Ground Truth

    This asymmetry is the structural encoding of small |I|.
    """
    # Input phase
    from gds.blocks.composition import StackComposition, ParallelComposition

    inputs = ParallelComposition(
        name="Inputs",
        left=truth_signal,
        right=noise,
    )

    # Generator receives store state + noise
    gen_phase = StackComposition(
        name="Generation Phase",
        first=inputs,
        second=generator_policy,
        wiring=[
            Wiring(
                source_block="Noise",
                source_port="Random Seed",
                target_block="Generator Policy",
                target_port="Random Seed",
                direction=FlowDirection.COVARIANT,
            ),
        ],
    )

    # Evaluator receives hypothesis + store state + history + truth
    eval_phase = StackComposition(
        name="Evaluation Phase",
        first=gen_phase,
        second=evaluator_policy,
        wiring=[
            Wiring(
                source_block="Generator Policy",
                source_port="Hypothesis",
                target_block="Evaluator Policy",
                target_port="Hypothesis",
                direction=FlowDirection.COVARIANT,
            ),
            Wiring(
                source_block="Truth Signal",
                source_port="Ground Truth",
                target_block="Evaluator Policy",
                target_port="Ground Truth",
                direction=FlowDirection.COVARIANT,
            ),
        ],
    )

    # Store update receives hypothesis + evaluation
    pipeline = StackComposition(
        name="OEM Pipeline",
        first=eval_phase,
        second=store_mechanism,
        wiring=[
            Wiring(
                source_block="Generator Policy",
                source_port="Hypothesis",
                target_block="Store Update",
                target_port="Hypothesis",
                direction=FlowDirection.COVARIANT,
            ),
            Wiring(
                source_block="Evaluator Policy",
                source_port="Evaluation Signal",
                target_block="Store Update",
                target_port="Evaluation Signal",
                direction=FlowDirection.COVARIANT,
            ),
        ],
    )

    # Temporal loop: store state feeds back to both generator and evaluator
    return TemporalLoop(
        name="OEM Loop",
        inner=pipeline,
        temporal_wiring=[
            Wiring(
                source_block="Store Update",
                source_port="Store State",
                target_block="Generator Policy",
                target_port="Store State",
                direction=FlowDirection.COVARIANT,
            ),
            Wiring(
                source_block="Store Update",
                source_port="Store State",
                target_block="Evaluator Policy",
                target_port="Store State",
                direction=FlowDirection.COVARIANT,
            ),
            Wiring(
                source_block="Store Update",
                source_port="Store History",
                target_block="Evaluator Policy",
                target_port="Store History",
                direction=FlowDirection.COVARIANT,
            ),
        ],
        exit_condition="Store inconsistency reaches zero (convergence) or store size exceeds bound without convergence (sophistry)",
    )


def build_spec() -> GDSSpec:
    """Build the full GDS specification with parameters."""
    spec = GDSSpec(
        name="Orthogonal Evaluator Model",
        description=(
            "Parameterized model of productive antagonism. "
            "Two key parameters: ρ(E,T) — evaluator's truth correlation, "
            "and |I| — shared information channel size. Productive "
            "antagonism requires ρ(E,T) > ρ(G,T) and bounded |I|."
        ),
    )

    # Register types
    for td in [Probability, ChannelSize, Quality, Inconsistency]:
        spec.register_type(td)

    # Register entities
    for entity in [generator_state, evaluator_state, store_state]:
        spec.register_entity(entity)

    # Register parameters
    for param in [rho_et, rho_gt, channel_overlap, channel_threshold]:
        spec.register_parameter(param.name, param.typedef)

    # Register blocks
    for block in [truth_signal, noise, generator_policy, evaluator_policy, store_mechanism]:
        spec.register_block(block)

    return spec


# ======================================================================
# Custom verification check
# ======================================================================


def check_observation_asymmetry(system_ir) -> list[Finding]:
    """SA-OEM-001: Evaluator's observation ports must be a strict superset
    of generator's observation ports.

    If they are equal, the system has symmetric observation and is at
    risk of sycophancy (|I| ≈ max).
    """
    findings = []

    # Find blocks by name pattern
    gen_fwd_in = set()
    eval_fwd_in = set()

    for block in system_ir.blocks:
        name_lower = block.name.lower()
        if "generator" in name_lower:
            sig = block.signature
            if isinstance(sig, tuple) and len(sig) >= 1:
                gen_fwd_in = set(sig[0].split(" + ")) if sig[0] else set()
        elif "evaluator" in name_lower:
            sig = block.signature
            if isinstance(sig, tuple) and len(sig) >= 1:
                eval_fwd_in = set(sig[0].split(" + ")) if sig[0] else set()

    if gen_fwd_in and eval_fwd_in:
        extra = eval_fwd_in - gen_fwd_in
        if extra:
            findings.append(Finding(
                check_id="SA-OEM-001",
                severity=Severity.INFO,
                message=(
                    f"Evaluator observes {len(extra)} additional channel(s) "
                    f"not visible to generator: {extra}. "
                    f"Small |I| — productive antagonism precondition met."
                ),
                source_elements=list(extra),
                passed=True,
            ))
        else:
            findings.append(Finding(
                check_id="SA-OEM-001",
                severity=Severity.WARNING,
                message=(
                    "Evaluator and generator observe identical channels. "
                    "Large |I| — sycophancy risk. The evaluator has no "
                    "independent signal."
                ),
                source_elements=[],
                passed=False,
            ))

    return findings


# ======================================================================
# Main
# ======================================================================


if __name__ == "__main__":
    from gds.canonical import project_canonical

    # Build and compile
    system = build_system()
    system_ir = compile_system("Orthogonal Evaluator Model", system)

    # Verify
    report = verify(system_ir)
    print(f"GDS verification: {report.checks_passed}/{report.checks_total} passed")
    for f in report.findings:
        if not f.passed:
            print(f"  FAIL {f.check_id}: {f.message}")

    # Custom check
    oem_findings = check_observation_asymmetry(system_ir)
    for f in oem_findings:
        status = "PASS" if f.passed else "FAIL"
        print(f"  {status} {f.check_id}: {f.message}")

    # Spec
    spec = build_spec()
    print(f"\nSpec: {spec.name}")
    print(f"Types: {len(spec.types)}")
    print(f"Entities: {len(spec.entities)}")
    print(f"Parameters: {len(spec.parameters)}")
    print(f"Blocks: {len(spec.blocks)}")

    # Canonical form
    canonical = project_canonical(spec)
    print(f"\nCanonical: {canonical.formula()}")

    # System structure
    print(f"\nBlocks ({len(system_ir.blocks)}):")
    for b in system_ir.blocks:
        print(f"  {b.name} ({b.block_type})")
    print(f"Wirings ({len(system_ir.wirings)}):")
    for w in system_ir.wirings:
        fb = " [FEEDBACK]" if w.is_feedback else ""
        temp = " [TEMPORAL]" if w.is_temporal else ""
        print(f"  {w.source} -> {w.target} [{w.label}] {w.direction}{fb}{temp}")
