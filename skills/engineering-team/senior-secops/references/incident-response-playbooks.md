# Incident Response Playbooks Reference Guide

## Overview
Comprehensive incident response procedures, playbooks, and frameworks for security operations teams to detect, respond to, contain, and recover from security incidents. Covers common incident types, escalation procedures, and post-incident analysis.

## Incident Classification

### Severity Levels

**P0 - Critical (Response Time: Immediate)**
- Active data breach or exfiltration
- Ransomware encryption in progress
- Critical system compromise (prod database, auth systems)
- Active DDoS taking down production
- Customer PII exposure confirmed

**Response:** All hands on deck, exec notification, war room

**P1 - High (Response Time: <30 min)**
- Suspicious access to sensitive systems
- Malware detected on critical systems
- Potential data breach (investigation needed)
- Successful phishing attack on privileged user
- Critical vulnerability exploitation attempt

**Response:** Security team mobilized, on-call engineer paged

**P2 - Medium (Response Time: <4 hours)**
- Malware on non-critical systems
- Failed authentication anomalies
- Policy violations (data mishandling)
- Non-critical system compromise
- Suspicious network traffic

**Response:** Assigned to on-duty SOC analyst

**P3 - Low (Response Time: <24 hours)**
- Security tool alerts requiring investigation
- Policy violations (minor)
- Phishing attempts (blocked)
- Vulnerability scan findings

**Response:** Added to ticket queue

## Incident Response Phases

### Phase 1: Detection & Triage (0-15 min)

**Initial Alert Sources:**
- SIEM alerts (Splunk, ELK, Datadog)
- EDR alerts (CrowdStrike, Carbon Black)
- IDS/IPS (Suricata, Snort)
- Cloud security (AWS GuardDuty, Azure Defender)
- User reports (phishing, suspicious activity)

**Triage Questions:**
1. What triggered the alert? (automatic vs manual report)
2. Which systems/users affected?
3. Is this confirmed malicious or potential false positive?
4. What's the potential impact? (data, systems, users)
5. Is the threat active or historical?

**Immediate Actions:**
- Document in incident management system (Jira, ServiceNow)
- Assign severity level
- Notify on-call engineer if P0/P1
- Begin evidence collection (logs, screenshots)

### Phase 2: Containment (15-60 min)

**Short-Term Containment (stop the bleeding):**

**For Compromised Accounts:**
- [ ] Disable user account immediately
- [ ] Revoke active sessions/tokens
- [ ] Reset credentials
- [ ] Check for newly created accounts
- [ ] Review recent account activity (logs)

