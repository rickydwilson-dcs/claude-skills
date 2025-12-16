# ASP.NET Core Patterns

Comprehensive guide to ASP.NET Core middleware, Minimal APIs vs Controllers, request handling, filters, and background services.

## Middleware Pipeline

### Request Pipeline Order

```csharp
var app = builder.Build();

// 1. Exception handling (outermost)
app.UseExceptionHandler("/error");

// 2. HTTPS redirection
app.UseHttpsRedirection();

// 3. Static files (short-circuit for static content)
app.UseStaticFiles();

// 4. Routing
app.UseRouting();

// 5. CORS (after routing, before auth)
app.UseCors();

// 6. Authentication
app.UseAuthentication();

// 7. Authorization
app.UseAuthorization();

// 8. Custom middleware
app.UseMiddleware<RequestLoggingMiddleware>();

// 9. Endpoints
app.MapControllers();
```

### Custom Middleware

```csharp
public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(
        RequestDelegate next,
        ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();

        try
        {
            await _next(context);
        }
        finally
        {
            stopwatch.Stop();
            _logger.LogInformation(
                "Request {Method} {Path} completed in {ElapsedMs}ms with status {Status}",
                context.Request.Method,
                context.Request.Path,
                stopwatch.ElapsedMilliseconds,
                context.Response.StatusCode);
        }
    }
}
```

### Extension Method Pattern

```csharp
public static class MiddlewareExtensions
{
    public static IApplicationBuilder UseRequestLogging(
        this IApplicationBuilder builder)
    {
        return builder.UseMiddleware<RequestLoggingMiddleware>();
    }
}

// Usage
app.UseRequestLogging();
```

## Minimal APIs vs Controllers

### When to Use Minimal APIs

- Simple CRUD operations
- Microservices with few endpoints
- Prototyping
- When reducing boilerplate is priority

### When to Use Controllers

- Complex APIs with many endpoints
- Need for filters and attributes
- APIs requiring model binding customization
- Large teams preferring MVC patterns

### Minimal API Example

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/products", async (IProductService service) =>
    Results.Ok(await service.GetAllAsync()));

app.MapGet("/products/{id}", async (int id, IProductService service) =>
    await service.GetByIdAsync(id) is Product product
        ? Results.Ok(product)
        : Results.NotFound());

app.MapPost("/products", async (CreateProductRequest request, IProductService service) =>
{
    var product = await service.CreateAsync(request);
    return Results.Created($"/products/{product.Id}", product);
});

app.Run();
```

### Minimal API Groups

```csharp
var products = app.MapGroup("/products")
    .WithTags("Products")
    .RequireAuthorization();

