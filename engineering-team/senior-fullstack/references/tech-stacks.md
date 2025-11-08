# Technology Stack Guide

## Overview

Comprehensive guide to modern fullstack technology stacks, including languages, frameworks, databases, DevOps tools, and cloud platforms.

## Languages

### JavaScript/TypeScript

**TypeScript**
- Static typing for JavaScript
- Enhanced IDE support
- Catch errors at compile time
- Better refactoring capabilities

**Configuration (tsconfig.json)**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve"
  }
}
```

**Best Practices**
- Enable strict mode
- Use type inference where possible
- Define interfaces for data structures
- Avoid `any` type

### Python

**Use Cases**
- Data processing
- Machine learning
- Scripting and automation
- Backend services (FastAPI, Django)

**Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Go

**Use Cases**
- High-performance services
- CLI tools
- Microservices
- Concurrent processing

**Strengths**
- Fast compilation
- Built-in concurrency
- Strong standard library
- Low memory footprint

### Kotlin (Android/Backend)

**Use Cases**
- Android mobile apps
- Backend services (Ktor, Spring Boot)
- Cross-platform development

### Swift (iOS)

**Use Cases**
- iOS mobile apps
- macOS applications
- SwiftUI for declarative UI

## Frontend Frameworks

### React

**Core Concepts**
- Component-based architecture
- Virtual DOM
- Hooks (useState, useEffect, useContext)
- Unidirectional data flow

**Ecosystem**
- React Router (routing)
- React Query (data fetching)
- Zustand/Jotai (state management)
- React Hook Form (forms)
- React Testing Library (testing)

**Best Practices**
- Keep components small and focused
- Use custom hooks for reusable logic
- Optimize with React.memo, useMemo, useCallback
- Handle loading and error states

### Next.js

**Features**
- Server-side rendering (SSR)
- Static site generation (SSG)
- API routes
- File-based routing
- Image optimization
- Incremental static regeneration (ISR)

**Rendering Strategies**
- Static Generation: Pre-render at build time
- Server-side Rendering: Render on each request
- Client-side Rendering: Render in browser
- Incremental Static Regeneration: Rebuild pages on demand

**App Router (Next.js 13+)**
- React Server Components
- Streaming
- Layouts and templates
- Loading UI
- Error handling

**Pages Router (Next.js 12)**
- getStaticProps: Fetch data at build time
- getServerSideProps: Fetch data on each request
- getStaticPaths: Generate dynamic routes

### React Native

**Cross-platform Mobile Development**
- iOS and Android from single codebase
- Native performance
- Hot reloading
- Large ecosystem

**Libraries**
- React Navigation (navigation)
- React Native Reanimated (animations)
- React Native Gesture Handler (gestures)
- Expo (managed workflow)

### Flutter

**Cross-platform Framework**
- Single codebase for iOS, Android, Web, Desktop
- Dart language
- Rich widget library
- Fast development

## Backend Frameworks

### Node.js + Express

**Lightweight Web Framework**
```javascript
const express = require('express');
const app = express();

app.use(express.json());

app.get('/api/users', async (req, res) => {
  const users = await User.findAll();
  res.json(users);
});

app.listen(3000);
```

**Middleware**
- Body parsing
- CORS
- Authentication
- Logging
- Error handling

### GraphQL

**Query Language for APIs**

**Advantages**
- Request exactly what you need
- Single endpoint
- Strong typing
- Real-time with subscriptions

**Popular Libraries**
- Apollo Server (Node.js)
- GraphQL Yoga (flexible)
- TypeGraphQL (TypeScript)
- Prisma (database integration)

**Schema Example**
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Query {
  user(id: ID!): User
  users: [User!]!
}

type Mutation {
  createUser(name: String!, email: String!): User!
}
```

### REST APIs

**Design Principles**
- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Status codes
- JSON responses

**Best Practices**
- Use nouns for resources (`/users`, not `/getUsers`)
- Version your API (`/api/v1/users`)
- Implement pagination
- Handle errors consistently
- Document with OpenAPI/Swagger

## Databases

### PostgreSQL

**Relational Database**

**Features**
- ACID compliance
- Advanced indexing
- JSON support
- Full-text search
- Window functions
- Common Table Expressions (CTEs)

**Use Cases**
- Complex queries
- Transactions
- Referential integrity
- Analytics

**Best Practices**
- Use indexes strategically
- Analyze query performance with EXPLAIN
- Use connection pooling
- Regular VACUUM operations

### Prisma ORM

**Modern Database Toolkit**

**Features**
- Type-safe database access
- Auto-generated migrations
- Intuitive query API
- Multiple database support

**Schema Example**
```prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

**Commands**
```bash
npx prisma init
npx prisma migrate dev --name init
npx prisma generate
npx prisma studio
```

### NeonDB

**Serverless PostgreSQL**

**Features**
- Automatic scaling
- Branching (Git-like for databases)
- Connection pooling
- Pay-per-use pricing

**Use Cases**
- Serverless applications
- Development/staging environments
- Cost-effective scaling

### Supabase

**Open-source Firebase Alternative**

**Features**
- PostgreSQL database
- Authentication
- Real-time subscriptions
- Storage
- Edge functions
- Auto-generated REST and GraphQL APIs

**Use Cases**
- Rapid prototyping
- Full-featured backend
- Real-time applications

### MongoDB (NoSQL)

**Document Database**

**Features**
- Schema flexibility
- Horizontal scaling
- Rich query language
- Aggregation pipeline

**Use Cases**
- Flexible schemas
- High write throughput
- Hierarchical data
- Content management

## DevOps Tools

### Docker

**Containerization Platform**

**Dockerfile Example**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

**Docker Compose**
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Kubernetes

**Container Orchestration**

**Features**
- Automated deployment
- Scaling
- Load balancing
- Self-healing
- Rolling updates

**Key Concepts**
- Pods: Smallest deployable units
- Services: Network abstraction
- Deployments: Declarative updates
- ConfigMaps: Configuration data
- Secrets: Sensitive data

### Terraform

**Infrastructure as Code**

**Use Cases**
- Cloud resource provisioning
- Multi-cloud deployments
- Version-controlled infrastructure
- Reproducible environments

**Example**
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "WebServer"
  }
}
```

