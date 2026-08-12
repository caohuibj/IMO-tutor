# Solution Review

Use when the student submits handwritten images or solution text.

## Preserve and normalize

1. Preserve references to all original solution images. If the runtime exposes an uploadable file reference, archive the originals to the problem/attempt Drive folder.
2. Transcribe the mathematical argument to Markdown/LaTeX. Do not silently repair mathematical mistakes in the transcription.
3. Mark any uncertain reading explicitly and resolve it from the image/context before using it as evidence for a verdict.

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

## Output

Give:

1. verdict and estimated score;
2. first gap, with the exact inference that fails or needs justification;
3. what remains valid after that point;
4. strategy assessment;
5. writing/rigor assessment;
6. concise repair advice without replacing the student's proof unless requested;
7. one short `proof compression`: the 2–4 essential mathematical moves in the student's approach.

Update the active Attempt record after review.
