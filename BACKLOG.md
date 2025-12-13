# Backlog

Product backlog for claude-skills repository. This is a temporary location until migrated to Jira.

> **TODO:** Migrate this backlog to Jira and test the `delivery-team/jira-expert` skill with it!

---

## High Priority

*(Empty - items moved to Completed)*

---

## Medium Priority

### Legacy Codebase Analyzer Skill & Agent
**Type:** Feature
**Effort:** Large
**Description:** Create new `legacy-codebase-analyzer` skill and `cs-legacy-codebase-analyzer` agent for comprehensive technical debt analysis and modernization strategy development.

**Skill Package:**
- **Location:** `skills/engineering-team/legacy-codebase-analyzer/`
- **7 Python Tools:** codebase_inventory.py, security_vulnerability_scanner.py, performance_bottleneck_detector.py, code_quality_analyzer.py, architecture_health_analyzer.py, technical_debt_scorer.py, modernization_roadmap_generator.py
- **3 References:** analysis_framework.md, modernization_patterns.md, deliverable_templates.md
- **3 Assets:** executive_summary_template.md, technical_debt_report_template.md, roadmap_template.md

**Agent:**
- **Location:** `agents/engineering/cs-legacy-codebase-analyzer.md`
- **Type:** Quality (Red) - Heavy analysis, resource-intensive
- **Model:** opus

**Acceptance Criteria:**
- [ ] Create skill package with all Python tools (standard library only)
- [ ] All 7 Python tools support `--help` and JSON output
- [ ] Create comprehensive SKILL.md with 5+ workflows
- [ ] Create agent with proper YAML frontmatter
- [ ] Document 5 key workflows in agent
- [ ] Validate with `python3 scripts/skill_builder.py --validate`
- [ ] Validate with `python3 scripts/agent_builder.py --validate`
- [ ] Add to AGENTS_CATALOG.md and SKILLS_CATALOG.md
- [ ] Update CLAUDE.md with new skill/agent references

**Related Prompts:** Legacy Codebase Analysis & Modernization Agent prompt (provided by user)

**Integration Points:**
- Complements `senior-architect` (architecture analysis)
- Complements `code-reviewer` (code quality metrics)
- Complements `senior-secops` (security scanning)
- Complements `cto-advisor` (strategic tech debt view)

---

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

## Strategic Gap Analysis Backlog (From Competitive Analysis)

**Source:** [MEGA-REPORT.md](output/sessions/rickywilson/2025-12-02_competitive-analysis-wshobson-agents/MEGA-REPORT.md)
**Analysis Date:** December 2, 2025

### Critical Priority

| # | Gap | Effort | Status |
|---|-----|--------|--------|
| 1 | **Mobile Development** (cs-mobile-engineer) | 21-34 SP | Not Started |

### High Priority - Immediate

| # | Gap | Effort | Status |
|---|-----|--------|--------|
| 2 | **GraphQL Specialist** (cs-graphql-architect) | 8-13 SP | Not Started |
| 3 | **Legacy Modernization** (cs-legacy-codebase-analyzer) | 8-13 SP | **In Backlog** (see Medium Priority) |
| 4 | **Observability Engineering** (cs-observability-engineer) | 13-21 SP | Not Started |
| 5 | **Incident Response** (cs-incident-responder) | 8-13 SP | Not Started |
| 6 | **Java/Spring Enterprise** (cs-java-engineer) | 13-21 SP | Not Started |
| 7 | **C# .NET Ecosystem** (cs-dotnet-engineer) | 13-21 SP | Not Started |
| 8 | **Real-time Streaming** (enhance cs-data-engineer) | 8-13 SP | Not Started |
| 9 | **Interactive Documentation** (enhance cs-technical-writer) | 8-13 SP | Not Started |

### Medium Priority

| # | Gap | Effort | Status |
|---|-----|--------|--------|
| 10 | **Network Engineering** (cs-network-engineer) | 8-13 SP | Not Started |
| 11 | **iOS Engineer** (cs-ios-engineer) | 8 SP | Not Started |
| 12 | **Flutter Engineer** (cs-flutter-engineer) | 8 SP | Not Started |
| 13 | **Mermaid Diagrams** (enhance cs-technical-writer) | 5 SP | Not Started |
| 14 | **SEO Strategist** (cs-seo-strategist) | 5 SP | Not Started |

### Explicitly Out of Scope (Irrelevant Domains)

- Game Development (Unity, Minecraft plugins)
- Blockchain/Web3
- Systems Programming (C/C++/Rust at kernel level)
- Embedded Systems (ARM microcontrollers)
- Quantitative Trading
- HR/Legal
- Customer/Sales Ops

---

## Python Tools Implementation Backlog

**Audit Date:** 2025-12-02
**Total Placeholder Scripts:** 27 of 82 (33%)
**Status:** Needs Implementation

All placeholder scripts follow identical boilerplate pattern with `analyze()` method containing `self.results['findings'] = []` and comment `# Main logic here` with no actual implementation.

---

### Priority 1: Code Quality & Review (3 scripts)

