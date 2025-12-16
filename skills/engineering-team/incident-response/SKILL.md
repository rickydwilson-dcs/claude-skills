---

# === CORE IDENTITY ===
name: incident-response
title: Incident Response Skill Package
description: Comprehensive incident response skill for security incident detection, containment, investigation, and recovery. Includes alert triage, severity classification, evidence collection, root cause analysis, and post-incident documentation with automated playbook execution.
domain: engineering
subdomain: security-operations

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "4-8 hours per incident"
frequency: "As needed (during security incidents)"
use-cases:
  - Detecting and triaging security alerts with severity classification
  - Executing incident containment playbooks for rapid response
  - Conducting forensic investigations with evidence collection
  - Generating post-incident reports with root cause analysis

# === RELATIONSHIPS ===
related-agents: [cs-incident-responder]
related-skills: [senior-secops, senior-security]
related-commands: [/audit.security]
orchestrated-by: [cs-incident-responder]

# === TECHNICAL ===
dependencies:
  scripts: [incident_detector.py, incident_responder.py, incident_analyzer.py, servicenow_incident_manager.py, servicenow_status_sync.py]
  references: [incident-response-playbooks.md, forensics-evidence-guide.md, communication-templates.md, servicenow-patterns.md]
  assets: [incident-runbook-template.md, incident-report-template.md, communication-plan-template.md, servicenow-incident-template.json, servicenow-severity-mapping.yaml, servicenow-config.yaml]
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack: [Python 3.8+, Markdown]

# === EXAMPLES ===
examples:
  - title: Alert Detection and Triage
    input: "python incident_detector.py --input /var/log/auth.log --severity P1"
    output: "Triage report with severity classification, IOC matches, and recommended actions"
  - title: Incident Containment
    input: "python incident_responder.py --incident INC-001 --playbook ransomware"
    output: "Containment actions executed with timeline and evidence collected"
  - title: Post-Incident Analysis
    input: "python incident_analyzer.py --incident INC-001 --report --output report.md"
    output: "Full incident report with RCA, impact assessment, and remediation plan"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-12-16
updated: 2025-12-16
license: MIT

# === DISCOVERABILITY ===
tags:
  - incident-response
  - security
  - forensics
  - containment
  - investigation
  - MTTD
  - MTTR
  - playbook
  - SOC
  - engineering
  - servicenow
  - itsm
featured: false
verified: true
---


# Incident Response

Complete toolkit for security incident detection, containment, investigation, and recovery with automated playbook execution and post-incident analysis.

## Overview

The Incident Response skill provides enterprise-grade incident response capabilities, enabling rapid detection, containment, and recovery from security incidents. This skill covers alert triage, severity classification, evidence collection, forensic investigation, root cause analysis, and post-incident documentation used by leading security operations centers.

Designed for incident responders, SOC analysts, and security engineers, this skill includes proven patterns for handling phishing attacks, ransomware, data breaches, and cloud account compromises. All content focuses on time-critical incident response with minimal mean time to detect (MTTD) and mean time to respond (MTTR).

**Core Value:** Reduce incident response time by 60%+ through automated detection, structured playbooks, and consistent post-incident analysis while maintaining evidence integrity and regulatory compliance.

## Quick Start

### Main Capabilities

This skill provides five core capabilities through automated scripts:

```bash
# Script 1: Incident Detector - Alert triage and severity classification
python scripts/incident_detector.py --input /path/to/logs --output json

# Script 2: Incident Responder - Containment and evidence collection
python scripts/incident_responder.py --incident INC-001 --playbook ransomware

# Script 3: Incident Analyzer - Root cause analysis and reporting
python scripts/incident_analyzer.py --incident INC-001 --report

# Script 4: ServiceNow Incident Manager - Create ITSM incidents from alerts
python scripts/servicenow_incident_manager.py --alert-file alert.json --output curl

# Script 5: ServiceNow Status Sync - Bi-directional status synchronization
python scripts/servicenow_status_sync.py --action resolve --snow-number INC0012345
```

## Core Capabilities

### 1. Incident Detector

Automated alert triage, severity classification, and indicator of compromise (IOC) correlation.

