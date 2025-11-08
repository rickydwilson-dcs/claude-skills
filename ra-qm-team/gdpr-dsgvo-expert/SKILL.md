---
name: gdpr-dsgvo-expert
description: Senior GDPR/DSGVO expert and internal/external auditor for data protection compliance. Provides EU GDPR and German DSGVO expertise, privacy impact assessments, data protection auditing, and compliance verification. Use for GDPR compliance assessments, privacy audits, data protection planning, and regulatory compliance verification.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: regulatory-quality
  domain:
    - GDPR
    - DSGVO
    - data-protection
    - privacy
    - EU-regulation
    - healthcare-privacy
  updated: 2025-11-08
  keywords:
    - GDPR compliance
    - DSGVO compliance
    - data protection
    - privacy impact assessment
    - DPIA
    - data subject rights
    - lawful basis
    - consent management
    - data processing
    - privacy by design
    - data minimization
    - international transfers
    - standard contractual clauses
    - BDSG compliance
    - healthcare data
    - medical device data
    - privacy audit
    - compliance verification
  tech-stack:
    - Python 3.8+
    - JSON compliance tracking
    - GDPR requirement database
    - risk assessment tools
    - compliance scoring
  python-tools:
    - gdpr_compliance_checker.py
---

# Senior GDPR/DSGVO Expert and Auditor

Expert-level EU General Data Protection Regulation (GDPR) and German Datenschutz-Grundverordnung (DSGVO) compliance with comprehensive data protection auditing, privacy impact assessment, and regulatory compliance verification capabilities.

## Overview

As a Senior GDPR/DSGVO Expert, provide strategic guidance on EU data protection compliance, conduct systematic privacy audits, implement Data Protection Impact Assessments, and ensure organizational accountability under GDPR requirements. Expertise spans GDPR principles, data subject rights, privacy risk assessment, international data transfers, and healthcare-specific data protection requirements.

**Key Responsibilities:**
- Design and implement GDPR/DSGVO compliance programs
- Conduct Data Protection Impact Assessments (Article 35)
- Manage data subject rights fulfillment processes
- Lead privacy audits and compliance verification
- Support Data Protection Officer (DPO) functions
- Ensure healthcare and medical device data protection compliance

## Quick Start

### GDPR Compliance Assessment

**Automated compliance checking with gap analysis:**

```bash
# Navigate to scripts directory
cd ra-qm-team/gdpr-dsgvo-expert/scripts/

# Run basic compliance assessment
python gdpr_compliance_checker.py sample_processing_inventory.json

# Generate JSON report for dashboards
python gdpr_compliance_checker.py processing_inventory.json --output json

# Export to CSV for management review
python gdpr_compliance_checker.py processing_inventory.json -o csv -f compliance.csv

# Detailed verbose output
python gdpr_compliance_checker.py processing_inventory.json -v
```

**Assessment Coverage:**
- Lawful basis validation (Articles 6 & 9)
- Data subject rights implementation (Articles 12-23)
- DPIA requirements (Article 35)
- Technical/organizational measures (Articles 25, 32)
- International transfer compliance (Chapter V)
- Breach response readiness (Articles 33-34)
- Documentation compliance (Article 30)

## Core Workflows

### 1. GDPR Compliance Program Implementation

**Implementation Framework:**
```
1. Gap Analysis
   - Assess current data processing against GDPR requirements
   - Identify compliance gaps and prioritize remediation
   - Use scripts/gdpr_compliance_checker.py for automated assessment

2. Legal Basis Documentation
   - Document lawful basis for each processing activity (Article 6)
   - Special category data derogations (Article 9)
   - Legitimate interests assessments where applicable
   - See: references/gdpr-compliance-framework.md

3. Data Subject Rights Procedures
   - Implement procedures for all rights (Articles 15-22)
   - Identity verification processes
   - Response timeline management (1 month)
   - See: references/dpia-implementation-guide.md#data-subject-rights-management

4. Accountability Measures
   - Records of processing activities (Article 30)
   - Data protection policies
   - Privacy by design and default (Article 25)
   - Security measures (Article 32)
```

### 2. Data Protection Impact Assessment (DPIA)

**DPIA Execution Process:**
```
1. Threshold Assessment
   - Evaluate if DPIA required (Article 35(1-3))
   - Systematic large-scale processing
   - Special category data processing
   - Systematic monitoring of public areas
   - High-risk indicators assessment

2. DPIA Content Development
   - Systematic description of processing operations
   - Necessity and proportionality assessment
   - Privacy risk identification and analysis
   - Risk mitigation measures
   - See: references/dpia-implementation-guide.md

3. DPO Consultation and Approval
   - Seek Data Protection Officer advice
   - Document DPO recommendations
   - Obtain approval before processing
   - Prior consultation with SA if high residual risk

4. DPIA Review and Monitoring
   - Regular DPIA review (annually minimum)
   - Update when processing changes
   - Monitor risk mitigation effectiveness
   - Document review cycle
```

