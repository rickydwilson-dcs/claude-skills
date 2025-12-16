#!/usr/bin/env python3
"""
Entity Framework Core Entity Generator

Generate complete EF Core entity stacks with repository, service, controller,
DTO, and AutoMapper profile following Clean Architecture patterns.

Part of senior-dotnet skill for engineering-team.

Usage:
    python entity_generator.py ENTITY_NAME [options]
    python entity_generator.py Product --fields "Id:int,Name:string,Price:decimal"
    python entity_generator.py --help
    python entity_generator.py --version
"""

import os
import sys
import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

__version__ = "1.0.0"


class EntityGenerator:
    """Generate EF Core entities with complete stack."""

    CSHARP_TYPES = {
        'int': 'int',
        'long': 'long',
        'string': 'string',
        'decimal': 'decimal',
        'double': 'double',
        'float': 'float',
        'bool': 'bool',
        'boolean': 'bool',
        'datetime': 'DateTime',
        'date': 'DateOnly',
        'time': 'TimeOnly',
        'guid': 'Guid',
        'byte': 'byte',
        'byte[]': 'byte[]',
        'bytes': 'byte[]',
    }

    RELATION_TYPES = ['OneToOne', 'OneToMany', 'ManyToOne', 'ManyToMany']

    def __init__(self, entity_name: str, fields: str = '',
                 relations: str = '', namespace: str = 'MyApp',
                 output_dir: Optional[str] = None, auditable: bool = False,
                 fluent_api: bool = False, verbose: bool = False):
        """
        Initialize Entity Generator.

        Args:
            entity_name: Name of the entity (PascalCase)
            fields: Comma-separated field definitions (Name:Type)
            relations: Comma-separated relation definitions (Name:RelationType)
            namespace: Root namespace for generated code
            output_dir: Output directory
            auditable: Include audit fields (CreatedAt, UpdatedAt, etc.)
            fluent_api: Use Fluent API configuration instead of data annotations
            verbose: Enable verbose output
        """
        self.entity_name = entity_name
        self.fields_str = fields
        self.relations_str = relations
        self.namespace = namespace
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.auditable = auditable
        self.fluent_api = fluent_api
        self.verbose = verbose

        # Parse fields and relations
        self.fields = self._parse_fields(fields)
        self.relations = self._parse_relations(relations)

    def _log(self, message: str) -> None:
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"  {message}")

    def _parse_fields(self, fields_str: str) -> List[Dict]:
        """Parse field definitions from string."""
        if not fields_str:
            return []

        fields = []
        for field_def in fields_str.split(','):
            field_def = field_def.strip()
            if ':' not in field_def:
                continue

            parts = field_def.split(':')
            name = parts[0].strip()
            type_str = parts[1].strip().lower()

            # Map to C# type
            csharp_type = self.CSHARP_TYPES.get(type_str, type_str)

            # Check if nullable
            nullable = type_str.endswith('?')
            if nullable:
                type_str = type_str[:-1]
                csharp_type = self.CSHARP_TYPES.get(type_str, type_str)

            fields.append({
                'name': name,
                'type': csharp_type,
                'nullable': nullable,
                'is_key': name.lower() == 'id'
            })

        return fields

    def _parse_relations(self, relations_str: str) -> List[Dict]:
        """Parse relation definitions from string."""
        if not relations_str:
            return []

        relations = []
        for rel_def in relations_str.split(','):
            rel_def = rel_def.strip()
            if ':' not in rel_def:
                continue

            parts = rel_def.split(':')
            name = parts[0].strip()
            rel_type = parts[1].strip()

            if rel_type not in self.RELATION_TYPES:
                continue

            relations.append({
                'name': name,
                'type': rel_type,
                'entity': name  # Assume entity name matches property name
            })

        return relations

    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if not self.entity_name:
            errors.append("Entity name is required")
        elif not self.entity_name[0].isupper():
            errors.append("Entity name must be PascalCase (start with uppercase)")
        elif not self.entity_name.isalnum():
            errors.append("Entity name must be alphanumeric only")

        return errors

    def generate(self) -> Dict:
        """Generate all files for the entity."""
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
            (self.output_dir / "Entities").mkdir(parents=True, exist_ok=True)
            (self.output_dir / "Repositories").mkdir(parents=True, exist_ok=True)
            (self.output_dir / "Services").mkdir(parents=True, exist_ok=True)
            (self.output_dir / "Controllers").mkdir(parents=True, exist_ok=True)
            (self.output_dir / "DTOs").mkdir(parents=True, exist_ok=True)
            (self.output_dir / "Mappings").mkdir(parents=True, exist_ok=True)
            if self.fluent_api:
                (self.output_dir / "Configurations").mkdir(parents=True, exist_ok=True)

            # Generate entity
            entity_path = self._generate_entity()
            files_created.append(entity_path)

            # Generate repository interface and implementation
            repo_interface_path = self._generate_repository_interface()
            repo_impl_path = self._generate_repository_implementation()
            files_created.extend([repo_interface_path, repo_impl_path])

            # Generate service interface and implementation
            service_interface_path = self._generate_service_interface()
            service_impl_path = self._generate_service_implementation()
            files_created.extend([service_interface_path, service_impl_path])

            # Generate DTOs
            dto_paths = self._generate_dtos()
            files_created.extend(dto_paths)

            # Generate AutoMapper profile
            mapper_path = self._generate_mapper_profile()
            files_created.append(mapper_path)

            # Generate controller
            controller_path = self._generate_controller()
            files_created.append(controller_path)

            # Generate Fluent API configuration if requested
            if self.fluent_api:
                config_path = self._generate_fluent_config()
                files_created.append(config_path)

            return {
                'success': True,
                'files_created': [str(f) for f in files_created],
                'entity_name': self.entity_name,
                'fields_count': len(self.fields),
                'relations_count': len(self.relations)
            }

        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)],
                'files_created': [str(f) for f in files_created]
            }

    def _generate_entity(self) -> Path:
        """Generate entity class."""
        properties = []

        # Add fields
        for field in self.fields:
            nullable_mark = '?' if field['nullable'] and field['type'] not in ['int', 'long', 'decimal', 'double', 'float', 'bool', 'Guid'] else ''
            required_attr = '' if field['nullable'] or field['is_key'] else '[Required]\n        '

            if field['is_key']:
                properties.append(f'        [Key]\n        public {field["type"]} {field["name"]} {{ get; set; }}')
            elif field['type'] == 'string' and not field['nullable']:
                properties.append(f'        {required_attr}[StringLength(256)]\n        public {field["type"]}{nullable_mark} {field["name"]} {{ get; set; }} = string.Empty;')
            else:
                properties.append(f'        {required_attr}public {field["type"]}{nullable_mark} {field["name"]} {{ get; set; }}')

        # Add relations
        for rel in self.relations:
            if rel['type'] == 'ManyToOne':
                properties.append(f'        public int {rel["name"]}Id {{ get; set; }}')
                properties.append(f'        public virtual {rel["entity"]} {rel["name"]} {{ get; set; }} = null!;')
            elif rel['type'] == 'OneToMany':
                properties.append(f'        public virtual ICollection<{rel["entity"]}> {rel["name"]}s {{ get; set; }} = new List<{rel["entity"]}>();')
            elif rel['type'] == 'OneToOne':
                properties.append(f'        public virtual {rel["entity"]}? {rel["name"]} {{ get; set; }}')
            elif rel['type'] == 'ManyToMany':
                properties.append(f'        public virtual ICollection<{rel["entity"]}> {rel["name"]}s {{ get; set; }} = new List<{rel["entity"]}>();')

        # Add audit fields if requested
        audit_properties = ''
        if self.auditable:
            audit_properties = '''
        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
        public string? CreatedBy { get; set; }
        public DateTime? UpdatedAt { get; set; }
        public string? UpdatedBy { get; set; }'''

        content = f'''using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace {self.namespace}.Domain.Entities;

/// <summary>
/// {self.entity_name} entity representing a {self.entity_name.lower()} in the system.
/// </summary>
public class {self.entity_name}
{{
{chr(10).join(properties)}{audit_properties}
}}
'''
        path = self.output_dir / "Entities" / f"{self.entity_name}.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_repository_interface(self) -> Path:
        """Generate repository interface."""
        content = f'''using {self.namespace}.Domain.Entities;

namespace {self.namespace}.Domain.Interfaces;

/// <summary>
/// Repository interface for {self.entity_name} entity.
/// </summary>
public interface I{self.entity_name}Repository
{{
    Task<{self.entity_name}?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<IEnumerable<{self.entity_name}>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<IEnumerable<{self.entity_name}>> GetPagedAsync(int page, int pageSize, CancellationToken cancellationToken = default);
    Task<int> GetCountAsync(CancellationToken cancellationToken = default);
    Task<{self.entity_name}> AddAsync({self.entity_name} entity, CancellationToken cancellationToken = default);
    Task UpdateAsync({self.entity_name} entity, CancellationToken cancellationToken = default);
    Task DeleteAsync({self.entity_name} entity, CancellationToken cancellationToken = default);
    Task<bool> ExistsAsync(int id, CancellationToken cancellationToken = default);
}}
'''
        path = self.output_dir / "Repositories" / f"I{self.entity_name}Repository.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_repository_implementation(self) -> Path:
        """Generate repository implementation."""
        content = f'''using Microsoft.EntityFrameworkCore;
using {self.namespace}.Domain.Entities;
using {self.namespace}.Domain.Interfaces;
using {self.namespace}.Infrastructure.Data;

namespace {self.namespace}.Infrastructure.Repositories;

/// <summary>
/// Repository implementation for {self.entity_name} entity.
/// </summary>
public class {self.entity_name}Repository : I{self.entity_name}Repository
{{
    private readonly ApplicationDbContext _context;

    public {self.entity_name}Repository(ApplicationDbContext context)
    {{
        _context = context;
    }}

    public async Task<{self.entity_name}?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
    {{
        return await _context.{self.entity_name}s
            .AsNoTracking()
            .FirstOrDefaultAsync(e => e.Id == id, cancellationToken);
    }}

    public async Task<IEnumerable<{self.entity_name}>> GetAllAsync(CancellationToken cancellationToken = default)
    {{
        return await _context.{self.entity_name}s
            .AsNoTracking()
            .ToListAsync(cancellationToken);
    }}

    public async Task<IEnumerable<{self.entity_name}>> GetPagedAsync(int page, int pageSize, CancellationToken cancellationToken = default)
    {{
        return await _context.{self.entity_name}s
            .AsNoTracking()
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(cancellationToken);
    }}

    public async Task<int> GetCountAsync(CancellationToken cancellationToken = default)
    {{
        return await _context.{self.entity_name}s.CountAsync(cancellationToken);
    }}

    public async Task<{self.entity_name}> AddAsync({self.entity_name} entity, CancellationToken cancellationToken = default)
    {{
        await _context.{self.entity_name}s.AddAsync(entity, cancellationToken);
        await _context.SaveChangesAsync(cancellationToken);
        return entity;
    }}

    public async Task UpdateAsync({self.entity_name} entity, CancellationToken cancellationToken = default)
    {{
        _context.{self.entity_name}s.Update(entity);
        await _context.SaveChangesAsync(cancellationToken);
    }}

    public async Task DeleteAsync({self.entity_name} entity, CancellationToken cancellationToken = default)
    {{
        _context.{self.entity_name}s.Remove(entity);
        await _context.SaveChangesAsync(cancellationToken);
    }}

    public async Task<bool> ExistsAsync(int id, CancellationToken cancellationToken = default)
    {{
        return await _context.{self.entity_name}s.AnyAsync(e => e.Id == id, cancellationToken);
    }}
}}
'''
        path = self.output_dir / "Repositories" / f"{self.entity_name}Repository.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_service_interface(self) -> Path:
        """Generate service interface."""
        content = f'''using {self.namespace}.Api.DTOs;

namespace {self.namespace}.Domain.Interfaces;

/// <summary>
/// Service interface for {self.entity_name} operations.
/// </summary>
public interface I{self.entity_name}Service
{{
    Task<{self.entity_name}Dto?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<IEnumerable<{self.entity_name}Dto>> GetAllAsync(CancellationToken cancellationToken = default);
    Task<PagedResult<{self.entity_name}Dto>> GetPagedAsync(int page, int pageSize, CancellationToken cancellationToken = default);
    Task<{self.entity_name}Dto> CreateAsync(Create{self.entity_name}Dto dto, CancellationToken cancellationToken = default);
    Task<{self.entity_name}Dto?> UpdateAsync(int id, Update{self.entity_name}Dto dto, CancellationToken cancellationToken = default);
    Task<bool> DeleteAsync(int id, CancellationToken cancellationToken = default);
}}

/// <summary>
/// Generic paged result wrapper.
/// </summary>
public class PagedResult<T>
{{
    public IEnumerable<T> Items {{ get; set; }} = Enumerable.Empty<T>();
    public int TotalCount {{ get; set; }}
    public int Page {{ get; set; }}
    public int PageSize {{ get; set; }}
    public int TotalPages => (int)Math.Ceiling((double)TotalCount / PageSize);
    public bool HasPreviousPage => Page > 1;
    public bool HasNextPage => Page < TotalPages;
}}
'''
        path = self.output_dir / "Services" / f"I{self.entity_name}Service.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_service_implementation(self) -> Path:
        """Generate service implementation."""
        content = f'''using AutoMapper;
using {self.namespace}.Api.DTOs;
using {self.namespace}.Domain.Entities;
using {self.namespace}.Domain.Interfaces;

namespace {self.namespace}.Infrastructure.Services;

/// <summary>
/// Service implementation for {self.entity_name} operations.
/// </summary>
public class {self.entity_name}Service : I{self.entity_name}Service
{{
    private readonly I{self.entity_name}Repository _repository;
    private readonly IMapper _mapper;

    public {self.entity_name}Service(I{self.entity_name}Repository repository, IMapper mapper)
    {{
        _repository = repository;
        _mapper = mapper;
    }}

    public async Task<{self.entity_name}Dto?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
    {{
        var entity = await _repository.GetByIdAsync(id, cancellationToken);
        return entity == null ? null : _mapper.Map<{self.entity_name}Dto>(entity);
    }}

    public async Task<IEnumerable<{self.entity_name}Dto>> GetAllAsync(CancellationToken cancellationToken = default)
    {{
        var entities = await _repository.GetAllAsync(cancellationToken);
        return _mapper.Map<IEnumerable<{self.entity_name}Dto>>(entities);
    }}

    public async Task<PagedResult<{self.entity_name}Dto>> GetPagedAsync(int page, int pageSize, CancellationToken cancellationToken = default)
    {{
        var entities = await _repository.GetPagedAsync(page, pageSize, cancellationToken);
        var totalCount = await _repository.GetCountAsync(cancellationToken);

        return new PagedResult<{self.entity_name}Dto>
        {{
            Items = _mapper.Map<IEnumerable<{self.entity_name}Dto>>(entities),
            TotalCount = totalCount,
            Page = page,
            PageSize = pageSize
        }};
    }}

    public async Task<{self.entity_name}Dto> CreateAsync(Create{self.entity_name}Dto dto, CancellationToken cancellationToken = default)
    {{
        var entity = _mapper.Map<{self.entity_name}>(dto);
        var created = await _repository.AddAsync(entity, cancellationToken);
        return _mapper.Map<{self.entity_name}Dto>(created);
    }}

    public async Task<{self.entity_name}Dto?> UpdateAsync(int id, Update{self.entity_name}Dto dto, CancellationToken cancellationToken = default)
    {{
        var entity = await _repository.GetByIdAsync(id, cancellationToken);
        if (entity == null)
            return null;

        _mapper.Map(dto, entity);
        await _repository.UpdateAsync(entity, cancellationToken);
        return _mapper.Map<{self.entity_name}Dto>(entity);
    }}

    public async Task<bool> DeleteAsync(int id, CancellationToken cancellationToken = default)
    {{
        var entity = await _repository.GetByIdAsync(id, cancellationToken);
        if (entity == null)
            return false;

        await _repository.DeleteAsync(entity, cancellationToken);
        return true;
    }}
}}
'''
        path = self.output_dir / "Services" / f"{self.entity_name}Service.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_dtos(self) -> List[Path]:
        """Generate DTO classes."""
        paths = []

        # Generate properties for DTOs (excluding audit fields for create/update)
        dto_properties = []
        create_properties = []
        update_properties = []

        for field in self.fields:
            nullable_mark = '?' if field['nullable'] else ''
            init_value = ' = string.Empty;' if field['type'] == 'string' and not field['nullable'] else ''

            dto_properties.append(f'    public {field["type"]}{nullable_mark} {field["name"]} {{ get; set; }}{init_value}')

            if not field['is_key']:  # Exclude Id from create/update DTOs
                create_properties.append(f'    public {field["type"]}{nullable_mark} {field["name"]} {{ get; set; }}{init_value}')
                update_properties.append(f'    public {field["type"]}{nullable_mark} {field["name"]} {{ get; set; }}{init_value}')

        # Add audit fields to response DTO only
        if self.auditable:
            dto_properties.extend([
                '    public DateTime CreatedAt { get; set; }',
                '    public string? CreatedBy { get; set; }',
                '    public DateTime? UpdatedAt { get; set; }',
                '    public string? UpdatedBy { get; set; }'
            ])

        # Main DTO (response)
        dto_content = f'''namespace {self.namespace}.Api.DTOs;

/// <summary>
/// Data transfer object for {self.entity_name} responses.
/// </summary>
public class {self.entity_name}Dto
{{
{chr(10).join(dto_properties)}
}}
'''
        dto_path = self.output_dir / "DTOs" / f"{self.entity_name}Dto.cs"
        dto_path.write_text(dto_content)
        paths.append(dto_path)
        self._log(f"Created {dto_path.name}")

        # Create DTO
        create_content = f'''using System.ComponentModel.DataAnnotations;

namespace {self.namespace}.Api.DTOs;

/// <summary>
/// Data transfer object for creating a {self.entity_name}.
/// </summary>
public class Create{self.entity_name}Dto
{{
{chr(10).join(create_properties)}
}}
'''
        create_path = self.output_dir / "DTOs" / f"Create{self.entity_name}Dto.cs"
        create_path.write_text(create_content)
        paths.append(create_path)
        self._log(f"Created {create_path.name}")

        # Update DTO
        update_content = f'''using System.ComponentModel.DataAnnotations;

namespace {self.namespace}.Api.DTOs;

/// <summary>
/// Data transfer object for updating a {self.entity_name}.
/// </summary>
public class Update{self.entity_name}Dto
{{
{chr(10).join(update_properties)}
}}
'''
        update_path = self.output_dir / "DTOs" / f"Update{self.entity_name}Dto.cs"
        update_path.write_text(update_content)
        paths.append(update_path)
        self._log(f"Created {update_path.name}")

        return paths

    def _generate_mapper_profile(self) -> Path:
        """Generate AutoMapper profile."""
        content = f'''using AutoMapper;
using {self.namespace}.Api.DTOs;
using {self.namespace}.Domain.Entities;

namespace {self.namespace}.Api.Mappings;

/// <summary>
/// AutoMapper profile for {self.entity_name} mappings.
/// </summary>
public class {self.entity_name}Profile : Profile
{{
    public {self.entity_name}Profile()
    {{
        // Entity to DTO
        CreateMap<{self.entity_name}, {self.entity_name}Dto>();

        // Create DTO to Entity
        CreateMap<Create{self.entity_name}Dto, {self.entity_name}>();

        // Update DTO to Entity
        CreateMap<Update{self.entity_name}Dto, {self.entity_name}>()
            .ForAllMembers(opts => opts.Condition((src, dest, srcMember) => srcMember != null));
    }}
}}
'''
        path = self.output_dir / "Mappings" / f"{self.entity_name}Profile.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_controller(self) -> Path:
        """Generate API controller."""
        content = f'''using Microsoft.AspNetCore.Mvc;
using {self.namespace}.Api.DTOs;
using {self.namespace}.Domain.Interfaces;

namespace {self.namespace}.Api.Controllers;

/// <summary>
/// API controller for {self.entity_name} operations.
/// </summary>
[ApiController]
[Route("api/[controller]")]
[Produces("application/json")]
public class {self.entity_name}sController : ControllerBase
{{
    private readonly I{self.entity_name}Service _service;
    private readonly ILogger<{self.entity_name}sController> _logger;

    public {self.entity_name}sController(I{self.entity_name}Service service, ILogger<{self.entity_name}sController> logger)
    {{
        _service = service;
        _logger = logger;
    }}

    /// <summary>
    /// Get all {self.entity_name.lower()}s with pagination.
    /// </summary>
    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<{self.entity_name}Dto>), StatusCodes.Status200OK)]
    public async Task<ActionResult<PagedResult<{self.entity_name}Dto>>> GetAll(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 10,
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Getting {self.entity_name.lower()}s - Page {{Page}}, Size {{PageSize}}", page, pageSize);
        var result = await _service.GetPagedAsync(page, pageSize, cancellationToken);
        return Ok(result);
    }}

    /// <summary>
    /// Get a {self.entity_name.lower()} by ID.
    /// </summary>
    [HttpGet("{{id}}")]
    [ProducesResponseType(typeof({self.entity_name}Dto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<ActionResult<{self.entity_name}Dto>> GetById(int id, CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Getting {self.entity_name.lower()} with ID {{Id}}", id);
        var result = await _service.GetByIdAsync(id, cancellationToken);

        if (result == null)
        {{
            _logger.LogWarning("{self.entity_name} with ID {{Id}} not found", id);
            return NotFound();
        }}

        return Ok(result);
    }}

    /// <summary>
    /// Create a new {self.entity_name.lower()}.
    /// </summary>
    [HttpPost]
    [ProducesResponseType(typeof({self.entity_name}Dto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<{self.entity_name}Dto>> Create(
        [FromBody] Create{self.entity_name}Dto dto,
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Creating new {self.entity_name.lower()}");
        var result = await _service.CreateAsync(dto, cancellationToken);
        return CreatedAtAction(nameof(GetById), new {{ id = result.Id }}, result);
    }}

    /// <summary>
    /// Update an existing {self.entity_name.lower()}.
    /// </summary>
    [HttpPut("{{id}}")]
    [ProducesResponseType(typeof({self.entity_name}Dto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    public async Task<ActionResult<{self.entity_name}Dto>> Update(
        int id,
        [FromBody] Update{self.entity_name}Dto dto,
        CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Updating {self.entity_name.lower()} with ID {{Id}}", id);
        var result = await _service.UpdateAsync(id, dto, cancellationToken);

        if (result == null)
        {{
            _logger.LogWarning("{self.entity_name} with ID {{Id}} not found for update", id);
            return NotFound();
        }}

        return Ok(result);
    }}

    /// <summary>
    /// Delete a {self.entity_name.lower()}.
    /// </summary>
    [HttpDelete("{{id}}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> Delete(int id, CancellationToken cancellationToken = default)
    {{
        _logger.LogInformation("Deleting {self.entity_name.lower()} with ID {{Id}}", id);
        var deleted = await _service.DeleteAsync(id, cancellationToken);

        if (!deleted)
        {{
            _logger.LogWarning("{self.entity_name} with ID {{Id}} not found for deletion", id);
            return NotFound();
        }}

        return NoContent();
    }}
}}
'''
        path = self.output_dir / "Controllers" / f"{self.entity_name}sController.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path

    def _generate_fluent_config(self) -> Path:
        """Generate Fluent API entity configuration."""
        property_configs = []

        for field in self.fields:
            if field['is_key']:
                property_configs.append(f'''            builder.HasKey(e => e.{field["name"]});''')
            elif field['type'] == 'string':
                max_length = 256 if not field['nullable'] else 512
                required = '.IsRequired()' if not field['nullable'] else ''
                property_configs.append(f'''            builder.Property(e => e.{field["name"]})
                .HasMaxLength({max_length}){required};''')
            elif not field['nullable']:
                property_configs.append(f'''            builder.Property(e => e.{field["name"]})
                .IsRequired();''')

        # Add relationship configurations
        for rel in self.relations:
            if rel['type'] == 'ManyToOne':
                property_configs.append(f'''
            builder.HasOne(e => e.{rel["name"]})
                .WithMany()
                .HasForeignKey(e => e.{rel["name"]}Id)
                .OnDelete(DeleteBehavior.Restrict);''')
            elif rel['type'] == 'OneToMany':
                property_configs.append(f'''
            builder.HasMany(e => e.{rel["name"]}s)
                .WithOne()
                .OnDelete(DeleteBehavior.Cascade);''')

        content = f'''using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using {self.namespace}.Domain.Entities;

namespace {self.namespace}.Infrastructure.Configurations;

/// <summary>
/// EF Core Fluent API configuration for {self.entity_name}.
/// </summary>
public class {self.entity_name}Configuration : IEntityTypeConfiguration<{self.entity_name}>
{{
    public void Configure(EntityTypeBuilder<{self.entity_name}> builder)
    {{
        builder.ToTable("{self.entity_name}s");

{chr(10).join(property_configs)}

        // Add indexes
        builder.HasIndex(e => e.Id);
    }}
}}
'''
        path = self.output_dir / "Configurations" / f"{self.entity_name}Configuration.cs"
        path.write_text(content)
        self._log(f"Created {path.name}")
        return path


