"""
Score model results against gold answers.

For MCQ items: exact match on the choice letter/text.
For open items: this is the part that genuinely needs your judgment as a
native speaker, not just an LLM judge. Recommended flow:
  1. Run the LLM-judge pass below for a first cut (fast, gets you unstuck).
  2. Spot-check a sample yourself, especially anything the judge scored as
     correct where register might still be wrong (see notes field on the
     item - a factually right answer in the wrong register should probably
     count as a partial failure, and an LLM judge often won't catch that).

Usage:
    python harness/score.py --results results/claude_results.jsonl --items data/seed_items_draft.jsonl
"""

import argparse
import json


def load_jsonl(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def score_mcq(response: str, gold: str) -> bool:
    return gold.strip().lower() in response.strip().lower()


def llm_judge_prompt(item: dict, response: str) -> str:
    return f"""You are scoring whether a model's answer is correct AND in the right \
register (Darija, not French, not formal MSA, unless the question explicitly \
asked for a different register).

Question: {item['prompt']}
Expected: {item['gold_answer']}
Notes on what a failure looks like: {item.get('notes', '')}

Model's answer: {response}

Respond with exactly one line: CORRECT, PARTIAL (right content, wrong \
register), or INCORRECT, followed by a one-sentence reason."""


def score_results(results_path: str, items_path: str):
    results = load_jsonl(results_path)
    items_by_id = {i["id"]: i for i in load_jsonl(items_path)}

    for r in results:
        item = items_by_id.get(r["id"])
        if not item:
            continue
        if item["answer_type"] == "mcq":
            correct = score_mcq(r["response"], item["gold_answer"])
            print(f"{r['id']}: {'CORRECT' if correct else 'INCORRECT'} (auto)")
        else:
            print(f"{r['id']}: NEEDS JUDGE PASS - use llm_judge_prompt() then review by hand")
            print(f"  prompt: {item['prompt']}")
            print(f"  response: {r['response'][:200]}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--items", required=True)
    args = parser.parse_args()

    score_results(args.results, args.items)
