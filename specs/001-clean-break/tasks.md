# Tasks: Clean Break - Pandora-Focused Restructure

**Input**: Design documents from `/specs/001-clean-break/`
**Prerequisites**: plan.md (complete), spec.md (complete)

**Tests**: No automated tests for this restructuring task. Validation will be manual verification and link checking.

**Organization**: Tasks are grouped by user story (P1, P2, P3) to enable phased execution and independent validation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (independent operations, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- File paths included where applicable

## Phase 1: Pre-flight and Setup

**Purpose**: Validate baseline and create backup before making changes

- [ ] T001 Verify git working directory is clean (no uncommitted changes)
- [ ] T002 Run baseline tests to establish current state (if test suite exists)
- [ ] T003 Create backup branch `backup-pre-clean-break` from current develop
- [ ] T004 Document current folder structure in specs/001-clean-break/migration-notes.md (BEFORE section)

**Checkpoint**: Baseline established - safe to proceed with restructuring

---

## Phase 2: Research & Path Audit

**Purpose**: Gather intelligence before making changes

- [ ] T005 [P] Search for all hardcoded paths referencing skill folders (grep for "engineering-team/", "marketing-skill/", etc.)
- [ ] T006 [P] Audit all agent files for skill path references (grep agents/ for "../../")
- [ ] T007 [P] Search documentation for upstream author references (grep for "Ali Rezvani", "alirezarezvani", upstream repo URLs)
- [ ] T008 [P] List all markdown files for link validation baseline
- [ ] T009 Document findings in specs/001-clean-break/research.md

**Checkpoint**: Complete understanding of changes needed

---

## Phase 3: User Story 1 - Repository Structure Reorganization (Priority: P1) 🎯

**Goal**: Move all skills to `skills/` directory, rename key folders, clean repository root

**Independent Test**: Clone repository and verify: (1) skills/ directory exists with 4 subdirectories, (2) docs/ exists, (3) no skill folders in root, (4) documentation/ folder removed

### US1: Folder Structure Creation

- [ ] T010 [US1] Create `skills/` directory at repository root
- [ ] T011 [US1] Create `docs/` directory at repository root (will receive documentation/ contents)

### US1: Skill Folder Moves with Renames

- [ ] T012 [P] [US1] Move and rename: `git mv marketing-skill/ skills/marketing-team/`
- [ ] T013 [P] [US1] Move and rename: `git mv project-management/ skills/delivery-team/`
- [ ] T014 [US1] Move: `git mv engineering-team/ skills/engineering-team/`
- [ ] T015 [US1] Move: `git mv product-team/ skills/product-team/`

### US1: CTO Advisor Special Move

- [ ] T016 [US1] Move cto-advisor to engineering: `git mv c-level-advisor/cto-advisor/ skills/engineering-team/cto-advisor/`

### US1: Documentation Move

- [ ] T017 [US1] Move documentation: `git mv documentation/ docs/`

### US1: Domain Deletions

- [ ] T018 [US1] Delete ra-qm-team: `git rm -r ra-qm-team/`
- [ ] T019 [US1] Delete c-level-advisor (now empty after cto-advisor move): `git rm -r c-level-advisor/`
- [ ] T020 [US1] Delete UPSTREAM_CONTRIBUTION_GUIDE.md: `git rm UPSTREAM_CONTRIBUTION_GUIDE.md`

### US1: Path Reference Updates - Core Files

- [ ] T021 [US1] Update skill paths in CLAUDE.md (find/replace for moved folders)
- [ ] T022 [US1] Update skill paths in README.md (find/replace for moved folders)
- [ ] T023 [US1] Update .gitignore if needed for new folder structure

### US1: Path Reference Updates - Agents

- [ ] T024 [P] [US1] Update agent paths in agents/marketing/ (change ../../marketing-skill/ to ../../skills/marketing-team/)
- [ ] T025 [P] [US1] Update agent paths in agents/product/ (change ../../product-team/ to ../../skills/product-team/)
- [ ] T026 [P] [US1] Update agent paths in agents/c-level/ (change ../../c-level-advisor/cto-advisor/ to ../../skills/engineering-team/cto-advisor/)
- [ ] T027 [US1] Update any agent paths referencing engineering-team, project-management folders
- [ ] T028 [US1] Remove agents for deleted domains (ra-qm agents, ceo-advisor agent)

### US1: Path Reference Updates - Documentation

- [ ] T029 [US1] Update documentation internal links for new docs/ location
- [ ] T030 [US1] Update documentation skill references for new skills/ structure

### US1: Path Reference Updates - Templates

- [ ] T031 [P] [US1] Check and update templates/ for any skill path references

### US1: Path Reference Updates - Python Scripts

- [ ] T032 [P] [US1] Search Python scripts for hardcoded paths (if any found in T005)
- [ ] T033 [US1] Update any hardcoded paths in Python scripts

### US1: Validation

- [ ] T034 [US1] Verify folder structure matches plan (skills/, docs/, 4 skill domains)
- [ ] T035 [US1] Verify deleted folders no longer exist (ra-qm-team/, c-level-advisor/, documentation/)
- [ ] T036 [US1] Run markdown link checker on all files
- [ ] T037 [US1] Test sample Python tool execution: `python skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py --help`
- [ ] T038 [US1] Verify agent paths resolve correctly (spot check agent files)

**Checkpoint**: Repository structure complete, all paths updated, validation passing

---

## Phase 4: User Story 2 - Attribution and Credit Restructure (Priority: P1)

**Goal**: Properly credit Ali Rezvani while establishing Pandora ownership

**Independent Test**: Review CONTRIBUTORS.md (exists with Ali Rezvani + upstream link) and README.md (has "Originally created by Ali Rezvani" + "Pandora-focused" statements)

### US2: Create Attribution Files

- [ ] T039 [US2] Create CONTRIBUTORS.md with Ali Rezvani as original author, link to https://github.com/alirezarezvani/claude-skills

### US2: Update README for Attribution and Pandora Focus

- [ ] T040 [US2] Add "Originally created by Ali Rezvani" section to README.md with upstream link
- [ ] T041 [US2] Update README.md hero/description to state "Pandora-focused"
- [ ] T042 [US2] Update README.md skill count and domain list (4 domains, ~26 skills)
- [ ] T043 [US2] Remove generic "for any organization" language from README.md

### US2: Validation

- [ ] T044 [US2] Human review: Verify CONTRIBUTORS.md content is accurate and respectful
- [ ] T045 [US2] Human review: Verify README.md attribution is prominent and clear
- [ ] T046 [US2] Human review: Verify README.md reflects Pandora focus throughout

**Checkpoint**: Attribution complete, Pandora ownership established

---

## Phase 5: User Story 3 - Pandora-Specific Skill Curation (Priority: P2)

**Goal**: Document removed content and update all references to reflect 4-domain structure

**Independent Test**: Review migration-notes.md (complete removal documentation) and verify docs/ references match actual 4 domains

### US3: Document Removals in Migration Notes

- [ ] T047 [US3] Complete specs/001-clean-break/migration-notes.md with:
  - Removed domains section (ra-qm-team, c-level-advisor/ceo-advisor)
  - Removed files section (UPSTREAM_CONTRIBUTION_GUIDE.md)
  - Renamed domains section (marketing-skill→marketing-team, project-management→delivery-team)
  - Moved skills section (cto-advisor)
  - Retained domains section (4 domains, ~26 skills)
  - Rationale for each change

### US3: Update Documentation References

- [ ] T048 [P] [US3] Update CLAUDE.md domain references (6 domains → 4 domains)
- [ ] T049 [P] [US3] Update any docs/ files referencing deleted domains
- [ ] T050 [US3] Update docs/ skill count references throughout (40 → ~26)

### US3: Validation

- [ ] T051 [US3] Verify migration-notes.md is complete and clear
- [ ] T052 [US3] Grep for any remaining references to ra-qm-team or deleted c-level skills
- [ ] T053 [US3] Verify all documentation accurately reflects 4-domain structure

**Checkpoint**: Curation documented, references updated

---

## Phase 6: User Story 4 - Clean Project Identity (Priority: P3)

**Goal**: Remove upstream references from all docs (except CONTRIBUTORS/README) and establish Pandora-specific language

**Independent Test**: Grep all docs/ files for "Ali Rezvani", "alirezarezvani", upstream repo URLs → should only find matches in CONTRIBUTORS.md and README.md

### US4: Documentation Cleanup Audit

- [ ] T054 [US4] Create list of all docs/ files containing upstream references (from T007 findings)
- [ ] T055 [US4] For each file identified, document specific lines/sections to modify

### US4: Remove Upstream References from Documentation

- [ ] T056 [P] [US4] Review and clean docs/WORKFLOW.md (remove upstream author references if present)
- [ ] T057 [P] [US4] Review and clean docs/standards/ files (remove upstream references)
- [ ] T058 [P] [US4] Review and clean docs/implementation/ files (remove upstream references)
- [ ] T059 [P] [US4] Review and clean docs/delivery/ files (remove upstream references)
- [ ] T060 [US4] Review CLAUDE.md and remove any upstream workflow references (keep constitution references)

### US4: Replace with Pandora-Specific Context

- [ ] T061 [P] [US4] Update docs/ files to reference Pandora teams/workflows where applicable
- [ ] T062 [P] [US4] Update CLAUDE.md with Pandora-specific use case examples
- [ ] T063 [US4] Replace generic "teams" or "organizations" language with Pandora-specific terminology

### US4: Validation

- [ ] T064 [US4] Grep docs/ for "Ali Rezvani" → should ONLY appear in CONTRIBUTORS.md and README.md
- [ ] T065 [US4] Grep docs/ for "alirezarezvani" → should ONLY appear in CONTRIBUTORS.md and README.md (as repo link)
- [ ] T066 [US4] Grep docs/ for upstream repo URL → should ONLY appear in CONTRIBUTORS.md and README.md
- [ ] T067 [US4] Human review: Spot check documentation for Pandora-specific context

**Checkpoint**: Clean project identity established, documentation reflects Pandora focus

---

## Phase 7: Final Validation and Polish

**Purpose**: Comprehensive validation before merge

### Link Validation

- [ ] T068 Run markdown link checker on entire repository
- [ ] T069 Fix any broken links found by link checker
- [ ] T070 Verify all internal cross-references work correctly

### Functional Validation

- [ ] T071 Test Python tool execution from multiple skills (verify no path issues)
- [ ] T072 Verify agent files can be read and parse correctly
- [ ] T073 Clone repository fresh and verify Quick Start from README.md works

### Git History Validation

- [ ] T074 Verify git history preserved: `git log --follow skills/marketing-team/content-creator/SKILL.md` (should show history)
- [ ] T075 Verify git history preserved for cto-advisor: `git log --follow skills/engineering-team/cto-advisor/SKILL.md`

### Success Criteria Verification

- [ ] T076 SC-001: Verify skills/ directory exists, 0 skill folders in root ✅
- [ ] T077 SC-002: Verify docs/ exists, documentation/ removed ✅
- [ ] T078 SC-003: Verify 0 broken markdown links ✅
- [ ] T079 SC-004: Verify README "Pandora-focused" + Ali Rezvani attribution ✅
- [ ] T080 SC-005: Verify CONTRIBUTORS.md exists with proper credit ✅
- [ ] T081 SC-006: Verify git history preserved (tested in T074-T075) ✅
- [ ] T082 SC-007: Verify exactly 4 domains, removals documented ✅
- [ ] T083 SC-008: Verify clone + test execution works ✅
- [ ] T084 SC-009: Verify 0 references to "generic organizational use" ✅

### Documentation Updates

- [ ] T085 Update specs/001-clean-break/migration-notes.md with final statistics (files moved, lines changed, etc.)
- [ ] T086 Update CHANGELOG.md with v2.3.0 or v3.0.0 release notes for Clean Break restructuring

### Commit and Push

- [ ] T087 Stage all changes: `git add -A`
- [ ] T088 Create comprehensive commit with conventional format
- [ ] T089 Push to origin: `git push origin 001-clean-break`

**Checkpoint**: All validation passing, ready for PR or merge

---

## Dependencies and Execution Order

### Critical Path (Must be sequential):
1. Phase 1 (Pre-flight) → Phase 2 (Research) → Phase 3 (US1 Structure) → Phase 4 (US2 Attribution) → Phase 5 (US3 Curation) → Phase 6 (US4 Identity) → Phase 7 (Validation)

### Within-Phase Parallelization:
- **Phase 2**: Tasks T005-T008 can run in parallel (all are audits)
- **Phase 3 US1 Moves**: Tasks T012-T013 can run in parallel (different source folders)
- **Phase 3 US1 Agent Updates**: Tasks T024-T026 can run in parallel (different agent directories)
- **Phase 3 US1 Misc Updates**: Tasks T029, T031, T032 can run in parallel
- **Phase 4 US2**: Tasks T040-T043 can run in parallel (all editing README sections)
- **Phase 5 US3**: Tasks T048-T050 can run in parallel (different doc files)
- **Phase 6 US4**: Tasks T056-T059 can run in parallel (different doc files)
- **Phase 6 US4**: Tasks T061-T062 can run in parallel
- **Phase 7**: Tasks T068-T073 should be sequential (fix issues as found)

### User Story Dependencies:
- US1 (Structure) MUST complete before US2 (Attribution) - need final paths
- US2 (Attribution) MUST complete before US3 (Curation) - need README/CONTRIBUTORS established
- US3 (Curation) MUST complete before US4 (Identity) - need migration notes as reference
- US4 (Identity) MUST complete before Final Validation

## Parallel Execution Examples

### Example 1: Research Phase
```bash
# Can run these greps simultaneously:
grep -r "engineering-team/" . > engineering-paths.txt &
grep -r "Ali Rezvani" docs/ > ali-references.txt &
grep -r "../../" agents/ > agent-paths.txt &
wait
```

### Example 2: US1 Skill Folder Moves
```bash
# Can execute moves in parallel (different source folders):
git mv marketing-skill/ skills/marketing-team/ &
git mv project-management/ skills/delivery-team/ &
wait
```

### Example 3: US3 Documentation Updates
```bash
# Can edit different files in parallel:
# Terminal 1: Edit CLAUDE.md
# Terminal 2: Edit docs/WORKFLOW.md
# Terminal 3: Edit docs/standards/cli-standards.md
```

## Implementation Strategy

**MVP Scope**: User Story 1 (Structure) + User Story 2 (Attribution)
- Delivers: Clean folder structure, proper attribution, functional repository
- Testable: Clone repo, verify structure, run sample tools
- Time: ~2-3 hours with validation

**Phase 2 Add-on**: User Story 3 (Curation)
- Delivers: Complete documentation of changes
- Testable: Review migration notes, verify doc references
- Time: ~1 hour

**Phase 3 Add-on**: User Story 4 (Identity)
- Delivers: Clean Pandora-specific identity
- Testable: Grep for upstream references
- Time: ~2-3 hours (depends on doc volume)

**Total Estimated Time**: 6-9 hours for complete restructuring

---

## Task Summary

**Total Tasks**: 89
- Phase 1 (Pre-flight): 4 tasks
- Phase 2 (Research): 5 tasks
- Phase 3 (US1 - Structure): 29 tasks
- Phase 4 (US2 - Attribution): 8 tasks
- Phase 5 (US3 - Curation): 7 tasks
- Phase 6 (US4 - Identity): 14 tasks
- Phase 7 (Validation): 22 tasks

**Parallelizable Tasks**: 27 tasks (30% of total)

**Independent Test Criteria**:
- US1: Folder structure verification
- US2: Attribution file verification
- US3: Migration notes completeness
- US4: Upstream reference grep audit

**Suggested MVP**: Phase 1 + Phase 2 + Phase 3 + Phase 4 (US1 + US2) = Functional restructured repository with proper attribution
