---
name: audit.dependencies
description: Check for outdated/vulnerable dependencies across your project with multi-phase analysis
category: audit
subcategory: security
pattern: multi-phase
version: 1.0.0
author: Claude Code
tags: [security, dependencies, audit, vulnerability, maintenance]
example_usage: /audit.dependencies
requires_input: false
requires_context: true
estimated_time: 15m
related_commands: [audit.security]
model_preference: sonnet
tools_required: [Read, Bash, Grep, Glob]
output_format: markdown
interactive: true
dangerous: false
difficulty: beginner
time_saved: 15 minutes per audit
frequency: Weekly
---

# Dependency Audit Command

Systematically discover, analyze, and generate remediation tasks for outdated and vulnerable dependencies in your project.

---

## Pattern Type: Multi-Phase (Discovery → Analysis → Task)

**Complexity:** Medium
**Execution Time:** 15 minutes
**Destructive:** No (read-only analysis)
**Project Type:** All project types (Python, Node.js, Ruby, Go, etc.)

---

## Usage

```bash
/audit.dependencies
```

### Options

- No arguments required
- Will auto-detect project type and dependency files
- Optional: Provide custom project path if not in current working directory

### Examples

```bash
# Run audit on current project
/audit.dependencies

# Audit finds outdated packages, security vulnerabilities, and compatibility issues
# Generates prioritized task list for remediation
```

---

## What This Command Does

### Context Gathering

The command will:
1. Detect all dependency management files (`package.json`, `requirements.txt`, `Gemfile`, `go.mod`, `Cargo.toml`, `pom.xml`, etc.)
2. Identify project type and technology stack
3. Catalog all dependencies with their current versions
4. Check for known security vulnerabilities
5. Identify outdated packages (version lag detection)
6. Analyze transitive/indirect dependencies

### Task Execution

Then it will:
1. **Discovery Phase:** Scan for dependency manifests and parse version information
2. **Analysis Phase:** Cross-reference against vulnerability databases and version registries
3. **Categorization Phase:** Rank findings by severity (critical, high, medium, low)
4. **Task Generation Phase:** Create actionable remediation tasks with priority

### Expected Output

You will receive:
- **Dependency Inventory Report** - Complete catalog of detected dependencies
- **Vulnerability Assessment** - Security issues with CVSS scores and fix availability
- **Outdated Packages Report** - Version lag analysis and update recommendations
- **Remediation Task List** - Prioritized tasks for addressing issues
- **Actionable Recommendations** - Specific guidance for each issue

**Output Location:** Console output with optional file export
**Output Format:** Markdown with structured sections

---

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Comprehensively catalog all dependencies in the project

**Steps:**
1. Scan project root and subdirectories for dependency manifest files
2. Identify package manager type for each manifest (npm, pip, bundler, cargo, go, maven, etc.)
3. Parse dependency specifications and extract package names, current versions, and constraints
4. Catalog direct dependencies and note which have transitive dependencies
5. Identify duplicate packages across different manifests (monorepo detection)

**Detection Strategy:**
- Glob patterns for manifest files: `package.json`, `package-lock.json`, `yarn.lock`, `requirements.txt`, `Pipfile`, `Pipfile.lock`, `pyproject.toml`, `setup.py`, `Gemfile`, `Gemfile.lock`, `go.mod`, `go.sum`, `Cargo.toml`, `Cargo.lock`, `pom.xml`, `build.gradle`
- Parse package specifications to extract names and version constraints
- Separate production dependencies from dev dependencies
- Flag duplicate/redundant packages across manifests

**Tools Used:** Glob (file discovery), Grep (version parsing), Bash (file analysis)

**Output:**
- Structured inventory of all dependencies found
- Package manager type identification
- Total count of direct and transitive dependencies

### Phase 2: Analysis

**Goal:** Assess security posture and update requirements for each dependency

**Steps:**
1. Cross-reference detected packages against known vulnerability databases
2. Check version lag: Compare current versions to latest available versions
3. Analyze dependency constraints: Identify overly restrictive vs. permissive version pinning
4. Detect deprecated/unmaintained packages
5. Assess license compatibility (optional)
6. Identify breaking change risks in available updates

**Analysis Criteria:**

