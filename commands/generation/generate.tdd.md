---
# === CORE IDENTITY ===
name: generate.tdd
title: TDD Red-Green-Refactor Cycle Guidance
description: Guide developers through Test-Driven Development cycles with test specification generation, fixture creation, and phase-by-phase workflow orchestration

category: generate
subcategory: testing

# === WEBSITE DISPLAY ===
difficulty: advanced
# Requires understanding of TDD methodology, test frameworks, and iterative development

time-saved: "4-6 hours per feature"
# Manual TDD without guidance takes 8-10 hours per feature, this saves 4-6 hours through automated spec generation and phase guidance

frequency: "Per feature implementation"
# Teams use TDD workflow once per feature during development

use-cases:
  - "Generate Given-When-Then test specifications from feature requirements"
  - "Guide Red-Green-Refactor cycles with phase-specific checklists and tips"
  - "Create comprehensive test fixtures with boundary values and edge cases"
  - "Detect test framework and configure TDD workflow for project"
  - "Analyze refactoring safety before REFACTOR phase"
  - "Track TDD cycle metrics for continuous improvement"

# === RELATIONSHIPS (Cross-linking) ===
related-agents:
  - cs-tdd-engineer
  - cs-qa-engineer
  - cs-fullstack-engineer

related-skills:
  - engineering-team/senior-qa

related-commands:
  - /generate.tests
  - /review.code

