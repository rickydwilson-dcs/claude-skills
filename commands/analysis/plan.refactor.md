---
# === CORE IDENTITY ===
name: plan.refactor
title: Code Refactoring Roadmap Generator
description: Analyze code architecture and generate a comprehensive, phased refactoring roadmap with prioritization, effort estimates, and risk assessment

category: plan
subcategory: code-quality

# === WEBSITE DISPLAY ===
difficulty: advanced
# Requires understanding of code architecture, design patterns, and refactoring strategies

time-saved: "45 minutes per session"
# Typical manual refactoring planning takes 1-2 hours, this automates analysis and planning

frequency: "Monthly per engineering team"
# Usually conducted during sprint planning or quarterly reviews

use-cases:
  - "Analyzing legacy codebases to identify architectural debt and create modernization roadmaps"
  - "Planning incremental refactoring phases that minimize disruption to ongoing feature development"
  - "Prioritizing refactoring efforts using business impact, complexity, and technical risk criteria"
  - "Generating detailed refactoring plans with effort estimates, dependencies, and success metrics"
  - "Assessing risks and validating refactoring strategies against team capacity and project timelines"

# === RELATIONSHIPS (Cross-linking) ===
related-agents:
  - cs-engineering-lead
  - cs-code-architect
  - cs-tech-debt-manager
  - cs-quality-lead

related-skills:
  - engineering-team/code-quality-analyzer
  - engineering-team/architecture-reviewer
  - engineering-team/refactoring-guide
  - engineering-team/technical-debt-framework

related-commands:
  - /analysis.code-review
  - /analysis.security-audit
  - /architecture.design-review

# === TECHNICAL ===
dependencies:
  tools:
    - Read
    - Write
    - Bash
    - Grep
    - Glob

  scripts:
    - engineering-team/code-quality-analyzer/scripts/quality_analyzer.py
    - engineering-team/refactoring-guide/scripts/refactor_planner.py
    - engineering-team/refactoring-guide/scripts/effort_estimator.py
    - engineering-team/refactoring-guide/scripts/risk_assessor.py

  python-packages: []
  # Standard library only - maximum portability

compatibility:
  claude-ai: true
  claude-code: true
  platforms:
    - macos
    - linux
    - windows

