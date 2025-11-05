# GDPR/DSGVO Compliance Checker - Scripts

This directory contains Python automation tools for GDPR/DSGVO compliance assessment and management.

## Available Scripts

### `gdpr_compliance_checker.py`

Comprehensive GDPR compliance assessment tool for data processing activities.

**Features**:
- Analyzes processing activities against GDPR requirements (Articles 6, 9, 10, 12-23, 25, 30, 32, 33-35, Chapter V)
- Risk-based assessment with priority scoring
- Identifies high-priority compliance gaps
- Supports text, JSON, and CSV output formats
- CI/CD integration with exit codes

**Quick Start**:
```bash
# View help and usage
python gdpr_compliance_checker.py --help

# Run basic assessment
python gdpr_compliance_checker.py sample_processing_inventory.json

# Generate JSON report for dashboard
python gdpr_compliance_checker.py sample_processing_inventory.json -o json -v

# Export CSV for spreadsheet analysis
python gdpr_compliance_checker.py sample_processing_inventory.json -o csv -f report.csv
```

**Input Format**:
The script accepts JSON files containing a processing inventory. See `sample_processing_inventory.json` for a complete example with 8 realistic scenarios including:
- Customer CRM database
- Patient health records (special category data)
- Employee HR system with international transfers
- Marketing analytics
- Medical device data collection
- Automated credit scoring
- Clinical research data
- Video surveillance (biometric data)

**Assessment Areas**:
1. **Lawful Basis (Art. 6)**: Validates legal basis for processing
2. **Special Categories (Art. 9)**: Checks special category data handling
3. **Data Subject Rights (Art. 12-23)**: Verifies all 7 rights implementation
4. **DPIAs (Art. 35)**: Identifies required impact assessments
5. **Technical Measures (Art. 25, 32)**: Assesses security and data protection by design
6. **International Transfers (Ch. V)**: Validates transfer mechanisms (SCCs, adequacy, BCRs)
7. **Breach Readiness (Art. 33-34)**: Checks notification procedures
8. **Documentation (Art. 30)**: Identifies missing records and agreements

**Output Formats**:

*Text (Human-readable)*:
```
======================================================================
GDPR/DSGVO COMPLIANCE ASSESSMENT REPORT
======================================================================
Generated: 2025-11-05 21:29:31 UTC

EXECUTIVE SUMMARY
----------------------------------------------------------------------
Total Processing Activities: 8
Overall Compliance Score: 62.5%

Risk Distribution:
  Critical Issues: 3
  High Risk:       3
  Medium Risk:     1
  Low Risk:        1

HIGH-PRIORITY GAPS REQUIRING IMMEDIATE ATTENTION
----------------------------------------------------------------------
1. [CRITICAL] Video Surveillance System
   Area: lawful_basis
   Issue: Legitimate interests cannot be used for special category data
...
```

*JSON (Machine-readable)*:
```json
{
  "metadata": {
    "tool": "gdpr_compliance_checker.py",
    "version": "1.0.0",
    "timestamp": "2025-11-05T21:29:36Z"
  },
  "results": {
    "summary": {
      "total_activities": 8,
      "overall_compliance_score": 62.5,
      "risk_distribution": {
        "critical": 3,
        "high": 3,
        "medium": 1,
        "low": 1
      }
    }
  }
}
```

*CSV (Spreadsheet-ready)*:
```csv
Activity ID,Activity Name,Overall Risk,Compliance Score,Lawful Basis Status,Data Subject Rights Score,DPIA Required,DPIA Completed,Technical Measures Score,High Priority Issues
PA-001,Customer CRM,HIGH,64.3,Pass,57.1,No,No,85.7,4
PA-002,Patient Health Records,MEDIUM,90.5,Pass,71.4,Yes,Yes,100.0,1
...
```

**Exit Codes**:
- `0`: Assessment completed successfully, no critical issues
- `1`: File not found or permission error
- `3`: Assessment completed but critical compliance issues detected
- `4`: Output file write error
- `130`: User cancelled operation

**CI/CD Integration**:
```bash
# Fail pipeline if critical issues detected
python gdpr_compliance_checker.py inventory.json -o json || exit 1

# Generate report but continue pipeline
python gdpr_compliance_checker.py inventory.json -o json -f report.json || true
```

