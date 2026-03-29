"""Diff Pass 1 (context-minimal) vs Pass 2 (schema-informed) extractions.

Produces a triage report identifying divergences between the two passes:
  - Propositions in Pass 2 not in Pass 1 (schema doing work, or contamination)
  - Propositions in Pass 1 not in Pass 2 (schema filtering, or missed)
  - Type upgrades (Pass 1 "asserted" → Pass 2 "commitment" or "conditional_commitment")
  - Presuppositions surfaced by only one pass

Output: models/euthyphro/llm_extractions/divergence_report.md
"""

import json
from pathlib import Path

HERE = Path(__file__).parent


def load_pass1() -> list[dict]:
    with open(HERE / "llm_extractions" / "pass1_gemini.json") as f:
        return json.load(f)


def load_pass2() -> list[dict]:
    with open(HERE / "llm_extractions" / "pass2_gemini.json") as f:
        return json.load(f)


def extract_p1_propositions(section: dict) -> dict:
    """Extract all propositions from a Pass 1 section, keyed by type."""
    result = {"asserted": [], "conceded": [], "presupposed": []}
    for ex in section.get("key_exchanges", []):
        for p in ex.get("propositions_asserted", []):
            result["asserted"].append({"speaker": ex["speaker"], "text": p})
        for p in ex.get("propositions_conceded", []):
            result["conceded"].append({"speaker": ex["speaker"], "text": p})
        for p in ex.get("propositions_presupposed", []):
            result["presupposed"].append({"speaker": ex["speaker"], "text": p})
    return result


def extract_p2_propositions(section: dict) -> dict:
    """Extract all propositions from a Pass 2 section, keyed by type."""
    result = {"commitment": [], "assertion": [], "presupposition": [],
              "conditional_commitment": []}
    for turn in section.get("substantive_turns", []):
        delta = turn.get("commitment_delta", {})
        for item in delta.get("added", []):
            if isinstance(item, dict):
                t = item.get("type", "assertion")
                result.setdefault(t, []).append({
                    "holder": item.get("holder", "?"),
                    "text": item.get("proposition", ""),
                    "confidence": item.get("confidence", "?"),
                    "source": item.get("source", "?"),
                    "available_to": item.get("available_to", "both"),
                })
    return result


def normalize_for_comparison(text: str) -> str:
    """Rough normalization for fuzzy matching between passes."""
    return text.lower().strip().rstrip(".")


def find_fuzzy_match(needle: str, haystack: list[str], threshold: float = 0.4) -> str | None:
    """Find a fuzzy match using word overlap."""
    needle_words = set(normalize_for_comparison(needle).split())
    best_score = 0.0
    best_match = None
    for h in haystack:
        h_words = set(normalize_for_comparison(h).split())
        if not needle_words or not h_words:
            continue
        overlap = len(needle_words & h_words)
        score = overlap / max(len(needle_words), len(h_words))
        if score > best_score:
            best_score = score
            best_match = h
    return best_match if best_score >= threshold else None


def diff_section(section_id: int, p1_props: dict, p2_props: dict) -> dict:
    """Diff propositions between the two passes for one section."""
    # Collect all P1 texts and all P2 texts
    p1_texts = []
    for category in p1_props.values():
        for item in category:
            p1_texts.append(item["text"])

    p2_texts = []
    for category in p2_props.values():
        for item in category:
            p2_texts.append(item["text"])

    # Find P2-only (in schema pass but not raw pass)
    p2_only = []
    for cat_name, items in p2_props.items():
        for item in items:
            match = find_fuzzy_match(item["text"], p1_texts)
            if not match:
                p2_only.append({**item, "schema_type": cat_name})

    # Find P1-only (in raw pass but not schema pass)
    p1_only = []
    for cat_name, items in p1_props.items():
        for item in items:
            match = find_fuzzy_match(item["text"], p2_texts)
            if not match:
                p1_only.append({**item, "raw_type": cat_name})

    # Find type upgrades (in both, but type changed)
    upgrades = []
    for p1_cat, p1_items in p1_props.items():
        for p1_item in p1_items:
            for p2_cat, p2_items in p2_props.items():
                for p2_item in p2_items:
                    if find_fuzzy_match(p1_item["text"], [p2_item["text"]]):
                        if p1_cat != p2_cat:
                            upgrades.append({
                                "p1_type": p1_cat,
                                "p2_type": p2_cat,
                                "p1_text": p1_item["text"],
                                "p2_text": p2_item["text"],
                                "p2_confidence": p2_item.get("confidence", "?"),
                            })

    return {
        "section_id": section_id,
        "p1_count": len(p1_texts),
        "p2_count": len(p2_texts),
        "p2_only": p2_only,
        "p1_only": p1_only,
        "type_upgrades": upgrades,
    }


