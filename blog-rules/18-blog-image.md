# /blog image — AI 图像生成

通过 Gemini（via nanobanana-mcp）为博客内容生成和编辑 AI 图像。Claude 担任创意总监角色，构建优化的 6 组件提示词，生成英雄图、内联插图、社交预览卡和 OG 图。

---

## 命令

| 命令 | 用途 |
|------|------|
| `/blog image generate <idea>` | 通过完整提示工程生成博客图片 |
| `/blog image edit <path> <instructions>` | 智能编辑现有博客图片 |
| `/blog image setup` | 配置 MCP 服务器和 API key |

---

## 博客图像类型

| 图像类型 | 宽高比 | 分辨率 | 领域模式 | 位置 |
|---------|--------|--------|---------|------|
| 英雄图/封面 | `16:9` | 2K 或 4K | Editorial / Landscape | 前置元数据 `coverImage` |
| OG/社交卡片 | `16:9` | 1K | Editorial / Infographic | 前置元数据 `ogImage` |
| 内联插图 | `16:9` 或 `4:3` | 1K | 按话题选择 | H2 后、正文前 |
| 内联产品图 | `4:3` 或 `1:1` | 1K | Product | 产品章节内 |
| 章节分隔图 | `8:1` 或 `4:1` | 1K | Abstract / Landscape | 主要章节之间 |

**尺寸要求：**
- 博客英雄图/封面：1200×630（OG 兼容）或 1920×1080
- Open Graph（OG）：1200×630（社交分享必须）
- 内联图：1200px+ 宽

---

## MCP 可用性检查

生成前检查 nanobanana-mcp 工具是否可用：

1. 尝试调用 `get_image_history`（轻量级，无副作用）
2. 成功：MCP 可用，继续生成
3. 失败：MCP 未配置，通知用户运行 `/blog image setup`
4. **内部调用时**（来自 blog-write/blog-rewrite）：静默返回，不报错，调用工作流继续使用库存照片

---

## 生成工作流

### Step 1：分析意图

确定博客需求：
- **图像类型**：英雄图、内联图、OG 卡片、章节分隔图？
- **博客话题**：文章关于什么？
- **风格**：照片写实、编辑感、插画、极简？
- **约束**：品牌色、特定尺寸、平台格式？
- **氛围**：权威、温馨、戏剧性、干净？

请求模糊时，就用例和风格提一个澄清问题。

### Step 2：选择领域模式

| 模式 | 使用场景 | 提示重点 |
|------|---------|---------|
| **Editorial** | 博客头图、特色图、生活方式 | 造型、构图、出版物参考 |
| **Product** | 电商文章、评测、对比 | 表面材质、棚拍灯光、干净背景 |
| **Landscape** | 环境背景、旅行、英雄区 | 大气透视、层次感、时间 |
| **UI/Web** | 科技博客图标、插图、示意图 | 干净矢量、扁平设计、精确配色 |
| **Infographic** | 数据驱动文章、流程、对比 | 布局结构、层级、无障碍配色 |
| **Abstract** | 图案背景、章节分隔、装饰 | 色彩理论、数学形式、纹理 |

### Step 3：构建 6 组件 Reasoning Brief

以自然叙述段落构建提示——绝不用关键词列表：

1. **Subject（主体）** — 谁/什么，含丰富物理细节（纹理、材质、尺度）
2. **Action（动作）** — 发生什么，姿势、手势、运动、状态
3. **Context（背景）** — 环境、场景、时间、季节、天气
4. **Composition（构图）** — 摄像角度、镜头类型、取景、留白、景深
5. **Lighting（光线）** — 光源、质感、方向、色温、阴影
6. **Style（风格）** — 艺术媒介、美学、胶片、参考艺术家/时代

**照片写实博客图像模板：**
```
A photorealistic [shot type] of [subject with physical detail], [action/pose],
set in [environment with specifics]. [Lighting conditions] create [mood].
Captured with [camera model], [focal length] lens at [f-stop], producing
[depth of field effect]. [Color palette/grading notes]. Aspect ratio 16:9,
suitable as a blog [hero image/inline illustration] at [target dimensions].
```

**插画/风格化模板：**
```
A [art style] [format] of [subject with character detail], featuring
[distinctive characteristics] with [color palette]. [Line style] and
[shading technique]. Background is [description]. [Mood/atmosphere].
```

### Step 4：设置宽高比

生成前先调用 `set_aspect_ratio`：

| 博客用途 | 比例 |
|---------|------|
| 英雄图 / 封面 / OG | `16:9` |
| 产品图 / 方形 | `4:3` 或 `1:1` |
| 章节分隔图 | `8:1` 或 `4:1` |
| 竖版（Stories）| `9:16` |

