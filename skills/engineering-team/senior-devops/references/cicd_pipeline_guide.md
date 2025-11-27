# CI/CD Pipeline Guide

## Overview

This reference guide provides comprehensive CI/CD patterns and best practices for GitHub Actions workflows, focusing on quality gates, progressive validation, and automated deployment strategies.

## Branch Strategy: develop → staging → main

### Branch Flow

```
feature/* ─────┐
fix/* ─────────┼──> develop ──> staging ──> main
refactor/* ────┘
```

| Branch | Purpose | Protection | Quality Gate |
|--------|---------|------------|--------------|
| develop | Integration | Soft | Fast validation (changed files) |
| staging | Pre-production | Medium | Full validation (all content) |
| main | Production | Strict | Production gate (source check) |

### Quality Gate Progression

**Develop (Fast Feedback):**
- Validate only changed files
- Target: < 2 minutes
- Focus: Catch obvious errors quickly

**Staging (Comprehensive):**
- Validate all content
- Target: < 5 minutes
- Focus: Full sweep before pre-production

**Main (Production Gate):**
- Verify source branch
- Target: < 3 minutes
- Focus: Final verification

## GitHub Actions Patterns

### Pattern 1: Incremental Validation

**Description:**
Only validate files that changed in the PR/push, reducing CI time significantly.

