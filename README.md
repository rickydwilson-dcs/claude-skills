# Claude Skills Library - Pandora Edition

**Production-Ready Skills for Pandora's Software Delivery Lifecycle**

A comprehensive library of reusable skill packages that accelerate Pandora's SDLC workflows through expert knowledge, automated analysis tools, and proven frameworks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude AI](https://img.shields.io/badge/Claude-AI-blue.svg)](https://claude.ai)
[![Claude Code](https://img.shields.io/badge/Claude-Code-purple.svg)](https://claude.ai/code)

---

## Purpose: Accelerating Pandora's SDLC

This library exists to help **Pandora's software development teams deliver value faster** by providing:

### Architecture & Security Excellence
- **Architecture analysis tools** - Instantly review Pandora's codebase structure, patterns, and dependencies
- **Security automation** - Automated OWASP vulnerability scanning and secrets detection for Pandora's applications
- **Technical debt tracking** - Identify and prioritize technical improvements across Pandora's systems

### Product & Delivery Velocity
- **Product prioritization frameworks** - Data-driven feature prioritization using RICE methodology for Pandora's roadmap
- **Sprint planning tools** - User story generation and velocity tracking for Pandora's agile teams
- **Atlassian integration** - Streamlined Jira/Confluence workflows for Pandora's delivery processes

### Engineering Best Practices
- **Engineering standards** - Proven patterns for fullstack, backend, DevOps, and AI/ML development aligned with Pandora's tech stack
- **Code quality automation** - Automated reviews and testing frameworks for Pandora's codebases
- **CI/CD optimization** - Pipeline improvements and deployment automation for Pandora's infrastructure

**The Goal:** Enable Pandora's entire development organization to adopt these skills into their day-to-day workflow, accelerating delivery of technical change and business value across all product teams.

> Originally created by [Ali Rezvani](https://github.com/alirezarezvani/claude-skills). This Pandora edition extends the original vision with specific focus on Pandora's software delivery lifecycle and team productivity needs.

---

## 🎯 Overview

This repository provides **modular, self-contained skill packages** specifically designed for Pandora's software delivery teams. Each skill augments Claude AI with specialized domain expertise and includes:

- **📖 Comprehensive documentation** - Workflows, best practices, and strategic frameworks tailored to Pandora's SDLC
- **🛠️ Python analysis tools** - 92 CLI utilities for automated architecture, security, and product analysis
- **📚 Knowledge bases** - Curated reference materials covering architecture patterns, security practices, and product frameworks
- **📋 Ready-to-use templates** - ADRs, C4 diagrams, PRDs, user stories, and sprint templates

**Key Benefits for Pandora:**
- ⚡ **Zero dependencies** - Python 3.8+ standard library only, works across Pandora's environments
- 🎯 **SDLC-optimized** - 34 skills, 34 agents, 16 slash commands covering architecture, security, product management, engineering, delivery
- 🔧 **Fast analysis** - Algorithmic tools without external API dependencies or rate limits
- 📈 **Measurable impact** - 40%+ time savings, 30%+ quality improvements, faster delivery cycles
- 👥 **Team adoption ready** - Designed for Pandora's entire development organization to use daily

---

## 📚 What's Inside

### Skills & Agents

- **[Skills Catalog](docs/SKILLS_CATALOG.md)** - 34 production-ready skills with Python CLI tools
  - **Marketing Skills (3)** - Content creation, demand generation, product marketing
  - **Product Skills (7)** - Product management, agile practices, UX research, UI design, business analysis, competitive analysis
  - **Engineering Skills (19)** - Architecture, security, fullstack, DevOps, AI/ML, data, QA, technical writing, mobile (React Native, Flutter, iOS)
  - **Delivery Skills (5)** - Jira, Confluence, Scrum, project management

- **[Agents Catalog](docs/AGENTS_CATALOG.md)** - 34 workflow orchestrator agents (v2.0)
  - Agents guide multi-step processes and intelligently invoke skills
  - Complete coverage for marketing, product, engineering, and delivery domains

### Builder Tools

- **[Agent Builder](scripts/agent_builder.py)** - Create agents in 1 hour instead of 2 days (96% faster)
  - Interactive + config modes, 9 validation checks, dynamic domain creation
- **[Skill Builder](scripts/skill_builder.py)** - Create skills in 2 hours instead of 3 days (93% faster)
  - Full scaffolding, placeholder generation, extended metadata
- **[Skill Upgrader](scripts/upgrade_skills_to_new_standards.py)** - Batch upgrade existing skills
  - Automated fixes: chmod +x, directories, metadata, missing sections

### Documentation

**Getting Started**
- **[Quick Start Guide](docs/QUICK_START.md)** - Get started in 5 minutes
- **[Installation Guide](docs/INSTALL.md)** - Complete setup instructions (Python 3.8+ only, no dependencies)
- **[Usage Guide](docs/USAGE.md)** - Comprehensive examples and workflows

**User Guides**
- **[Understanding Skills](docs/guides/understanding-skills.md)** - What skills are and how they work
- **[Using Skills](docs/guides/using-skills.md)** - Practical workflows with time savings
- **[Skill-to-Agent Flow](docs/guides/skill-to-agent-flow.md)** - How skills and agents connect

**Testing & Standards**
- **[Testing Guide](docs/testing/TESTING_GUIDE.md)** - Python script testing framework
- **[Standards Library](docs/standards/)** - Communication, quality, git, documentation, security standards
- **[Git Workflow](docs/WORKFLOW.md)** - Branch strategy and deployment pipeline

---

## ⚡ Quick Start

### Option 1: Claude AI (Upload & Reference)

```markdown
I need to review the architecture of this microservices application.

Please use the Senior Architect skill:
File: skills/engineering-team/senior-architect/SKILL.md

Analyze the architecture, identify patterns, and recommend improvements.
```

### Option 2: Claude Code (Agent Workflows)

```markdown
@cs-architect

Review the architecture of this codebase before our major release.
Focus on:
- Microservices patterns and service boundaries
- Dependency analysis and circular dependencies
- Scalability for 10x user growth
```

### Option 3: CLI Tools (Direct Execution)

```bash
# Architecture analysis
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --verbose

# Security audit
python3 skills/engineering-team/senior-security/scripts/security_auditor.py \
  --input . --output text --verbose

# Feature prioritization
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  features.csv --capacity 20
```

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** (for CLI tools)
- **Git** (for cloning repository)

### Quick Install

```bash
# Clone repository
git clone https://github.com/rickydwilson-dcs/claude-skills.git
cd claude-skills

# Verify Python (no dependencies needed!)
python3 --version  # Should be 3.8 or higher

# Test a tool
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --help
```

**That's it!** All Python tools use standard library only - no pip install required.

See [Installation Guide](docs/INSTALL.md) for detailed setup instructions.

---

## 📖 Usage Examples

### Example 1: Architecture Review (15 minutes, saves 3.75 hours)

```bash
# Run architecture analyzer
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --verbose > architecture-report.md

# Review findings: architecture score, patterns, issues, recommendations

# Create ADR for key decisions
cp skills/engineering-team/senior-architect/assets/adr-template.md \
  docs/architecture/ADR-001-microservices.md
```

### Example 2: Security Audit (10 minutes, saves 2.75 hours)

```bash
# Run security auditor
python3 skills/engineering-team/senior-security/scripts/security_auditor.py \
  --input src/auth --output text --verbose > security-audit.md

# Review: OWASP Top 10 issues, exposed secrets, weak cryptography

# Fix critical issues based on recommendations
```

### Example 3: Feature Prioritization (15 minutes, saves 3.5 hours)

```bash
# Create features CSV
cat > features.csv << 'EOF'
feature,reach,impact,confidence,effort
SSO Integration,1000,3,0.9,8
Dark Mode,500,1,1.0,2
Mobile App,2000,3,0.7,13
EOF

# Run RICE prioritizer
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  features.csv --capacity 20 > priorities.md

# Review: RICE scores, Quick Wins vs Big Bets, roadmap recommendations
```

### Example 4: User Story Generation (10 minutes, saves 1.75 hours)

```markdown
In Claude Code:

@cs-agile-product-owner

Generate user stories for our authentication feature:
- Epic: User Authentication System
- Sprint capacity: 30 story points
- Must include: Login, signup, password reset, 2FA

Output: 8-10 user stories with acceptance criteria and story point estimates
```

See [Usage Guide](docs/USAGE.md) for comprehensive examples and patterns.

---

## 🛠️ Production CLI Tools

**92 standardized Python CLI tools** with comprehensive testing framework:

### CLI Features
- **Consistent Interface** - All tools use `--help`, `--version`, `--output`, `--file`, `--verbose`
- **Multiple Formats** - Text (human-readable), JSON (machine-readable), CSV (spreadsheet)
- **Error Handling** - Standardized exit codes and UTF-8 encoding
- **Zero Dependencies** - Python 3.8+ standard library only

### Testing
- **2,814 automated tests** - Comprehensive test coverage (via pytest)
- **Sample Data** - 24 sample input files for immediate testing
- See [Testing Guide](docs/testing/TESTING_GUIDE.md) for details

---

## 🤖 Builder Tools (Automated Creation)

**Reduce development time by 93-96%** with zero-dependency builder tools for creating and validating agents and skills.

### Agent Builder

Create production-ready cs-* agents in **1 hour instead of 2 days** (96% faster):

```bash
# Interactive mode - guided workflow
python3 scripts/agent_builder.py

# Validate existing agent
python3 scripts/agent_builder.py --validate agents/marketing/cs-content-creator.md
```

**Features**: 9 validation checks, dynamic domain creation, template-based generation, zero dependencies

### Skill Builder

Create complete skill packages in **2 hours instead of 3 days** (93% faster):

```bash
# Interactive mode - 8-step workflow
python3 scripts/skill_builder.py

# Validate existing skill
python3 scripts/skill_builder.py --validate skills/marketing-team/content-creator
```

**Features**: Full directory scaffolding, placeholder generation, extended metadata YAML, executable tools

### Validation Results

- **34/34 agents passing** (100% validation rate)
- **34/34 skills passing** (100% validation rate)
- Zero external dependencies
- Average validation time: < 2 seconds

See [CLAUDE.md](CLAUDE.md#builder-tools-automated-creation--validation) for complete builder documentation.

---

## 🏗️ Skill Architecture

Each skill follows a consistent structure:

```
skill-name/
├── SKILL.md              # Master documentation with workflows
├── scripts/              # Python CLI tools (zero dependencies)
├── references/           # Expert knowledge bases (markdown)
└── assets/               # Templates (ADRs, PRDs, diagrams)
```

**Design Principles:**
- ✅ **Self-contained** - Each skill is independently deployable
- ✅ **Algorithmic** - Fast deterministic analysis without ML/LLM calls
- ✅ **Platform-specific** - Specific frameworks over generic advice
- ✅ **Template-heavy** - Ready-to-use templates for common deliverables

See [Skill Architecture](docs/guides/understanding-skills.md) for detailed explanation.

---

## 🤝 Contributing

Contributions to improve Pandora's skills library are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- How to contribute new skills or improvements
- Quality standards and architecture guidelines
- Submission process and review criteria

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for full text.

Copyright (c) 2024 Alireza Rezvani (original author)
Copyright (c) 2025 Pandora Digital Consulting Services (Pandora Edition)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

---

## 👤 Attribution

This repository is a fork of [Claude Skills Library](https://github.com/alirezarezvani/claude-skills) by **[Ali Rezvani](https://github.com/alirezarezvani)**.

**Original Author:** Ali Rezvani ([@alirezarezvani](https://github.com/alirezarezvani))
**Pandora Fork Maintainer:** Ricky Wilson ([@rickydwilson-dcs](https://github.com/rickydwilson-dcs))

**Key Differences in Pandora Edition:**
- Focus on Pandora's SDLC (architecture, security, product management, delivery)
- 34 skills covering software delivery lifecycle (vs original marketing focus)
- 92 Python CLI tools for automated analysis
- 34 workflow orchestrator agents (v2.0)
- Comprehensive testing framework (2,814 tests)
- Zero dependencies (Python 3.8+ standard library only)

**Thank you to Ali Rezvani** for creating the original framework and vision that made this possible.

---

## 🙏 Acknowledgments

Special thanks to:
- **Ali Rezvani** - Original Claude Skills Library creator and framework designer
- **Anthropic** - Claude AI and Claude Code platform
- **Pandora Development Teams** - Feedback and real-world validation
- **Open Source Community** - Contributions and improvements

---

## 📞 Support & Feedback

- **Questions:** [GitHub Discussions](https://github.com/rickydwilson-dcs/claude-skills/discussions)
- **Bug Reports:** [GitHub Issues](https://github.com/rickydwilson-dcs/claude-skills/issues)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Version:** 1.0.0 (Pandora Edition)
**Last Updated:** December 14, 2025
**Status:** 34 production skills, 34 agents, 16 slash commands, 92 CLI tools
**Compatibility:** Claude AI, Claude Code, Python 3.8+