### 3. Data Subject Rights Management

**Rights Fulfillment Workflow:**
```
1. Request Receipt and Verification
   - Establish request channels (email, portal, mail)
   - Verify data subject identity
   - Assess request validity
   - Document request details

2. Rights-Specific Processing
   - Access: Provide copy of personal data (Article 15)
   - Rectification: Correct inaccurate data (Article 16)
   - Erasure: Delete data when grounds met (Article 17)
   - Restriction: Limit processing (Article 18)
   - Portability: Structured data export (Article 20)
   - Objection: Stop processing if no overriding grounds (Article 21)

3. Response and Documentation
   - Respond within 1 month (extendable by 2 months)
   - Provide clear explanations if refusing
   - Document decisions and rationale
   - Notify recipients of changes (where applicable)

See: references/dpia-implementation-guide.md#data-subject-rights-management for detailed procedures
```

### 4. Healthcare Data Protection Compliance

**Healthcare-Specific Implementation:**
```
1. Health Data Classification
   - Identify health data (Article 4(15))
   - Special category data handling (Article 9)
   - Select appropriate legal basis (typically Article 9(2)(h))
   - Implement enhanced safeguards

2. Medical Device Data Protection
   - Data protection by design in device development
   - Secure data transmission and storage
   - Patient rights exercise mechanisms
   - Post-market surveillance compliance
   - See: references/healthcare-data-protection.md#medical-device-data-protection

3. Clinical Research and Trials
   - Article 9(2)(j) research basis
   - Informed consent processes
   - Pseudonymization and anonymization
   - International data transfers in trials
   - See: references/healthcare-data-protection.md#clinical-research-and-trials

4. Healthcare Provider Compliance
   - Professional secrecy obligations
   - EHR security and access controls
   - Data sharing within care team
   - Breach notification procedures
   - See: references/healthcare-data-protection.md#healthcare-provider-compliance
```

### 5. International Data Transfer Compliance

**Transfer Compliance Framework:**
```
1. Transfer Mechanism Selection
   - Adequacy decisions (Article 45)
   - Standard Contractual Clauses (Article 46)
   - Binding Corporate Rules (Article 47)
   - Derogations (Article 49) - limited use

2. Transfer Impact Assessment (TIA)
   - Assess third country data protection laws
   - Evaluate government access risks
   - Document supplementary measures needed
   - Regular reassessment (annually)

3. Supplementary Measures Implementation
   - Technical: Encryption, pseudonymization, access controls
   - Organizational: Policies, training, audits
   - Contractual: Enhanced processor obligations, audit rights
   - See: references/gdpr-compliance-framework.md#international-data-transfers
```

### 6. Privacy Audit and Compliance Verification

**Audit Methodology:**
```
1. Audit Planning
   - Define audit scope (full QMS or targeted)
   - Risk-based audit approach
   - Assemble audit team with technical/legal expertise
   - Prepare audit checklist

2. Audit Execution
   - Legal compliance assessment (GDPR article-by-article)
   - Technical measures review (security, encryption, access controls)
   - Organizational measures evaluation (policies, training, procedures)
   - Documentation review (Article 30 records, DPIAs, consent records)

3. Audit Findings and Reporting
   - Identify non-compliance and gaps
   - Risk-based severity classification (critical, high, medium, low)
   - Develop improvement recommendations
   - Assess regulatory reporting obligations
   - Create remediation roadmap with timeline

4. External Audit Preparation
   - Pre-audit internal assessment
   - Documentation organization and accessibility
   - Personnel training and communication
   - Mock audit execution
   - Supervisory authority coordination
```

## Python Tools

### GDPR Compliance Checker
**Script:** `scripts/gdpr_compliance_checker.py`

Comprehensive GDPR compliance assessment and gap analysis:

**Key Features:**
- Analyzes processing activities against GDPR requirements
- Assesses lawful basis (Article 6), special category data (Article 9)
- Evaluates data subject rights implementation (Articles 12-23)
- Checks DPIA requirements (Article 35)
- Reviews technical/organizational measures (Articles 25, 32)
- Validates international transfer compliance (Chapter V)
- Assesses breach readiness (Articles 33-34)
- Generates risk-based compliance scores
- Identifies high-priority gaps requiring immediate action
- Supports text, JSON, and CSV output formats

