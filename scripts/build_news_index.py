#!/usr/bin/env python3
"""Rebuilds news/index.html from the published articles in news/articles/.

The daily cron agent writes article pages (news/articles/YYYY-MM-DD-slug.html),
then runs this script to regenerate the news index page listing every article
newest first, each linked with its original source for attribution.

Usage: python3 build_news_index.py
"""
import json
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
  <link rel="canonical" href="https://zabez.com/news/index.html">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
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


SITE = "https://zabez.com"

FAVICON_BLOCK = (
    '  <link rel="icon" href="/favicon.ico" sizes="32x32">\n'
    '  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">\n'
    '  <link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
)


def repair_article_head(path: Path) -> None:
    """Self-heal a generated article page: fix malformed meta descriptions
    (the daily agent occasionally writes `.</title>` instead of `.">`),
    and inject canonical, favicon links, and NewsArticle JSON-LD if missing."""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    original = raw

    # Broken meta: <meta name="description" content="...</title>  (unterminated)
    raw = re.sub(
        r'(<meta name="description" content="[^"<>]*)</title>\s*',
        r'\1">\n',
        raw,
    )

    url = f"{SITE}/news/articles/{path.name}"
    if 'rel="canonical"' not in raw:
        raw = raw.replace(
            '<link rel="preconnect" href="https://fonts.googleapis.com">',
            f'<link rel="canonical" href="{url}">\n'
            + FAVICON_BLOCK
            + '  <link rel="preconnect" href="https://fonts.googleapis.com">',
            1,
        )

    if "application/ld+json" not in raw:
        title_m = re.search(r"<title>([^<·]+)", raw)
        desc_m = re.search(r'<meta name="description" content="([^"<>]*)"', raw)
        headline = title_m.group(1).strip() if title_m else path.stem
        description = desc_m.group(1).strip() if desc_m else ""
        date = path.stem[:10]
        ld = (
            '  <script type="application/ld+json">\n'
            "  " + json.dumps({
                "@context": "https://schema.org",
                "@type": "NewsArticle",
                "headline": headline,
                "description": description,
                "datePublished": date,
                "dateModified": date,
                "url": url,
                "author": {"@type": "Person", "name": "Kok Jabez", "url": f"{SITE}/"},
                "publisher": {"@type": "Organization", "name": "ZABEZ.com", "url": f"{SITE}/"},
                "image": f"{SITE}/assets/og-cover.png",
            }, ensure_ascii=False) + "\n  </script>\n"
        )
        raw = raw.replace("</head>", ld + "</head>", 1)

    if raw != original:
        path.write_text(raw, encoding="utf-8")
        print(f"repaired head: {path.name}")


def parse_article(path: Path):
    """Extract date, title, original-source URL, and description from an article page."""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    date = re.search(r'class="article-date">([^<]+)<', raw)
    title = re.search(r"<h1>([^<]+)</h1>", raw)
    src = re.search(r'class="article-source"[^>]*href="([^"]+)"', raw)
    desc = re.search(r'<meta name="description" content="([^"<>]*)"', raw)
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

    for p in sorted(ARTICLES.glob("*.html")):
        repair_article_head(p)

    articles = [parse_article(p) for p in sorted(ARTICLES.glob("*.html"))]
    articles.sort(key=lambda a: a["date"], reverse=True)

    # Dedupe: keep only the newest article per story (handles the daily cron
    # occasionally re-covering the same story with a new date or a retitled
    # variant, e.g. "Record-Setting AML Penalty Against UBS" vs the same title
    # with a trailing clause — prefix overlap of one title over another counts
    # as the same story)
    seen_keys = []
    deduped = []
    for a in articles:
        key = re.sub(r"[^a-z0-9]+", " ", a["title"].lower()).strip()[:80]
        if any(key.startswith(s) or s.startswith(key) for s in seen_keys):
            continue
        seen_keys.append(key)
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

    build_sitemap(articles)


# Core pages included in the sitemap alongside the deduped news articles.
# Orphaned duplicate article files are deliberately excluded.
CORE_PAGES = [
    ("", "weekly", "1.0"),
    ("cases/microsoft.html", "monthly", "0.9"),
    ("cases/google.html", "monthly", "0.9"),
    ("cases/jpmorgan.html", "monthly", "0.9"),
    ("cases/aws.html", "monthly", "0.9"),
    ("cases/meta.html", "monthly", "0.9"),
    ("cases/pfizer.html", "monthly", "0.9"),
    ("news/index.html", "daily", "0.8"),
    ("courses/index.html", "monthly", "0.8"),
    ("courses/mastery.html", "monthly", "0.8"),
    ("courses/free/lesson-1.html", "monthly", "0.6"),
    ("courses/free/lesson-2.html", "monthly", "0.6"),
    ("courses/free/lesson-3.html", "monthly", "0.6"),
    ("courses/free/lesson-4.html", "monthly", "0.6"),
    ("courses/free/lesson-5.html", "monthly", "0.6"),
]


def build_sitemap(articles):
    """Regenerate sitemap.xml: core pages + the deduped news articles."""
    today = datetime.now().strftime("%Y-%m-%d")
    entries = []
    for rel, freq, prio in CORE_PAGES:
        entries.append(
            f"  <url><loc>{SITE}/{rel}</loc><changefreq>{freq}</changefreq>"
            f"<priority>{prio}</priority></url>"
        )
    for a in articles:
        lastmod = a["path"].stem[:10] if re.match(r"\d{4}-\d{2}-\d{2}", a["path"].stem) else today
        entries.append(
            f"  <url><loc>{SITE}/news/articles/{a['path'].name}</loc>"
            f"<lastmod>{lastmod}</lastmod><changefreq>yearly</changefreq>"
            f"<priority>0.5</priority></url>"
        )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )
    (BASE / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"Sitemap rebuilt: {len(entries)} URLs -> {BASE / 'sitemap.xml'}")


if __name__ == "__main__":
    sys.exit(main())
