#!/usr/bin/env python3
"""Generate 2026-10-08 GRC news article pages."""
import pathlib

ART = pathlib.Path.home() / "projects/grc-portfolio/news/articles"
DATE_LONG = "October 8, 2026"
DATE_ISO = "2026-10-08"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} · GRC Daily Case Study · Zabez</title>
  <meta name="description" content="{desc}">
  <link rel="icon" href="/favicon.ico" sizes="32x32">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
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
          <span class="article-source">Source: <a href="{src_url}" target="_blank" rel="noopener">{src_name}</a></span>
        </div>
      </div>
    </section>

    <div class="wrap"><div class="article-hero-img"><img src="../../assets/img/{img}" alt="" loading="lazy"></div></div>

    <section class="case-body">
      <div class="wrap" style="max-width: var(--wrap);">
      <div class="case-main article-body">

{body}

        <p class="ref-note" style="margin-top:26px;"><strong>Attribution:</strong> Analysis based on <a href="{src_url}" target="_blank" rel="noopener">{src_name}</a> and related public reporting. This article is original commentary, not a repost of the source material.</p>

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

ARTICLES = [
    dict(
        slug="2026-10-08-fortibleed-fbi-warning",
        title="FBI Warns FortiBleed Is Still Active After 86,644 Fortinet Credentials Were Harvested",
        desc="The FBI and Secret Service say attackers are still using stolen credentials against internet-facing Fortinet firewalls, and some victims are locked out.",
        src_name="The Hacker News",
        src_url="https://thehackernews.com/2026/10/fbi-warns-fortibleed-remains-active.html",
        img="news-breach.jpg",
        body="""        <h2>What happened</h2>
        <p>
          The FBI and the US Secret Service issued a joint warning on Tuesday that the FortiBleed credential harvesting campaign remains an active threat against internet-facing Fortinet FortiGate firewalls and SSL VPN gateways. In the advisory, the agencies said the campaign "exploits reused or leaked credentials and legacy SHA-256 password storage, enabling threat actors to harvest and crack authentication data at scale," and that initial findings show attackers are continuing to scan exposed Fortinet firewalls using credentials they obtained earlier.
        </p>
        <p>
          FortiBleed was first documented in June 2026 by SOCRadar and Hudson Rock. The Russian-speaking operation is estimated to have collected more than 86,644 working device credentials across 194 countries as of June 19. The campaign runs in five stages: reconnaissance of exposed portals, credential stuffing and password spraying using data from leak dumps and infostealer logs, deployment of a Go-based tool called FortigateSniffer that passively intercepts authentication traffic across 24 protocols, offline cracking on GPU clusters using Hashmat and Hashtopolis, and finally lateral movement, Active Directory enumeration and exfiltration. New administrative accounts are created on the appliance to keep access.
        </p>
        <p>
          The agencies also warned that some victims may be locked out of their own devices because the attacker deleted or changed the original account password. CISA's earlier guidance asked Fortinet customers to enable phishing-resistant authentication, terminate active SSL VPN and administrative sessions, reset VPN and administrative passwords, store administrator credentials using PBKDF2, and review logs for suspicious activity. Investigators suspect the operator is an initial access broker selling access onward, with reporting tying the activity to INC and Lynx ransomware operations.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Credential reuse is the control that failed.</strong> The technology was not the weak point. Reused and leaked passwords were. That is a policy and monitoring problem, and it shows up in most environments that have never audited whether device administrative passwords are unique.
        </p>
        <p>
          <strong>Legacy password storage turns one exposure into many.</strong> The advisory specifically names SHA-256 storage. Where credentials are stored that way, stolen hashes can be cracked offline at scale. Moving administrator credentials to PBKDF2 is a documented action item, not a research project, and it reduces the value of a stolen hash.
        </p>
        <p>
          <strong>Recovery plans need to assume you lose admin access.</strong> Deleting accounts on the appliance is a simple way to hold a victim hostage. A response plan that assumes administrative access will still exist is incomplete. Break-glass access, offline configuration backups and a documented rebuild path belong in the runbook before an incident, not during one.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch whether CISA ties FortiBleed to a binding operational directive or a known exploited catalogue entry. Either move attaches an agency remediation deadline and gives private sector teams a date they can take to their own leadership. Watch also for the first ransomware deployment publicly attributed to access sold out of this campaign, because that is when board-level attention usually arrives.
        </p>
        <p>
          The practical work is unglamorous. Inventory every appliance reachable from the internet, confirm administrative credentials are unique and stored with PBKDF2, require phishing-resistant multi-factor authentication, and keep an out-of-band way to regain control of a device if an account disappears.
        </p>""",
    ),
    dict(
        slug="2026-10-08-cui-federal-contractor-rules",
        title="New Federal Contractor Rules for Sensitive Data Are Close to Landing",
        desc="Proposed rules would require contractors handling controlled unclassified information to meet NIST standards and report breaches within 72 hours.",
        src_name="CyberScoop",
        src_url="https://cyberscoop.com/federal-contractors-cui-cybersecurity-rules/",
        img="news-regulatory.jpg",
        body="""        <h2>What happened</h2>
        <p>
          Federal contractors that handle controlled unclassified information, known as CUI, are facing a substantial change in their security and reporting duties. Pending rules on how that data must be protected could arrive as soon as the end of this year, and likely no later than the end of the current presidential term, according to government contracting attorneys quoted by CyberScoop.
        </p>
        <p>
          As currently written, the proposed rules would require contractors to report unauthorized access to CUI, including access caused by a cyberattack, to the federal government within 72 hours of discovery. Contractors would also have to meet minimum electronic security standards drawn from NIST SP 800-171, applied to a broader group of contractors than ever before. The rule is a companion to existing Defense Department requirements covering the same category of data, and it sits inside a wider overhaul of the Federal Acquisition Regulation, including a Part 40 consolidation of supply chain and information security requirements.
        </p>
        <p>
          The intent is to replace a patchwork of agency specific terms such as "sensitive but unclassified" and "for official use only" with a single standard, so contractors comply with one set of rules rather than many. The effort traces back to a 2010 executive order. One practical complication remains: CUI is not always clearly marked, and contractors often cannot say with confidence which information they hold falls into the category.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>The 72 hour clock starts at discovery, not at certainty.</strong> That wording pushes detection and evidence handling into the compliance obligation. A contractor that cannot show when an incident was identified, and what was known at the time, will struggle to demonstrate it reported on time. Log retention and incident documentation stop being housekeeping.
        </p>
        <p>
          <strong>One standard is simpler, but only if scope is clear.</strong> Consolidating many agency requirements into NIST SP 800-171 should reduce duplicated effort, while broader applicability means smaller contractors inherit requirements they may not have staffed for. Data classification becomes the gating control. If you cannot reliably identify CUI in your environment, you cannot protect or report on it.
        </p>
        <p>
          <strong>Contract flow-down is where this travels.</strong> Prime contractors pass these obligations to subcontractors. A supplier that has never run a NIST based assessment may soon find it is a contract condition.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch the final rule text for two things: the effective date and any phase-in period, and whether agencies publish clearer guidance on marking CUI. Clearer marking would help contractors more than another control framework. Watch also whether the reporting channel is unified with existing cyber incident reporting requirements, because overlapping deadlines for the same event are a compliance trap.
        </p>
        <p>
          If your organization holds government data, start with a plain inventory: which contracts involve CUI, who owns the control set, where the evidence lives, and how quickly you could produce a defensible timeline of discovery if an incident happened this week.
        </p>""",
    ),
    dict(
        slug="2026-10-08-ransomware-recovery-ceo-charged",
        title="Ransomware Recovery Firm's CEO Charged With Secretly Paying Attackers",
        desc="Prosecutors say MonsterCloud's owner claimed he could decrypt files without paying ransoms while quietly buying keys from the attackers.",
        src_name="BleepingComputer",
        src_url="https://www.bleepingcomputer.com/news/security/ransomware-recovery-ceo-charged-over-secret-ransom-payments/",
        img="news-aml.jpg",
        body="""        <h2>What happened</h2>
        <p>
          The owner of ransomware remediation company MonsterCloud has been charged with defrauding ransomware victims by secretly paying their attackers for decryption keys while claiming to use proprietary technology to recover encrypted data. Zohar Pinhasi, 50, who also used the names "Zack Silver" and "Zack Green," was indicted by a federal grand jury in the Eastern District of New York on September 23 and arraigned on Wednesday in federal court in Brooklyn.
        </p>
        <p>
          He faces one count of conspiracy to commit wire fraud and two counts of wire fraud. Prosecutors say the alleged scheme ran from June 2018 to June 2023. The US Attorney's Office told BleepingComputer that Pinhasi surrendered, pleaded not guilty and was released on a $2 million bond.
        </p>
        <p>
          According to the indictment, Pinhasi owned and operated MonsterCloud LLC, a Florida based company that advertised tools for recovering encrypted data without paying cybercriminals. Prosecutors allege it had no such technology and instead contacted ransomware operators, paid for keys, and used those keys to restore customer files. Some contracts disclosed that the company might pay cybercriminals, the indictment says, but those contracts stated it would do so only if files could not be decrypted by other means, while dealing with attackers was usually the first step taken.
        </p>
        <p>
          Customers were allegedly charged far more than the ransoms paid. One recovery cited in the indictment involved about $8,200 paid to a gang and roughly $150,000 charged to the victim; another involved about $236,000 paid and about $380,000 charged. Prosecutors also say decrypted sample files were presented as "recovery proofs." In total, the scheme is alleged to have facilitated more than $8 million in ransom payments while charging hundreds of companies in the United States and Canada more than $19 million. If convicted, Pinhasi faces up to 20 years in prison. A 2019 ProPublica investigation raised similar concerns, which he disputed at the time.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Vendor claims are a control environment question.</strong> Incident response is bought in a hurry, often without the diligence applied to any other critical supplier. When a provider's core selling point is a capability nobody can verify, the buyer is relying on marketing. Contract terms that describe a method, a decision point and who authorizes a payment are more useful than a promise of recovery.
        </p>
        <p>
          <strong>Ransom payment governance is not optional.</strong> Sanctions exposure, disclosure duty and stakeholder trust all attach to the decision to pay, and that decision belongs with named executives under a documented process. The allegation here is that payments happened without the victim knowing.
        </p>
        <p>
          <strong>Incident response needs its own evidence trail.</strong> A recovery engagement should produce a timeline, a description of the method used, and a record of what was paid, to whom and on whose authority.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch whether the case prompts clearer disclosure expectations for incident response providers, since this is a fraud matter rather than a security failure. Watch also for how insurers respond, because a case built on secret payments gives them a reason to tighten verification of pre-approval.
        </p>
        <p>
          The practical takeaway is short. Know who you would call during a ransomware event before you need to, ask how they recover data and whether any payment is involved, and put the authorization path in writing.
        </p>""",
    ),
    dict(
        slug="2026-10-08-cisa-ot-binding-directive-push",
        title="OT Coalition Asks CISA to Make Federal OT Security Mandatory",
        desc="The OT Cybersecurity Coalition wants CISA to issue a binding directive for federal operational technology, pointing to an inventory gap.",
        src_name="Infosecurity Magazine",
        src_url="https://www.infosecurity-magazine.com/news/ot-coalition-cisa-mandate-federal/",
        img="news-government.jpg",
        body="""        <h2>What happened</h2>
        <p>
          The Operational Technology Cybersecurity Coalition has asked the US Cybersecurity and Infrastructure Security Agency to set mandatory security requirements for operational technology across federal civilian agencies. In a report published on October 6, the coalition called for a binding operational directive, arguing that no directive currently sets minimum practices for federal OT and that CISA lacks visibility into the risks.
        </p>
        <p>
          The coalition points to scale. Agencies rely on OT in more than 8,000 General Services Administration managed facilities, including laboratories, hospitals and ports of entry, where the technology runs HVAC, power, access control, water and building automation systems. The request follows a Government Accountability Office report published on September 30, which found that only seven of 22 civilian agencies reviewed had fully met Office of Management and Budget requirements to inventory networked OT and Internet of Things devices. Those inventories were due by September 2024, and the GAO said OMB had not issued updated fiscal year 2026 guidance.
        </p>
        <p>
          As proposed, the directive would require agencies to name a senior official or office responsible for OT security and to bring OT risk into enterprise risk management. It would set a baseline for asset inventory, network segmentation, remote access, configuration management, incident preparedness and verified recovery. The coalition's priority controls include changing default passwords, multi-factor authentication, segmentation and backups, but the report does not call for patching or firmware updates. John Gallagher of Viakoo flagged that gap, noting that remediation is missing. Louis Eichenbaum, federal chief technology officer at ColorTokens, said containment matters alongside prevention and that "we cannot patch our way out of cyber risk." The coalition framed the directive as complementary to CISA's CI Fortify resilience initiative.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Inventory is the precondition for every other control.</strong> The GAO finding is the important part of this story. A year past the deadline, most reviewed agencies still cannot fully account for their networked OT and IoT devices. You cannot assess, segment or recover what you have not counted, and the same holds where OT inventory sits with facilities rather than security.
        </p>
        <p>
          <strong>Ownership has to be named, not assumed.</strong> The proposed directive's first requirement is a designated senior official for OT security. That is governance language, and it exists because industrial control systems and cyber risk usually sit in different parts of an organization. A named owner with a seat in risk discussions is how those two worlds start talking before an incident forces them to.
        </p>
        <p>
          <strong>Containment is a risk acceptance decision.</strong> Many industrial devices cannot be patched quickly without disrupting operations. Segmentation, offline recovery and tested restoration buy time when patching is slow. Treating them as substitutes for patching is a risk decision that should be documented.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch whether CISA acts on the request and, if it does, whether patching and firmware updates make it into the final text. Watch also for the OMB guidance the GAO said was missing for fiscal year 2026, which would tell agencies what a complete inventory looks like.
        </p>
        <p>
          For anyone running OT outside government, the direction of travel still matters, even though binding directives do not apply to privately operated critical infrastructure. Federal baselines tend to become procurement expectations. Know what is on the network, name an owner, and prove you can recover a segment without patching your way out of the problem.
        </p>""",
    ),
    dict(
        slug="2026-10-08-cctld-dns-hijack-certificates",
        title="DNS Hijacks in Three Country Domains Let Attackers Mint Fake Certificates",
        desc="Google says attackers took over authoritative DNS records in .gh, .sl and .as and obtained unauthorized HTTPS certificates for its domains.",
        src_name="The Register",
        src_url="https://www.theregister.com/security/2026/10/07/attackers-hijacked-top-level-domains-minted-fake-security-certs-for-google-and-other-orgs/5301718",
        img="news-cloud.jpg",
        body="""        <h2>What happened</h2>
        <p>
          Attackers hijacked top level domains and used that control to alter DNS records and obtain fraudulent HTTPS certificates for several Google domains as well as domains belonging to other organizations. Google said it became aware of the series of attacks last week, affecting the .gh (Ghana), .sl (Sierra Leone) and .as (American Samoa) country code namespaces.
        </p>
        <p>
          Google said that during the hijacks, attackers modified authoritative DNS records and obtained unauthorized HTTPS certificates covering several Google domains and domains belonging to other organizations. It did not say which domains or organizations were affected. The company said the attacks did not compromise Google systems, that Chrome quickly blocked suspected counterfeit certificates across the affected country code top level domains, and that there is no reason to believe the certification authorities that issued the impacted certificates did anything wrong.
        </p>
        <p>
          The consequence of this combination is impersonation without the usual browser warning. Because the attacker controls both traffic routing and the private key attached to the unauthorized certificate, they can potentially intercept or modify data sent by users to the impersonated site, and use a trusted brand to distribute malware or run phishing campaigns.
        </p>
        <p>
          Google was direct about the limits of its own intervention. It said browser side action should not be relied on to protect users, that due to the complexity of DNS hijacks it cannot guarantee its analysis identified every affected domain, and that Chrome's interventions do not reliably protect people using other browsers. Its recommendations are ongoing monitoring of Certificate Transparency logs across all domains, including parked and regional country code properties, a review of recent CT log entries for organizations operating in .gh, .sl or .as, and restrictive Certification Authority Authorization records naming which authorities may issue certificates.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Domain and certificate assets are governance scope.</strong> Many organizations have domains registered years ago for a redirect or brand protection, and nobody currently owns them. Those are exactly the properties Google points at. An asset register that covers servers but not DNS zones and certificates has a blind spot at the trust layer, where users cannot tell the real site from a copy.
        </p>
        <p>
          <strong>Certificate Transparency is a free early warning system.</strong> Monitoring CT logs gives near real time notice when a certificate is issued for a domain you control. It is one of the few detective controls that costs almost nothing and produces high value alerts.
        </p>
        <p>
          <strong>Trust in a third party is not the same as assurance.</strong> Google did not blame the certification authorities. The lesson is structural: certificate issuance validation can be undermined by whoever controls the DNS answers at that moment. Registrars, DNS providers and certificate authorities each deserve a named owner.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch whether the affected registries and registrars publish details on how authoritative records were changed, because that determines whether this was a registry compromise, an account takeover at a registrar, or a weakness in delegation. Watch also for whether the industry revisits cached validation state, which Google warns can be used to mint certificates after a hijack ends.
        </p>
        <p>
          The practical actions are small and repeatable. List every domain you own, including the ones nobody uses, confirm which DNS provider holds each zone, turn on Certificate Transparency monitoring, publish CAA records that restrict issuance, and protect registrar accounts with strong authentication.
        </p>""",
    ),
]

for a in ARTICLES:
    html = HEAD.format(
        title=a["title"], desc=a["desc"], slug=a["slug"], img=a["img"],
        date_long=DATE_LONG, iso=DATE_ISO, src_url=a["src_url"],
        src_name=a["src_name"], body=a["body"],
    )
    p = ART / (a["slug"] + ".html")
    p.write_text(html)
    words = len(a["body"].split())
    print(f"{p.name}  body_words={words}")
