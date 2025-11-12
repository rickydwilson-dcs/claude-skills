# Best Practices Guide

## Overview

Comprehensive guide to coding standards, testing strategies, security practices, and development workflows for fullstack applications.

## Code Quality

### Writing Clean Code

**SOLID Principles**

**S - Single Responsibility Principle**
- Each class/function does one thing
- Easy to understand and test
- Minimal coupling

**O - Open/Closed Principle**
- Open for extension, closed for modification
- Use interfaces and abstract classes
- Plugin architecture

**L - Liskov Substitution Principle**
- Subtypes must be substitutable for base types
- Maintain behavioral consistency
- Contract-driven development

**I - Interface Segregation Principle**
- Many specific interfaces > one general interface
- Clients shouldn't depend on unused methods
- Focused contracts

**D - Dependency Inversion Principle**
- Depend on abstractions, not concretions
- High-level modules independent of low-level modules
- Dependency injection

### Code Style

**Naming Conventions**
- Use descriptive names
- Variables: camelCase (`userName`)
- Classes: PascalCase (`UserService`)
- Constants: UPPER_SNAKE_CASE (`MAX_RETRIES`)
- Files: kebab-case (`user-service.ts`)

**Function Design**
- Keep functions small (< 20 lines)
- One level of abstraction
- Descriptive names (verbs)
- Pure functions when possible

**Comments**
- Explain "why", not "what"
- Document complex algorithms
- Keep comments up-to-date
- Use JSDoc/TSDoc for documentation

**Code Organization**
```
src/
├── components/       # React components
├── hooks/           # Custom React hooks
├── services/        # Business logic
├── utils/           # Helper functions
├── types/           # TypeScript types
├── config/          # Configuration
└── lib/             # Third-party integrations
```

### Code Review Checklist

**Functionality**
- Does it meet requirements?
- Are edge cases handled?
- Is error handling appropriate?

**Code Quality**
- Follows style guide?
- No code duplication?
- Good naming?
- Appropriate comments?

**Testing**
- Tests included?
- Coverage adequate?
- Edge cases tested?

**Performance**
- Efficient algorithms?
- No N+1 queries?
- Appropriate caching?

**Security**
- Input validation?
- No sensitive data in logs?
- Secure dependencies?

## Testing Strategies

### Testing Pyramid

**Unit Tests (70%)**
- Test individual functions/methods
- Fast execution
- High coverage
- Isolated from dependencies

**Integration Tests (20%)**
- Test component interactions
- Database operations
- API endpoints
- Mock external services

**End-to-end Tests (10%)**
- Test complete user flows
- Real browser testing
- Critical paths only
- Slower but comprehensive

### Unit Testing Best Practices

**AAA Pattern: Arrange, Act, Assert**
```javascript
test('calculates total price', () => {
  // Arrange
  const items = [{ price: 10 }, { price: 20 }];

  // Act
  const total = calculateTotal(items);

  // Assert
  expect(total).toBe(30);
});
```

**Test Naming**
- Descriptive: "should calculate total when items exist"
- Format: "should [expected behavior] when [condition]"

**Test Independence**
- Each test runs in isolation
- No shared state
- Order doesn't matter

**Mock External Dependencies**
```javascript
jest.mock('../services/api');

test('fetches user data', async () => {
  const mockUser = { id: 1, name: 'John' };
  api.getUser.mockResolvedValue(mockUser);

  const user = await fetchUser(1);

  expect(user).toEqual(mockUser);
  expect(api.getUser).toHaveBeenCalledWith(1);
});
```

### Integration Testing

**Database Tests**
- Use test database
- Seed data before tests
- Clean up after tests
- Test transactions

**API Tests**
```javascript
describe('POST /api/users', () => {
  test('creates a user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@example.com' })
      .expect(201);

    expect(response.body).toMatchObject({
      name: 'John',
      email: 'john@example.com'
    });
  });
});
```

### End-to-end Testing

**Critical User Flows**
- User registration/login
- Purchase flow
- Content creation
- Account management

**Best Practices**
- Test happy paths and error scenarios
- Use data attributes for selectors
- Wait for elements properly
- Keep tests maintainable

**Example (Cypress)**
```javascript
describe('Checkout flow', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password');
    cy.visit('/products');
  });

  it('completes purchase', () => {
    cy.get('[data-testid="product-1"]').click();
    cy.get('[data-testid="add-to-cart"]').click();
    cy.get('[data-testid="cart"]').click();
    cy.get('[data-testid="checkout"]').click();

    cy.get('[data-testid="card-number"]').type('4242424242424242');
    cy.get('[data-testid="submit-payment"]').click();

    cy.url().should('include', '/order-confirmation');
    cy.get('[data-testid="order-number"]').should('exist');
  });
});
```

