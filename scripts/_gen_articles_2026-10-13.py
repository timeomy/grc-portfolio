#!/usr/bin/env python3
"""Generate the 2026-10-13 GRC daily case studies from the collected digests."""
import re
from pathlib import Path

BASE = Path.home() / "projects/grc-portfolio"
ART = BASE / "news" / "articles"

DATE_LONG = "October 13, 2026"
DATE_ISO = "2026-10-13"

ARTICLES = [
    {
        "slug": "2026-10-13-italian-dpa-wind-tre-fine",
        "title": "Italy Fines Wind Tre 16.7 Million Euros and Holds It Responsible for Its Sales Network",
        "desc": "Italy's data protection authority fined Wind Tre 16.7 million euros over unsolicited marketing and contracts activated without consent.",
        "source_url": "https://www.edpb.europa.eu/news/italian-dpa-fines-wind-tre-eur-16-700-000-for-unlawful-telemarketing-and-data-protection_en",
        "source_name": "European Data Protection Board",
        "img": "news-regulatory.jpg",
        "body": """
        <h2>What happened</h2>
        <p>
          Italy's data protection authority has fined the telecoms operator Wind Tre 16.7 million euros over how it handled personal data for marketing and how it concluded contracts through its sales partners. The decision appears on the European Data Protection Board as a national case, with a final decision date of June 5, 2026.
        </p>
        <p>
          The investigation followed a large number of complaints from individuals who said they kept receiving promotional contacts after objecting, or that contracts and services had been activated without their knowledge. The authority examined the processing carried out for telemarketing, the procedures used to close contracts through sales partners, and the technical and organisational measures the company had in place to prevent unlawful processing.
        </p>
        <p>
          Regulators found that people continued to receive promotional communications after exercising their right to object, or without having given valid consent at all. They also identified cases where contracts were activated without the individuals' knowledge, involving unlawful processing of their personal data. The authority concluded that the company's systems and procedures were not capable of preventing unlawful processing, or of giving effect to data subject requests promptly.
        </p>
        <p>
          The order went beyond the money. The authority issued a definitive ban on further processing of personal data acquired without consent, and required the company to adopt measures making data subject rights effective, particularly the right to object to direct marketing. Wind Tre must also strengthen the technical and organisational measures governing its sales network and the procedures used to verify that promotional activity and contract activations are lawful.
        </p>
        <p>
          The legal references cover the core of the regulation: principles relating to processing, lawfulness, transparency, the right of access, the right to object, controller responsibility, data protection by design and by default, and security of processing.
        </p>
        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Outsourcing a sales channel does not outsource the accountability.</strong> The authority's closing message is that a controller operating a complex sales network remains responsible for how personal data is processed inside it. That is the same principle behind third party risk programmes everywhere: activity can be delegated, the obligation cannot.
        </p>
        <p>
          <strong>Controls on paper are not controls.</strong> The findings describe gaps in technical and organisational measures and in the oversight applied to partners. A consent record nobody reconciles against suppression lists, or an activation process a partner can bypass, produces exactly this outcome at scale.
        </p>
        <p>
          <strong>The remedies are operational, not legal.</strong> The ban and the compliance order point at process design: how objections reach every outbound system fast enough to matter, and how an activation is authorised and evidenced before it happens.
        </p>
        <h2>What to watch</h2>
        <p>
          Watch how other European authorities treat sales networks and lead generation partners. Where this reasoning is followed, the evidence a regulator asks for will concern oversight: partner due diligence, monitoring, complaint root cause analysis, and records showing that objections actually stopped contact.
        </p>
        <p>
          For anyone running outbound marketing or channel partners, the starting point is unglamorous. Map where contact data enters the business, prove that an objection reaches every system capable of sending a message, and give partner compliance a measurable owner rather than a policy document.
        </p>
        """,
    },
    {
        "slug": "2026-10-13-norway-xandr-grindr-fine",
        "title": "Norway's Largest Ever Privacy Fine Lands on Xandr Over Grindr Ad Auctions",
        "desc": "Norway's data protection authority fined Microsoft-owned Xandr NOK 92 million for sharing sensitive Grindr user data with advertisers without valid consent.",
        "source_url": "https://www.bleepingcomputer.com/news/security/norway-fines-microsoft-ad-firm-96-million-over-grindr-data-sharing/",
        "source_name": "BleepingComputer",
        "img": "news-privacy.jpg",
        "body": """
        <h2>What happened</h2>
        <p>
          Norway's data protection authority, Datatilsynet, has fined the advertising company Xandr 92 million Norwegian kroner, around 9.6 million US dollars, for unlawfully processing and sharing sensitive data belonging to Grindr users in Norway. The regulator said it is the largest fine it has ever issued.
        </p>
        <p>
          Between July 2018 and April 2020, Xandr ran real-time advertising auctions inside Grindr. Advertisers bid for the right to display an ad to a user after receiving profiling information from Xandr, which acted as the intermediary for those auctions. The authority found this potentially exposed sensitive information, including sexual orientation, to thousands of companies.
        </p>
        <p>
          Xandr was a joint controller with Grindr during that period, which meant it shared responsibility for how the data was used and should have required and obtained explicit consent from the people concerned. According to the authority, Xandr assumed Grindr had collected valid consent but took no action to verify it, and did nothing to establish a legal basis for its own processing.
        </p>
        <p>
          Line Coll, Director General of Datatilsynet, said the fine was high because the breaches identified were very serious, and that thousands of users in Norway had been subjected to unlawful sharing of their sensitive data.
        </p>
        <p>
          The Austrian privacy organisation Noyb, which filed the original complaint in January 2020 together with the Norwegian Consumer Council, welcomed the decision and called it a major blow to the online advertising technology industry. Xandr, which now operates as Microsoft Advertising, was given three weeks to appeal. Microsoft said the investigation and outcome focused on conduct predating its acquisition of Xandr, that legal frameworks and their interpretation have changed since, and that the company is reviewing the decision.
        </p>
        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Joint controllership is an obligation, not a label.</strong> The decision turns on a failure to verify someone else's legal basis before building a commercial process on top of it. Every organisation that receives personal data from a partner or a publisher faces the same question: what evidence did you check, and when.
        </p>
        <p>
          <strong>Sensitive categories carry a far higher bar.</strong> Data revealing sexual orientation is a special category, so ordinary consent practices are not enough. Systems designed around inferred interests need re-examination when those inferences can reveal a protected characteristic.
        </p>
        <p>
          <strong>Programmatic pipelines concentrate risk.</strong> Data passed through an auction reaches an unknown number of parties in milliseconds, and the controller in the middle may not be able to say where it went. That is a data mapping and disclosure problem as much as a legal one.
        </p>
        <h2>What to watch</h2>
        <p>
          Watch whether the appeal proceeds, and whether other European authorities apply the same logic to intermediaries in advertising and analytics. Enforcement aimed at the middle of the chain, rather than only the publisher, is what changes vendor behaviour.
        </p>
        <p>
          For teams reviewing advertising and analytics vendors, the useful question is whether consent evidence is inspected rather than assumed, and whether records show what data left the organisation, to whom, and on what basis.
        </p>
        """,
    },
    {
        "slug": "2026-10-13-colorado-admt-chatbot-rules",
        "title": "Colorado Tightens the Test for When AI Output Materially Influences a Decision",
        "desc": "Colorado's attorney general released revised draft rules for the state's AI and chatbot laws ahead of an October 26 hearing and a January 2027 start.",
        "source_url": "https://www.jdsupra.com/legalnews/colorado-releases-revised-proposed-7145132/",
        "source_name": "JD Supra (Orrick client alert)",
        "img": "news-ai.jpg",
        "body": """
        <h2>What happened</h2>
        <p>
          On October 6, the Colorado attorney general released an interim redline of proposed rules implementing the state's Automated Decision-Making Technology Act, SB 26-189, and its Chatbot Safety Act, HB 26-1263. The rules were first filed on August 11 and will be the subject of a rulemaking hearing on October 26. The stated aim is to have rules adopted before both laws take effect on January 1, 2027.
        </p>
        <p>
          The most significant addition is a rule setting out when a system's output is presumed to materially influence a consequential decision. The presumption applies where the decision-maker reviews an output about the individual, such as a score, ranking, recommendation, or threshold, or uses it to screen data, and the output is consistent with the final outcome. A deployer can rebut the presumption by showing the output was only a de minimis factor. Tools used solely to summarise, organise, or present information for human review fall outside the definition. One of the draft's examples is a credit union denying loans to applicants scoring below a risk threshold.
        </p>
        <p>
          The draft also clarifies that a deployer remains responsible when a third party runs the technology on its behalf and the deployer uses the output to make the decision.
        </p>
        <p>
          Adverse outcome disclosures change as well. The August version would have required deployers to state the principal reasons for an adverse outcome and disclose any inferences or scores behind it. The redline drops that. Deployers would instead describe the technology's role with specificity, deliver disclosures through every channel they normally use with the consumer, and have 15 days to respond to information requests. The draft adds an exception for disclosures that would compromise legally required cybersecurity, fraud prevention, anti-money laundering, or sanctions compliance programmes.
        </p>
        <p>
          On consumer rights, the draft recasts access and correction as rights to request instructions for obtaining and correcting personal data, excludes opinions, predictions, scores, and protected evaluations from correction, and removes the requirement to hold adverse outcomes pending correction or human review. Human reviewers may be internal or external, provided they have actual authority to override the decision.
        </p>
        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Material influence is the hinge the regime turns on.</strong> A clear presumption with a defined rebuttal is easier to build controls around than a vague standard, and it tells deployers where documentation and testing effort belong.
        </p>
        <p>
          <strong>Disclosure duties are narrowing, but accountability is not.</strong> Dropping the principal reason requirement lowers the drafting burden. Being specific about the technology's role, and answering within a defined window, is still an operational commitment with a workflow behind it.
        </p>
        <p>
          <strong>Carve-outs need governing, not just citing.</strong> An exception for fraud prevention, anti-money laundering, or sanctions programmes only helps if someone can evidence that disclosure would genuinely compromise a required programme.
        </p>
        <h2>What to watch</h2>
        <p>
          Watch the October 26 hearing and the final text, particularly whether the de minimis rebuttal survives as drafted and how firmly the January 2027 effective date holds. Watch as well for other states copying the material influence test.
        </p>
        <p>
          For teams deploying AI in lending, employment, or insurance, the practical work is inventory: which decisions are supported by system output, who reviews it, and what the record shows.
        </p>
        """,
    },
    {
        "slug": "2026-10-13-flock-cve-numbering-authority",
        "title": "Flock Can Now Assign CVEs to Its Own Products and Researchers Are Wary",
        "desc": "Flock joined the CVE Program as a numbering authority for its own surveillance products, raising questions about vendors grading their own vulnerabilities.",
        "source_url": "https://cyberscoop.com/flock-cve-numbering-authority-cna/",
        "source_name": "CyberScoop",
        "img": "news-standards.jpg",
        "body": """
        <h2>What happened</h2>
        <p>
          Flock, the company behind automated licence plate readers and AI-powered cameras used by law enforcement, has been authorised as a CVE Numbering Authority. That gives it the right to assign CVE identifiers to vulnerabilities in its own products and to grade those defects. The company said it joins a programme of more than 550 numbering authorities, and that the role lets it assess, coordinate, and prioritise response to vulnerabilities internally.
        </p>
        <p>
          Chris Castaldo, Flock's chief information security officer, said the authority lets the company move faster when researchers report findings, remove confusion from duplicate or conflicting entries, and give customers a single trusted source of security information. Flock published a vulnerability disclosure policy in August and has created a security advisories page.
        </p>
        <p>
          Security experts acknowledge that many vendors hold numbering authority for good reason, while noting that Flock's business has drawn sustained scrutiny over privacy concerns and repeated reports of police misuse of its technology.
        </p>
        <p>
          Katie Moussouris, founder and chief executive of Luta Security, told CyberScoop that the measure of Flock as a numbering authority is whether its records give cities, police departments, and the public enough detail to track specific risks by product version, the nature of the vulnerability, and how to fix it. A vendor in that role writes the description and often sets the severity score, she said, so an immature vendor may misrepresent an issue through ignorance or an effort to downplay it. She also observed that Flock's products track drivers' movements, its customers are police, and its policy reserves the right to withhold publication where it decides disclosure would create a safety risk.
        </p>
        <p>
          Privacy and security researcher Zach Edwards described numbering authorities as essentially grading their own homework, and expects some researchers to keep disclosing flaws without coordinating with the company. Researchers reported defects last year in Flock's licence plate reader and gunshot detection system, which the company submitted to the National Vulnerability Database but deemed not material because the vulnerabilities required physical access to the device. Flock's disclosure policy rules out testing against live customer deployments, access to law enforcement data, physical attacks, denial of service testing, and social engineering, and there is no paid bug bounty.
        </p>
        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Self-attestation concentrates risk.</strong> When a vendor assigns the identifier, writes the description, and sets the severity, the quality of the record depends on that vendor's process maturity. Procurement teams inherit whatever that process produces.
        </p>
        <p>
          <strong>A disclosure policy is a governance document.</strong> Rules about which tests are permitted, whether researchers are paid, and when publication can be withheld are decisions about transparency that customers can assess before signing a contract.
        </p>
        <p>
          <strong>Conflicts of interest need visible mitigations.</strong> The concern is not that vendors lack the ability to assess their own code, but that nobody outside the vendor can audit the judgement calls when the stakes are highest.
        </p>
        <h2>What to watch</h2>
        <p>
          Watch what Flock actually publishes. The test is whether advisories arrive promptly, name affected versions, explain the flaw in enough detail to act on, and state the fix. A quiet advisory feed is a finding in itself.
        </p>
        <p>
          For organisations buying surveillance or public safety technology, the diligence questions are specific: the median time from report to advisory, which classes of testing are out of scope, and how defects with safety implications are handled.
        </p>
        """,
    },
    {
        "slug": "2026-10-13-ymco-money-mule-guilty-plea",
        "title": "A Guilty Plea in a 15,000-Mule Network Shows How Cybercrime Cash Actually Moves",
        "desc": "A leader of the YMCO money laundering network pleaded guilty in the US, in a case tied to at least $10 million stolen from over 750 bank accounts.",
        "source_url": "https://www.securityweek.com/mastermind-of-15000-mule-cybercrime-laundering-network-pleads-guilty-in-us/",
        "source_name": "SecurityWeek",
        "img": "news-aml.jpg",
        "body": """
        <h2>What happened</h2>
        <p>
          A dual citizen of Ukraine and Russia has pleaded guilty in a United States court for his role in a money laundering organisation used by cybercriminals. Oleg Korniev, 42, was a leader of Your Mule Cashout, a network of money mules and supporting internet infrastructure that let attackers move stolen funds outside the country.
        </p>
        <p>
          According to court documents, the network allowed cybercriminals to conceal the theft of money from the bank accounts of United States companies and transfer it abroad, primarily to Eastern European countries. In exchange, the criminals paid the organisation a percentage of the stolen funds. The network is estimated to have recruited more than 15,000 United States residents as money mules, and to have laundered at least 10 million dollars taken from over 750 bank accounts.
        </p>
        <p>
          The recruits were deceived into believing they were making genuine transfers for legitimate companies. They were told they would receive business payments into their personal accounts and that their job was to withdraw the money and wire it to overseas accounts. Instead, they withdrew stolen proceeds and forwarded them to conspirators abroad, and never received payment for the work.
        </p>
        <p>
          Court documents allege that Korniev helped create the organisation's policies and procedures, hired and managed employees, rewarded or punished them based on performance, and secured illegal services that supported its operations. He admitted to causing over 14.7 million dollars in actual and intended losses, and to laundering at least 7 million dollars from cybercriminals. He agreed to provide full restitution to known victims and to forfeit cash seized when he was arrested in Georgia.
        </p>
        <p>
          Korniev pleaded guilty to money laundering, computer fraud, access device theft, and aggravated identity theft, and faces between 2 and 50 years in prison. Four other members were previously arrested abroad, extradited to the United States, and sentenced to between 37 and 63 months, with restitution orders of over 9.1 million dollars each.
        </p>
        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Payment fraud is a cash-out problem as much as an intrusion problem.</strong> Stolen access is only useful if the proceeds can leave the banking system, and this network provided that service at industrial scale.
        </p>
        <p>
          <strong>Mule recruitment is a control gap at the receiving bank.</strong> Thousands of accounts were used to move funds. Detection at onboarding, transaction monitoring, and fast recall of payments are the controls that shrink the pool of usable accounts.
        </p>
        <p>
          <strong>Third party risk includes the people an organisation recruits.</strong> The network's own playbook, with documented policies, performance management, and rewards, is an uncomfortable reminder that fraud operations borrow the same structures legitimate businesses rely on.
        </p>
        <h2>What to watch</h2>
        <p>
          Watch how sentences in this and related cases compare, since sentence length is the clearest deterrent signal available. Watch also for further extraditions, and for whether victim restitution moves beyond the cash forfeited at arrest.
        </p>
        <p>
          For compliance and fraud teams, the practical point is that outbound payment controls and mule account detection still carry the load. Catching a fraudulent transfer before it leaves, and pulling it back quickly afterwards, limits damage more than any reconstruction that follows.
        </p>
        """,
    },
]

