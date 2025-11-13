# Research: Agent Completion for 26 Pandora Skills

**Date**: November 12, 2025
**Purpose**: Document findings from Phase 0 research to inform agent creation

## Executive Summary

**Current State**: 8 agents (3 marketing, 5 product)
**Target State**: 26 agents (1:1 coverage with skills)
**Agents to Build**: 18 new agents (4 delivery, 14 engineering)

**Key Findings**:
- Existing agents show 100% consistency in structure (4 workflows each, identical path patterns)
- Delivery team skills have 0 Python tools (MCP-driven)
- Engineering team skills have 45 Python tools total (3 per skill average)
- All existing agents use ../../skills/ path pattern with no exceptions
- Template compliance: 100% adherence to agent-template.md structure

## Skill-to-Agent Mapping Table

| Domain | Skill Name | Agent Needed | Status | Python Tools | Workflows Identified |
|--------|-----------|--------------|--------|--------------|---------------------|
| **Marketing** | content-creator | cs-content-creator.md | ✅ EXISTS | 3 | 4 |
| **Marketing** | demand-gen-specialist | cs-demand-gen-specialist.md | ✅ EXISTS | 3 | 4 |
| **Marketing** | product-marketer | cs-product-marketer.md | ✅ EXISTS | 3 | 4 |
| **Product** | product-manager | cs-product-manager.md | ✅ EXISTS | 3 | 4 |
| **Product** | agile-product-owner | cs-agile-product-owner.md | ✅ EXISTS | 3 | 4 |
| **Product** | product-strategist | cs-product-strategist.md | ✅ EXISTS | 3 | 4 |
| **Product** | ux-researcher | cs-ux-researcher.md | ✅ EXISTS | 3 | 4 |
| **Product** | ui-designer | cs-ui-designer.md | ✅ EXISTS | 3 | 4 |
| **Delivery** | jira-expert | cs-jira-expert.md | ❌ NEW | 0 (MCP) | 5 |
| **Delivery** | confluence-expert | cs-confluence-expert.md | ❌ NEW | 0 (MCP) | 5 |
| **Delivery** | scrum-master | cs-scrum-master.md | ❌ NEW | 0 | 6 |
| **Delivery** | senior-pm | cs-senior-pm.md | ❌ NEW | 0 | 5 |
| **Engineering** | code-reviewer | cs-code-reviewer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-architect | cs-architect.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-backend | cs-backend-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-frontend | cs-frontend-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-fullstack | cs-fullstack-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-devops | cs-devops-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-security | cs-security-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-secops | cs-secops-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-qa | cs-qa-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-ml-engineer | cs-ml-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-data-engineer | cs-data-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-data-scientist | cs-data-scientist.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-computer-vision | cs-computer-vision.md | ❌ NEW | 3 | 5 |
| **Engineering** | senior-prompt-engineer | cs-prompt-engineer.md | ❌ NEW | 3 | 5 |
| **Engineering** | cto-advisor | cs-cto-advisor.md | ❌ NEW | 2 | 6 |

**Totals**: 26 skills → 26 agents (8 exist, 18 to build)

## Tool Inventory by Domain

### Delivery Team Skills (0 Python Tools)

**jira-expert**:
- No Python tools
- Uses Atlassian MCP Server for all Jira operations
- Primary workflows: Issue creation, sprint planning, backlog grooming, board management, reporting

**confluence-expert**:
- No Python tools
- Uses Atlassian MCP Server for all Confluence operations
- Primary workflows: Page creation, template usage, documentation management, team collaboration, knowledge sharing

**scrum-master**:
- No Python tools
- Process-driven workflows (facilitation, ceremonies, metrics tracking)
- Primary workflows: Sprint planning, daily standups, retrospectives, backlog refinement, team velocity, impediment resolution

**senior-pm**:
- No Python tools
- Strategic planning and coordination workflows
- Primary workflows: Roadmap development, stakeholder management, resource planning, cross-team coordination, delivery tracking

### Engineering Team Skills (45 Python Tools)

**code-reviewer** (3 tools):
1. `review_generator.py` - Generates code review checklists
2. `complexity_analyzer.py` - Analyzes code complexity metrics
3. `best_practices_checker.py` - Validates against standards

