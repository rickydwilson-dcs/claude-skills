#!/usr/bin/env python3
"""
API Scaffolder
REST/GraphQL endpoint generation tool with OpenAPI spec parsing and CRUD boilerplate.

Features:
- REST and GraphQL API project scaffolding
- OpenAPI/Swagger spec parsing for endpoint generation
- Express/TypeScript project templates
- Authentication middleware scaffolding
- Docker and CI/CD configuration
- Database schema templates (Prisma)

Standard library only - no external dependencies required.
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class EndpointConfig:
    """Configuration for an API endpoint"""
    path: str
    method: str
    name: str
    description: str = ""
    request_body: Optional[Dict] = None
    response_schema: Optional[Dict] = None
    auth_required: bool = True


@dataclass
class ProjectConfig:
    """Configuration for the API project"""
    name: str
    api_type: str  # rest or graphql
    stack: str  # express-typescript, fastify-typescript, nestjs
    include_auth: bool = True
    include_docker: bool = True
    include_ci: bool = True
    database: str = "postgres"
    endpoints: List[EndpointConfig] = field(default_factory=list)


class APIScaffolder:
    """
    API project scaffolding tool for generating production-ready backends.
    """

    def __init__(self, config: ProjectConfig, output_dir: str, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("APIScaffolder initialized")

        self.config = config
        self.output_dir = Path(output_dir)
        self.verbose = verbose
        self.files_created: List[str] = []

    def scaffold(self) -> Dict[str, Any]:
        """Generate the complete project structure"""
        logger.debug(f"Scaffolding {self.config.api_type} API: {self.config.name}")
        if self.verbose:
            print(f"Scaffolding {self.config.api_type.upper()} API: {self.config.name}")
            print(f"Stack: {self.config.stack}")
            print(f"Output: {self.output_dir}\n")

        # Create project directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Generate base structure
        self._create_directory_structure()
        self._create_package_json()
        self._create_tsconfig()
        self._create_env_files()

        # Generate source code
        if self.config.api_type == "graphql":
            self._create_graphql_structure()
        else:
            self._create_rest_structure()

        # Generate database schema
        self._create_prisma_schema()

        # Generate optional components
        if self.config.include_auth:
            self._create_auth_middleware()

        if self.config.include_docker:
            self._create_docker_config()

        if self.config.include_ci:
            self._create_ci_config()

        # Generate tests
        self._create_test_structure()

        # Create README
        self._create_readme()

        return {
            "status": "success",
            "project_name": self.config.name,
            "api_type": self.config.api_type,
            "stack": self.config.stack,
            "output_directory": str(self.output_dir),
            "files_created": len(self.files_created),
            "files": self.files_created
        }

    def _write_file(self, relative_path: str, content: str):
        """Write a file and track it"""
        file_path = self.output_dir / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        self.files_created.append(relative_path)
        if self.verbose:
            print(f"  Created: {relative_path}")

    def _create_directory_structure(self):
        """Create base directory structure"""
        logger.debug("Creating directory structure")
        dirs = [
            "src/controllers", "src/services", "src/repositories",
            "src/middleware", "src/routes", "src/utils", "src/types",
            "src/config", "tests/unit", "tests/integration", "prisma"
        ]
        if self.config.api_type == "graphql":
            dirs.extend(["src/graphql/resolvers", "src/graphql/types", "src/graphql/loaders"])

        for d in dirs:
            (self.output_dir / d).mkdir(parents=True, exist_ok=True)

    def _create_package_json(self):
        """Generate package.json"""
        deps = {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "helmet": "^7.1.0",
            "compression": "^1.7.4",
            "dotenv": "^16.3.1",
            "@prisma/client": "^5.7.0",
            "zod": "^3.22.4"
        }

        dev_deps = {
            "typescript": "^5.3.3",
            "@types/node": "^20.10.0",
            "@types/express": "^4.17.21",
            "@types/cors": "^2.8.17",
            "@types/compression": "^1.7.5",
            "prisma": "^5.7.0",
            "tsx": "^4.6.2",
            "jest": "^29.7.0",
            "@types/jest": "^29.5.11",
            "ts-jest": "^29.1.1",
            "supertest": "^6.3.3",
            "@types/supertest": "^6.0.2"
        }

        if self.config.include_auth:
            deps.update({
                "jsonwebtoken": "^9.0.2",
                "bcryptjs": "^2.4.3"
            })
            dev_deps.update({
                "@types/jsonwebtoken": "^9.0.5",
                "@types/bcryptjs": "^2.4.6"
            })

        if self.config.api_type == "graphql":
            deps.update({
                "@apollo/server": "^4.10.0",
                "graphql": "^16.8.1",
                "dataloader": "^2.2.2"
            })

        scripts = {
            "dev": "tsx watch src/index.ts",
            "build": "tsc",
            "start": "node dist/index.js",
            "test": "jest",
            "test:watch": "jest --watch",
            "test:coverage": "jest --coverage",
            "migrate": "prisma migrate dev",
            "migrate:prod": "prisma migrate deploy",
            "db:seed": "tsx prisma/seed.ts",
            "db:studio": "prisma studio",
            "lint": "eslint src --ext .ts"
        }

        package = {
            "name": self.config.name,
            "version": "1.0.0",
            "description": f"{self.config.api_type.upper()} API generated by API Scaffolder",
            "main": "dist/index.js",
            "scripts": scripts,
            "dependencies": deps,
            "devDependencies": dev_deps,
            "engines": {"node": ">=18.0.0"}
        }

        self._write_file("package.json", json.dumps(package, indent=2))

    def _create_tsconfig(self):
        """Generate tsconfig.json"""
        tsconfig = {
            "compilerOptions": {
                "target": "ES2022",
                "module": "NodeNext",
                "moduleResolution": "NodeNext",
                "lib": ["ES2022"],
                "outDir": "./dist",
                "rootDir": "./src",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "resolveJsonModule": True,
                "declaration": True,
                "declarationMap": True,
                "sourceMap": True,
                "baseUrl": ".",
                "paths": {"@/*": ["src/*"]}
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist", "tests"]
        }
        self._write_file("tsconfig.json", json.dumps(tsconfig, indent=2))

    def _create_env_files(self):
        """Generate environment files"""
        env_content = f"""# {self.config.name} Environment Configuration
