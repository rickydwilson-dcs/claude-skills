# Claude Skills Library - Pandora Edition

**Production-Ready Skills for Pandora's Software Delivery Lifecycle** - A comprehensive library of reusable skill packages that accelerate Pandora's SDLC workflows through expert knowledge, automated analysis tools, and proven frameworks.

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

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude AI](https://img.shields.io/badge/Claude-AI-blue.svg)](https://claude.ai)
[![Claude Code](https://img.shields.io/badge/Claude-Code-purple.svg)](https://claude.ai/code)

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Documentation](#-documentation)
- [Production CLI Tools & Testing](#%EF%B8%8F-production-cli-tools--testing)
- [Agent Catalog](#-agent-catalog)
- [Available Skills](#-available-skills)
- [Quick Start](#-quick-start)
- [How to Use with Claude AI](#-how-to-use-with-claude-ai)
- [How to Use with Claude Code](#-how-to-use-with-claude-code)
- [Skill Architecture](#-skill-architecture)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [Contributing](#-contributing)
- [License](#-license)
- [Attribution](#-attribution)

---

## 🎯 Overview

This repository provides **modular, self-contained skill packages** specifically designed for Pandora's software delivery teams. Each skill augments Claude AI with specialized domain expertise and includes:

- **📖 Comprehensive documentation** - Workflows, best practices, and strategic frameworks tailored to Pandora's SDLC
- **🛠️ Python analysis tools** - 53 CLI utilities for automated architecture, security, and product analysis
- **📚 Knowledge bases** - Curated reference materials covering architecture patterns, security practices, and product frameworks
- **📋 Ready-to-use templates** - ADRs, C4 diagrams, PRDs, user stories, and sprint templates

**Key Benefits for Pandora:**
- ⚡ **Zero dependencies** - Python 3.8+ standard library only, works across Pandora's environments
- 🎯 **SDLC-optimized** - 42 skills covering architecture, security, product management, engineering, delivery, and compliance
- 🔧 **Fast analysis** - Algorithmic tools without external API dependencies or rate limits
- 📈 **Measurable impact** - 40%+ time savings, 30%+ quality improvements, faster delivery cycles
- 👥 **Team adoption ready** - Designed for Pandora's entire development organization to use daily

---

## 📖 Documentation

**Getting Started**
- **[Installation Guide](docs/INSTALL.md)** - Complete setup instructions (Python 3.8+ only, no dependencies required)
- **[Usage Guide](docs/USAGE.md)** - Comprehensive examples and workflows for Claude AI and Claude Code

**Testing & Quality**
- **[Testing Guide](docs/testing/TESTING_GUIDE.md)** - Python script testing framework and CLI standards
- **[Testing Quick Start](docs/testing/TESTING_QUICK_START.md)** - Quick reference for running tests

**Workflows & Standards**
- **[Git Workflow](docs/WORKFLOW.md)** - Branch strategy and deployment pipeline (develop → staging → main)
- **[Standards Library](docs/standards/)** - Communication, quality, git, documentation, and security standards

**Project Info**
- **[Changelog](CHANGELOG.md)** - Version history and notable changes
- **[Contributors](CONTRIBUTORS.md)** - Attribution to Ali Rezvani and fork maintainers

---

## 🛠️ Production CLI Tools & Testing

**53 standardized Python CLI tools** with comprehensive testing framework (v2.0.0):

### CLI Features
- **Consistent Interface** - All tools use argparse with standard flags: `--help`, `--version`, `--output`, `--file`, `--verbose`
- **Multiple Output Formats** - Text (human-readable), JSON (machine-readable), CSV (spreadsheet integration)
- **Error Handling** - Standardized exit codes and UTF-8 encoding support
- **Sample Data** - 24 sample input files across domains for immediate testing

### Testing Framework
- **2,814 Automated Tests** - 100% pass rate across all scripts
- **CI/CD Integration** - GitHub Actions with pytest
- **Comprehensive Coverage** - Help flags, execution, output formats, error handling, unicode support

### Quick Start
```bash
# Test architecture analysis
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . --verbose

# Test security audit
python3 skills/engineering-team/senior-security/scripts/security_auditor.py --input . --verbose

# Test RICE prioritization
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  docs/examples/sample-features.csv --capacity 20

# Run with JSON output for CI/CD integration
python3 skills/engineering-team/senior-security/scripts/security_auditor.py \
  --input . --output json --file security-report.json
```

**Learn More:** [TESTING_GUIDE.md](TESTING_GUIDE.md) | [docs/standards/cli-standards.md](docs/standards/cli-standards.md)

---

## 🤖 Agent Catalog

**27 production agents** that orchestrate skills and provide guided workflows (v2.0):

Agents are workflow orchestrators that intelligently invoke skills, coordinate Python tools, and guide you through complex multi-step processes. While skills provide the tools and knowledge, agents provide the intelligence to use them effectively.

| Agent | Domain | Skills Used | Description |
|-------|--------|-------------|-------------|
| **Marketing Agents (3)** ||||
| [cs-content-creator](agents/marketing/cs-content-creator.md) | Marketing | content-creator | Create SEO-optimized marketing content with brand voice consistency |
| [cs-demand-gen-specialist](agents/marketing/cs-demand-gen-specialist.md) | Marketing | marketing-demand-acquisition | Lead generation and conversion funnel optimization |
| [cs-product-marketer](agents/marketing/cs-product-marketer.md) | Marketing | product-marketing | Product positioning, GTM strategy, competitive intelligence |
| **Product Agents (5)** ||||
| [cs-product-manager](agents/product/cs-product-manager.md) | Product | product-manager-toolkit | RICE prioritization, roadmap generation, customer discovery |
| [cs-agile-product-owner](agents/product/cs-agile-product-owner.md) | Product | agile-product-owner | User story generation, backlog management, sprint planning |
| [cs-product-strategist](agents/product/cs-product-strategist.md) | Product | product-strategist | OKR cascade generation, vision/strategy alignment |
| [cs-ux-researcher](agents/product/cs-ux-researcher.md) | Product | ux-researcher-designer | User research, persona generation, UX analysis |
| [cs-ui-designer](agents/product/cs-ui-designer.md) | Product | ui-design-system | Design systems, component libraries, design tokens |
| **Engineering Agents (15)** ||||
| [cs-code-reviewer](agents/engineering/cs-code-reviewer.md) | Engineering | code-reviewer | Code quality analysis, standards enforcement, PR reviews |
| [cs-architect](agents/engineering/cs-architect.md) | Engineering | senior-architect | System design, architecture patterns, technology evaluation |
| [cs-backend-engineer](agents/engineering/cs-backend-engineer.md) | Engineering | senior-backend | API development, database design, backend optimization |
| [cs-frontend-engineer](agents/engineering/cs-frontend-engineer.md) | Engineering | senior-frontend | React/Next.js development, frontend architecture |
| [cs-fullstack-engineer](agents/engineering/cs-fullstack-engineer.md) | Engineering | senior-fullstack | Full-stack development, MERN/PERN/T3 stacks |
| [cs-devops-engineer](agents/engineering/cs-devops-engineer.md) | Engineering | senior-devops | CI/CD, infrastructure automation, cloud operations |
| [cs-security-engineer](agents/engineering/cs-security-engineer.md) | Engineering | senior-security | Threat modeling, security auditing, penetration testing |
| [cs-secops-engineer](agents/engineering/cs-secops-engineer.md) | Engineering | senior-secops | Security operations, incident response, compliance |
| [cs-qa-engineer](agents/engineering/cs-qa-engineer.md) | Engineering | senior-qa | Test strategy, automation frameworks, quality assurance |
| [cs-ml-engineer](agents/engineering/cs-ml-engineer.md) | Engineering | senior-ml-engineer | ML pipelines, model deployment, MLOps |
| [cs-data-engineer](agents/engineering/cs-data-engineer.md) | Engineering | senior-data-engineer | Data pipelines, ETL, data warehousing |
| [cs-data-scientist](agents/engineering/cs-data-scientist.md) | Engineering | senior-data-scientist | Statistical analysis, predictive modeling, experimentation |
| [cs-computer-vision](agents/engineering/cs-computer-vision.md) | Engineering | senior-computer-vision | Image processing, object detection, CV pipelines |
| [cs-prompt-engineer](agents/engineering/cs-prompt-engineer.md) | Engineering | senior-prompt-engineer | LLM integration, prompt optimization, AI workflows |
| [cs-cto-advisor](agents/engineering/cs-cto-advisor.md) | Engineering | cto-advisor | Technical strategy, team scaling, tech debt management |
| **Delivery Agents (4)** ||||
| [cs-jira-expert](agents/delivery/cs-jira-expert.md) | Delivery | jira-expert | Jira workflows, automation, project tracking |
| [cs-confluence-expert](agents/delivery/cs-confluence-expert.md) | Delivery | confluence-expert | Documentation management, knowledge bases |
| [cs-scrum-master](agents/delivery/cs-scrum-master.md) | Delivery | scrum-master | Scrum ceremonies, team facilitation, agile coaching |
| [cs-senior-pm](agents/delivery/cs-senior-pm.md) | Delivery | senior-pm | Project management, stakeholder communication, delivery |

### Agents vs Skills

**Skills** = Tools + Knowledge + Templates
- 26 Pandora-focused skills
- 53 automation tools
- Domain expertise packaged

**Agents** = Workflow Orchestrators
- Invoke skills intelligently
- Guide multi-step processes
- Coordinate tools and knowledge

**Example:** The [cs-architect](agents/engineering/cs-architect.md) agent uses the senior-architect skill's Python tools (project_architect.py, dependency_analyzer.py) plus knowledge bases (architecture patterns, system design workflows) to guide you through architecture design and technical decision-making. Similarly, [cs-product-manager](agents/product/cs-product-manager.md) uses RICE prioritization tools and customer interview analyzers to drive data-informed product decisions.

**Learn More:** [agents/CLAUDE.md](agents/CLAUDE.md) | [templates/agent-template.md](templates/agent-template.md)

---

## 🚀 Available Skills

### Marketing Skills

**3 comprehensive marketing skills** covering content creation, demand generation, and product marketing strategy.

#### 📝 Content Creator
**Status:** ✅ Production Ready | **Version:** 1.0

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks.

**What's Included:**
- **Brand Voice Analyzer** - Analyze text for tone, formality, and readability (Python CLI)
- **SEO Optimizer** - Comprehensive SEO scoring and optimization recommendations (Python CLI)
- **Brand Guidelines** - 5 personality archetypes and voice framework
- **Content Frameworks** - 15+ templates (blog posts, emails, social media, video scripts)
- **Social Media Optimization** - Platform-specific guides for LinkedIn, Twitter/X, Instagram, Facebook, TikTok
- **Content Calendar Template** - Monthly planning and distribution framework

**Learn More:** [skills/marketing-team/content-creator/SKILL.md](skills/marketing-team/content-creator/SKILL.md)

---

#### 🎯 Marketing Demand & Acquisition
**Status:** ✅ Production Ready | **Version:** 1.0

Expert demand generation, paid media, SEO, and partnerships for Series A+ startups.

**What's Included:**
- **CAC Calculator** - Calculate channel-specific and blended customer acquisition cost (Python CLI)
- **Full-Funnel Strategy** - TOFU → MOFU → BOFU frameworks
- **Channel Playbooks** - LinkedIn Ads, Google Ads, Meta, SEO, Partnerships
- **HubSpot Integration** - Campaign tracking, attribution, lead scoring
- **International Expansion** - EU vs US vs Canada tactics
- **Performance Benchmarks** - B2B SaaS CAC and conversion benchmarks

**Learn More:** [skills/marketing-team/marketing-demand-acquisition/SKILL.md](skills/marketing-team/marketing-demand-acquisition/SKILL.md)

---

#### 🚀 Marketing Strategy & Product Marketing
**Status:** ✅ Production Ready | **Version:** 1.0

Product marketing, positioning, GTM strategy, and competitive intelligence.

**What's Included:**
- **ICP Definition** - Firmographics and psychographics frameworks
- **Positioning** - April Dunford positioning methodology
- **GTM Strategy** - PLG, Sales-Led, and Hybrid motion playbooks
- **Launch Plans** - 90-day product launch frameworks (Tier 1/2/3)
- **Competitive Intelligence** - Battlecard templates and analysis frameworks
- **International Market Entry** - 5-phase market expansion playbooks
- **Sales Enablement** - Training programs and asset development

**Learn More:** [skills/marketing-team/marketing-strategy-pmm/SKILL.md](skills/marketing-team/marketing-strategy-pmm/SKILL.md)

---

### Engineering Team Skills

#### 💻 CTO Advisor
**Status:** ✅ Production Ready | **Version:** 1.0

Technical leadership guidance for engineering teams, architecture decisions, and technology strategy.

**What's Included:**
- **Tech Debt Analyzer** - Quantify and prioritize technical debt (Python CLI)
- **Team Scaling Calculator** - Model engineering team growth and structure (Python CLI)
- **Engineering Metrics Framework** - DORA metrics, velocity, and quality indicators
- **Technology Evaluation Framework** - Structured approach to technology selection
- **Architecture Decision Records** - ADR templates and best practices

**Core Workflows:**
1. Technical debt assessment and management
2. Engineering team scaling and structure
3. Technology evaluation and selection
4. Architecture decision documentation

**Learn More:** [skills/engineering-team/cto-advisor/SKILL.md](skills/engineering-team/cto-advisor/SKILL.md)

---

### Product Team Skills

#### 📊 Product Manager Toolkit
**Status:** ✅ Production Ready | **Version:** 1.0

Essential tools and frameworks for modern product management, from discovery to delivery.

**What's Included:**
- **RICE Prioritizer** - Automated feature prioritization with portfolio analysis (Python CLI)
- **Customer Interview Analyzer** - AI-powered insight extraction from user interviews (Python CLI)
- **PRD Templates** - 4 comprehensive formats (Standard, One-Page, Agile Epic, Feature Brief)
- **Discovery Frameworks** - Customer interview guides, hypothesis templates, opportunity solution trees
- **Metrics & Analytics** - North Star metrics, funnel analysis, feature success tracking

**Core Workflows:**
1. Feature prioritization with RICE scoring
2. Customer discovery and interview analysis
3. PRD development and stakeholder alignment
4. Product metrics and success measurement

**Learn More:** [skills/product-team/product-manager-toolkit/SKILL.md](skills/product-team/product-manager-toolkit/SKILL.md)

---

#### 🎯 Agile Product Owner
**Status:** ✅ Production Ready | **Version:** 1.0

Sprint execution and backlog management tools for agile product delivery.

**What's Included:**
- **User Story Generator** - INVEST-compliant stories with acceptance criteria (Python CLI)
- **Sprint Planner** - Capacity-based sprint planning automation
- **Epic Breakdown** - Automatic story generation from epics
- **Velocity Tracker** - Sprint metrics and burndown analysis
- **Agile Ceremonies** - Frameworks for standups, retros, planning, reviews

**Core Workflows:**
1. Backlog refinement and grooming
2. Sprint planning and capacity allocation
3. User story writing and acceptance criteria
4. Sprint execution and velocity tracking

**Learn More:** [skills/product-team/agile-product-owner/SKILL.md](skills/product-team/agile-product-owner/SKILL.md)

---

#### 🚀 Product Strategist
**Status:** ✅ Production Ready | **Version:** 1.0

Strategic planning and vision alignment for heads of product and product leaders.

**What's Included:**
- **OKR Cascade Generator** - Automated company → product → team goal alignment (Python CLI)
- **Alignment Scoring** - Vertical and horizontal OKR alignment measurement
- **Strategy Templates** - Growth, retention, revenue, and innovation frameworks
- **Team Scaling Tools** - Organizational design and structure planning
- **Vision Frameworks** - Product vision, positioning, and roadmap development

**Core Workflows:**
1. Strategic planning and OKR setting
2. Product vision and positioning
3. Roadmap development and communication
4. Team organization and scaling

**Learn More:** [skills/product-team/product-strategist/SKILL.md](skills/product-team/product-strategist/SKILL.md)

---

#### 🎨 UX Researcher Designer
**Status:** ✅ Production Ready | **Version:** 1.0

User research and experience design frameworks for creating user-centered products.

**What's Included:**
- **Persona Generator** - Data-driven persona creation from user research (Python CLI)
- **Journey Mapper** - Customer journey visualization and mapping
- **Research Synthesizer** - Pattern identification from user interviews
- **Usability Framework** - Testing protocols and heuristic evaluation
- **Design Thinking** - Double diamond process, workshops, and facilitation

**Core Workflows:**
1. User research planning and execution
2. Research synthesis and insight generation
3. Persona development and validation
4. Journey mapping and experience design

**Learn More:** [skills/product-team/ux-researcher-designer/SKILL.md](skills/product-team/ux-researcher-designer/SKILL.md)

---

#### 🎨 UI Design System
**Status:** ✅ Production Ready | **Version:** 1.0

Visual design systems and component architecture for consistent user interfaces.

**What's Included:**
- **Design Token Generator** - Complete token system from brand colors (Python CLI)
- **Component Architecture** - Atomic design implementation and organization
- **Responsive Calculator** - Breakpoint and grid system generation
- **Export Formats** - JSON, CSS, SCSS outputs for development handoff
- **Documentation Templates** - Storybook integration and component specs

**Core Workflows:**
1. Design token system creation
2. Component library architecture
3. Design system documentation
4. Developer handoff and implementation

**Learn More:** [skills/product-team/ui-design-system/SKILL.md](skills/product-team/ui-design-system/SKILL.md)

---

### Project Management Team Skills

**4 production-ready delivery skills** for project and agile delivery teams using Jira and Confluence.

#### 📋 Senior Project Management Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Strategic project management for software, SaaS, and digital applications.

**What's Included:**
- Portfolio management and strategic planning
- Stakeholder alignment and executive reporting
- Risk management and budget oversight
- Cross-functional team leadership
- Roadmap development and project charters
- Atlassian MCP integration for metrics and reporting

**Learn More:** See `skills/delivery-team/README.md` for details

---

#### 🏃 Scrum Master Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Agile facilitation for software development teams.

**What's Included:**
- Sprint planning and execution
- Daily standups and retrospectives
- Backlog refinement and grooming
- Velocity tracking and metrics
- Impediment removal and escalation
- Team coaching on agile practices
- Atlassian MCP integration for sprint management

**Learn More:** See `skills/delivery-team/README.md` for details

---

#### ⚙️ Atlassian Jira Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Jira configuration, JQL mastery, and technical operations.

**What's Included:**
- Advanced JQL query writing
- Project and workflow configuration
- Custom fields and automation rules
- Dashboards and reporting
- Integration setup and optimization
- Performance tuning
- Atlassian MCP integration for all Jira operations

**Learn More:** See `skills/delivery-team/README.md` for details

---

#### 📚 Atlassian Confluence Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Knowledge management and documentation architecture.

**What's Included:**
- Space architecture and organization
- Page templates and macro implementation
- Documentation strategy and governance
- Content collaboration workflows
- Jira integration and linking
- Search optimization and findability
- Atlassian MCP integration for documentation

**Learn More:** See `skills/delivery-team/README.md` for details

---

### Engineering Team Skills

**Complete engineering skills suite with 9 specialized roles** covering architecture, development, testing, security, and operations.

#### 🏗️ Senior Software Architect
**Status:** ✅ Production Ready | **Version:** 1.0

System architecture design, technology stack decisions, and architecture documentation.

**What's Included:**
- **Architecture Diagram Generator** - Create C4, sequence, and component diagrams (Python CLI)
- **Project Architect** - Scaffold architecture documentation and ADRs (Python CLI)
- **Dependency Analyzer** - Analyze and visualize dependencies (Python CLI)
- **Architecture Patterns** - Monolithic, microservices, serverless, event-driven patterns
- **System Design Workflows** - Step-by-step architecture design process
- **Tech Decision Guide** - Framework for technology stack selection

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### ⚛️ Senior Frontend Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Frontend development with React, Next.js, and TypeScript.

**What's Included:**
- **Component Generator** - Scaffold React components with TypeScript (Python CLI)
- **Bundle Analyzer** - Optimize bundle size and performance (Python CLI)
- **Frontend Scaffolder** - Complete frontend project setup (Python CLI)
- **React Patterns** - Component composition, hooks, state management
- **Next.js Optimization** - App Router, Server Components, performance tuning
- **Frontend Best Practices** - Accessibility, SEO, performance optimization

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 🔧 Senior Backend Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Backend development with Node.js, Express, GraphQL, Go, and Python.

**What's Included:**
- **API Scaffolder** - Generate REST and GraphQL endpoints (Python CLI)
- **Database Migration Tool** - Manage PostgreSQL migrations (Python CLI)
- **API Load Tester** - Performance testing and optimization (Python CLI)
- **API Design Patterns** - RESTful, GraphQL, microservices architecture
- **Database Optimization** - Query optimization, indexing, connection pooling
- **Backend Security** - Authentication, authorization, data validation

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 💻 Senior Fullstack Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

End-to-end application development with complete stack integration.

**What's Included:**
- **Fullstack Scaffolder** - Complete Next.js + GraphQL + PostgreSQL projects (Python CLI)
- **Project Scaffolder** - Production-ready project structure (Python CLI)
- **Code Quality Analyzer** - Comprehensive analysis and security scanning (Python CLI)
- **Tech Stack Guide** - Complete implementation guides for your stack
- **Architecture Patterns** - Full-stack system design and integration
- **Development Workflows** - Git, CI/CD, testing, deployment automation

**Learn More:** [skills/engineering-team/fullstack-engineer/SKILL.md](skills/engineering-team/fullstack-engineer/SKILL.md)

---

#### 🧪 Senior QA Testing Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Quality assurance and test automation for comprehensive testing strategies.

**What's Included:**
- **Test Suite Generator** - Create unit, integration, E2E tests (Python CLI)
- **Coverage Analyzer** - Analyze and report test coverage (Python CLI)
- **E2E Test Scaffolder** - Setup Playwright/Cypress tests (Python CLI)
- **Testing Strategies** - Testing pyramid, TDD, BDD methodologies
- **Test Automation Patterns** - Page objects, fixtures, mocking strategies
- **QA Best Practices** - Quality metrics, regression testing, performance testing

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 🚀 Senior DevOps Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

CI/CD automation, infrastructure as code, and deployment management.

**What's Included:**
- **Pipeline Generator** - Create GitHub Actions/CircleCI pipelines (Python CLI)
- **Terraform Scaffolder** - Generate infrastructure as code (Python CLI)
- **Deployment Manager** - Automate deployment workflows (Python CLI)
- **CI/CD Pipeline Guide** - Best practices for continuous integration/deployment
- **Infrastructure as Code** - Terraform, CloudFormation, Kubernetes
- **Deployment Strategies** - Blue-green, canary, rolling deployments

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 🛡️ Senior SecOps Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Security operations, vulnerability management, and compliance automation.

**What's Included:**
- **Security Scanner** - Automated vulnerability scanning (Python CLI)
- **Vulnerability Assessor** - Risk assessment and prioritization (Python CLI)
- **Compliance Checker** - GDPR, SOC2 compliance validation (Python CLI)
- **Security Standards** - OWASP Top 10, security best practices
- **Vulnerability Management** - Detection, assessment, remediation workflows
- **Compliance Requirements** - Compliance frameworks and automation

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 👁️ Code Reviewer
**Status:** ✅ Production Ready | **Version:** 1.0

Automated code review, quality checking, and PR analysis.

**What's Included:**
- **PR Analyzer** - Automated pull request analysis (Python CLI)
- **Code Quality Checker** - Quality metrics and scoring (Python CLI)
- **Review Report Generator** - Generate comprehensive review reports (Python CLI)
- **Code Review Checklist** - Comprehensive review standards
- **Coding Standards** - Language-specific conventions and best practices
- **Common Anti-patterns** - What to avoid and how to fix

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 🔐 Senior Security Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Security architecture, penetration testing, and cryptography implementation.

**What's Included:**
- **Threat Modeler** - Automated threat modeling (Python CLI)
- **Security Auditor** - Comprehensive security audits (Python CLI)
- **Pentest Automator** - Automated penetration testing (Python CLI)
- **Security Architecture Patterns** - Zero Trust, defense in depth, secure design
- **Penetration Testing Guide** - Testing methodologies and tools
- **Cryptography Implementation** - Encryption, hashing, secure communication

**Learn More:** See `skills/engineering-team/README.md` for details

---

### AI/ML/Data Team Skills

**5 specialized AI/ML and data engineering skills** for building modern data-driven and AI-powered products.

#### 📊 Senior Data Scientist
**Status:** ✅ Production Ready | **Version:** 1.0

Statistical modeling, experimentation, and business analytics.

**What's Included:**
- **Experiment Designer** - Design A/B tests and statistical experiments (Python CLI)
- **Feature Engineering Pipeline** - Automated feature engineering workflows (Python CLI)
- **Statistical Analyzer** - Statistical modeling and causal inference (Python CLI)
- **Statistical Methods** - Hypothesis testing, regression, time series, causal inference
- **Experimentation Framework** - A/B testing, multi-armed bandits, Bayesian optimization
- **Analytics Patterns** - Business metrics, dashboards, reporting

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 🔧 Senior Data Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Data pipeline engineering, ETL/ELT workflows, and data infrastructure.

**What's Included:**
- **Pipeline Orchestrator** - Build data pipelines with Airflow/Spark (Python CLI)
- **Data Quality Validator** - Data quality checks and monitoring (Python CLI)
- **ETL Generator** - Generate ETL/ELT workflows (Python CLI)
- **Data Pipeline Patterns** - Batch, streaming, lambda architecture
- **Data Quality Framework** - Validation, monitoring, lineage tracking
- **Data Modeling Guide** - Dimensional modeling, data vault, schema design

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 🤖 Senior ML/AI Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

MLOps, model deployment, and LLM integration for production AI systems.

**What's Included:**
- **Model Deployment Pipeline** - Deploy ML models to production (Python CLI)
- **MLOps Setup Tool** - Setup MLOps infrastructure with MLflow (Python CLI)
- **LLM Integration Builder** - Integrate LLMs into applications (Python CLI)
- **MLOps Production Patterns** - Model versioning, monitoring, A/B testing
- **LLM Integration Guide** - RAG, fine-tuning, prompt engineering
- **Model Deployment Strategies** - Serving, scaling, monitoring

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 💬 Senior Prompt Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

LLM optimization, RAG systems, and agentic AI development.

**What's Included:**
- **Prompt Optimizer** - Optimize prompts for better LLM responses (Python CLI)
- **RAG System Builder** - Build Retrieval Augmented Generation systems (Python CLI)
- **Agent Orchestrator** - Design and orchestrate AI agents (Python CLI)
- **Advanced Prompting Techniques** - Chain-of-thought, few-shot, meta-prompting
- **RAG Architecture Patterns** - Vector search, chunking, reranking
- **Agent Design Patterns** - ReAct, tool use, multi-agent systems

**Learn More:** See `skills/engineering-team/README.md` for details

---

#### 👁️ Senior Computer Vision Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Computer vision, image/video AI, and real-time visual inference.

**What's Included:**
- **Vision Model Trainer** - Train object detection and segmentation models (Python CLI)
- **Inference Optimizer** - Optimize vision model inference (Python CLI)
- **Video Processor** - Process and analyze video streams (Python CLI)
- **Vision Architecture Patterns** - Object detection, segmentation, classification
- **Real-time Inference Guide** - Edge deployment, optimization, latency reduction
- **Computer Vision Production** - Model serving, monitoring, data pipelines

**Learn More:** See `skills/engineering-team/README.md` for details

---


## ⚡ Quick Start

### For Claude AI Users

1. **Download** the skill package you need (or clone this repository)
2. **Upload** the SKILL.md file to your Claude conversation
3. **Reference** the skill: "Using the content-creator skill, help me write a LinkedIn post about AI"

### For Claude Code Users

1. **Clone** this repository into your project
2. **Load** the skill in your Claude Code session
3. **Execute** workflows and run analysis tools directly

---

## 🤖 How to Use with Claude AI

Claude AI can use these skills to provide specialized expertise in your conversations.

### Method 1: Upload Skill Documentation

**Step-by-Step:**

1. **Navigate to the skill folder** you want to use (e.g., `skills/marketing-team/content-creator/`)

2. **Upload the SKILL.md file** to your Claude conversation:
   - Click the attachment icon 📎
   - Select `SKILL.md` from the skill folder
   - Upload to the conversation

3. **Reference the skill in your prompts:**
   ```
   Using the content-creator skill, help me:
   - Write a blog post about sustainable technology
   - Analyze my brand voice from these 3 articles
   - Create a LinkedIn content calendar for November 2025
   ```

4. **Access reference materials as needed:**
   - Upload specific reference files (e.g., `references/content_frameworks.md`)
   - Claude will use the frameworks to guide content creation

### Method 2: Use Packaged .zip Archives

For easy sharing with your team:

1. **Download** the pre-packaged .zip file (e.g., `content-creator.zip`)
2. **Extract** to your local machine
3. **Upload SKILL.md** to Claude as described above

### Example Prompts

**Content Creator Skill:**
```
Using the content-creator skill:
1. Analyze this article for brand voice consistency
2. Optimize this blog post for the keyword "marketing automation"
3. Create a 30-day LinkedIn content calendar for our product launch
4. Write a Twitter thread explaining our new feature
```

**CTO Advisor Skill:**
```
Using the cto-advisor skill:
1. Analyze our technical debt and create a reduction roadmap
2. Calculate optimal team structure for scaling to 50 engineers
3. Evaluate whether we should adopt GraphQL or stick with REST
4. Create an ADR for our microservices migration decision
```

**Product Manager Toolkit:**
```
Using the product-manager-toolkit skill:
1. Prioritize our backlog of 50 features using RICE scoring
2. Analyze customer interview transcripts to extract pain points
3. Create a PRD for our new analytics dashboard feature
4. Design a customer discovery interview guide for B2B users
```

**Agile Product Owner:**
```
Using the agile-product-owner skill:
1. Generate user stories for our mobile app redesign epic
2. Plan next sprint with 30 story points capacity
3. Create acceptance criteria for authentication feature
4. Analyze our velocity trends over last 6 sprints
```

**Product Strategist:**
```
Using the product-strategist skill:
1. Generate OKR cascade from company goals to team level
2. Create product vision and positioning for new market
3. Design quarterly roadmap with strategic themes
4. Plan product team scaling from 5 to 20 people
```

**UX Researcher Designer:**
```
Using the ux-researcher-designer skill:
1. Create data-driven personas from 20 user interviews
2. Map customer journey for onboarding experience
3. Design usability test protocol for checkout flow
4. Synthesize research findings into actionable insights
```

**UI Design System:**
```
Using the ui-design-system skill:
1. Generate complete design token system from brand color #0066CC
2. Create component library architecture using atomic design
3. Define responsive breakpoints and grid system
4. Export design tokens as CSS variables for developers
```

**Fullstack Engineer:**
```
Using the fullstack-engineer skill:
1. Scaffold a new Next.js + GraphQL + PostgreSQL project
2. Analyze code quality and security vulnerabilities in existing project
3. Implement clean architecture patterns for backend API
4. Set up CI/CD pipeline with GitHub Actions and Docker
```

### Tips for Best Results

✅ **DO:**
- Reference the skill name explicitly in your prompts
- Upload relevant reference materials for complex tasks
- Ask Claude to use specific frameworks or templates from the skill
- Provide context about your industry, audience, or constraints

❌ **DON'T:**
- Assume Claude remembers the skill across different conversations (re-upload if needed)
- Mix too many skills in one conversation (focus on one domain at a time)
- Skip uploading the SKILL.md file (it contains essential workflows)

---

## 💻 How to Use with Claude Code

Claude Code can execute the Python analysis tools and integrate skills into your development workflow.

### Setup

1. **Clone this repository** into your project or workspace:
   ```bash
   git clone https://github.com/rickydwilson-dcs/claude-skills.git
   cd claude-skills
   ```

2. **Verify Python installation**:
   ```bash
   python3 --version  # Should be 3.8 or higher
   # No pip install needed - all scripts use standard library only!
   ```

3. **Test with core software delivery tools**:
   ```bash
   # Architecture analysis
   python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . --verbose

   # Security audit
   python3 skills/engineering-team/senior-security/scripts/security_auditor.py --input . --verbose

   # RICE prioritization
   python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
     docs/examples/sample-features.csv --capacity 20
   ```

### Using Core Analysis Tools

#### Architecture Analyzer

Analyze your codebase structure, patterns, and optimization opportunities:

```bash
# Comprehensive architecture analysis
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . --verbose

# JSON output for CI/CD integration
python3 skills/engineering-team/senior-architect/scripts/project_architect.py \
  --input . --output json --file architecture-report.json
```

**Output includes:**
- Project structure assessment
- Architecture pattern detection (monolithic, microservices, event-driven)
- Dependency analysis and circular dependency detection
- Scalability and performance recommendations
- Technical debt identification
- Improvement recommendations

#### Security Auditor

Comprehensive security analysis with OWASP Top 10 scanning:

```bash
# Full security audit
python3 skills/engineering-team/senior-security/scripts/security_auditor.py --input . --verbose

# JSON output for CI/CD pipelines
python3 skills/engineering-team/senior-security/scripts/security_auditor.py \
  --input . --output json --file security-report.json
```

**Output includes:**
- OWASP Top 10 vulnerability detection (SQL injection, XSS, CSRF, etc.)
- Exposed secrets detection (API keys, passwords, tokens)
- Weak cryptography identification (MD5, SHA1, weak ciphers)
- Dependency vulnerability scanning
- Security control verification
- Prioritized remediation recommendations

#### RICE Prioritizer (Product Management)

Data-driven feature prioritization using RICE framework:

```bash
# Prioritize features with capacity planning
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  docs/examples/sample-features.csv --capacity 20

# JSON output for roadmap tools
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  features.csv --capacity 20 --output json --file roadmap.json
```

**Output includes:**
- RICE scores for each feature (Reach × Impact × Confidence / Effort)
- Portfolio analysis (Quick Wins, Big Bets, Fill-Ins, Money Pits)
- Quarterly roadmap recommendations based on capacity
- Trade-off analysis for stakeholder alignment

#### Customer Interview Analyzer (Product Management)

Extract insights from user research transcripts:

```bash
python3 skills/product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py \
  docs/examples/sample-interview.txt
```

**Output includes:**
- Pain points extraction with severity ratings
- Feature requests identified from conversation
- Jobs-to-be-done patterns
- Sentiment analysis
- Theme extraction across multiple interviews

#### RICE Prioritizer (Product Manager)

Feature prioritization with portfolio analysis:

```bash
# Basic prioritization
python skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# With custom team capacity
python skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20

# Output as JSON
python skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --output json
```

#### Customer Interview Analyzer (Product Manager)

Extract insights from user interviews:

```bash
# Analyze single interview
python skills/product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py interview.txt

# Output as JSON for aggregation
python skills/product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py interview.txt json
```

#### User Story Generator (Product Owner)

Generate INVEST-compliant user stories:

```bash
# Interactive mode
python skills/product-team/agile-product-owner/scripts/user_story_generator.py

# Generate sprint plan with capacity
python skills/product-team/agile-product-owner/scripts/user_story_generator.py sprint 30
```

#### OKR Cascade Generator (Product Strategist)

Generate aligned OKR hierarchy:

```bash
# Generate OKRs for growth strategy
python skills/product-team/product-strategist/scripts/okr_cascade_generator.py growth

# Other strategy types: retention, revenue, innovation
python skills/product-team/product-strategist/scripts/okr_cascade_generator.py retention
```

#### Persona Generator (UX Researcher)

Create data-driven personas:

```bash
# Interactive persona creation
python skills/product-team/ux-researcher-designer/scripts/persona_generator.py

# Export as JSON
python skills/product-team/ux-researcher-designer/scripts/persona_generator.py --output json
```

#### Design Token Generator (UI Designer)

Generate complete design system tokens:

```bash
# Generate tokens from brand color
python skills/product-team/ui-design-system/scripts/design_token_generator.py "#0066CC" modern css

# Output formats: css, json, scss
python skills/product-team/ui-design-system/scripts/design_token_generator.py "#0066CC" modern json
```

#### Project Scaffolder (Fullstack Engineer)

Scaffold production-ready fullstack projects:

```bash
# Create new Next.js + GraphQL + PostgreSQL project
python skills/engineering-team/fullstack-engineer/scripts/project_scaffolder.py my-project --type nextjs-graphql

# Navigate and start
cd my-project && docker-compose up -d
```

#### Code Quality Analyzer (Fullstack Engineer)

Analyze code quality and security:

```bash
# Analyze existing project
python skills/engineering-team/fullstack-engineer/scripts/code_quality_analyzer.py /path/to/project

# Get JSON report
python skills/engineering-team/fullstack-engineer/scripts/code_quality_analyzer.py /path/to/project --json
```

#### Fullstack Scaffolder (Fullstack Engineer)

Rapid fullstack project generation:

```bash
# Generate fullstack application structure
python skills/engineering-team/fullstack-engineer/scripts/fullstack_scaffolder.py my-app --stack nextjs-graphql
```

### Integrating with Claude Code Workflows

**Example 1: Automated Content Quality Check**

```bash
# In your Claude Code session:
# 1. Write content using content-creator frameworks
# 2. Run automated analysis
python skills/marketing-team/content-creator/scripts/seo_optimizer.py output.md "target keyword"
python skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py output.md json

# 3. Claude Code reviews results and suggests improvements
```

**Example 2: Technical Debt Tracking**

```bash
# Run monthly tech debt analysis
python skills/engineering-team/cto-advisor/scripts/tech_debt_analyzer.py src/

# Claude Code generates report and roadmap
# Tracks progress over time
```

**Example 3: Content Pipeline Automation**

Create a workflow in Claude Code:
1. Generate content using content frameworks
2. Auto-run SEO optimizer on all drafts
3. Flag content below SEO score threshold (< 75)
4. Apply recommendations automatically
5. Re-score and validate

### Advanced: Custom Skill Development

Use this repository as a template to build your own skills:

1. **Fork this repository**
2. **Create new skill folder** following the architecture pattern
3. **Develop** your domain-specific tools and frameworks
4. **Document** workflows in SKILL.md
5. **Share** with your team or contribute back

See [CLAUDE.md](CLAUDE.md) for detailed architecture and development guidelines.

---

## 🏗️ Skill Architecture

Each skill package follows a consistent, modular structure:

```
{skill-category}/
└── {skill-name}/
    ├── SKILL.md                          # Master documentation
    ├── scripts/                          # Python CLI tools
    │   ├── {tool_name}.py               # Executable analysis tools
    │   └── ...
    ├── references/                       # Knowledge bases
    │   ├── {framework_name}.md          # Curated guidelines
    │   └── ...
    └── assets/                           # User templates
        ├── {template_name}.md           # Ready-to-use templates
        └── ...
```

### Design Principles

1. **Self-Contained** - Each skill is fully independent and deployable
2. **Documentation-Driven** - Success depends on clear, actionable documentation
3. **Algorithm Over AI** - Use deterministic analysis (code) when possible for speed and reliability
4. **Template-Heavy** - Provide ready-to-use frameworks users can customize
5. **Platform-Specific** - Focus on specific, actionable advice over generic best practices

### Component Responsibilities

| Component | Purpose | Format |
|-----------|---------|--------|
| **SKILL.md** | Entry point, workflows, usage instructions | Markdown |
| **scripts/** | Automated analysis and optimization tools | Python CLI |
| **references/** | Expert knowledge, frameworks, guidelines | Markdown |
| **assets/** | Templates for end-user customization | Markdown/YAML |

---

## 📦 Installation

### Prerequisites

- **Python 3.7+** (for running analysis scripts)
- **Claude AI account** or **Claude Code** (for using skills)
- **Git** (for cloning repository)

### Clone Repository

```bash
git clone https://github.com/rickydwilson-dcs/claude-skills.git
cd claude-skills
```

### Verify Python Installation

All scripts use Python standard library only - **no pip install required!**

```bash
python3 --version  # Should be 3.8 or higher
```

### Test Installation

```bash
# Test marketing skills
python skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py --help
python skills/marketing-team/content-creator/scripts/seo_optimizer.py --help

# Test CTO advisor skills
python skills/engineering-team/cto-advisor/scripts/tech_debt_analyzer.py --help
python skills/engineering-team/cto-advisor/scripts/team_scaling_calculator.py --help

# Test product team skills
python skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py --help
python skills/product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py --help
python skills/product-team/agile-product-owner/scripts/user_story_generator.py --help
python skills/product-team/product-strategist/scripts/okr_cascade_generator.py --help
python skills/product-team/ux-researcher-designer/scripts/persona_generator.py --help
python skills/product-team/ui-design-system/scripts/design_token_generator.py --help

# Test engineering team skills
python skills/engineering-team/fullstack-engineer/scripts/project_scaffolder.py --help
python skills/engineering-team/fullstack-engineer/scripts/code_quality_analyzer.py --help
python skills/engineering-team/fullstack-engineer/scripts/fullstack_scaffolder.py --help
```

---

## 📖 Usage Examples

### Example 1: Blog Post Optimization

**Scenario:** You've written a blog post and want to optimize it for SEO and brand consistency.

```bash
# Step 1: Check SEO
python skills/marketing-team/content-creator/scripts/seo_optimizer.py blog-post.md "AI automation"

# Output: SEO Score: 68/100
# Recommendations:
# - Add 3 more mentions of primary keyword (current density: 0.8%, target: 1-2%)
# - Include H2 heading with primary keyword
# - Add 2 internal links
# - Meta description too short (current: 120 chars, target: 150-160)

# Step 2: Check brand voice
python skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py blog-post.md

# Output:
# Formality: 7/10 (Professional)
# Tone: Authoritative, Informative
# Readability: 65 (Standard - college level)
# Recommendations:
# - Reduce sentence length by 15% for better readability
# - Use more active voice (currently 60%, target: 70%+)

# Step 3: Apply fixes in your editor
# Step 4: Re-run analysis to verify improvements
```

### Example 2: User Story Generation for Sprint

**Using Claude AI:**

1. Upload `skills/product-team/agile-product-owner/SKILL.md`
2. Prompt:
   ```
   Using the agile-product-owner skill, generate user stories for our authentication feature.

   Epic: User Authentication System
   Sprint capacity: 30 story points
   Team: 5 developers (2 backend, 2 frontend, 1 fullstack)

   Must include:
   - Login/logout functionality
   - Password reset flow
   - Remember me feature
   - Session management
   ```

3. Claude generates:
   - 8-10 user stories with acceptance criteria
   - Story point estimates
   - Technical dependencies identified
   - Backend/frontend split
   - Test scenarios for QA

### Example 3: React Component with Architecture Review

**Using Claude Code:**

```bash
# Step 1: Generate React component
# Ask Claude Code: "Create a reusable DataTable component with sorting, filtering, and pagination"

# Step 2: Review component architecture
python skills/engineering-team/senior-architect/scripts/project_architect.py --input src/components --verbose

# Output includes:
# - Component structure analysis
# - Props interface design review
# - Performance optimization recommendations
# - Accessibility compliance check
# - Reusability score

# Step 3: Run security audit on generated code
python skills/engineering-team/senior-security/scripts/security_auditor.py --input src/components/DataTable.tsx

# Output: XSS vulnerability checks, input sanitization, secure data handling
```

### Example 4: Feature Prioritization with RICE

**Using Product Manager Toolkit:**

```bash
# Step 1: Create features CSV
cat > features.csv << 'EOF'
feature,reach,impact,confidence,effort
SSO Integration,1000,3,0.9,8
Dark Mode,500,1,1.0,2
Mobile App,2000,3,0.6,15
API Rate Limiting,1500,2,0.8,3
Advanced Reporting,800,2,0.7,6
EOF

# Step 2: Run RICE prioritization
python skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv --capacity 20

# Output:
# === RICE Prioritization Results ===
# 1. API Rate Limiting - RICE: 750 (Quick Win ⚡)
# 2. SSO Integration - RICE: 337 (Big Bet 🎯)
# 3. Dark Mode - RICE: 250 (Quick Win ⚡)
# 4. Advanced Reporting - RICE: 187
# 5. Mobile App - RICE: 266 (over capacity)
#
# Recommended Q1 Roadmap: API Rate Limiting, SSO Integration, Dark Mode (18 points)
```

---

## 🔗 Related Projects & Tools

Explore our complete ecosystem of Claude Code augmentation tools and utilities:

### 🏭 Claude Code Skills & Agents Factory

**Repository:** [claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory)

**What it is:** Factory toolkit for generating production-ready Claude Skills and Agents at scale.

**Key Features:**
- 🎯 **69 Factory Presets** across 15 professional domains
- 🔧 **Smart Generation** - Automatically determines if Python code or prompt-only instruction is needed
- 📦 **Complete Skill Packages** - Generates SKILL.md, Python scripts, references, and sample data
- 🚀 **Multi-Platform Support** - Works with Claude.ai, Claude Code, and API
- ⚡ **Rapid Prototyping** - Create custom skills in minutes, not hours

**Perfect For:**
- Building custom skills beyond the 42 provided in this library
- Generating domain-specific agents for your organization
- Scaling AI customization across teams
- Rapid prototyping of specialized workflows

**Use Case:** "I need a skill for [your specific domain]? Use the Factory to generate it instantly!"

---

### 💎 Claude Code Tresor (Productivity Toolkit)

**Repository:** [claude-code-tresor](https://github.com/alirezarezvani/claude-code-tresor)

**What it is:** Comprehensive productivity enhancement toolkit with 20+ utilities for Claude Code development workflows.

**Key Features:**
- 🤖 **8 Autonomous Skills** - Background helpers (code quality, security, testing, docs)
- 👨‍💻 **8 Expert Agents** - Manual specialists via `@` mentions (architecture, debugging, performance)
- ⚡ **4 Workflow Commands** - Slash commands (`/scaffold`, `/review`, `/test-gen`, `/docs-gen`)
- 📋 **20+ Prompt Templates** - Common development scenarios ready to use
- 📚 **Development Standards** - Style guides and best practices

**Perfect For:**
- Solo developers seeking productivity acceleration
- Development teams standardizing processes
- Code quality automation and continuous improvement
- Professional Claude Code workflows from scaffolding through deployment

**Use Case:** "Working on a project in Claude Code? Use Tresor's agents, commands, and skills to supercharge your development workflow!"

---

### 🌟 How These Projects Work Together

**Complete Claude Code Ecosystem:**

```
┌─────────────────────────────────────────────────────────┐
│  Claude Skills Library (This Repository)                │
│  42 Domain Expert Skills - Marketing to Engineering     │
│  Use for: Domain expertise, frameworks, best practices  │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌──────────────┐  ┌───────────────────┐
│ Skill Factory│  │  Claude Tresor    │
│              │  │                   │
│ Create MORE  │  │ USE skills in     │
│ custom skills│  │ development       │
│              │  │                   │
│ For: Custom  │  │ For: Daily dev    │
│ domains &    │  │ workflows, code   │
│ org-specific │  │ quality, testing  │
│ needs        │  │ automation        │
└──────────────┘  └───────────────────┘
```

**Workflow:**
1. **Start here** (Skills Library) - Get 42 production-ready expert skills
2. **Expand** (Skill Factory) - Generate custom skills for your specific needs
3. **Supercharge** (Tresor) - Use skills + agents + commands in Claude Code development

**Together they provide:**
- ✅ 42 ready-to-use expert skills (this repo)
- ✅ Unlimited custom skill generation (Factory)
- ✅ Complete development workflow automation (Tresor)
- ✅ Cross-platform compatibility (Claude.ai, Claude Code, API)

**All repositories by [Alireza Rezvani](https://alirezarezvani.com)** - Building the complete Claude Code augmentation ecosystem.

---


## 🤝 Contributing

Contributions are welcome! This repository aims to democratize professional expertise through reusable skill packages.

### How to Contribute

1. **Fork** this repository
2. **Create** a feature branch (`git checkout -b feature/new-skill`)
3. **Develop** your skill following the architecture guidelines in [CLAUDE.md](CLAUDE.md)
4. **Test** your tools and validate documentation
5. **Submit** a pull request with detailed description

### Contribution Ideas

- **New Skills** - Domain expertise in your field (finance, HR, product management, etc.)
- **Tool Enhancements** - Improve existing Python analysis scripts
- **Framework Additions** - Add new templates or methodologies to existing skills
- **Documentation** - Improve how-to guides, examples, or translations
- **Bug Fixes** - Fix issues in scripts or documentation

### Quality Standards

All contributions should:
- ✅ Follow the modular skill architecture pattern
- ✅ Include comprehensive SKILL.md documentation
- ✅ Provide actionable, specific guidance (not generic advice)
- ✅ Use algorithmic tools (Python) when possible, not just documentation
- ✅ Include ready-to-use templates or examples
- ✅ Be self-contained and independently deployable

---

## 📄 License

This project is licensed under the **MIT License** - see below for details.

```
MIT License

Copyright (c) 2025 Alireza Rezvani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

You are free to:
- ✅ Use these skills commercially
- ✅ Modify and adapt to your needs
- ✅ Distribute to your team or clients
- ✅ Create derivative works

---

## 👤 Attribution

### Original Author

**Alireza Rezvani** - Creator of claude-skills

This repository is built on the foundational work of Alireza Rezvani, who created the original claude-skills architecture and skill library.

- 🌐 **Original Repository:** [github.com/alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- 📝 **Blog:** [medium.com/@alirezarezvani](https://medium.com/@alirezarezvani)

Alireza's vision was to **make world-class expertise accessible to everyone** through Claude AI. Each original skill represents hundreds of hours of domain expertise, distilled into actionable frameworks and automated tools.

### Pandora Edition

This is a **Pandora-focused fork** maintained by Ricky Wilson for Pandora's internal teams. We've specialized the repository to focus on our specific operational needs:

- **4 Core Domains:** Marketing, Product, Engineering, Delivery
- **26 Curated Skills:** Focused on Pandora's actual use cases
- **Pandora-Specific Workflows:** Tailored documentation and examples

For the full list of contributors, see [CONTRIBUTORS.md](CONTRIBUTORS.md).

---

## 🙏 Acknowledgments

- **Alireza Rezvani** - For creating the original claude-skills architecture and vision
- **Anthropic** - For building Claude AI and Claude Code, making this possible
- **Pandora Teams** - For testing and refining skills for our specific use cases
- **Open Source Community** - For tools and libraries that power the analysis scripts

---

## 📞 Support & Feedback

### For Pandora Teams

- **Documentation Issues:** Open an issue in this repository
- **Skill Requests:** Submit a feature request describing your Pandora use case
- **General Questions:** Contact the Pandora Skills maintainer

### For Original claude-skills

This is a fork of Ali Rezvani's original work. For questions about the upstream project:
- **Original Repository:** [github.com/alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills)
- **Creator Contact:** [alirezarezvani.com](https://alirezarezvani.com) or [blog](https://medium.com/@alirezarezvani)

---

<div align="center">

**🔗 Pandora Edition** | **🚀 Built with Claude AI** | **📦 Focused for Impact**

**Originally created by [Ali Rezvani](https://github.com/alirezarezvani/claude-skills)**

</div>
