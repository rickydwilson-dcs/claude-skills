# .NET Best Practices

Comprehensive guide to .NET development patterns, Clean Architecture, dependency injection, configuration management, and testing strategies.

## Solution Structure

### Clean Architecture Layout

```
MySolution/
├── src/
│   ├── Api/                    # ASP.NET Core Web API
│   │   ├── Controllers/        # HTTP endpoints
│   │   ├── Middleware/         # Custom middleware
│   │   ├── Extensions/         # Service extensions
│   │   └── Program.cs          # Entry point
│   ├── Domain/                 # Core business logic
│   │   ├── Entities/           # Domain entities
│   │   ├── Interfaces/         # Abstractions
│   │   ├── ValueObjects/       # Immutable value types
│   │   └── Events/             # Domain events
│   ├── Application/            # Use cases (optional)
│   │   ├── Commands/           # CQRS commands
│   │   ├── Queries/            # CQRS queries
│   │   └── Behaviors/          # MediatR behaviors
│   └── Infrastructure/         # External concerns
│       ├── Data/               # EF Core DbContext
│       ├── Repositories/       # Data access
│       └── Services/           # External services
├── tests/
│   ├── Api.Tests/              # Integration tests
│   ├── Domain.Tests/           # Unit tests
│   └── Infrastructure.Tests/   # Data access tests
├── MySolution.sln
└── Directory.Build.props       # Shared properties
```

### Dependency Rule

**Dependencies flow inward only:**
- Api → Application → Domain
- Infrastructure → Domain
- Domain has no dependencies

### Directory.Build.props

```xml
<Project>
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
</Project>
```

## Dependency Injection

### Service Registration Patterns

```csharp
// Register by interface
services.AddScoped<IRepository<T>, Repository<T>>();

// Register concrete type
services.AddSingleton<MyService>();

// Register with factory
services.AddScoped<IDbConnection>(sp =>
    new SqlConnection(configuration.GetConnectionString("Default")));

// Register open generics
services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
```

### Service Lifetimes

| Lifetime | Use Case |
|----------|----------|
| Singleton | Configuration, caches, thread-safe services |
| Scoped | DbContext, HTTP-bound services |
| Transient | Lightweight, stateless services |

### Registration Extensions

```csharp
public static class ServiceExtensions
{
    public static IServiceCollection AddApplicationServices(
        this IServiceCollection services)
    {
        services.AddScoped<IUserService, UserService>();
        services.AddScoped<IOrderService, OrderService>();
        return services;
    }
}

// Usage in Program.cs
builder.Services.AddApplicationServices();
```

## Configuration Management

### Options Pattern

```csharp
// Define options class
public class SmtpOptions
{
    public const string SectionName = "Smtp";

    public string Host { get; set; } = string.Empty;
    public int Port { get; set; } = 587;
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}

// Configure in Program.cs
builder.Services.Configure<SmtpOptions>(
    builder.Configuration.GetSection(SmtpOptions.SectionName));

// Inject in services
public class EmailService
{
    private readonly SmtpOptions _options;

    public EmailService(IOptions<SmtpOptions> options)
    {
        _options = options.Value;
    }
}
```

### appsettings.json Structure

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyDb;..."
  },
  "Smtp": {
    "Host": "smtp.example.com",
    "Port": 587
  },
  "Features": {
    "EnableNewCheckout": false
  }
}
```

### Environment Variables

```bash
# Override connection string
ConnectionStrings__DefaultConnection="Server=prod;..."

# Override nested settings
Smtp__Host="smtp.production.com"
```

## Logging

### Serilog Configuration

```csharp
// Program.cs
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .WriteTo.Console(new JsonFormatter())
    .WriteTo.Seq("http://localhost:5341")
    .CreateLogger();

builder.Host.UseSerilog();
```

### Structured Logging

```csharp
// Good - structured logging
_logger.LogInformation("Order {OrderId} created for user {UserId}",
    order.Id, user.Id);

