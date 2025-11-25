# Skill Builder - Usage Guide

**Tool:** `scripts/skill_builder.py`
**Purpose:** Create new skill packages with automated scaffolding
**Created:** November 22, 2025

---

## Quick Start

### Method 1: Interactive Mode (Recommended for First-Time Use)

```bash
python scripts/skill_builder.py
```

**Workflow:**
1. Enter skill name (kebab-case)
2. Select skill team domain (or create new)
3. Enter description (< 300 chars)
4. Add keywords (6-15 recommended)
5. Specify tech stack
6. List Python tools (1-4 recommended)
7. List reference guides (0-3 recommended)
8. Preview and confirm

**Time:** 5-10 minutes

### Method 2: Config File Mode (Recommended for Batch Creation)

**Step 1:** Create config file `my-skill.yaml`

```yaml
name: my-skill-name
domain: engineering-team
description: Brief description of what this skill provides
keywords:
  - keyword1
  - keyword2
  - keyword3
tech_stack:
  - Python 3.8+
  - PostgreSQL
  - Docker
tools:
  - tool1.py
  - tool2.py
references:
  - guide1.md
  - guide2.md
```

**Step 2:** Run builder

```bash
python scripts/skill_builder.py --config my-skill.yaml
```

**Time:** 2-3 minutes

---

## Validation

### Validate Existing Skill

```bash
python scripts/skill_builder.py --validate skills/team/skill-name/
```

**Output:**
```
Validating skill: skill-name
==================================================

✓ name_format: Valid
✓ directory_structure: Valid structure
✓ skill_md_completeness: Valid SKILL.md
✓ python_tools: Valid (3 tools)
✓ reference_guides: Valid (2 guides)
✓ assets_directory: Valid
✓ metadata_completeness: Valid metadata
✓ documentation_quality: Valid (3 workflows)
✓ integration_points: Valid (8 internal links)

Results: 9/9 checks passed

✅ Skill validation passed
```

### Validate All Skills

```bash
python scripts/validate_all_skills.py
```

---

## Generated Directory Structure

```
skills/{domain-team}/{skill-name}/
├── SKILL.md                    # Main documentation (populated from template)
├── scripts/                    # Python CLI tools
│   ├── tool1.py               # Placeholder with --help, executable
│   ├── tool2.py               # Placeholder with --help, executable
│   └── tool3.py               # Placeholder with --help, executable
├── references/                 # Knowledge base markdown files
│   ├── guide1.md              # Placeholder reference guide
│   └── guide2.md              # Placeholder reference guide
└── assets/                     # User-facing templates (empty initially)
    └── .gitkeep               # Ensures directory is tracked
```

---

## Post-Creation Checklist

After running skill_builder.py, complete these steps:

### 1. Review SKILL.md (30-60 minutes)

- [ ] Update Overview section with detailed description
- [ ] Fill in Core Capabilities (4-6 bullet points)
- [ ] Document Quick Start with actual commands
- [ ] Write Key Workflows (minimum 2, recommended 4)
- [ ] Add Python Tools documentation with examples
- [ ] Document Reference guides with use cases
- [ ] Add Templates section if applicable
- [ ] Update Best Practices section
- [ ] Define Performance Metrics
- [ ] Review Integration section

### 2. Implement Python Tools (1-3 hours per tool)

**For each tool in `scripts/`:**

1. Open tool file: `vim scripts/tool_name.py`
2. Replace TODO comments with actual implementation
3. Update docstrings with real descriptions
4. Add validation logic in `validate_input()`
5. Implement core functionality in `process()`
6. Format output in `generate_output()`
7. Test with various inputs
8. Update help text with real examples

**Example:**
```bash
# Test tool
python scripts/tool_name.py test-input.txt --verbose

# Test help
python scripts/tool_name.py --help

# Test JSON output
python scripts/tool_name.py test-input.txt --output results.json
```

### 3. Write Reference Guides (1-2 hours per guide)

**For each guide in `references/`:**

1. Open guide file: `vim references/guide_name.md`
2. Replace TODO sections with actual content
3. Add Key Concepts with clear explanations
4. Document Best Practices with examples
5. Include Frameworks/Methodologies
6. Add real-world Examples
7. Link to external Resources

### 4. Add User Templates to assets/ (Optional, 30 minutes)

**Examples:**
- Checklists
- Configuration templates
- Report templates
- Planning worksheets

```bash
# Create template
touch assets/template_name.md
vim assets/template_name.md
```

### 5. Validate Complete Skill (5 minutes)

```bash
python scripts/skill_builder.py --validate skills/{team}/{skill-name}/
```

**Target:** 9/9 checks passed

### 6. Test Integration (10 minutes)

```bash
# Test all tools
for tool in skills/{team}/{skill-name}/scripts/*.py; do
    python "$tool" --help
done

# Test actual usage
python skills/{team}/{skill-name}/scripts/tool1.py sample-input.txt
```

### 7. Commit to Git (5 minutes)

```bash
git add skills/{team}/{skill-name}/
git commit -m "feat(skills): implement {skill-name} for {team}"
git push origin feature/skill-{skill-name}
```

---

## Validation Checks Explained

### 1. Name Format
- Kebab-case (lowercase-with-hyphens)
- No `cs-` prefix (reserved for agents)
- 3-50 characters
- No consecutive hyphens

**Valid:** `data-analyst-toolkit`, `senior-architect`
**Invalid:** `DataAnalyst`, `cs-data-analyst`, `data--analyst`

