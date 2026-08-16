# IMO Tutor Project-only Setup Check

Use this file to configure and validate a clean ChatGPT Project without installing the `imo-tutor` Skill.

This Project hosts two routed subsystems:

- existing proof / second-round -> Google Drive + Google Sheets;
- Chinese High School Mathematics League first round -> Notion.

PR1 validates first-round routing and storage isolation only. Notion database/schema provisioning is validated in the later first-round persistence PR.

## Runtime upload list — exactly 18 Project files

### Workflows

1. `first-round-routing.md`
2. `problem-intake.md`
3. `no-spoiler-analysis.md`
4. `hint-manager.md`
5. `solution-review.md`
6. `solution-compare.md`
7. `note-compiler.md`
8. `drive-archive.md`
9. `problem-retrieval.md`

### References

10. `difficulty.json`
11. `domains.json`
12. `errors.json`
13. `concepts.json`
14. `methods.json`
15. `problem.schema.json`
16. `attempt.schema.json`
17. `search-query.schema.json`
18. `math-note-template.md`

`Problem_Index.csv` and `Attempts.csv` are setup assets for initializing Google Sheets headers. They are not required as Project runtime sources.

Copy the full contents of `project-only/PROJECT_INSTRUCTIONS.md` into the ChatGPT Project Instructions field.

## Static Project self-check prompt

Run this in a temporary Chat inside the Project before connecting durable student data:

```text
这是 IMO Tutor Project-only 安装自检。

不要开始任何数学题。
不要创建 Problem。
不要创建 Attempt。
不要修改 Google Drive、Google Sheets 或 Notion。
不要根据记忆猜测缺失文件。

请实际检查当前 Project sources，并逐个读取，而不是只根据文件名推断。

必须存在以下 18 个 runtime 文件：
first-round-routing.md
problem-intake.md
no-spoiler-analysis.md
hint-manager.md
solution-review.md
solution-compare.md
note-compiler.md
drive-archive.md
problem-retrieval.md
difficulty.json
domains.json
errors.json
concepts.json
methods.json
problem.schema.json
attempt.schema.json
search-query.schema.json
math-note-template.md

然后检查以下合同：
A. Problem ID 格式
B. Attempt ID 格式
C. H0-H6 hint levels
D. canonical domains
E. difficulty scale 必须是 1.0-10.0，步长 0.5；IMO/Shortlist baseline 只是校准锚点，不是下界
F. SOLUTION_LOCKED / no-spoiler rule 仅属于 proof / 二试 workflow
G. transient Attempt 在 finalize 前不能写 durable Attempts row
H. ARCHIVED 必须要求 durable Note + Sheet readback
I. exact/fuzzy retrieval 的基本路由
J. Redo 必须复用 Problem 并创建下一 Attempt
K. Redo finalize 前禁止读取旧 Attempt solution information
L. Sheet 中 array-valued fields 必须使用 compact JSON array 序列化
M. 明确的一试意图必须路由到 first-round-routing.md
N. 一试 raw training type 只能是 FILL_SET / CALC_SET / PRACTICE；FULL_EXAM 只能作为输入分类
O. 一试不得创建 Pxxxxxx / Attempt，不得写 Problem_Index / Attempts，不得走 proof Drive folder / Note archive
P. 明确的一试意图必须优先于旧 active proof Attempt 的隐式上下文
Q. Notion 不可用时不得 fallback 到 Google Drive / Google Sheets
R. 一试不得自动继承 H0-H6 / SOLUTION_LOCKED / 0-7 proof scoring

最后只输出一个安装报告：

PROJECT FILES: PASS / FAIL
FILES FOUND: n/18

PROOF / SECOND-ROUND CONTRACTS:
Problem ID: PASS/FAIL
Attempt ID: PASS/FAIL
Hints: PASS/FAIL
Domains: PASS/FAIL
Difficulty: PASS/FAIL
No spoiler: PASS/FAIL
Attempt lifecycle: PASS/FAIL
Archive/readback: PASS/FAIL
Retrieval: PASS/FAIL
Redo: PASS/FAIL
Redo isolation: PASS/FAIL
Sheet array serialization: PASS/FAIL

FIRST-ROUND CONTRACTS:
Routing file: PASS/FAIL
Training classifications: PASS/FAIL
Explicit switch precedence: PASS/FAIL
No proof IDs: PASS/FAIL
Storage isolation: PASS/FAIL
No Drive/Sheets fallback: PASS/FAIL
Proof-hint isolation: PASS/FAIL
Notion persistence schema: DEFERRED TO PR2

UI-ONLY CHECKS:
Project-only memory: UNKNOWN unless you can directly verify it
Installed imo-tutor Skill absent: UNKNOWN unless you can directly verify it
Notion connection/write capability: UNKNOWN unless you can directly verify it

FINAL:
READY FOR PR1 ROUTING / NOT READY

对于无法直接验证的内容必须写 UNKNOWN，禁止为了让安装通过而猜测 PASS。
```

## Proof / second-round storage self-check prompt

After connecting Google Drive and initializing the Sheet headers from `Problem_Index.csv` and `Attempts.csv`, run:

```text
继续 IMO Tutor Project-only 安装自检：只检查 proof / 二试持久层。

这不是正式题目。
不要创建 Problem 或 Attempt。
不要向 Problem_Index 或 Attempts 写正式数据。
不要创建一试 Notion 记录。

请使用 Google Drive / Sheets 实际完成以下检查：

1. 找到 Drive folder：IMO Tutor Data
2. 找到 Google Sheet：IMO Learning DB
3. 确认包含两个 tab：Problem_Index、Attempts
4. 读取 Problem_Index 第一行 header，并与 problem.schema.json properties 按字段和顺序比较
5. 读取 Attempts 第一行 header，并与 attempt.schema.json properties 按字段和顺序比较
6. 确认两个 tab 当前都没有正式数据行
7. 如果写操作可用，创建临时文件 _IMO_TUTOR_SETUP_PROBE，写入 IMO_TUTOR_PROJECT_ONLY_WRITE_TEST，重新读取确认完全一致；如果支持删除则删除

不要因为可以读取就推断可以写入。

输出：
DRIVE:
Folder found: PASS/FAIL
Sheet found: PASS/FAIL
Problem_Index tab: PASS/FAIL
Attempts tab: PASS/FAIL

SCHEMA:
Problem_Index header parity: PASS/FAIL
Attempts header parity: PASS/FAIL
Initial DB empty: PASS/FAIL

WRITE TEST:
Create: PASS/FAIL/UNAVAILABLE
Readback: PASS/FAIL/UNAVAILABLE
Cleanup: PASS/FAIL/MANUAL REQUIRED

FINAL PROOF STORAGE STATUS:
READY / NOT READY
```

## First-round persistence status in PR1

PR1 does not provision or validate the Notion databases. It only requires that:

- first-round durable storage is Notion;
- first-round work never falls back to proof-system Drive / Sheets;
- inability to persist to Notion is reported as incomplete persistence.

Notion database creation, schema validation, relation validation, and write/readback acceptance belong to PR2.

## Manual UI checks

The model must not guess these. Confirm manually before formal testing:

- the Project was created with Project-only memory when that option is available;
- the `imo-tutor` Personal Skill is not participating in this Project-only test;
- `00｜使用说明` and `01｜题库检索` are created only after setup checks pass;
- Notion connectivity is checked separately when PR2 is implemented.
