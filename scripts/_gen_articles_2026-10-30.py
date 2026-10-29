#!/usr/bin/env python3
"""Generate GRC news articles for 2026-10-30."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "news" / "articles"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · GRC Daily Case Study · Zabez</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://zabez.com/news/articles/{slug}.html">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/style.css">
  <style>
    .article-date {{ font-family: var(--mono); font-size: 12.5px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--gold); }}
    .article-source {{ font-family: var(--mono); font-size: 12px; color: var(--text-faint); }}
    .article-body {{ max-width: 72ch; }}
    .article-body h2 {{ font-family: var(--serif); font-weight: 500; font-size: 1.4rem; margin: 34px 0 12px; }}
    .article-body p {{ margin-bottom: 17px; color: var(--text-dim); font-size: 17px; line-height: 1.75; }}
    .article-body p strong {{ color: var(--text); font-weight: 600; }}
  </style>
  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "NewsArticle", "headline": "{title}", "description": "{desc}", "datePublished": "2026-10-30", "dateModified": "2026-10-30", "url": "https://zabez.com/news/articles/{slug}.html", "author": {{"@type": "Person", "name": "Kok Jabez", "url": "https://zabez.com/"}}, "publisher": {{"@type": "Organization", "name": "ZABEZ.com", "url": "https://zabez.com/"}}, "image": "https://zabez.com/assets/og-cover.png"}}
  </script>
  <meta property="og:title" content="{title}">
  <meta property="og:image" content="https://zabez.com/assets/img/{img}">
  <meta name="twitter:card" content="summary_large_image">
</head>
<body>

  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="../../index.html">ZABEZ<span class="dot">.</span>com</a>
      <nav class="nav">
        <a href="../../index.html#cases"><i data-lucide="search" class="ico"></i>Case Studies</a>
        <a href="../index.html">GRC News</a>
        <a href="../../index.html#free"><i data-lucide="file-text" class="ico"></i>Free Resources</a>
        <a href="../../index.html#about"><i data-lucide="user" class="ico"></i>About</a>
        <a href="../../index.html#contact"><i data-lucide="mail" class="ico"></i>Contact</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="case-hero">
      <div class="wrap">
        <p class="crumb"><a href="../index.html">← All GRC case studies</a></p>
        <span class="article-date">{date}</span>
        <span class="article-date" style="color: var(--text-faint);">By Kok Jabez</span>
        <h1>{title}</h1>
        <p class="subtitle">{desc}</p>
        <div class="score-strip">
          <span class="article-source">Source: <a href="{url}" target="_blank" rel="noopener">{source}</a></span>
        </div>
      </div>
    </section>

    <div class="wrap"><div class="article-hero-img"><img src="../../assets/img/{img}" alt="" loading="lazy"></div></div>

    <section class="case-body">
      <div class="wrap" style="max-width: var(--wrap);">
      <div class="case-main article-body">
{body}

        <p class="ref-note" style="margin-top:26px;"><strong>Attribution:</strong> Analysis based on <a href="{url}" target="_blank" rel="noopener">{source}</a> and related public reporting. This article is original commentary, not a repost of the source material.</p>

        <div class="next-case">
          <span>
            <span class="nc-lbl">More daily case studies</span><br>
            <a class="nc-name" href="../index.html">← Back to GRC News</a>
          </span>
        </div>

      </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="wrap">
      <div class="foot-inner">
        <span>© 2026 ZABEZ.com · GRC Portfolio</span>
        <span class="legal">Original analysis based on publicly available reporting, with the source cited above.</span>
      </div>
    </div>
  </footer>

  <script src="../assets/lucide.min.js"></script>
  <script src="../assets/anim.js"></script>
</body>
</html>
"""


def body(*blocks):
    out = []
    for tag, text in blocks:
        if tag == "h2":
            out.append(f"        <h2>{text}</h2>")
        else:
            out.append("        <p>\n        " + text.strip() + "\n        </p>")
    return "\n".join(out)


ARTICLES = []