PAGE = """<!DOCTYPE html>
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
  {{"@context": "https://schema.org", "@type": "NewsArticle", "headline": "{title}", "description": "{desc}", "datePublished": "{iso}", "dateModified": "{iso}", "url": "https://zabez.com/news/articles/{slug}.html", "author": {{"@type": "Person", "name": "Kok Jabez", "url": "https://zabez.com/"}}, "publisher": {{"@type": "Organization", "name": "ZABEZ.com", "url": "https://zabez.com/"}}, "image": "https://zabez.com/assets/og-cover.png"}}
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
        <span class="article-date">{date_long}</span>
        <span class="article-date" style="color: var(--text-faint);">By Kok Jabez</span>
        <h1>{title}</h1>
        <p class="subtitle">{desc}</p>
        <div class="score-strip">
          <span class="article-source">Source: <a href="{source_url}" target="_blank" rel="noopener">{source_name}</a></span>
        </div>
      </div>
    </section>

    <div class="wrap"><div class="article-hero-img"><img src="../../assets/img/{img}" alt="" loading="lazy"></div></div>

    <section class="case-body">
      <div class="wrap" style="max-width: var(--wrap);">
      <div class="case-main article-body">
{body}
        <p class="ref-note" style="margin-top:26px;"><strong>Attribution:</strong> Analysis based on <a href="{source_url}" target="_blank" rel="noopener">{source_name}</a> and related public reporting. This article is original commentary, not a repost of the source material.</p>

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

  <script src="../../assets/lucide.min.js"></script>
  <script src="../../assets/anim.js"></script>
</body>
</html>
"""

for a in ARTICLES:
    body = "\n".join(line.strip() for line in a["body"].strip().splitlines() if line.strip())
    # indent body block by 8 spaces for readability
    body_indented = "\n".join(("        " + line) for line in body.splitlines())
    html = PAGE.format(
        title=a["title"],
        desc=a["desc"],
        slug=a["slug"],
        iso=DATE_ISO,
        img=a["img"],
        source_url=a["source_url"],
        source_name=a["source_name"],
        date_long=DATE_LONG,
        body=body_indented,
    )
    out = ART / (a["slug"] + ".html")
    out.write_text(html, encoding="utf-8")

    # QA
    paras = re.findall(r"<p>(.*?)</p>", body, re.S)
    text = " ".join(re.sub(r"<[^>]+>", " ", x) for x in paras)
    words = len(text.split())
    print(f"{out.name}: words={words} desc_len={len(a['desc'])} emdash={chr(0x2014) in text} endash={chr(0x2013) in text}")
    if not (350 <= words <= 550):
        print(f"  !! WORD COUNT OUT OF RANGE: {words}")
    if len(a["desc"]) >= 160:
        print("  !! DESC TOO LONG")
