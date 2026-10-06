# Note Compiler

Compile the durable human-readable note for a problem after a durable Attempt finalization or later note update.

## Storage

Maintain exactly one native Google Doc named `<problem_id> Note` inside the Problem folder. Later Attempts update the same note. Markdown/LaTeX is the content convention. Do not create parallel transcription/review/post-review files in this workflow.

## Top-level structure

The note has two levels:

1. **Problem-level material** — statement, canonical metadata, and current synthesis.
2. **Attempt blocks** — one durable, attempt-bounded block per finalized Attempt, ordered by `attempt_no`.

Never merge the content of two Attempts into one review block. Later supplements (for example a reference-solution comparison) may be appended inside the same Attempt block with provenance, but the original student transcription and Core Review are not silently overwritten. Later Attempts may reinterpret progress without erasing earlier Attempt feedback.

## Required Problem-level sections

1. Problem metadata: ID, source, date, domain, difficulty, concepts, canonical methods.
2. Problem statement.
3. **Problem-level Synthesis**:
   - current key insight / reusable lemmas and methods;
   - current actual blocker or resolved blocker state;
   - `Next time I see this`: one compact retrieval cue for future transfer.

Problem-level synthesis may be updated after later Attempts, but it must not erase the historical Attempt blocks from which the synthesis was derived.

## Required Attempt block

For every finalized Attempt, append or update exactly one block headed by its exact `attempt_id`, for example `## P000123-A02`. Keep blocks ordered by `attempt_no`.

Each block contains, as applicable:

1. **Attempt metadata** — submitted/end time, duration, hint usage, verdict, result bucket, estimated score, and completion path (`此题完成`, give-up, or H6).
2. **Student solution transcription** — preserve the final coherent student work for that Attempt; never mix teacher/H6 mathematics into it.
3. **Core Review** — first gap, what remains valid, strategy, writing/rigor, repair advice, error tags, and proof compression.
4. **Corrected/revised proof** when the student produced one within that Attempt.
5. **Historical Transfer** — only when this Attempt was completed through explicit `此题完成`; include the historical Attempt IDs used and transfer judgment.
6. **Mathematical Extraction** — only on the `此题完成` path; separate Techniques, Insights, and Thinking Patterns. Store exact controlled `TP.*` IDs from `thinking-patterns.json` when applicable and record provenance (`STUDENT`, `HINT`, `REVIEW`, `REFERENCE`).
7. **Higher Mathematics Bridge** — only on the `此题完成` path; normally 1–3 genuine connections, each marked `SPECIAL_CASE`, `SAME_STRUCTURE`, or `ANALOGY`.
8. **Reference-solution comparison** when available. Preserve whether new ideas came from the reference rather than the student.
9. **Reinforcement Problems** — only on the `此题完成` path; record selected Near Transfer / Stretch / Disguised Transfer recommendations without external solution content.
10. **Visual Model** — only when useful on the `此题完成` path; record visualization goal, type, caption, memory hook, fidelity status (`FAITHFUL` or `SCHEMATIC`), higher-mathematics link when relevant, and durable image URL only if archival actually succeeded.

For a give-up/H6 ending without `此题完成`, do not populate Modules 2–6. If substantive checkpoint work exists, the Attempt block still contains the preserved student transcription and evidence-based final Core Review. If no substantive work exists, record the `UNSOLVED` Attempt with null/empty solution fields as appropriate.

## Thinking Pattern vocabulary

Thinking Pattern IDs are Note-level controlled vocabulary defined by `thinking-patterns.json`. They are not Sheet columns in this workflow. Use exact IDs; do not invent alternate spellings.

## Reference-solution refresh

A later official/reference solution may add a separate comparison subsection inside the relevant Attempt block. If that Attempt originally qualified for the six-module workflow, genuinely new reference-derived material may selectively refresh Mathematical Extraction, Higher Mathematics Bridge, Reinforcement Problems, or Visual Model, while preserving provenance and the original student-derived content. Do not overwrite the original Core Review or attribute reference ideas to the student.

## Readback requirement

The note is for reading; structured fields remain in Sheets. Do not duplicate every database column as prose.

After create/update, read the note back before its URL is used to archive the Problem. Verify that the relevant `attempt_id` block exists and that older Attempt blocks are still present. Write the observed `note_url` back to `Problem_Index` and the relevant finalized `Attempts` rows.