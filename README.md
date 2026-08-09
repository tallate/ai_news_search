<div align="center">

<img src="ai-news-search/assets/logo.svg" width="110" alt="AI News Search logo" />

# AI News Search · last_7_days_news

**最近 7 天 AI 新闻雷达 —— 多源采集、交叉核验、一键出中文摘要报告**

本仓库的核心是 [`ai-news-search`](ai-news-search/)：一个可直接安装到 Codex / Claude Code 的 AI 新闻检索 Skill，从官方公告、RSS/Folo、GitHub、X/Twitter 与 HN/Reddit 并行采集，输出按主题分组的带链接摘要与趋势。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform: macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)]()

</div>

---

## 快速开始

```bash
git clone https://github.com/<your-name>/last_7_days_news.git
mkdir -p ~/.codex/skills
cp -R last_7_days_news/ai-news-search ~/.codex/skills/
```

然后在 Codex 里直接说：

```text
用 ai-news-search 搜集今天最新的 AI 新闻，按主题分组，给出来源链接和趋势
```

## 目录

- [`ai-news-search/`](ai-news-search/) —— Skill 主目录（完整 README 见 [ai-news-search/README.md](ai-news-search/README.md)）
- `ai-news-search/scripts/` —— 10 个采集与报告脚本
- `ai-news-search/references/` —— X 高信号账号、RSS 源、GitHub 雷达规则

## License

[MIT](LICENSE) © 2026 last_7_days_news contributors

