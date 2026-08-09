#!/usr/bin/env python3
"""Build X search queries from keywords/accounts for the X collection track.

Outputs a JSON list of X search URLs. Optionally opens them in the default
browser when --open is passed (requires a logged-in X session).

Usage:
    python3 scripts/prepare_X_search.py --keywords "agent,MCP" --days 2
    python3 scripts/prepare_X_search.py --from @OpenAI,@AnthropicAI --days 2 --open
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta


DEFAULT_KEYWORDS = ["AI", "LLM", "agent", "coding-agent", "MCP", "RAG", "local-model", "inference"]


def build_queries(keywords, accounts, days):
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    until = datetime.now().strftime("%Y-%m-%d")
    queries = []

    for acc in accounts:
        queries.append(
            {
                "name": f"from {acc}",
                "query": f"from:{acc} since:{since} until:{until} -is:retweet",
                "url": f"https://x.com/search?q={quote(f'from:{acc} since:{since} until:{until} -is:retweet')}&f=live",
            }
        )

    for kw in keywords:
        queries.append(
            {
                "name": f"keyword {kw}",
                "query": f"{kw} since:{since} until:{until} min_faves:10 filter:links",
                "url": f"https://x.com/search?q={quote(f'{kw} since:{since} until:{until} min_faves:10 filter:links')}&f=live",
            }
        )
    return queries


def quote(q):
    import urllib.parse
    return urllib.parse.quote(q)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords", help="comma-separated keywords (default: standard AI set)")
    parser.add_argument("--from", dest="accounts", help="comma-separated X handles, e.g. @OpenAI,@AnthropicAI")
    parser.add_argument("--days", type=int, default=2)
    parser.add_argument("--open", action="store_true", help="open queries in the default browser")
    parser.add_argument("--output", help="write JSON to file")
    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()] if args.keywords else DEFAULT_KEYWORDS
    accounts = [a.strip() for a in args.accounts.split(",") if a.strip()] if args.accounts else []

    queries = build_queries(keywords, accounts, args.days)
    if not queries:
        print("No queries generated (provide --keywords or --from).", file=sys.stderr)
        sys.exit(2)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(queries, f, indent=2, ensure_ascii=False)
        print(f"Queries written to {args.output}")
    else:
        print(json.dumps(queries, indent=2, ensure_ascii=False))

    if args.open:
        for q in queries:
            subprocess.run(["open", q["url"]], check=False)


if __name__ == "__main__":
    main()

