# Code Review Checklist

## Overview

Comprehensive checklist for reviewing code across TypeScript, JavaScript, Python, Swift, Kotlin, and Go. This guide ensures consistent, high-quality code reviews that catch bugs, improve maintainability, and enforce best practices.

## Pre-Review Checklist

### Before Starting the Review

- [ ] Pull request description is clear and complete
- [ ] Tests are included and passing
- [ ] CI/CD pipeline is green
- [ ] Branch is up-to-date with target branch
- [ ] No merge conflicts exist
- [ ] Changes are reasonably sized (< 400 lines preferred)

### Context Gathering

- [ ] Understand the business requirement
- [ ] Review related tickets/issues
- [ ] Check architectural context
- [ ] Identify affected systems

## Code Quality Checklist

### Functionality

- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error scenarios are covered
- [ ] Input validation is present
- [ ] Return values are correct
- [ ] Null/undefined handled properly

### Readability

- [ ] Code is self-documenting
- [ ] Variable names are descriptive
- [ ] Functions have single responsibility
- [ ] Complexity is minimal
- [ ] Comments explain "why", not "what"
- [ ] No dead code or commented code

### Maintainability

- [ ] DRY principle followed (Don't Repeat Yourself)
- [ ] SOLID principles applied
- [ ] Proper separation of concerns
- [ ] Dependencies are minimal
- [ ] Configuration is externalized
- [ ] Magic numbers/strings avoided

### Performance

- [ ] No obvious performance issues
- [ ] Database queries are optimized
- [ ] No N+1 query problems
- [ ] Caching used appropriately
- [ ] Async operations handled correctly
- [ ] Memory leaks prevented

## Language-Specific Checklists

### TypeScript/JavaScript

**Type Safety**
- [ ] Proper TypeScript types (avoid `any`)
- [ ] Interfaces defined for complex objects
- [ ] Generic types used appropriately
- [ ] Type guards implemented

**Modern Patterns**
- [ ] ES6+ features used appropriately
- [ ] Promises/async-await over callbacks
- [ ] Destructuring used where beneficial
- [ ] Arrow functions used consistently
- [ ] Template literals for string concatenation

**React-Specific**
- [ ] Hooks used correctly (dependencies)
- [ ] Components properly memoized
- [ ] State management is appropriate
- [ ] Effects cleaned up properly
- [ ] Keys provided for lists

**Example Issues:**
```typescript
// Bad: Using 'any' type
function processData(data: any) {
  return data.value;
}

// Good: Proper typing
interface DataObject {
  value: string;
}

function processData(data: DataObject): string {
  return data.value;
}
```

### Python

**Pythonic Code**
- [ ] PEP 8 style guide followed
- [ ] List/dict comprehensions used appropriately
- [ ] Context managers for resources
- [ ] Type hints provided (Python 3.6+)
- [ ] f-strings for formatting

**Common Issues**
- [ ] Mutable default arguments avoided
- [ ] `with` statements for file operations
- [ ] Exception handling is specific
- [ ] `__init__.py` files present
- [ ] Virtual environment documented

**Example:**
```python
# Bad: Mutable default argument
def add_item(item, items=[]):
    items.append(item)
    return items

# Good: None with initialization
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Swift

**Swift-Specific**
- [ ] Optional unwrapping is safe
- [ ] Guard statements used appropriately
- [ ] Structs vs classes chosen correctly
- [ ] Protocol-oriented design
- [ ] Memory management (weak/unowned)

**Example:**
```swift
// Bad: Force unwrapping
let value = dictionary["key"]!

// Good: Optional binding
if let value = dictionary["key"] {
    // Use value safely
}

// Better: Guard for early exit
guard let value = dictionary["key"] else {
    return
}
```

### Kotlin

**Kotlin-Specific**
- [ ] Null safety utilized
- [ ] Extension functions used
- [ ] Data classes for models
- [ ] Coroutines for async
- [ ] Scope functions used appropriately

**Example:**
```kotlin
// Bad: Null checks everywhere
if (user != null) {
    if (user.name != null) {
        println(user.name)
    }
}

// Good: Safe call and let
user?.name?.let { println(it) }
```

### Go

**Go-Specific**
- [ ] Error handling explicit
- [ ] Defer used for cleanup
- [ ] Goroutines managed properly
- [ ] Channels used correctly
- [ ] Interfaces are minimal

**Example:**
```go
// Bad: Ignoring errors
result, _ := doSomething()

// Good: Proper error handling
result, err := doSomething()
if err != nil {
    return nil, fmt.Errorf("failed to do something: %w", err)
}
```

## Testing Checklist

### Test Coverage

- [ ] Unit tests included
- [ ] Integration tests where needed
- [ ] Edge cases tested
- [ ] Error scenarios tested
- [ ] Coverage meets requirements (80%+)
- [ ] Tests are deterministic

### Test Quality

- [ ] Tests are readable
- [ ] Test names are descriptive
- [ ] Arrange-Act-Assert pattern
- [ ] No test interdependencies
- [ ] Mock/stub external dependencies
- [ ] Tests run quickly

**Example Test Structure:**
```typescript
describe('calculateTotal', () => {
  it('should return sum of positive numbers', () => {
    // Arrange
    const numbers = [1, 2, 3];

    // Act
    const result = calculateTotal(numbers);

    // Assert
    expect(result).toBe(6);
  });

  it('should handle empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should handle negative numbers', () => {
    expect(calculateTotal([1, -2, 3])).toBe(2);
  });
});
```

## Security Checklist

### Input Validation

- [ ] All user input validated
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (output escaping)
- [ ] CSRF protection in place
- [ ] File uploads validated
- [ ] Rate limiting implemented

### Authentication & Authorization

- [ ] Authentication required where needed
- [ ] Authorization checks present
- [ ] Passwords hashed (bcrypt/argon2)
- [ ] Sessions secured
- [ ] JWT tokens validated
- [ ] Principle of least privilege

### Data Protection

- [ ] Sensitive data encrypted
- [ ] Secrets not in code
- [ ] Environment variables used
- [ ] Logs don't expose secrets
- [ ] HTTPS enforced
- [ ] Headers secured

**Security Anti-Patterns:**
```javascript
// Bad: SQL injection vulnerable
const query = `SELECT * FROM users WHERE id = ${userId}`;

// Good: Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// Bad: Plaintext password
const user = { password: req.body.password };

// Good: Hashed password
const hashedPassword = await bcrypt.hash(req.body.password, 10);
const user = { password: hashedPassword };
```

## Architecture Checklist

### Design Patterns

- [ ] Appropriate patterns used
- [ ] Not over-engineered
- [ ] Follows existing patterns
- [ ] Abstractions are useful
- [ ] Coupling is loose
- [ ] Cohesion is high

### Scalability

- [ ] Horizontal scaling possible
- [ ] No hardcoded limits
- [ ] Stateless where possible
- [ ] Database indexed properly
- [ ] Caching strategy clear
- [ ] Resource limits defined

## Documentation Checklist

### Code Documentation

- [ ] Complex logic explained
- [ ] Public APIs documented
- [ ] Parameters documented
- [ ] Return values documented
- [ ] Exceptions documented
- [ ] Examples provided

### Project Documentation

- [ ] README updated
- [ ] API docs updated
- [ ] Configuration documented
- [ ] Deployment guide updated
- [ ] Migration guide (if breaking)
- [ ] Changelog updated

## Git Checklist

### Commit Quality

- [ ] Commits are atomic
- [ ] Commit messages are clear
- [ ] Conventional commits format
- [ ] No WIP commits
- [ ] No merge commits (if squash merge)
- [ ] Signed commits (if required)

**Good Commit Messages:**
```
feat(auth): add OAuth2 login flow
fix(api): resolve race condition in user creation
refactor(db): extract query builder
docs(readme): update installation steps
test(api): add integration tests for payments
```

### Branch Management

- [ ] Feature branch from main/develop
- [ ] Branch name is descriptive
- [ ] No long-lived branches
- [ ] Rebased on target branch
- [ ] No unnecessary files committed

## Performance Checklist

### Frontend Performance

- [ ] Bundle size is reasonable
- [ ] Code splitting implemented
- [ ] Images optimized
- [ ] Lazy loading used
- [ ] No unnecessary re-renders
- [ ] Caching headers set

### Backend Performance

- [ ] Database queries optimized
- [ ] Indexes exist
- [ ] N+1 queries avoided
- [ ] Connection pooling used
- [ ] Appropriate timeout values
- [ ] Rate limiting in place

## Feedback Guidelines

### Providing Feedback

**Be Constructive**
- Focus on code, not person
- Explain why, not just what
- Suggest alternatives
- Acknowledge good work
- Use questions, not commands

**Prioritize Issues**
- Blocking: Security, bugs, breaking changes
- Major: Performance, architecture, maintainability
- Minor: Style, naming, comments
- Nitpicks: Personal preferences

**Example Feedback:**

```markdown
## Blocking Issues
- [ ] SQL injection vulnerability in user search (line 45)
- [ ] Authentication check missing in delete endpoint (line 123)

## Major Issues
- [ ] Consider extracting this 50-line function into smaller pieces (line 67)
- [ ] This N+1 query could cause performance issues at scale (line 89)

## Minor Issues
- [ ] Typo in variable name: "usre" should be "user" (line 34)
- [ ] Consider adding JSDoc for this public function (line 56)

## Positive Notes
- Great test coverage on the edge cases!
- Nice use of TypeScript generics here.
```

### Receiving Feedback

- Accept feedback graciously
- Ask questions if unclear
- Explain your reasoning
- Be open to alternatives
- Don't take it personally

## Quick Reference

### Review Priorities

1. **Security issues** - Always highest priority
2. **Bugs and correctness** - Functional issues
3. **Performance problems** - Scalability concerns
4. **Architecture concerns** - Design and maintainability
5. **Style and formatting** - Automated where possible

### Common Red Flags

- Functions longer than 50 lines
- Files longer than 500 lines
- Cyclomatic complexity > 10
- Test coverage < 70%
- No error handling
- Hardcoded values
- Commented-out code
- Console.log statements
- TODO comments without tickets

### Time Guidelines

- Small PR (< 100 lines): 15-30 minutes
- Medium PR (100-300 lines): 30-60 minutes
- Large PR (300-500 lines): 1-2 hours
- Very large PR (> 500 lines): Consider breaking up

## Conclusion

Use this checklist as a guide, not a rigid set of rules. Context matters - some items may not apply to every review. The goal is to catch issues early, maintain code quality, and facilitate knowledge sharing across the team.

**Key Takeaways:**
- Prioritize security and correctness
- Be thorough but pragmatic
- Provide actionable feedback
- Foster a positive review culture
- Continuously improve the process
