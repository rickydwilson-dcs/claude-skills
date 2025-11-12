# Backend Implementation Templates & Code Examples

Production-ready code templates, migration patterns, testing examples, and implementation guides for backend development.

## Project Setup Templates

### Express + TypeScript + Prisma Starter

**Project Structure:**
```
backend/
├── src/
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   ├── models/
│   ├── middleware/
│   ├── utils/
│   ├── config/
│   └── app.ts
├── prisma/
│   ├── schema.prisma
│   └── migrations/
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── tsconfig.json
├── package.json
└── Dockerfile
```

**package.json:**
```json
{
  "name": "backend-api",
  "version": "1.0.0",
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/app.ts",
    "build": "tsc",
    "start": "node dist/app.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint . --ext .ts",
    "format": "prettier --write \"src/**/*.ts\"",
    "migrate": "prisma migrate dev",
    "migrate:deploy": "prisma migrate deploy",
    "db:seed": "ts-node prisma/seed.ts"
  },
  "dependencies": {
    "express": "^4.18.2",
    "@prisma/client": "^5.0.0",
    "cors": "^2.8.5",
    "helmet": "^7.0.0",
    "express-rate-limit": "^6.8.0",
    "dotenv": "^16.3.1",
    "zod": "^3.21.4",
    "bcrypt": "^5.1.0",
    "jsonwebtoken": "^9.0.1",
    "winston": "^3.9.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.17",
    "@types/node": "^20.4.2",
    "@types/bcrypt": "^5.0.0",
    "@types/jsonwebtoken": "^9.0.2",
    "typescript": "^5.1.6",
    "ts-node": "^10.9.1",
    "ts-node-dev": "^2.0.0",
    "prisma": "^5.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.44.0",
    "prettier": "^3.0.0",
    "jest": "^29.6.1",
    "@types/jest": "^29.5.3",
    "ts-jest": "^29.1.1",
    "supertest": "^6.3.3",
    "@types/supertest": "^2.0.12"
  }
}
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

**Dockerfile:**
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
COPY prisma ./prisma/

RUN npm ci

COPY . .

RUN npm run build
RUN npx prisma generate

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/prisma ./prisma

EXPOSE 3000

CMD ["npm", "start"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - .:/app
      - /app/node_modules

  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
```

## Database Schema Templates

### Prisma Schema

**schema.prisma:**
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  password  String
  role      Role     @default(USER)
  posts     Post[]
  comments  Comment[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
  @@map("users")
}

model Post {
  id          String    @id @default(uuid())
  title       String
  content     String
  published   Boolean   @default(false)
  authorId    String
  author      User      @relation(fields: [authorId], references: [id], onDelete: Cascade)
  comments    Comment[]
  tags        Tag[]
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
  publishedAt DateTime?

  @@index([authorId])
  @@index([published, createdAt])
  @@map("posts")
}

model Comment {
  id        String   @id @default(uuid())
  content   String
  postId    String
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([postId])
  @@index([authorId])
  @@map("comments")
}

