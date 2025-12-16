# Incident Communication Plan Template

## Document Information

| Field | Value |
|-------|-------|
| **Plan Owner** | [Name, Title] |
| **Last Updated** | YYYY-MM-DD |
| **Next Review** | YYYY-MM-DD |
| **Classification** | INTERNAL |

---

## 1. Communication Objectives

### Primary Goals
- [ ] Ensure timely and accurate information flow during incidents
- [ ] Maintain stakeholder confidence through transparent communication
- [ ] Meet regulatory notification requirements
- [ ] Preserve evidence integrity during communication
- [ ] Support effective incident response coordination

### Communication Principles
1. **Accuracy over speed** - Only communicate verified information
2. **Consistency** - Single source of truth from designated spokesperson
3. **Appropriateness** - Tailor message to audience
4. **Documentation** - Record all communications for audit trail
5. **Legal review** - External communications require legal approval

---

## 2. Stakeholder Matrix

### Internal Stakeholders

| Stakeholder Group | Contact | Notification Trigger | Channel | Frequency | Owner |
|-------------------|---------|---------------------|---------|-----------|-------|
| Executive Leadership | [Name/Distribution] | P0, P1 | Phone, Email | Immediate + hourly | CISO |
| CISO | [Name] | All incidents | Phone | Immediate | SOC Lead |
| Legal/Compliance | [Name] | P0, P1, data breach | Phone | Immediate | CISO |
| IT Operations | [Name/Team] | P0, P1, P2 | Slack/Teams | Immediate | IC |
| Engineering Teams | [Name/Team] | Affected systems | Slack/Teams | As needed | Tech Lead |
| HR | [Name] | Insider threat, employee impact | Email | When relevant | CISO |
| Finance | [Name] | Financial impact, ransomware | Email | When relevant | CISO |
| Board of Directors | [Chair Name] | P0, material breach | Phone | Per board policy | CEO |

### External Stakeholders

| Stakeholder Group | Contact | Notification Trigger | Channel | Deadline | Owner |
|-------------------|---------|---------------------|---------|----------|-------|
| Customers (affected) | [Portal/Email] | Data breach involving their data | Email | Per SLA/regulation | Comms Lead |
| Regulators | [List regulators] | Per compliance requirements | Formal letter | Per regulation | Legal |
| Law Enforcement | [FBI field office, local PD] | Criminal activity, significant breach | Phone | When appropriate | Legal + CISO |
| Cyber Insurance | [Carrier contact] | P0, ransomware, significant loss | Phone | Per policy (usually 24-72h) | Legal |
| Media | [PR contact] | Public-facing incidents | Press release | Coordinated | PR Lead |
| Partners/Vendors | [List key partners] | If their data/access affected | Email | Contractual SLA | Account Manager |

---

## 3. Communication Channels

### Internal Channels

| Channel | Use Case | Access Control | Retention |
|---------|----------|----------------|-----------|
| **War Room (Slack/Teams)** | Real-time coordination | Incident responders only | 90 days |
| **Bridge Call (Zoom/Teams)** | Verbal updates, decision making | Invite only | Recorded for 30 days |
| **Email (encrypted)** | Formal updates, documentation | Security team + stakeholders | Per policy |
| **Incident Management System** | Ticket updates, tracking | Role-based | Permanent |
| **Physical War Room** | P0 incidents, sensitive discussions | Badge access | N/A |

### External Channels

| Channel | Use Case | Approval Required | Template |
|---------|----------|-------------------|----------|
| **Customer Portal** | Status updates | Comms Lead | Status page template |
| **Email (formal)** | Breach notifications | Legal + CISO + CEO | Notification template |
| **Press Release** | Media statements | Legal + PR + CEO | Press template |
| **Regulatory Portal** | Compliance filings | Legal | Regulatory template |
| **Phone (hotline)** | Customer inquiries | Comms Lead | FAQ script |

---

## 4. Message Templates

### Template 1: Initial Internal Alert

**Use:** First notification to internal stakeholders

```
SECURITY INCIDENT ALERT

Incident ID: [INC-YYYY-MM-DD-XXX]
Severity: [P0/P1/P2/P3]
Time Detected: [YYYY-MM-DD HH:MM UTC]

SUMMARY:
[2-3 sentence description of what happened]

AFFECTED:
- Systems: [List]
- Users: [Number/scope]

CURRENT STATUS:
[Brief status - investigating/containing/etc.]

INCIDENT TEAM:
- Incident Commander: [Name]
- War Room: [Channel/Link]

NEXT UPDATE: [Time]

DO NOT discuss outside designated channels.
```

### Template 2: Executive Briefing

**Use:** Updates to C-suite and board

