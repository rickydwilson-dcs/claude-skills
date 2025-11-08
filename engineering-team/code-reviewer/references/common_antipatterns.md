# Common Code Anti-Patterns

## Overview

This guide catalogs common anti-patterns found in code reviews across TypeScript, JavaScript, Python, Swift, Kotlin, and Go. Understanding these patterns helps prevent bugs, improve maintainability, and enhance code quality.

## General Anti-Patterns

### God Object / God Class

**Problem:** A single class/module that knows too much or does too much.

```typescript
// Bad: God class doing everything
class UserManager {
  validateEmail(email: string) {}
  hashPassword(password: string) {}
  sendEmail(to: string, subject: string) {}
  generateReport(userId: string) {}
  processPayment(amount: number) {}
  logActivity(activity: string) {}
}

// Good: Separated responsibilities
class EmailValidator {
  validate(email: string): boolean {}
}

class PasswordService {
  hash(password: string): string {}
}

class EmailService {
  send(to: string, subject: string): void {}
}

class ReportGenerator {
  generate(userId: string): Report {}
}

class PaymentProcessor {
  process(amount: number): Payment {}
}
```

### Magic Numbers and Strings

**Problem:** Hardcoded values without explanation.

```python
# Bad: Magic numbers
if user.age > 18:
    discount = price * 0.15

# Good: Named constants
ADULT_AGE = 18
STUDENT_DISCOUNT_RATE = 0.15

if user.age > ADULT_AGE:
    discount = price * STUDENT_DISCOUNT_RATE
```

### Deep Nesting

**Problem:** Multiple levels of indentation make code hard to read.

```typescript
// Bad: Deep nesting
function processOrder(order: Order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.customer) {
        if (order.customer.isActive) {
          if (order.total > 0) {
            // Process order
          }
        }
      }
    }
  }
}

// Good: Early returns / guard clauses
function processOrder(order: Order) {
  if (!order) return;
  if (order.items.length === 0) return;
  if (!order.customer) return;
  if (!order.customer.isActive) return;
  if (order.total <= 0) return;

  // Process order
}
```

### Premature Optimization

**Problem:** Optimizing before measuring performance.

```go
// Bad: Premature optimization
// Using complex caching before knowing if it's needed
var cache = make(map[string]*Result)
var mutex sync.RWMutex

func getResult(key string) *Result {
    mutex.RLock()
    if result, ok := cache[key]; ok {
        mutex.RUnlock()
        return result
    }
    mutex.RUnlock()

    // Complex calculation...
    result := calculate(key)

    mutex.Lock()
    cache[key] = result
    mutex.Unlock()

    return result
}

// Good: Start simple, optimize if needed
func getResult(key string) *Result {
    return calculate(key)
}
// Add caching AFTER measuring performance bottleneck
```

## TypeScript/JavaScript Anti-Patterns

### Callback Hell

**Problem:** Deeply nested callbacks.

```javascript
// Bad: Callback hell
getData(function(a) {
  getMoreData(a, function(b) {
    getMoreData(b, function(c) {
      getMoreData(c, function(d) {
        // Finally do something
      });
    });
  });
});

// Good: Promises
getData()
  .then(a => getMoreData(a))
  .then(b => getMoreData(b))
  .then(c => getMoreData(c))
  .then(d => {
    // Do something
  });

// Better: Async/await
async function process() {
  const a = await getData();
  const b = await getMoreData(a);
  const c = await getMoreData(b);
  const d = await getMoreData(c);
  // Do something
}
```

### Using 'any' Type

**Problem:** Defeats the purpose of TypeScript.

```typescript
// Bad: Using 'any'
function processData(data: any): any {
  return data.value.toUpperCase();
}

// Good: Proper types
interface DataObject {
  value: string;
}

function processData(data: DataObject): string {
  return data.value.toUpperCase();
}
```

### Modifying Props in React

**Problem:** Props should be immutable.

```typescript
// Bad: Modifying props
const UserProfile: React.FC<{ user: User }> = ({ user }) => {
  user.name = "Modified";  // Don't do this!
  return <div>{user.name}</div>;
};

// Good: Use state
const UserProfile: React.FC<{ user: User }> = ({ user: initialUser }) => {
  const [user, setUser] = useState(initialUser);

  const handleUpdate = () => {
    setUser({ ...user, name: "Modified" });
  };

  return <div>{user.name}</div>;
};
```

### Ignoring Errors

```typescript
// Bad: Silently catching errors
try {
  await riskyOperation();
} catch (error) {
  // Do nothing
}

// Good: Handle or propagate
try {
  await riskyOperation();
} catch (error) {
  logger.error('Risk operation failed', error);
  throw new OperationError('Failed to complete operation', { cause: error });
}
```

## Python Anti-Patterns

### Mutable Default Arguments

