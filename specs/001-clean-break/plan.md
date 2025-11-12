# Implementation Plan: Clean Break - Pandora-Focused Restructure

**Branch**: `001-clean-break` | **Date**: 2025-11-12 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-clean-break/spec.md`

## Summary

Restructure the claude-skills repository for Pandora-specific focus by reorganizing folder structure, curating domain-relevant skills, and establishing proper attribution. This involves moving all skills to a `skills/` directory, renaming key folders (documentation → docs, marketing-skill → marketing-team, project-management → delivery-team), removing non-Pandora domains (ra-qm-team, c-level-advisor except cto-advisor), and updating all path references throughout the codebase.

## Technical Context

**Language/Version**: Bash/Shell scripting for git operations, Python 3.8+ (existing tools), Markdown (documentation)
**Primary Dependencies**: git (for history-preserving moves), find/grep/sed (for path updates), markdown-link-check (for link validation)
**Storage**: Git repository with history preservation via `git mv` commands
**Testing**: Manual verification of folder structure, automated link checking, Python script execution tests
**Target Platform**: macOS/Linux development environment, GitHub repository hosting
**Project Type**: Repository restructuring (not traditional software development)
**Performance Goals**: Complete restructure without losing git history, all existing tools remain functional
**Constraints**: Must preserve git commit history for all moved files, zero broken links after restructuring
**Scale/Scope**: ~40 skills across 6 domains → ~26 skills across 4 domains, ~100+ files to move/update

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Skills as Products
✅ **PASS** - Restructuring maintains skill package self-containment. All SKILL.md, scripts/, references/, assets/ structures preserved during moves.

### Principle II: Documentation-Driven Development
✅ **PASS** - Documentation folder renamed to docs/ for clarity. All SKILL.md files remain under 450 lines (already compliant from Phase 4 refactoring).

### Principle III: Algorithm Over AI
✅ **PASS** - No new Python tools created. Existing tools unchanged except for path reference updates if needed.

### Principle IV: Template-Heavy Design
✅ **PASS** - Templates remain in assets/ directories within skill packages. No template changes required.

### Principle V: Platform-Specific Expertise
✅ **PASS** - No content changes to skills. Platform-specific guidance remains intact.

### Principle VI: Test-Validated Quality
⚠️ **ATTENTION REQUIRED** - After restructuring, must validate all Python tools still execute correctly with new paths. Run `./test_cli_standards.sh` to verify.

### Principle VII: Agent-Skill Separation
⚠️ **ATTENTION REQUIRED** - Agent relative paths must be updated from `../../domain-name/skill-name/` to `../../skills/domain-name/skill-name/`. Critical for agent functionality.

**Gate Status**: ✅ PASS with attention items
**Action Required**: Validate tool execution and update agent paths after folder moves.

## Project Structure

### Documentation (this feature)

```text
specs/001-clean-break/
├── plan.md              # This file
├── spec.md              # Feature specification (complete)
├── research.md          # Phase 0 research (to be created)
├── migration-notes.md   # Removal rationale and change log (Phase 1)
└── checklists/
    └── requirements.md  # Spec validation (complete)
```

### Source Code (repository root)

This is a restructuring task, so the "source code" is the repository structure itself:

**BEFORE (Current State)**:
```text
claude-skills/
├── engineering-team/       # 14 engineering skills
├── marketing-skill/        # 3 marketing skills
├── product-team/           # 5 product skills
├── c-level-advisor/        # 2 c-level skills (ceo, cto)
├── project-management/     # 6 PM skills
├── ra-qm-team/             # 12 RA/QM skills
├── documentation/          # All docs
├── agents/                 # Agent orchestrators
├── templates/              # Templates
└── [other root files]
```

**AFTER (Target State)**:
```text
claude-skills/
├── skills/                 # NEW: All skill packages
│   ├── engineering-team/   # 14 engineering + cto-advisor (15 total)
│   ├── marketing-team/     # 3 marketing (RENAMED from marketing-skill)
│   ├── product-team/       # 5 product
│   └── delivery-team/      # 6 PM (RENAMED from project-management)
├── docs/                   # RENAMED from documentation/
├── agents/                 # Updated with new paths
├── templates/              # Unchanged
└── [other root files]      # Updated references

