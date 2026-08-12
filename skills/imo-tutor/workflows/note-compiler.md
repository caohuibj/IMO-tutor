# Note Compiler

Compile the durable human-readable note for a problem.

## Storage

Maintain exactly one native Google Doc named `<problem_id> Note` inside the Problem folder. Later Attempts update the same note. Markdown/LaTeX is the content convention; v0.2 does not create parallel `.md`, transcription, review, or JSON files.

## Required sections

1. Problem metadata: ID, source, date, domain, difficulty.
2. Problem statement.
3. Attempt history: date/time, duration, hint usage, verdict, estimated score.
4. Student solution transcription, preserving attempt boundaries.
5. Teacher review: first gap, logic, strategy, writing, error tags.
6. Corrected/revised proof when the student produced one.
7. Reference solution comparison when available.
8. Key insight and reusable lemmas/methods.
9. The actual blocker: knowledge, technique, observation, strategy, execution, logic, writing, or time.
10. `Next time I see this`: one compact retrieval cue for future transfer.

The note is for reading; structured fields remain in Sheets. Do not duplicate every database column as prose.

After create/update, read the note back before its URL is used to archive the Problem. Write the observed `note_url` back to `Problem_Index` and the relevant finalized `Attempts` rows.
