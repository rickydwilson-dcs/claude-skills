# Incident Report: [INC-YYYY-MM-DD-XXX]

## Document Information

| Field | Value |
|-------|-------|
| **Report Date** | YYYY-MM-DD |
| **Incident ID** | INC-YYYY-MM-DD-XXX |
| **Classification** | CONFIDENTIAL |
| **Author** | [Name, Title] |
| **Reviewed By** | [Name, Title] |
| **Distribution** | [Security Team / Executive Team / Board] |

---

## Executive Summary

[Provide a 2-3 paragraph summary suitable for executive leadership. Include:
- What happened (high-level)
- Business impact
- Current status
- Key takeaways]

---

## Incident Overview

### Key Metrics

| Metric | Value |
|--------|-------|
| **Detection Time** | YYYY-MM-DD HH:MM UTC |
| **Containment Time** | YYYY-MM-DD HH:MM UTC |
| **Resolution Time** | YYYY-MM-DD HH:MM UTC |
| **Severity** | P0 / P1 / P2 / P3 |
| **Status** | Resolved / Ongoing |

### Response Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Mean Time to Detect (MTTD) | X hours | <1 hour | Met/Missed |
| Mean Time to Respond (MTTR) | X hours | <4 hours | Met/Missed |
| Mean Time to Contain (MTTC) | X hours | <8 hours | Met/Missed |
| Mean Time to Recover (MTTRec) | X hours | <24 hours | Met/Missed |

---

## Timeline of Events

| Timestamp (UTC) | Event | Actor | System | Notes |
|-----------------|-------|-------|--------|-------|
| YYYY-MM-DD HH:MM | Initial compromise | Attacker | [System] | [Details] |
| YYYY-MM-DD HH:MM | Lateral movement | Attacker | [System] | [Details] |
| YYYY-MM-DD HH:MM | Alert triggered | SIEM | [System] | [Details] |
| YYYY-MM-DD HH:MM | Incident declared | SOC | - | [Details] |
| YYYY-MM-DD HH:MM | Containment action | Security | [System] | [Details] |
| YYYY-MM-DD HH:MM | Incident resolved | Security | - | [Details] |

---

## Root Cause Analysis

### Attack Vector
[Describe how the attacker gained initial access]

**Classification:** [ ] Phishing [ ] Vulnerability [ ] Credential Theft [ ] Misconfiguration [ ] Insider [ ] Other

### Entry Point
[Specific system, service, or user account that was compromised first]

### Attack Path

```
[Initial Access] → [Persistence] → [Privilege Escalation] → [Lateral Movement] → [Objective]

Example:
Phishing Email → Macro Execution → Credential Dumping → Domain Admin → Data Exfiltration
```

### Vulnerability Exploited
- **CVE ID:** [If applicable]
- **Description:** [Vulnerability description]
- **Patch Status:** [Available/Applied/Pending]

### MITRE ATT&CK TTPs Identified

| Tactic | Technique | ID | Evidence |
|--------|-----------|-----|----------|
| Initial Access | [Technique] | T#### | [Evidence] |
| Execution | [Technique] | T#### | [Evidence] |
| Persistence | [Technique] | T#### | [Evidence] |
| Privilege Escalation | [Technique] | T#### | [Evidence] |
| Defense Evasion | [Technique] | T#### | [Evidence] |
| Lateral Movement | [Technique] | T#### | [Evidence] |
| Collection | [Technique] | T#### | [Evidence] |
| Exfiltration | [Technique] | T#### | [Evidence] |

---

## Impact Assessment

### Systems Affected

| System | Role | Impact | Recovery Status |
|--------|------|--------|-----------------|
| [System 1] | [Role] | [Impact] | Recovered |
| [System 2] | [Role] | [Impact] | Recovered |

### Users Affected
- **Internal Users:** [Number]
- **External Users/Customers:** [Number]

### Data Exposure

