# CTO Python Tools Documentation

Comprehensive guide to CTO advisory Python tools for technical debt analysis and team scaling.

## Tech Debt Analyzer

**Script:** `scripts/tech_debt_analyzer.py`

### Purpose

Analyzes technical debt across five critical dimensions:
- Architecture debt (monolithic design, tight coupling)
- Code quality debt (test coverage, complexity)
- Infrastructure debt (deployments, CI/CD)
- Security debt (dependencies, vulnerabilities)
- Performance debt (response times, optimization)

Provides debt scoring, prioritized recommendations, and reduction timeline planning.

### Installation

```bash
# No additional dependencies required (uses Python standard library)
python --version  # Requires Python 3.8+
```

### Input Format

The tool accepts JSON input with system assessment data:

```json
{
  "name": "Legacy E-commerce Platform",
  "architecture": {
    "monolithic_design": 80,
    "tight_coupling": 70,
    "no_microservices": 90
  },
  "code_quality": {
    "low_test_coverage": 75,
    "high_complexity": 65,
    "poor_documentation": 60
  },
  "infrastructure": {
    "manual_deployments": 70,
    "no_ci_cd": 60,
    "outdated_tools": 50
  },
  "security": {
    "outdated_dependencies": 85,
    "no_security_scans": 70,
    "missing_authentication": 40
  },
  "performance": {
    "slow_response_times": 60,
    "no_caching": 50,
    "unoptimized_queries": 65
  },
  "team_size": 8,
  "system_criticality": "high",
  "business_context": {
    "growth_phase": "rapid",
    "compliance_required": true
  }
}
```

### Field Definitions

**Debt Category Scores (0-100)**
- Score represents severity/presence of technical debt
- Higher scores = more severe debt
- 0 = no debt, 100 = critical debt
- Each category contains 2-3 specific debt indicators

**architecture**
- `monolithic_design`: Degree of monolithic architecture (vs microservices)
- `tight_coupling`: Level of component coupling
- `no_microservices`: Lack of service decomposition
- Optional: `poor_scalability`, `legacy_patterns`

**code_quality**
- `low_test_coverage`: Insufficient automated testing
- `high_complexity`: Code complexity and maintainability issues
- `poor_documentation`: Missing or outdated documentation
- Optional: `code_duplication`, `inconsistent_standards`

**infrastructure**
- `manual_deployments`: Lack of deployment automation
- `no_ci_cd`: Missing continuous integration/deployment
- `outdated_tools`: Legacy infrastructure tools
- Optional: `no_monitoring`, `poor_scalability`

**security**
- `outdated_dependencies`: Vulnerable or unmaintained dependencies
- `no_security_scans`: Lack of security testing
- `missing_authentication`: Security control gaps
- Optional: `unencrypted_data`, `compliance_issues`

**performance**
- `slow_response_times`: Performance bottlenecks
- `no_caching`: Missing caching strategies
- `unoptimized_queries`: Database/query inefficiencies
- Optional: `memory_leaks`, `resource_waste`

**Context Information**
- `team_size`: Number of engineers maintaining the system
- `system_criticality`: "low", "medium", "high", "critical"
- `business_context`:
  - `growth_phase`: "startup", "growth", "rapid", "mature"
  - `compliance_required`: true/false (affects security priority)

### Usage Examples

**Basic Analysis (Human-Readable Output)**
```bash
python scripts/tech_debt_analyzer.py system_data.json
```

Output includes:
- Overall debt score and level
- Category-by-category breakdown
- Prioritized recommendations
- Reduction timeline
- Risk assessment

**JSON Output (For Dashboards/Integration)**
```bash
python scripts/tech_debt_analyzer.py system_data.json --output json
```

Returns structured JSON with all analysis results.

**Save to File**
```bash
python scripts/tech_debt_analyzer.py system_data.json -o json -f debt_report.json
```

**View Help and Schema**
```bash
python scripts/tech_debt_analyzer.py --help
```

### Output Interpretation

**Debt Levels**
- **Critical (>80)**: Urgent attention required, high risk
- **High (60-80)**: Significant debt, prioritize remediation
- **Medium (40-60)**: Manageable, plan reduction
- **Low (<40)**: Acceptable level, monitor

**Capacity Allocation Recommendations**
- Critical debt: 40% engineering capacity
- High debt: 25% engineering capacity
- Medium debt: 15% engineering capacity
- Low debt: 10% ongoing maintenance

**Priority Framework**
1. **P0 (Critical)**: Security vulnerabilities, system instability
2. **P1 (High)**: Performance issues, scalability blockers
3. **P2 (Medium)**: Code quality, maintainability
4. **P3 (Low)**: Nice-to-haves, optimizations

### Example Analysis Session

