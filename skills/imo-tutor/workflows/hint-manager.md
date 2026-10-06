# Hint Manager

Use progressive disclosure. Record every released hint level on the current attempt.

## Levels

- `H0`: no hint.
- `H1`: one orientation question or weak directional cue; do not name the decisive method.
- `H2`: identify a useful structure/invariant/object class, but not the key lemma or full construction.
- `H3`: give a concrete intermediate goal or suggest the main method family.
- `H4`: give the key lemma or decisive construction, but not the complete proof chain.
- `H5`: give a near-complete proof skeleton with gaps the student must fill.
- `H6`: give a complete solution.

## Rules

1. Increase by one level when the user says only `再给一点`, `下一级`, or equivalent.
2. If the user explicitly asks for a level, release that level and mark all lower levels as effectively consumed.
3. Never silently jump levels because the student appears stuck.
4. Keep hints problem-specific, short, and cumulative.
5. Update `hint_max` and `hint_count` on the transient active Attempt. Checkpoint submissions do not create a durable `Attempts` row. Once an Attempt is finalized, do not continue its hint ladder or mutate its hint metadata except to correct a recording error.
6. If the student explicitly gives up and there has been **no substantive student solution work**, finalize the active Attempt as `verdict=UNSOLVED` and `result_bucket=UNSOLVED` using the current hint metadata.
7. If the student gives up **after one or more substantive checkpoint submissions**, finalize the latest coherent student work using `solution-review.md`: preserve/transcribe the work, assign the evidence-based verdict/result/score/gap, and do not force `UNSOLVED`. This ending path does not activate Modules 2–6.
8. If the student requests H6, first record the H6 release (`hint_max=H6` and the corresponding hint count). Finalize the current student work **before** revealing the H6 solution. With no substantive student work, use `UNSOLVED`; with substantive checkpoint work, use the evidence-based final Core Review. Then release the complete solution. H6 never activates Modules 2–6 by itself and must not overwrite a previously finalized verdict.