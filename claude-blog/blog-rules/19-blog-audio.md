# /blog audio — 音频叙述生成

使用 Google Gemini TTS 为博客文章生成专业音频叙述。支持摘要叙述（200-300词口述概览）、全文朗读和双播客对话模式，提供 30 种声音，支持 80+ 种语言，输出 HTML5 嵌入代码。

---

## 命令

| 命令 | 用途 |
|------|------|
| `/blog audio generate <file>` | 为博客文章生成音频叙述 |
| `/blog audio voices` | 显示可用声音及特点 |
| `/blog audio setup` | 检查/配置 Gemini TTS 的 API key |

---

## 前置条件

- Python 3.11+（由 `run.py` 自动管理 venv）
- 环境变量 `GOOGLE_AI_API_KEY`（与 blog-image 使用相同 key）
- FFmpeg（用于 WAV 转 MP3；缺失时降级到 WAV 输出）

## 始终使用 run.py 包装器

```bash
# 正确：
python3 scripts/run.py generate_audio.py --text "..." --voice Charon --json

# 错误（无 venv 会失败）：
python3 scripts/generate_audio.py --text "..."
```

---

## API Key 检查（门控模式）

生成音频前检查 API key：

```bash
echo $GOOGLE_AI_API_KEY
```

- **已设置**：继续生成
- **未设置**：引导用户：
  - "音频生成需要 Google AI API key，在 https://aistudio.google.com/apikey 免费获取"
  - "然后设置：`export GOOGLE_AI_API_KEY=your-key`"
  - "与 `/blog image` 使用相同的 key — 如果图像生成可用，音频也可用"
- **内部调用时**（来自 blog-write）：key 缺失时静默返回，绝不阻塞写作工作流

---

## 声音推荐

根据内容类型推荐声音：

| 场景 | 推荐声音 |
|------|---------|
| 文章叙述 | Charon（Informative）或 Sadaltager（Knowledgeable）|
| 教程/操作指南 | Achird（Friendly）或 Sulafat（Warm）|
| 新闻/分析 | Rasalgethi（Informative）或 Schedar（Even）|
| 生活方式/健康 | Aoede（Breezy）或 Vindemiatrix（Gentle）|
| 对话主持人 | Puck（Upbeat）或 Laomedeia（Upbeat）|
| 对话专家 | Kore（Firm）或 Charon（Informative）|

---

## 生成工作流

### Step 1：读取博客文章

读取文件并提取：
- 标题（来自 H1 或前置元数据）
- 完整内容（Markdown 正文）
- 大概字数

### Step 2：选择模式

询问用户（或如果指定了 `--mode` 则自动选择）：

| 模式 | 使用场景 | 输出 |
|------|---------|------|
| **Summary（摘要）** | 快速音频概览（1-2 分钟）| 200-300 词口述摘要 |
| **Full（全文）** | 完整朗读（5-15 分钟）| 全文转自然口语 |
| **Dialogue（对话）** | 播客风格（3-8 分钟）| 双人话题讨论 |

### Step 3：准备文字

**重要：Claude 准备文字，脚本只负责 TTS。**

**摘要模式：**
写 200-300 词口述摘要：
- 写成自然口语，而非书面文字
- 以文章关键发现或答案开头
- 覆盖 3-5 个主要要点
- 以可操作建议结尾
- 无 Markdown，无"在这篇文章中..."，无元评论
- 使用对话式过渡（"Here's what matters..."，"The key finding is..."）

**全文模式：**
将 Markdown 内容转为干净口语文字：
- 标题变为自然过渡（"Next, let's look at..."）
- 链接变为纯文字（删除 URL，保留锚文本）
- 图片和图表：省略或简短描述（"As the data shows..."）
- 代码块：口语描述（"The code uses a for-loop to..."）
- 列表：转为自然句子
- 删除前置元数据、Schema 标记、HTML 标签
- 添加简短开场：`"This is [title], published on [date]."`

