#!/usr/bin/env python3
"""
ASP.NET Core Security Configuration Generator

Generate security configuration for ASP.NET Core applications including
JWT authentication, Identity, OAuth2/OIDC, and authorization policies.

Part of senior-dotnet skill for engineering-team.

Usage:
    python security_config_generator.py [options]
    python security_config_generator.py --type jwt --roles Admin,User
    python security_config_generator.py --help
    python security_config_generator.py --version
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

__version__ = "1.0.0"


class SecurityConfigGenerator:
    """Generate ASP.NET Core security configuration."""

    VALID_AUTH_TYPES = ['jwt', 'identity', 'oidc', 'api-key']

    def __init__(self, auth_type: str = 'jwt', roles: str = 'Admin,User',
                 namespace: str = 'MyApp', output_dir: Optional[str] = None,
                 include_refresh: bool = True, verbose: bool = False):
        """
        Initialize Security Config Generator.

        Args:
            auth_type: Authentication type (jwt, identity, oidc, api-key)
            roles: Comma-separated list of roles
            namespace: Root namespace
            output_dir: Output directory
            include_refresh: Include refresh token support (for JWT)
            verbose: Enable verbose output
        """
        self.auth_type = auth_type
        self.roles = [r.strip() for r in roles.split(',')]
        self.namespace = namespace
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.include_refresh = include_refresh
        self.verbose = verbose

    def _log(self, message: str) -> None:
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"  {message}")

    def validate(self) -> List[str]:
        """Validate configuration."""
        errors = []

        if self.auth_type not in self.VALID_AUTH_TYPES:
            errors.append(f"Invalid auth type: {self.auth_type}")

        if not self.roles:
            errors.append("At least one role is required")

        return errors

    def generate(self) -> Dict:
        """Generate security configuration files."""
        errors = self.validate()
        if errors:
            return {
                'success': False,
                'errors': errors,
                'files_created': []
            }

        files_created = []

        try:
            # Create directories
            (self.output_dir / "Security").mkdir(parents=True, exist_ok=True)
            (self.output_dir / "Services").mkdir(parents=True, exist_ok=True)
            (self.output_dir / "Extensions").mkdir(parents=True, exist_ok=True)

            # Generate based on auth type
            if self.auth_type == 'jwt':
                files_created.extend(self._generate_jwt_config())
            elif self.auth_type == 'identity':
                files_created.extend(self._generate_identity_config())
            elif self.auth_type == 'oidc':
                files_created.extend(self._generate_oidc_config())
            elif self.auth_type == 'api-key':
                files_created.extend(self._generate_apikey_config())

            # Generate common files
            files_created.append(self._generate_auth_extension())
            files_created.append(self._generate_policies())
            files_created.append(self._generate_appsettings())

            return {
                'success': True,
                'files_created': [str(f) for f in files_created],
                'auth_type': self.auth_type,
                'roles': self.roles
            }

        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)],
                'files_created': [str(f) for f in files_created]
            }

    def _generate_jwt_config(self) -> List[Path]:
        """Generate JWT authentication configuration."""
        paths = []

        # JWT Options
        jwt_options = f'''namespace {self.namespace}.Security;

/// <summary>
/// JWT configuration options.
/// </summary>
public class JwtOptions
{{
    public const string SectionName = "Jwt";

    public string Secret {{ get; set; }} = string.Empty;
    public string Issuer {{ get; set; }} = string.Empty;
    public string Audience {{ get; set; }} = string.Empty;
    public int ExpirationMinutes {{ get; set; }} = 60;
    public int RefreshExpirationDays {{ get; set; }} = 7;
}}
'''
        path = self.output_dir / "Security" / "JwtOptions.cs"
        path.write_text(jwt_options)
        paths.append(path)
        self._log(f"Created {path.name}")

        # JWT Token Service Interface
        interface_content = f'''namespace {self.namespace}.Security;

/// <summary>
/// Interface for JWT token service.
/// </summary>
public interface IJwtTokenService
{{
    string GenerateAccessToken(string userId, string email, IEnumerable<string> roles);
    string GenerateRefreshToken();
    bool ValidateAccessToken(string token, out string? userId);
}}
'''
        path = self.output_dir / "Security" / "IJwtTokenService.cs"
        path.write_text(interface_content)
        paths.append(path)
        self._log(f"Created {path.name}")

        # JWT Token Service Implementation
        service_content = f'''using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;

namespace {self.namespace}.Security;

/// <summary>
/// JWT token generation and validation service.
/// </summary>
public class JwtTokenService : IJwtTokenService
{{
    private readonly JwtOptions _options;

    public JwtTokenService(IOptions<JwtOptions> options)
    {{
        _options = options.Value;
    }}

    public string GenerateAccessToken(string userId, string email, IEnumerable<string> roles)
    {{
        var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_options.Secret));
        var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);

        var claims = new List<Claim>
        {{
            new(JwtRegisteredClaimNames.Sub, userId),
            new(JwtRegisteredClaimNames.Email, email),
            new(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new(JwtRegisteredClaimNames.Iat, DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString(), ClaimValueTypes.Integer64)
        }};

        // Add roles
        foreach (var role in roles)
        {{
            claims.Add(new Claim(ClaimTypes.Role, role));
        }}

        var token = new JwtSecurityToken(
            issuer: _options.Issuer,
            audience: _options.Audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_options.ExpirationMinutes),
            signingCredentials: credentials
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }}

    public string GenerateRefreshToken()
    {{
        var randomNumber = new byte[64];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomNumber);
        return Convert.ToBase64String(randomNumber);
    }}

    public bool ValidateAccessToken(string token, out string? userId)
    {{
        userId = null;

        try
        {{
            var tokenHandler = new JwtSecurityTokenHandler();
            var key = Encoding.UTF8.GetBytes(_options.Secret);

            var validationParameters = new TokenValidationParameters
            {{
                ValidateIssuerSigningKey = true,
                IssuerSigningKey = new SymmetricSecurityKey(key),
                ValidateIssuer = true,
                ValidIssuer = _options.Issuer,
                ValidateAudience = true,
                ValidAudience = _options.Audience,
                ValidateLifetime = true,
                ClockSkew = TimeSpan.Zero
            }};

            var principal = tokenHandler.ValidateToken(token, validationParameters, out _);
            userId = principal.FindFirstValue(ClaimTypes.NameIdentifier);
            return true;
        }}
        catch
        {{
            return false;
        }}
    }}
}}
'''
        path = self.output_dir / "Security" / "JwtTokenService.cs"
        path.write_text(service_content)
        paths.append(path)
        self._log(f"Created {path.name}")

        # Auth Controller
        controller_content = f'''using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using {self.namespace}.Security;

namespace {self.namespace}.Controllers;

/// <summary>
/// Authentication controller for JWT token management.
/// </summary>
[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{{
    private readonly IJwtTokenService _tokenService;
    private readonly ILogger<AuthController> _logger;

    public AuthController(IJwtTokenService tokenService, ILogger<AuthController> logger)
    {{
        _tokenService = tokenService;
        _logger = logger;
    }}

    /// <summary>
    /// Login and get JWT token.
    /// </summary>
    [HttpPost("login")]
    [AllowAnonymous]
    [ProducesResponseType(typeof(TokenResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<ActionResult<TokenResponse>> Login([FromBody] LoginRequest request)
    {{
        // TODO: Validate credentials against your user store
        // This is a placeholder - implement your own user validation

        // Example: Generate token for valid user
        var accessToken = _tokenService.GenerateAccessToken(
            userId: "user-id",
            email: request.Email,
            roles: new[] {{ "User" }}
        );

        var refreshToken = _tokenService.GenerateRefreshToken();

        _logger.LogInformation("User {{Email}} logged in successfully", request.Email);

        return Ok(new TokenResponse
        {{
            AccessToken = accessToken,
            RefreshToken = refreshToken,
            ExpiresIn = 3600
        }});
    }}

    /// <summary>
    /// Refresh access token.
    /// </summary>
    [HttpPost("refresh")]
    [AllowAnonymous]
    [ProducesResponseType(typeof(TokenResponse), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<ActionResult<TokenResponse>> Refresh([FromBody] RefreshTokenRequest request)
    {{
        // TODO: Validate refresh token against your store
        // This is a placeholder - implement your own refresh token validation

        var accessToken = _tokenService.GenerateAccessToken(
            userId: "user-id",
            email: "user@example.com",
            roles: new[] {{ "User" }}
        );

        var refreshToken = _tokenService.GenerateRefreshToken();

        return Ok(new TokenResponse
        {{
            AccessToken = accessToken,
            RefreshToken = refreshToken,
            ExpiresIn = 3600
        }});
    }}
}}

public record LoginRequest
{{
    public string Email {{ get; init; }} = string.Empty;
    public string Password {{ get; init; }} = string.Empty;
}}

public record RefreshTokenRequest
{{
    public string RefreshToken {{ get; init; }} = string.Empty;
}}

public record TokenResponse
{{
    public string AccessToken {{ get; init; }} = string.Empty;
    public string RefreshToken {{ get; init; }} = string.Empty;
    public int ExpiresIn {{ get; init; }}
}}
'''
        (self.output_dir / "Controllers").mkdir(parents=True, exist_ok=True)
        path = self.output_dir / "Controllers" / "AuthController.cs"
        path.write_text(controller_content)
        paths.append(path)
        self._log(f"Created {path.name}")

        return paths

    def _generate_identity_config(self) -> List[Path]:
        """Generate ASP.NET Core Identity configuration."""
        paths = []

        # Application User
        user_content = f'''using Microsoft.AspNetCore.Identity;

namespace {self.namespace}.Security;

/// <summary>
/// Application user extending IdentityUser.
/// </summary>
public class ApplicationUser : IdentityUser
{{
    public string? FirstName {{ get; set; }}
    public string? LastName {{ get; set; }}
    public DateTime CreatedAt {{ get; set; }} = DateTime.UtcNow;
    public DateTime? LastLoginAt {{ get; set; }}
    public bool IsActive {{ get; set; }} = true;
}}
'''
        path = self.output_dir / "Security" / "ApplicationUser.cs"
        path.write_text(user_content)
        paths.append(path)
        self._log(f"Created {path.name}")

        # Application Role
        role_content = f'''using Microsoft.AspNetCore.Identity;

namespace {self.namespace}.Security;

/// <summary>
/// Application role extending IdentityRole.
/// </summary>
public class ApplicationRole : IdentityRole
{{
    public string? Description {{ get; set; }}
    public DateTime CreatedAt {{ get; set; }} = DateTime.UtcNow;
}}
'''
        path = self.output_dir / "Security" / "ApplicationRole.cs"
        path.write_text(role_content)
        paths.append(path)
        self._log(f"Created {path.name}")

        # Identity DbContext Extension
        dbcontext_content = f'''using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using {self.namespace}.Security;

namespace {self.namespace}.Data;

/// <summary>
/// Application DbContext with Identity support.
/// </summary>
public class ApplicationDbContext : IdentityDbContext<ApplicationUser, ApplicationRole, string>
{{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {{
    }}

    protected override void OnModelCreating(ModelBuilder builder)
    {{
        base.OnModelCreating(builder);

        // Customize Identity tables
        builder.Entity<ApplicationUser>(entity =>
        {{
            entity.ToTable("Users");
            entity.Property(e => e.FirstName).HasMaxLength(100);
            entity.Property(e => e.LastName).HasMaxLength(100);
        }});

        builder.Entity<ApplicationRole>(entity =>
        {{
            entity.ToTable("Roles");
            entity.Property(e => e.Description).HasMaxLength(256);
        }});
    }}
}}
'''
        (self.output_dir / "Data").mkdir(parents=True, exist_ok=True)
        path = self.output_dir / "Data" / "ApplicationDbContext.cs"
        path.write_text(dbcontext_content)
        paths.append(path)
        self._log(f"Created {path.name}")

        return paths

    def _generate_oidc_config(self) -> List[Path]:
        """Generate OpenID Connect configuration."""
        paths = []

        # OIDC Options
        oidc_options = f'''namespace {self.namespace}.Security;

/// <summary>
/// OpenID Connect configuration options.
/// </summary>
public class OidcOptions
{{
    public const string SectionName = "Oidc";

    public string Authority {{ get; set; }} = string.Empty;
    public string ClientId {{ get; set; }} = string.Empty;
    public string ClientSecret {{ get; set; }} = string.Empty;
    public string[] Scopes {{ get; set; }} = Array.Empty<string>();
    public string CallbackPath {{ get; set; }} = "/signin-oidc";
    public string SignedOutCallbackPath {{ get; set; }} = "/signout-callback-oidc";
}}
'''
        path = self.output_dir / "Security" / "OidcOptions.cs"
        path.write_text(oidc_options)
        paths.append(path)
        self._log(f"Created {path.name}")

        return paths

    def _generate_apikey_config(self) -> List[Path]:
        """Generate API Key authentication configuration."""
        paths = []

        # API Key Handler
        handler_content = f'''using System.Security.Claims;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Options;

namespace {self.namespace}.Security;

/// <summary>
/// API Key authentication handler.
/// </summary>
public class ApiKeyAuthenticationHandler : AuthenticationHandler<ApiKeyAuthenticationOptions>
{{
    private const string ApiKeyHeaderName = "X-Api-Key";

    public ApiKeyAuthenticationHandler(
        IOptionsMonitor<ApiKeyAuthenticationOptions> options,
        ILoggerFactory logger,
        UrlEncoder encoder)
        : base(options, logger, encoder)
    {{
    }}

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {{
        if (!Request.Headers.TryGetValue(ApiKeyHeaderName, out var apiKeyHeaderValues))
        {{
            return Task.FromResult(AuthenticateResult.NoResult());
        }}

        var providedApiKey = apiKeyHeaderValues.FirstOrDefault();

        if (string.IsNullOrEmpty(providedApiKey))
        {{
            return Task.FromResult(AuthenticateResult.NoResult());
        }}

        // Validate API key (implement your own validation logic)
        if (!Options.ValidApiKeys.Contains(providedApiKey))
        {{
            return Task.FromResult(AuthenticateResult.Fail("Invalid API Key"));
        }}

        var claims = new[]
        {{
            new Claim(ClaimTypes.Name, "ApiKeyUser"),
            new Claim(ClaimTypes.AuthenticationMethod, "ApiKey")
        }};

        var identity = new ClaimsIdentity(claims, Scheme.Name);
        var principal = new ClaimsPrincipal(identity);
        var ticket = new AuthenticationTicket(principal, Scheme.Name);

        return Task.FromResult(AuthenticateResult.Success(ticket));
    }}
}}

/// <summary>
/// API Key authentication options.
/// </summary>
public class ApiKeyAuthenticationOptions : AuthenticationSchemeOptions
{{
    public HashSet<string> ValidApiKeys {{ get; set; }} = new();
}}
'''
        path = self.output_dir / "Security" / "ApiKeyAuthenticationHandler.cs"
        path.write_text(handler_content)
        paths.append(path)
        self._log(f"Created {path.name}")

        return paths

    def _generate_auth_extension(self) -> Path:
        """Generate authentication service extension."""
        jwt_config = ''
        identity_config = ''
        oidc_config = ''
        apikey_config = ''

        if self.auth_type == 'jwt':
            jwt_config = '''
        // Configure JWT
        services.Configure<JwtOptions>(configuration.GetSection(JwtOptions.SectionName));
        services.AddScoped<IJwtTokenService, JwtTokenService>();

        var jwtOptions = configuration.GetSection(JwtOptions.SectionName).Get<JwtOptions>()!;

        services.AddAuthentication(options =>
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
                    Encoding.UTF8.GetBytes(jwtOptions.Secret)),
                ValidateIssuer = true,
                ValidIssuer = jwtOptions.Issuer,
                ValidateAudience = true,
                ValidAudience = jwtOptions.Audience,
                ValidateLifetime = true,
                ClockSkew = TimeSpan.Zero
            };
        });'''

        elif self.auth_type == 'identity':
            identity_config = '''
        // Configure Identity
        services.AddIdentity<ApplicationUser, ApplicationRole>(options =>
        {
            // Password settings
            options.Password.RequireDigit = true;
            options.Password.RequireLowercase = true;
            options.Password.RequireUppercase = true;
            options.Password.RequireNonAlphanumeric = true;
            options.Password.RequiredLength = 8;

            // Lockout settings
            options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
            options.Lockout.MaxFailedAccessAttempts = 5;

            // User settings
            options.User.RequireUniqueEmail = true;
        })
        .AddEntityFrameworkStores<ApplicationDbContext>()
        .AddDefaultTokenProviders();'''

        elif self.auth_type == 'oidc':
            oidc_config = '''
        // Configure OIDC
        services.Configure<OidcOptions>(configuration.GetSection(OidcOptions.SectionName));

        var oidcOptions = configuration.GetSection(OidcOptions.SectionName).Get<OidcOptions>()!;

        services.AddAuthentication(options =>
        {
            options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
            options.DefaultChallengeScheme = OpenIdConnectDefaults.AuthenticationScheme;
        })
        .AddCookie()
        .AddOpenIdConnect(options =>
        {
            options.Authority = oidcOptions.Authority;
            options.ClientId = oidcOptions.ClientId;
            options.ClientSecret = oidcOptions.ClientSecret;
            options.ResponseType = "code";
            options.SaveTokens = true;

            foreach (var scope in oidcOptions.Scopes)
            {
                options.Scope.Add(scope);
            }
        });'''

        elif self.auth_type == 'api-key':
            apikey_config = '''
        // Configure API Key Authentication
        var apiKeys = configuration.GetSection("ApiKeys").Get<string[]>() ?? Array.Empty<string>();

        services.AddAuthentication("ApiKey")
            .AddScheme<ApiKeyAuthenticationOptions, ApiKeyAuthenticationHandler>("ApiKey", options =>
            {
                options.ValidApiKeys = new HashSet<string>(apiKeys);
            });'''

        roles_list = ', '.join([f'"{r}"' for r in self.roles])

        content = f'''using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.IdentityModel.Tokens;
using {self.namespace}.Security;

namespace {self.namespace}.Extensions;

/// <summary>
/// Extension methods for configuring authentication services.
/// </summary>
public static class AuthenticationExtensions
{{
    public static IServiceCollection AddApplicationAuthentication(
        this IServiceCollection services,
        IConfiguration configuration)
    {{{jwt_config}{identity_config}{oidc_config}{apikey_config}

        // Configure Authorization Policies
        services.AddAuthorizationBuilder()
            .AddPolicy("RequireAdminRole", policy =>
                policy.RequireRole("Admin"))
            .AddPolicy("RequireUserRole", policy =>
                policy.RequireRole({roles_list}));

        return services;
    }}
}}
'''
        path = self.output_dir / "Extensions" / "AuthenticationExtensions.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_policies(self) -> Path:
        """Generate authorization policies."""
        policies = []
        for role in self.roles:
            policies.append(f'''    /// <summary>
    /// Policy requiring {role} role.
    /// </summary>
    public const string Require{role}Role = "Require{role}Role";''')

        content = f'''namespace {self.namespace}.Security;

/// <summary>
/// Authorization policy constants.
/// </summary>
public static class AuthorizationPolicies
{{
{chr(10).join(policies)}

    /// <summary>
    /// Policy requiring any authenticated user.
    /// </summary>
    public const string RequireAuthenticatedUser = "RequireAuthenticatedUser";
}}
'''
        path = self.output_dir / "Security" / "AuthorizationPolicies.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_appsettings(self) -> Path:
        """Generate appsettings.json security section."""
        if self.auth_type == 'jwt':
            settings = {
                "Jwt": {
                    "Secret": "YourSecretKeyHere-MustBeAtLeast32CharactersLong!",
                    "Issuer": "MyApp",
                    "Audience": "MyApp",
                    "ExpirationMinutes": 60,
                    "RefreshExpirationDays": 7
                }
            }
        elif self.auth_type == 'oidc':
            settings = {
                "Oidc": {
                    "Authority": "https://your-identity-provider.com",
                    "ClientId": "your-client-id",
                    "ClientSecret": "your-client-secret",
                    "Scopes": ["openid", "profile", "email"],
                    "CallbackPath": "/signin-oidc",
                    "SignedOutCallbackPath": "/signout-callback-oidc"
                }
            }
        elif self.auth_type == 'api-key':
            settings = {
                "ApiKeys": [
                    "your-api-key-1",
                    "your-api-key-2"
                ]
            }
        else:
            settings = {}

        content = json.dumps(settings, indent=2)
        path = self.output_dir / "appsettings.security.json"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path


def main():
    """Main entry point with CLI interface."""
    parser = argparse.ArgumentParser(
        description="Security Config Generator - Generate ASP.NET Core security configuration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --type jwt --roles Admin,User
  %(prog)s --type identity --roles Admin,Manager,User
  %(prog)s --type oidc
  %(prog)s --type api-key

Authentication Types:
  jwt      - JWT Bearer authentication (default)
  identity - ASP.NET Core Identity
  oidc     - OpenID Connect
  api-key  - API Key authentication

Part of senior-dotnet skill.
"""
    )

    parser.add_argument(
        '--type', '-t',
        choices=SecurityConfigGenerator.VALID_AUTH_TYPES,
        default='jwt',
        help='Authentication type (default: jwt)'
    )

    parser.add_argument(
        '--roles', '-r',
        default='Admin,User',
        help='Comma-separated roles (default: Admin,User)'
    )

    parser.add_argument(
        '--namespace', '-n',
        default='MyApp',
        help='Root namespace (default: MyApp)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output directory (default: current directory)'
    )

    parser.add_argument(
        '--no-refresh',
        action='store_true',
        help='Disable refresh token support (for JWT)'
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

    print(f"Generating security configuration")
    print(f"  Type: {args.type}")
    print(f"  Roles: {args.roles}")
    print()

    generator = SecurityConfigGenerator(
        auth_type=args.type,
        roles=args.roles,
        namespace=args.namespace,
        output_dir=args.output,
        include_refresh=not args.no_refresh,
        verbose=args.verbose
    )

    result = generator.generate()

    if result['success']:
        print(f"Security configuration generated successfully!")
        print(f"  Files created: {len(result['files_created'])}")
        for f in result['files_created']:
            print(f"    - {Path(f).name}")
        print("\nNext steps:")
        print("  1. Update appsettings.json with values from appsettings.security.json")
        print("  2. Add builder.Services.AddApplicationAuthentication(builder.Configuration); to Program.cs")
        print("  3. Add app.UseAuthentication(); and app.UseAuthorization(); to middleware pipeline")
    else:
        print("Error generating configuration:")
        for error in result['errors']:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
