# Speckit Removal Plan

**Date:** 2025-11-24
**Session:** 2025-11-24_20-33-06_docs-reorganization
**Reason:** Speckit is causing confusion and doesn't belong in this repository

---

## Issue

Speckit commands have contaminated the documentation:
- 106 references found across docs/ and commands/
- Examples in catalogs reference speckit commands
- Standards reference speckit patterns
- These commands don't exist in this repo and cause confusion

## Action Required

1. **Remove from commands/CATALOG.md**
   - Remove "General Category (Speckit Workflow)" section
   - Remove all 8 speckit command references
   - Update statistics (20 → 12 commands)

2. **Remove from docs/catalogs/commands.md**
   - Remove speckit workflow section
   - Update examples to use actual commands
   - Update statistics

3. **Update docs/catalogs/commands.md examples**
   - Replace speckit examples with analyze.*, generate.*, review.*
   - Use actual commands that exist

4. **Remove from commands/README.md**
   - Remove speckit references
   - Update examples
   - Update statistics

5. **Update .claude/commands/ directory**
   - Remove or move speckit commands (they're project-specific, not library commands)

## Replacement Examples

### Before (Speckit - WRONG)
```bash
/speckit.specify "Add user authentication"
/speckit.plan
/speckit.tasks
```

### After (Actual Commands - CORRECT)
```bash
/analyze.code-quality src/
/review.security
/generate.tests src/
```

---

## Files to Update

1. commands/CATALOG.md
2. commands/README.md
3. docs/catalogs/commands.md
4. docs/development/commands/installation.md
5. docs/development/commands/creation.md
6. Any other files with speckit references

---

## New Command Count

After removal:
- Total: 12 commands (not 20)
- Categories:
  - Analysis: 4 commands
  - Generation: 2 commands
  - Git: 2 commands
  - Workflow: 3 commands
  - Test: 1 command (sample)

---

## Next Steps

1. Execute cleanup
2. Verify no speckit references remain
3. Update all statistics
4. Update examples to use verb.object pattern
5. Commit changes

---

**Status:** Planning
**Priority:** High - Blocking correct documentation
