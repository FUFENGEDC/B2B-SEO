# B2B SEO Workflow

这份仓库用于搭建并运行一套 **B2B SEO 工作流**，目标是从“关键词研究”走到“线索转化”，形成可复用、可量化、可迭代的增长系统。

## 快速开始

1. 阅读主流程文档：`docs/b2b-seo-workflow.md`
2. 复制模板到你的项目空间并填写：
   - `templates/keyword-cluster-template.csv`
   - `templates/content-brief-template.md`
   - `templates/seo-experiment-log-template.csv`
3. 按照文档中的周节奏执行（Sprint 节奏）
4. 每周复盘一次、每月做一次策略迭代

# SEO Content OS

一个面向 **B2B 制造商网站** 的多模型 SEO 内容生产系统。  
目标不是“单纯用 AI 写文章”，而是把 **文章集群规划、竞对调研、关键词研究、大纲设计、EEAT、内链、成稿、配图、Schema、记录归档** 串成一套可复用、可协作、可追踪的工作流。

---

## 1. 系统目标

本系统用于生产符合以下要求的 B2B SEO 内容：

- 基于文章集群，而不是零散写文
- 基于关键词研究，而不是拍脑袋选题
- 基于竞对结构分析，而不是直接让 AI 硬写
- 基于 EEAT、GEO、FAQ、Schema 的结构化输出
- 基于内链和商业路径，而不是只追求流量
- 基于记录表归档，形成可复用内容资产

---

## 2. 适用场景

适用于 B2B 制造商 / 工厂型网站，例如：

- OEM / ODM 制造商
- 出口型工厂网站
- 行业解决方案型网站
- 有产品页、服务页、案例页、认证页、博客页的独立站

---

## 3. 三个模型的分工

本系统默认使用以下三个模型协作完成内容生产。

### GPT-5.4 Thinking
负责“判断、结构、逻辑、规范化输出”：

- Step 1：确认文章集群
- Step 2：确认文章主题
- Step 4：确定文章大纲 + FAQ
- Step 6：生成适合文章的 EEAT
- Step 10：生成结构化数据代码

### Gemini 3.1 Pro
负责“调研、扩展、成稿、图像规划”：

- Step 3：竞对调研与分析
- Step 5：关键词调研与分析
- Step 8：文章生成
- Step 9：文章配图规划

### Claude Opus 4.6
负责“站内路由、文件操作、记录归档、记忆调用”：

- Step 7：确认网站内链
- Step 11：所有内容回填到表格、跑代码、加文件、读取记忆

---

## 4. 所有模型的共同规则

- 三个模型都具有读取当前文件夹全部文件的能力。
- 每一步都必须先读取：
  - `/shared/rules/*`
  - `/shared/context/*`
  - 对应 `brief`
  - 上一步产出文件
- 后一步不得跳过前一步的结果直接生成内容。
- 文章生成前，必须已经具备：
  - 集群确认
  - 主题确认
  - 竞对分析
  - 大纲 + FAQ
  - 关键词映射
  - EEAT 包
  - 内链计划
- Schema 生成必须基于最终文章草稿，而不是基于假设结构。
- Step 11 必须完成归档记录，否则该篇文章视为未闭环。

---

## 5. 文章集群体系（必须使用 8 类）

本系统统一使用以下 8 类文章集群，不再使用旧的“产品型 / 工程类 / 认证类”粗分类方式。

1. 认知教育型集群  
2. 选型决策型集群  
3. 对比替代型集群  
4. 规格标准型集群  
5. 应用场景 / 解决方案型集群  
6. 工艺质量 / 问题排查型集群  
7. 认证合规型集群  
8. 采购合作 / 供应商评估型集群  

### 原则
- 每个主题必须先判断属于哪个集群，再进入后续流程。
- 每个集群都对应不同的搜索意图、漏斗阶段、商业价值和页面去向。
- 不允许跳过集群判断，直接写文章。

---

## 6. 问答式写作规则（非常重要）

为了更容易拿到 **精选摘要 / PAA / AI Overview 引用**，本系统要求：

- 文章尽量多采用 **问答式写法**
- 重要 H2 / H3 优先写成问题形式
- 每个关键问题下，采用：
  - **先直接回答**
  - **再展开解释**
- FAQ 不是可选项，而是大多数文章的必备项
- 适合用问题标题的常见形式：
  - What Is X?
  - How to Choose X?
  - Why Does X Happen?
  - What Should Buyers Check?
  - Is X Better Than Y?
  - How Do You Evaluate a Supplier?

### 目标
让文章更容易被搜索引擎和 AI 系统抽取为：
- 文本型精选摘要
- 列表型摘要
- FAQ 摘要
- PAA 问题回答

---

## 7. GEO 结构规则

每篇文章都必须具备 **GEO（生成式搜索优化）友好结构**。

