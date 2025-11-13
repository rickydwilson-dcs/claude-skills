# Implementation Plan: Agent Completion for 26 Pandora Skills

**Branch**: `002-agent-completion` | **Date**: November 12, 2025 | **Spec**: [spec.md](spec.md)
**Input**: Complete agent coverage for all 26 Pandora-focused skills (18 new agents needed)

## Summary

Build 18 new production-ready agents to achieve complete 1:1 skill-to-agent coverage for the Pandora edition. Currently 8 agents exist (3 marketing, 5 product); need to add 4 delivery-team agents and 14 engineering-team agents. Each agent will orchestrate its corresponding skill package using templates/agent-template.md, following established patterns from existing agents, with proper YAML frontmatter, relative paths (../../skills/), and minimum 4 documented workflows.

## Technical Context

**Language/Version**: Markdown (agent definitions), Python 3.8+ (existing skill tools)
**Primary Dependencies**: None (agents are markdown documentation files)
**Storage**: File system (agents/ directory structure)
**Testing**: Manual validation (relative path resolution, workflow documentation completeness)
**Target Platform**: Claude Code (VSCode extension) + Claude AI (web)
**Project Type**: Documentation library (agent orchestration definitions)
**Performance Goals**: N/A (documentation files)
**Constraints**:
- Must follow agent-template.md structure exactly
- Minimum 4 workflows per agent
- All relative paths must resolve from agents/domain/ location
- YAML frontmatter required for Claude Code discovery
**Scale/Scope**: 18 new agent files across 2 domains (delivery, engineering)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**No violations expected** - This is a documentation-only feature following established patterns.

## Project Structure

### Documentation (this feature)

```text
specs/002-agent-completion/
├── plan.md              # This file
├── spec.md              # Feature specification (user stories, requirements)
├── research.md          # Phase 0: Skill package analysis
├── data-model.md        # Phase 1: Agent structure patterns
├── quickstart.md        # Phase 1: Agent creation workflow
├── contracts/           # Phase 1: Agent validation contracts
│   ├── yaml-frontmatter.md
│   ├── relative-paths.md
│   └── workflow-completeness.md
└── tasks.md             # Phase 2: Task breakdown (created by /speckit.tasks)
```

### Source Code (repository root)

```text
agents/
├── marketing/                    # ✅ COMPLETE (3 agents)
│   ├── cs-content-creator.md
│   ├── cs-demand-gen-specialist.md
│   └── cs-product-marketer.md
├── product/                      # ✅ COMPLETE (5 agents)
│   ├── cs-product-manager.md
│   ├── cs-agile-product-owner.md
│   ├── cs-product-strategist.md
│   ├── cs-ux-researcher.md
│   └── cs-ui-designer.md
├── delivery/                     # ❌ TO BUILD (4 agents)
│   ├── cs-jira-expert.md         # NEW
│   ├── cs-confluence-expert.md   # NEW
│   ├── cs-scrum-master.md        # NEW
│   └── cs-senior-pm.md           # NEW
└── engineering/                  # ❌ TO BUILD (14 agents)
    ├── cs-code-reviewer.md       # NEW
    ├── cs-cto-advisor.md         # NEW
    ├── cs-architect.md           # NEW
    ├── cs-backend-engineer.md    # NEW
    ├── cs-frontend-engineer.md   # NEW
    ├── cs-fullstack-engineer.md  # NEW
    ├── cs-devops-engineer.md     # NEW
    ├── cs-security-engineer.md   # NEW
    ├── cs-secops-engineer.md     # NEW
    ├── cs-qa-engineer.md         # NEW
    ├── cs-ml-engineer.md         # NEW
    ├── cs-data-engineer.md       # NEW
    ├── cs-data-scientist.md      # NEW
    └── cs-computer-vision.md     # NEW

skills/                           # EXISTING (26 skills)
├── delivery-team/                # 4 skills
│   ├── jira-expert/
│   ├── confluence-expert/
│   ├── scrum-master/
│   └── senior-pm/
├── engineering-team/             # 15 skills (including cto-advisor)
│   ├── code-reviewer/
│   ├── cto-advisor/
│   ├── senior-architect/
│   ├── senior-backend/
│   ├── senior-frontend/
│   ├── senior-fullstack/
│   ├── senior-devops/
│   ├── senior-security/
│   ├── senior-secops/
│   ├── senior-qa/
│   ├── senior-ml-engineer/
│   ├── senior-data-engineer/
│   ├── senior-data-scientist/
│   ├── senior-computer-vision/
│   └── senior-prompt-engineer/
├── marketing-team/               # 3 skills ✅
└── product-team/                 # 5 skills ✅

templates/
└── agent-template.md             # EXISTING (base template)

docs/
└── standards/
    ├── quality-standards.md      # Agent quality requirements
    ├── documentation-standards.md # Agent documentation format
    └── communication-standards.md # Workflow clarity standards
```