```bash
# 1. Create input file for legacy system
cat > legacy_system.json << 'EOF'
{
  "name": "Legacy E-commerce Platform",
  "architecture": {"monolithic_design": 80, "tight_coupling": 70, "no_microservices": 90},
  "code_quality": {"low_test_coverage": 75, "high_complexity": 65},
  "infrastructure": {"manual_deployments": 70, "no_ci_cd": 60},
  "security": {"outdated_dependencies": 85, "no_security_scans": 70},
  "performance": {"slow_response_times": 60, "no_caching": 50},
  "team_size": 8,
  "system_criticality": "high",
  "business_context": {"growth_phase": "rapid", "compliance_required": true}
}
EOF

# 2. Run analysis
python scripts/tech_debt_analyzer.py legacy_system.json

# 3. Generate JSON for executive dashboard
python scripts/tech_debt_analyzer.py legacy_system.json -o json -f exec_report.json

# 4. Review results
cat exec_report.json | python -m json.tool
```

### Reduction Planning

**Quarter 1: Critical Issues**
- Address security vulnerabilities
- Implement basic CI/CD
- Add monitoring and alerting

**Quarter 2: High Priority**
- Increase test coverage to 60%
- Decompose into 2-3 services
- Implement caching layer

**Quarter 3: Medium Priority**
- Refactor high-complexity modules
- Complete documentation
- Performance optimization

**Quarter 4: Ongoing**
- Maintain test coverage >70%
- Continue service decomposition
- Monitor and prevent new debt

## Team Scaling Calculator

**Script:** `scripts/team_scaling_calculator.py`

### Purpose

Calculates optimal engineering team scaling strategy including:
- Hiring timeline and velocity
- Team structure and roles
- Budget projections
- Onboarding capacity
- Productivity impact analysis
- Risk assessment

### Installation

```bash
# No additional dependencies required (uses Python standard library)
python --version  # Requires Python 3.8+
```

### Input Format

```json
{
  "current_state": {
    "headcount": 25,
    "velocity": 450,
    "roles": {
      "engineering_manager": 2,
      "senior_engineer": 8,
      "mid_engineer": 10,
      "junior_engineer": 5
    },
    "attrition_rate": 12,
    "location": "US"
  },
  "growth_targets": {
    "target_headcount": 75,
    "timeline_quarters": 4,
    "priority_roles": ["senior_engineer", "engineering_manager"]
  },
  "constraints": {
    "max_hires_per_quarter": 15,
    "onboarding_capacity": 5,
    "budget_per_quarter": 2000000
  }
}
```

### Field Definitions

**current_state**
- `headcount`: Current number of engineers
- `velocity`: Current sprint velocity (story points/sprint)
- `roles`: Breakdown by role/level
  - `engineering_manager`: EM count
  - `senior_engineer`: Senior IC count
  - `mid_engineer`: Mid-level IC count
  - `junior_engineer`: Junior IC count
  - `staff_engineer`: Staff+ IC count (optional)
- `attrition_rate`: Annual attrition percentage
- `location`: Primary location (affects cost estimates)
  - Options: "US", "EU", "APAC", "Remote"

**growth_targets**
- `target_headcount`: Desired final headcount
- `timeline_quarters`: Number of quarters to reach target
- `priority_roles`: Array of roles to prioritize in hiring

**constraints** (optional)
- `max_hires_per_quarter`: Hiring velocity limit
- `onboarding_capacity`: Max simultaneous onboardings
- `budget_per_quarter`: Quarterly budget in dollars

### Usage Examples

**Basic Analysis**
```bash
python scripts/team_scaling_calculator.py team_data.json
```

**JSON Output**
```bash
python scripts/team_scaling_calculator.py team_data.json --output json
```

**Save Plan**
```bash
python scripts/team_scaling_calculator.py team_data.json -o json -f scaling_plan.json
```

**View Help**
```bash
python scripts/team_scaling_calculator.py --help
```

### Output Interpretation

**Hiring Plan**
- Quarter-by-quarter hiring targets
- Role distribution per quarter
- Cumulative headcount growth
- Budget requirements

**Team Structure**
- Recommended org structure
- Manager-to-engineer ratios
- Senior-to-junior ratios
- Specialization recommendations

**Productivity Analysis**
- Expected velocity changes
- Ramp-up timeline per role
- Aggregate productivity impact
- Break-even point

**Risk Assessment**
- Attrition impact modeling
- Onboarding capacity constraints
- Budget overrun risks
- Quality concerns with rapid growth

### Example Scenarios

