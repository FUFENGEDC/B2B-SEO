# /blog notebooklm — 来源支撑研究

直接在 Claude Code 中查询 Google NotebookLM 笔记本，获取基于用户上传文档的有来源支撑的 Gemini 答案。每次查询打开无头浏览器会话，从文档中获取答案后关闭。响应质量为 Tier 1（用户自己的主要来源），零幻觉风险。

---

## 命令

| 命令 | 用途 |
|------|------|
| `/blog notebooklm ask <question>` | 查询笔记本获取有来源支撑的答案 |
| `/blog notebooklm discover <url>` | 归档前智能发现笔记本内容 |
| `/blog notebooklm library list` | 列出库中所有笔记本 |
| `/blog notebooklm library add <url>` | 将笔记本添加到库 |
| `/blog notebooklm library search <query>` | 按关键词搜索笔记本 |
| `/blog notebooklm library remove <id>` | 从库中删除笔记本 |
| `/blog notebooklm setup` | 一次性 Google 认证（可见浏览器）|
| `/blog notebooklm status` | 检查认证状态 |
| `/blog notebooklm cleanup` | 清理浏览器状态（保留库）|

---

## 前置条件

- 有 NotebookLM 访问权限的 Google 账户
- Python 3.11+（由 `run.py` 自动管理 venv）
- Google Chrome（首次运行时通过 Patchright 自动安装）
- 一次性认证设置（在可见浏览器中手动 Google 登录）

---

## 始终使用 run.py 包装器

**绝不直接调用脚本，始终使用 `python3 scripts/run.py [script]`：**

```bash
# 正确：
python3 scripts/run.py auth_manager.py status
python3 scripts/run.py ask_question.py --question "..."

# 错误（无 venv 会失败）：
python3 scripts/auth_manager.py status
```

`run.py` 包装器自动创建 `.venv`、安装依赖、设置 Chrome 并执行目标脚本。

---

## 认证检查（门控模式）

任何查询操作前检查认证：

```bash
python3 scripts/run.py auth_manager.py status
```

- **已认证**：继续查询
- **未认证**：告知用户并引导到设置："NotebookLM 需要 Google 登录，运行 `/blog notebooklm setup` 进行认证"
- **内部调用时**（来自 blog-write 或 blog-researcher）：未认证时静默返回，不报错，绝不阻塞写作工作流

---

## 设置工作流

对于 `/blog notebooklm setup`：

```bash
# 打开可见浏览器进行手动 Google 登录（一次性）
python3 scripts/run.py auth_manager.py setup
```

告知用户："一个浏览器窗口将打开，请登录您的 Google 账户。"

认证通过浏览器配置文件 + cookie 注入（混合方式）持久化。

其他认证命令：
```bash
python3 scripts/run.py auth_manager.py status   # 检查认证
python3 scripts/run.py auth_manager.py reauth   # 重新认证
python3 scripts/run.py auth_manager.py clear    # 清除所有认证数据
```

---

## 查询工作流

对于 `/blog notebooklm ask <question>`：

### Step 1：检查认证

运行认证检查（见上方门控模式）。未认证时引导到设置。

### Step 2：确定笔记本

确定要查询哪个笔记本：
- 如提供了 `--notebook-url`：直接使用
- 如提供了 `--notebook-id`：在库中查找
- 两者都没有：使用库中的活跃笔记本
- 无活跃笔记本：显示库并请用户选择

### Step 3：提问

```bash
# 基础查询（使用活跃笔记本）
python3 scripts/run.py ask_question.py --question "Your question here"

# 按 ID 查询特定笔记本
python3 scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# 直接按 URL 查询
python3 scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# JSON 输出（内部/程序化使用）
python3 scripts/run.py ask_question.py --question "..." --json

# 显示浏览器（调试）
python3 scripts/run.py ask_question.py --question "..." --show-browser
```

### Step 4：分析并追问

