# Implementation Brief: Agent/Skill Builder System (Option 4)

**Project:** Automated Agent/Skill Creation Tools
**Date:** 2025-11-22
**Author:** Claude Code
**Priority:** Phase 1 - Foundation Enabler

---

## Executive Summary

Build automated creation tools for agents and skills to reduce creation time from days to hours and ensure consistency across all new additions. This is the highest priority development task with 9/10 ROI.

**Key Metrics:**
- Agent creation: 2 days → 1 hour (95% reduction)
- Skill creation: 3 days → 2 hours (93% reduction)
- Error rate: Manual (~20%) → Automated (<5%)

---

## Goals

1. **Agent Builder**: Interactive CLI tool to generate agents from template with validation
2. **Skill Builder**: Interactive CLI tool to create skill directory structures with scaffolding
3. **Validation System**: Automated checking of YAML frontmatter, relative paths, and structure
4. **Time Reduction**: Achieve 90%+ time savings for agent/skill creation
5. **Quality Assurance**: Ensure 100% consistency with existing patterns

---

## Current State Analysis

### Existing Infrastructure
- **28 production agents** across 4 domains (marketing, product, engineering, delivery)
- **29 production skills** with 60 Python automation tools
- **Agent template exists:** `templates/agent-template.md` (318 lines, comprehensive)
- **Skill template missing:** Must be created as part of this project
- **Manual process:** 12+ steps for agents, 15+ steps for skills
- **Error-prone:** Path errors, YAML mistakes, catalog update failures

### Pain Points
1. Agent creation takes 1-2 days of manual work
2. Skill creation takes 2-3 days of manual work
3. YAML frontmatter errors require debugging
4. Relative path validation is manual and error-prone
5. Catalog updates are manual and forgotten
6. No validation until agent is used (late error discovery)

---

## Scope

### Agent Builder Features
- ✅ Interactive CLI prompts for all required fields
- ✅ Fields: name, domain, skill package, description, model, tools
- ✅ Generate `agents/{domain}/cs-{name}.md` from template
- ✅ Validate YAML frontmatter (required fields, enum values)
- ✅ Validate relative paths (../../skills/{domain}/{skill}/ resolves)
- ✅ Auto-update `docs/AGENTS_CATALOG.md`
- ✅ Create placeholder workflows (minimum 3)
- ✅ Git integration (optional commit after creation)

### Skill Builder Features
- ✅ Interactive CLI prompts for skill parameters
- ✅ Fields: name, domain, tool count, reference count, description
- ✅ Create directory: `skills/{domain}/{skill-name}/{scripts,references,assets}/`
- ✅ Generate `SKILL.md` from template (must create template first!)
- ✅ Create placeholder Python tools with `--help` flag support
- ✅ Create placeholder reference markdown files
- ✅ Auto-update `docs/SKILLS_CATALOG.md`
- ✅ Git integration (optional commit after creation)

### Validation Features
- ✅ YAML parser for agent frontmatter
- ✅ Path resolution checker (relative paths must resolve)
- ✅ Structure validator (required files/directories exist)
- ✅ Standalone validation commands for existing agents/skills
- ✅ Bulk validation (`--all` flag)
- ✅ Exit codes for CI/CD integration

---

## Implementation Strategy

### Phase 1: Design (cs-architect)
**Agent:** `cs-architect`
**Model:** sonnet
**Duration:** 4-6 hours