### Test Coverage

**Target Coverage**
- Overall: 80%+
- Critical paths: 100%
- Utils/helpers: 95%+
- UI components: 70%+

**Coverage Tools**
- Istanbul (nyc)
- Jest coverage
- Codecov

**What Not to Test**
- Third-party libraries
- Configuration files
- Type definitions
- Trivial getters/setters

## Performance Optimization

### Frontend Performance

**Code Splitting**
```javascript
// Dynamic imports
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Route-based splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
```

**Memoization**
```javascript
// Expensive computation
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);

// Callback memoization
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

**Image Optimization**
```jsx
// Next.js Image component
<Image
  src="/photo.jpg"
  alt="Photo"
  width={800}
  height={600}
  placeholder="blur"
  loading="lazy"
/>
```

**Virtual Scrolling**
- Render only visible items
- React Virtual, React Window
- Improves performance with large lists

### Backend Performance

**Database Optimization**

**Indexing**
```sql
-- Index frequently queried columns
CREATE INDEX idx_users_email ON users(email);

-- Composite index for multiple columns
CREATE INDEX idx_posts_user_created ON posts(user_id, created_at);
```

**Query Optimization**
- Use EXPLAIN to analyze queries
- Avoid SELECT *
- Use joins instead of multiple queries
- Limit result sets

**N+1 Query Prevention**
```javascript
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

**Caching Strategies**

**In-memory Cache (Redis)**
```javascript
async function getUser(id) {
  // Check cache
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  // Fetch from database
  const user = await User.findByPk(id);

  // Store in cache
  await redis.set(`user:${id}`, JSON.stringify(user), 'EX', 3600);

  return user;
}
```

**CDN for Static Assets**
- CloudFront, Cloudflare
- Edge locations worldwide
- Reduced latency

### API Performance

**Pagination**
```javascript
// Offset-based
GET /api/posts?page=2&limit=20

// Cursor-based (better for large datasets)
GET /api/posts?cursor=abc123&limit=20
```

**Rate Limiting**
```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);
```

**Compression**
```javascript
const compression = require('compression');
app.use(compression());
```

## Security Best Practices

### Authentication

**Password Security**
- Hash passwords (bcrypt, argon2)
- Minimum length: 8 characters
- Enforce complexity
- Salt automatically

```javascript
const bcrypt = require('bcrypt');

// Hashing
const hashedPassword = await bcrypt.hash(password, 10);

// Verification
const isValid = await bcrypt.compare(password, hashedPassword);
```

**JWT Best Practices**
- Short expiration (15 minutes)
- Refresh token pattern
- Secure storage (httpOnly cookies)
- Validate on every request

```javascript
// Generate token
const token = jwt.sign({ userId: user.id }, SECRET, { expiresIn: '15m' });

// Verify token
const decoded = jwt.verify(token, SECRET);
```

### Authorization

**Role-Based Access Control**
```javascript
function requireRole(role) {
  return (req, res, next) => {
    if (!req.user || req.user.role !== role) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

app.delete('/api/users/:id', requireRole('admin'), deleteUser);
```

### Input Validation

**Server-side Validation (Required)**
```javascript
const { body, validationResult } = require('express-validator');

app.post('/api/users',
  body('email').isEmail(),
  body('name').isLength({ min: 2, max: 100 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // Process request
  }
);
```

**SQL Injection Prevention**
```javascript
// Bad: SQL injection vulnerable
const query = `SELECT * FROM users WHERE email = '${email}'`;

// Good: Parameterized query
const query = 'SELECT * FROM users WHERE email = ?';
const users = await db.query(query, [email]);
```

**XSS Prevention**
- Escape user input
- Content Security Policy
- Sanitize HTML

```javascript
const escape = require('escape-html');
const safeContent = escape(userInput);
```

### HTTPS

**Enforce HTTPS**
```javascript
app.use((req, res, next) => {
  if (!req.secure && req.get('x-forwarded-proto') !== 'https') {
    return res.redirect('https://' + req.get('host') + req.url);
  }
  next();
});
```

### Environment Variables

**Never commit secrets**
```bash
# .env (gitignored)
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
JWT_SECRET=your-secret-key
API_KEY=your-api-key
```