### 至少包含以下 3 种摘要形式中的 3 种以上
- 直接答案摘要（Direct Answer）
- 列表摘要（List Summary）
- 表格摘要（Table Summary）
- 步骤摘要（Step-by-Step Summary）
- FAQ 摘要（FAQ Summary）

### 强制要求
- H1 下方必须有 2–3 句直接答案
- 文中必须有 FAQ
- 文中至少有一个列表或表格或步骤块
- 开头不允许空话铺垫，要直接回答问题

---

## 8. 工作流总览（11 步）

### Step 1：确认文章集群（GPT）
输入：
- 种子主题
- 行业方向
- 产品方向
- 用户画像

输出：
- 最终集群类型
- 漏斗阶段
- 商业价值判断
- 下游页面建议

---

### Step 2：确认文章主题（GPT）
输入：
- Step 1 集群结果
- 集群候选标题

输出：
- 主题候选
- 优先级排序
- 最终选题
- 页面冲突风险说明

---

### Step 3：竞对调研与分析（Gemini）
输入：
- 最终选题
- 目标关键词
- 竞品 URL / SERP 观察

输出：
- 竞对结构表
- 常见 H2 / H3 模块
- FAQ / 表格 / 列表 / 步骤使用情况
- 可超越机会点
- 竞对缺失点

---

### Step 4：确定文章大纲 + FAQ（GPT）
输入：
- Step 3 竞对分析
- 对应文章集群的大纲模板

输出：
- H1
- 直接答案摘要
- H2 / H3 结构
- FAQ 列表
- GEO 摘要规划
- 差异化说明

---

### Step 5：关键词调研与分析（Gemini）
输入：
- 目标主题
- 大纲
- 种子词
- 竞品信息

方法顺序：
1. 用户需求逆向推导
2. AI 扩展
3. Google 下拉 / 相关搜索
4. 竞品关键词反查
5. SEMrush 筛选
6. SERP / PAA 补充

输出：
- 主关键词
- 次级关键词
- Supporting / 语义关键词
- FAQ / PAA 关键词
- 关键词布局建议

---

### Step 6：生成适合文章的 EEAT（GPT）
输入：
- 大纲
- 关键词映射
- 工厂 / 产品 / 案例信息

输出：
- Experience（经验）插入内容
- Expertise（专业）插入内容
- Authoritativeness（权威）插入内容
- Trustworthiness（可信）插入内容
- 推荐插入位置

---

### Step 7：确认网站内链（Claude）
输入：
- 页面清单
- 产品页
- 案例页
- 联系页
- 集群文章页
- 最终大纲

输出：
- 产品页内链
- 案例页内链
- 联系页内链
- 同集群文章内链
- 锚文本建议
- 避免页面冲突说明

---

### Step 8：文章生成（Gemini）
输入：
- 最终大纲
- FAQ
- 关键词布局
- EEAT 包
- 内链计划

输出：
- 完整文章 Markdown
- Meta Title
- Meta Description
- URL Slug
- FAQ
- CTA

### 必须遵守
- 至少 2500 字
- 采用问答式写法优先
- 至少 3 种 GEO 摘要形式
- B2B 买家视角
- 先答后讲
- 插入 EEAT
- 执行内链计划

---

### Step 9：文章配图（Gemini）
输入：
- 最终文章
- 大纲
- 关键词

输出：
- 推荐图片数量
- 图片位置
- 图片类型
- Alt 文本
- 文件命名建议

### 建议规则
- 每 500 字至少 1 张图
- 优先使用：
  - 产品图
  - 工艺流程图
  - 表格 / 数据图
  - 案例图

---

### Step 10：结构化数据代码生成（GPT）
输入：
- 最终文章
- FAQ
- 步骤块
- 图片规划

输出：
- Article Schema
- FAQPage Schema
- HowTo Schema
- ImageObject Schema

### 原则
- 必须输出有效 JSON-LD
- 不能凭空编造字段
- 必须与最终文章一致

---

### Step 11：回填表格 / 跑代码 / 加文件 / 读取记忆（Claude）
输入：
- 全部前置输出
- keyword-record-template.csv
- 页面 / 记忆 / context 文件

输出：
- 记录表回填完成
- 文件归档完成
- 缺失项检查完成
- 最终状态标记：
  - pass
  - revise
  - blocked

---

## 9. 目录说明

### `/shared/rules`
放统一规则，三个模型都必须先读。

包括但不限于：
- 站点定位规则
- 集群分类规则
- 搜索意图规则
- 大纲规则
- 关键词研究规则
- EEAT 规则
- 内链规则
- 问答式写作规则
- GEO 规则
- Schema 规则
- 质量门槛规则

### `/shared/context`
放站点上下文和长期资产，例如：
- 网站基础信息
- 页面库存
- 产品分类
- 案例清单
- 认证清单
- 品牌记忆 / 历史偏好

