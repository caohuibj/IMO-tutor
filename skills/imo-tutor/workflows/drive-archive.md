# Drive Archive

Use the connected Google Drive/Sheets tools as the persistence layer.

## Defaults

- Root folder: `IMO Tutor Data`
- Index workbook: `IMO Learning DB`
- Tabs: `Problem_Index`, `Attempts`

If the project explicitly configures other targets, use them.

## Write points

### New problem

Immediately write/update a `Problem_Index` record with statement, source, tags, difficulty, creation time, and `status=ANALYZED`.

### Active attempt

Before the student submits work, keep the active attempt as transient chat/session state. Do not write an incomplete `Attempts` row that lacks `submitted_at`, `verdict`, or `result_bucket`.

### Submitted attempt

Write an `Attempts` record when the student submits work. Preserve the original solution image reference/status and store the transcription/note link.

### End without submission

If the student explicitly gives up or requests H6 before submitting any solution, materialize a durable `Attempts` row at that time with:

- `submitted_at` set to the attempt end time;
- `verdict=UNSOLVED`;
- `result_bucket=UNSOLVED`;
- the final `hint_max` and `hint_count`;
- empty/null solution fields as appropriate.

If H6 caused the attempt to end, record `hint_max=H6`. Do not invent a `first_gap`, student solution, or student-derived key insight when none exists.

### Review

Update the same Attempt with verdict, score estimate, first gap, error tags, key insight, and timing/hint metadata.

### Archive

Compile/update the durable note, update the Problem Index summary fields, set `status=ARCHIVED`, and verify the written record can be read back before telling the student the chat can be archived.

## Data behavior

- Use the exact columns in the bundled CSV templates.
- Store controlled tags as delimiter-separated IDs or JSON strings consistently; do not invent alternate spellings.
- Do not place image bytes in Sheet cells. Store Drive URLs/IDs and image archive status.
- Do not claim an original image has been archived unless the Drive upload actually succeeded.