## Sample Data

### `sample_processing_inventory.json`

Comprehensive sample demonstrating 8 realistic data processing scenarios:

1. **PA-001**: Customer CRM - Standard business processing
2. **PA-002**: Patient Health Records - High-risk health data with DPIA
3. **PA-003**: Employee HR System - International transfers via SCCs
4. **PA-004**: Marketing Analytics - Multiple compliance gaps (critical)
5. **PA-005**: Medical Device Data - Health data without completed DPIA (critical)
6. **PA-006**: Automated Credit Scoring - Compliant automated decision-making
7. **PA-007**: Research Study - Special category data with proper safeguards
8. **PA-008**: Video Surveillance - Biometric data with major gaps (critical)

**Scenarios Include**:
- Basic personal data and special category data (health, genetic, biometric)
- Various lawful bases (consent, contract, legitimate interests)
- DPIAs required and completed/not completed
- International transfers (adequacy, SCCs, no transfers)
- Full and partial data subject rights implementation
- Strong and weak technical/organizational measures
- Complete and incomplete documentation

## Requirements

- Python 3.8+
- Standard library only (no external dependencies)

## Usage Patterns

### Quarterly Compliance Review
```bash
# Generate comprehensive report
python gdpr_compliance_checker.py Q4_2025_inventory.json -v > Q4_report.txt

# Export metrics for tracking
python gdpr_compliance_checker.py Q4_2025_inventory.json -o csv -f Q4_metrics.csv
```

### Pre-Audit Assessment
```bash
# Detailed JSON for remediation planning
python gdpr_compliance_checker.py inventory.json -o json -v -f pre_audit.json

# Focus on critical issues
python gdpr_compliance_checker.py inventory.json | grep -A5 "CRITICAL"
```

### Continuous Monitoring
```bash
# Daily automated check
0 2 * * * cd /compliance && python gdpr_compliance_checker.py inventory.json -o json -f daily_check.json

# Alert on critical issues
python gdpr_compliance_checker.py inventory.json -o json | \
  jq '.results.summary.risk_distribution.critical' | \
  [ $(cat) -gt 0 ] && echo "Critical GDPR issues detected" | mail -s "GDPR Alert" compliance@company.com
```

## Integration Examples

### Compliance Dashboard
```python
import json
import subprocess

# Run assessment
result = subprocess.run(
    ['python', 'gdpr_compliance_checker.py', 'inventory.json', '-o', 'json'],
    capture_output=True, text=True
)

data = json.loads(result.stdout)
compliance_score = data['results']['summary']['overall_compliance_score']
critical_count = data['results']['summary']['risk_distribution']['critical']

# Update dashboard metrics
update_dashboard(compliance_score, critical_count)
```

### Jira Integration
```bash
# Create Jira tickets for high-priority gaps
python gdpr_compliance_checker.py inventory.json -o json | \
  jq -r '.results.high_priority_gaps[] | select(.risk == "critical") |
    "[\(.risk | ascii_upcase)] \(.activity): \(.issue)"' | \
  while read issue; do
    jira create --project GDPR --type Bug --summary "$issue"
  done
```

## Troubleshooting

**Issue**: "File not found" error
**Solution**: Ensure JSON file path is correct and file exists

**Issue**: "Invalid JSON format" error
**Solution**: Validate JSON syntax using `python -m json.tool inventory.json`

**Issue**: "Warning: Skipping invalid activity"
**Solution**: Check activity data structure matches required fields (see sample file)

**Issue**: Script runs but shows 0 activities
**Solution**: Ensure JSON has top-level "processing_activities" array

## Support

For questions or issues:
- Review sample file: `sample_processing_inventory.json`
- Check SKILL documentation: `../SKILL.md`
- Validate JSON structure matches schema in `--help`

## Version History

- **1.0.0** (2025-11-05): Initial release
  - Full GDPR Article coverage (6, 9, 10, 12-23, 25, 30, 32, 33-35, Chapter V)
  - Risk-based assessment with priority scoring
  - Text, JSON, and CSV output formats
  - Comprehensive sample data with 8 scenarios
