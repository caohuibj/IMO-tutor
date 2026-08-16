# First-Round Routing & Isolation

Use this Project workflow only to classify and isolate Chinese High School Mathematics League first-round (`高联一试`) training from the existing proof / second-round lifecycle.

This workflow is loaded as a Project source. Do not depend on an installed `imo-tutor` Skill.

PR1 establishes routing and storage boundaries only. It does not yet define the Notion database schema, grading workflow, or longitudinal Review synthesis logic.

## System boundary

There are two independent persistence domains inside the same Project-based runtime.

### First round

- Durable source of truth: **Notion**.
- Raw training types:
  - `FILL_SET`: one grouped first-round fill-in set, typically the 8 fill-ins from a paper;
  - `CALC_SET`: one grouped first-round calculation/solution set, typically the 3 calculation problems from a paper;
  - `PRACTICE`: one problem or one grouped supplementary practice set targeting a curriculum topic or skill.
- `FULL_EXAM` is an input classification only. A later workflow may split one complete 8+3 paper into one `FILL_SET` and one `CALC_SET` durable record.
- First-round Review / reflection belongs to the first-round subsystem.
- Do not create proof-system Problem or Attempt identities for first-round work.
- Do not apply proof-system H0-H6 / `SOLUTION_LOCKED` merely because the work is mathematical. First-round coaching and grading rules are defined by first-round workflows.

### Existing proof / second-round system

- Durable source of truth: **Google Drive + Google Sheets**.
- Continue using the existing `Pxxxxxx` Problem identity, `Pxxxxxx-Axx` Attempt identity, `Problem_Index`, `Attempts`, Problem folders, notes, H0-H6 hint workflow, redo isolation, review, retrieval, and archive workflows without modification.

## Routing rules

Route to `FIRST_ROUND` when either condition holds:

1. the user explicitly identifies the work as `高联一试`, `一试填空`, `一试计算`, `一试练习`, `一试整卷`, or first-round Review/reflection; or
2. the current chat is already clearly established as first-round work and the user supplies the next fill set, calculation set, practice, or first-round Review request.

Within `FIRST_ROUND`, classify the input as `FILL_SET`, `CALC_SET`, `PRACTICE`, or `FULL_EXAM` when possible.

Do **not** infer first-round mode merely because a problem uses high-school curriculum mathematics. If first-round context is absent, preserve the existing proof / second-round routing behavior.

## Routing precedence

Apply these rules in order:

1. **Explicit stored Problem identity wins.** An explicit `Pxxxxxx`, especially `重做 P000237`, always belongs to the existing proof / second-round system.
2. **Explicit first-round intent wins over implicit chat state.** If the user explicitly says `高联一试`, `一试填空`, `一试计算`, `一试练习`, `一试整卷`, or first-round Review/reflection, route to `FIRST_ROUND` even if the same chat previously contained a proof / second-round Attempt.
3. **Implicit proof follow-ups stay with the active proof Attempt.** A hint request, submitted proof, reference-solution comparison, or archive request that clearly refers to the active proof / second-round Problem and does not explicitly switch to first-round remains in the existing system.
4. Usage/setup questions do not create records in either system unless the user explicitly asks to persist configuration.
5. Established first-round context routes subsequent first-round fill sets, calculation sets, practice, or Review requests to `FIRST_ROUND`.
6. Ambiguous standalone new problems keep the existing proof / second-round new-problem routing; do not silently reclassify them as first-round.

## Hard isolation invariants

For every `FIRST_ROUND` request:

- never allocate a `Pxxxxxx` Problem ID;
- never allocate a `Pxxxxxx-Axx` Attempt ID;
- never read or write `Problem_Index` for first-round persistence;
- never read or write `Attempts` for first-round persistence;
- never create an `IMO Tutor Data/<problem_id>` Drive folder;
- never invoke the existing Problem note / `drive-archive.md` path for first-round persistence;
- never write first-round records into the existing proof / second-round Google Drive / Google Sheets sequence;
- never silently reuse proof-system schemas, hint levels, verdicts, or 0-7 proof scoring for first-round records;
- never use one persistence domain as a fallback for the other.

If Notion persistence required by a first-round request is not yet available, **do not fall back to Google Drive or Google Sheets**. Keep the current analysis transient and state clearly that first-round durable persistence is incomplete.

For every existing proof / second-round request:

- keep the current `Pxxxxxx` allocation and redo rules unchanged;
- keep H0-H6 and `SOLUTION_LOCKED` unchanged;
- keep Google Drive / Google Sheets as the durable source of truth;
- do not create or update first-round Notion records merely because a problem involves school-level mathematics.

## PR1 acceptance checks

The following classifications must hold:

- `新的一题 IMO 2024 P2` -> existing proof / second-round workflow.
- `重做 P000237` -> existing redo workflow.
- while a proof Attempt is active, `高联一试填空复盘` -> `FIRST_ROUND / FILL_SET`; explicit system switch wins over the implicit active Attempt.
- while a proof Attempt is active, `再给一点提示` -> existing proof / second-round hint workflow.
- `高联一试计算题复盘` -> `FIRST_ROUND / CALC_SET`; no Drive/Sheets write.
- `今天做了解析几何一试专项 6 题` -> `FIRST_ROUND / PRACTICE`; one grouped training unit, not six Problems.
- a complete first-round 8+3 upload -> `FIRST_ROUND / FULL_EXAM`; no `Pxxxxxx` allocation.

PR1 must not modify the behavior or schemas of the existing proof / second-round workflows.
