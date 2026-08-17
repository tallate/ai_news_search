---
name: ai-news-xhs
description: "Turn a verified AI-news brief into a polished Xiaohongshu image-carousel post and prepare it for browser publishing. Use for daily AI morning reports, Xiaohongshu 图文早报, vertical information cards, publish copy, or scheduled Xiaohongshu draft preparation."
---

# AI News Xiaohongshu

Convert `ai-news-search` output into a source-linked Xiaohongshu image carousel. Keep factual text editable in PPTX, render it to PNG, prepare publishing copy, and use the browser to stage the post.

## Inputs and outputs

Require 3–5 verified news items and 1–2 GitHub Radar items. Each item needs a title, URL, source, publication time, summary, importance, and verification status.

Create a dated directory containing:

```text
news.json
slides.pptx
slides/slide-01.png ...
slides-montage.png
publish.md
```

## Workflow

1. Run `ai-news-search` completely, including official/research, public RSS/community, GitHub, authenticated Folo, and X tracks when available.
2. Select one claim per card. Preserve source attribution and uncertainty; separate reported facts from trends.
3. Read Anthropic's `frontend-design` skill from `https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md` before visual planning.
4. Define a subject-specific visual direction: audience, single job, 4–6 named colors, at least two type roles, layout concept, and one signature element. Revise any generic AI-gradient or reusable dashboard answer before building.
5. Use the Presentations skill to create a 9:16 editable PPTX. Render and visually inspect every slide; fix overflow, wrapping, contrast, and inconsistent source labels.
6. Write `publish.md` with a concise title, reader-facing summary, 3–8 hashtags, source links, AI-assistance disclosure, and limitations.
7. Open Xiaohongshu in the visible browser. Let the user handle login, MFA, and CAPTCHA. Upload the ordered PNG files and fill the title/body.
8. Pause immediately before the final Publish action. Show the public title, body, image count, and account destination, then request action-time confirmation. Publish only after confirmation.

## Carousel system

Use 6–8 cards:

- Cover: date and the day's central thesis.
- 3–5 topic cards: claim, why it matters, source, time, and uncertainty.
- GitHub Radar: repository, stars today, total stars, purpose, and metric caveat.
- Takeaway: 3 trends and source/disclosure footer.

Use 1080×1920 PNGs, phone-readable typography, high contrast, and a consistent source position. Favor one canvas composition over dashboard card grids. Let one signature visual device carry the identity; keep other decoration restrained.

## Publishing boundary

Treat browser upload and field entry as draft preparation. Final publication is representational communication and always requires immediate user confirmation. If the login expires, stop at the login page. If no authorized publishing surface is available, return the complete local package without simulating publication through unofficial APIs.

## Quality gate

Complete only when:

- every visible claim is sourced or marked uncertain;
- every slide passes render and overflow inspection;
- carousel order matches `publish.md`;
- no credentials, cookies, callback tokens, or private subscription exports are included;
- the browser is either staged before Publish or the local package clearly records the blocker.
