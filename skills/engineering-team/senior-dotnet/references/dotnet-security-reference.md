# .NET Security Reference

Comprehensive guide to ASP.NET Core security including authentication, authorization, Data Protection API, OWASP compliance, and security headers.

## Authentication Schemes

### JWT Bearer Authentication

```csharp
builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(configuration["Jwt:Secret"]!)),
        ValidateIssuer = true,
        ValidIssuer = configuration["Jwt:Issuer"],
        ValidateAudience = true,
        ValidAudience = configuration["Jwt:Audience"],
        ValidateLifetime = true,
        ClockSkew = TimeSpan.Zero
    };

    options.Events = new JwtBearerEvents
    {
        OnAuthenticationFailed = context =>
        {
            if (context.Exception is SecurityTokenExpiredException)
            {
                context.Response.Headers.Append("Token-Expired", "true");
            }
            return Task.CompletedTask;
        }
    };
});
```

### Cookie Authentication

```csharp
builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddCookie(options =>
    {
        options.Cookie.Name = "MyApp.Auth";
        options.Cookie.HttpOnly = true;
        options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
        options.Cookie.SameSite = SameSiteMode.Strict;
        options.ExpireTimeSpan = TimeSpan.FromHours(24);
        options.SlidingExpiration = true;
        options.LoginPath = "/login";
        options.LogoutPath = "/logout";
        options.AccessDeniedPath = "/forbidden";
    });
```

### ASP.NET Core Identity

```csharp
builder.Services.AddIdentity<ApplicationUser, IdentityRole>(options =>
{
    // Password requirements
    options.Password.RequireDigit = true;
    options.Password.RequireLowercase = true;
    options.Password.RequireUppercase = true;
    options.Password.RequireNonAlphanumeric = true;
    options.Password.RequiredLength = 12;
    options.Password.RequiredUniqueChars = 4;

    // Lockout settings
    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(15);
    options.Lockout.MaxFailedAccessAttempts = 5;
    options.Lockout.AllowedForNewUsers = true;

    // User settings
    options.User.RequireUniqueEmail = true;
    options.User.AllowedUserNameCharacters =
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._@+";

    // Sign-in settings
    options.SignIn.RequireConfirmedEmail = true;
    options.SignIn.RequireConfirmedAccount = true;
})
.AddEntityFrameworkStores<ApplicationDbContext>()
.AddDefaultTokenProviders();
```

### OAuth2/OpenID Connect

```csharp
builder.Services.AddAuthentication(options =>
{
    options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = OpenIdConnectDefaults.AuthenticationScheme;
})
.AddCookie()
.AddOpenIdConnect(options =>
{
    options.Authority = "https://identity.example.com";
    options.ClientId = "my-app";
    options.ClientSecret = "secret";
    options.ResponseType = "code";
    options.SaveTokens = true;

    options.Scope.Add("openid");
    options.Scope.Add("profile");
    options.Scope.Add("email");

    options.GetClaimsFromUserInfoEndpoint = true;
    options.ClaimActions.MapJsonKey("role", "role");
});
```

## Authorization

### Role-Based Authorization

```csharp
// Attribute-based
[Authorize(Roles = "Admin")]
public class AdminController : ControllerBase { }

[Authorize(Roles = "Admin,Manager")]
public IActionResult Edit() { }

// Policy-based
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("RequireAdmin", policy =>
        policy.RequireRole("Admin"));

    options.AddPolicy("RequireManager", policy =>
        policy.RequireRole("Admin", "Manager"));
});
```

### Claims-Based Authorization

```csharp
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("EmployeeOnly", policy =>
        policy.RequireClaim("EmployeeId"));

    options.AddPolicy("SeniorEmployee", policy =>
        policy.RequireClaim("EmployeeLevel", "Senior", "Manager"));
});
```

### Policy-Based Authorization

```csharp
// Custom requirement
public class MinimumAgeRequirement : IAuthorizationRequirement
{
    public int MinimumAge { get; }
    public MinimumAgeRequirement(int minimumAge) => MinimumAge = minimumAge;
}

// Handler
public class MinimumAgeHandler : AuthorizationHandler<MinimumAgeRequirement>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        MinimumAgeRequirement requirement)
    {
        var dobClaim = context.User.FindFirst("DateOfBirth");
        if (dobClaim != null &&
            DateTime.TryParse(dobClaim.Value, out var dob))
        {
            var age = DateTime.Today.Year - dob.Year;
            if (age >= requirement.MinimumAge)
            {
                context.Succeed(requirement);
            }
        }
        return Task.CompletedTask;
    }
}

// Registration
builder.Services.AddSingleton<IAuthorizationHandler, MinimumAgeHandler>();
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AtLeast18", policy =>
        policy.Requirements.Add(new MinimumAgeRequirement(18)));
});
```

### Resource-Based Authorization

```csharp
public class DocumentAuthorizationHandler :
    AuthorizationHandler<OperationAuthorizationRequirement, Document>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        OperationAuthorizationRequirement requirement,
        Document resource)
    {
        if (requirement.Name == Operations.Read.Name)
        {
            if (resource.IsPublic ||
                context.User.Identity?.Name == resource.OwnerId)
            {
                context.Succeed(requirement);
            }
        }

        return Task.CompletedTask;
    }
}

// Usage in controller
public async Task<IActionResult> Get(int id)
{
    var document = await _repository.GetAsync(id);
    var authResult = await _authorizationService
        .AuthorizeAsync(User, document, Operations.Read);

    if (!authResult.Succeeded)
        return Forbid();

    return Ok(document);
}
```