# === EXAMPLES (Min 2, Max 5) ===
examples:
  - title: "Basic Refactoring Analysis of Single Module"
    input: "/refactor-plan src/payment/processor.ts"
    output: |
      Refactoring Analysis Report: src/payment/processor.ts

      ═════════════════════════════════════════════════════════════════
      TECHNICAL DEBT ASSESSMENT
      ═════════════════════════════════════════════════════════════════

      DEBT SCORE: 7.8/10 (HIGH - Significant refactoring needed)
      MAINTAINABILITY INDEX: 32/100 (Very Poor)
      CYCLOMATIC COMPLEXITY: 12 avg (Target: 6)

      PRIORITY REFACTORING AREAS (5 identified):

      1. Extract Complex Payment Logic (HIGH PRIORITY - 13 story points)
         Current State: 450 LOC monolithic class with 8 responsibilities
         Target: 3-4 focused, single-responsibility classes
         Business Impact: Enables payment method plugins, reduces bugs by ~40%
         Risk Level: MEDIUM (Affects payment flow)
         Timeline: 2 sprints (2 engineers)
         Dependencies: Existing payment tests must pass
         Success Criteria:
           ✓ Reduced cyclomatic complexity to <6 per class
           ✓ 95%+ test coverage maintained
           ✓ No payment processing downtime
           ✓ Plugin architecture functional

      2. Replace Custom Error Handling (MEDIUM - 5 story points)
         Current: Custom exception classes and error codes
         Target: Standardized error framework + retry logic
         Benefit: Consistent error handling across services
         Risk: LOW (Isolated to error paths)
         Timeline: 1 sprint (1 engineer)
         Prerequisites: None

      3. Remove Deprecated Payment Methods (MEDIUM - 3 story points)
         Current: Support for 3 legacy payment processors
         Target: Remove, migrate users to new processors
         Benefit: 200+ LOC reduction, simplified testing
         Risk: LOW if migrations complete first
         Timeline: 2 weeks (1 engineer)
         Prerequisites: User migration complete (in progress)

      4. Implement Dependency Injection (MEDIUM-HIGH - 8 story points)
         Current: Hard-coded database and API dependencies
         Target: IoC container with registered dependencies
         Benefit: Testability, flexibility, reusability
         Risk: MEDIUM (Affects class instantiation throughout codebase)
         Timeline: 3 sprints
         Dependencies: Requires TypeScript upgrade

      5. Standardize Configuration Management (LOW - 2 story points)
         Current: Mix of env vars, config files, and hardcoded values
         Target: Single centralized config system
         Benefit: Consistency, reduces configuration errors
         Risk: LOW
         Timeline: 3-5 days

      ═════════════════════════════════════════════════════════════════
      RECOMMENDED REFACTORING ROADMAP
      ═════════════════════════════════════════════════════════════════

      Phase 1: Foundation (Sprints 1-2, 6 weeks)
      ├─ Remove deprecated payment methods (prerequisite)
      ├─ Standardize configuration (quick win)
      └─ Estimated Capacity: 5 story points
         Team: 1 engineer
         Risk: LOW

      Phase 2: Architecture (Sprints 3-5, 10 weeks)
      ├─ Implement dependency injection
      ├─ Extract complex payment logic
      └─ Estimated Capacity: 21 story points
         Team: 2 engineers (1 lead + 1 junior)
         Risk: MEDIUM (requires pairing)
         Blockers: TypeScript upgrade (1 sprint)

      Phase 3: Stabilization (Sprints 6-7, 6 weeks)
      ├─ Replace custom error handling
      ├─ Comprehensive testing and performance validation
      └─ Estimated Capacity: 5 story points
         Team: 1 engineer
         Risk: LOW

      TOTAL TIMELINE: ~5 months (16 sprints at 2-week sprints)
      TOTAL EFFORT: 31 story points distributed across phases

      ═════════════════════════════════════════════════════════════════
      RISK ASSESSMENT & MITIGATION
      ═════════════════════════════════════════════════════════════════

      CRITICAL RISKS:
      ✗ Payment system downtime during refactoring
        Mitigation: Feature flags, blue-green deployment, thorough staging testing
        Probability: MEDIUM | Impact: HIGH | Overall Risk: HIGH

      ✗ Regression in payment processing
        Mitigation: Contract testing, 100% code coverage, production monitoring
        Probability: MEDIUM | Impact: CRITICAL | Overall Risk: CRITICAL
        Recommended: Hire QA specialist for Phase 2

      MEDIUM RISKS:
      ⚠ Team ramp-up on refactored architecture
        Mitigation: Documentation, pair programming, code reviews
        Probability: HIGH | Impact: MEDIUM | Overall Risk: MEDIUM

      ⚠ TypeScript version conflicts
        Mitigation: Test in staging first, gradual rollout
        Probability: MEDIUM | Impact: MEDIUM | Overall Risk: MEDIUM

      ═════════════════════════════════════════════════════════════════
      BUSINESS CASE
      ═════════════════════════════════════════════════════════════════

      Benefits:
      + 40% reduction in payment-related bugs (estimated)
      + Enables new payment methods (untapped revenue: $500K-1M annually)
      + Improves developer velocity (+15% estimated on payment features)
      + Reduces on-call incidents (currently 2-3 per month from payment)
      + Better knowledge distribution (currently concentrated with 1 engineer)

      Costs:
      - 5 months engineering time (~100 story points)
      - Feature development pause during Phase 2
      - Testing and validation overhead

      ROI: HIGH - Estimated payback within 6 months of completion

      ═════════════════════════════════════════════════════════════════
      IMPLEMENTATION CHECKLIST
      ═════════════════════════════════════════════════════════════════

      Pre-Refactoring:
      ☐ Establish baseline metrics (complexity, test coverage, performance)
      ☐ Set up feature flags for new code paths
      ☐ Prepare blue-green deployment infrastructure
      ☐ Create detailed test plan for payment flows
      ☐ Schedule code review process for Phase 2

      During Refactoring:
      ☐ Track cycle time metrics for refactoring activities
      ☐ Monitor test coverage (maintain >95%)
      ☐ Daily sync with dependent teams
      ☐ Staged rollout to production with monitoring
      ☐ Document decisions and architectural changes

      Post-Refactoring:
      ☐ Validate business metrics (bug reduction, velocity)
      ☐ Gather team feedback on new architecture
      ☐ Update architecture documentation
      ☐ Plan for next debt areas if applicable
      ☐ Celebrate completion!

  - title: "Enterprise Codebase with Portfolio Prioritization"
    input: "/refactor-plan src/ --depth full --capacity 20 --business-impact"
    output: |
      Refactoring Analysis Report: Full Codebase Portfolio

      SUMMARY:
      ─────────────────────────────────────────────────────────────────
      Total Debt Score: 6.2/10 (MODERATE - Multiple Areas Needing Work)
      Files Analyzed: 342
      Modules Assessed: 28
      High Debt Areas: 6
      Medium Debt Areas: 12
      Low Debt Areas: 10

      TOP REFACTORING OPPORTUNITIES (by business impact):
      ─────────────────────────────────────────────────────────────────

      RANK 1: User Service Modernization (HIGH IMPACT)
      Impact Score: 9.2/10
      Effort: 13 story points
      Timeline: 4 weeks (2 engineers)
      Business Value: Enables SSO integration (revenue unlock: $2M+)
      Risk: MEDIUM
      Recommended Phase: Phase 1 (Quarter 1)

      RANK 2: Database Schema Optimization (HIGH IMPACT)
      Impact Score: 8.7/10
      Effort: 21 story points
      Timeline: 8 weeks (3 engineers)
      Business Value: 50% query latency reduction, auto-scaling enabled
      Risk: MEDIUM-HIGH (database schema changes)
      Recommended Phase: Phase 2 (Quarter 2)

      RANK 3: Frontend Component Architecture (MEDIUM IMPACT)
      Impact Score: 7.1/10
      Effort: 16 story points
      Timeline: 6 weeks (2 engineers)
      Business Value: 30% faster page loads, improves conversion rate
      Risk: LOW
      Recommended Phase: Phase 1 (can run parallel to User Service)

      [Full portfolio matrix with all 28 modules...]

      RECOMMENDED PRIORITIZATION STRATEGY:
      ─────────────────────────────────────────────────────────────────
      With 20 story points/month capacity:

      Months 1-2: User Service + Frontend Components (parallel)
      Months 3-4: Database Schema + Error Handling
      Months 5-6: Caching Layer + API Gateway
      Months 7+: Continuous debt reduction

      Expected Outcomes:
      ✓ 50% reduction in performance incidents
      ✓ 35% improvement in developer velocity
      ✓ Enables 3 new revenue features
      ✓ Reduces on-call burden by 40%

  - title: "Risk Assessment with Deployment Strategy"
    input: "/refactor-plan src/api/ --risk-focus --deployment-strategy"
    output: |
      Refactoring Risk Analysis: src/api/

      RISK ASSESSMENT MATRIX:
      ─────────────────────────────────────────────────────────────────

      By Severity & Likelihood:

      CRITICAL (Stop / Heavy Mitigation Required):
      ✗ API contract breaking changes (Probability: HIGH, Impact: CRITICAL)
        Areas: Request/response models, authentication flow
        Mitigation: Contract testing, version negotiation, gradual rollout
        Deployment: Canary with 5% traffic initially, 100% on validation

      HIGH (Requires Careful Planning):
      ⚠ Database query performance regression (Probability: MEDIUM, Impact: HIGH)
        Areas: ORM query optimization, index changes
        Mitigation: Load testing, query plan analysis, rollback plan
        Deployment: Blue-green with extended warm-up period

      MEDIUM (Standard Approach):
      ⚠ Internal refactoring side effects (Probability: MEDIUM, Impact: MEDIUM)
        Areas: Dependency extraction, test infrastructure changes
        Mitigation: Comprehensive unit & integration testing, code review
        Deployment: Feature flags for gradual rollout

      RECOMMENDED DEPLOYMENT STRATEGY:
      ─────────────────────────────────────────────────────────────────

      Phase 1: Feature Flagged Implementation
      └─ All new code deployed with kill switch
      └─ 2 weeks validation in production
      └─ Automatic rollback if issues detected

      Phase 2: Canary Deployment
      ├─ 5% traffic → 25% traffic → 50% traffic → 100%
      ├─ 24 hours between each stage
      ├─ Real-time monitoring at each stage
      └─ Auto-rollback on SLO violations

      Phase 3: Cleanup & Optimization
      └─ Remove old code paths
      └─ Clean up feature flags
      └─ Document decisions

      Production Monitoring Requirements:
      • API latency (p50/p95/p99)
      • Error rates by endpoint
      • Database query performance
      • Memory usage trends
      • Cache hit rates

      Rollback Checklist:
      ☐ Automated rollback capability tested
      ☐ Data migration reversible
      ☐ Cache invalidation plan
      ☐ Stakeholders notified
      ☐ Post-incident review template ready