DELETED:
├── ra-qm-team/             # 12 skills removed
└── c-level-advisor/        # ceo-advisor removed, cto-advisor moved
```

**Structure Decision**: This is a repository reorganization task. The structure shown above represents the folder hierarchy changes. No new code will be written; existing Python tools, documentation, and agents will be moved/updated to reflect new locations.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - All constitution principles pass or have clear attention items that don't require justification (standard validation tasks).

## Phase 0: Research & Decision Documentation

### Research Tasks

1. **Git History Preservation Strategy**
   - **Question**: What git commands preserve history when moving folders?
   - **Research**: Document `git mv` vs `mv + git add` behavior, verify history preservation with test case
   - **Output**: Concrete command sequence for history-preserving moves

2. **Path Reference Update Strategy**
   - **Question**: Where do path references exist in the codebase?
   - **Research**: Comprehensive search for hardcoded paths, relative path patterns, import statements
   - **Output**: Complete list of files requiring path updates with specific patterns to find/replace

3. **Link Validation Approach**
   - **Question**: How to systematically validate all markdown links after restructuring?
   - **Research**: Evaluate markdown-link-check or similar tools, test on sample files
   - **Output**: Automated link checking command/script

4. **Agent Path Update Patterns**
   - **Question**: What specific path patterns do agents use, and how should they change?
   - **Research**: Audit all agent files for skill references, document current patterns
   - **Output**: Find/replace mapping for agent path updates

5. **Attribution Best Practices**
   - **Question**: What's the standard approach for crediting original authors in forked projects?
   - **Research**: Review GitHub fork attribution patterns, MIT license requirements
   - **Output**: CONTRIBUTORS.md format and README.md attribution section template

6. **Documentation Cleanup Audit**
   - **Question**: Which documentation files contain upstream author references or repo links that should be removed?
   - **Research**: Grep all docs for "Ali Rezvani", "alirezarezvani", upstream repo URLs, contribution guidelines
   - **Output**: List of files requiring upstream reference removal (excluding CONTRIBUTORS.md and README.md)

### Decisions Log

| Decision | Rationale | Alternatives Considered |
|----------|-----------|-------------------------|
| Use `git mv` for all folder moves | Preserves git history automatically | `mv` + `git add` (requires manual history tracking) |
| Create `skills/` parent directory | Cleaner root, scalable for future growth | Leave in root (rejected: cluttered), use `src/` (rejected: not source code) |
| Rename folders during move | Clear Pandora identity from day 1 | Rename in separate step (rejected: doubles path update work) |
| Delete ra-qm-team and c-level | Not relevant to Pandora needs | Archive to branch (may do later if needed) |
| Move cto-advisor to engineering | Better organizational fit | Keep separate (rejected: only 1 C-level skill left), delete (rejected: still useful) |

**Output**: `research.md` with all decisions documented

## Phase 1: Execution Plan & Migration Notes

### Execution Sequence

This phase documents the step-by-step commands for execution (will be detailed in Phase 2 tasks):

1. **Pre-flight checks**
   - Verify clean working directory
   - Verify all tests pass (baseline)
   - Create backup branch

2. **Folder structure creation**
   - Create `skills/` directory
   - Create `docs/` directory

3. **Skill folder moves with renames**
   - `git mv marketing-skill/ skills/marketing-team/`
   - `git mv project-management/ skills/delivery-team/`
   - `git mv engineering-team/ skills/engineering-team/`
   - `git mv product-team/ skills/product-team/`
   - `git mv c-level-advisor/cto-advisor/ skills/engineering-team/cto-advisor/`

4. **Documentation move**
   - `git mv documentation/ docs/`

5. **Deletions with documentation**
   - Document removal rationale in `migration-notes.md`
   - `git rm -r ra-qm-team/`
   - `git rm -r c-level-advisor/`
   - `git rm UPSTREAM_CONTRIBUTION_GUIDE.md`

6. **Path reference updates**
   - Update CLAUDE.md skill paths
   - Update README.md skill paths
   - Update all agent files (agents/**/*.md)
   - Update templates if needed
   - Update Python scripts if hardcoded paths exist

7. **Attribution and upstream reference cleanup**
   - Create/update CONTRIBUTORS.md with Ali Rezvani attribution
   - Update README.md with Ali Rezvani attribution and Pandora focus
   - **REVIEW ALL OTHER DOCS** (in docs/ after move) to remove upstream author references and repo links
     - Keep attribution ONLY in CONTRIBUTORS.md and README.md
     - Remove references to Ali Rezvani's workflows, original repo links, upstream contribution guides
     - Update to reflect Pandora-specific context
   - Update project description for Pandora focus throughout

8. **Validation**
   - Run markdown link checker
   - Run `./test_cli_standards.sh` (if exists)
   - Manual smoke test of Python tools
   - Verify agent paths resolve

### Migration Notes Structure

`migration-notes.md` will document:

**Removed Domains:**
- ra-qm-team/ (12 skills): ISO 13485, MDR, FDA compliance - not applicable to Pandora
- c-level-advisor/ceo-advisor/: Strategic planning - not needed for current Pandora focus

**Removed Files:**
- UPSTREAM_CONTRIBUTION_GUIDE.md: No longer contributing upstream, fork diverged for Pandora needs

**Renamed Domains:**
- marketing-skill/ → marketing-team/: Align with team-based naming
- project-management/ → delivery-team/: Reflect actual team name at Pandora
- documentation/ → docs/: Standard convention

**Moved Skills:**
- cto-advisor: c-level-advisor/ → engineering-team/ (better organizational fit)

**Retained Domains (4 total, ~26 skills):**
- skills/marketing-team/ (3 skills)
- skills/engineering-team/ (15 skills including cto-advisor)
- skills/product-team/ (5 skills)
- skills/delivery-team/ (6 skills)

### Data Model

N/A - This is a repository restructuring task. No data models are involved.

### API Contracts

N/A - This is not an API development task.

### Quickstart

After restructuring is complete, users should:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rickydwilson-dcs/claude-skills.git
   cd claude-skills
   ```

