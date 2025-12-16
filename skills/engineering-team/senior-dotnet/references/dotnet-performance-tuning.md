# .NET Performance Tuning Guide

Comprehensive guide to optimizing .NET application performance including async patterns, memory management, caching, connection pooling, and profiling tools.

## Async Best Practices

### Proper Async/Await Usage

```csharp
// GOOD: Async all the way
public async Task<IActionResult> GetUserAsync(int id)
{
    var user = await _userService.GetByIdAsync(id);
    return Ok(user);
}

// BAD: Blocking on async (deadlock risk)
public IActionResult GetUser(int id)
{
    var user = _userService.GetByIdAsync(id).Result; // Blocks thread!
    return Ok(user);
}

// BAD: Unnecessary async
public async Task<int> GetCountAsync()
{
    return await Task.FromResult(42); // Just return 42 directly
}

// GOOD: Return task directly when no await needed
public Task<User> GetUserAsync(int id)
{
    return _repository.GetByIdAsync(id); // No async keyword needed
}
```

### ConfigureAwait Usage

```csharp
// Library code - use ConfigureAwait(false)
public async Task<Data> GetDataAsync()
{
    var result = await _httpClient.GetAsync(url)
        .ConfigureAwait(false);

    var content = await result.Content.ReadAsStringAsync()
        .ConfigureAwait(false);

    return JsonSerializer.Deserialize<Data>(content);
}

// ASP.NET Core - ConfigureAwait(false) not needed (no sync context)
// But doesn't hurt and helps when code is reused in other contexts
```

### Parallel Async Operations

```csharp
// GOOD: Parallel independent operations
public async Task<DashboardData> GetDashboardAsync(int userId)
{
    var userTask = _userService.GetByIdAsync(userId);
    var ordersTask = _orderService.GetRecentAsync(userId);
    var notificationsTask = _notificationService.GetUnreadAsync(userId);

    await Task.WhenAll(userTask, ordersTask, notificationsTask);

    return new DashboardData
    {
        User = userTask.Result,
        Orders = ordersTask.Result,
        Notifications = notificationsTask.Result
    };
}

// With timeout
public async Task<Data> GetWithTimeoutAsync()
{
    using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));

    try
    {
        return await _service.GetDataAsync(cts.Token);
    }
    catch (OperationCanceledException)
    {
        throw new TimeoutException("Operation timed out");
    }
}
```

### ValueTask for High-Performance Scenarios

```csharp
// Use ValueTask when result is often synchronous
public ValueTask<CachedItem> GetCachedItemAsync(string key)
{
    if (_cache.TryGetValue(key, out var item))
    {
        return ValueTask.FromResult(item); // No allocation
    }

    return new ValueTask<CachedItem>(LoadFromDatabaseAsync(key));
}

// IMPORTANT: Don't await ValueTask multiple times
var valueTask = GetCachedItemAsync("key");
var result = await valueTask;
// DON'T: await valueTask again - undefined behavior!
```

## Memory Management

### Span<T> and Memory<T>

```csharp
// GOOD: Use Span for stack-based slicing
public void ProcessData(ReadOnlySpan<byte> data)
{
    var header = data.Slice(0, 4);
    var payload = data.Slice(4);
    // No heap allocations for slices
}

// Parsing without allocations
public static int ParseInt(ReadOnlySpan<char> span)
{
    int result = 0;
    foreach (var c in span)
    {
        result = result * 10 + (c - '0');
    }
    return result;
}

// String manipulation without allocation
public static ReadOnlySpan<char> GetFileName(ReadOnlySpan<char> path)
{
    var lastSlash = path.LastIndexOf('/');
    return lastSlash >= 0 ? path.Slice(lastSlash + 1) : path;
}
```

### ArrayPool for Buffer Reuse

```csharp
public async Task ProcessLargeFileAsync(Stream stream)
{
    var buffer = ArrayPool<byte>.Shared.Rent(81920); // 80KB

    try
    {
        int bytesRead;
        while ((bytesRead = await stream.ReadAsync(buffer)) > 0)
        {
            ProcessChunk(buffer.AsSpan(0, bytesRead));
        }
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(buffer);
    }
}
```

