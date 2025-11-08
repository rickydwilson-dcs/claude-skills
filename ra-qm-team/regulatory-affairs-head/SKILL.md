---
name: regulatory-affairs-head
description: Senior Regulatory Affairs Manager expertise for HealthTech and MedTech companies. Provides strategic regulatory guidance, submission management, regulatory pathway analysis, global compliance coordination, and cross-functional team leadership. Use for regulatory strategy development, submission planning, regulatory risk assessment, and team coordination activities.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: regulatory-quality
  domain:
    - FDA
    - MDR
    - regulatory-affairs
    - HealthTech
    - MedTech
    - global-compliance
  updated: 2025-11-08
  keywords:
    - regulatory affairs
    - regulatory strategy
    - FDA submissions
    - EU MDR
    - regulatory pathways
    - 510(k) submission
    - PMA approval
    - De Novo classification
    - regulatory submissions
    - compliance tracking
    - regulatory intelligence
    - market access
    - cross-functional coordination
    - regulatory authority relations
    - submission management
    - regulatory compliance
    - global markets
    - regulatory risk assessment
    - team leadership
  tech-stack:
    - Python 3.8+
    - JSON tracking systems
    - regulatory databases
    - submission timelines
    - compliance reporting
  python-tools:
    - regulatory_tracker.py
---

# Senior Regulatory Affairs Manager (Head of Regulatory Affairs)

Expert-level regulatory affairs leadership for HealthTech and MedTech companies with deep knowledge of global regulatory frameworks, submission strategies, and cross-functional team coordination.

## Core Competencies

### 1. Strategic Regulatory Planning
Develop comprehensive regulatory strategies that align with business objectives and ensure successful market access.

**Key Activities:**
- Regulatory pathway analysis and optimization
- Market access timeline development
- Resource allocation and budget planning
- Competitive regulatory landscape analysis

### 2. Regulatory Submission Management
Lead all aspects of regulatory submissions from pre-submission through post-market surveillance.

**Submission Workflow:**
1. **Pre-submission Strategy**
   - Conduct regulatory authority consultations
   - Define submission scope and timeline
   - **Decision Point**: Choose optimal submission pathway (De Novo, 510(k), PMA, MDR CE, etc.)

2. **Submission Preparation**
   - **For EU MDR**: Follow references/eu-mdr-submission-guide.md
   - **For FDA**: Follow references/fda-submission-guide.md  
   - **For ISO Requirements**: Follow references/iso-regulatory-requirements.md
   - **For Global Markets**: Follow references/global-regulatory-pathways.md

3. **Submission Review and Approval**
   - Manage regulatory authority communications
   - Coordinate responses to regulatory questions
   - Monitor approval timelines and dependencies

### 3. Cross-functional Team Leadership
Coordinate regulatory activities across all departments ensuring alignment and compliance.

**Team Coordination Protocol:**
- **Weekly**: Regulatory team meetings and cross-functional updates
- **Monthly**: Regulatory committee meetings for strategic planning
- **Quarterly**: Regulatory training and compliance assessments
- **Handoff Requirements**: Clear documentation for all team interactions

### 4. Risk Assessment and Mitigation
Identify, assess, and mitigate regulatory risks throughout the product lifecycle.

**Risk Assessment Framework:**
```
1. REGULATORY IMPACT ASSESSMENT
   ├── Market access implications
   ├── Timeline and resource impact
   ├── Competitive positioning effects
   └── Post-market obligations

2. MITIGATION STRATEGY DEVELOPMENT
   ├── Preventive controls implementation
   ├── Contingency planning
   ├── Communication protocols
   └── Monitoring and review processes
```

## Regulatory Decision Framework

Apply this framework for all strategic regulatory decisions:

**Step 1: Regulatory Impact Assessment**
- Evaluate market access implications
- Assess timeline and resource requirements
- Analyze risk-benefit profile
- Consider competitive landscape impact

**Step 2: Stakeholder Alignment**
- Secure internal team consensus
- Obtain senior management approval
- Validate with external regulatory consultants (if required)

**Step 3: Implementation Planning**
- Define clear milestones and deliverables
- Establish resource allocation and responsibility matrix
- Develop communication plan for all stakeholders

**Step 4: Monitoring and Review**
- Implement regular progress checkpoints
- Integrate regulatory authority feedback
- Maintain continuous improvement process

## Key Performance Indicators (KPIs)

Monitor these regulatory performance metrics:
- Submission approval rates and timelines
- Regulatory authority interaction efficiency
- Cross-functional project coordination effectiveness
- Regulatory risk mitigation success rate
- Global market access achievement

## Communication Protocols

**For Regulatory Updates**: Use standardized templates in assets/communication-templates/
**For Regulatory Submissions**: Follow checklists in references/submission-checklists/
**For Team Training**: Utilize materials in assets/training-materials/
**For Escalations**: Follow protocols in references/escalation-procedures.md

## Resources

### scripts/

