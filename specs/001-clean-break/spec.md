# Feature Specification: Clean Break - Pandora-Focused Restructure

**Feature Branch**: `001-clean-break`
**Created**: 2025-11-12
**Status**: Draft
**Input**: User description: "Clean Break - Restructure project for Pandora-specific focus"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Repository Structure Reorganization (Priority: P1)

As a developer working on the Pandora-focused claude-skills repository, I need all skills organized in a dedicated folder structure so that the repository root is clean and the project purpose is immediately clear.

**Why this priority**: Foundation for all other changes. A clear structure enables efficient navigation and sets the stage for Pandora-specific customization.

**Independent Test**: Can be fully tested by cloning the repository and verifying all skills are in the `skills/` directory with no skill folders remaining in root, and delivers immediate clarity of project organization.

**Acceptance Scenarios**:

1. **Given** skills currently exist in root (engineering-team/, marketing-skill/, product-team/, project-management/), **When** restructuring is complete, **Then** all retained skills exist under `skills/` directory with renamed folders: marketing-team/, engineering-team/, product-team/, delivery-team/
2. **Given** documentation currently in `documentation/` folder, **When** restructuring is complete, **Then** all documentation exists in `docs/` folder with no broken internal links
3. **Given** references to skill paths exist throughout the repository (CLAUDE.md, README.md, agents), **When** restructuring is complete, **Then** all path references are updated to new locations and no broken links exist

---

### User Story 2 - Attribution and Credit Restructure (Priority: P1)

As the new project maintainer, I need to properly attribute the original author Ali Rezvani while establishing clear ownership for the Pandora-focused direction, so that intellectual property and contribution history are properly preserved.

**Why this priority**: Critical for legal/ethical clarity and establishing new project identity. Must be done before any external communication about the fork.

**Independent Test**: Can be fully tested by reviewing README.md, CONTRIBUTORS, and LICENSE files to verify Ali Rezvani is credited as original author while Pandora direction is clearly stated, and delivers proper attribution and project clarity.

**Acceptance Scenarios**:

1. **Given** current README references upstream workflows and generic organizational use, **When** attribution restructure is complete, **Then** README includes "Originally created by Ali Rezvani" section with link to original repo, and clearly states "Pandora-focused fork and direction"
2. **Given** various files contain Ali Rezvani's original workflows and references, **When** attribution restructure is complete, **Then** CONTRIBUTORS.md exists listing Ali Rezvani as original author with appropriate credit
3. **Given** project currently presents as generic skills library, **When** attribution restructure is complete, **Then** project description emphasizes Pandora-specific focus while maintaining original author credit

---

### User Story 3 - Pandora-Specific Skill Curation (Priority: P2)

As a Pandora team member, I need only the skills and agents relevant to Pandora's work preserved in the repository, so that the project remains focused and maintainable for our specific needs.

**Why this priority**: Reduces complexity and maintenance burden. Follows P1 restructuring but can be done incrementally as Pandora needs are identified.

**Independent Test**: Can be fully tested by reviewing `skills/` directory and verifying only Pandora-relevant skills remain, and delivers a focused, maintainable skill set aligned with actual organizational needs.

**Acceptance Scenarios**:

1. **Given** 40 skills currently exist (including ra-qm-team with 12 skills, c-level-advisor with 2 skills), **When** curation is complete, **Then** ra-qm-team/ and c-level-advisor/ directories no longer exist, and only 4 domains remain: marketing-team/, engineering-team/ (including cto-advisor), product-team/, delivery-team/
2. **Given** agents reference skills from deleted domains, **When** curation is complete, **Then** agents for ra-qm-team and c-level domains are removed, cto-advisor agent is moved to engineering domain with updated references
3. **Given** documentation references all 40 skills and 6 domains, **When** curation is complete, **Then** documentation reflects ~26 retained skills across 4 domains (Marketing, Engineering, Product, Delivery) with Pandora-specific context

---

### User Story 4 - Clean Project Identity (Priority: P3)

As a new contributor to the Pandora claude-skills project, I need clear documentation that reflects Pandora's needs and direction (not generic organizational use), so that I understand the project's purpose and can contribute effectively.

**Why this priority**: Improves developer experience and onboarding. Can be refined after core restructuring is complete.

**Independent Test**: Can be fully tested by a new developer reading CLAUDE.md and README.md and understanding Pandora-specific context without confusion about generic organizational use, and delivers clear project purpose and contribution guidelines.

**Acceptance Scenarios**:

1. **Given** CLAUDE.md contains generic organizational guidance, **When** identity cleanup is complete, **Then** CLAUDE.md reflects Pandora-specific workflows and use cases
2. **Given** README.md describes generic skill library for any organization, **When** identity cleanup is complete, **Then** README.md clearly states Pandora focus and specific domains of interest
3. **Given** documentation contains references to "teams" and "organizations" generically, **When** identity cleanup is complete, **Then** documentation uses Pandora-specific language and examples

---

### Edge Cases

- What happens when path references exist in Python scripts (hardcoded paths)?
- How does system handle broken symlinks or cached paths after restructure?
- What happens to git history when folders are moved (is history preserved)?
- How do external tools or CI/CD pipelines handle the new folder structure?
- What happens if some skills are partially Pandora-relevant (keep or remove)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST reorganize all retained skill folders into a new `skills/` directory at repository root with renamed folders:
  - `engineering-team/` → `skills/engineering-team/`
  - `marketing-skill/` → `skills/marketing-team/`
  - `product-team/` → `skills/product-team/`
  - `project-management/` → `skills/delivery-team/`
