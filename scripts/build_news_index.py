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
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="../index.html">ZABEZ<span class="dot">.</span>com</a>
      <nav class="nav">
        <a href="../index.html#cases"><i data-lucide="search" class="ico"></i><span>Case Studies</span></a>
        <a href="../index.html#free"><i data-lucide="file-text" class="ico"></i><span>Free Resources</span></a>
        <a href="../index.html#about"><i data-lucide="user" class="ico"></i><span>About</span></a>
        <a href="../index.html#contact"><i data-lucide="mail" class="ico"></i><span>Contact</span></a>
      </nav>
    </div>
  </header>
  <main>
    <section class="case-hero">
      <div class="wrap">
        <p class="crumb"><a href="../index.html">← ZABEZ.com</a></p>
        <h1>GRC News, <em style="font-style:italic;color:var(--gold-dark);">daily</em> case studies</h1>
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
        <p class="news-foot">Every article links to its original reporting for attribution. Original analysis by Zabez; not affiliated with the sources. Illustrations original to ZABEZ.com.</p>
      </div>
    </section>
  </main>
  <footer>
    <div class="wrap">
      <div class="foot-inner">
        <span>© 2026 ZABEZ.com · GRC Portfolio</span>
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



# Topic → illustration mapping for news articles. First match wins; keys are
# regex fragments tested against "title desc filename" lowercased.
TOPIC_IMAGES = [
    ("news-privacy",     r"privacy|gdpr|\bico\b|data protection|consent|surveillance"),
    ("news-aml",         r"\baml\b|money.?launder|fincen|bank secrecy"),
    ("news-sanctions",   r"sanction|ofac|embargo|export control"),
    ("news-breach",      r"breach|injection|vulnerab|exploit|hack|\bflaw\b|exposed|\bcve\b|ransom"),
    ("news-supplychain", r"supply.?chain|third.?party|covered list|vendor risk|transceiver"),
    ("news-ai",          r"\bai\b|artificial intelligence"),
    ("news-cloud",       r"\bcloud\b|fedramp|\bsaas\b|azure|\baws\b"),
    ("news-standards",   r"standard|\biso\b|etsi|\bcra\b|framework|certification"),
    ("news-health",      r"health|hipaa|pharma|\bfda\b|medical|\bgxp\b"),
    ("news-government",  r"pentagon|defen[cs]e|cmmc|military|federal|\bfcc\b|govern"),
    ("news-crypto",      r"crypto|bitcoin|digital asset|exchange"),
]
TOPIC_FALLBACK = "news-regulatory"


def topic_image(title, desc, filename):
    """Pick the branded illustration that fits a news story."""
    if re.search(r"\bai\b|artificial intelligence", title.lower()):
        return "news-ai"
    hay = f"{title} {desc} {filename}".lower()
    for image, pattern in TOPIC_IMAGES:
        if re.search(pattern, hay):
            return image
    return TOPIC_FALLBACK


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

    # Topic illustration: og:image for link sharing + in-page hero art
    title_m = re.search(r"<title>([^<\u00b7]+)", raw)
    desc_m = re.search(r'<meta name="description" content="([^"<>]*)"', raw)
    img = topic_image(title_m.group(1) if title_m else "", desc_m.group(1) if desc_m else "", path.name)
    img_url = f"{SITE}/assets/img/{img}.jpg"
    if 'property="og:image"' not in raw:
        raw = raw.replace(
            "</head>",
            f'  <meta property="og:title" content="{(title_m.group(1).strip() if title_m else path.stem)}">\n'
            f'  <meta property="og:image" content="{img_url}">\n'
            f'  <meta name="twitter:card" content="summary_large_image">\n</head>', 1)
    if "article-hero-img" not in raw and '<section class="case-body">' in raw:
        raw = raw.replace(
            '<section class="case-body">',
            f'<div class="wrap"><div class="article-hero-img"><img src="../../assets/img/{img}.jpg" alt="" loading="lazy"></div></div>\n\n    <section class="case-body">', 1)

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
        "img": topic_image(
            title.group(1) if title else "",
            desc.group(1) if desc else "",
            path.name,
        ),
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
    seen_srcs = set()
    deduped = []
    for a in articles:
        key = re.sub(r"[^a-z0-9]+", " ", a["title"].lower()).strip()[:80]
        if any(key.startswith(s) or s.startswith(key) for s in seen_keys):
            continue
        if a["src"] and a["src"] in seen_srcs:
            continue
        seen_keys.append(key)
        if a["src"]:
            seen_srcs.add(a["src"])
        deduped.append(a)
    articles = deduped

    items = []
    for a in articles:
        src_tag = f'<span class="news-src">Source: <a href="{a["src"]}" target="_blank" rel="noopener">original</a></span>' if a["src"] else ""
        desc = f'<p class="news-desc">{a["desc"]}</p>' if a["desc"] else ""
        rel = a["path"].name
        items.append(
            f'<article class="news-item reveal">'
            f'<a class="news-thumb" href="articles/{rel}"><img src="../assets/img/{a["img"]}.jpg" alt="" loading="lazy"></a>'
            f'<div><span class="news-date">{a["date"]}</span>'
            f'<h3><a href="articles/{rel}">{a["title"]}</a></h3>{desc}</div>'
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
    inject_homepage_latest(articles)


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


def inject_homepage_latest(articles):
    """Refresh the three newest stories on the homepage between the
    NEWS:LATEST markers, as image cards."""
    home = BASE / "index.html"
    if not home.exists():
        return
    raw = home.read_text(encoding="utf-8")
    start, end = "<!-- NEWS:LATEST:START -->", "<!-- NEWS:LATEST:END -->"
    if start not in raw or end not in raw:
        return
    cards = []
    for i, a in enumerate(articles[:3]):
        delay = f" reveal-d{i}" if i else ""
        cards.append(
            f'<a class="news-card reveal{delay}" href="news/articles/{a["path"].name}">'
            f'<div class="card-img"><img src="assets/img/{a["img"]}.jpg" alt="" loading="lazy"></div>'
            f'<div class="card-body"><span class="card-kicker"><span>{a["date"]}</span></span>'
            f'<h3>{a["title"]}</h3>'
            f'<p>{a["desc"][:150]}{"…" if len(a["desc"]) > 150 else ""}</p></div></a>'
        )
    block = start + "\n          " + "\n          ".join(cards) + "\n          " + end
    raw = raw[:raw.index(start)] + block + raw[raw.index(end) + len(end):]
    home.write_text(raw, encoding="utf-8")
    print(f"homepage: {min(3, len(articles))} latest stories injected")


if __name__ == "__main__":
    sys.exit(main())