# === ANALYTICS (Placeholder for future) ===
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors:
  - Engineering Leadership
  - Technical Debt Review Committee

created: 2025-11-24
updated: 2025-11-24

# === DISCOVERABILITY ===
tags:
  - refactoring
  - code-architecture
  - technical-debt
  - roadmap-planning
  - engineering-strategy
  - code-quality
  - legacy-modernization
  - effort-estimation

featured: false
verified: true
license: MIT

---

# Code Refactoring Roadmap Generator

## Purpose

This command analyzes your codebase for architectural issues, technical debt, and design problems, then generates a comprehensive, phased refactoring roadmap. It prioritizes refactoring efforts by business impact, complexity, and risk, providing detailed effort estimates, dependency analysis, and implementation strategies.

Perfect for:
- Legacy codebase modernization
- Technical debt management
- Architecture evolution planning
- Team capacity and sprint planning
- Risk-aware refactoring strategies

---

## Pattern Type: Multi-Phase (Discovery → Analysis → Task)

**Complexity:** High
**Execution Time:** 5-15 minutes (varies by codebase size)
**Destructive:** No (analysis only, no code modifications)

---

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Comprehensively scan the codebase to identify architectural debt, code complexity issues, and design problems

**Steps:**
1. Scan all source files for code metrics (complexity, duplication, dependencies)
2. Identify architectural anti-patterns (tight coupling, circular dependencies, god classes)
3. Detect code smell indicators (long methods, large classes, feature envy)
4. Catalog test coverage gaps and missing test categories
5. Map module dependencies and identify problematic patterns
6. Assess technology debt (outdated frameworks, security issues, performance bottlenecks)

