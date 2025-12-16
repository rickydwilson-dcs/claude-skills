# Entity Framework Core Guide

Comprehensive guide to Entity Framework Core including entity configuration, migrations, query optimization, change tracking, and concurrency handling.

## Entity Configuration

### Data Annotations

```csharp
public class Product
{
    [Key]
    public int Id { get; set; }

    [Required]
    [StringLength(200)]
    public string Name { get; set; } = string.Empty;

    [Column(TypeName = "decimal(18,2)")]
    public decimal Price { get; set; }

    [ForeignKey(nameof(Category))]
    public int CategoryId { get; set; }

    public virtual Category Category { get; set; } = null!;
}
```

### Fluent API Configuration

```csharp
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.ToTable("Products");

        builder.HasKey(p => p.Id);

        builder.Property(p => p.Name)
            .HasMaxLength(200)
            .IsRequired();

        builder.Property(p => p.Price)
            .HasPrecision(18, 2);

        builder.HasOne(p => p.Category)
            .WithMany(c => c.Products)
            .HasForeignKey(p => p.CategoryId)
            .OnDelete(DeleteBehavior.Restrict);

        builder.HasIndex(p => p.Name)
            .HasDatabaseName("IX_Products_Name");

        builder.HasIndex(p => new { p.CategoryId, p.Name })
            .IsUnique();
    }
}

// Apply configurations in DbContext
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.ApplyConfigurationsFromAssembly(
        typeof(ApplicationDbContext).Assembly);
}
```

### Value Objects

```csharp
public record Address
{
    public string Street { get; init; } = string.Empty;
    public string City { get; init; } = string.Empty;
    public string PostalCode { get; init; } = string.Empty;
    public string Country { get; init; } = string.Empty;
}

// Configure as owned entity
builder.OwnsOne(c => c.ShippingAddress, a =>
{
    a.Property(p => p.Street).HasMaxLength(200);
    a.Property(p => p.City).HasMaxLength(100);
    a.Property(p => p.PostalCode).HasMaxLength(20);
    a.Property(p => p.Country).HasMaxLength(100);
});
```

## Migrations

### Create Migration

```bash
# Create migration
dotnet ef migrations add InitialCreate --project src/Infrastructure --startup-project src/Api

# Apply migration
dotnet ef database update --project src/Infrastructure --startup-project src/Api

# Generate SQL script
dotnet ef migrations script --project src/Infrastructure --startup-project src/Api -o script.sql
```

### Migration with Data Seeding

```csharp
public partial class SeedInitialData : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.InsertData(
            table: "Categories",
            columns: new[] { "Id", "Name" },
            values: new object[,]
            {
                { 1, "Electronics" },
                { 2, "Books" },
                { 3, "Clothing" }
            });
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DeleteData(
            table: "Categories",
            keyColumn: "Id",
            keyValues: new object[] { 1, 2, 3 });
    }
}
```

### Programmatic Migration

```csharp
public static async Task MigrateDatabaseAsync(IHost host)
{
    using var scope = host.Services.CreateScope();
    var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();

    await context.Database.MigrateAsync();
}
```

## Query Optimization

### Eager Loading

```csharp
// Include related entities
var orders = await _context.Orders
    .Include(o => o.Customer)
    .Include(o => o.Items)
        .ThenInclude(i => i.Product)
    .ToListAsync();

// With filter
var orders = await _context.Orders
    .Include(o => o.Items.Where(i => i.Quantity > 0))
    .ToListAsync();
```

### Split Queries

```csharp
// Avoid Cartesian explosion
var orders = await _context.Orders
    .Include(o => o.Items)
    .Include(o => o.Payments)
    .AsSplitQuery()
    .ToListAsync();

// Global configuration
protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
{
    optionsBuilder.UseQuerySplittingBehavior(QuerySplittingBehavior.SplitQuery);
}
```

### Projections

```csharp
// Select only needed columns
var orderSummaries = await _context.Orders
    .Select(o => new OrderSummaryDto
    {
        Id = o.Id,
        CustomerName = o.Customer.Name,
        Total = o.Items.Sum(i => i.Price * i.Quantity),
        ItemCount = o.Items.Count
    })
    .ToListAsync();
```

### AsNoTracking

```csharp
// For read-only queries
var products = await _context.Products
    .AsNoTracking()
    .Where(p => p.IsActive)
    .ToListAsync();

// Global no-tracking
public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
    : base(options)
{
    ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.NoTracking;
}
```

### Compiled Queries

```csharp
private static readonly Func<ApplicationDbContext, int, Task<Product?>>
    GetProductById = EF.CompileAsyncQuery(
        (ApplicationDbContext context, int id) =>
            context.Products.FirstOrDefault(p => p.Id == id));

// Usage
var product = await GetProductById(_context, productId);
```

