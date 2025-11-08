# Backend Python Tools Documentation

Comprehensive documentation for Python CLI tools including API scaffolding, database migrations, and load testing automation.

## api_scaffolder.py

Production-ready API scaffolding tool for generating REST and GraphQL API projects with modern tech stacks.

### Overview

The API Scaffolder automates the creation of backend API projects with complete file structure, configuration, middleware, and boilerplate code. Supports multiple tech stacks and includes Docker, testing infrastructure, and CI/CD pipelines.

### Installation

```bash
# No dependencies required - uses Python standard library
python3 --version  # Requires Python 3.8+
```

### Usage

**Basic Commands:**
```bash
# Create REST API with Express + TypeScript + PostgreSQL
python scripts/api_scaffolder.py my-api --type rest --stack express-typescript

# Create GraphQL API with Apollo Server
python scripts/api_scaffolder.py my-graphql-api --type graphql --stack apollo

# Create minimal API (no database)
python scripts/api_scaffolder.py simple-api --type rest --minimal

# Show help
python scripts/api_scaffolder.py --help
```

**Available Options:**
- `name`: Project name (required)
- `--type/-t`: API type (rest, graphql) - default: rest
- `--stack/-s`: Tech stack (express-typescript, express-javascript, fastify, apollo, etc.)
- `--database/-d`: Database (postgresql, mysql, mongodb, none) - default: postgresql
- `--auth/-a`: Include authentication setup (default: true)
- `--docker`: Include Docker configuration (default: true)
- `--ci`: Include CI/CD pipelines (github, gitlab, circleci) - default: github
- `--minimal/-m`: Minimal setup without optional features
- `--output/-o`: Output directory - default: current directory

### Supported Stacks

**REST API:**
- `express-typescript`: Express + TypeScript + Prisma
- `express-javascript`: Express + JavaScript + Sequelize
- `fastify-typescript`: Fastify + TypeScript + Prisma
- `nestjs`: NestJS framework with TypeScript

**GraphQL:**
- `apollo-typescript`: Apollo Server + TypeScript + Prisma
- `apollo-javascript`: Apollo Server + JavaScript
- `graphql-yoga`: GraphQL Yoga + TypeScript

### Generated Project Structure

**Express + TypeScript + PostgreSQL:**
```
my-api/
├── src/
│   ├── controllers/
│   │   ├── authController.ts
│   │   └── userController.ts
│   ├── services/
│   │   ├── authService.ts
│   │   └── userService.ts
│   ├── repositories/
│   │   └── userRepository.ts
│   ├── middleware/
│   │   ├── auth.ts
│   │   ├── errorHandler.ts
│   │   ├── validation.ts
│   │   ├── rateLimiter.ts
│   │   └── logger.ts
│   ├── routes/
│   │   ├── authRoutes.ts
│   │   └── userRoutes.ts
│   ├── models/
│   │   └── types.ts
│   ├── utils/
│   │   ├── logger.ts
│   │   └── validation.ts
│   ├── config/
│   │   ├── database.ts
│   │   └── env.ts
│   ├── errors/
│   │   ├── baseError.ts
│   │   ├── authenticationError.ts
│   │   └── validationError.ts
│   └── app.ts
├── prisma/
│   ├── schema.prisma
│   ├── seed.ts
│   └── migrations/
├── tests/
│   ├── unit/
│   │   ├── userService.test.ts
│   │   └── authService.test.ts
│   └── integration/
│       └── userApi.test.ts
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
├── .env.example
├── .gitignore
├── .eslintrc.json
├── .prettierrc
├── tsconfig.json
├── jest.config.js
├── package.json
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Features Included

**Authentication Setup (--auth):**
- JWT-based authentication
- Password hashing with bcrypt
- Login/register endpoints
- Protected route middleware
- Token refresh mechanism

**Database Integration:**
- Prisma ORM configuration
- Database schema with User model
- Migration setup
- Seed data script
- Connection pooling

**Middleware:**
- Authentication middleware
- Request validation (Zod)
- Error handling
- Rate limiting (Redis)
- Logging (Winston)
- CORS and Helmet security

**Testing Infrastructure:**
- Jest configuration
- Unit test templates
- Integration test setup
- Supertest for API testing
- Coverage reporting

**Docker Configuration:**
- Multi-stage Dockerfile
- docker-compose.yml with:
  - App container
  - PostgreSQL container
  - Redis container
- Volume management
- Environment variables

**CI/CD Pipelines:**
- GitHub Actions workflow
- Automated testing
- Linting and formatting
- Docker image building
- Deployment scripts

### Output Example

```bash
$ python scripts/api_scaffolder.py my-api --type rest --stack express-typescript

