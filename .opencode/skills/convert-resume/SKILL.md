---
name: convert-resume
description: 将Markdown简历转换为带有颜色主题的HTML格式
mode: subagent
permission:
  edit: allow
  bash: allow
  webfetch: allow
  skill:
    "*": allow
---

# 简历格式转换技能

将Markdown简历转换为美观的HTML格式，支持多种颜色主题。

## 功能

1. Markdown → HTML（带CSS样式）
2. 支持多种颜色主题
3. 支持自定义样式

## 使用方法

### 命令行调用

```bash
# 转换为HTML
python convert_resume.py input.md --theme blue

# 查看可用主题
python convert_resume.py --list-themes
```

### 可用主题

| 主题名称 | 主色调 | 适用场景 |
|----------|--------|----------|
| blue | 蓝色系 | 科技、互联网 |
| green | 绿色系 | 环保、健康 |
| purple | 紫色系 | 创意、设计 |
| orange | 橙色系 | 活力、营销 |
| dark | 深色系 | 商务、金融 |
| minimal | 灰色系 | 简约、专业 |

## 技术实现

### 依赖库

```bash
pip install markdown jinja2
```

### 核心代码

```python
import markdown
from jinja2 import Template

# Markdown转HTML
def md_to_html(md_content, theme='blue'):
    html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    template = Template(HTML_TEMPLATE)
    return template.render(content=html_body, theme=theme)
```

## CSS主题样式

### 蓝色主题（科技风格）

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --accent-color: #3b82f6;
    --bg-color: #f8fafc;
    --text-color: #1e293b;
}

h1 { color: var(--primary-color); border-bottom: 3px solid var(--accent-color); }
h2 { color: var(--secondary-color); border-left: 4px solid var(--primary-color); padding-left: 12px; }
h3 { color: var(--primary-color); }
table { border-collapse: collapse; width: 100%; }
th { background-color: var(--primary-color); color: white; }
td { border: 1px solid #e2e8f0; padding: 8px; }
```

### 绿色主题（健康风格）

```css
:root {
    --primary-color: #16a34a;
    --secondary-color: #15803d;
    --accent-color: #22c55e;
    --bg-color: #f0fdf4;
    --text-color: #14532d;
}
```

### 紫色主题（创意风格）

```css
:root {
    --primary-color: #9333ea;
    --secondary-color: #7e22ce;
    --accent-color: #a855f7;
    --bg-color: #faf5ff;
    --text-color: #3b0764;
}
```

## 输出文件

转换后的文件保存在与原文件相同的目录：

```
output/{用户名字}/{公司}/
├── {用户名字}-{岗位}-简历.md          # 原始Markdown
└── {用户名字}-{岗位}-简历-{theme}.html # HTML版本
```

## 注意事项

1. 首次使用需要安装依赖：`pip install markdown jinja2`
2. 复杂的Markdown格式可能需要调整CSS
3. 用浏览器打开HTML文件即可查看效果
