# Starter Policy Pack, Free Download

Three ready-to-adapt templates: Information Security Policy, Acceptable Use Policy,
and a Risk Register. These are the documents every GRC program needs first.
Replace bracketed placeholders with your organization's details.

---

## 1. Information Security Policy (starter)

**Owner:** [CISO / Security Lead] · **Applies to:** all employees, contractors, and third parties with access

### 1.1 Purpose
Protect the confidentiality, integrity, and availability of [Company] information assets and comply with applicable legal, regulatory, and contractual obligations.

### 1.2 Scope
All information assets, data, systems, networks, and devices, owned or operated by [Company], and all personnel who access them.

### 1.3 Policy
1. **Access control.** Access is granted on least-privilege, need-to-know basis. Access reviews occur [quarterly/annually]. Terminated personnel lose access within [24 hours].
2. **Data classification.** Information is classified [Public / Internal / Confidential / Restricted] and handled per the Data Classification & Handling Policy [link].
3. **Endpoint protection.** Company devices must run approved [antivirus/EDR], receive updates within [X] days, and be encrypted at rest.
4. **Authentication.** [MFA] is mandatory for all remote access, privileged accounts, and [critical systems]. Passwords follow [NIST SP 800-63B] guidance.
5. **Incident reporting.** All suspected security incidents must be reported to [security@company.com] within [1 hour] of discovery. No retaliation for good-faith reporting.
6. **Third parties.** Vendors with access to [Company] data must complete [TPRM questionnaire] and contractually commit to [ISO 27001 / SOC 2 / applicable standard].
7. **Training.** All personnel complete security awareness training [upon hire and annually], including [phishing simulation].
8. **Exceptions.** Exceptions require documented approval by [CISO], with compensating controls and a remediation date.

### 1.4 Enforcement
Non-compliance may result in disciplinary action up to and including termination, and may be reported to regulators where required by law.

**Review:** [Annually] · **Next review:** [date]

---

## 2. Acceptable Use Policy (starter)

**Owner:** [Security Lead / HR] · **Applies to:** all personnel

1. Company resources are provided for business use; incidental personal use is permitted where it does not interfere with work or security.
2. Users must not:
   - Share credentials or bypass security controls (e.g., disabling MFA/AV).
   - Store [Confidential/Restricted] data on personal devices or unauthorized cloud services.
   - Download or install unapproved software.
   - Access, store, or transmit illegal, discriminatory, or harassing content.
3. Users must report lost/stolen devices and suspected compromise immediately.
4. [Company] may monitor resources to protect security and comply with law, consistent with [local privacy law / employee consent requirements].
5. Remote work requires [VPN] and adherence to [remote work policy].

---

## 3. Risk Register (starter format)

| ID | Risk / Threat | Asset | Likelihood (1-5) | Impact (1-5) | Risk Score | Owner | Controls in Place | Residual Score | Target Date | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| R-001 | Ransomware on file server | File server / shared drives | 4 | 5 | 20 | [IT Lead] | EDR, backups (daily, tested), MFA, user training | 8 | [Date] | Mitigating |
| R-002 | Vendor data breach | Customer data at [Vendor] | 3 | 4 | 12 | [Procurement] | TPRM questionnaire, contract DPA, annual review | 6 | [Date] | Monitoring |
| R-003 | Phishing → account takeover | Email / M365 | 4 | 4 | 16 | [Security] | MFA enforced, phishing sims, awareness training | 6 | [Date] | Mitigating |
| R-004 | Insider data exfiltration | HR / finance data | 2 | 4 | 8 | [HR] | DLP, least privilege, exit process | 4 | [Date] | Monitoring |
| R-005 | Cloud misconfiguration | AWS account | 3 | 5 | 15 | [DevOps] | IaC, CIS benchmarks, weekly review | 5 | [Date] | Mitigating |

**Scoring:** 5 = Almost certain / Catastrophic … 1 = Rare / Negligible. Risk Score = Likelihood × Impact.
**Review cadence:** monthly by [Risk Owner]; escalate score ≥ 15 to [Management/Board].

---

*Templates for adaptation, not legal advice. Tailor to your jurisdiction, contracts, and framework (ISO 27001 / NIST CSF / SOC 2) before use.*
