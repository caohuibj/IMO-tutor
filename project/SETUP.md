# Setup

本文件面向第一次安装 IMO Tutor 的学生。目标不是理解内部 schema，而是机械完成安装并跑通第一道题。

## 0. Preflight：先确认当前 ChatGPT 环境受支持

v1.0 不按 plan 名称猜测能力，而是按实际可用功能判断。继续安装前，确认以下全部成立：

- ChatGPT 中可以进入 `Plugins → Skills`；
- `Skills → Create` 中存在 `Upload from your computer`；
- 你的 workspace 允许 Skill upload / install；
- 可以创建 ChatGPT Project；
- 可以连接 Google Drive app；
- Google Drive / Docs / Sheets 的写操作可用，你有权限创建和更新自己的 Drive 文件与 Google Sheet。

如果缺少任一项，停止安装；当前环境不属于 IMO Tutor v1.0 的支持范围。Personal Skills 和 Google app actions 的可用性会受到 ChatGPT plan、workspace admin 配置和 OAuth scope 的影响，应以当前 ChatGPT 界面为准。

## 1. 下载 Release 资产

打开最新的 GitHub Release，下载：

```text
imo-tutor-v<version>.zip
Problem_Index.csv
Attempts.csv
PROJECT_INSTRUCTIONS.md
```

Release 还会附带：

```text
SETUP.md
PROJECT_GUIDE.md
USER_GUIDE.md
```

不需要 clone 仓库，也不要自己从仓库中挑文件重新打包。

## 2. 安装 Skill

1. 在 ChatGPT sidebar 进入 `Plugins`。
2. 打开 `Skills`。
3. 选择 `Create`。
4. 选择 `Upload from your computer`。
5. 上传 `imo-tutor-v<version>.zip`。
6. 等待扫描完成，并确认 Skill 可用。

Release zip 的预期结构是：

```text
imo-tutor/
├── SKILL.md
├── workflows/
└── references/
```

如果你在不同 ChatGPT surface 之间切换，例如 desktop 与 web/mobile，请在实际要使用 IMO Tutor 的 surface 上确认该 Skill 已安装可用。

## 3. 创建 ChatGPT Project

1. 创建一个新的 ChatGPT Project，推荐名称：`IMO Tutor`。
2. 打开 Release 中的 `PROJECT_INSTRUCTIONS.md`。
3. 将其完整复制到该 Project 的 Project Instructions。
4. 确认该 Project 中可以正常调用已安装的 `imo-tutor` Skill。

Skill 是当前 ChatGPT account/workspace/surface 的能力，不是每个 Project 内单独安装一次。Project 只需要配置自己的 Project Instructions 和数据连接。

不要把学生个人解答、Drive ID 或 credentials 写入 Project Instructions。

## 4. 连接 Google Drive

连接你自己的 Google Drive app，并确认写操作可用。

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

如果 ChatGPT 可以读取 Drive 但不能创建/更新 Drive 文件或 Sheet，请先解决权限/OAuth/workspace action 配置；只读连接不足以运行 IMO Tutor 持久化闭环。

## 5. 初始化 Learning DB

不要自己设计列名。直接使用 Release 中的两个 CSV：

```text
Problem_Index.csv
Attempts.csv
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

## 6. 建立并 Pin 两个长期通用 Chat

在 IMO Tutor Project 中建立两个通用 Chat：

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

创建后将 `00｜使用说明` 与 `01｜题库检索` **Pin 到 sidebar**，并保持不归档。Web 上可在 sidebar 对话的 `⋯` 菜单选择 `Pin chat`；移动端可长按对话后选择 `Pin chat`。

不要再创建长期的“新题”“批改”“Hints”通用 Chat；这些状态都应该留在具体题目的工作 Chat 中。

详细信息见 `PROJECT_GUIDE.md`。

## 7. 第一题 integration test

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

## 8. 新 Chat 检索测试

归档第一题 Chat 后，进入 Pin 的 `01｜题库检索`，输入：

```text
P000001
```

确认返回该题的 durable Note，而不是依赖旧 Chat memory。

再测试一个模糊查询，例如：

```text
最近做过的几何题
```

如果这道题满足条件，应能返回 `P000001`。

## 9. 重做测试

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

## 10. Setup 完成标准

以下全部成立才算安装完成：

```text
Skill upload/install available
Project Instructions ready
Google Drive write actions available
IMO Tutor Data exists
IMO Learning DB exists
Problem_Index + Attempts initialized
00｜使用说明 pinned
01｜题库检索 pinned
first problem archived
new-chat retrieval works
redo creates A02 without duplicate Problem
```

## 11. 迁移到新的 ChatGPT Project

IMO Tutor 的长期数据在 Google Drive / Sheets，不在旧 Chat。

迁移时：

1. 在目标 ChatGPT account/workspace/surface 中确认相同或更新版本的 `imo-tutor` Skill 已安装可用；不要把 Skill 当作 Project 内部文件重复安装；
2. 创建新的 ChatGPT Project，并复制 `PROJECT_INSTRUCTIONS.md`；
3. 连接能够访问原 `IMO Tutor Data` 和 `IMO Learning DB` 的同一个 Google Drive，并确认写操作可用；
4. 不要新建第二份同名数据库，除非你明确希望开始一套新数据；
5. 在新 Project 中重新建立并 Pin `00｜使用说明`、`01｜题库检索`；
6. 在 `01｜题库检索` 中输入一个已有 `Pxxxxx` 验证 readback；
7. 成功后即可继续使用，旧工作 Chat 不需要迁移。

## 12. 数据与隐私

- 每个学生只使用自己的私有 Drive 数据库。
- 不要把 credentials、private Drive IDs 或个人解答提交到公共 GitHub 仓库。
- 不要共享一份 Learning DB 给多个学生共同写入；v1.x 不支持班级/多人数据模型。
