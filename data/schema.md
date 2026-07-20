# Item schema

Each line in a `.jsonl` file is one item:

| field | type | notes |
|---|---|---|
| `id` | string | e.g. `cs_001`. Prefix by category: `cs_` codeswitch, `bl_` baseline rerun |
| `category` | string | `factual_qa` \| `reasoning` \| `instruction_following` |
| `register` | string | `codeswitch_fr_darija` \| `darija_arabic` \| `darija_arabizi` \| `msa` \| `french` |
| `prompt` | string | the actual text sent to the model |
| `answer_type` | string | `open` \| `mcq` |
| `choices` | list or null | only for `answer_type: mcq` |
| `gold_answer` | string | expected answer or key fact(s) the answer must contain |
| `source` | string | `original` if you wrote it, or benchmark name if adapted from an existing set |
| `notes` | string | why this item tests code-switch robustness specifically — what would a naive/wrong handling look like |

## Design notes for writing items

- Code-switch items should reflect how you'd *actually* text or say it, not
  a deliberately constructed mix. If it feels artificial to you when you
  write it, rewrite it.
- Vary where the switch happens: mid-sentence, between clauses, on a single
  loanword vs. a whole embedded phrase.
- Include a few items where getting the register wrong (e.g. responding in
  formal MSA to a casual Arabizi question) would itself count as a partial
  failure, even if the factual content is right — register mismatch is a
  real failure mode worth capturing, not just factual accuracy.
- Keep gold answers checkable. For `open` items, write 2-3 key facts the
  answer must contain rather than a single exact string, so scoring doesn't
  become a bottleneck.
- Watch gender agreement (`houwa`/`hiya`) on nouns, especially loanwords or
  technical terms (e.g. "capitale," "blockchain" are feminine). This is a
  cheap correctness check on items themselves, but it's also worth
  considering as its own evaluation dimension later - models may get gender
  agreement wrong even when they get the content right, which would be a
  genuinely Darija-specific failure mode not captured by English-centric
  benchmarks.
