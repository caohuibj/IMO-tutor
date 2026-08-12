# IMO Tutor User Guide

本文件面向已经完成安装的学生，说明每天如何使用 IMO Tutor。

## 1. 一句话原则

**一题一 Chat；做完归档；以后通过 Drive / Sheets 检索，不依赖旧 Chat memory。**

## 2. 每天做一道新题

### Step 1 — 新建工作 Chat

不要使用 `00｜使用说明` 或 `01｜题库检索`。

上传题图或输入题面。

系统应该：

- 分配 `Pxxxxx`；
- 识别 domain；
- 给出 global difficulty；
- 建立安全 metadata；
- 进入 `SOLUTION_LOCKED`；
- 不提前泄露完整解法。

拿到 Problem ID 后，推荐把 Chat 手动改名，例如：

```text
P000237｜IMO 2024 P1
```

### Step 2 — 独立思考

正常情况下直接开始做题，不需要向 Tutor 请求完整解法。

卡住时可以输入：

```text
H1
H2
H3
```

提示按级别逐步增加。不要一开始就请求 H6，除非你决定结束独立 Attempt。

### Step 3 — 提交解答

可以上传手写解答图片，也可以提交解答文本。

系统会：

- 保留原始解答图（runtime 能真实上传时）；
- 转写为 Markdown/LaTeX；
- 找出第一个数学上不可接受的步骤；
- 判断 verdict / result bucket；
- 估计 0–7 分；
- 记录 error tags、method tags、hint 使用和时间等 Attempt 数据。

### Step 4 — 看批改

优先关注：

1. 第一个真正的逻辑缺口；
2. 哪些部分仍然成立；
3. 方法选择是否合理；
4. 是 observation / technique / logic / writing 哪一类问题；
5. 下次遇到类似结构时应该注意什么。

不要只看分数。

### Step 5 — 完成归档

当 durable Note 和 Sheets 更新完成后，系统会把该 Problem 置为 `ARCHIVED`。

只有 durable readback 成功后才归档 Chat。

完成后把这个工作 Chat 从日常 Project chat list 中归档。

## 3. 查看某道旧题

进入长期保留的：

```text
01｜题库检索
```

输入：

```text
P00237
```

短 ID 会 normalize 到 canonical `P000237`。

系统应返回该题 durable Note，而不是依赖原工作 Chat。

## 4. 模糊找题

可以直接用自然语言：

```text
最近做错的2道几何题
难度8以上用过H3提示的数论题
找我曾经做错过的几何题
那道我用了反演但最后逻辑有问题的几何题
```

检索顺序是：

```text
自然语言
→ structured query
→ Attempts / Problem_Index
→ candidates
→ 必要时 search_text
→ Pxxxxx
```

主要可检索维度包括：

```text
domain
difficulty
date
result
hint
error
concept
method
```

不需要维护向量数据库。

## 5. 重做旧题

### Step 1 — 先找到题

在 `01｜题库检索` 中找到目标，例如：

```text
P000237
```

### Step 2 — 新建 redo 工作 Chat

不要直接在长期检索 Chat 中继续正式做题。

新建 Chat，输入：

```text
重做 P000237
```

系统应该：

- 复用同一个 `P000237`；
- 创建下一个 Attempt，例如 `P000237-A02`；
- 只读取题面、source、domain、difficulty 等安全 metadata；
- 不在提交前加载/展示旧 solution、key insight、error route、hint history 或 reference solution；
- 重新进入 `SOLUTION_LOCKED`。

推荐把 Chat 改名：

```text
P000237-A02｜Redo
```

### Step 3 — 完成新 Attempt

像第一次一样独立作答、请求 Hint、提交、批改和归档。

### Step 4 — 看进步

A02 finalize 之后，系统才读取上一 Attempt 做比较，例如：

```text
A01: 52 min | H3 | 3/7
A02: 24 min | H0 | 7/7
Change: -28 min | H3 -> H0 | +4 points
```

重点可以比较：

- `duration_minutes`；
- `hint_max` / `hint_count`；
- `estimated_score`；
- `result_bucket`；
- `first_gap` / `error_tags`；
- `method_tags`。

这才是长期训练中最有价值的 progress 数据。

## 6. `00｜使用说明` 应该问什么

长期保留的 `00｜使用说明` 只用于操作帮助，例如：

```text
怎么初始化新的 Learning DB？
为什么这道题还不能归档？
怎么迁移到新 Project？
怎么查最近做错的数论题？
```

不要在这个 Chat 中开始正式 Problem / Attempt。

## 7. 什么情况下应该开新 Chat

应该新建工作 Chat：

- 新的一道正式题；
- `重做 Pxxxxx`；
- 同一道题开始新的独立 Attempt。

不需要新建 Chat：

- 在当前 Attempt 中请求 H1/H2/H3；
- 上传当前题的补充解答页；
- 继续讨论当前 proof review；
- 查看当前题归档前的 Note。

## 8. 不要这样使用

### 不要把很多题堆在一个 Chat

错误：

```text
今天做 P1
然后再来 P2
然后再做 P3
```

这样会混淆 Problem / Attempt state。

### 不要靠旧 Chat 当数据库

错误：

```text
我记得上个月那个 Chat 里有一道反演题……
```

正确做法：进入 `01｜题库检索`，使用 structured retrieval。

### 不要在归档失败时直接结束

如果 Note、Sheet row 或图片应写入但没有成功，不要把 Chat 当作已完成。

## 9. 一周后的典型复习流程

```text
进入 01｜题库检索
↓
最近做错的3道几何题
↓
得到 P000237 / P000241 / P000248
↓
选择 P000237
↓
新建 Chat
↓
重做 P000237
↓
完成 A02
↓
比较 A01 vs A02
↓
归档 redo Chat
```

## 10. 长期维护习惯

建议：

- 永远保持 `00｜使用说明` 和 `01｜题库检索` 易于找到；
- 当前只保留少量未完成工作 Chat；
- 完成题及时归档 Chat；
- 不手工修改已写入的 ID；
- 不删除 `Problem_Index` / `Attempts` header；
- 升级 Skill 前保留自己的 Drive 数据；
- 升级或迁移后先用一个已有 `Pxxxxx` 做 readback 验证。

## 11. 何时算系统工作正常

你应该能够长期重复：

```text
新题
→ Pxxxxx
→ Attempt
→ Review
→ Note
→ ARCHIVED
→ 新 Chat 检索
→ Redo
→ A02/A03/...
→ Progress comparison
```

如果这条链路持续成立，IMO Tutor 就在按设计工作。
