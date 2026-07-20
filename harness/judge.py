"""
LLM-judge scoring pass. For each open-ended item, asks Claude to judge the
model's response as CORRECT, PARTIAL (right content, wrong register), or
INCORRECT, using the gold answer and the item's notes field.

Caveat, stated plainly: this uses Claude as the judge for BOTH Gemini's and
Claude's own answers. Self-preference bias (a judge favoring outputs from
its own model family) is a documented issue in LLM-as-judge setups. Treat
CORRECT verdicts on Claude's own answers with a bit more skepticism than
CORRECT verdicts on Gemini's - and treat any PARTIAL/INCORRECT verdict on
Claude's own answers as fairly trustworthy, since a biased judge would be
less likely to produce those against itself.

Usage:
    python harness/judge.py --results results/gemini_results.jsonl --items data/seed_items_draft.jsonl
    python harness/judge.py --results results/claude_results.jsonl --items data/seed_items_draft.jsonl
"""

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()


def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def judge_prompt(item, response):
    return f"""You are scoring a model's answer to a Darija (Moroccan Arabic) \
question for a research eval. Judge on two axes: factual/content \
correctness, and register (the answer should be in Darija, not French or \
formal MSA, unless the question explicitly calls for a different register).

Question: {item['prompt']}
Register expected: {item['register']}
Expected answer / gold: {item['gold_answer']}
Notes on what a failure looks like: {item.get('notes', '')}

Model's answer: {response}

Respond in exactly this format, nothing else:
VERDICT: <CORRECT|PARTIAL|INCORRECT>
REASON: <one sentence>

Where:
- CORRECT: factually right AND in the right register
- PARTIAL: factually right but wrong register (e.g. answered in French \
instead of Darija), OR register is right but content has a minor error
- INCORRECT: wrong content, fundamental misunderstanding, or non-answer"""


def parse_verdict(text):
    verdict_match = re.search(r"VERDICT:\s*(CORRECT|PARTIAL|INCORRECT)", text, re.IGNORECASE)
    reason_match = re.search(r"REASON:\s*(.+)", text)
    verdict = verdict_match.group(1).upper() if verdict_match else "UNPARSED"
    reason = reason_match.group(1).strip() if reason_match else text.strip()[:200]
    return verdict, reason


def run_judge(results_path: str, items_path: str, output_path: str = None):
    from models import call_claude  # reuses the already-working Anthropic client

    results = load_jsonl(results_path)
    items_by_id = {i["id"]: i for i in load_jsonl(items_path)}

    if output_path is None:
        base = Path(results_path).stem
        output_path = f"results/judge_{base}.jsonl"

    Path("results").mkdir(exist_ok=True)

    done_ids = set()
    if os.path.exists(output_path):
        done_ids = {r["id"] for r in load_jsonl(output_path)}

    with open(output_path, "a") as out:
        for r in results:
            if r["id"] in done_ids:
                continue
            item = items_by_id.get(r["id"])
            if not item:
                continue

            if item["answer_type"] == "mcq":
                hit = item["gold_answer"].strip().lower() in r["response"].strip().lower()
                verdict = "CORRECT" if hit else "INCORRECT"
                reason = "auto exact-match check"
            else:
                try:
                    judge_response = call_claude(judge_prompt(item, r["response"]))
                    verdict, reason = parse_verdict(judge_response)
                except Exception as e:
                    verdict, reason = "ERROR", str(e)

            record = {
                "id": r["id"],
                "category": item["category"],
                "register": item["register"],
                "verdict": verdict,
                "reason": reason,
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            out.flush()
            print(f"{r['id']}: {verdict} - {reason}")

    return output_path


def summarize(judge_path: str):
    records = load_jsonl(judge_path)
    counts = defaultdict(lambda: defaultdict(int))
    for r in records:
        counts[(r["category"], r["register"])][r["verdict"]] += 1

    print(f"\n=== Summary: {judge_path} ===")
    print(f"{'Category':<22}{'Register':<22}{'CORRECT':<10}{'PARTIAL':<10}{'INCORRECT':<10}")
    for (cat, reg), v in sorted(counts.items()):
        print(f"{cat:<22}{reg:<22}{v.get('CORRECT',0):<10}{v.get('PARTIAL',0):<10}{v.get('INCORRECT',0):<10}")

    total = defaultdict(int)
    for r in records:
        total[r["verdict"]] += 1
    n = len(records)
    print(f"\nTotal (n={n}): CORRECT={total.get('CORRECT',0)}  "
          f"PARTIAL={total.get('PARTIAL',0)}  INCORRECT={total.get('INCORRECT',0)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True)
    parser.add_argument("--items", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    out_path = run_judge(args.results, args.items, args.output)
    summarize(out_path)
