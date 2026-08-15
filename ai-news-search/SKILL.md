---
name: ai-news-search
description: "Explore and collect today's AI news from multiple sources including official company announcements, RSS/Folo feeds, GitHub hot repos, X/Twitter accounts, and web sources. Use when users ask to search for, collect, summarize, or analyze recent AI news, model/product releases, AI company updates, research papers, open source projects, policy and regulation, or AI industry applications. Provides structured workflows for building daily AI news reports with source links, publication times, importance analysis, and trend identification."
---

# AI News Search

Search and collect today's latest AI news from multiple channels, normalize results, and produce a structured, source-linked summary grouped by topic.

## Overview

This skill searches, organizes, and summarizes AI news from the last 7 days (default window). It covers model/product releases, RSS/Folo subscription signals, GitHub hot repositories, GitHub daily fast-riser projects, AI events/conferences, and X/Twitter discussion signals.

The default output is **not a plain news list** — it is a merged trend brief based on multiple evidence channels. Default structure:

- Hot Topics
- Viewpoints
- Opportunities
- GitHub Radar

## Core Scope

Collect AI news covering:
- Model/product releases (OpenAI, Anthropic, Google DeepMind, Meta AI, NVIDIA, Hugging Face, Mistral, DeepSeek, Qwen, xAI, Cohere, etc.)
- AI company dynamics (funding, hiring, partnerships, strategy)
- Research papers and breakthroughs
- Open source projects and GitHub hot repos
- Policy and regulation
- Industry applications and adoption

## Data Sources

### 1. Official & Primary Sources

**Priority ranking:** Official announcement > breaking news > blog posts > aggregation

- **X/Twitter accounts**: High-signal AI accounts for real-time updates (model releases, company news, papers)
- **RSS/Folo feeds**: Official blogs, newsletters, and popular AI publications
- **Official websites**: OpenAI, Anthropic, Google DeepMind, NVIDIA announcements pages
- **GitHub**: Trending AI repos, stars gained in last 24 hours
- **HN / Reddit**: For community signals and discussion triggers

### 2. Keywords to Search

Cover across: AI, LLM, agent, coding-agent, MCP, RAG, local-model, inference, eval, benchmark, alignment, fine-tuning, open-weights, tools, hardware

### 3. Default Query Families

Use these families, adjusted to the user's time window (default: last 7 days, prioritizing the last 24 hours):

- Recent AI / tech / industry news: `{topic} since:YYYY-MM-DD`
- Official announcements and release notes: official blog/news site search
- arXiv / research: `{topic} arxiv OR site:arxiv.org`
- GitHub: `{keyword} created:>YYYY-MM-DD` / `pushed:>YYYY-MM-DD`
- X/Twitter: `from:{account} since:YYYY-MM-DD` and keyword searches
- HN / Reddit: `site:news.ycombinator.com` / `site:reddit.com`

## Multi-Agent Orchestration

For comprehensive or multi-source requests, use subagents as the default execution model:

1. Split collection into independent source tracks before searching.
2. Inspect the available collaboration capacity and create as many useful subagents as the remaining slots allow. Prefer 2-4 concurrent workers; never create more workers than independent tracks.
3. Give each subagent one bounded track, the user's topic and time window, the normalized item schema, and a completion criterion. Tell it to return findings to the parent rather than writing the final report.
4. Start all workers before waiting. Keep one source family owned by one worker so searches do not duplicate each other.
5. While workers run, let the parent prepare queries, ranking criteria, or cover an unassigned track. The parent owns synthesis.
6. Wait for every worker, follow up once on missing evidence when useful, then merge, deduplicate, cross-check, rank, and write the final response.

Use this default assignment when capacity permits:

- **Official/research worker** — official company pages, primary announcements, papers, reputable public reporting.
- **RSS/community worker** — RSS/Folo, Hacker News, Reddit, practitioner blogs, and corroborating community signals.
- **GitHub worker** — new and fast-rising repositories using `references/github-hot-repos.md` and the bundled scripts.
- **X worker** — only when the request needs social signals and authenticated access is available.

For a narrow request that needs only one source family, search directly without subagents. When subagent tools are unavailable, execute the same tracks with parallel tool calls and continue normally. Report unavailable or failed tracks as coverage limits; do not invent their findings.

### Worker return contract

Require each worker to return:

