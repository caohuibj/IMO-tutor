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
5. Update `hint_max` and `hint_count` on the transient active attempt. If a durable `Attempts` row already exists because work was submitted, update its hint metadata as well.
6. If the student explicitly gives up before submitting any solution, finalize the active attempt as `verdict=UNSOLVED` and `result_bucket=UNSOLVED` using the current hint metadata.
7. If the student requests H6 before submitting any solution, first record the H6 release (`hint_max=H6` and the corresponding hint count), finalize the attempt as `UNSOLVED`, then release the complete solution. Do not overwrite an existing submitted-attempt verdict with `UNSOLVED`.