**For Compromised Systems:**
- [ ] Isolate system from network (disconnect or VLAN quarantine)
- [ ] Preserve system state (don't shut down - capture memory)
- [ ] Block malicious IPs at firewall
- [ ] Disable compromised services
- [ ] Take forensic snapshot

**For Data Breach:**
- [ ] Identify scope of exposed data
- [ ] Disable access vectors (close S3 bucket, patch vulnerability)
- [ ] Preserve evidence (logs, access records)
- [ ] Assess if data was exfiltrated (network logs)
- [ ] Begin notification process (legal, compliance)

**For Ransomware:**
- [ ] Isolate infected systems immediately
- [ ] Disable network shares to prevent spread
- [ ] Identify ransomware variant (malware hash, ransom note)
- [ ] Check backups (availability, last backup date)
- [ ] Do NOT pay ransom (FBI recommendation)

**Long-Term Containment (prevent recurrence):**
- Apply patches to vulnerabilities
- Update detection rules
- Strengthen authentication (MFA enforcement)
- Segment networks further
- Update firewall rules

### Phase 3: Investigation & Analysis (1-24 hours)

**Root Cause Analysis:**
1. **Timeline:** When did compromise begin?
2. **Attack Vector:** How did attacker gain access?
3. **Lateral Movement:** Where did they go?
4. **Data Access:** What data was accessed/exfiltrated?
5. **Persistence:** Did they establish backdoors?

**Evidence Collection:**
- System logs (auth, application, network)
- Network traffic captures (PCAP)
- Memory dumps
- Disk images
- Email headers (phishing investigations)
- Cloud API logs (AWS CloudTrail, Azure Activity Log)

**Tools:**
- Log analysis: Splunk, ELK Stack
- Forensics: Volatility (memory), Autopsy (disk)
- Network: Wireshark, Zeek
- Malware analysis: Cuckoo Sandbox, VirusTotal

**Analysis Questions:**
- What vulnerabilities were exploited?
- Was this targeted or opportunistic?
- Are other systems vulnerable to same attack?
- What controls failed?
- Could this have been detected sooner?

### Phase 4: Eradication (2-48 hours)

**Remove Threat:**
- [ ] Delete malware from all affected systems
- [ ] Remove backdoors and persistence mechanisms
- [ ] Patch vulnerabilities exploited
- [ ] Rebuild compromised systems from clean images
- [ ] Rotate all potentially compromised credentials
- [ ] Update security rules (WAF, IDS, EDR)

**Verification:**
- [ ] Scan all systems for IOCs (indicators of compromise)
- [ ] Verify malware signatures not present
- [ ] Confirm backdoors removed
- [ ] Test vulnerability patches
- [ ] Review logs for re-compromise attempts

### Phase 5: Recovery (2-7 days)

**Restore Operations:**
- [ ] Restore systems from clean backups (if applicable)
- [ ] Re-enable user accounts (with new credentials)
- [ ] Restore network connectivity
- [ ] Monitor for re-compromise (24-48 hour watch)
- [ ] Re-enable services incrementally
- [ ] Validate business operations

**Monitoring:**
- Enhanced logging for 30 days
- Daily review of related alerts
- Threat hunting for similar TTPs (tactics, techniques, procedures)

### Phase 6: Post-Incident Review (1-2 weeks after)

**Retrospective Meeting:**
- What happened? (timeline, root cause)
- What went well? (effective responses)
- What went poorly? (gaps, delays)
- What should we change? (process, tools, training)

**Deliverables:**
- Incident report (executive summary)
- Timeline of events
- Impact assessment (systems, data, downtime)
- Lessons learned
- Action items (process improvements, tool enhancements)

**Follow-Up Actions:**
- Implement process improvements
- Update runbooks
- Security awareness training (if human error involved)
- Vulnerability remediation
- Tool enhancements

## Common Incident Playbooks

### Playbook: Phishing Attack

**Indicators:**
- User reports suspicious email
- Email from spoofed sender
- Malicious link or attachment
- Request for credentials or payment

**Response Steps:**
1. Isolate: Have user forward email (don't click links), delete from inbox
2. Analyze: Check email headers, extract links/attachments
3. Scan: Submit to VirusTotal, analyze in sandbox
4. Block: Add sender to email block list, block malicious domains at firewall
5. Hunt: Search for similar emails across organization
6. Train: Send security awareness reminder to company

**Prevention:**
- SPF/DKIM/DMARC email authentication
- Link rewriting (Proofpoint, Mimecast)
- User training (monthly phishing simulations)

### Playbook: Ransomware

**Indicators:**
- Files encrypted (.locked, .encrypted extensions)
- Ransom note (text file or screen lock)
- Backup deletion attempts
- Lateral movement (SMB traffic spikes)

**Response Steps:**
1. Isolate: Disconnect infected systems immediately
2. Preserve: Take forensic snapshots before cleanup
3. Identify: Determine ransomware variant (use ID Ransomware)
4. Assess: Check backup availability and integrity
5. Restore: Rebuild systems from clean backups
6. Report: File FBI IC3 report, notify cyber insurance

**Do NOT:**
- Pay ransom (funds criminal activity, no guarantee of decryption)
- Connect systems until clean

**Prevention:**
- Offline/immutable backups
- Network segmentation
- Endpoint detection (EDR)
- Email filtering

### Playbook: Data Breach

**Indicators:**
- Unauthorized access to databases
- Large data downloads
- Exposed S3 bucket or public GitHub repo
- Customer report of compromised data

**Response Steps:**
1. Contain: Close access vector immediately
2. Scope: Determine what data was exposed (PII, PCI, PHI?)
3. Legal: Notify legal counsel and compliance team
4. Notify: Determine notification requirements (GDPR 72 hours, state breach laws)
5. Remediate: Fix root cause (patch vulnerability, restrict access)
6. Communicate: Prepare customer notification, PR statement

**Notification Requirements:**
- GDPR: 72 hours to regulator, immediate to affected individuals
- CCPA: Without unreasonable delay
- HIPAA: 60 days to HHS and affected individuals
- PCI DSS: Immediate to payment brands and acquiring bank

### Playbook: Compromised Cloud Account

**Indicators:**
- Unusual AWS/Azure/GCP activity
- Resource creation from new IPs
- Cryptocurrency mining instances
- CloudTrail/Activity Log anomalies

**Response Steps:**
1. Revoke: Disable compromised IAM credentials immediately
2. Audit: Review CloudTrail logs for unauthorized actions
3. Cleanup: Terminate unauthorized resources
4. Harden: Enforce MFA on all accounts
5. Monitor: Enable GuardDuty/Defender alerts

**Prevention:**
- MFA enforcement
- Least privilege IAM policies
- Access key rotation (90 days)
- CloudTrail/Activity Log monitoring

## Communication Protocols

### Internal Communication

**War Room:**
- Platform: Zoom/Slack war room channel
- Participants: Security team, on-call engineer, manager
- Frequency: Every 30-60 min updates during active incident

**Status Updates:**
- To: Engineering leadership, affected teams
- Frequency: Every 2-4 hours (P0/P1)
- Format: Brief summary, current status, ETA to resolution

### External Communication

**Customer Communication:**
- For P0 (customer-impacting): Status page update within 1 hour
- For data breach: Legal-approved notification
- Channel: Email, status page, support tickets

**Regulatory Reporting:**
- GDPR breach: 72 hours to supervisory authority
- PCI breach: Immediate to payment brands
- HIPAA breach: 60 days to HHS

**Law Enforcement:**
- FBI IC3 for ransomware, BEC fraud
- Secret Service for financial fraud
- Local police for physical threats

## Tools & Resources

**SIEM/Log Analysis:**
- Splunk Enterprise Security
- Elastic Security (ELK Stack)
- Datadog Security Monitoring

**Endpoint Detection (EDR):**
- CrowdStrike Falcon
- Carbon Black
- Microsoft Defender for Endpoint

**Incident Management:**
- PagerDuty (alerting)
- Jira Service Management (ticketing)
- ServiceNow (enterprise)

**Threat Intelligence:**
- MISP (Malware Information Sharing Platform)
- AlienVault OTX
- VirusTotal

**Forensics:**
- Volatility (memory forensics)
- Autopsy (disk forensics)
- Wireshark (network analysis)

---
**Last Updated:** November 23, 2025
**Related:** compliance_requirements.md, security_standards.md, vulnerability_management_guide.md
