# Backend Architecture Frameworks & Design Patterns

Comprehensive guide to backend architecture patterns, API design principles, and system design methodologies for building scalable, maintainable backend systems.

## API Design Patterns

### REST API Design Principles

**Resource-Based URL Structure:**
```
GET    /api/v1/users           # List all users
GET    /api/v1/users/:id       # Get specific user
POST   /api/v1/users           # Create user
PUT    /api/v1/users/:id       # Update user (full)
PATCH  /api/v1/users/:id       # Update user (partial)
DELETE /api/v1/users/:id       # Delete user

# Nested resources
GET    /api/v1/users/:id/posts          # User's posts
GET    /api/v1/posts/:id/comments       # Post's comments
```

**HTTP Status Codes:**
- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing/invalid auth
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource doesn't exist
- `409 Conflict`: Resource already exists
- `422 Unprocessable Entity`: Validation errors
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Temporary downtime

**Response Format:**
```json
{
  "success": true,
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150
  }
}
```

**Error Response Format:**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### GraphQL API Design

**Schema Design Principles:**
```graphql
# Type definitions
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
  published: Boolean!
  createdAt: DateTime!
}

# Queries
type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
  posts(userId: ID, published: Boolean): [Post!]!
}

# Mutations
type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!

  createPost(input: CreatePostInput!): Post!
  publishPost(id: ID!): Post!
}

# Input types
input CreateUserInput {
  name: String!
  email: String!
  password: String!
}

input UpdateUserInput {
  name: String
  email: String
}
```

**Resolver Pattern:**
```typescript
// Efficient N+1 query prevention with DataLoader
const userLoader = new DataLoader(async (ids: string[]) => {
  const users = await User.findByIds(ids);
  return ids.map(id => users.find(u => u.id === id));
});

const resolvers = {
  Query: {
    user: async (_: any, { id }: { id: string }) => {
      return userLoader.load(id);
    },
    users: async (_: any, { limit = 20, offset = 0 }) => {
      return User.findAll({ limit, offset });
    }
  },

  User: {
    posts: async (user: User) => {
      return Post.findByUserId(user.id);
    }
  },

  Mutation: {
    createUser: async (_: any, { input }: { input: CreateUserInput }) => {
      const user = await User.create(input);
      return user;
    }
  }
};
```

**Error Handling:**
```typescript
import { ApolloError, UserInputError, AuthenticationError } from 'apollo-server';

// Custom error classes
class NotFoundError extends ApolloError {
  constructor(message: string) {
    super(message, 'NOT_FOUND');
  }
}

// In resolvers
const user = await User.findById(id);
if (!user) {
  throw new NotFoundError(`User ${id} not found`);
}

// Validation errors
if (!isValidEmail(input.email)) {
  throw new UserInputError('Invalid email format', {
    invalidArgs: ['email']
  });
}
```

## Architecture Patterns

### Layered Architecture

**Structure:**
```
src/
├── controllers/      # HTTP handlers, route logic
├── services/         # Business logic
├── repositories/     # Data access layer
├── models/           # Data models/entities
├── middleware/       # Express middleware
├── utils/            # Helper functions
└── config/           # Configuration
```

**Controller Layer:**
```typescript
// controllers/userController.ts
import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/userService';

export class UserController {
  constructor(private userService: UserService) {}

  async getUser(req: Request, res: Response, next: NextFunction) {
    try {
      const { id } = req.params;
      const user = await this.userService.getUserById(id);

      if (!user) {
        return res.status(404).json({
          success: false,
          error: { message: 'User not found' }
        });
      }

      res.json({
        success: true,
        data: user
      });
    } catch (error) {
      next(error);
    }
  }

  async createUser(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await this.userService.createUser(req.body);
      res.status(201).json({
        success: true,
        data: user
      });
    } catch (error) {
      next(error);
    }
  }
}
```

**Service Layer:**
```typescript
// services/userService.ts
import { UserRepository } from '../repositories/userRepository';
import { hash } from 'bcrypt';

export class UserService {
  constructor(private userRepository: UserRepository) {}

  async getUserById(id: string) {
    return this.userRepository.findById(id);
  }

  async createUser(data: CreateUserDTO) {
    // Business logic validation
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
      throw new Error('Email already exists');
    }

    // Hash password
    const hashedPassword = await hash(data.password, 10);

    // Create user
    return this.userRepository.create({
      ...data,
      password: hashedPassword
    });
  }

  async updateUser(id: string, data: UpdateUserDTO) {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new Error('User not found');
    }

    return this.userRepository.update(id, data);
  }
}
```