```
EXECUTIVE INCIDENT BRIEFING

Date: [Date]
Incident: [INC-ID]
Classification: [CONFIDENTIAL]

SITUATION SUMMARY:
[3-4 sentences - what happened, current state, business impact]

KEY METRICS:
- Severity: [P0/P1]
- Status: [Active/Contained/Resolved]
- Duration: [X hours]
- Systems Affected: [Number]
- Users Impacted: [Number]

BUSINESS IMPACT:
- Revenue: [Impact or "None identified"]
- Operations: [Impact]
- Data Exposure: [Yes/No - if yes, what type]
- Regulatory: [Notification requirements]

ACTIONS TAKEN:
1. [Key action]
2. [Key action]
3. [Key action]

DECISIONS NEEDED:
- [ ] [Decision requiring executive input]

NEXT STEPS:
1. [Next major action]
2. [Timeline for resolution]

NEXT BRIEFING: [Time]

Questions: [Incident Commander, contact]
```

### Template 3: Customer Notification

**Use:** Notifying affected customers (requires Legal approval)

```
Subject: Important Security Notice - Action May Be Required

Dear [Customer Name],

We are writing to inform you of a security incident that [may have
affected / affected] your information.

WHAT HAPPENED:
On [date], we discovered [brief, factual description]. We immediately
[actions taken to secure systems].

WHAT INFORMATION WAS INVOLVED:
[List specific data types affected - be precise]

WHAT WE ARE DOING:
- [Action 1]
- [Action 2]
- [Credit monitoring/protection services if offered]

WHAT YOU CAN DO:
We recommend you:
1. [Specific actionable recommendation]
2. [Specific actionable recommendation]
3. [Specific actionable recommendation]

FOR MORE INFORMATION:
- Dedicated Response Line: [Phone number]
- Email: [Email address]
- FAQ: [URL]
- Hours: [Availability]

We sincerely apologize for any concern this may cause and remain
committed to protecting your information.

Sincerely,
[Name]
[Title]
[Company]
```

### Template 4: Press Statement

**Use:** Media inquiries (requires Legal + PR + CEO approval)

```
[COMPANY LETTERHEAD]

FOR IMMEDIATE RELEASE
[Date]

[COMPANY NAME] STATEMENT ON SECURITY INCIDENT

[City, State] - [Company Name] is aware of [brief, neutral description
of incident/claims].

[One sentence on immediate response actions taken.]

"[Quote from CEO or CISO about commitment to security/customers],"
said [Name], [Title].

[Company Name] is [working with law enforcement / conducting investigation /
taking steps to prevent recurrence].

[If customer data affected: We are notifying affected individuals and
offering [protective services].]

For more information, [affected individuals / customers] can contact
[phone number] or visit [URL].

[Company Name] will provide updates as appropriate.

###

Media Contact:
[Name]
[Email]
[Phone]
```

### Template 5: Regulatory Notification (GDPR Example)

**Use:** Formal regulatory filing (requires Legal + DPO approval)

```
PERSONAL DATA BREACH NOTIFICATION
Pursuant to Article 33, General Data Protection Regulation

To: [Supervisory Authority Name and Address]
From: [Company Name], Data Controller
Date: [YYYY-MM-DD]
Reference: [Internal Reference]

1. NATURE OF BREACH:
[Description including]:
- Categories of data subjects: [e.g., customers, employees]
- Approximate number: [Number]
- Categories of personal data: [e.g., names, email, financial]
- Approximate number of records: [Number]

2. DATA PROTECTION OFFICER CONTACT:
Name: [DPO Name]
Email: [DPO Email]
Phone: [DPO Phone]

3. LIKELY CONSEQUENCES:
[Description of potential impact to data subjects]

4. MEASURES TAKEN:
[Description of measures taken or proposed to]:
- Address the breach
- Mitigate possible adverse effects

5. COMMUNICATION TO DATA SUBJECTS:
[ ] Have been notified
[ ] Will be notified by [date]
[ ] Not required because [reason - e.g., encrypted data]

6. ADDITIONAL INFORMATION:
[Any supplementary details]

Submitted by:
[Name, Title]
[Date, Time]
[Signature]
```

---

## 5. Communication Timeline by Severity

### P0 - Critical Incident

| Timeframe | Action | Owner | Approval |
|-----------|--------|-------|----------|
| T+0 min | Activate war room, page responders | SOC Lead | - |
| T+15 min | Initial alert to executive team | Incident Commander | - |
| T+30 min | First status update (internal) | Comms Lead | IC |
| T+1 hour | Executive briefing call | CISO | - |
| T+2 hours | Legal/compliance assessment | Legal | - |
| T+4 hours | Board notification (if material) | CEO | Legal |
| T+24 hours | Customer notification decision | Legal + CISO | CEO |
| T+72 hours | Regulatory notification (if required) | Legal | CISO |
| Ongoing | Hourly status updates | Comms Lead | IC |

### P1 - High Severity

| Timeframe | Action | Owner | Approval |
|-----------|--------|-------|----------|
| T+0 min | War room activation | SOC Lead | - |
| T+30 min | Initial alert to CISO | Incident Commander | - |
| T+1 hour | First status update | Comms Lead | IC |
| T+2 hours | Executive summary (if business impact) | CISO | - |
| T+4 hours | Legal assessment (if data involved) | Legal | - |
| Ongoing | Bi-hourly status updates | Comms Lead | IC |

