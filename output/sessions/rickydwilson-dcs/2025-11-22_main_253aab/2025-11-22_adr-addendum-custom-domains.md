# ADR Addendum: Custom Domain Support

**Date:** November 22, 2025
**Status:** Approved
**Author:** Claude Code
**Parent ADR:** 2025-11-22_agent-skill-builder-adr.md
**Version:** 1.1

---

## Change Request

**Requirement:** Users should be able to create new agent domains beyond the predefined set (marketing, product, engineering, delivery).

**Rationale:**
- Current ADR hardcodes 4 domains, limiting extensibility
- Teams may need custom domains (e.g., "sales", "finance", "operations", "c-level")
- Repository already has `agents/c-level/` directory not in the predefined list
- Flexibility enables repository growth without code changes

---

## Decision: Support Custom Domain Creation

### Updated Domain Strategy

**Previous Approach:**
```python
# Hardcoded domain validation
VALID_DOMAINS = ['marketing', 'product', 'engineering', 'delivery']

def validate_domain(domain: str) -> bool:
    return domain in VALID_DOMAINS
```

**New Approach:**
```python
# Dynamic domain discovery + custom domain support
def get_existing_domains() -> List[str]:
    """Discover existing agent domains from file system"""
    agents_dir = Path("agents")
    return [d.name for d in agents_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

def validate_domain_format(domain: str) -> Tuple[bool, str]:
    """Validate domain name format (kebab-case, lowercase)"""
    pattern = r'^[a-z][a-z0-9-]*$'
    if not re.match(pattern, domain):
        return False, f"Domain must be lowercase kebab-case: {domain}"
    if len(domain) < 3:
        return False, f"Domain too short (min 3 chars): {domain}"
    if len(domain) > 30:
        return False, f"Domain too long (max 30 chars): {domain}"
    return True, "Valid domain format"

def handle_domain_selection(interactive: bool = True) -> str:
    """
    Interactive domain selection with custom domain option

    Returns:
        Selected domain name (existing or new)
    """
    existing_domains = get_existing_domains()

    print("Select domain:")
    for idx, domain in enumerate(existing_domains, 1):
        print(f"{idx}. {domain}")
    print(f"{len(existing_domains) + 1}. Create new domain")

    choice = input(f"\nDomain (1-{len(existing_domains) + 1}): ").strip()

    # Existing domain selected
    if choice.isdigit() and 1 <= int(choice) <= len(existing_domains):
        return existing_domains[int(choice) - 1]

    # New domain requested
    if choice.isdigit() and int(choice) == len(existing_domains) + 1:
        return create_new_domain()

    # Invalid selection
    print("❌ Invalid selection")
    return handle_domain_selection(interactive)

def create_new_domain() -> str:
    """
    Interactive workflow for creating a new domain

    Returns:
        New domain name
    """
    print("\n🆕 Create New Domain")
    print("-" * 40)
    print("Domain names should be:")
    print("  • Lowercase kebab-case (e.g., 'sales-ops', 'finance')")
    print("  • Descriptive and concise (3-30 chars)")
    print("  • Represent a functional area")
    print("\nExamples: sales, finance, operations, c-level, customer-success\n")

    domain = input("New domain name: ").strip().lower()

    # Validate format
    valid, message = validate_domain_format(domain)
    if not valid:
        print(f"❌ {message}")
        return create_new_domain()

    # Check for conflicts
    existing = get_existing_domains()
    if domain in existing:
        print(f"❌ Domain '{domain}' already exists")
        return create_new_domain()

    # Confirm creation
    print(f"\n✓ Domain format valid: {domain}")
    print(f"\nThis will create:")
    print(f"  • agents/{domain}/ directory")
    print(f"  • agents/{domain}/CATALOG.md file")

    confirm = input("\nCreate this domain? (y/n): ").strip().lower()

    if confirm == 'y':
        create_domain_directory(domain)
        return domain
    else:
        print("❌ Domain creation cancelled")
        return handle_domain_selection()

def create_domain_directory(domain: str) -> None:
    """
    Create new domain directory structure

    Args:
        domain: Domain name (validated)

    Creates:
        agents/{domain}/
        agents/{domain}/CATALOG.md
    """
    domain_path = Path(f"agents/{domain}")
    domain_path.mkdir(parents=True, exist_ok=True)

    # Create CATALOG.md
    catalog_content = f"""# {domain.replace('-', ' ').title()} Agents

This directory contains agents for the {domain} domain.

## Agents

<!-- Agents will be listed here automatically by agent_builder.py -->

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Domain:** {domain}
**Agent Count:** 0
"""

    catalog_path = domain_path / "CATALOG.md"
    catalog_path.write_text(catalog_content)

    print(f"✅ Created: {domain_path}/")
    print(f"✅ Created: {catalog_path}")
```