High-value tools for everyday development workflows.

**Implementation Plan:** [output/sessions/rickywilson/2025-12-02_code-reviewer-implementation-plan/IMPLEMENTATION_PLAN.md](output/sessions/rickywilson/2025-12-02_code-reviewer-implementation-plan/IMPLEMENTATION_PLAN.md)

| Script | Skill | Implementation Needed |
|--------|-------|----------------------|
| `code_quality_checker.py` | code-reviewer | Static analysis: complexity metrics (cyclomatic, cognitive), code smells detection, maintainability index |
| `pr_analyzer.py` | code-reviewer | PR analysis: diff parsing, change impact assessment, review checklist generation, risk scoring |
| `review_report_generator.py` | code-reviewer | Report generation: findings aggregation, severity categorization, actionable recommendations |

**Path:** `skills/engineering-team/code-reviewer/scripts/`

---

### Priority 2: Architecture Tools (3 scripts)

Critical for system design and technical decisions.

| Script | Skill | Implementation Needed |
|--------|-------|----------------------|
| `architecture_diagram_generator.py` | senior-architect | Mermaid/PlantUML generation from code analysis, dependency graphs, component diagrams |
| `dependency_analyzer.py` | senior-architect | Package.json/requirements.txt parsing, dependency tree visualization, circular dependency detection |
| `project_architect.py` | senior-architect | Project structure analysis, architecture pattern detection (MVC, Clean, Hexagonal) |

**Path:** `skills/engineering-team/senior-architect/scripts/`

---

### Priority 3: Security Tools (6 scripts)

Essential for security posture and compliance.

#### SecOps (3 scripts)

| Script | Skill | Implementation Needed |
|--------|-------|----------------------|
| `compliance_checker.py` | senior-secops | Framework compliance (SOC2, HIPAA, GDPR) checklist validation, gap identification |
| `security_scanner.py` | senior-secops | SAST-lite: secret detection, hardcoded credentials, unsafe patterns, OWASP Top 10 checks |
| `vulnerability_assessor.py` | senior-secops | CVE database integration, dependency vulnerability scanning, risk scoring |

**Path:** `skills/engineering-team/senior-secops/scripts/`

#### Security (3 scripts)

| Script | Skill | Implementation Needed |
|--------|-------|----------------------|
| `pentest_automator.py` | senior-security | Automated security test generation, common vulnerability probes, injection test cases |
| `security_auditor.py` | senior-security | Code audit: authentication/authorization patterns, input validation, encryption usage |
| `threat_modeler.py` | senior-security | STRIDE analysis, attack surface mapping, threat categorization, mitigation recommendations |

**Path:** `skills/engineering-team/senior-security/scripts/`

---

### Priority 4: Backend Tools (3 scripts)

Core API and database development.

| Script | Skill | Implementation Needed |
|--------|-------|----------------------|
| `api_load_tester.py` | senior-backend | HTTP load generation, concurrent request handling, latency percentiles, throughput measurement |
| `api_scaffolder.py` | senior-backend | REST/GraphQL endpoint generation, OpenAPI spec parsing, CRUD boilerplate |
| `database_migration_tool.py` | senior-backend | Schema diff detection, migration file generation, rollback scripts |

**Path:** `skills/engineering-team/senior-backend/scripts/`

---

### Priority 5: DevOps Tools (3 scripts)

CI/CD and infrastructure automation.

| Script | Skill | Implementation Needed |
|--------|-------|----------------------|
| `deployment_manager.py` | senior-devops | Deployment orchestration, environment management, rollback procedures, health checks |
| `terraform_scaffolder.py` | senior-devops | IaC template generation, provider-specific modules (AWS/GCP/Azure), variable management |
| `pipeline_generator.py` | senior-devops | CI/CD YAML generation (GitHub Actions, GitLab CI, Jenkins), stage templates |

**Path:** `skills/engineering-team/senior-devops/scripts/`

---

### Priority 6: Frontend Tools (3 scripts)

UI development and optimization.

| Script | Skill | Implementation Needed |
|--------|-------|----------------------|
| `bundle_analyzer.py` | senior-frontend | Bundle size analysis, tree-shaking recommendations, chunk splitting suggestions |
| `component_generator.py` | senior-frontend | React/Vue/Angular component scaffolding, prop type generation, test stub generation |
| `frontend_scaffolder.py` | senior-frontend | Project initialization templates, routing setup, state management boilerplate |

**Path:** `skills/engineering-team/senior-frontend/scripts/`

---

### Priority 7: Fullstack Tools (3 scripts)

End-to-end development scaffolding.

| Script | Skill | Implementation Needed |
|--------|-------|----------------------|
| `code_quality_analyzer.py` | senior-fullstack | Cross-stack analysis: frontend/backend consistency, API contract validation |
| `fullstack_scaffolder.py` | senior-fullstack | Full application templates: Next.js, Nuxt, SvelteKit with API routes |
| `project_scaffolder.py` | senior-fullstack | Monorepo setup, workspace configuration, shared utilities |

