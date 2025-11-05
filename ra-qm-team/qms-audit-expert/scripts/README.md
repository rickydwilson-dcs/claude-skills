# QMS Audit Expert Scripts

Python automation tools for ISO 13485 QMS audit management.

## Available Scripts

### audit_checklist_generator.py

**Purpose:** Generate comprehensive ISO 13485:2016 audit checklists with risk-based focus.

**Features:**
- Complete ISO 13485:2016 clause coverage (Clauses 4-8)
- 52 standard audit questions covering all QMS requirements
- Risk-based question prioritization (CRITICAL, HIGH, MEDIUM, LOW)
- Previous finding follow-up tracking
- Audit coverage metrics and analysis
- Multiple output formats (text, JSON, CSV)
- Customizable focus areas and risk prioritization

**Usage:**
```bash
# Generate full audit checklist
python audit_checklist_generator.py audit_scope.json

# JSON output for audit software integration
python audit_checklist_generator.py audit_scope.json --output json

# CSV export for spreadsheet tracking
python audit_checklist_generator.py audit_scope.json -o csv -f checklist.csv

# Verbose mode with detailed clause information
python audit_checklist_generator.py audit_scope.json -v
```

**Input Format:**
```json
{
  "audit_scope": {
    "audit_type": "Internal Audit",
    "scope_description": "Full QMS Review",
    "organization": "Acme Medical Devices"
  },
  "focus_areas": ["7.3", "8.2"],
  "risk_areas": ["Design Controls", "CAPA"],
  "previous_findings": [
    {
      "finding_id": "F-2024-001",
      "clause": "7.3.4",
      "description": "Design review not conducted at all stages",
      "status": "OPEN",
      "car_number": "CAR-2024-015",
      "identified_date": "2024-10-15",
      "target_closure": "2024-12-15",
      "follow_up_required": true
    }
  ]
}
```

**Output:**
- Text: Human-readable checklist with audit report template
- JSON: Structured data with complete metadata and metrics
- CSV: Spreadsheet-compatible question list

**Coverage:**
- Clause 4 (QMS): 7 questions
- Clause 5 (Management): 7 questions
- Clause 6 (Resources): 5 questions
- Clause 7 (Product Realization): 20 questions
- Clause 8 (Measurement): 13 questions

**Sample File:** `sample_audit_scope.json`

---

### audit-schedule-optimizer.py (Planned)

**Purpose:** Risk-based audit planning and schedule optimization.

**Features:**
- Annual audit schedule generation
- Risk-based frequency determination
- Resource allocation optimization
- Auditor competency matching
- Regulatory requirement tracking

---

### audit-prep-checklist.py (Planned)

**Purpose:** Comprehensive audit preparation automation.

**Features:**
- Pre-audit document review checklist
- Auditee notification generation
- Logistics coordination tracking
- Evidence collection planning
- Audit team briefing materials

---

### nonconformity-tracker.py (Planned)

**Purpose:** Audit finding and CAPA integration management.

**Features:**
- Finding categorization (Major/Minor/Observation)
- CAPA linkage tracking
- Follow-up audit scheduling
- Effectiveness verification tracking
- Trend analysis by clause/process

---

### audit-performance-analyzer.py (Planned)

**Purpose:** Audit program effectiveness monitoring.

**Features:**
- Audit KPI calculation
- Finding trend analysis
- Auditor performance metrics
- Process improvement identification
- Program optimization recommendations

---

## Common CLI Patterns

All scripts follow standard CLI conventions:

```bash
# Get help
python script_name.py --help

# Standard options
--output, -o {text,json,csv}  # Output format
--file, -f FILE               # Write to file
--verbose, -v                 # Detailed output
--version                     # Show version
```

## Output Format Examples

### Text Output
```
================================================================================
ISO 13485:2016 QMS AUDIT CHECKLIST
================================================================================
Generated: 2025-11-05
Audit Type: Internal Audit

--- AUDIT COVERAGE METRICS ---
Total Questions: 52
Critical Questions: 25
High Risk Questions: 20

[Questions organized by clause...]
```

### JSON Output
```json
{
  "metadata": {
    "tool": "audit_checklist_generator.py",
    "version": "1.0.0",
    "timestamp": "2025-11-05T12:00:00Z"
  },
  "coverage_metrics": {
    "total_questions": 52,
    "critical_questions": 25
  },
  "checklist": [...]
}
```

### CSV Output
```csv
Question ID,Clause,Sub-Clause,Risk Level,Question,Compliance Criteria,Evidence Required
4.1.1,4.1,General Requirements,CRITICAL,"Has QMS been established?","QMS documented","Quality Manual"
```

