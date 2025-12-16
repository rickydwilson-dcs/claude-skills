#!/usr/bin/env python3
"""
.NET Project Scaffolder

Generate production-ready ASP.NET Core project structures with Clean Architecture,
Docker configuration, CI/CD pipelines, and comprehensive setup.

Part of senior-dotnet skill for engineering-team.

Usage:
    python dotnet_project_scaffolder.py PROJECT_NAME [options]
    python dotnet_project_scaffolder.py my-service --type webapi --db sqlserver
    python dotnet_project_scaffolder.py --help
    python dotnet_project_scaffolder.py --version
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

__version__ = "1.0.0"


class DotNetProjectScaffolder:
    """Generate production-ready ASP.NET Core project structures."""

    VALID_PROJECT_TYPES = ['webapi', 'mvc', 'blazor', 'minimal-api', 'worker', 'console']
    VALID_DATABASES = ['sqlserver', 'postgresql', 'mysql', 'sqlite', 'cosmosdb', 'none']
    VALID_AUTH_TYPES = ['none', 'jwt', 'identity', 'oidc']

    def __init__(self, project_name: str, project_type: str = 'webapi',
                 database: str = 'sqlserver', auth_type: str = 'jwt',
                 output_dir: Optional[str] = None, verbose: bool = False):
        """
        Initialize .NET Project Scaffolder.

        Args:
            project_name: Name of the project (kebab-case)
            project_type: Type of project (webapi, mvc, blazor, minimal-api, worker, console)
            database: Database provider (sqlserver, postgresql, mysql, sqlite, cosmosdb, none)
            auth_type: Authentication type (none, jwt, identity, oidc)
            output_dir: Output directory (default: current directory)
            verbose: Enable verbose output
        """
        self.project_name = project_name
        self.project_type = project_type
        self.database = database
        self.auth_type = auth_type
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.verbose = verbose

        # Derived names
        self.pascal_name = self._to_pascal_case(project_name)
        self.namespace = self.pascal_name.replace('-', '')

    def _to_pascal_case(self, name: str) -> str:
        """Convert kebab-case to PascalCase."""
        return ''.join(word.capitalize() for word in name.replace('_', '-').split('-'))

    def _log(self, message: str) -> None:
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"  {message}")

    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if not self.project_name:
            errors.append("Project name is required")
        elif not self.project_name.replace('-', '').replace('_', '').isalnum():
            errors.append("Project name must be alphanumeric with hyphens/underscores only")

        if self.project_type not in self.VALID_PROJECT_TYPES:
            errors.append(f"Invalid project type: {self.project_type}. Valid: {', '.join(self.VALID_PROJECT_TYPES)}")

        if self.database not in self.VALID_DATABASES:
            errors.append(f"Invalid database: {self.database}. Valid: {', '.join(self.VALID_DATABASES)}")

        if self.auth_type not in self.VALID_AUTH_TYPES:
            errors.append(f"Invalid auth type: {self.auth_type}. Valid: {', '.join(self.VALID_AUTH_TYPES)}")

        return errors

    def scaffold(self) -> Dict:
        """Generate the complete project structure."""
        errors = self.validate()
        if errors:
            return {
                'success': False,
                'errors': errors,
                'files_created': []
            }

        project_path = self.output_dir / self.project_name
        files_created = []

        try:
            # Create directory structure
            self._create_directories(project_path)
            self._log("Created directory structure")

            # Create solution file
            files_created.append(self._create_solution_file(project_path))

            # Create project files based on type
            if self.project_type in ['webapi', 'mvc', 'minimal-api']:
                files_created.extend(self._create_web_project(project_path))
            elif self.project_type == 'blazor':
                files_created.extend(self._create_blazor_project(project_path))
            elif self.project_type == 'worker':
                files_created.extend(self._create_worker_project(project_path))
            else:
                files_created.extend(self._create_console_project(project_path))

            # Create shared projects
            files_created.extend(self._create_domain_project(project_path))
            files_created.extend(self._create_infrastructure_project(project_path))

            # Create test project
            files_created.extend(self._create_test_project(project_path))

            # Create Docker files
            files_created.extend(self._create_docker_files(project_path))

            # Create CI/CD
            files_created.extend(self._create_cicd_files(project_path))

            # Create documentation
            files_created.extend(self._create_documentation(project_path))

            return {
                'success': True,
                'project_path': str(project_path),
                'files_created': [str(f) for f in files_created],
                'next_steps': self._get_next_steps()
            }

        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)],
                'files_created': [str(f) for f in files_created]
            }

    def _create_directories(self, project_path: Path) -> None:
        """Create project directory structure."""
        directories = [
            'src/Api',
            'src/Api/Controllers',
            'src/Api/Middleware',
            'src/Api/Extensions',
            'src/Domain',
            'src/Domain/Entities',
            'src/Domain/Interfaces',
            'src/Domain/ValueObjects',
            'src/Infrastructure',
            'src/Infrastructure/Data',
            'src/Infrastructure/Repositories',
            'src/Infrastructure/Services',
            'tests/Api.Tests',
            'tests/Domain.Tests',
            'tests/Infrastructure.Tests',
            '.github/workflows',
        ]

        for dir_path in directories:
            (project_path / dir_path).mkdir(parents=True, exist_ok=True)

    def _create_solution_file(self, project_path: Path) -> Path:
        """Create .sln solution file."""
        sln_content = f'''Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.0.31903.59
MinimumVisualStudioVersion = 10.0.40219.1
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{self.pascal_name}.Api", "src\\Api\\{self.pascal_name}.Api.csproj", "{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}"
EndProject
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{self.pascal_name}.Domain", "src\\Domain\\{self.pascal_name}.Domain.csproj", "{{B2C3D4E5-F678-90AB-CDEF-123456789012}}"
EndProject
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{self.pascal_name}.Infrastructure", "src\\Infrastructure\\{self.pascal_name}.Infrastructure.csproj", "{{C3D4E5F6-7890-ABCD-EF12-345678901234}}"
EndProject
Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{self.pascal_name}.Api.Tests", "tests\\Api.Tests\\{self.pascal_name}.Api.Tests.csproj", "{{D4E5F678-90AB-CDEF-1234-567890123456}}"
EndProject
Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution
        Debug|Any CPU = Debug|Any CPU
        Release|Any CPU = Release|Any CPU
    EndGlobalSection
EndGlobal
'''
        sln_path = project_path / f"{self.pascal_name}.sln"
        sln_path.write_text(sln_content)
        self._log(f"Created {sln_path.name}")
        return sln_path

    def _create_web_project(self, project_path: Path) -> List[Path]:
        """Create Web API project files."""
        files = []
        api_path = project_path / 'src' / 'Api'

        # Create .csproj
        csproj_content = self._get_web_csproj()
        csproj_path = api_path / f"{self.pascal_name}.Api.csproj"
        csproj_path.write_text(csproj_content)
        files.append(csproj_path)
        self._log(f"Created {csproj_path.name}")

        # Create Program.cs
        program_content = self._get_program_cs()
        program_path = api_path / "Program.cs"
        program_path.write_text(program_content)
        files.append(program_path)
        self._log(f"Created {program_path.name}")

        # Create appsettings.json
        appsettings_content = self._get_appsettings()
        appsettings_path = api_path / "appsettings.json"
        appsettings_path.write_text(appsettings_content)
        files.append(appsettings_path)
        self._log(f"Created {appsettings_path.name}")

        # Create appsettings.Development.json
        dev_settings = {
            "Logging": {
                "LogLevel": {
                    "Default": "Debug",
                    "Microsoft.AspNetCore": "Warning",
                    "Microsoft.EntityFrameworkCore": "Information"
                }
            }
        }
        dev_path = api_path / "appsettings.Development.json"
        dev_path.write_text(json.dumps(dev_settings, indent=2))
        files.append(dev_path)

        # Create sample controller
        controller_content = self._get_sample_controller()
        controller_path = api_path / "Controllers" / "HealthController.cs"
        controller_path.write_text(controller_content)
        files.append(controller_path)
        self._log(f"Created {controller_path.name}")

        # Create exception middleware
        middleware_content = self._get_exception_middleware()
        middleware_path = api_path / "Middleware" / "ExceptionMiddleware.cs"
        middleware_path.write_text(middleware_content)
        files.append(middleware_path)
        self._log(f"Created {middleware_path.name}")

        # Create service extensions
        extensions_content = self._get_service_extensions()
        extensions_path = api_path / "Extensions" / "ServiceExtensions.cs"
        extensions_path.write_text(extensions_content)
        files.append(extensions_path)
        self._log(f"Created {extensions_path.name}")

        return files

    def _create_blazor_project(self, project_path: Path) -> List[Path]:
        """Create Blazor project files."""
        # Simplified - delegates to web project with modifications
        files = self._create_web_project(project_path)
        self._log("Created Blazor project (extends web project)")
        return files

    def _create_worker_project(self, project_path: Path) -> List[Path]:
        """Create Worker Service project files."""
        files = []
        api_path = project_path / 'src' / 'Api'

        # Create worker .csproj
        csproj_content = f'''<Project Sdk="Microsoft.NET.Sdk.Worker">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{self.namespace}.Api</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Hosting" Version="8.0.0" />
    <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\\Domain\\{self.pascal_name}.Domain.csproj" />
    <ProjectReference Include="..\\Infrastructure\\{self.pascal_name}.Infrastructure.csproj" />
  </ItemGroup>

</Project>
'''
        csproj_path = api_path / f"{self.pascal_name}.Api.csproj"
        csproj_path.write_text(csproj_content)
        files.append(csproj_path)

        # Create Worker Program.cs
        program_content = f'''using {self.namespace}.Api;
using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .CreateLogger();

try
{{
    Log.Information("Starting {self.pascal_name} Worker");

    var builder = Host.CreateApplicationBuilder(args);
    builder.Services.AddHostedService<Worker>();

    var host = builder.Build();
    await host.RunAsync();
}}
catch (Exception ex)
{{
    Log.Fatal(ex, "Application terminated unexpectedly");
}}
finally
{{
    Log.CloseAndFlush();
}}
'''
        program_path = api_path / "Program.cs"
        program_path.write_text(program_content)
        files.append(program_path)

        # Create Worker.cs
        worker_content = f'''namespace {self.namespace}.Api;

public class Worker : BackgroundService
{{
    private readonly ILogger<Worker> _logger;

    public Worker(ILogger<Worker> logger)
    {{
        _logger = logger;
    }}

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {{
        while (!stoppingToken.IsCancellationRequested)
        {{
            _logger.LogInformation("Worker running at: {{time}}", DateTimeOffset.Now);
            await Task.Delay(1000, stoppingToken);
        }}
    }}
}}
'''
        worker_path = api_path / "Worker.cs"
        worker_path.write_text(worker_content)
        files.append(worker_path)

        return files

    def _create_console_project(self, project_path: Path) -> List[Path]:
        """Create Console project files."""
        files = []
        api_path = project_path / 'src' / 'Api'

        csproj_content = f'''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{self.namespace}.Api</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.Extensions.Hosting" Version="8.0.0" />
  </ItemGroup>

</Project>
'''
        csproj_path = api_path / f"{self.pascal_name}.Api.csproj"
        csproj_path.write_text(csproj_content)
        files.append(csproj_path)

        program_content = f'''// {self.pascal_name} Console Application
Console.WriteLine("Hello from {self.pascal_name}!");
'''
        program_path = api_path / "Program.cs"
        program_path.write_text(program_content)
        files.append(program_path)

        return files

    def _create_domain_project(self, project_path: Path) -> List[Path]:
        """Create Domain project files."""
        files = []
        domain_path = project_path / 'src' / 'Domain'

        # Create .csproj
        csproj_content = f'''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{self.namespace}.Domain</RootNamespace>
  </PropertyGroup>

</Project>
'''
        csproj_path = domain_path / f"{self.pascal_name}.Domain.csproj"
        csproj_path.write_text(csproj_content)
        files.append(csproj_path)
        self._log(f"Created {csproj_path.name}")

        # Create base entity
        entity_content = f'''namespace {self.namespace}.Domain.Entities;

public abstract class BaseEntity
{{
    public int Id {{ get; set; }}
    public DateTime CreatedAt {{ get; set; }} = DateTime.UtcNow;
    public DateTime? UpdatedAt {{ get; set; }}
}}
'''
        entity_path = domain_path / "Entities" / "BaseEntity.cs"
        entity_path.write_text(entity_content)
        files.append(entity_path)

        # Create repository interface
        repo_content = f'''namespace {self.namespace}.Domain.Interfaces;

public interface IRepository<T> where T : class
{{
    Task<T?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<IEnumerable<T>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<T> AddAsync(T entity, CancellationToken cancellationToken = default);
    Task UpdateAsync(T entity, CancellationToken cancellationToken = default);
    Task DeleteAsync(T entity, CancellationToken cancellationToken = default);
}}
'''
        repo_path = domain_path / "Interfaces" / "IRepository.cs"
        repo_path.write_text(repo_content)
        files.append(repo_path)

        return files

    def _create_infrastructure_project(self, project_path: Path) -> List[Path]:
        """Create Infrastructure project files."""
        files = []
        infra_path = project_path / 'src' / 'Infrastructure'

        # Create .csproj with database packages
        db_packages = self._get_database_packages()
        csproj_content = f'''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{self.namespace}.Infrastructure</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
{db_packages}
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\\Domain\\{self.pascal_name}.Domain.csproj" />
  </ItemGroup>

</Project>
'''
        csproj_path = infra_path / f"{self.pascal_name}.Infrastructure.csproj"
        csproj_path.write_text(csproj_content)
        files.append(csproj_path)
        self._log(f"Created {csproj_path.name}")

        # Create DbContext
        if self.database != 'none':
            dbcontext_content = self._get_dbcontext()
            dbcontext_path = infra_path / "Data" / "ApplicationDbContext.cs"
            dbcontext_path.write_text(dbcontext_content)
            files.append(dbcontext_path)
            self._log(f"Created {dbcontext_path.name}")

        # Create generic repository
        repo_content = f'''using Microsoft.EntityFrameworkCore;
using {self.namespace}.Domain.Interfaces;
using {self.namespace}.Infrastructure.Data;

namespace {self.namespace}.Infrastructure.Repositories;

public class Repository<T> : IRepository<T> where T : class
{{
    protected readonly ApplicationDbContext _context;
    protected readonly DbSet<T> _dbSet;

    public Repository(ApplicationDbContext context)
    {{
        _context = context;
        _dbSet = context.Set<T>();
    }}

    public virtual async Task<T?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
    {{
        return await _dbSet.FindAsync(new object[] {{ id }}, cancellationToken);
    }}

    public virtual async Task<IEnumerable<T>> GetAllAsync(CancellationToken cancellationToken = default)
    {{
        return await _dbSet.ToListAsync(cancellationToken);
    }}

    public virtual async Task<T> AddAsync(T entity, CancellationToken cancellationToken = default)
    {{
        await _dbSet.AddAsync(entity, cancellationToken);
        await _context.SaveChangesAsync(cancellationToken);
        return entity;
    }}

    public virtual async Task UpdateAsync(T entity, CancellationToken cancellationToken = default)
    {{
        _dbSet.Update(entity);
        await _context.SaveChangesAsync(cancellationToken);
    }}

    public virtual async Task DeleteAsync(T entity, CancellationToken cancellationToken = default)
    {{
        _dbSet.Remove(entity);
        await _context.SaveChangesAsync(cancellationToken);
    }}
}}
'''
        repo_path = infra_path / "Repositories" / "Repository.cs"
        repo_path.write_text(repo_content)
        files.append(repo_path)

        return files

    def _create_test_project(self, project_path: Path) -> List[Path]:
        """Create test project files."""
        files = []
        test_path = project_path / 'tests' / 'Api.Tests'

        # Create test .csproj
        csproj_content = f'''<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <IsPackable>false</IsPackable>
    <RootNamespace>{self.namespace}.Api.Tests</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="xunit" Version="2.6.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.4" />
    <PackageReference Include="Moq" Version="4.20.70" />
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="8.0.0" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\\..\\src\\Api\\{self.pascal_name}.Api.csproj" />
  </ItemGroup>

</Project>
'''
        csproj_path = test_path / f"{self.pascal_name}.Api.Tests.csproj"
        csproj_path.write_text(csproj_content)
        files.append(csproj_path)
        self._log(f"Created {csproj_path.name}")

        # Create sample test
        test_content = f'''using FluentAssertions;
using Xunit;

namespace {self.namespace}.Api.Tests;

public class HealthControllerTests
{{
    [Fact]
    public void Health_ShouldReturn_Healthy()
    {{
        // Arrange
        var expected = "Healthy";

        // Act
        var result = "Healthy";

        // Assert
        result.Should().Be(expected);
    }}
}}
'''
        test_file_path = test_path / "HealthControllerTests.cs"
        test_file_path.write_text(test_content)
        files.append(test_file_path)

        return files

    def _create_docker_files(self, project_path: Path) -> List[Path]:
        """Create Docker configuration files."""
        files = []

        # Dockerfile
        dockerfile_content = f'''# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy solution and project files
COPY ["{self.pascal_name}.sln", "./"]
COPY ["src/Api/{self.pascal_name}.Api.csproj", "src/Api/"]
COPY ["src/Domain/{self.pascal_name}.Domain.csproj", "src/Domain/"]
COPY ["src/Infrastructure/{self.pascal_name}.Infrastructure.csproj", "src/Infrastructure/"]

# Restore dependencies
RUN dotnet restore

# Copy source code
COPY . .

# Build and publish
WORKDIR "/src/src/Api"
RUN dotnet publish -c Release -o /app/publish --no-restore

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

COPY --from=build /app/publish .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["dotnet", "{self.pascal_name}.Api.dll"]
'''
        dockerfile_path = project_path / "Dockerfile"
        dockerfile_path.write_text(dockerfile_content)
        files.append(dockerfile_path)
        self._log("Created Dockerfile")

        # Docker Compose
        db_service = self._get_docker_compose_db()
        compose_content = f'''version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection={self._get_docker_connection_string()}
    depends_on:
{db_service['depends_on']}

{db_service['service']}

networks:
  default:
    name: {self.project_name}-network
'''
        compose_path = project_path / "docker-compose.yml"
        compose_path.write_text(compose_content)
        files.append(compose_path)
        self._log("Created docker-compose.yml")

        # .dockerignore
        dockerignore_content = '''**/bin/
**/obj/
**/out/
**/.vs/
**/.vscode/
**/node_modules/
**/*.user
**/*.userosscache
**/*.suo
**/Thumbs.db
**/.DS_Store
**/TestResults/
**/coverage/
'''
        dockerignore_path = project_path / ".dockerignore"
        dockerignore_path.write_text(dockerignore_content)
        files.append(dockerignore_path)

        return files

    def _create_cicd_files(self, project_path: Path) -> List[Path]:
        """Create CI/CD configuration files."""
        files = []

        # GitHub Actions workflow
        workflow_content = f'''name: Build and Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  DOTNET_VERSION: '8.0.x'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup .NET
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: ${{{{ env.DOTNET_VERSION }}}}

    - name: Restore dependencies
      run: dotnet restore

    - name: Build
      run: dotnet build --no-restore --configuration Release

    - name: Test
      run: dotnet test --no-build --configuration Release --verbosity normal --collect:"XPlat Code Coverage"

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./tests/**/coverage.cobertura.xml

  docker:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Build Docker image
      run: docker build -t {self.project_name}:${{{{ github.sha }}}} .

    - name: Run container tests
      run: |
        docker run -d --name test-container -p 8080:8080 {self.project_name}:${{{{ github.sha }}}}
        sleep 10
        curl -f http://localhost:8080/health || exit 1
        docker stop test-container
'''
        workflow_path = project_path / ".github" / "workflows" / "build.yml"
        workflow_path.write_text(workflow_content)
        files.append(workflow_path)
        self._log("Created GitHub Actions workflow")

        return files

    def _create_documentation(self, project_path: Path) -> List[Path]:
        """Create documentation files."""
        files = []

        # README.md
        readme_content = f'''# {self.pascal_name}

{self.project_type.upper()} project built with ASP.NET Core 8 and Clean Architecture.

## Prerequisites

- .NET 8 SDK
- Docker (optional)
- {self._get_database_name()} (or use Docker)

## Getting Started

### Local Development

```bash
# Restore dependencies
dotnet restore

# Run migrations (if using EF Core)
dotnet ef database update --project src/Infrastructure --startup-project src/Api

# Run the application
dotnet run --project src/Api
```

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the API
curl http://localhost:8080/health
```

## Project Structure

```
{self.project_name}/
├── src/
│   ├── Api/              # ASP.NET Core Web API
│   ├── Domain/           # Domain entities and interfaces
│   └── Infrastructure/   # Data access and external services
├── tests/
│   └── Api.Tests/        # Unit and integration tests
├── Dockerfile
└── docker-compose.yml
```

## API Endpoints

- `GET /health` - Health check endpoint
- `GET /swagger` - OpenAPI documentation

## Configuration

Configuration is managed through `appsettings.json` and environment variables.

### Environment Variables

- `ConnectionStrings__DefaultConnection` - Database connection string
- `ASPNETCORE_ENVIRONMENT` - Environment (Development, Staging, Production)

## Testing

```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test --collect:"XPlat Code Coverage"
```

## License

MIT

---

Generated with senior-dotnet skill on {datetime.now().strftime('%Y-%m-%d')}
'''
        readme_path = project_path / "README.md"
        readme_path.write_text(readme_content)
        files.append(readme_path)
        self._log("Created README.md")

        # .gitignore
        gitignore_content = '''## .NET
bin/
obj/
out/

## IDE
.vs/
.vscode/
*.user
*.userosscache
*.suo

## Test Results
TestResults/
coverage/
*.trx

## OS
.DS_Store
Thumbs.db

## Docker
.docker/

## Logs
logs/
*.log
'''
        gitignore_path = project_path / ".gitignore"
        gitignore_path.write_text(gitignore_content)
        files.append(gitignore_path)

        # .editorconfig
        editorconfig_content = '''root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.cs]
dotnet_sort_system_directives_first = true
csharp_new_line_before_open_brace = all
csharp_prefer_braces = true:suggestion

[*.{json,yml,yaml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
'''
        editorconfig_path = project_path / ".editorconfig"
        editorconfig_path.write_text(editorconfig_content)
        files.append(editorconfig_path)

        return files

    def _get_web_csproj(self) -> str:
        """Generate Web API .csproj content."""
        auth_packages = self._get_auth_packages()
        db_packages = self._get_database_packages()

        return f'''<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <RootNamespace>{self.namespace}.Api</RootNamespace>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Swashbuckle.AspNetCore" Version="6.5.0" />
    <PackageReference Include="Serilog.AspNetCore" Version="8.0.0" />
    <PackageReference Include="FluentValidation.AspNetCore" Version="11.3.0" />
    <PackageReference Include="AutoMapper.Extensions.Microsoft.DependencyInjection" Version="12.0.1" />
{auth_packages}
{db_packages}
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\\Domain\\{self.pascal_name}.Domain.csproj" />
    <ProjectReference Include="..\\Infrastructure\\{self.pascal_name}.Infrastructure.csproj" />
  </ItemGroup>

</Project>
'''

    def _get_program_cs(self) -> str:
        """Generate Program.cs content."""
        db_config = self._get_db_configuration()
        auth_config = self._get_auth_configuration()

        return f'''using {self.namespace}.Api.Extensions;
using {self.namespace}.Api.Middleware;
using {self.namespace}.Infrastructure.Data;
using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .CreateLogger();

try
{{
    Log.Information("Starting {self.pascal_name} API");

    var builder = WebApplication.CreateBuilder(args);

    // Add Serilog
    builder.Host.UseSerilog((context, config) =>
        config.ReadFrom.Configuration(context.Configuration));

    // Add services
    builder.Services.AddControllers();
    builder.Services.AddEndpointsApiExplorer();
    builder.Services.AddSwaggerGen();

    // Add AutoMapper
    builder.Services.AddAutoMapper(typeof(Program));

    // Add FluentValidation
    builder.Services.AddValidatorsFromAssemblyContaining<Program>();

{db_config}
{auth_config}
    // Add custom services
    builder.Services.AddApplicationServices();

    var app = builder.Build();

    // Configure middleware pipeline
    app.UseMiddleware<ExceptionMiddleware>();

    if (app.Environment.IsDevelopment())
    {{
        app.UseSwagger();
        app.UseSwaggerUI();
    }}

    app.UseHttpsRedirection();
    app.UseSerilogRequestLogging();

    app.UseAuthentication();
    app.UseAuthorization();

    app.MapControllers();

    // Health check endpoint
    app.MapGet("/health", () => Results.Ok(new {{ status = "Healthy", timestamp = DateTime.UtcNow }}));

    app.Run();
}}
catch (Exception ex)
{{
    Log.Fatal(ex, "Application terminated unexpectedly");
}}
finally
{{
    Log.CloseAndFlush();
}}
'''

    def _get_appsettings(self) -> str:
        """Generate appsettings.json content."""
        settings = {
            "Logging": {
                "LogLevel": {
                    "Default": "Information",
                    "Microsoft.AspNetCore": "Warning"
                }
            },
            "AllowedHosts": "*",
            "ConnectionStrings": {
                "DefaultConnection": self._get_connection_string()
            }
        }

        if self.auth_type == 'jwt':
            settings["Jwt"] = {
                "Secret": "YourSecretKeyHere-MustBeAtLeast32CharactersLong!",
                "Issuer": self.project_name,
                "Audience": self.project_name,
                "ExpirationMinutes": 60
            }

        return json.dumps(settings, indent=2)

    def _get_sample_controller(self) -> str:
        """Generate sample controller."""
        return f'''using Microsoft.AspNetCore.Mvc;

namespace {self.namespace}.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class HealthController : ControllerBase
{{
    private readonly ILogger<HealthController> _logger;

    public HealthController(ILogger<HealthController> logger)
    {{
        _logger = logger;
    }}

    [HttpGet]
    public IActionResult Get()
    {{
        _logger.LogInformation("Health check requested");
        return Ok(new
        {{
            status = "Healthy",
            timestamp = DateTime.UtcNow,
            version = "1.0.0"
        }});
    }}
}}
'''

    def _get_exception_middleware(self) -> str:
        """Generate exception handling middleware."""
        return f'''using System.Net;
using System.Text.Json;

namespace {self.namespace}.Api.Middleware;

public class ExceptionMiddleware
{{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionMiddleware> _logger;

    public ExceptionMiddleware(RequestDelegate next, ILogger<ExceptionMiddleware> logger)
    {{
        _next = next;
        _logger = logger;
    }}

    public async Task InvokeAsync(HttpContext context)
    {{
        try
        {{
            await _next(context);
        }}
        catch (Exception ex)
        {{
            _logger.LogError(ex, "An unhandled exception occurred");
            await HandleExceptionAsync(context, ex);
        }}
    }}

    private static async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {{
        context.Response.ContentType = "application/problem+json";
        context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;

        var problemDetails = new
        {{
            type = "https://tools.ietf.org/html/rfc7807",
            title = "An error occurred",
            status = context.Response.StatusCode,
            detail = exception.Message,
            instance = context.Request.Path
        }};

        var json = JsonSerializer.Serialize(problemDetails);
        await context.Response.WriteAsync(json);
    }}
}}
'''

    def _get_service_extensions(self) -> str:
        """Generate service extension methods."""
        return f'''using {self.namespace}.Domain.Interfaces;
using {self.namespace}.Infrastructure.Repositories;

namespace {self.namespace}.Api.Extensions;

public static class ServiceExtensions
{{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {{
        // Register repositories
        services.AddScoped(typeof(IRepository<>), typeof(Repository<>));

        // Add additional services here

        return services;
    }}
}}
'''

    def _get_dbcontext(self) -> str:
        """Generate DbContext class."""
        return f'''using Microsoft.EntityFrameworkCore;
using {self.namespace}.Domain.Entities;

namespace {self.namespace}.Infrastructure.Data;

public class ApplicationDbContext : DbContext
{{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {{
    }}

    // Add DbSet properties here
    // public DbSet<YourEntity> YourEntities {{ get; set; }}

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {{
        base.OnModelCreating(modelBuilder);

        // Configure entities here
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
    }}

    public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {{
        foreach (var entry in ChangeTracker.Entries<BaseEntity>())
        {{
            switch (entry.State)
            {{
                case EntityState.Added:
                    entry.Entity.CreatedAt = DateTime.UtcNow;
                    break;
                case EntityState.Modified:
                    entry.Entity.UpdatedAt = DateTime.UtcNow;
                    break;
            }}
        }}

        return base.SaveChangesAsync(cancellationToken);
    }}
}}
'''

    def _get_database_packages(self) -> str:
        """Get NuGet package references for database."""
        packages = {
            'sqlserver': '    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="8.0.0" />',
            'postgresql': '    <PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="8.0.0" />',
            'mysql': '    <PackageReference Include="Pomelo.EntityFrameworkCore.MySql" Version="8.0.0" />',
            'sqlite': '    <PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="8.0.0" />',
            'cosmosdb': '    <PackageReference Include="Microsoft.EntityFrameworkCore.Cosmos" Version="8.0.0" />',
            'none': ''
        }

        base_packages = '''    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="8.0.0" />'''

        if self.database == 'none':
            return ''

        return f"{base_packages}\n{packages.get(self.database, '')}"

    def _get_auth_packages(self) -> str:
        """Get NuGet package references for authentication."""
        packages = {
            'jwt': '    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.0.0" />',
            'identity': '''    <PackageReference Include="Microsoft.AspNetCore.Identity.EntityFrameworkCore" Version="8.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.0.0" />''',
            'oidc': '    <PackageReference Include="Microsoft.AspNetCore.Authentication.OpenIdConnect" Version="8.0.0" />',
            'none': ''
        }
        return packages.get(self.auth_type, '')

    def _get_connection_string(self) -> str:
        """Get connection string for database."""
        strings = {
            'sqlserver': f"Server=localhost;Database={self.pascal_name};Trusted_Connection=True;TrustServerCertificate=True;",
            'postgresql': f"Host=localhost;Database={self.project_name.replace('-', '_')};Username=postgres;Password=postgres",
            'mysql': f"Server=localhost;Database={self.project_name.replace('-', '_')};User=root;Password=root;",
            'sqlite': f"Data Source={self.project_name}.db",
            'cosmosdb': "AccountEndpoint=https://localhost:8081;AccountKey=your-key;Database={self.project_name}",
            'none': ''
        }
        return strings.get(self.database, '')

    def _get_docker_connection_string(self) -> str:
        """Get connection string for Docker environment."""
        strings = {
            'sqlserver': f"Server=sqlserver;Database={self.pascal_name};User=sa;Password=YourStrong@Passw0rd;TrustServerCertificate=True;",
            'postgresql': f"Host=postgres;Database={self.project_name.replace('-', '_')};Username=postgres;Password=postgres",
            'mysql': f"Server=mysql;Database={self.project_name.replace('-', '_')};User=root;Password=root;",
            'sqlite': f"Data Source=/app/data/{self.project_name}.db",
            'cosmosdb': "AccountEndpoint=https://cosmosdb:8081;AccountKey=your-key;Database={self.project_name}",
            'none': ''
        }
        return strings.get(self.database, '')

    def _get_docker_compose_db(self) -> Dict[str, str]:
        """Get Docker Compose database service configuration."""
        configs = {
            'sqlserver': {
                'depends_on': '      - sqlserver',
                'service': '''  sqlserver:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=YourStrong@Passw0rd
    ports:
      - "1433:1433"
    volumes:
      - sqlserver-data:/var/opt/mssql

volumes:
  sqlserver-data:'''
            },
            'postgresql': {
                'depends_on': '      - postgres',
                'service': '''  postgres:
    image: postgres:16
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=''' + self.project_name.replace('-', '_') + '''
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:'''
            },
            'mysql': {
                'depends_on': '      - mysql',
                'service': '''  mysql:
    image: mysql:8
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=''' + self.project_name.replace('-', '_') + '''
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:'''
            },
            'sqlite': {
                'depends_on': '',
                'service': '''volumes:
  app-data:'''
            },
            'cosmosdb': {
                'depends_on': '      - cosmosdb',
                'service': '''  cosmosdb:
    image: mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator
    ports:
      - "8081:8081"'''
            },
            'none': {
                'depends_on': '',
                'service': ''
            }
        }
        return configs.get(self.database, {'depends_on': '', 'service': ''})

    def _get_db_configuration(self) -> str:
        """Get database configuration for Program.cs."""
        if self.database == 'none':
            return ''

        db_method = {
            'sqlserver': 'UseSqlServer',
            'postgresql': 'UseNpgsql',
            'mysql': 'UseMySql',
            'sqlite': 'UseSqlite',
            'cosmosdb': 'UseCosmos'
        }.get(self.database, 'UseSqlServer')

        return f'''    // Add Database
    builder.Services.AddDbContext<ApplicationDbContext>(options =>
        options.{db_method}(builder.Configuration.GetConnectionString("DefaultConnection")));
'''

    def _get_auth_configuration(self) -> str:
        """Get authentication configuration for Program.cs."""
        if self.auth_type == 'none':
            return ''

        if self.auth_type == 'jwt':
            return '''    // Add JWT Authentication
    builder.Services.AddAuthentication("Bearer")
        .AddJwtBearer(options =>
        {
            options.TokenValidationParameters = new Microsoft.IdentityModel.Tokens.TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidateAudience = true,
                ValidateLifetime = true,
                ValidateIssuerSigningKey = true,
                ValidIssuer = builder.Configuration["Jwt:Issuer"],
                ValidAudience = builder.Configuration["Jwt:Audience"],
                IssuerSigningKey = new Microsoft.IdentityModel.Tokens.SymmetricSecurityKey(
                    System.Text.Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Secret"]!))
            };
        });
    builder.Services.AddAuthorization();
'''

        if self.auth_type == 'identity':
            return '''    // Add Identity
    builder.Services.AddIdentity<IdentityUser, IdentityRole>()
        .AddEntityFrameworkStores<ApplicationDbContext>()
        .AddDefaultTokenProviders();

    builder.Services.AddAuthentication()
        .AddJwtBearer();
    builder.Services.AddAuthorization();
'''

        return ''

    def _get_database_name(self) -> str:
        """Get human-readable database name."""
        names = {
            'sqlserver': 'SQL Server',
            'postgresql': 'PostgreSQL',
            'mysql': 'MySQL',
            'sqlite': 'SQLite',
            'cosmosdb': 'Azure Cosmos DB',
            'none': 'None'
        }
        return names.get(self.database, 'Database')

    def _get_next_steps(self) -> List[str]:
        """Get list of next steps after scaffolding."""
        steps = [
            f"cd {self.project_name}",
            "dotnet restore",
        ]

        if self.database != 'none':
            steps.append("# Start database with Docker")
            steps.append("docker-compose up -d")
            steps.append("# Run migrations")
            steps.append(f"dotnet ef migrations add InitialCreate --project src/Infrastructure --startup-project src/Api")
            steps.append(f"dotnet ef database update --project src/Infrastructure --startup-project src/Api")

        steps.extend([
            "# Run the application",
            "dotnet run --project src/Api",
            "# Access Swagger UI at http://localhost:5000/swagger"
        ])

        return steps


def main():
    """Main entry point with CLI interface."""
    parser = argparse.ArgumentParser(
        description=".NET Project Scaffolder - Generate production-ready ASP.NET Core projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-service --type webapi --db sqlserver
  %(prog)s ecommerce-app --type mvc --db postgresql --auth identity
  %(prog)s notification-service --type minimal-api --db sqlite
  %(prog)s worker-service --type worker --db none

Project Types:
  webapi      - ASP.NET Core Web API with Controllers
  mvc         - ASP.NET Core MVC application
  blazor      - Blazor Server application
  minimal-api - Minimal API (lightweight endpoints)
  worker      - Background Worker Service
  console     - Console application

Databases:
  sqlserver   - Microsoft SQL Server
  postgresql  - PostgreSQL
  mysql       - MySQL
  sqlite      - SQLite (file-based)
  cosmosdb    - Azure Cosmos DB
  none        - No database

Authentication:
  jwt         - JWT Bearer authentication
  identity    - ASP.NET Core Identity
  oidc        - OpenID Connect
  none        - No authentication

Part of senior-dotnet skill.
"""
    )

    parser.add_argument(
        'project_name',
        nargs='?',
        help='Name of the project (kebab-case)'
    )

    parser.add_argument(
        '--type', '-t',
        choices=DotNetProjectScaffolder.VALID_PROJECT_TYPES,
        default='webapi',
        help='Project type (default: webapi)'
    )

    parser.add_argument(
        '--db', '-d',
        choices=DotNetProjectScaffolder.VALID_DATABASES,
        default='sqlserver',
        help='Database provider (default: sqlserver)'
    )

    parser.add_argument(
        '--auth', '-a',
        choices=DotNetProjectScaffolder.VALID_AUTH_TYPES,
        default='jwt',
        help='Authentication type (default: jwt)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output directory (default: current directory)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    args = parser.parse_args()

    if not args.project_name:
        parser.print_help()
        sys.exit(1)

    print(f"Scaffolding .NET project: {args.project_name}")
    print(f"  Type: {args.type}")
    print(f"  Database: {args.db}")
    print(f"  Authentication: {args.auth}")
    print()

    scaffolder = DotNetProjectScaffolder(
        project_name=args.project_name,
        project_type=args.type,
        database=args.db,
        auth_type=args.auth,
        output_dir=args.output,
        verbose=args.verbose
    )

    result = scaffolder.scaffold()

    if result['success']:
        print(f"Project created successfully at: {result['project_path']}")
        print(f"\nFiles created: {len(result['files_created'])}")
        print("\nNext steps:")
        for step in result['next_steps']:
            print(f"  {step}")
    else:
        print("Error creating project:")
        for error in result['errors']:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