# === TECHNICAL ===
dependencies:
  tools:
    - Read
    - Write
    - Bash
    - Grep
    - Glob

  scripts:
    - engineering-team/senior-qa/scripts/tdd_workflow.py
    - engineering-team/senior-qa/scripts/test_spec_generator.py
    - engineering-team/senior-qa/scripts/fixture_generator.py
    - engineering-team/senior-qa/scripts/format_detector.py
    - engineering-team/senior-qa/scripts/refactor_analyzer.py

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
  - title: "TDD Cycle for User Authentication Feature"
    input: "/generate.tdd \"User can login with email and password\" --framework jest"
    output: |
      TDD Workflow: User Authentication Feature

      FRAMEWORK DETECTION
      ════════════════════════════════════════════════════════════════
      Framework: Jest (detected from package.json)
      Coverage Format: Istanbul/NYC
      Language: TypeScript
      Confidence: 95%

      REQUIREMENT ANALYSIS
      ════════════════════════════════════════════════════════════════
      Requirement: "User can login with email and password"
      Subject: user
      Action: login
      Conditions: email and password provided

      GENERATED TEST SPECIFICATIONS (7 specs)
      ════════════════════════════════════════════════════════════════

      Happy Path Tests:
      ✓ Spec 1: should login successfully with valid credentials
        GIVEN: user has valid email and password
        WHEN: login is invoked
        THEN: returns authenticated user object
        Priority: HIGH

      Input Validation Tests:
      ✓ Spec 2: should reject empty email
        GIVEN: empty email is provided
        WHEN: attempting to login
        THEN: validation error is returned
        Priority: HIGH

      ✓ Spec 3: should reject invalid email format
        GIVEN: email without @ symbol is provided
        WHEN: attempting to login
        THEN: validation error is returned
        Priority: HIGH

      ✓ Spec 4: should handle null password gracefully
        GIVEN: null/undefined password is provided
        WHEN: attempting to login
        THEN: appropriate error handling occurs
        Priority: HIGH

      Authentication Tests:
      ✓ Spec 5: should deny access for unauthenticated user
        GIVEN: user is not authenticated
        WHEN: attempting to login
        THEN: 401 Unauthorized is returned
        Priority: HIGH

      Edge Case Tests:
      ✓ Spec 6: should handle resource not found
        GIVEN: the requested resource does not exist
        WHEN: attempting to login
        THEN: 404 Not Found is returned
        Priority: MEDIUM

      ✓ Spec 7: should handle boundary values
        GIVEN: input is at boundary (min/max/zero)
        WHEN: attempting to login
        THEN: boundary is handled correctly
        Priority: MEDIUM

      GENERATED FIXTURES
      ════════════════════════════════════════════════════════════════
      Email Fixtures:
        - valid: "user@example.com"
        - valid_subdomain: "user@mail.example.com"
        - valid_plus: "user+tag@example.com"
        - invalid_no_at: "userexample.com"
        - invalid_spaces: "user @example.com"
        - xss: "<script>alert('xss')</script>"
        - sql_injection: "'; DROP TABLE users; --"

      🔴 RED PHASE - Write Failing Tests
      ════════════════════════════════════════════════════════════════

      Checklist:
      [ ] Test describes expected behavior clearly
      [ ] Test fails for the right reason (not syntax error)
      [ ] Test is focused on one behavior
      [ ] Test uses descriptive naming (should_X_when_Y)

      Generated Test File: src/auth/__tests__/login.test.ts

      ```typescript
      // Auto-generated test specifications
      // Framework: Jest

      describe('Feature: User Login', () => {
        beforeEach(() => {
          // Setup test fixtures
        });

        afterEach(() => {
          // Cleanup
        });

        describe('happy_path', () => {
          it('should login successfully with valid credentials', () => {
            // GIVEN: user has valid email and password
            // TODO: Setup preconditions

            // WHEN: login is invoked
            // TODO: Execute action

            // THEN: returns authenticated user object
            // TODO: Assert expectations
            expect(true).toBe(false); // RED phase - implement me
          });
        });

        describe('input_validation', () => {
          it('should reject empty email', () => {
            // GIVEN: empty input is provided
            // WHEN: attempting to login
            // THEN: a validation error is returned
            expect(true).toBe(false); // RED phase - implement me
          });

          it('should handle null input gracefully', () => {
            // GIVEN: null/undefined input is provided
            // WHEN: attempting to login
            // THEN: appropriate error handling occurs
            expect(true).toBe(false); // RED phase - implement me
          });
        });
      });
      ```

      NEXT STEPS
      ════════════════════════════════════════════════════════════════
      1. Copy test file to src/auth/__tests__/login.test.ts
      2. Run tests: npm test -- --testPathPattern=login.test.ts
      3. Verify tests FAIL for right reason (no implementation)
      4. Write minimal implementation code (GREEN phase)
      5. Run: /generate.tdd --phase green to get GREEN guidance

      Report generated in 2.1s
      Generated by: TDD Workflow v1.0.0

  - title: "TDD GREEN Phase Guidance"
    input: "/generate.tdd --phase green --test-file src/auth/__tests__/login.test.ts"
    output: |
      TDD Workflow: GREEN Phase

      🟢 GREEN PHASE - Make Tests Pass
      ════════════════════════════════════════════════════════════════

      Test File: src/auth/__tests__/login.test.ts
      Tests: 7 specs
      Status: 7 failing → make them pass

      Checklist:
      [✓] All tests pass
      [ ] Implementation is minimal (no extra features)
      [ ] No premature optimization
      [ ] Code compiles/runs without errors

      GUIDANCE
      ════════════════════════════════════════════════════════════════

      💡 Write Minimal Code
         Write just enough code to make the test pass
         Example:
         ```typescript
         // Minimal implementation
         function validateEmail(email: string): boolean {
           return email.includes('@');  // Simple first pass
         }
         ```

      💡 Avoid Premature Optimization
         Focus on making the test pass, not perfect code
         Tip: You can improve the code in the REFACTOR phase

      💡 Run Tests Frequently
         Run tests after each small change
         Command: npm test -- --watch

      IMPLEMENTATION TEMPLATE
      ════════════════════════════════════════════════════════════════
      ```typescript
      // src/auth/login.ts - Minimal implementation

      export interface LoginResult {
        userId: string;
        email: string;
        token: string;
      }

      export async function login(email: string, password: string): Promise<LoginResult> {
        // Minimal implementation - just pass the tests
        if (!email || !email.includes('@')) {
          throw new Error('Invalid email format');
        }

        if (!password) {
          throw new Error('Password required');
        }

        // Return minimal valid response
        return {
          userId: '1',
          email: email,
          token: 'token'
        };
      }
      ```

      NEXT STEPS
      ════════════════════════════════════════════════════════════════
      1. Implement minimal code following template
      2. Run tests: npm test -- --testPathPattern=login.test.ts
      3. Verify all tests PASS
      4. Run: /generate.tdd --phase refactor to get REFACTOR guidance

      Report generated in 0.8s
      Generated by: TDD Workflow v1.0.0

  - title: "TDD REFACTOR Phase with Safety Analysis"
    input: "/generate.tdd --phase refactor --input src/auth"
    output: |
      TDD Workflow: REFACTOR Phase

      🔵 REFACTOR PHASE - Improve the Design
      ════════════════════════════════════════════════════════════════

      REFACTORING SAFETY ANALYSIS
      ════════════════════════════════════════════════════════════════

      📊 Analysis Overview:
         Files Analyzed: 3
         Code Smells Found: 2
         Refactoring Suggestions: 4

      ✅ Refactoring Readiness: READY
         Safety Score: high

      🔒 Safety Checks:
         ✅ test_files_exist: Found 3 test files
         ✅ coverage_reports: Coverage reports found
         ✅ ci_configuration: CI pipeline configured

      🔍 Code Smells Detected (2):
         - [MEDIUM] src/auth/login.ts: high_complexity
           Detail: 8 conditionals, 3 loops
           Suggestion: Break down into smaller, focused functions

         - [LOW] src/auth/login.ts: too_many_functions
           Detail: 12 functions
           Suggestion: Consider splitting related functions into separate modules

      💡 Refactoring Suggestions:
         1. [HIGH] extract_method: Extract validation logic
            Steps: Identify nested block → Extract to new method → Replace with call → Run tests

         2. [MEDIUM] simplify_conditional: Simplify complex conditions
            Steps: Identify complex conditions → Extract to boolean methods → Use early returns → Run tests

         3. [LOW] improve_naming: Review variable names
            Steps: Scan for unclear names → Rename using domain language → Update references → Run tests

      REFACTOR CHECKLIST
      ════════════════════════════════════════════════════════════════
      [ ] All tests still pass after each change
      [ ] Code is more readable
      [ ] Duplication is reduced
      [ ] Names are meaningful
      [ ] No behavior changes introduced

      SAFE REFACTORING TECHNIQUES
      ════════════════════════════════════════════════════════════════

      1. Extract Method
         - Move validation logic to validateCredentials()
         - Move token generation to generateToken()

      2. Rename for Clarity
         - 'pwd' → 'password'
         - 'u' → 'user'

      3. Remove Duplication
         - Extract common error handling
         - Consolidate validation checks

      REFACTORED CODE EXAMPLE
      ════════════════════════════════════════════════════════════════
      ```typescript
      // src/auth/login.ts - Refactored

      const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

      function validateEmail(email: string): void {
        if (!email || !EMAIL_REGEX.test(email)) {
          throw new ValidationError('Invalid email format');
        }
      }

      function validatePassword(password: string): void {
        if (!password || password.length < 8) {
          throw new ValidationError('Password must be at least 8 characters');
        }
      }

      export async function login(email: string, password: string): Promise<LoginResult> {
        validateEmail(email);
        validatePassword(password);

        const user = await findUserByEmail(email);
        await verifyPassword(password, user.passwordHash);

        return createLoginResult(user);
      }
      ```

      GOLDEN RULE
      ════════════════════════════════════════════════════════════════
      Run tests after EVERY change. If tests fail, revert immediately!

      Command: npm test -- --watch

      NEXT STEPS
      ════════════════════════════════════════════════════════════════
      1. Apply refactoring suggestions one at a time
      2. Run tests after EACH change
      3. If tests fail, revert immediately
      4. When complete, run: npm test -- --coverage
      5. Start next feature with: /generate.tdd "New feature requirement"

      Report generated in 1.5s
      Generated by: TDD Workflow v1.0.0

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
  - QA Team
  - Engineering Team