**Rapid Growth Scenario**
```bash
cat > rapid_growth.json << 'EOF'
{
  "current_state": {
    "headcount": 25,
    "velocity": 450,
    "roles": {"engineering_manager": 2, "senior_engineer": 8, "mid_engineer": 10, "junior_engineer": 5},
    "attrition_rate": 12,
    "location": "US"
  },
  "growth_targets": {
    "target_headcount": 75,
    "timeline_quarters": 4
  }
}
EOF

python scripts/team_scaling_calculator.py rapid_growth.json
```

**Controlled Growth Scenario**
```bash
cat > controlled_growth.json << 'EOF'
{
  "current_state": {
    "headcount": 25,
    "velocity": 450,
    "roles": {"engineering_manager": 2, "senior_engineer": 8, "mid_engineer": 10, "junior_engineer": 5},
    "attrition_rate": 8,
    "location": "Remote"
  },
  "growth_targets": {
    "target_headcount": 40,
    "timeline_quarters": 4,
    "priority_roles": ["senior_engineer"]
  },
  "constraints": {
    "max_hires_per_quarter": 5,
    "onboarding_capacity": 3
  }
}
EOF

python scripts/team_scaling_calculator.py controlled_growth.json
```

### Hiring Velocity Guidelines

**Conservative (Safe)**
- 10-15% headcount growth per quarter
- 2-3 simultaneous onboardings
- High senior-to-junior ratio (50%+ senior)

**Moderate (Balanced)**
- 20-25% headcount growth per quarter
- 4-5 simultaneous onboardings
- Balanced ratios (30% senior, 50% mid, 20% junior)

**Aggressive (Risky)**
- 30%+ headcount growth per quarter
- 6+ simultaneous onboardings
- More junior-heavy to scale faster
- Requires strong onboarding program

### Budget Estimation

**US Market (2024 Estimates)**
- Junior Engineer: $120-150K total comp
- Mid Engineer: $150-200K total comp
- Senior Engineer: $180-250K total comp
- Staff+ Engineer: $220-350K total comp
- Engineering Manager: $180-280K total comp

**Multipliers by Location**
- Remote (US): 0.9x
- EU: 0.7-0.8x
- APAC: 0.5-0.7x

**Additional Costs**
- Recruiting: $25-30K per hire
- Onboarding: $10-15K per hire
- Tools/equipment: $5-10K per person/year
- Training: $2-5K per person/year

## Integration Workflows

### Quarterly Planning Workflow

```bash
# 1. Assess technical debt
python scripts/tech_debt_analyzer.py current_systems.json -o json -f debt_q4.json

# 2. Calculate team scaling needs
python scripts/team_scaling_calculator.py team_targets.json -o json -f hiring_q4.json

# 3. Allocate capacity based on debt level
# High debt = 25% capacity → Factor into velocity planning

# 4. Create quarterly OKRs incorporating both insights
# - Debt reduction goals
# - Team growth milestones
# - Delivery targets adjusted for onboarding
```

### Board Presentation Workflow

```bash
# 1. Generate tech debt dashboard
python scripts/tech_debt_analyzer.py production_systems.json -o json

# 2. Generate hiring plan
python scripts/team_scaling_calculator.py scaling_plan.json -o json

# 3. Use outputs in board deck:
# - Slide 5: Technical health (debt scores)
# - Slide 8: Team growth plan (hiring timeline)
# - Slide 10: Budget (hiring costs + debt remediation)
```

### Architecture Review Workflow

```bash
# 1. Before major refactoring - baseline assessment
python scripts/tech_debt_analyzer.py system_before.json -o json -f baseline.json

# 2. After refactoring - measure improvement
python scripts/tech_debt_analyzer.py system_after.json -o json -f after.json

# 3. Calculate debt reduction
# Compare scores, validate capacity investment ROI
```

## Best Practices

### Technical Debt Analysis

**Regular Cadence**
- Run analysis quarterly
- Track trends over time
- Celebrate debt reduction
- Prevent new debt accumulation

**Honest Assessment**
- Don't underestimate debt scores
- Include team in assessment
- Use objective metrics where possible
- Document assumptions

**Action-Oriented**
- Convert analysis to OKRs
- Assign ownership
- Track progress
- Adjust capacity allocation

### Team Scaling

**Plan Ahead**
- Start hiring 6 months before need
- Account for ramp-up time
- Build hiring pipeline early
- Over-communicate needs

**Hire for Diversity**
- Experience levels (senior + mid)
- Backgrounds and perspectives
- Skills and specializations
- Remote vs on-site

**Onboarding Excellence**
- Structured 90-day plan
- Buddy system
- Clear first tasks
- Regular check-ins

**Monitor Ratios**
- Manager : Engineer (1:7-10)
- Senior : Mid : Junior (3:5:2)
- Stay within healthy ranges
- Adjust as needed

## Troubleshooting

### Common Issues

