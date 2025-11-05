# MDR 2017/745 Compliance Scripts

Production-ready Python automation tools for EU MDR 2017/745 Medical Device Regulation compliance tracking and management.

## Available Scripts

### mdr_compliance_tracker.py

**Purpose:** Comprehensive MDR compliance tracking dashboard with gap analysis, CE marking readiness assessment, and submission timeline generation.

**Features:**
- Tracks compliance across all MDR annexes and articles
- Calculates overall readiness percentage
- Identifies blocking gaps for CE marking
- Generates submission timelines
- Tracks Post-Market Clinical Follow-up (PMCF) commitments
- Monitors UDI system compliance
- Estimates remaining effort and resource requirements

**Usage:**
```bash
# Basic text dashboard
python mdr_compliance_tracker.py sample_mdr_requirements.json

# JSON output
python mdr_compliance_tracker.py data.json --output json

# CSV export
python mdr_compliance_tracker.py data.json -o csv -f report.csv

# Verbose detailed report
python mdr_compliance_tracker.py data.json -v

# Help
python mdr_compliance_tracker.py --help
```

**Input:** JSON file with MDR requirements, PMCF commitments, and UDI status
**Output:** Text/JSON/CSV compliance dashboard

**Sample Data:** `sample_mdr_requirements.json` - Complete example for Class IIb cardiac monitoring device

**Key Metrics:**
- Overall compliance readiness percentage
- Blocking gaps count and details
- CE marking readiness assessment (GSPR, Tech Doc, Clinical, PMS, UDI)
- Compliance by MDR Annex/Article
- Effort estimation (hours and weeks)
- Submission timeline (monthly breakdown)

**MDR Coverage:**
- Annex I - General Safety and Performance Requirements (GSPR)
- Annex II/III - Technical Documentation
- Annex XIV / Article 61 - Clinical Evaluation
- Articles 83-92 - Post-Market Surveillance
- Article 27 - UDI System

**Status Tracking:**
- NOT_STARTED (0% weight)
- IN_PROGRESS (30% weight)
- PARTIALLY_COMPLIANT (60% weight)
- COMPLIANT (90% weight)
- VERIFIED (100% weight)
- NOT_APPLICABLE (100% weight)

**Priority Levels:**
- BLOCKING - Must complete for CE marking
- HIGH - Critical for submission
- MEDIUM - Important but not blocking
- LOW - Future consideration

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## Installation

No installation required. Scripts use Python standard library only.

```bash
# Make executable (optional)
chmod +x mdr_compliance_tracker.py

# Run directly
python mdr_compliance_tracker.py sample_mdr_requirements.json
```

## Quick Start

1. Copy `sample_mdr_requirements.json` to create your device's compliance data file
2. Update metadata with your device information
3. Add/modify requirements to match your device class and regulatory strategy
4. Update status, target dates, and responsible persons
5. Run tracker to generate compliance dashboard

```bash
# Copy sample and customize
cp sample_mdr_requirements.json my_device_mdr.json
# Edit my_device_mdr.json with your data

# Generate dashboard
python mdr_compliance_tracker.py my_device_mdr.json

# Export for team review
python mdr_compliance_tracker.py my_device_mdr.json -v -f compliance_review.txt
```

## Integration Examples

### Weekly Status Report
```bash
# Generate JSON for automated reporting
python mdr_compliance_tracker.py current_status.json -o json -f weekly_report.json
```

### Management Dashboard
```bash
# Quick executive summary
python mdr_compliance_tracker.py current_status.json | head -30
```

### Notified Body Preparation
```bash
# Comprehensive submission readiness report
python mdr_compliance_tracker.py pre_submission.json -v > nb_readiness_report.txt
```

### Project Planning
```bash
# Export to CSV for Gantt chart creation
python mdr_compliance_tracker.py project_plan.json -o csv -f requirements_timeline.csv
```

## Output Examples

