# Developer Documentation Guide

## README Framework

### 1. The 5-Second Rule

Within 5 seconds of landing on your README, developers should know:
1. **What** is this project?
2. **Why** should I care?
3. **How** do I get started?

**Example opening:**
```markdown
# Project Name

A fast, lightweight JavaScript validation library with zero dependencies.

Validate forms, API requests, and user input with simple, chainable rules. 10x faster than competitors, 5 KB minified.

```bash
npm install project-name
```
```

### 2. Pyramid Structure

Organize content from most to least important. Front-load critical information.

**Priority order:**
1. Project name and one-line description
2. Key features (3-5 bullets)
3. Quick start code example
4. Installation instructions
5. Basic usage
6. Documentation links
7. Contributing guidelines
8. License

### 3. README Template

```markdown
# Project Name

[![Build Status](https://img.shields.io/github/workflow/status/user/repo/CI)](link)
[![npm version](https://img.shields.io/npm/v/package)](link)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

One-sentence description of what this project does.

## Features

- Feature 1 with clear benefit
- Feature 2 with clear benefit
- Feature 3 with clear benefit

## Quick Start

```javascript
// Show the simplest possible usage
const example = require('project-name');
const result = example.doSomething();
```

## Installation

```bash
npm install project-name
```

**Requirements:**
- Node.js 18 or higher
- npm 9 or higher

## Usage

### Basic Example

```javascript
// Complete, runnable example
const Project = require('project-name');

const instance = new Project({
  option1: 'value1',
  option2: 'value2'
});

const result = instance.process();
console.log(result);
```

### Advanced Usage

See the [full documentation](https://docs.example.com) for advanced features.

## Documentation

- [API Reference](https://docs.example.com/api)
- [Tutorials](https://docs.example.com/tutorials)
- [Examples](./examples)

## Contributing

Contributions welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

## License

[MIT](LICENSE) © [Author Name](https://github.com/author)

## Support

- [Documentation](https://docs.example.com)
- [Issue Tracker](https://github.com/user/repo/issues)
- [Discord Community](https://discord.gg/example)
```

### 4. Badge Guidelines

**Essential badges (use sparingly):**
- Build status (CI/CD)
- Version number
- License
- Code coverage (if >80%)

**Avoid badge overload:**
- Maximum 5-6 badges
- Only include meaningful signals
- Keep them at the top, before description

