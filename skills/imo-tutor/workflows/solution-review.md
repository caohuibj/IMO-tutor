# Solution Review

Use when the student submits handwritten images or solution text.

## Attempt completion semantics

A solution/photo/text submission is a **checkpoint submission**, not automatically the end of the Attempt.

The active Attempt remains open across one or more checkpoint submissions. The student will explicitly end the normal Attempt by saying exactly `此题完成` (or by an unmistakable message that contains that explicit completion phrase).

Hard rule:

- Before `此题完成`: review only the current mathematical work using **Module 1 — Core Review**. Do not run Historical Transfer, Mathematical Extraction, Higher Mathematics Bridge, Reinforcement Problems, or Visual Model.
- On `此题完成`: finalize the active Attempt exactly once, then run the complete six-module feedback workflow.
- Do not infer completion merely because a submitted proof appears complete, correct, or polished.

If `此题完成` arrives together with a new photo/text submission, incorporate that submission first, perform the final Core Review, then finalize and run Modules 2–6.

If `此题完成` arrives without new mathematical content, finalize using the latest accumulated coherent solution state for the active Attempt.

Explicit give-up and H6 remain separate attempt-ending paths under `hint-manager.md`; they do not by themselves activate Modules 2–6. The six-module extension is gated by the explicit `此题完成` trigger.

## Preserve and normalize checkpoint work

1. Use the active `problem_id` and `attempt_id`; a redo reuses the existing Problem folder and never creates a new Problem row.
2. Preserve all original solution images across checkpoint submissions. If the runtime exposes uploadable originals, they may be archived incrementally in the Problem folder as `<attempt_id>-solution-01.<ext>`, `<attempt_id>-solution-02.<ext>`, ... without creating an `Attempts` row yet.
3. Transcribe each checkpoint as needed for review. Do not silently repair mathematical mistakes.
4. Treat explicit later corrections as superseding the corrected portion of earlier work; otherwise preserve non-overlapping pages/steps cumulatively.
5. Before finalization, keep the current coherent solution transcription and provisional review state transient. Do not write an incomplete `Attempts` row.
6. At finalization: Store the complete transcription in `Attempts.solution_transcription`; do not create a separate transcription file.
7. Mark any uncertain reading explicitly and resolve it from the image/context before using it as evidence for a review judgment.

## Mathematical review

Check the proof in order and find the **first mathematically unacceptable step**. Then determine whether later work depends on it.

Use one verdict vocabulary for reviews:

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

Before `此题完成`, these judgments are **provisional checkpoint reviews** and may change after later submissions. Only the final review is persisted as the Attempt verdict/result.

## Review dimensions

Evaluate:

- correctness;
- completeness/case coverage;
- rigor;
- strategy;
- exposition/notation;
- generalization or reusable insight.

Estimate an IMO-style score `0–7` only as an estimate unless an official marking scheme is available. Before completion, label it as provisional when useful.

## Error diagnosis

Tag errors with controlled values from `errors.json`. Prefer the cause over the symptom. Bind knowledge/technique/observation errors to a `concept_tag` or `method_tag` when possible.

Important distinction:

- student does not know a theorem -> `KNOWLEDGE`;
- student knows it but applies it incorrectly -> `TECHNIQUE`;
- student knows and can apply it but fails to notice it is relevant -> `OBSERVATION`.

## Retrieval fields for the finalized Attempt

Only at finalization, make the attempt-level retrieval fields describe what happened in **this student's completed Attempt**, not merely the canonical problem solution:

- `method_tags`: controlled methods actually used by the student when identifiable, e.g. `M.GEO.Inversion` if the submitted proof used inversion;
- `error_tags`: controlled diagnosed errors from this attempt;
- `search_text`: a short retrieval-oriented summary of the student's approach and blocker using ordinary mathematical language, without fabricating details;
- domain/difficulty/source fields remain snapshots of the Problem metadata.

Canonical/likely problem methods remain problem metadata; `Attempts.method_tags` records the student's actual approach for retrieval.

## Finalization on `此题完成`

When the explicit completion trigger is received:

1. assemble the latest coherent student solution from all checkpoint submissions, respecting explicit corrections and preserving mathematical mistakes;
2. perform the final Core Review on that completed state;
3. set `submitted_at` to the completion time;
4. materialize the active Attempt exactly once in `Attempts`, including archived solution-image URLs/status, final `solution_transcription`, final verdict/result/score/gap/error fields, timing, hint metadata, and attempt-level retrieval fields;
5. update the existing `Problem_Index` summary row;
6. mark the current Attempt finalized;
7. continue to `post-review-transfer.md` for Modules 2–6.

Do not create a second durable Attempt row for multiple checkpoint submissions within the same Attempt.


## Finalization on give-up or H6 without `此题完成`

Give-up/H6 is an attempt-ending path but **not** the six-module completion trigger. Finalize the current Attempt once, then stop after the Core Review / permitted H6 response.

Use the latest coherent checkpoint state available **before** any H6 solution is revealed.

- If there has been no substantive student mathematical work, finalize as `verdict=UNSOLVED`, `result_bucket=UNSOLVED`, with empty/null solution fields as appropriate.
- If substantive checkpoint work exists, preserve and transcribe it, perform a final Core Review, and assign `verdict`, `result_bucket`, estimated score, `first_gap`, and error/method fields from the actual student work. Do **not** force `UNSOLVED` merely because the student gives up or requests H6.
- For H6, record the H6 release in hint metadata and finalize the student work **before** releasing the complete solution, so teacher-provided mathematics cannot contaminate the student's transcription or verdict.
- Neither give-up nor H6 activates Historical Transfer, Mathematical Extraction, Higher Mathematics Bridge, Reinforcement Problems, or Visual Model.
- Once an Attempt has ended through give-up/H6, a later `此题完成` message does not retroactively convert that ended Attempt into the six-module completion path. Do not automatically backfill Modules 2–6.

## Module 1 output — Core Review

For every checkpoint submission, give only the normal review layer:

1. provisional/final verdict and estimated score as appropriate;
2. first gap, with the exact inference that fails or needs justification;
3. what remains valid after that point;
4. strategy assessment;
5. writing/rigor assessment;
6. concise repair advice without replacing the student's proof unless requested;
7. one short `proof compression`: the 2–4 essential mathematical moves in the student's approach.

Before `此题完成`, stop here. Do not add any of today's post-review extension modules.

## Post-review handoff

Run the complete extension only when the active Attempt was completed through the explicit `此题完成` trigger.

The complete feedback then has six modules:

1. Core Review — this file;
2. Historical Transfer;
3. Mathematical Extraction;
4. Higher Mathematics Bridge;
5. Reinforcement Problems;
6. Visual Model — optional when visualization has clear learning value.

Do not let later modules silently revise the mathematical verdict. If a contradiction is discovered, state the correction explicitly.