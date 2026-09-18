#!/usr/bin/env python3
"""Write today's GRC news articles from the site template."""
from pathlib import Path

BASE = Path.home() / "projects" / "grc-portfolio"
TPL = (BASE / "news" / "article-template.html").read_text(encoding="utf-8")
OUT = BASE / "news" / "articles"

DATE = "September 19, 2026"

ARTICLES = []

# ---------------------------------------------------------------- article 1
ARTICLES.append({
    "slug": "2026-09-19-post-quantum-eo-14412",
    "title": "Post-Quantum on Deadline: What EO 14412 Means for Risk and Compliance",
    "description": "EO 14412 sets 2030 and 2031 deadlines for federal post-quantum migration and turns cryptographic inventory into an audit question.",
    "source_name": "DataBreachToday",
    "source_url": "https://www.databreachtoday.com/webinars/post-quantum-on-deadline-what-eo-14412-means-for-risk-compliance-w-7376",
    "body": """
        <h2>What happened</h2>
        <p>
          Executive Order 14412, signed on June 22, 2026 under the title "Securing the Nation
          Against Advanced Cryptographic Attacks", moves federal cryptography work onto a
          calendar. It directs agencies to migrate high value assets and high impact systems to
          post-quantum cryptography under NIST standards: key establishment by December 31, 2030,
          digital signatures by December 31, 2031.
        </p>
        <p>
          The threat it addresses is not a future break, it is collection happening now.
          Adversaries are already taking encrypted material in the expectation of decrypting it
          later, once large-scale quantum computers exist, the pattern usually called harvest now,
          decrypt later. <strong>Data that must stay confidential for a decade is already inside
          the exposure window.</strong>
        </p>
        <p>
          Three structural pieces make it more than an IT project. Within 30 days, each agency head
          had to name a PQC migration lead reporting to the chief information officer, responsible
          for agency-wide cryptographic inventory management and a prioritized migration plan.
          Within 90 days, the Office of Management and Budget was directed to require every agency
          to review its inventory of high value assets and high impact systems and submit a
          transition plan. Within 180 days, the Federal Acquisition Regulatory Council is to
          propose a rule requiring covered contractors to comply with NIST standards, including
          those incorporating PQC algorithms, by December 31, 2030.
        </p>
        <p>
          Two later dates matter for governance teams. Within 270 days, CISA and NIST are to
          publish guidance on the minimum elements of a cryptographic bill of materials, so
          cryptographic assets inside hardware and software can be assessed automatically. The
          same window covers a separate proposal on contractor vulnerability disclosure policies,
          which must accept reports of weaknesses such as missing encryption.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>The first deliverable is an inventory, and inventories are where compliance
          programmes find out how little they know.</strong> No organisation can migrate what it
          has not traced, and few can list every place encryption is used: TLS endpoints, key
          stores, signing services, embedded firmware, supplier libraries, archives at rest. That
          discovery work is an evidence trail, and evidence trails are what assessors ask to see.
        </p>
        <p>
          The order also places accountability where risk teams can use it. A named migration lead
          who owns the inventory and the plan follows the same pattern as any other control owner.
          A plan nobody can be questioned about fails the first test a regulator applies: who
          decided this, when, and on what basis.
        </p>
        <p>
          Procurement is the part that reaches past government. Contractors have carried security
          requirements through contract flowdowns for years, and a rule naming a 2030 compliance
          date gives those requirements a sharper edge. Vendors who cannot answer questions about
          their own cryptographic posture should expect them in due diligence questionnaires long
          before a deadline lands.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch the FAR proposals, which set the date that flows down to suppliers and
          subcontractors, and the cryptographic bill of materials guidance, which will define the
          taxonomy organisations use to declare what they run. Watch whether sector regulators in
          financial services, health and utilities adopt the same framing, because a reference in
          sectoral rules turns good practice into a finding.
        </p>
        <p>
          For private sector teams, the useful question is not whether the order applies to you
          but whether you could produce a defensible list of your cryptographic assets today.
        </p>
""",
})