**对话模式：**
编写关于文章的双人对话脚本：
- Speaker1 = 主持人（好奇，善于提问）
- Speaker2 = 专家（知识渊博，表达清晰）
- 每行格式：`[Speaker1] What's the key takeaway here?`
- 以对话方式覆盖文章主要观点
- 15-25 次交流（产生约 3-8 分钟音频）
- 自然，不生硬（"That's a great point" 优于 "Indeed, as the research indicates"）

### Step 4：选择声音

用户已选择时使用其选择，否则按模式推荐：
- 摘要/全文：默认使用 Charon（Informative）
- 对话：默认使用 Puck（主持人）+ Kore（专家）

### Step 5：生成音频

将准备好的文字写入临时文件，然后调用：

```bash
# 单声音（摘要或全文模式）
python3 scripts/run.py generate_audio.py \
  --text-file /tmp/blog_audio_prepared.txt \
  --voice Charon \
  --model flash \
  --output /path/to/audio/post-slug.mp3 \
  --json

# 双声音（对话模式）
python3 scripts/run.py generate_audio.py \
  --text-file /tmp/blog_audio_dialogue.txt \
  --voice Puck \
  --voice2 Kore \
  --model pro \
  --output /path/to/audio/post-slug-dialogue.mp3 \
  --json
```

**模型选择：**
- `flash`（默认）：快速、经济。适合摘要和标准叙述。
- `pro`：更高质量。用于对话模式或高级内容。

### Step 6：交付

向用户展示结果：
1. **文件路径** — 音频保存位置
2. **时长** — 易读格式（如 "3:42"）
3. **嵌入代码** — 可直接粘贴的 HTML5 audio 标签
4. **费用** — 估算 API 成本
5. **放置建议** — 在博客文章中的插入位置

---

## 嵌入指南

### 标准 HTML（Hugo、Jekyll、静态站点）
```html
<audio controls preload="metadata">
  <source src="audio/post-slug.mp3" type="audio/mpeg">
  Your browser does not support the audio element.
</audio>
```

### MDX（Next.js、Gatsby）
```jsx
<audio controls preload="metadata">
  <source src="/audio/post-slug.mp3" type="audio/mpeg" />
</audio>
```

### WordPress
```
[audio src="audio/post-slug.mp3"]
```

### 放置位置
在引言之后（第一个 H2 下方）或文章最顶部插入音频播放器，加标签："Listen to this article" 或 "Audio version"。

---

## 内部 API（供 blog-write 调用）

**输入：**
- `text`：准备好的文字（Claude 已清理）
- `voice`：声音名称（默认：Charon）
- `voice2`：对话的第二声音（可选）
- `model`：flash 或 pro
- `output_path`：文件保存路径

**输出：**
```markdown
### 音频叙述
- **路径：** /path/to/audio/post-slug.mp3
- **时长：** 3:42
- **声音：** Charon
- **嵌入：** `<audio controls preload="metadata"><source src="audio/post-slug.mp3" type="audio/mpeg"></audio>`
```

**优雅降级：** 如果 `GOOGLE_AI_API_KEY` 未设置，立即静默返回。写作工作流继续，不生成音频。绝不因音频不可用而阻塞 blog-write。

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| GOOGLE_AI_API_KEY 未设置 | 从 https://aistudio.google.com/apikey 获取 key |
| 未找到 FFmpeg | 安装：`sudo apt install ffmpeg`，降级到 WAV 输出 |
| 限速 | 等待并重试，查看 https://aistudio.google.com/rate-limit |
| 文字过长（>32k tokens）| 分节生成，分别处理 |
| 声音名称未知 | 运行 `/blog audio voices` 查看有效选项 |
| API 错误 | 检查 key 有效性、模型可用性（预览模型）|
| API key 缺失（内部调用）| 静默返回，写作工作流继续 |
