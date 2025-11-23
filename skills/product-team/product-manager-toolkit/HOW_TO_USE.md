# How to Use the Product Manager Toolkit Skill

## Quick Start

Hey Claude—I just added the "product-manager-toolkit" skill. Can you help prioritize features?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "product-manager-toolkit" skill. Can you help prioritize features?
```

### Example 2: Specific Workflow
```
Hey Claude—I just added the "product-manager-toolkit" skill. Can you help me with [workflow name]?
```

### Example 3: Integration with Other Skills
```
Hey Claude—I just added the "product-manager-toolkit" skill. Can you use it together with related skills to deliver a complete solution?
```

## What to Provide

When using this skill, provide:

- **Product Context**: Product vision, target users
- **Goals** (optional): What you want to achieve
- **Constraints** (optional): Timeline, resources, market conditions

## What You'll Get

This skill will provide:

- **Product Strategy**: Roadmap, prioritization, success metrics
- **User Stories**: Well-defined requirements with acceptance criteria
- **Documentation**: PRDs, specifications, stakeholder communications
- **Automated Tools**: 2 Python scripts for data processing and analysis

## Python Tools Available

This skill includes the following Python tools:

- **customer_interview_analyzer.py**: Customer Interview Analyzer
- **rice_prioritizer.py**: RICE Prioritization Framework

You can run these tools directly:

```bash
python skills/product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py --help
```

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements for better results
2. **Provide Context**: Include relevant background information about your project
3. **Iterate**: Start with a focused request, then refine based on initial results
4. **Combine Skills**: This skill works well with other product skills for comprehensive solutions

## Related Skills

Consider using these skills together:

- **[Agile Product Owner](../../product-team/agile-product-owner/)**: Complementary expertise for agile product owner tasks
- **[Business Analyst Toolkit](../../product-team/business-analyst-toolkit/)**: Complementary expertise for business analyst toolkit tasks
- **[Product Strategist](../../product-team/product-strategist/)**: Complementary expertise for product strategist tasks

---

**Skill**: product-manager-toolkit
**Domain**: product-team
**Version**: 1.0.0
**Last Updated**: 2025-11-08
