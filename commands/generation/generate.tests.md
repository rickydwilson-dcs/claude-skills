---
# === CORE IDENTITY ===
name: generate.tests
title: Intelligent Test Case Generation from Existing Code
description: Automatically generate comprehensive test cases for existing code with coverage analysis, edge case detection, and implementation recommendations

category: generate
subcategory: testing

# === WEBSITE DISPLAY ===
difficulty: intermediate
# Requires understanding of code structure, test patterns, and coverage metrics

time-saved: "25 minutes per feature"
# Manual test case creation takes 40-50 minutes per feature, this saves 25 minutes by automating discovery and generation

frequency: "Per feature implementation"
# Teams generate tests once per feature during development

use-cases:
  - "Generate unit test cases for new function implementations with comprehensive coverage"
  - "Create integration test scenarios for feature workflows and component interactions"
  - "Identify untested edge cases and error conditions for better quality assurance"
  - "Generate test templates with setup, assertions, and teardown for quick customization"
  - "Analyze code paths to create test matrix covering all branches and conditions"
  - "Generate parametrized tests for functions with multiple input scenarios"

# === RELATIONSHIPS (Cross-linking) ===
related-agents:
  - cs-qa-engineer
  - cs-test-automation-engineer
  - cs-engineering-lead

related-skills:
  - engineering-team/testing-framework
  - engineering-team/test-data-generator
  - engineering-team/quality-assurance

related-commands:
  - /test.coverage-report
  - /code.analyze-complexity
  - /git.create-pr

