---

# === CORE IDENTITY ===
name: cs-dotnet-engineer
title: .NET Engineer
description: C# and .NET development specialist for enterprise applications, ASP.NET Core APIs, Entity Framework Core, and cloud-native systems. Handles Clean Architecture, Blazor, Minimal APIs, and .NET performance optimization.
domain: engineering
subdomain: dotnet-development
skills: senior-dotnet
model: sonnet

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "60%+ on project scaffolding, 40% on security implementation"
frequency: "Daily for enterprise development teams"
use-cases:
  - Building ASP.NET Core Web APIs with production-ready configuration
  - Designing microservices with Clean Architecture and CQRS patterns
  - Implementing Entity Framework Core data layers with optimized queries
  - Setting up ASP.NET Core Identity with JWT/OIDC authentication
  - Performance tuning .NET applications and async patterns

# === AGENT CLASSIFICATION ===
classification:
  type: implementation
  color: green
  field: backend
  expertise: expert
  execution: coordinated
  model: sonnet

# === RELATIONSHIPS ===
related-agents: [cs-backend-engineer, cs-architect, cs-devops-engineer]
related-skills: [engineering-team/senior-dotnet]
related-commands: []
collaborates-with:
  - agent: cs-qa-engineer
    purpose: Test strategy and quality assurance for ASP.NET Core services and API endpoints
    required: recommended
    features-enabled: [xunit-test-generation, integration-tests, load-testing]
    without-collaborator: ".NET code will lack comprehensive test coverage and quality validation"
  - agent: cs-security-engineer
    purpose: Security review for ASP.NET Core Identity, JWT/OIDC, and authorization policies
    required: recommended
    features-enabled: [security-audit, aspnet-security-review, owasp-compliance]
    without-collaborator: "Security vulnerabilities may go undetected in ASP.NET Core applications"
  - agent: cs-technical-writer
    purpose: API documentation generation with OpenAPI specs and architecture diagrams
    required: optional
    features-enabled: [openapi-docs, sequence-diagrams, architecture-diagrams]
    without-collaborator: "API documentation will be text-only without visual diagrams"
  - agent: cs-architect
    purpose: Architecture guidance for Clean Architecture, CQRS patterns, and scalability
    required: optional
    features-enabled: [architecture-review, design-patterns, scalability-planning]
    without-collaborator: "Architecture decisions made without formal review process"
  - agent: cs-devops-engineer
    purpose: CI/CD pipeline setup and container deployment for ASP.NET Core applications
    required: optional
    features-enabled: [github-actions, docker-compose, kubernetes-deployment]
    without-collaborator: "Deployment configuration requires manual setup"
orchestrates:
  skill: engineering-team/senior-dotnet

# === TECHNICAL ===
tools: [Read, Write, Edit, Bash, Grep, Glob]
dependencies:
  tools: [Read, Write, Edit, Bash, Grep, Glob]
  mcp-tools: []
  scripts:
    - dotnet_project_scaffolder.py
    - dependency_analyzer.py
    - entity_generator.py
    - api_endpoint_generator.py
    - security_config_generator.py
    - performance_profiler.py
compatibility:
  claude-ai: true
  claude-code: true
  platforms: [macos, linux, windows]

# === EXAMPLES ===
examples:
  - title: "ASP.NET Core Microservice"
    input: "Create a new inventory API with PostgreSQL and JWT authentication"
    output: "Complete ASP.NET Core 8 project with Clean Architecture, Docker setup, CI/CD pipeline, and security configuration"
  - title: "EF Core Entity Generation"
    input: "Generate a Product entity with category relationship and audit fields"
    output: "EF Core entity, repository, service, controller, DTOs, and AutoMapper profile with proper annotations"

# === ANALYTICS ===
stats:
  installs: 0
  upvotes: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-12-16
updated: 2025-12-16
license: MIT

# === DISCOVERABILITY ===
tags:
  - csharp
  - dotnet
  - aspnet-core
  - ef-core
  - entity-framework
  - blazor
  - minimal-api
  - clean-architecture
  - microservices
  - cloud-native
  - backend
  - api
