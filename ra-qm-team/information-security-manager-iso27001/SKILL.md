---
name: information-security-manager-iso27001
description: Senior Information Security Manager specializing in ISO 27001 and ISO 27002 implementation for HealthTech and MedTech companies. Provides ISMS implementation, cybersecurity risk assessment, security controls management, and compliance oversight. Use for ISMS design, security risk assessments, control implementation, and ISO 27001 certification activities.
---

# Senior Information Security Manager - ISO 27001/27002 Specialist

Expert-level Information Security Management System (ISMS) implementation and cybersecurity governance with comprehensive knowledge of ISO 27001, ISO 27002, and healthcare-specific security requirements.

## Quick Start: ISO 27001:2022 Compliance Assessment

**NEW: Production-ready ISMS Compliance Checker**

Assess your organization's ISO 27001:2022 compliance with automated gap analysis and remediation roadmap:

```bash
# Run compliance assessment
cd ra-qm-team/information-security-manager-iso27001/scripts/
python3 isms_compliance_checker.py sample_iso27001_assessment.json

# Generate JSON report for dashboards
python3 isms_compliance_checker.py assessment.json -o json -f report.json

# Export to CSV for spreadsheet analysis
python3 isms_compliance_checker.py assessment.json -o csv -f compliance.csv
```

**Key Features:**
- Evaluates all 93 ISO 27001:2022 Annex A controls
- Calculates compliance percentage by theme (Organizational, People, Physical, Technological)
- Identifies critical gaps with prioritized remediation roadmap
- Provides maturity level assessment (Initial → Optimized)
- Assesses security risk exposure
- Supports text, JSON, and CSV output formats

