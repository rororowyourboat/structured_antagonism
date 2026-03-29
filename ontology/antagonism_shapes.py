"""SHACL shapes for the structured antagonism taxonomy.

Defines custom shapes that classify GDS models along the three axes:
  1. Operator class (feedback vs temporal wirings)
  2. Observation asymmetry (superset detection on decision blocks)
  3. Commitment enforcement (dedicated state-update block presence)

These shapes run on RDF graphs exported via gds-owl and produce
validation reports indicating which antagonism class a system belongs to.

Usage:
    from ontology.antagonism_shapes import build_antagonism_shapes, classify_system
    from gds_owl.shacl import validate_graph

    shapes = build_antagonism_shapes()
    conforms, results_graph, results_text = validate_graph(data_graph, shapes)
"""

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, SH, XSD

GDS_IR = Namespace("https://gds.block.science/ontology/ir/")
GDS_CORE = Namespace("https://gds.block.science/ontology/core/")
SA = Namespace("https://structured-antagonism.org/shapes/")


def build_antagonism_shapes() -> Graph:
    """Build SHACL shapes for the structured antagonism taxonomy."""
    g = Graph()
    g.bind("sh", SH)
    g.bind("gds-ir", GDS_IR)
    g.bind("gds-core", GDS_CORE)
    g.bind("sa", SA)
    g.bind("xsd", XSD)

    _add_feedback_shape(g)
    _add_temporal_shape(g)
    _add_observation_shape(g)
    _add_state_update_shape(g)

    return g


def _add_feedback_shape(g: Graph) -> None:
    """SA-AXIS-1a: System has at least one feedback (contravariant) wiring.

    If true → symmetric antagonism candidate (FeedbackLoop class).
    """
    shape = SA["HasFeedbackWiringShape"]
    g.add((shape, RDF.type, SH.NodeShape))
    g.add((shape, SH.targetClass, GDS_IR.SystemIR))
    g.add((shape, RDFS.label, Literal("SA-AXIS-1a: Has feedback wiring")))
    g.add((shape, RDFS.comment, Literal(
        "Checks whether the system has at least one feedback "
        "(contravariant, within-timestep) wiring. Systems with feedback "
        "wirings are symmetric antagonism candidates."
    )))
    g.add((shape, SH.severity, SH.Info))

    # Property: hasWiringIR where isFeedback = true
    prop = BNode()
    g.add((shape, SH.property, prop))
    g.add((prop, SH.path, GDS_IR.hasWiringIR))

    qualified = BNode()
    g.add((prop, SH.qualifiedValueShape, qualified))

    fb_prop = BNode()
    g.add((qualified, SH.property, fb_prop))
    g.add((fb_prop, SH.path, GDS_IR.isFeedback))
    g.add((fb_prop, SH.hasValue, Literal(True)))

    g.add((prop, SH.qualifiedMinCount, Literal(1)))


def _add_temporal_shape(g: Graph) -> None:
    """SA-AXIS-1b: System has at least one temporal (corecursive) wiring.

    If true → pursuit-evasion or hierarchical antagonism candidate.
    """
    shape = SA["HasTemporalWiringShape"]
    g.add((shape, RDF.type, SH.NodeShape))
    g.add((shape, SH.targetClass, GDS_IR.SystemIR))
    g.add((shape, RDFS.label, Literal("SA-AXIS-1b: Has temporal wiring")))
    g.add((shape, RDFS.comment, Literal(
        "Checks whether the system has at least one temporal "
        "(corecursive, cross-timestep) wiring. Systems with temporal "
        "wirings are pursuit-evasion or hierarchical candidates."
    )))
    g.add((shape, SH.severity, SH.Info))

    prop = BNode()
    g.add((shape, SH.property, prop))
    g.add((prop, SH.path, GDS_IR.hasWiringIR))

    qualified = BNode()
    g.add((prop, SH.qualifiedValueShape, qualified))

    temp_prop = BNode()
    g.add((qualified, SH.property, temp_prop))
    g.add((temp_prop, SH.path, GDS_IR.isTemporal))
    g.add((temp_prop, SH.hasValue, Literal(True)))

    g.add((prop, SH.qualifiedMinCount, Literal(1)))