**Path:** `skills/engineering-team/senior-fullstack/scripts/`

---

### Priority 8: QA Tools (3 scripts)

Testing automation and coverage.

| Script | Skill | Implementation Needed |
|--------|-------|----------------------|
| `coverage_analyzer.py` | senior-qa | Coverage report parsing (lcov, cobertura), gap identification, coverage trend analysis |
| `e2e_test_scaffolder.py` | senior-qa | Playwright/Cypress test generation, page object patterns, fixture management |
| `test_suite_generator.py` | senior-qa | Test case generation from requirements, boundary value analysis, test data generation |

**Path:** `skills/engineering-team/senior-qa/scripts/`

---

### Implementation Tracking

- [x] Priority 1: Code Review (3 scripts) ✅ COMPLETED (2,124 lines total)
- [ ] Priority 2: Architecture (3 scripts)
- [ ] Priority 3: Security (6 scripts)
- [ ] Priority 4: Backend (3 scripts)
- [ ] Priority 5: DevOps (3 scripts)
- [ ] Priority 6: Frontend (3 scripts)
- [ ] Priority 7: Fullstack (3 scripts)
- [ ] Priority 8: QA (3 scripts)

### Implementation Guidelines

**Standard Library Only:** All implementations must use Python standard library only (no pip dependencies).

**Reference Implementations:** Use these as examples:
- `sprint_metrics_calculator.py` - Comprehensive calculations, weighted scoring
- `fixture_generator.py` - Boundary value analysis, edge case detection
- `changelog_generator.py` - Git parsing, conventional commit extraction
- `rice_prioritizer.py` - Full RICE calculation, portfolio analysis

### File Paths Reference

```
# Code Reviewer
skills/engineering-team/code-reviewer/scripts/code_quality_checker.py
skills/engineering-team/code-reviewer/scripts/pr_analyzer.py
skills/engineering-team/code-reviewer/scripts/review_report_generator.py

# Senior Architect
skills/engineering-team/senior-architect/scripts/architecture_diagram_generator.py
skills/engineering-team/senior-architect/scripts/dependency_analyzer.py
skills/engineering-team/senior-architect/scripts/project_architect.py

# Senior Backend
skills/engineering-team/senior-backend/scripts/api_load_tester.py
skills/engineering-team/senior-backend/scripts/api_scaffolder.py
skills/engineering-team/senior-backend/scripts/database_migration_tool.py

# Senior DevOps
skills/engineering-team/senior-devops/scripts/deployment_manager.py
skills/engineering-team/senior-devops/scripts/terraform_scaffolder.py
skills/engineering-team/senior-devops/scripts/pipeline_generator.py

# Senior Frontend
skills/engineering-team/senior-frontend/scripts/bundle_analyzer.py
skills/engineering-team/senior-frontend/scripts/component_generator.py
skills/engineering-team/senior-frontend/scripts/frontend_scaffolder.py

# Senior Fullstack
skills/engineering-team/senior-fullstack/scripts/code_quality_analyzer.py
skills/engineering-team/senior-fullstack/scripts/fullstack_scaffolder.py
skills/engineering-team/senior-fullstack/scripts/project_scaffolder.py

# Senior QA
skills/engineering-team/senior-qa/scripts/coverage_analyzer.py
skills/engineering-team/senior-qa/scripts/e2e_test_scaffolder.py
skills/engineering-team/senior-qa/scripts/test_suite_generator.py

# Senior SecOps
skills/engineering-team/senior-secops/scripts/compliance_checker.py
skills/engineering-team/senior-secops/scripts/security_scanner.py
skills/engineering-team/senior-secops/scripts/vulnerability_assessor.py

# Senior Security
skills/engineering-team/senior-security/scripts/pentest_automator.py
skills/engineering-team/senior-security/scripts/security_auditor.py
skills/engineering-team/senior-security/scripts/threat_modeler.py
```

---

## Completed

### CI/CD Auto-Promotion Pipeline
**Type:** Feature
**Effort:** Medium
**Completed:** 2025-12-13
**Description:** GitHub Actions workflows that automatically promote code through the branch workflow when tests pass.

**Acceptance Criteria:**
- [x] Push to develop triggers test suite (`ci-quality-gate.yml`, `quality-gates.yml`)
- [x] If tests pass, auto-merge develop → staging (`auto-promote.yml`)
- [x] If staging checks pass, auto-merge staging → main (`promote-to-main.yml` with optional auto-merge)
- [x] Notifications on promotion success/failure (via GitHub notifications)
- [x] Manual approval gate option for main promotion (default: PR requires approval, optional: auto-merge)

**Configuration:**
- Auto-merge disabled by default (safe)
- Enable via repository variable: `AUTO_MERGE_STAGING_TO_MAIN=true`
- Optional delay: `AUTO_MERGE_DELAY_SECONDS` (default: 60)
- Kill switch: `.github/WORKFLOW_KILLSWITCH` with `AUTO_MERGE: DISABLED`

**Related:** `/commit.changes` command, `docs/WORKFLOW.md`

---

**Last Updated:** 2025-12-13