**Issue: "File not found" error**
```bash
# Solution: Use absolute path or verify location
python scripts/tech_debt_analyzer.py /full/path/to/data.json
```

**Issue: "Invalid JSON" error**
```bash
# Solution: Validate JSON syntax
python -m json.tool your_file.json
# Fix any syntax errors shown
```

**Issue: Unexpected debt scores**
```bash
# Solution: Verify input ranges
# - Debt scores should be 0-100
# - Higher = more severe debt
# Review each category for accuracy
```

**Issue: Scaling plan seems unrealistic**
```bash
# Solution: Adjust constraints
# - Lower max_hires_per_quarter
# - Extend timeline_quarters
# - Increase onboarding_capacity if possible
```

### Getting Help

```bash
# View detailed help
python scripts/tech_debt_analyzer.py --help
python scripts/team_scaling_calculator.py --help

# Check Python version
python --version  # Should be 3.8+

# Verify script location
ls -la scripts/*.py
```

## Tool Comparison

| Feature | Tech Debt Analyzer | Team Scaling Calculator |
|---------|-------------------|------------------------|
| **Primary Use** | System health assessment | Hiring planning |
| **Input Type** | System metrics | Team metrics |
| **Output** | Debt scores + recommendations | Hiring plan + budget |
| **Time Horizon** | Current state + next 2-4 quarters | 1-2 years |
| **Best For** | Quarterly reviews, refactor planning | Annual planning, budgeting |
| **Update Frequency** | Quarterly | Bi-annually or as needed |
| **Stakeholders** | Engineering team, CTO | CTO, CFO, CEO, HR |

## Advanced Usage

### Batch Processing

```bash
# Process multiple systems
for file in systems/*.json; do
    python scripts/tech_debt_analyzer.py "$file" -o json -f "results/$(basename $file)"
done

# Process multiple team scenarios
for scenario in scenarios/*.json; do
    python scripts/team_scaling_calculator.py "$scenario" -o json -f "plans/$(basename $scenario)"
done
```

### Trend Analysis

```bash
# Track debt over time
python scripts/tech_debt_analyzer.py q1_data.json -o json -f debt_q1.json
python scripts/tech_debt_analyzer.py q2_data.json -o json -f debt_q2.json
python scripts/tech_debt_analyzer.py q3_data.json -o json -f debt_q3.json
python scripts/tech_debt_analyzer.py q4_data.json -o json -f debt_q4.json

# Compare trends with custom script
python analysis/compare_trends.py debt_q*.json
```

### Integration with Dashboards

```python
import json
import subprocess

# Run analysis programmatically
result = subprocess.run(
    ['python', 'scripts/tech_debt_analyzer.py', 'data.json', '-o', 'json'],
    capture_output=True,
    text=True
)

debt_data = json.loads(result.stdout)

# Push to dashboard
dashboard_api.update_metrics('tech_debt', debt_data)
```

## Data Privacy & Security

- All processing is local (no external API calls)
- No data transmitted to external services
- Input files may contain sensitive team/system data
- Recommended: Encrypt storage, restrict file permissions
- Add to .gitignore if version controlling

```bash
# Secure file permissions
chmod 600 system_data.json
chmod 600 team_data.json

# Add to .gitignore
echo "*_data.json" >> .gitignore
echo "team_*.json" >> .gitignore
echo "system_*.json" >> .gitignore
```

## Real-World Examples

### Example 1: Legacy System Modernization

**Scenario**: E-commerce platform built in 2015, 8-person team

```bash
# Initial assessment
python scripts/tech_debt_analyzer.py legacy_platform.json

# Results showed:
# - Overall debt: 72 (High)
# - Critical: Security (85), Architecture (80)
# - Recommendation: 25% capacity to debt reduction

# Quarterly progress
python scripts/tech_debt_analyzer.py legacy_platform_q2.json
# Debt reduced to 61 (Medium-High)

python scripts/tech_debt_analyzer.py legacy_platform_q4.json
# Debt reduced to 48 (Medium)
```

### Example 2: Hyper-Growth Startup

**Scenario**: Series B startup scaling from 25 to 75 engineers in 12 months

```bash
# Initial planning
python scripts/team_scaling_calculator.py hyper_growth.json

# Results:
# - Q1: Hire 8 (3 senior, 4 mid, 1 EM)
# - Q2: Hire 12 (2 senior, 7 mid, 3 junior)
# - Q3: Hire 15 (3 senior, 9 mid, 3 junior)
# - Q4: Hire 10 (2 senior, 6 mid, 2 junior)
# - Budget: $18M over 4 quarters
# - Risk: High (onboarding capacity stretched)

# Adjusted to controlled growth
# Reduced to 50 engineers over 18 months
# Lower risk, better quality outcomes
```
