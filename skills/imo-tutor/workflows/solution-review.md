# Solution Review

Use when the student submits handwritten images or solution text.

## Preserve and normalize

1. Use the active `problem_id` and `attempt_id`; a redo reuses the existing Problem folder and never creates a new Problem row.
2. Preserve all original solution images. If the runtime exposes uploadable originals, archive them in the Problem folder as `<attempt_id>-solution-01.<ext>`, `<attempt_id>-solution-02.<ext>`, ...
3. Transcribe the mathematical argument to Markdown/LaTeX. Do not silently repair mathematical mistakes in the transcription.
4. Store the complete transcription in `Attempts.solution_transcription`; do not create a separate transcription file in v0.2.
5. Mark any uncertain reading explicitly and resolve it from the image/context before using it as evidence for a verdict.

## Mathematical review

Check the proof in order and find the **first mathematically unacceptable step**. Then determine whether later work depends on it.

Use one verdict:

- `FULLY_CORRECT`
- `MINOR_OMISSION`
- `INCOMPLETE`
- `RECOVERABLE_GAP`
- `MAJOR_GAP`
- `INCORRECT`
- `UNSOLVED`

Map to result buckets:

- `CORRECT`: FULLY_CORRECT, MINOR_OMISSION
- `PARTIAL`: INCOMPLETE, RECOVERABLE_GAP
- `INCORRECT`: MAJOR_GAP, INCORRECT
- `UNSOLVED`: UNSOLVED

## Review dimensions

Evaluate:

- correctness;
- completeness/case coverage;
- rigor;
- strategy;
- exposition/notation;
- generalization or reusable insight.

Estimate an IMO-style score `0–7` only as an estimate unless an official marking scheme is available.

## Error diagnosis

Tag errors with controlled values from `errors.json`. Prefer the cause over the symptom. Bind knowledge/technique/observation errors to a `concept_tag` or `method_tag` when possible.

Important distinction:

- student does not know a theorem -> `KNOWLEDGE`;
- student knows it but applies it incorrectly -> `TECHNIQUE`;
- student knows and can apply it but fails to notice it is relevant -> `OBSERVATION`.

## Persistence after review

Once `submitted_at`, `verdict`, and `result_bucket` are known, materialize the active Attempt exactly once in `Attempts`, including the preserved image URLs/status and `solution_transcription`. Then update the existing `Problem_Index` summary row. Do not create a new Problem for a second or later Attempt.

## Output

Give:

1. verdict and estimated score;
2. first gap, with the exact inference that fails or needs justification;
3. what remains valid after that point;
4. strategy assessment;
5. writing/rigor assessment;
6. concise repair advice without replacing the student's proof unless requested;
7. one short `proof compression`: the 2–4 essential mathematical moves in the student's approach.
