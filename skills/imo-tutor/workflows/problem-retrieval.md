# Problem Retrieval

Use for exact IDs, fuzzy natural-language searches, redo requests, and post-review historical-transfer retrieval.

## Source of truth

Query Google Drive/Sheets durable records. Do not answer from remembered chat history when the request refers to prior student work. Continue using `Problem_Index`, `Attempts`, and the durable problem note; do not introduce vector search or another retrieval store in this workflow.

## Action precedence

Classify the user action before loading durable content. If the request is a redo, route directly to **Redo mode**. Redo intent takes precedence over exact lookup, even when the request contains an exact or short-form Problem ID such as `重做 P00237`; normalize the ID, but do not load `note_url` content or old `Attempts` before the new Attempt is finalized.

## Exact lookup

Canonical stored IDs use six digits, for example `P000237`. Accept a user-entered `P` followed by 1-6 digits and left-pad the numeric part to six digits before lookup, so `P00237` resolves to `P000237`.

For an exact lookup such as `P000237`:

1. normalize the ID;
2. fetch exactly the matching `Problem_Index` row;
3. follow its `note_url` and return the durable problem note;
4. do not run fuzzy search when the exact row exists.

If the row does not exist, report that the problem ID was not found. Do not guess a nearby ID.

## Fuzzy query parsing

Translate the user's wording into `search-query.schema.json` fields before reading rows. Prefer controlled fields over free-text matching.

Common semantics:

- `最近` -> sort by `attempt_at` descending.
- `做错` -> `result_buckets = [INCORRECT]`.
- `没完全做对` -> `result_buckets = [PARTIAL, INCORRECT, UNSOLVED]`.
- `曾经做错` -> `historical_result_match = true` with `INCORRECT`.
- `几何/数论/代数/组合` -> `GEO/NT/ALG/CMB`.
- `难度8以上` -> `difficulty_gte = 8.0`.
- `用过H3提示` -> `hint_min = H3`; hint levels are ordered `H0 < H1 < ... < H6`.
- known method phrases use controlled method tags, e.g. `反演` -> `M.GEO.Inversion`.
- generic logic-error wording may use an error-category prefix such as `LOGIC.*`; exact known errors should use the full controlled error tag.
- an explicit number such as `2道` -> `limit = 2`.
- words that cannot be represented by controlled fields go to `keywords` for `search_text` fallback.

## Query execution

Use the shortest structured path that can answer the query.

1. Exact `problem_id` -> `Problem_Index` + durable note only.
2. Pure problem metadata filters with no attempt-level conditions may query `Problem_Index` directly.
3. Queries involving result, hint use, student method, error, or attempt date query `Attempts` first. Use the snapshot fields already stored there; join `Problem_Index` only after candidate problem IDs are known.
4. Apply domain, difficulty, date, result, hint, concept, method, and error filters before `search_text`.
5. Use `search_text` only for unresolved `keywords`, and only on the structured candidate set when possible. Do not use free-text search as the default retrieval path.
6. Deduplicate by `problem_id`, sort as requested, stop after `limit`, and return a short candidate list with problem IDs and safe identifying metadata. Load a full note only after an exact ID is selected.

`attempt_at` is the selected Attempt's `submitted_at` timestamp used for sorting.

### Latest-versus-historical result semantics

When `result_buckets` is present and `historical_result_match=false`, scan newest first and keep only the first (latest) Attempt encountered for each `problem_id`, then apply the query filters. An older incorrect Attempt must not make a problem match after a later correct Attempt.

When `historical_result_match=true`, any historical Attempt may satisfy the result filter. Deduplicate by `problem_id` and rank each problem by its most recent matching Attempt.

When no result filter is present, attempt-level filters such as `hint_min`, `method_tags`, and `error_tags` may match any Attempt; deduplicate by `problem_id` using the most recent matching Attempt. This supports queries such as `难度8以上用过H3提示的数论题` and `那道我用了反演但最后逻辑有问题的几何题` without forcing a vector database.

For category-prefix error filters such as `LOGIC.*`, match any stored `error_tag` beginning with `LOGIC.`.

## Post-review historical-transfer retrieval

