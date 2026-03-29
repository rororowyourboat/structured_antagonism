"""Generative Adversarial Network — OGS game structure.

Encodes the GAN generator-discriminator system as a two-player game
with within-timestep feedback (.feedback operator). This is the
"symmetric antagonism" class in the structured antagonism taxonomy.

The key structural property: both players are peers in the composition.
Neither accumulates state across timesteps — the feedback is a scalar
gradient signal within a single training step. This distinguishes GANs
from pursuit-evasion systems (Socratic elenchus) which use .loop().

OGS Game Theory Decomposition:
    Players: Generator, Discriminator
    Generator: noise → sample (forward), gradient ← discriminator (backward)
    Discriminator: sample → classification (forward), loss ← ground truth (backward)
    Composition: (noise_source | real_data) >> generator >> discriminator
        .feedback([discriminator_signal -> generator])

    The minimax objective:
        min_G max_D V(D, G) = E[log D(x)] + E[log(1 - D(G(z)))]

    Nash equilibrium (if reached): generator perfectly models
    the data distribution — p_g = p_data.

    Failure mode: mode collapse — generator and discriminator
    share the same information channel, feedback loses orthogonality.

References:
    - Goodfellow et al., "Generative Adversarial Networks" (2014)
    - Research journal Entry 7: taxonomy of antagonistic systems
"""

from ogs.dsl.compile import compile_to_ir
from ogs.dsl.composition import (
    FeedbackFlow,
    FeedbackLoop,
    Flow,
    SequentialComposition,
)
from ogs.dsl.games import CovariantFunction, DecisionGame
from ogs.dsl.pattern import ActionSpace, Pattern, PatternInput, TerminalCondition
from ogs.dsl.types import CompositionType, InputType, Signature, port
from ogs.ir.models import PatternIR

# ======================================================================
# Atomic Games — OGS primitives
# ======================================================================

generator = DecisionGame(
    name="Generator",
    signature=Signature(
        x=(port("Noise Vector"),),
        y=(port("Generated Sample"),),
        r=(port("Discriminator Gradient"),),
        s=(port("Generator Loss"),),
    ),
    logic=(
        "Generator receives a noise vector z ~ p_z and produces a sample "
        "G(z). The backward channel carries the discriminator's gradient "
        "signal, which the generator uses to update its parameters toward "
        "producing samples that fool the discriminator."
    ),
    tags={"role": "generator", "class": "symmetric_antagonism"},
)

discriminator = DecisionGame(
    name="Discriminator",
    signature=Signature(
        x=(port("Generated Sample"), port("Real Sample")),
        y=(port("Classification"),),
        r=(port("Ground Truth Label"),),
        s=(port("Discriminator Gradient"),),
    ),
    logic=(
        "Discriminator receives both a generated sample G(z) and a real "
        "sample x ~ p_data. It outputs a classification D(x) in [0, 1] "
        "estimating the probability that the input is real. The backward "
        "channel carries the ground truth label, and the coutility "
        "(Discriminator Gradient) feeds back to the Generator."
    ),
    tags={"role": "discriminator", "class": "symmetric_antagonism"},
)

noise_source = CovariantFunction(
    name="Noise Source",
    signature=Signature(
        x=(),
        y=(port("Noise Vector"),),
    ),
    logic="Samples z ~ p_z (typically standard normal or uniform).",
    tags={"role": "environment"},
)

real_data = CovariantFunction(
    name="Real Data Source",
    signature=Signature(
        x=(),
        y=(port("Real Sample"),),
    ),
    logic="Samples x ~ p_data from the true data distribution.",
    tags={"role": "environment"},
)


# ======================================================================
# Composition — build the game tree
# ======================================================================


def build_game() -> FeedbackLoop:
    """Build the GAN as an OGS composite game.

    Structure: generator >> discriminator .feedback([gradient -> generator])

    The generator receives noise and produces samples. The discriminator
    receives both generated and real samples and classifies them. The
    discriminator's gradient signal feeds back to the generator within
    the same timestep — this is .feedback(), not .loop().
    """
    adversarial_pair = SequentialComposition(
        name="Adversarial Pair",
        first=generator,
        second=discriminator,
        wiring=[
            Flow(
                source_game=generator,
                source_port="Generated Sample",
                target_game=discriminator,
                target_port="Generated Sample",
            ),
        ],
    )

    return FeedbackLoop(
        name="GAN Training Loop",
        inner=adversarial_pair,
        feedback_wiring=[
            FeedbackFlow(
                source_game=discriminator,
                source_port="Discriminator Gradient",
                target_game=generator,
                target_port="Discriminator Gradient",
            ),
        ],
        signature=Signature(),
    )


# ======================================================================
# Pattern — top-level specification with metadata
# ======================================================================


def build_pattern() -> Pattern:
    """Build the complete OGS Pattern for the GAN."""
    return Pattern(
        name="Generative Adversarial Network",
        game=build_game(),
        inputs=[
            PatternInput(
                name="Noise Distribution",
                input_type=InputType.EXTERNAL_WORLD,
                schema_hint="z ~ N(0, I) or U(-1, 1)",
                target_game="Generator",
                flow_label="Noise Vector",
            ),
            PatternInput(
                name="Training Data",
                input_type=InputType.EXTERNAL_WORLD,
                schema_hint="x ~ p_data (true data distribution)",
                target_game="Discriminator",
                flow_label="Real Sample",
            ),
        ],
        composition_type=CompositionType.FEEDBACK,
        terminal_conditions=[
            TerminalCondition(
                name="Nash Equilibrium",
                actions={
                    "Generator": "p_g = p_data",
                    "Discriminator": "D(x) = 0.5 for all x",
                },
                outcome=(
                    "Generator perfectly models the data distribution. "
                    "Discriminator cannot distinguish real from generated."
                ),
                description=(
                    "Minimax fixed point: the generator's distribution "
                    "matches the true data distribution."
                ),
                payoff_description="V(D,G) = -log(4)",
            ),
            TerminalCondition(
                name="Mode Collapse",
                actions={
                    "Generator": "p_g covers subset of p_data modes",
                    "Discriminator": "D(x) > 0.5 for uncovered modes",
                },
                outcome=(
                    "Generator converges to producing a limited set of "
                    "outputs. Discriminator easily identifies uncovered "
                    "modes but gradient signal is insufficient to escape."
                ),
                description=(
                    "Degenerate equilibrium: feedback channel has lost "
                    "orthogonality. Generator and discriminator share "
                    "the same information about which modes are covered."
                ),
                payoff_description="V(D,G) > -log(4)",
            ),
        ],
        action_spaces=[
            ActionSpace(
                game="Generator",
                actions=["Generate sample from current p_g"],
            ),
            ActionSpace(
                game="Discriminator",
                actions=["Classify as real", "Classify as fake"],
            ),
        ],
        source="dsl",
    )


def build_ir() -> PatternIR:
    """Compile the Pattern to OGS PatternIR."""
    return compile_to_ir(build_pattern())