### `/templates`
放固定模板。

本系统优先沿用以下模板：
- `article-cluster-research-template.md`
- `content-brief-template.md`
- `keyword-record-template.csv`

并可扩展：
- `competitor-analysis-template.md`
- `outline-output-template.md`
- `keyword-map-template.csv`
- `eeat-pack-template.md`
- `internal-link-plan-template.csv`
- `image-brief-template.md`
- `schema-input-template.yaml`

### `/prompts`
放每一步对应模型的 prompt 文件，按模型拆分：
- `/prompts/gpt`
- `/prompts/gemini`
- `/prompts/claude`

### `/inputs`
放每篇文章的输入信息：
- article brief
- seed keywords
- competitor URLs
- source notes

### `/outputs`
按步骤存放产物，保证流程可追踪、可回溯。

---

## 10. 必须沿用的现有模板

### 1）文章集群调研模板
文件：
`templates/article-cluster-research-template.md`

用途：
- 规划 8 大集群下的候选标题
- 标记优先级
- 标记搜索意图
- 标记漏斗阶段
- 作为 Step 1 / Step 2 的输入基础

### 2）内容 Brief 模板
文件：
`templates/content-brief-template.md`

用途：
- 记录基础信息
- 记录关键词规划
- 记录搜索意图与 CTA
- 调用 8 大集群对应的大纲模板
- 记录 EEAT / 内链 / 外链 / 素材 / Schema / DoD

### 3）关键词记录表
文件：
`templates/keyword-record-template.csv`

用途：
- 回填文章标题
- 回填大纲摘要
- 回填关键词
- 回填内链 / 外链
- 回填 URL / 字数 / GEO / Schema / 收录状态
- 作为最终归档记录

---

## 11. 内容质量门槛（DoD）

每篇文章至少满足以下要求：

- [ ] 字数 ≥ 2500
- [ ] 主关键词出现在标题、H1、首段、Meta Title
- [ ] 至少包含 3 种 GEO 摘要形式
- [ ] FAQ 已添加
- [ ] 问答式写法已充分使用
- [ ] EEAT 4 个维度都有落点
- [ ] 内链至少包含：
  - 产品页 × 1
  - 案例页 × 1
  - 联系页 × 1
- [ ] 至少 2 条权威外链
- [ ] 配图数量达标，Alt 已写
- [ ] 至少 2 种 Schema 已添加（视文章结构而定）
- [ ] 记录表已回填
- [ ] 最终状态不是 blocked

---

## 12. 内容生产的底层原则

### 原则 1：先研究，再生成
不能把 AI 当“直接写稿机”。  
必须先经过：
- 集群判断
- 主题判断
- 竞对调研
- 关键词分析
- 大纲设计
- EEAT 规划
- 内链规划

### 原则 2：先回答，再展开
尤其是 H2 / H3 里的关键问题，优先使用：
- 直接答案
- 列表
- 表格
- FAQ

### 原则 3：优先做能承接询盘的主题
高优先级通常包括：
- 采购合作 / 供应商评估型
- 应用场景 / 解决方案型
- 选型决策型

### 原则 4：不是只做流量，而是做转化路径
每篇文章都应该想清楚：
- 它引到哪个页面
- 它服务哪个集群
- 它是引流型、养熟型，还是转化型

---

## 13. 成功标准

这套系统成功，不是因为“AI 写得很快”，而是因为：

- 文章集群更清晰
- 选题更稳定
- 竞对分析更系统
- 大纲更适合抢摘要
- 关键词布局更自然
- EEAT 更有实感
- 内链更服务转化
- Schema 更规范
- 最终记录更完整
- 三个模型各做自己最擅长的事

---

## 14. 一句话理解这套系统

这不是一个“AI 写文章工具”，  
而是一套 **B2B SEO 内容生产操作系统**。

它的核心不是让某一个模型变得更强，  
而是让 **GPT 管判断、Gemini 管调研与成稿、Claude 管路由与归档**，  
再加上你自己的商业判断，形成真正可持续的内容生产流程。


## 仓库结构

### 文档（docs/）
- `b2b-seo-workflow.md`：完整工作流、RACI、KPI 与 SOP
- `content-creation-sop.md`：内容生产 12 步标准流程（EEAT + GEO + Schema）
- `keyword-research-sop.md`：关键词调研 SOP（4 大流程 + 5 大方法 + SERP 分析）

### 模板（templates/）
- `keyword-cluster-template.csv`：关键词聚类与优先级模板
- `keyword-record-template.csv`：文章关键词词表（含内链/外链/Schema 归档）
- `content-brief-template.md`：内容 Brief 模板（含 EEAT/GEO/DoD 清单）
- `article-cluster-research-template.md`：文章集群标题调研 + 竞对大纲记录表
- `seo-experiment-log-template.csv`：实验与优化记录模板
