# IMO Tutor

一个面向单个学生、可安装、可迁移、可长期复用的 IMO 证明题训练工作流。

IMO Tutor 由一个 ChatGPT Skill、Project Instructions 和学生自己的 Google Drive / Google Sheets 学习数据库组成。Chat 是临时工作台；Google Drive / Sheets 是长期记录的 source of truth。

## v1.0 目标

一个从未参与项目开发的新学生，只依赖 GitHub Release、README 和 `project/SETUP.md`，能够：

1. 下载并安装 `imo-tutor` Skill；
2. 建立自己的 ChatGPT Project；
3. 连接自己的 Google Drive 并初始化 `IMO Learning DB`；
4. 持续完成 `新题 → 作答 → 批改 → 归档 → 检索 → 重做`；
5. 在更换 ChatGPT Project 时继续使用同一份 Drive / Sheets 数据。

每个学生使用自己的私有 Google Drive。公共仓库只包含 workflow、schema、文档和测试，不包含学生解答、私人 Drive ID 或 credentials。

## 支持环境

v1.0 采用 **capability-gated** 支持方式，不假设所有 ChatGPT plan / workspace 都具有相同功能。安装前先确认：

- ChatGPT 中存在 `Plugins → Skills → Create → Upload from your computer`，并允许你上传 Personal Skill；
- 你的 workspace 管理策略没有禁止 Skill upload / install；
- 可以创建和使用 ChatGPT Project；
- 已连接 Google Drive app，并且 Google Drive / Docs / Sheets 的写操作可用；
- 你有权限在自己的 Drive 中创建/更新文件和 Google Sheet。

如果缺少上述任一能力，当前环境不属于 IMO Tutor v1.0 的支持范围；不要继续初始化数据库。Personal Skills、Google app actions 和 workspace 权限可能随 ChatGPT plan / 管理策略变化，具体以 OpenAI 当前产品界面与官方帮助为准。

## 核心体验

- **No spoiler by default**：新题进入 `SOLUTION_LOCKED`，除非学生主动请求提示，否则不提前泄露关键引理、构造或完整解法。
- **Progressive hints**：按 `H1–H6` 逐级给提示。
- **Proof review**：检查正确性、严谨性、策略和表达，保留手写原图并转写 Markdown/LaTeX。
- **Durable archive**：题目、Attempt、Note 和检索字段写入学生自己的 Google Drive / Sheets。
- **Retrieval**：支持 `P00237`、`最近做错的2道几何题` 等精确/模糊检索。
- **Redo**：`重做 P00237` 创建新的 Attempt，提交前隔离旧解答；完成后比较例如 `52 min + H3 + 3/7` 与 `24 min + H0 + 7/7`。

## 安装

推荐从 GitHub Release 下载 `imo-tutor-v<version>.zip`，不要从仓库中手工挑选 Skill 文件。

完整步骤见 [`project/SETUP.md`](project/SETUP.md)。安装完成后，建议继续阅读：

- [`project/PROJECT_GUIDE.md`](project/PROJECT_GUIDE.md)：Project、左侧对话、Chat 生命周期和迁移规则；
- [`project/USER_GUIDE.md`](project/USER_GUIDE.md)：日常做题、提示、批改、归档、检索和重做用法；
- [`project/PROJECT_INSTRUCTIONS.md`](project/PROJECT_INSTRUCTIONS.md)：复制到 ChatGPT Project Instructions 的运行规则。

## 推荐的 Project 对话结构

安装后只长期保留两个通用对话，并把它们 Pin 到 sidebar；其他题目一题一 Chat，完成即归档。

```text
IMO Tutor
├── 00｜使用说明        ← Pin；只问怎么使用系统
├── 01｜题库检索        ← Pin；只查历史题和选择重做题
└── 当前题目 Chat       ← 一题一 Chat；完成并 ARCHIVED 后归档
```

正式 redo 建议在新的工作 Chat 中输入 `重做 Pxxxxx`，不要在长期的 `01｜题库检索` 中继续做题。

## 数据布局

默认使用：

```text
Google Drive
└── IMO Tutor Data/
    ├── P000001/
    │   ├── P000001-problem-01.jpg
    │   ├── P000001-A01-solution-01.jpg
    │   └── P000001 Note
    └── ...

Google Sheets: IMO Learning DB
├── Problem_Index
└── Attempts
```

旧 Chat 不是长期数据库。历史检索和重做必须读取 Drive / Sheets durable records。

## Roadmap

| Version | Scope |
|---|---|
| v0.1 | 核心 Skill / schema / workflow 骨架 |
| v0.2 | Google Drive / Sheets 持久化闭环 |
| v0.3 | 教学质量校准：no-spoiler、hints、批改、difficulty/tags |
| v0.4 | 检索 + 重做 + 多 Attempt |
| v1.0 | 单个学生可独立安装、迁移并长期使用 |

### v1.x 明确不做

IMO Tutor v1.x 是 **single-user learning tool**，不是 classroom management product。以下能力不在 roadmap 中：

- teacher profile；
- 班级管理；
- 共享学生数据库；
- 教师 dashboard；
- 学生权限系统；
- 多人协作 Project；
- 教师统计后台。

如果未来开发这些能力，应作为独立产品方向评估，而不是 v1.x 的自然扩展。

## v1.0 验收

一个未参与开发的新学生，仅依赖 Release + README + SETUP，应能独立完成：

```text
安装 Skill
→ 创建 Project
→ 连接并初始化自己的 Drive / Sheets
→ 新题
→ 作答
→ 批改
→ 归档
→ 新 Chat 检索该题
→ 新 Chat 重做该题
→ 产生 A02 并看到 Attempt 对比
```

这条 fresh-student acceptance test 通过，才发布最终 `v1.0.0`。

## Development

运行 deterministic contract tests：

```bash
python -m unittest discover -s tests
```

Behavioral eval cases 位于 `evals/`。发布流程由 `.github/workflows/release.yml` 负责校验版本并生成可安装 Skill zip。
