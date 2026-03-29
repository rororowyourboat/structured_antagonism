"""Phase B: LLM-assisted structural extraction for Euthyphro annotation.

Two passes per the methodology:
  Pass 1 (context-minimal): Raw text only, no schema. Segment turns,
    classify speech acts, list candidate propositions.
  Pass 2 (schema-informed): Full v2.0 schema provided. Populate all
    fields including commitment types, cycle signals, confidence.

Uses Gemini 3 Flash Preview with thinking enabled, JSON output.
API key resolved from 1Password via .env.

Usage:
    # Resolve API key and run both passes
    export GEMINI_API_KEY=$(op read "op://Private/Gemini API key/credential")
    uv run python models/euthyphro/extract.py
"""

import json
import subprocess
import sys
from pathlib import Path

from google import genai
from google.genai import types

HERE = Path(__file__).parent
ROOT = HERE.parent.parent


def get_api_key() -> str:
    """Resolve GEMINI_API_KEY from 1Password."""
    import os

    key = os.environ.get("GEMINI_API_KEY")
    if key and not key.startswith("op://"):
        return key
    # Resolve from 1Password
    ref = key or "op://Private/Gemini API key/credential"
    result = subprocess.run(
        ["op", "read", ref], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def load_raw_turns() -> list[dict]:
    """Load the 232 mechanically-extracted turns."""
    with open(HERE / "raw_turns.json") as f:
        data = json.load(f)
    return data["turns"]


def load_dialogue_text() -> str:
    """Load the full Jowett dialogue text (lines 282-1151)."""
    with open(ROOT / "references" / "euthyphro.txt") as f:
        lines = f.readlines()
    return "".join(lines[281:1151])


def load_schema() -> str:
    """Load the annotation methodology for the schema-informed pass."""
    with open(HERE / "annotation-methodology.md") as f:
        return f.read()


def load_section_index() -> str:
    """Load the Pass 1 section-level outline."""
    with open(HERE / "pass1_context_minimal.json") as f:
        return f.read()


def call_gemini(api_key: str, prompt: str, output_path: Path) -> None:
    """Call Gemini with thinking enabled, stream JSON response to file."""
    client = genai.Client(api_key=api_key)

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        ),
    ]
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
        response_mime_type="application/json",
    )

    print(f"  Calling Gemini (gemini-3-flash-preview, thinking=HIGH)...")
    chunks = []
    for chunk in client.models.generate_content_stream(
        model="gemini-3-flash-preview",
        contents=contents,
        config=config,
    ):
        if chunk.text:
            chunks.append(chunk.text)
            print(".", end="", flush=True)
    print()

    result = "".join(chunks)
    output_path.write_text(result)
    print(f"  Saved to {output_path} ({len(result)} chars)")


# ======================================================================
# Pass 1: Context-minimal
# ======================================================================

PASS1_PROMPT_TEMPLATE = """You are a careful reader of Platonic dialogues. Below is the full text of Plato's Euthyphro in Benjamin Jowett's translation.

Your task: For each of the following dialogue sections, identify the key propositions that each speaker ASSERTS or CONCEDES. Do NOT use any technical vocabulary about "commitment stores" or "game theory." Just read the text carefully and note what each person says and agrees to.

For each section, provide:
- section_id: the section number from the index
- key_exchanges: array of the most important speaker turns in that section, each with:
  - speaker: "Socrates" or "Euthyphro"
  - turn_range: approximate turn numbers from the raw turn data
  - act: what the speaker is doing (proposing, questioning, agreeing, objecting, evading, etc.)
  - propositions_asserted: what the speaker states as their own view
  - propositions_conceded: what the speaker agrees to under questioning (even if they wouldn't have volunteered it)
  - propositions_presupposed: anything implied but not explicitly stated

Here is the section index for reference:
{section_index}

Here is the full dialogue text:
{dialogue_text}

Here are the raw turn numbers for reference (232 speaker-change turns):
{turn_summary}

Return a JSON array of section objects."""


def build_pass1_prompt(turns: list[dict], dialogue_text: str, section_index: str) -> str:
    # Compact turn summary: just id, speaker, first 60 chars
    turn_lines = []
    for t in turns:
        preview = t["text"][:60].replace('"', "'")
        turn_lines.append(f'T{t["turn_id"]}: {t["speaker"]}: "{preview}..."')
    turn_summary = "\n".join(turn_lines)

    return PASS1_PROMPT_TEMPLATE.format(
        section_index=section_index,
        dialogue_text=dialogue_text,
        turn_summary=turn_summary,
    )


