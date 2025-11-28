# TDD Methodology

## Overview

Test-Driven Development (TDD) is a software development methodology where tests are written before implementation code. The practice follows a strict Red-Green-Refactor cycle that drives design decisions through failing tests. TDD produces well-tested, modular code with high confidence in behavior correctness.

**Core Philosophy**: Write a failing test first, make it pass with minimal code, then improve the design while keeping tests green.

**Value Proposition**:
- 40% fewer bugs in production
- Self-documenting code through test specifications
- Confidence to refactor without breaking functionality
- Emergent design that responds to actual requirements

---

## Red-Green-Refactor Cycle

### RED Phase: Write a Failing Test

**Goal**: Define expected behavior through a test that fails for the right reason.

**Checklist**:
- [ ] Test describes one specific behavior
- [ ] Test uses clear Given-When-Then structure
- [ ] Test name follows `should_X_when_Y` pattern
- [ ] Test fails because functionality doesn't exist (not syntax error)
- [ ] Test is focused and isolated

**Process**:
```python
# Pytest Example - RED Phase
def test_should_return_true_for_valid_email_format():
    """
    GIVEN a string in valid email format
    WHEN validateEmail is called
    THEN it should return True
    """
    # This test will FAIL - validateEmail doesn't exist yet
    result = validate_email("user@example.com")
    assert result is True
```

```typescript
// Jest Example - RED Phase
describe('EmailValidator', () => {
  it('should return true for valid email format', () => {
    // GIVEN: a valid email string
    const email = 'user@example.com';

    // WHEN: validateEmail is called
    const result = validateEmail(email);

    // THEN: it returns true
    expect(result).toBe(true);
    // This test FAILS - validateEmail is undefined
  });
});
```

**Common Mistakes to Avoid**:
- Writing tests that pass immediately (tests nothing)
- Testing implementation details instead of behavior
- Writing multiple assertions testing different behaviors
- Using vague test names like "test1" or "testValidation"

---

### GREEN Phase: Make It Pass

**Goal**: Write the minimum code to make the failing test pass.

**Checklist**:
- [ ] All tests pass (including the new one)
- [ ] Implementation is minimal (no extra features)
- [ ] No premature optimization
- [ ] Code compiles and runs without errors
- [ ] No refactoring yet - just make it work

**Process**:
```python
# Pytest Example - GREEN Phase
def validate_email(email: str) -> bool:
    """Minimal implementation to pass the test"""
    return '@' in email  # Simplest solution that works
```

```typescript
// Jest Example - GREEN Phase
function validateEmail(email: string): boolean {
  // Minimal implementation - just enough to pass
  return email.includes('@');
}
```

**Key Principle**: "Fake it till you make it"
- It's okay to hardcode values initially
- Add just enough logic to pass the current test
- More tests will drive out the real implementation

**Common Mistakes to Avoid**:
- Writing more code than needed to pass the test
- Anticipating future requirements
- Optimizing before tests are green
- Refactoring while trying to make tests pass

---

### REFACTOR Phase: Improve the Design

**Goal**: Improve code quality while keeping all tests green.

**Checklist**:
- [ ] All tests still pass after each change
- [ ] Code is more readable
- [ ] Duplication is reduced
- [ ] Names are meaningful and consistent
- [ ] No new behavior introduced
- [ ] Small, incremental changes

**Process**:
```python
# Pytest Example - REFACTOR Phase
import re

def validate_email(email: str) -> bool:
    """
    Refactored: More robust email validation
    Tests still pass - behavior unchanged
    """
    if not email or not isinstance(email, str):
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

```typescript
// Jest Example - REFACTOR Phase
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

