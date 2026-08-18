#!/usr/bin/env python3
"""Rebuilds news/index.html from the published articles in news/articles/.

The daily cron agent writes article pages (news/articles/YYYY-MM-DD-slug.html),
then runs this script to regenerate the news index page listing every article
newest first, each linked with its original source for attribution.

Usage: python3 build_news_index.py
"""
import re
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ARTICLES = BASE / "news" / "articles"
INDEX = BASE / "news" / "index.html"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GRC News, Daily Case Studies · Zabez</title>
  <meta name="description" content="Original GRC case studies written daily: governance, risk, compliance, privacy, and regulatory enforcement, analyzed and rewritten in our own words with sources cited.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/style.css">
  <style>
    .news-list {{ margin-top: 8px; }}
    .news-item {{
      padding: 22px 4px;
      border-bottom: 1px solid var(--line-soft);
      display: grid;
      grid-template-columns: 96px 1fr auto;
      gap: 18px;
      align-items: baseline;
    }}
    .news-date {{ font-family: var(--mono); font-size: 12px; color: var(--gold); letter-spacing: 0.06em; }}
    .news-item h3 {{ font-family: var(--serif); font-weight: 500; font-size: 1.35rem; line-height: 1.3; }}
    .news-item h3 a {{ color: var(--text); }}
    .news-item h3 a:hover {{ color: var(--gold-soft); }}
    .news-src {{ font-family: var(--mono); font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-faint); white-space: nowrap; }}
    .news-desc {{ font-size: 16px; color: var(--text-dim); margin-top: 6px; max-width: 70ch; }}
    .news-foot {{ margin-top: 26px; font-family: var(--mono); font-size: 12px; color: var(--text-faint); }}
    @media (max-width: 640px) {{
      .news-item {{ grid-template-columns: 1fr; gap: 6px; }}
      .news-src {{ grid-column: 1; }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="../index.html">ZABEZ<span class="dot">.</span>com</a>
      <nav class="nav">
        <a href="../index.html#cases"><i data-lucide="search" class="ico"></i>Case Studies</a>
        <a href="../index.html#news">GRC News</a>
        <a href="../index.html#free"><i data-lucide="file-text" class="ico"></i>Free Resources</a>
        <a href="../index.html#about"><i data-lucide="user" class="ico"></i>About</a>
        <a href="../index.html#contact"><i data-lucide="mail" class="ico"></i>Contact</a>
      </nav>
    </div>
  </header>
  <main>
    <section class="case-hero" style="background: var(--green); color: #fff;">
      <div class="wrap">
        <p class="crumb"><a href="../index.html">All case studies</a></p>
        <h1 style="color: #fff;">GRC News, Daily Case Studies</h1>
        <p class="subtitle">
          Original write-ups of the governance, risk, compliance, privacy, and regulatory
          enforcement stories that matter. Published daily, rewritten in our own words,
          with every claim traced back to its source.
        </p>
        <div class="score-strip">
          <span class="tag">Updated {updated}</span>
          <span class="tag">{count} articles</span>
        </div>
      </div>
    </section>
    <section>
      <div class="wrap">
        <div class="news-list">
          {items}
        </div>
        <p class="news-foot">Every article links to its original reporting for attribution. Original analysis by Zabez; not affiliated with the sources.</p>
      </div>
    </section>
  </main>
  <footer>
    <div class="wrap">
      <div class="foot-inner">
        <span>© 2026 Zabez · GRC Portfolio</span>
        <span class="legal">Original analysis based on publicly available reporting, with sources cited in each article.</span>
      </div>
    </div>
  </footer>
<script src="../assets/lucide.min.js"></script>
<script src="../assets/anim.js"></script>
</body>
</html>
"""


def parse_article(path: Path):
    """Extract date, title, original-source URL, and description from an article page."""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    date = re.search(r'class="article-date">([^<]+)<', raw)
    title = re.search(r"<h1>([^<]+)</h1>", raw)
    src = re.search(r'class="article-source"[^>]*href="([^"]+)"', raw)
    desc = re.search(r'<meta name="description" content="([^"]+)"', raw)
    return {
        "path": path,
        "date": date.group(1).strip() if date else path.stem[:10],
        "title": title.group(1).strip() if title else path.stem,
        "src": src.group(1) if src else "",
        "desc": desc.group(1) if desc else "",
    }


def main():
    if not ARTICLES.exists():
        print("No articles directory yet:", ARTICLES)
        return 1

    articles = [parse_article(p) for p in sorted(ARTICLES.glob("*.html"))]
    articles.sort(key=lambda a: a["date"], reverse=True)

    # Dedupe: keep only the newest article per normalized title (handles the
    # daily cron occasionally re-covering the same story with a new date)
    seen_titles = set()
    deduped = []
    for a in articles:
        key = re.sub(r"[^a-z0-9]+", " ", a["title"].lower()).strip()[:80]
        if key in seen_titles:
            continue
        seen_titles.add(key)
        deduped.append(a)
    articles = deduped

    items = []
    for a in articles:
        src_tag = f'<span class="news-src">Source: <a href="{a["src"]}" target="_blank" rel="noopener">original</a></span>' if a["src"] else ""
        desc = f'<p class="news-desc">{a["desc"]}</p>' if a["desc"] else ""
        rel = a["path"].name
        items.append(
            f'<article class="news-item">'
            f'<span class="news-date">{a["date"]}</span>'
            f'<div><h3><a href="articles/{rel}">{a["title"]}</a></h3>{desc}</div>'
            f'{src_tag}'
            f'</article>\n'
        )

    page = TEMPLATE.format(
        updated=datetime.now().strftime("%Y-%m-%d %H:%M"),
        count=len(articles),
        items="".join(items),
    )
    INDEX.write_text(page, encoding="utf-8")
    print(f"Index rebuilt: {len(articles)} articles -> {INDEX}")


if __name__ == "__main__":
    sys.exit(main())