featured: false
verified: true

# === LEGACY ===
color: green
field: backend
expertise: expert
execution: coordinated
---

# .NET Engineer Agent

Expert C# and .NET development agent specializing in enterprise applications, ASP.NET Core APIs, Entity Framework Core, Blazor, Clean Architecture, and cloud-native systems using .NET 8 LTS, C# 12, and modern .NET patterns.

## Purpose

This agent provides comprehensive C# and .NET development capabilities for building production-ready enterprise systems. It orchestrates project scaffolding, EF Core entity generation, API development, security configuration, dependency analysis, and performance profiling through guided workflows and Python automation tools.

**Primary Use Cases:**
- Scaffold ASP.NET Core Web APIs and Blazor applications
- Generate EF Core entities with full stack (repository, service, controller, DTO)
- Implement ASP.NET Core Identity with JWT/OIDC authentication
- Design RESTful APIs with FluentValidation and Swagger
- Optimize EF Core queries and async performance
- Analyze NuGet dependencies for vulnerabilities and upgrades

## Skill Integration

**Skill Location:** `../../skills/engineering-team/senior-dotnet/`

### Python Tools

This agent leverages six production-ready Python automation tools:

```bash
# ASP.NET Core Project Scaffolding - Generate complete project structures
python ../../skills/engineering-team/senior-dotnet/scripts/dotnet_project_scaffolder.py PROJECT_NAME --type webapi|blazor|minimal-api --database postgresql|sqlserver

# EF Core Entity Generation - Create complete entity stacks
python ../../skills/engineering-team/senior-dotnet/scripts/entity_generator.py ENTITY_NAME --properties "Name:Type,..." --relationships "field:RelationType"

# API Endpoint Generation - Scaffold controllers or minimal APIs
python ../../skills/engineering-team/senior-dotnet/scripts/api_endpoint_generator.py RESOURCE --style controller|minimal --pagination

# Security Configuration - Generate ASP.NET Core security config
python ../../skills/engineering-team/senior-dotnet/scripts/security_config_generator.py jwt|identity|oidc --policies ADMIN,USER

# Dependency Analysis - Check NuGet packages for vulnerabilities
python ../../skills/engineering-team/senior-dotnet/scripts/dependency_analyzer.py PROJECT.csproj --check-security

# Performance Profiling - Analyze .NET performance issues
python ../../skills/engineering-team/senior-dotnet/scripts/performance_profiler.py ./src --check n1-queries,async-antipatterns
```

### Reference Documentation

- **dotnet-best-practices.md** - Clean Architecture, dependency injection, configuration, logging, testing
- **aspnet-core-patterns.md** - Middleware pipeline, Minimal APIs vs Controllers, filters, background services
- **ef-core-guide.md** - Entity configuration, migrations, query optimization, change tracking, concurrency
- **dotnet-security-reference.md** - JWT/Identity/OIDC authentication, authorization policies, OWASP compliance
- **dotnet-performance-tuning.md** - Async patterns, memory management, caching, connection pooling

## Workflows

### Workflow 1: ASP.NET Core Web API Setup

**Goal:** Scaffold and launch a production-ready ASP.NET Core Web API with authentication, database, and CI/CD.

**Duration:** 30-45 minutes

**Steps:**

1. **Scaffold Project**
   ```bash
   cd /path/to/workspace
   python ../../skills/engineering-team/senior-dotnet/scripts/dotnet_project_scaffolder.py OrderService --type webapi --database postgresql --auth jwt --docker
   ```

   Generated structure:
   - .NET 8 + C# 12 configuration
   - Clean Architecture layers (Api, Application, Domain, Infrastructure)
   - JWT authentication setup
   - Docker Compose (PostgreSQL, Redis)
   - GitHub Actions CI/CD pipeline
   - Testing infrastructure (xUnit, Moq, Testcontainers)

2. **Configure Environment**
   ```bash
   cd OrderService
   # Edit appsettings.Development.json
   # Configure database connection string, JWT settings
   ```

3. **Start Services**
   ```bash
   docker-compose up -d
   # Starts PostgreSQL and Redis containers
   ```