**Structure Decision**: Using existing agents/ directory structure. No new directories needed. New agents created in agents/delivery/ and agents/engineering/ following the established pattern from agents/marketing/ and agents/product/.

## Complexity Tracking

> **No complexity violations** - This feature follows existing patterns and adds no new complexity.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Phase 0: Research (Prior to Implementation)

### Research Questions

1. **Skill Package Analysis**
   - For each of the 18 skills without agents, what Python tools exist in scripts/?
   - What knowledge bases exist in references/?
   - What templates exist in assets/?
   - What are the primary workflows documented in SKILL.md?

2. **Existing Agent Pattern Analysis**
   - How do existing 8 agents structure their workflows?
   - What's the typical workflow count (3, 4, or 5+)?
   - How are Python tools documented and invoked?
   - How are success metrics structured?

3. **Relative Path Validation**
   - Verify all existing agents use ../../skills/domain-team/ pattern
   - Document any path resolution issues in current agents
   - Confirm agents/delivery/ and agents/engineering/ directories don't exist yet

4. **Template Compliance**
   - Compare existing agents to templates/agent-template.md
   - Identify any deviations from template in production agents
   - Document any additional sections added beyond template

### Research Deliverables (research.md)

- Skill-to-Agent mapping table (26 rows)
- Tool inventory per skill (scripts/ directory contents)
- Workflow pattern analysis from existing 8 agents
- Path resolution verification results
- Template compliance report

## Phase 1: Design

### Design Questions

1. **Agent Creation Order**
   - Should we build delivery agents first (simpler, 4 total) or engineering agents (more complex, 14 total)?
   - Batch creation vs. iterative validation approach?

2. **Workflow Design Patterns**
   - What are the 4 core workflows for each agent type?
   - How do we differentiate primary/advanced/integration workflows?
   - Time estimates for each workflow category?

3. **Success Metrics Standardization**
   - What metric categories apply to delivery agents (efficiency, quality, collaboration)?
   - What metric categories apply to engineering agents (code quality, velocity, reliability)?
   - Should metrics be skill-specific or role-specific?

4. **Documentation Updates**
   - When do we update agent counts (3→8→26) in CLAUDE.md, README.md, install.sh?
   - Should counts be updated incrementally or at completion?

### Design Deliverables

- **data-model.md**: Agent structure specification
  - YAML frontmatter schema
  - Section templates (Purpose, Skill Integration, Workflows, Success Metrics)
  - Relative path patterns
  - Workflow documentation format

- **quickstart.md**: Agent creation workflow
  - Step-by-step agent creation process
  - Template usage guide
  - Path validation checklist
  - Workflow development guide
  - Testing and validation steps

