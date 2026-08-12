# IMO Tutor Project Guide

本文件定义 IMO Tutor 在 ChatGPT Project 中的长期组织方式。目标是让 Project 在使用几十、几百道题后仍然保持清晰。

## 1. 核心原则

### Chat 是工作台，Drive / Sheets 是长期记忆

不要靠翻旧 Chat 找历史题。长期记录以：

```text
Google Drive: IMO Tutor Data
Google Sheets: IMO Learning DB
```

为准。

### 一道题一个工作 Chat

同一个工作 Chat 不要连续处理多道正式题目。每道新题和每次正式 redo 都使用独立工作 Chat。

### 完成即归档

当 durable Note、`Problem_Index`、`Attempts` 全部写入并 readback 成功后，该工作 Chat 就完成使命，应归档。

## 2. 推荐的 Project 结构

正常情况下，左侧 Project chat list / sidebar 只需要长期看到两个 **Pinned** 通用 Chat，加上少量当前正在做的题：

```text
IMO Tutor
├── 00｜使用说明              ← Pin
├── 01｜题库检索              ← Pin
├── P000237｜IMO 2024 P1      ← 当前题
└── P000241-A02｜Redo         ← 当前重做
```

已经完成的题目 Chat 应归档，因此不会长期占据 Project chat list。

## 3. 两个长期通用 Chat 如何建立

这两个 Chat 不是需要迁移的数据对象。无论第一次安装还是迁移到新 Project，都按同一种方式**新建并初始化**：

```text
新建普通 Chat
→ 发送一条职责说明
→ 改名
→ Pin 到 sidebar
```

真正的系统规则来自 Project Instructions；首条职责消息只是让该 Chat 从一开始就保持单一用途。

### `00｜使用说明`

初始化首条消息：

```text
这是 IMO Tutor 的长期使用说明对话。这里只回答系统安装、使用、归档、迁移、Hint 规则等问题，不在这里开始正式题目或 Attempt。
```

发送后将 Chat 改名为：

```text
00｜使用说明
```

然后 Pin 到 sidebar，并保持不归档。

职责：回答“系统怎么用”。

适合的问题：

```text
怎么开始一道新题？
H1 到 H6 有什么区别？
什么时候归档？
如何迁移到新的 Project？
Drive 里应该有什么？
```

禁止用途：

- 不在这里上传正式题目开始 Attempt；
- 不在这里批改正式解答；
- 不在这里进行 redo。

这个 Chat 应长期保持轻量，不承载具体题目的 solution state。

### `01｜题库检索`

初始化首条消息：

```text
这是 IMO Tutor 的长期题库检索对话。这里只用于从 Google Drive / Sheets 检索历史题、查看 Note、筛选重做题。正式重做时另开新的工作 Chat。
```

发送后将 Chat 改名为：

```text
01｜题库检索
```

然后 Pin 到 sidebar，并保持不归档。

职责：查询 durable learning database，并帮助决定下一道要复习/重做的题。

典型输入：

```text
P00237
最近做错的2道几何题
难度8以上用过H3提示的数论题
那道我用了反演但最后逻辑有问题的几何题
```

适合用途：

- 精确查看某题 Note；
- 模糊检索历史题；
- 比较候选题；
- 决定下一道重做题。

不建议在这里正式开始 redo。找到目标 `Pxxxxx` 后，新建工作 Chat，再输入：

```text
重做 Pxxxxx
```

这样可避免长期检索 Chat 混入某一题的 `SOLUTION_LOCKED`、hint 和 solution review 状态。

Web 上可在 sidebar 对话的 `⋯` 菜单选择 `Pin chat`；移动端可长按对话后选择 `Pin chat`。

## 4. 不要创建这些长期通用 Chat

v1.0 不推荐长期保留：

```text
新题
批改
Hints
Progress Dashboard
```

原因：