# === TECHNICAL ===
dependencies:
  tools:
    - Read
    - Write
    - Bash
    - Grep
    - Glob

  scripts:
    - engineering-team/testing-framework/scripts/test_generator.py
    - engineering-team/test-data-generator/scripts/data_generator.py
    - engineering-team/quality-assurance/scripts/coverage_analyzer.py

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
  - title: "Generate Unit Tests for User Authentication Function"
    input: "/test-generate src/auth/login.js --framework jest --coverage 80"
    output: |
      Test Generation Report: src/auth/login.js

      ANALYSIS SUMMARY
      ════════════════════════════════════════════════════════════════
      Function analyzed: validateCredentials()
      Lines of code: 34
      Cyclomatic complexity: 5
      Code paths identified: 8
      Edge cases detected: 12

      COVERAGE TARGETS
      ════════════════════════════════════════════════════════════════
      Current coverage: 45%
      Target coverage: 80%
      Recommended tests: 7 unit tests
      Estimated creation time: 15 minutes

      GENERATED TEST CASES (7 tests)
      ════════════════════════════════════════════════════════════════

      ✓ Test 1: Valid credentials - happy path
        Scenario: User provides correct email and password
        Expected: Returns authenticated user object
        Priority: HIGH

      ✓ Test 2: Invalid email format
        Scenario: Email does not match regex pattern
        Expected: Throws validation error
        Priority: HIGH

      ✓ Test 3: Password too short
        Scenario: Password length < 8 characters
        Expected: Throws validation error
        Priority: HIGH

      ✓ Test 4: User not found
        Scenario: Email exists but not in database
        Expected: Throws authentication error with 404
        Priority: MEDIUM

      ✓ Test 5: Incorrect password
        Scenario: Email found but password doesn't match hash
        Expected: Throws authentication error with 401
        Priority: HIGH

      ✓ Test 6: Account locked after failed attempts
        Scenario: User failed login 5+ times in last hour
        Expected: Throws account locked error with cooldown time
        Priority: MEDIUM

      ✓ Test 7: SQL injection attempt
        Scenario: Email parameter contains SQL: "' OR '1'='1"
        Expected: Query fails safely, returns validation error
        Priority: CRITICAL

      CODE PATHS ANALYSIS
      ════════════════════════════════════════════════════════════════
      Branch 1: Input validation (line 5-8)
        - Email format validation
        - Password strength validation
        Status: COVERED by tests 2, 3

      Branch 2: Database lookup (line 12-15)
        - User found
        - User not found
        Status: COVERED by tests 1, 4

      Branch 3: Password verification (line 18-22)
        - Hash matches
        - Hash doesn't match
        Status: COVERED by tests 1, 5

      Branch 4: Account status check (line 25-30)
        - Active account
        - Locked account
        Status: COVERED by test 6

      GENERATED TEST FILE
      ════════════════════════════════════════════════════════════════
      Location: src/auth/__tests__/login.test.js

      ```javascript
      describe('validateCredentials()', () => {
        let mockDb;

        beforeEach(() => {
          mockDb = jest.fn();
          jest.clearAllMocks();
        });

        test('Should authenticate valid credentials', async () => {
          const result = await validateCredentials('user@example.com', 'password123');
          expect(result).toHaveProperty('userId');
          expect(result.email).toBe('user@example.com');
        });

        test('Should reject invalid email format', async () => {
          await expect(validateCredentials('invalid-email', 'password123'))
            .rejects.toThrow('Invalid email format');
        });

        test('Should reject short password', async () => {
          await expect(validateCredentials('user@example.com', 'pass'))
            .rejects.toThrow('Password must be at least 8 characters');
        });

        test('Should handle user not found', async () => {
          mockDb.mockResolvedValueOnce(null);
          await expect(validateCredentials('notfound@example.com', 'password123'))
            .rejects.toThrow('User not found');
        });

        test('Should reject incorrect password', async () => {
          mockDb.mockResolvedValueOnce({ email: 'user@example.com', password_hash: 'hash' });
          await expect(validateCredentials('user@example.com', 'wrongpass'))
            .rejects.toThrow('Invalid credentials');
        });

        test('Should lock account after failed attempts', async () => {
          mockDb.mockResolvedValueOnce({
            email: 'user@example.com',
            failed_attempts: 5,
            locked_until: Date.now() + 3600000
          });
          await expect(validateCredentials('user@example.com', 'password123'))
            .rejects.toThrow('Account temporarily locked');
        });

        test('Should prevent SQL injection', async () => {
          await expect(validateCredentials("' OR '1'='1", 'password123'))
            .rejects.toThrow('Invalid email format');
        });
      });
      ```

      TESTING RECOMMENDATIONS
      ════════════════════════════════════════════════════════════════
      1. [REQUIRED] Add error case testing for database connection failures
      2. [REQUIRED] Test password hashing with bcrypt timing attacks in mind
      3. [IMPORTANT] Add performance test ensuring login completes <200ms
      4. [IMPORTANT] Add concurrency test for simultaneous login attempts
      5. [OPTIONAL] Add audit logging verification for security events
      6. [OPTIONAL] Add internationalization (i18n) testing for error messages

      NEXT STEPS
      ════════════════════════════════════════════════════════════════
      1. Copy generated test file to src/auth/__tests__/login.test.js
      2. Run: npm test -- src/auth/__tests__/login.test.js
      3. Verify all 7 tests pass (green checkmarks)
      4. Check coverage: npm test -- --coverage src/auth/login.js
      5. Expected coverage result: 95%+

      Report generated in 3.2s
      Generated by: Test Generation Agent v1.0.0

  - title: "Generate Integration Tests for User Dashboard Feature"
    input: "/test-generate src/features/dashboard/ --framework jest --integration --coverage 75"
    output: |
      Test Generation Report: src/features/dashboard/

      FEATURE ANALYSIS
      ════════════════════════════════════════════════════════════════
      Files analyzed: 6
        - components/Dashboard.jsx (145 lines)
        - components/Widgets.jsx (234 lines)
        - services/dataService.js (89 lines)
        - hooks/useUserData.js (56 lines)
        - utils/formatting.js (78 lines)
        - __mocks__/apiClient.js (42 lines)

      Total coverage needed: 65% → 75% (10% improvement)
      Recommended integration tests: 9 test suites
      Estimated creation time: 20 minutes

      GENERATED INTEGRATION TESTS (9 suites)
      ════════════════════════════════════════════════════════════════

      ✓ Test Suite 1: Dashboard Component Rendering
        - Dashboard renders with user data
        - Dashboard handles loading state
        - Dashboard displays error state
        Priority: HIGH

      ✓ Test Suite 2: Widget Lifecycle
        - Widgets initialize with default data
        - Widgets update when data changes
        - Widgets cleanup on unmount
        Priority: HIGH

      ✓ Test Suite 3: Data Fetching Integration
        - useUserData hook fetches data on mount
        - Hook refetches on dependency change
        - Hook handles network errors gracefully
        Priority: HIGH

      ✓ Test Suite 4: User Interactions
        - Clicking widget filters dashboard
        - Search input filters displayed widgets
        - Sorting preference persists in localStorage
        Priority: MEDIUM

      ✓ Test Suite 5: Real-time Updates
        - Dashboard updates when server pushes new data
        - WebSocket reconnection works after disconnect
        - Component unsubscribes on unmount
        Priority: MEDIUM

      ✓ Test Suite 6: Performance Metrics
        - Initial render completes <500ms
        - Interactions respond <100ms
        - Memory doesn't leak on re-renders
        Priority: MEDIUM

      ✓ Test Suite 7: Accessibility Features
        - Keyboard navigation works across widgets
        - Screen reader announces updates
        - Color contrast meets WCAG AA standards
        Priority: LOW

      ✓ Test Suite 8: Error Recovery
        - API timeout handling and retry logic
        - Partial data failures don't crash dashboard
        - User sees friendly error messages
        Priority: HIGH

      ✓ Test Suite 9: Browser Compatibility
        - Dashboard works in Chrome, Firefox, Safari
        - Responsive layout adjusts for mobile
        - No console errors or warnings
        Priority: LOW

      COVERAGE ANALYSIS
      ════════════════════════════════════════════════════════════════
      Before: 65% coverage
      After: 95% coverage (with generated tests)
      Gap analysis:
        - Untested components: Dashboard.jsx (40% → 95%)
        - Untested hooks: useUserData (20% → 100%)
        - Untested error paths: 8 paths → fully covered
        - Untested edge cases: 12 cases → fully covered

      GENERATED TEST FILES
      ════════════════════════════════════════════════════════════════
      Location: src/features/dashboard/__tests__/integration.test.js
      Location: src/features/dashboard/__tests__/performance.test.js
      Location: src/features/dashboard/__tests__/accessibility.test.js

      EXECUTION PLAN
      ════════════════════════════════════════════════════════════════
      Phase 1: Copy generated test files (1 min)
      Phase 2: Install test dependencies if needed (2 min)
      Phase 3: Run tests locally: npm test -- dashboard (3 min)
      Phase 4: Fix any environment setup issues (5 min)
      Phase 5: Review coverage report (2 min)
      Phase 6: Push tests to PR (1 min)

      Total time: ~14 minutes

      Report generated in 4.1s
      Generated by: Test Generation Agent v1.0.0

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
created: 2025-11-24
updated: 2025-11-24