created: 2025-11-28
updated: 2025-11-28

# === DISCOVERABILITY ===
tags:
  - tdd
  - test-driven-development
  - red-green-refactor
  - test-generation
  - test-specs
  - fixtures
  - given-when-then
  - bdd
  - quality-assurance
  - testing

featured: false
verified: true
license: MIT

---

# Generate TDD

Guide developers through Test-Driven Development Red-Green-Refactor cycles with automated test specification generation, fixture creation, framework detection, and phase-by-phase workflow orchestration.

---

## Pattern Type: Multi-Phase

**Complexity:** Medium-High
**Execution Time:** 2-10 minutes depending on requirement complexity
**Destructive:** No (generates files but doesn't modify existing code unless explicitly requested)

---

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Detect test framework and analyze project configuration for TDD setup

**Steps:**
1. Scan project for test framework configuration (package.json, pyproject.toml, etc.)
2. Detect test framework (Jest, Vitest, Mocha, Pytest, JUnit, RSpec)
3. Identify coverage format (Istanbul, LCOV, Cobertura, JaCoCo)
4. Detect primary programming language
5. Find existing test patterns and conventions
6. Identify test file locations and naming patterns

**Tools Used:** Glob, Read, Bash (for format_detector.py)

**Output:** Framework configuration, coverage tools, language detection, recommendations

**Example Command:**
```bash
python3 skills/engineering-team/senior-qa/scripts/format_detector.py --input . --output json
```

### Phase 2: Analysis (RED Phase)

**Goal:** Parse requirement and generate comprehensive test specifications

**Analysis Dimensions:**

1. **Requirement Parsing**
   - Extract subject (user, system, service)
   - Extract action verb (create, validate, process)
   - Identify conditions (when, if, given)
   - Extract expected outcomes (should, must, will)

2. **Test Specification Generation**
   - Happy path scenarios
   - Input validation cases
   - Authentication/authorization cases
   - Error handling scenarios
   - Edge cases and boundaries

3. **Fixture Generation**
   - Boundary values (min, max, zero)
   - Invalid inputs (null, empty, malformed)
   - Security test data (XSS, SQL injection)
   - Factory patterns for entities

4. **Priority Assignment**
   - HIGH: Core functionality, security
   - MEDIUM: Error handling, edge cases
   - LOW: Performance, accessibility

**Example Commands:**
```bash
python3 skills/engineering-team/senior-qa/scripts/test_spec_generator.py \
  --input . \
  --requirement "User can login with email" \
  --framework jest \
  --output template

python3 skills/engineering-team/senior-qa/scripts/fixture_generator.py \
  --input . \
  --type email \
  --output json
```

### Phase 3: Task Execution (GREEN Phase)

**Goal:** Guide implementation of minimal code to pass tests

**Actions:**

1. **TDD Workflow Guidance**
   - Display GREEN phase checklist
   - Provide minimal implementation tips
   - Show "fake it till you make it" patterns
   - Emphasize avoiding premature optimization

2. **Implementation Templates**
   - Provide skeletal implementation code
   - Show minimal patterns for passing tests
   - Demonstrate incremental implementation

3. **Test Execution Guidance**
   - Commands to run tests
   - Watch mode for continuous feedback
   - Coverage verification commands

**Example Command:**
```bash
python3 skills/engineering-team/senior-qa/scripts/tdd_workflow.py \
  --input . \
  --phase green \
  --test-file tests/test_login.py
```

### Phase 4: Task Execution (REFACTOR Phase)

**Goal:** Analyze code for safe refactoring and provide improvement suggestions

**Actions:**

1. **Safety Analysis**
   - Check test coverage exists
   - Verify CI/CD pipeline configured
   - Analyze code smell density
   - Calculate safety score

2. **Refactoring Suggestions**
   - Extract method opportunities
   - Rename for clarity
   - Remove duplication
   - Simplify conditionals

3. **Guided Refactoring**
   - Step-by-step instructions
   - Test verification commands
   - Revert guidance if tests fail

**Example Command:**
```bash
python3 skills/engineering-team/senior-qa/scripts/refactor_analyzer.py \
  --input ./src \
  --output json \
  --verbose
```

### Phase 5: Reporting

**Goal:** Present TDD guidance in clear, actionable format

**Report Includes:**

1. **Framework Detection**
   - Detected test framework
   - Coverage format
   - Confidence level
   - Configuration recommendations

2. **Test Specifications**
   - Given-When-Then specs
   - Priority levels
   - Category groupings
   - Framework-specific code templates

3. **Fixtures**
   - Boundary value fixtures
   - Edge case data
   - Security test patterns
   - Factory examples

4. **Phase Guidance**
   - Current phase checklist
   - Best practice tips
   - Anti-patterns to avoid
   - Next steps

5. **Metrics**
   - Cycle tracking
   - Coverage targets
   - Safety scores
   - Improvement recommendations

---

## Arguments

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `requirement` | Conditional | Feature requirement to generate specs from | None |
| `--phase` | No | TDD phase (red, green, refactor) | red |
| `--framework` | No | Test framework (jest, pytest, vitest, mocha) | auto-detect |
| `--input` | No | Project directory to analyze | . |
| `--test-file` | No | Specific test file for phase guidance | None |
| `--output` | No | Output format (text, json, template) | text |

---

## Usage Examples

### Basic Usage

```bash
# Generate TDD workflow for new feature
/generate.tdd "Add email validation function"

# Specify test framework
/generate.tdd "User registration" --framework pytest

# Get GREEN phase guidance
/generate.tdd --phase green --test-file tests/test_auth.py

# Get REFACTOR phase analysis
/generate.tdd --phase refactor --input src/auth

# Detect framework only
/generate.tdd --detect-framework
```

### Advanced Usage

```bash
# Generate with specific output format
/generate.tdd "API endpoint validation" --framework jest --output template

# Full TDD cycle with file output
/generate.tdd "Payment processing" --framework jest --output json --file tdd-specs.json

# Refactor analysis with verbose output
/generate.tdd --phase refactor --input ./src --verbose
```

---

## Integration with Related Commands

### /generate.tdd vs /generate.tests

| Aspect | /generate.tdd | /generate.tests |
|--------|---------------|-----------------|
| **Approach** | Test-first (requirements → tests → code) | Test-after (code → tests) |
| **Input** | Feature requirements | Existing code |
| **Primary Use** | New feature development | Adding tests to existing code |
| **Output** | Failing test specs + workflow guidance | Passing tests for existing code |
| **Methodology** | TDD Red-Green-Refactor | Traditional testing |

**Complementary Usage:**
1. Use `/generate.tdd` for new features (test-first)
2. Use `/generate.tests` for legacy code (test-after)
3. Both produce comprehensive test coverage

---

## TDD Best Practices Embedded

This command embeds TDD best practices from `references/tdd_methodology.md`:

### RED Phase
- Write test before implementation
- Test should fail for right reason (not syntax)
- One behavior per test
- Descriptive test names (should_X_when_Y)

### GREEN Phase
- Write minimal code to pass
- "Fake it till you make it" is OK
- No premature optimization
- Run tests after every small change

### REFACTOR Phase
- Run tests after EVERY change
- Revert immediately if tests fail
- Small, incremental improvements
- No new behavior during refactor

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "No test framework detected" | Missing config files | Specify --framework explicitly |
| "Requirement cannot be parsed" | Vague requirement | Add more detail: subject, action, conditions |
| "Target path does not exist" | Invalid --input path | Verify directory exists |
| "Safety score too low" | Insufficient test coverage | Write characterization tests first |

---

## Dependencies

### Python Scripts (Standard Library Only)

- `tdd_workflow.py` - Red-Green-Refactor orchestration
- `test_spec_generator.py` - Given-When-Then spec generation
- `fixture_generator.py` - Test data and boundary values
- `format_detector.py` - Framework auto-detection
- `refactor_analyzer.py` - Refactoring safety analysis

### Supported Frameworks

- **JavaScript/TypeScript:** Jest, Vitest, Mocha
- **Python:** Pytest
- **Java:** JUnit
- **Ruby:** RSpec

---

## Success Metrics

- **Test-First Rate:** 90%+ of features developed with test-first approach
- **Cycle Time:** < 5 minutes per Red-Green-Refactor cycle
- **Coverage:** 90%+ on TDD-developed code
- **Bug Reduction:** 40% fewer bugs vs test-after
- **Developer Confidence:** 95%+ confident making changes

---

**Command Pattern:** Multi-Phase
**Execution Time:** 2-10 minutes
**Category:** Generation > Testing
