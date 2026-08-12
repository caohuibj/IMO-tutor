# Problem Intake

Use for a new problem supplied as an image, screenshot, or text.

## Steps

1. Read and normalize the statement. Preserve mathematical quantifiers, domains, equality/inequality signs, and geometric incidence conditions.
2. Decide whether this is genuinely a new problem. If it is an existing problem ID or clearly a redo, route to retrieval instead.
3. Allocate the next internal ID in the form `P000001`, `P000002`, ... by consulting `Problem_Index`. Do not reuse IDs.
4. Record source metadata when known: competition, year, official number, shortlist code, region, and type.
5. Classify the primary IMO domain: `ALG`, `CMB`, `GEO`, or `NT`. Add a secondary domain only when materially useful.
6. Assign controlled `concept_tags` and `method_tags`. Method tags may include likely solution methods, but do not reveal them to the student if they would spoil the problem.
7. Rate global difficulty on the AoPS-style scale in `difficulty.json`, using 0.5 increments. Official problem position is a prior, not a hard constraint.
8. Perform enough internal analysis to build a valid solution route and hint ladder. Keep decisive information locked.
9. Create/update the durable problem record immediately with `status=ANALYZED`.

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
