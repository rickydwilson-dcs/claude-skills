---
# === CORE IDENTITY ===
name: review.code
title: Comprehensive Code Review with Quality Analysis
description: Analyze code for quality, security, and performance issues with detailed findings and actionable recommendations for improvement

category: review
subcategory: code-quality

# === WEBSITE DISPLAY ===
difficulty: intermediate
# Requires understanding of code architecture and quality metrics

time-saved: "20 minutes per PR"
# Typical manual code review takes 30-40 minutes, this saves 20 minutes by automating analysis

frequency: "Daily per development team"
# Most teams review PRs multiple times per day

use-cases:
  - "Reviewing pull requests before merging with automated quality and security checks"
  - "Analyzing new code for performance bottlenecks, architectural issues, and best practice violations"
  - "Identifying security vulnerabilities, input validation gaps, and potential memory leaks"
  - "Generating review reports with specific line numbers and remediation recommendations"

# === RELATIONSHIPS (Cross-linking) ===
related-agents:
  - cs-code-reviewer
  - cs-engineering-lead
  - cs-security-analyst

related-skills:
  - engineering-team/code-quality-analyzer
  - engineering-team/security-scanner
  - engineering-team/performance-analyzer

related-commands:
  - /security.scan-secrets
  - /test.coverage-report
  - /git.create-pr

# === TECHNICAL ===
dependencies:
  tools:
    - Read
    - Write
    - Bash
    - Grep
    - Glob

  scripts:
    - engineering-team/code-quality-analyzer/scripts/quality_analyzer.py
    - engineering-team/security-scanner/scripts/security_checker.py
    - engineering-team/performance-analyzer/scripts/performance_profiler.py

  python-packages: []
  # Standard library only - maximum portability

compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows

# === EXAMPLES (Min 2, Max 5) ===
examples:
  - title: "Basic Code Review of Single File"
    input: "/code-review src/handlers/user.js"
    output: |
      Code Review Report: src/handlers/user.js

      QUALITY SCORE: 7.2/10 (Good)

      CRITICAL ISSUES (2):
      ✗ Line 45: Unvalidated user input in database query
        Risk: SQL injection vulnerability
        Recommendation: Use parameterized queries or ORM
        Severity: HIGH

      ✗ Line 67: Hardcoded API secret in code
        Risk: Credential exposure
        Recommendation: Move to environment variables
        Severity: CRITICAL

      WARNINGS (4):
      ⚠ Line 12: Complex function (cyclomatic complexity: 8)
        Recommendation: Break into smaller functions

      ⚠ Line 89: Unhandled promise rejection
        Risk: Silent failures in production
        Recommendation: Add .catch() handler

      ⚠ Line 103: Inefficient loop (O(n²) complexity)
        Recommendation: Use Set for lookups instead of array.includes()

      ⚠ Line 156: Missing error handling for file operations
        Recommendation: Add try-catch or Promise.catch()

      IMPROVEMENTS (3):
      ✓ Consider: Add input validation schema using Joi or Zod
      ✓ Consider: Extract database logic to separate data access layer
      ✓ Consider: Add comprehensive error logging

      FILES ANALYZED: 1
      LINES OF CODE: 234
      EXECUTION TIME: 2.3s

  - title: "Full PR Review with Portfolio Analysis"
    input: "/code-review --pr #1234 --include-security --include-performance"
    output: |
      Code Review Report: PR #1234 - Add User Dashboard

      FILES ANALYZED: 12
      TOTAL LINES: 2,847
      CHANGES: +1,240 -340 ~1,267 modified

      ═════════════════════════════════════════════════
      OVERALL QUALITY SCORE: 8.1/10 (Good)
      ═════════════════════════════════════════════════

      CRITICAL ISSUES (1): 1 SQL injection risk
      HIGH ISSUES (3): 3 security concerns
      MEDIUM ISSUES (5): 5 code quality issues
      LOW ISSUES (2): 2 style issues

      SECURITY ANALYSIS (if --include-security):
      ✗ Line 156 (user-profile.js): Unvalidated user_id in SQL query
      ✗ Line 234 (dashboard.js): Missing CSRF token validation
      ✗ Line 67 (api.js): Insufficient rate limiting
      ✗ Line 445 (auth.js): Weak password validation regex

      PERFORMANCE ANALYSIS (if --include-performance):
      ⚠ Line 89: N+1 query problem in user data fetching
        Expected impact: 2-3s latency per dashboard load
        Recommendation: Use SQL JOIN instead of separate queries

      ⚠ Line 234: Unnecessary re-renders in React components
        Expected impact: 30-50ms slower UI interactions
        Recommendation: Use useMemo() for expensive calculations

      ARCHITECTURE ANALYSIS:
      ✓ Good: Proper separation of concerns (controllers, services, models)
      ✓ Good: Consistent error handling patterns
      ⚠ Consider: Extract duplicated validation logic into shared utilities

      TESTING COVERAGE:
      - Unit tests: 84% (Target: 80%) ✓
      - Integration tests: 62% (Target: 70%) ⚠
      - E2E tests: Present for happy path ✓
      - Edge cases: 3 untested scenarios identified

      RECOMMENDED ACTIONS:
      1. [BLOCKING] Fix SQL injection on line 156 before merge
      2. [BLOCKING] Add CSRF token validation on line 234
      3. [IMPORTANT] Refactor N+1 query on line 89
      4. [OPTIONAL] Add integration tests for payment flow
      5. [OPTIONAL] Document dashboard data flow in PR comments

      ═════════════════════════════════════════════════
      RECOMMENDATION: Approve with required changes
      - Fix 2 blocking security issues
      - Address 1 critical N+1 query performance issue
      - Request testing of edge cases
      ═════════════════════════════════════════════════

      Report generated in 4.7s
      Reviewed by: Code Review Agent v2.1.0