function validateEmail(email: string): boolean {
  // Refactored: extracted regex, added type check
  // All tests still pass
  if (!email || typeof email !== 'string') {
    return false;
  }
  return EMAIL_REGEX.test(email);
}
```

**Safe Refactoring Techniques**:
1. **Extract Method** - Move code block to new function
2. **Rename** - Improve variable/function names
3. **Inline** - Remove unnecessary indirection
4. **Extract Variable** - Name complex expressions
5. **Simplify Conditionals** - Use guard clauses, early returns

**Golden Rule**: Run tests after EVERY change. If tests fail, revert immediately.

---

## TDD Best Practices

### Test Naming Conventions

Use descriptive names that explain the scenario:

**Pattern**: `should_[expected_behavior]_when_[condition]`

```python
# Good names
def test_should_return_error_when_email_is_empty():
def test_should_accept_email_with_plus_sign():
def test_should_reject_email_without_domain():

# Bad names
def test_email():
def test_validation_1():
def test_it_works():
```

### Arrange-Act-Assert (AAA) Structure

Every test should have three distinct sections:

```python
def test_should_calculate_total_with_discount():
    # ARRANGE (Given) - Setup test data
    cart = ShoppingCart()
    cart.add_item(Product("Widget", 100))
    discount = Discount(percent=10)

    # ACT (When) - Execute the action
    total = cart.calculate_total(discount)

    # ASSERT (Then) - Verify the result
    assert total == 90
```

### Test Isolation

Each test must be independent:

```python
# Good - uses fresh fixtures
class TestUserService:
    def setup_method(self):
        self.db = create_test_database()
        self.service = UserService(self.db)

    def teardown_method(self):
        self.db.cleanup()

    def test_create_user(self):
        user = self.service.create("test@example.com")
        assert user.email == "test@example.com"

# Bad - shares state between tests
shared_user = None  # DON'T DO THIS

def test_create():
    global shared_user
    shared_user = create_user()

def test_update():
    shared_user.name = "New Name"  # Depends on test_create running first!
```

### Edge Case Coverage

Always test boundary conditions:

```python
class TestAgeValidator:
    def test_should_accept_minimum_age(self):
        assert is_valid_age(0) is True

    def test_should_accept_maximum_age(self):
        assert is_valid_age(150) is True

    def test_should_reject_negative_age(self):
        assert is_valid_age(-1) is False

    def test_should_reject_above_maximum(self):
        assert is_valid_age(151) is False

    def test_should_handle_none(self):
        assert is_valid_age(None) is False
```

---

## Anti-Patterns to Avoid

### 1. Test-After Development (TAD)

**Problem**: Writing tests after implementation misses design benefits.

**Why It's Bad**:
- Tests often match implementation rather than requirements
- Harder to achieve good coverage
- No design feedback loop
- Tests feel like a chore

**Solution**: Always write the test first, even if it feels slower initially.

### 2. Testing Implementation Details

**Problem**: Tests coupled to internal structure break when code is refactored.

```python
# Bad - tests implementation
def test_user_stored_in_dict():
    service = UserService()
    service.create("test@example.com")
    assert "test@example.com" in service._users  # Private attribute!

# Good - tests behavior
def test_user_can_be_retrieved_after_creation():
    service = UserService()
    service.create("test@example.com")
    user = service.get("test@example.com")
    assert user is not None
```

### 3. Over-Mocking

**Problem**: Mocking everything makes tests pass without verifying real behavior.

```python
# Bad - mocks everything, tests nothing
def test_process_order(mocker):
    mocker.patch('service.validate', return_value=True)
    mocker.patch('service.save', return_value=True)
    mocker.patch('service.notify', return_value=True)
    result = process_order(order)
    assert result is True  # What did this actually test?

# Good - test real behavior with minimal mocking
def test_process_order_validates_and_saves():
    order = create_test_order()
    db = InMemoryDatabase()
    service = OrderService(db)

    service.process(order)

    saved_order = db.get_order(order.id)
    assert saved_order.status == "processed"
