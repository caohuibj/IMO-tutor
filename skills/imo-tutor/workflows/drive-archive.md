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
    P000123-A01-visual-01.png
    P000123 Note
```

Rules:

- Problem folder: `<problem_id>`
- Problem images: `<problem_id>-problem-<NN>.<ext>`
- Attempt ID: `<problem_id>-A<attempt_no:02d>`; attempt 100 naturally becomes `A100`
- Solution images: `<attempt_id>-solution-<NN>.<ext>`
- Optional generated mathematical visuals: `<attempt_id>-visual-<NN>.<ext>`
- Durable note: native Google Doc named `<problem_id> Note`
- Keep transcription in `Attempts.solution_transcription`; do not create separate transcription/review files in this workflow.
- Do not create separate post-review JSON/Markdown files; Historical Transfer, Mathematical Extraction, Higher Mathematics Bridge, Reinforcement Problems, and Visual Model belong in the durable note.

## Problem identity

`Problem_Index` contains exactly one row per Problem.

For intake, reuse an existing Problem when any of these exact identities is available:

1. explicit `problem_id`;
2. exact canonical globally unique `source_id`, such as `IMO-2024-P1`;
3. exact normalized statement.

Ambiguous/local source IDs such as `P1`, `1`, or `A3` are metadata only and must not trigger deduplication. Otherwise allocate the next `Pxxxxxx` from the maximum numeric suffix in `Problem_Index` plus one. Do not use UUIDs, timestamps, fuzzy matching, or a separate sequence store.

## Write points

### New problem

For a genuinely new Problem:

1. create the `<problem_id>` folder;
2. archive supplied problem images when the runtime exposes uploadable originals;
3. append one `Problem_Index` row with `status=ANALYZED`, `folder_url`, and `problem_image_url` when archived.

If an image was supplied but could not actually be uploaded, leave the image URL empty/null as the schema allows, report that the persistence loop is incomplete, and do not claim success.

### Active attempt and checkpoint submissions

Keep the active Attempt open across one or more solution/photo/text checkpoint submissions. A checkpoint does not end the Attempt and does not create an `Attempts` row. The normal completion trigger is the explicit phrase `此题完成`.

Use:

- `attempt_no = Problem_Index.attempt_count + 1`;
- `attempt_id = <problem_id>-A<attempt_no:02d>`.

Do not write an incomplete `Attempts` row that lacks `submitted_at`, `verdict`, or `result_bucket`.

When checkpoint images are materializable, they may be uploaded incrementally under the active `<attempt_id>-solution-<NN>` names and their observed URLs kept in transient state for final materialization. This does not finalize the Attempt. Interim reviews remain chat/session state.

### Completion-triggered submitted attempt

A photo/text submission by itself does not trigger durable Attempt materialization. Only when the student explicitly says `此题完成` does the normal completed Attempt finalize.

On `此题完成`:

1. archive any remaining materializable original solution images in the existing Problem folder;
2. assemble/transcribe the latest coherent solution from all checkpoint submissions without repairing mathematical mistakes;
3. complete the final mathematical review;
4. append exactly one `Attempts` row for the whole Attempt, including image URLs/status, final transcription, verdict, result bucket, score/gap/error fields, timing, and hint metadata;
5. update the existing `Problem_Index` row summary fields (`last_attempt_at`, `attempt_count`, latest result, best score, hint/error/key-insight/search fields as applicable);
6. run `post-review-transfer.md` for Modules 2–6;
7. if a Visual Model is generated and the runtime exposes an uploadable asset, archive it and reference the observed Drive URL in the note.

Multiple checkpoint submissions before `此题完成` belong to this single Attempt and must not create multiple `Attempts` rows.

Do not append a second `Problem_Index` row for a redo.

### Attempt ended by give-up or H6 without `此题完成`

Give-up/H6 ends the current Attempt but does **not** activate Modules 2–6. Finalize once using the student state that existed before any H6 solution is revealed.

If there has been **no substantive student solution work**, materialize one durable `Attempts` row with:

- the current `attempt_id` / `attempt_no`;
- `submitted_at` set to the attempt end time;
- `verdict=UNSOLVED`;
- `result_bucket=UNSOLVED`;
- the final `hint_max` and `hint_count`;
- empty/null solution fields as appropriate.

If one or more substantive checkpoint submissions exist:

1. archive any remaining materializable checkpoint images;
2. assemble/transcribe the latest coherent student work without repairing it;
3. perform the final Core Review on that student work;
4. assign the evidence-based `verdict`, `result_bucket`, estimated score, `first_gap`, error/method fields, timing, and hint metadata;
5. append exactly one durable `Attempts` row;
6. update the same `Problem_Index` summary row.

Do **not** force `UNSOLVED` merely because the student gave up or requested H6 after doing substantive work. If H6 caused the attempt to end, record `hint_max=H6`. Finalize the student's work **before** the complete solution is released. Never mix H6/teacher solution content into `solution_transcription` or student-derived `key_insight`.

Give-up/H6 finalization never activates Historical Transfer, Mathematical Extraction, Higher Mathematics Bridge, Reinforcement Problems, or Visual Model by itself.

### Note and archive

Maintain one native Google Doc named `<problem_id> Note` per Problem; update it on later Attempts instead of creating a new note.

#### A. Normal completion through `此题完成`

Archive in this order:

1. finalize the Attempt review and materialize/update the required Sheet rows;
2. run the six-module post-review transfer workflow;
3. archive any uploadable Visual Model assets that were actually generated;
4. compile/create/update the durable note, including the completed Attempt and six-module feedback content;
5. read the note back successfully and verify the finalized `attempt_id` block is present without deleting older Attempt blocks;
6. write the observed `note_url` to `Problem_Index` and to the relevant finalized `Attempts` rows;
7. update the Problem summary and set `status=ARCHIVED`;
8. read back the `Problem_Index` row and verify `status=ARCHIVED`, `folder_url`, and `note_url` are present before telling the student the chat can be archived.

#### B. Attempt ended by give-up/H6 without `此题完成`

Archive the finalized Attempt normally, but **do not run or populate Modules 2–6** merely because the Attempt ended. Compile/update the note with its own `attempt_id` block, preserving any substantive student checkpoint work and the evidence-based Core Review; if there was no substantive work, record the `UNSOLVED` Attempt state. Respect the no-spoiler state and keep any H6/teacher solution separate from the student transcription. Then read the note back, verify the new Attempt block and all older Attempt blocks remain present, and perform the same Sheet verification required for `ARCHIVED`.

`ARCHIVED` therefore requires a verified durable note and successful Sheet readback. A missing optional visual asset does not block `ARCHIVED`, but its absence must not be misrepresented as successful visual archival.

## Reinforcement-problem persistence

Externally recommended reinforcement problems are recommendations only. Do not append them to `Problem_Index`, create Problem folders, or count them as Attempts merely because they appeared in feedback.

Only after the student chooses a recommended problem should a fresh working Chat run `problem-intake.md`, allocate/reuse the proper Problem identity, and begin at H0 in `SOLUTION_LOCKED` state.

## Data behavior

- Use the exact columns defined by `problem.schema.json` / `attempt.schema.json` and present in the initialized Sheet headers. CSV templates are setup assets and are not required as Project runtime sources.
- Serialize every array-valued field in Sheet cells as a compact JSON array, for example `["GEO.Circle","GEO.Tangent"]`. Do not switch between delimiter-separated and JSON encodings across chats or rows.
- Store only controlled tag IDs; do not invent alternate spellings.
- Do not place image bytes in Sheet cells. Store Drive URLs/IDs and image archive status where existing schema fields support them; richer visual metadata stays in the note in this version.
- Do not claim an original or generated image has been archived unless the Drive upload actually succeeded.
- Prefer the shortest successful connector sequence; do not add speculative retry systems or alternate storage paths.