**Tools Used:** Glob (file discovery), Grep (pattern matching), Read (code analysis)

### Phase 2: Analysis

**Goal:** Process findings and identify prioritized refactoring opportunities with business impact

**Steps:**
1. Calculate code metrics (cyclomatic complexity, maintainability index, coupling metrics)
2. Prioritize issues by severity, effort, and business impact
3. Group related issues into refactoring units
4. Estimate effort for each refactoring (story points)
5. Assess risks and dependencies between refactoring areas
6. Calculate timeline based on team capacity
7. Generate risk mitigation strategies

**Analysis Criteria:**
- **Code Quality Metrics** - Complexity, duplication, test coverage gaps
- **Architectural Issues** - Coupling, cohesion, scalability concerns
- **Business Impact** - Revenue unlock, user experience, reliability improvements
- **Implementation Risk** - Complexity, dependencies, required expertise
- **Team Capacity** - Available engineers, skill levels, sprint commitments

### Phase 3: Task Execution

**Goal:** Create actionable refactoring plan with prioritized phases

**Steps:**
1. Organize refactoring efforts into logical phases (4-12 week chunks)
2. Define phase dependencies and prerequisite work
3. Calculate resource requirements per phase
4. Create detailed task breakdown
5. Document deployment strategy and rollback plans
6. Establish success criteria and metrics
7. Generate implementation checklist

**Actions:**
- **Phase Planning** - Organize work into meaningful, shippable phases
- **Effort Estimation** - Detailed story point breakdown per phase
- **Risk Assessment** - Identify critical risks and mitigation strategies
- **Rollout Strategy** - Deployment approach (feature flags, blue-green, canary)
- **Monitoring Plan** - Metrics to track during and after refactoring

### Phase 4: Reporting

**Goal:** Present findings, prioritized roadmap, and implementation strategy

