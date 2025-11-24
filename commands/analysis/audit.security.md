---
name: audit.security
title: Security Audit Command
description: OWASP Top 10 scan + secrets detection + vulnerability analysis for code repositories
category: audit
subcategory: security
difficulty: intermediate
time-saved: 30 minutes per audit
frequency: Weekly, before releases
use-cases:
  - Identify OWASP Top 10 vulnerabilities before deployment
  - Detect hardcoded secrets and credentials in codebase
  - Generate compliance audit reports for security reviews
  - Prepare code for production release with security validation
dependencies:
  tools:
    - Read
    - Bash
    - Grep
    - Glob
  scripts:
    - owasp_scanner.py
    - secrets_detector.py
    - vulnerability_analyzer.py
  python-packages: []
related-agents:
  - cs-security-architect
related-skills:
  - security-hardening
  - compliance-framework
related-commands:
  - analysis.code-quality-review
  - analysis.dependency-audit
compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows
examples:
  - title: "Quick Security Scan"
    input: "/audit.security /path/to/project"
    output: "Security Audit Report with findings categorized by severity"
  - title: "OWASP Compliance Check"
    input: "/audit.security /path/to/project --format owasp"
    output: "OWASP Top 10 mapped findings with remediation recommendations"
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0
version: v1.0.0
author: Claude Skills Team
created: 2025-11-24
updated: 2025-11-24
tags:
  - owasp-top-10
  - secrets-detection
  - vulnerability-scanning
  - security-audit
  - compliance
featured: false
verified: true
license: MIT
---

# Security Audit Command

Performs comprehensive security analysis on code repositories with OWASP Top 10 vulnerability scanning, secrets detection, and vulnerability identification. This multi-phase command provides actionable findings with severity levels and remediation recommendations.

---

## Pattern Type: Multi-Phase

**Complexity:** Intermediate
**Execution Time:** 5-10 minutes (depends on codebase size)
**Destructive:** No (read-only analysis)

---

## Usage

```bash
/audit.security [path-to-scan] [options]
```

### Arguments

- `path-to-scan` - Absolute or relative path to the project directory (required)
- `--format` - Output format: `standard`, `owasp`, or `json` (optional, default: standard)
- `--severity` - Minimum severity to report: `low`, `medium`, `high`, `critical` (optional, default: low)
- `--exclude` - Comma-separated patterns to exclude from scan (optional)
- `--report` - Generate detailed HTML report (optional)

### Examples

```bash
# Basic security scan
/audit.security ./src

# OWASP-focused audit
/audit.security ./src --format owasp

# High severity only
/audit.security ./src --severity high

# With exclusions
/audit.security ./src --exclude node_modules,vendor,dist

# Generate HTML report
/audit.security ./src --report security-audit-report.html

# JSON output for CI/CD integration
/audit.security ./src --format json > audit-results.json
```

---

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Gather comprehensive information about security posture and vulnerabilities

**Steps:**

1. Scan directory structure for sensitive files and directories
2. Identify codebase composition (languages, frameworks, dependencies)
3. Locate secrets-prone files (.env, config, credentials patterns)
4. Map authentication and authorization implementations
5. Catalog API endpoints and data handling patterns
6. Identify third-party integrations and external dependencies

**Tools Used:** Glob (directory scanning), Grep (pattern matching), Read (sensitive file analysis)

**Discovery Checklist:**
- [ ] Project structure mapped
- [ ] Sensitive file locations identified
- [ ] Dependencies cataloged
- [ ] Security-relevant code patterns found
- [ ] Configuration files located

### Phase 2: Analysis

**Goal:** Process findings and identify vulnerabilities against OWASP Top 10 and security best practices

**Steps:**

1. Analyze each finding against OWASP Top 10 categories
2. Compare configurations against security best practices
3. Categorize issues by severity and impact
4. Map findings to remediation strategies
5. Calculate security score and compliance metrics
6. Cross-reference with CWE/CVE databases (when applicable)

**Analysis Criteria:**

