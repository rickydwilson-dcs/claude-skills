# How to Use the Technical Writer Skill

## Quick Start

Hey Claude—I just added the "technical-writer" skill. Can you audit our documentation quality and identify improvements we need to make before the next release?

## Example Invocations

### Example 1: Documentation Quality Audit
```
Hey Claude—I just added the "technical-writer" skill. Can you run a comprehensive documentation audit and tell me what needs to be fixed before our v2.0 release?
```

**What Claude will do:**
- Run doc_quality_analyzer.py on your documentation
- Check readability, completeness, link health, and style consistency
- Identify critical issues (broken links, missing content)
- Provide prioritized recommendations
- Generate quality score and improvement metrics

### Example 2: README Generation
```
Hey Claude—I just added the "technical-writer" skill. Can you generate a comprehensive README for this project? We need installation instructions, usage examples, and API documentation.
```

**What Claude will do:**
- Discover project structure and tech stack
- Extract dependencies from package files
- Generate installation instructions
- Create usage examples from code
- Add API reference sections
- Format with badges and proper sections

### Example 3: CHANGELOG Maintenance
```
Hey Claude—I just added the "technical-writer" skill. Can you update our CHANGELOG with all commits since v1.5.0 and prepare it for the v2.0.0 release?
```

**What Claude will do:**
- Parse git commits since v1.5.0
- Group commits by type (feat, fix, docs, breaking)
- Generate Keep a Changelog format
- Add links to commits and PRs
- Create release section for v2.0.0
- Highlight breaking changes

### Example 4: API Documentation Creation
```
Hey Claude—I just added the "technical-writer" skill. Can you generate comprehensive API documentation from our OpenAPI spec and ensure it follows best practices?
```

**What Claude will do:**
- Parse OpenAPI specification
- Generate endpoint documentation
- Create request/response examples
- Document authentication requirements
- Format error codes and descriptions
- Validate documentation completeness

### Example 5: Pre-Release Documentation Review
```
Hey Claude—I just added the "technical-writer" skill. Can you perform a complete pre-release documentation review? We're launching v2.0 next week and need everything to be perfect.
```

**What Claude will do:**
- Run full documentation audit (quality analyzer)
- Update README with current project state
- Finalize CHANGELOG for release
- Validate all API documentation
- Check for broken links and outdated content
- Generate comprehensive review report
- Provide actionable improvement list

### Example 6: Documentation Standards Enforcement
```
Hey Claude—I just added the "technical-writer" skill. Can you help standardize documentation across our microservices? We need consistent README files, CHANGELOGs, and API docs for all 8 services.
```

**What Claude will do:**
- Analyze existing documentation across services
- Identify inconsistencies in format and style
- Generate standardized templates
- Update documentation to follow standards
- Create style guide for team
- Validate consistency across all services

## What to Provide

When using this skill, provide:

### For Quality Audits
- **Documentation Directory**: Path to docs folder or specific files
- **Audit Scope** (optional): Which types to check (readme, api, guides, tutorials)
- **Quality Baseline** (optional): Previous quality report for comparison
- **Target Score** (optional): Minimum acceptable quality score

### For README Generation
- **Project Directory**: Root directory of project
- **Template Preference** (optional): minimal, standard, or comprehensive
- **Custom Sections** (optional): Specific sections you want included
- **Preserve Content** (optional): Custom sections to keep unchanged

### For CHANGELOG Updates
- **Version Range** (optional): Which commits to include (e.g., since v1.5.0)
- **Release Version** (optional): Version number for release preparation
- **Manual Entries** (optional): Additional entries not from commits
- **Breaking Changes** (optional): Breaking changes to highlight

### For API Documentation
- **API Specification** (optional): OpenAPI/Swagger spec file
- **Source Directory** (optional): Code directory to scan for annotations
- **Documentation Format** (optional): Markdown, HTML, or JSON output
- **Validation Rules** (optional): Custom validation criteria

## What You'll Get

This skill will provide:

