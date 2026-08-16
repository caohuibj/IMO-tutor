# IMO Tutor Project-only Setup Check

Use this file to configure and validate a clean ChatGPT Project without installing the `imo-tutor` Skill.

## Runtime upload list — exactly 19 Project files

### Workflows

1. `problem-intake.md`
2. `no-spoiler-analysis.md`
3. `hint-manager.md`
4. `solution-review.md`
5. `solution-compare.md`
6. `note-compiler.md`
7. `drive-archive.md`
8. `problem-retrieval.md`

### References and setup contracts

9. `difficulty.json`
10. `domains.json`
11. `errors.json`
12. `concepts.json`
13. `methods.json`
14. `problem.schema.json`
15. `attempt.schema.json`
16. `search-query.schema.json`
17. `math-note-template.md`
18. `Problem_Index.csv`
19. `Attempts.csv`

The two CSV files remain Project runtime sources in this baseline because the current `drive-archive.md` explicitly uses the bundled CSV templates as the Sheet column contract. Removing that runtime dependency is a separate change and must not be bundled into the Project-only deployment PR.

Copy the full contents of `project-only/PROJECT_INSTRUCTIONS.md` into the ChatGPT Project Instructions field.

## Static Project self-check prompt

Run this in a temporary Chat inside the Project before connecting durable student data:

```text
这是 IMO Tutor Project-only 安装自检。

不要开始任何数学题。
不要创建 Problem。
不要创建 Attempt。
不要修改 Google Drive。
不要根据记忆猜测缺失文件。

请实际检查当前 Project sources，并逐个读取，而不是只根据文件名推断。

必须存在以下 19 个 runtime 文件：
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
Problem_Index.csv
Attempts.csv

然后检查以下合同：
A. Problem ID 格式
B. Attempt ID 格式
C. H0-H6 hint levels
D. canonical domains
E. difficulty scale 必须是 1.0-10.0，步长 0.5
F. SOLUTION_LOCKED / no-spoiler rule
G. transient Attempt 在 finalize 前不能写 durable Attempts row
H. ARCHIVED 必须要求 durable Note + Sheet readback
I. exact/fuzzy retrieval 的基本路由
J. Redo 必须复用 Problem 并创建下一 Attempt
K. Redo finalize 前禁止读取旧 Attempt solution information
L. drive-archive.md 与两个 CSV template 的 runtime contract 一致

最后只输出一个安装报告：

PROJECT FILES: PASS / FAIL
FILES FOUND: n/19

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
CSV runtime contract: PASS/FAIL

UI-ONLY CHECKS:
Project-only memory: UNKNOWN unless you can directly verify it
Installed imo-tutor Skill absent: UNKNOWN unless you can directly verify it

FINAL:
READY / NOT READY

对于无法直接验证的内容必须写 UNKNOWN，禁止为了让安装通过而猜测 PASS。
```

## Storage self-check prompt

After connecting Google Drive and initializing the Sheet headers from `Problem_Index.csv` and `Attempts.csv`, run:

```text
继续 IMO Tutor Project-only 安装自检。

这不是正式题目。
不要创建 Problem 或 Attempt。
不要向 Problem_Index 或 Attempts 写正式数据。

请使用 Google Drive / Sheets 实际完成以下检查：

1. 找到 Drive folder：IMO Tutor Data
2. 找到 Google Sheet：IMO Learning DB
3. 确认包含两个 tab：Problem_Index、Attempts
4. 读取 Problem_Index 第一行 header，并与 Problem_Index.csv 比较
5. 读取 Attempts 第一行 header，并与 Attempts.csv 比较
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
- `00｜使用说明` and `01｜题库检索` are created only after setup checks pass.