def main():
    """Main entry point with CLI interface."""
    parser = argparse.ArgumentParser(
        description="Entity Generator - Generate complete EF Core entity stacks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s Product --fields "Id:int,Name:string,Price:decimal"
  %(prog)s Order --fields "Id:int,Total:decimal" --relations "Customer:ManyToOne"
  %(prog)s User --fields "Id:int,Email:string,Name:string" --auditable
  %(prog)s Invoice --fields "Id:int,Amount:decimal" --fluent-api

Field Types:
  int, long, string, decimal, double, float, bool, datetime, date, time, guid, byte[]

Relation Types:
  OneToOne, OneToMany, ManyToOne, ManyToMany

Part of senior-dotnet skill.
"""
    )

    parser.add_argument(
        'entity_name',
        nargs='?',
        help='Name of the entity (PascalCase)'
    )

    parser.add_argument(
        '--fields', '-f',
        default='',
        help='Comma-separated field definitions (Name:Type)'
    )

    parser.add_argument(
        '--relations', '-r',
        default='',
        help='Comma-separated relation definitions (Name:RelationType)'
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
        '--auditable', '-a',
        action='store_true',
        help='Include audit fields (CreatedAt, UpdatedAt, etc.)'
    )

    parser.add_argument(
        '--fluent-api',
        action='store_true',
        help='Generate Fluent API configuration instead of data annotations'
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

    if not args.entity_name:
        parser.print_help()
        sys.exit(1)

    print(f"Generating entity: {args.entity_name}")
    if args.fields:
        print(f"  Fields: {args.fields}")
    if args.relations:
        print(f"  Relations: {args.relations}")
    if args.auditable:
        print(f"  Auditable: Yes")
    print()

    generator = EntityGenerator(
        entity_name=args.entity_name,
        fields=args.fields,
        relations=args.relations,
        namespace=args.namespace,
        output_dir=args.output,
        auditable=args.auditable,
        fluent_api=args.fluent_api,
        verbose=args.verbose
    )

    result = generator.generate()

    if result['success']:
        print(f"Entity generated successfully!")
        print(f"  Files created: {len(result['files_created'])}")
        for f in result['files_created']:
            print(f"    - {Path(f).name}")
    else:
        print("Error generating entity:")
        for error in result['errors']:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