# ======================================================================
# Pass 2: Schema-informed
# ======================================================================

PASS2_PROMPT_TEMPLATE = """You are annotating Plato's Euthyphro for a formal game-theoretic encoding. Below is the full dialogue text, the raw turn segmentation (232 speaker-change turns), and the annotation schema you must follow.

Your task: For each of the 19 dialogue sections identified in the section index, produce a schema-compliant annotation. Focus on the SUBSTANTIVE turns — turns where definitions are proposed, concessions are made, or refutations are delivered. Skip purely phatic turns ("Yes.", "True.", "Certainly.") UNLESS they constitute a concession to a Socratic question that carries a presupposition.

For each substantive turn or group of turns, provide:
- turn_range: the turn IDs covered (e.g. "T108-T138" for the Euthyphro dilemma)
- speaker: "Socrates" or "Euthyphro"
- stephanus: Stephanus reference
- speech_act: primary and secondary if applicable, with justification
- commitment_delta: what was added, removed, or suspended
  - For each added item: holder, proposition (normalized per the rules), type (commitment | assertion | presupposition | conditional_commitment), source (explicit | extracted | implicit), available_to (both | socrates_only | euthyphro_only), confidence (high | medium | low)
  - For conditional_commitments: include antecedent, consequent, antecedent_status, discharged
  - For removed items: exact string match to a prior proposition, removal_type
  - For suspended items: reason
- cycle_signal: flag if this turn demonstrates circularity, with definition IDs
- annotation_confidence and notes

IMPORTANT RULES:
1. "Piety is what is dear to the gods" and "Piety is what all the gods love" are DIFFERENT propositions. Do not normalize to equivalence.
2. Conditionals stay conditional until discharged. "If X then Y" enters as conditional_commitment.
3. Euthyphro's one-word agreements ("Yes", "True", "Certainly") to Socratic questions ARE concessions if the question carries a substantive presupposition. Flag these.
4. Mark confidence: low on any commitment inference that a reasonable scholar might contest.
5. The terminal condition is CIRCULARITY (D5 reduces to D3), not flat inconsistency.

Here is the annotation schema and methodology:
{schema}

Here is the section index for structural reference:
{section_index}

Here is the full dialogue text:
{dialogue_text}

Here is the raw turn data (232 turns):
{turn_summary}

Return a JSON object with a "sections" array, where each section contains the annotated turns for that dialogue section."""


def build_pass2_prompt(
    turns: list[dict], dialogue_text: str, section_index: str, schema: str
) -> str:
    turn_lines = []
    for t in turns:
        preview = t["text"][:80].replace('"', "'")
        turn_lines.append(f'T{t["turn_id"]} [{t["line_start"]}-{t["line_end"]}] {t["speaker"]}: "{preview}..."')
    turn_summary = "\n".join(turn_lines)

    return PASS2_PROMPT_TEMPLATE.format(
        schema=schema,
        section_index=section_index,
        dialogue_text=dialogue_text,
        turn_summary=turn_summary,
    )


# ======================================================================
# Main
# ======================================================================


def main():
    api_key = get_api_key()
    turns = load_raw_turns()
    dialogue_text = load_dialogue_text()
    section_index = load_section_index()
    schema = load_schema()

    output_dir = HERE / "llm_extractions"
    output_dir.mkdir(exist_ok=True)

    if "--pass2-only" not in sys.argv:
        print("=== Pass 1: Context-minimal extraction ===")
        prompt1 = build_pass1_prompt(turns, dialogue_text, section_index)
        print(f"  Prompt length: {len(prompt1)} chars")
        call_gemini(api_key, prompt1, output_dir / "pass1_gemini.json")

    print("\n=== Pass 2: Schema-informed extraction ===")
    prompt2 = build_pass2_prompt(turns, dialogue_text, section_index, schema)
    print(f"  Prompt length: {len(prompt2)} chars")
    call_gemini(api_key, prompt2, output_dir / "pass2_gemini.json")

    print("\nDone. Outputs in models/euthyphro/llm_extractions/")
    print("Next: diff the two passes and triage divergences.")


if __name__ == "__main__":
    main()