# === ANALYTICS (Placeholder for future) ===
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors:
  - Engineering Team
  - Security Team
created: 2025-11-24
updated: 2025-11-24

# === DISCOVERABILITY ===
tags:
  - code-review
  - code-quality
  - security-analysis
  - performance-analysis
  - best-practices
  - code-inspection
  - pull-requests
  - static-analysis

featured: false
verified: true
license: MIT

---

# Code Review

Comprehensive code analysis command that examines code for quality, security, and performance issues with detailed findings and actionable recommendations.

---

## Pattern Type: Multi-Phase

**Complexity:** Medium
**Execution Time:** 2-5 minutes depending on scope
**Destructive:** No (read-only analysis)

---

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Gather comprehensive code information and structure

**Steps:**
1. Scan specified directory/files for code artifacts
2. Identify file types (JavaScript, Python, Go, Java, etc.)
3. Count lines of code and measure scope
4. Detect dependencies and imports
5. Build code dependency graph

**Tools Used:** Glob, Read, Bash (for file metrics)

**Output:** Inventory of files, lines of code, languages, dependencies

### Phase 2: Analysis

**Goal:** Process code against quality, security, and performance criteria

**Analysis Dimensions:**

1. **Code Quality**
   - Cyclomatic complexity (function branching)
   - Code duplication detection
   - Naming convention compliance
   - Function length analysis
   - Parameter count validation
   - Cohesion scoring

2. **Security**
   - Hardcoded secrets detection
   - SQL injection vulnerabilities
   - Command injection risks
   - Cross-site scripting (XSS) patterns
   - Weak authentication/authorization
   - Insecure deserialization
   - Dependency vulnerability scanning
   - Input validation gaps

3. **Performance**
   - N+1 query detection
   - Memory leak patterns
   - Infinite loop detection
   - Inefficient algorithms (O(n²), O(n³))
   - Unoptimized loops
   - Blocking operations on main thread
   - Unnecessary re-renders (React)
   - Connection pooling issues

4. **Best Practices**
   - Error handling completeness
   - Logging and debugging capabilities
   - Documentation coverage
   - Test coverage analysis
   - Architecture patterns
   - Design pattern application
   - API design consistency

**Scoring System:**
- 9-10: Excellent (ready to merge)
- 8-9: Good (minor improvements)
- 7-8: Fair (address warnings)
- 6-7: Poor (significant issues)
- <6: Critical (do not merge)

### Phase 3: Task Execution

**Goal:** Generate findings, recommendations, and action items

**Actions:**

1. **Issue Categorization**
   - Organize by severity: CRITICAL → HIGH → MEDIUM → LOW
   - Group by type: Security, Performance, Quality, Architecture
   - Calculate impact and effort for each issue

2. **Recommendation Generation**
   - Provide specific remediation for each issue
   - Include code examples when applicable
   - Link to reference documentation (OWASP, best practices)
   - Estimate effort to fix

3. **Report Compilation**
   - Summary with quality score
   - Critical issues requiring fixes
   - High-priority improvements
   - Architecture observations
   - Testing coverage analysis
   - Final recommendation (merge/request changes)

**Blocking Issues:** Issues that must be fixed before merge
- Security vulnerabilities (CRITICAL, HIGH)
- Memory leaks
- Production failures

### Phase 4: Reporting

**Goal:** Present findings in clear, actionable format

**Report Includes:**

