# /blog taxonomy — CMS 分类管理

跨平台管理博客文章的标签、分类和话题集群。支持 WordPress REST API、Shopify GraphQL、Ghost Content API、Strapi REST/GraphQL 和 Sanity GROQ。

---

## 命令

| 命令 | 用途 |
|------|------|
| `/blog taxonomy suggest <file>` | 从内容中提取候选标签和分类 |
| `/blog taxonomy sync <cms>` | 通过认证 API 将分类同步到 CMS |
| `/blog taxonomy audit [directory]` | 检查薄标签、孤立标签、分类臃肿 |

---

## 标签建议工作流

### Step 1：解析内容结构

读取目标文件，提取：
- 所有 H2 和 H3 标题（主话题信号）
- 加粗和斜体短语（强调信号）
- 如前置元数据已有标签/分类，提取现有值

### Step 2：词频分析

扫描正文中的高频短语：
- 1词：最少出现 4 次（排除停用词）
- 2词短语：最少出现 3 次
- 3词短语：最少出现 2 次

排除常见非标签词：冠词、介词、连词、代词。

### Step 3：语义分组

将相关候选词归为簇：
- 合并单复数变体（保留更常用形式）
- 合并带连字符与不带连字符形式
- 将同义词归并到最高频术语

### Step 4：去重并排名

- 对 slugified 名称进行模糊匹配（Levenshtein 距离 ≤ 2）
- 每个候选词评分：`(频率 × 2) + (标题出现 × 5) + (强调 × 1)`
- 返回排名前 5-10 的建议

### 输出格式

```
## 标签建议：[文章标题]

| 排名 | 标签 | 评分 | 来源 |
|------|------|------|------|
| 1 | content-marketing | 18 | H2 + 6次提及 |
| 2 | seo-strategy | 14 | H3 + 4次提及 |
| 3 | keyword-research | 11 | 5次提及 + 加粗 |

### 建议分类
- 主分类：[最适合的分类]
- 次分类：[可选的第二分类]
```

---

## CMS 适配器

### 适配器概览

| CMS | API 类型 | 认证方式 | 标签模型 |
|-----|---------|---------|---------|
| WordPress | REST | 应用密码（base64）| 具有 ID 的一级实体 |
| Shopify | GraphQL（Admin API）| Admin API 访问令牌 | Article 上的字符串数组 |
| Ghost | REST（Admin API）| 带 JWT 签名的 API key | 一级实体 |
| Strapi | REST 或 GraphQL | API token（Bearer）| 用户定义的内容类型 |
| Sanity | GROQ / Mutations | 项目令牌（Bearer）| 文档类型 |

### WordPress 适配器

**获取标签列表：**
```
GET {CMS_URL}/wp-json/wp/v2/tags?per_page=100&search={keyword}
Authorization: Basic {base64(username:app_password)}
```

**创建标签：**
```
POST {CMS_URL}/wp-json/wp/v2/tags
Body: {"name": "Tag Name", "slug": "tag-name", "description": "Optional"}
```

**获取分类列表（支持层级 parent 字段）：**
```
GET {CMS_URL}/wp-json/wp/v2/categories?per_page=100
```

**创建分类：**
```
POST {CMS_URL}/wp-json/wp/v2/categories
Body: {"name": "Category", "slug": "category", "parent": 0}
```

**为文章分配标签：**
```
POST {CMS_URL}/wp-json/wp/v2/posts/{id}
Body: {"tags": [1, 2, 3], "categories": [4]}
```

分页：通过 `X-WP-TotalPages` 响应头处理全量列表。

### Shopify 适配器

Shopify 的标签是 Article 对象上的字符串数组，不是一级实体。

**更新文章标签（GraphQL Admin API）：**
```graphql
mutation {
  articleUpdate(id: "gid://shopify/Article/123", article: {
    tags: ["tag-one", "tag-two", "tag-three"]
  }) {
    article { id tags }
    userErrors { field message }
  }
}
```

**列出所有已使用标签（GraphQL）：**
```graphql
{
  articles(first: 250) {
    edges {
      node { id title tags }
    }
  }
}
```

认证头：`X-Shopify-Access-Token: {token}`

注意：REST API 于 2024年10月标记为旧版，2025年4月起新应用必须使用 GraphQL。

### Ghost 适配器

