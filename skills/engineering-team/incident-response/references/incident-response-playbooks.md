# Incident Response Playbooks Reference Guide

## Overview

Comprehensive incident response procedures, playbooks, and frameworks for security operations teams to detect, respond to, contain, and recover from security incidents. This guide integrates with the incident-response Python tools for automated detection, containment, and analysis.

## Incident Classification

### Severity Levels

| Severity | Response Time | Description | Examples |
|----------|---------------|-------------|----------|
| **P0 - Critical** | Immediate | Active breach, confirmed data exfiltration, critical system compromise | Active ransomware, confirmed PII breach, prod DB compromise |
| **P1 - High** | <30 minutes | Potential breach, suspicious privileged activity | Malware on critical systems, successful phishing on admin |
| **P2 - Medium** | <4 hours | Anomalies, policy violations, contained threats | Failed attacks, non-critical malware, policy violations |
| **P3 - Low** | <24 hours | Informational alerts, blocked attempts | Blocked phishing, vulnerability scan findings |

### Escalation Matrix

```
P3 (Low)     → SOC Analyst (ticket queue)
P2 (Medium)  → On-duty SOC Analyst (direct assignment)
P1 (High)    → Security Team Lead + On-call Engineer (page)
P0 (Critical) → All Hands + CISO + Executive Team (war room)
```

## Incident Response Phases

### Phase 1: Detection & Triage (0-15 minutes)

**Objectives:**
- Identify and classify the incident
- Assign severity level
- Begin evidence preservation
- Initiate response procedures

**Tool Integration:**
```bash
# Automated detection and triage
python incident_detector.py --input /var/log/ --output json --file triage.json

# Filter for high-severity only
python incident_detector.py --input alerts.json --severity P1
```

**Triage Checklist:**
- [ ] What triggered the alert? (SIEM, EDR, user report, etc.)
- [ ] Which systems/users are affected?
- [ ] Is this confirmed malicious or potential false positive?
- [ ] What's the potential impact? (data, systems, users)
- [ ] Is the threat active or historical?
- [ ] Has this incident type been seen before?

**Immediate Actions:**
1. Document in incident management system
2. Assign incident ID and severity level
3. Notify appropriate responders based on severity
4. Begin evidence collection (preserve logs, screenshots)

### Phase 2: Containment (15-60 minutes)

**Objectives:**
- Stop the bleeding (prevent further damage)
- Isolate affected systems
- Preserve evidence
- Prevent lateral movement

**Tool Integration:**
```bash
# Execute containment playbook
python incident_responder.py --incident INC-001 --playbook ransomware

# Specific containment action
python incident_responder.py --incident INC-001 --action isolate --target server01

# Collect evidence during containment
python incident_responder.py --incident INC-001 --collect-evidence --paths /var/log/auth.log
```

**Short-Term Containment:**

| Scenario | Actions |
|----------|---------|
| **Compromised Account** | Disable account, revoke sessions, reset credentials, check for new accounts |
| **Compromised System** | Network isolation (disconnect/VLAN), preserve memory, block malicious IPs |
| **Data Breach** | Close access vectors, identify data scope, preserve logs, notify legal |
| **Ransomware** | Isolate systems, disable shares, identify variant, verify backups |

**Long-Term Containment:**
- Apply emergency patches
- Update detection rules
- Strengthen authentication (enforce MFA)
- Segment networks further
- Update firewall rules

### Phase 3: Investigation & Analysis (1-24 hours)

**Objectives:**
- Determine root cause
- Map attack timeline
- Identify full scope of compromise
- Collect forensic evidence

**Tool Integration:**
```bash
# Root cause analysis
python incident_analyzer.py --incident INC-001 --rca --attack-vector phishing

# Impact assessment
python incident_analyzer.py --incident INC-001 --impact

# Full incident report
python incident_analyzer.py --incident INC-001 --report --output markdown
```

**Investigation Questions:**
1. **Timeline:** When did compromise begin?
2. **Attack Vector:** How did attacker gain access?
3. **Lateral Movement:** Where did they go after initial access?
4. **Data Access:** What data was accessed/exfiltrated?
5. **Persistence:** Did they establish backdoors?

**Evidence Collection Priority (Order of Volatility):**
1. Memory (RAM) - Most volatile
2. Network connections
3. Running processes
4. System logs
5. Disk contents - Least volatile

### Phase 4: Eradication (2-48 hours)

**Objectives:**
- Remove all traces of the threat
- Patch vulnerabilities exploited
- Remove persistence mechanisms
- Verify clean state

