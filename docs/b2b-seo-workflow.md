# B2B SEO 端到端工作流（可执行版）

## 1. Workflow Contract（先定义“完成”）

### 1.1 目标
- 用自然流量持续产出 MQL/SQL，而不是只看 PV。

### 1.2 统一输入/输出
- **输入**：关键词池、ICP、产品卖点、历史数据。
- **输出**：可归因页面、可追踪实验、可复盘结论。

### 1.3 完成标准（Definition of Done）
一篇内容仅在同时满足以下条件才算“完成”：
1. 已发布并可索引。
2. 已绑定 CTA 并可追踪转化事件。
3. 已进入 7/30 天复盘队列。
4. 已记录下一轮优化动作（若表现未达标）。

---

## 2. 角色与交接（RACI + Handoff）

| 环节 | Owner | 协作 | 必交付物 |
|---|---|---|---|
| 关键词优先级 | SEO Lead | Sales / PMM | 优先级关键词清单 |
| Brief 产出 | SEO Lead | Editor / SME | `content-brief` |
| 内容生产 | Editor | SME / Design | 可发布稿件 |
| 发布上线 | Dev / WebOps | SEO Lead | 可抓取 URL + 校验截图 |
| 实验复盘 | SEO Lead | Analyst / Sales | 实验结论 + 下轮动作 |

**交接规则（必须）**：
- 无 Brief 不得进入写作。
- 无追踪参数不得发布。
- 无 7/30 天任务不得归档。

---

## 3. 6 阶段流程（带 Entry / Exit / SLA）

## Stage 0：数据与技术基线（季度）

**Entry**：准备启动季度 SEO 计划。

**关键动作**：
- Search Console / GA4 / CRM 打通。
- 核心页面索引、canonical、sitemap 正常。
- 转化事件命名统一（如 `seo_demo_submit`）。

**Exit**：
- 追踪链路已验证（从 landing 到 CRM）。
- 基线巡检表已归档。

**SLA**：季度第一周内完成。

---

## Stage 1：机会池构建（双周）

**Entry**：已有 ICP 与核心场景。

**关键动作**：
- 汇总关键词并映射 TOFU/MOFU/BOFU。
- 使用统一评分模型算 `priority_score`。

**Exit**：
- 形成“可执行 backlog”（至少未来 4 周量）。

**SLA**：每两周更新一次。

---

## Stage 2：计划与 Brief（每周一）

**Entry**：Backlog 中存在 `status=backlog` 且评分达标主题。

**关键动作**：
- 运行 `seo_workflow.py weekly-plan` 生成周计划。
- 给每个主题产出一份 Brief。

**Exit**：
- 主题状态改为 `brief_ready`。
- Brief 内 CTA 与转化目标已定义。

**SLA**：周一 18:00 前完成。

---

## Stage 3：生产与质检（周二~周三）

**Entry**：主题处于 `brief_ready`。

**关键动作**：
- 完成内容草稿、素材、内链。
- SEO Lead 按 DoD 质检。

**Exit**：
- 状态改为 `ready_to_publish`。
- 所有必填 SEO 字段齐全（Title/Description/Slug/Schema）。

**SLA**：不超过 2 个工作日。

---

## Stage 4：发布与索引跟踪（周四）

**Entry**：`ready_to_publish` 且发布窗口可用。

**关键动作**：
- 发布后 24h 内检查可抓取与索引状态。
- 记录首日指标（曝光、CTR、点击）。

**Exit**：
- 状态改为 `published`。
- 看板已填入 `published_url` 与发布日期。

**SLA**：发布后 24h 完成首轮检查。

---

## Stage 5：7/30 天优化与实验（周五 + 月复盘）

**Entry**：内容已发布。

**关键动作**：
- 7 天看 CTR 和排名趋势。
- 30 天看 MQL/SQL 贡献。
- 对低表现页创建实验并记录到实验日志。

**Exit**：
- 状态改为 `optimizing` 或 `scaled`。
- 有明确结论：保留 / 回滚 / 二次实验。

**SLA**：
- D+7 必做轻复盘；
- D+30 必做业务复盘。

---

## 4. 看板状态机（必须按此流转）

`backlog -> brief_ready -> in_production -> ready_to_publish -> published -> optimizing -> scaled`

回退规则：
- 质检不通过：`ready_to_publish -> in_production`
- 30 天表现差：`published -> optimizing`

---

## 5. 周节奏（操作层）

参考：`ops/weekly-cadence.md`

- 周一：优先级评审 + 周计划生成 + Brief 完成
- 周二/三：生产与质检
- 周四：发布与索引检查
- 周五：复盘 + 实验立项

---

## 6. KPI（运营 + 业务双视角）

**运营 KPI**
- 当周按时发布率（目标 ≥ 90%）
- 发布后 24h 可抓取通过率（目标 = 100%）
- 7 天复盘完成率（目标 = 100%）

**业务 KPI**
- 非品牌自然流量
- SEO 来源 MQL/SQL
- 页面级 CVR 与 SQL 贡献页面数

---

## 7. 最小可运行版本（2 人团队）

每周只做 1 个主题，也要跑完全链路：
1. 关键词评分入池
2. 生成周计划
3. 产出 Brief 并发布
4. D+7/D+30 复盘并记录实验

没有复盘，不算完成。