### Object Pooling

```csharp
// Configure object pooling
builder.Services.AddSingleton<ObjectPool<StringBuilder>>(
    serviceProvider =>
    {
        var policy = new StringBuilderPooledObjectPolicy();
        return new DefaultObjectPool<StringBuilder>(policy, 100);
    });

// Usage
public class ReportGenerator
{
    private readonly ObjectPool<StringBuilder> _pool;

    public ReportGenerator(ObjectPool<StringBuilder> pool)
    {
        _pool = pool;
    }

    public string GenerateReport(IEnumerable<Item> items)
    {
        var sb = _pool.Get();

        try
        {
            foreach (var item in items)
            {
                sb.AppendLine(item.ToString());
            }
            return sb.ToString();
        }
        finally
        {
            _pool.Return(sb);
        }
    }
}
```

### Reducing Allocations

```csharp
// BAD: String concatenation in loop
string result = "";
foreach (var item in items)
{
    result += item.Name + ", "; // New string each iteration
}

// GOOD: StringBuilder
var sb = new StringBuilder();
foreach (var item in items)
{
    sb.Append(item.Name).Append(", ");
}
var result = sb.ToString();

// BETTER: String.Join
var result = string.Join(", ", items.Select(i => i.Name));

// BAD: Boxing value types
object boxed = 42; // Allocates on heap

// GOOD: Generic constraints avoid boxing
void Process<T>(T value) where T : struct { }
```

## Caching Strategies

### In-Memory Caching

```csharp
builder.Services.AddMemoryCache();

public class ProductService
{
    private readonly IMemoryCache _cache;
    private readonly IProductRepository _repository;

    public ProductService(IMemoryCache cache, IProductRepository repository)
    {
        _cache = cache;
        _repository = repository;
    }

    public async Task<Product> GetProductAsync(int id)
    {
        var cacheKey = $"product_{id}";

        if (!_cache.TryGetValue(cacheKey, out Product product))
        {
            product = await _repository.GetByIdAsync(id);

            var cacheOptions = new MemoryCacheEntryOptions()
                .SetSlidingExpiration(TimeSpan.FromMinutes(5))
                .SetAbsoluteExpiration(TimeSpan.FromHours(1))
                .SetPriority(CacheItemPriority.Normal)
                .SetSize(1);

            _cache.Set(cacheKey, product, cacheOptions);
        }

        return product;
    }

    public void InvalidateProduct(int id)
    {
        _cache.Remove($"product_{id}");
    }
}
```

### Distributed Caching with Redis

```csharp
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("Redis");
    options.InstanceName = "MyApp_";
});

public class DistributedCacheService
{
    private readonly IDistributedCache _cache;
    private readonly JsonSerializerOptions _jsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    public DistributedCacheService(IDistributedCache cache)
    {
        _cache = cache;
    }

    public async Task<T?> GetAsync<T>(string key, CancellationToken ct = default)
    {
        var data = await _cache.GetAsync(key, ct);

        if (data == null)
            return default;

        return JsonSerializer.Deserialize<T>(data, _jsonOptions);
    }

    public async Task SetAsync<T>(string key, T value, TimeSpan? expiration = null,
        CancellationToken ct = default)
    {
        var options = new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = expiration ?? TimeSpan.FromHours(1)
        };

        var data = JsonSerializer.SerializeToUtf8Bytes(value, _jsonOptions);
        await _cache.SetAsync(key, data, options, ct);
    }
}
```

### Response Caching

```csharp
builder.Services.AddResponseCaching();

app.UseResponseCaching();

[HttpGet("{id}")]
[ResponseCache(Duration = 60, VaryByQueryKeys = new[] { "version" })]
public async Task<IActionResult> GetProduct(int id, string? version)
{
    var product = await _productService.GetProductAsync(id);
    return Ok(product);
}
```

### Output Caching (.NET 7+)

