#!/usr/bin/env python3
"""Generate today's GRC news article pages from the day's digest selection."""
import re
from pathlib import Path

BASE = Path.home() / "projects" / "grc-portfolio"
ARTICLES = BASE / "news" / "articles"
DATE_ISO = "2026-09-18"
DATE_HUMAN = "September 18, 2026"

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
    .article-body blockquote {{ border-left: 2px solid var(--gold); padding: 2px 0 2px 18px; margin: 18px 0; color: var(--text-dim); font-style: italic; }}
  </style>
  <script type="application/ld+json">
  {{"@context": "https://schema.org", "@type": "NewsArticle", "headline": "{title}", "description": "{desc}", "datePublished": "{date_iso}", "dateModified": "{date_iso}", "url": "https://zabez.com/news/articles/{slug}.html", "author": {{"@type": "Person", "name": "Kok Jabez", "url": "https://zabez.com/"}}, "publisher": {{"@type": "Organization", "name": "ZABEZ.com", "url": "https://zabez.com/"}}, "image": "https://zabez.com/assets/og-cover.png"}}
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
        <span class="article-date">{date_human}</span>
        <span class="article-date" style="color: var(--text-faint);">By Kok Jabez</span>
        <h1>{title}</h1>
        <p class="subtitle">{desc}</p>
        <div class="score-strip">
          <span class="article-source">Source: <a href="{url}" target="_blank" rel="noopener">{src}</a></span>
        </div>
      </div>
    </section>

    <div class="wrap"><div class="article-hero-img"><img src="../../assets/img/{img}" alt="" loading="lazy"></div></div>

    <section class="case-body">
      <div class="wrap" style="max-width: var(--wrap);">
      <div class="case-main article-body">

{body}

        <p class="ref-note" style="margin-top:26px;"><strong>Attribution:</strong> Analysis based on <a href="{url}" target="_blank" rel="noopener">{src}</a> and related public reporting. This article is original commentary, not a repost of the source material.</p>

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