# ---------------------------------------------------------------- article 2
ARTICLES.append({
    "slug": "2026-09-19-fbi-impersonation-scams",
    "title": "FBI Logs $1.6 Billion in Impersonation Scams, and the Gap Is Verification",
    "description": "FBI data shows nearly 61,000 impersonation complaints and $1.6 billion in losses since January 2025, averaging over $26,000 per case.",
    "source_name": "The Register",
    "source_url": "https://www.theregister.com/cyber-crime/2026/09/18/fbi-fake-cop-and-government-impersonation-scams-cost-victims-16b/5297499",
    "body": """
        <h2>What happened</h2>
        <p>
          The FBI's Internet Crime Complaint Center recorded close to 61,000 complaints of law
          enforcement and government impersonation between January 2025 and July 2026, with
          reported losses above $1.6 billion. The reporting by The Register puts the average loss
          per complaint at more than $26,000.
        </p>
        <p>
          The largest category is also the crudest. Callers claim the target has been linked to a
          crime and demand payment to make the charges disappear, threatening arrest or prison
          time if it is not paid. Roughly 11 percent of complaints describe a jury duty or missed
          court date variant, 6,833 reports carrying losses of nearly $36 million.
        </p>
        <p>
          Two other variants matter because they show the fraudsters doing research first. Medical
          practitioners have been told their licence is expiring or has been used in a crime, with
          payment demanded for renewal or to protect a professional reputation. That pattern
          appears in 3,322 reports with losses above $37 million. A smaller group, 496 complaints,
          covers claims that a driver's licence or passport had expired.
        </p>
        <p>
          The most expensive approach targeted people in ethnic communities, foreign nationals and
          international students in the United States. Scammers posed as foreign police or
          diplomatic officials and threatened to cancel a home country passport or arrange
          extradition, sometimes on video calls with uniforms and sets built to resemble
          government offices. Those 1,809 complaints account for more than $140 million, close to
          10 percent of total losses from less than 3 percent of complaints.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Impersonating authority is a control problem, not a gullibility problem.</strong>
          Every one of these schemes depends on a victim accepting an unverified claim about
          identity and acting on it under pressure. That is the same weakness behind invoice fraud,
          payroll diversion and help desk social engineering, and it is answered with the same
          design choices: out-of-band verification, a second pair of eyes on any payment above a
          threshold, and a clear route for an employee to refuse an urgent request.
        </p>
        <p>
          The complaint data is also useful risk register material. It gives rough loss frequency
          and severity by scenario, it shows that one targeted variant loses far more per
          incident, and it names the pressure tactics involved. Registers built on generic labels
          age badly. Ones built on scenario detail hold up when someone asks why a control exists
          and what it prevents.
        </p>
        <p>
          Impersonation is also a duty of care question for anyone serving a vulnerable
          population. Calls that land on elderly customers, or on staff in a clinical setting, are
          predictable enough to plan for. Awareness training that only tells people to be careful
          adds very little. Training that gives them a specific, fast way to verify a caller adds a
          control.
        </p>

        <h2>What to watch</h2>
        <p>
          The FBI's most recent annual figures put total cybercrime losses at $20.87 billion for
          2025, the first time the number passed $20 billion, so expect this category to keep
          growing in volume and in reported losses. Watch whether telecoms operators and payment
          providers come under pressure over spoofed numbers, since caller ID remains the entry
          point for most of these calls. Watch too how banks set reimbursement rules for
          authorised push payment losses, because where liability sits changes the incentive to
          design better verification at the point of payment.
        </p>
""",
})