model Tag {
  id    String @id @default(uuid())
  name  String @unique
  posts Post[]

  @@map("tags")
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

### Database Migration Template

**Migration File:**
```sql
-- CreateTable
CREATE TABLE "users" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "role" TEXT NOT NULL DEFAULT 'USER',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "posts" (
    "id" TEXT NOT NULL,
    "title" TEXT NOT NULL,
    "content" TEXT NOT NULL,
    "published" BOOLEAN NOT NULL DEFAULT false,
    "authorId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "publishedAt" TIMESTAMP(3),

    CONSTRAINT "posts_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- CreateIndex
CREATE INDEX "users_email_idx" ON "users"("email");

-- CreateIndex
CREATE INDEX "posts_authorId_idx" ON "posts"("authorId");

-- CreateIndex
CREATE INDEX "posts_published_createdAt_idx" ON "posts"("published", "createdAt");

-- AddForeignKey
ALTER TABLE "posts" ADD CONSTRAINT "posts_authorId_fkey" FOREIGN KEY ("authorId") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;
```

## Middleware Templates

### Authentication Middleware

```typescript
// middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { AuthenticationError } from '../errors/authenticationError';

export interface AuthRequest extends Request {
  user?: {
    id: string;
    email: string;
    role: string;
  };
}

export function authenticate(req: AuthRequest, res: Response, next: NextFunction) {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      throw new AuthenticationError('No token provided');
    }

    const token = authHeader.substring(7);
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;

    req.user = {
      id: decoded.id,
      email: decoded.email,
      role: decoded.role
    };

    next();
  } catch (error) {
    if (error instanceof jwt.JsonWebTokenError) {
      next(new AuthenticationError('Invalid token'));
    } else {
      next(error);
    }
  }
}

export function authorize(...roles: string[]) {
  return (req: AuthRequest, res: Response, next: NextFunction) => {
    if (!req.user) {
      return next(new AuthenticationError());
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        error: { message: 'Insufficient permissions' }
      });
    }

    next();
  };
}
```

### Validation Middleware

```typescript
// middleware/validation.ts
import { Request, Response, NextFunction } from 'express';
import { z } from 'zod';
import { ValidationError } from '../errors/validationError';

export function validate(schema: z.ZodSchema) {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = await schema.parseAsync(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        const fields = error.errors.map(err => ({
          field: err.path.join('.'),
          message: err.message
        }));

        next(new ValidationError('Validation failed', fields));
      } else {
        next(error);
      }
    }
  };
}

// schemas/userSchemas.ts
import { z } from 'zod';

export const createUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
  password: z.string().min(8).max(100)
});

export const updateUserSchema = z.object({
  name: z.string().min(2).max(100).optional(),
  email: z.string().email().optional()
});

export const loginSchema = z.object({
  email: z.string().email(),
  password: z.string()
});
```

### Rate Limiting Middleware

```typescript
// middleware/rateLimiter.ts
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

export const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:api:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests, please try again later',
  standardHeaders: true,
  legacyHeaders: false
});

export const authLimiter = rateLimit({
  store: new RedisStore({
    client: redis,
    prefix: 'rl:auth:'
  }),
  windowMs: 15 * 60 * 1000,
  max: 5, // Limit login attempts
  message: 'Too many login attempts, please try again later',
  skipSuccessfulRequests: true
});
```

### Logging Middleware

```typescript
// middleware/logger.ts
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'backend-api' },
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    })
  ]
});

export function requestLogger(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;

    logger.info('HTTP Request', {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: `${duration}ms`,
      ip: req.ip,
      userAgent: req.get('user-agent')
    });
  });

  next();
}
```

## Service Implementation Templates

### Authentication Service

```typescript
// services/authService.ts
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { UserRepository } from '../repositories/userRepository';
import { AuthenticationError } from '../errors/authenticationError';
import { ValidationError } from '../errors/validationError';

export class AuthService {
  constructor(
    private userRepository: UserRepository,
    private jwtSecret: string = process.env.JWT_SECRET!,
    private jwtExpiry: string = process.env.JWT_EXPIRY || '7d'
  ) {}

  async register(data: RegisterDTO) {
    // Check if user exists
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
      throw new ValidationError('Email already registered', [
        { field: 'email', message: 'Email already in use' }
      ]);
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(data.password, 10);

    // Create user
    const user = await this.userRepository.create({
      ...data,
      password: hashedPassword
    });

    // Generate token
    const token = this.generateToken(user);

    return { user, token };
  }

  async login(email: string, password: string) {
    // Find user
    const user = await this.userRepository.findByEmailWithPassword(email);
    if (!user) {
      throw new AuthenticationError('Invalid credentials');
    }

    // Verify password
    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      throw new AuthenticationError('Invalid credentials');
    }

    // Generate token
    const token = this.generateToken(user);

    // Remove password from response
    const { password: _, ...userWithoutPassword } = user;

    return { user: userWithoutPassword, token };
  }

  async verifyToken(token: string) {
    try {
      const decoded = jwt.verify(token, this.jwtSecret) as any;
      const user = await this.userRepository.findById(decoded.id);

      if (!user) {
        throw new AuthenticationError('User not found');
      }

      return user;
    } catch (error) {
      throw new AuthenticationError('Invalid token');
    }
  }

  async refreshToken(oldToken: string) {
    const user = await this.verifyToken(oldToken);
    return this.generateToken(user);
  }

  private generateToken(user: { id: string; email: string; role: string }) {
    return jwt.sign(
      {
        id: user.id,
        email: user.email,
        role: user.role
      },
      this.jwtSecret,
      { expiresIn: this.jwtExpiry }
    );
  }
}
```

### Email Service

```typescript
// services/emailService.ts
import nodemailer from 'nodemailer';

export class EmailService {
  private transporter: nodemailer.Transporter;

  constructor() {
    this.transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT || '587'),
      secure: false,
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
      }
    });
  }

  async sendWelcomeEmail(to: string, name: string) {
    await this.transporter.sendMail({
      from: process.env.FROM_EMAIL,
      to,
      subject: 'Welcome to Our Platform',
      html: `
        <h1>Welcome ${name}!</h1>
        <p>Thank you for signing up.</p>
      `
    });
  }

  async sendPasswordResetEmail(to: string, resetToken: string) {
    const resetUrl = `${process.env.FRONTEND_URL}/reset-password?token=${resetToken}`;

    await this.transporter.sendMail({
      from: process.env.FROM_EMAIL,
      to,
      subject: 'Password Reset Request',
      html: `
        <h1>Password Reset</h1>
        <p>Click the link below to reset your password:</p>
        <a href="${resetUrl}">${resetUrl}</a>
        <p>This link expires in 1 hour.</p>
      `
    });
  }
}
```

## Testing Templates

### Unit Test Template

```typescript
// tests/unit/userService.test.ts
import { UserService } from '../../src/services/userService';
import { UserRepository } from '../../src/repositories/userRepository';
import { ValidationError } from '../../src/errors/validationError';

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockUserRepository = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn()
    } as any;

    userService = new UserService(mockUserRepository);
  });

  describe('createUser', () => {
    const validInput = {
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123'
    };

    it('should create user successfully', async () => {
      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockUserRepository.create.mockResolvedValue({
        id: '123',
        name: validInput.name,
        email: validInput.email,
        role: 'USER',
        createdAt: new Date(),
        updatedAt: new Date()
      });

      const result = await userService.createUser(validInput);

      expect(result).toBeDefined();
      expect(result.email).toBe(validInput.email);
      expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(validInput.email);
      expect(mockUserRepository.create).toHaveBeenCalled();
    });

    it('should throw ValidationError if email exists', async () => {
      mockUserRepository.findByEmail.mockResolvedValue({
        id: '123',
        email: validInput.email
      } as any);

      await expect(userService.createUser(validInput)).rejects.toThrow(ValidationError);
      expect(mockUserRepository.create).not.toHaveBeenCalled();
    });
  });

  describe('getUserById', () => {
    it('should return user if found', async () => {
      const user = {
        id: '123',
        name: 'John Doe',
        email: 'john@example.com',
        role: 'USER',
        createdAt: new Date(),
        updatedAt: new Date()
      };

      mockUserRepository.findById.mockResolvedValue(user);

      const result = await userService.getUserById('123');

      expect(result).toEqual(user);
      expect(mockUserRepository.findById).toHaveBeenCalledWith('123');
    });

    it('should return null if user not found', async () => {
      mockUserRepository.findById.mockResolvedValue(null);

      const result = await userService.getUserById('999');

      expect(result).toBeNull();
    });
  });
});
```

### Integration Test Template

```typescript
// tests/integration/userApi.test.ts
import request from 'supertest';
import app from '../../src/app';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

describe('User API Integration Tests', () => {
  beforeAll(async () => {
    await prisma.$connect();
  });

  afterAll(async () => {
    await prisma.user.deleteMany();
    await prisma.$disconnect();
  });

  beforeEach(async () => {
    await prisma.user.deleteMany();
  });

  describe('POST /api/users', () => {
    it('should create new user', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data.email).toBe(userData.email);
      expect(response.body.data).not.toHaveProperty('password');

      // Verify in database
      const user = await prisma.user.findUnique({
        where: { email: userData.email }
      });
      expect(user).toBeDefined();
    });

    it('should return 422 for duplicate email', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123'
      };

      // Create first user
      await request(app).post('/api/users').send(userData).expect(201);

      // Try to create duplicate
      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(422);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });

    it('should return 422 for invalid email', async () => {
      const userData = {
        name: 'John Doe',
        email: 'invalid-email',
        password: 'password123'
      };

      const response = await request(app)
        .post('/api/users')
        .send(userData)
        .expect(422);

      expect(response.body.success).toBe(false);
    });
  });

  describe('GET /api/users/:id', () => {
    it('should return user by id', async () => {
      // Create user first
      const createResponse = await request(app)
        .post('/api/users')
        .send({
          name: 'John Doe',
          email: 'john@example.com',
          password: 'password123'
        });

      const userId = createResponse.body.data.id;

      // Get user
      const response = await request(app)
        .get(`/api/users/${userId}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.id).toBe(userId);
      expect(response.body.data.email).toBe('john@example.com');
    });

    it('should return 404 for non-existent user', async () => {
      const response = await request(app)
        .get('/api/users/non-existent-id')
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('NOT_FOUND');
    });
  });

  describe('Authentication', () => {
    it('should register and login user', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123'
      };

      // Register
      const registerResponse = await request(app)
        .post('/api/auth/register')
        .send(userData)
        .expect(201);

      expect(registerResponse.body.data).toHaveProperty('token');
      const token = registerResponse.body.data.token;

      // Login
      const loginResponse = await request(app)
        .post('/api/auth/login')
        .send({
          email: userData.email,
          password: userData.password
        })
        .expect(200);

      expect(loginResponse.body.data).toHaveProperty('token');

      // Access protected route
      const meResponse = await request(app)
        .get('/api/auth/me')
        .set('Authorization', `Bearer ${token}`)
        .expect(200);

      expect(meResponse.body.data.email).toBe(userData.email);
    });
  });
});
```

## API Route Templates

### RESTful Routes

```typescript
// routes/userRoutes.ts
import { Router } from 'express';
import { UserController } from '../controllers/userController';
import { authenticate, authorize } from '../middleware/auth';
import { validate } from '../middleware/validation';
import { createUserSchema, updateUserSchema } from '../schemas/userSchemas';