---

## Updated Interactive Workflow

### Step 2: Domain Selection (Updated)

**Before:**
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

**After:**
```
Step 2/7: Domain
----------------
Select domain:
1. marketing      (3 agents)
2. product        (6 agents)
3. engineering    (15 agents)
4. delivery       (4 agents)
5. c-level        (2 agents)
6. Create new domain

Domain (1-6): 6

🆕 Create New Domain
--------------------------------------------
Domain names should be:
  • Lowercase kebab-case (e.g., 'sales-ops', 'finance')
  • Descriptive and concise (3-30 chars)
  • Represent a functional area

Examples: sales, finance, operations, customer-success

New domain name: sales

✓ Domain format valid: sales

This will create:
  • agents/sales/ directory
  • agents/sales/CATALOG.md file

Create this domain? (y/n): y

✅ Created: agents/sales/
✅ Created: agents/sales/CATALOG.md
✓ Domain: sales
```

---

## Domain-to-Skill Team Mapping

### Challenge

Agents live in `agents/{domain}/` but skills live in `skills/{domain-team}/`. The mapping isn't 1:1:

| Agent Domain | Skill Team | Path Pattern |
|--------------|------------|--------------|
| marketing | marketing-team | skills/marketing-team/ |
| product | product-team | skills/product-team/ |
| engineering | engineering-team | skills/engineering-team/ |
| delivery | delivery-team | skills/delivery-team/ |
| c-level | c-level-advisor | skills/c-level-advisor/ |
| **sales** (new) | **???** | **???** |

### Solution: Automatic Mapping with Override

```python
def map_domain_to_skill_team(domain: str) -> str:
    """
    Map agent domain to skill team directory

    Default pattern: {domain}-team
    Special cases: Handle exceptions

    Args:
        domain: Agent domain name

    Returns:
        Skill team directory name
    """
    # Known exceptions
    DOMAIN_EXCEPTIONS = {
        'c-level': 'c-level-advisor',
        # Add more as needed
    }

    if domain in DOMAIN_EXCEPTIONS:
        return DOMAIN_EXCEPTIONS[domain]

    # Default pattern: append '-team'
    return f"{domain}-team"

def get_skill_teams_for_domain(domain: str) -> List[str]:
    """
    Find all skill teams that could map to this domain

    Returns list of skill team directories that exist
    """
    skill_team = map_domain_to_skill_team(domain)
    skills_dir = Path("skills")

    # Check if default mapping exists
    if (skills_dir / skill_team).exists():
        return [skill_team]

    # Search for similar names
    all_teams = [d.name for d in skills_dir.iterdir() if d.is_dir()]
    similar = [t for t in all_teams if domain in t or t in domain]

    return similar if similar else all_teams

def prompt_skill_team_for_new_domain(domain: str) -> str:
    """
    When creating agent in new domain, ask which skill team to use
    """
    potential_teams = get_skill_teams_for_domain(domain)

    print(f"\nSkill team for '{domain}' domain:")
    print("Select skill team or create new:")

    for idx, team in enumerate(potential_teams, 1):
        print(f"{idx}. skills/{team}/")
    print(f"{len(potential_teams) + 1}. Create new skill team")

    choice = input(f"\nSkill team (1-{len(potential_teams) + 1}): ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(potential_teams):
        return potential_teams[int(choice) - 1]

    if choice.isdigit() and int(choice) == len(potential_teams) + 1:
        return create_new_skill_team(domain)

    print("❌ Invalid selection")
    return prompt_skill_team_for_new_domain(domain)

def create_new_skill_team(domain: str) -> str:
    """
    Create new skill team directory for domain
    """
    suggested_name = f"{domain}-team"

    print(f"\n🆕 Create New Skill Team")
    print(f"Suggested name: {suggested_name}")

    team_name = input(f"Skill team name [{suggested_name}]: ").strip() or suggested_name

    # Validate format
    valid, message = validate_domain_format(team_name)
    if not valid:
        print(f"❌ {message}")
        return create_new_skill_team(domain)

    # Create directory
    team_path = Path(f"skills/{team_name}")
    team_path.mkdir(parents=True, exist_ok=True)

    # Create README.md
    readme_content = f"""# {team_name.replace('-', ' ').title()}

Skills for the {domain} domain.

## Skills

<!-- Skills will be listed here -->

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Skill Count:** 0
"""

    (team_path / "README.md").write_text(readme_content)
    (team_path / "CLAUDE.md").write_text(f"# {team_name} - Domain Guide\n\n[Documentation to be added]")

    print(f"✅ Created: {team_path}/")

    return team_name
```

