# How to Use the Cto Advisor Skill

## Quick Start

Hey Claude—I just added the "cto-advisor" skill. Can you analyze my current codebase?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "cto-advisor" skill. Can you analyze my current codebase?
```

### Example 2: Specific Workflow
```
Hey Claude—I just added the "cto-advisor" skill. Can you help me with comprehensive technical debt assessment?
```

### Example 3: Integration with Other Skills
```
Hey Claude—I just added the "cto-advisor" skill. Can you use it together with related skills to deliver a complete solution?
```

## What to Provide

When using this skill, provide:

- **Primary Input**: Describe what you need help with
- **Context** (optional): Background information, constraints
- **Preferences** (optional): Specific approaches or requirements

## What You'll Get

This skill will provide:

- **Analysis**: Comprehensive evaluation of your request
- **Recommendations**: Actionable guidance and best practices
- **Deliverables**: Formatted outputs and documentation
- **Automated Tools**: 2 Python scripts for data processing and analysis

## Python Tools Available

This skill includes the following Python tools:

- **team_scaling_calculator.py**: Engineering Team Scaling Calculator - Optimize team growth and structure
- **tech_debt_analyzer.py**: Technical Debt Analyzer - Assess and prioritize technical debt across systems

You can run these tools directly:

```bash
python skills/engineering-team/cto-advisor/scripts/team_scaling_calculator.py --help
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

**Skill**: cto-advisor
**Domain**: engineering-team
**Version**: 1.0.0
**Last Updated**: 2025-11-08