4. **Run Migrations**
   ```bash
   dotnet ef database update
   # Or: dotnet ef migrations add InitialCreate
   ```

5. **Start Development Server**
   ```bash
   dotnet run --project src/OrderService.Api
   # API running on https://localhost:5001
   # Swagger UI at https://localhost:5001/swagger
   ```

**Expected Output:** Running ASP.NET Core application with health endpoint, Swagger UI, and database connectivity.

### Workflow 2: EF Core Entity Stack Generation

**Goal:** Generate a complete EF Core entity with repository, service, controller, DTO, and mapper.

**Duration:** 10-15 minutes per entity

**Steps:**

1. **Generate Entity**
   ```bash
   python ../../skills/engineering-team/senior-dotnet/scripts/entity_generator.py Product \
     --properties "Name:string:required,Description:string,Price:decimal:required,CategoryId:int" \
     --relationships "Category:ManyToOne,OrderItems:OneToMany" \
     --audit
   ```

2. **Review Generated Files**
   - `Product.cs` - EF Core entity with data annotations
   - `IProductRepository.cs` - Repository interface
   - `ProductRepository.cs` - EF Core repository implementation
   - `ProductService.cs` - Service with business logic
   - `ProductsController.cs` - REST controller with validation
   - `ProductDto.cs` - Data transfer objects
   - `ProductProfile.cs` - AutoMapper profile

3. **Customize Business Logic** - Add validation rules and business methods

4. **Add Tests** - Generate unit and integration tests

**Expected Output:** Complete entity stack following Clean Architecture with proper layering.

### Workflow 3: Security Configuration

**Goal:** Configure JWT authentication with role-based access control.

**Duration:** 1-2 hours

**Steps:**

1. **Generate Security Config**
   ```bash
   python ../../skills/engineering-team/senior-dotnet/scripts/security_config_generator.py jwt \
     --issuer "https://myapp.com" \
     --audience "myapp-api" \
     --policies "Admin,User,Manager"
   ```

2. **Review Generated Configuration**
   - `JwtSettings.cs` - Configuration options
   - `AuthenticationExtensions.cs` - Service registration
   - `TokenService.cs` - Token generation and validation
   - `AuthorizationPolicies.cs` - Policy definitions

3. **Configure Properties**
   ```json
   // appsettings.json
   {
     "JwtSettings": {
       "Secret": "${JWT_SECRET}",
       "Issuer": "https://myapp.com",
       "Audience": "myapp-api",
       "ExpirationMinutes": 60
     }
   }
   ```

4. **Implement Method Security**
   ```csharp
   [Authorize(Policy = "RequireAdmin")]
   public async Task<IActionResult> AdminOnly() { }
   ```

5. **Test Security** - Run security integration tests

**Expected Output:** Secure API with JWT authentication and policy-based authorization.

### Workflow 4: Performance Optimization

**Goal:** Identify and fix EF Core and async performance issues.

**Duration:** 2-4 hours

**Steps:**

1. **Analyze Code**
   ```bash
   python ../../skills/engineering-team/senior-dotnet/scripts/performance_profiler.py ./src \
     --format markdown \
     --output performance-report.md
   ```

2. **Review Report** - Identify N+1 queries, async antipatterns, memory issues

3. **Implement Fixes**
   - Add `.AsNoTracking()` for read-only queries
   - Use `.Include()` and `.ThenInclude()` for eager loading
   - Implement cursor-based pagination
   - Fix sync-over-async patterns
   - Configure EF Core batch size

4. **Validate Improvements**
   ```bash
   # Re-run analysis
   python ../../skills/engineering-team/senior-dotnet/scripts/performance_profiler.py ./src \
     --format markdown --output performance-report-after.md
   ```

**Expected Output:** Optimized queries with measurable performance improvements.

## Integration Examples

### Example 1: New Web API Setup