Use this mode only after the current Attempt has been explicitly completed with `此题完成` and finalized. It is an internal retrieval path for Module 2 of `post-review-transfer.md`, not a substitute for user-facing fuzzy search.

Build a small historical candidate set at **Attempt grain**. Before ranking:

- exclude the current `attempt_id`;
- do not deduplicate by `problem_id`;
- allow older Attempts of the same Problem;
- for same-Problem candidates require `attempt_no < current attempt_no`.

Derive an internal current-Attempt transfer signature before ranking. It may include exact Note-level `TP.*` Thinking Pattern IDs from `thinking-patterns.json`; this prepass is retrieval-only and does not alter the student-visible six-module order.

Then rank in this order:

1. same or closely related `TP.*` Thinking Pattern IDs from durable Attempt blocks/notes;
2. same or closely related `error_tags` / `error_targets`;
3. same student-used `method_tags`;
4. same or closely related `concept_tags`;
5. structurally similar blocker or proof pattern using `search_text` as a fallback;
6. same surface domain/topic only as a weak fallback.

Use Sheet fields for efficient initial recall, then exact `TP.*` matches in durable notes when cross-domain structural retrieval is useful. Do not introduce a vector store.

Prefer mathematical-mechanism similarity over source, score, or superficial wording. A previous high-scoring Attempt may still be useful if it exposed the same fragile step; a previous low-scoring Attempt may be irrelevant if its blocker was different.

Retrieve 3–5 candidates when possible, then inspect only the 1–2 strongest candidate notes/Attempts in depth. The goal is to decide whether a previously observed issue is now `RESOLVED`, `IMPROVED`, `RECURRED`, `NOT_TESTED`, or has been replaced by a `NEW_ISSUE`. These judgments are note-level prose labels in this version, not stored enums.

Do not run this mode before a redo has been explicitly completed with `此题完成`.

## Redo mode

For `重做 P000237`:

1. normalize and locate the existing `Problem_Index` row;
2. before submission, read only the statement and safe metadata needed to start the attempt: `problem_id`, source, domain, difficulty, and other non-spoiling metadata;
3. do **not** load the durable note or old `Attempts` rows before the new attempt is finalized, because they may contain old solutions, key insights, error details, hint history, or reference-solution information;
4. reuse the existing Problem folder and note identity. Do not append a new `Problem_Index` row;
5. start a transient active attempt with `attempt_no = attempt_count + 1`, `attempt_id = <problem_id>-A<attempt_no:02d>`, `hint_max=H0`, and `hint_count=0`;
6. set `SOLUTION_LOCKED` and follow the normal hint/review flow;
7. checkpoint submissions do not materialize a durable `Attempts` row; keep the redo Attempt active across one or more submissions;
8. materialize exactly one new durable `Attempts` row when the student explicitly says `此题完成`, or when an existing give-up/H6 rule explicitly ends the Attempt;
9. only the `此题完成` path activates the six-module post-review transfer workflow;
10. after finalization, update the same `Problem_Index` row and the same `<problem_id> Note`.

## Post-redo comparison

Only after the new Attempt is finalized may any post-redo comparison occur. Automatically load the immediately preceding Attempt and show the redo progress comparison **only when the new redo Attempt was completed through explicit `此题完成`**. This comparison may be incorporated into Module 2 — Historical Transfer.

If the redo Attempt ended through give-up/H6 without `此题完成`, do **not** automatically load old Attempt content or emit post-redo comparison as part of the ending feedback. Historical comparison is allowed later only if the user separately requests retrieval/comparison after the Attempt has ended.

Use existing fields; do not create a progress table or new storage model.

Prefer these comparisons when available:

- duration: `duration_minutes`;
- hint dependence: `hint_max` / `hint_count`;
- outcome: `verdict`, `result_bucket`, `estimated_score`;
- mathematical blocker: `first_gap`, `error_tags`;
- approach change: `method_tags`.

Example shape:

```text
A01: 52 min | H3 | 3/7
A02: 24 min | H0 | 7/7
Change: -28 min | H3 -> H0 | +4 points
```

If a field is missing, omit that comparison rather than inventing a value. The comparison is derived from `Attempts`; no additional persistence layer is needed.

The post-redo comparison may be incorporated into the broader Historical Transfer module when that produces a clearer training narrative.