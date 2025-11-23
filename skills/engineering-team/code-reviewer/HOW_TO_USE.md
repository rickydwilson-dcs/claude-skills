# How to Use the Code Reviewer Skill

## Quick Start

Hey Claude—I just added the "code-reviewer" skill. Can you review this pull request?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "code-reviewer" skill. Can you review this pull request?
```

### Example 2: Specific Workflow
```
Hey Claude—I just added the "code-reviewer" skill. Can you help me with pull request review?
```

### Example 3: Integration with Other Skills
```
Hey Claude—I just added the "code-reviewer" skill. Can you use it together with related skills to deliver a complete solution?
```

## What to Provide

When using this skill, provide:

- **Primary Input**: Describe what you need help with
- **Context** (optional): Background information, constraints
- **Preferences** (optional): Specific approaches or requirements

## What You'll Get

This skill will provide:

- **Code Review**: Detailed analysis of code quality, patterns, issues
- **Improvement Suggestions**: Specific recommendations with examples
- **Best Practices**: Guidance on industry standards
- **Automated Tools**: 3 Python scripts for data processing and analysis

## Python Tools Available

This skill includes the following Python tools:

- **code_quality_checker.py**: Code Quality Checker
- **pr_analyzer.py**: Pr Analyzer
- **review_report_generator.py**: Review Report Generator

You can run these tools directly:

```bash
python skills/engineering-team/code-reviewer/scripts/code_quality_checker.py --help
```

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements for better results
2. **Provide Context**: Include relevant background information about your project
3. **Iterate**: Start with a focused request, then refine based on initial results
4. **Combine Skills**: This skill works well with other engineering skills for comprehensive solutions

## Related Skills

Consider using these skills together:

- **[Senior Security](../../engineering-team/senior-security/)**: Complementary expertise for senior security tasks
- **[Senior Frontend](../../engineering-team/senior-frontend/)**: Complementary expertise for senior frontend tasks
- **[Senior Secops](../../engineering-team/senior-secops/)**: Complementary expertise for senior secops tasks

---

**Skill**: code-reviewer
**Domain**: engineering-team
**Version**: 1.0.0
**Last Updated**: 2025-11-23