## Data Protection API

### Basic Usage

```csharp
public class SecureDataService
{
    private readonly IDataProtector _protector;

    public SecureDataService(IDataProtectionProvider provider)
    {
        _protector = provider.CreateProtector("MyApp.SecureData.v1");
    }

    public string Protect(string plaintext) => _protector.Protect(plaintext);
    public string Unprotect(string ciphertext) => _protector.Unprotect(ciphertext);
}
```

### Time-Limited Data

```csharp
private readonly ITimeLimitedDataProtector _protector;

public SecureDataService(IDataProtectionProvider provider)
{
    _protector = provider.CreateProtector("MyApp.TimeLimited.v1")
        .ToTimeLimitedDataProtector();
}

public string ProtectWithExpiration(string data, TimeSpan lifetime)
{
    return _protector.Protect(data, lifetime);
}
```

### Key Management

```csharp
builder.Services.AddDataProtection()
    .PersistKeysToDbContext<ApplicationDbContext>()
    .ProtectKeysWithCertificate("thumbprint")
    .SetDefaultKeyLifetime(TimeSpan.FromDays(90))
    .SetApplicationName("MyApp");
```

## OWASP Compliance Checklist

### 1. Injection Prevention

```csharp
// BAD: SQL Injection vulnerable
var sql = $"SELECT * FROM Users WHERE Id = {userId}";

// GOOD: Parameterized query
var user = await _context.Users
    .Where(u => u.Id == userId)
    .FirstOrDefaultAsync();

// GOOD: FromSqlInterpolated (safe)
var users = await _context.Users
    .FromSqlInterpolated($"SELECT * FROM Users WHERE Id = {userId}")
    .ToListAsync();
```

### 2. XSS Prevention

```csharp
// In Razor - automatic encoding
<p>@Model.UserInput</p>

// Raw HTML (be careful!)
@Html.Raw(Model.SanitizedHtml)

// Manual encoding
var encoded = HtmlEncoder.Default.Encode(userInput);
```

### 3. CSRF Protection

```csharp
// Automatic with Razor Pages and MVC
[ValidateAntiForgeryToken]
[HttpPost]
public IActionResult Submit([FromForm] FormData data) { }

// API - use header validation
builder.Services.AddAntiforgery(options =>
{
    options.HeaderName = "X-XSRF-TOKEN";
});
```

### 4. Sensitive Data Exposure

```csharp
// Never log sensitive data
_logger.LogInformation("User {UserId} logged in", user.Id); // Good
_logger.LogInformation("User logged in: {User}", user); // Bad - might include password

// Use Data Protection for sensitive storage
var protectedData = _protector.Protect(sensitiveData);
```

### 5. Security Misconfiguration

```csharp
// Disable detailed errors in production
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/error");
    app.UseHsts();
}

// Remove server headers
builder.WebHost.ConfigureKestrel(options =>
{
    options.AddServerHeader = false;
});
```

## Security Headers

### Configuration

```csharp
app.Use(async (context, next) =>
{
    // Prevent clickjacking
    context.Response.Headers.Append("X-Frame-Options", "DENY");

    // XSS protection
    context.Response.Headers.Append("X-XSS-Protection", "1; mode=block");

    // Prevent MIME sniffing
    context.Response.Headers.Append("X-Content-Type-Options", "nosniff");

    // Content Security Policy
    context.Response.Headers.Append(
        "Content-Security-Policy",
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'");

    // Referrer Policy
    context.Response.Headers.Append("Referrer-Policy", "strict-origin-when-cross-origin");

    // Permissions Policy
    context.Response.Headers.Append(
        "Permissions-Policy",
        "geolocation=(), microphone=(), camera=()");

    await next();
});
```

### HSTS

```csharp
// In production
if (!app.Environment.IsDevelopment())
{
    app.UseHsts();
}

builder.Services.AddHsts(options =>
{
    options.Preload = true;
    options.IncludeSubDomains = true;
    options.MaxAge = TimeSpan.FromDays(365);
});
```

## Secrets Management

### Development Secrets

```bash
# Initialize secrets
dotnet user-secrets init

# Set secret
dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=..."

# List secrets
dotnet user-secrets list
```

### Azure Key Vault

```csharp
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{vaultName}.vault.azure.net/"),
    new DefaultAzureCredential());
```

### Environment Variables

```csharp
// appsettings.json (development only)
{
  "ConnectionStrings": {
    "DefaultConnection": "Development connection string"
  }
}

// Production: Use environment variables
// ConnectionStrings__DefaultConnection=Production connection string
```

## Security Testing

### Penetration Testing Headers

```csharp
// Add for security testing
app.Use(async (context, next) =>
{
    // Report security issues
    context.Response.Headers.Append(
        "Report-To",
        """{"group":"security-reports","max_age":31536000,"endpoints":[{"url":"https://example.com/security-report"}]}""");

    await next();
});
```

---

**Last Updated:** 2025-12-16
**Applies To:** ASP.NET Core 8