### Documentation Analysis
- **Quality Score**: Overall score (0-100) with category breakdown
- **Readability Metrics**: Grade level, complexity, sentence length
- **Completeness Report**: Missing sections, examples, required content
- **Link Health**: Broken links, redirects, external link validation
- **Style Issues**: Terminology inconsistencies, formatting problems
- **Actionable Recommendations**: Prioritized list of improvements

### README Files
- **Structured README**: Professional format with all standard sections
- **Auto-Generated Content**: Installation, usage, examples from code
- **Project Badges**: Build status, version, license shields
- **Consistent Formatting**: Matches style guide standards
- **Working Examples**: Tested code snippets and commands

### CHANGELOG Updates
- **Formatted Entries**: Keep a Changelog format
- **Grouped Commits**: Organized by type (feat, fix, docs, breaking)
- **Linked References**: Links to commits, PRs, issues
- **Release Sections**: Prepared release documentation
- **Breaking Changes**: Highlighted with migration guidance

### API Documentation
- **Endpoint Documentation**: Complete API reference
- **Request/Response Examples**: Working code examples
- **Authentication Guides**: How to authenticate and authorize
- **Error Documentation**: All error codes and handling
- **Consistent Format**: Standard structure across all endpoints

### Automated Tools
4 Python scripts for data processing and analysis:
- **doc_quality_analyzer.py**: Documentation quality assessment
- **readme_generator.py**: Automated README creation/updates
- **changelog_manager.py**: Git-synchronized changelog maintenance
- **api_doc_formatter.py**: API documentation formatting and validation

## Python Tools Available

This skill includes the following Python tools:

### 1. Documentation Quality Analyzer
**Purpose:** Comprehensive documentation quality assessment

```bash
python skills/engineering-team/technical-writer/scripts/doc_quality_analyzer.py --help

# Basic usage
python skills/engineering-team/technical-writer/scripts/doc_quality_analyzer.py ./docs

# JSON output for CI/CD
python skills/engineering-team/technical-writer/scripts/doc_quality_analyzer.py ./docs --format json
```

**Features:**
- Quality scoring (0-100 scale)
- Readability analysis
- Link validation
- Completeness checks
- Style consistency

### 2. README Generator
**Purpose:** Automated README creation and updates

```bash
python skills/engineering-team/technical-writer/scripts/readme_generator.py --help

# Generate comprehensive README
python skills/engineering-team/technical-writer/scripts/readme_generator.py . --template comprehensive

# Update existing README
python skills/engineering-team/technical-writer/scripts/readme_generator.py . --update
```

**Features:**
- Template-based generation
- Project discovery
- Dependency extraction
- Example generation
- Badge creation

### 3. CHANGELOG Manager
**Purpose:** Git-synchronized changelog maintenance

```bash
python skills/engineering-team/technical-writer/scripts/changelog_manager.py --help

# Sync with git commits
python skills/engineering-team/technical-writer/scripts/changelog_manager.py --sync-git

# Prepare for release
python skills/engineering-team/technical-writer/scripts/changelog_manager.py --prepare-release v2.0.0
```

**Features:**
- Git commit parsing
- Conventional commit support
- Keep a Changelog format
- Release preparation
- Breaking change highlighting

### 4. API Documentation Formatter
**Purpose:** Consistent API documentation formatting

```bash
python skills/engineering-team/technical-writer/scripts/api_doc_formatter.py --help

# Generate from OpenAPI spec
python skills/engineering-team/technical-writer/scripts/api_doc_formatter.py openapi.yaml --output docs/api.md

# Validate existing docs
python skills/engineering-team/technical-writer/scripts/api_doc_formatter.py docs/api.md --validate
```

**Features:**
- OpenAPI parsing
- Code annotation scanning
- Format validation
- Example generation
- Consistency checking

## Tips for Best Results

### 1. Regular Documentation Audits
Run quality analyzer weekly to catch issues early:
```bash
# Weekly documentation health check
python skills/engineering-team/technical-writer/scripts/doc_quality_analyzer.py . --verbose
```
**Benefit:** Prevents documentation drift and maintains quality

