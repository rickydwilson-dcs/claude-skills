# How to Use the Jira Expert Skill

## Quick Start

Hey Claude—I just added the "jira-expert" skill. Can you set up a custom workflow?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "jira-expert" skill. Can you set up a custom workflow?
```

### Example 2: Specific Workflow
```
Hey Claude—I just added the "jira-expert" skill. Can you provide a comprehensive analysis?
```

### Example 3: Integration with Other Skills
```
Hey Claude—I just added the "jira-expert" skill. Can you use it together with related skills to deliver a complete solution?
```

## What to Provide

When using this skill, provide:

- **Project Context**: Team structure, workflow needs
- **Current Setup** (optional): Existing configurations
- **Goals** (optional): What you want to optimize

## What You'll Get

This skill will provide:

- **Analysis**: Comprehensive evaluation of your request
- **Recommendations**: Actionable guidance and best practices
- **Deliverables**: Formatted outputs and documentation
- **Automated Tools**: 1 Python scripts for data processing and analysis

## Python Tools Available

This skill includes the following Python tools:

- **jql_query_builder.py**: JQL Query Builder - Jira Query Language Generator

You can run these tools directly:

```bash
python skills/delivery-team/jira-expert/scripts/jql_query_builder.py --help
```

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements for better results
2. **Provide Context**: Include relevant background information about your project
3. **Iterate**: Start with a focused request, then refine based on initial results
4. **Combine Skills**: This skill works well with other delivery skills for comprehensive solutions

## Related Skills

Consider using these skills together:

- **[Scrum Master](../../delivery-team/scrum-master/)**: Complementary expertise for scrum master tasks
- **[Senior Pm](../../delivery-team/senior-pm/)**: Complementary expertise for senior pm tasks
- **[Confluence Expert](../../delivery-team/confluence-expert/)**: Complementary expertise for confluence expert tasks

---

**Skill**: jira-expert
**Domain**: delivery-team
**Version**: 1.0.0
**Last Updated**: 2025-11-23
