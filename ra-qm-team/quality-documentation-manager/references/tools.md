# Python Tools Documentation

Complete documentation for all Python automation tools including usage examples, integration patterns, and troubleshooting guidance for document management automation.

## Table of Contents
1. [Document Control Dashboard](#document-control-dashboard)
2. [Change Control Automation](#change-control-automation)
3. [Regulatory Documentation Validator](#regulatory-documentation-validator)
4. [DMS Performance Monitor](#dms-performance-monitor)
5. [Integration Patterns](#integration-patterns)
6. [Troubleshooting Guide](#troubleshooting-guide)

---

## Document Control Dashboard

### Overview

**Script:** `scripts/document-control-dashboard.py`

Comprehensive document management performance monitoring tool for tracking document control metrics, compliance status, and operational efficiency.

**Purpose:**
- Monitor document control key performance indicators
- Track document approval cycle times
- Identify overdue reviews and expired documents
- Generate compliance reports for management review
- Support continuous improvement initiatives

### Features

**Core Capabilities:**
- Real-time document status monitoring
- Approval cycle time analysis
- Overdue document identification
- Compliance scoring and trending
- Department and document type breakdowns
- Customizable reporting periods
- Multi-format output (text, JSON, CSV, HTML)

**Metrics Tracked:**
- Total controlled documents
- Documents pending approval
- Documents overdue for review
- Average approval cycle time
- Documents with missing metadata
- Obsolete documents not archived
- Training completion rates (by document)

### Usage

**Basic Usage:**
```bash
# Generate monthly dashboard
python scripts/document-control-dashboard.py --period monthly

# Generate quarterly executive summary
python scripts/document-control-dashboard.py --period quarterly --format summary

# Export to JSON for integration
python scripts/document-control-dashboard.py --period monthly --output json --file metrics.json
```

**Command-Line Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--period` | Reporting period (weekly, monthly, quarterly, annual) | monthly |
| `--metrics` | Specific metrics to display (approval-times, overdue, compliance) | all |
| `--output` | Output format (text, json, csv, html) | text |
| `--file` | Output file path | stdout |
| `--department` | Filter by department | all |
| `--document-type` | Filter by document type (SOP, WI, FORM, etc.) | all |
| `--verbose` | Include detailed breakdowns | false |

**Advanced Examples:**
```bash
# Track approval times for SOPs only
python scripts/document-control-dashboard.py --metrics approval-times --document-type SOP

# Generate HTML report for management review
python scripts/document-control-dashboard.py --period quarterly --output html --file mgmt-review.html

# Monitor overdue documents by department
python scripts/document-control-dashboard.py --metrics overdue --department QA --verbose

# Export compliance data for trending
python scripts/document-control-dashboard.py --metrics compliance --output csv --file compliance-trend.csv
```

### Output Examples

**Text Output (Default):**
```
DOCUMENT CONTROL DASHBOARD - November 2025
Generated: 2025-11-08 10:30:00

SUMMARY METRICS:
Total Controlled Documents: 342
Documents Pending Approval: 8
Documents Overdue for Review: 12
Average Approval Cycle Time: 5.2 days

APPROVAL CYCLE TIME ANALYSIS:
Department       | Avg Days | Min | Max | Count
Quality          | 4.8      | 2   | 12  | 45
Engineering      | 6.1      | 3   | 15  | 32
Manufacturing    | 4.2      | 2   | 9   | 28
Regulatory       | 5.9      | 3   | 14  | 18

OVERDUE REVIEW ANALYSIS:
Document ID      | Title                    | Days Overdue | Dept
SOP-QA-0012      | Document Control SOP     | 15           | QA
WI-MFG-0089      | Assembly Instruction     | 8            | MFG
SOP-RA-0003      | Submission Planning      | 22           | RA

COMPLIANCE SCORE: 96.5%
- Documents with current approval: 98.2%
- Documents reviewed on time: 96.5%
- Obsolete documents archived: 100%
- Metadata completeness: 94.8%
```

**JSON Output:**
```json
{
  "report_date": "2025-11-08",
  "period": "monthly",
  "summary": {
    "total_documents": 342,
    "pending_approval": 8,
    "overdue_review": 12,
    "avg_approval_days": 5.2
  },
  "approval_cycle_times": [
    {
      "department": "Quality",
      "avg_days": 4.8,
      "min_days": 2,
      "max_days": 12,
      "count": 45
    }
  ],
  "overdue_documents": [
    {
      "document_id": "SOP-QA-0012",
      "title": "Document Control SOP",
      "days_overdue": 15,
      "department": "QA",
      "owner": "Jane Smith"
    }
  ],
  "compliance_score": 96.5,
  "compliance_breakdown": {
    "current_approval": 98.2,
    "timely_review": 96.5,
    "obsolete_archived": 100.0,
    "metadata_complete": 94.8
  }
}
```

### Integration Patterns

**PowerBI/Tableau Integration:**
```bash
# Export monthly data for visualization
python scripts/document-control-dashboard.py --period monthly --output json --file dashboard-$(date +%Y%m).json
```

**Management Review Automation:**
```bash
# Generate quarterly report for management review
python scripts/document-control-dashboard.py --period quarterly --output html --file mgmt-review-$(date +%Y-Q%q).html
```

**Alerting and Notifications:**
```bash
# Check for overdue documents and send alert if found
OVERDUE=$(python scripts/document-control-dashboard.py --metrics overdue --output json | jq '.summary.overdue_review')
if [ "$OVERDUE" -gt 10 ]; then
  python scripts/send-alert.py --message "High number of overdue documents: $OVERDUE"
fi
```

---

## Change Control Automation

### Overview

**Script:** `scripts/change-control-automation.py`

Document change workflow automation and tracking system for managing change requests, impact assessments, and implementation verification.

**Purpose:**
- Automate change request workflows
- Track change status and timeline
- Facilitate impact assessments
- Generate change control reports
- Support regulatory compliance

### Features

**Change Request Management:**
- Create new change requests
- Update change status
- Assign reviewers and approvers
- Track completion dates
- Link related documents and changes

**Impact Assessment Support:**
- Impact assessment templates
- Risk scoring
- Regulatory impact flags
- Resource estimation
- Timeline calculation

**Reporting:**
- Change request status reports
- Open changes by priority
- Change cycle time analysis
- Change trends and patterns
- Effectiveness tracking

### Usage

**Change Request Operations:**
```bash
# Create new change request
python scripts/change-control-automation.py create \
  --document SOP-QA-0012 \
  --reason "Add regulatory review step" \
  --requestor "Jane Smith" \
  --priority high

# Update change status
python scripts/change-control-automation.py update CR-2025-045 \
  --status under-review \
  --notes "Impact assessment in progress"

# Complete change request
python scripts/change-control-automation.py complete CR-2025-045 \
  --implementation-date 2025-11-15 \
  --verification-complete true

# Close change request
python scripts/change-control-automation.py close CR-2025-045 \
  --effectiveness-verified true \
  --notes "Change implemented successfully"
```

**Reporting Operations:**
```bash
# Generate change status report
python scripts/change-control-automation.py report \
  --status open \
  --output json

# Analyze change cycle times
python scripts/change-control-automation.py analyze \
  --period quarterly \
  --metric cycle-time

# Track overdue changes
python scripts/change-control-automation.py report \
  --status overdue \
  --format email \
  --recipients document-control@company.com
```

**Command-Line Options:**

| Command | Description | Required Args |
|---------|-------------|---------------|
| `create` | Create new change request | --document, --reason, --requestor |
| `update` | Update change request status | change_id, --status |
| `complete` | Mark change as completed | change_id, --implementation-date |
| `close` | Close change request | change_id |
| `report` | Generate change reports | --status or --period |
| `analyze` | Analyze change metrics | --period, --metric |
| `list` | List change requests | (optional filters) |

### Output Examples

**Change Request Creation:**
```
CHANGE REQUEST CREATED: CR-2025-045

Document: SOP-QA-0012 v2.1
Reason: Add regulatory review step
Requestor: Jane Smith
Priority: High
Status: Pending Review
Created: 2025-11-08

Next Steps:
1. Impact assessment required
2. Assign to Change Control Board
3. Target review date: 2025-11-15

Change Request URL: /change-requests/CR-2025-045
```

**Change Status Report:**
```
OPEN CHANGE REQUESTS - November 2025

Priority: HIGH (3 changes)
- CR-2025-045: SOP-QA-0012 (Pending Review) - 3 days open
- CR-2025-047: WI-MFG-0089 (Under Review) - 8 days open
- CR-2025-049: SOP-RA-0003 (Approved, Pending Implementation) - 12 days open

Priority: MEDIUM (5 changes)
- CR-2025-044: FORM-QA-0025 (Pending Review) - 5 days open
- CR-2025-046: SOP-ENG-0102 (Under Review) - 7 days open
...

OVERDUE CHANGES (2):
- CR-2025-038: SOP-MFG-0045 (Approved, Overdue for Implementation) - 5 days overdue
- CR-2025-041: WI-QC-0067 (Implementation Complete, Overdue for Verification) - 3 days overdue

CYCLE TIME ANALYSIS:
Average Time to Approval: 8.5 days
Average Time to Implementation: 14.2 days
Average Total Cycle Time: 22.7 days
```

### Integration Patterns

**Jira Integration:**
```bash
# Create Jira ticket when change request created
python scripts/change-control-automation.py create --document SOP-QA-0012 --reason "Update" --requestor "Jane" --jira-create true
```

**Email Notifications:**
```bash
# Send weekly digest of open change requests
python scripts/change-control-automation.py report --status open --format email --recipients team@company.com
```

**Workflow Automation:**
```bash
# Auto-route based on impact assessment
python scripts/change-control-automation.py auto-route CR-2025-045 --based-on impact-assessment
```

---

## Regulatory Documentation Validator

### Overview

**Script:** `scripts/regulatory-doc-validator.py`

Regulatory documentation compliance verification tool for validating technical documentation against EU MDR, FDA, and ISO requirements.

**Purpose:**
- Validate regulatory submission documents
- Verify completeness per regulatory requirements
- Check document structure and format
- Identify missing sections or information
- Generate validation reports for submission packages

### Features

**Validation Standards:**
- EU MDR Annex II and III compliance
- FDA 510(k) documentation requirements
- FDA PMA documentation requirements
- ISO 13485 documentation requirements
- ISO 14971 risk management file requirements

**Validation Checks:**
- Document completeness (all required sections present)
- Cross-reference verification
- Format and structure compliance
- Metadata completeness
- Version consistency
- Signature and approval verification

**Reporting:**
- Validation checklist completion
- Missing elements identification
- Non-compliance findings
- Remediation recommendations
- Audit-ready validation reports

### Usage

**Basic Validation:**
```bash
# Validate EU MDR technical documentation
python scripts/regulatory-doc-validator.py \
  --standard MDR \
  --annexes II,III \
  --document-path /path/to/tech-doc/ \
  --output validation-report.pdf

# Validate FDA 510(k) submission
python scripts/regulatory-doc-validator.py \
  --standard FDA \
  --type 510k \
  --document-path /path/to/submission/ \
  --checklist fda-510k-checklist.json

# Validate ISO 13485 QMS documentation
python scripts/regulatory-doc-validator.py \
  --standard ISO13485 \
  --document-path /path/to/qms/ \
  --output qms-validation.html
```

**Command-Line Options:**

| Option | Description | Values |
|--------|-------------|--------|
| `--standard` | Regulatory standard | MDR, FDA, ISO13485, ISO14971 |
| `--type` | Submission type (FDA only) | 510k, PMA, DeNovo |
| `--annexes` | MDR annexes to validate | II, III, XIV |
| `--document-path` | Path to documents | Directory path |
| `--checklist` | Custom checklist file | JSON file path |
| `--output` | Output report file | File path |
| `--format` | Output format | pdf, html, json, csv |
| `--verbose` | Detailed findings | true/false |

### Output Examples

**Validation Report:**
```
REGULATORY DOCUMENTATION VALIDATION REPORT
Standard: EU MDR 2017/745
Annexes: II, III
Validation Date: 2025-11-08

OVERALL COMPLIANCE: 92%

ANNEX II VALIDATION:
Section 1: Device Description - COMPLETE (100%)
  ✓ General description
  ✓ Intended purpose
  ✓ Risk classification
  ✓ Device variants
  ✓ Previous generations

Section 2: Information Supplied - COMPLETE (100%)
  ✓ Labels and IFU
  ✓ Patient implant card
  ✓ SSCP reference

Section 3: Design and Manufacturing - INCOMPLETE (85%)
  ✓ Design specifications
  ✓ Manufacturing sites
  ✗ Missing: Sterilization validation report
  ✓ Subcontractors identified
  ! WARNING: Supplier audit report outdated (>3 years)

Section 4: GSPR Compliance - COMPLETE (100%)
  ✓ GSPR checklist complete
  ✓ Solutions documented
  ✓ Standards applied
  ✓ Justifications provided

Section 5: Risk Management - INCOMPLETE (90%)
  ✓ Risk management file present
  ✓ Residual risks documented
  ✗ Missing: Risk-benefit analysis conclusion
  ✓ Risk management report

Section 6: Verification and Validation - COMPLETE (100%)
  ✓ Bench testing complete
  ✓ Clinical evaluation report
  ✓ PMCF plan

FINDINGS SUMMARY:
Critical: 0
Major: 2
  - Missing sterilization validation report (Section 3)
  - Missing risk-benefit analysis conclusion (Section 5)
Minor: 1
  - Supplier audit report outdated (Section 3)

RECOMMENDATIONS:
1. Complete sterilization validation per ISO 11137
2. Update risk-benefit analysis with formal conclusion
3. Conduct supplier re-audit or obtain recent audit report

NEXT STEPS:
Address all major findings before regulatory submission.
Minor findings should be addressed but do not block submission.
```

### Integration Patterns

**Submission Package Review:**
```bash
# Validate entire submission package
python scripts/regulatory-doc-validator.py --standard FDA --type 510k --document-path submission-package/ --output package-validation.html
```

**Pre-Submission Quality Gate:**
```bash
# Validate before submission review meeting
python scripts/regulatory-doc-validator.py --standard MDR --annexes II,III --document-path tech-doc/ --output validation.pdf
if [ $? -eq 0 ]; then
  echo "Validation passed - ready for submission"
else
  echo "Validation failed - address findings before proceeding"
fi
```

---

## DMS Performance Monitor

### Overview

**Script:** `scripts/dms-performance-monitor.py`

Document management system performance optimization tool for monitoring system health, user activity, and operational metrics.

**Purpose:**
- Monitor DMS system performance
- Track user activity and adoption
- Identify performance bottlenecks
- Generate system health reports
- Support capacity planning

### Features

**System Metrics:**
- System uptime and availability
- Response time monitoring
- Database performance
- Storage utilization
- Concurrent user load

**User Metrics:**
- Active users (daily, weekly, monthly)
- Document operations (create, edit, approve)
- Search activity and success rate
- Login patterns and peak usage times

**Performance Analysis:**
- Slow query identification
- Large document identification
- System bottlenecks
- Capacity projections
- Optimization recommendations

### Usage

**System Health Monitoring:**
```bash
# Generate system health report
python scripts/dms-performance-monitor.py --health-check

# Monitor specific metrics
python scripts/dms-performance-monitor.py --metrics uptime,response-time,storage

# Check for performance issues
python scripts/dms-performance-monitor.py --analyze-performance --period weekly
```

**User Activity Monitoring:**
```bash
# Generate user activity report
python scripts/dms-performance-monitor.py --activity-report --period monthly

# Track user adoption metrics
python scripts/dms-performance-monitor.py --adoption-metrics --output json
```

**Command-Line Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--health-check` | Run system health checks | - |
| `--metrics` | Specific metrics (comma-separated) | all |
| `--activity-report` | Generate user activity report | - |
| `--adoption-metrics` | Track adoption metrics | - |
| `--analyze-performance` | Analyze performance issues | - |
| `--period` | Reporting period | daily |
| `--output` | Output format (text, json, html) | text |
| `--file` | Output file path | stdout |

### Output Examples

**System Health Report:**
```
DMS PERFORMANCE MONITOR - System Health Check
Generated: 2025-11-08 14:30:00

SYSTEM STATUS: HEALTHY

Uptime: 99.7% (last 30 days)
  Last outage: 2025-10-22 (2 hours)
  Mean time between failures: 45 days

Response Time:
  Average: 0.85 seconds
  95th percentile: 1.4 seconds
  99th percentile: 2.1 seconds
  Target: < 2 seconds ✓

Concurrent Users:
  Current: 87
  Peak (last 24h): 152
  Peak (last 30d): 184
  Capacity: 250

Storage Utilization:
  Total capacity: 5 TB
  Used: 2.3 TB (46%)
  Growth rate: 120 GB/month
  Projected full: April 2027

Database Performance:
  Query response time: 125ms (avg)
  Slow queries: 3 (>1 second)
  Index health: Good
  Database size: 45 GB

WARNINGS:
- 3 slow queries identified (see detailed report)
- Storage growth rate higher than projected (review retention policy)

RECOMMENDATIONS:
1. Optimize slow queries (document search, user activity report)
2. Review retention policy and archive older documents
3. Plan for storage expansion in 2027
```

---

## Integration Patterns

### Automated Reporting Pipeline

**Daily Metrics Collection:**
```bash
#!/bin/bash
# daily-metrics.sh - Collect daily document control metrics

DATE=$(date +%Y-%m-%d)

# Collect document control metrics
python scripts/document-control-dashboard.py --period daily --output json --file metrics/doc-control-$DATE.json

# Collect change control metrics
python scripts/change-control-automation.py report --status all --output json --file metrics/change-control-$DATE.json

# Collect DMS performance metrics
python scripts/dms-performance-monitor.py --metrics all --output json --file metrics/dms-performance-$DATE.json

# Upload to analytics platform
python scripts/upload-to-analytics.py --directory metrics/ --date $DATE
```

### Management Review Automation

**Quarterly Management Review:**
```bash
#!/bin/bash
# quarterly-mgmt-review.sh - Generate quarterly management review package

QUARTER=$(date +%Y-Q%q)

# Generate document control dashboard
python scripts/document-control-dashboard.py --period quarterly --output html --file reports/doc-control-$QUARTER.html

# Generate change control analysis
python scripts/change-control-automation.py analyze --period quarterly --output html --file reports/change-control-$QUARTER.html

# Validate regulatory documentation
python scripts/regulatory-doc-validator.py --standard ISO13485 --output html --file reports/qms-validation-$QUARTER.html

# Generate DMS performance report
python scripts/dms-performance-monitor.py --health-check --period quarterly --output html --file reports/dms-performance-$QUARTER.html

# Compile into management review package
python scripts/compile-mgmt-review.py --quarter $QUARTER --output mgmt-review-$QUARTER.pdf
```

### Alerting and Notifications

**Overdue Document Alert:**
```bash
#!/bin/bash
# check-overdue-documents.sh - Alert for overdue documents

OVERDUE=$(python scripts/document-control-dashboard.py --metrics overdue --output json | jq '.summary.overdue_review')

if [ "$OVERDUE" -gt 10 ]; then
  python scripts/document-control-dashboard.py --metrics overdue --format email --recipients document-control@company.com
  python scripts/send-slack-notification.py --channel quality --message "High number of overdue documents: $OVERDUE"
fi
```

---

## Troubleshooting Guide

### Common Issues and Solutions

**Issue: Script Not Found or Permission Denied**
```bash
# Solution: Ensure script is executable and in correct location
cd /path/to/ra-qm-team/quality-documentation-manager/scripts/
chmod +x document-control-dashboard.py

# Run with python explicitly
python document-control-dashboard.py --help
```

**Issue: Module Import Errors**
```bash
# Solution: Install required dependencies
pip install -r requirements.txt

# Or install specific module
pip install pandas openpyxl jinja2
```

**Issue: JSON Output Formatting Error**
```bash
# Solution: Validate JSON output
python scripts/document-control-dashboard.py --output json | jq .

# If jq reports error, check for invalid characters or encoding issues
python scripts/document-control-dashboard.py --output json --encoding utf-8
```

**Issue: Performance Slow with Large Document Sets**
```bash
# Solution: Use filtering options
python scripts/document-control-dashboard.py --document-type SOP --department QA

# Or limit reporting period
python scripts/document-control-dashboard.py --period weekly
```

**Issue: Output File Permission Denied**
```bash
# Solution: Check directory permissions
ls -la output-directory/

# Create directory if doesn't exist
mkdir -p output-directory/
chmod 755 output-directory/
```

### Debug Mode

**Enable Verbose Logging:**
```bash
# Run with debug flag
python scripts/document-control-dashboard.py --debug --verbose

# Redirect output to log file
python scripts/document-control-dashboard.py --debug 2> debug.log
```

### Performance Optimization

**Large Dataset Optimization:**
- Use date range filters to limit data processed
- Export to CSV and process with external tools for very large datasets
- Consider batch processing for reporting across many departments
- Use database indexes for frequently queried fields

**Memory Management:**
- Process documents in batches rather than loading all at once
- Clear temporary files regularly
- Monitor memory usage during execution

### Support and Feedback

**Getting Help:**
- Check tool documentation: `python script.py --help`
- Review example commands in this guide
- Contact document control team for assistance
- Submit issues or feature requests to project repository

---

**Version:** 1.0
**Last Updated:** 2025-11-08
**Document Owner:** Quality Documentation Manager
**Next Review Date:** 2026-11-08
