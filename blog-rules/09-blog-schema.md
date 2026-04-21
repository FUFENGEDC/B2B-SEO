# /blog schema — JSON-LD 结构化数据

使用 @graph 模式为博客文章生成完整的 JSON-LD Schema 标记。将多种 Schema 类型合并到单个 `<script>` 标签中，使用稳定的 @id 引用进行实体链接。

---

## 9步工作流

### Step 1：读取内容

从博客文章提取所有与 Schema 相关的数据：
- **标题**（headline）
- **作者**（姓名、职位、社交链接、资质）
- **日期**（datePublished, dateModified / lastUpdated）
- **描述**（Meta 描述）
- **FAQ 部分**（问题和答案对）
- **图片**（封面图 URL、尺寸、alt 文本；内文图）
- **组织信息**（站点名称、URL、Logo）
- **字数**（从内容长度估算）
- **标签/分类**（用于 BreadcrumbList）
- **Slug**（从文件名或前置元数据）

---

### Step 2：BlogPosting Schema

完整 BlogPosting，含所有必填和推荐属性：

```json
{
  "@type": "BlogPosting",
  "@id": "{siteUrl}/blog/{slug}#article",
  "headline": "文章标题（最多110字符）",
  "description": "Meta描述（150-160字符）",
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "author": { "@id": "{siteUrl}/author/{author-slug}#person" },
  "publisher": { "@id": "{siteUrl}#organization" },
  "image": { "@id": "{siteUrl}/blog/{slug}#primaryimage" },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{siteUrl}/blog/{slug}"
  },
  "wordCount": 2400,
  "articleBody": "内容前200字符摘要..."
}
```

**必填属性**：@type, headline, datePublished, author, publisher, image  
**推荐属性**：description, dateModified, mainEntityOfPage, wordCount, articleBody（摘录）

---

### Step 3：Person Schema（作者）

作者 Schema，含稳定 @id 用于交叉引用：

```json
{
  "@type": "Person",
  "@id": "{siteUrl}/author/{author-slug}#person",
  "name": "作者姓名",
  "jobTitle": "职位或头衔",
  "url": "{siteUrl}/author/{author-slug}",
  "sameAs": [
    "https://twitter.com/handle",
    "https://linkedin.com/in/handle",
    "https://github.com/handle"
  ]
}
```

可选属性（可用时包含）：
- `alumniOf`：教育机构（Organization 类型）
- `worksFor`：雇主（如同一实体则引用 Organization @id）

---

### Step 4：Organization Schema

博客所属组织实体：

```json
{
  "@type": "Organization",
  "@id": "{siteUrl}#organization",
  "name": "组织名称",
  "url": "{siteUrl}",
  "logo": {
    "@type": "ImageObject",
    "url": "{siteUrl}/logo.png",
    "width": 600,
    "height": 60
  },
  "sameAs": [
    "https://twitter.com/org",
    "https://linkedin.com/company/org",
    "https://github.com/org"
  ]
}
```

**Logo 要求**：
- 必须是有效的图片 URL
- Google 建议最小 112×112px，最大 600px 宽
- BlogPosting 发布者推荐矩形 Logo

---

### Step 5：BreadcrumbList Schema

显示内容层级的导航面包屑：

```json
{
  "@type": "BreadcrumbList",
  "@id": "{siteUrl}/blog/{slug}#breadcrumb",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "首页",
      "item": "{siteUrl}"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "分类名称",
      "item": "{siteUrl}/blog/category/{category-slug}"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "文章标题",
      "item": "{siteUrl}/blog/{slug}"
    }
  ]
}
```

没有分类时，用"博客"作为第二个面包屑项，URL 为 `{siteUrl}/blog`。

---

### Step 6：FAQPage Schema

从博客文章的 FAQ 部分提取问答对：

```json
{
  "@type": "FAQPage",
  "@id": "{siteUrl}/blog/{slug}#faq",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "问题内容？",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "完整回答文字（40-60字，含统计）。"
      }
    }
  ]
}
```