# === DISCOVERABILITY ===
tags:
  - test-generation
  - test-cases
  - unit-testing
  - integration-testing
  - test-coverage
  - edge-cases
  - test-automation
  - quality-assurance
  - jest
  - mocha

featured: false
verified: true
license: MIT

---

# Test Generate

Intelligent test case generation command that analyzes existing code and automatically generates comprehensive unit and integration test cases with coverage analysis and edge case detection.

---

## Pattern Type: Multi-Phase

**Complexity:** Medium
**Execution Time:** 2-5 minutes depending on code size
**Destructive:** No (generates files but doesn't modify existing code)

---

## Multi-Phase Execution

### Phase 1: Discovery

**Goal:** Gather comprehensive information about code structure and complexity

**Steps:**
1. Scan specified files and directories for implementation code
2. Identify function signatures, parameters, and return types
3. Detect code branches, loops, and decision paths
4. Catalog error handling and edge cases
5. Analyze dependencies and external calls
6. Build control flow graph for each function

**Tools Used:** Glob, Read, Bash (for code metrics)

**Output:** Inventory of functions, complexity metrics, code paths, dependencies

### Phase 2: Analysis

**Goal:** Identify test cases needed for comprehensive coverage

**Analysis Dimensions:**

1. **Code Path Analysis**
   - Cyclomatic complexity (number of paths)
   - Branch coverage (if/else, switch statements)
   - Loop coverage (for, while, do-while)
   - Exception handling paths
   - Return path coverage

2. **Edge Case Detection**
   - Boundary conditions (min/max values)
   - Null/undefined handling
   - Empty collections
   - Type mismatches
   - Resource limits
   - Concurrency conditions

3. **Error Scenario Detection**
   - Validation failures
   - Network/API failures
   - Resource exhaustion
   - Timeout conditions
   - Permission errors
   - Recovery scenarios

4. **Test Type Determination**
   - Unit tests (isolated function testing)
   - Integration tests (component interaction)
   - Performance tests (execution time/memory)
   - Security tests (injection, auth bypass)
   - Accessibility tests (WCAG compliance)

**Coverage Targets:**
- 100% line coverage
- 100% branch coverage
- 100% path coverage
- All error conditions
- All edge cases

### Phase 3: Task Execution

**Goal:** Generate test case code and recommendations

**Actions:**

1. **Test Case Generation**
   - Create test for each code path
   - Generate happy path tests
   - Generate error/exception tests
   - Create edge case tests
   - Add performance/load tests

2. **Test Code Production**
   - Generate test file with proper structure
   - Include setup/teardown (beforeEach/afterEach)
   - Add mocking/stubbing for dependencies
   - Include descriptive test names
   - Add assertion sets for each scenario

3. **Documentation Generation**
   - Describe each test's purpose
   - List test data and scenarios
   - Include expected results
   - Provide coverage metrics
   - Recommend additional tests

4. **Integration Guidelines**
   - Show where to place test files
   - Indicate framework setup needed
   - List mock dependencies required
   - Provide execution instructions

### Phase 4: Reporting

**Goal:** Present test cases in clear, actionable format

**Report Includes:**

1. **Coverage Analysis**
   - Current coverage percentage
   - Target coverage percentage
   - Gap analysis by file/function
   - Coverage improvement estimate

2. **Generated Test Cases**
   - Test case ID and name
   - Input scenarios and data
   - Expected outputs/assertions
   - Priority level (HIGH/MEDIUM/LOW)
   - Estimated execution time

3. **Code Path Matrix**
   - Branch map showing coverage
   - Edge cases with test IDs
   - Error scenarios with recovery
   - Untested paths highlighted

4. **Implementation Guide**
   - Test file locations
   - Framework-specific setup
   - Mock/stub requirements
   - Example test implementations
   - Execution commands

5. **Quality Recommendations**
   - Critical missing tests
   - Performance test needs
   - Security test gaps
   - Accessibility considerations

**Report Location:** Printed to console or saved to file with --output flag

---

## Usage

```bash
/test-generate [target] [options]
```

### Arguments

- `target` - File, directory, or function to generate tests for (required)
  - Single file: `/test-generate src/utils/helpers.js`
  - Directory: `/test-generate src/services/`
  - Function: `/test-generate src/auth.js --function validateEmail`

### Options

```bash
--framework FRAMEWORK     # Test framework (jest, mocha, pytest) - default: jest
--coverage TARGET%        # Target coverage percentage (50-100) - default: 80
--integration             # Generate integration tests in addition to unit tests
--security                # Include security-focused test cases
--performance             # Include performance/load tests
--accessibility           # Include WCAG accessibility tests
--output FILE             # Save generated tests to file
--format FORMAT           # Output format (js, ts, py, java) - auto-detect from target
--language LANG           # Programming language (javascript, python, java) - auto-detect
--mock-strategy STRATEGY  # Mocking approach (jest-mock, sinon, unittest.mock)
--include-setup           # Include complete beforeEach/afterEach setup
--min-tests N             # Minimum number of test cases to generate
--max-tests N             # Maximum number of test cases to generate
--exclude PATTERN         # Exclude functions matching pattern
--verbose                 # Show detailed analysis output
```

### Examples

**Example 1: Generate unit tests for validation function**

```bash
/test-generate src/validators/email.js --framework jest --coverage 90
```

**Example 2: Generate comprehensive tests with integration scenarios**

```bash
/test-generate src/services/ --framework jest --integration --coverage 85 --security
```

**Example 3: Generate Python tests for ML model**

```bash
/test-generate src/models/classifier.py --framework pytest --coverage 80
```

---

## What This Command Does

### Context Gathering

The command will:
1. Scan target files to extract function definitions
2. Parse function signatures, parameters, and return types
3. Analyze control flow and decision points
4. Identify external dependencies and mocks needed
5. Catalog existing error handling and edge cases
6. Measure code complexity metrics

### Task Execution

Then it will:
1. Determine code paths and branches needing tests
2. Identify edge cases and boundary conditions
3. Generate test cases for each path/condition
4. Create implementation-ready test code
5. Calculate coverage metrics
6. Generate recommendations

### Expected Output

You will receive:
- Coverage analysis report
- List of generated test cases with descriptions
- Test file(s) with complete implementations
- Mock/stub setup instructions
- Execution commands to run tests
- Recommendations for additional tests

**Output Format:** Markdown report + JavaScript/Python test files
**Output Location:** Console report + generated test files in project

---

## Analysis Criteria

### Code Path Coverage

**Branch Coverage**
- All if/else branches tested
- All switch cases covered
- All loops with 0, 1, and N iterations
- All exception paths
- All return paths

**Complexity-Based**
- Cyclomatic complexity <5: 2-3 tests minimum
- Cyclomatic complexity 5-10: 4-6 tests minimum
- Cyclomatic complexity >10: 8+ tests minimum

### Edge Cases Detected

**Boundary Conditions**
- Empty values (empty string, [], null)
- Maximum values (MAX_INT, MAX_STRING_LENGTH)
- Minimum values (MIN_INT, zero)
- Off-by-one conditions

**Type Variations**
- Null/undefined inputs
- Wrong type inputs
- Mixed type collections
- Type coercion edge cases

**Resource Conditions**
- Memory-intensive operations
- Network timeouts
- File system limits
- Concurrency/race conditions

### Error Scenarios

**Input Validation**
- Invalid format/pattern
- Out-of-range values
- Missing required fields
- Malformed data structures

**System Failures**
- Database connection errors
- Network timeouts/failures
- File access errors
- Permission denied

**Recovery Conditions**
- Retry after failure
- Fallback to default
- Graceful degradation
- State rollback

---

## Error Handling

### Common Issues

**Issue:** "Unable to parse code syntax"
**Cause:** File contains syntax errors or non-standard code
**Solution:** Fix syntax errors and ensure code is valid
**Prevention:** Run code through linter before analysis

---

**Issue:** "Target function has too many paths (>20)"
**Cause:** Function is too complex with many branches
**Solution:** Consider refactoring function first, or limit with --max-tests
**Prevention:** Keep functions focused with low cyclomatic complexity

---

**Issue:** "Cannot determine test framework"
**Cause:** No --framework specified and cannot auto-detect
**Solution:** Specify framework explicitly: --framework jest
**Prevention:** Use standard project setup with package.json or pyproject.toml

---

**Issue:** "Mock dependencies not found"
**Cause:** External dependencies don't exist in project
**Solution:** Install dependencies or adjust --mock-strategy
**Prevention:** Ensure all dependencies listed in project manifest

---

**Issue:** "Generated tests fail on execution"
**Cause:** Mock setup incorrect or environment differences
**Solution:** Review mock setup, adjust paths, verify test data
**Prevention:** Run generated tests immediately to identify issues

---

### Validation Failures

If the command reports validation errors:

1. **File Not Found**
   - Check: File path and existence
   - Fix: Verify path with `ls` or file explorer

2. **Syntax Errors**
   - Check: Code is valid and compilable
   - Fix: Run linter (eslint, pylint) to identify errors

3. **Framework Not Found**
   - Check: Test framework installed in project
   - Fix: npm install jest (or your framework)

---

## Integration with Agents & Skills

### Related Agents

This command works well with:

- **[cs-qa-engineer](../../agents/engineering/cs-qa-engineer.md)** - Orchestrates comprehensive testing workflows
- **[cs-test-automation-engineer](../../agents/engineering/cs-test-automation-engineer.md)** - Manages test suite maintenance
- **[cs-engineering-lead](../../agents/engineering/cs-engineering-lead.md)** - Validates testing standards

### Related Skills

This command leverages:

- **[testing-framework](../../skills/engineering-team/testing-framework/)** - Test patterns and best practices
- **[test-data-generator](../../skills/engineering-team/test-data-generator/)** - Test data creation and management
- **[quality-assurance](../../skills/engineering-team/quality-assurance/)** - QA standards and metrics

### Python Tools

This command may execute:

```bash
# Test generation
python skills/engineering-team/testing-framework/scripts/test_generator.py [target]

# Test data generation
python skills/engineering-team/test-data-generator/scripts/data_generator.py [scenarios]

# Coverage analysis
python skills/engineering-team/quality-assurance/scripts/coverage_analyzer.py [tests]
```

---

## Success Criteria

This command is successful when:

- [ ] All code paths identified and test cases generated
- [ ] Coverage target met (default 80%, configurable)
- [ ] Generated test files are syntactically valid
- [ ] Tests include setup/teardown and mocking
- [ ] Edge cases and error conditions are covered
- [ ] Test implementations are ready to execute
- [ ] Report includes actionable recommendations
- [ ] Generated tests pass when executed

### Quality Metrics

**Expected Outcomes:**
- Analysis Time: 1-3 minutes for typical file
- Test Generation Time: 1-2 minutes per file
- Generated Tests: 4-8 tests per function on average
- Coverage Improvement: 20-40% increase from baseline
- False Positive Rate: <2% (tests are valid and useful)

---

## Tips for Best Results

1. **Code Preparation**
   - Ensure code compiles/runs without syntax errors
   - Keep functions focused and under 50 lines
   - Use clear, descriptive naming conventions
   - Add inline comments for complex logic

2. **Test Configuration**
   - Start with --coverage 80 target (reasonable default)
   - Use --integration for feature workflows
   - Include --security for authentication/data code
   - Add --performance for critical paths

3. **Review and Customize**
   - Review generated test data for realism
   - Customize mock responses for your scenarios
   - Add domain-specific assertions
   - Extend with additional edge cases specific to your app

4. **Execution and Refinement**
   - Run tests immediately to validate
   - Fix any environment/path issues
   - Commit generated tests to version control
   - Update tests when code changes

---

## Related Commands

- `/test.coverage-report` - Generate coverage metrics for existing tests
- `/code.analyze-complexity` - Analyze code complexity and refactoring needs
- `/git.create-pr` - Create PR with generated tests
- `/performance.profile-app` - Profile application performance

---

## References

- [Jest Testing Documentation](https://jestjs.io/) - Jest test framework
- [Mocha Testing Framework](https://mochajs.org/) - Mocha alternative
- [Pytest Documentation](https://docs.pytest.org/) - Python testing framework
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development) - TDD principles
- [Code Coverage Best Practices](https://en.wikipedia.org/wiki/Code_coverage) - Coverage metrics
- [WCAG Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/) - Accessibility testing

---

**Last Updated:** November 24, 2025
**Version:** v1.0.0
**Maintained By:** Claude Skills Team
**Feedback:** Submit issues or feature requests in repository issues