**Badge services:**
- [Shields.io](https://shields.io) - Custom badges
- GitHub Actions badges - Build status
- npm badges - Package version

### 5. Visual Elements

**When to include:**
- Screenshots for UI tools or libraries
- Architecture diagrams for complex systems
- GIFs for demonstrating interactive features
- Logo (if project has branding)

**Best practices:**
- Keep images under 500 KB
- Use relative paths: `![Screenshot](./docs/screenshot.png)`
- Provide alt text for accessibility
- Show real usage, not marketing fluff

### 6. Code Examples in README

**Rules for README examples:**
- Must be complete and runnable
- Show the most common use case first
- Keep examples under 20 lines
- Link to more examples in `/examples` directory

**Example structure:**
```markdown
## Usage

### Basic Example
[Simple, common case - 10 lines max]

### Advanced Example
[More complex scenario - 20 lines max]

### More Examples
See the [examples directory](./examples) for:
- [Authentication](./examples/auth.js)
- [Error handling](./examples/errors.js)
- [Custom configuration](./examples/config.js)
```

## CHANGELOG Best Practices

### 1. Keep a Changelog Format

Follow [keepachangelog.com](https://keepachangelog.com) standard.

**Template:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features that have been added

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Features that have been removed

### Fixed
- Bug fixes

### Security
- Security vulnerability fixes

## [1.2.0] - 2025-11-28

### Added
- New `validate()` method for input validation
- Support for custom error messages
- TypeScript type definitions

### Changed
- Improved performance of `parse()` method by 40%
- Updated dependencies to latest versions

### Fixed
- Fixed memory leak in event listeners
- Corrected timezone handling in date parsing

## [1.1.0] - 2025-10-15

### Added
- Initial release of validation system

## [1.0.0] - 2025-09-01

### Added
- Core functionality
- Basic documentation
- Test suite

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

### 2. Change Categories

Use these standard categories consistently:

**Added** - New features
- New API endpoints
- New configuration options
- New commands or tools

**Changed** - Modifications to existing features
- Updated behavior
- Performance improvements
- Dependency updates

**Deprecated** - Features marked for future removal
- Include removal timeline
- Suggest alternatives
- Update migration guide

**Removed** - Deleted features
- List removed functionality
- Explain why removed
- Link to migration guide if needed

**Fixed** - Bug fixes
- Describe the bug
- Include issue number: "Fixed #123"
- Note user impact

**Security** - Security patches
- Describe vulnerability (without details that enable exploits)
- Include CVE if applicable
- Recommend immediate upgrade

### 3. Writing Change Entries

**Good change entry format:**
```markdown
### Added
- New `authenticate()` method with OAuth 2.0 support (#145)
- CLI flag `--verbose` for detailed logging (#156)
```

**Best practices:**
- Start with verb (past tense): Added, Fixed, Changed
- Be specific: "Fixed memory leak in event listeners" not "Fixed bug"
- Include issue/PR numbers: (#123)
- Group related changes
- Order by importance within category

**Avoid:**
- Vague descriptions: "Various improvements"
- Developer jargon: "Refactored internal helpers"
- Implementation details: "Changed loop to map function"
- Obvious changes: "Updated version number"

### 4. Semantic Versioning

Follow [semver.org](https://semver.org) for version numbers: MAJOR.MINOR.PATCH

**MAJOR version (X.0.0):** Breaking changes
- Removed features
- Changed API signatures
- Incompatible changes

**MINOR version (0.X.0):** New features (backward-compatible)
- New functionality
- New optional parameters
- New methods/endpoints

**PATCH version (0.0.X):** Bug fixes (backward-compatible)
- Bug fixes
- Security patches
- Documentation updates

**Examples:**
- `1.0.0` → `2.0.0`: Breaking change (renamed method)
- `1.2.0` → `1.3.0`: New feature (added method)
- `1.2.3` → `1.2.4`: Bug fix (fixed validation)

## Getting Started Guide

### 1. Time-to-First-Success

Optimize for the fastest path to a working example.

**Goal:** Developer sees success within 5 minutes.

**Pattern:**
1. **Prerequisites check** (30 seconds)
2. **Installation** (1 minute)
3. **First working example** (2 minutes)
4. **Verification** (1 minute)
5. **Next steps** (links)

### 2. Getting Started Template

```markdown
# Getting Started

This guide will get you up and running with Project Name in 5 minutes.

## Prerequisites

Before you begin, ensure you have:
- Node.js 18 or higher ([Download](https://nodejs.org))
- npm 9 or higher (comes with Node.js)
- A text editor
- Basic JavaScript knowledge

**Check your versions:**
```bash
node --version  # Should show v18.0.0 or higher
npm --version   # Should show 9.0.0 or higher
```

## Step 1: Install

Install the package via npm:

```bash
npm install project-name
```

## Step 2: Create Your First Script

Create a new file `hello.js`:

```javascript
const Project = require('project-name');

// Initialize
const app = new Project();

// Use it
const result = app.greet('World');
console.log(result);
```

## Step 3: Run It

Execute your script:

```bash
node hello.js
```

**You should see:**
```
Hello, World!
```

## Success!

You've successfully installed and used Project Name.

## Next Steps

Now that you're set up, explore these topics:
- [Basic Usage](./docs/usage.md) - Learn core features
- [Configuration](./docs/config.md) - Customize behavior
- [Examples](./examples) - See more examples
- [API Reference](./docs/api.md) - Full API documentation

## Troubleshooting

**Problem:** `Cannot find module 'project-name'`
**Solution:** Run `npm install project-name` in your project directory

**Problem:** `node: command not found`
**Solution:** Install Node.js from [nodejs.org](https://nodejs.org)

Need more help? [Open an issue](https://github.com/user/repo/issues)
```

### 3. Copy-Paste Commands

Make all commands copy-paste ready.

**Good examples:**
```bash
# Clone the repository
git clone https://github.com/user/repo.git
cd repo

# Install dependencies
npm install

# Run tests
npm test
```

**Best practices:**
- One command per line
- Include directory changes: `cd repo`
- Show expected output when helpful
- Use comments to explain each step
- Avoid placeholders when possible

**When placeholders are necessary:**
```bash
# Replace YOUR_API_KEY with your actual key
export API_KEY="YOUR_API_KEY"

# Or use a specific example format
export API_KEY="sk_live_abc123def456"
```

## Contributing Guide

### 1. CONTRIBUTING.md Template

```markdown
# Contributing to Project Name

Thank you for your interest in contributing! This document explains how to contribute to this project.

## Ways to Contribute

- Report bugs
- Suggest new features
- Improve documentation
- Submit code changes

## Before You Start

1. Check existing [issues](https://github.com/user/repo/issues) and [pull requests](https://github.com/user/repo/pulls)
2. For major changes, open an issue first to discuss
3. Read our [Code of Conduct](CODE_OF_CONDUCT.md)

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/repo.git
cd repo
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## Making Changes

### Code Style

- Follow existing code style
- Run linter: `npm run lint`
- Format code: `npm run format`

### Writing Tests

- Add tests for new features
- Ensure all tests pass: `npm test`
- Maintain >80% code coverage

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org):

```
feat: Add user authentication
fix: Correct timezone handling
docs: Update API reference
test: Add validation tests
```

## Submitting Changes

### 1. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 2. Create Pull Request

1. Go to the original repository
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill out the PR template
5. Submit

### Pull Request Guidelines

- Clear title describing the change
- Reference related issues: "Fixes #123"
- Include screenshots for UI changes
- Update documentation if needed
- Ensure CI checks pass

## Review Process

1. Maintainers review your PR
2. Address any feedback
3. Once approved, maintainers will merge

## Need Help?

- Join our [Discord](https://discord.gg/example)
- Open a [discussion](https://github.com/user/repo/discussions)
- Email: support@example.com

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
```

### 2. Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug Report
about: Report a bug to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Description
A clear description of the bug.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., macOS 14.0]
- Node.js version: [e.g., 18.17.0]
- Package version: [e.g., 1.2.0]

## Additional Context
Screenshots, logs, or other relevant information.
```

### 3. Pull Request Template

Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description
Brief description of the changes.

## Related Issue
Fixes #(issue number)

## Type of Change
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change (fix or feature that changes existing behavior)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran.

## Checklist
- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where needed
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
- [ ] Any dependent changes have been merged

## Screenshots (if applicable)
Add screenshots to help explain your changes.
```

### 4. Code of Conduct

Use a standard Code of Conduct like [Contributor Covenant](https://www.contributor-covenant.org/).

**Key sections:**
- Our pledge
- Standards for behavior
- Enforcement responsibilities
- Scope
- Reporting guidelines
- Consequences

## Architecture Decision Records (ADRs)

### 1. ADR Format

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need to choose a database for our application. The application requires:
- ACID transactions
- Complex queries with joins
- Strong consistency
- 10M+ records
- Multi-region support in future

## Decision
We will use PostgreSQL as our primary database.

## Consequences

### Positive
- Strong ACID guarantees
- Mature, well-tested database
- Excellent query optimizer
- Rich ecosystem of tools
- JSON support for flexible schema
- PostGIS for future geospatial features

### Negative
- More complex to scale horizontally than NoSQL
- Requires careful index management for performance
- Steeper learning curve for team members unfamiliar with SQL

### Neutral
- Need to set up backup strategy
- Requires monitoring and maintenance
- Need to plan for future sharding

## Alternatives Considered

### MongoDB
- Pros: Flexible schema, horizontal scaling
- Cons: Weaker consistency, less mature for complex queries
- Rejected: Our data is highly relational

### MySQL
- Pros: Similar features to PostgreSQL, widely used
- Cons: Less advanced features, weaker JSON support
- Rejected: PostgreSQL has better features for our use case

## References
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Team discussion](link-to-discussion)
```

### 2. When to Create ADRs

Create an ADR when deciding:
- Architecture patterns (microservices, monolith)
- Technology choices (frameworks, databases)
- Process changes (deployment strategy, testing approach)
- Breaking changes to public APIs
- Security or compliance decisions

**Don't create ADRs for:**
- Implementation details
- Routine bug fixes
- Minor refactoring
- Style preferences

### 3. ADR Naming Convention

**Format:** `ADR-{number}: {short-title}`

**Examples:**
- ADR-001: Use PostgreSQL for primary database
- ADR-002: Adopt REST over GraphQL
- ADR-003: Implement feature flags
- ADR-004: Choose JWT for authentication

**Storage:** `docs/adr/` directory

### 4. ADR Statuses

- **Proposed:** Under discussion
- **Accepted:** Decision made, implementation pending
- **Implemented:** Decision made and implemented
- **Deprecated:** No longer relevant
- **Superseded:** Replaced by another ADR (reference it)

## Error Message Writing

### 1. Four-Part Error Message Pattern

Every error message should tell users:
1. **What** went wrong
2. **Why** it went wrong
3. **How** to fix it
4. **Where** to get help

**Bad error:**
```
Error: Invalid input
```

**Good error:**
```
Error: Invalid email address

The email 'user@domain' is missing a top-level domain.

Please provide a valid email address like 'user@example.com'

For more help, see: https://docs.example.com/errors/invalid-email
```

### 2. Error Message Template

```
[ERROR_CODE] Brief description

Detailed explanation of what went wrong and why.

To fix this:
1. First action to try
2. Second action to try

For more information, see: [documentation link]
```

**Example:**
```
[AUTH_001] Authentication failed

The API key 'sk_test_abc...' is invalid or has been revoked.

To fix this:
1. Check that you're using the correct API key
2. Generate a new API key at https://dashboard.example.com/keys
3. Ensure the key has not expired (keys expire after 90 days)

For more information, see: https://docs.example.com/authentication
```

### 3. Error Code Design

**Format:** `[CATEGORY]_[NUMBER]`

**Categories:**
- AUTH - Authentication errors
- VAL - Validation errors
- NET - Network errors
- DB - Database errors
- SYS - System errors

**Examples:**
- AUTH_001: Invalid API key
- VAL_002: Missing required field
- NET_003: Connection timeout
- DB_004: Query failed
- SYS_005: Out of memory

### 4. Error Message Best Practices

**Do:**
- Use plain language, not technical jargon
- Be specific: "Port 3000 is already in use" not "Port unavailable"
- Provide actionable fixes
- Include error codes for support
- Link to documentation

**Don't:**
- Blame the user: "You entered invalid data"
- Use vague terms: "Something went wrong"
- Show stack traces to end users (log them instead)
- Use technical jargon: "ECONNREFUSED"
- Leave users stuck with no next step

## Release Notes

### 1. Release Notes Template

```markdown
# Release v1.2.0 - November 28, 2025

## Highlights

The biggest update since v1.0! This release focuses on performance improvements and developer experience.

**Key improvements:**
- 40% faster query performance
- New TypeScript definitions
- Improved error messages

## Breaking Changes

### Renamed Method
`getUserData()` has been renamed to `getUser()` for consistency.

**Migration:**
```javascript
// Before
const data = await api.getUserData(id);

// After
const data = await api.getUser(id);
```

### Changed Default Behavior
The `strict` option now defaults to `true` instead of `false`.

**Migration:** If you relied on lenient validation, explicitly set `strict: false`:
```javascript
const api = new API({ strict: false });
```

## New Features

### User Authentication
New built-in authentication support with OAuth 2.0.

```javascript
const api = new API({
  auth: {
    type: 'oauth2',
    clientId: 'your-client-id'
  }
});
```

See the [authentication guide](https://docs.example.com/auth) for details.

### TypeScript Support
Full TypeScript definitions included.

```typescript
import { API, User } from 'project-name';

const api = new API();
const user: User = await api.getUser('123');
```

## Improvements

- Improved query performance by 40% for large datasets
- Better error messages with actionable fixes
- Updated all dependencies to latest versions
- Reduced bundle size by 15% (45 KB → 38 KB minified)

## Bug Fixes

- Fixed memory leak in event listeners (#234)
- Corrected timezone handling in date parsing (#245)
- Fixed rare race condition in connection pooling (#256)

## Deprecations

The `timeout` option is deprecated. Use `requestTimeout` instead. The old option will be removed in v2.0.

```javascript
// Deprecated
new API({ timeout: 5000 });

// Use this instead
new API({ requestTimeout: 5000 });
```

## Documentation

- New [Getting Started guide](https://docs.example.com/getting-started)
- Updated [API reference](https://docs.example.com/api)
- Added 10 new [examples](https://github.com/user/repo/tree/main/examples)

## Upgrade Guide

### From v1.1.x

```bash
npm install project-name@1.2.0
```

Review the [migration guide](https://docs.example.com/migrations/v1.2) for breaking changes.

### From v1.0.x

We recommend upgrading to v1.1.0 first, then to v1.2.0.

## Contributors

Thank you to all contributors who made this release possible:
- @contributor1 - New authentication system
- @contributor2 - Performance improvements
- @contributor3 - TypeScript definitions

Full changelog: [v1.1.0...v1.2.0](https://github.com/user/repo/compare/v1.1.0...v1.2.0)
```

### 2. Release Note Sections

**Essential sections:**
- Version number and date
- Highlights (2-4 key points)
- Breaking changes with migration guide
- New features with examples
- Bug fixes
- Upgrade instructions

**Optional sections:**
- Deprecations
- Performance improvements
- Security fixes
- Documentation updates
- Contributors

### 3. Breaking Changes Communication

**Announce breaking changes:**
- In release notes (prominently)
- In CHANGELOG (with migration steps)
- On website/blog
- Via email (for major changes)
- In deprecation warnings (one version before removal)

**Migration guide format:**
```markdown
## Breaking Change: Method Renamed

`oldMethod()` → `newMethod()`

### Before (v1.x)
```javascript
api.oldMethod();
```

### After (v2.x)
```javascript
api.newMethod();
```

### Automated Migration
Run this codemod to update automatically:
```bash
npx project-codemod v2-method-rename
```
```

### 4. Version Highlights

**Craft compelling highlights:**
- Focus on user benefits, not implementation
- Use numbers: "40% faster", "50 new features"
- Be specific: "New authentication system" not "Improvements"
- Lead with most impactful change

**Good examples:**
- "10x faster query performance on large datasets"
- "New TypeScript definitions for better IDE support"
- "50+ bug fixes improve stability"

**Avoid:**
- "Various improvements"
- "Minor changes"
- "Refactored internals"

---

**Last Updated:** November 28, 2025
**Applies To:** GitHub repositories, open source projects, developer tools
**Related:** technical_writing_standards.md, api_documentation_patterns.md