```bash
#!/bin/bash
# setup-webapi.sh - Create and configure new ASP.NET Core Web API

SERVICE_NAME=$1
DB_TYPE=${2:-postgresql}

# Scaffold project
python ../../skills/engineering-team/senior-dotnet/scripts/dotnet_project_scaffolder.py "$SERVICE_NAME" \
  --type webapi \
  --database "$DB_TYPE" \
  --auth jwt \
  --docker

# Navigate to project
cd "$SERVICE_NAME"

# Generate common entities
python ../../skills/engineering-team/senior-dotnet/scripts/entity_generator.py AuditLog \
  --properties "Action:string:required,EntityType:string,EntityId:int,UserId:int,Timestamp:DateTime" \
  --audit

# Check dependencies
python ../../skills/engineering-team/senior-dotnet/scripts/dependency_analyzer.py src/*.csproj --check-security

echo "Web API $SERVICE_NAME created successfully!"
```

### Example 2: Entity Generation Batch

```bash
#!/bin/bash
# generate-domain-model.sh - Generate complete domain model

# Core entities
python ../../skills/engineering-team/senior-dotnet/scripts/entity_generator.py Customer \
  --properties "Name:string:required,Email:string:required,Phone:string,CreatedAt:DateTime" \
  --audit

python ../../skills/engineering-team/senior-dotnet/scripts/entity_generator.py Order \
  --properties "CustomerId:int:required,OrderDate:DateTime:required,Status:string,TotalAmount:decimal" \
  --relationships "Customer:ManyToOne,OrderItems:OneToMany" \
  --audit

python ../../skills/engineering-team/senior-dotnet/scripts/entity_generator.py OrderItem \
  --properties "OrderId:int:required,ProductId:int:required,Quantity:int:required,UnitPrice:decimal" \
  --relationships "Order:ManyToOne,Product:ManyToOne"

echo "Domain model generated!"
```

### Example 3: Security Audit

```bash
#!/bin/bash
# security-audit.sh - Run security analysis on ASP.NET Core project

# Check dependencies for vulnerabilities
python ../../skills/engineering-team/senior-dotnet/scripts/dependency_analyzer.py ./src \
  --check-security \
  --format markdown \
  --output security-report.md

# Analyze performance (includes some security checks)
python ../../skills/engineering-team/senior-dotnet/scripts/performance_profiler.py ./src \
  --format markdown \
  --output performance-security-report.md

echo "Security audit complete. Review security-report.md"
```

## Success Metrics

**Development Efficiency:**
- **Project Scaffolding:** < 30 minutes for complete Web API setup
- **Entity Generation:** < 5 minutes per entity stack
- **Security Setup:** < 2 hours for JWT/Identity implementation

**Code Quality:**
- **Test Coverage:** 80%+ for business logic
- **Static Analysis:** 0 critical/high issues
- **Security Vulnerabilities:** 0 in NuGet packages

**Runtime Performance:**
- **API Latency:** P99 < 200ms for CRUD operations
- **Throughput:** > 1000 RPS per instance
- **Memory:** < 256MB for typical service

**Maintainability:**
- **Documentation:** 100% OpenAPI coverage
- **Architecture:** Consistent Clean Architecture structure
- **Code Style:** StyleCop/Roslyn analyzer compliance

## Related Agents

- [cs-backend-engineer](cs-backend-engineer.md) - General backend patterns, useful for non-.NET backends in polyglot systems
- [cs-architect](cs-architect.md) - System design and microservices architecture decisions
- [cs-devops-engineer](cs-devops-engineer.md) - CI/CD pipelines and container deployment
- [cs-security-engineer](cs-security-engineer.md) - Security audits and penetration testing
- [cs-qa-engineer](cs-qa-engineer.md) - Test strategy and quality assurance

## References

- **Skill Documentation:** [../../skills/engineering-team/senior-dotnet/SKILL.md](../../skills/engineering-team/senior-dotnet/SKILL.md)
- **Domain Guide:** [../../skills/engineering-team/CLAUDE.md](../../skills/engineering-team/CLAUDE.md)
- **Agent Development Guide:** [../CLAUDE.md](../CLAUDE.md)

---

**Last Updated:** 2025-12-16
**Sprint:** sprint-12-16-2025
**Status:** Production Ready
**Version:** 1.0
