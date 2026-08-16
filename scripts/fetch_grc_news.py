#!/usr/bin/env python3
"""
GRC Daily News Aggregator
=========================
Fetches GRC-relevant news from curated RSS/Atom feeds, filters by governance/risk/
compliance keywords, dedupes, and writes:
  1. ~/projects/grc-portfolio/news/index.html  ,  the site's news page (static, regenerated)
  2. ~/projects/grc-portfolio/news/news.json    ,  machine-readable latest items
  3. stdout (markdown digest)                   ,  for the daily cron delivery

Usage:  python3 fetch_grc_news.py [--days N] [--limit M]
"""
import json
import re
import sys
import time
import html
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
NEWS_DIR = BASE / "news"
NEWS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- feeds
FEEDS = [
    ("The Hacker News",         "https://feeds.feedburner.com/TheHackersNews"),
    ("SC Media",                "https://www.scmagazine.com/feed"),
    ("Infosecurity Magazine",   "https://www.infosecurity-magazine.com/rss/news/"),
    ("Help Net Security",       "https://www.helpnetsecurity.com/feed/"),
    ("Compliance Week",         "https://www.complianceweek.com/rss"),
    ("CSO Online",              "https://feeds.feedburner.com/CSOonline"),
    ("CyberScoop",              "https://www.cyberscoop.com/feed/"),
    ("Cybersecurity Dive",      "https://www.cybersecuritydive.com/feeds/news/"),
    ("DataBreachToday",         "https://www.databreachtoday.com/rss-feeds"),
    ("CISA Advisories",         "https://www.cisa.gov/cybersecurity-advisories/all.xml"),
    ("SEC Press Releases",      "https://www.sec.gov/news/pressreleases.rss"),
    ("Krebs on Security",       "https://krebsonsecurity.com/feed/"),
    ("The Register - Security", "https://www.theregister.com/security/headlines.atom"),
    ("Google AI Blog",          "https://blog.google/technology/ai/rss/"),
    ("Risky Business",          "https://www.risky.biz/feeds/risky-business"),
    ("Compliance.ai",           "https://www.compliance.ai/feed"),
]

# ---------------------------------------------------------------- keywords
# CORE keywords: title alone qualifies as GRC-relevant (strong signal)
CORE_KEYWORDS = [
    # governance / risk / compliance core
    "grc", "governance", "compliance", "risk management", "risk assessment",
    "risk register", "third-party risk", "tprm", "vendor risk", "enterprise risk",
    # frameworks & standards
    "iso 27001", "iso27001", "soc 2", "soc2", "nist", "cobit", "fedramp",
    "pci dss", "hipaa", "hitrust", "ccpa", "cpra", "lgpd", "glba", "sox 404",
    "cis controls", "coso",
    # privacy & data protection
    "gdpr", "privacy", "data protection", "data privacy", "data subject",
    "cookie consent", "data residency", "data localization",
    # regulatory & enforcement
    "regulator", "regulation", "enforcement", "penalty", "sanction",
    "consent order", "settlement", "lawsuit", "litigation", "indictment",
    "eu ai act", "ai act", "digital markets act", "digital services act",
    "dora", "nis2", "cyber resilience act", "cmmc", "ai governance",
    "responsible ai", "board of directors", "cyber insurance", "attestation",
    # enforcement language (SEC/DOJ/regulator actions)
    "charges", "charged", "fined", "fines", "court rules",
    "court blocks", "sues", "sued", "proposes", "proposal", "finalizes",
    "crackdown", "crackdowns", "indicts", "indicted", "settles", "settled",
    "suspended", "revokes", "bans ", "banned", "order ",
    # regulator bodies
    "ftc", "edpb", "sec fines", "ico ", "cnil", "garante", "dpc ",
    "hhs", "cfpb", "finra", "occ ", "ecb ", "europol", "fbi", "doj",
    # audit & control
    "audit", "auditor", "internal audit", "certification", "access control",
    "iam", "identity and access",
]

# SECONDARY keywords: only qualify when combined with a CORE keyword in same title
SECONDARY_KEYWORDS = [
    "breach", "data breach", "ransomware", "fine", "vulnerability",
    "incident response", "exposed", "leak", "security", "cyber", "hack",
    "penalty", "violation", "fraud", "malware",
]