NODE_ENV=development
PORT=3000

# Database
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/{self.config.name}?schema=public"

# Redis (for caching/sessions)
REDIS_URL="redis://localhost:6379"
"""
        if self.config.include_auth:
            env_content += """
# Authentication
JWT_SECRET="your-super-secret-key-change-in-production"
JWT_EXPIRES_IN="15m"
JWT_REFRESH_EXPIRES_IN="7d"
"""
        self._write_file(".env.example", env_content)
        self._write_file(".gitignore", """node_modules/
dist/
.env
.env.local
*.log
coverage/
.DS_Store
""")

    def _create_rest_structure(self):
        """Generate REST API source files"""
        logger.debug("Creating REST API structure")
        # Main entry point
        app_content = '''import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { config } from './config/env';
import { errorHandler } from './middleware/errorHandler';
import { requestLogger } from './middleware/requestLogger';
import routes from './routes';

const app = express();

// Middleware
app.use(helmet());
app.use(cors());
app.use(compression());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(requestLogger);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API routes
app.use('/api', routes);

// Error handling
app.use(errorHandler);

export default app;
'''
        self._write_file("src/app.ts", app_content)

        index_content = '''import app from './app';
import { config } from './config/env';
import { prisma } from './lib/db';

const startServer = async () => {
  try {
    // Test database connection
    await prisma.$connect();
    console.log('Database connected successfully');

    app.listen(config.port, () => {
      console.log(`Server running on http://localhost:${config.port}`);
      console.log(`Environment: ${config.nodeEnv}`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
};

startServer();
'''
        self._write_file("src/index.ts", index_content)

        # Config
        config_content = '''import dotenv from 'dotenv';
dotenv.config();

export const config = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000', 10),
  databaseUrl: process.env.DATABASE_URL || '',
  redisUrl: process.env.REDIS_URL || '',
  jwtSecret: process.env.JWT_SECRET || 'default-secret',
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '15m',
  jwtRefreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d',
};
'''
        self._write_file("src/config/env.ts", config_content)

        # Database client
        db_content = '''import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
'''
        self._write_file("src/lib/db.ts", db_content)

        # Middleware
        error_handler = '''import { Request, Response, NextFunction } from 'express';
import { ZodError } from 'zod';

export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public isOperational = true
  ) {
    super(message);
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

export const errorHandler = (
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) => {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      status: 'error',
      message: err.message,
    });
  }

  if (err instanceof ZodError) {
    return res.status(400).json({
      status: 'error',
      message: 'Validation error',
      errors: err.errors,
    });
  }

  console.error('Unexpected error:', err);
  return res.status(500).json({
    status: 'error',
    message: 'Internal server error',
  });
};
'''
        self._write_file("src/middleware/errorHandler.ts", error_handler)

        request_logger = '''import { Request, Response, NextFunction } from 'express';

export const requestLogger = (req: Request, res: Response, next: NextFunction) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.originalUrl} ${res.statusCode} - ${duration}ms`);
  });
  next();
};
'''
        self._write_file("src/middleware/requestLogger.ts", request_logger)

        # Routes
        routes_content = '''import { Router } from 'express';
import userRoutes from './user.routes';

const router = Router();

router.use('/users', userRoutes);

export default router;
'''
        self._write_file("src/routes/index.ts", routes_content)

        user_routes = '''import { Router } from 'express';
import { UserController } from '../controllers/user.controller';

const router = Router();
const controller = new UserController();

router.get('/', controller.findAll);
router.get('/:id', controller.findOne);
router.post('/', controller.create);
router.put('/:id', controller.update);
router.delete('/:id', controller.delete);

export default router;
'''
        self._write_file("src/routes/user.routes.ts", user_routes)

        # Controller
        controller_content = '''import { Request, Response, NextFunction } from 'express';
import { UserService } from '../services/user.service';
import { createUserSchema, updateUserSchema } from '../types/user.types';

export class UserController {
  private service = new UserService();

  findAll = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const users = await this.service.findAll();
      res.json({ data: users });
    } catch (error) {
      next(error);
    }
  };

  findOne = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await this.service.findById(req.params.id);
      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  create = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const data = createUserSchema.parse(req.body);
      const user = await this.service.create(data);
      res.status(201).json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  update = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const data = updateUserSchema.parse(req.body);
      const user = await this.service.update(req.params.id, data);
      res.json({ data: user });
    } catch (error) {
      next(error);
    }
  };

  delete = async (req: Request, res: Response, next: NextFunction) => {
    try {
      await this.service.delete(req.params.id);
      res.status(204).send();
    } catch (error) {
      next(error);
    }
  };
}
'''
        self._write_file("src/controllers/user.controller.ts", controller_content)

        # Service
        service_content = '''import { UserRepository } from '../repositories/user.repository';
import { CreateUserInput, UpdateUserInput } from '../types/user.types';
import { AppError } from '../middleware/errorHandler';

export class UserService {
  private repository = new UserRepository();

  async findAll() {
    return this.repository.findAll();
  }

  async findById(id: string) {
    const user = await this.repository.findById(id);
    if (!user) {
      throw new AppError(404, 'User not found');
    }
    return user;
  }

  async create(data: CreateUserInput) {
    return this.repository.create(data);
  }

  async update(id: string, data: UpdateUserInput) {
    await this.findById(id);
    return this.repository.update(id, data);
  }

  async delete(id: string) {
    await this.findById(id);
    return this.repository.delete(id);
  }
}
'''
        self._write_file("src/services/user.service.ts", service_content)

        # Repository
        repository_content = '''import { prisma } from '../lib/db';
import { CreateUserInput, UpdateUserInput } from '../types/user.types';

export class UserRepository {
  async findAll() {
    return prisma.user.findMany({
      orderBy: { createdAt: 'desc' },
    });
  }

  async findById(id: string) {
    return prisma.user.findUnique({ where: { id } });
  }

  async findByEmail(email: string) {
    return prisma.user.findUnique({ where: { email } });
  }

  async create(data: CreateUserInput) {
    return prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserInput) {
    return prisma.user.update({ where: { id }, data });
  }

  async delete(id: string) {
    return prisma.user.delete({ where: { id } });
  }
}
'''
        self._write_file("src/repositories/user.repository.ts", repository_content)

        # Types
        types_content = '''import { z } from 'zod';

export const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(100),
  password: z.string().min(8).optional(),
});

export const updateUserSchema = createUserSchema.partial();

export type CreateUserInput = z.infer<typeof createUserSchema>;
export type UpdateUserInput = z.infer<typeof updateUserSchema>;
'''
        self._write_file("src/types/user.types.ts", types_content)

    def _create_graphql_structure(self):
        """Generate GraphQL API source files"""
        logger.debug("Creating GraphQL API structure")
        # Main entry point for GraphQL
        index_content = '''import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { config } from './config/env';
import { typeDefs } from './graphql/schema';
import { resolvers } from './graphql/resolvers';
import { createContext } from './graphql/context';
import { prisma } from './lib/db';

const startServer = async () => {
  const app = express();

  const server = new ApolloServer({
    typeDefs,
    resolvers,
  });

  await server.start();

  app.use(helmet({ contentSecurityPolicy: false }));
  app.use(cors());
  app.use(express.json());

  app.get('/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
  });

  app.use('/graphql', expressMiddleware(server, {
    context: createContext,
  }));

  await prisma.$connect();
  console.log('Database connected successfully');

  app.listen(config.port, () => {
    console.log(`GraphQL server running on http://localhost:${config.port}/graphql`);
  });
};

startServer();
'''
        self._write_file("src/index.ts", index_content)

        # GraphQL Schema
        schema_content = '''export const typeDefs = `#graphql
  type User {
    id: ID!
    email: String!
    name: String!
    posts: [Post!]!
    createdAt: String!
    updatedAt: String!
  }

  type Post {
    id: ID!
    title: String!
    content: String
    published: Boolean!
    author: User!
    createdAt: String!
    updatedAt: String!
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
    posts(published: Boolean): [Post!]!
    post(id: ID!): Post
  }

  type Mutation {
    createUser(input: CreateUserInput!): User!
    updateUser(id: ID!, input: UpdateUserInput!): User!
    deleteUser(id: ID!): Boolean!
    createPost(input: CreatePostInput!): Post!
    updatePost(id: ID!, input: UpdatePostInput!): Post!
    deletePost(id: ID!): Boolean!
  }

  input CreateUserInput {
    email: String!
    name: String!
  }

  input UpdateUserInput {
    email: String
    name: String
  }

  input CreatePostInput {
    title: String!
    content: String
    authorId: ID!
  }

  input UpdatePostInput {
    title: String
    content: String
    published: Boolean
  }
`;
'''
        self._write_file("src/graphql/schema.ts", schema_content)

        # Resolvers
        resolvers_content = '''import { prisma } from '../lib/db';
import { createLoaders } from './loaders';

export const resolvers = {
  Query: {
    users: () => prisma.user.findMany(),
    user: (_: any, { id }: { id: string }) => prisma.user.findUnique({ where: { id } }),
    posts: (_: any, { published }: { published?: boolean }) =>
      prisma.post.findMany({ where: published !== undefined ? { published } : {} }),
    post: (_: any, { id }: { id: string }) => prisma.post.findUnique({ where: { id } }),
  },

  Mutation: {
    createUser: (_: any, { input }: { input: { email: string; name: string } }) =>
      prisma.user.create({ data: input }),
    updateUser: (_: any, { id, input }: { id: string; input: any }) =>
      prisma.user.update({ where: { id }, data: input }),
    deleteUser: async (_: any, { id }: { id: string }) => {
      await prisma.user.delete({ where: { id } });
      return true;
    },
    createPost: (_: any, { input }: { input: { title: string; content?: string; authorId: string } }) =>
      prisma.post.create({ data: input }),
    updatePost: (_: any, { id, input }: { id: string; input: any }) =>
      prisma.post.update({ where: { id }, data: input }),
    deletePost: async (_: any, { id }: { id: string }) => {
      await prisma.post.delete({ where: { id } });
      return true;
    },
  },

  User: {
    posts: (parent: { id: string }, _: any, context: any) =>
      context.loaders.postsByUser.load(parent.id),
  },

  Post: {
    author: (parent: { authorId: string }, _: any, context: any) =>
      context.loaders.user.load(parent.authorId),
  },
};
'''
        self._write_file("src/graphql/resolvers/index.ts", resolvers_content)

        # DataLoaders
        loaders_content = '''import DataLoader from 'dataloader';
import { prisma } from '../lib/db';

export const createLoaders = () => ({
  user: new DataLoader(async (ids: readonly string[]) => {
    const users = await prisma.user.findMany({
      where: { id: { in: [...ids] } },
    });
    return ids.map(id => users.find(u => u.id === id) || null);
  }),

  postsByUser: new DataLoader(async (userIds: readonly string[]) => {
    const posts = await prisma.post.findMany({
      where: { authorId: { in: [...userIds] } },
    });
    return userIds.map(userId => posts.filter(p => p.authorId === userId));
  }),
});
'''
        self._write_file("src/graphql/loaders.ts", loaders_content)

        # Context
        context_content = '''import { createLoaders } from './loaders';

export interface Context {
  loaders: ReturnType<typeof createLoaders>;
  user?: { id: string; email: string };
}

export const createContext = async ({ req }: { req: any }): Promise<Context> => {
  return {
    loaders: createLoaders(),
  };
};
'''
        self._write_file("src/graphql/context.ts", context_content)

        # Config and DB (same as REST)
        self._write_file("src/config/env.ts", '''import dotenv from 'dotenv';
dotenv.config();

export const config = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '4000', 10),
  databaseUrl: process.env.DATABASE_URL || '',
  jwtSecret: process.env.JWT_SECRET || 'default-secret',
};
''')

        self._write_file("src/lib/db.ts", '''import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
''')

    def _create_prisma_schema(self):
        """Generate Prisma schema"""
        schema = f'''// Prisma Schema for {self.config.name}
generator client {{
  provider = "prisma-client-js"
}}

datasource db {{
  provider = "postgresql"
  url      = env("DATABASE_URL")
}}

model User {{
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  password  String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email])
}}

model Post {{
  id        String   @id @default(uuid())
  title     String
  content   String?  @db.Text
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
  @@index([published])
}}
'''
        self._write_file("prisma/schema.prisma", schema)

        # Seed file
        seed = '''import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  const user = await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      email: 'admin@example.com',
      name: 'Admin User',
      posts: {
        create: [
          { title: 'Hello World', content: 'First post content', published: true },
          { title: 'Draft Post', content: 'Draft content', published: false },
        ],
      },
    },
  });
  console.log('Seeded user:', user);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
'''
        self._write_file("prisma/seed.ts", seed)

    def _create_auth_middleware(self):
        """Generate authentication middleware"""
        auth_content = '''import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '../config/env';
import { AppError } from './errorHandler';

export interface AuthRequest extends Request {
  user?: { id: string; email: string };
}

export const authenticate = (req: AuthRequest, res: Response, next: NextFunction) => {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    throw new AppError(401, 'No token provided');
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, config.jwtSecret) as { id: string; email: string };
    req.user = decoded;
    next();
  } catch (error) {
    throw new AppError(401, 'Invalid token');
  }
};

export const generateToken = (payload: { id: string; email: string }) => {
  return jwt.sign(payload, config.jwtSecret, { expiresIn: config.jwtExpiresIn });
};

export const generateRefreshToken = (payload: { id: string }) => {
  return jwt.sign(payload, config.jwtSecret, { expiresIn: config.jwtRefreshExpiresIn });
};
'''
        self._write_file("src/middleware/auth.ts", auth_content)

        auth_service = '''import bcrypt from 'bcryptjs';
import { UserRepository } from '../repositories/user.repository';
import { generateToken, generateRefreshToken } from '../middleware/auth';
import { AppError } from '../middleware/errorHandler';

export class AuthService {
  private userRepo = new UserRepository();

  async register(email: string, password: string, name: string) {
    const existing = await this.userRepo.findByEmail(email);
    if (existing) {
      throw new AppError(400, 'Email already in use');
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const user = await this.userRepo.create({
      email,
      name,
      password: hashedPassword,
    });

    const token = generateToken({ id: user.id, email: user.email });
    const refreshToken = generateRefreshToken({ id: user.id });

    return { user: { id: user.id, email: user.email, name: user.name }, token, refreshToken };
  }

  async login(email: string, password: string) {
    const user = await this.userRepo.findByEmail(email);
    if (!user || !user.password) {
      throw new AppError(401, 'Invalid credentials');
    }

    const valid = await bcrypt.compare(password, user.password);
    if (!valid) {
      throw new AppError(401, 'Invalid credentials');
    }

    const token = generateToken({ id: user.id, email: user.email });
    const refreshToken = generateRefreshToken({ id: user.id });

    return { user: { id: user.id, email: user.email, name: user.name }, token, refreshToken };
  }
}
'''
        self._write_file("src/services/auth.service.ts", auth_service)

    def _create_docker_config(self):
        """Generate Docker configuration"""
        dockerfile = f'''FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npx prisma generate

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/prisma ./prisma
EXPOSE 3000
CMD ["npm", "start"]
'''
        self._write_file("Dockerfile", dockerfile)

        compose = f'''version: '3.8'
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/{self.config.name}
      - REDIS_URL=redis://redis:6379
      - NODE_ENV=production
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB={self.config.name}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
'''
        self._write_file("docker-compose.yml", compose)

    def _create_ci_config(self):
        """Generate CI/CD configuration"""
        workflow = f'''name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: {self.config.name}_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npx prisma generate
      - run: npx prisma migrate deploy
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/{self.config.name}_test
      - run: npm test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/{self.config.name}_test

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
'''
        self._write_file(".github/workflows/ci.yml", workflow)

    def _create_test_structure(self):
        """Generate test files"""
        jest_config = '''{
  "preset": "ts-jest",
  "testEnvironment": "node",
  "roots": ["<rootDir>/tests"],
  "testMatch": ["**/*.test.ts"],
  "moduleNameMapper": {
    "^@/(.*)$": "<rootDir>/src/$1"
  },
  "setupFilesAfterEnv": ["<rootDir>/tests/setup.ts"],
  "coverageDirectory": "coverage",
  "collectCoverageFrom": ["src/**/*.ts", "!src/**/*.d.ts"]
}
'''
        self._write_file("jest.config.json", jest_config)

        setup = '''import { prisma } from '../src/lib/db';

beforeAll(async () => {
  // Setup test database
});

afterAll(async () => {
  await prisma.$disconnect();
});
'''
        self._write_file("tests/setup.ts", setup)

        user_test = '''import request from 'supertest';
import app from '../src/app';

describe('User API', () => {
  describe('GET /api/users', () => {
    it('should return list of users', async () => {
      const response = await request(app).get('/api/users');
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('data');
    });
  });

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'test@example.com', name: 'Test User' });
      expect(response.status).toBe(201);
      expect(response.body.data).toHaveProperty('id');
    });

    it('should return 400 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'invalid', name: 'Test' });
      expect(response.status).toBe(400);
    });
  });
});
'''
        self._write_file("tests/integration/user.test.ts", user_test)

    def _get_endpoints_docs(self) -> str:
        """Return endpoint documentation based on API type"""
        if self.config.api_type == 'graphql':
            return """- `GET /graphql` - GraphQL Playground