# ---------------------------------------------------------------- 1. ICO
ARTICLES.append(dict(
    slug="2026-10-30-ico-reprimand-staffordshire-police",
    title="ICO Reprimands Staffordshire Police for Disclosing a Victim's Address",
    desc="The ICO reprimanded Staffordshire Police after a protection notice sent to an abuser contained the victim's new home address. No fine was issued.",
    date="October 30, 2026",
    url="https://www.infosecurity-magazine.com/news/ico-reprimand-staffordshire-police/",
    source="Infosecurity Magazine",
    img="news-privacy.jpg",
    blocks=[
        ("h2", "What happened"),
        ("p", """The UK Information Commissioner's Office issued a reprimand to Staffordshire Police on 28 October over an incident from March 2024. The force had served a Domestic Violence Protection Notice on a man identified as P, on his release from prison, to protect the victim of his abuse. The notice included the victim's home address, which had not previously been known to P."""),
        ("p", """The reprimand explains why that mattered. The ICO learned of allegations that P had subjected the victim to physical and emotional abuse over several years, forcing her to relocate repeatedly. In that context, it said, her current address was highly sensitive information and should have been handled as such."""),
        ("p", """The ICO found the force had failed to put in place appropriate measures to prevent the disclosure, citing poor completion rates for mandatory training in data protection and in issuing DVPNs. It did not fine the force. It pointed to improvements since the incident: higher training completion, new leadership roles for domestic abuse cases, new procedures and new technology for supporting victims."""),
        ("p", """Sally-Anne Poole, the ICO's head of investigations, said the case is a reminder of getting the basics right, and that organisations must protect the personal information in their care especially where there is a known risk to someone's safety. The regulator had warned in 2023 about this exact risk, noting seven reprimands over the previous 14 months."""),
        ("h2", "Why this is a GRC story"),
        ("p", """<strong>Training completion is a control metric until it becomes a finding.</strong> Most organisations report mandatory training completion in a management pack and it rarely changes a decision. Here the regulator used the completion rate as evidence that appropriate measures were not in place, which turns a soft dashboard number into a documented failure."""),
        ("p", """<strong>Template design is a data protection control.</strong> A protection notice is a standard document with populated fields, and somewhere an address field was filled that should never have been filled for this recipient. Data minimisation is usually discussed at collection, and this case shows it matters at disclosure too, where the recipient is the specific threat."""),
        ("p", """<strong>A reprimand is an enforcement outcome, not an acquittal.</strong> The ICO weighed remediation against penalty and chose the lighter path, but the finding of unlawful handling stands. The pattern worth copying is that documented, verifiable fixes carried more weight than arguments about intent."""),
        ("p", """<strong>Safety critical data needs its own label.</strong> Information about a person at known risk of physical harm is not ordinary personal data, and pushing it through a generic workflow is how mistakes travel. Classification schemes that stop at confidential and restricted tend to miss this entirely."""),
        ("h2", "What to watch"),
        ("p", """Whether the ICO moves from reprimands to penalties in a repeat sector. The 2023 warning followed by another policing incident suggests the lighter tool remains the default. The internal question is whether your templates get field level review before third party disclosures, and whether you can show who approved the last ten."""),
    ],
))