- **Security Vulnerabilities** - Known CVEs affecting current version, CVSS severity score, availability of patches
- **Version Currency** - Current version vs. latest available, major/minor/patch lag, release date of current version
- **Dependency Health** - Package maintenance status, last update date, community activity level
- **Compatibility Risk** - Breaking changes in newer versions, dependency conflicts, transitive issues
- **License Compliance** - License type, compatibility with project license (if applicable)

**Data Sources:**
- npm: npm registry API, GitHub advisory database
- Python: PyPI API, OSV database for CVE information
- Ruby: Ruby gems API, security advisory database
- Go: Go module proxy, CVE databases
- Rust: Crates.io API, rustsec advisory database
- Java/Maven: Maven Central, Sonatype advisories

**Scoring Logic:**
- **Critical (Score 9+):** Known exploitable vulnerabilities with public POCs, CVSS 9.0+, or actively exploited
- **High (7-8.9):** Important vulnerabilities or major version lag (>5 versions behind)
- **Medium (4-6.9):** Moderate vulnerabilities or moderate version lag (2-4 versions behind)
- **Low (0-3.9):** Minor issues or minor version lag (minor updates available)

### Phase 3: Categorization & Prioritization

**Goal:** Organize findings by actionable priority and risk impact

**Steps:**
1. Group findings by severity (critical → high → medium → low)
2. Within each severity level, rank by:
   - Update ease (patch vs. major version)
   - Dependency breadth (how many other packages depend on this)
   - Last maintenance date (stale packages prioritized)
3. Identify quick wins (patch updates with no breaking changes)
4. Flag complex updates (major version changes, transitive conflicts)

**Prioritization Rules:**
- Critical vulnerabilities → Always urgent
- Direct dependencies → Higher priority than transitive
- Widely-used packages → Higher priority (impact scope)
- Long-unmaintained packages → Escalate urgency
- Production dependencies → Higher priority than dev

### Phase 4: Reporting

**Goal:** Present comprehensive findings with actionable next steps

**Report Includes:**

#### Executive Summary
- Total dependencies discovered
- Total vulnerabilities found (by severity)
- Total outdated packages
- Overall security posture score (0-100)
- Key recommendations (top 3 actions)

#### Security Findings Section
- Table of vulnerable packages with:
  - Package name
  - Current version
  - Vulnerability ID (CVE)
  - CVSS score
  - Severity level
  - Available patch/fix version
  - Days since discovery
- Affected components and risk exposure

#### Outdated Packages Section
- Table of packages with updates available:
  - Package name
  - Current version
  - Latest version
  - Version lag (major.minor.patch gaps)
  - Last update date
  - Update type (major/minor/patch)
- Dependencies with long maintenance gaps (>1 year)

#### Dependency Health Section
- Unmaintained/deprecated packages requiring replacement
- Packages with low community activity
- License compatibility issues (if applicable)

#### Transitive Dependency Issues
- Indirect vulnerabilities affecting project
- Indirect outdated packages
- Conflict resolution recommendations

#### Action Items Section (Task-Ready)
Each issue includes:
- **What:** Clear description of the issue
- **Why:** Impact and risk explanation
- **How:** Specific remediation steps
- **Effort:** Estimated update difficulty
- **Risk:** Potential breaking changes or side effects

**Report Location:** Console output with optional markdown file export
**Report Format:** Structured markdown with tables and priority indicators

---

## Implementation Details

### Dependency File Detection Algorithm

```
For each language/package manager:
  - Identify standard manifest files
  - Parse version specifications (exact, ranges, wildcards)
  - Extract direct and transitive dependencies
  - Flag duplicate packages across tools
  - Categorize as production or development
```

### Vulnerability Assessment Process

```
For each discovered package:
  1. Check public vulnerability databases (NVD, GitHub advisories, etc.)
  2. Extract CVE identifiers and CVSS scores
  3. Determine if current version is affected
  4. Identify first patched version
  5. Calculate days since vulnerability disclosure
```

### Version Update Analysis

```
For each package:
  1. Query latest available version
  2. Calculate version lag (major, minor, patch differences)
  3. Check for breaking changes between versions
  4. Identify deprecation warnings
  5. Assess transitive impact of updates
```

---

## Success Criteria

This command is successful when:

- [x] All dependency manifest files are discovered (no false negatives)
- [x] All detected packages are correctly identified with version info
- [x] Vulnerability database lookups complete successfully
- [x] Version lag calculations are accurate
- [x] Issues are correctly prioritized by severity and impact
- [x] Actionable remediation guidance is provided for each issue
- [x] Transitive dependencies are analyzed
- [x] Report is exported to file for team sharing

