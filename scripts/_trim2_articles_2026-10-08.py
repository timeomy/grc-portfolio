#!/usr/bin/env python3
"""Final trims on the 2026-10-08 article HTML so bodies land near the 500-550 word range."""
import pathlib

ART = pathlib.Path.home() / "projects/grc-portfolio/news/articles"

EDITS = {
    "2026-10-08-cctld-dns-hijack-certificates.html": [
        ("The consequence of this combination is impersonation without the usual browser warning. Because the attacker controls both traffic routing and the private key attached to the unauthorized certificate, they can potentially intercept or modify data sent by users to the impersonated site, and use a trusted brand to distribute malware or run phishing campaigns.",
         "The consequence is impersonation without the usual browser warning. Because the attacker controls both traffic routing and the private key attached to the unauthorized certificate, they can intercept or modify data sent to the impersonated site, and use a trusted brand to run phishing campaigns."),
        ("Many organizations have domains registered years ago for a redirect or brand protection, and nobody currently owns them. Those are exactly the properties Google points at. An asset register that covers servers but not DNS zones and certificates has a blind spot at the trust layer, where users cannot tell the real site from a copy.",
         "Many organizations have domains registered years ago for a redirect or brand protection, and nobody currently owns them. Those are exactly the properties Google points at. An asset register that covers servers but not DNS zones has a blind spot at the trust layer, where users cannot tell the real site from a copy."),
        ("Its recommendations are ongoing monitoring of Certificate Transparency logs across all domains, including parked and regional country code properties, a review of recent CT log entries for organizations operating in .gh, .sl or .as, and restrictive Certification Authority Authorization records naming which authorities may issue certificates.",
         "Its recommendations are ongoing monitoring of Certificate Transparency logs across all domains, including parked and regional country code properties, a review of recent CT log entries for organizations in .gh, .sl or .as, and restrictive Certification Authority Authorization records naming which authorities may issue certificates."),
    ],
    "2026-10-08-cisa-ot-binding-directive-push.html": [
        ("The coalition points to scale. Agencies rely on OT in more than 8,000 General Services Administration managed facilities, including laboratories, hospitals and ports of entry, where the technology runs HVAC, power, access control, water and building automation systems.",
         "The coalition points to scale. Agencies rely on OT in more than 8,000 General Services Administration managed facilities, including laboratories, hospitals and ports of entry running HVAC, power, access control, water and building automation systems."),
        ("That is governance language, and it exists because industrial control systems and cyber risk usually sit in different parts of an organization. A named owner with a seat in risk discussions is how those two worlds start talking before an incident forces them to.",
         "That is governance language, and it exists because industrial control systems and cyber risk usually sit in different parts of an organization. A named owner with a seat in risk discussions is how those two worlds start talking."),
        ("For anyone running OT outside government, the direction of travel still matters, even though binding directives do not apply to privately operated critical infrastructure. Federal baselines tend to become procurement expectations. Know what is on the network, name an owner, and prove you can recover a segment without patching your way out of the problem.",
         "For anyone running OT outside government, the direction of travel still matters. Federal baselines tend to become procurement expectations. Know what is on the network, name an owner, and prove you can recover a segment without patching your way out of the problem."),
    ],
    "2026-10-08-ransomware-recovery-ceo-charged.html": [
        ("Customers were allegedly charged far more than the ransoms paid. One recovery cited in the indictment involved about $8,200 paid to a gang and roughly $150,000 charged to the victim; another involved about $236,000 paid and about $380,000 charged.",
         "Customers were allegedly charged far more than the ransoms paid. One recovery cited in the indictment involved about $236,000 paid to a gang and roughly $380,000 charged to the victim."),
        ("Prosecutors also say decrypted sample files were presented as \"recovery proofs.\" In total, the scheme is alleged to have facilitated more than $8 million in ransom payments while charging hundreds of companies in the United States and Canada more than $19 million.",
         "Prosecutors also say decrypted sample files were presented as \"recovery proofs.\" In total, the scheme is alleged to have facilitated more than $8 million in ransom payments while charging hundreds of companies in the United States and Canada over $19 million."),
    ],
}

for fname, edits in EDITS.items():
    p = ART / fname
    html = p.read_text()
    for old, new in edits:
        if old in html:
            html = html.replace(old, new, 1)
        else:
            print("MISS:", fname, old[:60])
    p.write_text(html)
    print("updated", fname)