- **FR-002**: System MUST rename `documentation/` folder to `docs/` and update all references
- **FR-003**: System MUST preserve git history for moved files and folders
- **FR-004**: System MUST update all relative path references in:
  - CLAUDE.md
  - README.md
  - Agent files (agents/**/*.md)
  - Python scripts (if any hardcoded paths exist)
  - Documentation files
  - Template files
- **FR-005**: System MUST create/update CONTRIBUTORS.md file crediting Ali Rezvani as original author with link to upstream repository (https://github.com/alirezarezvani/claude-skills)
- **FR-006**: System MUST update README.md to clearly state Pandora-specific focus while maintaining "Originally created by" attribution to Ali Rezvani
- **FR-007**: System MUST remove the following domains and move/rename as specified:
  - DELETE: `ra-qm-team/` directory and all associated agents
  - DELETE: `c-level-advisor/` directory and all associated agents (including ceo-advisor)
  - MOVE: CTO advisor skill from `c-level-advisor/cto-advisor/` to `engineering-team/cto-advisor/`
  - All removed content MUST be documented in migration notes with removal rationale
- **FR-008**: System MUST update project description, mission statement, and documentation to reflect Pandora-specific use cases rather than generic organizational use
- **FR-009**: System MUST validate all markdown links are not broken after restructuring
- **FR-010**: System MUST update .gitignore if needed to reflect new folder structure

### Key Entities

- **Skill Package**: Self-contained folder containing SKILL.md, scripts/, references/, assets/. Must be moved from root to `skills/` directory while preserving internal structure.
- **Agent**: Orchestration file in `agents/` directory. Must have path references updated to point to new `skills/` locations.
- **Documentation File**: Markdown file in current `documentation/` directory. Must be moved to `docs/` with all cross-references updated.
- **Attribution Record**: New or updated files (CONTRIBUTORS.md, README.md sections) that properly credit Ali Rezvani as original author.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Repository root contains `skills/` directory with all skill packages, and no skill-related folders remain in root (0 skill folders in root after completion)
- **SC-002**: Documentation exists in `docs/` directory, and `documentation/` directory no longer exists (100% migration)
- **SC-003**: All markdown links in README.md, CLAUDE.md, and documentation files resolve correctly with 0 broken links (validated by link checker)
- **SC-004**: README.md clearly states "Pandora-focused" direction and includes "Originally created by Ali Rezvani" attribution (human verification)
- **SC-005**: CONTRIBUTORS.md exists with Ali Rezvani credited as original author with link to upstream repository (file exists and contains required information)
- **SC-006**: Git history is preserved for all moved files (git log --follow shows file history through moves)
- **SC-007**: Exactly 4 skill domains remain (marketing-team/, engineering-team/, product-team/, delivery-team/), ra-qm-team/ and c-level-advisor/ directories are deleted, cto-advisor is in engineering-team/, with removal documented in migration notes (26 skills from 4 domains)
- **SC-008**: Project can be cloned and all scripts/tools work without modification to account for new paths (functional test: clone, run tests, execute sample workflows)
- **SC-009**: CLAUDE.md and README.md reflect Pandora-specific context with 0 references to "generic organizational use" or "any organization" (content audit passes)

## Assumptions & Dependencies

### Assumptions

- Git is available for history-preserving moves (`git mv` commands)
- All current tests pass before restructuring begins (baseline quality established)
- Python tools use relative paths or will be updated to do so
- No external CI/CD pipelines depend on current folder structure (or can be updated)
- Pandora-relevant skills can be identified through team consultation or documented criteria
- Attribution to Ali Rezvani is legally and ethically sufficient (no additional licensing concerns)

### Dependencies

- Access to git repository with write permissions
- Link checker tool for validating markdown links (e.g., `markdown-link-check`)
- Agreement on which skills are Pandora-relevant (requires stakeholder input)
- Decision on whether to archive removed skills or delete entirely (suggests archiving in separate branch)

## Out of Scope

- Modifying the functionality of existing skills or agents (only restructuring/reorganizing)
- Creating new Pandora-specific skills (focus is on reorganization of existing content)
- Changing skill documentation content beyond path references (content remains as-is)
- Re-architecting the skill package format or agent structure (format stays the same)
- Migrating to different version control system or repository hosting
- Changing LICENSE file terms (attribution only, not license modification)

## Risks & Mitigations

### Risk: Broken internal links after restructure
**Mitigation**: Use automated link checker before and after changes; comprehensive find-and-replace for common path patterns; manual review of critical files

### Risk: Git history lost during folder moves
**Mitigation**: Use `git mv` for all moves; test history preservation on sample file first; document move commands for repeatability

### Risk: External dependencies break (CI/CD, documentation sites, etc.)
**Mitigation**: Document all path changes in migration guide; search codebase for hardcoded paths; update CI/CD configs as part of restructure

### Risk: Unclear which skills are Pandora-relevant
**Mitigation**: Create explicit criteria document; consult with Pandora teams before removal; archive removed skills in separate branch for potential recovery

### Risk: Attribution to Ali Rezvani is legally insufficient
**Mitigation**: Review LICENSE file terms from upstream; consult with legal if needed; err on side of more attribution rather than less

## Notes

This specification focuses on WHAT needs to change (folder structure, attribution, curation) and WHY (Pandora-specific focus, clear ownership, maintainability), without prescribing HOW to implement (specific git commands, scripts, or tools). The planning phase will determine the technical approach.