1. **Executive Summary**
   - Overall quality score
   - Critical issue count
   - Merge recommendation
   - Estimated remediation time

2. **Detailed Findings**
   - Each issue with line number and code snippet
   - Severity level with justification
   - Specific remediation steps
   - References to standards/docs

3. **Security Findings** (if --include-security)
   - Vulnerabilities by CWE
   - CVSS risk scores
   - Exploit likelihood
   - Remediation guidance

4. **Performance Findings** (if --include-performance)
   - Bottlenecks with impact estimates
   - Algorithm complexity analysis
   - Resource utilization patterns
   - Optimization recommendations

5. **Recommendations**
   - Blocking issues (must fix)
   - Important improvements (should fix)
   - Optional enhancements (nice to fix)
   - Testing gaps to address

6. **Metrics**
   - Quality score trend
   - Issue distribution
   - Architecture assessment
   - Code health indicators

**Report Location:** Printed to console or saved to file with --output flag

---

## Usage

```bash
/code-review [target] [options]
```

### Arguments

- `target` - File, directory, or PR to review (required)
  - Local file: `/code-review src/handlers/user.js`
  - Directory: `/code-review src/`
  - PR reference: `/code-review --pr #1234`

### Options

```bash
--pr #NUMBER          # Review specific pull request
--include-security    # Run detailed security analysis
--include-performance # Run performance analysis
--severity LEVEL      # Filter issues by severity (critical,high,medium,low)
--format FORMAT       # Output format (text, json, html) - default: text
--output FILE         # Save report to file
--exclude PATTERN     # Exclude files matching pattern (e.g., *.test.js)
--max-issues N        # Limit report to N issues (default: 50)
--compare-branch BR   # Compare against branch to show new issues only
```

### Examples

**Example 1: Review single file**

```bash
/code-review src/handlers/user.js
```

**Example 2: Full analysis with all checks**

```bash
/code-review --pr #1234 --include-security --include-performance
```

---

## What This Command Does

### Context Gathering

The command will:
1. Scan all specified files and directories
2. Parse code structure and dependencies
3. Identify programming language and frameworks
4. Catalog imports, dependencies, and external calls
5. Measure lines of code and complexity metrics

### Task Execution

Then it will:
1. Run quality analysis (complexity, duplication, naming)
2. Scan for security vulnerabilities (if --include-security)
3. Analyze performance patterns (if --include-performance)
4. Evaluate architecture and design patterns
5. Check test coverage and error handling
6. Generate severity-categorized issue list

### Expected Output

You will receive:
- Overall code quality score (0-10)
- Critical issues requiring fixes before merge
- Security vulnerabilities with remediation
- Performance bottlenecks with impact estimates
- Architecture observations and recommendations
- Test coverage analysis
- Clear merge/no-merge recommendation

**Output Format:** Markdown by default, JSON with --format json
**Output Location:** Console (or file with --output)

---

## Analysis Criteria

### Code Quality Metrics

**Cyclomatic Complexity**
- Measures number of decision paths through code
- Threshold: 5 (warning), 10+ (critical)
- Remedy: Break into smaller functions

**Code Duplication**
- Detects repeated code blocks
- Threshold: 3+ instances of same 5+ line block
- Remedy: Extract into shared function/utility

**Function Length**
- Target: <20 lines for utilities, <40 for complex
- Remedy: Break into smaller focused functions

**Parameter Count**
- Target: ≤3 parameters (4+ is warning)
- Remedy: Use objects for multiple parameters

### Security Vulnerabilities

**CRITICAL (Must Fix):**
- Hardcoded secrets (API keys, passwords, tokens)
- SQL injection with user input
- Remote code execution risks
- Authentication/authorization bypass

**HIGH (Should Fix):**
- Cross-site scripting (XSS) opportunities
- Insecure deserialization
- Weak encryption
- Missing input validation
- Insufficient rate limiting

**MEDIUM (Consider):**
- Logging sensitive data
- Weak password requirements
- Missing error handling
- Unvalidated redirects

### Performance Issues

**N+1 Queries**
- Impact: Typically 1-5s latency per request
- Detection: Loop with nested database query
- Remedy: Use JOIN or batching

**Inefficient Algorithms**
- O(n²) loops: Impact grows quadratically
- O(n³) operations: Severely impacts scalability
- Remedy: Use set operations, hash maps, sorting

**Memory Leaks**
- Unbounded caches without eviction
- Event listeners without cleanup
- Circular references in JavaScript
- Impact: Process will crash or slow over time

---

## Error Handling

### Common Issues