## N+1 Query Prevention

### Problem Pattern

```csharp
// BAD: N+1 queries
var orders = await _context.Orders.ToListAsync();
foreach (var order in orders)
{
    // Each iteration causes a new query!
    var items = await _context.OrderItems
        .Where(i => i.OrderId == order.Id)
        .ToListAsync();
}
```

### Solution Patterns

```csharp
// GOOD: Eager loading
var orders = await _context.Orders
    .Include(o => o.Items)
    .ToListAsync();

// GOOD: Batch loading
var orderIds = orders.Select(o => o.Id).ToList();
var items = await _context.OrderItems
    .Where(i => orderIds.Contains(i.OrderId))
    .ToListAsync();

var itemsByOrder = items.GroupBy(i => i.OrderId)
    .ToDictionary(g => g.Key, g => g.ToList());
```

## Change Tracking

### Entity States

| State | Description |
|-------|-------------|
| Detached | Not tracked by context |
| Unchanged | Tracked, no changes |
| Added | New entity, will be inserted |
| Modified | Changed, will be updated |
| Deleted | Will be deleted |

### Manual State Management

```csharp
// Attach existing entity
_context.Entry(entity).State = EntityState.Modified;

// Update specific properties only
_context.Entry(entity).Property(e => e.Name).IsModified = true;

// Detach entity
_context.Entry(entity).State = EntityState.Detached;
```

### Audit Fields

```csharp
public override Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
{
    foreach (var entry in ChangeTracker.Entries<IAuditable>())
    {
        switch (entry.State)
        {
            case EntityState.Added:
                entry.Entity.CreatedAt = DateTime.UtcNow;
                entry.Entity.CreatedBy = _currentUser.Id;
                break;
            case EntityState.Modified:
                entry.Entity.UpdatedAt = DateTime.UtcNow;
                entry.Entity.UpdatedBy = _currentUser.Id;
                break;
        }
    }

    return base.SaveChangesAsync(cancellationToken);
}
```

## Concurrency Handling

### Optimistic Concurrency

```csharp
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;

    [Timestamp]
    public byte[] RowVersion { get; set; } = null!;
}

// Or with Fluent API
builder.Property(p => p.RowVersion)
    .IsRowVersion();
```

### Handling Conflicts

```csharp
try
{
    await _context.SaveChangesAsync();
}
catch (DbUpdateConcurrencyException ex)
{
    foreach (var entry in ex.Entries)
    {
        var proposedValues = entry.CurrentValues;
        var databaseValues = await entry.GetDatabaseValuesAsync();

        if (databaseValues == null)
        {
            // Entity was deleted
            throw new Exception("Entity was deleted by another user");
        }

        // Client wins strategy
        entry.OriginalValues.SetValues(databaseValues);

        // Or: Database wins strategy
        // entry.CurrentValues.SetValues(databaseValues);
    }

    await _context.SaveChangesAsync();
}
```

## Transactions

### Implicit Transactions

```csharp
// SaveChanges uses implicit transaction
await _context.Products.AddAsync(product);
await _context.OrderItems.AddRangeAsync(items);
await _context.SaveChangesAsync(); // All or nothing
```

### Explicit Transactions

```csharp
using var transaction = await _context.Database.BeginTransactionAsync();

try
{
    await _context.Products.AddAsync(product);
    await _context.SaveChangesAsync();

    // External operation
    await _paymentService.ProcessPaymentAsync();

    await _context.Orders.AddAsync(order);
    await _context.SaveChangesAsync();

    await transaction.CommitAsync();
}
catch
{
    await transaction.RollbackAsync();
    throw;
}
```

## Raw SQL

### FromSqlRaw

```csharp
var products = await _context.Products
    .FromSqlRaw("SELECT * FROM Products WHERE Price > {0}", minPrice)
    .ToListAsync();

// With interpolation (safe)
var products = await _context.Products
    .FromSqlInterpolated($"SELECT * FROM Products WHERE Price > {minPrice}")
    .ToListAsync();
```

### ExecuteSqlRaw

```csharp
await _context.Database.ExecuteSqlRawAsync(
    "UPDATE Products SET Price = Price * {0} WHERE CategoryId = {1}",
    multiplier, categoryId);
```

## Performance Diagnostics

### Query Logging

```csharp
// appsettings.Development.json
{
  "Logging": {
    "LogLevel": {
      "Microsoft.EntityFrameworkCore.Database.Command": "Information"
    }
  }
}
```

### Query Tags

```csharp
var products = await _context.Products
    .TagWith("GetActiveProducts - ProductService")
    .Where(p => p.IsActive)
    .ToListAsync();
```

---

**Last Updated:** 2025-12-16
**Applies To:** Entity Framework Core 8