**Features:**
- Severity classification (P0-P3) based on incident type and scope
- Pattern detection (brute force, data exfiltration, lateral movement)
- IOC correlation with known threat indicators
- Alert aggregation and deduplication
- Real-time log parsing and analysis

**Usage:**
```bash
python scripts/incident_detector.py --input /var/log/auth.log --severity P1 --output json
```

### 2. Incident Responder

Containment action execution, timeline tracking, and evidence collection with playbook support.

**Features:**
- Pre-built playbooks (phishing, ransomware, data breach, cloud compromise)
- Automated containment actions with rollback capability
- Evidence collection with chain of custody tracking
- Timeline generation with all incident events
- Integration with ticketing systems (Jira, ServiceNow)

**Usage:**
```bash
python scripts/incident_responder.py --incident INC-001 --action contain --collect-evidence
```

### 3. Incident Analyzer

Root cause analysis, impact assessment, and remediation recommendations with report generation.

**Features:**
- Attack vector and entry point identification
- Dwell time calculation and lateral movement mapping
- Business impact quantification (systems, users, data, cost)
- MTTD/MTTR metrics calculation
- Markdown and HTML report generation
- Lessons learned documentation

**Usage:**
```bash
python scripts/incident_analyzer.py --incident INC-001 --rca --impact --report
```

## Key Workflows

### 1. Alert Detection and Triage

**Time:** 15-30 minutes

1. **Ingest Security Alerts** - Collect alerts from SIEM, EDR, IDS/IPS, and user reports
2. **Run Incident Detector** - Execute incident_detector.py for automated classification
3. **Classify Severity** - Assign P0-P3 severity based on scope and impact
4. **Correlate IOCs** - Match indicators against known threat databases
5. **Generate Triage Report** - Create prioritized alert list with recommended actions

**Expected Output:** Prioritized incident list with severity levels and response recommendations

**Example:**
```bash
# Detect potential incidents from authentication logs
python scripts/incident_detector.py \
  --input /var/log/auth.log \
  --ioc-file known-bad-ips.txt \
  --output json \
  --file triage-report.json

# Output: Triage report with P0 data breach detected, 3 affected systems
```

### 2. Incident Containment and Response

**Time:** 30 minutes - 4 hours (depending on severity)

1. **Activate Incident Response** - Initiate formal IR process and war room
2. **Execute Containment Playbook** - Run incident_responder.py with appropriate playbook
3. **Isolate Affected Systems** - Quarantine compromised hosts and accounts
4. **Preserve Evidence** - Collect logs, memory dumps, and system state
5. **Track Timeline** - Document all actions with timestamps

**Expected Output:** Contained incident with evidence preserved and timeline documented

**Example:**
```bash
# Execute ransomware containment playbook
python scripts/incident_responder.py \
  --incident INC-2025-12-16-001 \
  --playbook ransomware \
  --collect-evidence \
  --output-dir ./evidence/INC-001

# Output: 5 containment actions executed, 12 evidence items collected
```

### 3. Forensic Investigation and Analysis

**Time:** 4-24 hours

1. **Analyze Evidence** - Review collected logs, memory dumps, and disk images
2. **Perform Root Cause Analysis** - Identify attack vector and entry point
3. **Map Attack Path** - Document lateral movement and data access
4. **Assess Impact** - Quantify affected systems, users, and data
5. **Develop Remediation Plan** - Create immediate and long-term fixes

**Expected Output:** Root cause analysis with attack timeline and impact assessment

**Example:**
```bash
# Full incident analysis with RCA
python scripts/incident_analyzer.py \
  --incident INC-2025-12-16-001 \
  --evidence-dir ./evidence/INC-001 \
  --rca \
  --impact \
  --output json

# Output: Attack vector: phishing, dwell time: 26 hours, 150 users affected
```

### 4. Post-Incident Review and Documentation

**Time:** 1-2 days after incident closure

1. **Generate Incident Report** - Create executive summary and technical details
2. **Calculate Metrics** - Compute MTTD, MTTR, and containment effectiveness
3. **Document Lessons Learned** - Identify what worked and what needs improvement
4. **Define Action Items** - Create remediation tasks with owners and deadlines
5. **Update Playbooks** - Improve runbooks based on incident learnings

