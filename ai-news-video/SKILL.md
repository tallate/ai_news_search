---
name: ai-news-video
description: "Turn a structured AI-news brief into narrated vertical slide video content: create editable PPTX information cards, render slide images, generate a narration script and TTS audio, align subtitles, and compose a review-ready 9:16 MP4. Use when users want daily AI news converted into short-form video for WeChat, Xiaohongshu, or similar personal publishing. Keep publishing manual unless the user explicitly requests and has authorized an official publishing integration."
---

# AI News Video

Convert verified AI-news items into an editable slide deck and a narrated short video. Treat the PPTX as the source of truth for visible facts; render it to images for the final video so titles, numbers, repository names, and citations remain exact.

## Inputs and outputs

Accept either the output of `ai-news-search` or a user-supplied structured brief. Require, for each selected item, a title, URL, source, publication time, short summary, category, importance, and verification status. Keep unsupported claims out of the script.

Create a dated output directory containing:

```text
news.json          # selected, normalized items
script.txt         # narration with slide markers
slides.pptx        # editable 9:16 source deck
slides/            # rendered slide PNGs
narration.mp3      # TTS output
subtitles.srt      # timed captions
video.mp4          # review-ready vertical video
publish.md         # title, caption, hashtags, source links, limitations
review.html        # optional local review page with assets and checks
```

## Workflow

1. **Select and fact-check.** Choose 3–5 items for a 45–90 second video. Prefer primary sources, preserve publication times, and label uncertainty. Build a compact data object before writing copy.
2. **Write the narrative.** Use this order unless the user requests another format: hook/cover, 2–3 hot-topic cards, GitHub radar or trend card, takeaway, sources/end card. Keep one idea per slide. Write spoken Chinese that sounds natural at approximately 2.5–3.5 Chinese characters per second. Mark each slide with `[S01]`, `[S02]`, etc.
3. **Build the PPTX.** Load the `presentations` skill and follow its local PowerPoint workflow. Use a 9:16 portrait canvas, native text for all facts, high contrast, a restrained visual system, and source notes for externally sourced claims. Use at least 50pt titles, 35pt slide titles, 24pt subheads, and 16pt body text unless a supplied template requires otherwise. Keep each slide readable on a phone; shorten copy instead of shrinking type.
4. **Render and inspect.** Render every slide to PNG, inspect individual slides at full size, run slide overflow checks, and fix clipping, wrapping, overlap, or unreadable text before making the video. Never use generative video to redraw factual text.
5. **Generate audio.** Use a configured TTS provider. Doubao voice is an optional default for Chinese narration; use its long-text or emotion-capable endpoint when credentials and service access are available. Keep API keys outside files and environment logs. If TTS is unavailable, return the script and mark audio/video incomplete.
6. **Align subtitles.** Prefer provider timestamps or forced alignment from the final narration audio. Generate an SRT whose cues follow slide markers and never cover key card text. Check that the final spoken text matches the approved script.
7. **Compose the MP4.** Use the rendered slide PNGs as the visual track, hold each slide for its narration segment, add the narration, optional low-volume licensed music, and burned-in captions. Export H.264/AAC, 1080×1920, 30 fps, with no watermark added by this workflow.
8. **Prepare publishing copy.** Generate a short title, platform-specific caption, 3–8 hashtags, source links, and a limitations note. Keep the final state as a review package. Upload or publish only through an explicitly authorized official integration.

## Slide system

Use a consistent five-part deck:

- **Cover:** date, promise, and one strong visual cue.
- **Topic cards:** one claim, one key number, one “why it matters” sentence, and a small source label.
- **Radar card:** repository/project, star change, total stars, language or use case, and caveat when metrics are snapshots.
- **Takeaway:** 2–3 trends or implications, clearly separated from reported facts.
- **Sources:** short URLs or source names, time window, and AI-generated-content disclosure when appropriate.

Use deterministic HTML/SVG or native slide elements for charts, labels, and numbers. Use image generation or stock assets only for decorative backgrounds or illustrations, and record their provenance. Do not copy the reference image's logo, account identity, or copyrighted artwork.

## Provider choices

- **Narrative model:** use the existing AI-news workflow or another model to summarize only supplied, verified items.
- **TTS:** Doubao is recommended when Chinese voice quality, emotion, or a custom voice is important; any compatible TTS provider is acceptable behind the same `narration.mp3` contract.
- **Video composition:** use FFmpeg or Remotion after slide rendering. The composition layer must not alter slide text.
- **Publishing:** generate drafts and assets first. WeChat public-account drafts may be automated only with the account's official credentials and approved API scope. Treat Xiaohongshu personal publishing as manual unless an approved official or partner API is available.

## Quality gate

Complete the run only when:

- every visible factual claim has a source link or an uncertainty label;
- the PPTX opens and every slide passes render/overflow inspection;
- narration, subtitles, and slide order agree;
- the MP4 is 1080×1920, has audible speech, and plays from start to finish;
- `publish.md` contains title, caption, hashtags, sources, and limitations;
- no credentials, cookies, private voice samples, or temporary files are included in the output package.

If any gate fails, return the failed artifact and a concise fix list instead of presenting the package as publish-ready.
