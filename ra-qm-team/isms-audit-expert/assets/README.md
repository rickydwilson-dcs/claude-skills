# ISMS Audit Expert - Assets

This directory contains templates, sample data, and supporting materials for ISO 27001 ISMS auditing.

## ISO 27001 Gap Analysis Assets

### sample_iso27001_assessment.json

Sample control assessment data file demonstrating the required format for the ISO 27001 gap analyzer tool.

**Contents:**
- 31 sample control assessments covering key controls across all 4 themes
- Realistic maturity levels ranging from 0 (Not Implemented) to 4 (Measured)
- Complete metadata including organization, auditor, and audit date
- Implementation notes and evidence references for each control

**Control Coverage:**
- **Organizational (10 controls)**: Policies, roles, access control, incident management
- **People (5 controls)**: Screening, training, remote working, event reporting
- **Physical (3 controls)**: Perimeters, entry controls, clear desk
- **Technological (13 controls)**: Endpoints, authentication, malware, logging, cryptography, SDLC

**How to Use:**

1. **Copy as template for your assessment:**
   ```bash
   cp sample_iso27001_assessment.json my_org_assessment.json
   ```

2. **Update the metadata section:**
   - organization: Your company name
   - audit_date: Current assessment date
   - auditor: Lead auditor name and credentials
   - scope: Assessment scope description

3. **Assess all 93 Annex A controls:**
   - Set current_maturity (0-5) based on actual implementation
   - Set target_maturity (typically 3-4 for most controls)
   - Mark is_applicable: false for non-applicable controls
   - Add implementation_notes describing current state
   - List evidence documents in the evidence array
   - Assign responsible_person for each control

4. **Run gap analysis:**
   ```bash
   python scripts/iso27001_gap_analyzer.py my_org_assessment.json -v
   ```

**Maturity Level Guidelines:**

- **Level 0 - Not Implemented**: No process or control exists
  - Example: No incident response procedures documented

- **Level 1 - Ad-hoc**: Reactive, informal approach
  - Example: Security handled on case-by-case basis without procedures

- **Level 2 - Defined**: Documented process exists
  - Example: Security policy written but not regularly enforced

- **Level 3 - Consistent**: Process implemented organization-wide
  - Example: Access control consistently applied across all systems

- **Level 4 - Measured**: Process monitored with KPIs
  - Example: Security metrics tracked and reviewed monthly

- **Level 5 - Optimized**: Continuous improvement driven by metrics
  - Example: Automated security improvements based on performance data

**Full ISO 27001:2022 Annex A Control List:**

To create a complete assessment, add entries for all 93 controls:

**Organizational (37 controls):** 5.1-5.37
- Information security policies
- Roles and responsibilities
- Asset management
- Access control
- Supplier relationships
- Incident management
- Business continuity
- Compliance

**People (8 controls):** 6.1-6.8
- Screening
- Terms of employment
- Security awareness and training
- Disciplinary process
- Remote working
- Event reporting

**Physical (14 controls):** 7.1-7.14
- Security perimeters
- Physical entry controls
- Secure areas
- Equipment protection
- Supporting utilities
- Cabling security
- Disposal

**Technological (34 controls):** 8.1-8.34
- Endpoint devices
- Access rights management
- Authentication
- Malware protection
- Vulnerability management
- Configuration management
- Backup and recovery
- Logging and monitoring
- Network security
- Cryptography
- Secure development

**Sample Assessment Represents:**
A typical mid-sized HealthTech company preparing for ISO 27001 certification:
- Basic security foundation in place (Level 2-3 for some controls)
- Significant gaps in incident response and monitoring (Level 0-1)
- Strong physical security (Level 3-4)
- Moderate technical controls (Level 2-3)
- Overall readiness: 6.5% (MODERATE_GAPS status)
- Estimated remediation effort: 39 weeks

## Additional Assets

### isms-audit-templates/
Audit planning, execution, and reporting templates (to be added)

### security-testing-tools/
Security assessment automation scripts (to be added)

### compliance-checklists/
ISO 27001 and regulatory compliance verification checklists (to be added)

### training-materials/
Security auditor training and competency development programs (to be added)

---

**Last Updated:** November 5, 2025
**Maintained By:** ISMS Audit Expert Team