- **contracts/**: Validation contracts
  - yaml-frontmatter.md: Required fields and format
  - relative-paths.md: Path resolution requirements
  - workflow-completeness.md: Minimum 4 workflows, each with Goal/Steps/Output/Time

## Phase 2: Implementation Tasks

*NOTE: tasks.md will be generated by /speckit.tasks command after Phase 1 design is complete*

### Anticipated Task Categories

1. **Delivery Team Agents** (4 agents)
   - Create agents/delivery/ directory
   - Build cs-jira-expert.md
   - Build cs-confluence-expert.md
   - Build cs-scrum-master.md
   - Build cs-senior-pm.md
   - Validate all 4 agents

2. **Engineering Team Agents - Batch 1** (Core Engineering, 5 agents)
   - Create agents/engineering/ directory
   - Build cs-backend-engineer.md
   - Build cs-frontend-engineer.md
   - Build cs-fullstack-engineer.md
   - Build cs-architect.md
   - Build cs-code-reviewer.md

3. **Engineering Team Agents - Batch 2** (DevOps/Security, 4 agents)
   - Build cs-devops-engineer.md
   - Build cs-security-engineer.md
   - Build cs-secops-engineer.md
   - Build cs-qa-engineer.md

4. **Engineering Team Agents - Batch 3** (AI/ML/Data, 4 agents)
   - Build cs-ml-engineer.md
   - Build cs-data-engineer.md
   - Build cs-data-scientist.md
   - Build cs-computer-vision.md

5. **Engineering Team Agents - Batch 4** (Leadership/Specialty, 2 agents)
   - Build cs-cto-advisor.md
   - Build cs-prompt-engineer.md (senior-prompt-engineer skill)

6. **Documentation Updates**
   - Update CLAUDE.md agent count and architecture diagram
   - Update README.md agent catalog (remove old entries, add new 18)
   - Update install.sh agent counts (3→26, update domain options)
   - Update specs/001-clean-break/migration-notes.md final counts

7. **Testing and Validation**
   - Test all relative paths resolve correctly
   - Validate all agents have 4+ workflows
   - Verify YAML frontmatter consistency
   - Test agent discovery in Claude Code (if possible)

## Success Criteria

### Completion Gates

- [ ] **Phase 0 Complete**: research.md delivered with skill analysis and pattern documentation
- [ ] **Phase 1 Complete**: data-model.md, quickstart.md, contracts/ delivered
- [ ] **Phase 2 Complete**: All 18 agents created and validated (tasks.md fully checked off)
- [ ] **Documentation Updated**: All counts corrected across CLAUDE.md, README.md, install.sh
- [ ] **Quality Gates Passed**: All agents follow template, paths resolve, 4+ workflows documented

### Measurable Outcomes

- **SC-001**: 26 total agents (8 existing + 18 new) mapped 1:1 to 26 skills
- **SC-002**: 100% of new agents have minimum 4 documented workflows
- **SC-003**: 100% of relative paths resolve correctly from agent locations
- **SC-004**: All documentation reflects accurate agent counts (26 agents)
- **SC-005**: Zero broken links in new agent files
- **SC-006**: All new agents discoverable by Claude Code (@cs-agent-name syntax)

## Risk Management

### Identified Risks

1. **Risk**: Scope creep - temptation to improve existing 8 agents while building new 18
   - **Mitigation**: Strict focus on new agent creation only; improvements deferred to future feature

2. **Risk**: Path resolution errors due to inconsistent skill folder naming
   - **Mitigation**: Validate paths during research phase; document any naming inconsistencies

3. **Risk**: Workflow quality varies across 18 agents due to batch creation
   - **Mitigation**: Use existing 8 agents as quality baseline; peer review workflows before completion

4. **Risk**: Documentation updates introduce errors (broken links, wrong counts)
   - **Mitigation**: Create documentation update checklist; validate with grep/find commands

### Dependencies

- **Blocker**: Phase 0 research must complete before Phase 1 design
- **Blocker**: Phase 1 design must complete before Phase 2 implementation
- **Dependency**: templates/agent-template.md must remain stable during implementation
- **Dependency**: No changes to skills/ structure during agent creation

## Timeline Estimate

**Phase 0 (Research)**: 1 day
- Skill package analysis: 4 hours
- Existing agent pattern analysis: 2 hours
- Path validation and template compliance: 2 hours

**Phase 1 (Design)**: 1 day
- data-model.md: 3 hours
- quickstart.md: 2 hours
- contracts/: 3 hours

**Phase 2 (Implementation)**: 3-4 days
- Delivery agents (4): 0.5 days
- Engineering agents batch 1 (5): 1 day
- Engineering agents batch 2 (4): 0.75 days
- Engineering agents batch 3 (4): 0.75 days
- Engineering agents batch 4 (2): 0.5 days
- Documentation updates: 0.25 days
- Testing and validation: 0.5 days

**Total Estimate**: 5-6 days

## Next Steps

1. Run `/speckit.plan` to generate research.md template
2. Complete Phase 0 research (skill analysis)
3. Run `/speckit.plan` again to generate Phase 1 deliverables
4. Complete Phase 1 design (data-model.md, quickstart.md, contracts/)
5. Run `/speckit.tasks` to generate tasks.md
6. Execute Phase 2 implementation tasks in order

---

**Plan Status**: Draft
**Last Updated**: November 12, 2025
**Next Milestone**: Phase 0 Research