🚀 API Scaffolder
==================

Project: my-api
Type: REST API
Stack: Express + TypeScript + Prisma
Database: PostgreSQL
Auth: Enabled
Docker: Enabled
CI/CD: GitHub Actions

Creating project structure... ✓
Generating configuration files... ✓
Setting up authentication... ✓
Creating middleware... ✓
Generating controllers and services... ✓
Setting up database schema... ✓
Creating test infrastructure... ✓
Generating Docker configuration... ✓
Setting up CI/CD pipeline... ✓

✅ Project created successfully!

Next steps:
  cd my-api
  npm install
  cp .env.example .env
  # Update .env with your configuration
  docker-compose up -d
  npm run migrate
  npm run dev

Your API will be available at http://localhost:3000
```

### Configuration Options

**Customization:**
```bash
# Minimal setup (no auth, docker, or CI/CD)
python scripts/api_scaffolder.py simple-api --minimal

# MongoDB instead of PostgreSQL
python scripts/api_scaffolder.py mongo-api --database mongodb

# GraphQL API with authentication
python scripts/api_scaffolder.py gql-api --type graphql --auth

# Custom output directory
python scripts/api_scaffolder.py my-api --output /path/to/projects/
```

### Common Workflows

**Standard REST API Project:**
```bash
# 1. Scaffold project
python scripts/api_scaffolder.py my-api --type rest --stack express-typescript

# 2. Install dependencies
cd my-api && npm install

# 3. Configure environment
cp .env.example .env
# Edit .env with database credentials

# 4. Start services
docker-compose up -d

# 5. Run migrations
npm run migrate

# 6. Start development server
npm run dev
```

**GraphQL API Project:**
```bash
# 1. Scaffold GraphQL project
python scripts/api_scaffolder.py graphql-api --type graphql --stack apollo-typescript

# 2. Setup and start
cd graphql-api
npm install
cp .env.example .env
docker-compose up -d
npm run migrate
npm run dev

# 3. Access GraphQL Playground
# Open http://localhost:3000/graphql
```

---

## database_migration_tool.py

Comprehensive database migration management tool for creating, running, and rolling back database migrations across multiple databases.

### Overview

Automates database schema migrations with support for PostgreSQL, MySQL, and MongoDB. Includes migration generation, version tracking, rollback capabilities, and migration testing.

### Usage

**Basic Commands:**
```bash
# Create new migration
python scripts/database_migration_tool.py create "add_user_table"

# Run pending migrations
python scripts/database_migration_tool.py migrate

# Rollback last migration
python scripts/database_migration_tool.py rollback

# Show migration status
python scripts/database_migration_tool.py status

# Show help
python scripts/database_migration_tool.py --help
```

**Available Options:**
- `command`: Action to perform (create, migrate, rollback, status, reset)
- `name`: Migration name (for create command)
- `--database/-d`: Database type (postgresql, mysql, mongodb) - default: postgresql
- `--connection/-c`: Database connection string
- `--dry-run`: Preview changes without executing
- `--steps/-s`: Number of migrations to rollback - default: 1
- `--force/-f`: Force operation without confirmation
- `--verbose/-v`: Show detailed output

### Migration Commands

**Create Migration:**
```bash
# Create new migration file
python scripts/database_migration_tool.py create "add_user_table"

# Creates file: migrations/20250108_120000_add_user_table.sql
```

**Run Migrations:**
```bash
# Run all pending migrations
python scripts/database_migration_tool.py migrate

# Dry run (preview changes)
python scripts/database_migration_tool.py migrate --dry-run

# Run with verbose output
python scripts/database_migration_tool.py migrate --verbose
```

**Rollback Migrations:**
```bash
# Rollback last migration
python scripts/database_migration_tool.py rollback

# Rollback last 3 migrations
python scripts/database_migration_tool.py rollback --steps 3

# Force rollback without confirmation
python scripts/database_migration_tool.py rollback --force
```

**Check Status:**
```bash
# Show migration status
python scripts/database_migration_tool.py status

