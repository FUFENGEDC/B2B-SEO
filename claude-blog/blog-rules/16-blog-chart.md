# /blog chart — SVG 数据可视化

为博客文章生成深色模式兼容的内联 SVG 图表。由 `blog-write` 和 `blog-rewrite` 在发现图表价值数据时内部调用，不是面向用户的独立命令。

---

## 输入格式

```
图表请求：
- 类型：horizontal bar（水平柱状图）
- 标题："AI Citation Sources by Platform"
- 数据：ChatGPT 43.8%, Perplexity 6.6%, Google AI Overviews 2.2%, Reddit 7.15%
- 来源：Ahrefs, December 2025
- 平台：mdx（或 html）
```

---

## 图表类型选择

根据数据模式选择，多样性是强制要求 — 同一篇文章中绝不重复类型：

| 数据模式 | 最佳图表类型 |
|---------|------------|
| 前后对比 | 分组柱状图（Grouped bar chart） |
| 排名因素/相关性 | 棒棒糖图（Lollipop chart） |
| 整体占比/市场份额 | 甜甜圈图（Donut chart） |
| 时间趋势 | 折线图（Line chart） |
| 百分比改善 | 水平柱状图（Horizontal bar chart） |
| 分布/范围 | 面积图（Area chart） |
| 多维评分 | 雷达图（Radar chart） |

---

## 不可违反的样式规则

所有图表必须在深色和浅色背景都能正常显示：

```
文字元素：    fill="currentColor"
网格线：      stroke="currentColor" opacity="0.08"
坐标轴线：    stroke="currentColor" opacity="0.3"
背景：        透明（根 SVG 上无 fill）
副标题文字：  fill="currentColor" opacity="0.45"
来源文字：    fill="currentColor" opacity="0.35"
标签文字：    fill="currentColor" opacity="0.8"
```

### 颜色调色板

| 颜色 | Hex | 用途 |
|------|-----|------|
| 橙色 | `#f97316` | 主色/最高值 |
| 天蓝色 | `#38bdf8` | 次色/对比 |
| 紫色 | `#a78bfa` | 第三色/特殊分类 |
| 绿色 | `#22c55e` | 第四色/正向指标 |

彩色元素内的文字：`fill="white"` + `fontWeight="800"`

---

## 标准 SVG 外壳

### HTML 格式

```xml
<svg
  viewBox="0 0 560 380"
  style="max-width: 100%; height: auto; font-family: 'Inter', system-ui, sans-serif"
  role="img"
  aria-label="包含关键数据点的图表描述"
>
  <title>图表标题</title>
  <desc>为屏幕阅读器提供的描述，含所有关键数据点和来源</desc>

  <!-- 图表内容 -->

  <text x="280" y="372" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.35">
    Source: 来源名称 (年份)
  </text>
</svg>
```

### JSX/MDX 格式（camelCase 属性）

```jsx
<svg
  viewBox="0 0 560 380"
  style={{maxWidth: '100%', height: 'auto', fontFamily: "'Inter', system-ui, sans-serif"}}
  role="img"
  aria-label="图表描述"
>
  <title>图表标题</title>
  <desc>为屏幕阅读器提供的描述</desc>

  {/* 图表内容 */}

  <text x="280" y="372" textAnchor="middle" fontSize="10" fill="currentColor" opacity="0.35">
    Source: 来源名称 (年份)
  </text>
</svg>
```

---

## JSX 属性转换（MDX 必须）

| HTML | JSX |
|------|-----|
| `stroke-width` | `strokeWidth` |
| `stroke-dasharray` | `strokeDasharray` |
| `stroke-linecap` | `strokeLinecap` |
| `text-anchor` | `textAnchor` |
| `font-size` | `fontSize` |
| `font-weight` | `fontWeight` |
| `font-family` | `fontFamily` |
| `class` | `className` |
| `style="..."` | `style={{...}}` |

---

## 各图表类型构建方法

### 水平柱状图（Horizontal Bar Chart）

适用于：百分比改善、单指标比较

1. 定义图表区域：x=80, y=40, width=440, height=280
2. 计算条高：`chartHeight / dataCount - gap`（gap=8）
3. 计算条宽：`(value / maxValue) * chartWidth`
4. 条位置：`y = chartY + index * (barHeight + gap)`
5. 左侧标签（右对齐，x=75）：分类名称
6. 条末端值标签：百分比或数字
7. 底部居中来源文字