ITEMS = [
    dict(
        slug="2026-09-18-ofcom-online-safety-fines-unpaid",
        title="Ofcom Has Fined £7 Million Under the Online Safety Act, But Most of It Is Unpaid",
        desc="Ofcom has fined 11 service providers more than £7 million under the Online Safety Act, yet its enforcement chief says most penalties remain unpaid.",
        url="https://www.theregister.com/security/2026/09/17/ofcom-discovers-issuing-online-safety-act-fines-is-easier-than-collecting-them/5297110",
        src="The Register",
        img="news-regulatory.jpg",
        body="""        <h2>What happened</h2>
        <p>
          Ofcom's enforcement chief has told peers that most of the fines the regulator has
          issued under the Online Safety Act remain unpaid. Suzanne Cater, director of
          enforcement, told the House of Lords Communications and Digital Committee that a
          further payment had arrived this week, but that "realistically the majority have not
          been paid." The regulator has fined 11 service providers more than £7 million
          ($9.4 million) under its Online Safety Act powers so far.
        </p>
        <p>
          Oliver Griffiths, a group director at Ofcom, said enforcement has so far concentrated
          on smaller companies in the pornography industry. The largest single penalty,
          £1.4 million ($1.88 million), went to 8579 LLC in February. He told the committee the
          picture should improve as the regulator moves on to larger companies, where collection
          difficulties should be less pronounced.
        </p>
        <p>
          The gap sits in the regulator's powers rather than its willingness to use them. Ofcom
          cannot shut a service down worldwide, though it can ask a court to restrict UK access,
          a power it first used in May against an unnamed suicide forum whose operator had
          already been fined £950,000 ($1.2 million). Moving operations or infrastructure
          overseas is not an escape, because courts can order third parties such as internet
          service providers to block UK access. But business disruption measures require
          continuing noncompliance and cannot be used purely to recover an unpaid fine. Some
          services, Griffiths said, complied after being fined and then failed to pay, leaving
          Ofcom to chase the debt without UK assets to pursue.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>An enforcement regime is only as strong as its collection rate.</strong> Most
          compliance programmes model regulatory risk as the fine plus the remediation cost.
          That model assumes the fine gets paid. Where penalties go unpaid and uncollected, the
          practical deterrent weakens, and the risk picture becomes uneven between companies
          that can be reached and companies that cannot.
        </p>
        <p>
          There is a governance lesson for anyone running a compliance function. Ofcom says it
          would rather secure compliance before opening an investigation than litigate a debt
          afterwards, and that it is beginning to use its power to hold senior managers
          personally liable in certain circumstances. Both are early signals of a regulator
          working out which levers actually change behaviour. Read alongside the Online Safety
          Act's risk assessment and transparency duties, the message is that evidence of the
          work is the defence, not a promise to do better.
        </p>
        <p>
          For compliance teams outside media and tech, the transferable point is structural. The
          services Ofcom struggles to collect from are often the ones with no UK assets and no
          appetite to stay in the market.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch whether Ofcom starts publishing the outstanding balance and the number of unpaid
          penalties. Regulators rarely name non-payers by accident, and naming changes behaviour.
        </p>
        <p>
          Watch how the judgment debt route performs against offshore operators. If registering a
          fine as a judgment debt does not produce payment, the next step is likely pressure on
          payment intermediaries, app stores and advertisers rather than on the service itself.
        </p>
        <p>
          Watch the first large-platform cases. If they pay, Ofcom's current explanation holds.
          If they are contested for years, the argument that size solves collection will look
          weaker than it does today.
        </p>""",
    ),
    dict(
        slug="2026-09-18-coast-guard-fbi-ship-cyber-boarding",
        title="Coast Guard and FBI Board Foreign Ships Over Suspected Cyber Compromise",
        desc="The Coast Guard and FBI boarded two US-bound tankers in the Gulf of Mexico after indications that the vessels' networks had been compromised.",
        url="https://cyberscoop.com/coast-guard-fbi-investigate-tanker-cyberattacks/",
        src="CyberScoop",
        img="news-supplychain.jpg",
        body="""        <h2>What happened</h2>
        <p>
          The US Coast Guard and the FBI boarded two foreign commercial vessels bound for the
          United States to investigate suspected cyber compromises, the agencies said in a joint
          statement. The joint offshore security boardings took place in the Gulf of Mexico on
          August 21 and August 24. According to the statement, they were carried out "to ensure
          integrity of the vessel's operational and information technology systems following
          indications that the networks of both vessels were compromised."
        </p>
        <p>
          The boarding parties were not routine inspections. They combined Coast Guard law
          enforcement personnel, Coast Guard Cyber Protection Team members, a vessel inspector
          and operators from the FBI Cyber Action Team. The agencies said there are currently no
          reports of operational disruptions, vessel instability, physical danger to crews or
          environmental impacts, and that the Coast Guard is managing communications with port
          operators, vessel owners and local maritime stakeholders to keep port operations
          running.
        </p>
        <p>
          The vessels were reported to be tankers carrying oil and natural gas. The first was
          reportedly compromised in the Strait of Gibraltar and lost communications for more than
          30 hours. Reporting has raised the question of whether Iran, or another group
          exploiting tensions between Iran and the United States, was responsible. The agencies
          credited the captain, crew and shore-side corporate staff as critical partners in
          mitigating the threats.
        </p>
        <p>
          The boardings sit against a wider maritime cyber picture. Coast Guard cyber teams have
          been examining "dark fleets" carrying sanctioned oil from Iran and Russia, which depend
          on digital masking to hide their movements and carry additional cyber risk. An
          executive order signed in 2024 gave the Coast Guard expanded authorities to respond to
          cyber incidents, citing the risk of cascading harm to the global supply chain.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>This is a critical infrastructure regulator using inspection powers in
          response to a cyber incident.</strong> For most sectors, cyber oversight arrives as a
          questionnaire or a reporting duty. In maritime it arrived as personnel boarding a
          vessel at sea. That is the direction of travel for operational technology generally,
          where a compromise can cause physical consequences rather than just data loss.
        </p>
        <p>
          The governance anatomy of the incident is worth studying. The tankers were foreign
          flagged, owned and operated through layers of companies, and crewed by seafarers who
          had no hand in selecting the technology on board. That is a supply chain in which the
          party carrying the operational risk is rarely the party that procured the systems. It
          is the same problem that surfaces in supplier assurance questionnaires across every
          industry, with better photographs.
        </p>
        <p>
          There is also a sanctions dimension. Where vessels operate to move sanctioned cargo and
          use digital masking to do it, cyber risk management and sanctions compliance stop being
          separate programmes. Both depend on knowing who owns, operates and connects to the
          asset.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch the attribution question. If a state actor is named, expect the incident to move
          into sanctions designations and diplomatic channels.
        </p>
        <p>
          Watch whether the Coast Guard's boarding authorities are extended or formalised. Every
          expansion of inspection powers creates an evidence obligation for the operators, and
          eventually a contractual one.
        </p>
        <p>
          Watch port operators and charterers. If vessel cyber assurance starts appearing in
          charterparty terms and insurance conditions, that is the moment the guidance becomes
          operational reality.
        </p>""",
    ),
    dict(
        slug="2026-09-18-uk-ai-risk-management-toolkit",
        title="UK Publishes an AI Risk Management Toolkit for Delivery Teams",
        desc="DSIT's new AI Risk Management Toolkit gives multidisciplinary teams a workbook, a monitoring dashboard and probing questions to assess AI risk.",
        url="https://www.complianceweek.com/artificial-intelligence/u-k-ai-risk-management-toolkit-targets-current-and-future-compliance/",
        src="Compliance Week",
        img="news-ai.jpg",
        body="""        <h2>What happened</h2>
        <p>
          The UK government has published an AI Risk Management Toolkit for the
          multidisciplinary teams that design, procure, operate and deliver AI products. The
          Department for Science, Innovation and Technology published the toolkit on September 8,
          and Compliance Week reported the release on September 17.
        </p>
        <p>
          The toolkit is not a standalone document. It is built to implement the risk management
          processes set out in the Orange Book, the long-standing UK government guide to managing
          risk, and it is meant to sit alongside the Cyber Assessment Framework. It covers four
          phases: risk identification and assessment, risk treatment, risk monitoring and risk
          reporting.
        </p>
        <p>
          Four artefacts come with it. There is a guide to AI risk assessment, a set of critical
          questions intended to expose where AI risk is hiding in a specific solution, a workbook
          for recording identified risks, their assessment and treatment actions, and an AI risk
          monitoring dashboard showing the overall risk profile of the solution along with the
          likelihood of different degrees of success and failure.
        </p>
        <p>
          The toolkit also sets an accountability structure. Multi-disciplinary AI risk
          management teams should ideally be led by a named individual, an AI governance officer,
          and should include senior leaders who set risk appetite and tolerance, data teams, AI
          practitioners, security, legal and compliance, business domain experts and end users.
          The Government Digital Service encourages departments to keep a central log of AI risks
          and share it with GDS and DSIT's central AI risk team.
        </p>
        <p>
          One design assumption runs through the document: an AI system has no final version.
          Risk assessment is expected to continue from use case identification to retirement,
          with reassessment when a model drifts or is updated, after alpha and beta releases, and
          through stress testing in live service.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>The toolkit converts an abstract debate into named owners and recorded
          decisions.</strong> Much of the AI governance material published over the past three
          years describes principles. This one asks teams to write down the risk, the treatment
          and the person accountable for it, and to keep that record current. That is an evidence
          trail, and evidence trails are what assessors ask for.
        </p>
        <p>
          The third-party section is the part compliance teams should read first. It asks for
          testing, evaluation and validation of third-party elements, whether data, software or
          hardware, for supplier processes to report known or potential vulnerabilities, for
          redundancy covering third-party functions, for procedures to bypass the AI solution,
          and for contracts with robust warranty and indemnity provisions. That is a supplier
          assurance checklist written in the language of procurement.
        </p>
        <p>
          The structure of the team matters as much as the content. Giving the work a named AI
          governance officer and a standing set of disciplines mirrors the way mature risk
          functions handle other domains, and it avoids the common failure where AI risk lands on
          one person with no authority.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch whether the toolkit starts appearing in tender requirements and assurance
          questions. Guidance becomes binding in practice when it is written into a procurement
          process.
        </p>
        <p>
          Watch the central risk log. If departments begin sharing a common register of AI risks,
          the aggregate picture will inform where the next round of policy lands.
        </p>
        <p>
          Watch the crossover with emerging AI regulation. Organisations adopting the toolkit now
          are building the records that future oversight will ask for.
        </p>""",
    ),
    dict(
        slug="2026-09-18-sec-innovation-exemption-tokenized-stock",
        title="SEC Grants a Five-Year Innovation Exemption for Tokenized Stock Trading",
        desc="The SEC gave tokenized securities venues conditional five-year relief from exchange registration to trade tokenized NMS stock via permissioned pools.",
        url="https://www.sec.gov/newsroom/press-releases/2026-90-sec-issues-innovation-exemption-facilitate-trading-tokenized-nms-stock-request-comment",
        src="SEC Press Releases",
        img="news-crypto.jpg",
        body="""        <h2>What happened</h2>
        <p>
          The Securities and Exchange Commission issued an order on September 17 granting
          temporary, conditional relief to Tokenized Securities Venues, or TSVs, from the
          definition of "exchange" in the Securities Exchange Act of 1934. The relief lets those
          venues trade tokenized National Market System stock through permissioned automated
          market makers and liquidity pools. The Commission calls it the Innovation Exemption and
          has opened it for public comment.
        </p>
        <p>
          A TSV brings buyers and sellers together by operating one or more AMM liquidity pools
          for permissioned participants, and by setting the standards participants must meet to
          trade there. The exemption is conditional. Tokenized NMS stock traded this way is
          subject to limits on the number of symbols and the volume traded. A venue must verify
          that a tokenized stock gives holders the same rights and privileges as the traditional
          stock of the same class, including dividends and voting rights. Before listing stock
          tokenized by an unaffiliated third party, the venue must give written notice and an
          opportunity to object to the issuer of the underlying stock.
        </p>
        <p>
          Technical and conduct conditions follow. Smart contracts used by a venue must be
          auditable, public and deployed on a public, permissionless distributed ledger. A venue
          must stop trading a tokenized stock at the same time as any trading stoppage in the
          underlying stock on its primary listing exchange, and must give public notice about its
          operations, its trading activity and the trading activity of its affiliates. The order
          also grants a conditional exemption from the definition of "dealer" for liquidity
          providers that supply tokenized NMS stock using proprietary capital. The relief expires
          five years after publication.
        </p>
        <p>
          "The Innovation Exemption, while temporary, would allow TSVs to trade tokenized NMS
          stock in a permissioned environment today while the Commission considers the need for
          additional action to facilitate onchain trading," said SEC Chairman Paul S. Atkins.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Every condition in this order is a control that someone has to evidence.</strong>
          Relief from registration is not relief from compliance. A venue that cannot show that
          its smart contracts are auditable and publicly deployed, that its access standards are
          enforced, or that holders really do hold the same rights as holders of the underlying
          stock, has not met the terms on which it is allowed to operate.
        </p>
        <p>
          The five-year sunset is the most telling design choice. Regulators use temporary
          exemptions when they want to observe a market before writing permanent rules, which
          puts the supervised party in the position of generating the evidence that shapes the
          eventual framework. For compliance teams at venues, brokers and asset managers, that
          means surveillance, recordkeeping and disclosure arrangements need to be built for
          tokenized instruments now, not after the rule is final.
        </p>
        <p>
          The conditions also reach into areas that product teams often treat as legal detail:
          what rights a token actually conveys, whether an issuer was told before a third party
          tokenized its stock, and whether trading halts propagate correctly.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch the comment file. What venues, issuers and investor advocates ask for will show
          where the conditions are workable and where they are not.
        </p>
        <p>
          Watch the first enforcement action involving a tokenized instrument. The conditions in
          this order read like a list of the things a future case will allege were not done.
        </p>""",
    ),
    dict(
        slug="2026-09-18-prediction-markets-employee-trading",
        title="Prediction Markets Push Employee Trading Rules Into New Territory",
        desc="Compliance teams are being urged to extend employee trading surveillance to prediction market contracts that sit outside existing broker feeds.",
        url="https://www.complianceweek.com/best-practices/preparing-for-prediction-markets-regulations-is-a-safe-bet/",
        src="Compliance Week",
        img="news-aml.jpg",
        body="""        <h2>What happened</h2>
        <p>
          Compliance Week has published guidance for compliance teams on prediction market
          contracts, written by Alma Angotti, Michael Herde and Tyler Paretchan of FTI
          Consulting. The article argues that contracts offered mainly by Kalshi and Polymarket
          have moved beyond sports betting into election outcomes, military operations and
          corporate performance metrics, and that some now resemble capital markets derivatives
          while sitting outside the surveillance firms run over their own staff.
        </p>
        <p>
          The regulatory hooks are not new. Section 15(g) of the Securities Exchange Act of 1934
          and Rule 17j-1 of the Investment Company Act of 1940 exist to keep personal trading by
          employees with access to material non-public information free of actual or potential
          conflicts, and the SEC expects registered firms to take active steps to prevent
          conflicted transactions. FINRA has not announced specific monitoring of prediction
          markets, but its 2026 Annual Regulatory Oversight Report focuses on manipulative
          trading and cites Rule 3110, which requires supervisory procedures reasonably designed
          to identify trades violating insider trading and manipulative trading rules for the
          accounts of the firm and its associated persons.
        </p>
        <p>
          The authors set out a practical sequence: bring compliance, legal and the business
          together to agree the firm's position, review which existing policies can be adjusted
          and which need to be written, look at surveillance tools that can monitor contracts the
          the way broker feeds are monitored, and tell employees plainly what is and is not allowed.
        </p>
        <p>
          There is enforcement context on both sides of the argument. On May 6 the SEC charged 21
          individuals over an insider trading scheme involving material non-public information
          about corporate transactions. The CFTC fined former Congressman George Santos $35,000
          for betting on his own attendance at the State of the Union address on Kalshi.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>This is a policy scope problem, and policy scope problems get discovered by
          enforcement.</strong> Most employee trading policies are written around brokers,
          accounts and pre-clearance workflows. A contract on a corporate outcome, bought on a
          platform that never touches the firm's broker feed, sits outside all of it while
          carrying the same conflict of interest.
        </p>
        <p>
          The uncomfortable part is that a reminder that employees must not act on inside
          information is not, on its own, a control. A control produces evidence: training
          records, attestations, surveillance coverage, and a documented decision about which
          platforms are in scope. The authors make this point directly, noting that asking
          employees to behave is unlikely to be a strong defence under scrutiny.
        </p>
        <p>
          Prediction markets also raise a data governance question for firms that use them. Where
          pricing on a corporate event is visible to anyone, some desks will treat it as market
          intelligence. That is a legitimate use until the same desk is advising on the event in
          question.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch for the SEC or FINRA to state explicitly whether prediction market contracts fall
          within existing personal trading and supervision rules. Right now firms are reading the
          intent of rules written before these products existed.
        </p>
        <p>
          Watch the SEC's work on exchange traded funds tied to prediction market contracts.
          Moving these products into regulated markets pulls them into regulated surveillance.
        </p>
        <p>
          Watch the first enforcement case against an individual who used a prediction market
          instead of a derivative. That case will define the perimeter faster than any guidance.
        </p>""",
    ),
]


def word_count(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    text = text.replace("&nbsp;", " ")
    return len([w for w in re.split(r"\s+", text) if w.strip()])


def main() -> None:
    for item in ITEMS:
        path = ARTICLES / f"{item['slug']}.html"
        if path.exists():
            print(f"SKIP exists: {path.name}")
            continue
        html = HEAD.format(
            title=item["title"],
            desc=item["desc"],
            slug=item["slug"],
            date_iso=DATE_ISO,
            date_human=DATE_HUMAN,
            url=item["url"],
            src=item["src"],
            img=item["img"],
            body=item["body"],
        )
        path.write_text(html, encoding="utf-8")
        wc = word_count(item["body"])
        has_dash = ("\u2014" in html) or ("\u2013" in html)
        print(f"WROTE {path.name}  body_words={wc}  desc_chars={len(item['desc'])}  "
              f"dashes={'YES' if has_dash else 'no'}")
        if not (350 <= wc <= 550):
            print(f"  !! word count out of range: {wc}")
        if len(item["desc"]) > 160:
            print(f"  !! description too long: {len(item['desc'])}")


if __name__ == "__main__":
    main()
