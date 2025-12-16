# Incident Communication Templates

## Overview

Effective communication during security incidents is critical for coordination, stakeholder management, and regulatory compliance. This guide provides templates and protocols for all incident communication needs.

## Internal Communication

### War Room Setup Notification

**Channel:** Security incident Slack/Teams channel

```
=== INCIDENT WAR ROOM ACTIVATED ===

Incident ID: [INC-YYYY-MM-DD-XXX]
Severity: [P0/P1/P2/P3]
Time: [YYYY-MM-DD HH:MM UTC]

INCIDENT SUMMARY:
[Brief 2-3 sentence description of the incident]

AFFECTED SYSTEMS:
- [System 1]
- [System 2]

WAR ROOM DETAILS:
- Channel: #incident-[INC-ID]
- Bridge: [Zoom/Teams link]
- Incident Commander: [Name]

ROLES ASSIGNED:
- Incident Commander: [Name]
- Technical Lead: [Name]
- Communications Lead: [Name]
- Scribe: [Name]

NEXT UPDATE: [Time] or as situation changes

DO NOT discuss this incident outside designated channels.
```

### Status Update Template (Every 30-60 minutes)

```
=== INCIDENT STATUS UPDATE ===

Incident ID: [INC-ID]
Update #: [X]
Time: [YYYY-MM-DD HH:MM UTC]
Severity: [P0/P1/P2/P3]
Status: [ACTIVE | CONTAINED | INVESTIGATING | RESOLVED]

CURRENT SITUATION:
[2-3 sentences describing current state]

ACTIONS COMPLETED SINCE LAST UPDATE:
- [Action 1] - [Completed/In Progress]
- [Action 2] - [Completed/In Progress]

IN PROGRESS:
- [Current action being taken]

BLOCKERS/NEEDS:
- [Any blockers or resource needs]

NEXT STEPS:
1. [Next action]
2. [Following action]

ETA TO [CONTAINMENT/RESOLUTION]: [Time estimate or "Unknown"]

NEXT UPDATE: [Time]

Questions? Contact: [Incident Commander]
```

### Escalation Notification (P0/P1)

```
=== URGENT: SECURITY INCIDENT ESCALATION ===

TO: [Executive Team / CISO / CTO]
FROM: Security Operations
TIME: [YYYY-MM-DD HH:MM UTC]

INCIDENT DETAILS:
- ID: [INC-ID]
- Severity: [P0/P1]
- Status: [ACTIVE/CONTAINED]

EXECUTIVE SUMMARY:
[3-4 sentences describing incident, impact, and current response]

BUSINESS IMPACT:
- Affected Systems: [List]
- Affected Users: [Number]
- Estimated Downtime: [Hours]
- Data Exposure Risk: [High/Medium/Low]

IMMEDIATE ACTIONS TAKEN:
1. [Action 1]
2. [Action 2]
3. [Action 3]

REQUIRED DECISIONS:
- [ ] [Decision needed from leadership]
- [ ] [Resource approval needed]

NEXT BRIEFING: [Time]

Contact for questions: [Incident Commander, phone]
```

### Incident Closure Notification

```
=== INCIDENT RESOLVED ===

Incident ID: [INC-ID]
Resolution Time: [YYYY-MM-DD HH:MM UTC]
Total Duration: [X hours Y minutes]

RESOLUTION SUMMARY:
[Brief description of how incident was resolved]

ROOT CAUSE:
[High-level root cause - detailed RCA to follow]

IMPACT SUMMARY:
- Affected Systems: [Number]
- Affected Users: [Number]
- Downtime: [Duration]
- Data Exposure: [Yes/No - details if yes]

POST-INCIDENT:
- Full RCA scheduled: [Date]
- Lessons learned meeting: [Date]
- Action items tracking: [Jira/Link]

IMMEDIATE FOLLOW-UPS:
1. [Follow-up item]
2. [Follow-up item]

Thank you to everyone who assisted with response.

Full incident report will be distributed by: [Date]
```

## External Communication

### Customer Notification (Data Breach)

**Note:** All external communications must be reviewed by Legal before sending.

