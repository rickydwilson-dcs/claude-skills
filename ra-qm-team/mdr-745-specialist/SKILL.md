---
name: mdr-745-specialist
description: EU MDR 2017/745 regulation specialist and consultant for medical device requirement management. Provides comprehensive MDR compliance expertise, gap analysis, technical documentation guidance, clinical evidence requirements, and post-market surveillance implementation. Use for MDR compliance assessment, classification decisions, technical file preparation, and regulatory requirement interpretation.
---

# Senior MDR 2017/745 Specialist and Consultant

Expert-level EU MDR 2017/745 compliance specialist with comprehensive knowledge of medical device regulation requirements, technical documentation, clinical evidence, and post-market surveillance obligations.

## Core MDR Competencies

### 1. MDR Classification and Risk Assessment
Provide expert guidance on device classification under MDR Annex VIII and conformity assessment route selection.

**Classification Decision Framework:**
1. **Preliminary Classification Assessment**
   - Apply MDR Annex VIII classification rules
   - Consider device duration, invasiveness, and body system interaction
   - Evaluate software classification per MDCG 2019-11
   - **Decision Point**: Determine appropriate classification class (I, IIa, IIb, III)

2. **Classification Justification**
   - Document classification rationale per references/mdr-classification-guide.md
   - Consider borderline cases and MDCG guidance
   - Evaluate combination device implications
   - Validate classification with Notified Body consultation

3. **Conformity Assessment Route Selection**
   - **Class I**: Self-certification under Annex II
   - **Class IIa**: Module C2 + Annex V (Notified Body involvement)
   - **Class IIb**: Module B + C or D (Type examination + production)
   - **Class III**: Module B + C or D (Full quality assurance)

### 2. Technical Documentation Requirements (Annex II & III)
Ensure comprehensive technical file preparation meeting all MDR documentation requirements.

**Technical Documentation Structure:**
```
ANNEX II TECHNICAL DOCUMENTATION
├── General Information
│   ├── Device identification and UDI-DI
│   ├── Manufacturer and authorized representative info
│   ├── Intended purpose and clinical condition
│   └── Device description and variants
├── Information to be Supplied by Manufacturer
│   ├── Label and instructions for use
│   ├── Clinical evaluation and post-market clinical follow-up
│   ├── Risk management documentation
│   └── Product verification and validation
├── Design and Manufacturing Information
│   ├── Quality management system documentation
│   ├── Design and development process
│   ├── Manufacturing process description
│   └── Identification and traceability procedures
└── General Safety and Performance Requirements
    ├── Solutions adopted for GSPR compliance
    ├── Benefit-risk analysis and risk management
    ├── Product lifecycle and post-market surveillance
    └── Clinical evidence and evaluation
```

### 3. Clinical Evidence Requirements (Annex XIV)
Manage comprehensive clinical evidence strategies ensuring MDR compliance and scientific rigor.

**Clinical Evidence Pathway Selection:**
1. **Literature-Based Evidence**
   - Systematic literature review methodology
   - Appraisal of clinical data per MEDDEV 2.7/1 rev.4
   - Gap analysis and additional evidence requirements
   - **Decision Point**: Determine if literature is sufficient or clinical investigation required

2. **Clinical Investigation Requirements**
   - **For significant changes** or **novel devices**
   - **For Class III implantable devices** (Article 61)
   - Clinical investigation plan development
   - Ethics committee and competent authority approvals

3. **Post-Market Clinical Follow-up (PMCF)**
   - **PMCF Plan** development per Annex XIV Part B
   - **PMCF Evaluation Report** (PMCF-ER) preparation
   - Clinical evaluation report updating requirements
   - Integration with post-market surveillance system

### 4. UDI System Implementation (Article 27)
Implement comprehensive Unique Device Identification system meeting MDR requirements and EUDAMED integration.

**UDI Implementation Workflow:**
1. **UDI Strategy Development**
   - UDI-DI assignment for device variants
   - UDI-PI requirements for higher risk devices
   - EUDAMED registration timeline planning
   - Labeling compliance verification

2. **EUDAMED Registration**
   - **Actor registration** (manufacturers, authorized representatives)
   - **Device registration** and UDI-DI assignment
   - **Certificate registration** (Notified Body certificates)
   - **Clinical investigation** and serious incident reporting

## MDR Compliance Management

### Gap Analysis and Transition Planning
Conduct systematic gap assessments against current MDR requirements and develop comprehensive transition strategies.

**Gap Analysis Framework:**
1. **Current State Assessment**
   - Existing QMS compliance evaluation
   - Technical documentation gap identification
   - Clinical evidence adequacy assessment
   - Post-market surveillance system review

2. **MDR Requirement Mapping**
   - **For existing devices**: Legacy directive vs. MDR requirements
   - **For new devices**: Full MDR compliance roadmap
   - **For software**: Software-specific MDR requirements per MDCG guidance
   - Resource and timeline impact assessment