# ---------------------------------------------------------------- 2. SEC
ARTICLES.append(dict(
    slug="2026-10-30-sec-false-filings-crypto-fraud",
    title="SEC Says False Filings Were the Sales Material in a $130 Million Scheme",
    desc="The SEC charged two Colorado-incorporated entities with using false Form ADV and Form D filings to make a $130 million crypto scheme look legitimate.",
    date="October 30, 2026",
    url="https://www.sec.gov/newsroom/press-releases/2026-110-two-entities-charged-130-million-fraud-scheme-used-false-sec-filings-boost-investor-confidence",
    source="SEC Press Releases",
    img="news-crypto.jpg",
    blocks=[
        ("h2", "What happened"),
        ("p", """The Securities and Exchange Commission charged two foreign operated, Colorado incorporated entities, BG Wealth Sharing Ltd and DSJ Exchange Pty Ltd, over a scheme that raised more than $130 million from tens of thousands of retail investors. The complaint was filed in the Northern District of California and covers conduct from at least October 2025 through June 2026."""),
        ("p", """According to the SEC, the pair sold a supposed wealth sharing programme with promises of extraordinary, risk free returns generated by trading signals for crypto asset trading. BG Wealth claimed to be the world's largest hedge fund, registered with the SEC as an investment adviser, and partnered with a licensed and secure crypto platform. The regulator says none of that was true, and that the defendants created the appearance of legitimacy by submitting false Form ADV and Form D filings. Those filings are publicly viewable, and the complaint says they were shown to investors as proof that the SEC had approved the business."""),
        ("p", """The outreach was deliberate: social media, encrypted messaging, weekly live videoconferences and a mobile app. The complaint alleges the defendants displayed fake certificates bearing the SEC seal and made periodic payments to some investors, a Ponzi like tactic, while misappropriating the rest. Laura D'Allaird, who leads the SEC's Cyber and Emerging Technologies Unit, said the scheme was well planned and built to keep investors engaged."""),
        ("p", """The complaint charges both entities under the antifraud provisions of the Securities Act of 1933 and the Securities Exchange Act of 1934, and charges BG Wealth under sections 204(a) and 207 of the Investment Advisers Act of 1940. The SEC seeks injunctions, disgorgement with prejudgment interest and civil penalties. Its investor education office has warned that scammers use exempt reporting adviser filings to imply SEC approval."""),
        ("h2", "Why this is a GRC story"),
        ("p", """<strong>A filing is a notice, not a licence.</strong> Form ADV and Form D record that a submission was made. Nothing about their existence speaks to whether the business is real, and the scheme worked because investors treated a public record as a regulatory stamp."""),
        ("p", """<strong>Marketing approval is a compliance control.</strong> Claims about registration, assets under management and regulated partnerships all passed through someone's review before reaching investors. Where that review does not demand evidence for each specific claim, marketing becomes an uncontrolled channel for misrepresentation."""),
        ("p", """<strong>The partner claim is a third party risk question.</strong> One entity was presented as a licensed and secure platform. Repeat a partner's licensing claims in your own materials and you have adopted them as your own. Verification has to reach the regulator's register, not a screenshot."""),
        ("p", """<strong>Payments as evidence of legitimacy.</strong> Early payouts are the oldest trust mechanic in fraud and they work on sophisticated people too. The lesson is procedural: verification has to happen before funds move, not after the first payment arrives."""),
        ("h2", "What to watch"),
        ("p", """Whether the court freezes assets or appoints a receiver, since recovery usually turns on the first filing. The check any compliance team can run in minutes is to read an adviser's Form ADV on the SEC register rather than counting filings, and to require the same of any partner whose licence you intend to repeat."""),
    ],
))

# ---------------------------------------------------------------- 3. VMware
ARTICLES.append(dict(
    slug="2026-10-30-vmware-esx-audit-logging-kev",
    title="A 2.7 Severity VMware Flaw Lands on CISA's Exploited List Because It Erases the Audit Trail",
    desc="CISA added CVE-2026-41709, a VMware ESX logging flaw, to its exploited vulnerabilities list after a China-linked group used it to hide activity.",
    date="October 30, 2026",
    url="https://thehackernews.com/2026/10/china-linked-hackers-exploited-vmware.html",
    source="The Hacker News",
    img="news-cloud.jpg",
    blocks=[
        ("h2", "What happened"),
        ("p", """CISA added CVE-2026-41709, a flaw in Broadcom's VMware ESX, to its Known Exploited Vulnerabilities catalog on Wednesday, after CrowdStrike reported that a China linked threat actor tracked as Warp Panda had weaponised it in attacks against the US legal sector. The vulnerability is described as insufficient logging, which could let an actor with admin access perform certain operations without those operations being recorded. Its CVSS score is 2.7."""),
        ("p", """Broadcom published an advisory in July 2026 stating the issue was fixed in VMware Cloud Foundation SXi-9.1.0.0-25370933 and ESXi-9.0.2.0100-25595025, in vSphere Foundation at the same versions, in ESX build ESXi80U3j-25429389, in Cloud Foundation 5.2.4 and in Telco Cloud Platform."""),
        ("p", """The exploitation detail comes from CrowdStrike's 2026 Legal Threat Landscape Report, which said Warp Panda used the flaw as a zero day in early 2026 to reduce audit trail visibility. The group, also tracked as Armory Castle, Clay Typhoon and VerdantBamboo, has a history of weaponising zero days in Citrix NetScaler and Ivanti Connect Secure appliances. Its pattern is to enter through internet facing edge devices, pivot into vCenter and deploy custom malware such as BRICKSTORM and SharpStorm. Some intrusions harvested cloud session tokens to reach Microsoft 365 without credential alerts, and in at least one case the actor registered a new multi factor authentication device so access would survive a password reset. Mandiant this month also attributed to the group a critical BeyondTrust Remote Support flaw."""),
        ("h2", "Why this is a GRC story"),
        ("p", """<strong>A low score does not mean a low priority.</strong> A 2.7 does not move on a CVSS driven triage queue. What moves it is the exploited in the wild signal, which is what assessors actually ask about: how fast do you remediate known exploited vulnerabilities, and can you evidence it. Severity scoring answers a different question from active exploitation."""),
        ("p", """<strong>The failure is invisible in the system that failed.</strong> A logging flaw produces no alert, because the missing evidence is the alert. Monitoring that relies only on hypervisor logs inherits the gap. Detection has to sit somewhere the attacker did not reach, which in practice means network, identity and endpoint telemetry in a platform with separate credentials and separate retention."""),
        ("p", """<strong>Admin access is not a trust boundary.</strong> The flaw requires admin rights, which is often used to argue lower risk. In these intrusions, reaching hypervisor admin is a routine step, and treating administrative access as inherently trustworthy removes the control that would have caught it. Immutable log storage is the compensating measure, and it is the one most often skipped on cost."""),
        ("p", """<strong>MFA enrolment belongs in the change record.</strong> Registering a new authentication factor is a privileged change. Where that action generates no reviewable event, persistence outlives the incident response. Governance of authentication factors deserves a line of its own in access management policy, next to joiner, mover and leaver."""),
        ("h2", "What to watch"),
        ("p", """Whether CISA sets a remediation deadline for federal agencies, and whether CrowdStrike publishes indicators defenders can hunt with. The test for everyone else is short: can you produce hypervisor logs for the last 90 days from a system your virtualisation administrators cannot modify, and can you show who approved the last MFA device they enrolled."""),
    ],
))

