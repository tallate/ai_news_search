#!/usr/bin/env python3
"""Generate a Markdown or HTML report from AI news collection data."""

import json
import sys
import os


def generate_markdown(news_items, output_path=None):
    """Generate a Markdown report from news items."""
    lines = ["# AI News Report", ""]
    
    # Group by category
    categories = {}
    for item in news_items:
        cat = item.get("category", "general")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    for cat, items in categories.items():
        lines.append(f"## {cat.replace('_', ' ').title()}")
        lines.append("")
        for item in items:
            lines.append(f"### {item.get('title', 'Untitled')}")
            lines.append(f"- Source: [{item.get('source', '')}]({item.get('url', '')})")
            lines.append(f"- Published: {item.get('published_at', 'N/A')}")
            lines.append(f"- Importance: {item.get('importance', 'Medium')}")
            lines.append("")
            lines.append(item.get("summary", ""))
            lines.append("")
    
    result = "\n".join(lines)
    if output_path:
        with open(output_path, "w") as f:
            f.write(result)
        print(f"Report saved to {output_path}")
    else:
        print(result)
    
    return result


def generate_html(news_items, output_path=None):
    """Generate an HTML report from news items."""
    md_content = generate_markdown(news_items)
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AI News Report</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        h3 {{ color: #666; margin-bottom: 5px; }}
        a {{ color: #0366d6; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
<pre>{md_content}</pre>
</body>
</html>"""
    
    if output_path:
        with open(output_path, "w") as f:
            f.write(html)
        print(f"HTML report saved to {output_path}")
    else:
        print(html)
    
    return html


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_report.py <json_file> [output_path] [--html]", file=sys.stderr)
        sys.exit(1)
    
    with open(sys.argv[1]) as f:
        items = json.load(f)
    
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    use_html = "--html" in sys.argv
    
    if use_html:
        generate_html(items, output_path)
    else:
        generate_markdown(items, output_path)
