# Problem Retrieval

Use for exact IDs and fuzzy natural-language searches in a new or existing chat.

## Source of truth

Query Google Drive/Sheets durable records. Do not answer from remembered chat history when the request refers to prior student work.

## Exact lookup

For `P000237`, search the matching `Problem_Index` row and then load the linked durable note/attempt records.

## Fuzzy query parsing

Translate the user's wording into `search-query.schema.json` fields. Common semantics:

- `最近` -> sort by `attempt_at` descending.
- `做错` -> `result_bucket = INCORRECT`.
- `没完全做对` -> `PARTIAL | INCORRECT | UNSOLVED`.
- `曾经做错` -> match any historical Attempt with `INCORRECT`, not only the latest result.
- `几何/数论/代数/组合` -> `GEO/NT/ALG/CMB`.
- `难度8以上` -> `difficulty_gte = 8.0`.
- `用过提示` -> `hint_min = H1`.
- an explicit number such as `2道` -> `limit = 2`.

`attempt_at` is the selected Attempt's `submitted_at` timestamp used for sorting.

`Attempts` deliberately contains snapshots of domain, difficulty, concept/method tags, and search text. For recent-attempt queries, scan bounded chunks from the newest end of `Attempts`.

- If `historical_result_match=false`, consider only the first (latest) Attempt encountered for each `problem_id`, then apply the requested filters. An older incorrect Attempt must not make a problem match if its latest Attempt is correct.
- If `historical_result_match=true`, any historical Attempt may satisfy the filters. Deduplicate results by `problem_id` and rank each problem by its most recent matching Attempt.

Stop once enough matching problem IDs are known. This avoids unnecessary full-table scans for common queries such as `最近做错的2道几何题` while preserving latest-versus-historical semantics.

For semantic phrases such as `那道用了圆和相似、最后逻辑不严谨的题`, search controlled concept/method/error tags plus `search_text`, rank candidates, and return a short candidate list before loading a full note.

## Redo mode

For `重做 P000237`:

1. Load the existing `Problem_Index` row, statement, and safe metadata.
2. Reuse the existing Problem folder and durable note. Do not append a new `Problem_Index` row.
3. Start a transient active attempt with `attempt_no = attempt_count + 1` and `attempt_id = P000237-A<attempt_no:02d>`, `hint_max=H0`, and `hint_count=0`.
4. Set H0 and `SOLUTION_LOCKED`.
5. Do not show previous solution, key insight, error details that reveal the route, or prior hints until the new attempt is submitted.
6. Materialize exactly one new durable `Attempts` row only when the student submits work or explicitly ends the attempt without a submission.
7. After finalization, update the same `Problem_Index` row and the same `<problem_id> Note`.