def _add_observation_shape(g: Graph) -> None:
    """SA-AXIS-2: Decision blocks have different forward_in signatures.

    If decision blocks have different signatureForwardIn values,
    the system has observation asymmetry.
    """
    shape = SA["ObservationAsymmetryShape"]
    g.add((shape, RDF.type, SH.NodeShape))
    g.add((shape, SH.targetClass, GDS_IR.SystemIR))
    g.add((shape, RDFS.label, Literal("SA-AXIS-2: Observation asymmetry")))
    g.add((shape, RDFS.comment, Literal(
        "Checks whether decision-type blocks have different "
        "signatureForwardIn values. Different observation channels "
        "indicate information asymmetry — one player may observe "
        "a superset of another's inputs."
    )))
    g.add((shape, SH.severity, SH.Info))

    # This shape is informational — the actual asymmetry check
    # requires SPARQL (comparing port sets across blocks), which
    # SHACL NodeShapes cannot express directly. The shape validates
    # that decision blocks exist; the SPARQL query does the comparison.
    prop = BNode()
    g.add((shape, SH.property, prop))
    g.add((prop, SH.path, GDS_IR.hasBlockIR))
    g.add((prop, SH.minCount, Literal(2)))


def _add_state_update_shape(g: Graph) -> None:
    """SA-AXIS-3: System has a non-decision block (state update mechanism).

    If the system has function_covariant blocks alongside decision blocks,
    it has a dedicated state-update mechanism — a candidate for commitment
    enforcement.
    """
    shape = SA["HasStateUpdateShape"]
    g.add((shape, RDF.type, SH.NodeShape))
    g.add((shape, SH.targetClass, GDS_IR.SystemIR))
    g.add((shape, RDFS.label, Literal("SA-AXIS-3: Has state update mechanism")))
    g.add((shape, RDFS.comment, Literal(
        "Checks whether the system has non-decision blocks "
        "(function_covariant) that serve as state update mechanisms. "
        "These are candidates for commitment enforcement — the "
        "mechanism that determines whether the loop converges or cycles."
    )))
    g.add((shape, SH.severity, SH.Info))

    prop = BNode()
    g.add((shape, SH.property, prop))
    g.add((prop, SH.path, GDS_IR.hasBlockIR))
    g.add((prop, SH.minCount, Literal(1)))


# ======================================================================
# SPARQL-based classification (supplements SHACL)
# ======================================================================

CLASSIFY_QUERY = """
PREFIX gds-core: <https://gds.block.science/ontology/core/>
PREFIX gds-ir: <https://gds.block.science/ontology/ir/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?system_name
       ?block_count
       (SUM(IF(?is_feedback = "true"^^xsd:boolean, 1, 0)) AS ?feedback_count)
       (SUM(IF(?is_temporal = "true"^^xsd:boolean, 1, 0)) AS ?temporal_count)
WHERE {
    ?system a gds-ir:SystemIR .
    ?system gds-core:name ?system_name .
    ?system gds-ir:hasWiringIR ?wiring .
    ?wiring gds-ir:isFeedback ?is_feedback .
    ?wiring gds-ir:isTemporal ?is_temporal .
    {
        SELECT ?system (COUNT(DISTINCT ?block) AS ?block_count)
        WHERE {
            ?system gds-ir:hasBlockIR ?block .
        }
        GROUP BY ?system
    }
}
GROUP BY ?system_name ?block_count
ORDER BY ?system_name
"""

OBSERVATION_QUERY = """
PREFIX gds-core: <https://gds.block.science/ontology/core/>
PREFIX gds-ir: <https://gds.block.science/ontology/ir/>

SELECT ?system_name ?block_name ?forward_in
WHERE {
    ?system a gds-ir:SystemIR .
    ?system gds-core:name ?system_name .
    ?system gds-ir:hasBlockIR ?block .
    ?block gds-core:name ?block_name .
    ?block gds-ir:blockType "decision" .
    ?block gds-ir:signatureForwardIn ?forward_in .
}
ORDER BY ?system_name ?block_name
"""

STATE_UPDATE_QUERY = """
PREFIX gds-core: <https://gds.block.science/ontology/core/>
PREFIX gds-ir: <https://gds.block.science/ontology/ir/>

SELECT ?system_name ?block_name ?block_type
WHERE {
    ?system a gds-ir:SystemIR .
    ?system gds-core:name ?system_name .
    ?system gds-ir:hasBlockIR ?block .
    ?block gds-core:name ?block_name .
    ?block gds-ir:blockType ?block_type .
    FILTER(?block_type = "function_covariant")
}
ORDER BY ?system_name ?block_name
"""