- **OWASP A01:2021 - Broken Access Control** - Missing or weak access controls, privilege escalation paths
- **OWASP A02:2021 - Cryptographic Failures** - Weak encryption, hardcoded keys, missing HTTPS enforcement
- **OWASP A03:2021 - Injection** - SQL injection, command injection, code injection vulnerabilities
- **OWASP A04:2021 - Insecure Design** - Missing authentication, weak session management
- **OWASP A05:2021 - Security Misconfiguration** - Debug modes enabled, default credentials, exposed configs
- **OWASP A06:2021 - Vulnerable Components** - Outdated dependencies, known vulnerabilities
- **OWASP A07:2021 - Authentication Failures** - Weak password policies, session fixation, credential exposure
- **OWASP A08:2021 - Data Integrity Failures** - Insecure deserialization, CSRF, missing validations
- **OWASP A09:2021 - Logging/Monitoring Failures** - Missing audit logs, insufficient error handling
- **OWASP A10:2021 - SSRF** - Server-side request forgery, unvalidated redirects

**Severity Classification:**

- **CRITICAL** - Immediate exploitability, direct data breach risk, hardcoded secrets
- **HIGH** - Likely exploitable, significant security impact, authentication bypass
- **MEDIUM** - Conditional exploitability, information disclosure, privilege escalation
- **LOW** - Unlikely exploitation, information gathering, defense in depth

### Phase 3: Secrets Detection

**Goal:** Identify and flag hardcoded credentials and sensitive information

**Steps:**

1. Scan for API keys and tokens patterns
2. Detect database connection strings
3. Find hardcoded credentials (passwords, usernames)
4. Identify AWS keys, SSH keys, private certificates
5. Check for personal identifiable information (PII)
6. Flag environment variable leaks

**Patterns Detected:**

- AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
- PRIVATE KEY patterns (RSA, EC, etc.)
- Database URLs with embedded credentials
- API key patterns (GitHub, Stripe, SendGrid, etc.)
- JWT tokens and bearer tokens
- OAuth secrets
- OAuth2 credentials
- .env file contents

### Phase 4: Vulnerability Mapping

**Goal:** Map identified issues to specific code locations and affected components

**Steps:**

1. Locate vulnerable code patterns
2. Identify affected files and line numbers
3. Determine impact scope (single function, module, application-wide)
4. Cross-reference with dependency versions
5. Link to remediation examples

**Output Includes:**

- File path and line number
- Vulnerable code snippet
- OWASP/CWE classification
- Severity level
- Detailed description
- Remediation steps
- Reference links

### Phase 5: Reporting

**Goal:** Present findings and actionable recommendations

**Report Includes:**

- Executive summary with security score (0-100)
- Critical findings requiring immediate action
- Categorized findings by OWASP Top 10
- Detailed issue list with:
  - Location (file, line)
  - Description
  - Severity
  - Remediation steps
  - Reference links
- Statistics and trends
- Coverage metrics
- Compliance alignment (if applicable)
- Next steps and recommendations

**Report Location:** Generated in stdout + optional HTML/JSON file

---

## What This Command Does

### Context Gathering

The command will:

1. Recursively scan the specified directory and subdirectories
2. Identify sensitive files and configuration patterns
3. Parse source code for security-relevant patterns
4. Map authentication/authorization implementations
5. Catalog external dependencies and integrations
6. Analyze error handling and logging approaches

### Task Execution

Then it will:

1. Run OWASP Top 10 vulnerability checks against discovered patterns
2. Execute secrets detection against all source files
3. Validate cryptographic implementations
4. Check access control patterns
5. Verify input validation practices
6. Analyze dependency versions for known vulnerabilities

### Expected Output

You will receive:

- Structured security findings with severity levels
- OWASP Top 10 mapping for each issue
- Remediation recommendations with examples
- Security score (0-100 scale)
- Code locations requiring review
- Optional HTML report with visualizations
- JSON export for CI/CD integration

**Output Location:** Console output + optional file outputs
**Output Format:** Markdown (terminal), HTML (report), JSON (programmatic)

---

## Error Handling

### Common Issues

**Issue:** "Path not found or not accessible"
**Cause:** Invalid path specified or insufficient permissions
**Solution:** Verify path exists and you have read permissions
**Prevention:** Use absolute paths, check directory permissions before running

---

**Issue:** "No vulnerabilities found" (when you expect findings)
**Cause:** Scan patterns may not match your codebase language/framework
**Solution:** Review discovery phase findings, run with --format owasp for detailed output
**Prevention:** Ensure supported language/framework, run manual spot checks

