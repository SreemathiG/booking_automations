"""
AI Test Data Generator
======================
Uses Google Gemini (free tier) to generate test cases.
Run this ONCE before executing tests:
    python -m ai_generator.generate_test_data

Output is saved to test_data/search_data.json
Tests read from this JSON file — zero API calls during test execution.
"""

import json
import os
import sys
import urllib.request
import urllib.error

# Ensure project root is on the path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv
from ai_generator.prompts import SEARCH_DATA_PROMPT

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


def call_gemini(api_key: str, prompt: str) -> str:
    """Send a prompt to Gemini and return the raw text response."""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024
        }
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(request) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"\nERROR: Gemini API returned {e.code} {e.reason}")
        print(f"Details: {error_body}")
        sys.exit(1)

    except (KeyError, IndexError) as e:
        print(f"\nERROR: Unexpected Gemini response structure: {e}")
        sys.exit(1)


def extract_json(raw: str) -> list:
    """
    Robustly extract a JSON array from raw text.
    Handles cases where the model adds markdown code fences or extra commentary.
    """
    # Strip markdown code fences
    if "```" in raw:
        blocks = raw.split("```")
        for block in blocks:
            block = block.strip()
            if block.startswith("json"):
                block = block[4:].strip()
            if block.startswith("["):
                raw = block
                break

    # Find the JSON array boundaries
    start = raw.find("[")
    end   = raw.rfind("]") + 1

    if start == -1 or end == 0:
        print(f"\nERROR: No JSON array found in response.\nRaw output:\n{raw}")
        sys.exit(1)

    json_str = raw[start:end]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"\nERROR: JSON parsing failed: {e}")
        print(f"Extracted string:\n{json_str}")
        sys.exit(1)


def validate_cases(cases: list) -> list:
    """Ensure each case has the required fields."""
    required_fields = {"location", "expected_keyword", "description"}
    valid = []

    for i, case in enumerate(cases):
        missing = required_fields - set(case.keys())
        if missing:
            print(f"WARNING: Case {i+1} missing fields {missing} — skipping")
            continue
        valid.append(case)

    if not valid:
        print("ERROR: No valid test cases were generated.")
        sys.exit(1)

    return valid


def generate_and_save():
    # ── Validate API key ─────────────────────────────────────────
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if not api_key or api_key == "your-gemini-api-key-here":
        print("\nERROR: GEMINI_API_KEY is not set in your .env file.")
        print("Get a free key at: https://aistudio.google.com/app/apikey")
        print("Then update .env:  GEMINI_API_KEY=your-key-here\n")
        sys.exit(1)

    # ── Call Gemini ───────────────────────────────────────────────
    print("\nCalling Gemini API...")
    raw_response = call_gemini(api_key, SEARCH_DATA_PROMPT)

    # ── Parse + validate ──────────────────────────────────────────
    cases = extract_json(raw_response)
    cases = validate_cases(cases)

    # ── Save to file ──────────────────────────────────────────────
    output_dir  = os.path.join(PROJECT_ROOT, "test_data")
    output_path = os.path.join(output_dir, "search_data.json")
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

    # ── Summary ───────────────────────────────────────────────────
    print(f"\n✅ Generated {len(cases)} test cases → test_data/search_data.json\n")
    for i, case in enumerate(cases, 1):
        print(f"   {i}. [{case['location']}] {case['description']}")
    print()


if __name__ == "__main__":
    generate_and_save()