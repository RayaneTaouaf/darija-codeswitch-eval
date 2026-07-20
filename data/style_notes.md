# Style notes (running list, from native review)

Rules confirmed across two rounds of corrections — use these when drafting
new items so fewer come back with fixes.

## Gender agreement (houwa / hiya)
- Singular nouns need agreement: `houwa` (masc) / `hiya` (fem).
- Confirmed feminine: capitale, blockchain
- Confirmed masculine: jbel (mountain), rôle
- **Plural nouns take `houma` regardless of gender** — no houwa/hiya split
  for plurals (confirmed via "les avantages" / "le rôle" both working with
  no gender-specific fix needed once number was right).
- When in doubt on a new noun, default to writing it and flagging it as
  low-confidence rather than guessing.

## Vocabulary
- "know" → `3arf` (not `t3ref`/`t3rf`) — corrected twice, treat as settled.
- tomatoes → `maticha` (not `tomatich`)
- steps → `khatawat` (not `khtawat`)
- books → `ktouba` (not `ktoub`)
- speed/quickly → `sor3a` (not `sre3a`)
- distance → drop `kayna` when asking "chhal distance..." (no verb needed)

## Grammar / phrasing
- Time expressions ("at 8h") → `m3a` not `f`
- "at what time" → `m3ach` not `f ay wa9t`
- Duration ("how long did it take") → `da` not `dat`
- "capacity of / holds" (e.g. a bus) → `kayhez` not `kayb9a`
- Counting people with a quantity → needs `dial` (e.g. "28 dial nas", not
  just "28 nas")
- "give me" as indirect object → `liya` is often redundant/wrong where
  French already has an indirect pronoun — e.g. "donne moi" not "donne liya"
- "invite someone to X" → `n3red 3leh l X`, not a literal calque of "call
  them for X"
- Time-of-day spelling: `la3chya` (evening), not `l3achiya`
- fo9ach vs fach — `fo9ach` is the natural "when" for historical/date
  questions

## Definite article ("l-" / "le")
- Recurring miss: dropping the definite article where Darija keeps it.
  Confirmed: `l afkar` (not `afkar`), `f lkhedma` (not `f khedma`), `dial
  lktouba` (not `dial ktouba`). Default to including it when the English/
  French equivalent would use "the," and flag if unsure.

## Gender agreement extends to verbs, not just pronouns
- `taman` (price) is masculine → confirmed via `ikoun` not `tkoun`. So the
  houwa/hiya gender rule isn't just about the pronoun itself, it also
  determines verb conjugation. Apply gender-checking to verbs agreeing with
  a noun, not only to houwa/hiya questions.

## "chhal men X" construction
- Confirmed across both arabizi (`chhal men place`, `chhal men beida`) and
  arabic script (`شحال من كيلومتر`) — "how many/how much of X" needs `men`/
  `من`, dropping it reads as broken in both scripts. Treat as a general
  rule, not register-specific.

## Plural vs. singular in counted nouns
- Counted plural takes the plural noun form: `2 beidat` (eggs), not `2
  beida`. But the separate "how many of X" question construction uses the
  singular inside `chhal men X`: `chhal men beida`, not `chhal men beidat`.
  These look contradictory unless you treat them as two different
  constructions with different rules, not one rule.

## Resolved: njme3 vs. ndir
- `njme3` = save money. `ndir` = make/earn money. Not a register variant of
  the same idea - genuinely different verbs. cs_057's grammar correction
  (nwefer → ndir) silently changed the question from "how do I save money"
  to "how do I earn money." Fixed in the item, but worth remembering as a
  general risk: a grammar fix on a mistranslated verb can change what the
  question actually asks, not just how it's phrased. Worth a quick meaning
  sanity-check on any item where the corrected word is a verb, not just a
  function word.

## Resolved: n3red needs a pronoun object matching audience number
- `n3red` (invite) always takes a pronoun object matching who's being
  invited: `3leh` for singular (him), `3lihom` for plural (them). Confirmed
  in cs_056. Treat as a firm rule, not something to drop for brevity.

## Confidence notes
- Arabic-script items are consistently the ones needing the fewest content
  corrections once written carefully, but remain the register I'm least
  confident drafting from scratch — keep flagging new ones for review.
- Codeswitch items are where most vocabulary/phrasing mistakes cluster,
  which is itself informative: mixing registers is exactly where an LLM
  draft is least reliable, which is the whole premise of the project.