- “新题”会诱导把很多题堆在一个 Chat；
- 批改和 Hint 都属于具体 Attempt；
- Progress 已经可以由检索和 Attempt comparison 获得，不需要另建 dashboard Chat。

## 5. 工作 Chat 生命周期

### 新题

```text
新建 Chat
→ 上传题目
→ 分配 Pxxxxx
→ SOLUTION_LOCKED
→ 作答 / Hints
→ 提交
→ Review
→ Note + Sheets readback
→ ARCHIVED
→ 归档 Chat
```

### Redo

```text
在 01｜题库检索 找到 Pxxxxx
→ 新建工作 Chat
→ 输入 重做 Pxxxxx
→ 创建下一个 Attempt
→ SOLUTION_LOCKED
→ 独立重做
→ Review
→ A01 vs A02 comparison
→ durable update
→ 归档 Chat
```

## 6. Chat 命名建议

系统分配 Problem ID 后，推荐手动把工作 Chat 改成容易识别的名字。

第一次 Attempt：

```text
P000237｜IMO 2024 P1
P000238｜Geometry
```

Redo：

```text
P000237-A02｜Redo
P000237-A03｜Redo
```

优先使用真实 `problem_id` / `attempt_id`，这样 Chat、Drive 和 Sheets 的视觉标识保持一致。

Chat 名称只是导航辅助，不是数据库字段，也不能代替 Drive / Sheets readback。

## 7. 什么状态下不能归档 Chat

如果以下任一情况成立，不要声称该题已经完整归档：

- 应保存的原始图片实际没有成功写入 Drive；
- `Attempts` 还没有 finalized row；
- durable Note 还不能读取；
- `Problem_Index.note_url` 未写回；
- `Problem_Index.status` 还不是 `ARCHIVED`；
- Sheet readback 未确认。

先修复持久化，再归档工作 Chat。

## 8. 如何找旧题

不要打开已归档 Chat 搜索。

进入 `01｜题库检索`：

精确：

```text
P000237
P00237
```

结构化模糊检索：

```text
最近做错的2道几何题
难度8以上用过H3提示的数论题
找我曾经做错过的几何题
```

检索首先使用 `domain / difficulty / date / result / hint / error / concept / method` 等结构化字段，必要时才使用 `search_text` 消歧。

## 9. Project 迁移

迁移的核心不是复制旧 Chat，而是让新的 Project 重新连接同一份 durable database。

Skill 属于当前 ChatGPT account/workspace/surface 的能力，不属于某一个 Project。迁移前先确认目标环境中 `imo-tutor` 已安装可用；如果换了 surface，也要在实际使用的 surface 上确认 Skill 可用。

```text
旧 Project
    ↓
Google Drive / Sheets 保持不变
    ↓
目标 ChatGPT 环境确认 imo-tutor 已安装
    ↓
创建新 Project
    ↓
复制 PROJECT_INSTRUCTIONS
    ↓
连接同一个 Drive，并确认写操作可用
    ↓
新建并初始化 00｜使用说明
    ↓
新建并初始化 01｜题库检索
    ↓
用 Pxxxxx 验证检索
```

“新建并初始化”就是第 3 节的四步：**新建 Chat → 发送职责首条消息 → 改名 → Pin**。旧的两个通用 Chat 和旧工作 Chat 都不需要迁移。

只要新 Project 能读取和更新原 `IMO Learning DB` 与 `IMO Tutor Data`，长期学习记录就仍然存在。

## 10. v1.x Workspace Scope

IMO Tutor v1.x 只服务一个学生自己的学习 workspace。

明确不包含：

- teacher profile；
- classroom / 班级管理；
- 多学生共享 Learning DB；
- teacher dashboard；
- 权限系统；
- 多人协作 Project；
- 教师统计后台。

如果多人共用一份 Sheet，现有 `Pxxxxx`、Attempt sequencing 和隐私假设都不再成立，因此不属于 v1.x 支持范围。
