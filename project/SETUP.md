# Setup

本文件面向第一次安装 IMO Tutor 的学生。目标不是理解内部 schema，而是机械完成安装并跑通第一道题。

## 0. 准备

你需要：

- 一个可以创建 ChatGPT Project 并安装 Skill 的 ChatGPT 环境；
- 一个自己的 Google Drive；
- GitHub Release 中的 `imo-tutor-v<version>.zip`；
- 本仓库的 `project/PROJECT_INSTRUCTIONS.md`。

所有学习数据都保存在你自己的 Google Drive / Google Sheets 中，不需要共享给项目作者。

## 1. 安装 Skill

1. 打开最新的 GitHub Release。
2. 下载 `imo-tutor-v<version>.zip`。
3. 将这个 zip 作为一个 ChatGPT Skill 安装；不要重新打包内部文件。
4. 确认安装后的 Skill 名称为 `imo-tutor`。

Release zip 的预期结构是：

```text
imo-tutor/
├── SKILL.md
├── workflows/
└── references/
```

## 2. 创建 ChatGPT Project

1. 创建一个新的 ChatGPT Project，推荐名称：`IMO Tutor`。
2. 打开 `project/PROJECT_INSTRUCTIONS.md`。
3. 将其完整复制到该 Project 的 Project Instructions。
4. 确认 Project 中可以使用刚安装的 `imo-tutor` Skill。

不要把学生个人解答、Drive ID 或 credentials 写入 Project Instructions。

## 3. 连接 Google Drive

连接你自己的 Google Drive app / connector。

在 Drive 中创建：

```text
IMO Tutor Data/
```

再创建一个 Google Sheet：

```text
IMO Learning DB
```

在该 Sheet 中创建两个 tab：

```text
Problem_Index
Attempts
```

## 4. 初始化 Learning DB

不要自己设计列名。直接使用 Skill 中的两个 CSV header：

```text
skills/imo-tutor/references/Problem_Index.csv
skills/imo-tutor/references/Attempts.csv
```

分别把：

- `Problem_Index.csv` 第一行复制为 `Problem_Index` tab 的 header；
- `Attempts.csv` 第一行复制为 `Attempts` tab 的 header。

保持列名、顺序和大小写不变。

初始化完成后应满足：

```text
Google Drive
├── IMO Tutor Data/
└── IMO Learning DB
    ├── Problem_Index
    └── Attempts
```

## 5. 建立推荐的 Project 对话

在 IMO Tutor Project 中建立并长期保留两个通用 Chat：

### `00｜使用说明`

用途：只询问系统怎么使用，例如：

```text
怎么开始一道新题？
什么时候可以归档？
H1 到 H6 有什么区别？
怎么迁移到新的 Project？
```

不要在这里正式做题。

### `01｜题库检索`

用途：只查历史题，例如：

```text
P00237
最近做错的2道几何题
难度8以上用过H3提示的数论题
```

如果决定重做某题，推荐另开一个新的工作 Chat，再输入：

```text
重做 P00237
```

这两个通用 Chat 保持不归档，便于长期从 Project chat list / sidebar 找到。不要再创建长期的“新题”“批改”“Hints”通用 Chat；这些状态都应该留在具体题目的工作 Chat 中。

详细信息见 `project/PROJECT_GUIDE.md`。

## 6. 第一题 integration test

新建一个**新的工作 Chat**，不要使用 `00｜使用说明` 或 `01｜题库检索`。

### A. 新题

1. 上传一道题目图片或输入题面。
2. 确认系统分配一个 `Pxxxxxx`，例如 `P000001`。
3. 确认系统给出 domain / difficulty 等安全 metadata，但没有泄露完整解法。
4. 确认状态为 `SOLUTION_LOCKED`。
5. 检查 `Problem_Index`：应该只有这一道 Problem 的一行。
6. 如果题目来自图片，检查 `IMO Tutor Data/P000001/` 中是否保存原始题图。只有真实上传成功时才算通过。

### B. Hint

1. 输入 `H1`。
2. 再输入 `H2`。
3. 确认提示逐级增加，没有直接跳到完整解法。

### C. 提交与批改

1. 上传手写解答图片或提交解答文本。
2. 确认原始解答图在 runtime 可 materialize 时被保存到同一 Problem folder。
3. 确认生成 Markdown/LaTeX transcription。
4. 确认完成 proof review。
5. 检查 `Attempts`：应出现 `P000001-A01`，且只出现一行对应这个完成的 Attempt。

### D. 归档

1. 完成该题的 durable Note。
2. 确认 `P000001 Note` 可读取。
3. 确认 `Problem_Index.note_url` 已写回。
4. 确认 `Problem_Index.status = ARCHIVED`。
5. 只有这些 durable records readback 成功后，才归档该工作 Chat。

## 7. 新 Chat 检索测试

归档第一题 Chat 后，进入长期保留的 `01｜题库检索`，输入：

```text
P000001
```

确认返回该题的 durable Note，而不是依赖旧 Chat memory。

再测试一个模糊查询，例如：

```text
最近做过的几何题
```

如果这道题满足条件，应能返回 `P000001`。

## 8. 重做测试

新建一个新的工作 Chat，输入：

```text
重做 P000001
```

确认：

1. 仍然使用 `P000001`，不创建第二个 Problem；
2. 新 Attempt 为 `P000001-A02`；
3. 提交前只显示题面和安全 metadata；
4. 不显示 A01 的旧解答、key insight、error route 或 hint history；
5. 状态重新进入 `SOLUTION_LOCKED`；
6. A02 完成后，`Attempts` 总共有两行：A01、A02；
7. 系统能够比较 A01 与 A02 的时间、hint、score/result 等进步数据。

完成后再次归档该工作 Chat。

## 9. Setup 完成标准

以下全部成立才算安装完成：

```text
Skill ready
Project Instructions ready
Google Drive connected
IMO Tutor Data exists
IMO Learning DB exists
Problem_Index + Attempts initialized
00｜使用说明 exists
01｜题库检索 exists
first problem archived
new-chat retrieval works
redo creates A02 without duplicate Problem
```

## 10. 迁移到新的 ChatGPT Project

IMO Tutor 的长期数据在 Google Drive / Sheets，不在旧 Chat。

迁移时：

1. 在新的 ChatGPT Project 安装相同或更新版本的 `imo-tutor` Skill；
2. 复制 `PROJECT_INSTRUCTIONS.md`；
3. 连接能够访问原 `IMO Tutor Data` 和 `IMO Learning DB` 的同一个 Google Drive；
4. 不要新建第二份同名数据库，除非你明确希望开始一套新数据；
5. 在新 Project 的 `01｜题库检索` 中输入一个已有 `Pxxxxx` 验证 readback；
6. 成功后即可继续使用，旧工作 Chat 不需要迁移。

## 11. 数据与隐私

- 每个学生只使用自己的私有 Drive 数据库。
- 不要把 credentials、private Drive IDs 或个人解答提交到公共 GitHub 仓库。
- 不要共享一份 Learning DB 给多个学生共同写入；v1.x 不支持班级/多人数据模型。
