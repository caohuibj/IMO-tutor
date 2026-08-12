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

### New attempt

Write an `Attempts` record when the student submits work. Preserve the original solution image reference/status and store the transcription/note link.

### Review

Update the same Attempt with verdict, score estimate, first gap, error tags, key insight, and timing/hint metadata.

### Archive

Compile/update the durable note, update the Problem Index summary fields, set `status=ARCHIVED`, and verify the written record can be read back before telling the student the chat can be archived.

## Data behavior

- Use the exact columns in the bundled CSV templates.
- Store controlled tags as delimiter-separated IDs or JSON strings consistently; do not invent alternate spellings.
- Do not place image bytes in Sheet cells. Store Drive URLs/IDs and image archive status.
- Do not claim an original image has been archived unless the Drive upload actually succeeded.