**When to Use:**
- Development branches (develop, feature/*)
- Large repositories with many files
- Fast feedback loops needed

**Implementation:**

```yaml
detect-changes:
  runs-on: ubuntu-latest
  outputs:
    agents_changed: ${{ steps.detect.outputs.agents_changed }}
    agents_list: ${{ steps.detect.outputs.agents_list }}
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Detect changed files
      id: detect
      run: |
        # Get changed files between base and head
        if [[ "${{ github.event_name }}" == "pull_request" ]]; then
          BASE_SHA="${{ github.event.pull_request.base.sha }}"
          HEAD_SHA="${{ github.event.pull_request.head.sha }}"
        else
          BASE_SHA="${{ github.event.before }}"
          HEAD_SHA="${{ github.sha }}"
        fi

        CHANGED_FILES=$(git diff --name-only "$BASE_SHA" "$HEAD_SHA")

        # Filter to specific content types
        AGENTS=$(echo "$CHANGED_FILES" | grep '^agents/.*\.md$' || true)
        if [[ -n "$AGENTS" ]]; then
          echo "agents_changed=true" >> $GITHUB_OUTPUT
          echo "agents_list<<EOF" >> $GITHUB_OUTPUT
          echo "$AGENTS" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
        else
          echo "agents_changed=false" >> $GITHUB_OUTPUT
        fi
```

**Benefits:**
- 80%+ faster CI for typical PRs
- Reduces GitHub Actions minutes usage
- Provides faster developer feedback

**Trade-offs:**
- May miss integration issues
- Requires full validation before production

### Pattern 2: Conditional Job Execution

**Description:**
Run jobs only when relevant files change or specific conditions are met.

**When to Use:**
- Different validation for different content types
- Skip expensive operations when not needed
- Optimize CI resource usage

**Implementation:**

```yaml
validate-agents:
  needs: detect-changes
  if: needs.detect-changes.outputs.agents_changed == 'true'
  runs-on: ubuntu-latest
  steps:
    - name: Validate changed agents
      run: |
        AGENTS="${{ needs.detect-changes.outputs.agents_list }}"
        echo "$AGENTS" | while read -r agent; do
          if [[ -n "$agent" && -f "$agent" ]]; then
            python3 scripts/agent_builder.py --validate "$agent"
          fi
        done
```

**Benefits:**
- Skips irrelevant jobs entirely
- Clear job dependencies
- Easy to understand flow

### Pattern 3: Matrix Strategy for Parallel Validation

**Description:**
Run validation in parallel across multiple content types or categories.

**When to Use:**
- Large content validation suites
- Independent validation tasks
- Maximize parallelization

**Implementation:**

```yaml
validate-content:
  strategy:
    fail-fast: false
    matrix:
      content_type: [agents, skills, commands]
  runs-on: ubuntu-latest
  steps:
    - name: Validate ${{ matrix.content_type }}
      run: |
        case "${{ matrix.content_type }}" in
          agents)
            bash scripts/validate_all_agents.sh
            ;;
          skills)
            python3 scripts/validate_all_skills.py
            ;;
          commands)
            python3 scripts/validate_all_commands.py
            ;;
        esac
```

**Benefits:**
- Parallel execution reduces total time
- Independent failures don't block other types
- Easy to add new content types

### Pattern 4: Scheduled Full Validation

**Description:**
Run comprehensive validation on a schedule to catch drift or accumulated issues.

**When to Use:**
- Nightly/weekly full validation
- Catch issues not covered by incremental validation
- Verify overall repository health

**Implementation:**

```yaml
on:
  schedule:
    # Run at 2 AM UTC daily
    - cron: '0 2 * * *'
  workflow_dispatch:
    inputs:
      full_validation:
        description: 'Run full validation'
        type: boolean
        default: true

jobs:
  nightly-validation:
    if: github.event_name == 'schedule' || github.event.inputs.full_validation == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Full validation sweep
        run: |
          bash scripts/validate_all_agents.sh
          python3 scripts/validate_all_skills.py
          python3 scripts/validate_all_commands.py
```

**Benefits:**
- Catches accumulated issues
- Provides regular health checks
- Enables manual full validation when needed

## Security Scanning Integration

### Dependency Scanning

```yaml
security-scan:
  runs-on: ubuntu-latest
  continue-on-error: true  # Warning only
  steps:
    - name: Install safety
      run: pip install safety

    - name: Scan dependencies
      run: |
        if [[ -f requirements.txt ]]; then
          safety check -r requirements.txt --output text || \
            echo "::warning::Security vulnerabilities found"
        fi
```

### Secrets Detection

```yaml
secrets-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: gitleaks/gitleaks-action@v2
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Branch Protection Configuration

### Main Branch (Strict)

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "Production Gate (Main)",
      "Full Validation (Staging)"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1
  },
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

### Staging Branch (Medium)

```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "Full Validation (Staging)"
    ]
  },
  "enforce_admins": false,
  "allow_force_pushes": false
}
```

### Develop Branch (Soft)

```json
{
  "required_status_checks": {
    "strict": false,
    "contexts": [
      "Quick Checks (Develop)",
      "Validate Changed Content (Develop)"
    ]
  }
}
```

## Workflow Optimization

### Concurrency Control

```yaml
concurrency:
  group: quality-gate-${{ github.ref }}
  cancel-in-progress: true
```

Cancels previous runs on the same branch, reducing wasted resources.

### Caching Strategies

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
    cache: 'pip'

- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### Timeout Configuration

```yaml
jobs:
  quick-checks:
    timeout-minutes: 3

  full-validation:
    timeout-minutes: 10

  production-gate:
    timeout-minutes: 5
```

## Rollback Procedures

### Automatic Rollback Conditions

1. **Staging validation fails:**
   - PR blocked from merging
   - Developer notified via PR comment
   - No automatic rollback needed (changes not merged)

2. **Production deployment fails:**
   - Revert PR from main to previous state
   - Or: `git revert HEAD && git push`

### Manual Rollback

```bash
# Revert last commit on main
git checkout main
git revert HEAD --no-edit
git push origin main

# Or revert to specific commit
git revert <commit-sha> --no-edit
git push origin main
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Skip All Validation

**What not to do:**
```yaml
# DON'T add skip options that bypass all validation
if: "!contains(github.event.head_commit.message, '[skip ci]')"
```

**Why:** Opens door to unvalidated code reaching production.

### Anti-Pattern 2: Long-Running Sequential Jobs

**What not to do:**
```yaml
# DON'T run everything sequentially when parallel is possible
steps:
  - run: validate agents  # 2 min
  - run: validate skills  # 3 min
  - run: validate commands  # 1 min
  # Total: 6 minutes sequential
```

**Better:** Use matrix or parallel jobs for independent validations.

### Anti-Pattern 3: Ignoring Failures

**What not to do:**
```yaml
# DON'T ignore all failures
continue-on-error: true  # On critical validation
```

**Better:** Only use `continue-on-error` for informational checks.

## Tools and Resources

### Validation Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate_all_agents.sh` | Validate all 28 agents | `bash scripts/validate_all_agents.sh` |
| `validate_all_skills.py` | Validate all 29 skills | `python3 scripts/validate_all_skills.py` |
| `validate_all_commands.py` | Validate all 14 commands | `python3 scripts/validate_all_commands.py` |
| `test_all_python_tools.py` | Test CLI compliance | `python3 scripts/test_all_python_tools.py` |
| `validate_cross_references.py` | Check agent↔skill links | `python3 scripts/validate_cross_references.py` |

### Recommended Tools

- **yamllint:** YAML syntax validation
- **safety:** Python dependency security scanning
- **gitleaks:** Secrets detection in commits
- **act:** Local GitHub Actions testing

## Conclusion

Key takeaways for effective CI/CD in this repository:

1. **Progressive validation:** Increase rigor as code moves toward production
2. **Incremental checking:** Fast feedback on develop, full validation on staging
3. **Branch protection:** Enforce quality gates at each promotion point
4. **Security integration:** Scan dependencies and secrets before production
5. **Optimization:** Use caching, concurrency, and parallel jobs
6. **Clear ownership:** Each branch has specific validation requirements

---

**Last Updated:** November 27, 2025
**Version:** 1.0
