# B2B SEO Workflow

这是一套**可执行**的 B2B SEO 工作流仓库：不仅有策略文档，还包含看板模板、阶段门禁（Stage Gate）、SLA、周计划生成脚本，能直接从关键词池跑到 MQL/SQL 复盘。

## 你之前会觉得“不完整”的原因

典型失败点是只有“该做什么”，没有“谁在什么时候把什么交给谁”。
本仓库现在补齐了：
- 明确阶段入口/出口（Entry/Exit Criteria）
- 明确状态流转（Backlog → Brief Ready → In Production → Published → Optimizing）
- 明确交接物（Brief、URL、实验记录、复盘结论）
- 明确执行节奏（周会/日常/发布后 24h/7d/30d）

## 快速开始（15 分钟）

1. 阅读主流程：`docs/b2b-seo-workflow.md`
2. 准备关键词池：填写 `templates/keyword-cluster-template.csv`
3. 生成本周计划：
   ```bash
   python scripts/seo_workflow.py weekly-plan \
     --keywords templates/keyword-cluster-template.csv \
     --limit 5 \
     --out ops/weekly-plan.csv
   ```
4. 将计划导入看板：`templates/workflow-board-template.csv`
5. 周五复盘时更新：`templates/seo-experiment-log-template.csv`


## 按你要求的“代运营式交付”

如果你希望我按“你给产品+关键词表，我来做集群、优先级、逐篇大纲、关键词定稿、E-E-A-T和内外链”的方式协作，请使用：

- 流程说明：`docs/content-cluster-delivery-workflow.md`
- 集群模板：`templates/article-cluster-backlog-template.csv`
- 大纲审核模板：`templates/article-outline-review-template.md`
- 优先级脚本：
  ```bash
  python scripts/cluster_priority.py --input <你的关键词表.csv> --output ops/cluster-priority-plan.csv --limit 50
  ```

## 目录结构

- `docs/b2b-seo-workflow.md`：完整 SOP（RACI、门禁、SLA、节奏、KPI）
- `ops/weekly-cadence.md`：周会模板 + 交付节拍
- `scripts/seo_workflow.py`：关键词打分/周计划生成工具
- `templates/keyword-cluster-template.csv`：关键词池
- `templates/content-brief-template.md`：内容 Brief 模板
- `templates/workflow-board-template.csv`：工作流看板模板
- `templates/seo-experiment-log-template.csv`：实验日志