### 2. Automate in CI/CD
Add documentation quality gates to your pipeline:
```yaml
# Fail builds if documentation quality drops below 80
python scripts/doc_quality_analyzer.py . --format json --min-score 80
```
**Benefit:** Enforces documentation standards automatically

### 3. Use Templates Consistently
Stick to comprehensive template for all projects:
```bash
# Standardize README across all projects
python scripts/readme_generator.py . --template comprehensive
```
**Benefit:** Consistency makes onboarding faster

### 4. Keep CHANGELOG Current
Sync changelog after each merge to main:
```bash
# Update CHANGELOG after merging PRs
python scripts/changelog_manager.py --sync-git --since last-release
```
**Benefit:** Never scramble to write release notes

### 5. Validate Before Releases
Run full documentation review before every release:
```bash
# Pre-release checklist
python scripts/doc_quality_analyzer.py . --verbose
python scripts/readme_generator.py . --update
python scripts/changelog_manager.py --prepare-release v2.0.0
python scripts/api_doc_formatter.py docs/api.md --validate
```
**Benefit:** Professional documentation for every release

### 6. Combine with Code Reviews
Use technical-writer skill alongside code-reviewer:
```bash
# First: code review
python skills/engineering-team/code-reviewer/scripts/pr_analyzer.py 123

# Then: documentation review
python skills/engineering-team/technical-writer/scripts/doc_quality_analyzer.py docs/
```
**Benefit:** Ensure both code and docs meet quality standards

### 7. Leverage Reference Documentation
Consult reference docs for complex questions:
- **Documentation Standards** - Quality criteria and organization
- **Writing Style Guide** - Voice, tone, terminology conventions
- **API Best Practices** - API-specific documentation guidance

### 8. Target Appropriate Readability
Match documentation complexity to audience:
- **Internal docs**: Grade level 10-12 (technical team)
- **User guides**: Grade level 8-10 (general developers)
- **Public APIs**: Grade level 6-8 (broad audience)

### 9. Fix Broken Links Immediately
Links rot quickly - prioritize link health:
```bash
# Validate links in all documentation
python scripts/doc_quality_analyzer.py . --check-links
```
**Benefit:** Professional appearance and better user experience

### 10. Preserve Custom Content
When updating, preserve custom sections:
```bash
# Update README without losing custom content
python scripts/readme_generator.py . --update --preserve-custom
```
**Benefit:** Automation without losing manual improvements

## Related Skills

Consider using these skills together:

### Complementary Skills

**[Code Reviewer](../../engineering-team/code-reviewer/)**
- Use for: Code quality analysis before documentation
- Integration: Identify code changes requiring doc updates
- Workflow: Code review → Documentation updates

**[Senior DevOps](../../engineering-team/senior-devops/)**
- Use for: CI/CD pipeline integration
- Integration: Automated documentation quality gates
- Workflow: Pipeline setup → Documentation automation

**[Senior Fullstack](../../engineering-team/senior-fullstack/)**
- Use for: API implementation and documentation
- Integration: API code → Documentation generation
- Workflow: Implement API → Document API

### Slash Commands

**[/update.docs](../../../commands/workflow/update.docs.md)**
- Automates README, CHANGELOG, and catalog updates
- Uses technical-writer tools under the hood
- Run after creating agents or skills

**[/review.code](../../../commands/analysis/review.code.md)**
- Reviews code quality including documentation
- Identifies missing or outdated docs
- Run before documentation audits

**[/create.pr](../../../commands/git/create.pr.md)**
- Creates pull requests with documentation changes
- Ensures documentation commits follow standards
- Run after documentation updates

---

**Skill**: technical-writer
**Domain**: engineering-team
**Version**: 1.0.0
**Last Updated**: 2025-11-28
**Time Savings**: 50%+ on documentation tasks
**Quality Improvement**: 30%+ in consistency and completeness