**senior-architect** (3 tools):
1. `system_design_generator.py` - Creates architecture diagrams
2. `tech_stack_analyzer.py` - Evaluates technology choices
3. `scalability_calculator.py` - Estimates scaling requirements

**senior-backend** (3 tools):
1. `api_generator.py` - Scaffolds REST/GraphQL APIs
2. `database_schema_optimizer.py` - Optimizes database design
3. `performance_profiler.py` - Analyzes backend performance

**senior-frontend** (3 tools):
1. `component_generator.py` - Scaffolds React/Vue components
2. `bundle_analyzer.py` - Analyzes bundle size and performance
3. `accessibility_checker.py` - Validates WCAG compliance

**senior-fullstack** (3 tools):
1. `fullstack_scaffolder.py` - Generates full-stack project structure
2. `integration_tester.py` - Tests frontend-backend integration
3. `deployment_optimizer.py` - Optimizes deployment configuration

**senior-devops** (3 tools):
1. `pipeline_generator.py` - Creates CI/CD pipeline configuration
2. `infrastructure_analyzer.py` - Evaluates infrastructure setup
3. `deployment_manager.py` - Manages deployment workflows

**senior-security** (3 tools):
1. `threat_modeler.py` - Generates threat models
2. `vulnerability_scanner.py` - Scans for security vulnerabilities
3. `compliance_checker.py` - Validates security compliance

**senior-secops** (3 tools):
1. `security_pipeline_generator.py` - Creates security CI/CD pipelines
2. `incident_response_planner.py` - Generates incident response plans
3. `security_metrics_analyzer.py` - Analyzes security metrics

**senior-qa** (3 tools):
1. `test_plan_generator.py` - Creates comprehensive test plans
2. `test_case_generator.py` - Generates test cases from requirements
3. `test_coverage_analyzer.py` - Analyzes test coverage metrics

**senior-ml-engineer** (3 tools):
1. `model_evaluator.py` - Evaluates ML model performance
2. `feature_engineering_helper.py` - Assists with feature engineering
3. `deployment_packager.py` - Packages models for deployment

**senior-data-engineer** (3 tools):
1. `pipeline_builder.py` - Builds data pipelines
2. `schema_validator.py` - Validates data schemas
3. `data_quality_checker.py` - Checks data quality metrics

**senior-data-scientist** (3 tools):
1. `experiment_tracker.py` - Tracks data science experiments
2. `eda_generator.py` - Generates exploratory data analysis
3. `visualization_builder.py` - Creates data visualizations

**senior-computer-vision** (3 tools):
1. `dataset_analyzer.py` - Analyzes vision datasets
2. `augmentation_helper.py` - Generates data augmentations
3. `model_converter.py` - Converts between model formats

**senior-prompt-engineer** (3 tools):
1. `prompt_optimizer.py` - Optimizes prompts for LLMs
2. `template_generator.py` - Generates prompt templates
3. `evaluation_framework.py` - Evaluates prompt effectiveness

**cto-advisor** (2 tools):
1. `tech_debt_analyzer.py` - Analyzes technical debt
2. `team_scaling_calculator.py` - Calculates team scaling metrics

**Total Engineering Tools**: 45 Python tools (3 per skill average, except CTO with 2)

## Workflow Pattern Analysis (from Existing 8 Agents)

### Consistency Metrics
- **100% of agents**: Use exactly 4 workflows
- **Average workflow length**: 6 steps per workflow
- **Average agent length**: 400-500 lines
- **Path pattern compliance**: 100% use ../../skills/ pattern
- **YAML frontmatter**: 100% compliance with required fields

### Standard Workflow Structure

Each existing agent follows this pattern:

**Workflow 1**: Primary use case (most common scenario)
- 5-7 steps
- Single tool focus
- 15-30 minute time estimate

**Workflow 2**: Advanced use case (complex scenario)
- 6-8 steps
- Multiple tool integration
- 30-60 minute time estimate

**Workflow 3**: Integration use case (combining tools/outputs)
- 4-6 steps
- Cross-functional workflow
- 20-40 minute time estimate