**Eradication Checklist:**
- [ ] Delete malware from all affected systems
- [ ] Remove backdoors and persistence mechanisms
- [ ] Patch exploited vulnerabilities
- [ ] Rebuild compromised systems from clean images
- [ ] Rotate all potentially compromised credentials
- [ ] Update security rules (WAF, IDS, EDR)

**Verification:**
- [ ] Scan all systems for indicators of compromise (IOCs)
- [ ] Verify malware signatures not present
- [ ] Confirm backdoors removed
- [ ] Test vulnerability patches
- [ ] Review logs for re-compromise attempts

### Phase 5: Recovery (2-7 days)

**Objectives:**
- Restore normal operations
- Validate system integrity
- Monitor for re-compromise
- Return to business as usual

**Recovery Steps:**
1. Restore systems from clean backups (if applicable)
2. Re-enable user accounts (with new credentials)
3. Restore network connectivity incrementally
4. Monitor enhanced for 24-48 hours
5. Re-enable services in priority order
6. Validate business operations

**Post-Recovery Monitoring:**
- Enhanced logging for 30 days minimum
- Daily review of related alerts
- Threat hunting for similar TTPs
- User behavior analytics enabled

### Phase 6: Post-Incident Review (1-2 weeks after)

**Objectives:**
- Document lessons learned
- Improve processes
- Update playbooks
- Prevent recurrence

**Retrospective Agenda:**
1. What happened? (timeline, root cause)
2. What went well? (effective responses)
3. What went poorly? (gaps, delays)
4. What should we change? (process, tools, training)

**Deliverables:**
- Incident report (executive summary)
- Timeline of events
- Impact assessment (systems, data, downtime)
- Lessons learned document
- Action items (process improvements)

## Common Incident Playbooks

### Playbook: Phishing Attack

**Indicators:**
- User reports suspicious email
- Spoofed sender address
- Malicious link or attachment
- Request for credentials/payment

**Response Steps:**
```bash
# Execute phishing playbook
python incident_responder.py --incident INC-001 --playbook phishing
```

