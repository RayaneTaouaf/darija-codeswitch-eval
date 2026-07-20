"""
Run a set of items against a model, caching results incrementally so a
crash or rate limit doesn't lose progress.

Usage:
    python harness/run_eval.py --items data/seed_items_draft.jsonl --model claude
"""

import argparse
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from models import MODEL_REGISTRY

load_dotenv()


def load_items(path: str) -> list[dict]:
    items = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def load_done_ids(results_path: str) -> set[str]:
    if not os.path.exists(results_path):
        return set()
    done = set()
    with open(results_path) as f:
        for line in f:
            line = line.strip()
            if line:
                done.add(json.loads(line)["id"])
    return done


def run(items_path: str, model_name: str, output_dir: str = "results", sleep: float = 1.0):
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f"Unknown model '{model_name}'. Options: {list(MODEL_REGISTRY)}")

    call_fn = MODEL_REGISTRY[model_name]
    items = load_items(items_path)

    Path(output_dir).mkdir(exist_ok=True)
    results_path = os.path.join(output_dir, f"{model_name}_results.jsonl")
    done_ids = load_done_ids(results_path)

    with open(results_path, "a") as out:
        for item in items:
            if item["id"] in done_ids:
                continue
            try:
                response = call_fn(item["prompt"])
                record = {
                    "id": item["id"],
                    "model": model_name,
                    "prompt": item["prompt"],
                    "register": item["register"],
                    "category": item["category"],
                    "response": response,
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
                print(f"[{model_name}] {item['id']} done")
            except Exception as e:
                print(f"[{model_name}] {item['id']} FAILED: {e}")
            time.sleep(sleep)  # be polite to rate limits


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--items", required=True, help="Path to items .jsonl")
    parser.add_argument("--model", required=True, choices=list(MODEL_REGISTRY))
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--sleep", type=float, default=1.0)
    args = parser.parse_args()

    run(args.items, args.model, args.output_dir, args.sleep)