```csharp
builder.Services.AddOutputCache(options =>
{
    options.AddBasePolicy(builder => builder.Expire(TimeSpan.FromMinutes(10)));

    options.AddPolicy("Products", builder =>
        builder.Expire(TimeSpan.FromMinutes(5))
               .Tag("products"));
});

app.UseOutputCache();

[HttpGet]
[OutputCache(PolicyName = "Products")]
public async Task<IActionResult> GetProducts()
{
    return Ok(await _productService.GetAllAsync());
}

// Invalidate by tag
public async Task InvalidateProductCache(IOutputCacheStore store)
{
    await store.EvictByTagAsync("products", default);
}
```

## Connection Pooling

### Database Connection Pooling

```csharp
// SQL Server - pooling enabled by default
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 3,
            maxRetryDelay: TimeSpan.FromSeconds(30),
            errorNumbersToAdd: null);
    }));

// Connection string pooling settings
"Server=localhost;Database=MyDb;User Id=sa;Password=xxx;
 Min Pool Size=5;Max Pool Size=100;Connection Timeout=30;
 Connection Lifetime=0;Pooling=true"
```

### HttpClient Pooling with IHttpClientFactory

```csharp
// BAD: Creates new HttpClient each time (socket exhaustion)
using var client = new HttpClient();
var response = await client.GetAsync(url);

// GOOD: Use IHttpClientFactory
builder.Services.AddHttpClient<IApiClient, ApiClient>(client =>
{
    client.BaseAddress = new Uri("https://api.example.com");
    client.DefaultRequestHeaders.Add("Accept", "application/json");
    client.Timeout = TimeSpan.FromSeconds(30);
})
.ConfigurePrimaryHttpMessageHandler(() => new SocketsHttpHandler
{
    PooledConnectionLifetime = TimeSpan.FromMinutes(5),
    PooledConnectionIdleTimeout = TimeSpan.FromMinutes(2),
    MaxConnectionsPerServer = 100
})
.AddPolicyHandler(GetRetryPolicy())
.AddPolicyHandler(GetCircuitBreakerPolicy());

// Retry policy with Polly
static IAsyncPolicy<HttpResponseMessage> GetRetryPolicy()
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .WaitAndRetryAsync(3, retryAttempt =>
            TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)));
}

// Circuit breaker
static IAsyncPolicy<HttpResponseMessage> GetCircuitBreakerPolicy()
{
    return HttpPolicyExtensions
        .HandleTransientHttpError()
        .CircuitBreakerAsync(5, TimeSpan.FromSeconds(30));
}
```

## EF Core Performance

### Efficient Querying

```csharp
// Use AsNoTracking for read-only queries
var products = await _context.Products
    .AsNoTracking()
    .Where(p => p.IsActive)
    .ToListAsync();

// Project to DTOs to avoid over-fetching
var productDtos = await _context.Products
    .AsNoTracking()
    .Where(p => p.CategoryId == categoryId)
    .Select(p => new ProductDto
    {
        Id = p.Id,
        Name = p.Name,
        Price = p.Price
    })
    .ToListAsync();

// Avoid N+1 with Include
var orders = await _context.Orders
    .Include(o => o.Customer)
    .Include(o => o.OrderItems)
        .ThenInclude(oi => oi.Product)
    .ToListAsync();

// Use split queries for complex includes
var orders = await _context.Orders
    .Include(o => o.OrderItems)
    .AsSplitQuery()
    .ToListAsync();
```

### Bulk Operations

```csharp
// Use ExecuteUpdate for bulk updates (.NET 7+)
await _context.Products
    .Where(p => p.CategoryId == categoryId)
    .ExecuteUpdateAsync(setters => setters
        .SetProperty(p => p.IsActive, false)
        .SetProperty(p => p.ModifiedAt, DateTime.UtcNow));

// Use ExecuteDelete for bulk deletes
await _context.Products
    .Where(p => p.IsDeleted && p.DeletedAt < cutoffDate)
    .ExecuteDeleteAsync();
```

### Compiled Queries