---

**Issue:** "False positive: legitimate secret-like value detected"
**Cause:** Pattern matching detected non-secret that looks like credential
**Solution:** Add to --exclude patterns, review detected value context
**Prevention:** Configure exclusion patterns for test/mock data

---

### Validation Failures

If the command reports validation errors:

1. **Missing Dependencies**
   - Check: Python 3.8+ installed with standard library
   - Fix: Ensure Python environment properly configured

2. **Permission Denied**
   - Check: Read access to target directory
   - Fix: Grant read permissions with chmod, use sudo if necessary

3. **Timeout**
   - Check: Codebase size and complexity
   - Fix: Reduce scope with --exclude patterns

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-security-architect](../../agents/engineering/cs-security-architect.md)** - Provides comprehensive security architecture review using audit findings
- **[cs-devops-engineer](../../agents/engineering/cs-devops-engineer.md)** - Integrates findings into CI/CD security gates
- **[cs-compliance-officer](../../agents/delivery/cs-compliance-officer.md)** - Maps findings to compliance frameworks

### Related Skills

This command leverages:

- **[security-hardening](../../skills/engineering-team/security-hardening/)** - Security best practices and hardening techniques
- **[compliance-framework](../../skills/delivery-team/compliance-framework/)** - Compliance standards and audit frameworks
- **[dependency-management](../../skills/engineering-team/dependency-management/)** - Vulnerability scanning for dependencies

### Python Tools

This command executes:

```bash
# OWASP vulnerability scanning
python skills/engineering-team/security-hardening/scripts/owasp_scanner.py [target-path]

# Secrets detection
python skills/engineering-team/security-hardening/scripts/secrets_detector.py [target-path]

# Vulnerability analysis
python skills/engineering-team/security-hardening/scripts/vulnerability_analyzer.py [target-path]
```

---

## Success Criteria

This command is successful when:

- [ ] All source files scanned without errors (100% coverage)
- [ ] OWASP Top 10 check complete with categorized findings
- [ ] Secrets detection identified all hardcoded credentials
- [ ] Severity classification assigned to each finding
- [ ] Remediation steps provided for each issue
- [ ] Report generated with actionable recommendations
- [ ] Execution completed within acceptable time
- [ ] Zero false negatives for CRITICAL/HIGH severity items

### Quality Metrics

**Expected Outcomes:**

- **Scan Coverage:** 95%+ of source code scanned
- **Finding Accuracy:** 90%+ relevant findings (low false positive rate)
- **Severity Distribution:** Typically 5-10% CRITICAL, 15-25% HIGH, rest MEDIUM/LOW
- **Remediation Clarity:** 100% of findings have actionable next steps

---

## Tips for Best Results

1. **Prepare Baseline**
   - Run initial audit before security improvements
   - Use JSON export to track trends over time
   - Establish baseline metrics for comparison

2. **Integrate into CI/CD**
   - Run on every commit with JSON output
   - Fail builds on CRITICAL findings
   - Generate trend reports for team visibility

3. **Review False Positives**
   - Validate all HIGH and CRITICAL findings manually
   - Update exclusion patterns for legitimate patterns
   - Document exceptions with justification

4. **Remediation Priority**
   - Address CRITICAL findings immediately
   - Schedule HIGH findings for next sprint
   - Batch MEDIUM/LOW fixes for technical debt
   - Track remediation status and verify fixes

5. **Team Communication**
   - Share reports with security team
   - Educate developers on identified patterns
   - Provide remediation examples and references
   - Track metrics for improvement visibility

---

## Related Commands

- `/analysis.code-quality-review` - Comprehensive code quality analysis
- `/analysis.dependency-audit` - Dependency vulnerability scanning
- `/test.security-tests` - Security-focused testing

---

## References

- [OWASP Top 10 2021](https://owasp.org/Top10/) - Official OWASP Top 10 vulnerabilities
- [CWE/CVSS Scoring](https://cwe.mitre.org/) - Common Weakness Enumeration reference
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework) - Security standards
- [SANS Secure Coding](https://www.sans.org/white-papers/) - Secure coding practices

---

**Last Updated:** 2025-11-24
**Version:** v1.0.0
**Maintained By:** Claude Skills Team
**Feedback:** Report issues via GitHub Issues with `[security-audit]` tag