**Expected Output:** Complete incident report with lessons learned and improvement actions

**Example:**
```bash
# Generate post-incident report
python scripts/incident_analyzer.py \
  --incident INC-2025-12-16-001 \
  --report \
  --output incident-report.md

# Output: 15-page incident report with RCA, impact, and remediation plan
```

## Python Tools

### incident_detector.py

Automated alert triage and severity classification with IOC correlation and pattern detection.

**Key Features:**
- Severity classification (P0-Critical, P1-High, P2-Medium, P3-Low)
- Detection patterns: brute force, credential stuffing, data exfiltration, lateral movement, privilege escalation
- IOC correlation: IP addresses, domains, file hashes, email addresses
- Log format support: JSON, syslog, auth.log, Apache/Nginx access logs
- Alert aggregation and deduplication
- Confidence scoring for each detection

**CLI Arguments:**
- `--input` - Path to log file or directory (required)
- `--ioc-file` - Path to IOC file for correlation (optional)
- `--severity` - Filter by minimum severity level: P0, P1, P2, P3 (optional)
- `--output` - Output format: text, json, csv (default: text)
- `--file` - Output file path (optional, defaults to stdout)
- `--help` - Show usage information
- `--version` - Show version

**Common Usage:**
```bash
# Basic detection from auth logs
python scripts/incident_detector.py --input /var/log/auth.log

# Detection with IOC correlation
python scripts/incident_detector.py --input logs/ --ioc-file iocs.txt --output json

# Filter for high-severity incidents only
python scripts/incident_detector.py --input alerts.json --severity P1 --file critical.json

# Help
python scripts/incident_detector.py --help
```

**Use Cases:**
- Real-time security alert monitoring
- Daily security log review
- Threat hunting exercises
- Post-breach indicator searches

### incident_responder.py

Incident containment, timeline tracking, and evidence collection with playbook execution.

**Key Features:**
- Pre-built playbooks: phishing, ransomware, data_breach, cloud_compromise, insider_threat
- Containment actions: account disable, network isolation, credential rotation, service shutdown
- Evidence collection: logs, memory state, system config, network captures
- Chain of custody tracking with SHA-256 hashing
- Timeline generation with all incident events
- Action logging with timestamps and outcomes

**CLI Arguments:**
- `--incident` - Incident identifier (required)
- `--playbook` - Playbook to execute: phishing, ransomware, data_breach, cloud_compromise, insider_threat (optional)
- `--action` - Specific action: contain, isolate, disable, preserve (optional)
- `--collect-evidence` - Enable evidence collection (flag)
- `--output-dir` - Directory for evidence storage (default: ./evidence)
- `--timeline` - Generate incident timeline (flag)
- `--output` - Output format: text, json (default: text)
- `--help` - Show usage information
- `--version` - Show version

**Common Usage:**
```bash
# Execute ransomware containment playbook
python scripts/incident_responder.py --incident INC-001 --playbook ransomware

# Collect evidence for investigation
python scripts/incident_responder.py --incident INC-001 --collect-evidence --output-dir ./evidence

# Generate incident timeline
python scripts/incident_responder.py --incident INC-001 --timeline --output json

# Specific containment action
python scripts/incident_responder.py --incident INC-001 --action isolate

# Help
python scripts/incident_responder.py --help
```

**Use Cases:**
- Active incident containment
- Evidence preservation for forensics
- Incident timeline documentation
- Playbook-driven response automation

### incident_analyzer.py

Root cause analysis, impact assessment, and post-incident report generation.

**Key Features:**
- Attack vector identification: phishing, vulnerability exploitation, misconfiguration, insider
- Dwell time calculation (time from compromise to detection)
- Lateral movement path reconstruction
- Impact quantification: systems, users, data records, estimated cost
- MTTD/MTTR metrics calculation
- Remediation plan generation (immediate, short-term, long-term)
- Markdown and HTML report output
- Lessons learned documentation

**CLI Arguments:**
- `--incident` - Incident identifier (required)
- `--evidence-dir` - Path to collected evidence (optional)
- `--rca` - Perform root cause analysis (flag)
- `--impact` - Perform impact assessment (flag)
- `--report` - Generate full incident report (flag)
- `--output` - Output format: text, json, markdown (default: text)
- `--file` - Output file path (optional, defaults to stdout)
- `--help` - Show usage information
- `--version` - Show version