**获取标签列表：**
```
GET {CMS_URL}/ghost/api/admin/tags/?limit=all
Authorization: Ghost {jwt_token}
```

**创建标签：**
```
POST {CMS_URL}/ghost/api/admin/tags/
Body: {"tags": [{"name": "Tag Name", "slug": "tag-name"}]}
```

JWT 生成：用 admin API key（id:secret 格式）签名，iat = 当前时间，exp = 5分钟，audience = `/admin/`。

### Strapi 适配器

端点由内容类型自动生成，典型配置：

```
GET {CMS_URL}/api/tags?pagination[pageSize]=100
POST {CMS_URL}/api/tags
Body: {"data": {"name": "Tag Name", "slug": "tag-name"}}
Authorization: Bearer {api_token}
```

Strapi v4+ 使用 `data` 包装器。检查内容类型 schema 确认字段名。

### Sanity 适配器

**查询标签（GROQ）：**
```
*[_type == "tag"] { _id, name, slug }
```

**创建标签（Mutations API）：**
```
POST https://{project_id}.api.sanity.io/v2024-01-01/data/mutate/{dataset}
Body: {"mutations": [{"create": {"_type": "tag", "name": "Tag", "slug": {"current": "tag"}}}]}
Authorization: Bearer {token}
```

---

## 分类审计工作流

### Step 1：清单盘点

扫描目标目录中的所有文章（或从 CMS 获取）。建立映射：
- tag_name → [使用该标签的文章文件/ID 列表]
- category_name → [文章文件/ID 列表]

### Step 2：健康检查

| 检查项 | 阈值 | 建议行动 |
|--------|------|---------|
| 薄标签存档 | < 5 篇文章/标签 | 建议 noindex 或合并 |
| 孤立标签 | 0 篇文章 | 建议删除 |
| 标签臃肿 | > 50 个标签 | 建议整合 |
| 分类深度 | > 3 层 | 建议扁平化 |
| 未分类文章 | 未分配分类 | 分配至合适分类 |
| 重复 slug | 相同 slug 不同名称 | 合并为规范版本 |

### Step 3：建议

按优先级分组：
- **Critical**：孤立标签产生空存档页（抓取浪费）
- **High**：薄标签 < 3 篇文章（用户体验差，SEO 信号弱）
- **Medium**：标签臃肿超 50 个（分类稀释，导航困难）
- **Low**：命名不一致（大小写混用、连字符 vs 空格）

### 输出格式

```
## 分类审计：[站点/目录]

**总标签数**：[n] | **总分类数**：[n]
**健康**：[n] | **薄**：[n] | **孤立**：[n]

### 关键问题
- [孤立标签列表]

### 建议
1. 合并 [tag-a] 和 [tag-b]（同话题，合计 [n] 篇文章）
2. 删除孤立标签：[列表]
3. 给 < 5 篇文章的标签存档添加 noindex
```

---

## 全站指南

- 每个站点目标 5-10 个主分类（宽泛话题）
- 标签需至少 5 篇文章才应创建存档页
- 使用一致 slug 格式：小写、连字符分隔
- 每篇文章必须属于恰好 1 个主分类
- 每篇文章标签数：推荐 3-8 个，绝不超过 15 个

---

## 环境变量

| 变量 | 用途 | 示例 |
|------|------|------|
| CMS_TYPE | 平台标识符 | wordpress, shopify, ghost, strapi, sanity |
| CMS_URL | CMS 基础 URL | https://example.com |
| CMS_API_KEY | 认证凭证 | 应用密码、API token 或 key |

这些变量必须在 shell 环境中设置。不要将凭证存储在文件中或提交到版本控制。运行时通过 `$CMS_TYPE`、`$CMS_URL`、`$CMS_API_KEY` 读取。

---

## 错误处理

| 错误 | 处理方式 |
|------|---------|
| 缺少环境变量 | 报告缺失的变量并提供期望格式 |
| 凭证无效（401/403）| 报告"认证失败 — 检查 CMS_API_KEY"，不重试 |
| 连接超时 | 报告超时，建议检查 CMS_URL |
| 重复标签 slug | 跳过创建，注明"标签已存在：[名称]" |
| API 限速（429）| 等待后重试一次，持续则上报 |
| 不支持的 CMS | 列出 5 个支持平台并退出 |