```
Subject: Important Security Notice from [Company Name]

Dear [Customer Name],

We are writing to inform you of a security incident that may have affected
your personal information.

WHAT HAPPENED:
On [date], we discovered [brief, factual description of incident]. We
immediately took action to secure our systems and launched an investigation
with the assistance of [external forensics firm, if applicable].

WHAT INFORMATION WAS INVOLVED:
Based on our investigation, the following information may have been accessed:
- [Type of data]
- [Type of data]

WHAT WE ARE DOING:
We have taken the following steps:
- [Action 1]
- [Action 2]
- [Action 3]

We are also offering [credit monitoring/identity protection services] at
no cost to you for [X months/years].

WHAT YOU CAN DO:
We recommend you take the following precautions:
1. [Recommended action]
2. [Recommended action]
3. [Recommended action]

FOR MORE INFORMATION:
If you have questions, please contact our dedicated response team:
- Phone: [Number]
- Email: [Email]
- Website: [URL]

We sincerely apologize for any concern this may cause and are committed
to protecting your information.

Sincerely,
[Name]
[Title]
[Company Name]
```

### Regulatory Notification (GDPR - 72 hours)

```
PERSONAL DATA BREACH NOTIFICATION
[Under Article 33 of the General Data Protection Regulation]

To: [Supervisory Authority]
From: [Company Name], Data Controller
Date: [YYYY-MM-DD]
Reference: [Internal Reference Number]

1. NATURE OF THE BREACH:
[Description of the breach including categories of data and approximate
number of data subjects affected]

- Categories of data subjects affected: [e.g., customers, employees]
- Approximate number of data subjects: [Number]
- Categories of personal data: [e.g., names, email addresses]
- Approximate number of records: [Number]

2. CONTACT DETAILS:
Data Protection Officer: [Name]
Email: [Email]
Phone: [Phone]

3. LIKELY CONSEQUENCES:
[Description of the likely consequences of the breach]

4. MEASURES TAKEN:
[Description of measures taken or proposed to address the breach and
mitigate possible adverse effects]

5. COMMUNICATION TO DATA SUBJECTS:
[ ] Data subjects have been informed
[ ] Data subjects will be informed by [date]
[ ] Communication to data subjects is not required because [reason]

6. ADDITIONAL INFORMATION:
[Any other relevant information]

Submitted by:
[Name, Title]
[Date, Time]
```

### Press Statement Template

```
[COMPANY LETTERHEAD]

FOR IMMEDIATE RELEASE
[Date]

[COMPANY NAME] RESPONDS TO SECURITY INCIDENT

[City, State] – [Company Name] today announced that it recently discovered
a security incident affecting [brief description].

Upon discovery on [date], [Company Name] immediately [actions taken]. The
company has engaged [law enforcement/forensic experts] and is actively
investigating the incident.

"[Quote from CEO/CISO about company's commitment to security and customer
trust]," said [Name], [Title] of [Company Name].

The company is notifying potentially affected individuals and offering
[protective services offered]. [Company Name] has established a dedicated
response line at [phone number] and website at [URL] for those with questions.

[Company Name] takes the security of [customer/user] information seriously
and is implementing additional safeguards to prevent similar incidents in
the future.

###

Media Contact:
[Name]
[Email]
[Phone]
```

## Communication Timing Guidelines

### Notification Deadlines by Regulation

| Regulation | Deadline | Recipient | Notes |
|------------|----------|-----------|-------|
| GDPR | 72 hours | Supervisory authority | From awareness of breach |
| GDPR | Without undue delay | Data subjects | If high risk to rights |
| CCPA | Without unreasonable delay | Attorney General (>500 CA residents) | 30 days recommended |
| HIPAA | 60 days | HHS OCR | From discovery |
| HIPAA | 60 days | Affected individuals | From discovery |
| HIPAA | Immediate | Media (if >500 residents in state) | - |
| PCI DSS | Immediately | Payment brands | Upon discovery |
| PCI DSS | Immediately | Acquiring bank | Upon discovery |
| SEC | 4 business days | SEC (material incidents) | Form 8-K |

