---
name: senior-secops
description: Comprehensive SecOps skill for application security, vulnerability management, compliance, and secure development practices. Includes security scanning, vulnerability assessment, compliance checking, and security automation. Use when implementing security controls, conducting security audits, responding to vulnerabilities, or ensuring compliance requirements.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: Engineering
  domain: engineering
  updated: 2025-11-23
  keywords:
  - engineering
  - senior
  - secops
  tech-stack:
  - Python 3.8+
  - Markdown
  python-tools:
  - compliance_checker.py
  - security_scanner.py
  - vulnerability_assessor.py
---


license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: engineering
  domain: security-operations
  updated: 2025-11-08
  keywords:
    - security operations
    - vulnerability management
    - security scanning
    - compliance
    - application security
    - threat assessment
    - security controls
    - incident response
    - SIEM
    - log analysis
    - security automation
    - patch management
    - security audits
    - vulnerability remediation
    - access control
  tech-stack:
    - Python
    - OWASP tools
    - Snyk
    - SonarQube
    - GitHub Security
    - Docker
    - Kubernetes
    - AWS Security
    - Prometheus
  python-tools:
    - security_scanner.py
    - vulnerability_assessor.py
    - compliance_checker.py

# Senior SecOps

Complete toolkit for senior SecOps engineers with comprehensive security operations, vulnerability management, and compliance frameworks.

## Overview

The Senior SecOps skill provides enterprise-grade security operations frameworks, vulnerability management tools, and compliance automation for modern cloud infrastructure. This skill covers security scanning, vulnerability assessment, compliance checking, incident response, and security automation used by leading security teams.

Designed for senior security operations engineers, this skill includes proven patterns for application security, infrastructure security, cloud security (AWS/GCP/Azure), and compliance frameworks (SOC 2, ISO 27001, GDPR). All content focuses on production security with defense-in-depth strategies.

**Core Value:** Build automated security operations that detect 95%+ of vulnerabilities before exploitation while maintaining compliance and enabling rapid incident response.

## Quick Start

### Main Capabilities

This skill provides three core capabilities through automated scripts:

```bash
# Script 1: Security Scanner
python scripts/security_scanner.py [options]

# Script 2: Vulnerability Assessor
python scripts/vulnerability_assessor.py [options]

# Script 3: Compliance Checker
python scripts/compliance_checker.py [options]
```

## Core Capabilities

### 1. Security Scanner

Automated tool for security scanner tasks.

**Features:**
- Automated scaffolding
- Best practices built-in
- Configurable templates
- Quality checks

**Usage:**
```bash
python scripts/security_scanner.py <project-path> [options]
```

### 2. Vulnerability Assessor

Comprehensive analysis and optimization tool.

**Features:**
- Deep analysis
- Performance metrics
- Recommendations
- Automated fixes

**Usage:**
```bash
python scripts/vulnerability_assessor.py <target-path> [--verbose]
```

### 3. Compliance Checker

Advanced tooling for specialized tasks.

**Features:**
- Expert-level automation
- Custom configurations
- Integration ready
- Production-grade output

**Usage:**
```bash
python scripts/compliance_checker.py [arguments] [options]
```

## Key Workflows

### 1. Perform Security Scan and Vulnerability Assessment

**Time:** 3-4 hours

1. **Scope Security Scan** - Define what to scan (application, infrastructure, dependencies)
2. **Run Security Scanner** - Execute security_scanner.py across codebase and infrastructure
3. **Analyze Vulnerabilities** - Review findings with vulnerability_assessor.py
4. **Prioritize Remediation** - Focus on critical and high-severity issues
5. **Track Resolution** - Monitor vulnerability lifecycle to closure

**Expected Output:** Prioritized vulnerability list with remediation plan and timeline

### 2. Ensure Compliance Requirements

**Time:** 1-2 days

1. **Identify Compliance Standards** - Determine applicable frameworks (SOC 2, ISO 27001, GDPR)
2. **Run Compliance Checker** - Execute compliance_checker.py for automated checks
3. **Review Gaps** - Identify missing controls and documentation
4. **Implement Remediations** - Address compliance gaps systematically
5. **Document Evidence** - Collect artifacts for audit readiness

**Expected Output:** Compliance status report with gap remediation plan

### 3. Respond to Security Incident

**Time:** Variable (1-24 hours depending on severity)

1. **Detect and Triage** - Identify incident severity and scope
2. **Contain Threat** - Isolate affected systems and prevent spread
3. **Investigate Root Cause** - Analyze logs, vulnerabilities, and attack vectors
4. **Remediate Vulnerability** - Patch systems and close security gaps
5. **Document and Learn** - Create incident report and improve defenses

**Expected Output:** Resolved incident with root cause analysis and prevention measures

## Python Tools

### security_scanner.py

Scans applications and infrastructure for security vulnerabilities with OWASP Top 10 coverage and custom rule support.