const router = Router();
const controller = new UserController();

// Public routes
router.post('/users',
  validate(createUserSchema),
  controller.create
);

// Protected routes
router.use(authenticate);

router.get('/users',
  authorize('ADMIN'),
  controller.list
);

router.get('/users/:id',
  controller.getById
);

router.put('/users/:id',
  validate(updateUserSchema),
  controller.update
);

router.delete('/users/:id',
  authorize('ADMIN'),
  controller.delete
);

export default router;
```

### GraphQL Resolvers

```typescript
// resolvers/userResolvers.ts
import { UserService } from '../services/userService';
import { AuthenticationError } from '../errors/authenticationError';

export const userResolvers = {
  Query: {
    user: async (_: any, { id }: { id: string }, context: any) => {
      if (!context.user) {
        throw new AuthenticationError();
      }
      return context.services.userService.getUserById(id);
    },

    users: async (_: any, { limit, offset }: any, context: any) => {
      if (!context.user || context.user.role !== 'ADMIN') {
        throw new AuthenticationError('Admin access required');
      }
      return context.services.userService.getUsers({ limit, offset });
    }
  },

  Mutation: {
    createUser: async (_: any, { input }: any, context: any) => {
      return context.services.userService.createUser(input);
    },

    updateUser: async (_: any, { id, input }: any, context: any) => {
      if (!context.user || (context.user.id !== id && context.user.role !== 'ADMIN')) {
        throw new AuthenticationError('Unauthorized');
      }
      return context.services.userService.updateUser(id, input);
    }
  },

  User: {
    posts: async (user: any, _: any, context: any) => {
      return context.services.postService.getPostsByUserId(user.id);
    }
  }
};
```

## Environment Configuration

**.env.example:**
```env
# Server
NODE_ENV=development
PORT=3000
API_VERSION=v1

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/mydb

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRY=7d

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
FROM_EMAIL=noreply@yourapp.com

# Frontend
FRONTEND_URL=http://localhost:3001

# Logging
LOG_LEVEL=info

# Rate Limiting
RATE_LIMIT_WINDOW=15
RATE_LIMIT_MAX=100

# Cloudinary (for file uploads)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

This comprehensive template collection provides production-ready code patterns and examples for building robust backend systems.
