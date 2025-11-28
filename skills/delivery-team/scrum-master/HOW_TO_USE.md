# How to Use the Scrum Master Skill

## Quick Start

Hey Claude—I just added the "scrum-master" skill. Can you facilitate sprint planning?

## Example Invocations

### Example 1: Sprint Planning
```
Hey Claude—I just added the "scrum-master" skill. Can you help me plan our next sprint?
We have a team velocity of 30 points and need to prioritize 15 backlog items.
```

### Example 2: Sprint Retrospective
```
Hey Claude—I just added the "scrum-master" skill. We're running a retrospective for
8 people with 90 minutes available. The sprint was tough - health score was 65.
What format do you recommend?
```

### Example 3: Velocity Analysis
```
Hey Claude—I just added the "scrum-master" skill. Our last 5 sprints completed
23, 25, 21, 28, and 24 story points. Can you analyze our velocity trends?
```

## What to Provide

When using this skill, provide:

- **Project Context**: Team size, sprint length, current ceremonies
- **Historical Data**: Velocity history, completion rates
- **Goals** (optional): What you want to optimize (velocity, predictability, team health)

## What You'll Get

This skill will provide:

- **Analysis**: Sprint metrics, velocity trends, health scores
- **Recommendations**: Backlog prioritization, format recommendations
- **Deliverables**: Sprint plans, ceremony guides, MCP commands for Jira
- **Automated Tools**: 4 Python scripts for metrics, prioritization, and facilitation

## Python Tools Available

This skill includes the following Python tools:

- **sprint_metrics_calculator.py**: 6-metric sprint health analysis with velocity trends
- **prioritize_backlog.py**: Value/effort/risk backlog prioritization with sprint allocation
- **sprint_backlog_optimizer.py**: RICE-integrated sprint planning with MCP commands
- **retro_format_selector.py**: Intelligent retrospective format recommendation

Run any tool with `--help` for detailed usage:

```bash
python skills/delivery-team/scrum-master/scripts/sprint_metrics_calculator.py --help
python skills/delivery-team/scrum-master/scripts/prioritize_backlog.py --help
python skills/delivery-team/scrum-master/scripts/sprint_backlog_optimizer.py --help
python skills/delivery-team/scrum-master/scripts/retro_format_selector.py --help
```

## Example Workflows

### Complete Sprint Planning Workflow

```bash
# 1. Analyze velocity from past sprints
python skills/delivery-team/scrum-master/scripts/sprint_metrics_calculator.py --velocity 23 25 21 28 24 --committed 25 --completed 21 --capacity 25

# 2. Prioritize backlog using value/effort/risk
python skills/delivery-team/scrum-master/scripts/prioritize_backlog.py backlog.json --capacity 30 --quick-wins

# 3. Optimize for sprint with RICE integration (optional)
python skills/delivery-team/scrum-master/scripts/sprint_backlog_optimizer.py rice_output.json --velocity 30 --sprint-goal "Improve auth" --sprint-name "Sprint 24"

# 4. Use generated MCP commands to create Jira sprint
```

### Retrospective Facilitation Workflow

```bash
# 1. Get format recommendation based on context
python skills/delivery-team/scrum-master/scripts/retro_format_selector.py --team-size 8 --time 90 --focus technical --health-score 65 --output-guide

# 2. Review facilitation guide and prepare materials
# 3. Run retro following the recommended format
# 4. Document action items in Confluence (via MCP)
```

### Sprint Health Analysis Workflow

```bash
# Full sprint analysis with 6-metric health score
python skills/delivery-team/scrum-master/scripts/sprint_metrics_calculator.py \
  --velocity 23 25 21 28 24 \
  --committed 25 --completed 21 \
  --capacity 25 \
  --blockers 2 --morale 7 \
  --json > sprint_health.json
```

## Tips for Best Results

1. **Use Historical Data**: Provide at least 3-5 sprints of velocity data for accurate trends
2. **Include Team Context**: Team size, blockers, and morale affect health scores
3. **Combine Tools**: Use metrics output to inform prioritization and retro format selection
4. **Iterate**: Start with metrics analysis, then prioritize, then plan
5. **Integrate with MCP**: Use generated MCP commands for Jira/Confluence automation

## Related Skills

Consider using these skills together:

- **[Senior PM](../../delivery-team/senior-pm/)**: Portfolio management and stakeholder reporting
- **[Confluence Expert](../../delivery-team/confluence-expert/)**: Sprint documentation and retrospective notes
- **[Jira Expert](../../delivery-team/jira-expert/)**: Board configuration and workflow automation
- **[Product Manager Toolkit](../../product-team/product-manager-toolkit/)**: RICE prioritization integration

---

**Skill**: scrum-master
**Domain**: delivery-team
**Version**: 1.1.0
**Last Updated**: 2025-11-28