---

## Updated Validation Rules

### Agent Validation (Updated)

**Rule 2: YAML Frontmatter Validation**

**Before:**
```python
VALID_DOMAINS = ['marketing', 'product', 'engineering', 'delivery']

def validate_domain(domain: str) -> Tuple[bool, str]:
    if domain not in VALID_DOMAINS:
        return False, f"Domain must be one of: {', '.join(VALID_DOMAINS)}"
    return True, "Valid domain"
```

**After:**
```python
def validate_domain(domain: str, agent_path: Path) -> Tuple[bool, str]:
    """
    Validate domain exists as directory in agents/

    Args:
        domain: Domain from YAML frontmatter
        agent_path: Path to agent file being validated

    Returns:
        (valid, message) tuple
    """
    # Extract domain from agent path
    expected_domain = agent_path.parent.name

    # Check frontmatter matches location
    if domain != expected_domain:
        return False, f"Domain mismatch: YAML says '{domain}' but file is in 'agents/{expected_domain}/'"

    # Check domain directory exists
    domain_dir = Path(f"agents/{domain}")
    if not domain_dir.exists():
        return False, f"Domain directory does not exist: agents/{domain}/"

    # Validate domain format
    valid, message = validate_domain_format(domain)
    if not valid:
        return False, f"Invalid domain format: {message}"

    return True, f"Valid domain: {domain}"
```

---

## Updated Skill Builder

### Skill Domain Selection (Updated)

**Step 2: Domain Selection**

