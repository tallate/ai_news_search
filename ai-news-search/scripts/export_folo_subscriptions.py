#!/usr/bin/env python3
"""Export Folo RSS subscriptions."""

import json
import sys
import os


def export_subscriptions(output_path=None):
    """
    Placeholder to export Folo RSS subscriptions.
    In a real implementation, this would read from Folo's local database
    or API and output a formatted list.
    """
    subscriptions = {
        "official_feeds": [
            "https://openai.com/news/",
            "https://www.anthropic.com/news",
            "https://deepmind.google/discover/blog/",
            "https://ai.meta.com/blog/",
            "https://blogs.nvidia.com/",
            "https://huggingface.co/blog",
        ],
        "news_feeds": [
            "https://techcrunch.com/category/artificial-intelligence/feed/",
            "https://venturebeat.com/category/ai/feed/",
            "https://www.technologyreview.com/feed/",
        ],
        "hn_feed": "https://news.ycombinator.com/rss",
        "arxiv_ai": "http://export.arxiv.org/rss/cs.AI",
    }

    if output_path:
        with open(output_path, "w") as f:
            json.dump(subscriptions, f, indent=2, ensure_ascii=False)
        print(f"Exported subscriptions to {output_path}")
    else:
        print(json.dumps(subscriptions, indent=2, ensure_ascii=False))

    return subscriptions


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    export_subscriptions(path)