// Bad - string interpolation
_logger.LogInformation($"Order {order.Id} created for user {user.Id}");
```

### Log Levels

| Level | Use Case |
|-------|----------|
| Trace | Detailed debugging information |
| Debug | Development-time information |
| Information | General operational entries |
| Warning | Abnormal or unexpected events |
| Error | Errors and exceptions |
| Critical | System failures |

## Testing Strategies

### Unit Tests (xUnit)

```csharp
public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _mockRepo;
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _mockRepo = new Mock<IOrderRepository>();
        _sut = new OrderService(_mockRepo.Object);
    }

    [Fact]
    public async Task CreateOrder_ValidOrder_ReturnsOrderId()
    {
        // Arrange
        var order = new Order { /* ... */ };
        _mockRepo.Setup(r => r.AddAsync(It.IsAny<Order>(), default))
            .ReturnsAsync(order);

        // Act
        var result = await _sut.CreateOrderAsync(order);

        // Assert
        result.Should().NotBeNull();
        result.Id.Should().BeGreaterThan(0);
    }
}
```

### Integration Tests

```csharp
public class OrdersControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public OrdersControllerTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Replace real database with in-memory
                services.AddDbContext<AppDbContext>(options =>
                    options.UseInMemoryDatabase("TestDb"));
            });
        }).CreateClient();
    }

    [Fact]
    public async Task GetOrders_ReturnsOkResult()
    {
        // Act
        var response = await _client.GetAsync("/api/orders");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }
}
```

### Test Naming Convention

```csharp
// Pattern: MethodName_StateUnderTest_ExpectedBehavior
[Fact]
public void GetById_NonExistentId_ReturnsNull()
{
    // ...
}

[Fact]
public async Task CreateOrder_EmptyCart_ThrowsValidationException()
{
    // ...
}
```

## Error Handling

### Global Exception Handler

```csharp
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;

    public GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    {
        _logger = logger;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext context,
        Exception exception,
        CancellationToken cancellationToken)
    {
        _logger.LogError(exception, "Unhandled exception occurred");

        var problemDetails = exception switch
        {
            ValidationException ex => new ValidationProblemDetails(ex.Errors),
            NotFoundException ex => new ProblemDetails
            {
                Status = StatusCodes.Status404NotFound,
                Title = "Not Found",
                Detail = ex.Message
            },
            _ => new ProblemDetails
            {
                Status = StatusCodes.Status500InternalServerError,
                Title = "Server Error"
            }
        };

        context.Response.StatusCode = problemDetails.Status ?? 500;
        await context.Response.WriteAsJsonAsync(problemDetails, cancellationToken);

        return true;
    }
}
```

### Result Pattern

```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }

    public static Result<T> Success(T value) =>
        new() { IsSuccess = true, Value = value };

    public static Result<T> Failure(string error) =>
        new() { IsSuccess = false, Error = error };
}
```

## Code Quality

### Required NuGet Packages

```xml
<ItemGroup>
  <PackageReference Include="StyleCop.Analyzers" Version="1.2.0-beta.556">
    <PrivateAssets>all</PrivateAssets>
  </PackageReference>
  <PackageReference Include="Microsoft.CodeAnalysis.NetAnalyzers" Version="8.0.0">
    <PrivateAssets>all</PrivateAssets>
  </PackageReference>
</ItemGroup>
```

### .editorconfig Rules

```ini
[*.cs]
# Naming
dotnet_naming_rule.private_fields_underscore.symbols = private_fields
dotnet_naming_rule.private_fields_underscore.style = prefix_underscore
dotnet_naming_rule.private_fields_underscore.severity = suggestion

dotnet_naming_symbols.private_fields.applicable_kinds = field
dotnet_naming_symbols.private_fields.applicable_accessibilities = private

dotnet_naming_style.prefix_underscore.required_prefix = _
dotnet_naming_style.prefix_underscore.capitalization = camel_case

# Code style
csharp_prefer_braces = true:suggestion
csharp_style_var_for_built_in_types = true:suggestion
```

## Health Checks

```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>()
    .AddUrlGroup(new Uri("https://external-api.com/health"), "External API")
    .AddRedis(configuration.GetConnectionString("Redis")!);

app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});
```

---

**Last Updated:** 2025-12-16
**Applies To:** .NET 8, ASP.NET Core 8