products.MapGet("/", GetAllProducts);
products.MapGet("/{id}", GetProductById);
products.MapPost("/", CreateProduct);
products.MapPut("/{id}", UpdateProduct);
products.MapDelete("/{id}", DeleteProduct);
```

### Controller Example

```csharp
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _service;

    public ProductsController(IProductService service)
    {
        _service = service;
    }

    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<ProductDto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<ProductDto>>> GetAll()
    {
        return Ok(await _service.GetAllAsync());
    }

    [HttpGet("{id}")]
    [ProducesResponseType(typeof(ProductDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        var product = await _service.GetByIdAsync(id);
        if (product == null) return NotFound();
        return Ok(product);
    }
}
```

## Request/Response Handling

### Model Binding

```csharp
[HttpGet]
public async Task<IActionResult> Search(
    [FromQuery] string query,
    [FromQuery] int page = 1,
    [FromQuery] int pageSize = 10)
{
    // ...
}

[HttpPost]
public async Task<IActionResult> Create(
    [FromBody] CreateProductRequest request)
{
    // ...
}

[HttpPut("{id}")]
public async Task<IActionResult> Update(
    [FromRoute] int id,
    [FromBody] UpdateProductRequest request)
{
    // ...
}
```

### Custom Model Binder

```csharp
public class DateRangeModelBinder : IModelBinder
{
    public Task BindModelAsync(ModelBindingContext bindingContext)
    {
        var startValue = bindingContext.ValueProvider.GetValue("startDate");
        var endValue = bindingContext.ValueProvider.GetValue("endDate");

        if (DateTime.TryParse(startValue.FirstValue, out var start) &&
            DateTime.TryParse(endValue.FirstValue, out var end))
        {
            bindingContext.Result = ModelBindingResult.Success(
                new DateRange(start, end));
        }

        return Task.CompletedTask;
    }
}
```

### Content Negotiation

```csharp
builder.Services.AddControllers(options =>
{
    options.RespectBrowserAcceptHeader = true;
    options.ReturnHttpNotAcceptable = true;
})
.AddXmlSerializerFormatters()
.AddJsonOptions(options =>
{
    options.JsonSerializerOptions.PropertyNamingPolicy =
        JsonNamingPolicy.CamelCase;
    options.JsonSerializerOptions.DefaultIgnoreCondition =
        JsonIgnoreCondition.WhenWritingNull;
});
```

## Filters

### Action Filters

```csharp
public class ValidationFilter : IAsyncActionFilter
{
    public async Task OnActionExecutionAsync(
        ActionExecutingContext context,
        ActionExecutionDelegate next)
    {
        if (!context.ModelState.IsValid)
        {
            context.Result = new BadRequestObjectResult(
                new ValidationProblemDetails(context.ModelState));
            return;
        }

        await next();
    }
}
```

### Exception Filters

```csharp
public class ApiExceptionFilter : IExceptionFilter
{
    private readonly ILogger<ApiExceptionFilter> _logger;

    public ApiExceptionFilter(ILogger<ApiExceptionFilter> logger)
    {
        _logger = logger;
    }

    public void OnException(ExceptionContext context)
    {
        _logger.LogError(context.Exception, "Unhandled exception");

        var problemDetails = new ProblemDetails
        {
            Status = StatusCodes.Status500InternalServerError,
            Title = "Server Error",
            Instance = context.HttpContext.Request.Path
        };

        context.Result = new ObjectResult(problemDetails)
        {
            StatusCode = problemDetails.Status
        };
    }
}
```

### Filter Registration

```csharp
// Global registration
builder.Services.AddControllers(options =>
{
    options.Filters.Add<ValidationFilter>();
    options.Filters.Add<ApiExceptionFilter>();
});

// Attribute registration
[ServiceFilter(typeof(ValidationFilter))]
public class ProductsController : ControllerBase
{
    // ...
}
```

## Background Services

### IHostedService

```csharp
public class HealthCheckBackgroundService : BackgroundService
{
    private readonly ILogger<HealthCheckBackgroundService> _logger;
    private readonly IServiceScopeFactory _scopeFactory;

    public HealthCheckBackgroundService(
        ILogger<HealthCheckBackgroundService> logger,
        IServiceScopeFactory scopeFactory)
    {
        _logger = logger;
        _scopeFactory = scopeFactory;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            _logger.LogInformation("Running health check at: {time}", DateTimeOffset.Now);

            using var scope = _scopeFactory.CreateScope();
            var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();

            // Perform health check
            await dbContext.Database.CanConnectAsync(stoppingToken);

            await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
        }
    }
}

// Registration
builder.Services.AddHostedService<HealthCheckBackgroundService>();
```

### Queue Processing

```csharp
public class QueuedHostedService : BackgroundService
{
    private readonly IBackgroundTaskQueue _taskQueue;
    private readonly ILogger<QueuedHostedService> _logger;

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var workItem = await _taskQueue.DequeueAsync(stoppingToken);

            try
            {
                await workItem(stoppingToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing queued work item");
            }
        }
    }
}
```

## CORS Configuration

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowSpecificOrigin", policy =>
    {
        policy.WithOrigins("https://app.example.com")
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });

    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

app.UseCors("AllowSpecificOrigin");
```

## Response Caching

```csharp
builder.Services.AddResponseCaching();
builder.Services.AddOutputCache(options =>
{
    options.AddBasePolicy(builder => builder.Expire(TimeSpan.FromMinutes(5)));
    options.AddPolicy("Products", builder =>
        builder.Expire(TimeSpan.FromMinutes(10))
               .Tag("products"));
});

// Usage
[OutputCache(PolicyName = "Products")]
[HttpGet]
public async Task<IActionResult> GetProducts()
{
    // ...
}
```

## Rate Limiting

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(
        context => RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.User.Identity?.Name ?? context.Connection.RemoteIpAddress?.ToString() ?? "anonymous",
            factory: _ => new FixedWindowRateLimiterOptions
            {
                AutoReplenishment = true,
                PermitLimit = 100,
                Window = TimeSpan.FromMinutes(1)
            }));

    options.OnRejected = async (context, token) =>
    {
        context.HttpContext.Response.StatusCode = 429;
        await context.HttpContext.Response.WriteAsync(
            "Too many requests. Please try again later.", token);
    };
});

app.UseRateLimiter();
```

---

**Last Updated:** 2025-12-16
**Applies To:** ASP.NET Core 8