**Common Usage:**
```bash
# Root cause analysis only
python scripts/incident_analyzer.py --incident INC-001 --rca

# Impact assessment only
python scripts/incident_analyzer.py --incident INC-001 --impact

# Full incident report
python scripts/incident_analyzer.py --incident INC-001 --report --output markdown --file report.md

# JSON output for automation
python scripts/incident_analyzer.py --incident INC-001 --rca --impact --output json

# Help
python scripts/incident_analyzer.py --help
```

**Use Cases:**
- Post-incident forensic analysis
- Executive reporting on security incidents
- Compliance documentation (breach notifications)
- Security program improvement planning

### servicenow_incident_manager.py

Generate ServiceNow incident payloads from observability alerts for enterprise ITSM integration.

**Key Features:**
- Alert format auto-detection (Prometheus, NewRelic, DataDog, PagerDuty)
- Severity-to-priority mapping (P0-P3 → ServiceNow impact/urgency/priority)
- CMDB Configuration Item linking
- Assignment group routing
- curl command generation for API testing

**CLI Arguments:**
- `--alert-file` - Path to alert JSON file (required)
- `--severity` - Override alert severity: P0, P1, P2, P3 (optional)
- `--assignment-group` - Target assignment group (optional)
- `--ci-name` - CMDB Configuration Item name (optional)
- `--output` - Output format: json, text, curl (default: json)
- `--file` - Output file path (optional, defaults to stdout)
- `--help` - Show usage information
- `--version` - Show version

**Common Usage:**
```bash
# Generate incident payload from alert
python scripts/servicenow_incident_manager.py --alert-file alert.json --output json

# Generate curl command for testing
python scripts/servicenow_incident_manager.py --alert-file alert.json \
  --assignment-group "Platform Engineering" \
  --ci-name "pandora-api-prod" \
  --output curl

# Specify severity override
python scripts/servicenow_incident_manager.py --alert-file alert.json --severity P1 --output curl

# Help
python scripts/servicenow_incident_manager.py --help
```

**Use Cases:**
- Escalating observability alerts to ServiceNow incidents
- ITSM integration for audit compliance
- Automated incident ticket creation from monitoring
- Linking incidents to CMDB Configuration Items

### servicenow_status_sync.py

Bi-directional status synchronization between monitoring alerts and ServiceNow incidents.

**Key Features:**
- State mapping (alert state → ServiceNow incident state)
- Work notes generation and updates
- Resolution code handling (fixed, workaround, duplicate, etc.)
- curl command generation for API testing
- Audit trail maintenance

**CLI Arguments:**
- `--action` - Action to perform: acknowledge, update, hold, resolve, close, reopen (required)
- `--snow-number` - ServiceNow incident number (required)
- `--status` - New status value (optional)
- `--notes` - Work notes content (optional)
- `--resolution-code` - Resolution code: fixed, workaround, duplicate, not_reproducible (optional)
- `--output` - Output format: json, text, curl (default: json)
- `--file` - Output file path (optional, defaults to stdout)
- `--help` - Show usage information
- `--version` - Show version

**Common Usage:**
```bash
# Acknowledge incident
python scripts/servicenow_status_sync.py --action acknowledge \
  --snow-number INC0012345 \
  --notes "Investigation started"

# Add work notes during response
python scripts/servicenow_status_sync.py --action update \
  --snow-number INC0012345 \
  --notes "Containment actions executed"

# Resolve incident
python scripts/servicenow_status_sync.py --action resolve \
  --snow-number INC0012345 \
  --resolution-code fixed \
  --notes "Root cause fixed, patch deployed"

# Generate curl command
python scripts/servicenow_status_sync.py --action resolve \
  --snow-number INC0012345 \
  --output curl

# Help
python scripts/servicenow_status_sync.py --help
```

**Use Cases:**
- Synchronizing alert state with ServiceNow incidents
- Maintaining audit trail of incident response actions
- Resolving and closing ITSM tickets from response workflows
- Status updates during incident lifecycle

## Reference Documentation

### Incident Response Playbooks