**Report Includes:**
- Technical debt assessment with severity scores
- Detailed refactoring opportunities with effort estimates
- Prioritized roadmap with recommended phases
- Risk assessment and mitigation strategies
- Business case with benefits and ROI
- Implementation checklist and success criteria
- Deployment strategy with monitoring plan

**Report Location:** Saved as `.md` file in current directory or specified output path

---

## Usage

```bash
/refactor-plan path [options]
```

### Basic Analysis of Single Module

```bash
# Example 1: Quick analysis of a single file
/refactor-plan src/payment/processor.ts
```

Analyzes a single file or module for refactoring opportunities and generates recommended improvements.

### Full Codebase Analysis with Portfolio Prioritization

```bash
# Example 2: Full codebase analysis with business prioritization
/refactor-plan src/ --depth full --capacity 20 --business-impact
```

Analyzes entire codebase, prioritizes by business impact, and adjusts roadmap based on team capacity (20 story points/month).

### Risk-Focused Assessment with Deployment Strategy

```bash
# Example 3: Risk-focused analysis for critical systems
/refactor-plan src/api/ --risk-focus --deployment-strategy
```

Emphasizes risk analysis and provides detailed deployment approach (feature flags, blue-green, canary deployment).

### Generate JSON Output for Tool Integration

```bash
# Example 4: JSON output for automation and tool integration
/refactor-plan src/ --format json > refactor-plan.json
```

Outputs structured JSON data for integration with project management tools, dashboards, or automation.

### Arguments

- `path` - Directory or file path to analyze (required)
- `--depth` - Analysis depth: `basic` (quick scan), `standard` (detailed), or `full` (comprehensive with dependencies) (default: standard)
- `--capacity` - Team capacity in story points per month (optional, enables timeline calculation)
- `--business-impact` - Prioritize by business impact rather than technical debt severity (optional)
- `--risk-focus` - Emphasize risk assessment and mitigation strategies (optional)
- `--deployment-strategy` - Include detailed deployment approach and rollback plans (optional)
- `--format` - Output format: `markdown` (default), `json`, or `text`
- `--timeline` - Include estimated timeline with sprint allocation (optional)
- `--tech-stack` - Specify technology stack for context-specific recommendations (optional)

### Examples

The command supports multiple usage scenarios:

```bash
# Basic example: Quick analysis of a service module
/refactor-plan src/services/user-service
```

This runs a quick scan of the user service module, identifying key refactoring opportunities and effort estimates.

```bash
# Advanced example: Full codebase analysis with business prioritization
/refactor-plan . --depth full --business-impact --capacity 20
```

Analyzes the entire codebase, prioritizes opportunities by business impact rather than technical debt alone, and adjusts timeline to match 20 story points per month team capacity.

```bash
# Risk-focused example: Critical payment system analysis
/refactor-plan src/payment --risk-focus --deployment-strategy
```

Performs deep risk assessment on the payment system and provides specific deployment strategies (feature flags, blue-green, canary) to minimize production risk.

```bash
# JSON export example: Generate roadmap for architecture review
/refactor-plan . --depth full --timeline --format json > roadmap.json
```

Generates a comprehensive refactoring plan with timeline and exports as JSON for integration with project management tools and architecture review workflows.

---

## What This Command Does

### Context Gathering

The command will:
1. Scan source files in target directory/file
2. Analyze code metrics (complexity, duplication, dependencies)
3. Identify architectural patterns and anti-patterns
4. Assess test coverage and validation gaps
5. Review technology and dependency versions
6. Check for security and performance concerns

### Analysis Process

The command:
1. Calculates code quality scores across multiple dimensions
2. Prioritizes findings by impact, effort, and business value
3. Groups related issues into refactoring units
4. Estimates effort using complexity scoring
5. Assesses risks and interdependencies
6. Generates timeline based on capacity
7. Develops deployment and rollback strategies

### Expected Output

You will receive:
- **Executive Summary** - Debt scores, key metrics, top opportunities
- **Detailed Refactoring Opportunities** - Each with effort, timeline, risk, and business case
- **Prioritized Roadmap** - Phased approach with resource requirements
- **Risk Assessment** - Critical/high/medium risks with mitigation strategies
- **Implementation Plan** - Phase-by-phase breakdown with success criteria
- **Deployment Strategy** - Specific approach for production safety
- **Business Case** - Benefits, costs, and ROI analysis