**Deliverables:**
- Architecture Decision Record (ADR)
- Technical design for agent builder
- Technical design for skill builder
- Validation strategy and architecture
- **Skill template specification** (critical - doesn't exist yet!)
- Integration points with existing system (session_manager.py pattern)
- Error handling strategy
- Testing strategy

**Key Decisions:**
- Interactive CLI vs config file approach
- Validation timing (pre-generation vs post-generation)
- Catalog update strategy (append vs regenerate)
- Git integration approach (automatic vs manual)

---

### Phase 2: Build Agent Builder (cs-backend-engineer)
**Agent:** `cs-backend-engineer`
**Model:** sonnet
**Duration:** 1-2 days

**Deliverables:**
- `scripts/agent_builder.py` (interactive CLI, ~400-600 lines)
- Agent template integration (parse and populate)
- YAML validation module (PyYAML or standard library)
- Path validation module (os.path resolution)
- AGENTS_CATALOG.md auto-update logic
- Unit tests (pytest or standard library unittest)
- README documentation

**Technical Requirements:**
```python
#!/usr/bin/env python3
"""
Agent Builder - Interactive CLI for creating new agents

Usage:
    python scripts/agent_builder.py
    python scripts/agent_builder.py --non-interactive --config agent-config.json
"""

# Key functions
def prompt_agent_details() -> dict:
    """Interactive prompts for agent configuration"""

def validate_agent_name(name: str) -> bool:
    """Validate agent name format (no cs- prefix, alphanumeric-hyphens)"""

def validate_yaml_frontmatter(agent_path: str) -> bool:
    """Parse and validate YAML frontmatter against schema"""

def validate_relative_paths(agent_path: str, skill_package: str) -> bool:
    """Verify ../../skills/{domain}/{skill}/ resolves correctly"""

def generate_agent(config: dict) -> str:
    """Generate agent file from template with provided config"""

def update_agents_catalog(agent_name: str, domain: str, description: str):
    """Append new agent to AGENTS_CATALOG.md"""

def main():
    """Main CLI entry point"""
```

**Validation Rules:**
- Agent name: lowercase, hyphens only, no cs- prefix
- Domain: must be one of [marketing, product, engineering, delivery]
- Skill package: must exist in skills/{domain}/
- Model: must be one of [sonnet, opus, haiku]
- Tools: must be subset of [Read, Write, Bash, Grep, Glob]
- YAML: required fields (name, description, skills, domain, model, tools)
- Paths: all ../../ references must resolve to existing directories

---

### Phase 3: Build Skill Builder (cs-backend-engineer)
**Agent:** `cs-backend-engineer`
**Model:** sonnet
**Duration:** 1-2 days

**Prerequisites:**
- ⚠️ **CRITICAL:** Skill template must be created first (Phase 1 output)

**Deliverables:**
- `templates/skill-template.md` (NEW - designed in Phase 1)
- `scripts/skill_builder.py` (interactive CLI, ~500-700 lines)
- Directory scaffolding system
- SKILLS_CATALOG.md auto-update logic
- Placeholder Python tool generator
- Placeholder reference generator
- Unit tests
- README documentation

**Technical Requirements:**
```python
#!/usr/bin/env python3
"""
Skill Builder - Interactive CLI for creating new skills

Usage:
    python scripts/skill_builder.py
    python scripts/skill_builder.py --non-interactive --config skill-config.json
"""

# Key functions
def prompt_skill_details() -> dict:
    """Interactive prompts for skill configuration"""

def create_skill_structure(base_path: str):
    """Create skills/{domain}/{skill-name}/{scripts,references,assets}/"""

def generate_skill_md(base_path: str, config: dict):
    """Generate SKILL.md from template"""

def generate_placeholder_tool(script_path: str, tool_name: str):
    """Create Python tool with --help flag and basic structure"""

def generate_placeholder_reference(ref_path: str, ref_name: str):
    """Create reference markdown file with template structure"""

def update_skills_catalog(skill_name: str, domain: str, description: str):
    """Append new skill to SKILLS_CATALOG.md"""

def main():
    """Main CLI entry point"""
```

**Directory Structure Created:**
```
skills/{domain}/{skill-name}/
├── SKILL.md                    # Generated from template
├── scripts/
│   ├── tool1.py               # Placeholder with --help
│   ├── tool2.py               # Placeholder with --help
│   └── tool3.py               # Placeholder with --help
├── references/
│   ├── reference1.md          # Placeholder with structure
│   └── reference2.md          # Placeholder with structure
└── assets/
    └── .gitkeep               # Ensure directory is tracked
```

**Placeholder Python Tool Template:**
```python
#!/usr/bin/env python3
"""
{TOOL_NAME} - Brief description

Part of {SKILL_NAME} skill for {DOMAIN} team.
"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="{TOOL_NAME} - Brief description"
    )
    parser.add_argument(
        'input',
        help='Input file or data'
    )
    parser.add_argument(
        '--output',
        help='Output file (default: stdout)',
        default=None
    )

    args = parser.parse_args()

    # TODO: Implement tool logic
    print(f"Processing: {args.input}")
    print("TODO: Add implementation")

if __name__ == "__main__":
    main()
```

---

### Phase 4: Validation System (cs-qa-engineer)
**Agent:** `cs-qa-engineer`
**Model:** sonnet
**Duration:** 1 day

**Deliverables:**
- `scripts/validate_agent.py` (standalone validator, ~200-300 lines)
- `scripts/validate_skill.py` (standalone validator, ~200-300 lines)
- Test suite for validation logic
- CI/CD integration examples
- Documentation

**Validation Scripts:**
```bash
# Validate single agent
python scripts/validate_agent.py agents/engineering/cs-architect.md

# Validate all agents
python scripts/validate_agent.py --all

# Validate single skill
python scripts/validate_skill.py skills/marketing-team/content-creator/

# Validate all skills
python scripts/validate_skill.py --all

# JSON output for CI/CD
python scripts/validate_agent.py --all --format json
```

**Exit Codes:**
- 0: All validations passed
- 1: Validation errors found
- 2: Invalid arguments or file not found

**Validation Checks:**

**Agent Validation:**
1. File exists and is readable
2. YAML frontmatter present and parseable
3. Required YAML fields present (name, description, skills, domain, model, tools)
4. Domain is valid enum value
5. Model is valid enum value
6. Tools are valid subset
7. Relative paths resolve (../../skills/{domain}/{skill}/)
8. Minimum 3 workflows documented
9. Skill package referenced actually exists

**Skill Validation:**
1. Directory exists
2. SKILL.md exists and is readable
3. scripts/ directory exists
4. references/ directory exists
5. assets/ directory exists
6. At least one Python tool in scripts/
7. All Python tools have --help flag
8. All Python tools are executable (chmod +x)
9. SKILL.md follows template structure

---

### Phase 5: Documentation (Manual or cs-technical-writer)
**Duration:** 0.5 days

**Deliverables:**
- Updated `CLAUDE.md` with builder usage section
- Updated `scripts/README.md` with new tools
- Usage examples and workflows
- Troubleshooting guide
- Integration with existing workflows

**Documentation Sections:**

1. **Quick Start Guide**
```bash
# Create a new agent
python scripts/agent_builder.py

# Create a new skill
python scripts/skill_builder.py

# Validate everything
python scripts/validate_agent.py --all
python scripts/validate_skill.py --all
```

2. **Common Workflows**
- Creating an agent for existing skill
- Creating a skill and agent together
- Validating before committing
- Updating catalogs after creation

3. **Troubleshooting**
- YAML parsing errors
- Path resolution failures
- Catalog update conflicts
- Permission issues

---

## Agent Assignments Summary

| Phase | Agent | Model | Duration | Key Output |
|-------|-------|-------|----------|------------|
| **1. Design** | cs-architect | sonnet | 4-6h | ADR, skill template spec, validation strategy |
| **2. Agent Builder** | cs-backend-engineer | sonnet | 1-2d | agent_builder.py, validation modules |
| **3. Skill Builder** | cs-backend-engineer | sonnet | 1-2d | skill_builder.py, skill template |
| **4. Validation** | cs-qa-engineer | sonnet | 1d | validate_agent.py, validate_skill.py, tests |
| **5. Documentation** | Manual | - | 0.5d | CLAUDE.md updates, usage guides |

**Total Estimated Effort:** 4-6 days

---

## Technical Architecture

### Component Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (CLI)                      │
├─────────────────────────────────────────────────────────────┤
│  agent_builder.py    │  skill_builder.py    │  validate_*.py│
├─────────────────────────────────────────────────────────────┤
│                    Core Validation Logic                     │
│  - YAML Parser       │  - Path Resolver     │  - Linter     │
├─────────────────────────────────────────────────────────────┤
│                    Template System                           │
│  agent-template.md   │  skill-template.md   │  tool-tpl.py  │
├─────────────────────────────────────────────────────────────┤
│                    Catalog Management                        │
│  AGENTS_CATALOG.md   │  SKILLS_CATALOG.md   │  update logic │
├─────────────────────────────────────────────────────────────┤
│                    File System (Repository)                  │
│  agents/             │  skills/             │  templates/   │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow: Agent Creation
```
1. User runs: python scripts/agent_builder.py
2. CLI prompts for: name, domain, skill, description, model, tools
3. Validate inputs: name format, domain enum, skill exists
4. Load template: templates/agent-template.md
5. Populate template: Replace {{placeholders}} with user input
6. Validate output: YAML frontmatter, relative paths
7. Write file: agents/{domain}/cs-{name}.md
8. Update catalog: docs/AGENTS_CATALOG.md (append entry)
9. Report success: Print file path and next steps
```

### Data Flow: Skill Creation
```
1. User runs: python scripts/skill_builder.py
2. CLI prompts for: name, domain, tool_count, ref_count, description
3. Validate inputs: name format, domain enum
4. Create structure: skills/{domain}/{name}/{scripts,references,assets}/
5. Generate SKILL.md: From skill-template.md
6. Generate tools: {tool_count} placeholder Python scripts
7. Generate references: {ref_count} placeholder markdown files
8. Update catalog: docs/SKILLS_CATALOG.md (append entry)
9. Report success: Print directory path and next steps
```

---

## Success Criteria

### Functional Requirements
- [ ] Agent created in <5 minutes with valid YAML and paths
- [ ] Skill created in <10 minutes with complete directory structure
- [ ] All 28 existing agents pass validation
- [ ] All 29 existing skills pass validation
- [ ] New agents pass validation on first try (100% success rate)
- [ ] New skills pass validation on first try (100% success rate)
- [ ] Catalogs auto-update correctly (no manual editing needed)
- [ ] No template editing required (all via CLI)

### Performance Requirements
- [ ] Agent creation: 2 days → 1 hour (95% reduction achieved)
- [ ] Skill creation: 3 days → 2 hours (93% reduction achieved)
- [ ] Validation runs in <3 seconds per agent/skill
- [ ] Bulk validation (<5 seconds for all 28 agents + 29 skills)
- [ ] Zero errors from generated files (validation pass rate: 100%)

### Quality Requirements
- [ ] Generated agents match template structure exactly
- [ ] Generated skills have consistent directory structure
- [ ] Validation catches 100% of known error patterns
- [ ] Documentation is clear and complete (no user questions)
- [ ] Error messages are actionable (tell user how to fix)

### Integration Requirements
- [ ] Works with existing session system
- [ ] Compatible with git workflow (feature branches)
- [ ] Can be wrapped by slash commands (future Option 2)
- [ ] Can be invoked by orchestrator (future Option 5)

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Skill template doesn't exist** | High - blocks Phase 3 | 100% | Create in Phase 1 (cs-architect designs, includes in ADR) |
| **Relative path validation complex** | Medium - validation failures | Medium | Test against all 28 existing agents, handle edge cases |
| **YAML parsing edge cases** | Medium - generation failures | Medium | Use PyYAML library, validate against all existing frontmatter |
| **Catalog update conflicts** | Low - merge conflicts | Low | Atomic operations, backup before update, provide undo |
| **Template changes break builder** | Medium - maintenance burden | Low | Version templates, validate compatibility on update |
| **Python version incompatibility** | Low - deployment issues | Low | Require Python 3.8+, use standard library only |

---

## Dependencies

### Input Dependencies
- ✅ `templates/agent-template.md` (exists, 318 lines)
- ❌ `templates/skill-template.md` (MUST CREATE in Phase 1)
- ✅ Existing agents for validation testing (28 production agents)
- ✅ Existing skills for validation testing (29 production skills)
- ✅ Session system pattern (reference: `scripts/session_manager.py`)

### Output Dependencies (What This Enables)
- ✅ **Option 2 (Slash Commands):** Can wrap builders as `/agent.create`, `/skill.create`
- ✅ **Option 3 (Doc Agent):** Builders maintain catalogs, reducing doc agent scope
- ✅ **Option 5 (Orchestrator):** Orchestrator can invoke builders programmatically
- ✅ **Rapid Scaling:** Enables reaching 50+ agents/skills target by Q3 2026

---

## Timeline & Milestones

### Week 1
- **Days 1-2:** Phase 1 (Design) - cs-architect creates ADR and skill template
- **Days 3-5:** Phase 2 (Agent Builder) - cs-backend-engineer implements and tests

### Week 2
- **Days 1-3:** Phase 3 (Skill Builder) - cs-backend-engineer implements and tests
- **Day 4:** Phase 4 (Validation) - cs-qa-engineer implements validators
- **Day 5:** Phase 5 (Documentation) - Update guides and examples

### Milestones
1. **M1 (Day 2):** ADR approved, skill template created ✅
2. **M2 (Day 5):** Agent builder functional, 1 test agent created ✅
3. **M3 (Day 8):** Skill builder functional, 1 test skill created ✅
4. **M4 (Day 9):** Validation system complete, all existing agents/skills pass ✅
5. **M5 (Day 10):** Documentation complete, ready for team use ✅

---

## Testing Strategy

### Unit Tests
```python
# test_agent_builder.py
def test_validate_agent_name():
    assert validate_agent_name("data-engineer") == True
    assert validate_agent_name("cs-data-engineer") == False  # No cs- prefix
    assert validate_agent_name("data_engineer") == False     # No underscores

def test_validate_yaml_frontmatter():
    valid_yaml = """---
name: cs-test-agent
description: Test agent
skills: test-skill
domain: engineering
model: sonnet
tools: [Read, Write, Bash]
---"""
    assert validate_yaml_frontmatter(valid_yaml) == True

def test_validate_relative_paths():
    # Test against actual file system
    assert validate_relative_paths("agents/engineering/cs-architect.md", "senior-architect") == True
```

### Integration Tests
```bash
# Test end-to-end agent creation
python scripts/agent_builder.py --non-interactive \
  --config test-agent-config.json \
  --output /tmp/test-agent.md

# Validate generated agent
python scripts/validate_agent.py /tmp/test-agent.md

# Clean up
rm /tmp/test-agent.md
```

### Validation Tests
```bash
# Test all existing agents pass validation
python scripts/validate_agent.py --all

# Test all existing skills pass validation
python scripts/validate_skill.py --all

# Expected: 100% pass rate for existing agents/skills
```

---

## Rollout Plan

### Phase 1: Internal Testing (Day 10-12)
- Create 2 test agents using agent_builder.py
- Create 1 test skill using skill_builder.py
- Validate no errors, consistent output
- Document any issues found

### Phase 2: Team Rollout (Day 13-15)
- Announce new builders in team channel
- Provide usage documentation link
- Create example video/walkthrough
- Monitor first 3-5 uses, collect feedback

### Phase 3: Iteration (Day 16-20)
- Address user feedback
- Fix any discovered bugs
- Add requested features (if quick wins)
- Update documentation with FAQs

---

## Maintenance & Support

### Ongoing Maintenance
- **Template updates:** When agent/skill templates change, update builders
- **Validation updates:** Add new checks as patterns emerge
- **Catalog updates:** Ensure catalog format stays consistent
- **Documentation:** Keep CLAUDE.md synchronized with tool changes

### Support Channels
- **Documentation:** CLAUDE.md, scripts/README.md
- **Issues:** GitHub issues for bug reports
- **Questions:** Team channel for usage questions
- **Updates:** Update CHANGELOG.md for builder changes

---

## Future Enhancements (Post-MVP)

### Phase 2 Integration: Slash Commands
```bash
/agent.create --name data-engineer --domain engineering --skill data-pipeline
/skill.create --name data-quality --domain engineering
/validate --all
```

### Phase 5 Integration: Orchestration
```
@cs-repository-manager create agent cs-sales-engineer for product domain
  → Invokes agent_builder.py programmatically
  → Auto-commits to feature branch
  → Creates PR with description
```

### Advanced Features
- **Batch creation:** Create multiple agents/skills from CSV/JSON
- **Template customization:** User-defined templates beyond defaults
- **Migration tools:** Migrate existing agents to new format
- **Analytics:** Track creation metrics, common patterns
- **AI suggestions:** Recommend workflows, tools based on agent type

---

## Success Metrics (Post-Launch)

### Adoption Metrics
- **Target:** 100% of new agents created via builder (vs manual)
- **Target:** 100% of new skills created via builder (vs manual)
- **Target:** 0 YAML errors in new agents (100% pass validation)
- **Target:** 0 path errors in new agents (100% pass validation)

### Efficiency Metrics
- **Baseline:** 2 days per agent, 3 days per skill (manual)
- **Target:** 1 hour per agent, 2 hours per skill (builder)
- **Measurement:** Track creation time for next 10 agents/skills

### Quality Metrics
- **Validation pass rate:** 100% for builder-generated agents/skills
- **Catalog consistency:** 100% of new agents/skills in catalogs
- **Template adherence:** 100% match to template structure

---

## Appendix A: Example Commands

### Agent Builder - Interactive Mode
```bash
$ python scripts/agent_builder.py

🤖 Agent Builder - Create a new agent

Agent name (without cs- prefix): data-engineer
Domain:
  1. marketing
  2. product
  3. engineering
  4. delivery
Select domain (1-4): 3

Skill package: data-pipeline

Description: Orchestrates data pipeline workflows for ETL processes

Model:
  1. sonnet (recommended)
  2. opus
  3. haiku
Select model (1-3): 1

Tools (select multiple, comma-separated):
  1. Read
  2. Write
  3. Bash
  4. Grep
  5. Glob
Select tools (e.g., 1,2,3): 1,2,3

✅ Generating agent: agents/engineering/cs-data-engineer.md
✅ Validating YAML frontmatter... OK
✅ Validating relative paths... OK
✅ Updating AGENTS_CATALOG.md... OK

🎉 Agent created successfully!

📁 Location: agents/engineering/cs-data-engineer.md
📝 Next steps:
   1. Review and customize workflows
   2. Test relative path: ../../skills/engineering-team/data-pipeline/
   3. Commit: git add agents/engineering/cs-data-engineer.md docs/AGENTS_CATALOG.md
```

### Skill Builder - Interactive Mode
```bash
$ python scripts/skill_builder.py

📦 Skill Builder - Create a new skill

Skill name: data-quality
Domain:
  1. marketing-team
  2. product-team
  3. engineering-team
  4. delivery-team
Select domain (1-4): 3

Description: Data quality validation and profiling tools

Number of Python tools (1-10): 3
Number of reference docs (1-10): 2

✅ Creating directory structure... OK
✅ Generating SKILL.md... OK
✅ Creating Python tools (3)... OK
   - scripts/data_validator.py
   - scripts/data_profiler.py
   - scripts/quality_reporter.py
✅ Creating reference docs (2)... OK
   - references/data_quality_metrics.md
   - references/validation_rules.md
✅ Updating SKILLS_CATALOG.md... OK

🎉 Skill created successfully!

📁 Location: skills/engineering-team/data-quality/
📝 Next steps:
   1. Implement Python tools (see scripts/*.py)
   2. Write reference documentation (see references/*.md)
   3. Add example templates to assets/
   4. Create agent: python scripts/agent_builder.py
```

---

## Appendix B: Validation Output Examples

### Agent Validation - Success
```bash
$ python scripts/validate_agent.py agents/engineering/cs-data-engineer.md

✅ Validating: agents/engineering/cs-data-engineer.md

✅ File exists and readable
✅ YAML frontmatter present
✅ Required fields: name, description, skills, domain, model, tools
✅ Domain value valid: engineering
✅ Model value valid: sonnet
✅ Tools values valid: Read, Write, Bash
✅ Relative path resolves: ../../skills/engineering-team/data-pipeline/
✅ Minimum 3 workflows documented (found: 4)
✅ Skill package exists: skills/engineering-team/data-pipeline/

🎉 Validation passed: 0 errors, 0 warnings
```

### Agent Validation - Errors
```bash
$ python scripts/validate_agent.py agents/engineering/cs-broken-agent.md

❌ Validating: agents/engineering/cs-broken-agent.md

✅ File exists and readable
✅ YAML frontmatter present
❌ Missing required field: 'model'
❌ Invalid domain value: 'data' (must be one of: marketing, product, engineering, delivery)
❌ Invalid tool value: 'Deploy' (must be subset of: Read, Write, Bash, Grep, Glob)
❌ Relative path does not resolve: ../../skills/engineering-team/nonexistent-skill/
⚠️  Only 2 workflows documented (minimum: 3)

❌ Validation failed: 4 errors, 1 warning

Fix these issues and run validation again.
```

---

## Appendix C: Configuration File Examples

### Agent Configuration (JSON)
```json
{
  "name": "data-engineer",
  "domain": "engineering",
  "skill_package": "data-pipeline",
  "description": "Orchestrates data pipeline workflows for ETL processes",
  "model": "sonnet",
  "tools": ["Read", "Write", "Bash", "Grep"],
  "workflows": [
    "Pipeline Setup",
    "Data Transformation",
    "Quality Validation",
    "Deployment"
  ]
}
```

### Skill Configuration (JSON)
```json
{
  "name": "data-quality",
  "domain": "engineering-team",
  "description": "Data quality validation and profiling tools",
  "tool_count": 3,
  "tool_names": [
    "data_validator",
    "data_profiler",
    "quality_reporter"
  ],
  "reference_count": 2,
  "reference_names": [
    "data_quality_metrics",
    "validation_rules"
  ]
}
```

---

**Document Version:** 1.0
**Last Updated:** 2025-11-22
**Status:** Ready for Implementation
**Next Action:** Exit plan mode and begin Phase 1 (cs-architect design)