# ---------------------------------------------------------------- 4. GitHub CI/CD
ARTICLES.append(dict(
    slug="2026-10-30-github-issues-cicd-supply-chain",
    title="Hidden Commands in GitHub Issues Turned 61 Public Repos into a Supply Chain Target",
    desc="Researchers found 83 attacks against 61 public GitHub repositories, with malicious commands hidden in HTML comments that triggered CI workflows.",
    date="October 30, 2026",
    url="https://www.theregister.com/security/2026/10/29/attackers-turn-github-issues-into-supply-chain-campaign-against-61-public-repos-in-less-than-an-hour/5306153",
    source="The Register",
    img="news-supplychain.jpg",
    blocks=[
        ("h2", "What happened"),
        ("p", """Researchers at Radware identified at least 83 attacks against 61 public GitHub repositories, including well known projects such as Google LangExtract, Trivy, Brave browser and MLflow, in what they suspect was a coordinated campaign to run commands in CI/CD environments and steal credentials and access tokens. They shared the findings with The Register."""),
        ("p", """The campaign was fast: 77 of the malicious items appeared inside a 43 minute window on 1 September, with six more within the following two minutes. The attacker used 74 GitHub accounts, many with legitimate development histories, which the researchers say suggests those accounts were compromised rather than created for the job."""),
        ("p", """The attack chain is what makes it notable. Malicious commands were hidden inside HTML comments in issues, pull requests and comments, so the payload did not appear on the rendered page. Where a repository is configured to respond to that event, a workflow fires automatically, within about a second according to researcher Gabi Nakibly. If the workflow incorporates attacker controlled content into shell source, the hidden command runs, collects environment variables and sends them to an attacker controlled server."""),
        ("p", """The researchers found the campaign while investigating prompt injection on GitHub. Their judgement is that the goal was a supply chain attack: take repository credentials, change the code, and push the change to everyone downstream."""),
        ("h2", "Why this is a GRC story"),
        ("p", """<strong>Public repositories accept untrusted input by design.</strong> An issue tracker is an open channel that anyone can post to. The moment a workflow treats it as a trigger, the repository has wired the internet into its build system, which is an architecture decision rather than a detail for whoever wrote the YAML."""),
        ("p", """<strong>Workflow authoring is a security control.</strong> The weakness is interpolation of event content into shell commands, and the mitigations are known and rarely enforced: pass event data through environment variables, scope the workflow token to the minimum, restrict which events can trigger privileged jobs, require approval for first time contributors and pin actions to a commit."""),
        ("p", """<strong>Credential exposure in CI is a data flow question.</strong> Runner environments hold registry tokens, cloud keys and signing material. A workflow that can be induced to run attacker code can be induced to send those values outward, so the control question is which secrets it can reach and whether they are usable anywhere else."""),
        ("p", """<strong>Third party trust moves downstream.</strong> Consumers rely on maintainer accounts being intact. When those credentials are stolen, release artifacts inherit the compromise and the people installing them have no practical way to tell."""),
        ("h2", "What to watch"),
        ("p", """Whether Radware publishes indicators, and how GitHub responds, given that the trigger is platform behaviour rather than a bug. The internal test is a search of your workflows for event content interpolated into run steps, plus a review of which secrets reach jobs triggered by issues or comments."""),
    ],
))

