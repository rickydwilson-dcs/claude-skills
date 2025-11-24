---
name: review.code-pr
description: Performs comprehensive code review with quality analysis
category: review
pattern: multi-phase
version: 1.0.0
author: Claude Skills Team
tags: [code-review, quality, analysis]
model_preference: sonnet
---

# Code Review Command

## Usage

```bash
/review.code-pr [pull-request-number]
```

### Arguments

- `pull-request-number` - GitHub PR number to review (required)

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Gather PR information and analyze changed files

**Steps:**
1. Fetch PR metadata from GitHub
2. Identify all changed files
3. Categorize changes by type (feature, bugfix, refactor, docs)

### Phase 2: Analysis

**Goal:** Perform comprehensive code quality analysis

**Steps:**
1. Analyze code changes for best practices
2. Check for performance issues
3. Review security implications
4. Verify test coverage

### Phase 3: Task Execution

**Goal:** Generate detailed review findings

**Steps:**
1. Document all findings
2. Categorize by severity
3. Provide actionable recommendations

### Phase 4: Reporting

**Goal:** Present comprehensive review report

**Report Includes:**
- Summary of findings
- Detailed issues with locations
- Recommendations for improvement
- Estimated effort to address

## Examples

### Example 1: Basic PR Review

```bash
/review.code-pr 123
```

This performs a complete code review of PR #123.

### Example 2: With Options

```bash
/review.code-pr 123 --detailed
```

This performs a detailed review with verbose output.

## Error Handling

### Common Issue: PR Not Found

**Issue:** Pull request number doesn't exist

**Cause:** Invalid PR number provided

**Solution:** Verify the PR number exists on GitHub

**Prevention:** Check GitHub before running command

### Common Issue: Insufficient Permissions

**Issue:** Cannot access private repository

**Cause:** Authentication token lacks required permissions

**Solution:** Update GitHub token with appropriate scopes

**Prevention:** Verify token permissions before running

## Success Criteria

This command is successful when:

- [ ] All changed files are analyzed
- [ ] Quality issues are identified
- [ ] Recommendations are provided
- [ ] Report is generated