**Repository Layer:**
```typescript
// repositories/userRepository.ts
import { PrismaClient } from '@prisma/client';

export class UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string) {
    return this.prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        name: true,
        email: true,
        createdAt: true,
        // Exclude password
      }
    });
  }

  async findByEmail(email: string) {
    return this.prisma.user.findUnique({
      where: { email }
    });
  }

  async create(data: CreateUserData) {
    return this.prisma.user.create({
      data,
      select: {
        id: true,
        name: true,
        email: true,
        createdAt: true
      }
    });
  }

  async update(id: string, data: UpdateUserData) {
    return this.prisma.user.update({
      where: { id },
      data,
      select: {
        id: true,
        name: true,
        email: true,
        updatedAt: true
      }
    });
  }
}
```

### Dependency Injection Pattern

**Setup with TypeDI:**
```typescript
// container.ts
import { Container } from 'typedi';
import { PrismaClient } from '@prisma/client';
import { UserRepository } from './repositories/userRepository';
import { UserService } from './services/userService';
import { UserController } from './controllers/userController';

// Register dependencies
Container.set('prisma', new PrismaClient());
Container.set(UserRepository, new UserRepository(Container.get('prisma')));
Container.set(UserService, new UserService(Container.get(UserRepository)));
Container.set(UserController, new UserController(Container.get(UserService)));
```

**Usage in Routes:**
```typescript
// routes/userRoutes.ts
import { Router } from 'express';
import { Container } from 'typedi';
import { UserController } from '../controllers/userController';

const router = Router();
const controller = Container.get(UserController);

router.get('/users/:id', (req, res, next) =>
  controller.getUser(req, res, next)
);
router.post('/users', (req, res, next) =>
  controller.createUser(req, res, next)
);

export default router;
```

### Repository Pattern

**Generic Repository:**
```typescript
// repositories/baseRepository.ts
export abstract class BaseRepository<T> {
  constructor(protected prisma: PrismaClient, protected model: string) {}

  async findById(id: string): Promise<T | null> {
    return this.prisma[this.model].findUnique({ where: { id } });
  }

  async findAll(options?: FindOptions): Promise<T[]> {
    return this.prisma[this.model].findMany({
      skip: options?.offset,
      take: options?.limit,
      where: options?.where,
      orderBy: options?.orderBy
    });
  }

  async create(data: Partial<T>): Promise<T> {
    return this.prisma[this.model].create({ data });
  }

  async update(id: string, data: Partial<T>): Promise<T> {
    return this.prisma[this.model].update({
      where: { id },
      data
    });
  }

  async delete(id: string): Promise<T> {
    return this.prisma[this.model].delete({ where: { id } });
  }
}
```

### CQRS Pattern (Command Query Responsibility Segregation)

**Separate Read and Write Models:**
```typescript
// commands/createUserCommand.ts
export class CreateUserCommand {
  constructor(
    public readonly name: string,
    public readonly email: string,
    public readonly password: string
  ) {}
}

// commandHandlers/createUserHandler.ts
export class CreateUserHandler {
  async execute(command: CreateUserCommand) {
    // Validation
    if (!isValidEmail(command.email)) {
      throw new ValidationError('Invalid email');
    }

    // Business logic
    const hashedPassword = await hash(command.password, 10);

    // Persist
    const user = await this.userRepository.create({
      name: command.name,
      email: command.email,
      password: hashedPassword
    });

    // Emit event
    await this.eventBus.publish(new UserCreatedEvent(user));

    return user;
  }
}

// queries/getUserQuery.ts
export class GetUserQuery {
  constructor(public readonly id: string) {}
}

// queryHandlers/getUserHandler.ts
export class GetUserHandler {
  async execute(query: GetUserQuery) {
    // Read from optimized read model
    return this.userReadRepository.findById(query.id);
  }
}
```

## Microservices Patterns

### Service Communication

**Synchronous (REST):**
```typescript
// Service A calling Service B
import axios from 'axios';

class OrderService {
  async createOrder(userId: string, items: Item[]) {
    // Call User Service to validate user
    const user = await axios.get(`${USER_SERVICE_URL}/users/${userId}`);

    if (!user.data) {
      throw new Error('User not found');
    }

    // Call Inventory Service to check stock
    const inventory = await axios.post(`${INVENTORY_SERVICE_URL}/check`, {
      items
    });

    if (!inventory.data.available) {
      throw new Error('Items out of stock');
    }

    // Create order
    return this.orderRepository.create({
      userId,
      items,
      status: 'pending'
    });
  }
}
```

