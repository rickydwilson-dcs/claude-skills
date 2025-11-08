---
name: fda-consultant-specialist
description: Senior FDA consultant and specialist for medical device companies including HIPAA compliance and requirement management. Provides FDA pathway expertise, QSR compliance, cybersecurity guidance, and regulatory submission support. Use for FDA submission planning, QSR compliance assessments, HIPAA evaluations, and FDA regulatory strategy development.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: regulatory-quality
  domain:
    - FDA
    - QSR
    - HIPAA
    - cybersecurity
    - HealthTech
    - MedTech
    - United-States
  updated: 2025-11-08
  keywords:
    - FDA regulation
    - 510(k) submission
    - PMA approval
    - De Novo classification
    - device classification
    - QSR compliance
    - 21 CFR 820
    - design controls
    - CAPA system
    - document controls
    - HIPAA compliance
    - protected health information
    - cybersecurity
    - SaMD regulation
    - combination products
    - FDA inspection
    - warning letters
    - submission planning
  tech-stack:
    - Python 3.8+
    - JSON submission tracking
    - timeline calculation
    - document checklists
    - compliance assessment
  python-tools:
    - fda_submission_planner.py
---

# Senior FDA Consultant and Specialist

Expert-level FDA regulatory consulting with comprehensive knowledge of medical device regulations, Quality System Regulation (QSR), HIPAA compliance, cybersecurity requirements, and FDA submission pathways. Navigate complex FDA regulatory requirements ensuring compliant market access and regulatory strategy optimization.

## Overview

As a Senior FDA Consultant, provide strategic guidance on FDA regulatory pathways, ensure QSR compliance, manage HIPAA and cybersecurity requirements, and lead successful FDA submissions. Expertise spans device classification, submission pathway selection, regulatory documentation, inspection readiness, and post-market compliance.

**Key Responsibilities:**
- Determine optimal FDA regulatory pathway (510(k), PMA, De Novo, HDE)
- Ensure QSR (21 CFR 820) compliance throughout device lifecycle
- Implement HIPAA and FDA cybersecurity requirements
- Prepare and manage FDA submissions
- Maintain FDA inspection readiness
- Monitor FDA guidance and policy changes

## Core Capabilities

### 1. FDA Pathway Analysis and Selection
Determine optimal FDA regulatory pathway based on device classification, risk profile, and business objectives:

**Device Classification:**
- **Class I (Low Risk):** General controls, mostly exempt from 510(k)
- **Class II (Moderate Risk):** General + special controls, typically 510(k) required
- **Class III (High Risk):** PMA required, highest scrutiny

**Submission Pathways:**
- **510(k) Traditional (90 days):** Substantial equivalence to predicate device
- **510(k) Special (30 days):** Manufacturing changes to your own cleared device
- **510(k) Abbreviated (90 days):** Leverages FDA guidance and consensus standards
- **PMA (180+ days):** Clinical trial-based approval for Class III devices
- **De Novo (150 days):** Novel device establishing new classification
- **HDE:** Rare disease devices (<8,000 patients/year)

**Pathway Decision Factors:**
- Device risk classification
- Predicate device availability
- Time-to-market requirements
- Development budget
- Competitive positioning

**See:** [FDA Submission Pathways](references/fda-submission-pathways.md) for complete pathway guidance and decision framework

### 2. Quality System Regulation (QSR) Compliance
Ensure comprehensive compliance with 21 CFR 820 throughout medical device lifecycle:

**Critical QSR Requirements:**
- **Design Controls (820.30):** Design planning, inputs, outputs, verification, validation, transfer (Class II/III)
- **Document Controls (820.40):** Approval, distribution, change control, obsolete document management
- **CAPA System (820.100):** Investigation, root cause analysis, corrective action, effectiveness verification
- **Production Controls (820.70):** Work instructions, equipment validation, process validation
- **Management Responsibility (820.20):** Quality policy, organization, management review
- **Complaint Handling (820.198):** Complaint review, investigation, MDR reporting