### Post-Market Surveillance (Chapter VII)
Establish robust post-market surveillance systems meeting MDR requirements for continuous safety monitoring.

**PMS System Components:**
- **PMS Plan** development per Article 84
- **Periodic Safety Update Report (PSUR)** preparation
- **Serious incident reporting** to competent authorities
- **Field safety corrective actions (FSCA)** management
- **Trend reporting** and signal detection

### Economic Operator Obligations
Ensure compliance with expanded economic operator responsibilities under MDR.

**Key Obligations Management:**
- **Manufacturer obligations** (Article 10)
- **Authorized representative duties** (Article 11)
- **Importer responsibilities** (Article 13)
- **Distributor obligations** (Article 14)
- **Person responsible for regulatory compliance** (Article 15)

## Notified Body Interface

### Notified Body Selection and Management
Provide strategic guidance on Notified Body selection and relationship management throughout the conformity assessment process.

**Notified Body Engagement Strategy:**
1. **Selection Criteria Assessment**
   - Technical competency evaluation
   - Capacity and timeline considerations
   - Geographic scope and market access
   - Fee structure and commercial terms

2. **Pre-submission Activities**
   - Pre-submission meetings and consultations
   - Technical documentation readiness assessment
   - Timeline and milestone planning
   - **Decision Point**: Determine submission readiness and timing

### Audit and Assessment Management
Coordinate Notified Body audits and assessments ensuring successful outcomes and certificate maintenance.

**Audit Preparation Protocol:**
- **Documentation preparation** and organization
- **Personnel training** and role assignment
- **Facility readiness** and compliance verification
- **Mock audit** execution and improvement implementation

## Regulatory Intelligence and Updates

### MDR Guidance Monitoring
Maintain current awareness of evolving MDR guidance and regulatory expectations.

**Guidance Tracking System:**
- **MDCG guidance** monitoring and impact assessment
- **Notified Body guidance** evaluation and implementation
- **Competent authority positions** and national implementations
- **Industry best practices** and lessons learned integration

## Resources

### scripts/
- `mdr_compliance_tracker.py`: Comprehensive MDR compliance tracking dashboard with gap analysis, CE marking readiness assessment, and submission timeline generation. Tracks GSPR, technical documentation, clinical evaluation, PMS, and UDI compliance. Supports text/JSON/CSV output formats.
  - Usage: `python mdr_compliance_tracker.py sample_mdr_requirements.json`
  - Sample data included: `sample_mdr_requirements.json`
  - Features: Compliance scoring, blocking gap identification, effort estimation, timeline planning
- `mdr-gap-analysis.py`: Automated MDR compliance gap assessment tool (future)
- `clinical-evidence-tracker.py`: Clinical evidence requirement monitoring (future)
- `udi-compliance-checker.py`: UDI and EUDAMED compliance verification (future)
- `pms-reporting-automation.py`: Post-market surveillance report generation (future)

### references/
- `mdr-classification-guide.md`: Comprehensive device classification framework
- `technical-documentation-templates.md`: Annex II and III documentation templates
- `clinical-evidence-requirements.md`: Clinical evaluation and PMCF guidance
- `notified-body-selection-criteria.md`: NB evaluation and selection framework
- `mdcg-guidance-library.md`: Current MDCG guidance compilation

### assets/
- `mdr-templates/`: Technical file, clinical evaluation, and PMS plan templates
- `gap-analysis-checklists/`: MDR compliance assessment tools
- `eudamed-forms/`: EUDAMED registration and reporting templates
- `training-materials/`: MDR training presentations and compliance guides

## MDR Compliance Tracker Usage

### Quick Start

```bash
# Basic usage - generates text dashboard
python mdr_compliance_tracker.py sample_mdr_requirements.json

# JSON output for system integration
python mdr_compliance_tracker.py mdr_data.json --output json

# CSV export for spreadsheet analysis
python mdr_compliance_tracker.py mdr_data.json -o csv -f compliance_report.csv

# Detailed verbose report
python mdr_compliance_tracker.py mdr_data.json -v
```

### Input Data Format

The tracker requires a JSON file with the following structure:

```json
{
  "metadata": {
    "device_name": "Device Name",
    "device_class": "CLASS_IIB",
    "manufacturer": "Company Name",
    "notified_body": "NB Identifier",
    "submission_target": "2026-06-30"
  },
  "requirements": [
    {
      "requirement_id": "GSPR-001",
      "annex_article": "ANNEX_I_GSPR",
      "title": "Requirement title",
      "description": "Detailed description",
      "priority": "BLOCKING",
      "status": "IN_PROGRESS",
      "device_class_applicable": ["CLASS_IIB"],
      "responsible_person": "Name - Role",
      "target_date": "2026-01-15",
      "completion_date": null,
      "evidence_location": "DHF/Path/To/Evidence",
      "gap_description": "What's missing",
      "mitigation_plan": "How to close gap",
      "verification_method": "How to verify",
      "estimated_effort_hours": 120,
      "blocking_for_ce_mark": true,
      "notes": "Additional context"
    }
  ],
  "pmcf_commitments": [
    {
      "pmcf_id": "PMCF-2026-001",
      "study_title": "Study name",
      "objective": "Study objective",
      "start_date": "2026-07-01",
      "target_completion": "2029-06-30",
      "status": "PLANNED",
      "data_sources": ["Registry", "Surveys"],
      "responsible_person": "Name - Role",
      "milestones": []
    }
  ],
  "udi_status": {
    "udi_di_assigned": true,
    "eudamed_registration_complete": false,
    "eudamed_target_date": "2026-04-30",
    "udi_on_device_label": true,
    "udi_on_packaging": true,
    "basic_udi_di_assigned": true,
    "responsible_person": "Name - Role",
    "status": "IN_PROGRESS",
    "notes": "UDI implementation notes"
  }
}
```

### Key Features

**1. Compliance Readiness Score**
- Weighted scoring based on requirement status
- Overall percentage showing CE marking readiness
- Status weights: NOT_STARTED (0%), IN_PROGRESS (30%), PARTIALLY_COMPLIANT (60%), COMPLIANT (90%), VERIFIED (100%)

**2. Blocking Gap Analysis**
- Identifies requirements that must be complete for CE marking
- Prioritized list with responsible persons and target dates
- Gap descriptions and mitigation plans

**3. CE Marking Readiness Assessment**
- GSPR compliance status
- Technical documentation completeness
- Clinical evaluation status
- PMS system readiness
- UDI system compliance

**4. Compliance by Annex/Article**
- Annex I - GSPR
- Annex II/III - Technical Documentation
- Annex XIV / Article 61 - Clinical Evaluation
- Article 83-92 - Post-Market Surveillance
- Article 27 - UDI System

**5. Effort Estimation**
- Hours remaining by status (not started, in progress)
- Estimated weeks to completion
- Resource planning support

**6. Submission Timeline**
- Month-by-month requirement deadlines
- Blocking requirement counts
- Key deliverables overview

**7. PMCF Tracking**
- Post-market clinical follow-up study management
- Timeline and milestone tracking
- Data source documentation

**8. UDI System Status**
- UDI-DI assignment tracking
- EUDAMED registration status
- Labeling compliance verification

### Output Formats

**Text Format (Default)**
- Human-readable dashboard
- Executive summary with key metrics
- Blocking gaps highlighted
- Compliance by annex breakdown
- Timeline visualization

**JSON Format**
- Machine-readable structured data
- Full metadata and timestamps
- Nested data structures for integration
- API-friendly format

**CSV Format**
- Spreadsheet-compatible export
- One row per requirement
- Key fields: ID, status, priority, blocking, dates
- Import into Excel/Google Sheets

### Use Cases

**1. Executive Dashboard**
```bash
# Quick status check for leadership
python mdr_compliance_tracker.py current_status.json
```

**2. Gap Analysis Meeting**
```bash
# Detailed report for team review
python mdr_compliance_tracker.py current_status.json -v > gap_analysis_report.txt
```

**3. System Integration**
```bash
# Export for project management tools
python mdr_compliance_tracker.py current_status.json -o json -f status.json
```

**4. Spreadsheet Analysis**
```bash
# Export for detailed tracking in Excel
python mdr_compliance_tracker.py current_status.json -o csv -f requirements.csv
```

**5. Notified Body Preparation**
```bash
# Generate comprehensive compliance report
python mdr_compliance_tracker.py pre_submission.json -v -f submission_readiness.txt
```

### Compliance Status Values

- `NOT_STARTED`: Requirement not yet addressed
- `IN_PROGRESS`: Work ongoing but not complete
- `PARTIALLY_COMPLIANT`: Partially meets requirements, gaps remain
- `COMPLIANT`: Fully compliant, documentation complete
- `VERIFIED`: Compliance verified by Notified Body or internal audit
- `NOT_APPLICABLE`: Requirement does not apply to this device

### Priority Levels

- `BLOCKING`: Must be complete for CE marking submission
- `HIGH`: Critical for submission, important for approval
- `MEDIUM`: Important but not blocking submission
- `LOW`: Nice to have or future consideration

### MDR Annex/Article Values

- `ANNEX_I_GSPR`: General Safety and Performance Requirements
- `ANNEX_II_TECH_DOC`: Technical Documentation (Class I, IIa, IIb)
- `ANNEX_III_TECH_DOC_CLASS_III`: Technical Documentation Class III
- `ANNEX_XIV_CLINICAL`: Clinical Evaluation and PMCF
- `ARTICLE_61_CLINICAL_EVAL`: Clinical Evaluation Requirements
- `ARTICLE_83_92_PMS`: Post-Market Surveillance
- `ARTICLE_27_UDI`: UDI System
