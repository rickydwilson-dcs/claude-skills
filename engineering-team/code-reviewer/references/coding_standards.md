# Coding Standards

## Overview

Language-specific coding standards for TypeScript, JavaScript, Python, Swift, Kotlin, and Go. This guide ensures consistent, readable, and maintainable code across projects.

## TypeScript/JavaScript Standards

### Naming Conventions

**Variables and Functions**
```typescript
// camelCase for variables and functions
const userName = 'John';
function calculateTotal(items: Item[]): number {}

// PascalCase for classes and interfaces
class UserService {}
interface UserData {}

// UPPER_SNAKE_CASE for constants
const MAX_RETRY_COUNT = 3;
const API_ENDPOINT = 'https://api.example.com';
```

**Files and Modules**
```
// kebab-case for files
user-service.ts
auth-middleware.ts
api-client.ts

// index.ts for barrel exports
src/
├── services/
│   ├── user-service.ts
│   ├── auth-service.ts
│   └── index.ts  // Re-exports
```

### TypeScript Best Practices

**Prefer Interfaces Over Types**
```typescript
// Prefer interface for object shapes
interface User {
  id: string;
  name: string;
  email: string;
}

// Use type for unions, intersections
type Status = 'pending' | 'active' | 'inactive';
type UserWithStatus = User & { status: Status };
```

**Avoid 'any' - Use Proper Types**
```typescript
// Bad
function processData(data: any) {
  return data.value;
}

// Good - Define proper type
interface DataObject {
  value: string;
  metadata?: Record<string, unknown>;
}

function processData(data: DataObject): string {
  return data.value;
}

// Better - Use generics for flexibility
function processData<T extends { value: string }>(data: T): string {
  return data.value;
}
```

**Strict Null Checks**
```typescript
// Enable in tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true
  }
}

// Handle undefined/null explicitly
function getUser(id: string): User | undefined {
  return users.find(u => u.id === id);
}

// Use at call site
const user = getUser('123');
if (user) {
  console.log(user.name);
}

// Or use optional chaining
console.log(user?.name);
```

### Modern JavaScript Patterns

**Async/Await over Promises**
```typescript
// Bad - Promise chains
function fetchUserData(id: string) {
  return fetch(`/api/users/${id}`)
    .then(response => response.json())
    .then(data => processData(data))
    .catch(error => handleError(error));
}

// Good - Async/await
async function fetchUserData(id: string): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();
    return processData(data);
  } catch (error) {
    handleError(error);
    throw error;
  }
}
```

**Destructuring and Spread**
```typescript
// Object destructuring
const { name, email, ...rest } = user;

// Array destructuring
const [first, second, ...others] = items;

// Function parameters
function createUser({ name, email, role = 'user' }: UserInput) {}

// Spread for immutability
const updatedUser = { ...user, name: 'New Name' };
const newArray = [...oldArray, newItem];
```

**Template Literals**
```typescript
// Bad
const message = 'Hello, ' + user.name + '! You have ' + count + ' messages.';

// Good
const message = `Hello, ${user.name}! You have ${count} messages.`;

// Multiline strings
const html = `
  <div class="user-card">
    <h2>${user.name}</h2>
    <p>${user.email}</p>
  </div>
`;
```

### React-Specific Standards

**Functional Components with Hooks**
```typescript
// Prefer functional components
interface UserProfileProps {
  userId: string;
}

const UserProfile: React.FC<UserProfileProps> = ({ userId }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <Spinner />;
  if (!user) return <NotFound />;

  return <UserCard user={user} />;
};
```

**Custom Hooks for Logic Reuse**
```typescript
function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
}

// Usage
function UserProfile({ userId }: { userId: string }) {
  const { user, loading, error } = useUser(userId);
  // ...
}
```

## Python Standards

### PEP 8 Compliance

**Naming Conventions**
```python
# snake_case for variables and functions
user_name = 'John'
def calculate_total(items):
    pass

# PascalCase for classes
class UserService:
    pass

# UPPER_SNAKE_CASE for constants
MAX_RETRY_COUNT = 3
API_ENDPOINT = 'https://api.example.com'

# Private members with leading underscore
class User:
    def __init__(self, name):
        self._internal_id = generate_id()
        self.name = name
```

**Imports Organization**
```python
# Standard library imports
import os
import sys
from typing import List, Optional

# Third-party imports
import numpy as np
import pandas as pd
from flask import Flask, request

# Local imports
from .models import User
from .services import UserService
```

### Type Hints (Python 3.6+)

```python
from typing import List, Dict, Optional, Union

def get_user(user_id: int) -> Optional[Dict[str, str]]:
    """Fetch user by ID."""
    return database.find_one(user_id)

def process_items(items: List[str], count: int = 10) -> List[str]:
    """Process list of items."""
    return items[:count]

# Generics
from typing import TypeVar, Generic

T = TypeVar('T')

class Repository(Generic[T]):
    def find(self, id: int) -> Optional[T]:
        pass
```

### Pythonic Patterns

**List Comprehensions**
```python
# Bad
squares = []
for x in range(10):
    squares.append(x**2)

# Good
squares = [x**2 for x in range(10)]

# With filter
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
user_map = {user.id: user.name for user in users}
```