**Problem:** Default mutable arguments are shared across calls.

```python
# Bad: Mutable default argument
def add_item(item, items=[]):
    items.append(item)
    return items

result1 = add_item(1)  # [1]
result2 = add_item(2)  # [1, 2] - Unexpected!

# Good: Use None
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Bare Except Clauses

**Problem:** Catching all exceptions including system exits.

```python
# Bad: Bare except
try:
    risky_operation()
except:  # Catches KeyboardInterrupt, SystemExit, etc.
    pass

# Good: Specific exceptions
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except IOError as e:
    logger.error(f"IO error: {e}")

# Acceptable: Catch Exception (not BaseException)
try:
    risky_operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### Using 'is' for Value Comparison

**Problem:** 'is' checks identity, not equality.

```python
# Bad: Using 'is' for values
if x is 5:  # Checking object identity
    pass

# Good: Using '==' for values
if x == 5:  # Checking value equality
    pass

# 'is' is correct for singletons
if x is None:  # Correct
    pass

if x is True:  # Correct
    pass
```

### Not Using Context Managers

**Problem:** Resources not properly closed.

```python
# Bad: Manual file handling
file = open('data.txt', 'r')
data = file.read()
file.close()  # Might not execute if error occurs

# Good: Context manager
with open('data.txt', 'r') as file:
    data = file.read()
# File automatically closed
```

## Swift Anti-Patterns

### Force Unwrapping

**Problem:** App crashes if value is nil.

```swift
// Bad: Force unwrapping
let user = fetchUser(id: userId)!
print(user.name)  // Crashes if user is nil

// Good: Optional binding
if let user = fetchUser(id: userId) {
    print(user.name)
}

// Better: Guard for early exit
guard let user = fetchUser(id: userId) else {
    return
}
print(user.name)
```

### Implicitly Unwrapped Optionals

**Problem:** Defeats optional safety unless necessary.

```swift
// Bad: Unnecessary IUO
var user: User! = nil

// Good: Regular optional
var user: User? = nil

// IUO acceptable for: IBOutlets, dependency injection
@IBOutlet var label: UILabel!  // Acceptable
```

### Retain Cycles in Closures

**Problem:** Memory leaks from strong reference cycles.

```swift
// Bad: Creating retain cycle
class ViewController: UIViewController {
    var name: String = "View"

    func setup() {
        someAsyncOperation { [self] in
            // Strong reference to self
            print(self.name)
        }
    }
}

// Good: Weak self
class ViewController: UIViewController {
    var name: String = "View"

    func setup() {
        someAsyncOperation { [weak self] in
            guard let self = self else { return }
            print(self.name)
        }
    }
}
```

## Kotlin Anti-Patterns

### Not Using Data Classes

**Problem:** Manually implementing equals, hashCode, toString.

```kotlin
// Bad: Regular class for data
class User(val id: String, val name: String) {
    override fun equals(other: Any?): Boolean {
        // Manual implementation
    }
    override fun hashCode(): Int {
        // Manual implementation
    }
}

// Good: Data class
data class User(val id: String, val name: String)
// Auto-generates equals, hashCode, toString, copy
```

### Force Non-Null Assertion (!!)

**Problem:** Defeats null safety, can cause crashes.

```kotlin
// Bad: Force non-null
val name = user!!.name!!.firstName!!

// Good: Safe calls
val name = user?.name?.firstName

// Good: Let for non-null operation
user?.name?.let { name ->
    println(name.firstName)
}
```

### Not Using Scope Functions

**Problem:** Verbose code that could be more concise.

```kotlin
// Bad: Verbose
val user = User("1", "John")
user.email = "john@example.com"
user.age = 30
database.save(user)

// Good: Apply for configuration
val user = User("1", "John").apply {
    email = "john@example.com"
    age = 30
}
database.save(user)

// Good: Let for transformation
user?.let { u ->
    database.save(u)
}
```

## Go Anti-Patterns

### Ignoring Errors

**Problem:** Most common Go anti-pattern.

```go
// Bad: Ignoring errors
result, _ := doSomething()
file, _ := os.Open("file.txt")

// Good: Handle errors
result, err := doSomething()
if err != nil {
    return fmt.Errorf("failed: %w", err)
}

file, err := os.Open("file.txt")
if err != nil {
    return fmt.Errorf("failed to open file: %w", err)
}
defer file.Close()
```

### Not Using defer

**Problem:** Resources not properly cleaned up.

```go
// Bad: Manual cleanup
file, err := os.Open("file.txt")
if err != nil {
    return err
}
// ... lots of code ...
file.Close()  // Might be forgotten or not reached

// Good: Defer cleanup
file, err := os.Open("file.txt")
if err != nil {
    return err
}
defer file.Close()  // Always executed
```

### Goroutine Leaks