### Internal Notification Timing

| Severity | Initial Notification | Status Updates | Escalation |
|----------|---------------------|----------------|------------|
| P0 | Immediate | Every 30 min | Immediate to executives |
| P1 | Within 15 min | Every 60 min | Within 30 min if uncontained |
| P2 | Within 1 hour | Every 2-4 hours | If escalates |
| P3 | Within 4 hours | Daily | As needed |

## Communication Approval Matrix

| Communication Type | Approval Required |
|-------------------|-------------------|
| Internal status updates | Incident Commander |
| Executive briefings | CISO |
| Customer notifications | Legal + CISO + CEO |
| Regulatory notifications | Legal + CISO + DPO |
| Press statements | Legal + PR + CEO |
| Law enforcement contact | Legal + CISO |

## Post-Incident Communication

### Lessons Learned Meeting Invitation

```
Subject: Incident [INC-ID] Post-Incident Review

You are invited to the post-incident review for [INC-ID].

Meeting Details:
- Date: [Date]
- Time: [Time]
- Location: [Room/Video link]
- Duration: 90 minutes

Agenda:
1. Incident Timeline Review (20 min)
2. Root Cause Analysis Discussion (20 min)
3. What Went Well (15 min)
4. Areas for Improvement (15 min)
5. Action Items and Owners (15 min)
6. Open Discussion (5 min)

Pre-Reading:
- Incident Report: [Link]
- Timeline: [Link]

Please come prepared to discuss your involvement and observations.

This is a blameless review focused on process improvement.
```

### Executive Summary Report

```
INCIDENT EXECUTIVE SUMMARY
Incident ID: [INC-ID]
Classification: [CONFIDENTIAL]
Date: [YYYY-MM-DD]

OVERVIEW
On [date], [Company Name] experienced a [type of incident] that resulted
in [brief impact summary]. The incident was detected at [time], contained
at [time], and resolved at [time].

KEY METRICS
- Time to Detect: [X hours]
- Time to Contain: [X hours]
- Time to Resolve: [X hours]
- Systems Affected: [Number]
- Users Affected: [Number]
- Estimated Cost: $[Amount]

ROOT CAUSE
[2-3 sentence summary of root cause]

RESPONSE EFFECTIVENESS
[Summary of what went well and what needs improvement]

REMEDIATION STATUS
| Action | Status | Owner | Due Date |
|--------|--------|-------|----------|
| [Action] | [Status] | [Name] | [Date] |

RECOMMENDED INVESTMENTS
1. [Recommendation with estimated cost]
2. [Recommendation with estimated cost]

CONCLUSION
[Summary statement about incident handling and forward-looking security
posture improvements]

Prepared by: [Name, Title]
Reviewed by: [Name, Title]
Date: [YYYY-MM-DD]
```

## Communication Don'ts

### Never Include in External Communications:
- Technical details of vulnerabilities
- Specific attack methods
- Names of attackers (if known)
- Speculation about impact
- Unverified information
- Blame or finger-pointing

### Never Share Externally Without Legal Review:
- Customer notifications
- Regulatory filings
- Press statements
- Social media posts about incidents
- Responses to media inquiries

## Quick Reference: Communication Checklist

### P0/P1 Incident Communication Checklist

- [ ] War room activated and notified
- [ ] Executive notification sent
- [ ] Status update schedule established
- [ ] Communications lead assigned
- [ ] Legal notified (for potential external comms)
- [ ] PR on standby (if customer-facing)
- [ ] Regulatory notification timeline documented
- [ ] Customer notification draft prepared (if needed)

### Incident Closure Communication Checklist

- [ ] Internal resolution notification sent
- [ ] War room closed
- [ ] Customer notifications sent (if required)
- [ ] Regulatory notifications filed (if required)
- [ ] Lessons learned meeting scheduled
- [ ] Final report distributed
- [ ] Action items assigned and tracked

---
**Last Updated:** December 16, 2025
**Related:** incident-response-playbooks.md, forensics-evidence-guide.md
**Approval Required:** Legal review for all external communications