# Output:
# Migration Status
# ================
#
# Pending Migrations:
#   - 20250108_120000_add_user_table.sql
#   - 20250108_130000_add_post_table.sql
#
# Applied Migrations:
#   - 20250108_110000_create_schema.sql (applied: 2025-01-08 11:30:45)
```

### Migration File Format

**PostgreSQL Migration:**
```sql
-- migrations/20250108_120000_add_user_table.sql

-- UP Migration
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'USER',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Add trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE
    ON users FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- DOWN Migration (for rollback)
-- separator: -- DOWN --
DROP TABLE IF EXISTS users CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column();
```

### Features

**Version Tracking:**
- Stores migration history in database
- Tracks applied migrations with timestamps
- Prevents duplicate migrations
- Supports out-of-order migration detection

**Rollback Support:**
- DOWN migrations for reverting changes
- Multi-step rollback capability
- Transaction support for safety
- Dry-run mode for testing

**Safety Features:**
- Transaction wrapping for atomic operations
- Confirmation prompts for destructive operations
- Dry-run mode for previewing changes
- Migration checksum validation

**Multi-Database Support:**
- PostgreSQL (native)
- MySQL (dialect translation)
- MongoDB (schema-less migrations)

### Output Example

```bash
$ python scripts/database_migration_tool.py migrate

🔄 Database Migration Tool
==========================

Database: PostgreSQL
Connection: postgresql://localhost:5432/mydb

Pending Migrations: 2

Running migration: 20250108_120000_add_user_table.sql
  ✓ CREATE TABLE users
  ✓ CREATE INDEX idx_users_email
  ✓ CREATE TRIGGER update_users_updated_at
  Duration: 45ms

Running migration: 20250108_130000_add_post_table.sql
  ✓ CREATE TABLE posts
  ✓ CREATE INDEX idx_posts_author
  ✓ ADD FOREIGN KEY posts_author_fkey
  Duration: 52ms

✅ 2 migrations applied successfully
Total duration: 97ms
```

### Common Workflows

**Development Workflow:**
```bash
# 1. Create migration for new feature
python scripts/database_migration_tool.py create "add_comments_table"

# 2. Edit migration file
# vim migrations/20250108_140000_add_comments_table.sql

# 3. Test migration (dry-run)
python scripts/database_migration_tool.py migrate --dry-run

# 4. Apply migration
python scripts/database_migration_tool.py migrate

# 5. If issues, rollback
python scripts/database_migration_tool.py rollback
```

**Production Deployment:**
```bash
# 1. Check status before deployment
python scripts/database_migration_tool.py status

# 2. Backup database first
pg_dump -h localhost -U postgres mydb > backup.sql

# 3. Run migrations
python scripts/database_migration_tool.py migrate --verbose

# 4. Verify migration success
python scripts/database_migration_tool.py status
```

---

## api_load_tester.py

Advanced API load testing tool for stress testing, performance benchmarking, and capacity planning of backend APIs.

### Overview

Simulates real-world traffic patterns to test API performance under load. Supports concurrent requests, customizable scenarios, and detailed performance metrics.

### Usage

**Basic Commands:**
```bash
# Simple load test
python scripts/api_load_tester.py http://localhost:3000/api/users

# Custom concurrent users and requests
python scripts/api_load_tester.py http://localhost:3000/api/users --users 100 --requests 1000

# POST request load test
python scripts/api_load_tester.py http://localhost:3000/api/users --method POST --data user.json

# Load test with authentication
python scripts/api_load_tester.py http://localhost:3000/api/users --header "Authorization: Bearer token"

# Show help
python scripts/api_load_tester.py --help
```

**Available Options:**
- `url`: Target API endpoint (required)
- `--method/-m`: HTTP method (GET, POST, PUT, DELETE) - default: GET
- `--users/-u`: Concurrent users - default: 10
- `--requests/-r`: Total requests - default: 100
- `--duration/-d`: Test duration in seconds (alternative to --requests)
- `--data`: JSON file with request body (for POST/PUT)
- `--header/-H`: Custom headers (can be used multiple times)
- `--timeout`: Request timeout in seconds - default: 30
- `--output/-o`: Output format (text, json, html) - default: text
- `--save/-s`: Save report to file
- `--verbose/-v`: Show detailed output

### Load Testing Scenarios

**Steady Load Test:**
```bash
# 50 concurrent users, 1000 total requests
python scripts/api_load_tester.py http://localhost:3000/api/users \
  --users 50 \
  --requests 1000
