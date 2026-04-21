# /blog persona — 写作人格管理

基于 NNGroup 4维音调框架创建、存储和执行写作人格。确保 blog-write 和 blog-rewrite 生成的内容声音一致。

---

## 命令

| 命令 | 用途 |
|------|------|
| `/blog persona create` | 交互式问卷构建新人格 |
| `/blog persona list` | 显示所有已保存人格 |
| `/blog persona use <name>` | 激活当前会话的人格 |
| `/blog persona show <name>` | 显示完整人格配置 |

---

## Create 工作流

运行 6步交互式问卷。每步提问，等待回复后继续。

### Step 1：品牌基础

询问用户：
- **品牌名称**：公司或个人品牌
- **行业**：主要行业（如 SaaS、医疗、金融、教育）
- **目标受众**：谁来读博客（角色、经验水平、目标）
- **品牌使命一句话**：品牌帮助人们做什么

### Step 2：音调维度（NNGroup 框架）

将每个维度呈现为 0.0-1.0 滑块，解释两端并举例：

| 维度 | 0.0端 | 1.0端 | 0.0示例 | 1.0示例 |
|------|------|------|--------|--------|
| funny_serious | 幽默 | 严肃 | "说实话，没人读条款声明" | "理解法律协议保护你的业务" |
| formal_casual | 正式 | 随意 | "我们很高兴地宣布" | "猜猜怎么着 — 上线了！" |
| respectful_irreverent | 尊重 | 不拘一格 | "感谢您的耐心" | "是的，老方法确实有问题" |
| enthusiastic_matter_of_fact | 热情 | 就事论事 | "这改变了一切！" | "这是结果。" |

**如用户不确定的默认值：** `[0.6, 0.5, 0.3, 0.5]`（略严肃，均衡正式度，尊重，均衡热情度）

### Step 3：写作规则

先让用户选择**词汇层级**，再自动建议对应的可读性档位（用户可覆盖）：

| 设置 | 问什么 | 默认值 |
|------|--------|--------|
| 词汇层级 | 消费者、专业或技术 | 专业 |
| 可读性档位 | 从层级自动填充（见下表） | 年级 8-10 |
| 句子长度均值 | 每句平均词数 | 18 |
| 句子长度标准差 | 句长变化程度 | 6 |
| 缩略词频率 | 0.0（从不）到 1.0（总是） | 0.6 |
| 最大被动语态 | 被动句型比例上限 | 10% |

### Step 4：Do's and Don'ts（CMI 品牌声音表）

每项列表请用户提供 3-5 条。根据音调维度提供起始示例：

**Do 示例：** "用数据支持声明"、"直接称呼读者为 you"、"用问题或统计数据开头"

**Don't 示例：** "不要使用专业术语而不定义"、"不要以 There is/There are 开头"、"不要用 game-changer 等套话"

### Step 5：摘要标签偏好

博客文章摘要/要点框使用的标签。让用户选择：

- Key Takeaways（默认）
- The Bottom Line
- What You'll Learn
- TL;DR
- Quick Summary
- In a Nutshell
- 自定义标签

### Step 6：声音样本（可选）

询问用户是否有 1-3 个体现期望声音的现有内容 URL。存储在人格中供参考。如果提供，读取每个 URL 并提取：
- 平均句长
- 缩略词频率
- 音调维度估算
- 词汇等级

将提取值与人格设置比较，标记任何不匹配。

### 保存

将完成的人格保存为 JSON：`skills/blog/references/personas/<name>.json`（使用连字符格式命名）

---

## 人格配置 Schema

```json
{
  "name": "acme-saas",
  "description": "B2B营销内容的专业SaaS声音",
  "brand": "Acme Corp",
  "industry": "SaaS",
  "audience": "中型公司的营销经理",
  "mission": "帮助营销团队自动化报告",
  "tone_dimensions": {
    "funny_serious": 0.7,
    "formal_casual": 0.4,
    "respectful_irreverent": 0.2,
    "enthusiastic_matter_of_fact": 0.5
  },
  "readability": {
    "flesch_grade_min": 8,
    "flesch_grade_max": 10,
    "flesch_ease_min": 50,
    "flesch_ease_max": 60
  },
  "style": {
    "sentence_length_mean": 18,
    "sentence_length_std": 6,
    "contraction_frequency": 0.6,
    "passive_voice_max_pct": 10,
    "vocabulary_tier": "professional",
    "summary_label": "Key Takeaways"
  },
  "voice_samples": [],
  "do": [
    "用数据支持每个主要声明",
    "直接以 you 称呼读者",
    "用可行动的洞察开头"
  ],
  "dont": [
    "不要不加解释地使用专业术语",
    "不要写超过30词的句子",
    "不要以 We at Acme 开头"
  ]
}
```

---

## 可读性档位（按词汇层级）

| 层级 | Flesch 年级 | Flesch 分 | 典型用途 |
|------|------------|----------|---------|
| 消费者（Consumer） | 6-8 | 60-80 | 健康、生活方式、个人理财 |
| 专业（Professional） | 8-10 | 50-60 | B2B、营销、管理 |
| 技术（Technical） | 10-12 | 30-50 | 工程、医疗、法律 |

用户选择层级后自动填充可读性字段。如用户想要非标准组合（如解释性内容的技术词汇+消费者可读性），允许覆盖。

---

## 与 blog-write 和 blog-rewrite 集成

人格激活时（通过 `/blog persona use <name>`），Writer Agent 加载人格 JSON 并在生成期间执行以下约束：

1. **生成前**：加载人格，将音调维度和风格规则注入 blog-writer Agent 的系统提示。
2. **生成中**：作者遵循 do/dont 规则，目标句长均值/标准差，按指定频率使用缩略词。
3. **生成后验证**：根据人格约束检查输出：
   - 句长分布在目标均值 ±1 标准差内
   - 可读性分数在指定年级档内
   - 被动语态比例低于上限
   - 通过模式匹配未发现"dont"规则违规

验证失败时，标记具体违规并建议修改。

---

## 其他命令

**List 命令：**
Glob `skills/blog/references/personas/*.json` 并显示表格：

| 人格 | 行业 | 受众 | 词汇 |
|------|------|------|------|
| acme-saas | SaaS | 营销经理 | Professional |

无人格时，提示用户创建一个。

**Show 命令：**
读取指定人格 JSON，以格式化摘要显示所有音调维度、风格规则和 do/dont 列表。

**Use 命令：**
读取人格 JSON 并确认激活。打印将被执行的关键约束摘要。人格在当前对话会话中保持激活状态。

---

## 错误处理

| 错误 | 处理 |
|------|------|
| 无效音调值 | 如用户提供 0.0-1.0 以外的值，夹紧到最近有效边界并警告 |
| 声音样本 URL 无法访问 | 跳过该 URL，在配置中注明样本不可用 |
| 空人格目录 | 运行 list 或 show 时无已保存人格，提示用户先创建 |
| 名称冲突 | 创建时人格名称已存在，询问是否覆盖或选择不同名称 |
| JSON 格式错误 | 人格文件损坏时，报告错误并提供从问卷重新创建的选项 |