> **重要说明**：Google 2023年8月起将 FAQ 富结果限制为政府和医疗站点。但 FAQ Schema 仍有价值：
> - AI 系统（ChatGPT, Perplexity, Gemini）提取 FAQ 数据用于引用
> - 为未来富结果资格变化做好准备
> - 改善内容组织信号

---

### Step 7：VideoObject Schema（如有视频）

文章中每个 YouTube 嵌入视频生成一个 VideoObject：

```json
{
  "@type": "VideoObject",
  "@id": "{siteUrl}/blog/{slug}#video-{index}",
  "name": "视频标题",
  "description": "视频描述摘录（前200字符）",
  "thumbnailUrl": "https://img.youtube.com/vi/{videoId}/hqdefault.jpg",
  "uploadDate": "{ISO 8601 日期}",
  "contentUrl": "https://www.youtube.com/watch?v={videoId}",
  "embedUrl": "https://www.youtube.com/embed/{videoId}",
  "duration": "PT{M}M{S}S",
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": { "@type": "WatchAction" },
    "userInteractionCount": {viewCount}
  }
}
```

每个 VideoObject 添加到 @graph 数组。@id fragment 使用 `#video-1`, `#video-2` 等。

---

### Step 7.5：ImageObject Schema（封面图）

```json
{
  "@type": "ImageObject",
  "@id": "{siteUrl}/blog/{slug}#primaryimage",
  "url": "https://cdn.pixabay.com/photo/.../image.jpg",
  "width": 1200,
  "height": 630,
  "caption": "与 alt 文本匹配的描述性说明"
}
```

**图片要求**：
- URL 必须可爬取且公开可访问
- Width 和 height 应反映实际图片尺寸
- Caption 应与图片 alt 文本匹配或高度一致
- 首选尺寸：1200×630（OG 兼容）或 1920×1080

---

### Step 8：验证与警告

#### 永远不用的废弃类型

| 类型 | 废弃时间 | 原因 |
|------|---------|------|
| HowTo | 2023年9月 | Google 不再显示富结果 |
| SpecialAnnouncement | 2025年7月 | 废弃 |
| Practice Problem | 已废弃 | 教育标记 |
| Dataset | 通用用途废弃 | — |
| Sitelinks Search Box | 废弃 | — |
| Q&A | 2026年1月 | 与 FAQPage 不同，已废弃 |

#### 验证检查

1. 所有 @id 引用解析到 @graph 内的实体
2. dateModified 等于或晚于 datePublished
3. headline 不超过 110 字符
4. description 在 50-160 字符之间
5. 所有 URL 为绝对路径（非相对路径）
6. 图片尺寸为正整数
7. BreadcrumbList position 从 1 开始顺序编号
8. FAQPage 至少有 2 个问题

> **AI 引用优化说明**：使用 3 种或以上 Schema 类型的页面 AI 引用可能性约高 13%。本技能可生成最多 7 种类型，最大化搜索引擎理解和 AI 提取。

---

### Step 9：输出

将所有 Schema 合并到单个 `<script>` 标签中使用 @graph 模式：

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "BlogPosting", ... },
    { "@type": "Person", ... },
    { "@type": "Organization", ... },
    { "@type": "BreadcrumbList", ... },
    { "@type": "FAQPage", ... },
    { "@type": "VideoObject", ... },
    { "@type": "ImageObject", ... }
  ]
}
</script>
```

**@graph 模式的优势：**
- 单个 script 标签代替多个 — 更干净的 HTML
- 通过稳定的 @id 引用进行实体链接（如作者通过 @id 引用 Person）
- Google 和 AI 系统正确解析 @graph 数组
- 作为单个块更易维护和更新

**输出选项：**
- **嵌入 HTML** — 直接粘贴到 `<head>` 或 `</body>` 前
- **独立 JSON** — 用于 CMS Schema 字段或 API 注入
- **MDX 组件** — 如项目使用 MDX，包装在组件中

将生成的 Schema 保存到博客文章文件中，或按用户需求保存到独立的 Schema 文件。