- coverage window, queries/source families checked, and any access limitation;
- 3-10 normalized candidate items with title, URL, source/author, publication time, summary, engagement when available, category, and importance;
- primary-source status and corroborating links for high-importance claims;
- a short list of duplicates, weak claims, or facts needing parent verification.

A worker is complete only when every returned factual item has a stable source link and timestamp, or is explicitly marked uncertain.

## Collection Tracks

Assign these tracks to subagents using the orchestration above:

### Track 1: Official & Public Sources

1. Check official company announcement pages and blogs for today's releases
2. Search for model/product/paper announcements
3. Include funding, partnership, and hiring news from major AI companies
4. Cross-check against X/Twitter for real-time signals

### Track 2: RSS/Folo Subscriptions

1. Query known RSS subscriptions for new feed items in the last 24 hours
2. Filter for AI-related content using the keywords above
3. Deduplicate using content similarity before aggregating
4. If Folo is unavailable without login, fall back to the feeds listed in `references/ai-radar-sources.md`

### Track 3: GitHub Repository Radar

1. Collect GitHub trending AI repos, ranked by star gain in the last 24 hours
2. Include newly created repositories and top repos with recent activity
3. Search across: AI, LLM, agent, coding-agent, MCP, RAG, local-model, and inference terms
4. Include the repo URL, stars gained today, total stars, description, and why it matters
5. Do NOT rank purely by total stars - combine stars gained in last 24 hours with engagement signals

See `references/github-hot-repos.md` for the full radar rules.

### Track 4: X/Twitter Collection (Optional)

If the user asks for X/Twitter content or social signals:

1. Load account list from `references/x-high-signal-accounts.txt`
2. Validate X cookies first (`scripts/validate_X_cookies.py`); refresh via `scripts/ensure_X_cookies.sh` when needed
3. Collect the first 10-20 high-signal samples from each tracked account
4. Cross-check social posts against public news sources whenever possible
5. Sample order: 2-3 official accounts first, then 1-2 core people, then 2-3 community accounts
6. For news about recent AI trends, prioritize official account timelines over Home feed

### Track 5: Merge, Cross-Check, and Rank the Evidence

After the public-source, RSS/Folo, GitHub, and X tracks finish, merge and rank:

- Merge normalized results across tracks and deduplicate by content similarity.
- Cross-check social claims against public sources; a claim with only one unsupported source must not be presented as fact.
- Rank the merged set by: source quality, freshness, originality, community momentum, engagement, and relevance to the user's ask.
- Produce the final brief only after cross-checking; do not browse without validating.

## Keyword Handling

- Start from the default keyword set (AI, LLM, agent, coding-agent, MCP, RAG, local-model, inference) and broaden based on the user's ask.
- For a user-specified topic, filter items that do not match the topic.
- When the user asks about a specific company/product, prioritize official account timelines and official RSS feeds before community aggregation.
- Use filtered keyword lists for RSS feeds to reduce noise (see "RSS Filtering Keywords").

## X Cookie Rules

- X collection requires a valid cookie file (`x_cookies.json`) when using xgo.ing RSS bridges or browser automation.
- Validate cookies with `scripts/validate_X_cookies.py`; refresh them when expired (typically ~2-3 weeks).
- Never commit cookie files to the repository; keep them out of version control.

## Browser Collection Mode

Use browser mode only when the search API is unavailable or login is needed:

1. Open the search/account page in the browser (`scripts/open_X_login_cdp.sh`).
2. Collect 10-20 high-signal samples per account.
3. Only add accounts when the topic genuinely demands it; don't over-collect.
4. Capture source links, timestamps, and engagement signals.
5. Cross-check browser-mode findings against other tracks.

## Normalization & Deduplication

Normalize each item to contain:
- **title** - Actual news title
- **url** - Source link
- **source** - Source name
- **published_at** - Publication timestamp
- **summary** - 2-3 sentence summary
- **engagement** - Signals if available (stars, likes, retweets)
- **category** - One of: model_release, product, company, research, open_source, policy, application
- **importance** - Low / Medium / High / Critical