### 分组柱状图（Grouped Bar Chart）

适用于：前后、A vs B 对比

1. Y 轴定义分组，每组内有多条
2. 使用 2 种颜色（主色 + 次色）
3. 顶部添加图例：彩色方块 + 每系列标签
4. 分组间距 > 组内间距

### 甜甜圈图（Donut Chart）

适用于：整体占比、市场份额

1. 圆心：cx=280, cy=180，外半径=140，内半径=80
2. 使用累积角度计算弧段
3. 每段：`<path d="M... A... L... A... Z" fill="color" />`
4. 圆心文字：总计或关键标签
5. 图表下方图例：彩色方块 + 标签 + 数值

### 折线图（Line Chart）

适用于：时间趋势

1. X 轴：时间段，均匀间距
2. Y 轴：数值范围，4-5 条网格线
3. 绘制网格线：`stroke="currentColor" opacity="0.08"`
4. 绘制数据点：`<circle cx=... cy=... r="4" fill="color" />`
5. 连接：`<polyline points="..." fill="none" stroke="color" strokeWidth="2" />`
6. 可选：折线下方面积填充 `opacity="0.1"`

### 棒棒糖图（Lollipop Chart）

适用于：排名因素、相关性

1. 水平方向（类似柱状图但带圆圈）
2. 从轴到数据点的细线：`stroke="currentColor" opacity="0.15" strokeWidth="1"`
3. 数据点处的圆圈：`r="6"` + 填充颜色
4. 圆圈旁的数值标签
5. Y 轴上的分类（左对齐）

### 面积图（Area Chart）

适用于：分布、累积数据

1. 同折线图，但有折线下方填充区域
2. 面积填充：`<path d="M... L... L... Z" fill="color" opacity="0.15" />`
3. 顶部折线：`stroke="color" strokeWidth="2" fill="none"`
4. 网格线在面积后面

### 雷达图（Radar Chart）

适用于：多维评分（5-7个轴）

1. 圆心：cx=280, cy=190
2. 绘制同心多边形网格（3-4级）
3. 以等角度计算各轴端点
4. 在每个轴上按比例绘制数据点
5. 用填充多边形连接数据点：`fill="color" opacity="0.2" stroke="color"`
6. 在外边缘标注各轴

---

## 输出格式

每个图表用 `<figure>` 元素包裹：

**HTML：**
```html
<figure>
  <svg viewBox="0 0 560 380" style="max-width: 100%; height: auto; font-family: 'Inter', system-ui, sans-serif" role="img" aria-label="[描述]">
    <title>[图表标题]</title>
    <desc>[为屏幕阅读器提供的完整描述，含数据点]</desc>
    <!-- 图表内容 -->
    <text x="280" y="372" text-anchor="middle" font-size="10" fill="currentColor" opacity="0.35">
      Source: [来源名称] ([年份])
    </text>
  </svg>
</figure>
```

**MDX：**
```mdx
<figure className="chart-container" style={{margin: '2.5rem 0', textAlign: 'center', padding: '1.5rem', borderRadius: '12px'}}>
  <svg viewBox="0 0 560 380" style={{maxWidth: '100%', height: 'auto', fontFamily: "'Inter', system-ui, sans-serif"}} role="img" aria-label="[描述]">
    <title>[图表标题]</title>
    <desc>[完整描述]</desc>
    {/* 使用 camelCase 属性的图表内容 */}
    <text x="280" y="372" textAnchor="middle" fontSize="10" fill="currentColor" opacity="0.35">
      Source: [来源名称] ([年份])
    </text>
  </svg>
</figure>
```

---

## 质量检查清单（返回前验证）

- [ ] 无硬编码文字颜色（全部使用 `currentColor`）
- [ ] 无白色/浅色背景（透明或无填充）
- [ ] 底部有来源归因文字
- [ ] SVG 上有 `role="img"` 和 `aria-label`
- [ ] SVG 内部有 `<title>` 和 `<desc>`
- [ ] 该图表类型在本文中未已使用
- [ ] 如是 MDX：所有属性为 camelCase（属性名无连字符）
- [ ] 数据值与来源数据精确匹配
- [ ] 仅使用批准的调色板颜色
- [ ] ViewBox 为 `0 0 560 380`（标准）或有理由的替代值
