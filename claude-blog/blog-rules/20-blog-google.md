# /blog google — Google API 集成

博客性能的 Google API 直连：PageSpeed Insights、CrUX 核心网页指标（25周历史）、Search Console、URL 检查、索引 API、GA4 自然流量、NLP 实体分析（E-E-A-T）、YouTube 视频搜索和 Google Ads 关键词规划师。4个凭证层级，13个命令。

---

## 前置条件

**运行任何命令前始终检查凭证：**
```bash
python3 skills/blog-google/scripts/run.py google_auth --check --json
```

**配置文件：** `~/.config/claude-seo/google-api.json`（与 claude-seo 共享）
```json
{
  "api_key": "AIzaSy...",
  "oauth_client_path": "/path/to/client_secret.json",
  "default_property": "sc-domain:example.com",
  "ga4_property_id": "properties/123456789",
  "ads_developer_token": "...",
  "ads_customer_id": "123-456-7890"
}
```

如配置缺失，读取 `references/auth-setup.md` 引导用户完成设置。

---

## 凭证层级

| 层级 | 检测方式 | 可用命令 |
|------|---------|---------|
| **0**（API Key）| `api_key` 存在 | `pagespeed`、`crux`、`crux-history`、`youtube`、`nlp` |
| **1**（OAuth/SA）| + OAuth token 或 service account | 层级 0 + `gsc`、`inspect`、`index` |
| **2**（完整）| + `ga4_property_id` 已配置 | 层级 1 + `ga4` |
| **3**（Ads）| + `ads_developer_token` + `ads_customer_id` | 层级 2 + `keywords` |

运行命令前始终告知检测到的层级。

---

## 命令速查

| 命令 | 用途 | 层级 |
|------|------|------|
| `/blog google setup` | 检查/配置 API 凭证 | — |
| `/blog google pagespeed <url>` | PSI Lighthouse + CrUX 实地数据 | 0 |
| `/blog google crux <url>` | 仅 CrUX 实地数据（p75 指标）| 0 |
| `/blog google crux-history <url>` | 25周 CWV 趋势分析 | 0 |
| `/blog google youtube <query>` | YouTube 视频搜索（播放量、点赞、时长）| 0 |
| `/blog google nlp <url-or-text>` | NLP 实体提取 + 情感分析 | 0 |
| `/blog google gsc <property>` | Search Console：点击、展示、CTR、排名 | 1 |
| `/blog google inspect <url>` | URL 检查：索引状态、规范 | 1 |
| `/blog google index <url>` | 提交 URL 到索引 API | 1 |
| `/blog google ga4 [property-id]` | GA4 自然流量报告 | 2 |
| `/blog google keywords <seed>` | Google Ads 关键词规划师创意 | 3 |
| `/blog google report <type>` | PDF/HTML 性能报告 | — |
| `/blog google quotas` | 显示所有 API 的速率限制 | — |

---

## PageSpeed + CrUX

### `/blog google pagespeed <url>`

已发布博客文章的 Lighthouse 实验室数据 + CrUX 实地数据合并报告。

**脚本：** `python3 skills/blog-google/scripts/run.py pagespeed_check <url> --json`

输出合并实验室分数（某一时刻的 Lighthouse）和实地数据（28天 Chrome 用户指标）。CrUX 优先 URL 级别，降级到来源级别。

### `/blog google crux <url>`

仅 CrUX 实地数据（不运行 Lighthouse），更快。

**脚本：** `python3 skills/blog-google/scripts/run.py pagespeed_check <url> --crux-only --json`

### `/blog google crux-history <url>`

25周 CrUX 历史趋势。显示 CWV 指标是在改善、稳定还是下降。

**脚本：** `python3 skills/blog-google/scripts/run.py crux_history <url> --json`

---

## Search Console

### `/blog google gsc <property>`

搜索分析：最近 28 天的点击量、展示量、CTR、排名。

**脚本：** `python3 skills/blog-google/scripts/run.py gsc_query --property <property> --json`

默认：28天，维度=query,page，类型=web，限制1000。

包含快速赢得检测：排名第 4-10 且展示量高的查询词。

### `/blog google inspect <url>`

URL 检查：来自 Google 的真实索引状态。

**脚本：** `python3 skills/blog-google/scripts/run.py gsc_inspect <url> --json`

返回：verdict（PASS/FAIL）、覆盖状态、robots.txt 状态、索引状态、页面抓取状态、规范选择、移动友好性、富媒体结果。

批量检查：`python3 skills/blog-google/scripts/run.py gsc_inspect --batch <file> --json`

---

## 索引 API

### `/blog google index <url>`

通知 Google URL 更新，用于新博客文章的快速索引。

**脚本：** `python3 skills/blog-google/scripts/run.py indexing_notify <url> --json`

索引 API 官方用于 JobPosting 和 BroadcastEvent/VideoObject 页面，务必告知用户此限制。每日配额：200 个发布请求。

批量：`python3 skills/blog-google/scripts/run.py indexing_notify --batch <file> --json`

---

## GA4 流量

### `/blog google ga4 [property-id]`

自然流量报告：每日 sessions、用户、浏览量、跳出率、参与度。