每个响应后有后续提示。**必须的行为：**
1. **停止** — 不要立即回应用户
2. **分析** — 将答案与用户原始请求比较
3. **识别缺口** — 确定是否需要更多信息
4. **追问** — 如有缺口，立即追问
5. **重复** — 持续到信息完整
6. **综合** — 回应用户前整合所有答案

---

## 智能发现工作流

对于 `/blog notebooklm discover <url>`：

添加笔记本而不知道其内容时，先查询它：

```bash
# Step 1：发现内容
python3 scripts/run.py ask_question.py \
  --question "What is the content of this notebook? What topics are covered? Provide a complete overview briefly and concisely" \
  --notebook-url "<URL>"

# Step 2：用发现的元数据添加
python3 scripts/run.py notebook_manager.py add \
  --url "<URL>" \
  --name "<基于内容的名称>" \
  --description "<基于内容的描述>" \
  --topics "<提取的话题>"
```

**绝不猜测或使用通用描述，始终发现或向用户询问。**

---

## 库管理

```bash
# 列出所有笔记本
python3 scripts/run.py notebook_manager.py list

# 添加笔记本（所有参数必填 — 先发现或询问用户！）
python3 scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "描述性名称" \
  --description "这个笔记本包含的内容" \
  --topics "topic1,topic2,topic3"

# 按关键词搜索
python3 scripts/run.py notebook_manager.py search --query "keyword"

# 设置活跃笔记本
python3 scripts/run.py notebook_manager.py activate --id notebook-id

# 删除笔记本
python3 scripts/run.py notebook_manager.py remove --id notebook-id

# 库统计
python3 scripts/run.py notebook_manager.py stats
```

---

## 内部 API（供 blog-write / blog-researcher 调用）

**输入（由调用技能提供）：**
- `question`：与博客话题相关的研究问题
- `notebook_id` 或 `notebook_url`：要查询的笔记本
- `context`："internal"（标记优雅降级模式）

**流程：**
1. 检查认证状态 — 未认证则静默返回空结果
2. 用研究问题查询笔记本
3. 解析并返回结构化响应

**输出（返回给调用技能）：**
```markdown
### NotebookLM 研究
- **来源：** [笔记本名称]
- **问题：** [提问内容]
- **答案：** [来自用户文档的有来源支撑的回答]
- **来源质量：** Tier 1（用户上传的主要文档）
```

**优雅降级：** 认证缺失或查询失败时，立即静默返回。调用工作流继续使用基于 WebSearch 的研究。绝不因 NotebookLM 不可用而阻塞 blog-write 或 blog-rewrite。

---

## 数据存储

所有数据存储在技能目录内：
- `scripts/data/library.json` — 笔记本元数据和库
- `scripts/data/auth_info.json` — 认证状态
- `scripts/data/browser_state/` — 带 Cookie 的 Chrome 配置文件

**安全：** 所有数据目录已 gitignore，绝不提交认证或浏览器状态。

---

## 错误处理

| 错误 | 解决方案 |
|------|---------|
| 未认证 | 运行 `/blog notebooklm setup` |
| ModuleNotFoundError | 始终使用 `run.py` 包装器 |
| 浏览器崩溃 | `cleanup_manager.py --confirm --preserve-library`，然后重新认证 |
| 限速（50次/天）| 等到太平洋时间午夜或切换 Google 账户 |
| 笔记本未找到 | 用 `notebook_manager.py list` 检查 |
| 查询超时（120秒）| 简化问题重试，或用 `--show-browser` 调试 |
| MCP 不可用（内部）| 静默返回，写作工作流使用 WebSearch |

---

## 限制

- 无会话持久性（每个问题 = 新浏览器会话）
- 免费 Google 账户限速（每天 50 次查询）
- 需手动上传（用户必须在 NotebookLM 网页端添加文档）
- 浏览器开销（每次查询需几秒启动 + 关闭）
- 仅限本地 Claude Code（网页版 UI 不可用）