```csharp
public class ProductRepository
{
    private static readonly Func<AppDbContext, int, Task<Product?>> GetByIdQuery =
        EF.CompileAsyncQuery((AppDbContext context, int id) =>
            context.Products.FirstOrDefault(p => p.Id == id));

    private readonly AppDbContext _context;

    public Task<Product?> GetByIdAsync(int id)
    {
        return GetByIdQuery(_context, id);
    }
}
```

## Profiling Tools

### Built-in Diagnostics

```csharp
// Enable detailed EF Core logging
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString)
           .LogTo(Console.WriteLine, LogLevel.Information)
           .EnableSensitiveDataLogging()
           .EnableDetailedErrors());

// DiagnosticSource for tracing
builder.Services.AddSingleton<DiagnosticListener>(sp =>
    new DiagnosticListener("MyApp"));
```

### MiniProfiler Integration

```csharp
builder.Services.AddMiniProfiler(options =>
{
    options.RouteBasePath = "/profiler";
    options.ColorScheme = StackExchange.Profiling.ColorScheme.Dark;
    options.EnableMvcFilterProfiling = true;
    options.EnableMvcViewProfiling = true;
}).AddEntityFramework();

app.UseMiniProfiler();

// Usage in code
using (MiniProfiler.Current.Step("Loading products"))
{
    var products = await _repository.GetAllAsync();
}
```

### Application Insights

```csharp
builder.Services.AddApplicationInsightsTelemetry();

// Custom telemetry
public class OrderService
{
    private readonly TelemetryClient _telemetry;

    public async Task<Order> ProcessOrderAsync(OrderRequest request)
    {
        using var operation = _telemetry.StartOperation<RequestTelemetry>("ProcessOrder");

        var stopwatch = Stopwatch.StartNew();

        try
        {
            var order = await CreateOrderAsync(request);

            _telemetry.TrackMetric("OrderProcessingTime", stopwatch.ElapsedMilliseconds);
            _telemetry.TrackEvent("OrderCreated", new Dictionary<string, string>
            {
                ["OrderId"] = order.Id.ToString(),
                ["CustomerId"] = request.CustomerId.ToString()
            });

            return order;
        }
        catch (Exception ex)
        {
            _telemetry.TrackException(ex);
            throw;
        }
    }
}
```

### BenchmarkDotNet for Micro-Benchmarks

```csharp
[MemoryDiagnoser]
[RankColumn]
public class SerializationBenchmarks
{
    private readonly User _user = new() { Name = "John", Age = 30 };

    [Benchmark(Baseline = true)]
    public string NewtonsoftJson()
    {
        return JsonConvert.SerializeObject(_user);
    }

    [Benchmark]
    public string SystemTextJson()
    {
        return JsonSerializer.Serialize(_user);
    }
}

// Run: dotnet run -c Release
```

## Performance Checklist

### General
- [ ] Use async/await properly (async all the way)
- [ ] Avoid blocking calls (.Result, .Wait())
- [ ] Use CancellationToken for long operations
- [ ] Implement proper exception handling

### Memory
- [ ] Use Span<T>/Memory<T> for buffer operations
- [ ] Use ArrayPool for temporary buffers
- [ ] Avoid string concatenation in loops
- [ ] Profile for memory leaks with dotMemory

### Database
- [ ] Use AsNoTracking for read-only queries
- [ ] Project to DTOs (avoid over-fetching)
- [ ] Use Include/ThenInclude to prevent N+1
- [ ] Consider compiled queries for hot paths
- [ ] Use bulk operations for mass updates

### HTTP
- [ ] Use IHttpClientFactory (connection pooling)
- [ ] Configure appropriate timeouts
- [ ] Implement retry policies with Polly
- [ ] Use circuit breakers for resilience

### Caching
- [ ] Implement appropriate caching strategy
- [ ] Use distributed cache for scaled deployments
- [ ] Set appropriate expiration policies
- [ ] Implement cache invalidation

---

**Last Updated:** 2025-12-16
**Applies To:** .NET 8