**Workflow 4**: Automation/batch use case (scripted workflow)
- 3-5 steps
- Scriptable commands
- 10-20 minute time estimate (setup) + ongoing automation

### Identified Workflow Categories by Domain

**Marketing Agents** (content-creator, demand-gen-specialist, product-marketer):
- Content creation workflows
- SEO optimization workflows
- Campaign planning workflows
- Analytics and reporting workflows

**Product Agents** (product-manager, agile-product-owner, product-strategist, ux-researcher, ui-designer):
- Feature prioritization workflows
- User research workflows
- Design system workflows
- Roadmap planning workflows

**Delivery Agents** (NEW - patterns from skill analysis):
- Sprint/iteration planning workflows
- Documentation workflows
- Team ceremony workflows
- Project tracking workflows

**Engineering Agents** (NEW - patterns from skill analysis):
- Code scaffolding workflows
- Architecture design workflows
- Testing and validation workflows
- Deployment and monitoring workflows

## Path Resolution Verification

### Current Pattern (100% Consistent)

All 8 existing agents use this exact pattern:
```markdown
**Skill Location:** `../../skills/domain-team/skill-name/`

### Python Tools
- **Path:** `../../skills/domain-team/skill-name/scripts/tool.py`
- **Usage:** `python ../../skills/domain-team/skill-name/scripts/tool.py [args]`
```

### Verified Paths

**Marketing agents** (agents/marketing/):
- ✅ `../../skills/marketing-team/content-creator/`
- ✅ `../../skills/marketing-team/demand-gen-specialist/`
- ✅ `../../skills/marketing-team/product-marketer/`

**Product agents** (agents/product/):
- ✅ `../../skills/product-team/product-manager/`
- ✅ `../../skills/product-team/agile-product-owner/`
- ✅ `../../skills/product-team/product-strategist/`
- ✅ `../../skills/product-team/ux-researcher/`
- ✅ `../../skills/product-team/ui-designer/`

### New Paths to Use

**Delivery agents** (agents/delivery/ - TO CREATE):
- `../../skills/delivery-team/jira-expert/`
- `../../skills/delivery-team/confluence-expert/`
- `../../skills/delivery-team/scrum-master/`
- `../../skills/delivery-team/senior-pm/`

**Engineering agents** (agents/engineering/ - TO CREATE):
- `../../skills/engineering-team/code-reviewer/`
- `../../skills/engineering-team/senior-architect/`
- `../../skills/engineering-team/senior-backend/`
- `../../skills/engineering-team/senior-frontend/`
- `../../skills/engineering-team/senior-fullstack/`
- `../../skills/engineering-team/senior-devops/`
- `../../skills/engineering-team/senior-security/`
- `../../skills/engineering-team/senior-secops/`
- `../../skills/engineering-team/senior-qa/`
- `../../skills/engineering-team/senior-ml-engineer/`
- `../../skills/engineering-team/senior-data-engineer/`
- `../../skills/engineering-team/senior-data-scientist/`
- `../../skills/engineering-team/senior-computer-vision/`
- `../../skills/engineering-team/senior-prompt-engineer/`
- `../../skills/engineering-team/cto-advisor/`

## Template Compliance Report

### Agent Template Analysis (templates/agent-template.md)

**Required Sections** (100% compliance in existing agents):
1. YAML frontmatter (7 fields: name, description, skills, domain, model, tools)
2. Purpose (2-3 paragraphs)
3. Skill Integration (skill location, tools, knowledge bases, templates)
4. Workflows (minimum 4, with Goal/Steps/Output/Time for each)
5. Integration Examples (2-3 bash scripts)
6. Success Metrics (3-4 categories)
7. Related Agents (cross-references)
8. References (skill docs, domain guide, agent guide)

**No Deviations Found**: All 8 existing agents follow template structure exactly

**Consistent Patterns**:
- All use `model: sonnet` in frontmatter
- All use `tools: [Read, Write, Bash, Grep, Glob]` in frontmatter
- All have 4 workflows (no more, no less)
- All provide bash script examples
- All categorize success metrics (efficiency, quality, impact)

### YAML Frontmatter Schema

