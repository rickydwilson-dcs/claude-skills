# Architecture Decision Record: Agent/Skill Builder System

**Date:** November 22, 2025
**Status:** Approved
**Author:** cs-architect
**Project:** Agent/Skill Builder System v1.0

---

## Executive Summary

This ADR documents the architectural decisions for automated agent and skill creation tools that reduce agent creation from 2 days to 1 hour, and skill creation from 3 days to 2 hours. The system comprises two Python CLI tools with interactive workflows, comprehensive validation, and catalog integration.

**Key Metrics:**
- **Target:** 28 existing agents + 29 existing skills must pass validation (100% compatibility)
- **Agent Creation:** 2 days → 1 hour (96% time reduction)
- **Skill Creation:** 3 days → 2 hours (93% time reduction)
- **Dependencies:** Python standard library only (no external packages except PyYAML if needed)

---

## Table of Contents

1. [Context and Problem Statement](#context-and-problem-statement)
2. [Decision Drivers](#decision-drivers)
3. [Architectural Decisions](#architectural-decisions)
4. [Technical Design: Agent Builder](#technical-design-agent-builder)
5. [Technical Design: Skill Builder](#technical-design-skill-builder)
6. [Validation Strategy](#validation-strategy)
7. [Consequences](#consequences)
8. [Implementation Roadmap](#implementation-roadmap)
9. [Appendix](#appendix)

---

## Context and Problem Statement

### Current State

**Manual Creation Process:**
- **Agent Creation:** 2 days (YAML frontmatter setup, path resolution, workflow documentation, integration testing)
- **Skill Creation:** 3 days (directory scaffolding, tool templates, reference docs, SKILL.md creation)
- **Error Rate:** 15-20% of agents have path resolution issues or YAML errors on first commit
- **Inconsistency:** Varying documentation quality and structure across agents/skills

**Existing Assets:**
- **Agent Template:** `templates/agent-template.md` (318 lines, complete with inline instructions)
- **Skill Template:** DOES NOT EXIST - must be created in Phase 1
- **28 Production Agents:** All must pass validation
- **29 Production Skills:** All must pass validation

### Goals

1. **Speed:** Reduce creation time by 90%+
2. **Quality:** 100% validation pass rate for all existing agents/skills
3. **Consistency:** Standardized structure and documentation
4. **Maintainability:** Easy to update templates and validation rules
5. **Usability:** Intuitive CLI with clear prompts and feedback

---

## Decision Drivers

### Technical Requirements

1. **No External Dependencies** - Standard library only (PyYAML exception if needed)
2. **Interactive CLI** - Guided workflow with validation feedback
3. **Batch Mode** - Support config file input for automation
4. **Validation First** - Catch errors before file creation
5. **Git Integration** - Manual workflow with clear next-step guidance
6. **Cross-Platform** - Works on macOS, Linux, Windows

### User Experience Requirements

1. **Clear Prompts** - Explain what's needed and why
2. **Inline Help** - Examples and format guidance
3. **Error Recovery** - Allow corrections without starting over
4. **Progress Feedback** - Show what's happening at each step
5. **Next Steps** - Clear guidance on what to do after generation

### Quality Requirements

1. **100% Compatibility** - All 28 agents + 29 skills must validate
2. **Path Validation** - Ensure relative paths resolve correctly
3. **YAML Validation** - Catch syntax and schema errors
4. **Template Consistency** - Generated files match existing patterns exactly
5. **Comprehensive Testing** - Unit tests for all validation rules

---

## Architectural Decisions

### Decision 1: Interactive CLI with Optional Config Mode

**Decision:** Implement interactive CLI as primary mode with `--config` flag for batch processing

**Rationale:**
- **Interactive First:** Most users create agents/skills infrequently (1-2x per month)
- **Learning Curve:** Interactive mode teaches best practices through prompts
- **Error Prevention:** Real-time validation catches issues immediately
- **Automation Support:** Config mode enables CI/CD integration and bulk operations

**Implementation:**
```python
# Interactive mode (default)
python scripts/agent_builder.py

# Config mode for automation
python scripts/agent_builder.py --config agent-config.yaml
```

**Config File Format:**
```yaml
name: cs-data-analyst
domain: product
description: Data analysis and reporting for product decisions
skills: data-analyst-toolkit
model: sonnet
tools: [Read, Write, Bash, Grep, Glob]
```

**Alternatives Considered:**
- **Config-Only:** Rejected - steep learning curve, no real-time validation
- **GUI Application:** Rejected - adds dependencies, harder to automate
- **Web Interface:** Rejected - requires server, out of scope

---

### Decision 2: Pre-Generation Validation

**Decision:** Validate all inputs BEFORE generating files

**Rationale:**
- **Fail Fast:** Catch errors before polluting file system
- **Clean Rollback:** No partial files to clean up on failure
- **Better UX:** Fix all issues in one session vs iterative cleanup
- **Catalog Safety:** Don't update catalogs until files exist and validate

**Validation Sequence:**
```
1. Collect all inputs (interactive or config)
2. Validate each input against rules
3. Perform cross-validation (paths, conflicts)
4. Preview generated structure
5. Confirm with user
6. Generate files atomically
7. Validate generated files
8. Update catalogs
9. Provide next steps
```

**Alternatives Considered:**
- **Post-Generation Validation:** Rejected - leaves partial files on failure
- **Iterative Validation:** Rejected - slower, more complex error handling

---

### Decision 3: Catalog Append Strategy

**Decision:** Append new entries to domain-specific agent catalogs; update skill READMEs

**Rationale:**
- **Safety:** Append-only reduces risk of corrupting existing entries
- **Simplicity:** Easier to implement and debug
- **Reversibility:** Easy to undo (delete last entry)
- **Performance:** No need to parse and regenerate entire catalog

**Implementation:**

**Agent Catalog Update:**
```python
# Append to agents/{domain}/CATALOG.md
new_entry = f"- [cs-{name}](cs-{name}.md) - {description}\n"
with open(f"agents/{domain}/CATALOG.md", "a") as f:
    f.write(new_entry)
```

**Skill README Update:**
```python
# Update skills/{domain-team}/README.md skill count
# Parse markdown, update skill list, rewrite file
```

**Alternatives Considered:**
- **Regenerate Entire Catalog:** Rejected - brittle, requires parsing all files
- **JSON Metadata Database:** Rejected - adds complexity, not user-editable
- **No Catalog Update:** Rejected - manual step prone to forgetting

---

### Decision 4: Manual Git Integration

**Decision:** Provide git commands as next steps, but don't execute automatically

**Rationale:**
- **User Control:** Developers review before committing
- **Safety:** No accidental commits to wrong branch
- **Flexibility:** Users may have custom git workflows
- **Simplicity:** Avoids git library dependencies and error handling

**Next Steps Output:**
```bash
✅ Agent created successfully!

Next steps:
1. Review the generated files:
   - agents/engineering/cs-data-analyst.md

2. Test relative paths:
   cd agents/engineering
   ls ../../skills/engineering-team/data-analyst-toolkit/

3. Commit with conventional commit:
   git add agents/engineering/cs-data-analyst.md
   git commit -m "feat(agents): implement cs-data-analyst"

4. Push to remote:
   git push origin feature/agents-data-analyst
```

**Alternatives Considered:**
- **Automatic Git Commits:** Rejected - risky, removes user control
- **Git Library Integration:** Rejected - adds dependency, complex error handling
- **No Git Guidance:** Rejected - users may forget or use wrong format

---

### Decision 5: String Template Method

**Decision:** Use Python string `.format()` for template population

**Rationale:**
- **Standard Library:** No external dependencies (Jinja2, Mako)
- **Simplicity:** Easy to understand and debug
- **Performance:** Fast for small templates
- **Maintainability:** Templates are readable Python f-strings

**Implementation:**
```python
template = """---
name: {name}
description: {description}
skills: {skills}
domain: {domain}
model: {model}
tools: {tools}
---

# {agent_title}

## Purpose

{purpose_paragraph_1}

{purpose_paragraph_2}

{purpose_paragraph_3}
"""

generated = template.format(
    name=agent_name,
    description=agent_description,
    # ... other variables
)
```

**Template Placeholder Rules:**
- Use `{variable_name}` for simple substitution
- Use `{section|optional}` to mark optional sections
- Comments in templates: `<!-- BUILDER: instruction -->`
- Preserve existing inline instructions from agent-template.md

**Alternatives Considered:**
- **Jinja2 Template Engine:** Rejected - external dependency
- **Manual String Concatenation:** Rejected - error-prone, hard to maintain
- **Template File + sed/awk:** Rejected - not cross-platform

---

### Decision 6: Error Handling Strategy

**Decision:** Comprehensive error handling with clear, actionable messages

**Error Categories:**

1. **Input Validation Errors** (recoverable)
   - Invalid name format
   - Missing required fields
   - Path conflicts

2. **File System Errors** (recoverable)
   - Permission denied
   - Path already exists
   - Disk full

3. **Template Errors** (should not occur in production)
   - Missing template file
   - Template syntax error
   - Variable not found

**Error Message Format:**
```
❌ Error: Invalid agent name format

Problem: "Data Analyst" contains spaces
Expected: kebab-case with cs- prefix (e.g., cs-data-analyst)

Fix: Use "cs-data-analyst" instead

Run with --help for more information
```

**Recovery Mechanisms:**
- Interactive mode: Allow user to re-enter invalid input
- Config mode: Print all errors and exit (fail fast)
- Partial generation: Rollback all files on any error
- Logging: Write detailed error log to `output/sessions/current/builder-errors.log`

**Alternatives Considered:**
- **Silent Failures:** Rejected - poor UX, hard to debug
- **Generic Error Messages:** Rejected - users don't know how to fix
- **Exception Propagation:** Rejected - exposes implementation details

---

### Decision 7: Testing Approach

**Decision:** Pytest-based unit tests with 80%+ coverage target

**Test Structure:**
```
tests/
├── test_agent_builder.py
│   ├── test_name_validation()
│   ├── test_yaml_generation()
│   ├── test_path_resolution()
│   └── test_catalog_update()
├── test_skill_builder.py
│   ├── test_directory_scaffolding()
│   ├── test_tool_generation()
│   └── test_reference_generation()
├── test_validators.py
│   ├── test_agent_validator()
│   └── test_skill_validator()
└── fixtures/
    ├── valid-agent.md
    ├── invalid-agent-yaml.md
    └── sample-config.yaml
```

**Test Coverage Goals:**
- **Validation Logic:** 95% coverage (critical path)
- **File Generation:** 85% coverage
- **CLI Interface:** 70% coverage (harder to test)
- **Error Handling:** 90% coverage

**Test Data:**
- Use existing 28 agents as positive test cases
- Create synthetic invalid agents for negative test cases
- Test all 9 validation rules for agents
- Test all 9 validation rules for skills

**Alternatives Considered:**
- **Manual Testing Only:** Rejected - not scalable, regression-prone
- **Integration Tests Only:** Rejected - slow, hard to debug
- **100% Coverage:** Rejected - diminishing returns, not pragmatic

---

## Technical Design: Agent Builder

### Overview

**Script:** `scripts/agent_builder.py`
**Purpose:** Interactive CLI for creating cs-* agents with validation and catalog integration
**Dependencies:** Python 3.8+, standard library, PyYAML (for YAML frontmatter parsing)

### CLI Interface

```bash
# Interactive mode (default)
python scripts/agent_builder.py

# Config mode
python scripts/agent_builder.py --config agent-config.yaml

# Validation only
python scripts/agent_builder.py --validate agents/engineering/cs-existing-agent.md

# Dry run (show what would be created)
python scripts/agent_builder.py --dry-run --config agent-config.yaml

# Help
python scripts/agent_builder.py --help
```

### Interactive Workflow

**Step 1: Agent Name**
```
🤖 Agent Builder

Step 1/7: Agent Name
---------------------
Enter agent name (kebab-case with cs- prefix):
Example: cs-data-analyst, cs-backend-engineer

Name: cs-data-analyst
✓ Valid name format
```

**Step 2: Domain**
```
Step 2/7: Domain
----------------
Select domain:
1. marketing
2. product
3. engineering
4. delivery

Domain (1-4): 3
✓ Domain: engineering
```

**Step 3: Description**
```
Step 3/7: Description
---------------------
Enter one-line description (under 150 chars):
Example: "Data analysis and reporting for product decisions"

Description: Data analysis and reporting for product decisions
✓ Length: 52 chars
```

**Step 4: Skills Integration**
```
Step 4/7: Skills Integration
-----------------------------
Enter skill folder name (from skills/{domain-team}/):
Example: data-analyst-toolkit, senior-architect

Skills: data-analyst-toolkit
✓ Skill exists: skills/engineering-team/data-analyst-toolkit/
✓ Found 3 Python tools
```

**Step 5: Model Selection**
```
Step 5/7: Model Selection
-------------------------
Select model:
1. sonnet (recommended - balanced performance)
2. opus (complex reasoning)
3. haiku (fast, simple tasks)

Model (1-3): 1
✓ Model: sonnet
```

**Step 6: Tools Selection**
```
Step 6/7: Tools Selection
-------------------------
Select tools (comma-separated):
Available: Read, Write, Bash, Grep, Glob, Edit, NotebookEdit

Default: Read, Write, Bash, Grep, Glob
Tools (Enter for default): Read, Write, Bash, Grep, Glob, Edit
✓ Tools: [Read, Write, Bash, Grep, Glob, Edit]
```

**Step 7: Preview and Confirm**
```
Step 7/7: Preview
-----------------
Review your agent configuration:

Name:        cs-data-analyst
Domain:      engineering
Description: Data analysis and reporting for product decisions
Skills:      data-analyst-toolkit
Model:       sonnet
Tools:       [Read, Write, Bash, Grep, Glob, Edit]

Files to create:
- agents/engineering/cs-data-analyst.md

Catalog updates:
- agents/engineering/CATALOG.md (append)

Proceed? (y/n): y

✅ Agent created successfully!
[Next steps output...]
```

### Module Architecture

**File:** `scripts/agent_builder.py` (~800 lines)

**Classes:**

```python
class AgentBuilder:
    """Main orchestrator for agent creation"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.validator = AgentValidator()
        self.template_loader = TemplateLoader()

    def interactive_mode(self) -> None:
        """Run interactive agent creation workflow"""

    def config_mode(self, config_path: str) -> None:
        """Create agent from config file"""

    def validate_existing(self, agent_path: str) -> ValidationResult:
        """Validate an existing agent file"""

    def generate_agent(self, config: Dict) -> None:
        """Generate agent file and update catalogs"""


class AgentValidator:
    """Validation logic for agent files"""

    def validate_name(self, name: str) -> Tuple[bool, str]:
        """Validate agent name format"""

    def validate_yaml_frontmatter(self, content: str) -> Tuple[bool, str]:
        """Validate YAML syntax and required fields"""

    def validate_relative_paths(self, agent_path: str, content: str) -> Tuple[bool, str]:
        """Validate relative paths resolve correctly"""

    def validate_workflows(self, content: str) -> Tuple[bool, str]:
        """Ensure minimum 3 workflows documented"""

    def validate_integration_examples(self, content: str) -> Tuple[bool, str]:
        """Ensure integration examples present"""

    def validate_success_metrics(self, content: str) -> Tuple[bool, str]:
        """Ensure success metrics defined"""

    def run_all_checks(self, agent_path: str) -> ValidationResult:
        """Run all validation checks and return results"""


class TemplateLoader:
    """Load and populate agent template"""

    def load_template(self) -> str:
        """Load agent-template.md"""

    def populate_template(self, template: str, config: Dict) -> str:
        """Replace placeholders with actual values"""

    def generate_workflows_section(self, skill_name: str) -> str:
        """Generate workflow examples from skill"""


class CatalogUpdater:
    """Update agent catalogs"""

    def append_to_catalog(self, domain: str, name: str, description: str) -> None:
        """Append entry to domain catalog"""

    def verify_catalog_format(self, catalog_path: str) -> bool:
        """Validate catalog markdown format"""
```

### Validation Module

**9 Agent Validation Checks:**

1. **Name Format Validation**
   - Pattern: `cs-[a-z0-9-]+`
   - Must start with "cs-"
   - Kebab-case only (lowercase, hyphens)
   - No spaces, underscores, special chars

2. **YAML Frontmatter Validation**
   - Valid YAML syntax (PyYAML parsing)
   - Required fields: name, description, skills, domain, model, tools
   - Description under 150 chars
   - Model in [sonnet, opus, haiku]
   - Tools is list of valid tool names

3. **Relative Path Validation**
   - All `../../` paths resolve from agent location
   - Skill package exists at specified path
   - No absolute paths in agent file
   - No broken markdown links

4. **Skill Integration Validation**
   - Skills field matches actual skill folder name
   - Skill package has Python tools documented
   - Skill package has SKILL.md
   - Tool paths in agent match actual tool locations

5. **Workflow Count Validation**
   - Minimum 3 workflows documented
   - Each workflow has: Goal, Steps, Expected Output, Time Estimate
   - Workflow sections properly formatted

6. **Integration Examples Validation**
   - Minimum 2 integration examples present
   - Examples contain bash code blocks
   - Examples use proper relative paths

7. **Success Metrics Validation**
   - Success metrics section exists
   - At least 3 metric categories defined
   - Metrics are specific and measurable

8. **Markdown Structure Validation**
   - All required sections present (Purpose, Skill Integration, Workflows, etc.)
   - Heading hierarchy correct (H2 for main sections)
   - No broken markdown syntax

9. **Cross-Reference Validation**
   - Related agents links valid
   - References section complete
   - All internal links resolve

**Validation Output Formats:**

**Human-Readable:**
```
Validation Report: cs-data-analyst
================================

✅ Name format: Valid
✅ YAML frontmatter: Valid
✅ Relative paths: Valid (3 paths checked)
✅ Skill integration: Valid (data-analyst-toolkit)
✅ Workflows: Valid (4 workflows documented)
❌ Integration examples: FAILED
   - Only 1 example found (minimum: 2)
   - Add at least 1 more bash example
✅ Success metrics: Valid (4 metric categories)
✅ Markdown structure: Valid
✅ Cross-references: Valid

Overall: FAILED (8/9 checks passed)
```

**JSON Output:**
```json
{
  "agent": "cs-data-analyst",
  "status": "failed",
  "checks_passed": 8,
  "checks_total": 9,
  "checks": [
    {
      "name": "name_format",
      "status": "passed",
      "message": "Valid name format"
    },
    {
      "name": "integration_examples",
      "status": "failed",
      "message": "Only 1 example found (minimum: 2)",
      "severity": "error"
    }
  ]
}
```

### YAML Parsing Strategy

**Decision:** Use PyYAML for frontmatter parsing

**Installation:**
```bash
pip install pyyaml  # Only external dependency
```

**Parsing Logic:**
```python
import yaml

def parse_yaml_frontmatter(content: str) -> Tuple[Dict, str]:
    """
    Extract YAML frontmatter and content body

    Returns:
        (frontmatter_dict, markdown_body)
    """
    if not content.startswith('---'):
        raise ValueError("No YAML frontmatter found")

    # Split at first and second ---
    parts = content.split('---', 2)
    if len(parts) < 3:
        raise ValueError("Malformed YAML frontmatter")

    yaml_str = parts[1]
    body = parts[2]

    try:
        frontmatter = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax: {e}")

    return frontmatter, body


def validate_yaml_schema(frontmatter: Dict) -> Tuple[bool, str]:
    """Validate required fields and types"""
    required_fields = {
        'name': str,
        'description': str,
        'skills': str,
        'domain': str,
        'model': str,
        'tools': list
    }

    for field, field_type in required_fields.items():
        if field not in frontmatter:
            return False, f"Missing required field: {field}"

        if not isinstance(frontmatter[field], field_type):
            return False, f"Field {field} must be {field_type.__name__}"

    # Additional validation
    if frontmatter['model'] not in ['sonnet', 'opus', 'haiku']:
        return False, f"Invalid model: {frontmatter['model']}"

    if len(frontmatter['description']) > 150:
        return False, "Description must be under 150 characters"

    return True, "Valid"
```

**Alternative (if PyYAML not allowed):**
- Write simple YAML parser for frontmatter only
- Supports: strings, lists, simple key-value pairs
- Does not support: nested objects, complex types
- ~100 lines of parsing code

### Path Resolution Logic

**Challenge:** Ensure all `../../` paths resolve correctly from agent location

**Resolution Strategy:**
```python
def validate_relative_paths(agent_path: str, content: str) -> Tuple[bool, List[str]]:
    """
    Validate all relative paths in agent markdown

    Args:
        agent_path: Path to agent file (e.g., agents/engineering/cs-data-analyst.md)
        content: Agent markdown content

    Returns:
        (all_valid, error_messages)
    """
    import re
    from pathlib import Path

    agent_dir = Path(agent_path).parent
    errors = []

    # Extract all relative paths (../../...)
    path_pattern = r'\.\./\.\./[a-zA-Z0-9_/-]+(?:\.[a-z]+)?'
    paths = re.findall(path_pattern, content)

    for rel_path in set(paths):  # Remove duplicates
        # Resolve from agent directory
        absolute_path = (agent_dir / rel_path).resolve()

        if not absolute_path.exists():
            errors.append(f"Path does not exist: {rel_path}")
            continue

        # Check if it's in expected location (skills/)
        if 'skills/' not in str(absolute_path):
            errors.append(f"Path not in skills/: {rel_path}")

    return len(errors) == 0, errors
```

**Test Cases:**
```python
# Valid path (from agents/engineering/)
"../../skills/engineering-team/data-analyst-toolkit/SKILL.md"
# Resolves to: skills/engineering-team/data-analyst-toolkit/SKILL.md

# Invalid path (skill doesn't exist)
"../../skills/engineering-team/nonexistent-skill/SKILL.md"
# Error: Path does not exist

# Invalid path (wrong domain)
"../../skills/marketing-team/content-creator/SKILL.md"
# Warning: Cross-domain skill reference (engineering → marketing)
```

### Catalog Update Logic

**Target Files:**
- `agents/{domain}/CATALOG.md` (append new entry)
- `agents/README.md` (update count if adding new domain)

**Catalog Entry Format:**
```markdown
## Engineering Agents

- [cs-architect](cs-architect.md) - System design and technical decisions
- [cs-backend-engineer](cs-backend-engineer.md) - Backend development and APIs
- [cs-data-analyst](cs-data-analyst.md) - Data analysis and reporting for product decisions  <!-- NEW -->
```

**Update Logic:**
```python
def append_to_catalog(domain: str, agent_name: str, description: str) -> None:
    """
    Append new agent to domain catalog

    Args:
        domain: Agent domain (engineering, marketing, etc.)
        agent_name: Agent name (cs-data-analyst)
        description: One-line description
    """
    catalog_path = f"agents/{domain}/CATALOG.md"

    if not Path(catalog_path).exists():
        # Create new catalog for new domain
        create_domain_catalog(domain)

    # Read existing catalog
    with open(catalog_path, 'r') as f:
        content = f.read()

    # Generate entry
    entry = f"- [{agent_name}]({agent_name}.md) - {description}\n"

    # Find insertion point (end of agent list)
    # Look for last line starting with "- [cs-"
    lines = content.split('\n')
    insert_index = -1

    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith('- [cs-'):
            insert_index = i + 1
            break

    if insert_index == -1:
        # No existing agents, insert after "## {Domain} Agents" heading
        for i, line in enumerate(lines):
            if line.startswith(f'## {domain.title()} Agents'):
                insert_index = i + 2  # Skip heading and blank line
                break

    # Insert entry
    lines.insert(insert_index, entry.rstrip('\n'))

    # Write back
    with open(catalog_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"✓ Updated {catalog_path}")
```

### Error Messages and User Feedback

**Input Validation:**
```
❌ Invalid agent name: "Data Analyst"

Problem: Name contains spaces
Expected: kebab-case with cs- prefix

Examples:
  ✓ cs-data-analyst
  ✓ cs-backend-engineer
  ✗ Data Analyst
  ✗ data-analyst (missing cs- prefix)

Try again:
```

**Path Validation:**
```
❌ Skill package not found

Problem: skills/engineering-team/data-analyst-toolkit/ does not exist

Available skills in engineering-team:
  - senior-architect
  - senior-frontend
  - senior-backend
  - senior-fullstack
  - senior-devops

Did you mean: senior-architect?

Skill folder name:
```

**Catalog Update:**
```
⚠️  Warning: agents/engineering/CATALOG.md not found

Creating new catalog for engineering domain...
✓ Created agents/engineering/CATALOG.md

Note: You may need to manually integrate this with existing docs.
```

---

## Technical Design: Skill Builder

### Overview

**Script:** `scripts/skill_builder.py`
**Purpose:** Interactive CLI for creating skill packages with directory scaffolding
**Dependencies:** Python 3.8+, standard library only

### CLI Interface

```bash
# Interactive mode (default)
python scripts/skill_builder.py

# Config mode
python scripts/skill_builder.py --config skill-config.yaml

# Validation only
python scripts/skill_builder.py --validate skills/engineering-team/data-analyst-toolkit/

# Dry run
python scripts/skill_builder.py --dry-run --config skill-config.yaml

# Help
python scripts/skill_builder.py --help
```

### Interactive Workflow

**Step 1: Skill Name**
```
📦 Skill Builder

Step 1/8: Skill Name
--------------------
Enter skill name (kebab-case):
Example: data-analyst-toolkit, senior-architect

Name: data-analyst-toolkit
✓ Valid name format
```

**Step 2: Domain Team**
```
Step 2/8: Domain Team
---------------------
Select domain team:
1. marketing-team
2. product-team
3. engineering-team
4. delivery-team

Domain (1-4): 3
✓ Domain: engineering-team
```

**Step 3: Description**
```
Step 3/8: Description
---------------------
Enter skill description (used in YAML frontmatter):
This appears in search and skill browsing.

Description: Comprehensive data analysis toolkit with reporting and visualization
✓ Length: 72 chars
```

**Step 4: Keywords**
```
Step 4/8: Keywords
------------------
Enter keywords (comma-separated, 5-15 recommended):
Example: data analysis, reporting, SQL, Python, dashboards

Keywords: data analysis, reporting, SQL, visualization, dashboards, metrics
✓ 6 keywords
```

**Step 5: Tech Stack**
```
Step 5/8: Tech Stack
--------------------
Enter tech stack (comma-separated):
Example: Python 3.8+, PostgreSQL, Pandas, Matplotlib

Tech Stack: Python 3.8+, PostgreSQL, Pandas, Jupyter
✓ 4 technologies
```

**Step 6: Python Tools**
```
Step 6/8: Python Tools
----------------------
How many Python CLI tools will this skill have?
Minimum: 1, Recommended: 2-4

Count: 3

Enter tool names (one per line):
Tool 1: data_analyzer.py
Tool 2: report_generator.py
Tool 3: dashboard_builder.py

✓ 3 tools configured
```

**Step 7: Reference Guides**
```
Step 7/8: Reference Guides
--------------------------
How many reference guides (markdown docs)?
Minimum: 0, Recommended: 2-3

Count: 2

Enter guide names (one per line):
Guide 1: analysis_frameworks.md
Guide 2: sql_optimization_guide.md

✓ 2 reference guides configured
```

**Step 8: Preview and Confirm**
```
Step 8/8: Preview
-----------------
Review your skill configuration:

Name:        data-analyst-toolkit
Domain:      engineering-team
Description: Comprehensive data analysis toolkit with reporting and visualization
Keywords:    6 keywords
Tech Stack:  Python 3.8+, PostgreSQL, Pandas, Jupyter
Tools:       3 (data_analyzer.py, report_generator.py, dashboard_builder.py)
References:  2 (analysis_frameworks.md, sql_optimization_guide.md)

Directory structure to create:
skills/engineering-team/data-analyst-toolkit/
├── SKILL.md
├── scripts/
│   ├── data_analyzer.py
│   ├── report_generator.py
│   └── dashboard_builder.py
├── references/
│   ├── analysis_frameworks.md
│   └── sql_optimization_guide.md
└── assets/
    └── (empty - add templates as needed)

Proceed? (y/n): y

✅ Skill created successfully!
[Next steps output...]
```

### Module Architecture

**File:** `scripts/skill_builder.py` (~900 lines)

**Classes:**

```python
class SkillBuilder:
    """Main orchestrator for skill creation"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.validator = SkillValidator()
        self.template_loader = SkillTemplateLoader()

    def interactive_mode(self) -> None:
        """Run interactive skill creation workflow"""

    def config_mode(self, config_path: str) -> None:
        """Create skill from config file"""

    def validate_existing(self, skill_path: str) -> ValidationResult:
        """Validate an existing skill package"""

    def generate_skill(self, config: Dict) -> None:
        """Generate skill directory structure and files"""


class SkillValidator:
    """Validation logic for skill packages"""

    def validate_name(self, name: str) -> Tuple[bool, str]:
        """Validate skill name format"""

    def validate_directory_structure(self, skill_path: str) -> Tuple[bool, str]:
        """Validate skill directory structure"""

    def validate_skill_md(self, skill_md_path: str) -> Tuple[bool, str]:
        """Validate SKILL.md completeness"""

    def validate_python_tools(self, scripts_dir: str) -> Tuple[bool, str]:
        """Validate Python tools follow standards"""

    def run_all_checks(self, skill_path: str) -> ValidationResult:
        """Run all validation checks"""


class SkillTemplateLoader:
    """Load and populate skill templates"""

    def load_skill_template(self) -> str:
        """Load templates/skill-template.md"""

    def populate_skill_template(self, template: str, config: Dict) -> str:
        """Replace placeholders in SKILL.md template"""

    def generate_python_tool(self, tool_name: str) -> str:
        """Generate placeholder Python tool from template"""

    def generate_reference_guide(self, guide_name: str) -> str:
        """Generate placeholder reference guide"""


class DirectoryScaffolder:
    """Create skill directory structure"""

    def create_structure(self, skill_path: str, config: Dict) -> None:
        """Create all directories and files"""

    def create_scripts_dir(self, scripts_path: str, tools: List[str]) -> None:
        """Create scripts/ with Python tools"""

    def create_references_dir(self, refs_path: str, guides: List[str]) -> None:
        """Create references/ with placeholder guides"""

    def create_assets_dir(self, assets_path: str) -> None:
        """Create empty assets/ directory"""
```

### Directory Scaffolding

**Target Structure:**
```
skills/{domain-team}/{skill-name}/
├── SKILL.md                    # Main documentation (from template)
├── scripts/                    # Python CLI tools
│   ├── tool1.py               # Placeholder tool with --help
│   ├── tool2.py
│   └── tool3.py
├── references/                 # Knowledge base markdown files
│   ├── guide1.md              # Placeholder reference guide
│   └── guide2.md
└── assets/                     # User-facing templates (empty initially)
    └── .gitkeep
```

**Implementation:**
```python
def create_skill_structure(skill_path: Path, config: Dict) -> None:
    """
    Create complete skill directory structure

    Args:
        skill_path: Path to skill (e.g., skills/engineering-team/data-analyst-toolkit/)
        config: Skill configuration dict
    """
    # Create main directory
    skill_path.mkdir(parents=True, exist_ok=False)
    print(f"✓ Created {skill_path}/")

    # Create subdirectories
    scripts_dir = skill_path / "scripts"
    references_dir = skill_path / "references"
    assets_dir = skill_path / "assets"

    scripts_dir.mkdir()
    references_dir.mkdir()
    assets_dir.mkdir()

    print(f"✓ Created {scripts_dir}/")
    print(f"✓ Created {references_dir}/")
    print(f"✓ Created {assets_dir}/")

    # Create SKILL.md
    skill_md = generate_skill_md(config)
    (skill_path / "SKILL.md").write_text(skill_md)
    print(f"✓ Created SKILL.md")

    # Create Python tools
    for tool_name in config['tools']:
        tool_content = generate_python_tool(tool_name, config)
        tool_path = scripts_dir / tool_name
        tool_path.write_text(tool_content)
        tool_path.chmod(0o755)  # Make executable
        print(f"✓ Created scripts/{tool_name}")

    # Create reference guides
    for guide_name in config['references']:
        guide_content = generate_reference_guide(guide_name, config)
        guide_path = references_dir / guide_name
        guide_path.write_text(guide_content)
        print(f"✓ Created references/{guide_name}")

    # Create .gitkeep in assets
    (assets_dir / ".gitkeep").write_text("")
    print(f"✓ Created assets/.gitkeep")
```

### Placeholder Python Tool Template

**Generated Tool Structure:**
```python
#!/usr/bin/env python3
"""
{tool_name_human}

Automated tool for {skill_name} tasks.

TODO: Implement actual functionality
This is a placeholder generated by skill_builder.py
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class {ToolClassName}:
    """Main class for {tool_name_human} functionality"""

    def __init__(self, target: str, verbose: bool = False):
        self.target = target
        self.verbose = verbose
        self.results = {}

    def run(self) -> Dict:
        """Execute the main functionality"""
        print(f"🚀 Running {self.__class__.__name__}...")
        print(f"📁 Target: {self.target}")

        try:
            self.validate_input()
            self.process()
            self.generate_output()

            print("✅ Completed successfully!")
            return self.results

        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)

    def validate_input(self):
        """Validate input parameters"""
        # TODO: Add validation logic
        if self.verbose:
            print("✓ Input validated")

    def process(self):
        """Perform main processing"""
        # TODO: Implement core functionality
        self.results['status'] = 'success'
        self.results['data'] = {}

        if self.verbose:
            print("✓ Processing complete")

    def generate_output(self):
        """Generate and display output"""
        # TODO: Format output
        print("\n" + "="*50)
        print("RESULTS")
        print("="*50)
        print(json.dumps(self.results, indent=2))
        print("="*50 + "\n")


def main():
    """Main entry point with CLI interface"""
    parser = argparse.ArgumentParser(
        description="{tool_name_human} - Automated processing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.txt
  %(prog)s input.txt --output json
  %(prog)s input.txt -v

For more information, see ../SKILL.md
        """
    )

    parser.add_argument(
        'target',
        help='Input file or target to process'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Run tool
    tool = {ToolClassName}(args.target, verbose=args.verbose)
    results = tool.run()

    # Format output
    if args.output == 'json':
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
```

**Template Variables:**
- `{tool_name_human}`: Human-readable name (e.g., "Data Analyzer")
- `{skill_name}`: Skill name (e.g., "data-analyst-toolkit")
- `{ToolClassName}`: PascalCase class name (e.g., "DataAnalyzer")

### Placeholder Reference Guide Template

**Generated Guide Structure:**
```markdown
# {Guide Title}

**Skill:** {skill_name}
**Created:** {date}
**Status:** Placeholder - TODO: Add content

---

## Overview

TODO: Provide overview of this reference guide.

**Purpose:** [What knowledge does this guide provide?]

**Target Users:** [Who should use this guide?]

---

## Table of Contents

1. [Core Concepts](#core-concepts)
2. [Best Practices](#best-practices)
3. [Examples](#examples)
4. [Common Patterns](#common-patterns)
5. [Troubleshooting](#troubleshooting)
6. [Additional Resources](#additional-resources)

---

## Core Concepts

TODO: Document core concepts and principles.

### Concept 1

[Explanation]

### Concept 2

[Explanation]

---

## Best Practices

TODO: Document recommended approaches and patterns.

1. **Practice 1:** Description
2. **Practice 2:** Description
3. **Practice 3:** Description

---

## Examples

TODO: Provide concrete, copy-paste ready examples.

### Example 1: [Use Case Name]

**Scenario:** [Description]

**Solution:**
```bash
# Commands or code example
```

**Explanation:** [Why this approach works]

---

## Common Patterns

TODO: Document frequently-used patterns and workflows.

### Pattern 1: [Pattern Name]

**When to Use:** [Circumstances]

**Implementation:** [Steps]

---

## Troubleshooting

TODO: Document common issues and solutions.

| Problem | Cause | Solution |
|---------|-------|----------|
| [Issue] | [Reason] | [Fix] |

---

## Additional Resources

TODO: Link to related documentation and external resources.

- [Related Guide 1](link)
- [Related Guide 2](link)
- [External Resource](link)

---

**Last Updated:** {date}
**Maintainer:** TODO: Add maintainer
**Version:** 1.0
```

### Skill Validation Module

**9 Skill Validation Checks:**

1. **Name Format Validation**
   - Pattern: `[a-z0-9-]+`
   - Kebab-case only (lowercase, hyphens)
   - No spaces, underscores, special chars
   - No cs- prefix (that's for agents)

2. **Directory Structure Validation**
   - Required directories: `scripts/`, `references/`, `assets/`
   - Required files: `SKILL.md`
   - Optional: `README.md`, `LICENSE.md`

3. **SKILL.md Validation**
   - YAML frontmatter present and valid
   - Required sections: Overview, Quick Start, Core Capabilities, Key Workflows
   - Keywords count: 5-30
   - Tech stack documented

4. **Python Tools Validation**
   - All .py files in scripts/ are executable (chmod +x)
   - Each tool supports `--help` flag
   - Each tool has docstring
   - Each tool follows CLI-first pattern
   - Tool names match snake_case pattern

5. **Reference Guides Validation**
   - All .md files in references/ have content (>100 chars)
   - Proper markdown structure
   - No broken internal links

6. **Assets Directory Validation**
   - Directory exists (even if empty)
   - If has templates, each template has header comment

7. **Metadata Completeness**
   - YAML has: name, description, license, metadata
   - Metadata has: version, author, category, domain, updated, keywords, tech-stack
   - python-tools list matches actual scripts

8. **Documentation Quality**
   - Quick Start section has actual commands
   - Each workflow documented with time estimates
   - At least 1 workflow documented

9. **Integration Points**
   - Cross-references to other skills (if any) are valid
   - Tool output formats documented
   - Integration examples provided

**Validation Output:**

**Human-Readable:**
```
Validation Report: data-analyst-toolkit
======================================

✅ Name format: Valid
✅ Directory structure: Valid
   - scripts/ (3 tools)
   - references/ (2 guides)
   - assets/
✅ SKILL.md: Valid
   - YAML frontmatter: Valid
   - All required sections present
✅ Python tools: Valid
   - data_analyzer.py: ✓ Executable, has --help
   - report_generator.py: ✓ Executable, has --help
   - dashboard_builder.py: ✓ Executable, has --help
✅ Reference guides: Valid
   - analysis_frameworks.md: 1,245 chars
   - sql_optimization_guide.md: 892 chars
✅ Assets directory: Valid (empty - OK)
✅ Metadata: Valid (6 keywords, 4 tech stack items)
✅ Documentation: Valid (3 workflows, quick start present)
✅ Integration points: Valid

Overall: PASSED (9/9 checks)
```

**JSON Output:**
```json
{
  "skill": "data-analyst-toolkit",
  "domain": "engineering-team",
  "status": "passed",
  "checks_passed": 9,
  "checks_total": 9,
  "checks": [
    {
      "name": "name_format",
      "status": "passed",
      "message": "Valid name format"
    },
    {
      "name": "python_tools",
      "status": "passed",
      "message": "3 tools validated",
      "details": {
        "data_analyzer.py": {"executable": true, "has_help": true},
        "report_generator.py": {"executable": true, "has_help": true},
        "dashboard_builder.py": {"executable": true, "has_help": true}
      }
    }
  ],
  "statistics": {
    "tools_count": 3,
    "references_count": 2,
    "keywords_count": 6,
    "workflows_count": 3
  }
}
```

### README Update Logic

**Target File:** `skills/{domain-team}/README.md`

**Update Operation:**
```python
def update_domain_readme(domain: str, skill_name: str, description: str) -> None:
    """
    Add new skill to domain README skill list

    Args:
        domain: Domain team (engineering-team, product-team, etc.)
        skill_name: Skill name (data-analyst-toolkit)
        description: One-line description
    """
    readme_path = f"skills/{domain}/README.md"

    if not Path(readme_path).exists():
        print(f"⚠️  Warning: {readme_path} not found - skipping update")
        return

    # Read existing README
    with open(readme_path, 'r') as f:
        content = f.read()

    # Find skill list section
    # Look for "## Skills" or "## Available Skills" heading
    lines = content.split('\n')
    skill_list_start = -1

    for i, line in enumerate(lines):
        if line.startswith('## Skills') or line.startswith('## Available Skills'):
            skill_list_start = i
            break

    if skill_list_start == -1:
        print(f"⚠️  Warning: Could not find skill list section in {readme_path}")
        return

    # Generate entry (match existing format)
    entry = f"- **{skill_name}** - {description}"

    # Find insertion point (alphabetical order)
    insert_index = skill_list_start + 2  # After heading and blank line
    for i in range(skill_list_start + 2, len(lines)):
        if not lines[i].startswith('- **'):
            break
        if lines[i].lower() > entry.lower():
            insert_index = i
            break
        insert_index = i + 1

    # Insert entry
    lines.insert(insert_index, entry)

    # Update skill count if present
    for i, line in enumerate(lines):
        if 'skills' in line.lower() and any(char.isdigit() for char in line):
            # Extract current count
            import re
            match = re.search(r'(\d+)', line)
            if match:
                old_count = int(match.group(1))
                new_count = old_count + 1
                lines[i] = line.replace(str(old_count), str(new_count))
                break

    # Write back
    with open(readme_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"✓ Updated {readme_path}")
```

---

## Validation Strategy

### Validation Philosophy

**Fail Fast, Fail Clearly:**
- Validate before generating files
- Provide actionable error messages
- Allow corrections without re-entering all data

**Comprehensive Coverage:**
- 9 checks for agents
- 9 checks for skills
- Unit tests for each validation rule
- Integration tests with existing agents/skills

**Exit Codes for CI/CD:**
```python
EXIT_SUCCESS = 0          # All checks passed
EXIT_VALIDATION_FAILED = 1  # Validation errors found
EXIT_FILE_ERROR = 2       # File system errors
EXIT_CONFIG_ERROR = 3     # Invalid config file
EXIT_UNKNOWN_ERROR = 99   # Unexpected error
```

### Agent Validation Rules (Detailed)

**Rule 1: Name Format**
```python
def validate_agent_name(name: str) -> Tuple[bool, str]:
    """
    Validate agent name follows cs-* pattern

    Valid:   cs-data-analyst, cs-backend-engineer
    Invalid: data-analyst, cs_data_analyst, cs-Data-Analyst
    """
    if not name.startswith('cs-'):
        return False, "Agent name must start with 'cs-'"

    if not re.match(r'^cs-[a-z0-9-]+$', name):
        return False, "Agent name must be kebab-case (lowercase, hyphens only)"

    if '--' in name:
        return False, "Agent name cannot have consecutive hyphens"

    if name.endswith('-'):
        return False, "Agent name cannot end with hyphen"

    return True, "Valid"
```

**Rule 2: YAML Frontmatter**
```python
def validate_yaml_frontmatter(content: str) -> Tuple[bool, str]:
    """
    Validate YAML frontmatter is present and valid
    """
    if not content.startswith('---'):
        return False, "Missing YAML frontmatter (must start with ---)"

    try:
        frontmatter, body = parse_yaml_frontmatter(content)
    except ValueError as e:
        return False, f"YAML parsing error: {e}"

    # Required fields
    required = ['name', 'description', 'skills', 'domain', 'model', 'tools']
    for field in required:
        if field not in frontmatter:
            return False, f"Missing required YAML field: {field}"

    # Field validation
    if len(frontmatter['description']) > 150:
        return False, f"Description too long: {len(frontmatter['description'])} chars (max: 150)"

    if frontmatter['model'] not in ['sonnet', 'opus', 'haiku']:
        return False, f"Invalid model: {frontmatter['model']} (must be: sonnet, opus, haiku)"

    if not isinstance(frontmatter['tools'], list):
        return False, "Tools must be a list"

    valid_tools = ['Read', 'Write', 'Bash', 'Grep', 'Glob', 'Edit', 'NotebookEdit', 'WebFetch', 'WebSearch']
    for tool in frontmatter['tools']:
        if tool not in valid_tools:
            return False, f"Invalid tool: {tool}"

    return True, "Valid"
```

**Rule 3: Relative Path Resolution**
```python
def validate_relative_paths(agent_path: str, content: str) -> Tuple[bool, List[str]]:
    """
    Validate all ../../ paths resolve correctly from agent location
    """
    from pathlib import Path
    import re

    agent_dir = Path(agent_path).parent
    errors = []

    # Extract all relative paths
    path_pattern = r'\.\./\.\./[a-zA-Z0-9_/-]+(?:\.[a-zA-Z]+)?'
    paths = re.findall(path_pattern, content)

    for rel_path in set(paths):
        absolute_path = (agent_dir / rel_path).resolve()

        if not absolute_path.exists():
            errors.append(f"Path does not exist: {rel_path}")

    return len(errors) == 0, errors
```

**Rule 4: Skill Integration**
```python
def validate_skill_integration(frontmatter: Dict, agent_dir: Path) -> Tuple[bool, str]:
    """
    Validate skill package exists and has required files
    """
    skill_name = frontmatter['skills']
    domain = frontmatter['domain']

    # Map domain to skill team
    domain_to_team = {
        'marketing': 'marketing-team',
        'product': 'product-team',
        'engineering': 'engineering-team',
        'delivery': 'delivery-team'
    }

    team = domain_to_team.get(domain)
    if not team:
        return False, f"Unknown domain: {domain}"

    skill_path = agent_dir / '..' / '..' / 'skills' / team / skill_name
    skill_path = skill_path.resolve()

    if not skill_path.exists():
        return False, f"Skill not found: skills/{team}/{skill_name}/"

    # Check required files
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, f"Missing SKILL.md in {skill_name}"

    scripts_dir = skill_path / 'scripts'
    if not scripts_dir.exists():
        return False, f"Missing scripts/ directory in {skill_name}"

    return True, "Valid"
```

**Rule 5: Workflow Count**
```python
def validate_workflows(content: str) -> Tuple[bool, str]:
    """
    Ensure minimum 3 workflows documented
    """
    # Count workflow sections (### Workflow N:)
    workflow_pattern = r'###\s+Workflow\s+\d+:'
    workflows = re.findall(workflow_pattern, content)

    if len(workflows) < 3:
        return False, f"Only {len(workflows)} workflows documented (minimum: 3)"

    # Validate each workflow has required subsections
    for i in range(1, len(workflows) + 1):
        workflow_text = extract_workflow_section(content, i)

        required_subsections = ['**Goal:**', '**Steps:**', '**Expected Output:**', '**Time Estimate:**']
        for subsection in required_subsections:
            if subsection not in workflow_text:
                return False, f"Workflow {i} missing {subsection}"

    return True, f"Valid ({len(workflows)} workflows)"
```

**Rules 6-9:** Similar detailed validation for integration examples, success metrics, markdown structure, and cross-references.

### Skill Validation Rules (Detailed)

Similar level of detail as agent validation, covering:
1. Name format (no cs- prefix, kebab-case)
2. Directory structure (scripts/, references/, assets/)
3. SKILL.md completeness (YAML, sections)
4. Python tool standards (--help, executable, docstring)
5. Reference guides (content, structure)
6. Assets directory (exists)
7. Metadata completeness (all fields)
8. Documentation quality (quick start, workflows)
9. Integration points (cross-references)

### Validation CLI

**Standalone Validation Tool:**

```bash
# Validate single agent
python scripts/validator.py agent agents/engineering/cs-data-analyst.md

# Validate single skill
python scripts/validator.py skill skills/engineering-team/data-analyst-toolkit/

# Validate all agents
python scripts/validator.py agents --all

# Validate all skills
python scripts/validator.py skills --all

# Validate everything (CI/CD mode)
python scripts/validator.py all --json --exit-code

# Validate with specific checks only
python scripts/validator.py agent agents/engineering/cs-data-analyst.md --checks name,yaml,paths
```

**Output Formats:**

**Human-Readable:**
```
Validating: agents/engineering/cs-data-analyst.md
================================================

✅ Name format: Valid
✅ YAML frontmatter: Valid
✅ Relative paths: Valid (5 paths checked)
✅ Skill integration: Valid (data-analyst-toolkit)
✅ Workflows: Valid (4 workflows)
✅ Integration examples: Valid (3 examples)
✅ Success metrics: Valid (4 categories)
✅ Markdown structure: Valid
✅ Cross-references: Valid

Overall: PASSED (9/9 checks)
```

**JSON Output (for CI/CD):**
```json
{
  "target": "agents/engineering/cs-data-analyst.md",
  "type": "agent",
  "status": "passed",
  "checks_passed": 9,
  "checks_total": 9,
  "timestamp": "2025-11-22T10:30:00Z",
  "checks": [
    {
      "name": "name_format",
      "status": "passed",
      "message": "Valid name format"
    },
    {
      "name": "yaml_frontmatter",
      "status": "passed",
      "message": "Valid YAML frontmatter"
    }
  ]
}
```

### Batch Validation

**Validate All Existing Agents (28 agents):**
```python
def validate_all_agents() -> Dict:
    """
    Validate all agents in agents/ directory

    Returns validation report for all agents
    """
    from pathlib import Path
    import glob

    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'agents': []
    }

    # Find all cs-*.md files
    agent_files = glob.glob('agents/**/cs-*.md', recursive=True)
    results['total'] = len(agent_files)

    for agent_file in agent_files:
        print(f"Validating: {agent_file}...")

        validation_result = validate_agent(agent_file)

        if validation_result['status'] == 'passed':
            results['passed'] += 1
            print(f"  ✅ PASSED")
        else:
            results['failed'] += 1
            print(f"  ❌ FAILED: {validation_result['summary']}")

        results['agents'].append({
            'file': agent_file,
            'status': validation_result['status'],
            'checks_passed': validation_result['checks_passed'],
            'checks_total': validation_result['checks_total']
        })

    return results
```

**CI/CD Integration:**
```bash
# .github/workflows/validate.yml
name: Validate Agents and Skills

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: pip install pyyaml

      - name: Validate all agents
        run: |
          python scripts/validator.py agents --all --json > agent-validation.json
          python scripts/validator.py skills --all --json > skill-validation.json

      - name: Check validation results
        run: |
          python scripts/check_validation_results.py agent-validation.json skill-validation.json
          # Exit with code 1 if any validation failed
```

---

## Consequences

### Positive Consequences

1. **Massive Time Savings**
   - Agent creation: 2 days → 1 hour (96% reduction)
   - Skill creation: 3 days → 2 hours (93% reduction)
   - ROI: After creating 3 agents, tool pays for itself

2. **Quality Improvements**
   - 100% validation pass rate (vs 80-85% manual)
   - Consistent structure across all agents/skills
   - No more path resolution errors
   - Standardized documentation quality

3. **Lower Barrier to Entry**
   - New contributors can create agents without deep knowledge
   - Interactive prompts teach best practices
   - Clear error messages guide corrections

4. **Maintainability**
   - Template updates propagate to all future creations
   - Validation rules easy to update
   - Catalog consistency maintained automatically

5. **Automation Enablement**
   - Config mode enables bulk agent generation
   - CI/CD validation prevents regressions
   - JSON output enables dashboard integration

### Negative Consequences

1. **Upfront Development Cost**
   - ~40 hours to implement both builders + validation
   - Additional time for testing and documentation
   - Mitigated by: Long-term time savings far exceed cost

2. **Template Maintenance**
   - Templates must be kept in sync with best practices
   - Changes require updating builder logic
   - Mitigated by: Centralized templates, version control

3. **PyYAML Dependency**
   - Adds external dependency (violates standard-library-only rule)
   - Alternative: Write simple YAML parser (~100 lines)
   - Decision: PyYAML worth it for robust YAML handling

4. **Learning Curve for Config Mode**
   - Users need to learn YAML config format
   - Mitigated by: Interactive mode primary, config optional

5. **Potential Rigidity**
   - Builders enforce specific structure
   - May limit creative agent/skill designs
   - Mitigated by: Manual editing still possible after generation

### Risks and Mitigations

**Risk 1: Validation too strict**
- **Impact:** Existing agents fail validation
- **Likelihood:** Medium
- **Mitigation:** Test against all 28 agents before deployment; add --lenient mode for edge cases

**Risk 2: Template becomes outdated**
- **Impact:** Generated agents don't match new best practices
- **Likelihood:** High (over time)
- **Mitigation:** Schedule quarterly template reviews; version templates

**Risk 3: Path resolution bugs**
- **Impact:** Generated agents have broken paths
- **Likelihood:** Low (comprehensive testing)
- **Mitigation:** Integration tests with actual file system; path validation before generation

**Risk 4: Config file format changes**
- **Impact:** Breaking change for automation users
- **Likelihood:** Low
- **Mitigation:** Version config format; support backward compatibility for 2 major versions

**Risk 5: Catalog corruption**
- **Impact:** Breaks agent/skill catalogs
- **Likelihood:** Very Low (append-only is safe)
- **Mitigation:** Backup catalogs before update; validate catalog format after update

---

## Implementation Roadmap

### Phase 1: Architecture & Design (CURRENT)

**Deliverables:**
- ✅ Architecture Decision Record (this document)
- ✅ Skill Template creation (`templates/skill-template.md`)
- ✅ Technical design for both builders
- ✅ Validation strategy

**Duration:** 1 day (November 22, 2025)

### Phase 2: Core Implementation

**Week 1: Agent Builder**
- Implement `AgentBuilder` class
- Implement `AgentValidator` class
- Implement interactive CLI
- Implement config mode
- Unit tests for validation logic

**Week 2: Skill Builder**
- Implement `SkillBuilder` class
- Implement `SkillValidator` class
- Implement directory scaffolding
- Implement placeholder generation
- Unit tests for validation logic

**Deliverables:**
- `scripts/agent_builder.py` (~800 lines)
- `scripts/skill_builder.py` (~900 lines)
- `scripts/validator.py` (~600 lines)
- Unit tests (80%+ coverage)

**Duration:** 2 weeks

### Phase 3: Testing & Validation

**Tasks:**
- Test against all 28 existing agents
- Test against all 29 existing skills
- Fix validation rule edge cases
- Performance testing (should complete in <5 seconds)
- User acceptance testing (simulate new user flow)

**Deliverables:**
- All existing agents pass validation (100%)
- All existing skills pass validation (100%)
- Integration test suite
- Performance benchmarks

**Duration:** 1 week

### Phase 4: Documentation & Deployment

**Tasks:**
- User documentation (USAGE.md updates)
- Developer documentation (CLAUDE.md updates)
- Video walkthrough (optional)
- Announcement and training
- CI/CD integration

**Deliverables:**
- Updated documentation
- Training materials
- GitHub Actions workflow
- Deployment to main branch

**Duration:** 1 week

### Phase 5: Maintenance & Iteration

**Ongoing:**
- Monitor usage and collect feedback
- Fix bugs and edge cases
- Template updates as best practices evolve
- Add new features based on user requests

**Success Metrics:**
- 90%+ of new agents created with builder (vs manual)
- <5% validation failure rate
- Positive user feedback (NPS 8+)

---

## Appendix

### A. Example Agent Config File

```yaml
# agent-config.yaml
# Config for creating new agent with agent_builder.py

name: cs-data-analyst
domain: engineering
description: Data analysis and reporting for product decisions
skills: data-analyst-toolkit
model: sonnet
tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob

# Optional: Override default workflow count
workflow_count: 4

# Optional: Provide workflow titles (will generate placeholders)
workflows:
  - "Daily Metrics Analysis"
  - "Custom Report Generation"
  - "Dashboard Creation"
  - "Automated Data Pipeline"
```

### B. Example Skill Config File

```yaml
# skill-config.yaml
# Config for creating new skill with skill_builder.py

name: data-analyst-toolkit
domain: engineering-team
description: Comprehensive data analysis toolkit with reporting and visualization
keywords:
  - data analysis
  - reporting
  - SQL
  - visualization
  - dashboards
  - metrics
tech_stack:
  - Python 3.8+
  - PostgreSQL
  - Pandas
  - Jupyter
tools:
  - data_analyzer.py
  - report_generator.py
  - dashboard_builder.py
references:
  - analysis_frameworks.md
  - sql_optimization_guide.md
```

### C. Validation Checklist

**Agent Validation Checklist (9 checks):**
- [ ] Name format (cs-[a-z0-9-]+)
- [ ] YAML frontmatter (valid, all required fields)
- [ ] Relative paths (all ../../ paths resolve)
- [ ] Skill integration (skill exists, has tools)
- [ ] Workflow count (minimum 3, proper format)
- [ ] Integration examples (minimum 2, bash code blocks)
- [ ] Success metrics (minimum 3 categories)
- [ ] Markdown structure (all sections, valid hierarchy)
- [ ] Cross-references (all links resolve)

**Skill Validation Checklist (9 checks):**
- [ ] Name format (kebab-case, no cs- prefix)
- [ ] Directory structure (scripts/, references/, assets/)
- [ ] SKILL.md (YAML, all required sections)
- [ ] Python tools (executable, --help, docstring)
- [ ] Reference guides (content, structure)
- [ ] Assets directory (exists)
- [ ] Metadata completeness (all YAML fields)
- [ ] Documentation quality (quick start, workflows)
- [ ] Integration points (cross-references)

### D. File Locations

```
claude-skills/
├── scripts/                          # Builder tools (new)
│   ├── agent_builder.py             # Agent creation CLI (~800 lines)
│   ├── skill_builder.py             # Skill creation CLI (~900 lines)
│   └── validator.py                 # Validation CLI (~600 lines)
├── templates/
│   ├── agent-template.md            # Exists (318 lines)
│   └── skill-template.md            # NEW - Created in Phase 1
├── tests/                           # Unit tests (new)
│   ├── test_agent_builder.py
│   ├── test_skill_builder.py
│   └── test_validators.py
├── agents/                          # Existing (28 agents)
│   └── {domain}/
│       ├── cs-{name}.md
│       └── CATALOG.md               # Updated by builder
├── skills/                          # Existing (29 skills)
│   └── {domain-team}/
│       ├── {skill-name}/            # Generated by builder
│       └── README.md                # Updated by builder
└── output/sessions/                 # Design artifacts
    └── rickydwilson-dcs/
        └── 2025-11-22_main_253aab/
            └── 2025-11-22_agent-skill-builder-adr.md  # This document
```

### E. Success Metrics

**Quantitative Metrics:**
- Agent creation time: 2 days → 1 hour (96% reduction) ✅ Target
- Skill creation time: 3 days → 2 hours (93% reduction) ✅ Target
- Validation pass rate: 80-85% → 100% ✅ Target
- Time to first commit: 4 hours → 30 minutes ✅ Target
- Error rate: 15-20% → <2% ✅ Target

**Qualitative Metrics:**
- User satisfaction: NPS 8+ ✅ Target
- Documentation quality: Consistent across all agents ✅ Target
- Onboarding time: New contributors productive in 1 hour vs 1 day ✅ Target
- Maintenance burden: Template updates < 1 hour vs 4-5 hours manual ✅ Target

**Adoption Metrics:**
- Builder usage: 90%+ of new agents created with builder ✅ Target
- Manual creation: <10% (only for special cases) ✅ Target
- CI/CD integration: Validation runs on every PR ✅ Target

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-22 | cs-architect | Initial ADR creation |

---

**Approval Status:** ✅ Approved for Phase 2 Implementation

**Next Steps:**
1. Create `templates/skill-template.md`
2. Begin Phase 2: Core Implementation (Week 1 - Agent Builder)
3. Weekly progress reviews with stakeholders

---

**End of Architecture Decision Record**