**Asynchronous (Message Queue):**
```typescript
// Using RabbitMQ
import amqp from 'amqplib';

class EventPublisher {
  async publishOrderCreated(order: Order) {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();

    await channel.assertExchange('orders', 'topic', { durable: true });

    channel.publish(
      'orders',
      'order.created',
      Buffer.from(JSON.stringify(order)),
      { persistent: true }
    );

    await channel.close();
    await connection.close();
  }
}

class OrderCreatedConsumer {
  async consume() {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();

    await channel.assertExchange('orders', 'topic', { durable: true });
    const queue = await channel.assertQueue('', { exclusive: true });

    await channel.bindQueue(queue.queue, 'orders', 'order.created');

    channel.consume(queue.queue, async (msg) => {
      if (msg) {
        const order = JSON.parse(msg.content.toString());
        await this.handleOrderCreated(order);
        channel.ack(msg);
      }
    });
  }

  private async handleOrderCreated(order: Order) {
    // Handle event (e.g., send email, update inventory)
  }
}
```

### Circuit Breaker Pattern

**Prevent cascading failures:**
```typescript
class CircuitBreaker {
  private failures = 0;
  private lastFailTime = 0;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  constructor(
    private threshold = 5,
    private timeout = 60000,
    private halfOpenRequests = 3
  ) {}

  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailTime >= this.timeout) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = 'closed';
  }

  private onFailure() {
    this.failures++;
    this.lastFailTime = Date.now();

    if (this.failures >= this.threshold) {
      this.state = 'open';
    }
  }
}

// Usage
const breaker = new CircuitBreaker();

async function callExternalService() {
  return breaker.call(async () => {
    return axios.get('https://external-api.com/data');
  });
}
```

### API Gateway Pattern

**Single entry point for multiple microservices:**
```typescript
// gateway/routes.ts
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';

const app = express();

// User Service
app.use('/api/users', createProxyMiddleware({
  target: 'http://user-service:3001',
  changeOrigin: true,
  pathRewrite: { '^/api/users': '/users' }
}));

// Order Service
app.use('/api/orders', createProxyMiddleware({
  target: 'http://order-service:3002',
  changeOrigin: true,
  pathRewrite: { '^/api/orders': '/orders' }
}));

// Product Service
app.use('/api/products', createProxyMiddleware({
  target: 'http://product-service:3003',
  changeOrigin: true,
  pathRewrite: { '^/api/products': '/products' }
}));
```

## Performance Patterns

### Caching Strategies

**Redis Caching:**
```typescript
import Redis from 'ioredis';

class CacheService {
  private redis = new Redis();

  async get<T>(key: string): Promise<T | null> {
    const value = await this.redis.get(key);
    return value ? JSON.parse(value) : null;
  }

  async set(key: string, value: any, ttl = 3600) {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }

  async del(key: string) {
    await this.redis.del(key);
  }
}

// Cache-aside pattern
class UserService {
  async getUserById(id: string) {
    // Try cache first
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return cached;

    // Fetch from database
    const user = await this.userRepository.findById(id);

    // Store in cache
    if (user) {
      await this.cache.set(`user:${id}`, user, 3600);
    }

    return user;
  }
}
```

**Cache Invalidation:**
```typescript
class UserService {
  async updateUser(id: string, data: UpdateUserDTO) {
    // Update database
    const user = await this.userRepository.update(id, data);

    // Invalidate cache
    await this.cache.del(`user:${id}`);

    return user;
  }
}
```

### Database Query Optimization

**N+1 Query Prevention:**
```typescript
// Bad: N+1 queries
const users = await User.findAll();
for (const user of users) {
  const posts = await Post.findByUserId(user.id); // N queries
}

// Good: Single query with join
const users = await prisma.user.findMany({
  include: {
    posts: true
  }
});
```

**Pagination:**
```typescript
// Offset-based (simple but slow for large datasets)
async function getUsers(page: number, limit: number) {
  return prisma.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
    orderBy: { createdAt: 'desc' }
  });
}

// Cursor-based (efficient for large datasets)
async function getUsersCursor(cursor?: string, limit = 20) {
  return prisma.user.findMany({
    take: limit,
    ...(cursor && {
      cursor: { id: cursor },
      skip: 1
    }),
    orderBy: { createdAt: 'desc' }
  });
}
```

