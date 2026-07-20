# Darija Code-Switch Eval

**Status:** MVP complete — 60 items, native-reviewed, run against two frontier
models (Gemini 3.1 Flash-Lite, Claude Sonnet 5), scored by an LLM judge with
manual spot-checks. See Results below.

## Motivation

Existing Darija benchmarks (DarijaMMLU, DarijaHellaSwag, DarijaBench, from the
Atlas-Chat project; TerjamaBench from AtlasIA) evaluate models on clean,
single-register input — a full question in Darija, or MSA, or Arabizi, but
not mixed. Real Moroccan text messaging and speech constantly code-switches
between French, Darija (Arabic script), and Darija (Arabizi/Latin script),
often within a single sentence. A 2025 survey of 40+ Arabic LLM benchmarks
flagged "cultural misalignment in translated datasets" and "insufficient
multi-turn dialogue assessment" as open gaps — this project targets the
code-switching piece of that gap directly.

This is **not** a from-scratch benchmark. It extends existing work by testing
a scenario (natural code-switching) that published Darija benchmarks don't
cover.

## Method

1. 60 hand-written items spanning three categories (factual QA, reasoning,
   instruction-following) and four registers (French-Darija codeswitch,
   Darija Arabizi, Darija Arabic script, with control items in each pure
   register alongside the codeswitched ones).
2. Every item was drafted as an LLM first pass, then corrected by a native
   Darija speaker before being accepted into the set — the corrections
   themselves are logged in `data/style_notes.md` as a running grammar guide.
3. Ran the full set against two models from different families: Gemini 3.1
   Flash-Lite and Claude Sonnet 5.
4. Scored every response with an LLM-judge pass (Claude, see caveat below),
   verdicting each as CORRECT / PARTIAL (right content, wrong register) /
   INCORRECT, cross-checked against a manual read of a subset.

**Not done, flagged as future work:** a baseline rerun of an existing
single-register benchmark (DarijaMMLU or TerjamaBench) against current
frontier models, to check whether published numbers have drifted since those
benchmarks were released. The infrastructure supports it; it just wasn't
run in this pass.

## Results

### Headline numbers

| Model | CORRECT | PARTIAL | INCORRECT | n |
|---|---|---|---|---|
| Gemini 3.1 Flash-Lite | 35 (58%) | 23 (38%) | 2 (3%) | 60 |
| Claude Sonnet 5 | 20 (33%) | 36 (60%) | 4 (7%) | 60 |

Scored by an LLM judge (Claude) against gold answers and per-item failure
notes, with the caveat that Claude judging its own outputs risks
self-preference bias, which would push Claude's numbers up, not down.
Claude still scored lower than Gemini, which makes the gap more
trustworthy, not less.

### Finding 1: register fidelity differs substantially by model

The original hypothesis was that code-switched input would confuse models
into the wrong register. Instead, the two models differ in how reliably
they honor the requested register at all, across nearly every category,
most sharply on pure-Arabizi instructions, where Gemini got 1/6 items in
full correct register and Claude got 0/6, drifting into MSA every time.

### Finding 2: topic-triggered French collapse replicates, narrower than expected

France-adjacent topics (Eiffel Tower, official language/currency,
inter-city travel) triggered full French collapse on both models for
several items (cs_007, 015, 018, 023, 035, 038, 045). This replicates
across model families, but the formal scoring shows it is a specific case
of the broader register-fidelity gap in Finding 1, not the dominant driver
on its own.

### Finding 3: models make the same dialectal mistakes the style guide predicts

- cs_057: Claude answered the Darija word for "earn money" as if it meant
  "save money," the exact njme3-vs-ndir confusion documented in
  data/style_notes.md from the item-writing phase.
- cs_036: both models gave the same wrong founding year for Al Akhawayn
  University (1995 instead of 1993).

### Correction to an earlier claim

An early manual read concluded that explicit "answer in Darija"
instructions reliably override topic-driven drift in both models. The
formal scoring pass does not fully support that: cs_052 was scored PARTIAL
for Claude despite the direct instruction. Recorded here rather than
dropped, since catching this is part of what native review is for.

## Repo layout

    data/
      schema.md               item field definitions
      style_notes.md          running Darija grammar guide
      items_template.jsonl    one example per register/category
      seed_items_draft.jsonl  the 60 native-reviewed items
    harness/
      models.py               API client wrappers per model
      run_eval.py              runs items, caches results
      score.py                 exact match for MCQ, flags open items
      judge.py                 LLM-judge pass with verdicts
    results/
      gemini_results.jsonl        raw Gemini responses
      claude_results.jsonl        raw Claude responses
      judge_gemini_results.jsonl  judge verdicts on Gemini
      judge_claude_results.jsonl  judge verdicts on Claude

## Running it

This needs network access to Anthropic and Google APIs, so run it on your
own machine, not in a sandboxed environment.

    pip install -r requirements.txt --break-system-packages
    cp .env.example .env
    python harness/run_eval.py --items data/seed_items_draft.jsonl --model claude
    python harness/judge.py --results results/claude_results.jsonl --items data/seed_items_draft.jsonl

## Limitations

- 60 items is a small sample; some category/register subgroups are only
  5-6 items, so per-cell percentages are directional, not precise.
- The LLM judge is Claude, scoring both models including itself.
- Only two models compared. A third, ideally Atlas-Chat, would strengthen
  the claim, but it is not hosted by any enabled Inference Provider.
- No native-speaker quality grading of the Darija itself in CORRECT
  responses, only content plus register.

## Citing prior work

- Atlas-Chat, DarijaMMLU, DarijaHellaSwag, DarijaBench, MBZUAI-Paris
- TerjamaBench, Darija Chatbot Arena, AtlasIA
- Arabizi vs LLMs, 2025
- Nile-Chat, dual-script Egyptian Arabic models
- "Evaluating Arabic Large Language Models" survey, 2025
