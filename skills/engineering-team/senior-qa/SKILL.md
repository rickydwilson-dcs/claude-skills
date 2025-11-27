---

# === CORE IDENTITY ===
name: senior-qa
title: Senior QA Skill Package
description: Comprehensive QA and testing skill for quality assurance, test automation, and testing strategies for ReactJS, NextJS, NodeJS applications. Includes test suite generation, coverage analysis, E2E testing setup, and quality metrics. Use when designing test strategies, writing test cases, implementing test automation, performing manual testing, or analyzing test coverage.
domain: engineering
subdomain: quality-assurance

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "TODO: Quantify time savings"
frequency: "TODO: Estimate usage frequency"
use-cases:
  - Designing comprehensive test strategies and test plans
  - Implementing automated testing frameworks
  - Setting up continuous testing in CI/CD pipelines
  - Conducting performance and load testing

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
    input: "TODO: Add example input for senior-qa"
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
tags: [analysis, automation, design, engineering, senior, testing]
featured: false
verified: true
---


# Senior QA

Complete toolkit for senior QA engineers with comprehensive testing strategies, automation frameworks, and quality assurance best practices.

## Overview

The Senior QA skill provides world-class testing frameworks, automation tools, and quality assurance methodologies for modern software development. This skill covers unit testing, integration testing, E2E testing, test coverage analysis, and quality metrics used by leading engineering teams.

Designed for senior QA engineers and test automation specialists, this skill includes proven patterns for React/Next.js/Node.js applications, test suite generation, coverage optimization, and E2E test scaffolding. All content focuses on production-grade testing with industry best practices.

**Core Value:** Build comprehensive test suites that catch 90%+ of bugs before production while maintaining fast CI/CD pipelines and high developer productivity.

## Quick Start

### Main Capabilities

This skill provides three core capabilities through automated scripts:

```bash
# Script 1: Test Suite Generator
python scripts/test_suite_generator.py [options]

# Script 2: Coverage Analyzer
python scripts/coverage_analyzer.py [options]

# Script 3: E2E Test Scaffolder
python scripts/e2e_test_scaffolder.py [options]
```

## Core Capabilities

### 1. Test Suite Generator

Automated tool for test suite generator tasks.

**Features:**
- Automated scaffolding
- Best practices built-in
- Configurable templates
- Quality checks

**Usage:**
```bash
python scripts/test_suite_generator.py <project-path> [options]
```

### 2. Coverage Analyzer

Comprehensive analysis and optimization tool.

**Features:**
- Deep analysis
- Performance metrics
- Recommendations
- Automated fixes

**Usage:**
```bash
python scripts/coverage_analyzer.py <target-path> [--verbose]
```

### 3. E2E Test Scaffolder

Advanced tooling for specialized tasks.

**Features:**
- Expert-level automation
- Custom configurations
- Integration ready
- Production-grade output

**Usage:**
```bash
python scripts/e2e_test_scaffolder.py [arguments] [options]
```

## Key Workflows

### 1. Design Test Strategy for New Feature

**Time:** 2-3 hours

1. **Analyze Feature Requirements** - Understand what needs testing
2. **Identify Test Scenarios** - Map out happy path, edge cases, error conditions
3. **Generate Test Suite** - Use test_suite_generator.py to scaffold tests
4. **Implement Tests** - Write unit, integration, and E2E tests
5. **Verify Coverage** - Run coverage_analyzer.py to ensure adequate coverage

**Expected Output:** Comprehensive test suite with >80% coverage

### 2. Improve Test Coverage

**Time:** 4-6 hours

1. **Run Coverage Analysis** - Identify gaps with coverage_analyzer.py
2. **Prioritize Coverage Gaps** - Focus on critical paths first
3. **Write Missing Tests** - Add tests for uncovered code
4. **Refactor for Testability** - Break down complex functions
5. **Verify Improvement** - Re-run coverage analysis

**Expected Output:** Test coverage increased by 15-30%

### 3. Set Up E2E Testing

**Time:** 1-2 days

1. **Design E2E Test Scenarios** - Identify critical user journeys
2. **Scaffold E2E Framework** - Use e2e_test_scaffolder.py
3. **Implement Test Cases** - Write Cypress or Playwright tests
4. **Integrate with CI/CD** - Add E2E tests to pipeline
5. **Monitor and Maintain** - Keep tests stable and fast

