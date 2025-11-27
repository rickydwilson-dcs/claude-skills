---

# === CORE IDENTITY ===
name: code-reviewer
title: Code Reviewer Skill Package
description: Comprehensive code review skill for TypeScript, JavaScript, Python, Swift, Kotlin, Go. Includes automated code analysis, best practice checking, security scanning, and review checklist generation. Use when reviewing pull requests, providing code feedback, identifying issues, or ensuring code quality standards.
domain: engineering
subdomain: engineering-general

# === WEBSITE DISPLAY ===
difficulty: intermediate
time-saved: "TODO: Quantify time savings"
frequency: "TODO: Estimate usage frequency"
use-cases:
  - Primary workflow for Code Reviewer
  - Analysis and recommendations for code reviewer tasks
  - Best practices implementation for code reviewer
  - Integration with related skills and workflows

# === RELATIONSHIPS ===
related-agents: []
related-skills: []
related-commands: []
orchestrated-by: []

# === TECHNICAL ===
dependencies:
  scripts: []
  references: []
  assets: []
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack: [Python 3.8+, Markdown]

# === EXAMPLES ===
examples:
  -
    title: Example Usage
    input: "TODO: Add example input for code-reviewer"
    output: "TODO: Add expected output"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-10-19
updated: 2025-11-23
license: MIT

# === DISCOVERABILITY ===
tags: [analysis, code, engineering, reviewer, security]
featured: false
verified: true
---


# Code Reviewer

Expert code review skill with automated analysis tools for modern programming languages. Provides comprehensive review checklists, coding standards enforcement, and anti-pattern detection across TypeScript, JavaScript, Python, Swift, Kotlin, and Go.

## Overview

This skill delivers production-ready code review capabilities through three Python automation tools and extensive reference documentation. Whether conducting pull request reviews, enforcing coding standards, or identifying common anti-patterns, this skill ensures consistent, high-quality code across your team.

**Use this skill when:**
- Reviewing pull requests for quality and security
- Enforcing language-specific coding standards
- Identifying common anti-patterns and code smells
- Generating comprehensive review reports
- Training team members on best practices

## Quick Start

### Analyze a Pull Request
```bash
# Basic PR analysis
python scripts/pr_analyzer.py 123 --repo=company/project

# Full quality check on codebase
python scripts/code_quality_checker.py ./src --language=typescript

# Generate comprehensive review report
python scripts/review_report_generator.py 123 --format=markdown
```

### Access Documentation
- Review Checklist: `references/code_review_checklist.md`
- Coding Standards: `references/coding_standards.md`
- Anti-Patterns Guide: `references/common_antipatterns.md`

## Core Capabilities

- **Automated Pull Request Analysis** - Comprehensive PR analysis with metrics, complexity scores, and review priority recommendations
- **Multi-Language Code Quality Checking** - Support for TypeScript, JavaScript, Python, Swift, Kotlin, and Go with SOLID principles validation
- **Security Vulnerability Detection** - Identify SQL injection, XSS, authentication issues, and other security concerns
- **Best Practice Enforcement** - Language-specific coding standards, naming conventions, and patterns
- **Anti-Pattern Detection** - Catalog of common anti-patterns across languages, databases, and testing
- **Automated Review Report Generation** - Detailed, actionable reports with categorized findings and feedback suggestions

## Python Tools

### 1. PR Analyzer

Automated pull request analysis with comprehensive metrics and insights.

**Features:**
- Code diff analysis and impact assessment
- Complexity metrics calculation
- Test coverage evaluation
- Security vulnerability detection
- Breaking change identification
- Review priority recommendations

**Usage:**
```bash
python scripts/pr_analyzer.py <pr-number> [--repo=owner/name]
python scripts/pr_analyzer.py 123 --repo=company/project --json
```