```python
def prompt_skill_domain() -> str:
    """
    Prompt for skill team domain

    Returns:
        Skill team directory name (e.g., 'marketing-team')
    """
    # Discover existing skill teams
    skills_dir = Path("skills")
    existing_teams = [d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

    print("Step 2/8: Skill Team Domain")
    print("-" * 40)
    print("Select skill team:")

    for idx, team in enumerate(existing_teams, 1):
        skill_count = len(list((skills_dir / team).glob("*/")))
        print(f"{idx}. {team} ({skill_count} skills)")

    print(f"{len(existing_teams) + 1}. Create new skill team")

    choice = input(f"\nSkill team (1-{len(existing_teams) + 1}): ").strip()

    # Existing team selected
    if choice.isdigit() and 1 <= int(choice) <= len(existing_teams):
        return existing_teams[int(choice) - 1]

    # New team requested
    if choice.isdigit() and int(choice) == len(existing_teams) + 1:
        return create_new_skill_team_interactive()

    print("❌ Invalid selection")
    return prompt_skill_domain()

def create_new_skill_team_interactive() -> str:
    """
    Interactive workflow for creating new skill team
    """
    print("\n🆕 Create New Skill Team")
    print("-" * 40)
    print("Skill team names should be:")
    print("  • Lowercase kebab-case with '-team' suffix")
    print("  • Match agent domain (e.g., 'sales-team' for 'sales' domain)")
    print("\nExamples: sales-team, finance-team, operations-team\n")

    team_name = input("New skill team name: ").strip().lower()

    # Validate format
    if not team_name.endswith('-team'):
        print("⚠️  Skill teams typically end with '-team' suffix")
        add_suffix = input("Add '-team' suffix? (y/n): ").strip().lower()
        if add_suffix == 'y':
            team_name = f"{team_name}-team"

    valid, message = validate_domain_format(team_name.replace('-team', ''))
    if not valid:
        print(f"❌ {message}")
        return create_new_skill_team_interactive()

    # Check conflicts
    if Path(f"skills/{team_name}").exists():
        print(f"❌ Skill team '{team_name}' already exists")
        return create_new_skill_team_interactive()

    # Create structure
    create_skill_team_structure(team_name)

    return team_name

def create_skill_team_structure(team_name: str) -> None:
    """
    Create new skill team directory with README and CLAUDE.md
    """
    team_path = Path(f"skills/{team_name}")
    team_path.mkdir(parents=True, exist_ok=True)

    # README.md
    readme = f"""# {team_name.replace('-', ' ').title()}

Skills for the {team_name.replace('-team', '')} domain.

## Overview

This skill team provides tools, frameworks, and workflows for {team_name.replace('-team', '')} functions.

## Skills

<!-- Skills will be listed here automatically -->

## Quick Start

[Documentation to be added]

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Skill Count:** 0
"""
    (team_path / "README.md").write_text(readme)

    # CLAUDE.md
    claude_md = f"""# {team_name.replace('-', ' ').title()} - Domain Guide

## Purpose

This directory contains skills for the {team_name.replace('-team', '')} domain.

## Available Skills

[Skills will be documented here]

## Development Guidelines

[Guidelines to be added]

---

**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""
    (team_path / "CLAUDE.md").write_text(claude_md)

    print(f"✅ Created: {team_path}/")
    print(f"✅ Created: {team_path}/README.md")
    print(f"✅ Created: {team_path}/CLAUDE.md")
```

---

## Migration Plan

### Existing Code Impact

**No Breaking Changes:**
- All existing agents still validate (domains exist as directories)
- All existing skills still validate (team directories exist)
- Backward compatible with current structure

**New Capabilities:**
- Can create agents in new domains dynamically
- Can create skills in new team directories dynamically
- No hardcoded domain lists

### Testing Strategy

**Test Cases:**

1. **Create agent in existing domain**
   - Should work as before (no regression)

2. **Create agent in new domain**
   - Prompts for domain creation
   - Creates directory structure
   - Validates correctly

3. **Validate existing agents**
   - All 28 agents pass validation
   - No domain errors

4. **Create skill in existing team**
   - Should work as before

5. **Create skill in new team**
   - Prompts for team creation
   - Creates directory structure
   - Validates correctly

6. **Domain-to-team mapping**
   - Existing mappings work (marketing → marketing-team)
   - New domains prompt for team selection
   - Can create new teams for new domains

---

## Updated ADR Sections

### Decision 1: Interactive CLI (Updated)

**New Interactive Mode Features:**
- Domain selection shows existing + "Create new" option
- Creating new domain creates directory + CATALOG.md
- Skill team selection shows existing + "Create new" option
- Creating new team creates directory + README.md + CLAUDE.md

### Validation Rules (Updated)

**Agent Validation:**
- ✅ Domain directory exists (not hardcoded list)
- ✅ Domain format valid (kebab-case, 3-30 chars)
- ✅ Domain matches file location

**Skill Validation:**
- ✅ Team directory exists
- ✅ Team format valid (kebab-case, typically ends with '-team')
- ✅ Team has README.md and CLAUDE.md