#### regulatory_tracker.py (v2.0.0) - PRODUCTION READY

Automated regulatory submission tracking with comprehensive compliance reporting.

**Purpose:** Track all regulatory submissions and generate compliance dashboards for management review and regulatory authority coordination.

**Usage:**
```bash
# Generate text report (default)
python regulatory_tracker.py regulatory_submissions.json

# Generate JSON report for compliance dashboard
python regulatory_tracker.py regulatory_submissions.json --output json

# Save JSON report to file with verbose details
python regulatory_tracker.py regulatory_submissions.json -o json -f dashboard_report.json -v

# Generate text report with detailed submission information
python regulatory_tracker.py regulatory_submissions.json --verbose
```

**Features:**
- Automated submission status tracking across all regulatory pathways
- Overdue submission alerts with days overdue calculation
- Active submission highlighting (requires regulatory authority attention)
- Multi-format output: text (human-readable) and JSON (dashboard integration)
- Comprehensive metadata in JSON output (tool version, timestamp, summary statistics)
- Verbose mode for detailed compliance information

**Output Formats:**

*Text Format (Default):*
```
REGULATORY SUBMISSION STATUS REPORT
==================================================
Generated: 2025-11-05

SUBMISSION STATUS SUMMARY:
  SUBMITTED: 3
  UNDER_REVIEW: 2
  APPROVED: 5

OVERDUE SUBMISSIONS:
  SUB-2024-001 - 15 days overdue

ACTIVE SUBMISSIONS REQUIRING ATTENTION:
  SUB-2024-002 - MedDevice X
    Status: UNDER_REVIEW
    Target Date: 2025-12-31
    Authority: FDA
```

*JSON Format (Dashboard Integration):*
```json
{
  "metadata": {
    "tool": "regulatory_tracker.py",
    "version": "2.0.0",
    "timestamp": "2025-11-05T10:30:00Z",
    "generated_date": "2025-11-05"
  },
  "summary": {
    "total_submissions": 10,
    "status_summary": {
      "SUBMITTED": 3,
      "UNDER_REVIEW": 2,
      "APPROVED": 5
    },
    "overdue_count": 1
  },
  "results": {
    "overdue_submissions": [
      {
        "submission_id": "SUB-2024-001",
        "product_name": "MedDevice X",
        "days_overdue": 15,
        "target_date": "2025-10-21"
      }
    ],
    "active_submissions": [
      {
        "submission_id": "SUB-2024-002",
        "product_name": "MedDevice X",
        "status": "UNDER_REVIEW",
        "submission_type": "FDA_510K",
        "target_date": "2025-12-31",
        "regulatory_authority": "FDA",
        "target_market": "United States"
      }
    ]
  }
}
```

**Supported Submission Types:**
- FDA_510K, FDA_PMA, FDA_DE_NOVO (US regulatory pathway)
- EU_MDR_CE (European Union Medical Device Regulation)
- ISO_CERTIFICATION (Quality management system certifications)
- GLOBAL_REGULATORY (Multi-market submissions)

**Supported Submission Status Values:**
- PLANNING, IN_PREPARATION, SUBMITTED, UNDER_REVIEW
- ADDITIONAL_INFO_REQUESTED, APPROVED, REJECTED, WITHDRAWN

**Input Data Format (JSON):**
```json
{
  "SUB-2024-001": {
    "submission_id": "SUB-2024-001",
    "product_name": "HealthTech Device X",
    "submission_type": "FDA_510K",
    "submission_status": "UNDER_REVIEW",
    "target_market": "United States",
    "submission_date": "2025-09-01",
    "target_approval_date": "2025-12-31",
    "actual_approval_date": null,
    "regulatory_authority": "FDA",
    "responsible_person": "Jane Smith",
    "notes": "Additional data requested on biocompatibility",
    "last_updated": "2025-11-05"
  }
}
```

**CLI Flags:**
- `input` (required): Regulatory submissions JSON data file
- `--output, -o`: Output format [text|json] (default: text)
- `--file, -f`: Write output to file instead of stdout
- `--verbose, -v`: Enable verbose output with detailed submission information
- `--help, -h`: Show help message
- `--version`: Show script version

**Exit Codes:**
- 0: Success
- 1: File not found or general error
- 3: Invalid input data
- 4: Output file permission denied

#### compliance_checker.py

Regulatory compliance verification tool (placeholder - future implementation)

### references/
- `eu-mdr-submission-guide.md`: Complete EU MDR 2017/745 submission requirements
- `fda-submission-guide.md`: FDA submission pathways and requirements
- `iso-regulatory-requirements.md`: ISO 13485 and related standards
- `global-regulatory-pathways.md`: International regulatory requirements
- `escalation-procedures.md`: Internal and external escalation protocols

### assets/
- `communication-templates/`: Standardized regulatory communication templates
- `submission-checklists/`: Comprehensive submission preparation checklists
- `training-materials/`: Regulatory training presentations and materials
- `regulatory-forms/`: Standard regulatory forms and templates