**Access in code**
```javascript
const dbUrl = process.env.DATABASE_URL;
```

### CORS Configuration

```javascript
const cors = require('cors');

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS.split(','),
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE']
}));
```

### Dependency Security

**Regular Updates**
```bash
# Check for vulnerabilities
npm audit

# Fix automatically
npm audit fix

# Update dependencies
npm update
```

**Use Security Tools**
- Snyk
- Dependabot
- npm audit
- OWASP Dependency-Check

## Error Handling

### Centralized Error Handling

```javascript
// Error handler middleware
app.use((err, req, res, next) => {
  console.error(err.stack);

  // Don't leak error details in production
  const message = process.env.NODE_ENV === 'production'
    ? 'Internal server error'
    : err.message;

  res.status(err.status || 500).json({
    error: message
  });
});
```

### Custom Error Classes

```javascript
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = 'ValidationError';
    this.status = 400;
  }
}

class NotFoundError extends Error {
  constructor(message) {
    super(message);
    this.name = 'NotFoundError';
    this.status = 404;
  }
}
```

### Error Logging

```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Log errors
logger.error('Error occurred', { error: err, userId: req.user.id });
```

## Documentation

### Code Documentation

**JSDoc/TSDoc**
```typescript
/**
 * Calculate the total price of items in cart
 * @param items - Array of cart items
 * @param taxRate - Tax rate as decimal (e.g., 0.1 for 10%)
 * @returns Total price including tax
 * @throws {ValidationError} If items array is empty
 */
function calculateTotal(items: CartItem[], taxRate: number): number {
  if (items.length === 0) {
    throw new ValidationError('Cart is empty');
  }

  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal * (1 + taxRate);
}
```

### API Documentation

**OpenAPI/Swagger**
```yaml
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
      responses:
        200:
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
```

### README Structure

```markdown
# Project Name

Brief description

## Prerequisites
- Node.js 18+
- PostgreSQL 15+

## Installation
```bash
npm install
cp .env.example .env
```

## Configuration
Environment variables...

## Usage
How to run...

## Testing
How to test...

## Deployment
Deployment instructions...

## Contributing
Contribution guidelines...

## License
License information...
```

## Git Workflow

### Commit Messages

**Conventional Commits**
```
feat: add user authentication
fix: resolve memory leak in data processor
docs: update API documentation
test: add integration tests for payments
refactor: extract validation logic
chore: update dependencies
```

### Branch Strategy

**Main branches**
- main: Production code
- develop: Development code

**Feature branches**
```bash
git checkout -b feature/user-auth develop
# ... work on feature ...
git checkout develop
git merge --no-ff feature/user-auth
```

### Pull Request Checklist

- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No console.log statements
- [ ] Environment variables documented
- [ ] Breaking changes noted

## Deployment

### Pre-deployment Checklist

- [ ] All tests pass
- [ ] Code reviewed and approved
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Monitoring configured
- [ ] Rollback plan defined

### Zero-downtime Deployment

**Blue-Green Deployment**
1. Deploy to new environment (green)
2. Run smoke tests
3. Switch traffic to green
4. Keep blue for rollback

**Database Migrations**
- Make migrations backward compatible
- Run migrations before code deployment
- Test rollback procedures

### Post-deployment

- Monitor error rates
- Check performance metrics
- Verify critical flows
- Review logs

## Monitoring

### Key Metrics

**Application Metrics**
- Request rate
- Error rate
- Response time (p50, p95, p99)
- Throughput

**Business Metrics**
- User signups
- Conversion rate
- Revenue
- Feature adoption

### Alerting

**Alert Conditions**
- Error rate > 1%
- Response time > 2s (p95)
- CPU > 80%
- Memory > 85%
- Disk > 90%

**Alert Channels**
- Email
- Slack
- PagerDuty
- SMS (critical only)

## Maintenance

### Regular Tasks

**Daily**
- Review error logs
- Check performance metrics
- Monitor deployments

**Weekly**
- Review security alerts
- Update dependencies
- Refactor technical debt

**Monthly**
- Review architecture
- Update documentation
- Conduct postmortems

### Technical Debt

**Track Debt**
- Document in issues
- Estimate impact
- Prioritize with features

**Regular Refactoring**
- Allocate 20% time
- Boy Scout Rule (leave code better)
- Incremental improvements

## Conclusion

Following these best practices ensures:
- High code quality
- Strong security
- Good performance
- Easy maintenance
- Team productivity

Remember: Best practices evolve. Stay updated with industry trends and adapt as needed.