### Connection Pooling

**PostgreSQL Connection Pool:**
```typescript
import { Pool } from 'pg';

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,                    // Maximum connections
  idleTimeoutMillis: 30000,   // Close idle connections after 30s
  connectionTimeoutMillis: 2000
});

// Use pool for queries
export async function query(text: string, params?: any[]) {
  const client = await pool.connect();
  try {
    return await client.query(text, params);
  } finally {
    client.release();
  }
}
```

## Error Handling Patterns

### Custom Error Classes

```typescript
// errors/baseError.ts
export abstract class BaseError extends Error {
  constructor(
    public message: string,
    public statusCode: number,
    public code: string
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// errors/notFoundError.ts
export class NotFoundError extends BaseError {
  constructor(resource: string, id: string) {
    super(`${resource} ${id} not found`, 404, 'NOT_FOUND');
  }
}

// errors/validationError.ts
export class ValidationError extends BaseError {
  constructor(
    message: string,
    public fields: { field: string; message: string }[]
  ) {
    super(message, 422, 'VALIDATION_ERROR');
  }
}

// errors/authenticationError.ts
export class AuthenticationError extends BaseError {
  constructor(message = 'Authentication required') {
    super(message, 401, 'AUTHENTICATION_ERROR');
  }
}
```

### Global Error Handler

```typescript
// middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express';
import { BaseError } from '../errors/baseError';

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error
  console.error('Error:', {
    message: err.message,
    stack: err.stack,
    path: req.path,
    method: req.method
  });

  // Handle known errors
  if (err instanceof BaseError) {
    return res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message
      }
    });
  }

  // Handle unknown errors
  res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
}
```

## Testing Strategies

### Unit Testing

```typescript
// userService.test.ts
import { UserService } from '../services/userService';
import { UserRepository } from '../repositories/userRepository';

describe('UserService', () => {
  let userService: UserService;
  let userRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    userRepository = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      create: jest.fn(),
      update: jest.fn()
    } as any;

    userService = new UserService(userRepository);
  });

  describe('createUser', () => {
    it('should create user with hashed password', async () => {
      const input = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123'
      };

      userRepository.findByEmail.mockResolvedValue(null);
      userRepository.create.mockResolvedValue({
        id: '123',
        ...input,
        password: 'hashed'
      });

      const user = await userService.createUser(input);

      expect(user).toBeDefined();
      expect(userRepository.findByEmail).toHaveBeenCalledWith(input.email);
      expect(userRepository.create).toHaveBeenCalled();
    });

    it('should throw error if email exists', async () => {
      const input = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123'
      };

      userRepository.findByEmail.mockResolvedValue({ id: '123' } as any);

      await expect(userService.createUser(input)).rejects.toThrow('Email already exists');
    });
  });
});
```

### Integration Testing

```typescript
// userController.integration.test.ts
import request from 'supertest';
import app from '../app';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

describe('User API', () => {
  beforeAll(async () => {
    // Setup test database
    await prisma.$connect();
  });

  afterAll(async () => {
    // Cleanup
    await prisma.user.deleteMany();
    await prisma.$disconnect();
  });

  describe('POST /api/users', () => {
    it('should create new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          name: 'John Doe',
          email: 'john@example.com',
          password: 'password123'
        })
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data.email).toBe('john@example.com');
    });

    it('should return 422 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          name: 'John Doe',
          email: 'invalid-email',
          password: 'password123'
        })
        .expect(422);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });
});
```

## Documentation Standards

### API Documentation with Swagger/OpenAPI

```typescript
/**
 * @swagger
 * /api/users:
 *   post:
 *     summary: Create new user
 *     tags: [Users]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - name
 *               - email
 *               - password
 *             properties:
 *               name:
 *                 type: string
 *                 example: John Doe
 *               email:
 *                 type: string
 *                 format: email
 *                 example: john@example.com
 *               password:
 *                 type: string
 *                 format: password
 *     responses:
 *       201:
 *         description: User created successfully
 *       422:
 *         description: Validation error
 */
router.post('/users', userController.createUser);
```

This comprehensive framework guide provides the foundation for building scalable, maintainable backend systems using modern patterns and best practices.
