# Incident Response Runbook Template

## Runbook Information

| Field | Value |
|-------|-------|
| **Runbook Name** | [Incident Type] Response Runbook |
| **Version** | 1.0 |
| **Last Updated** | YYYY-MM-DD |
| **Owner** | Security Operations Team |
| **Review Frequency** | Quarterly |

---

## Quick Reference

| Item | Details |
|------|---------|
| **Severity Classification** | P0: Immediate / P1: <30min / P2: <4hr / P3: <24hr |
| **Response Time SLA** | [Target time based on severity] |
| **On-Call Contact** | [PagerDuty/Opsgenie alias or phone] |
| **War Room Channel** | #incident-response |
| **Escalation Path** | SOC → Security Lead → CISO |

---

## 1. Detection

### Alert Sources
- [ ] SIEM (Splunk/Elastic/Datadog)
- [ ] EDR (CrowdStrike/Carbon Black)
- [ ] Cloud Security (GuardDuty/Defender)
- [ ] User Report
- [ ] Other: ____________

### Initial Triage Questions
1. What triggered the alert?
2. Which systems are affected?
3. Is this confirmed malicious?
4. What is the potential impact?
5. Is the threat active?

### Automated Detection
```bash
# Run automated triage
python incident_detector.py \
  --input /var/log/ \
  --output json \
  --file triage-report.json
```

### Severity Classification Criteria

| Severity | Criteria |
|----------|----------|
| **P0** | [ ] Active data breach [ ] Ransomware spreading [ ] Critical system down |
| **P1** | [ ] Potential breach [ ] Malware on critical systems [ ] Privileged access compromise |
| **P2** | [ ] Contained threat [ ] Policy violation [ ] Non-critical system impact |
| **P3** | [ ] Blocked attempt [ ] Informational alert [ ] Minor policy violation |

**Assigned Severity:** [ ] P0 [ ] P1 [ ] P2 [ ] P3

---

## 2. Containment

### Immediate Actions (First 15 Minutes)

#### For Compromised Accounts
- [ ] Disable affected user account
- [ ] Revoke all active sessions
- [ ] Check for newly created accounts
- [ ] Block source IP (if external)

**Commands:**
```bash
# Execute account containment
python incident_responder.py \
  --incident [INC-ID] \
  --action disable_account \
  --target [username]
```

#### For Compromised Systems
- [ ] Isolate from network (disconnect/VLAN)
- [ ] DO NOT shut down (preserve memory)
- [ ] Block malicious IPs at firewall
- [ ] Take forensic snapshot

**Commands:**
```bash
# Execute system isolation
python incident_responder.py \
  --incident [INC-ID] \
  --action isolate_system \
  --target [hostname]
```

#### For Data Breach
- [ ] Close access vector immediately
- [ ] Identify data exposure scope
- [ ] Preserve access logs
- [ ] Notify Legal team

### Playbook Execution

```bash
# Execute full containment playbook
python incident_responder.py \
  --incident [INC-ID] \
  --playbook [phishing|ransomware|data_breach|cloud_compromise] \
  --output json
```

### Containment Verification
- [ ] Threat activity stopped
- [ ] No lateral movement observed
- [ ] Evidence preserved
- [ ] Timeline documented

---

## 3. Evidence Preservation

### Evidence Collection Checklist

| Evidence Type | Location | Collected | Hash |
|---------------|----------|-----------|------|
| Memory dump | /evidence/memory/ | [ ] | |
| System logs | /var/log/ | [ ] | |
| Auth logs | /var/log/auth.log | [ ] | |
| Network capture | /evidence/pcap/ | [ ] | |
| Application logs | [path] | [ ] | |

### Collection Commands

```bash
# Automated evidence collection
python incident_responder.py \
  --incident [INC-ID] \
  --collect-evidence \
  --paths /var/log/auth.log /var/log/syslog /var/log/audit/ \
  --output-dir /evidence/[INC-ID]
```

### Chain of Custody

| Timestamp | Collector | Action | Evidence ID |
|-----------|-----------|--------|-------------|
| | | | |
| | | | |

---

## 4. Investigation

### Investigation Questions
1. **Timeline:** When did compromise begin?
2. **Entry Point:** How did attacker gain access?
3. **Lateral Movement:** Where did they go?
4. **Data Access:** What was accessed/exfiltrated?
5. **Persistence:** Are there backdoors?

### Analysis Commands

```bash
# Root cause analysis
python incident_analyzer.py \
  --incident [INC-ID] \
  --evidence-dir /evidence/[INC-ID] \
  --rca \
  --attack-vector [phishing|vulnerability|credential_theft]

# Impact assessment
python incident_analyzer.py \
  --incident [INC-ID] \
  --impact
```

### IOC Documentation

| IOC Type | Value | Context |
|----------|-------|---------|
| IP Address | | |
| Domain | | |
| File Hash | | |
| Email | | |

---

## 5. Eradication

### Eradication Checklist
- [ ] Remove malware from all systems
- [ ] Remove backdoors/persistence
- [ ] Patch exploited vulnerability
- [ ] Reset compromised credentials
- [ ] Update security rules

### Verification Steps
- [ ] IOC scan clean on all systems
- [ ] No malware signatures detected
- [ ] Vulnerability patched and verified
- [ ] No re-compromise attempts in logs

---

## 6. Recovery

### Recovery Steps
- [ ] Restore from clean backup (if needed)
- [ ] Re-enable accounts with new credentials
- [ ] Restore network connectivity
- [ ] Enable enhanced monitoring
- [ ] Validate business operations

### Monitoring Period
- [ ] Enhanced logging enabled for 30 days
- [ ] Daily alert review scheduled
- [ ] Threat hunting for similar TTPs
- [ ] User behavior analytics active

---

## 7. Post-Incident

### Documentation
- [ ] Full incident report generated
- [ ] Timeline documented
- [ ] Evidence manifest completed
- [ ] Lessons learned documented

### Report Generation

```bash
# Generate full incident report
python incident_analyzer.py \
  --incident [INC-ID] \
  --evidence-dir /evidence/[INC-ID] \
  --report \
  --output markdown \
  --file /reports/[INC-ID]-report.md
```

### Follow-Up Actions

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| | | | [ ] Open |
| | | | [ ] Open |
| | | | [ ] Open |

### Lessons Learned Meeting
- **Date:**
- **Attendees:**
- **Key Findings:**

---

## Appendix: Contact Information

| Role | Name | Contact |
|------|------|---------|
| Security Lead | | |
| On-Call Engineer | | |
| CISO | | |
| Legal Counsel | | |
| PR/Communications | | |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | | Initial version |
