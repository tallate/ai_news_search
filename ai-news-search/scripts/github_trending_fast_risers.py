#!/usr/bin/env python3
"""Fetch GitHub trending AI repos ranked by recent (24h-7d) momentum.

Fast-riser heuristics:
  1. Search GitHub for repos created/pushed in the last 7 days (prioritizing
     last 24h) across AI keywords, sorted by stars.
  2. Prefer repos with recent pushes and engagement (forks/issues).
  3. Fall back to the GitHub trending page (daily) when the API is limited.

Note: exact 24h star deltas require historical star data (e.g. star-history
services); this script approximates with creation/push recency + star count
and flags the estimate in the output.

Usage:
    python3 scripts/github_trending_fast_risers.py [--hours 24|72|168] [--limit 20]
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone


KEYWORDS = ["AI", "LLM", "agent", "coding-agent", "MCP", "RAG", "local-model", "inference"]
GITHUB_API = "https://api.github.com/search/repositories"
TRENDING_URL = "https://github.com/trending?since=daily"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "ai-news-search"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_trending():
    """Parse the GitHub trending page as a fallback signal."""
    req = urllib.request.Request(TRENDING_URL, headers={"User-Agent": "ai-news-search"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
    repos = []
    for m in re.finditer(r'href="/([^"/]+/[^"/]+)"[^>]*>.*?<p[^>]*>(.*?)</p>', html, re.S):
        full_name, desc = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
        repos.append({"name": full_name, "description": desc, "source": "github-trending"})
    return repos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=int, default=168, choices=[24, 48, 72, 168])
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    since = (datetime.now(timezone.utc) - timedelta(hours=args.hours)).strftime("%Y-%m-%d")
    repos, seen = [], set()

    for kw in KEYWORDS:
        params = {
            "q": f"{kw} created:>{since} pushed:>{since}",
            "sort": "stars",
            "order": "desc",
            "per_page": 10,
        }
        url = f"{GITHUB_API}?{urllib.parse.urlencode(params)}"
        try:
            data = fetch_json(url)
        except Exception as exc:
            print(f"GitHub search failed for '{kw}': {exc}", file=sys.stderr)
            continue
        for item in data.get("items", []):
            name = item.get("full_name")
            if not name or name in seen:
                continue
            seen.add(name)
            repos.append(
                {
                    "name": name,
                    "url": item.get("html_url", ""),
                    "description": item.get("description") or "",
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "open_issues": item.get("open_issues_count", 0),
                    "language": item.get("language"),
                    "created_at": item.get("created_at", ""),
                    "pushed_at": item.get("pushed_at", ""),
                    "stars_gained_today": "estimate",  # needs star-history data
                    "source": "github-search",
                }
            )

    # Trending page fallback
    try:
        for repo in fetch_trending():
            if repo["name"] not in seen:
                repos.append({**repo, "stars": None, "forks": None})
    except Exception as exc:
        print(f"Trending page fetch failed: {exc}", file=sys.stderr)

    # Sort: stars desc first, then recency of pushes
    repos.sort(key=lambda r: (r.get("stars") or 0), reverse=True)
    print(json.dumps(repos[: args.limit], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