**Expected Output:** Production E2E test suite running in CI/CD

## Python Tools

### test_suite_generator.py

Generates comprehensive test suites from source code analysis with unit, integration, and edge case coverage.

**Key Features:**
- Automated test scaffolding for React/Next.js/Node.js
- Unit test generation with Jest/React Testing Library patterns
- Integration test templates with database and API mocking
- Edge case identification and test generation
- Test naming conventions and file structure automation

**Common Usage:**
```bash
# Generate test suite for component
python scripts/test_suite_generator.py src/components/Button.tsx

# Generate tests for entire directory
python scripts/test_suite_generator.py src/components/ --recursive

# Help
python scripts/test_suite_generator.py --help
```

**Use Cases:**
- Scaffolding tests for new components or modules
- Ensuring consistent test structure across codebase
- Accelerating test development for large codebases
- Training junior engineers on testing patterns

### coverage_analyzer.py

Analyzes test coverage with detailed gap identification and actionable recommendations for improvement.

**Key Features:**
- Line, branch, and function coverage metrics
- Coverage gap identification by file and function
- Priority scoring (critical paths vs. utility functions)
- Historical trend analysis
- Integration with Jest, Istanbul, and NYC coverage tools
- Visual coverage reports with heat maps

**Common Usage:**
```bash
# Analyze coverage for project
python scripts/coverage_analyzer.py .

# Detailed report with recommendations
python scripts/coverage_analyzer.py . --verbose

# JSON output for CI/CD integration
python scripts/coverage_analyzer.py . --output json

# Help
python scripts/coverage_analyzer.py --help
```

**Use Cases:**
- Identifying untested code before production
- Setting coverage targets and tracking progress
- Prioritizing test development efforts
- Generating coverage reports for stakeholders

### e2e_test_scaffolder.py

Scaffolds end-to-end test infrastructure with Cypress or Playwright including page objects, test data, and CI/CD integration.

**Key Features:**
- E2E framework setup (Cypress or Playwright)
- Page Object Model pattern generation
- Test data management and fixtures
- CI/CD pipeline integration (GitHub Actions, CircleCI)
- Visual regression testing setup
- Parallelization and sharding configuration

**Common Usage:**
```bash
# Scaffold Cypress E2E tests
python scripts/e2e_test_scaffolder.py --framework cypress

# Scaffold Playwright tests
python scripts/e2e_test_scaffolder.py --framework playwright

# With CI/CD integration
python scripts/e2e_test_scaffolder.py --framework cypress --ci github-actions

# Help
python scripts/e2e_test_scaffolder.py --help
```

**Use Cases:**
- Setting up E2E testing for new applications
- Migrating from Selenium to modern frameworks
- Implementing visual regression testing
- Establishing E2E testing standards across teams

## Reference Documentation

### Testing Strategies

Comprehensive guide available in `references/testing_strategies.md`:

- Detailed patterns and practices
- Code examples
- Best practices
- Anti-patterns to avoid
- Real-world scenarios

### Test Automation Patterns

Complete workflow documentation in `references/test_automation_patterns.md`:

- Step-by-step processes
- Optimization strategies
- Tool integrations
- Performance tuning
- Troubleshooting guide

### Qa Best Practices

Technical reference guide in `references/qa_best_practices.md`:

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
python scripts/coverage_analyzer.py .

# Review recommendations
# Apply fixes
```

### 3. Implement Best Practices

Follow the patterns and practices documented in:
- `references/testing_strategies.md`
- `references/test_automation_patterns.md`
- `references/qa_best_practices.md`

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
python scripts/coverage_analyzer.py .
python scripts/e2e_test_scaffolder.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Common Issues

Check the comprehensive troubleshooting section in `references/qa_best_practices.md`.

### Getting Help

- Review reference documentation
- Check script output messages
- Consult tech stack documentation
- Review error logs

## Resources

- Pattern Reference: `references/testing_strategies.md`
- Workflow Guide: `references/test_automation_patterns.md`
- Technical Guide: `references/qa_best_practices.md`
- Tool Scripts: `scripts/` directory
