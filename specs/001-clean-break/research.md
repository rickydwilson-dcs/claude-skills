# Research: Clean Break Restructuring

**Date**: 2025-11-12
**Purpose**: Document technical research and findings before executing restructuring

## Path Reference Audit

### Skill Path References Found

**engineering-team/**: ~683 references in .md and .py files
- High volume due to 14 skills in this domain
- Will need bulk find/replace after move to skills/engineering-team/

**marketing-skill/**: ~294 references in .md files
- Moderate volume
- Must update to marketing-team/ after rename

**project-management/**: (not individually counted, included in overall audit)
- Must update to delivery-team/ after rename

**c-level-advisor/**: Multiple references in agent files
- cs-ceo-advisor agent will be deleted
- cs-cto-advisor agent paths must update to skills/engineering-team/cto-advisor/

### Agent Path Patterns

**Current Pattern**: `../../domain-name/skill-name/`

**Examples Found**:
- `../../c-level-advisor/ceo-advisor/`
- `../../c-level-advisor/cto-advisor/`
- `../../marketing-skill/content-creator/`
- `../../project-management/senior-pm/`

**New Pattern After Restructure**: `../../skills/domain-name/skill-name/`

**Update Strategy**:
1. Global find/replace for each domain
2. Test agent file parsing after updates
3. Verify relative paths resolve correctly

### Upstream Author References

**"Ali Rezvani" mentions**: 28 occurrences across markdown files

**Files likely containing references** (to be cleaned except CONTRIBUTORS.md and README.md):
- Documentation files in documentation/ (soon to be docs/)
- Possibly CLAUDE.md
- Possibly in some skill SKILL.md files (need review)

**Cleanup Strategy**:
- Keep references ONLY in CONTRIBUTORS.md and README.md
- Remove from all other documentation
- Replace with Pandora-specific context where applicable

### Markdown Files Count

**Total markdown files**: 313 files

**Link Validation Strategy**:
- Use markdown-link-check or similar tool
- Run before and after restructuring
- Fix broken links systematically

## Git History Preservation

**Command**: `git mv source destination`

**Why**: Git automatically tracks moves when using `git mv`, preserving full commit history

**Verification**: Use `git log --follow <file>` to confirm history preserved

**Test Case** (to run after first move):
```bash
git mv marketing-skill/ skills/marketing-team/
git log --follow skills/marketing-team/content-creator/SKILL.md
# Should show full history including commits before the move
```

## Find/Replace Patterns

### For CLAUDE.md and README.md

**Pattern 1**: Skill folder paths in root
```bash
# Find
engineering-team/
marketing-skill/
product-team/
project-management/
c-level-advisor/
documentation/

# Replace with
skills/engineering-team/
skills/marketing-team/
skills/product-team/
skills/delivery-team/
skills/engineering-team/  # for cto-advisor references
docs/
```

### For Agent Files

**Pattern 2**: Agent relative paths
```bash
# agents/marketing/*.md
../../marketing-skill/ → ../../skills/marketing-team/

# agents/product/*.md
../../product-team/ → ../../skills/product-team/

# agents/c-level/cs-cto-advisor.md
../../c-level-advisor/cto-advisor/ → ../../skills/engineering-team/cto-advisor/

# All agent files
../../engineering-team/ → ../../skills/engineering-team/
../../project-management/ → ../../skills/delivery-team/
```

### For Documentation Files

**Pattern 3**: Cross-references within docs
```bash
# After moving documentation/ to docs/
../documentation/ → ./  # (within docs/)
documentation/ → docs/  # (from root-level files)
```

## Link Validation Tools

**Option 1**: markdown-link-check (npm package)
```bash
npm install -g markdown-link-check
markdown-link-check README.md
find . -name "*.md" -exec markdown-link-check {} \;
```

**Option 2**: Manual verification
- Test key navigation paths
- Verify agent skill references
- Check documentation cross-references

**Chosen Approach**: Manual spot-checking of critical files + automated checks on README/CLAUDE.md

## Attribution Best Practices

### Standard GitHub Fork Attribution

**CONTRIBUTORS.md Format**:
```markdown
# Contributors

## Original Author

- **Ali Rezvani** - Original creator of claude-skills
  - GitHub: [@alirezarezvani](https://github.com/alirezarezvani)
  - Repository: [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)

## Pandora Fork Maintainers

- **[Your Name]** - Pandora-focused fork and direction
  - Specialized for Pandora's engineering, product, marketing, and delivery teams
```

**README.md Attribution Section**:
```markdown
## Attribution

Originally created by [Ali Rezvani](https://github.com/alirezarezvani/claude-skills).

This is a Pandora-focused fork customized for our specific team needs and workflows.
```

### MIT License Compliance

- Original LICENSE file should remain unchanged (preserves Ali Rezvani's copyright)
- Attribution in README and CONTRIBUTORS satisfies MIT license requirements
- Fork nature clearly stated

## Python Tool Path Considerations

**Current Assumption**: Python tools use relative imports within their skill package

**Risk**: If any tools have hardcoded absolute paths to other skills

**Mitigation**:
1. Grep Python files for potential hardcoded paths (T005/T032)
2. Test execution of sample tools after restructuring (T037)
3. Fix any issues found

**Most Likely Outcome**: No changes needed - tools are self-contained within skill packages

## Execution Order Rationale

### Why This Sequence

1. **Create target directories first** (skills/, docs/)
   - Provides destinations for moves
   - Clear structure

2. **Move/rename skill folders** (with git mv)
   - Preserves history
   - Can run some in parallel (different source folders)

3. **Move documentation** (git mv documentation/ docs/)
   - Single operation
   - History preserved

4. **Delete unwanted domains** (git rm -r)
   - Only after moves complete
   - Prevents accidental deletion of items we want to keep (cto-advisor)

5. **Update path references** (find/replace in files)
   - Only after physical moves complete
   - Ensures paths point to actual locations

6. **Add attribution** (create CONTRIBUTORS.md, update README)
   - After structure stable
   - Clean point to establish new identity

7. **Clean documentation** (remove upstream references)
   - After attribution established
   - Know what to keep (CONTRIBUTORS/README) vs. what to clean (everything else)

8. **Validate** (tests, link checks)
   - Final step
   - Catch any issues before committing

## Time Estimates

Based on task complexity and file volumes:

- **Phase 1** (Pre-flight): 15 minutes
- **Phase 2** (Research): 30 minutes
- **Phase 3** (US1 Structure): 90-120 minutes (most file operations)
- **Phase 4** (US2 Attribution): 30 minutes
- **Phase 5** (US3 Curation): 30 minutes
- **Phase 6** (US4 Identity): 60-90 minutes (depends on cleanup volume)
- **Phase 7** (Validation): 45-60 minutes

**Total**: 5-7 hours for complete execution with careful validation

**MVP** (US1 + US2 only): 2.5-3 hours

## Risks and Mitigations

### Risk 1: Broken Links After Restructuring
**Likelihood**: High (313 markdown files, many cross-references)
**Impact**: Medium (confusing but not breaking)
**Mitigation**: Systematic find/replace, automated link checking, manual verification of key paths

### Risk 2: Git History Loss
**Likelihood**: Low (using git mv)
**Impact**: High (lose project history)
**Mitigation**: Test with first move, verify with git log --follow, backup branch created

### Risk 3: Agent Paths Not Resolving
**Likelihood**: Medium (many relative paths to update)
**Impact**: High (agents won't work)
**Mitigation**: Systematic pattern matching, test agent file parsing, spot-check resolution

### Risk 4: Python Tools Break
**Likelihood**: Low (tools are self-contained)
**Impact**: Medium (tools need fixing)
**Mitigation**: Test sample tool execution, grep for hardcoded paths first

### Risk 5: Incomplete Upstream Reference Cleanup
**Likelihood**: Medium (28 references to find/clean)
**Impact**: Low (cosmetic, doesn't break functionality)
**Mitigation**: Grep before and after, systematic review, acceptance that some may remain in skill content (acceptable if not in main docs)

---

**Research Complete**: Ready to proceed with Phase 3 (US1 Structure Reorganization)
