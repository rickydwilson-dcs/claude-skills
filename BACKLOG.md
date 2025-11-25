# Backlog

Product backlog for claude-skills repository. This is a temporary location until migrated to Jira.

> **TODO:** Migrate this backlog to Jira and test the `delivery-team/jira-expert` skill with it!

---

## High Priority

### CI/CD Auto-Promotion Pipeline
**Type:** Feature
**Effort:** Medium
**Description:** Create GitHub Actions workflow that automatically promotes code through the branch workflow when tests pass.

**Acceptance Criteria:**
- [ ] Push to develop triggers test suite
- [ ] If tests pass, auto-merge develop → staging
- [ ] If staging checks pass, auto-merge staging → main
- [ ] Notifications on promotion success/failure
- [ ] Manual approval gate option for main promotion

**Related:** `/commit.changes` command, `docs/WORKFLOW.md`

---

## Medium Priority

### Jira Integration Testing
**Type:** Task
**Effort:** Small
**Description:** Test the `delivery-team/jira-expert` skill by migrating this backlog to Jira.

**Acceptance Criteria:**
- [ ] Create Jira project for claude-skills
- [ ] Migrate all backlog items to Jira
- [ ] Test skill's Jira MCP integration
- [ ] Document any issues or improvements needed

---

## Low Priority

*(Empty)*

---

## Completed

*(Move items here when done)*

---

**Last Updated:** 2025-11-25