### Text Format (Default)
```
================================================================================
EU MDR 2017/745 COMPLIANCE TRACKING DASHBOARD
================================================================================
Report Generated: 2025-11-05
Device: SmartCardio Pro - Cardiac Monitoring System
Device Class: CLASS_IIB

--- OVERALL MDR COMPLIANCE READINESS ---
Compliance Score: 62.0%

--- CE MARKING READINESS ASSESSMENT ---
Status: NOT_READY
Blocking Gaps: 7
...
```

### JSON Format
```json
{
  "metadata": {
    "tool": "mdr_compliance_tracker.py",
    "version": "1.0.0",
    "timestamp": "2025-11-05T21:28:56Z",
    "device_name": "SmartCardio Pro"
  },
  "summary": {
    "overall_readiness_pct": 62.0,
    "blocking_gaps_count": 7,
    ...
  }
}
```

### CSV Format
```csv
Requirement ID,Annex/Article,Title,Status,Priority,Blocking,Target Date,Responsible,Effort Hours,Gap Description
GSPR-001,ANNEX_I_GSPR,General Safety Requirements,COMPLIANT,BLOCKING,True,2025-12-15,Dr. Sarah Mueller,0,
...
```

## Data Structure

### Metadata
- device_name
- device_class (CLASS_I, CLASS_IIA, CLASS_IIB, CLASS_III)
- manufacturer
- notified_body
- submission_target

### Requirements
- requirement_id
- annex_article
- title, description
- priority, status
- device_class_applicable
- responsible_person
- target_date, completion_date
- evidence_location
- gap_description, mitigation_plan
- verification_method
- estimated_effort_hours
- blocking_for_ce_mark
- notes

### PMCF Commitments
- pmcf_id
- study_title, objective
- start_date, target_completion
- status
- data_sources
- responsible_person
- milestones

### UDI Status
- udi_di_assigned
- eudamed_registration_complete
- eudamed_target_date
- udi_on_device_label, udi_on_packaging
- basic_udi_di_assigned
- responsible_person
- status, notes

## Best Practices

1. **Regular Updates:** Update compliance data weekly or bi-weekly
2. **Accurate Status:** Use appropriate status values, avoid premature "COMPLIANT" marking
3. **Blocking Flags:** Mark requirements as blocking only if truly required for CE submission
4. **Effort Estimation:** Estimate hours realistically for resource planning
5. **Evidence Location:** Document evidence paths for audit trail
6. **Gap Description:** Be specific about what's missing
7. **Mitigation Plans:** Document concrete action items with owners and dates

## Troubleshooting

### Script won't run
```bash
# Check Python version (requires 3.7+)
python --version

# Use python3 if needed
python3 mdr_compliance_tracker.py sample_mdr_requirements.json
```

### JSON parsing error
```bash
# Validate JSON syntax
python -m json.tool your_file.json
```

### Missing fields error
- Ensure all required fields are present in your JSON
- Compare to sample_mdr_requirements.json structure
- Check enum values (ANNEX_I_GSPR, BLOCKING, IN_PROGRESS, etc.)

## Future Scripts (Planned)

- `mdr-gap-analysis.py` - Automated gap assessment tool
- `clinical-evidence-tracker.py` - Clinical evidence monitoring
- `udi-compliance-checker.py` - UDI and EUDAMED verification
- `pms-reporting-automation.py` - PMS report generation

## Documentation

For complete MDR specialist guidance, see:
- `../SKILL.md` - Full MDR specialist skill documentation
- `../references/` - MDR guidance and templates
- `../assets/` - MDR compliance templates

## Support

For questions or issues:
1. Review sample_mdr_requirements.json for data structure
2. Check SKILL.md for detailed usage instructions
3. Validate JSON format with `python -m json.tool`

## Version History

**1.0.0** (2025-11-05)
- Initial release
- Full MDR compliance tracking
- Gap analysis and readiness assessment
- PMCF and UDI tracking
- Text/JSON/CSV output formats
- Sample data included

---

**Script Author:** MDR 2017/745 Specialist Team
**Skill:** ra-qm-team/mdr-745-specialist
**Version:** 1.0.0
**Last Updated:** 2025-11-05