1. **Isolate:** Forward email (don't click links), delete from inbox
2. **Analyze:** Check email headers, extract links/attachments
3. **Scan:** Submit to sandbox analysis (VirusTotal, etc.)
4. **Block:** Add sender to blocklist, block malicious domains
5. **Hunt:** Search for similar emails across organization
6. **Train:** Send security awareness reminder

**Prevention Controls:**
- SPF/DKIM/DMARC email authentication
- Link rewriting and sandboxing
- Regular phishing simulations

### Playbook: Ransomware

**Indicators:**
- Files encrypted with unusual extensions
- Ransom note displayed
- Backup deletion attempts
- Unusual SMB traffic (lateral spread)

**Response Steps:**
```bash
# Execute ransomware playbook - IMMEDIATE ACTION
python incident_responder.py --incident INC-001 --playbook ransomware
```

1. **Isolate:** Disconnect infected systems IMMEDIATELY
2. **Preserve:** Take forensic snapshots (memory first)
3. **Identify:** Determine ransomware variant (ID Ransomware)
4. **Assess:** Verify backup availability and integrity
5. **Restore:** Rebuild from clean backups
6. **Report:** File FBI IC3 report, notify cyber insurance

**Critical Rules:**
- DO NOT pay ransom (no guarantee, funds criminals)
- DO NOT shut down systems (preserve memory)
- DO NOT reconnect until verified clean

### Playbook: Data Breach

**Indicators:**
- Unauthorized database access
- Large data downloads/exports
- Exposed cloud storage (S3, etc.)
- Customer reports of compromised data

**Response Steps:**
```bash
# Execute data breach playbook
python incident_responder.py --incident INC-001 --playbook data_breach
```

1. **Contain:** Close access vector immediately
2. **Scope:** Determine what data was exposed (PII, PCI, PHI?)
3. **Legal:** Notify legal counsel and compliance team
4. **Notify:** Determine regulatory notification requirements
5. **Remediate:** Fix root cause (patch, restrict access)
6. **Communicate:** Prepare customer/PR notifications

**Notification Timelines:**
| Regulation | Deadline | Authority |
|------------|----------|-----------|
| GDPR | 72 hours | Supervisory authority |
| CCPA | Without unreasonable delay | Attorney General |
| HIPAA | 60 days | HHS + affected individuals |
| PCI DSS | Immediate | Payment brands + acquiring bank |

### Playbook: Cloud Account Compromise

**Indicators:**
- Unusual AWS/Azure/GCP activity
- Resource creation from new IPs/regions
- Cryptocurrency mining instances
- CloudTrail anomalies

**Response Steps:**
```bash
# Execute cloud compromise playbook
python incident_responder.py --incident INC-001 --playbook cloud_compromise
```

1. **Revoke:** Disable compromised IAM credentials immediately
2. **Audit:** Review CloudTrail/Activity logs
3. **Cleanup:** Terminate unauthorized resources
4. **Harden:** Enforce MFA on all accounts
5. **Monitor:** Enable GuardDuty/Defender alerts

**Prevention Controls:**
- MFA enforcement on all accounts
- Least privilege IAM policies
- Access key rotation (90 days)
- CloudTrail monitoring with alerts

### Playbook: Insider Threat

**Indicators:**
- Unusual data access patterns
- Mass downloads/exports
- After-hours access to sensitive systems
- Policy bypass attempts

**Response Steps:**
```bash
# Execute insider threat playbook (requires approval)
python incident_responder.py --incident INC-001 --playbook insider_threat
```

1. **Preserve:** Collect evidence BEFORE alerting subject
2. **Coordinate:** Involve HR and Legal early
3. **Monitor:** Enhanced logging on subject's activity
4. **Document:** All observations with timestamps
5. **Act:** Disable access (coordinate with HR)

**Critical Rules:**
- DO NOT alert subject prematurely
- DO coordinate with HR/Legal before visible actions
- DO preserve chain of custody for evidence

## Communication Protocols

### Internal Communication

**War Room Setup:**
- Platform: Dedicated Slack/Teams channel or Zoom bridge
- Participants: Security team, affected system owners, management
- Update frequency: Every 30-60 minutes during active incident

**Status Update Template:**
```
INCIDENT UPDATE - [INC-ID] - [TIMESTAMP]
Status: [ACTIVE/CONTAINED/RESOLVED]
Severity: [P0/P1/P2/P3]
Summary: [Brief description]
Impact: [Systems/users affected]
Actions Taken: [List recent actions]
Next Steps: [Planned actions]
ETA to Resolution: [If known]
```

### External Communication

**Customer Notification Triggers:**
- P0 incidents affecting customer data
- Data breaches with PII/PCI/PHI exposure
- Extended service outages (>4 hours)

**Regulatory Reporting:**
- GDPR: 72 hours to supervisory authority
- PCI: Immediate to payment brands
- HIPAA: 60 days to HHS
- State laws: Varies by jurisdiction

## Tools & Resources

### Detection Tools
- **SIEM:** Splunk, Elastic Security, Datadog
- **EDR:** CrowdStrike, Carbon Black, Microsoft Defender
- **IDS/IPS:** Suricata, Snort, Zeek

### Incident Management
- **Ticketing:** Jira Service Management, ServiceNow
- **Alerting:** PagerDuty, Opsgenie
- **Communication:** Slack, Microsoft Teams

### Forensics
- **Memory:** Volatility, LiME
- **Disk:** Autopsy, FTK Imager
- **Network:** Wireshark, tcpdump

### Threat Intelligence
- **IOC Databases:** MISP, AlienVault OTX, VirusTotal
- **TTPs:** MITRE ATT&CK Framework
- **Ransomware ID:** ID Ransomware, No More Ransom

## Integration with Python Tools

### Automated Detection Pipeline
```bash
#!/bin/bash
# Daily security log analysis
python incident_detector.py \
  --input /var/log/ \
  --ioc-file /etc/security/known-bad-iocs.txt \
  --output json \
  --file /var/reports/daily-triage.json

# Alert on P0/P1 findings
if grep -q '"severity": "P0"\|"severity": "P1"' /var/reports/daily-triage.json; then
  # Send alert
  echo "Critical findings detected" | mail -s "Security Alert" soc@company.com
fi
```

### Incident Response Automation
```bash
#!/bin/bash
# Automated containment for confirmed ransomware
python incident_responder.py \
  --incident "$INCIDENT_ID" \
  --playbook ransomware \
  --output-dir "/evidence/$INCIDENT_ID" \
  --output json
```

### Post-Incident Reporting
```bash
#!/bin/bash
# Generate comprehensive incident report
python incident_analyzer.py \
  --incident "$INCIDENT_ID" \
  --evidence-dir "/evidence/$INCIDENT_ID" \
  --report \
  --output markdown \
  --file "/reports/$INCIDENT_ID-final-report.md"
```

---
**Last Updated:** December 16, 2025
**Related:** forensics-evidence-guide.md, communication-templates.md
**Python Tools:** incident_detector.py, incident_responder.py, incident_analyzer.py