# ---------------------------------------------------------------- article 3
ARTICLES.append({
    "slug": "2026-09-19-flood-compliance-lessons",
    "title": "Compliance Lessons From the July Fourth Flood: Plans Fail Where Authority Is Unclear",
    "description": "A compliance veteran's account of the July 4, 2025 Guadalupe River flood turns five hard lessons into a case for better risk planning.",
    "source_name": "Compliance Week",
    "source_url": "https://www.complianceweek.com/compliance-week/learning-from-loss-compliance-lessons-from-the-july-fourth-flood/",
    "body": """
        <h2>What happened</h2>
        <p>
          Compliance Week published a piece built around a new book by compliance veteran Tom
          Fox, "Deluge Before Dawn: Heartbreak, Survival and Resilience After the Guadalupe River
          Raged". Fox lives in the Texas Hill Country and experienced the July 4, 2025 Guadalupe
          River flood as a local, and the article draws five lessons for organisations planning
          their own worst days.
        </p>
        <p>
          The first is that systems which function under stress are activated, not invented during
          the crisis. When the river rose, the data that mattered was unavailable, information
          arrived in fragments, the people responsible for crisis oversight were unreachable, and
          nobody had been deputised to set priorities. By the time the picture was clear, several
          options for reducing harm had closed.
        </p>
        <p>
          The second concerns lines drawn years earlier. Camp Mystic had operated for nearly a
          century. When FEMA maps placed its cabins in a potential flood area, the directors
          contested the maps on the strength of historical experience, appealed, and won. The site
          carried on and new structures went up. The article's assessment is blunt: fully compliant
          and still a disaster waiting to happen.
        </p>
        <p>
          The third is that crises arrive together. The flood came at night, on a holiday, with
          cell service failing and evacuation routes becoming impassable. One failure fed the next.
        </p>
        <p>
          The last two lessons are about trust and memory. A local community foundation stood up a
          dedicated fund within hours because decades of grant reviews, board governance and donor
          stewardship had made its credibility work like infrastructure. A 1987 storm that killed
          ten children produced lessons that did not hold, and the article warns that forgetting
          invites tragedy anew.
        </p>

        <h2>Why this is a GRC story</h2>
        <p>
          <strong>Compliance sets a floor, and this story is about what happens when a team treats
          the floor as the ceiling.</strong> Contested maps are a legitimate process, and the
          appeal was procedurally correct. The problem is that the decision weighed historical
          experience against evolving conditions and chose the answer that preserved the business,
          with the downside carried by other people. That is a risk acceptance decision, and risk
          acceptance is where governance either works or does not.
        </p>
        <p>
          The planning lessons transfer without stretching. Named decision makers,
          pre-authorised deputies, one source of truth for status and a rehearsal of multisystem
          failure are the same requirements any continuity plan needs, whether the trigger is a
          flood, a ransomware event or a supplier outage. An organisation that has never tested who
          takes over when the usual owner is unreachable does not have a plan, it has a document.
        </p>
        <p>
          The trust lesson is the one most often skipped. Good governance is slow work with no
          visible output until the day it is needed. Here it was the difference between hours and
          weeks in getting help to people.
        </p>

        <h2>What to watch</h2>
        <p>
          Watch how anniversary coverage treats resilience as against emergency response, because
          the harder questions are about decisions made years earlier and who owned them. For
          teams well outside Texas, the practical follow up is a plan review with three questions
          attached: who decides when the usual owner is unreachable, what happens when two critical
          systems fail at once, and where the organisation has accepted a risk on the strength of
          experience rather than evidence.
        </p>
""",
})

for art in ARTICLES:
    html = TPL
    html = html.replace("{{TITLE}}", art["title"])
    html = html.replace("{{DESCRIPTION}}", art["description"])
    html = html.replace("{{DATE}}", DATE)
    html = html.replace("{{SOURCE_URL}}", art["source_url"])
    html = html.replace("{{SOURCE_NAME}}", art["source_name"])
    html = html.replace("{{BODY}}", art["body"].strip("\n"))
    dest = OUT / f"{art['slug']}.html"
    dest.write_text(html, encoding="utf-8")
    print(f"wrote {dest.name} ({len(html)} bytes)")
