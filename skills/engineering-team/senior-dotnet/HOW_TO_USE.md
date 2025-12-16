# How to Use: Senior .NET Skill

Quick start guide for using the senior-dotnet skill for C#/.NET development.

## Quick Start

### 1. Scaffold a New Project

```bash
# Create a Web API with PostgreSQL, JWT auth, and Docker
python3 scripts/dotnet_project_scaffolder.py MyApi \
  --type webapi \
  --database postgresql \
  --auth jwt \
  --docker \
  --output ./projects

# Create a Blazor Server app with SQL Server and Identity
python3 scripts/dotnet_project_scaffolder.py MyApp \
  --type blazor \
  --database sqlserver \
  --auth identity \
  --output ./projects

# Create minimal API with Clean Architecture
python3 scripts/dotnet_project_scaffolder.py MyService \
  --type minimal-api \
  --architecture clean \
  --database postgresql \
  --output ./projects
```

### 2. Generate Entity Stack

```bash
# Generate full entity stack (Entity, Repository, Service, Controller, DTOs)
python3 scripts/entity_generator.py Product \
  --properties "Name:string:required,Price:decimal:required,Description:string,CategoryId:int" \
  --output ./src/Domain

# Generate with relationships
python3 scripts/entity_generator.py Order \
  --properties "OrderDate:DateTime:required,TotalAmount:decimal,Status:string" \
  --relationships "Customer:ManyToOne,OrderItems:OneToMany" \
  --audit \
  --output ./src/Domain
```

### 3. Create API Endpoints

```bash
# Generate Controller-style endpoints
python3 scripts/api_endpoint_generator.py Products \
  --entity Product \
  --style controller \
  --pagination \
  --output ./src/Web/Controllers

# Generate Minimal API endpoints
python3 scripts/api_endpoint_generator.py Orders \
  --entity Order \
  --style minimal \
  --validation \
  --output ./src/Web/Endpoints
```

### 4. Analyze Dependencies

```bash
# Check for vulnerabilities
python3 scripts/dependency_analyzer.py MyProject.csproj --check-security

# Full analysis with markdown report
python3 scripts/dependency_analyzer.py ./src \
  --check-security \
  --format markdown \
  --output dependency-report.md
```

### 5. Configure Security

```bash
# Generate JWT authentication setup
python3 scripts/security_config_generator.py jwt \
  --issuer "https://myapp.com" \
  --audience "myapp-api" \
  --output ./src/Infrastructure/Security

# Generate Identity with policies
python3 scripts/security_config_generator.py identity \
  --policies "Admin,Manager,User" \
  --output ./src/Infrastructure/Security

# Generate OIDC configuration
python3 scripts/security_config_generator.py oidc \
  --authority "https://login.microsoftonline.com/tenant" \
  --client-id "app-client-id" \
  --output ./src/Infrastructure/Security
```

### 6. Profile Performance

```bash
# Analyze C# code for performance issues
python3 scripts/performance_profiler.py ./src \
  --format markdown \
  --output performance-report.md

# Check for specific issues
python3 scripts/performance_profiler.py ./src/Repositories \
  --check n1-queries \
  --check async-antipatterns
```

## Common Workflows

### New Web API Project

1. **Scaffold project:**
   ```bash
   python3 scripts/dotnet_project_scaffolder.py OrdersApi \
     --type webapi \
     --database postgresql \
     --auth jwt \
     --docker \
     --cicd github
   ```

2. **Generate domain entities:**
   ```bash
   python3 scripts/entity_generator.py Order \
     --properties "CustomerId:int:required,OrderDate:DateTime,Status:OrderStatus" \
     --relationships "OrderItems:OneToMany,Customer:ManyToOne" \
     --audit

   python3 scripts/entity_generator.py OrderItem \
     --properties "ProductId:int:required,Quantity:int:required,UnitPrice:decimal" \
     --relationships "Order:ManyToOne,Product:ManyToOne"
   ```

3. **Create endpoints:**
   ```bash
   python3 scripts/api_endpoint_generator.py Orders \
     --entity Order \
     --style controller \
     --pagination \
     --validation
   ```

4. **Configure security:**
   ```bash
   python3 scripts/security_config_generator.py jwt \
     --policies "Admin,Customer"
   ```

### Modernizing Legacy Code

1. **Analyze dependencies:**
   ```bash
   python3 scripts/dependency_analyzer.py ./LegacyApp \
     --check-security \
     --format markdown \
     --output dependency-audit.md
   ```

2. **Profile performance:**
   ```bash
   python3 scripts/performance_profiler.py ./LegacyApp \
     --format markdown \
     --output performance-audit.md
   ```

3. **Review reports and prioritize fixes**

### Adding New Feature

1. **Generate entity:**
   ```bash
   python3 scripts/entity_generator.py Feature \
     --properties "Name:string:required,Description:string,IsEnabled:bool"
   ```

2. **Create API:**
   ```bash
   python3 scripts/api_endpoint_generator.py Features \
     --entity Feature \
     --validation
   ```

3. **Run security check:**
   ```bash
   python3 scripts/dependency_analyzer.py . --check-security
   ```

## What to Provide

| Tool | Required Input | Optional Input |
|------|----------------|----------------|
| **Project Scaffolder** | Project name | Type, database, auth, architecture |
| **Entity Generator** | Entity name, properties | Relationships, audit fields |
| **Endpoint Generator** | Resource name, entity | Style, pagination, validation |
| **Dependency Analyzer** | Project path | Security check, output format |
| **Security Generator** | Auth type | Issuer, audience, policies |
| **Performance Profiler** | Code path | Specific checks, output format |

## What to Expect

### Project Scaffolder Output
- Complete project structure
- Program.cs with configured services
- appsettings.json templates
- Docker and CI/CD files (optional)

### Entity Generator Output
- Entity class with data annotations
- Repository interface and implementation
- Service layer with business logic
- Controller with CRUD operations
- DTOs for API contracts
- AutoMapper profile

### Endpoint Generator Output
- Controller or Minimal API handlers
- FluentValidation validators
- Pagination support (optional)
- OpenAPI annotations

### Dependency Analyzer Output
- Package inventory
- Vulnerability warnings
- Upgrade recommendations
- Framework compatibility notes

### Security Generator Output
- Authentication configuration
- Authorization policies
- Token service (JWT)
- Security middleware setup

### Performance Profiler Output
- N+1 query detection
- Async/await issues
- Memory allocation warnings
- EF Core optimization tips

## Reference Documentation

For in-depth guidance, see:

- [dotnet-best-practices.md](references/dotnet-best-practices.md) - Architecture patterns
- [aspnet-core-patterns.md](references/aspnet-core-patterns.md) - ASP.NET Core patterns
- [ef-core-guide.md](references/ef-core-guide.md) - Entity Framework Core
- [dotnet-security-reference.md](references/dotnet-security-reference.md) - Security implementation
- [dotnet-performance-tuning.md](references/dotnet-performance-tuning.md) - Performance optimization

## Tips

1. **Start with scaffolding** - Use project scaffolder for consistent structure
2. **Generate entities early** - Build your domain model with entity generator
3. **Check dependencies regularly** - Run security checks before releases
4. **Profile before optimizing** - Use profiler to identify actual bottlenecks
5. **Use Clean Architecture** - For larger projects, use `--architecture clean`

---

**Skill:** senior-dotnet
**Version:** 1.0.0
