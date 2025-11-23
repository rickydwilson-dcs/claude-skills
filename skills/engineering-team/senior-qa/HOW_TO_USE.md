# How to Use the Senior Qa Skill

## Quick Start

Hey Claude—I just added the "senior-qa" skill. Can you create a test strategy?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "senior-qa" skill. Can you create a test strategy?
```

### Example 2: Specific Workflow
```
Hey Claude—I just added the "senior-qa" skill. Can you help me with design test strategy for new feature?
```

### Example 3: Integration with Other Skills
```
Hey Claude—I just added the "senior-qa" skill. Can you use it together with related skills to deliver a complete solution?
```

## What to Provide

When using this skill, provide:

- **Application Details**: What needs to be tested
- **Context** (optional): Test coverage goals, known issues
- **Preferences** (optional): Testing frameworks, automation level

## What You'll Get

This skill will provide:

- **Test Strategy**: Comprehensive testing approach
- **Test Cases**: Specific test scenarios and acceptance criteria
- **Automation Plan**: Framework recommendations and implementation guidance
- **Automated Tools**: 3 Python scripts for data processing and analysis

## Python Tools Available

This skill includes the following Python tools:

- **coverage_analyzer.py**: Coverage Analyzer
- **e2e_test_scaffolder.py**: E2E Test Scaffolder
- **test_suite_generator.py**: Test Suite Generator

You can run these tools directly:

```bash
python skills/engineering-team/senior-qa/scripts/coverage_analyzer.py --help
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

**Skill**: senior-qa
**Domain**: engineering-team
**Version**: 1.0.0
**Last Updated**: 2025-11-23