**Output Location:** `refactor-plan.md` (or specified path)
**Output Format:** Markdown (human-readable), JSON (structured data), or text (plain)

---

## Multi-Phase Refactoring Strategy

### Phase Composition

Each phase is designed as:
- **Duration:** 2-8 weeks (adjustable)
- **Effort:** 5-20 story points (based on team)
- **Team:** 1-3 engineers (depends on complexity)
- **Risk Level:** Defined and mitigated
- **Success Metrics:** Clear acceptance criteria

### Phase Dependencies

Phases are ordered to:
1. **Build Foundation** - Create prerequisites for complex work
2. **Reduce Risks** - Address critical risks early
3. **Enable Features** - Complete work that unblocks new capabilities
4. **Optimize & Stabilize** - Polish and performance tuning

### Capacity Planning

The roadmap accounts for:
- Team size and skill levels
- Parallel vs. sequential work
- Buffer time for unknowns
- Ongoing feature development
- Operational overhead (on-call, meetings)

---

## Prioritization Criteria

The command prioritizes refactoring opportunities using:

### Primary Criteria
- **Business Impact** - Revenue unlock, user experience, reliability
- **Technical Risk** - Complexity, criticality, dependencies
- **Effort Required** - Complexity score, implementation difficulty
- **Time to Value** - Quick wins vs. strategic investments

### Secondary Criteria
- **Team Expertise** - Skills required vs. available
- **Dependency Analysis** - Prerequisite work identification
- **Risk Exposure** - Critical system impact assessment
- **Opportunity Cost** - Impact on feature development velocity

### Weighting

Impact weights vary based on context:
- **Risk-Focused:** Minimize risk, then maximize business value
- **Business-Focused:** Maximize ROI, then minimize effort
- **Velocity-Focused:** Maximize development speed, prioritize bottlenecks

---

## Risk Management

### Risk Categories

**Critical:** Stop work, implement heavy mitigation, may require external help
**High:** Requires careful planning, mitigation required, staged rollout
**Medium:** Standard approach, thorough testing, code review focus
**Low:** Standard procedures apply

### Mitigation Strategies

**Code Changes:**
- Feature flags (kill switch capability)
- Contract testing (maintain API compatibility)
- Canary deployments (gradual rollout)
- Blue-green deployments (zero-downtime)

**Data Changes:**
- Backup and recovery procedures
- Data validation and rollback checks
- Dual-write periods (old + new systems)

**Dependency Management:**
- Service mocking for testing
- Gradual API version migration
- Compatibility shims and adapters

---

## Success Criteria

This command is successful when:

- [ ] Refactoring priorities align with team and business goals
- [ ] Effort estimates are defensible with detailed breakdown
- [ ] Timeline accounts for team capacity and constraints
- [ ] Risk assessment identifies and mitigates critical concerns
- [ ] Deployment strategy minimizes production impact
- [ ] Success metrics are measurable and tracked
- [ ] Implementation plan is actionable and phase-gated
- [ ] Stakeholders understand business case and ROI

### Quality Metrics

**Expected Outcomes:**
- **Debt Reduction:** 30-50% decrease in technical debt score over 6 months
- **Velocity Improvement:** 15-25% increase in development speed post-refactoring
- **Quality Gains:** 40-60% reduction in defect rates
- **Reliability:** 50%+ reduction in outages related to debt areas
- **Timeline Accuracy:** 80%+ of actual effort within estimated range

---

## Error Handling

### Common Issues

**Issue:** Command takes longer than expected on large codebase
**Cause:** Full analysis of 1000+ files with complex dependencies
**Solution:** Use `--depth basic` for initial scan, then `--depth full` on specific modules
**Prevention:** Run on specific areas first, expand scope gradually

---

**Issue:** Effort estimates seem too high/low
**Cause:** Estimation uses complexity metrics that may not match team's actual velocity
**Solution:** Adjust capacity parameter to match team's actual story point velocity
**Prevention:** Calibrate with 2-3 completed refactoring projects

---

**Issue:** Roadmap doesn't match team constraints
**Cause:** Recommended phases exceed available capacity
**Solution:** Extend timeline with `--capacity` flag or reduce scope per phase
**Prevention:** Specify capacity flag from the start