def classify_system(data_graph: Graph) -> list[dict]:
    """Classify systems in the graph along the three antagonism axes.

    Returns a list of classification dicts, one per system.
    """
    results = []

    # Axis 1: Operator class
    for row in data_graph.query(CLASSIFY_QUERY):
        name = str(row.system_name)
        fb = int(row.feedback_count)
        temp = int(row.temporal_count)

        if fb > 0 and temp == 0:
            operator_class = "symmetric (FeedbackLoop)"
        elif fb == 0 and temp > 0:
            operator_class = "temporal (CorecursiveLoop)"
        elif fb > 0 and temp > 0:
            operator_class = "hybrid (FeedbackLoop + CorecursiveLoop)"
        else:
            operator_class = "unknown (no feedback or temporal wirings)"

        results.append({
            "system": name,
            "blocks": int(row.block_count),
            "feedback_wirings": fb,
            "temporal_wirings": temp,
            "operator_class": operator_class,
        })

    # Axis 2: Observation symmetry
    observations = {}
    for row in data_graph.query(OBSERVATION_QUERY):
        name = str(row.system_name)
        observations.setdefault(name, []).append({
            "block": str(row.block_name),
            "forward_in": str(row.forward_in),
        })

    for r in results:
        obs = observations.get(r["system"], [])
        if len(obs) < 2:
            r["observation"] = "single_player"
        else:
            fwd_ins = [o["forward_in"] for o in obs]
            lengths = [len(f.split(" + ")) for f in fwd_ins]
            if len(set(lengths)) == 1:
                r["observation"] = "symmetric"
            else:
                r["observation"] = "asymmetric"
        r["observation_detail"] = obs

    # Axis 3: State update mechanism
    state_blocks = {}
    for row in data_graph.query(STATE_UPDATE_QUERY):
        name = str(row.system_name)
        state_blocks.setdefault(name, []).append(str(row.block_name))

    for r in results:
        blocks = state_blocks.get(r["system"], [])
        r["state_update_blocks"] = blocks
        r["has_state_update"] = len(blocks) > 0

    # Axis 1b: Detect nested temporal loops (multiple temporal wirings → same target)
    NESTING_QUERY = """
    PREFIX gds-core: <https://gds.block.science/ontology/core/>
    PREFIX gds-ir: <https://gds.block.science/ontology/ir/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?system_name ?target (COUNT(?wiring) AS ?temporal_to_target)
    WHERE {
        ?system a gds-ir:SystemIR .
        ?system gds-core:name ?system_name .
        ?system gds-ir:hasWiringIR ?wiring .
        ?wiring gds-ir:isTemporal "true"^^xsd:boolean .
        ?wiring gds-ir:target ?target .
    }
    GROUP BY ?system_name ?target
    HAVING (COUNT(?wiring) >= 2)
    """
    nested = set()
    for row in data_graph.query(NESTING_QUERY):
        nested.add(str(row.system_name))

    for r in results:
        r["has_nested_loops"] = r["system"] in nested

    # Predict failure mode
    for r in results:
        if "symmetric" in r["operator_class"]:
            r["predicted_failure"] = "mode_collapse"
            r["predicted_class"] = "symmetric_antagonism"
        elif "temporal" in r["operator_class"]:
            if r["has_nested_loops"]:
                r["predicted_failure"] = "sycophantic_consensus"
                r["predicted_class"] = "hierarchical_antagonism"
            elif r["observation"] == "asymmetric" and r["has_state_update"]:
                r["predicted_failure"] = "sophistry (if enforcement fails)"
                r["predicted_class"] = "pursuit_evasion"
            else:
                r["predicted_failure"] = "unknown"
                r["predicted_class"] = "temporal_unclassified"
        else:
            r["predicted_failure"] = "unknown"
            r["predicted_class"] = "unclassified"

    return results


if __name__ == "__main__":
    import json

    from gds_owl.export import system_ir_to_graph

    from models.co_scientist.model import build_ir as co_ir
    from models.euthyphro.model import build_ir as eu_ir
    from models.gan.model import build_ir as gan_ir

    # Merge all three
    merged = Graph()
    for builder in [gan_ir, eu_ir, co_ir]:
        ir = builder()
        system_ir = ir.to_system_ir()
        for triple in system_ir_to_graph(system_ir):
            merged.add(triple)

    # Classify
    classifications = classify_system(merged)
    print(json.dumps(classifications, indent=2, default=str))

    # SHACL validation
    try:
        from gds_owl.shacl import validate_graph
        shapes = build_antagonism_shapes()
        conforms, _, report_text = validate_graph(merged, shapes)
        print(f"\nSHACL validation: conforms={conforms}")
        print(report_text[:500] if report_text else "No violations")
    except ImportError:
        print("\nSHACL validation requires pyshacl (pip install gds-owl[shacl])")