---

## Implementation Checklist

**agent_builder.py Updates:**
- [ ] Replace hardcoded VALID_DOMAINS with `get_existing_domains()`
- [ ] Add `create_new_domain()` function
- [ ] Add `create_domain_directory()` function
- [ ] Update domain selection prompt with "Create new" option
- [ ] Update domain validation to check directory exists
- [ ] Add domain format validation function

**skill_builder.py Updates:**
- [ ] Replace hardcoded team list with dynamic discovery
- [ ] Add `create_new_skill_team_interactive()` function
- [ ] Add `create_skill_team_structure()` function
- [ ] Update skill team selection prompt with "Create new" option
- [ ] Add skill team format validation

**validator.py Updates:**
- [ ] Update domain validation (check directory exists vs hardcoded list)
- [ ] Add domain format validation
- [ ] Update skill team validation
- [ ] Test against all existing agents/skills (100% pass rate)

**Documentation Updates:**
- [ ] Update CLAUDE.md with custom domain instructions
- [ ] Update agents/CLAUDE.md with domain creation workflow
- [ ] Add examples of creating custom domains
- [ ] Document domain-to-team mapping conventions

---

## Benefits

**Flexibility:**
- ✅ No code changes needed to add new domains
- ✅ Teams can organize agents by their needs
- ✅ Supports organic growth of repository

**Usability:**
- ✅ Clear prompts for domain/team creation
- ✅ Validates format before creating
- ✅ Creates necessary scaffolding automatically

**Maintainability:**
- ✅ No hardcoded lists to update
- ✅ Self-documenting structure (README.md, CLAUDE.md)
- ✅ Consistent patterns across all domains

**Backward Compatibility:**
- ✅ All existing agents work unchanged
- ✅ All existing skills work unchanged
- ✅ No migration required

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Domain name conflicts** | Medium | Validate against existing domains before creation |
| **Inconsistent naming** | Low | Provide clear examples and validation rules |
| **Orphan directories** | Low | Document cleanup process, require README.md/CLAUDE.md |
| **Documentation gap** | Medium | Auto-generate skeleton documentation with TODOs |
| **Team confusion** | Low | Update docs with clear examples, show agent counts per domain |

---

## Acceptance Criteria

**Must Have:**
- [ ] Can create agent in existing domain (regression test)
- [ ] Can create agent in new domain with directory creation
- [ ] Can create skill in existing team (regression test)
- [ ] Can create skill in new team with directory creation
- [ ] All 28 existing agents validate successfully
- [ ] All 29 existing skills validate successfully
- [ ] Domain format validation works
- [ ] Skill team format validation works

**Should Have:**
- [ ] Shows agent count per domain in selection
- [ ] Shows skill count per team in selection
- [ ] Auto-suggests team names based on domain
- [ ] Creates CATALOG.md for new domains
- [ ] Creates README.md + CLAUDE.md for new teams

**Nice to Have:**
- [ ] Warns if domain has no skills yet
- [ ] Suggests creating matching skill team for new domain
- [ ] Validates domain-to-team naming conventions

---

## Conclusion

This addendum updates the Agent/Skill Builder System to support dynamic domain creation while maintaining 100% backward compatibility. Users can now create custom domains (e.g., sales, finance, operations) without code changes, enabling organic repository growth.

**Key Changes:**
1. Replace hardcoded domain lists with dynamic discovery
2. Add "Create new domain" option to agent builder
3. Add "Create new skill team" option to skill builder
4. Validate domain/team format instead of enum membership
5. Auto-create directory structure with scaffolding

**Impact:**
- ✅ No breaking changes
- ✅ All existing agents/skills validate
- ✅ New flexibility for custom domains
- ✅ Clear user prompts and validation

**Implementation:** Phase 2 and Phase 3 will incorporate these changes.

---

**Version:** 1.1
**Date:** November 22, 2025
**Status:** Approved
**Next Review:** After Phase 2 implementation