---

### Validation Failures

If the command reports validation errors:

1. **Path Not Found**
   - Check: File/directory path is correct
   - Fix: Use absolute path or verify relative path from current directory

2. **Insufficient Code to Analyze**
   - Check: Directory contains valid source files (.js, .ts, .py, .go, etc.)
   - Fix: Ensure target is a code directory, not config/assets

3. **Unsupported Technology**
   - Check: Your technology is in the supported list
   - Fix: Use `--tech-stack` parameter for context, or contact team

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-engineering-lead](../../agents/engineering/cs-engineering-lead.md)** - Approves refactoring strategy and allocates team resources
- **[cs-code-architect](../../agents/engineering/cs-code-architect.md)** - Designs refactoring approach and architecture decisions
- **[cs-tech-debt-manager](../../agents/engineering/cs-tech-debt-manager.md)** - Tracks technical debt and prioritizes paydown efforts
- **[cs-quality-lead](../../agents/engineering/cs-quality-lead.md)** - Ensures quality standards maintained during refactoring

### Related Skills

This command leverages:

- **[code-quality-analyzer](../../skills/engineering-team/code-quality-analyzer/)** - Core code metrics and analysis
- **[architecture-reviewer](../../skills/engineering-team/architecture-reviewer/)** - Architectural pattern detection
- **[refactoring-guide](../../skills/engineering-team/refactoring-guide/)** - Specific refactoring strategies and best practices
- **[technical-debt-framework](../../skills/engineering-team/technical-debt-framework/)** - Debt prioritization and ROI calculation

### Python Tools

This command may execute:

```bash
# Core analysis
python skills/engineering-team/code-quality-analyzer/scripts/quality_analyzer.py src/

# Refactoring planning
python skills/engineering-team/refactoring-guide/scripts/refactor_planner.py analysis.json

# Effort estimation
python skills/engineering-team/refactoring-guide/scripts/effort_estimator.py plan.json

# Risk assessment
python skills/engineering-team/refactoring-guide/scripts/risk_assessor.py refactoring-items.json
```

---

## Tips for Best Results

### 1. **Start with Risk Assessment**
   - Run with `--risk-focus` first to understand critical concerns
   - Address critical/high risks before starting refactoring
   - Why: Prevents costly failures and stakeholder concerns

### 2. **Engage Stakeholders Early**
   - Share business case before committing to timeline
   - Get buy-in on prioritization and capacity allocation
   - Why: Ensures alignment and prevents scope creep

### 3. **Phase Work Incrementally**
   - 4-8 week phases are optimal (not too long, visibility is good)
   - Complete at least Phase 1 to validate approach
   - Why: Allows course correction and builds team confidence

### 4. **Include Buffer Time**
   - Add 20-30% buffer for unknowns and integration issues
   - Plan operational work (reviews, testing, deployment)
   - Why: Realistic timelines increase stakeholder trust

### 5. **Monitor Progress Closely**
   - Track actual vs. estimated effort per phase
   - Adjust future phases based on learnings
   - Why: Improves estimation for future refactoring

### 6. **Capture Decisions**
   - Document architecture decisions made during refactoring
   - Record what worked and what didn't
   - Why: Prevents repeating same mistakes in future

---

## Related Commands

- `/analysis.code-review` - In-depth code quality assessment for PRs and modules
- `/analysis.security-audit` - Security-focused code analysis and vulnerability detection
- `/architecture.design-review` - Architecture and design pattern evaluation

---

## References

- [Code Quality Analyzer Guide](../../skills/engineering-team/code-quality-analyzer/SKILL.md) - Deep dive on metrics and analysis
- [Refactoring Guide](../../skills/engineering-team/refactoring-guide/SKILL.md) - Specific refactoring patterns and strategies
- [Technical Debt Framework](../../skills/engineering-team/technical-debt-framework/SKILL.md) - Debt prioritization methodology
- [Architecture Best Practices](../../skills/engineering-team/architecture-reviewer/references/architecture-patterns.md) - Design patterns and anti-patterns

---

**Last Updated:** November 24, 2025
**Version:** v1.0.0
**Status:** Production Ready
**Maintained By:** Claude Skills Team
**Feedback:** Submit issues or feature requests to the Claude Skills repository