Comprehensive playbook guide in `references/incident-response-playbooks.md`:

- Severity classification (P0-P3) with response times
- Six-phase incident response framework
- Playbooks: phishing, ransomware, data breach, cloud compromise
- Communication protocols (internal, external, regulatory)
- Tool recommendations and integration patterns

### Forensics and Evidence Guide

Evidence collection best practices in `references/forensics-evidence-guide.md`:

- Order of volatility for evidence collection
- Chain of custody requirements
- Hash verification procedures
- Legal and compliance considerations
- Evidence storage and retention

### Communication Templates

Stakeholder communication templates in `references/communication-templates.md`:

- War room setup and status updates
- Executive briefing format
- Customer notification templates
- Regulatory notification (GDPR, HIPAA, PCI)
- Post-incident communication

### ServiceNow Integration Patterns

ServiceNow ITSM integration guide in `references/servicenow-patterns.md`:

- REST API patterns for incident management
- Severity-to-priority mapping (P0-P3 → impact/urgency/priority)
- CMDB Configuration Item linking
- Event Management integration
- Bi-directional status synchronization
- Alert-to-incident mapping (Prometheus, NewRelic, DataDog)
- Authentication methods (Basic, OAuth, Token)
- Error handling and retries

## Success Metrics

Track incident response effectiveness with these metrics:

**Detection Metrics:**
- Mean Time to Detect (MTTD): Target < 1 hour for P0/P1
- Alert accuracy: Target > 95% true positive rate
- IOC coverage: Percentage of known threats detected

**Response Metrics:**
- Mean Time to Respond (MTTR): Target < 4 hours for P0, < 24 hours for P1
- Containment rate: Target 98%+ incidents contained before spread
- Evidence completeness: All required evidence collected

**Quality Metrics:**
- False positive rate: Target < 5%
- Recurring incidents: Target < 2% (same root cause)
- Playbook coverage: Incidents with applicable playbooks

**Improvement Metrics:**
- Lessons learned implementation rate
- Control effectiveness improvement
- Training completion rate post-incident

## Tech Stack

**Languages:** Python 3.8+, Bash, PowerShell
**Log Formats:** JSON, syslog, CEF, CLF, auth.log
**Integration:** ServiceNow (Incident, Change, CMDB), Jira, PagerDuty, Slack
**Alert Sources:** Prometheus, NewRelic, DataDog, PagerDuty, CloudWatch
**Evidence:** SHA-256 hashing, tar/gzip compression
**Reporting:** Markdown, HTML, JSON

## Best Practices Summary

### Detection
- Aggregate alerts from multiple sources
- Correlate with threat intelligence
- Maintain low false positive rates
- Tune detection rules regularly

### Containment
- Follow pre-defined playbooks
- Document all actions taken
- Preserve evidence before remediation
- Communicate with stakeholders

### Investigation
- Establish clear timeline
- Identify all affected systems
- Determine data exposure scope
- Document chain of custody

### Recovery
- Validate system integrity
- Monitor for re-compromise
- Update detection rules
- Conduct lessons learned review

## Troubleshooting

### Common Issues

**Detection tool not finding alerts:**
- Verify log file path and permissions
- Check log format compatibility
- Ensure IOC file is properly formatted
- Review detection pattern configuration

**Evidence collection failing:**
- Verify write permissions to output directory
- Check available disk space
- Ensure source files are accessible
- Review hash verification errors

**Report generation incomplete:**
- Verify all required inputs are provided
- Check evidence directory structure
- Ensure incident data is available
- Review error messages for missing data

### Getting Help

- Review reference documentation in `references/`
- Check script output with `--verbose` flag
- Consult incident response playbooks
- Review error logs and stack traces

## Resources

- Playbook Reference: `references/incident-response-playbooks.md`
- Evidence Guide: `references/forensics-evidence-guide.md`
- Communication Templates: `references/communication-templates.md`
- ServiceNow Patterns: `references/servicenow-patterns.md`
- ServiceNow Config: `assets/servicenow-config.yaml`
- ServiceNow Templates: `assets/servicenow-incident-template.json`, `assets/servicenow-severity-mapping.yaml`
- Tool Scripts: `scripts/` directory
- Asset Templates: `assets/` directory
