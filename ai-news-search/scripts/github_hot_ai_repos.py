#!/usr/bin/env python3
"""Fetch GitHub trending AI repos based on 24-hour star gain."""

import json
import sys
import urllib.request
import urllib.parse


# Keywords to search across for AI-related repos
AI_KEYWORDS = [
    "AI", "LLM", "agent", "coding-agent", "MCP",
    "RAG", "local-model", "inference",
]


def search_github_repos(query, per_page=10):
    """Search GitHub API for repositories matching the query."""
    base_url = "https://api.github.com/search/repositories"
    params = {
        "q": f"{query} created:>{get_date_string()}",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error searching GitHub: {e}", file=sys.stderr)
        return {"items": []}


def get_date_string():
    """Get date string for past 7 days."""
    from datetime import datetime, timedelta
    date = datetime.utcnow() - timedelta(days=7)
    return date.strftime("%Y-%m-%d")


def fetch_hot_ai_repos():
    """Main entry point to fetch trending AI repositories."""
    all_repos = []
    seen = set()

    for keyword in AI_KEYWORDS:
        result = search_github_repos(keyword)
        for item in result.get("items", []):
            repo_name = item.get("full_name", "")
            if repo_name and repo_name not in seen:
                seen.add(repo_name)
                all_repos.append({
                    "name": repo_name,
                    "url": item.get("html_url", ""),
                    "description": item.get("description", ""),
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "created_at": item.get("created_at", ""),
                    "pushed_at": item.get("pushed_at", ""),
                    "language": item.get("language", ""),
                    "topics": item.get("topics", []),
                })

    # Sort by stars descending
    all_repos.sort(key=lambda x: x["stars"], reverse=True)
    return all_repos[:20]


if __name__ == "__main__":
    repos = fetch_hot_ai_repos()
    print(json.dumps(repos, indent=2, ensure_ascii=False))