**Issue:** "No files found matching pattern"
**Cause:** Directory path is incorrect or pattern too restrictive
**Solution:** Verify path exists and adjust exclusion patterns
**Prevention:** Use absolute paths and test glob pattern first

---

**Issue:** "Syntax error in target file"
**Cause:** File is not valid code for detected language
**Solution:** Verify file is complete and compilable
**Prevention:** Ensure code compiles/runs before review

---

**Issue:** "Unable to determine language"
**Cause:** File extension not recognized or ambiguous
**Solution:** Specify language with --lang flag
**Prevention:** Use standard file extensions (.js, .py, .go, etc.)

---

**Issue:** "Analysis timed out (>10 minutes)"
**Cause:** Repository too large or analysis too complex
**Solution:** Limit scope with --exclude or analyze specific files
**Prevention:** Review smaller areas incrementally

---

**Issue:** "Security database outdated"
**Cause:** Dependency vulnerability data not current
**Solution:** Run with --update-db to refresh
**Prevention:** Periodically update security definitions

---

### Validation Failures

If the command reports validation errors:

1. **File Not Readable**
   - Check: File permissions and path
   - Fix: Verify path and ensure read permissions

2. **Invalid Configuration**
   - Check: Command-line arguments
   - Fix: Review options with /code-review --help

3. **Incomplete Analysis**
   - Check: Disk space and memory
   - Fix: Restart command, ensure system resources available

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-code-reviewer](../../agents/engineering/cs-code-reviewer.md)** - Orchestrates multi-PR review workflows
- **[cs-engineering-lead](../../agents/engineering/cs-engineering-lead.md)** - Validates quality across team PRs
- **[cs-security-analyst](../../agents/engineering/cs-security-analyst.md)** - Focuses on vulnerability detection

### Related Skills

This command leverages:

- **[code-quality-analyzer](../../skills/engineering-team/code-quality-analyzer/)** - Quality metrics and duplication detection
- **[security-scanner](../../skills/engineering-team/security-scanner/)** - Vulnerability and secret detection
- **[performance-analyzer](../../skills/engineering-team/performance-analyzer/)** - Performance bottleneck analysis

### Python Tools

This command may execute:

```bash
# Code quality analysis
python skills/engineering-team/code-quality-analyzer/scripts/quality_analyzer.py [target]

# Security vulnerability scanning
python skills/engineering-team/security-scanner/scripts/security_checker.py [target]

# Performance profiling
python skills/engineering-team/performance-analyzer/scripts/performance_profiler.py [target]
```

---

## Success Criteria

This command is successful when:

- [ ] All specified files are analyzed without errors
- [ ] Quality score is calculated and severity issues categorized
- [ ] Critical security issues are identified with remediation
- [ ] Performance bottlenecks flagged with impact estimates
- [ ] Merge/no-merge recommendation provided based on blocking issues
- [ ] Report includes actionable next steps with effort estimates
- [ ] Output is clear and accessible to both developers and leads

### Quality Metrics

**Expected Outcomes:**
- Analysis Time: 2-5 minutes for typical PR
- Issue Detection Rate: 85%+ accuracy on known vulnerabilities
- False Positive Rate: <5% (reducing review burden)
- Recommendation Accuracy: 90%+ match with manual review consensus

---

## Tips for Best Results

1. **Review Scope**
   - Include security and performance analyses for critical paths
   - Focus on business logic, not generated code
   - Exclude vendored dependencies and build artifacts

2. **Interpret Results**
   - Not all warnings require fixes (assess risk vs. effort)
   - Consider architecture and team standards
   - Use recommendations as conversation starters, not mandates

3. **Action Items**
   - Fix all CRITICAL/HIGH security issues before merge
   - Address MEDIUM/HIGH code quality issues in same PR or follow-up
   - Log performance improvements as technical debt when appropriate

---

## Related Commands

- `/security.scan-secrets` - Specialized secret detection across entire repo
- `/test.coverage-report` - Generate test coverage metrics
- `/git.create-pr` - Create PR with review checklist
- `/performance.profile-app` - Deep performance profiling

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Security vulnerabilities
- [Code Complete](https://www.amazon.com/Code-Complete-Practical-Handbook-Construction/dp/0735619670/) - Code quality principles
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-your-journey-to-mastery-20th-anniversary-edition/) - Best practices
- [Secure Coding Guidelines](https://www.securecoding.cert.org/) - CERT secure coding standards
- [CWE List](https://cwe.mitre.org/) - Common Weakness Enumeration reference

---

**Last Updated:** November 24, 2025
**Version:** v1.0.0
**Maintained By:** Claude Skills Team
**Feedback:** Submit issues or feature requests in repository issues