2. **Verify structure**:
   ```bash
   ls skills/  # Should show: marketing-team, engineering-team, product-team, delivery-team
   ls docs/    # Should show documentation files
   ```

3. **Run a sample skill**:
   ```bash
   python skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py --help
   ```

4. **Read Pandora-specific guidance**:
   ```bash
   cat README.md  # Updated with Pandora focus
   cat CONTRIBUTORS.md  # Ali Rezvani attribution
   ```

## Phase 2: Task Breakdown

Phase 2 is handled by `/speckit.tasks` command (not generated by `/speckit.plan`).

The tasks command will break down the execution sequence into discrete, testable tasks.

## Risks & Mitigations (from spec)

| Risk | Mitigation |
|------|------------|
| Broken internal links after restructure | Use automated link checker before and after; comprehensive find-and-replace |
| Git history lost during folder moves | Use `git mv` for all moves; test on sample file first |
| External dependencies break | Document all path changes; search for hardcoded paths; update CI/CD |
| Python tools fail with new paths | Run test suite after restructuring; verify relative paths work |

## Success Criteria (from spec)

- SC-001: ✅ skills/ directory exists, 0 skill folders in root
- SC-002: ✅ docs/ exists, documentation/ removed
- SC-003: ✅ 0 broken markdown links (validated)
- SC-004: ✅ README states "Pandora-focused" with Ali Rezvani attribution
- SC-005: ✅ CONTRIBUTORS.md exists with proper credit
- SC-006: ✅ Git history preserved for all moved files
- SC-007: ✅ Exactly 4 domains remain with documented removals
- SC-008: ✅ Clone + test execution works without path modifications
- SC-009: ✅ 0 references to "generic organizational use"

## Next Steps

1. Execute Phase 0: Create `research.md` with detailed command sequences and validation approaches
2. Execute Phase 1: Create `migration-notes.md` documenting all changes and rationale
3. Run `/speckit.tasks` to generate discrete implementation tasks
4. Execute tasks systematically with validation at each step
5. Final verification against all success criteria before merging

---

**Plan Status**: ✅ COMPLETE - Ready for `/speckit.tasks`
