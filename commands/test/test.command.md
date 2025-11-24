---
name: test.command
title: Sample Test Command
description: A sample command for testing the command builder validation
category: test
subcategory: validation
difficulty: beginner
time-saved: "5 minutes per use"
frequency: "As-needed"
use-cases:
  - "Testing command builder validation functionality"
  - "Demonstrating proper command structure"
dependencies:
  tools:
    - Read
    - Write
  scripts: []
  python-packages: []
compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows
examples:
  - title: "Basic Usage"
    input: "/test.command"
    output: "Command executed successfully"
  - title: "Advanced Usage"
    input: "/test.command --verbose"
    output: "Command executed with detailed output"
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
  - test
  - validation
  - sample
featured: false
verified: true
license: MIT
---

# Sample Test Command

This is a sample command for testing the command builder validation system.

---

## Usage

```bash
/test.command [options]
```

### Arguments

- `--verbose` - Enable verbose output (optional)

### Examples

```bash
# Basic usage
/test.command

# With verbose output
/test.command --verbose
```

---

## What This Command Does

### Context Gathering

The command will:
1. Read current project state
2. Verify command structure
3. Validate all required fields

### Task Execution

Then it will:
1. Execute sample validation logic
2. Generate sample output
3. Report results

### Expected Output

You will receive:
- Validation status
- Execution summary
- Sample results

**Output Location:** Console output
**Output Format:** markdown

---

## Error Handling

### Common Issues

**Issue:** Command not found
**Cause:** Command file missing or incorrectly named
**Solution:** Verify file exists at commands/test/test.command.md
**Prevention:** Use command builder to create commands

---

**Issue:** Invalid YAML frontmatter
**Cause:** Syntax errors in frontmatter
**Solution:** Validate YAML syntax
**Prevention:** Use command builder with validation

---

**Issue:** Missing required fields
**Cause:** Required metadata fields not provided
**Solution:** Add all required fields to frontmatter
**Prevention:** Follow command metadata schema

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-quality-engineer](../../agents/engineering/cs-quality-engineer.md)** - Validates command quality

### Related Skills

This command leverages:

- **[engineering-team/scaffolding](../../skills/engineering-team/scaffolding/)** - Uses scaffolding patterns

---

## Success Criteria

This command is successful when:

- [ ] All validation checks pass
- [ ] Output format is correct
- [ ] No errors during execution
- [ ] Results are comprehensive

### Quality Metrics

**Expected Outcomes:**
- Validation: 100% pass rate
- Execution time: < 5 seconds
- Output completeness: 100%

---

## Tips for Best Results

1. **Validation First**
   - Always validate before execution
   - Ensures proper structure

2. **Clear Inputs**
   - Provide specific arguments
   - Better results

3. **Review Output**
   - Check all sections
   - Verify completeness

---

## Related Commands

- `/workflow.validate-all` - Validates all commands
- `/code.review` - Reviews code quality

---

## References

- [Command Standards](../../docs/standards/command-standards.md) - Validation rules
- [Command Schema](../../schema/command-metadata-schema.md) - Metadata specification

---

**Last Updated:** 2025-11-24
**Version:** v1.0.0
**Maintained By:** Claude Skills Team
**Feedback:** Open an issue in the repository
