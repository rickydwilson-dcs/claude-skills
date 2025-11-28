# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- {new_feature_description}

### Changed
- {change_description}

### Deprecated
- {deprecation_description}

### Removed
- {removal_description}

### Fixed
- {bug_fix_description}

### Security
- {security_fix_description}

## [{version}] - {YYYY-MM-DD}

### Added
- {new_feature_description_1}
- {new_feature_description_2}
- {new_feature_description_3}

### Changed
- {change_description_1}
- {change_description_2}
- {change_description_3}

### Deprecated
- {deprecation_description_1}
- {deprecation_description_2}

### Removed
- {removal_description_1}
- {removal_description_2}

### Fixed
- {bug_fix_description_1}
- {bug_fix_description_2}
- {bug_fix_description_3}

### Security
- {security_fix_description_1}
- {security_fix_description_2}

## [{version}] - {YYYY-MM-DD}

### Added
- {new_feature_description_1}
- {new_feature_description_2}

### Changed
- {change_description_1}
- {change_description_2}

### Fixed
- {bug_fix_description_1}
- {bug_fix_description_2}

## [{version}] - {YYYY-MM-DD}

### Added
- {new_feature_description_1}
- {new_feature_description_2}

### Fixed
- {bug_fix_description_1}
- {bug_fix_description_2}

### Security
- {security_fix_description_1}

## [{version}] - {YYYY-MM-DD}

### Added
- Initial release
- {feature_1}
- {feature_2}
- {feature_3}

---

## Version Guidelines

### Semantic Versioning Format
```
MAJOR.MINOR.PATCH
```

**MAJOR** version when you make incompatible API changes
**MINOR** version when you add functionality in a backwards compatible manner
**PATCH** version when you make backwards compatible bug fixes

### Change Categories

#### Added
New features or functionality added to the project.

**Examples:**
- New API endpoints
- New configuration options
- New command-line flags
- New documentation sections

#### Changed
Changes to existing functionality that don't break backwards compatibility.

**Examples:**
- Updated dependencies
- Performance improvements
- Refactored internal code
- Enhanced error messages

#### Deprecated
Features that are still available but planned for removal in future versions.

**Examples:**
- Deprecated API endpoints (with migration path)
- Deprecated configuration options
- Deprecated command-line flags

**Format:**
```
- `{feature_name}` is deprecated and will be removed in v{version}. Use `{replacement}` instead.
```

#### Removed
Features or functionality removed from the project.

**Examples:**
- Removed deprecated features
- Removed unsupported platforms
- Removed obsolete dependencies

**Note:** Removals typically result in a MAJOR version bump.

#### Fixed
Bug fixes and patches.

**Examples:**
- Fixed memory leaks
- Fixed race conditions
- Fixed incorrect calculations
- Fixed documentation errors

#### Security
Security fixes and vulnerability patches.

**Examples:**
- Fixed security vulnerabilities (with CVE numbers if applicable)
- Updated dependencies with security patches
- Enhanced authentication/authorization

**Format:**
```
- Fixed {vulnerability_type} vulnerability in {component} (CVE-{number})
```

### Best Practices

1. **Keep the unreleased section at the top** - Makes it easy to add new changes
2. **Use present tense** - "Add feature" not "Added feature" in descriptions
3. **Link to issues/PRs** - Reference GitHub issues or pull requests where applicable
4. **Group by type first, then by area** - Makes scanning easier
5. **Be concise but descriptive** - Balance brevity with clarity
6. **Include breaking changes prominently** - Call out API changes
7. **Date format: YYYY-MM-DD** - ISO 8601 standard
8. **Add links at bottom** - Link versions to release tags or compare views

### Linking Format

Add comparison links at the bottom of the file:

```markdown
[Unreleased]: https://github.com/{org}/{repo}/compare/v{latest}...HEAD
[{version}]: https://github.com/{org}/{repo}/compare/v{previous}...v{version}
[{previous}]: https://github.com/{org}/{repo}/releases/tag/v{previous}
```

### Example Entry

```markdown
## [2.1.0] - 2025-01-15

### Added
- New `/api/v2/users` endpoint for user management (#123)
- Support for PostgreSQL 15 (#145)
- Configuration option `cache.ttl` for custom cache expiration (#156)

### Changed
- Updated Express.js from v4.17 to v4.18 (#134)
- Improved error messages for validation failures (#142)
- Refactored database connection pooling for better performance (#151)

### Deprecated
- `/api/v1/users` endpoint is deprecated and will be removed in v3.0. Use `/api/v2/users` instead. (#123)

### Fixed
- Fixed memory leak in WebSocket connections (#138)
- Fixed race condition in concurrent request handling (#147)
- Fixed incorrect timestamp formatting in logs (#149)

### Security
- Fixed SQL injection vulnerability in search endpoint (CVE-2025-1234) (#140)
- Updated jsonwebtoken to v9.0.0 to address security advisory (#143)
```

---

[Unreleased]: https://github.com/{org}/{repo}/compare/v{latest}...HEAD
[{version}]: https://github.com/{org}/{repo}/compare/v{previous}...v{version}
[{previous}]: https://github.com/{org}/{repo}/releases/tag/v{previous}