**Problem:** Goroutines never exit, causing memory leaks.

```go
// Bad: Goroutine leak
func process() {
    ch := make(chan int)
    go func() {
        for {
            // Blocks forever if nothing sends to ch
            val := <-ch
            process(val)
        }
    }()
}

// Good: Context for cancellation
func process(ctx context.Context) {
    ch := make(chan int)
    go func() {
        for {
            select {
            case val := <-ch:
                process(val)
            case <-ctx.Done():
                return  // Exit goroutine
            }
        }
    }()
}
```

## Database Anti-Patterns

### N+1 Queries

**Problem:** Multiple queries when one would suffice.

```typescript
// Bad: N+1 queries
const users = await User.findAll();
for (const user of users) {
  user.posts = await Post.findAll({ where: { userId: user.id } });
}

// Good: Single query with join
const users = await User.findAll({
  include: [{ model: Post }]
});
```

### No Indexing

**Problem:** Slow queries on unindexed columns.

```sql
-- Bad: No index on frequently queried column
SELECT * FROM users WHERE email = 'user@example.com';

-- Good: Create index
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';
```

### SELECT *

**Problem:** Fetching unnecessary data.

```sql
-- Bad: Fetching all columns
SELECT * FROM users WHERE id = 1;

-- Good: Specific columns
SELECT id, name, email FROM users WHERE id = 1;
```

## Security Anti-Patterns

### SQL Injection

**Problem:** Unsanitized user input in queries.

```typescript
// Bad: SQL injection vulnerability
const query = `SELECT * FROM users WHERE email = '${userInput}'`;

// Good: Parameterized query
const query = 'SELECT * FROM users WHERE email = ?';
const users = await db.query(query, [userInput]);
```

### Storing Plaintext Passwords

**Problem:** Passwords not hashed.

```python
# Bad: Plaintext password
user.password = request.form['password']

# Good: Hashed password
import bcrypt
password = request.form['password'].encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
user.password = hashed
```

### Exposing Secrets

**Problem:** Secrets in code or logs.

```javascript
// Bad: Hardcoded secrets
const API_KEY = 'sk_live_1234567890';

// Good: Environment variables
const API_KEY = process.env.API_KEY;

// Bad: Logging sensitive data
logger.info(`User logged in: ${user.email}, password: ${user.password}`);

// Good: Don't log sensitive data
logger.info(`User logged in: ${user.email}`);
```

## Performance Anti-Patterns

### Unnecessary Re-renders (React)

**Problem:** Components re-rendering when they don't need to.

```typescript
// Bad: New object/function on every render
function ParentComponent() {
  return <ChildComponent data={{ value: 1 }} onClick={() => {}} />;
}
// ChildComponent re-renders every time even if nothing changed

// Good: Memoization
function ParentComponent() {
  const data = useMemo(() => ({ value: 1 }), []);
  const onClick = useCallback(() => {}, []);
  return <ChildComponent data={data} onClick={onClick} />;
}
```

### Loading Everything Upfront

**Problem:** Loading all data at once.

```typescript
// Bad: Load all users
const users = await User.findAll();  // Could be millions

// Good: Pagination
const users = await User.findAll({
  limit: 20,
  offset: page * 20
});

// Better: Cursor-based pagination
const users = await User.findAll({
  where: { id: { gt: lastSeenId } },
  limit: 20
});
```

## Testing Anti-Patterns

### Testing Implementation Details

**Problem:** Tests break when refactoring without behavior change.

```typescript
// Bad: Testing implementation
test('uses useState', () => {
  const { result } = renderHook(() => useState(0));
  expect(result.current).toEqual([0, expect.any(Function)]);
});

// Good: Testing behavior
test('increments counter when button clicked', () => {
  render(<Counter />);
  fireEvent.click(screen.getByText('Increment'));
  expect(screen.getByText('Count: 1')).toBeInTheDocument();
});
```

### No Test Isolation

**Problem:** Tests depend on each other.

```python
# Bad: Test interdependence
def test_create_user():
    global test_user
    test_user = User.create(name="Test")

def test_update_user():
    test_user.name = "Updated"  # Depends on previous test
    test_user.save()

# Good: Independent tests
def test_create_user():
    user = User.create(name="Test")
    assert user.name == "Test"

def test_update_user():
    user = User.create(name="Test")
    user.name = "Updated"
    user.save()
    assert user.name == "Updated"
```

## Conclusion

Recognizing and avoiding these anti-patterns leads to:
- More maintainable code
- Fewer bugs
- Better performance
- Improved security
- Easier testing

**Key Takeaways:**
- Use proper error handling
- Follow language idioms
- Keep it simple (KISS)
- Don't repeat yourself (DRY)
- Favor composition over inheritance
- Write tests that test behavior, not implementation

Always ask: "Is there a simpler way to solve this problem?"