**Output:**
```
PR Analysis Report (#123):
- Files Changed: 12 files
- Lines Changed: +245 / -87
- Complexity Score: Medium (6/10)
- Test Coverage Impact: +3%
- Security Concerns: 1 medium issue
- Review Priority: High
- Estimated Review Time: 45 minutes

Recommendations:
1. Review authentication changes carefully (security-critical)
2. Verify test coverage for new UserService methods
3. Consider breaking into smaller PRs (>300 lines)
```

### 2. Code Quality Checker

Comprehensive code analysis across multiple languages with actionable recommendations.

**Features:**
- Multi-language support (TS/JS/Python/Swift/Kotlin/Go)
- SOLID principles validation
- Code smell detection
- Performance issue identification
- Documentation quality assessment
- Configurable rulesets

**Usage:**
```bash
python scripts/code_quality_checker.py <path> [--language=typescript]
python scripts/code_quality_checker.py ./src --verbose --json
```

**Checks:**
- Cyclomatic complexity
- Function/method length
- Code duplication
- Naming conventions
- Error handling patterns
- Test coverage

### 3. Review Report Generator

Generate detailed, actionable review reports with categorized findings.

**Features:**
- Multi-level issue categorization (blocking/major/minor)
- Language-specific best practice checks
- Security vulnerability assessment
- Performance concern flagging
- Markdown/JSON output formats
- Automated feedback suggestions

**Usage:**
```bash
python scripts/review_report_generator.py <pr-number> [options]
python scripts/review_report_generator.py 123 --format=markdown
```

## Reference Documentation

Detailed guides available in the `references/` directory:

### Code Review Checklist
**[code_review_checklist.md](references/code_review_checklist.md)** - Comprehensive review guide covering:
- Pre-review preparation and context gathering
- Code quality assessment (functionality, readability, maintainability)
- Language-specific checklists (TypeScript/JavaScript, Python, Swift, Kotlin, Go)
- Testing requirements and best practices
- Security review checklist (injection, auth, data protection)
- Architecture and scalability considerations
- Documentation standards
- Git workflow and commit quality
- Performance optimization checks
- Feedback guidelines and review priorities

### Coding Standards
**[coding_standards.md](references/coding_standards.md)** - Language-specific standards including:
- Naming conventions across all supported languages
- TypeScript/JavaScript best practices and modern patterns
- React-specific standards (hooks, components, performance)
- Python PEP 8 compliance and Pythonic patterns
- Swift optionals handling and protocol-oriented design
- Kotlin null safety and data classes
- Go error handling and interfaces
- Code formatting and file organization
- Documentation standards (JSDoc, docstrings)
- Linting and formatting tool recommendations

### Common Anti-Patterns
**[common_antipatterns.md](references/common_antipatterns.md)** - Catalog of anti-patterns to avoid:
- General anti-patterns (God objects, magic numbers, deep nesting, premature optimization)
- TypeScript/JavaScript issues (callback hell, 'any' type abuse, React prop mutations)
- Python problems (mutable defaults, bare except, context manager neglect)
- Swift pitfalls (force unwrapping, retain cycles, IUO overuse)
- Kotlin concerns (null assertion abuse, data class neglect)
- Go mistakes (error ignoring, defer neglect, goroutine leaks)
- Database anti-patterns (N+1 queries, missing indexes, SELECT *)
- Security vulnerabilities (SQL injection, plaintext passwords, secret exposure)
- Performance issues (unnecessary re-renders, bulk loading)
- Testing anti-patterns (implementation testing, test interdependence)

## Key Workflows

### Workflow 1: Pull Request Review

```bash
# 1. Analyze the PR
python scripts/pr_analyzer.py 123 --repo=company/project

# 2. Review changed files with quality checker
python scripts/code_quality_checker.py ./src --language=typescript

# 3. Generate comprehensive review report
python scripts/review_report_generator.py 123 --format=markdown

# 4. Review output and provide feedback using checklist
# Reference: references/code_review_checklist.md
```

### Workflow 2: Codebase Quality Audit