- `POST /graphql` - GraphQL endpoint"""
        else:
            return """- `GET /api/users` - List all users
- `GET /api/users/:id` - Get user by ID
- `POST /api/users` - Create user
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user"""

    def _create_readme(self):
        """Generate README.md"""
        readme = f'''# {self.config.name}

{self.config.api_type.upper()} API built with {self.config.stack}

## Quick Start

```bash
# Install dependencies
npm install

# Setup environment
cp .env.example .env

# Start database
docker-compose up -d db redis

# Run migrations
npm run migrate

# Seed database
npm run db:seed

# Start development server
npm run dev
```

## API Endpoints

{"### GraphQL" if self.config.api_type == "graphql" else "### REST"}

{self._get_endpoints_docs()}

- `GET /health` - Health check

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm test` - Run tests
- `npm run migrate` - Run database migrations
- `npm run db:studio` - Open Prisma Studio

## Tech Stack

- **Runtime:** Node.js 20+
- **Language:** TypeScript
- **Framework:** {'Apollo Server' if self.config.api_type == 'graphql' else 'Express'}
- **Database:** PostgreSQL + Prisma ORM
- **Validation:** Zod
- **Testing:** Jest + Supertest

Generated by API Scaffolder v1.0.0
'''
        self._write_file("README.md", readme)


def parse_openapi_spec(spec_path: str) -> List[EndpointConfig]:
    """Parse OpenAPI spec to extract endpoints"""
    logger.debug(f"Parsing OpenAPI spec: {spec_path}")
    with open(spec_path, 'r') as f:
        spec = json.load(f)

    endpoints = []
    if not spec.get('paths'):
        logger.warning("No paths found in OpenAPI spec")
    for path, methods in spec.get('paths', {}).items():
        for method, details in methods.items():
            if method in ['get', 'post', 'put', 'delete', 'patch']:
                endpoints.append(EndpointConfig(
                    path=path,
                    method=method.upper(),
                    name=details.get('operationId', f"{method}_{path.replace('/', '_')}"),
                    description=details.get('summary', ''),
                    request_body=details.get('requestBody'),
                    response_schema=details.get('responses', {}).get('200'),
                    auth_required='security' in details
                ))
    return endpoints


def format_json_output(result: Dict) -> str:
    """Format result as JSON"""
    return json.dumps(result, indent=2)


def format_text_output(result: Dict) -> str:
    """Format result as human-readable text"""
    lines = [
        "=" * 60,
        "API SCAFFOLDER RESULTS",
        "=" * 60,
        "",
        f"Project: {result['project_name']}",
        f"Type: {result['api_type'].upper()}",
        f"Stack: {result['stack']}",
        f"Output: {result['output_directory']}",
        f"Files Created: {result['files_created']}",
        "",
        "FILES:",
        "-" * 40
    ]
    for f in result['files'][:20]:
        lines.append(f"  {f}")
    if len(result['files']) > 20:
        lines.append(f"  ... and {len(result['files']) - 20} more")
    lines.extend(["", "=" * 60])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="API Scaffolder - Generate production-ready REST/GraphQL APIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-api
  %(prog)s my-api --type graphql
  %(prog)s my-api --type rest --stack express-typescript --auth
  %(prog)s my-api --openapi spec.json
  %(prog)s my-api --output ./projects --format json

API Types:
  rest     - REST API with Express (default)
  graphql  - GraphQL API with Apollo Server

Stacks:
  express-typescript - Express.js with TypeScript (default)
        """)

    parser.add_argument('name', nargs='?', help='Project name')
    parser.add_argument('--type', '-t', choices=['rest', 'graphql'], default='rest', help='API type')
    parser.add_argument('--stack', '-s', default='express-typescript', help='Tech stack')
    parser.add_argument('--output', '-o', default='.', help='Output directory')
    parser.add_argument('--auth', action='store_true', help='Include authentication')
    parser.add_argument('--docker', action='store_true', default=True, help='Include Docker config')
    parser.add_argument('--ci', action='store_true', default=True, help='Include CI/CD config')
    parser.add_argument('--openapi', help='OpenAPI spec file to parse')
    parser.add_argument('--format', '-f', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    if not args.name:
        parser.print_help()
        print("\nError: Project name is required")
        sys.exit(1)

    endpoints = []
    if args.openapi:
        try:
            endpoints = parse_openapi_spec(args.openapi)
            if args.verbose:
                print(f"Parsed {len(endpoints)} endpoints from OpenAPI spec")
        except Exception as e:
            print(f"Error parsing OpenAPI spec: {e}", file=sys.stderr)
            sys.exit(1)

    config = ProjectConfig(
        name=args.name,
        api_type=args.type,
        stack=args.stack,
        include_auth=args.auth,
        include_docker=args.docker,
        include_ci=args.ci,
        endpoints=endpoints
    )

    output_path = Path(args.output) / args.name
    scaffolder = APIScaffolder(config, str(output_path), args.verbose)

    try:
        result = scaffolder.scaffold()
    except Exception as e:
        print(f"Error scaffolding project: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == 'json':
        print(format_json_output(result))
    else:
        print(format_text_output(result))


if __name__ == '__main__':
    main()