**Context Managers**
```python
# Always use with statement for files
with open('file.txt', 'r') as f:
    content = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def database_transaction():
    connection = connect()
    try:
        yield connection
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        connection.close()

# Usage
with database_transaction() as conn:
    conn.execute(query)
```

**f-strings for Formatting**
```python
# Bad
message = "Hello, %s! You have %d messages." % (user.name, count)
message = "Hello, {}! You have {} messages.".format(user.name, count)

# Good
message = f"Hello, {user.name}! You have {count} messages."

# With expressions
message = f"Total: ${sum(prices):.2f}"
```

## Swift Standards

### Naming Conventions

```swift
// camelCase for variables and functions
let userName = "John"
func calculateTotal(items: [Item]) -> Double {}

// PascalCase for types
class UserService {}
struct UserData {}
enum UserStatus {}

// Constants
let maxRetryCount = 3
```

### Optionals Handling

```swift
// Safe unwrapping with if let
if let user = fetchUser(id: userId) {
    print(user.name)
}

// Guard for early exit
guard let user = fetchUser(id: userId) else {
    return
}

// Optional chaining
let email = user?.contact?.email

// Nil coalescing
let name = user?.name ?? "Anonymous"
```

### Protocol-Oriented Design

```swift
// Define protocol
protocol Identifiable {
    var id: String { get }
}

// Conform to protocol
struct User: Identifiable {
    let id: String
    let name: String
}

// Protocol extensions
extension Identifiable {
    func log() {
        print("ID: \(id)")
    }
}
```

## Kotlin Standards

### Null Safety

```kotlin
// Nullable types explicit
var name: String? = null

// Safe calls
val length = name?.length

// Elvis operator
val length = name?.length ?: 0

// Smart casts
if (name != null) {
    println(name.length)  // Auto-cast to non-null
}

// Let function
name?.let {
    println(it.length)
}
```

### Data Classes

```kotlin
// Auto-generates equals, hashCode, toString, copy
data class User(
    val id: String,
    val name: String,
    val email: String
)

// Usage
val user = User("1", "John", "john@example.com")
val updated = user.copy(name = "Jane")
```

### Extension Functions

```kotlin
// Add functionality to existing classes
fun String.isEmail(): Boolean {
    return this.contains("@") && this.contains(".")
}

// Usage
val valid = "test@example.com".isEmail()
```

## Go Standards

### Naming Conventions

```go
// camelCase for private
var userName string
func calculateTotal(items []Item) float64 {}

// PascalCase for public (exported)
type UserService struct {}
func NewUserService() *UserService {}

// Acronyms stay uppercase
var userID string  // not userId
var httpClient *http.Client  // not httpClient
```

### Error Handling

```go
// Always check errors
result, err := doSomething()
if err != nil {
    return nil, fmt.Errorf("failed to do something: %w", err)
}

// Early returns for errors
func processUser(id string) (*User, error) {
    user, err := fetchUser(id)
    if err != nil {
        return nil, err
    }

    if err := validateUser(user); err != nil {
        return nil, err
    }

    return user, nil
}
```

### Interfaces

```go
// Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

// Accept interfaces, return structs
func ProcessData(r Reader) (*Result, error) {
    // Implementation
}
```

## Code Formatting

### Line Length
- TypeScript/JavaScript: 80-100 characters
- Python: 79 characters (PEP 8)
- Swift: 100-120 characters
- Kotlin: 100-120 characters
- Go: 80-120 characters

### Indentation
- TypeScript/JavaScript: 2 spaces
- Python: 4 spaces
- Swift: 4 spaces
- Kotlin: 4 spaces
- Go: Tabs

### File Organization

**TypeScript/JavaScript**
```
src/
├── components/     # React components
├── services/       # Business logic
├── models/         # Types/interfaces
├── utils/          # Helper functions
├── hooks/          # Custom React hooks
└── config/         # Configuration
```

**Python**
```
project/
├── project/        # Main package
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   └── utils.py
├── tests/          # Test files
└── setup.py
```

## Documentation Standards

### JSDoc/TSDoc (TypeScript/JavaScript)

```typescript
/**
 * Calculate the total price of items including tax
 * @param items - Array of items to calculate
 * @param taxRate - Tax rate as decimal (e.g., 0.1 for 10%)
 * @returns Total price including tax
 * @throws {ValidationError} If items array is empty
 */
function calculateTotal(items: Item[], taxRate: number): number {
    // Implementation
}
```

### Docstrings (Python)

```python
def calculate_total(items: List[Item], tax_rate: float) -> float:
    """
    Calculate the total price of items including tax.

    Args:
        items: List of items to calculate
        tax_rate: Tax rate as decimal (e.g., 0.1 for 10%)

    Returns:
        Total price including tax

    Raises:
        ValidationError: If items list is empty
    """
    pass
```

## Linting and Formatting Tools

**TypeScript/JavaScript**
- ESLint for linting
- Prettier for formatting
- TypeScript compiler for type checking

**Python**
- pylint or flake8 for linting
- black for formatting
- mypy for type checking

**Swift**
- SwiftLint for linting

**Kotlin**
- ktlint for linting

**Go**
- go fmt for formatting
- golint for linting
- go vet for analysis

## Conclusion

Consistent coding standards improve:
- Code readability
- Team collaboration
- Code maintenance
- Onboarding efficiency

Use automated tools to enforce standards and focus code reviews on logic and architecture rather than style.
