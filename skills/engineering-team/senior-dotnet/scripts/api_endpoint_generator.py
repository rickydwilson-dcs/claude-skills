#!/usr/bin/env python3
"""
API Endpoint Generator

Generate RESTful API endpoints with Controllers or Minimal APIs,
including validation, error handling, pagination, and OpenAPI documentation.

Part of senior-dotnet skill for engineering-team.

Usage:
    python api_endpoint_generator.py RESOURCE_NAME [options]
    python api_endpoint_generator.py products --methods GET,POST,PUT,DELETE
    python api_endpoint_generator.py --help
    python api_endpoint_generator.py --version
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

__version__ = "1.0.0"


class ApiEndpointGenerator:
    """Generate RESTful API endpoints."""

    VALID_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    VALID_STYLES = ['controller', 'minimal-api']

    def __init__(self, resource_name: str, methods: str = 'GET,POST,PUT,DELETE',
                 style: str = 'controller', paginated: bool = False,
                 namespace: str = 'MyApp', output_dir: Optional[str] = None,
                 verbose: bool = False):
        """
        Initialize API Endpoint Generator.

        Args:
            resource_name: Name of the resource (e.g., 'products', 'orders')
            methods: Comma-separated HTTP methods
            style: API style (controller or minimal-api)
            paginated: Include pagination support
            namespace: Root namespace
            output_dir: Output directory
            verbose: Enable verbose output
        """
        self.resource_name = resource_name.lower()
        self.methods = [m.strip().upper() for m in methods.split(',')]
        self.style = style
        self.paginated = paginated
        self.namespace = namespace
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.verbose = verbose

        # Derived names
        self.singular_name = self._singularize(resource_name)
        self.pascal_name = self._to_pascal_case(self.singular_name)
        self.plural_pascal = self._to_pascal_case(resource_name)

    def _log(self, message: str) -> None:
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"  {message}")

    def _to_pascal_case(self, name: str) -> str:
        """Convert to PascalCase."""
        return ''.join(word.capitalize() for word in name.replace('_', '-').split('-'))

    def _singularize(self, name: str) -> str:
        """Simple singularization (removes trailing 's')."""
        if name.endswith('ies'):
            return name[:-3] + 'y'
        elif name.endswith('es'):
            return name[:-2]
        elif name.endswith('s') and not name.endswith('ss'):
            return name[:-1]
        return name

    def validate(self) -> List[str]:
        """Validate configuration."""
        errors = []

        if not self.resource_name:
            errors.append("Resource name is required")

        for method in self.methods:
            if method not in self.VALID_METHODS:
                errors.append(f"Invalid HTTP method: {method}")

        if self.style not in self.VALID_STYLES:
            errors.append(f"Invalid style: {self.style}")

        return errors

    def generate(self) -> Dict:
        """Generate API endpoint files."""
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
            if self.style == 'controller':
                (self.output_dir / "Controllers").mkdir(parents=True, exist_ok=True)
            else:
                (self.output_dir / "Endpoints").mkdir(parents=True, exist_ok=True)

            (self.output_dir / "DTOs").mkdir(parents=True, exist_ok=True)
            (self.output_dir / "Validators").mkdir(parents=True, exist_ok=True)

            # Generate based on style
            if self.style == 'controller':
                files_created.append(self._generate_controller())
            else:
                files_created.append(self._generate_minimal_api())

            # Generate DTOs
            files_created.extend(self._generate_dtos())

            # Generate validators
            files_created.extend(self._generate_validators())

            return {
                'success': True,
                'files_created': [str(f) for f in files_created],
                'resource': self.resource_name,
                'style': self.style,
                'methods': self.methods
            }

        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)],
                'files_created': [str(f) for f in files_created]
            }

    def _generate_controller(self) -> Path:
        """Generate MVC controller."""
        methods_code = []

        if 'GET' in self.methods:
            if self.paginated:
                methods_code.append(self._get_controller_get_all_paged())
            else:
                methods_code.append(self._get_controller_get_all())
            methods_code.append(self._get_controller_get_by_id())

        if 'POST' in self.methods:
            methods_code.append(self._get_controller_post())

        if 'PUT' in self.methods:
            methods_code.append(self._get_controller_put())

        if 'PATCH' in self.methods:
            methods_code.append(self._get_controller_patch())

        if 'DELETE' in self.methods:
            methods_code.append(self._get_controller_delete())

        content = f'''using Microsoft.AspNetCore.Mvc;
using FluentValidation;
using {self.namespace}.Api.DTOs;
using {self.namespace}.Domain.Interfaces;

namespace {self.namespace}.Api.Controllers;

/// <summary>
/// API controller for {self.pascal_name} operations.
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class {self.plural_pascal}Controller : ControllerBase
{{
    private readonly I{self.pascal_name}Service _service;
    private readonly ILogger<{self.plural_pascal}Controller> _logger;
    private readonly IValidator<Create{self.pascal_name}Request> _createValidator;
    private readonly IValidator<Update{self.pascal_name}Request> _updateValidator;

    public {self.plural_pascal}Controller(
        I{self.pascal_name}Service service,
        ILogger<{self.plural_pascal}Controller> logger,
        IValidator<Create{self.pascal_name}Request> createValidator,
        IValidator<Update{self.pascal_name}Request> updateValidator)
    {{
        _service = service;
        _logger = logger;
        _createValidator = createValidator;
        _updateValidator = updateValidator;
    }}

{chr(10).join(methods_code)}
}}
'''
        path = self.output_dir / "Controllers" / f"{self.plural_pascal}Controller.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_minimal_api(self) -> Path:
        """Generate Minimal API endpoints."""
        endpoints = []

        if 'GET' in self.methods:
            if self.paginated:
                endpoints.append(self._get_minimal_get_all_paged())
            else:
                endpoints.append(self._get_minimal_get_all())
            endpoints.append(self._get_minimal_get_by_id())

        if 'POST' in self.methods:
            endpoints.append(self._get_minimal_post())

        if 'PUT' in self.methods:
            endpoints.append(self._get_minimal_put())

        if 'DELETE' in self.methods:
            endpoints.append(self._get_minimal_delete())

        content = f'''using FluentValidation;
using {self.namespace}.Api.DTOs;
using {self.namespace}.Domain.Interfaces;

namespace {self.namespace}.Api.Endpoints;

/// <summary>
/// Minimal API endpoints for {self.pascal_name}.
/// </summary>
public static class {self.pascal_name}Endpoints
{{
    public static void Map{self.pascal_name}Endpoints(this IEndpointRouteBuilder app)
    {{
        var group = app.MapGroup("/api/{self.resource_name}")
            .WithTags("{self.plural_pascal}")
            .WithOpenApi();

{chr(10).join(endpoints)}
    }}
}}
'''
        path = self.output_dir / "Endpoints" / f"{self.pascal_name}Endpoints.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _get_controller_get_all(self) -> str:
        """Generate GET all method for controller."""
        return f'''    /// <summary>
    /// Get all {self.resource_name}.
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(IEnumerable<{self.pascal_name}Response>), StatusCodes.Status200OK)]
    public async Task<ActionResult<IEnumerable<{self.pascal_name}Response>>> GetAll(
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Getting all {self.resource_name}");
        var result = await _service.GetAllAsync(cancellationToken);
        return Ok(result);
    }}'''

    def _get_controller_get_all_paged(self) -> str:
        """Generate GET all with pagination for controller."""
        return f'''    /// <summary>
    /// Get all {self.resource_name} with pagination.
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(PagedResponse<{self.pascal_name}Response>), StatusCodes.Status200OK)]
    public async Task<ActionResult<PagedResponse<{self.pascal_name}Response>>> GetAll(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 10,
        [FromQuery] string? sortBy = null,
        [FromQuery] bool descending = false,
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Getting {self.resource_name} - Page {{Page}}, Size {{PageSize}}", page, pageSize);

        if (page < 1) page = 1;
        if (pageSize < 1) pageSize = 10;
        if (pageSize > 100) pageSize = 100;

        var result = await _service.GetPagedAsync(page, pageSize, sortBy, descending, cancellationToken);
        return Ok(result);
    }}'''

    def _get_controller_get_by_id(self) -> str:
        """Generate GET by ID method for controller."""
        return f'''
    /// <summary>
    /// Get a {self.singular_name} by ID.
    /// </summary>
    [HttpGet("{{id}}")]
    [ProducesResponseType(typeof({self.pascal_name}Response), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult<{self.pascal_name}Response>> GetById(
        int id,
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Getting {self.singular_name} with ID {{Id}}", id);
        var result = await _service.GetByIdAsync(id, cancellationToken);

        if (result == null)
        {{
            return NotFound(new ProblemDetails
            {{
                Title = "{self.pascal_name} not found",
                Detail = $"{self.pascal_name} with ID {{id}} was not found.",
                Status = StatusCodes.Status404NotFound
            }});
        }}

        return Ok(result);
    }}'''

    def _get_controller_post(self) -> str:
        """Generate POST method for controller."""
        return f'''
    /// <summary>
    /// Create a new {self.singular_name}.
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof({self.pascal_name}Response), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<{self.pascal_name}Response>> Create(
        [FromBody] Create{self.pascal_name}Request request,
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Creating new {self.singular_name}");

        var validationResult = await _createValidator.ValidateAsync(request, cancellationToken);
        if (!validationResult.IsValid)
        {{
            return ValidationProblem(new ValidationProblemDetails(
                validationResult.Errors.GroupBy(e => e.PropertyName)
                    .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray())
            ));
        }}

        var result = await _service.CreateAsync(request, cancellationToken);
        return CreatedAtAction(nameof(GetById), new {{ id = result.Id }}, result);
    }}'''

    def _get_controller_put(self) -> str:
        """Generate PUT method for controller."""
        return f'''
    /// <summary>
    /// Update an existing {self.singular_name}.
    /// </summary>
    [HttpPut("{{id}}")]
    [ProducesResponseType(typeof({self.pascal_name}Response), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ValidationProblemDetails), StatusCodes.Status400BadRequest)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult<{self.pascal_name}Response>> Update(
        int id,
        [FromBody] Update{self.pascal_name}Request request,
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Updating {self.singular_name} with ID {{Id}}", id);

        var validationResult = await _updateValidator.ValidateAsync(request, cancellationToken);
        if (!validationResult.IsValid)
        {{
            return ValidationProblem(new ValidationProblemDetails(
                validationResult.Errors.GroupBy(e => e.PropertyName)
                    .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray())
            ));
        }}

        var result = await _service.UpdateAsync(id, request, cancellationToken);
        if (result == null)
        {{
            return NotFound(new ProblemDetails
            {{
                Title = "{self.pascal_name} not found",
                Detail = $"{self.pascal_name} with ID {{id}} was not found.",
                Status = StatusCodes.Status404NotFound
            }});
        }}

        return Ok(result);
    }}'''

    def _get_controller_patch(self) -> str:
        """Generate PATCH method for controller."""
        return f'''
    /// <summary>
    /// Partially update an existing {self.singular_name}.
    /// </summary>
    [HttpPatch("{{id}}")]
    [ProducesResponseType(typeof({self.pascal_name}Response), StatusCodes.Status200OK)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<ActionResult<{self.pascal_name}Response>> Patch(
        int id,
        [FromBody] Patch{self.pascal_name}Request request,
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Patching {self.singular_name} with ID {{Id}}", id);

        var result = await _service.PatchAsync(id, request, cancellationToken);
        if (result == null)
        {{
            return NotFound(new ProblemDetails
            {{
                Title = "{self.pascal_name} not found",
                Detail = $"{self.pascal_name} with ID {{id}} was not found.",
                Status = StatusCodes.Status404NotFound
            }});
        }}

        return Ok(result);
    }}'''

    def _get_controller_delete(self) -> str:
        """Generate DELETE method for controller."""
        return f'''
    /// <summary>
    /// Delete a {self.singular_name}.
    /// </summary>
    [HttpDelete("{{id}}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(
        int id,
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Deleting {self.singular_name} with ID {{Id}}", id);

        var deleted = await _service.DeleteAsync(id, cancellationToken);
        if (!deleted)
        {{
            return NotFound(new ProblemDetails
            {{
                Title = "{self.pascal_name} not found",
                Detail = $"{self.pascal_name} with ID {{id}} was not found.",
                Status = StatusCodes.Status404NotFound
            }});
        }}

        return NoContent();
    }}'''

    def _get_minimal_get_all(self) -> str:
        """Generate GET all for minimal API."""
        return f'''        group.MapGet("/", async (
            I{self.pascal_name}Service service,
            CancellationToken ct) =>
        {{
            var result = await service.GetAllAsync(ct);
            return Results.Ok(result);
        }})
        .WithName("GetAll{self.plural_pascal}")
        .Produces<IEnumerable<{self.pascal_name}Response>>(StatusCodes.Status200OK);'''

    def _get_minimal_get_all_paged(self) -> str:
        """Generate GET all with pagination for minimal API."""
        return f'''        group.MapGet("/", async (
            [AsParameters] PaginationQuery query,
            I{self.pascal_name}Service service,
            CancellationToken ct) =>
        {{
            var page = Math.Max(1, query.Page ?? 1);
            var pageSize = Math.Clamp(query.PageSize ?? 10, 1, 100);
            var result = await service.GetPagedAsync(page, pageSize, query.SortBy, query.Descending ?? false, ct);
            return Results.Ok(result);
        }})
        .WithName("GetAll{self.plural_pascal}")
        .Produces<PagedResponse<{self.pascal_name}Response>>(StatusCodes.Status200OK);'''

    def _get_minimal_get_by_id(self) -> str:
        """Generate GET by ID for minimal API."""
        return f'''
        group.MapGet("/{{id}}", async (
            int id,
            I{self.pascal_name}Service service,
            CancellationToken ct) =>
        {{
            var result = await service.GetByIdAsync(id, ct);
            return result is not null
                ? Results.Ok(result)
                : Results.NotFound();
        }})
        .WithName("Get{self.pascal_name}ById")
        .Produces<{self.pascal_name}Response>(StatusCodes.Status200OK)
        .Produces(StatusCodes.Status404NotFound);'''

    def _get_minimal_post(self) -> str:
        """Generate POST for minimal API."""
        return f'''
        group.MapPost("/", async (
            Create{self.pascal_name}Request request,
            IValidator<Create{self.pascal_name}Request> validator,
            I{self.pascal_name}Service service,
            CancellationToken ct) =>
        {{
            var validationResult = await validator.ValidateAsync(request, ct);
            if (!validationResult.IsValid)
            {{
                return Results.ValidationProblem(validationResult.ToDictionary());
            }}

            var result = await service.CreateAsync(request, ct);
            return Results.Created($"/api/{self.resource_name}/{{result.Id}}", result);
        }})
        .WithName("Create{self.pascal_name}")
        .Produces<{self.pascal_name}Response>(StatusCodes.Status201Created)
        .ProducesValidationProblem();'''

    def _get_minimal_put(self) -> str:
        """Generate PUT for minimal API."""
        return f'''
        group.MapPut("/{{id}}", async (
            int id,
            Update{self.pascal_name}Request request,
            IValidator<Update{self.pascal_name}Request> validator,
            I{self.pascal_name}Service service,
            CancellationToken ct) =>
        {{
            var validationResult = await validator.ValidateAsync(request, ct);
            if (!validationResult.IsValid)
            {{
                return Results.ValidationProblem(validationResult.ToDictionary());
            }}

            var result = await service.UpdateAsync(id, request, ct);
            return result is not null
                ? Results.Ok(result)
                : Results.NotFound();
        }})
        .WithName("Update{self.pascal_name}")
        .Produces<{self.pascal_name}Response>(StatusCodes.Status200OK)
        .ProducesValidationProblem()
        .Produces(StatusCodes.Status404NotFound);'''

    def _get_minimal_delete(self) -> str:
        """Generate DELETE for minimal API."""
        return f'''
        group.MapDelete("/{{id}}", async (
            int id,
            I{self.pascal_name}Service service,
            CancellationToken ct) =>
        {{
            var deleted = await service.DeleteAsync(id, ct);
            return deleted
                ? Results.NoContent()
                : Results.NotFound();
        }})
        .WithName("Delete{self.pascal_name}")
        .Produces(StatusCodes.Status204NoContent)
        .Produces(StatusCodes.Status404NotFound);'''

    def _generate_dtos(self) -> List[Path]:
        """Generate DTO classes."""
        paths = []

        # Response DTO
        response_content = f'''namespace {self.namespace}.Api.DTOs;

/// <summary>
/// Response DTO for {self.pascal_name}.
/// </summary>
public record {self.pascal_name}Response
{{
    public int Id {{ get; init; }}
    // Add your properties here
    public DateTime CreatedAt {{ get; init; }}
    public DateTime? UpdatedAt {{ get; init; }}
}}
'''
        response_path = self.output_dir / "DTOs" / f"{self.pascal_name}Response.cs"
        response_path.write_text(response_content)
        paths.append(response_path)
        self._log(f"Created {response_path.name}")

        # Create Request DTO
        if 'POST' in self.methods:
            create_content = f'''namespace {self.namespace}.Api.DTOs;

/// <summary>
/// Request DTO for creating a {self.pascal_name}.
/// </summary>
public record Create{self.pascal_name}Request
{{
    // Add your properties here
    public string Name {{ get; init; }} = string.Empty;
}}
'''
            create_path = self.output_dir / "DTOs" / f"Create{self.pascal_name}Request.cs"
            create_path.write_text(create_content)
            paths.append(create_path)
            self._log(f"Created {create_path.name}")

        # Update Request DTO
        if 'PUT' in self.methods:
            update_content = f'''namespace {self.namespace}.Api.DTOs;

/// <summary>
/// Request DTO for updating a {self.pascal_name}.
/// </summary>
public record Update{self.pascal_name}Request
{{
    // Add your properties here
    public string Name {{ get; init; }} = string.Empty;
}}
'''
            update_path = self.output_dir / "DTOs" / f"Update{self.pascal_name}Request.cs"
            update_path.write_text(update_content)
            paths.append(update_path)
            self._log(f"Created {update_path.name}")

        # Paged Response if paginated
        if self.paginated:
            paged_content = f'''namespace {self.namespace}.Api.DTOs;

/// <summary>
/// Generic paged response wrapper.
/// </summary>
public record PagedResponse<T>
{{
    public IEnumerable<T> Items {{ get; init; }} = Enumerable.Empty<T>();
    public int TotalCount {{ get; init; }}
    public int Page {{ get; init; }}
    public int PageSize {{ get; init; }}
    public int TotalPages => (int)Math.Ceiling((double)TotalCount / PageSize);
    public bool HasPreviousPage => Page > 1;
    public bool HasNextPage => Page < TotalPages;
}}

/// <summary>
/// Pagination query parameters.
/// </summary>
public record PaginationQuery
{{
    public int? Page {{ get; init; }}
    public int? PageSize {{ get; init; }}
    public string? SortBy {{ get; init; }}
    public bool? Descending {{ get; init; }}
}}
'''
            paged_path = self.output_dir / "DTOs" / "PagedResponse.cs"
            paged_path.write_text(paged_content)
            paths.append(paged_path)
            self._log(f"Created {paged_path.name}")

        return paths

    def _generate_validators(self) -> List[Path]:
        """Generate FluentValidation validators."""
        paths = []

        # Create validator
        if 'POST' in self.methods:
            create_content = f'''using FluentValidation;
using {self.namespace}.Api.DTOs;

namespace {self.namespace}.Api.Validators;

/// <summary>
/// Validator for Create{self.pascal_name}Request.
/// </summary>
public class Create{self.pascal_name}RequestValidator : AbstractValidator<Create{self.pascal_name}Request>
{{
    public Create{self.pascal_name}RequestValidator()
    {{
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(256).WithMessage("Name must not exceed 256 characters");

        // Add more validation rules
    }}
}}
'''
            create_path = self.output_dir / "Validators" / f"Create{self.pascal_name}RequestValidator.cs"
            create_path.write_text(create_content)
            paths.append(create_path)
            self._log(f"Created {create_path.name}")

        # Update validator
        if 'PUT' in self.methods:
            update_content = f'''using FluentValidation;
using {self.namespace}.Api.DTOs;

namespace {self.namespace}.Api.Validators;

/// <summary>
/// Validator for Update{self.pascal_name}Request.
/// </summary>
public class Update{self.pascal_name}RequestValidator : AbstractValidator<Update{self.pascal_name}Request>
{{
    public Update{self.pascal_name}RequestValidator()
    {{
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Name is required")
            .MaximumLength(256).WithMessage("Name must not exceed 256 characters");

        // Add more validation rules
    }}
}}
'''
            update_path = self.output_dir / "Validators" / f"Update{self.pascal_name}RequestValidator.cs"
            update_path.write_text(update_content)
            paths.append(update_path)
            self._log(f"Created {update_path.name}")

        return paths


def main():
    """Main entry point with CLI interface."""
    parser = argparse.ArgumentParser(
        description="API Endpoint Generator - Generate RESTful API endpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s products --methods GET,POST,PUT,DELETE
  %(prog)s orders --methods GET,POST --paginated
  %(prog)s users --style minimal-api --methods GET,POST
  %(prog)s reports --methods GET --paginated

HTTP Methods:
  GET     - Read resource(s)
  POST    - Create resource
  PUT     - Update resource (full)
  PATCH   - Update resource (partial)
  DELETE  - Delete resource

API Styles:
  controller  - Traditional MVC controller (default)
  minimal-api - ASP.NET Core Minimal APIs

Part of senior-dotnet skill.
"""
    )

    parser.add_argument(
        'resource_name',
        nargs='?',
        help='Name of the resource (plural, e.g., products, orders)'
    )

    parser.add_argument(
        '--methods', '-m',
        default='GET,POST,PUT,DELETE',
        help='Comma-separated HTTP methods (default: GET,POST,PUT,DELETE)'
    )

    parser.add_argument(
        '--style', '-s',
        choices=ApiEndpointGenerator.VALID_STYLES,
        default='controller',
        help='API style (default: controller)'
    )

    parser.add_argument(
        '--paginated', '-p',
        action='store_true',
        help='Include pagination support for GET endpoints'
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

    if not args.resource_name:
        parser.print_help()
        sys.exit(1)

    print(f"Generating API endpoints: {args.resource_name}")
    print(f"  Style: {args.style}")
    print(f"  Methods: {args.methods}")
    if args.paginated:
        print(f"  Paginated: Yes")
    print()

    generator = ApiEndpointGenerator(
        resource_name=args.resource_name,
        methods=args.methods,
        style=args.style,
        paginated=args.paginated,
        namespace=args.namespace,
        output_dir=args.output,
        verbose=args.verbose
    )

    result = generator.generate()

    if result['success']:
        print(f"Endpoints generated successfully!")
        print(f"  Files created: {len(result['files_created'])}")
        for f in result['files_created']:
            print(f"    - {Path(f).name}")
    else:
        print("Error generating endpoints:")
        for error in result['errors']:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