| Data Type | Records | Confirmed Exposure | Confirmed Exfiltration |
|-----------|---------|-------------------|----------------------|
| PII | [Number] | Yes/No | Yes/No |
| Credentials | [Number] | Yes/No | Yes/No |
| Financial | [Number] | Yes/No | Yes/No |
| Proprietary | [Volume] | Yes/No | Yes/No |

### Business Impact

| Category | Impact Level | Description |
|----------|--------------|-------------|
| Confidentiality | High/Medium/Low | [Description] |
| Integrity | High/Medium/Low | [Description] |
| Availability | High/Medium/Low | [Description] |
| Financial | $[Amount] | [Breakdown] |
| Reputational | High/Medium/Low | [Description] |
| Regulatory | High/Medium/Low | [Requirements triggered] |

### Financial Impact Estimate

| Category | Amount |
|----------|--------|
| Investigation/Forensics | $[Amount] |
| Legal Fees | $[Amount] |
| Customer Notification | $[Amount] |
| Credit Monitoring | $[Amount] |
| System Recovery | $[Amount] |
| Business Interruption | $[Amount] |
| Regulatory Fines (Potential) | $[Amount] |
| **Total Estimated** | **$[Amount]** |

---

## Response Actions Taken

### Detection Phase
1. [Action taken]
2. [Action taken]

### Containment Phase
1. [Action taken]
2. [Action taken]

### Eradication Phase
1. [Action taken]
2. [Action taken]

### Recovery Phase
1. [Action taken]
2. [Action taken]

---

## Regulatory and Notification Status

### Regulatory Notifications

| Regulation | Required | Deadline | Status | Date Submitted |
|------------|----------|----------|--------|----------------|
| GDPR | Yes/No | [Date] | Pending/Complete | [Date] |
| HIPAA | Yes/No | [Date] | Pending/Complete | [Date] |
| PCI DSS | Yes/No | [Date] | Pending/Complete | [Date] |
| State Laws | Yes/No | [Date] | Pending/Complete | [Date] |

### Customer Notifications
- **Required:** Yes / No
- **Number to Notify:** [Number]
- **Status:** Pending / In Progress / Complete
- **Date Sent:** [Date]

---

## Lessons Learned

### What Went Well
1. [Positive observation]
2. [Positive observation]
3. [Positive observation]

### Areas for Improvement
1. [Improvement area]
2. [Improvement area]
3. [Improvement area]

### Control Failures

| Control | Expected | Actual | Gap |
|---------|----------|--------|-----|
| [Control] | [Expected behavior] | [Actual behavior] | [Gap identified] |

---

## Remediation Plan

### Immediate Actions (24-48 hours)

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | [ ] Open |
| [Action] | [Name] | [Date] | [ ] Open |

### Short-Term (30 days)

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | [ ] Open |
| [Action] | [Name] | [Date] | [ ] Open |

### Medium-Term (90 days)

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | [ ] Open |
| [Action] | [Name] | [Date] | [ ] Open |

### Long-Term (6-12 months)

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | [ ] Open |

---

## Appendices

### Appendix A: Evidence Inventory

| Evidence ID | Type | Source | Hash (SHA-256) | Location |
|-------------|------|--------|----------------|----------|
| EVD-001 | [Type] | [Source] | [Hash] | [Path] |

### Appendix B: IOC List

| IOC Type | Value | Context | Action |
|----------|-------|---------|--------|
| IP | [IP] | [Context] | Blocked |
| Domain | [Domain] | [Context] | Blocked |
| Hash | [Hash] | [Context] | Added to EDR |

### Appendix C: Communication Log

| Date/Time | Type | Audience | Summary |
|-----------|------|----------|---------|
| [DateTime] | [Type] | [Audience] | [Summary] |

---

## Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Report Author | | | |
| Security Lead | | | |
| CISO | | | |

---

**Classification:** CONFIDENTIAL
**Distribution:** Limited to authorized personnel only