def generate_report(diffs: list[dict]) -> str:
    lines = []
    lines.append("# Divergence Report: Pass 1 vs Pass 2")
    lines.append("")
    lines.append("Context-minimal (Pass 1) vs schema-informed (Pass 2) extraction.")
    lines.append("Divergences triaged as: **contamination** (P2 adds scholarly interpretation"),
    lines.append("not in text), **schema doing work** (P2 surfaces distinctions P1 misses),")
    lines.append("or **genuine ambiguity** (flag for manual review).")
    lines.append("")

    # Summary stats
    total_p2_only = sum(len(d["p2_only"]) for d in diffs)
    total_p1_only = sum(len(d["p1_only"]) for d in diffs)
    total_upgrades = sum(len(d["type_upgrades"]) for d in diffs)
    lines.append(f"**Summary:** {total_p2_only} P2-only, {total_p1_only} P1-only, {total_upgrades} type upgrades")
    lines.append("")

    # Per-section details
    for d in diffs:
        sid = d["section_id"]
        if not d["p2_only"] and not d["p1_only"] and not d["type_upgrades"]:
            continue

        lines.append(f"---")
        lines.append(f"## Section {sid} (P1: {d['p1_count']} props, P2: {d['p2_count']} props)")
        lines.append("")

        if d["p2_only"]:
            lines.append(f"### P2-only ({len(d['p2_only'])} — schema surfaced or contamination)")
            for item in d["p2_only"]:
                conf = item.get("confidence", "?")
                src = item.get("source", "?")
                avail = item.get("available_to", "both")
                lines.append(f"- [{item.get('schema_type', '?')}] ({conf}/{src}) {item.get('holder', '?')}: {item['text']}")
                if avail != "both":
                    lines.append(f"  - available_to: {avail}")
            lines.append("")

        if d["p1_only"]:
            lines.append(f"### P1-only ({len(d['p1_only'])} — raw pass captured, schema filtered)")
            for item in d["p1_only"]:
                lines.append(f"- [{item.get('raw_type', '?')}] {item.get('speaker', '?')}: {item['text']}")
            lines.append("")

        if d["type_upgrades"]:
            lines.append(f"### Type upgrades ({len(d['type_upgrades'])})")
            for u in d["type_upgrades"]:
                lines.append(f"- {u['p1_type']} → **{u['p2_type']}** ({u['p2_confidence']})")
                lines.append(f"  - P1: {u['p1_text']}")
                lines.append(f"  - P2: {u['p2_text']}")
            lines.append("")

    # Triage guidance
    lines.append("---")
    lines.append("## Triage Guidance")
    lines.append("")
    lines.append("For each P2-only item, ask:")
    lines.append("1. **Is this in the text?** If yes → schema doing work (keep)")
    lines.append("2. **Is this a scholarly interpretation?** If yes → contamination (flag)")
    lines.append("3. **Is this genuinely ambiguous?** If yes → manual review")
    lines.append("")
    lines.append("For each P1-only item, ask:")
    lines.append("1. **Did the schema correctly filter this?** (e.g., phatic/irrelevant)")
    lines.append("2. **Did the schema incorrectly drop this?** (e.g., relevant assertion lost)")
    lines.append("")
    lines.append("For type upgrades, the key question:")
    lines.append("- P1 'asserted' → P2 'commitment': Was this actually conceded under questioning,")
    lines.append("  or just stated? The upgrade is correct if Socrates can invoke it later.")

    return "\n".join(lines)


def main():
    p1 = load_pass1()
    p2 = load_pass2()

    # Match sections by ID
    p1_by_id = {s["section_id"]: s for s in p1}
    p2_by_id = {s["section_id"]: s for s in p2}

    all_ids = sorted(set(p1_by_id.keys()) | set(p2_by_id.keys()))

    diffs = []
    for sid in all_ids:
        p1_section = p1_by_id.get(sid, {})
        p2_section = p2_by_id.get(sid, {})
        p1_props = extract_p1_propositions(p1_section)
        p2_props = extract_p2_propositions(p2_section)
        d = diff_section(sid, p1_props, p2_props)
        diffs.append(d)

    report = generate_report(diffs)

    out_path = HERE / "llm_extractions" / "divergence_report.md"
    out_path.write_text(report)
    print(report)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