### Quality Metrics

**Expected Outcomes:**
- **Detection Accuracy:** 95%+ of dependencies correctly identified
- **Vulnerability Coverage:** 90%+ of known vulnerabilities found
- **Update Availability:** Accurate patch/update recommendations
- **Task Clarity:** Each finding has actionable next steps
- **Time to Remediation:** Prioritization enables quick critical fixes

---

## Tips for Best Results

1. **Before Running**
   - Ensure all lock files are committed (for accurate version info)
   - Note any monorepo structure for context
   - Identify high-security environments (finance, healthcare, etc.)

2. **Interpreting Results**
   - Critical/High vulnerabilities require immediate action
   - Batch similar-severity updates to reduce risk
   - Test major version updates in staging first
   - Review changelogs for breaking changes

3. **Post-Audit Actions**
   - Implement recommended updates in priority order
   - Run full test suite after each major update
   - Monitor for regressions in staging/production
   - Schedule regular audits (weekly recommended)

4. **Ongoing Maintenance**
   - Enable dependabot/renovate bots for continuous monitoring
   - Set up security alerting for zero-day disclosures
   - Document internal package standards and constraints
   - Create runbooks for emergency security patches

---

## Related Commands

- `/analysis.security-audit` - Comprehensive security analysis beyond dependencies
- `/git.code-review` - Review security-related code changes
- `/workflow.create-pr` - Create PR for dependency updates

---

## Integration with Skills & Agents

This command works with:

- **Engineering Team Skills** - Dependency management best practices
- **Delivery Team Agents** - Security compliance and audit trails
- **DevOps Workflows** - Automated dependency scanning and patching

---

## Error Handling

### Common Issues

**Issue:** No dependency files found
**Cause:** Project uses indirect dependency management or non-standard locations
**Solution:** Check for dependency files in subdirectories or monorepo roots
**Prevention:** Standardize dependency management file locations

---

**Issue:** Incomplete vulnerability data for private/internal packages
**Cause:** Private packages not in public vulnerability databases
**Solution:** Cross-reference with internal security advisories
**Prevention:** Maintain internal package security documentation

---

**Issue:** Version constraint conflicts prevent updates
**Cause:** Transitive dependencies have incompatible version requirements
**Solution:** Analyze dependency tree to find compatible versions or evaluate alternatives
**Prevention:** Regularly update dependencies before constraints become too tight

---

### Validation Failures

If the command reports errors:

1. **Missing Manifests**
   - Check: Project root contains dependency files
   - Fix: Navigate to project root or specify explicit path

2. **Parse Errors**
   - Check: Manifest files are valid (valid JSON/YAML/TOML)
   - Fix: Validate manifest syntax before audit

3. **Network Errors (if checking databases)**
   - Check: Internet connectivity and proxy settings
   - Fix: Ensure API access to vulnerability databases

---

## Validation Checklist (8 Checks)

All command implementations must pass:

- [x] **Metadata Complete:** All 8 YAML frontmatter fields present (name, description, category, pattern, version, author, tags, model_preference)
- [x] **Naming Convention:** Uses correct format `category.command-name` (analysis.dependency-audit)
- [x] **Pattern Documentation:** Multi-phase pattern fully documented with 4 distinct phases
- [x] **Usage Examples:** Clear examples with expected behavior
- [x] **Execution Steps:** Detailed walkthrough of discovery, analysis, task generation
- [x] **Success Criteria:** Measurable outcomes defined with quality metrics
- [x] **Error Handling:** Common issues documented with solutions
- [x] **Integration Points:** Related commands, skills, agents documented

---

## References

- [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/) - Dependency vulnerability scanner
- [GitHub Security Advisories](https://github.com/advisories) - CVE database
- [National Vulnerability Database](https://nvd.nist.gov/) - Official CVE repository
- [Snyk Vulnerability Database](https://snyk.io/vuln/) - Real-time vulnerability data
- [NIST Software Supply Chain Security](https://csrc.nist.gov/projects/supply-chain-risk-management) - Best practices

---

**Last Updated:** November 24, 2025
**Version:** 1.0.0
**Maintained By:** Claude Code
**Feedback:** Report issues via project repository