See detailed documentation in [Resources section](#scriptsisms_compliance_checkerpy) below.

## Core ISMS Competencies

### 1. ISO 27001 ISMS Implementation
Design and implement comprehensive Information Security Management Systems aligned with ISO 27001:2022 and healthcare regulatory requirements.

**ISMS Implementation Framework:**
```
ISO 27001 ISMS IMPLEMENTATION
├── ISMS Planning and Design
│   ├── Information security policy development
│   ├── Scope and boundaries definition
│   ├── Risk assessment methodology
│   └── Security objectives establishment
├── Security Risk Management
│   ├── Asset identification and classification
│   ├── Threat and vulnerability assessment
│   ├── Risk analysis and evaluation
│   └── Risk treatment planning
├── Security Controls Implementation
│   ├── ISO 27002 controls selection
│   ├── Technical controls deployment
│   ├── Administrative controls establishment
│   └── Physical controls implementation
└── ISMS Operation and Monitoring
    ├── Security incident management
    ├── Performance monitoring
    ├── Management review
    └── Continuous improvement
```

### 2. Information Security Risk Assessment (ISO 27001 Clause 6.1.2)
Conduct systematic information security risk assessments ensuring comprehensive threat identification and risk treatment.

**Risk Assessment Methodology:**
1. **Asset Identification and Classification**
   - Information assets inventory and valuation
   - System and infrastructure asset mapping
   - Data classification and handling requirements
   - **Decision Point**: Determine asset criticality and protection requirements

2. **Threat and Vulnerability Analysis**
   - **For Healthcare Data**: Follow references/healthcare-threat-modeling.md
   - **For Medical Devices**: Follow references/device-security-assessment.md
   - **For Cloud Services**: Follow references/cloud-security-evaluation.md
   - Threat landscape analysis and modeling

3. **Risk Analysis and Evaluation**
   - Risk likelihood and impact assessment
   - Risk level determination and prioritization
   - Risk acceptability evaluation
   - Risk treatment option analysis

### 3. ISO 27002 Security Controls Implementation
Implement comprehensive security controls framework ensuring systematic information security protection.

**Security Controls Categories:**
```
ISO 27002:2022 CONTROLS FRAMEWORK
├── Organizational Controls (5.1-5.37)
│   ├── Information security policies
│   ├── Organization of information security
│   ├── Human resource security
│   └── Supplier relationship security
├── People Controls (6.1-6.8)
│   ├── Screening and terms of employment
│   ├── Information security awareness
│   ├── Disciplinary processes
│   └── Remote working guidelines
├── Physical Controls (7.1-7.14)
│   ├── Physical security perimeters
│   ├── Equipment protection
│   ├── Secure disposal and reuse
│   └── Clear desk and screen policies
└── Technological Controls (8.1-8.34)
    ├── Access control management
    ├── Cryptography and key management
    ├── Systems security
    ├── Network security controls
    ├── Application security
    ├── Secure development
    └── Supplier relationship security
```

### 4. Healthcare-Specific Security Requirements
Implement security measures addressing unique healthcare and medical device requirements.

**Healthcare Security Framework:**
- **HIPAA Technical Safeguards**: Access control, audit controls, integrity, transmission security
- **Medical Device Cybersecurity**: FDA cybersecurity guidance and IEC 62304 integration
- **Clinical Data Protection**: Clinical trial data security and patient privacy
- **Interoperability Security**: HL7 FHIR and healthcare standard security

## Advanced Information Security Applications

### Medical Device Cybersecurity Management
Implement comprehensive cybersecurity measures for connected medical devices and IoT healthcare systems.

**Device Cybersecurity Framework:**
1. **Device Security Assessment**
   - Security architecture review and validation
   - Vulnerability assessment and penetration testing
   - Threat modeling and attack surface analysis
   - **Decision Point**: Determine device security classification and controls

2. **Security Controls Implementation**
   - **Device Authentication**: Multi-factor authentication and device identity
   - **Data Protection**: Encryption at rest and in transit
   - **Network Security**: Segmentation and monitoring
   - **Update Management**: Secure software update mechanisms

3. **Security Monitoring and Response**
   - Security event monitoring and SIEM integration
   - Incident response and forensic capabilities
   - Threat intelligence and vulnerability management
   - Security awareness and training programs

### Cloud Security Management
Ensure comprehensive security for cloud-based healthcare systems and SaaS applications.

**Cloud Security Strategy:**
- **Cloud Security Assessment**: Cloud service provider evaluation and due diligence
- **Data Residency and Sovereignty**: Regulatory compliance and data location requirements
- **Shared Responsibility Model**: Cloud provider and customer security responsibilities
- **Cloud Access Security**: Identity and access management for cloud services

### Privacy and Data Protection Integration
Integrate information security with privacy and data protection requirements ensuring comprehensive data governance.

**Privacy-Security Integration:**
- **Privacy by Design**: Security controls supporting privacy requirements
- **Data Minimization**: Security measures for data collection and retention limits
- **Data Subject Rights**: Technical measures supporting privacy rights exercise
- **Cross-Border Data Transfer**: Security controls for international data transfers

## ISMS Governance and Operations

### Information Security Policy Framework
Establish comprehensive information security policies ensuring organizational security governance.

**Policy Framework Structure:**
- **Information Security Policy**: Top-level security commitment and direction
- **Acceptable Use Policy**: System and data usage guidelines
- **Access Control Policy**: User access and privilege management
- **Incident Response Policy**: Security incident handling procedures
- **Business Continuity Policy**: Security aspects of continuity planning

### Security Awareness and Training Program
Develop and maintain comprehensive security awareness programs ensuring organizational security culture.

**Training Program Components:**
- **General Security Awareness**: All-staff security training and awareness
- **Role-Based Security Training**: Specialized training for specific roles
- **Incident Response Training**: Security incident handling and escalation
- **Regular Security Updates**: Ongoing security communication and updates

### Security Incident Management (ISO 27001 Clause 8.2.3)
Implement robust security incident management processes ensuring effective incident response and recovery.

**Incident Management Process:**
1. **Incident Detection and Reporting**
2. **Incident Classification and Prioritization**
3. **Incident Investigation and Analysis**
4. **Incident Response and Containment**
5. **Recovery and Post-Incident Activities**
6. **Lessons Learned and Improvement**

## ISMS Performance and Compliance

### Security Metrics and KPIs
Monitor comprehensive security performance indicators ensuring ISMS effectiveness and continuous improvement.

**Security Performance Dashboard:**
- **Security Control Effectiveness**: Control implementation and performance metrics
- **Incident Management Performance**: Response times, resolution rates, impact assessment
- **Compliance Status**: Regulatory and standard compliance verification
- **Risk Management Effectiveness**: Risk treatment success and residual risk levels
- **Security Awareness Metrics**: Training completion, phishing simulation results

### Internal Security Auditing
Conduct systematic internal security audits ensuring ISMS compliance and effectiveness.

**Security Audit Program:**
- **Risk-Based Audit Planning**: Audit scope and frequency based on risk assessment
- **Technical Security Testing**: Vulnerability assessments and penetration testing
- **Compliance Auditing**: ISO 27001 and regulatory requirement verification
- **Process Auditing**: ISMS process effectiveness evaluation

### Management Review and Continuous Improvement
Lead management review processes ensuring systematic ISMS evaluation and strategic security planning.

**Management Review Framework:**
- **Security Performance Review**: Metrics analysis and trend identification
- **Risk Assessment Updates**: Risk landscape changes and impact evaluation
- **Compliance Status Review**: Regulatory and certification compliance assessment
- **Security Investment Planning**: Security technology and resource allocation
- **Strategic Security Planning**: Security strategy alignment with business objectives

## Regulatory and Certification Management

### ISO 27001 Certification Management
Oversee ISO 27001 certification processes ensuring successful certification and maintenance.

**Certification Management:**
- **Pre-certification Readiness**: Gap analysis and remediation planning
- **Certification Audit Management**: Stage 1 and Stage 2 audit coordination
- **Surveillance Audit Preparation**: Ongoing compliance and improvement demonstration
- **Certification Maintenance**: Certificate renewal and scope management

### Regulatory Security Compliance
Ensure comprehensive compliance with healthcare security regulations and standards.

**Regulatory Compliance Framework:**
- **HIPAA Security Rule**: Technical, administrative, and physical safeguards
- **GDPR Security Requirements**: Technical and organizational measures
- **FDA Cybersecurity Guidance**: Medical device cybersecurity compliance
- **NIST Cybersecurity Framework**: Cybersecurity risk management integration

## Resources

### scripts/
- `isms_compliance_checker.py`: ISO 27001:2022 Annex A controls compliance assessment and gap analysis
- `isms-performance-dashboard.py`: Comprehensive ISMS metrics monitoring and reporting (planned)
- `security-risk-assessment.py`: Automated security risk assessment and documentation (planned)
- `compliance-monitoring.py`: Regulatory and standard compliance tracking (planned)
- `incident-response-automation.py`: Security incident workflow automation (planned)

### references/
- `iso27001-implementation-guide.md`: Complete ISO 27001 ISMS implementation framework
- `iso27002-controls-library.md`: Comprehensive security controls implementation guidance
- `healthcare-threat-modeling.md`: Healthcare-specific threat assessment methodologies
- `device-security-assessment.md`: Medical device cybersecurity evaluation frameworks
- `cloud-security-evaluation.md`: Cloud service security assessment criteria

### scripts/isms_compliance_checker.py

**Production-Ready ISO 27001:2022 Compliance Assessment Tool**

Comprehensive security controls compliance checker supporting all 93 ISO 27001:2022 Annex A controls across four control themes.

**Features:**
- **Complete Control Coverage**: Assesses all 93 Annex A controls (37 Organizational, 8 People, 14 Physical, 34 Technological)
- **Compliance Calculation**: Theme-based and overall compliance percentage with maturity level assessment
- **Control Effectiveness Rating**: Tracks implementation status and operational effectiveness
- **Gap Analysis**: Identifies critical security control gaps requiring immediate attention
- **Risk Assessment**: Calculates security risk exposure based on control implementation status
- **Remediation Roadmap**: Generates prioritized remediation plan (immediate, short-term, medium-term, long-term)
- **Multiple Output Formats**: Text, JSON, and CSV reports for different stakeholders

**Usage:**
```bash
# Basic compliance assessment
python isms_compliance_checker.py sample_iso27001_assessment.json

# JSON output for integration
python isms_compliance_checker.py assessment.json --output json

# CSV export for spreadsheet analysis
python isms_compliance_checker.py assessment.json -o csv -f compliance_report.csv

# Detailed verbose report
python isms_compliance_checker.py assessment.json -v

# Save to file
python isms_compliance_checker.py assessment.json -f compliance_report.txt
```

**Input Format:**
JSON file with ISO 27001 assessment data including:
- Metadata (organization, scope, assessment date)
- Controls array with:
  - Control ID (e.g., "5.1", "8.24")
  - Control name (ISO 27001:2022 Annex A control title)
  - Theme (ORGANIZATIONAL, PEOPLE, PHYSICAL, TECHNOLOGICAL)
  - Status (IMPLEMENTED, PARTIALLY_IMPLEMENTED, NOT_IMPLEMENTED, NOT_APPLICABLE, PLANNED)
  - Effectiveness rating (EFFECTIVE, PARTIALLY_EFFECTIVE, INEFFECTIVE, NOT_TESTED)
  - Evidence of implementation
  - Identified gaps
  - Remediation plan and priority
  - Target completion date
  - Responsible person

**Sample Input:**
See `scripts/sample_iso27001_assessment.json` for complete example with 35 representative controls across all themes.

**Output Reports:**

*Text Format (Default):*
- Executive summary with overall compliance percentage and maturity level
- Compliance by control theme (Organizational, People, Physical, Technological)
- Critical gaps identified with priority levels
- Remediation roadmap with phased implementation plan
- Security risk assessment with risk level and score
- Key recommendations for improving security posture
- Detailed control assessment (verbose mode)

*JSON Format:*
- Metadata with tool version and assessment details
- Executive summary with compliance and risk metrics
- Theme-by-theme compliance breakdown
- Remediation roadmap with control counts per phase
- Detailed control data and gap analysis (verbose mode)

*CSV Format:*
- Tabular export for spreadsheet analysis
- One row per control with status, effectiveness, gaps, and priorities
- Suitable for pivot tables and compliance tracking

**Compliance Maturity Levels:**
- **OPTIMIZED** (≥95%): World-class security posture, continuous improvement
- **MANAGED** (85-94%): Strong controls, systematic monitoring
- **DEFINED** (70-84%): Standard processes, documented controls
- **DEVELOPING** (50-69%): Basic controls, significant gaps remain
- **INITIAL** (<50%): Ad-hoc security, major compliance work required

**Risk Assessment:**
- **CRITICAL**: >10 critical gaps or >20 high priority gaps
- **HIGH**: 6-10 critical gaps or 11-20 high priority gaps
- **MEDIUM**: 1-5 critical gaps or 6-10 high priority gaps
- **LOW**: Minimal critical/high priority gaps

**Remediation Priorities:**
- **CRITICAL**: Immediate action required, significant security risk
- **HIGH**: Short-term (0-3 months), important security improvement
- **MEDIUM**: Medium-term (3-6 months), standard security enhancement
- **LOW**: Long-term (6-12 months), incremental improvement

**ISO 27001:2022 Control Themes:**

*Organizational Controls (5.1-5.37): 37 controls*
- Information security policies and governance
- Organization of information security
- Human resource security
- Asset management
- Access control policies
- Supplier relationships

*People Controls (6.1-6.8): 8 controls*
- Screening and employment terms
- Security awareness and training
- Disciplinary processes
- Remote working security

*Physical Controls (7.1-7.14): 14 controls*
- Physical security perimeters
- Equipment protection and siting
- Storage media security
- Secure disposal

*Technological Controls (8.1-8.34): 34 controls*
- Access control implementation
- Cryptography
- Network security
- Application security
- Secure development
- System monitoring

**Use Cases:**
1. **Pre-Certification Assessment**: Identify gaps before ISO 27001 certification audit
2. **Surveillance Audit Preparation**: Demonstrate ongoing compliance for surveillance audits
3. **Management Review**: Provide ISMS performance data for management review meetings
4. **Risk Treatment Planning**: Prioritize security investments based on compliance gaps
5. **Security Dashboard**: Generate regular compliance status reports for stakeholders
6. **Gap Analysis**: Compare current state against ISO 27001:2022 requirements
7. **Remediation Tracking**: Monitor progress of security control implementation projects

**Integration:**
- Export JSON for security dashboards and GRC platforms
- CSV export for executive reporting and compliance tracking
- Automated compliance monitoring in CI/CD pipelines
- Regular assessment scheduling for continuous compliance

**Example Workflow:**

1. **Prepare Assessment Data**:
   - Conduct control-by-control implementation review
   - Document evidence and gaps for each control
   - Assign remediation priorities based on risk

2. **Run Compliance Check**:
   ```bash
   python isms_compliance_checker.py current_assessment.json -o json -f report.json
   ```

3. **Review Results**:
   - Analyze overall compliance percentage and maturity level
   - Identify critical gaps requiring immediate attention
   - Review remediation roadmap for resource planning

4. **Plan Remediation**:
   - Prioritize immediate actions (critical priority controls)
   - Allocate budget for short-term and medium-term improvements
   - Assign ownership for each remediation task

5. **Track Progress**:
   - Update assessment data as controls are implemented
   - Re-run checker monthly to monitor improvement
   - Generate trend reports for management

### assets/
- `isms-templates/`: Information security policy, procedure, and documentation templates (planned)
- `risk-assessment-tools/`: Security risk assessment worksheets and calculation tools (planned)
- `audit-checklists/`: ISO 27001 and security compliance audit checklists (planned)
- `training-materials/`: Information security awareness and training programs (planned)
