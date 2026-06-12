#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简历格式转换工具
将Markdown简历转换为带有颜色主题的HTML或PDF格式
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("请先安装依赖：pip install markdown")
    sys.exit(1)

try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except ImportError:
    HAS_WEASYPRINT = False

try:
    from jinja2 import Template
except ImportError:
    print("请先安装依赖：pip install jinja2")
    sys.exit(1)

# HTML模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--bg-color);
            padding: 40px;
            max-width: 900px;
            margin: 0 auto;
        }
        
        :root {
            {% if theme == 'blue' %}
            --primary-color: #2563eb;
            --secondary-color: #1e40af;
            --accent-color: #3b82f6;
            --bg-color: #f8fafc;
            --text-color: #1e293b;
            --light-gray: #e2e8f0;
            {% elif theme == 'green' %}
            --primary-color: #16a34a;
            --secondary-color: #15803d;
            --accent-color: #22c55e;
            --bg-color: #f0fdf4;
            --text-color: #14532d;
            --light-gray: #dcfce7;
            {% elif theme == 'purple' %}
            --primary-color: #9333ea;
            --secondary-color: #7e22ce;
            --accent-color: #a855f7;
            --bg-color: #faf5ff;
            --text-color: #3b0764;
            --light-gray: #f3e8ff;
            {% elif theme == 'orange' %}
            --primary-color: #ea580c;
            --secondary-color: #c2410c;
            --accent-color: #f97316;
            --bg-color: #fff7ed;
            --text-color: #431407;
            --light-gray: #ffedd5;
            {% elif theme == 'dark' %}
            --primary-color: #374151;
            --secondary-color: #1f2937;
            --accent-color: #6b7280;
            --bg-color: #111827;
            --text-color: #f9fafb;
            --light-gray: #374151;
            {% else %}
            --primary-color: #374151;
            --secondary-color: #4b5563;
            --accent-color: #9ca3af;
            --bg-color: #ffffff;
            --text-color: #1f2937;
            --light-gray: #e5e7eb;
            {% endif %}
        }
        
        h1 {
            color: var(--primary-color);
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 8px;
            padding-bottom: 12px;
            border-bottom: 3px solid var(--accent-color);
        }
        
        h2 {
            color: var(--secondary-color);
            font-size: 1.5em;
            font-weight: 600;
            margin-top: 32px;
            margin-bottom: 16px;
            padding-left: 12px;
            border-left: 4px solid var(--primary-color);
        }
        
        h3 {
            color: var(--primary-color);
            font-size: 1.2em;
            font-weight: 600;
            margin-top: 24px;
            margin-bottom: 12px;
        }
        
        p {
            margin-bottom: 12px;
            color: var(--text-color);
        }
        
        strong {
            color: var(--primary-color);
        }
        
        hr {
            border: none;
            border-top: 2px solid var(--light-gray);
            margin: 24px 0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 0.95em;
        }
        
        th {
            background-color: var(--primary-color);
            color: white;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 10px 16px;
            border: 1px solid var(--light-gray);
        }
        
        tr:nth-child(even) {
            background-color: var(--bg-color);
        }
        
        tr:hover {
            background-color: var(--light-gray);
        }
        
        ul, ol {
            margin: 12px 0;
            padding-left: 24px;
        }
        
        li {
            margin-bottom: 8px;
            color: var(--text-color);
        }
        
        code {
            background-color: var(--light-gray);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: "SF Mono", Monaco, Menlo, Consolas, monospace;
            font-size: 0.9em;
        }
        
        pre {
            background-color: var(--secondary-color);
            color: white;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 16px 0;
        }
        
        pre code {
            background-color: transparent;
            color: white;
            padding: 0;
        }
        
        blockquote {
            border-left: 4px solid var(--accent-color);
            padding-left: 16px;
            margin: 16px 0;
            color: var(--secondary-color);
            font-style: italic;
        }
        
        a {
            color: var(--primary-color);
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        @media print {
            body {
                padding: 20px;
                max-width: 100%;
            }
            
            h1 {
                font-size: 2em;
            }
            
            h2 {
                font-size: 1.3em;
            }
        }
    </style>
</head>
<body>
    {{ content }}
</body>
</html>'''

# 可用主题
THEMES = {
    'blue': '蓝色系 - 科技、互联网',
    'green': '绿色系 - 环保、健康',
    'purple': '紫色系 - 创意、设计',
    'orange': '橙色系 - 活力、营销',
    'dark': '深色系 - 商务、金融',
    'minimal': '灰色系 - 简约、专业'
}


def list_themes():
    """列出可用主题"""
    print("\n可用主题：")
    print("-" * 40)
    for name, desc in THEMES.items():
        print(f"  {name:10} - {desc}")
    print()


def md_to_html(md_content, title="简历", theme='blue'):
    """
    将Markdown转换为带有CSS样式的HTML
    
    Args:
        md_content: Markdown内容
        title: 页面标题
        theme: 颜色主题
    
    Returns:
        完整的HTML字符串
    """
    # 转换Markdown为HTML
    extensions = ['tables', 'fenced_code', 'nl2br']
    html_body = markdown.markdown(md_content, extensions=extensions)
    
    # 使用Jinja2模板渲染
    template = Template(HTML_TEMPLATE)
    html = template.render(
        content=html_body,
        title=title,
        theme=theme
    )
    
    return html


def html_to_pdf(html_content, output_path):
    """
    将HTML转换为PDF
    
    Args:
        html_content: HTML内容
        output_path: PDF输出路径
    """
    if not HAS_WEASYPRINT:
        print("错误：PDF转换需要weasyprint库")
        print("请运行：pip install weasyprint")
        print("或者使用HTML版本：--format html")
        return False
    
    HTML(string=html_content).write_pdf(output_path)
    print(f"PDF已生成：{output_path}")
    return True


def convert_file(input_path, output_format='html', theme='blue', title=None):
    """
    转换文件
    
    Args:
        input_path: 输入文件路径
        output_format: 输出格式（html/pdf）
        theme: 颜色主题
        title: 页面标题
    """
    # 读取Markdown文件
    input_path = Path(input_path)
    if not input_path.exists():
        print(f"错误：文件不存在 - {input_path}")
        return
    
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 设置标题
    if title is None:
        title = input_path.stem
    
    # 转换为HTML
    html_content = md_to_html(md_content, title, theme)
    
    # 生成输出路径（主题名加入文件名）
    output_dir = input_path.parent
    stem = input_path.stem
    
    if output_format == 'html':
        output_path = output_dir / f"{stem}-{theme}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML已生成：{output_path}")
    
    elif output_format == 'pdf':
        html_path = output_dir / f"{stem}-{theme}.html"
        pdf_path = output_dir / f"{stem}-{theme}.pdf"
        
        # 先保存HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML已生成：{html_path}")
        
        # 转换为PDF
        html_to_pdf(html_content, pdf_path)
    
    else:
        print(f"错误：不支持的格式 - {output_format}")
        return


def main():
    parser = argparse.ArgumentParser(
        description='将Markdown简历转换为带有颜色主题的HTML或PDF格式'
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='输入的Markdown文件路径'
    )
    
    parser.add_argument(
        '-f', '--format',
        choices=['html', 'pdf'],
        default='html',
        help='输出格式（默认：html）'
    )
    
    parser.add_argument(
        '-t', '--theme',
        choices=list(THEMES.keys()),
        default='blue',
        help='颜色主题（默认：blue）'
    )
    
    parser.add_argument(
        '--title',
        help='页面标题（默认使用文件名）'
    )
    
    parser.add_argument(
        '--list-themes',
        action='store_true',
        help='列出可用主题'
    )
    
    args = parser.parse_args()
    
    # 列出主题
    if args.list_themes:
        list_themes()
        return
    
    # 检查输入文件
    if not args.input:
        parser.print_help()
        return
    
    # 执行转换
    convert_file(
        input_path=args.input,
        output_format=args.format,
        theme=args.theme,
        title=args.title
    )


if __name__ == '__main__':
    main()
