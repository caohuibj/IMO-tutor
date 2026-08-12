# Problem Retrieval

Use for exact IDs and fuzzy natural-language searches in a new or existing chat.

## Source of truth

Query Google Drive/Sheets durable records. Do not answer from remembered chat history when the request refers to prior student work.

## Exact lookup

For `P000237`, fetch the matching `Problem_Index` row and the linked durable note/attempt records.

## Fuzzy query parsing

Translate the user's wording into `search-query.schema.json` fields. Common semantics:

- `最近` -> sort by the relevant attempt timestamp descending.
- `做错` -> `result_bucket = INCORRECT`.
- `没完全做对` -> `PARTIAL | INCORRECT | UNSOLVED`.
- `曾经做错` -> match any historical Attempt with `INCORRECT`, not only the latest result.
- `几何/数论/代数/组合` -> `GEO/NT/ALG/CMB`.
- `难度8以上` -> `difficulty_gte = 8.0`.
- `用过提示` -> `hint_min = H1`.
- an explicit number such as `2道` -> `limit = 2`.

For semantic phrases such as `那道用了圆和相似、最后逻辑不严谨的题`, search across controlled concept/method/error tags plus `search_text`, rank candidates, and return a short candidate list before loading a full note.

## Redo mode

For `重做 P000237`:

1. Load statement and safe metadata.
2. Create a new Attempt.
3. Set H0 and `SOLUTION_LOCKED`.
4. Do not show previous solution, key insight, error details that reveal the route, or prior hints until the new attempt is submitted.
