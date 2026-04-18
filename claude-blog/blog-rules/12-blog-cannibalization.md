# /blog cannibalization — 关键词蚕食检测

检测多篇博客文章争夺相同搜索关键词的情况。支持本地免费模式和 DataForSEO API 模式。

---

## 两种模式

| 模式 | 标志 | 成本 | 数据来源 |
|------|------|------|---------|
| 本地（默认） | — | 免费 | 通过 Grep/Read 分析文件内容 |
| API | `--api` | ~$0.01/次 | DataForSEO Page Intersection + Ranked Keywords |

本地模式无需 API 密钥。API 模式需要环境变量：`DATAFORSEO_LOGIN` 和 `DATAFORSEO_PASSWORD`。

---

## 本地模式工作流

### Step 1：扫描博客文件

用 Glob 查找目标目录中的所有内容文件：
- 模式：`**/*.md`, `**/*.mdx`, `**/*.html`
- 跳过：`node_modules/`, `.git/`, `drafts/` 中的文件

### Step 2：提取主关键词

对每个文件，从以下位置提取关键词信号：
- **标题标签或 H1**（最高权重）
- **H2 标题**（中等权重）
- **第一段**（辅助信号）
- **Meta 描述**（如前置元数据中有）

提取方法：
1. 将标题和 H1 分词为 1-gram、2-gram 和 3-gram 短语
2. 按短语在标题 + H2 + 第一段中的频率评分
3. 选择评分最高的 2-3 词短语作为主关键词
4. 从 H2 标题记录次要关键词

### Step 3：按相似度聚类

按以下匹配规则（优先顺序）对文章分组：

1. **精确匹配**：2+ 篇文章的主关键词完全相同
2. **词干匹配**：相同词根（如 "optimize" vs "optimization"）
3. **语义重叠**：两个关键词针对相同搜索意图（如 "best CRM software" vs "top CRM tools 2026"）
4. **子集匹配**：一个关键词包含另一个（如 "email marketing" vs "email marketing for startups"）

### Step 4：评分和标记

对每个有 2+ 篇文章的簇，评估严重程度并生成建议。

---

## API 模式工作流（DataForSEO）

需要 `--api` 标志。使用 WebFetch 调用 DataForSEO 端点。

### 使用的端点

**Page Intersection** — 查找多个 URL 都排名的关键词：
```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/page_intersection/live
Authorization: Basic <base64(login:password)>

{
  "pages": {
    "1": "https://example.com/post-a",
    "2": "https://example.com/post-b"
  },
  "language_code": "en",
  "location_code": 2840
}
```
成本：~$0.01/次。返回重叠关键词及排名、搜索量、CPC。

**Ranked Keywords** — 获取单个 URL 排名的所有关键词：
```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live

{
  "target": "https://example.com/post-a",
  "language_code": "en",
  "location_code": 2840
}
```

### API 分析步骤

1. 收集用户的所有已发布 URL（或从 sitemap 获取）
2. 为每个 URL 运行 Ranked Keywords 构建关键词画像
3. 为共享关键词簇的 URL 对运行 Page Intersection
4. 使用以下公式计算严重程度
5. 输出含搜索量和排名数据的增强报告

---

## 严重程度评分

### 四个严重程度级别

| 级别 | 标准 | 紧急性 |
|------|------|--------|
| Critical（关键） | 完全相同关键词，两篇文章都在前 20 | 立即处理 |
| High（高） | 相同关键词簇，一篇胜出 | 本周处理 |
| Medium（中） | 相关关键词，部分 SERP 重叠 | 本月处理 |
| Low（低） | 语义相似但意图确认不同 | 监测 |

### API 模式严重程度公式

```
严重程度分 = 重叠数量 × 平均搜索量 × (1 / 排名差距)
```

其中：
- `重叠数量` = 共享排名关键词数量
- `平均搜索量` = 共享关键词的月均搜索量
- `排名差距` = 平均排名位置的绝对差值（最小值 1）

分数越高 = 蚕食问题越紧急。

### 本地模式严重程度启发式

无 SERP 数据时，使用简化评分：
- **Critical**：文章间主关键词精确匹配
- **High**：主关键词词干匹配，或 3+ 个共享 H2 关键词
- **Medium**：主关键词语义重叠
- **Low**：仅子集匹配，或共享次要关键词

---

## 输出格式

### 摘要表

```
| 文章A | 文章B | 共享关键词 | 严重程度 | 建议 |
|-------|-------|---------|--------|------|
| /best-crm-tools | /top-crm-software | best crm, crm tools | Critical | MERGE |
| /email-tips | /email-marketing-guide | email marketing | High | DIFFERENTIATE |
| /seo-basics | /seo-for-beginners | seo basics, beginner seo | Critical | CANONICAL |
| /react-hooks | /react-state-mgmt | react, state | Low | NO ACTION |
```

### 各簇详情

对每个标记的簇提供：
- 两篇文章的标题和 URL
- 重叠关键词完整列表（API 模式含搜索量）
- 哪篇更强（更全面、结构更好）
- 含理由的具体建议

---

## 四种解决方案

### MERGE（合并）
当两页都薄或以相似深度覆盖相同意图：
- 将两篇的最佳内容合并成一篇综合文章
- 301 重定向较弱的 URL 到合并后的文章
- 保留所有指向任一 URL 的内链

### DIFFERENTIATE（差异化）
当页面服务不同意图但关键词定向有重叠：
- 将较弱文章的主关键词转向相关的长尾词
- 更新标题、H1 和 Meta 描述反映新重点
- 在两篇文章间添加内链，信号话题独特性

### CANONICAL（规范化）
当一篇明显更权威，另一篇是次等副本：
- 在较弱页面添加 `rel="canonical"` 指向权威页面
- 如较弱页面无独特价值，考虑 noindex
- 从较弱页面链接到权威页面

### NO ACTION（无行动）
当意图确实不同，尽管表面关键词相似：
- 记录理由供未来审计参考
- 每季度监测排名变化
- 如任一文章排名下降则重新评估

---

## 错误处理

| 错误 | 处理 |
|------|------|
| 未找到博客文件 | 报告"在 [目录] 未找到博客文件"，建议检查路径 |
| DataForSEO 凭证缺失 | API 模式下自动降级为本地模式并通知用户 |
| API 限速（429） | 等待后重试一次，如持续则切换本地模式 |
| WebFetch 失败 | 跳过该来源，报告"无法验证 — 来源不可访问" |
| 单文章目录 | 报告"蚕食分析需要至少 2 篇文章"并优雅退出 |