SKIP_PATTERNS = [
    r"advertorial", r"sponsored", r"webinar", r"white paper", r"ebook",
    r"cve-2026-\d{4,}", r"^patch", r"weekly newsletter", r"malware steals",
    r"macos malware", r"go-based", r"android malware", r"call centers",
    r"bank cards", r"nfc relay",
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36 GRCNewsAggregator/1.0"


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def parse_feed(xml_text: str):
    """Parse RSS 2.0 or Atom into list of (title, link, date_str)."""
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items
    # Atom
    entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")
    for e in entries:
        title = e.findtext("{http://www.w3.org/2005/Atom}title") or ""
        link_el = e.find("{http://www.w3.org/2005/Atom}link")
        link = link_el.get("href") if link_el is not None else ""
        date = e.findtext("{http://www.w3.org/2005/Atom}updated") or \
               e.findtext("{http://www.w3.org/2005/Atom}published") or ""
        items.append((title.strip(), link.strip(), date.strip()))
    # RSS 2.0
    for item in root.findall(".//item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        date = item.findtext("pubDate") or item.findtext("dc:date") or ""
        items.append((title.strip(), link.strip(), date.strip()))
    return items


def parse_date(s: str):
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M %z",
                "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%d"):
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    return None


def normalize_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", t.lower())


def is_grc_relevant(title: str) -> bool:
    tl = title.lower()
    if any(re.search(p, tl) for p in SKIP_PATTERNS):
        return False
    # Core keyword match qualifies on its own
    if any(k in tl for k in CORE_KEYWORDS):
        return True
    # Secondary keyword matches only qualify alongside a core keyword
    if any(k in tl for k in SECONDARY_KEYWORDS):
        return any(k in tl for k in CORE_KEYWORDS)
    return False


def main():
    days = 2
    limit = 40
    args = sys.argv[1:]
    if "--days" in args:
        days = int(args[args.index("--days") + 1])
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])

    cutoff = datetime.now() - timedelta(days=days)
    seen = {}
    errors = []

    for name, url in FEEDS:
        try:
            xml_text = fetch(url)
            for title, link, datestr in parse_feed(xml_text):
                if not title or not link:
                    continue
                if not is_grc_relevant(title):
                    continue
                dt = parse_date(datestr)
                if dt is None:
                    dt = datetime.now()
                if dt.tzinfo is not None:
                    dt = dt.replace(tzinfo=None)
                if dt < cutoff:
                    continue
                key = normalize_title(title)
                if key in seen:
                    continue
                seen[key] = {
                    "title": html.unescape(re.sub(r"<[^>]+>", "", title)).strip(),
                    "link": link,
                    "source": name,
                    "date": dt.strftime("%Y-%m-%d"),
                }
        except Exception as e:  # noqa: BLE001
            errors.append(f"{name}: {e}")

    items = sorted(seen.values(), key=lambda x: x["date"], reverse=True)

    # Cap per-source so one prolific feed can't dominate the digest
    source_count = {}
    balanced = []
    for it in items:
        src = it["source"]
        if source_count.get(src, 0) >= 4:
            continue
        source_count[src] = source_count.get(src, 0) + 1
        balanced.append(it)
        if len(balanced) >= limit:
            break
    items = balanced[:limit]

    # ---- write news.json ----  (collector only; the daily cron agent
    # regenerates news/index.html after publishing rewritten articles)
    (NEWS_DIR / "news.json").write_text(
        json.dumps({"generated": datetime.now().isoformat(timespec="seconds"),
                    "count": len(items), "items": items}, indent=2))

    # ---- stdout: markdown digest for cron delivery ----
    print(f"# GRC News Digest, {datetime.now().strftime('%A, %B %d, %Y')}\n")
    print(f"**{len(items)} items** from {len(FEEDS)} sources (last {days} days)\n")
    for it in items:
        print(f"- **[{it['source']}]** {it['title']}\n  {it['link']}")
    if errors:
        print(f"\n⚠️ {len(errors)} feeds failed: {', '.join(e.split(':')[0] for e in errors)}")
    print(f"\nRaw items saved to: {NEWS_DIR / 'news.json'}")


if __name__ == "__main__":
    main()