## Dependencies

All scripts use Python 3.8+ standard library only. No external dependencies required.

**Required modules:**
- argparse (CLI parsing)
- json (JSON input/output)
- sys (Exit codes, stderr)
- pathlib (Path handling)
- datetime (Timestamps)
- typing (Type hints)
- dataclasses (Data structures)
- enum (Enumerations)

## Error Handling

Scripts follow standard exit codes:

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | Normal completion |
| 1 | File error | Input file not found |
| 3 | Processing error | Invalid JSON format |
| 4 | Output error | Cannot write output file |

## Integration Examples

### Bash Script Integration
```bash
#!/bin/bash
# Generate monthly audit checklist

AUDIT_DATE=$(date +%Y-%m-%d)
AUDIT_FILE="audit_scope_${AUDIT_DATE}.json"

# Create scope file
cat > "$AUDIT_FILE" <<EOF
{
  "audit_scope": {
    "audit_type": "Monthly Internal Audit",
    "audit_date": "$AUDIT_DATE"
  },
  "focus_areas": ["8.2", "8.5"]
}
EOF

# Generate checklist
python audit_checklist_generator.py "$AUDIT_FILE" -o csv -f "checklist_${AUDIT_DATE}.csv"

echo "Audit checklist generated: checklist_${AUDIT_DATE}.csv"
```

### Python Integration
```python
import subprocess
import json

# Create audit scope
scope = {
    "audit_scope": {"audit_type": "Pre-Cert Audit"},
    "focus_areas": [],
    "risk_areas": ["Design Controls", "CAPA"]
}

# Write scope file
with open('scope.json', 'w') as f:
    json.dump(scope, f)

# Generate checklist
result = subprocess.run(
    ['python', 'audit_checklist_generator.py', 'scope.json', '-o', 'json'],
    capture_output=True,
    text=True
)

# Parse results
checklist = json.loads(result.stdout)
print(f"Generated {checklist['coverage_metrics']['total_questions']} questions")
```

### Audit Management Software Integration
```python
import requests
import json

# Generate checklist
checklist_json = subprocess.check_output([
    'python', 'audit_checklist_generator.py',
    'scope.json', '-o', 'json'
])

checklist = json.loads(checklist_json)

# Upload to audit management system
response = requests.post(
    'https://audit-system.example.com/api/checklists',
    json=checklist,
    headers={'Authorization': 'Bearer TOKEN'}
)

print(f"Checklist uploaded: {response.json()['id']}")
```

## Troubleshooting

### Script Won't Execute
```bash
# Make script executable
chmod +x audit_checklist_generator.py

# Run with Python explicitly
python3 audit_checklist_generator.py --help
```

### JSON Syntax Errors
```bash
# Validate JSON before running
python -m json.tool audit_scope.json

# Or use online validator
# https://jsonlint.com/
```

### Import Errors
```bash
# Verify Python version
python --version  # Should be 3.8+

# Check if running in correct directory
pwd
ls *.py
```

## Best Practices

**File Organization:**
- Store audit scope files in dedicated directory
- Use dated filenames: `audit_scope_2025-11-05.json`
- Keep generated checklists for audit records
- Archive completed audits with findings

**Version Control:**
- Track audit scope changes in git
- Document customizations to standard questions
- Version control organization-specific checklists
- Tag releases for audit cycles

**Quality Assurance:**
- Review generated checklists before audit
- Validate coverage metrics meet requirements
- Test scripts with sample data before production
- Maintain backup of configuration files

**Security:**
- Do not hardcode sensitive audit findings
- Use environment variables for API credentials
- Sanitize data before external sharing
- Follow data retention policies

## Support

For issues or questions:
1. Run script with `--help` flag
2. Check sample files in scripts directory
3. Review SKILL.md for detailed documentation
4. Validate JSON input format
5. Check Python version compatibility

## Future Enhancements

**Planned Features:**
- Multi-standard support (ISO 9001, ISO 14001)
- Question bank customization interface
- Historical audit comparison
- Finding severity scoring
- Automated audit report generation
- Integration with CAPA tracking systems
- Real-time audit collaboration
- Mobile-friendly checklist formats

## Contributing

When adding new scripts:
1. Follow Python CLI Standards (standards/cli-standards.md)
2. Include comprehensive help text
3. Support text, JSON, and CSV output
4. Add sample input files
5. Update this README
6. Document in SKILL.md

---

**Script Count:** 1 production-ready, 4 planned
**Last Updated:** 2025-11-05
**Python Version:** 3.8+
**License:** Part of claude-skills project