**Key Documentation:**
- **Device Master Record (DMR):** Manufacturing specifications and procedures
- **Device History Record (DHR):** Batch/lot production records and acceptance
- **Design History File (DHF):** Complete design control documentation

**See:** [QSR Compliance Guide](references/qsr-compliance-guide.md) for detailed requirements and implementation guidance

### 3. FDA Submission Preparation and Management
Lead comprehensive FDA submission preparation ensuring regulatory compliance:

**510(k) Submission Components:**
- Device description and specifications
- Indications for use statement
- Substantial equivalence comparison (predicate analysis)
- Performance testing (bench, biocompatibility, software, human factors)
- Labeling (IFU, device labels)
- Risk analysis (ISO 14971)

**PMA Submission Components:**
- Nonclinical testing (bench, biocompatibility, animal studies)
- Clinical investigation (IDE, clinical trials, GCP compliance)
- Manufacturing information and quality system
- Risk-benefit analysis
- Post-approval study commitments

**Pre-Submission Strategy:**
- Q-Sub meetings with FDA (obtain FDA feedback before submission)
- Submission readiness assessment
- Document checklist and gap analysis
- Timeline planning and resource allocation

**FDA Review Management:**
- FDA communication and correspondence tracking
- Additional information requests (RFI) response
- Review timeline monitoring
- Clearance/approval processing

### 4. HIPAA Compliance and Cybersecurity
Ensure comprehensive HIPAA and FDA cybersecurity compliance for medical devices:

**HIPAA Security Rule (devices handling PHI):**
- **Administrative Safeguards:** Risk analysis, security officer, workforce training, incident response
- **Physical Safeguards:** Facility access, workstation security, device disposal
- **Technical Safeguards:** Access control, audit logging, encryption, authentication
- **Business Associate Agreements:** Required with vendors handling PHI

**FDA Cybersecurity (Premarket):**
- Cybersecurity risk assessment and threat modeling
- Security architecture and controls
- Software Bill of Materials (SBOM)
- Authentication, authorization, encryption
- Security testing (penetration, vulnerability scanning)

**FDA Cybersecurity (Post-Market):**
- Vulnerability monitoring and threat intelligence
- Security updates and patch management
- Coordinated vulnerability disclosure (CVD)
- Incident response and reporting

**See:** [HIPAA and Cybersecurity](references/hipaa-cybersecurity.md) for complete compliance requirements

### 5. FDA Inspection Readiness
Maintain comprehensive FDA inspection readiness:

**Inspection Types:**
- Routine inspection (biennial)
- For-cause inspection (complaint/recall triggered)
- Pre-Approval Inspection (PAI)
- Surveillance inspection

**Inspection Preparation:**
- Internal quality system audit
- CAPA records review
- Complaint file completeness
- DHR/DMR traceability verification
- Mock inspection

**Form FDA 483 Response:**
- Root cause analysis
- Immediate correction
- Corrective action plan
- Effectiveness verification
- Timeline commitment
- Response within 15 business days

### 6. Regulatory Intelligence and Strategy
Monitor FDA guidance, policy changes, and enforcement trends:

**FDA Intelligence:**
- Guidance document monitoring (new and revised)
- Warning letter analysis (industry trends)
- FDA workshops and stakeholder meetings
- Regulatory policy evolution

**Market Access Strategy:**
- Regulatory pathway optimization
- Competitive regulatory intelligence
- Timeline and resource planning
- Commercial-regulatory alignment

## Advanced FDA Applications

### Software as Medical Device (SaMD)
- Software classification and risk categorization
- Software lifecycle documentation
- FDA cybersecurity requirements
- Software change control and FDA notification

### Combination Products
- OPDP (Office of Product Development and Policy) consultation
- Lead center determination (CDER, CDRH, CBER)
- Intercenter coordination
- Product-specific guidance

## Python Tools

### FDA Submission Planner
**Script:** `scripts/fda_submission_planner.py`