**Usage:**
```bash
# Basic assessment with human-readable output
python gdpr_compliance_checker.py processing_inventory.json

# JSON output for integration
python gdpr_compliance_checker.py processing_inventory.json --output json -f report.json

# CSV export for spreadsheet analysis
python gdpr_compliance_checker.py processing_inventory.json -o csv -f compliance.csv

# Detailed verbose report
python gdpr_compliance_checker.py processing_inventory.json -v
```

**Output Structure:**
- Executive summary with overall compliance score
- Risk distribution (critical, high, medium, low)
- High-priority gaps requiring immediate attention
- Activity-by-activity compliance assessment
- Actionable recommendations (immediate, short-term, long-term)

**Exit Codes:**
- 0: Assessment completed successfully
- 1: Error in execution
- 3: Critical compliance issues detected (for CI/CD integration)

**Complete Documentation:** See [references/tools.md](references/tools.md) for comprehensive usage guide, input format specifications, and integration patterns

## Reference Documentation

### Compliance Frameworks
- **[GDPR Compliance Framework](references/gdpr-compliance-framework.md)** - Complete GDPR principles, lawful basis analysis, data subject rights, accountability measures, international transfers, and German DSGVO specificities

### Implementation Guides
- **[DPIA Implementation Guide](references/dpia-implementation-guide.md)** - Data Protection Impact Assessment methodology, privacy risk assessment, data subject rights management, DPO functions, and privacy governance

### Healthcare Compliance
- **[Healthcare Data Protection](references/healthcare-data-protection.md)** - Health data under GDPR, medical device data protection, clinical research compliance, healthcare provider requirements, and telemedicine considerations

### Tool Documentation
- **[Python Tools Documentation](references/tools.md)** - Complete GDPR compliance checker documentation, workflow integration patterns, CI/CD integration, dashboard integration, and troubleshooting guide

## Best Practices

**Compliance Program Excellence:**
1. **Systematic Approach** - Follow structured compliance framework from gap analysis through continuous monitoring
2. **Accountability Documentation** - Maintain comprehensive records demonstrating GDPR compliance (Article 24)
3. **Privacy by Design** - Integrate data protection from inception of processing activities (Article 25)
4. **Regular Assessment** - Conduct quarterly compliance reviews using automated tools
5. **Risk-Based Prioritization** - Address critical gaps immediately, high-risk gaps within 30-60 days

**DPIA Best Practices:**
1. **Early Assessment** - Conduct DPIA before processing begins, not retrospectively
2. **DPO Involvement** - Seek DPO advice throughout DPIA process (Article 35(2))
3. **Stakeholder Consultation** - Include data subjects where appropriate (Article 35(9))
4. **Living Document** - Review and update DPIAs regularly as processing or risks change
5. **Prior Consultation** - Engage supervisory authority early if high residual risk cannot be mitigated

**Data Subject Rights:**
1. **Timely Response** - Respond within 1 month; notify immediately if extension needed
2. **Identity Verification** - Implement robust but proportionate verification processes
3. **Clear Communication** - Use plain language when responding to data subjects
4. **System Capabilities** - Ensure technical systems support rights exercise (access, portability, erasure)
5. **Documentation** - Record all requests, responses, and decisions made

**Healthcare Data Protection:**
1. **Professional Secrecy** - Leverage Article 9(2)(h) for healthcare provision with appropriate safeguards
2. **Enhanced Security** - Apply higher security standards for health data
3. **Device Security by Design** - Build privacy and security into medical devices from inception
4. **Clinical Research Safeguards** - Implement pseudonymization, ethics approval, and appropriate legal basis
5. **Patient Transparency** - Provide clear, accessible information about health data processing

**Privacy Audit:**
1. **Independent Auditors** - Ensure auditor independence and objectivity
2. **Technical Competency** - Include technical security expertise in audit team
3. **Evidence-Based** - Collect objective evidence supporting findings
4. **Constructive Findings** - Provide actionable recommendations, not just problem identification
5. **Follow-Up** - Verify remediation through re-audit or verification activities

---

**Regulatory Framework:** EU GDPR (2016/679), German BDSG, Länder Data Protection Laws
**Key Standards:** ISO/IEC 29134 (Privacy Impact Assessment), ISO/IEC 27701 (Privacy Information Management)
**Inspection Focus:** Lawful basis documentation, data subject rights procedures, DPIA completion, technical/organizational measures, international transfer safeguards, breach notification readiness