**脚本：** `python3 skills/blog-google/scripts/run.py ga4_report --property <id> --json`

默认：28天，按 Organic Search 渠道组过滤。

顶部落地页：`python3 skills/blog-google/scripts/run.py ga4_report --property <id> --report top-pages --json`

---

## YouTube（视频发现）

YouTube 提及与 AI 可见性相关性最强（0.737，Ahrefs 75K 品牌数据）。免费，仅需 API key。由 blog-write 和 blog-rewrite 用于视频嵌入。

### `/blog google youtube <query>`

搜索与博客话题相关的 YouTube 视频。

**脚本：** `python3 skills/blog-google/scripts/run.py youtube_search search "<query>" --json`

**配额：** 每次搜索 100 单位（每天免费 10,000 单位）。

返回：标题、频道、播放量、点赞、时长、描述、标签。

视频详情 + 评论：`python3 skills/blog-google/scripts/run.py youtube_search video <video_id> --json`

---

## NLP 内容分析

Google 自己的实体/情感分析，增强博客内容的 E-E-A-T 评分。

### `/blog google nlp <url-or-text>`

完整 NLP 分析：实体、情感、内容分类。

**脚本：** `python3 skills/blog-google/scripts/run.py nlp_analyze --url <url> --json`

**免费层级：** 每月 5,000 单位。需在 GCP 项目上启用计费。

仅实体提取：`python3 skills/blog-google/scripts/run.py nlp_analyze --url <url> --features entities --json`

---

## 关键词研究（Google Ads）

黄金级关键词搜索量数据。需要 Google Ads 账户（层级 3）。

### `/blog google keywords <seed>`

从种子词生成博客话题研究的关键词创意。

**脚本：** `python3 skills/blog-google/scripts/run.py keyword_planner ideas "<seed>" --json`

搜索量查询：`python3 skills/blog-google/scripts/run.py keyword_planner volume "<kw1>,<kw2>" --json`

---

## 报告

### `/blog google report <type>`

生成含图表的专业 PDF/HTML 报告。

**脚本：** `python3 skills/blog-google/scripts/run.py google_report --type <type> --data <json> --domain <domain> --format pdf`

| 类型 | 输入 | 输出 |
|------|------|------|
| `cwv-audit` | PSI + CrUX + CrUX 历史数据 | 含仪表盘和时间线的 CWV 审计 |
| `gsc-performance` | GSC 查询数据 | 含查询表格的 Search Console 报告 |
| `indexation` | 批量检查数据 | 含覆盖甜甜圈图的索引状态报告 |
| `full` | 所有数据合并 | 综合 Google SEO 报告 |

PDF 生成需要系统库：`sudo apt install libpango1.0-dev libcairo2-dev`。weasyprint 不可用时降级为 HTML。

---

## 速率限制

| API | 每分钟 | 每天 | 认证 |
|-----|--------|------|------|
| PSI v5 | 240 QPM | 25,000 QPD | API Key |
| CrUX + History | 150 QPM（共享）| 无限 | API Key |
| GSC 搜索分析 | 1,200 QPM/站 | 30M QPD | Service Account |
| GSC URL 检查 | 600 QPM | 2,000 QPD/站 | Service Account |
| 索引 API | 380 RPM | 200 发布/天 | Service Account |
| GA4 Data API | 10并发（360版50）| 200K Core Tokens/天（360版2M）| Service Account |
| YouTube Data | — | 10,000 单位/天 | API Key |
| NLP API | — | 5,000 单位/月 | API Key（需计费）|

---

## 与博客工作流集成

| 调用方技能 | 使用场景 |
|-----------|---------|
| blog-seo-check | 已发布文章 URL 的实时 CWV 数据（PSI + CrUX）|
| blog-rewrite | NLP 实体分析，识别 E-E-A-T 实体缺口 |
| blog-geo | 真实搜索展示洞察的 GSC 数据 |
| blog-audit | 所有已发布博客 URL 的批量 CWV + 索引检查 |
| blog-write / blog-rewrite | YouTube 搜索用于视频嵌入 |

凭证未配置时优雅降级。

---

## 技术说明

- INP 于 2024年3月12日取代 FID，绝不再引用 FID
- CrUX 的 CLS 值为字符串编码（如 "0.05"），脚本负责解析
- CrUX 404 = Chrome 流量不足，不是认证错误
- 搜索分析数据有 2-3 天延迟
- 索引 API 官方仅用于 JobPosting/BroadcastEvent 页面
- 所有 Google API 在正常使用量下均**免费**

---

## 错误处理

| 场景 | 处理方式 |
|------|---------|
| 未配置凭证 | 运行 `/blog google setup`，列出层级 0 命令（仅需 API key）|
| Service account 缺少 GSC 访问权限 | 在 GSC > 设置 > 用户 > 添加中添加 `client_email` |
| CrUX 数据不可用（404）| Chrome 流量不足，使用 PSI 实验室数据作为备选 |
| 未找到 GA4 property | 在 GA4 管理 > Property 详情中查找 property ID |
| 索引 API 配额超限 | 每天 200 条限制，优先提交最重要的 URL |
| 限速（429）| 等待并以指数退避重试 |