Rules:
- Validate a feed item against at least one other source when possible (don't rely on engagement alone)
- If login is needed, use `scripts/export_folo_subscriptions.py` or cookie export helper
- Cross-check social posts against public sources whenever possible
- Rank merged set by: source quality, freshness, originality, community momentum, engagement, and relevance to user's ask

### Data Fields

Each normalized item includes, at minimum:

1. **title** — actual news title
2. **url** — source link
3. **source / author** — source name or author/site
4. **published_at** — publication timestamp
5. **summary** — 2-3 sentence summary
6. **engagement** — stars/likes/retweets when available
7. **category** — model_release, product, company, research, open_source, policy, application
8. **importance** — Low / Medium / High / Critical

Additional rules:
- Keep the window at the last 7 days by default; extend only when the user asks.
- Capture source links, author/title, and engagement signals.
- Deduplicate across sources; drop items that produce no new signal.
- Only include items validated against at least one other source.

## Output Format

Generate structured summary with:

1. **Hot Topics** — Top 3-5 most important news items today
2. **Viewpoints** — Key perspectives, opinions, and community sentiment
3. **Opportunities** — Market trends, partnership angles, adoption signals
4. **GitHub Radar** — Trending repos with star gains in the last 24h
5. **One-page summary** — When the user asks for a summary, or when an executive version with links is needed

For each news item in the summary include:
- Source link
- Publication time
- Why it matters (1-2 sentences)

Finally, identify 3-5 trends worth watching.

### Output Categories

- **Hot Topics**: the 3-5 most important or discussed items; include official announcements, breakthroughs, community momentum, and time-sensitive developments.
- **Viewpoints**: what the community is saying — opinions and sentiment; label opinion vs. fact and attribute where possible.
- **Opportunities**: product/company/integration/collaboration opportunities, adoption signals, open-source, and funding angles.
- **GitHub Radar**: trending repos with repo link, stars gained, total stars, description, and why it matters.
- **One-page summary**: when the user asks for a summary, or when an executive version with links is needed; include the top items with links and a short executive take.

## Output Language

- If the user asks for Chinese output, write the summary in Chinese (中文摘要)
- Group by topic/theme
- Give each news item: source link, publish time, and why it matters
- End with 3-5 trend recommendations

## Ranking Rules

- Rank news items by: source quality, freshness, originality, community momentum, engagement, and relevance to the user's ask.
- Do not rank purely by engagement; cross-check before trusting a number.
- For GitHub repos, rank by 24h star gain combined with engagement, not by total stars alone.

## Ranking Rules For Feed Items

- Prefer official announcement feeds over aggregation feeds.
- De-prioritize items older than the window unless they are still relevant.
- Drop duplicate/derivative coverage once an authoritative source is found.
- Keep items that a user would reasonably want to know; remove pure noise.

## Cross-Check Rules

- Verify any high-importance claim against a second source (official announcement, reputable outlet, or primary evidence).
- Do not present unsupported judgments as hard facts.
- For each conclusion, reference 1-2 supporting source samples.
- Flag uncertainty when official sources do not establish availability, pricing, or behavior.

## RSS Filtering Keywords

Apply these filters to RSS feeds to reduce noise:

- Include: AI, LLM, agent, coding-agent, MCP, RAG, local-model, inference, eval, benchmark, alignment, fine-tuning, open-weights, tools, hardware
- Exclude clearly off-topic content: pure sports, entertainment, politics without an AI angle, generic deals without tech relevance
- For Folo/RSS, prefer feeds that are personalized/curated for AI

## Execution Learnings

**Confirmed wins**

- X popular browsing is more stable and higher-signal than Home feed or plain search.
- Official accounts + core people give the best trend/opportunity signal.
- Folo subscriptions act as a strong personalized radar but need cross-checking with public sources.
- Independent blogs on the HN Popular Blog / LLM layer give early, useful signals.
- GitHub trending combined with engagement checks beats raw star counts.

**Confirmed failure modes**

- Folo feeds are not available without login/cookies; fall back to public RSS.
- Search result order is unreliable; cross-check against official pages.
- Retrying on a single search page can miss content; use multiple query families.
- Unsupported claims without stable source links must not be treated as confirmed facts.
- X collection without valid cookies will fail; validate first.

## X Collection Recommendations

**Recommended**

- Validate cookies first (`scripts/validate_X_cookies.py`).
- Collect 10-20 high-signal samples per account before cross-checking with public news sources.
- Sample order: 2-3 official accounts first, then 1-2 core people, then 2-3 community accounts.
- Add Home feed only when search/filter lacks signal.
- Run random/other search queries when the account list is thin.
- Cross-check X findings against public sources; rank by credibility.
- Generate an HTML report with `scripts/generate_report.py` and the `template.html` when the user wants a shareable artifact.
- For GitHub hot repos, pair the repo link with the related X/news signal.

**Not recommended**

- Do not make browser mode the default; use it only when the API is unavailable.
- Do not use Home feed as the only signal source.
- Do not use long keyword strings as the main search strategy.
- Do not rely on a single source type.
- Do not collect X content into a cluttered, unranked state.
- Do not present conclusions as a single source's view without attribution.

## Report Files

- Generate a one-page Markdown or HTML summary with source links.
- Use `scripts/generate_report.py` (Markdown/HTML) with the collected JSON.
- Use `scripts/template.md` / `scripts/template.html` as the base layout.
- Include: Hot Topics, Viewpoints, Opportunities, GitHub Radar, and trends.

## Quick Decisions

- User wants a quick overview of public news → use the one-page template with the top items and links.
- User wants comprehensive analysis → run all tracks, cross-check, and produce a detailed report.
- User asks about GitHub topics/developer ecosystem → run the GitHub radar track and include repo signals.
- User asks for X/news/social signals → validate cookies, run the X track, and cross-check with public sources.
- Folo/RSS unavailable (no login) → fall back to official pages and public RSS feeds; note the limitation.

## Known Folo Coverage From This Machine

The local Folo database contains a broad AI coverage list: model labs and platforms (OpenAI, Anthropic, Google, DeepMind, Meta AI, NVIDIA, Hugging Face, Mistral, DeepSeek, Qwen, xAI, Cohere, Perplexity, Groq, EleutherAI, Replicate, etc.), researchers and executives (Karpathy, Altman, Amodei, Hassabis, Ng, Fei-Fei Li, Hinton, LeCun, Willison, Mollick, etc.), AI coding and agent tools (Cursor, Cline, LangChain, LlamaIndex, Dify, Windsurf, Bolt/Lovable/Replit, etc.), and lists/newsletters (Last Week in AI, AI Breakfast, The Rundown, AI Engineer, Latent Space, DeepLearning.AI, BAIR, Stanford HAI, arXiv).

See:

- `references/x-high-signal-accounts.txt` — account list exported from Folo
- `references/ai-radar-sources.md` — official feeds and feeds observed in Folo

## Official And Primary RSS Feeds To Add When Missing

When the Folo list is missing or login is unavailable, add:

- OpenAI: https://openai.com/news/
- Anthropic: https://www.anthropic.com/news
- Google DeepMind: https://deepmind.google/discover/blog/
- Meta AI: https://ai.meta.com/blog/
- NVIDIA: https://blogs.nvidia.com/
- Hugging Face: https://huggingface.co/blog
- Mistral AI: https://mistral.ai/news/
- TechCrunch AI / VentureBeat AI / The Verge / MIT Tech Review
- arXiv cs.AI: http://export.arxiv.org/rss/cs.AI

## HN Popular Blog OPML Layer

- Hacker News: https://news.ycombinator.com/rss
- HN Algolia front-page API: https://hn.algolia.com/api/v1/search?tags=front_page
- Practitioner blogs and newsletters that regularly hit the HN front page (Simon Willison, BAIR, Last Week in AI, Latent Space, etc.)

## Scripts

Available helper scripts in `scripts/`:

- `scripts/export_folo_subscriptions.py` - Export Folo RSS subscriptions (placeholder)
- `scripts/export_X_cookies.py` - Export X cookies from Chrome/Edge (macOS)
- `scripts/validate_X_cookies.py` - Validate the X cookie file
- `scripts/ensure_X_cookies.sh` - Validate -> login (CDP) -> export -> validate
- `scripts/open_X_login_cdp.sh` - Open X login in a CDP-enabled browser profile
- `scripts/prepare_X_search.py` - Build X search queries from keywords/accounts
- `scripts/github_hot_ai_repos.py` - Fetch GitHub trending AI repos (keyword sweep)
- `scripts/github_trending_fast_risers.py` - Fast-riser ranking + trending fallback
- `scripts/generate_report.py` - Generate a Markdown/HTML report from items JSON
- `scripts/template.md` / `scripts/template.html` - One-page report templates

## Reference Files

- `references/x-high-signal-accounts.txt` - High-signal X/Twitter accounts (Folo export)
- `references/ai-radar-sources.md` - Official RSS sources and Folo-observed feeds
- `references/github-hot-repos.md` - GitHub radar keywords, ranking, and cross-check rules

## Verification Guideline

- Do NOT present unsupported judgments as hard facts
- Cross-check claims against official sources when possible
- For each conclusion, reference 1-2 supporting source samples
- Use the collection pass to validate, not just to browse