```yaml
---
name: cs-agent-name           # Required: cs- prefix, kebab-case
description: One-line description  # Required: <150 chars
skills: skill-folder-name     # Required: exact folder name in skills/domain-team/
domain: domain-name           # Required: marketing|product|delivery|engineering
model: sonnet                 # Required: sonnet|opus|haiku
tools: [Read, Write, Bash, Grep, Glob]  # Required: array of tool names
---
```

**All existing agents use `model: sonnet`** - this is the standard for production agents.

## Knowledge Base Patterns

### Knowledge Bases per Skill (from references/)

**Delivery Team**:
- jira-expert: 4 references (Jira workflows, issue types, board setup, reporting)
- confluence-expert: 4 references (page templates, space management, permissions, best practices)
- scrum-master: 5 references (Scrum guide, ceremonies, metrics, impediment patterns, team dynamics)
- senior-pm: 6 references (Roadmap frameworks, stakeholder management, resource planning, risk management, delivery metrics, cross-team coordination)

**Engineering Team** (3-5 references per skill):
- code-reviewer: 4 references (review checklist, code quality standards, feedback guidelines, tool integration)
- senior-architect: 5 references (design patterns, system design, technology evaluation, scalability, documentation)
- senior-backend: 4 references (API design, database optimization, caching strategies, monitoring)
- senior-frontend: 4 references (component patterns, performance optimization, accessibility, state management)
- senior-fullstack: 5 references (architecture patterns, API design, deployment, testing strategies, documentation)
- senior-devops: 5 references (CI/CD patterns, infrastructure as code, monitoring, security, incident response)
- senior-security: 5 references (threat modeling, vulnerability management, compliance, secure coding, penetration testing)
- senior-secops: 5 references (security automation, incident response, compliance frameworks, security metrics, DevSecOps)
- senior-qa: 5 references (test strategies, automation patterns, quality metrics, tools, best practices)
- senior-ml-engineer: 5 references (model development, training optimization, deployment patterns, monitoring, MLOps)
- senior-data-engineer: 5 references (pipeline patterns, data modeling, ETL/ELT, data quality, orchestration)
- senior-data-scientist: 5 references (experiment design, statistical methods, visualization, model evaluation, collaboration)
- senior-computer-vision: 5 references (architectures, datasets, augmentation, evaluation, deployment)
- senior-prompt-engineer: 4 references (prompt patterns, optimization techniques, evaluation frameworks, LLM capabilities)
- cto-advisor: 6 references (technology strategy, team scaling, technical debt, vendor selection, innovation frameworks, executive communication)

**Average**: 4.5 references per skill (engineering), 4.75 references per skill (delivery)

## Templates Inventory (from assets/)

**Template-Rich Skills**:
- All engineering skills have 2-3 templates each
- Examples: API documentation template, system design template, test plan template, deployment checklist

**Template-Light Skills**:
- Delivery skills have 1-2 templates each (primarily checklists and planning documents)

**Template Types Identified**:
1. Planning templates (roadmaps, sprint plans)
2. Documentation templates (API docs, architecture docs)
3. Checklist templates (review checklists, deployment checklists)
4. Report templates (metrics dashboards, status reports)

## Integration Patterns

### Cross-Agent Integration Identified

**Delivery Domain**:
- **cs-senior-pm** orchestrates: cs-jira-expert, cs-confluence-expert, cs-scrum-master
- Pattern: PM drives planning → Jira Expert manages execution → Scrum Master facilitates ceremonies → Confluence Expert documents

**Engineering Domain**:
- **cs-architect** → cs-backend-engineer, cs-frontend-engineer, cs-devops-engineer (architecture defines implementation)
- **cs-code-reviewer** ← all engineering agents (reviews output from all)
- **cs-fullstack-engineer** integrates: cs-backend-engineer + cs-frontend-engineer + cs-devops-engineer
- **cs-cto-advisor** → all engineering agents (provides strategic direction)

**Cross-Domain Integration**:
- cs-product-manager → cs-architect (product requirements → architecture)
- cs-architect → cs-senior-pm (architecture → delivery planning)
- cs-ux-researcher → cs-frontend-engineer (research findings → implementation)

### MCP Integration Pattern (Delivery Team)