# ---------------------------------------------------------------- 5. Public Citizen
ARTICLES.append(dict(
    slug="2026-10-30-corporate-enforcement-reversals-tracker",
    title="205 Corporate Enforcement Cases Reversed, and What That Does to Compliance Risk Models",
    desc="Public Citizen's tracker counts 205 corporate enforcement cases terminated or reversed, 44 percent of them tied to the administration.",
    date="October 30, 2026",
    url="https://www.complianceweek.com/regulatory-enforcement/trump-administration-has-dropped-or-reversed-205-corporate-enforcement-cases-public-citizen-finds/",
    source="Compliance Week",
    img="news-regulatory.jpg",
    blocks=[
        ("h2", "What happened"),
        ("p", """Compliance Week reported on 29 October that the Trump administration has terminated or reversed 205 corporate enforcement cases, according to Public Citizen's Corporate Enforcement Tracker. The count covers federal criminal investigations, lawsuits and previously resolved settlements reached under the Biden administration. Public Citizen says 90 of the 205, or 44 percent, have ties to President Trump or his administration, mostly transactional, with most involving payments toward Trump aligned campaign groups or administration initiatives."""),
        ("p", """The tracker's own aggregates do not map neatly onto that headline. Its summary table records 12 actions halted and 233 canceled, a total of 245, and it says enforcement has been canceled or frozen against more than 200 corporations. It covers over 530 cases against more than 430 corporations, and Public Citizen published an October 2026 report on enforcement cancelled against 200 corporations. The organisation notes that an investigation or allegation does not mean a law was broken."""),
        ("h2", "Why this is a GRC story"),
        ("p", """<strong>Enforcement probability is an input, not a background assumption.</strong> Programmes are justified on a mix of legal obligation, customer requirement and enforcement risk. When the third element moves, the business case for a control moves with it, and compliance teams get asked to defend spend that was previously assumed rather than argued."""),
        ("p", """<strong>Political exposure is a third party risk category.</strong> Most due diligence frameworks handle it badly or not at all, and on this evidence it is a variable that shows up in enforcement outcomes. Do you know the campaign exposure of the entities you rely on, and would you be comfortable if it were published?"""),
        ("p", """<strong>Numbers that disagree are a governance signal.</strong> The gap between 205 and 245 is not a scandal, since the two count different things over different periods. It is a reminder that counts like this get repeated in board papers without their definitions attached."""),
        ("p", """<strong>Advocacy data is data, with a provenance question.</strong> The tracker comes from a consumer advocacy organisation with a clear position, drawing on public records. That does not make it unusable, and it does mean treating it as a lead rather than a finding, checked against court records before anything is built on it."""),
        ("h2", "What to watch"),
        ("p", """Whether the methodology survives scrutiny as the count grows, and whether any reversed matters are reopened by courts. The practical step is smaller than the politics: keep your own enforcement exposure register, with the specific matters, agencies and dates that apply to you, rather than reasoning from national totals that may not describe your situation."""),
    ],
))


def strip_plain(html_text):
    txt = re.sub(r"<[^>]+>", " ", html_text)
    return re.sub(r"\s+", " ", txt).strip()


def main():
    written = []
    for a in ARTICLES:
        b = body(*a["blocks"])
        page = HEAD.format(
            title=a["title"], desc=a["desc"], slug=a["slug"], date=a["date"],
            url=a["url"], source=a["source"], img=a["img"], body=b,
        )
        plain = strip_plain(b)
        words = len(plain.split())
        dash = ("\u2014" in page) or ("\u2013" in page)
        path = ART / f"{a['slug']}.html"
        path.write_text(page, encoding="utf-8")
        written.append((a["slug"], words, dash, len(a["desc"])))
        print(f"{a['slug']}: body_words={words} dash={dash} desc_len={len(a['desc'])}")
    print(f"\nWrote {len(written)} articles")
    bad = [w for w in written if not (350 <= w[1] <= 550) or w[2] or w[3] >= 160]
    if bad:
        print("NEEDS REVIEW:", bad)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