### CI/CD

**GitHub Actions**
```yaml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm test
      - run: npm run build
```

**CircleCI**
- Fast builds
- Docker layer caching
- Parallel execution
- Advanced workflows

## Cloud Platforms

### AWS (Amazon Web Services)

**Core Services**
- EC2: Virtual servers
- S3: Object storage
- RDS: Managed databases
- Lambda: Serverless functions
- API Gateway: API management
- CloudFront: CDN
- ECS/EKS: Container services

### GCP (Google Cloud Platform)

**Core Services**
- Compute Engine: VMs
- Cloud Storage: Object storage
- Cloud SQL: Managed databases
- Cloud Functions: Serverless
- Cloud Run: Containerized apps
- Kubernetes Engine: Managed Kubernetes

### Azure (Microsoft Azure)

**Core Services**
- Virtual Machines
- Blob Storage
- Azure SQL Database
- Azure Functions
- App Service
- Azure Kubernetes Service

### Vercel

**Frontend Deployment Platform**

**Features**
- Zero-config Next.js deployment
- Automatic HTTPS
- Preview deployments
- Edge functions
- Analytics

**Use Cases**
- Next.js applications
- Static sites
- Jamstack projects

### Railway

**Full-stack Deployment**

**Features**
- Deploy from GitHub
- Managed databases
- Environment variables
- Automatic scaling
- Pay-per-use

## Testing

### Jest

**JavaScript Testing Framework**

**Features**
- Zero configuration
- Snapshot testing
- Mocking
- Code coverage
- Watch mode

**Example**
```javascript
describe('User service', () => {
  test('creates a user', async () => {
    const user = await createUser({ name: 'John' });
    expect(user.name).toBe('John');
  });
});
```

### React Testing Library

**Component Testing**

**Principles**
- Test user behavior, not implementation
- Query by accessibility
- Avoid testing internals

**Example**
```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('submits form', async () => {
  render(<LoginForm />);

  await userEvent.type(screen.getByLabelText('Email'), 'test@example.com');
  await userEvent.click(screen.getByRole('button', { name: 'Login' }));

  expect(screen.getByText('Welcome')).toBeInTheDocument();
});
```

### Cypress

**End-to-end Testing**

**Features**
- Real browser testing
- Time travel debugging
- Automatic waiting
- Network stubbing

**Example**
```javascript
describe('Login flow', () => {
  it('logs in successfully', () => {
    cy.visit('/login');
    cy.get('[data-testid="email"]').type('user@example.com');
    cy.get('[data-testid="password"]').type('password123');
    cy.get('[data-testid="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

## Development Tools

### ESLint

**JavaScript Linter**

**Configuration**
```json
{
  "extends": ["next/core-web-vitals", "prettier"],
  "rules": {
    "no-console": "warn",
    "prefer-const": "error"
  }
}
```

### Prettier

**Code Formatter**

**Configuration**
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

### Git Hooks (Husky)

**Automated Quality Checks**

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged",
      "pre-push": "npm test"
    }
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"]
  }
}
```

## Monitoring and Logging

### Sentry

**Error Tracking**
- Real-time error alerts
- Stack traces
- User context
- Performance monitoring

### Datadog

**Monitoring Platform**
- Infrastructure monitoring
- APM (Application Performance Monitoring)
- Log aggregation
- Custom dashboards

### LogRocket

**Session Replay**
- Replay user sessions
- Console logs
- Network activity
- Redux/Vuex state

## Technology Selection Guide

### When to Use What

**Next.js**
- SEO-critical applications
- E-commerce
- Marketing sites
- Blogs

**React SPA**
- Complex dashboards
- Internal tools
- Rich interactions
- Real-time apps

**React Native**
- Cross-platform mobile apps
- Shared codebase priority
- Native feel required

**GraphQL**
- Complex data requirements
- Multiple frontend clients
- Real-time features
- Rapid iteration

**REST**
- Simple CRUD operations
- Public APIs
- Third-party integrations
- Standard HTTP clients

**PostgreSQL**
- Complex queries
- Strong consistency
- Relational data
- ACID requirements

**MongoDB**
- Flexible schemas
- High write throughput
- Hierarchical data
- Document storage

## Stack Combinations

### JAMstack (Next.js + Headless CMS)
- Next.js frontend
- Contentful/Sanity CMS
- Vercel deployment
- Static + ISR

### MERN Stack
- MongoDB
- Express
- React
- Node.js

### T3 Stack
- TypeScript
- tRPC
- Tailwind CSS
- Next.js
- Prisma

### Serverless Stack
- Next.js (Vercel)
- Supabase (Database + Auth)
- Edge functions
- CDN distribution

## Best Practices

1. **Choose boring technology** - Prefer mature, well-supported tools
2. **Start with monolith** - Microservices when you need them
3. **Use managed services** - Focus on business logic
4. **Automate everything** - CI/CD, testing, deployment
5. **Monitor from day one** - Observability is critical
6. **Version control everything** - Code, infrastructure, configurations
7. **Document decisions** - ADRs (Architecture Decision Records)
8. **Keep dependencies updated** - Security and features