### P2/P3 - Medium/Low Severity

| Timeframe | Action | Owner | Approval |
|-----------|--------|-------|----------|
| T+1 hour | Ticket created, initial triage | SOC Analyst | - |
| T+4 hours | Status update to security team | Analyst | - |
| Daily | Summary in daily security report | SOC Lead | - |
| Resolution | Closure notification | Analyst | - |

---

## 6. Approval Matrix

| Communication Type | Required Approvals | Timeline |
|-------------------|-------------------|----------|
| Internal status updates | Incident Commander | Real-time |
| Executive briefings | CISO | Within 15 min |
| Customer notifications | Legal + CISO + CEO | Before sending |
| Regulatory filings | Legal + CISO + DPO | Before deadline |
| Press statements | Legal + PR + CEO | Before release |
| Board notifications | CEO + General Counsel | Per board policy |
| Law enforcement contact | Legal + CISO | Before contact |
| Partner notifications | Legal + Account Manager | Per contract |

---

## 7. Communication Dos and Don'ts

### DO:
- [ ] Stick to verified facts only
- [ ] Use approved templates and channels
- [ ] Document all communications with timestamps
- [ ] Get required approvals before external communications
- [ ] Keep messages concise and actionable
- [ ] Provide clear next steps and contact information
- [ ] Use encrypted channels for sensitive information

### DON'T:
- [ ] Speculate about cause, impact, or attribution
- [ ] Share technical vulnerability details externally
- [ ] Communicate outside designated channels
- [ ] Promise specific timelines without verification
- [ ] Assign blame or use inflammatory language
- [ ] Discuss ongoing investigation details publicly
- [ ] Respond to media without PR/Legal approval

---

## 8. Contact Directory

### Incident Response Team

| Role | Primary | Backup | Phone | Email |
|------|---------|--------|-------|-------|
| CISO | [Name] | [Name] | [Phone] | [Email] |
| SOC Lead | [Name] | [Name] | [Phone] | [Email] |
| Security Engineer | [Name] | [Name] | [Phone] | [Email] |
| Comms Lead | [Name] | [Name] | [Phone] | [Email] |
| Legal Counsel | [Name] | [Name] | [Phone] | [Email] |
| DPO | [Name] | [Name] | [Phone] | [Email] |
| PR Lead | [Name] | [Name] | [Phone] | [Email] |

### External Contacts

| Organization | Contact | Phone | Email/Portal |
|--------------|---------|-------|--------------|
| FBI Cyber Division | [Local field office] | [Phone] | ic3.gov |
| Cyber Insurance | [Carrier name] | [Phone] | [Email] |
| Forensics Firm | [Firm name] | [Phone] | [Email] |
| Legal Firm | [Firm name] | [Phone] | [Email] |
| PR Agency | [Agency name] | [Phone] | [Email] |

### Regulatory Authorities

| Regulator | Jurisdiction | Portal/Contact | Deadline |
|-----------|--------------|----------------|----------|
| ICO | UK GDPR | ico.org.uk | 72 hours |
| [State AG] | [State] | [Portal] | Varies |
| HHS OCR | HIPAA | hhs.gov/ocr | 60 days |
| FTC | US Consumer | ftc.gov | Prompt |
| SEC | US Public Co | sec.gov | 4 business days |

---

## 9. Plan Maintenance

### Review Schedule

| Review Type | Frequency | Owner | Last Completed |
|-------------|-----------|-------|----------------|
| Full plan review | Annual | CISO | [Date] |
| Contact verification | Quarterly | Comms Lead | [Date] |
| Template updates | As needed | Legal | [Date] |
| Tabletop exercise | Semi-annual | Security Team | [Date] |

### Change Log

| Date | Change | Author | Approved By |
|------|--------|--------|-------------|
| [Date] | Initial plan creation | [Name] | [Name] |
| [Date] | [Change description] | [Name] | [Name] |

---

## Appendix A: Quick Reference Card

**Print and post in war room:**

```
INCIDENT COMMUNICATION QUICK REFERENCE

P0/P1 IMMEDIATE ACTIONS:
1. Activate war room: #incident-[ID]
2. Page IC and responders
3. Notify CISO within 15 minutes
4. Begin status updates every 30-60 min

APPROVAL REQUIRED FOR:
- Customer notifications: Legal + CISO + CEO
- Press statements: Legal + PR + CEO
- Regulatory filings: Legal + CISO + DPO

NEVER WITHOUT APPROVAL:
- Media statements
- Customer breach notifications
- Social media posts
- Partner communications

EMERGENCY CONTACTS:
- CISO: [Phone]
- Legal: [Phone]
- PR: [Phone]
- FBI Cyber: [Phone]
```

---

**Classification:** INTERNAL
**Distribution:** Security Team, Legal, Communications
**Last Updated:** YYYY-MM-DD
