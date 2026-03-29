"""AI Co-Scientist — OGS game structure.

Encodes the hierarchical multi-agent system from Google's "Towards an
AI Co-Scientist" (Gottweis et al., 2025) as a compositional game with
nested temporal loops. This is the "hierarchical antagonism" class in
the structured antagonism taxonomy.

The key structural property: two levels of temporal iteration.
The inner pipeline (Generation >> Reflection >> Ranking >> Evolution)
processes hypotheses within a research round. The outer loop (Meta-Review)
accumulates insights across rounds, reasoning about the *distribution*
of inner-loop outcomes rather than individual hypotheses.

This is .loop().loop() — nested corecursive composition — which
distinguishes it from both symmetric antagonism (.feedback(), GAN)
and pursuit-evasion antagonism (.loop(), Socratic elenchus).

OGS Game Theory Decomposition:
    Inner pipeline: Gen >> Reflect >> Rank >> Evolve
    Outer loop: Meta-Review closes over inner pipeline across rounds

    Composition:
        inner = Gen >> Reflect >> Rank >> Evolve
        round = inner.corecursive([hypothesis_population -> Gen])
        system = round.corecursive([meta_insights -> Gen])

    Convergence criterion: Elo-stable hypothesis ranking — top hypotheses
    maintain their ranking across consecutive rounds.

    Failure mode: sycophantic consensus — inner loop agents converge on
    locally popular answers because outer meta-review signal is too weak
    relative to inner-loop reward.

References:
    - Gottweis et al., "Towards an AI Co-Scientist" (2025)
    - Research journal Entry 7-8: taxonomy of antagonistic systems
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
# Atomic Games — inner pipeline agents
# ======================================================================

generation = DecisionGame(
    name="Generation Agent",
    signature=Signature(
        x=(port("Research Goal"), port("Meta Insights")),
        y=(port("Candidate Hypotheses"),),
        r=(port("Ranking Feedback"),),
        s=(port("Generation Quality Signal"),),
    ),
    logic=(
        "Generates novel hypotheses based on the research goal and "
        "accumulated meta-insights from prior rounds. Uses diverse "
        "generation strategies (literature-grounded, analogical, "
        "contrarian) to maintain population diversity."
    ),
    tags={"role": "generator", "class": "hierarchical_antagonism"},
)

reflection = CovariantFunction(
    name="Reflection Agent",
    signature=Signature(
        x=(port("Candidate Hypotheses"),),
        y=(port("Critiqued Hypotheses"),),
    ),
    logic=(
        "Reviews each hypothesis for internal consistency, novelty, "
        "and testability. Produces structured critiques identifying "
        "weaknesses, missing evidence, and logical gaps. Does not "
        "rank — only annotates."
    ),
    tags={"role": "critic", "class": "hierarchical_antagonism"},
)

ranking = DecisionGame(
    name="Ranking Agent",
    signature=Signature(
        x=(port("Critiqued Hypotheses"),),
        y=(port("Ranked Hypotheses"),),
        r=(port("Evolution Outcome"),),
        s=(port("Ranking Feedback"),),
    ),
    logic=(
        "Conducts pairwise tournament comparisons between hypotheses "
        "using Elo rating. Simulates debates between hypothesis pairs "
        "to determine the stronger candidate based on novelty, "
        "correctness, and evidential support. Produces an Elo-ranked "
        "ordering."
    ),
    tags={"role": "evaluator", "class": "hierarchical_antagonism"},
)

evolution = CovariantFunction(
    name="Evolution Agent",
    signature=Signature(
        x=(port("Ranked Hypotheses"),),
        y=(port("Evolved Population"), port("Evolution Outcome")),
    ),
    logic=(
        "Selects top-ranked hypotheses for survival. Applies variation "
        "operators: mutation (small modifications), crossover (combining "
        "ideas from two hypotheses), and immigration (injecting new "
        "hypotheses from scratch). Outputs the next-generation population."
    ),
    tags={"role": "mechanism", "class": "hierarchical_antagonism"},
)

meta_review = DecisionGame(
    name="Meta-Review Agent",
    signature=Signature(
        x=(port("Evolved Population"), port("Round History")),
        y=(port("Meta Insights"),),
        r=(port("Research Outcome"),),
        s=(port("Meta Quality Signal"),),
    ),
    logic=(
        "Operates on the *distribution* of outcomes across rounds, "
        "not individual hypotheses. Identifies systematic patterns: "
        "which hypothesis families consistently score well, which "
        "research directions are exhausted, what blind spots the "
        "inner pipeline exhibits. Produces strategic guidance that "
        "biases the next round's generation."
    ),
    tags={"role": "meta_evaluator", "class": "hierarchical_antagonism"},
)


# ======================================================================
# Composition — build the game tree
# ======================================================================


def build_game() -> CorecursiveLoop:
    """Build the AI Co-Scientist as nested corecursive loops.

    Structure:
        inner = Generation >> Reflection >> Ranking >> Evolution
        round = inner.corecursive(evolved_population -> generation)
        system = (round >> meta_review).corecursive(meta_insights -> generation)

    The inner loop iterates hypotheses within a round.
    The outer loop accumulates meta-insights across rounds.
    Both are .loop() (covariant, cross-timestep) — this is .loop().loop().
    """
    # Inner pipeline: Generation >> Reflection >> Ranking >> Evolution
    gen_to_reflect = SequentialComposition(
        name="Generate and Critique",
        first=generation,
        second=reflection,
        wiring=[
            Flow(
                source_game=generation,
                source_port="Candidate Hypotheses",
                target_game=reflection,
                target_port="Candidate Hypotheses",
            ),
        ],
    )

    reflect_to_rank = SequentialComposition(
        name="Critique and Rank",
        first=gen_to_reflect,
        second=ranking,
        wiring=[
            Flow(
                source_game=reflection,
                source_port="Critiqued Hypotheses",
                target_game=ranking,
                target_port="Critiqued Hypotheses",
            ),
        ],
    )

    inner_pipeline = SequentialComposition(
        name="Inner Pipeline",
        first=reflect_to_rank,
        second=evolution,
        wiring=[
            Flow(
                source_game=ranking,
                source_port="Ranked Hypotheses",
                target_game=evolution,
                target_port="Ranked Hypotheses",
            ),
        ],
    )

    # Inner temporal loop: evolved population feeds back to generation
    inner_loop = CorecursiveLoop(
        name="Hypothesis Evolution Loop",
        inner=inner_pipeline,
        corecursive_wiring=[
            Flow(
                source_game=evolution,
                source_port="Evolved Population",
                target_game=generation,
                target_port="Meta Insights",
            ),
        ],
        exit_condition="Elo rankings stabilize within round",
    )

    # Outer composition: inner loop >> meta-review
    round_with_meta = SequentialComposition(
        name="Research Round",
        first=inner_loop,
        second=meta_review,
        wiring=[
            Flow(
                source_game=evolution,
                source_port="Evolved Population",
                target_game=meta_review,
                target_port="Evolved Population",
            ),
        ],
    )

    # Outer temporal loop: meta-insights feed back to next round's generation
    return CorecursiveLoop(
        name="AI Co-Scientist",
        inner=round_with_meta,
        corecursive_wiring=[
            Flow(
                source_game=meta_review,
                source_port="Meta Insights",
                target_game=generation,
                target_port="Meta Insights",
            ),
        ],
        exit_condition="Top hypotheses maintain Elo ranking across consecutive rounds",
    )


# ======================================================================
# Pattern — top-level specification with metadata
# ======================================================================


def build_pattern() -> Pattern:
    """Build the complete OGS Pattern for the AI Co-Scientist."""
    return Pattern(
        name="AI Co-Scientist",
        game=build_game(),
        inputs=[
            PatternInput(
                name="Research Goal",
                input_type=InputType.EXTERNAL_WORLD,
                schema_hint="Natural language research question or hypothesis space",
                target_game="Generation Agent",
                flow_label="Research Goal",
            ),
            PatternInput(
                name="Literature Corpus",
                input_type=InputType.EXTERNAL_WORLD,
                schema_hint="Access to scientific literature for grounding",
                target_game="Generation Agent",
                flow_label="Research Goal",
            ),
        ],
        composition_type=CompositionType.CORECURSIVE,
        terminal_conditions=[
            TerminalCondition(
                name="Elo Stability",
                actions={
                    "Generation Agent": "Produce hypotheses",
                    "Ranking Agent": "Rank via tournament",
                    "Meta-Review Agent": "Confirm stability",
                },
                outcome=(
                    "Top-ranked hypotheses maintain their Elo rating "
                    "across consecutive rounds. The system has converged "
                    "on a stable set of high-quality hypotheses."
                ),
                description="Convergence: hypothesis rankings stabilize",
                payoff_description="Stable Elo ranking across rounds",
            ),
            TerminalCondition(
                name="Sycophantic Consensus",
                actions={
                    "Generation Agent": "Produce similar hypotheses",
                    "Ranking Agent": "Rank consistently",
                    "Meta-Review Agent": "Fail to detect convergence",
                },
                outcome=(
                    "Inner loop agents converge on locally popular answers. "
                    "Meta-review signal is too weak to redirect generation. "
                    "Population diversity collapses."
                ),
                description=(
                    "Failure mode: hierarchical antagonism degenerates "
                    "when outer loop signal is dominated by inner loop"
                ),
                payoff_description="Low diversity, high inner-loop agreement",
            ),
        ],
        source="dsl",
    )


def build_ir() -> PatternIR:
    """Compile the Pattern to OGS PatternIR."""
    return compile_to_ir(build_pattern())
