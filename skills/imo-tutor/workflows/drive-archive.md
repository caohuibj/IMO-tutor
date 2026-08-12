# Drive Archive

Use the connected Google Drive/Sheets tools directly as the persistence layer. Do not introduce a repository layer, storage abstraction, queue, or secondary database for this workflow.

## Defaults

- Root folder: `IMO Tutor Data`
- Index workbook: `IMO Learning DB`
- Tabs: `Problem_Index`, `Attempts`

If the project explicitly configures other targets, use them.

## Storage layout and names

Use one Drive folder per Problem:

```text
IMO Tutor Data/
  P000123/
    P000123-problem-01.jpg
    P000123-A01-solution-01.jpg
    P000123-A01-solution-02.jpg
    P000123 Note
```

Rules:

- Problem folder: `<problem_id>`
- Problem images: `<problem_id>-problem-<NN>.<ext>`
- Attempt ID: `<problem_id>-A<attempt_no:02d>`
- Solution images: `<attempt_id>-solution-<NN>.<ext>`
- Durable note: native Google Doc named `<problem_id> Note`
- Keep transcription in `Attempts.solution_transcription`; do not create separate transcription/review files in v0.2.

## Problem identity

`Problem_Index` contains exactly one row per Problem.

For intake, reuse an existing Problem when any of these exact identities is available:

1. explicit `problem_id`;
2. exact `source_id`;
3. exact normalized statement.

Otherwise allocate the next `Pxxxxxx` from the maximum numeric suffix in `Problem_Index` plus one. Do not use UUIDs, timestamps, fuzzy matching, or a separate sequence store.

## Write points

### New problem

For a genuinely new Problem:

1. create the `<problem_id>` folder;
2. archive supplied problem images when the runtime exposes uploadable originals;
3. append one `Problem_Index` row with `status=ANALYZED`, `folder_url`, and `problem_image_url` when archived.

If an image was supplied but could not actually be uploaded, leave the image URL empty/null as the schema allows, report that the persistence loop is incomplete, and do not claim success.

### Active attempt

Before the student submits work, keep the active attempt as transient chat/session state.

Use:

- `attempt_no = Problem_Index.attempt_count + 1`;
- `attempt_id = <problem_id>-A<attempt_no:02d>`.

Do not write an incomplete `Attempts` row that lacks `submitted_at`, `verdict`, or `result_bucket`.

### Submitted attempt

Submission triggers durable materialization after the review has produced the required fields.

1. archive all materializable original solution images in the existing Problem folder;
2. transcribe the student's work to Markdown/LaTeX without repairing mistakes;
3. complete the mathematical review;
4. append exactly one `Attempts` row for the attempt, including image URLs/status, transcription, verdict, result bucket, score/gap/error fields, timing, and hint metadata;
5. update the existing `Problem_Index` row summary fields (`last_attempt_at`, `attempt_count`, latest result, best score, hint/error/key-insight/search fields as applicable).

Do not append a second `Problem_Index` row for a redo.

### End without submission

If the student explicitly gives up or requests H6 before submitting any solution, materialize one durable `Attempts` row with:

- the current `attempt_id` / `attempt_no`;
- `submitted_at` set to the attempt end time;
- `verdict=UNSOLVED`;
- `result_bucket=UNSOLVED`;
- the final `hint_max` and `hint_count`;
- empty/null solution fields as appropriate.

If H6 caused the attempt to end, record `hint_max=H6`. Do not invent a `first_gap`, student solution, or student-derived key insight when none exists. Then update the same `Problem_Index` summary row.

### Note and archive

Maintain one native Google Doc named `<problem_id> Note` per Problem; update it on later Attempts instead of creating a new note.

Archive in this order:

1. compile/create/update the durable note;
2. read the note back successfully;
3. write the observed `note_url` to `Problem_Index` and to the relevant finalized `Attempts` rows;
4. update the Problem summary and set `status=ARCHIVED`;
5. read back the `Problem_Index` row and verify `status=ARCHIVED`, `folder_url`, and `note_url` are present before telling the student the chat can be archived.

`ARCHIVED` therefore requires a verified durable note and successful Sheet readback.

## Data behavior

- Use the exact columns in the bundled CSV templates.
- Store controlled tags as delimiter-separated IDs or JSON strings consistently; do not invent alternate spellings.
- Do not place image bytes in Sheet cells. Store Drive URLs/IDs and image archive status.
- Do not claim an original image has been archived unless the Drive upload actually succeeded.
- Prefer the shortest successful connector sequence; do not add speculative retry systems or alternate storage paths.
