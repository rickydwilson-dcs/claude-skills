# How to Use the Business Analyst Toolkit Skill

## Quick Start

Hey Claude—I just added the "business-analyst-toolkit" skill. Can you analyze this dataset?

## Example Invocations

### Example 1: Basic Usage
```
Hey Claude—I just added the "business-analyst-toolkit" skill. Can you analyze this dataset?
```

### Example 2: Specific Workflow
```
Hey Claude—I just added the "business-analyst-toolkit" skill. Can you help me with [workflow name]?
```

### Example 3: Integration with Other Skills
```
Hey Claude—I just added the "business-analyst-toolkit" skill. Can you use it together with related skills to deliver a complete solution?
```

## What to Provide

When using this skill, provide:

- **Dataset**: Your data files (CSV, JSON, Excel) or database connection details
- **Context** (optional): Business objectives, key metrics of interest
- **Constraints** (optional): Performance requirements, data privacy considerations

## What You'll Get

This skill will provide:

- **Analysis Reports**: Statistical summaries, trend analysis, insights
- **Visualizations**: Charts and graphs showing key findings
- **Recommendations**: Data-driven action items
- **Automated Tools**: 7 Python scripts for data processing and analysis

## Python Tools Available

This skill includes the following Python tools:

- **charter_builder.py**: Charter Builder - Generate process improvement charters
- **gap_analyzer.py**: Gap Analyzer - Identify missing elements in process documentation
- **improvement_planner.py**: Improvement Planner - Generate process improvement plans from gap analysis
- **kpi_calculator.py**: KPI Calculator - Calculate process KPIs and efficiency metrics
- **process_parser.py**: Process Parser - Universal process documentation parser
- **raci_generator.py**: RACI Generator - Create RACI matrices from process documentation
- **stakeholder_mapper.py**: Stakeholder Mapper - Create stakeholder maps and engagement plans

You can run these tools directly:

```bash
python skills/product-team/business-analyst-toolkit/scripts/charter_builder.py --help
```

## Tips for Best Results

1. **Be Specific**: Provide clear, detailed requirements for better results
2. **Provide Context**: Include relevant background information about your project
3. **Iterate**: Start with a focused request, then refine based on initial results
4. **Combine Skills**: This skill works well with other product skills for comprehensive solutions

## Related Skills

Consider using these skills together:

- **[Agile Product Owner](../../product-team/agile-product-owner/)**: Complementary expertise for agile product owner tasks
- **[Product Manager Toolkit](../../product-team/product-manager-toolkit/)**: Complementary expertise for product manager toolkit tasks
- **[Product Strategist](../../product-team/product-strategist/)**: Complementary expertise for product strategist tasks

---

**Skill**: business-analyst-toolkit
**Domain**: product-team
**Version**: 1.0.0
**Last Updated**: 2025-11-23