### Step 5：通过 MCP 生成

| MCP 工具 | 使用时机 |
|---------|---------|
| `set_aspect_ratio` | 比例不同于 1:1 时，始终先调用 |
| `gemini_generate_image` | 从构建的提示生成新图 |
| `gemini_edit_image` | 修改现有图片 |
| `gemini_chat` | 迭代优化 / 多轮对话 |
| `get_image_history` | 查看已生成图片 |
| `clear_conversation` | 重置会话上下文 |

**模型选择：**
- **NB2 Flash**（默认）：适合大多数博客图 — 快速，14种比例，4K，$0.067/张
- **NB Pro**：含文字叠加英雄图（94% 文字准确率）或最高质量需求 — $0.134/张
- **Original**：经济选项 $0.039/张 — 5种比例，最高 1K

### Step 6：后处理（需要时）

```bash
# 裁剪到博客英雄图尺寸（1200×630）
magick input.png -resize 1200x630^ -gravity center -extent 1200x630 hero.png

# 转 WebP（网页优化）
magick input.png -quality 85 output.webp

# 转 AVIF（最小，现代格式）
magick input.png -quality 80 output.avif
```

检查 `magick`（ImageMagick 7）是否可用。不可用时降级到 `convert`。

### Step 7：交付

提供：
1. **图片路径** — 保存位置（`~/Documents/nanobanana_generated/`）
2. **构建的提示词** — 展示完整 Reasoning Brief（教育意义）
3. **设置** — 模型、宽高比、领域模式
4. **Alt 文字** — 描述性句子，10-125 字符，自然融入话题关键词
5. **前置元数据片段**（英雄图/OG 图）：
```yaml
coverImage: "/path/to/generated-image.png"
coverImageAlt: "描述性 alt 文字含话题关键词"
ogImage: "/path/to/generated-image.png"
```
6. **优化建议** — 1-2 条相关建议

---

## 编辑工作流

对于 `/blog image edit <path> <instructions>`：

1. 读取图片路径和编辑指令
2. 增强指令（绝不直接传递原始文字）：

| 用户说 | Claude 构建 |
|--------|------------|
| "remove background" | 详细的边缘保留背景移除说明 |
| "make it warmer" | 具体色温偏移及保留说明 |
| "add text" | 字体风格、尺寸、位置、对比度、可读性说明 |
| "make it brighter" | 增加曝光、提亮暗部、保持高光 |
| "crop for social" | 以 center-gravity 裁剪至 1200×630 |

3. 用增强指令调用 `gemini_edit_image`
4. 返回修改后图片路径和描述

---

## Alt 文字规范

每张生成图必须提供 alt 文字：
- 完整描述句（不是关键词列表）
- 10-125 字符
- 自然融入话题关键词
- 描述图片内容及与内容的相关性
- 图表/信息图：包含关键数据点

好：`Marketing team analyzing AI search traffic data on a dashboard showing citation metrics`
差：`SEO AI marketing blog optimization image`

---

## 安全过滤器自动重写

收到 `IMAGE_SAFETY` 或 `SAFETY` 时，不要放弃。自动重写并重试：

1. 识别可能的触发因素（暴力、公众人物、NSFW 相邻、过于谨慎的过滤器）
2. 用正面措辞重写 — 描述想要的，而非要避免的
3. 人物描述改为通用（去掉类似名人的具体特征）
4. 戏剧性场景软化："intense"→"focused"，"battle"→"competition"
5. 用重写提示重试（最多 3 次后上报用户）

---

## 编辑优先于重新生成

图片 80% 符合预期时，用 `gemini_chat` 进行对话式编辑，而非从头重新生成。会话保持风格一致性，定向编辑保留已有优点。

| 情况 | 策略 |
|------|------|
| 颜色略微偏差 | 编辑（"shift the color temperature warmer"）|
| 构图完全错误 | 重新生成（修改 Brief）|
| 场景对但光线错 | 编辑（"change to golden hour lighting from the left"）|
| 缺少细节 | 编辑（"add a steaming coffee cup on the desk"）|

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| MCP 未配置 | 运行 `/blog image setup` |
| API key 无效 | 从 https://aistudio.google.com/apikey 获取新 key |
| 限速（429）| 等待 60秒重试 |
| `IMAGE_SAFETY` | 自动重写（见上方）|
| `PROHIBITED_CONTENT` | 内容政策违规，不可重试 |
| `SAFETY` | 重写提示词 |
| 请求模糊 | 生成前提一个澄清问题 |
| 图片质量差 | 检查 Reasoning Brief — 通常缺少光线描述（最大质量影响因素）|
| MCP 不可用（内部调用）| 静默返回，调用工作流使用库存照片 |