### 2. Directory Structure
- `scripts/` directory exists
- `references/` directory exists
- `assets/` directory exists

### 3. SKILL.md Completeness
- YAML frontmatter present
- Required sections exist:
  - ## Overview
  - ## Core Capabilities
  - ## Quick Start
  - ## Key Workflows
  - ## Python Tools

### 4. Python Tools
- All tools in `scripts/` are executable (`chmod +x`)
- All tools use argparse (support `--help` flag)
- All tools have docstrings

### 5. Reference Guides
- All `.md` files in `references/` exist
- Files have content (minimum 100 chars)
- Proper markdown formatting

### 6. Assets Directory
- Directory exists (may be empty)

### 7. Metadata Completeness
- YAML frontmatter has all required fields:
  - name
  - description
  - metadata.version
  - metadata.updated
  - metadata.keywords

### 8. Documentation Quality
- Quick Start section has code examples
- At least 1 workflow documented

### 9. Integration Points
- Cross-references are valid
- No broken links to internal files
- `references/`, `scripts/`, `assets/` paths resolve

---

## Common Issues

### Issue 1: Validation Fails - "Not Executable"

**Error:**
```
✗ python_tools: tool1.py: not executable; tool2.py: not executable
```

**Solution:**
```bash
chmod +x skills/{team}/{skill-name}/scripts/*.py
```

### Issue 2: Validation Fails - "Missing YAML fields"

**Error:**
```
✗ metadata_completeness: Missing YAML fields: metadata
```

**Solution:**

Check SKILL.md YAML frontmatter has nested metadata:
```yaml
---
name: skill-name
description: Description here
metadata:
  version: 1.0.0
  updated: 2025-11-22
  keywords:
    - keyword1
---
```

### Issue 3: Validation Fails - "No workflows documented"

**Error:**
```
✗ documentation_quality: No workflows documented
```

**Solution:**

Add at least one workflow in SKILL.md:
```markdown
## Key Workflows

### 1. Primary Workflow Name

**Time:** 2-3 hours

1. **Step 1** - Description
2. **Step 2** - Description
3. **Step 3** - Description
```

### Issue 4: Validation Fails - "Broken link"

**Error:**
```
✗ integration_points: Broken link: references/missing_guide.md
```

**Solution:**

Either:
1. Create the missing file: `touch references/missing_guide.md`
2. Remove the broken link from SKILL.md

---

## Examples

### Example 1: Data Quality Toolkit

**Config:**
```yaml
name: data-quality-toolkit
domain: engineering-team
description: Comprehensive data quality validation and profiling tools
keywords:
  - data quality
  - validation
  - profiling
  - data governance
tech_stack:
  - Python 3.8+
  - SQL
  - Pandas
tools:
  - data_validator.py
  - data_profiler.py
  - quality_reporter.py
references:
  - quality_metrics.md
  - validation_rules.md
```

**Result:** Complete skill package in `skills/engineering-team/data-quality-toolkit/`

### Example 2: Marketing Analytics

**Config:**
```yaml
name: marketing-analytics
domain: marketing-team
description: Marketing analytics and reporting toolkit with campaign analysis
keywords:
  - marketing analytics
  - campaign analysis
  - reporting
  - metrics
tech_stack:
  - Python 3.8+
  - Google Analytics API
  - Tableau
tools:
  - campaign_analyzer.py
  - report_generator.py
references:
  - marketing_metrics.md
  - campaign_frameworks.md
```

**Result:** Complete skill package in `skills/marketing-team/marketing-analytics/`

---

## Tips for Success

### 1. Start with Existing Skills as Examples

Browse successful skills:
```bash
# Marketing examples
cat skills/marketing-team/content-creator/SKILL.md

# Engineering examples
cat skills/engineering-team/senior-architect/SKILL.md

# Product examples
cat skills/product-team/product-manager-toolkit/SKILL.md
```

### 2. Use Descriptive Names

**Good:**
- `data-quality-toolkit`
- `senior-architect`
- `content-creator`

**Avoid:**
- `data-tool` (too generic)
- `qa` (too short)
- `data_quality_validation_profiling_toolkit` (too long)

### 3. Write for Your Audience

**Consider:**
- Who will use this skill?
- What problems does it solve?
- What level of expertise do they have?

**Tailor documentation accordingly**

### 4. Test Before Committing

**Checklist:**
- [ ] All Python tools run without errors
- [ ] `--help` flag works on all tools
- [ ] SKILL.md has no placeholder text
- [ ] Reference guides have actual content
- [ ] Validation passes (9/9 checks)
- [ ] Examples work as documented

---

## Integration with Agent Builder

**Skill → Agent Flow:**

1. **Create Skill** (this tool)
   ```bash
   python scripts/skill_builder.py --config skill.yaml
   ```

2. **Create Agent** (agent_builder.py)
   ```bash
   python scripts/agent_builder.py --config agent.yaml
   ```

3. **Link in Agent Config**
   ```yaml
   skills: skill-name  # References skill folder
   domain: engineering  # Maps to engineering-team
   ```

4. **Agent References Skill**
   ```markdown
   ## Skill Integration
   **Skill Location:** `../../skills/engineering-team/skill-name/`
   ```

---

## Additional Resources

- **Skill Template:** `templates/skill-template.md`
- **Agent Builder:** `scripts/agent_builder.py`
- **Main Documentation:** `CLAUDE.md`
- **Team Guides:** `skills/{team}/CLAUDE.md`

---

**Last Updated:** November 22, 2025
**Tool Version:** 1.0.0
**Status:** Production Ready
