# Problem Intake

Use for a new problem supplied as an image, screenshot, or text.

## Steps

1. Read and normalize the statement. Preserve mathematical quantifiers, domains, equality/inequality signs, and geometric incidence conditions.
2. Decide whether this is genuinely a new problem before allocating an ID:
   - explicit existing `problem_id` -> reuse that Problem;
   - exact existing `source_id` -> reuse that Problem;
   - exact normalized-statement match -> reuse that Problem;
   - otherwise create a new Problem.
   Do not use fuzzy/semantic deduplication in v0.2.
3. For a genuinely new Problem, allocate `P000001`, `P000002`, ... from `Problem_Index`: read existing `problem_id` values, take the largest numeric suffix, add 1, and zero-pad to six digits. If there are no problem rows, start at `P000001`. Do not reuse IDs.
4. Create the Drive folder named exactly `<problem_id>` under the configured root. For supplied problem images, archive each materializable original as `<problem_id>-problem-01.<ext>`, `<problem_id>-problem-02.<ext>`, ... before the first `Problem_Index` write. If the runtime cannot expose uploadable bytes/file references, do not claim the image is archived and treat the persistence loop as incomplete.
5. Record source metadata when known: competition, year, official number, shortlist code, region, and type.
6. Classify the primary IMO domain: `ALG`, `CMB`, `GEO`, or `NT`. Add a secondary domain only when materially useful.
7. Assign controlled `concept_tags` and `method_tags`. Method tags may include likely solution methods, but do not reveal them to the student if they would spoil the problem.
8. Rate global difficulty on the AoPS-style scale in `difficulty.json`, using 0.5 increments. Official problem position is a prior, not a hard constraint.
9. Perform enough internal analysis to build a valid solution route and hint ladder. Keep decisive information locked.
10. Append exactly one durable `Problem_Index` row for a new Problem with statement, metadata, `folder_url`, archived `problem_image_url` when available, and `status=ANALYZED`. Reused Problems must update the existing row rather than append another Problem row.
11. Initialize a transient active attempt with `attempt_no = attempt_count + 1`, `attempt_id = <problem_id>-A<attempt_no:02d>`, `hint_max=H0`, and `hint_count=0`. Do not write a durable `Attempts` row until the student submits work or explicitly ends the attempt without a submission.

## Student-visible output at H0

Show only:

- problem ID;
- normalized statement only if useful for confirming OCR/reading;
- primary domain;
- difficulty rating/range and short calibration;
- broad prerequisite knowledge that does not reveal the decisive route;
- likely general risk (e.g. proof rigor, case handling), only if non-spoiling;
- `Hint level: H0` and that progressive hints are available.

Do not show the candidate solution, key lemma, decisive construction, key substitution, or final result derivation.