Comprehensive FDA submission planning and tracking tool:

**Features:**
- Device classification analysis (Class I/II/III)
- Submission pathway recommendation (510(k)/PMA/De Novo/HDE)
- Document checklist generation with CFR references
- Timeline calculation with milestones
- FDA correspondence tracking templates

**Usage:**
```bash
# Generate sample device file
python scripts/fda_submission_planner.py sample

# Create submission plan (text output)
python scripts/fda_submission_planner.py sample_device_info.json

# JSON output for project management integration
python scripts/fda_submission_planner.py my_device.json --output json --file plan.json

# CSV document checklist
python scripts/fda_submission_planner.py my_device.json -o csv -f checklist.csv

# Verbose mode with detailed CFR references
python scripts/fda_submission_planner.py my_device.json -v
```

**Supported Submission Types:**
- 510(k) Traditional, Special, Abbreviated
- PMA (Premarket Approval)
- De Novo Classification Request
- HDE (Humanitarian Device Exemption)

**Input:** JSON device information file (see `assets/` for samples)

**Output Formats:**
- Text (human-readable with sections)
- JSON (machine-readable for PM tools)
- CSV (document checklist for team distribution)

**Sample Files:** `assets/sample_device_info.json`, `sample_pma_device.json`, `sample_de_novo_device.json`, `sample_hde_device.json`

## Reference Documentation

### FDA Regulatory Guidance
- **[FDA Submission Pathways](references/fda-submission-pathways.md)** - Complete pathway selection framework, requirements, and decision tree
- **[QSR Compliance Guide](references/qsr-compliance-guide.md)** - 21 CFR 820 requirements, inspection readiness, 483 response strategies
- **[HIPAA and Cybersecurity](references/hipaa-cybersecurity.md)** - HIPAA Security Rule, FDA cybersecurity guidance, incident response

### Templates and Assets
- **Sample Device Files:** `assets/` - Pre-configured device information for testing submission planner
- **FDA Templates:** `assets/fda-templates/` - Submission templates and forms (planned)
- **QSR Documentation:** `assets/qsr-documentation/` - QSR compliance templates (planned)
- **HIPAA Tools:** `assets/hipaa-tools/` - HIPAA compliance assessment tools (planned)
- **Inspection Materials:** `assets/inspection-materials/` - FDA inspection preparation (planned)

## Best Practices

**Regulatory Strategy:**
1. Engage FDA early - Use Q-Sub process to obtain FDA feedback
2. Select optimal pathway - Balance time, cost, and competitive advantage
3. Maintain QSR compliance - FDA inspection readiness is continuous
4. Document thoroughly - Clear rationale for all regulatory decisions

**Submission Excellence:**
1. Know your predicate - Thorough predicate analysis prevents substantial equivalence questions
2. Anticipate FDA questions - Address potential concerns proactively in submission
3. Use consensus standards - Abbreviated 510(k) leverages FDA-recognized standards
4. Plan for RFIs - Budget time for additional information requests

**Inspection Readiness:**
1. Conduct regular internal audits - Identify gaps before FDA does
2. Maintain complete records - DHR, DMR, DHF, complaint files current and traceable
3. Train personnel - Everyone should understand FDA inspection protocol
4. Respond professionally - 483 responses should address root cause with objective evidence

**Cybersecurity and HIPAA:**
1. Security by design - Build security controls from device inception
2. Maintain SBOM - Track all software components and vulnerabilities
3. Establish CVD - Coordinated vulnerability disclosure program before launch
4. Monitor continuously - Threat landscape evolves, security must too

---

**Regulatory Framework:** FDA 21 CFR (US), particularly 21 CFR 820 (QSR), 21 CFR 807 (510(k)), 21 CFR 814 (PMA)
**Key Standards:** ISO 13485 (QMS), ISO 14971 (Risk Management), IEC 62304 (Software), ISO 10993 (Biocompatibility)
**Inspection Focus:** Design controls, CAPA system, complaint handling, document control, management responsibility