```

**Spike Test:**
```bash
# Sudden spike: 200 concurrent users for 60 seconds
python scripts/api_load_tester.py http://localhost:3000/api/users \
  --users 200 \
  --duration 60
```

**Endurance Test:**
```bash
# Sustained load: 30 users for 30 minutes
python scripts/api_load_tester.py http://localhost:3000/api/users \
  --users 30 \
  --duration 1800
```

**Stress Test:**
```bash
# Increasing load until failure
python scripts/api_load_tester.py http://localhost:3000/api/users \
  --users 500 \
  --requests 5000
```

### Features

**Performance Metrics:**
- Response times (min, max, avg, median, p95, p99)
- Requests per second (RPS)
- Success/failure rates
- Error categorization
- Throughput (MB/s)
- Concurrent connections

**Request Customization:**
- Custom HTTP headers
- Request body from JSON file
- Query parameters
- Cookie support
- Authentication tokens

**Output Formats:**
- Text (console-friendly)
- JSON (machine-readable)
- HTML (visual reports)
- CSV (spreadsheet import)

### Output Example

```bash
$ python scripts/api_load_tester.py http://localhost:3000/api/users --users 50 --requests 1000

⚡ API Load Tester
==================

Target: http://localhost:3000/api/users
Method: GET
Concurrent Users: 50
Total Requests: 1000

Running load test... ██████████████████████████████ 100%

📊 Performance Results
======================

Total Requests: 1000
Successful: 985 (98.5%)
Failed: 15 (1.5%)
Duration: 12.45s

Requests/Second: 80.3 RPS
Throughput: 2.4 MB/s

Response Times:
  Min: 45ms
  Max: 1,234ms
  Avg: 156ms
  Median: 142ms
  P95: 287ms
  P99: 456ms

Errors:
  500 Internal Error: 10 (1.0%)
  503 Service Unavailable: 5 (0.5%)

✅ Load test completed successfully
```

**HTML Report:**
```bash
# Generate HTML report
python scripts/api_load_tester.py http://localhost:3000/api/users \
  --users 100 \
  --requests 1000 \
  --output html \
  --save report.html

# Open report in browser
# Includes charts for:
# - Response time distribution
# - Requests per second over time
# - Error rate timeline
# - Percentile breakdown
```

### Common Workflows

**API Health Check:**
```bash
# Quick health check
python scripts/api_load_tester.py http://localhost:3000/health \
  --users 10 \
  --requests 100
```

**Performance Benchmarking:**
```bash
# Benchmark API endpoint
python scripts/api_load_tester.py http://localhost:3000/api/users \
  --users 50 \
  --requests 1000 \
  --output json \
  --save baseline.json

# Compare after optimization
python scripts/api_load_tester.py http://localhost:3000/api/users \
  --users 50 \
  --requests 1000 \
  --output json \
  --save optimized.json

# Compare results
python scripts/compare_load_tests.py baseline.json optimized.json
```

**Capacity Planning:**
```bash
# Test increasing load levels
for users in 10 50 100 200 500; do
  echo "Testing with $users concurrent users..."
  python scripts/api_load_tester.py http://localhost:3000/api/users \
    --users $users \
    --requests 1000 \
    --output json \
    --save "load_test_${users}users.json"
done

# Analyze results to find capacity limits
```

### Best Practices

**Before Load Testing:**
1. Test in staging environment (never production)
2. Baseline current performance
3. Set up monitoring (CPU, memory, database)
4. Inform team of testing schedule

**During Load Testing:**
1. Monitor server metrics
2. Watch for error rate spikes
3. Track database connection pool
4. Check log files for errors

**After Load Testing:**
1. Analyze bottlenecks
2. Document findings
3. Create optimization tickets
4. Re-test after improvements

### Integration with Monitoring

**Grafana Dashboard:**
```bash
# Run load test while monitoring Grafana
python scripts/api_load_tester.py http://localhost:3000/api/users \
  --users 100 \
  --duration 300 \
  --verbose

# Correlate load test timeline with:
# - CPU usage
# - Memory consumption
# - Database queries
# - Response times
```

This comprehensive tool documentation provides everything needed to scaffold, migrate, and load test backend APIs effectively.