**Key Features:**
- OWASP Top 10 vulnerability detection
- Dependency vulnerability scanning (npm audit, pip-audit integration)
- Infrastructure misconfiguration detection
- Secret scanning (API keys, credentials, tokens)
- SAST (Static Application Security Testing) capabilities
- Custom security rule definition
- CI/CD pipeline integration

**Common Usage:**
```bash
# Scan application codebase
python scripts/security_scanner.py /path/to/project

# Scan with specific rules
python scripts/security_scanner.py /path/to/project --rules owasp,secrets

# JSON output for automation
python scripts/security_scanner.py /path/to/project --output json

# Help
python scripts/security_scanner.py --help
```

**Use Cases:**
- Pre-deployment security checks in CI/CD
- Quarterly security assessments
- Onboarding new applications to security program
- Detecting hardcoded secrets before commit

### vulnerability_assessor.py

Assesses and prioritizes vulnerabilities with CVSS scoring, exploitability analysis, and remediation guidance.

**Key Features:**
- CVSS v3.1 scoring and classification
- Exploitability assessment (known exploits, public PoCs)
- Business impact analysis
- Remediation effort estimation
- False positive filtering
- Vulnerability lifecycle tracking
- Integration with vulnerability databases (CVE, NVD)

**Common Usage:**
```bash
# Assess vulnerabilities from scan results
python scripts/vulnerability_assessor.py scan_results.json

# Prioritize by CVSS and exploitability
python scripts/vulnerability_assessor.py scan_results.json --prioritize

# Generate executive report
python scripts/vulnerability_assessor.py scan_results.json --report executive

# Help
python scripts/vulnerability_assessor.py --help
```

**Use Cases:**
- Prioritizing vulnerability remediation efforts
- Executive reporting on security posture
- Tracking vulnerability SLA compliance
- Evaluating security program effectiveness

### compliance_checker.py

Automates compliance checking for SOC 2, ISO 27001, GDPR, and other frameworks with control mapping and evidence collection.

**Key Features:**
- Multi-framework support (SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS)
- Automated control checks
- Evidence collection and documentation
- Gap analysis and remediation tracking
- Audit readiness assessment
- Continuous compliance monitoring
- Custom control framework support

**Common Usage:**
```bash
# Check SOC 2 compliance
python scripts/compliance_checker.py --framework soc2

# Check multiple frameworks
python scripts/compliance_checker.py --frameworks soc2,iso27001,gdpr

# Generate audit report
python scripts/compliance_checker.py --framework soc2 --report audit

# Help
python scripts/compliance_checker.py --help
```

**Use Cases:**
- Pre-audit compliance assessments
- Continuous compliance monitoring
- Onboarding to new compliance frameworks
- Executive reporting on compliance status

## Reference Documentation

### Security Standards

Comprehensive guide available in `references/security_standards.md`:

- Detailed patterns and practices
- Code examples
- Best practices
- Anti-patterns to avoid
- Real-world scenarios

### Vulnerability Management Guide

Complete workflow documentation in `references/vulnerability_management_guide.md`:

- Step-by-step processes
- Optimization strategies
- Tool integrations
- Performance tuning
- Troubleshooting guide

### Compliance Requirements

Technical reference guide in `references/compliance_requirements.md`:

- Technology stack details
- Configuration examples
- Integration patterns
- Security considerations
- Scalability guidelines

## Tech Stack

**Languages:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Database:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI
**Cloud:** AWS, GCP, Azure

## Development Workflow

### 1. Setup and Configuration

```bash
# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### 2. Run Quality Checks

```bash
# Use the analyzer script
python scripts/vulnerability_assessor.py .

# Review recommendations
# Apply fixes
```

### 3. Implement Best Practices

Follow the patterns and practices documented in:
- `references/security_standards.md`
- `references/vulnerability_management_guide.md`
- `references/compliance_requirements.md`

## Best Practices Summary

### Code Quality
- Follow established patterns
- Write comprehensive tests
- Document decisions
- Review regularly

### Performance
- Measure before optimizing
- Use appropriate caching
- Optimize critical paths
- Monitor in production

### Security
- Validate all inputs
- Use parameterized queries
- Implement proper authentication
- Keep dependencies updated

### Maintainability
- Write clear code
- Use consistent naming
- Add helpful comments
- Keep it simple

## Common Commands

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/vulnerability_assessor.py .
python scripts/compliance_checker.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Common Issues

Check the comprehensive troubleshooting section in `references/compliance_requirements.md`.

### Getting Help

- Review reference documentation
- Check script output messages
- Consult tech stack documentation
- Review error logs

## Resources

- Pattern Reference: `references/security_standards.md`
- Workflow Guide: `references/vulnerability_management_guide.md`
- Technical Guide: `references/compliance_requirements.md`
- Tool Scripts: `scripts/` directory
