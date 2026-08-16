# IMO Tutor Project-only Setup Check

Use this file to configure and validate a clean ChatGPT Project without installing the `imo-tutor` Skill.

## Runtime upload list — exactly 18 Project files

### Workflows

1. `problem-intake.md`
2. `no-spoiler-analysis.md`
3. `hint-manager.md`
4. `solution-review.md`
5. `solution-compare.md`
6. `note-compiler.md`
7. `drive-archive.md`
8. `problem-retrieval.md`
9. `first-round-routing.md`

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

PR1 adds only first-round routing/isolation. The Notion database schema and Notion storage self-check are deferred to the later persistence PR. Until then, first-round work must never fall back to the second-round Drive / Sheets database.

## Static Project self-check prompt

Run this in a temporary Chat inside the Project before connecting durable student data:

```text
这是 IMO Tutor Project-only 安装自检。

不要开始任何数学题。
不要创建 Problem。
不要创建 Attempt。
不要修改 Google Drive。
不要修改 Notion。
不要根据记忆猜测缺失文件。

请实际检查当前 Project sources，并逐个读取，而不是只根据文件名推断。

必须存在以下 18 个 runtime 文件：
problem-intake.md
no-spoiler-analysis.md
hint-manager.md
solution-review.md
solution-compare.md
note-compiler.md
drive-archive.md
problem-retrieval.md
first-round-routing.md
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
F. SOLUTION_LOCKED / no-spoiler rule
G. transient Attempt 在 finalize 前不能写 durable Attempts row
H. ARCHIVED 必须要求 durable Note + Sheet readback
I. exact/fuzzy retrieval 的基本路由
J. Redo 必须复用 Problem 并创建下一 Attempt
K. Redo finalize 前禁止读取旧 Attempt solution information
L. Sheet 中 array-valued fields 必须使用 compact JSON array 序列化
M. first-round routing：明确的一试请求必须读取 first-round-routing.md
N. first-round isolation：一试不得分配 Pxxxxxx / Attempt ID，不得写 Problem_Index / Attempts，不得创建二试 Drive Problem folder
O. routing precedence：显式 Pxxxxxx/Redo 归二试；显式一试意图优先于旧 Chat 中隐式 active Attempt；未显式切换的一般 hint follow-up 仍归当前二试 Attempt
P. persistence split：二试 durable source = Google Drive / Sheets；一试 durable source = Notion；两者不得互相 fallback

最后只输出一个安装报告：

PROJECT FILES: PASS / FAIL
FILES FOUND: n/18

CONTRACTS:
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
First-round routing: PASS/FAIL
First-round isolation: PASS/FAIL
Routing precedence: PASS/FAIL
Persistence split: PASS/FAIL

UI-ONLY CHECKS:
Project-only memory: UNKNOWN unless you can directly verify it
Installed imo-tutor Skill absent: UNKNOWN unless you can directly verify it
Notion connection: UNKNOWN unless you can directly verify it

FINAL:
READY / NOT READY

对于无法直接验证的内容必须写 UNKNOWN，禁止为了让安装通过而猜测 PASS。
```

## Existing proof / second-round storage self-check prompt

After connecting Google Drive and initializing the Sheet headers from `Problem_Index.csv` and `Attempts.csv`, run:

```text
继续 IMO Tutor Project-only 二试存储自检。

这不是正式题目。
不要创建 Problem 或 Attempt。
不要向 Problem_Index 或 Attempts 写正式数据。
不要写入 Notion。

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

FINAL STORAGE STATUS:
READY / NOT READY
```

## Manual UI checks

The model must not guess these. Confirm manually before formal testing:

- the new Project was created with Project-only memory when that option is available;
- the `imo-tutor` Personal Skill is not participating in this Project-only test;
- Notion is connected before PR2 persistence validation;
- `00｜使用说明` and `01｜题库检索` are created only after setup checks pass.