```

### 4. Skipping the Refactor Phase

**Problem**: Green tests don't mean good code. Technical debt accumulates.

**Signs You're Skipping Refactor**:
- Methods longer than 20 lines
- Duplicated code across tests or implementation
- Hard-to-understand conditionals
- Poor naming persisting from "fake it" phase

**Solution**: Budget 30% of TDD time for refactoring. After every green, ask: "Can this be clearer?"

### 5. Large Test Steps

**Problem**: Writing too much implementation code between test runs.

```python
# Bad - wrote 50 lines, test fails, hard to debug
def test_full_checkout_flow():
    # Tests entire checkout: cart, payment, inventory, email
    pass  # Fails somewhere in 50 lines of setup

# Good - one behavior at a time
def test_cart_calculates_subtotal():
    # Just tests cart subtotal calculation
    pass

def test_cart_applies_discount():
    # Just tests discount application
    pass
```

---

## Framework-Specific Patterns

### Jest/Vitest (JavaScript/TypeScript)

```typescript
// Structure
describe('ModuleName', () => {
  describe('methodName', () => {
    it('should [behavior] when [condition]', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});

// Async testing
it('should fetch user data', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Test User');
});

// Mocking
jest.mock('./database');
const mockDb = database as jest.Mocked<typeof database>;
mockDb.query.mockResolvedValue({ rows: [] });
```

### Pytest (Python)

```python
# Structure with fixtures
import pytest

@pytest.fixture
def user_service():
    db = InMemoryDatabase()
    return UserService(db)

def test_should_create_user(user_service):
    user = user_service.create("test@example.com")
    assert user.email == "test@example.com"

# Parametrized testing
@pytest.mark.parametrize("email,expected", [
    ("valid@example.com", True),
    ("invalid", False),
    ("", False),
])
def test_email_validation(email, expected):
    assert validate_email(email) == expected

# Exception testing
def test_should_raise_on_duplicate():
    with pytest.raises(DuplicateUserError):
        service.create("existing@example.com")
```

### Mocha/Chai (JavaScript)

```javascript
const { expect } = require('chai');

describe('Calculator', function() {
  let calculator;

  beforeEach(function() {
    calculator = new Calculator();
  });

  describe('#add()', function() {
    it('should return sum of two numbers', function() {
      expect(calculator.add(2, 3)).to.equal(5);
    });

    it('should handle negative numbers', function() {
      expect(calculator.add(-1, 1)).to.equal(0);
    });
  });
});
```

---

## TDD Metrics

### Cycle Time

Track how long each Red-Green-Refactor cycle takes:

| Cycle Length | Assessment |
|--------------|------------|
| < 5 minutes | Ideal - small, focused steps |
| 5-15 minutes | Acceptable for complex features |
| > 15 minutes | Too large - break into smaller tests |

### Test Coverage

Coverage targets by component type:

| Component Type | Target Coverage |
|----------------|----------------|
| Business Logic | 90%+ |
| API Endpoints | 80%+ |
| UI Components | 70%+ |
| Utilities | 95%+ |

**Warning**: 100% coverage doesn't mean quality tests. Focus on behavior coverage.

### Test Quality Indicators

- **Test-to-Code Ratio**: 1:1 to 2:1 is healthy
- **Test Run Time**: Keep under 30 seconds for unit tests
- **Flaky Test Rate**: Should be < 1%
- **Test Maintenance**: If tests break often on refactoring, they're too coupled

---

## Conclusion

**Key Takeaways**:

1. **Always write the test first** - It drives better design and catches requirements issues early

2. **Keep cycles short** - Aim for under 5 minutes per Red-Green-Refactor cycle

3. **Never skip refactoring** - Code quality is built incrementally, not bolted on later

4. **Test behaviors, not implementation** - Tests should survive refactoring

5. **Run tests constantly** - After every change, even small ones

6. **Embrace the discipline** - TDD feels slow initially but prevents costly bugs and rework

**Getting Started**:
1. Pick a small feature or bug fix
2. Write one failing test
3. Make it pass with minimal code
4. Refactor if needed
5. Repeat

The habit builds over time. Start small, stay consistent, and trust the process.