```bash
# 1. Run quality checker on entire codebase
python scripts/code_quality_checker.py ./ --verbose

# 2. Identify anti-patterns
grep -r "any" src/**/*.ts  # TypeScript: avoid 'any'
grep -r "except:" src/**/*.py  # Python: check bare excepts

# 3. Generate comprehensive report
python scripts/code_quality_checker.py ./ --json > quality-report.json

# 4. Prioritize fixes
# Review report and tackle blocking/major issues first
```

### Workflow 3: Team Standards Enforcement

```bash
# 1. Configure linters based on standards
# ESLint for TypeScript/JavaScript
# pylint/flake8 for Python
# SwiftLint for Swift
# Reference: references/coding_standards.md

# 2. Setup pre-commit hooks
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
python scripts/code_quality_checker.py $(git diff --cached --name-only)
EOF
chmod +x .git/hooks/pre-commit

# 3. Add CI/CD quality gates
# GitHub Actions example:
# - name: Code Quality Check
#   run: python scripts/code_quality_checker.py ./src
```

## Language Support

**TypeScript/JavaScript**
- Type safety validation
- React patterns and hooks
- Async/await best practices
- Modern ES6+ features
- ESLint/Prettier integration

**Python**
- PEP 8 compliance
- Type hints validation
- Pythonic patterns
- Context managers
- Import organization

**Swift**
- Optional safety
- Protocol-oriented design
- Memory management
- SwiftLint integration

**Kotlin**
- Null safety
- Data classes
- Coroutines
- Extension functions

**Go**
- Error handling
- Goroutine management
- Interface design
- Idiomatic Go

## Best Practices Summary

### Review Priorities

1. **Security** - SQL injection, XSS, authentication issues
2. **Correctness** - Logic errors, edge case handling
3. **Performance** - N+1 queries, memory leaks, inefficient algorithms
4. **Maintainability** - Code clarity, documentation, test coverage
5. **Style** - Formatting, naming conventions (automated preferred)

### Common Red Flags

- Functions >50 lines
- Cyclomatic complexity >10
- Test coverage <70%
- No error handling
- Hardcoded secrets
- Commented-out code
- Missing documentation

### Effective Feedback

**DO:**
- Be constructive and specific
- Explain the "why" behind suggestions
- Acknowledge good practices
- Suggest alternatives
- Use questions to guide learning

**DON'T:**
- Focus on personal preferences
- Be vague or unclear
- Nitpick trivial issues
- Assume bad intentions
- Skip positive feedback

## Integration

### CI/CD Pipeline

```yaml
# .github/workflows/code-review.yml
name: Code Review
on: [pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Run Quality Checker
        run: python scripts/code_quality_checker.py ./src
      - name: Generate Report
        run: python scripts/review_report_generator.py ${{ github.event.pull_request.number }}
```

### Pre-commit Hooks

```bash
# Install pre-commit framework
pip install pre-commit

# Add .pre-commit-config.yaml
hooks:
  - repo: local
    hooks:
      - id: code-quality
        name: Code Quality Check
        entry: python scripts/code_quality_checker.py
        language: system
```

## Additional Resources

- **Review Checklist:** [references/code_review_checklist.md](references/code_review_checklist.md)
- **Coding Standards:** [references/coding_standards.md](references/coding_standards.md)
- **Anti-Patterns:** [references/common_antipatterns.md](references/common_antipatterns.md)
- **Python Tools:** `scripts/` directory

## Getting Help

1. **Review guidelines:** See [code_review_checklist.md](references/code_review_checklist.md)
2. **Language standards:** Consult [coding_standards.md](references/coding_standards.md)
3. **Pattern recognition:** Review [common_antipatterns.md](references/common_antipatterns.md)
4. **Tool usage:** Run any script with `--help` flag

---

**Version:** 1.0.0
**Last Updated:** 2025-11-08
**Documentation Structure:** Progressive disclosure with references/