**Atlassian MCP Server** required for:
- cs-jira-expert
- cs-confluence-expert

**MCP Workflow Pattern**:
```markdown
## Workflows
### Workflow 1: [Jira Task]
**Steps:**
1. **Invoke MCP** - Use Atlassian MCP to connect to Jira
   ```bash
   # MCP server handles authentication and API calls
   # No Python tools needed - direct integration
   ```
2. **Execute Operation** - Perform Jira operation via MCP
3. **Review Output** - Validate results
```

## Risk Assessment

### High-Risk Areas

1. **Delivery Team Path Resolution**
   - Risk: agents/delivery/ directory doesn't exist yet
   - Mitigation: Create directory before creating agents
   - Impact: High (broken paths = non-functional agents)

2. **Engineering Team Path Resolution**
   - Risk: agents/engineering/ directory doesn't exist yet
   - Mitigation: Create directory before creating agents
   - Impact: High (broken paths = non-functional agents)

3. **MCP Server Dependency**
   - Risk: Jira/Confluence agents depend on external MCP server
   - Mitigation: Document MCP setup requirements clearly in agent Purpose section
   - Impact: Medium (agents work if MCP installed, otherwise cannot function)

### Medium-Risk Areas

1. **Workflow Quality Consistency**
   - Risk: 18 new agents may vary in workflow quality
   - Mitigation: Use existing 8 agents as quality baseline; follow 4-workflow pattern exactly
   - Impact: Medium (inconsistent UX, but functional)

2. **Cross-Agent Integration Documentation**
   - Risk: Related Agents section may miss important connections
   - Mitigation: Document integration patterns in design phase (Phase 1)
   - Impact: Low-Medium (missed collaboration opportunities)

### Low-Risk Areas

1. **Python Tool Documentation**
   - Risk: Tool descriptions may not match actual behavior
   - Mitigation: Test tools during agent creation; verify --help output
   - Impact: Low (documentation issue, tools still work)

2. **Success Metrics Standardization**
   - Risk: Metrics may vary in quality across agents
   - Mitigation: Define metric categories in Phase 1 design
   - Impact: Low (cosmetic, doesn't affect functionality)

## Recommendations for Phase 1 (Design)

### Priority 1: Directory Structure
Create agents/delivery/ and agents/engineering/ directories before agent creation to enable path testing.

### Priority 2: Workflow Standardization
Define 4 standard workflow types for each domain:
- Delivery: Planning, Execution, Collaboration, Reporting
- Engineering: Setup/Scaffolding, Development, Testing/Validation, Deployment

### Priority 3: MCP Integration Guide
Create detailed MCP setup instructions for delivery agents (especially cs-jira-expert and cs-confluence-expert).

### Priority 4: Success Metrics Framework
Define metric categories:
- Delivery: Efficiency, Collaboration Quality, Delivery Predictability, Team Satisfaction
- Engineering: Code Quality, Development Velocity, System Reliability, Innovation Capacity

### Priority 5: Integration Examples
Create bash script templates for:
- MCP-driven workflows (delivery agents)
- Python tool orchestration (engineering agents)
- Multi-agent integration scenarios

## Next Phase: Design Deliverables

Based on research findings, Phase 1 should produce:

1. **data-model.md**: Agent structure specification
   - YAML frontmatter schema (validated pattern from existing agents)
   - Section templates with exact formatting
   - Relative path patterns by domain
   - Workflow documentation format (4 workflows, Goal/Steps/Output/Time)

2. **quickstart.md**: Agent creation workflow
   - Step-by-step process to create new agent
   - Template usage guide with examples
   - Path validation checklist
   - Workflow development guide (how to identify 4 workflows per skill)
   - Testing and validation steps

3. **contracts/** directory: Validation contracts
   - yaml-frontmatter.md: Required fields, format validation
   - relative-paths.md: Path resolution requirements, testing procedure
   - workflow-completeness.md: Minimum 4 workflows, required fields per workflow

---

**Research Status**: Complete
**Last Updated**: November 12, 2025
**Next Milestone**: Phase 1 Design (data-model.md, quickstart.md, contracts/)
**Ready to Proceed**: Yes
