# Problem Retrieval

Use for exact IDs, fuzzy natural-language searches, and redo requests in a new or existing chat.

## Source of truth

Query Google Drive/Sheets durable records. Do not answer from remembered chat history when the request refers to prior student work. Continue using `Problem_Index`, `Attempts`, and the durable problem note; do not introduce vector search or another retrieval store for v0.4.

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

When `result_buckets` is present and `historical_result_match=false`, first keep only the latest Attempt for each `problem_id`, then apply the query filters. An older incorrect Attempt must not make a problem match after a later correct Attempt.

When `historical_result_match=true`, any historical Attempt may satisfy the result filter. Deduplicate by `problem_id` and rank each problem by its most recent matching Attempt.

When no result filter is present, attempt-level filters such as `hint_min`, `method_tags`, and `error_tags` may match any Attempt; deduplicate by `problem_id` using the most recent matching Attempt. This supports queries such as `难度8以上用过H3提示的数论题` and `那道我用了反演但最后逻辑有问题的几何题` without forcing a vector database.

For category-prefix error filters such as `LOGIC.*`, match any stored `error_tag` beginning with `LOGIC.`.

## Redo mode

For `重做 P000237`:

1. normalize and locate the existing `Problem_Index` row;
2. before submission, read only the statement and safe metadata needed to start the attempt: `problem_id`, source, domain, difficulty, and other non-spoiling metadata;
3. do **not** load the durable note or old `Attempts` rows before the new attempt is finalized, because they may contain old solutions, key insights, error details, hint history, or reference-solution information;
4. reuse the existing Problem folder and note identity; do not append a new `Problem_Index` row;
5. start a transient active attempt with `attempt_no = attempt_count + 1`, `attempt_id = <problem_id>-A<attempt_no:02d>`, `hint_max=H0`, and `hint_count=0`;
6. set `SOLUTION_LOCKED` and follow the normal hint/review flow;
7. materialize exactly one new durable `Attempts` row only when the student submits work or explicitly ends the attempt without a submission;
8. after finalization, update the same `Problem_Index` row and the same `<problem_id> Note`.

## Post-redo comparison

Only after the new Attempt is finalized, load the new Attempt and the immediately preceding Attempt and show a concise progress comparison. Use existing fields; do not create a progress table or new storage model.

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
