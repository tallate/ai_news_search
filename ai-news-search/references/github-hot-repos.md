# GitHub Hot Repository Radar

Rules and keywords for the GitHub track of AI news collection. The radar is
designed to surface repos that are *rising fast right now*, not just the
largest repos overall.

## Keywords to Search

Search across these terms, combined with the topic keywords when the user
asks for a specific theme:

- AI
- LLM
- agent
- coding-agent
- MCP
- RAG
- local-model
- inference
- eval / benchmark (when evaluating model quality)
- fine-tuning / alignment (when relevant)
- open-weights / open-source model

## Ranking Rules

- Rank by **star gain in the last 24 hours**, not by total stars.
- Combine star gain with engagement signals: forks, issues, discussions,
  recent commits (pushed_at), README quality.
- Prefer repos that are new or that jumped in popularity within the window.
- Do NOT rank purely by total stars; a big old repo with no recent activity
  is not a hot repo.
- Include newly created repositories and top repos with recent activity.

## Query Families

Use these families, adjusting the date window to the user's ask
(default: last 7 days, prioritize last 24h):

- `{keyword} created:>YYYY-MM-DD` — new repos in the window
- `{keyword} pushed:>YYYY-MM-DD` — actively maintained repos
- `{keyword} stars:>100` — repos with meaningful traction
- `{keyword} created:>YYYY-MM-DD pushed:>YYYY-MM-DD` — new AND active
- GitHub trending (daily/weekly): `https://github.com/trending?since=daily`

## Output Fields

For each repo include:

- **name** — full repo name (owner/repo)
- **url** — GitHub link
- **description** — what it does
- **stars** — total stars
- **stars_gained_today** — 24h star gain when available
- **language** — primary language
- **created_at / pushed_at** — recency signals
- **why_it_matters** — 1-2 sentences tying it to the current AI news cycle

## Cross-Check Rules

- Verify a repo exists and is not a fork/fake by checking the GitHub page or
  API metadata.
- Do not present a repo as "trending" based on stars alone; confirm activity
  (recent pushes, releases, issues).
- When a repo is also covered by HN/Reddit/X, note the community signal.

## Low-Quality Detection

- Flag repos with empty READMEs, no description, or no recent activity.
- Be suspicious of overnight star jumps from bots or cross-promotion; check
  the contributor and issue history.
- A repo that only repackages another project without attribution should be
  de-prioritized.

## Helper Scripts

- `scripts/github_hot_ai_repos.py` — GitHub Search API across the keywords,
  sorted by stars (fallback ranking).
- `scripts/github_trending_fast_risers.py` — fast-riser ranking: 24h
  activity + trending page fallback.

