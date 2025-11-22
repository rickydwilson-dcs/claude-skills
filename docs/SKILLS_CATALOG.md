# Skills Catalog

**Complete catalog of 43 production-ready skills for Pandora's SDLC**

This document provides detailed descriptions of all available skills in the Claude Skills Library. Each skill is a self-contained package with Python CLI tools, expert knowledge bases, and ready-to-use templates.

**Validation Status**: 28/28 passing (100%)
**Last Validated**: November 22, 2025

## Validation

All skills pass 9 validation checks:
- ✓ Valid directory structure (scripts/, references/, assets/)
- ✓ SKILL.md with required sections
- ✓ Extended metadata YAML (version, author, category, keywords, tech-stack)
- ✓ Python tools marked executable
- ✓ Complete frontmatter with name, description, license

Use `python3 scripts/skill_builder.py --validate <skill-dir>` to validate skills.

See [Builder Standards](standards/builder-standards.md) for complete validation criteria.

---

## Table of Contents

- [Marketing Skills](#marketing-skills) - 3 skills
- [Product Team Skills](#product-team-skills) - 6 skills
- [Engineering Team Skills](#engineering-team-skills) - 15 skills
- [Delivery Team Skills](#delivery-team-skills) - 4 skills

---

## Marketing Skills

**3 comprehensive marketing skills** covering content creation, demand generation, and product marketing strategy.

### 📝 Content Creator
**Status:** ✅ Production Ready | **Version:** 1.0

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks.

**What's Included:**
- **Brand Voice Analyzer** - Analyze text for tone, formality, and readability (Python CLI)
- **SEO Optimizer** - Comprehensive SEO scoring and optimization recommendations (Python CLI)
- **Brand Guidelines** - 5 personality archetypes and voice framework
- **Content Frameworks** - 15+ templates (blog posts, emails, social media, video scripts)
- **Social Media Optimization** - Platform-specific guides for LinkedIn, Twitter/X, Instagram, Facebook, TikTok
- **Content Calendar Template** - Monthly planning and distribution framework

**Learn More:** [skills/marketing-team/content-creator/SKILL.md](../skills/marketing-team/content-creator/SKILL.md)

---

### 🎯 Marketing Demand & Acquisition
**Status:** ✅ Production Ready | **Version:** 1.0

Expert demand generation, paid media, SEO, and partnerships for Series A+ startups.

**What's Included:**
- **CAC Calculator** - Calculate channel-specific and blended customer acquisition cost (Python CLI)
- **Full-Funnel Strategy** - TOFU → MOFU → BOFU frameworks
- **Channel Playbooks** - LinkedIn Ads, Google Ads, Meta, SEO, Partnerships
- **HubSpot Integration** - Campaign tracking, attribution, lead scoring
- **International Expansion** - EU vs US vs Canada tactics
- **Performance Benchmarks** - B2B SaaS CAC and conversion benchmarks

**Learn More:** [skills/marketing-team/marketing-demand-acquisition/SKILL.md](../skills/marketing-team/marketing-demand-acquisition/SKILL.md)

---

### 🚀 Marketing Strategy & Product Marketing
**Status:** ✅ Production Ready | **Version:** 1.0

Product marketing, positioning, GTM strategy, and competitive intelligence.

**What's Included:**
- **ICP Definition** - Firmographics and psychographics frameworks
- **Positioning** - April Dunford positioning methodology
- **GTM Strategy** - PLG, Sales-Led, and Hybrid motion playbooks
- **Launch Plans** - 90-day product launch frameworks (Tier 1/2/3)
- **Competitor Battle Cards** - Head-to-head comparison templates
- **Pricing Strategy** - Value-based and competitive pricing models
- **Messaging Frameworks** - Before/After/Bridge and Hero's Journey

**Learn More:** [skills/marketing-team/marketing-strategy-product-marketing/SKILL.md](../skills/marketing-team/marketing-strategy-product-marketing/SKILL.md)

---

## Product Team Skills

**6 comprehensive product skills** covering product management, agile practices, strategy, UX research, UI design, and business analysis.

### 📊 Product Manager Toolkit
**Status:** ✅ Production Ready | **Version:** 1.0

RICE prioritization, customer discovery, PRD templates, and OKR frameworks for product leaders.

**What's Included:**
- **RICE Prioritizer** - Feature prioritization with reach/impact/confidence/effort scoring (Python CLI)
- **Customer Interview Analyzer** - Extract pain points, feature requests, sentiment (Python CLI)
- **PRD Template** - Comprehensive product requirements document
- **OKR Framework** - Objectives and key results for product teams
- **Discovery Frameworks** - Jobs-to-be-Done, Customer Journey Mapping
- **Product Analytics** - Retention, Activation, Engagement metrics
- **Roadmap Templates** - Now/Next/Later and quarterly planning

**Learn More:** [skills/product-team/product-manager-toolkit/SKILL.md](../skills/product-team/product-manager-toolkit/SKILL.md)

---

### 📋 Agile Product Owner
**Status:** ✅ Production Ready | **Version:** 1.0

User story generation, sprint planning, backlog refinement, and velocity tracking for agile teams.

**What's Included:**
- **User Story Generator** - Generate well-formed user stories with acceptance criteria (Python CLI)
- **Story Point Estimator** - T-shirt sizing and planning poker frameworks (Python CLI)
- **Sprint Planning Templates** - Sprint goals, capacity planning, retrospectives
- **Backlog Refinement** - DEEP principles (Detailed, Estimated, Emergent, Prioritized)
- **Velocity Tracking** - Sprint velocity analysis and forecasting
- **Definition of Done** - Team agreements and quality gates
- **Release Planning** - Multi-sprint release roadmaps

**Learn More:** [skills/product-team/agile-product-owner/SKILL.md](../skills/product-team/agile-product-owner/SKILL.md)

---

### 🎯 Product Strategist
**Status:** ✅ Production Ready | **Version:** 1.0

Market analysis, competitive intelligence, product vision, and go-to-market strategy.

**What's Included:**
- **Market Opportunity Calculator** - TAM/SAM/SOM analysis (Python CLI)
- **Porter's Five Forces** - Industry competitive analysis framework
- **Product Vision Template** - North Star metrics and vision statements
- **GTM Strategy** - Go-to-market playbooks for different product types
- **Competitive Analysis** - Feature comparison and SWOT analysis
- **Business Model Canvas** - Lean startup methodology
- **Product-Market Fit** - Sean Ellis test and PMF metrics

**Learn More:** [skills/product-team/product-strategist/SKILL.md](../skills/product-team/product-strategist/SKILL.md)

---

### 🔍 UX Researcher
**Status:** ✅ Production Ready | **Version:** 1.0

User research, usability testing, interview guides, and insight synthesis for UX teams.

**What's Included:**
- **Research Plan Template** - Study design, participant recruitment, analysis plan
- **Interview Guide Generator** - Create structured interview scripts (Python CLI)
- **Usability Test Scripts** - Task-based testing frameworks
- **Affinity Mapping** - Pattern identification and insight synthesis
- **Persona Templates** - User persona creation with jobs-to-be-done
- **Prototype Testing** - Moderated and unmoderated testing guides
- **Research Repository** - Organize and share research findings

**Learn More:** [skills/product-team/ux-researcher/SKILL.md](../skills/product-team/ux-researcher/SKILL.md)

---

### 🎨 UI Designer
**Status:** ✅ Production Ready | **Version:** 1.0

Design systems, component libraries, accessibility standards, and visual design for product teams.

**What's Included:**
- **Design System Template** - Color, typography, spacing, components
- **Component Library** - Atomic design methodology (atoms, molecules, organisms)
- **Accessibility Checker** - WCAG 2.1 AA compliance verification (Python CLI)
- **Design Tokens** - Cross-platform design token management
- **Responsive Design** - Mobile-first and adaptive design patterns
- **Style Guide** - Visual language and brand consistency
- **Handoff Documentation** - Designer-to-developer collaboration

**Learn More:** [skills/product-team/ui-designer/SKILL.md](../skills/product-team/ui-designer/SKILL.md)

---

### 📊 Business Analyst Toolkit
**Status:** ✅ Production Ready | **Version:** 1.0

Business process analysis, workflow mapping, gap identification, and improvement planning for operational efficiency.

**What's Included:**
- **Process Parser** - Parse process documentation and extract structured workflow data (Python CLI)
- **Gap Analyzer** - Identify gaps in process documentation with severity scoring (Python CLI)
- **Stakeholder Mapper** - Map stakeholders and generate engagement strategies (Python CLI)
- **RACI Generator** - Create RACI matrices for role clarity (Python CLI)
- **Charter Builder** - Generate comprehensive process improvement charters (Python CLI)
- **Improvement Planner** - Build phased improvement roadmaps with Gantt charts (Python CLI)
- **KPI Calculator** - Calculate process KPIs and efficiency metrics with trend analysis (Python CLI)
- **Process Charter Template** - Define process scope, objectives, roles, and metrics
- **RACI Matrix Template** - Clarify roles and responsibilities across activities
- **Improvement Proposal Template** - Build comprehensive business case with ROI analysis
- **Stakeholder Analysis Template** - Map stakeholder landscape and develop engagement strategies

**Learn More:** [skills/product-team/business-analyst-toolkit/SKILL.md](../skills/product-team/business-analyst-toolkit/SKILL.md)

---

## Engineering Team Skills

**15 comprehensive engineering skills** covering code review, architecture, backend, frontend, fullstack, DevOps, security, QA, AI/ML, data, and CTO advisory.

### 🔍 Code Reviewer
**Status:** ✅ Production Ready | **Version:** 1.0

Systematic code review frameworks, security checklist, and pull request templates.

**What's Included:**
- **Code Quality Analyzer** - Analyze code complexity, maintainability, security (Python CLI)
- **Review Checklist** - 50+ point code review checklist
- **PR Templates** - Comprehensive pull request documentation
- **Security Review** - OWASP Top 10 vulnerability detection
- **Performance Review** - Time/space complexity analysis
- **Testing Review** - Unit, integration, e2e test coverage
- **Architecture Review** - Design patterns and SOLID principles

**Learn More:** [skills/engineering-team/code-reviewer/SKILL.md](../skills/engineering-team/code-reviewer/SKILL.md)

---

### 🏗️ Senior Architect
**Status:** ✅ Production Ready | **Version:** 1.0

Architecture analysis, system design, ADRs, and C4 diagrams for technical architects.

**What's Included:**
- **Project Architect** - Analyze codebase structure, patterns, dependencies (Python CLI)
- **Dependency Analyzer** - Identify circular dependencies and coupling (Python CLI)
- **Architecture Patterns** - Microservices, CQRS, Event Sourcing, Hexagonal
- **ADR Template** - Architecture Decision Records documentation
- **C4 Diagrams** - Context, Container, Component, Code visualization
- **Design Reviews** - Trade-off analysis and technical decision frameworks
- **Scalability Patterns** - Caching, sharding, load balancing strategies

**Learn More:** [skills/engineering-team/senior-architect/SKILL.md](../skills/engineering-team/senior-architect/SKILL.md)

---

### ⚙️ Senior Backend Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

API design, database optimization, caching strategies, and backend best practices.

**What's Included:**
- **API Design Guide** - RESTful API design principles and GraphQL patterns
- **Database Schema Validator** - Schema design review and normalization (Python CLI)
- **Performance Profiler** - Query optimization and indexing strategies (Python CLI)
- **Caching Patterns** - Redis, Memcached, CDN strategies
- **Background Jobs** - Queue management (Sidekiq, Celery, Bull)
- **Rate Limiting** - Token bucket and sliding window algorithms
- **Monitoring** - APM, logging, alerting best practices

**Learn More:** [skills/engineering-team/senior-backend/SKILL.md](../skills/engineering-team/senior-backend/SKILL.md)

---

### 🎨 Senior Frontend Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

React/Vue/Angular patterns, state management, performance optimization, and accessibility.

**What's Included:**
- **Component Library Generator** - Scaffold component structure (Python CLI)
- **Bundle Analyzer** - Webpack/Vite bundle size optimization (Python CLI)
- **React Patterns** - Hooks, Context, Custom Hooks, HOCs, Render Props
- **State Management** - Redux, Zustand, Jotai, Recoil patterns
- **Performance** - Code splitting, lazy loading, memoization
- **Testing** - Jest, React Testing Library, Playwright patterns
- **Accessibility** - ARIA, keyboard navigation, screen reader optimization

**Learn More:** [skills/engineering-team/senior-frontend/SKILL.md](../skills/engineering-team/senior-frontend/SKILL.md)

---

### 🌐 Senior Fullstack Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Full-stack architecture, API integration, database design, and deployment automation.

**What's Included:**
- **Project Scaffolder** - Generate full-stack project structure (Python CLI)
- **Code Quality Analyzer** - Comprehensive code quality assessment (Python CLI)
- **Full-Stack Patterns** - Next.js, Remix, SvelteKit architectures
- **API Integration** - REST, GraphQL, tRPC, gRPC patterns
- **Database Design** - PostgreSQL, MongoDB, Redis best practices
- **Authentication** - JWT, OAuth, SAML, passwordless patterns
- **Deployment** - Docker, Kubernetes, serverless architectures

**Learn More:** [skills/engineering-team/senior-fullstack/SKILL.md](../skills/engineering-team/senior-fullstack/SKILL.md)

---

### ☁️ Senior DevOps Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

CI/CD pipelines, infrastructure as code, monitoring, and reliability engineering.

**What's Included:**
- **CI/CD Pipeline Generator** - GitHub Actions, GitLab CI, CircleCI templates (Python CLI)
- **Infrastructure Validator** - Terraform/CloudFormation validation (Python CLI)
- **Docker Best Practices** - Dockerfile optimization and multi-stage builds
- **Kubernetes Patterns** - Deployments, Services, Ingress, ConfigMaps
- **Monitoring Stack** - Prometheus, Grafana, ELK, DataDog setup
- **Incident Response** - On-call playbooks and runbooks
- **SRE Practices** - SLO/SLI/SLA definition and error budgets

**Learn More:** [skills/engineering-team/senior-devops/SKILL.md](../skills/engineering-team/senior-devops/SKILL.md)

---

### 🔒 Senior Security Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Security auditing, vulnerability scanning, penetration testing, and secure coding practices.

**What's Included:**
- **Security Auditor** - OWASP Top 10 vulnerability scanning (Python CLI)
- **Dependency Scanner** - CVE detection and SBOM generation (Python CLI)
- **Secure Coding** - Input validation, authentication, authorization patterns
- **Penetration Testing** - OWASP ZAP, Burp Suite, sqlmap guides
- **Threat Modeling** - STRIDE framework and attack tree analysis
- **Security Headers** - CSP, HSTS, X-Frame-Options configuration
- **Secrets Management** - HashiCorp Vault, AWS Secrets Manager

**Learn More:** [skills/engineering-team/senior-security/SKILL.md](../skills/engineering-team/senior-security/SKILL.md)

---

### 🛡️ Senior SecOps Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Security operations, incident response, threat hunting, and compliance automation.

**What's Included:**
- **Incident Response Playbook** - Security incident handling procedures
- **Log Analyzer** - Security log analysis and anomaly detection (Python CLI)
- **Threat Intelligence** - MITRE ATT&CK framework and IOC management
- **SIEM Configuration** - Splunk, Elastic Security, Sentinel setup
- **Compliance Automation** - SOC 2, ISO 27001, GDPR checklists
- **Vulnerability Management** - Patch management and CVE tracking
- **Security Metrics** - MTTD, MTTR, security posture dashboards

**Learn More:** [skills/engineering-team/senior-secops/SKILL.md](../skills/engineering-team/senior-secops/SKILL.md)

---

### ✅ Senior QA Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Test automation, quality gates, regression testing, and QA strategy.

**What's Included:**
- **Test Plan Generator** - Create comprehensive test plans (Python CLI)
- **Coverage Analyzer** - Identify untested code paths (Python CLI)
- **Testing Pyramid** - Unit, integration, e2e test strategy
- **Automation Frameworks** - Selenium, Playwright, Cypress patterns
- **API Testing** - Postman, REST Assured, Pact contract testing
- **Performance Testing** - JMeter, k6, Locust load testing
- **Quality Metrics** - Defect density, test coverage, flakiness tracking

**Learn More:** [skills/engineering-team/senior-qa/SKILL.md](../skills/engineering-team/senior-qa/SKILL.md)

---

### 🤖 Senior ML Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Machine learning pipelines, model training, MLOps, and production ML systems.

**What's Included:**
- **Model Evaluator** - Evaluate model performance metrics (Python CLI)
- **Feature Engineering** - Feature selection, transformation, encoding
- **ML Pipelines** - Kubeflow, MLflow, Airflow orchestration
- **Model Serving** - TensorFlow Serving, TorchServe, FastAPI
- **Experiment Tracking** - Weights & Biases, Neptune, MLflow
- **Data Versioning** - DVC, LakeFS, Delta Lake
- **Model Monitoring** - Drift detection, A/B testing, shadow deployment

**Learn More:** [skills/engineering-team/senior-ml-engineer/SKILL.md](../skills/engineering-team/senior-ml-engineer/SKILL.md)

---

### 📊 Senior Data Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Data pipelines, ETL/ELT, data warehousing, and analytics engineering.

**What's Included:**
- **Pipeline Generator** - Create data pipeline scaffolding (Python CLI)
- **Data Quality Checker** - Data validation and profiling (Python CLI)
- **ETL Patterns** - Airflow, Prefect, Dagster workflows
- **Data Warehousing** - Snowflake, BigQuery, Redshift design
- **Data Modeling** - Kimball dimensional modeling, Data Vault
- **Stream Processing** - Kafka, Flink, Spark Streaming
- **Data Governance** - Metadata management, lineage, quality

**Learn More:** [skills/engineering-team/senior-data-engineer/SKILL.md](../skills/engineering-team/senior-data-engineer/SKILL.md)

---

### 📈 Senior Data Scientist
**Status:** ✅ Production Ready | **Version:** 1.0

Statistical analysis, predictive modeling, experimentation, and data storytelling.

**What's Included:**
- **Statistical Test Runner** - Hypothesis testing automation (Python CLI)
- **Experiment Designer** - A/B test sample size and power analysis (Python CLI)
- **Statistical Methods** - T-tests, ANOVA, regression, time series
- **Causal Inference** - Propensity scoring, difference-in-differences
- **Experimentation** - A/B testing, multi-armed bandits, sequential testing
- **Data Visualization** - Matplotlib, Seaborn, Plotly best practices
- **Reporting** - Jupyter notebooks, dashboards, stakeholder communication

**Learn More:** [skills/engineering-team/senior-data-scientist/SKILL.md](../skills/engineering-team/senior-data-scientist/SKILL.md)

---

### 👁️ Senior Computer Vision Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

Image processing, object detection, segmentation, and production CV systems.

**What's Included:**
- **Image Augmentation Pipeline** - Data augmentation strategies (Python CLI)
- **Model Benchmarking** - Compare CV model performance (Python CLI)
- **Object Detection** - YOLO, Faster R-CNN, EfficientDet
- **Segmentation** - U-Net, Mask R-CNN, DeepLab
- **Image Classification** - ResNet, EfficientNet, Vision Transformers
- **Video Processing** - Frame extraction, temporal modeling
- **Edge Deployment** - ONNX, TensorRT, Core ML optimization

**Learn More:** [skills/engineering-team/senior-computer-vision/SKILL.md](../skills/engineering-team/senior-computer-vision/SKILL.md)

---

### ✍️ Senior Prompt Engineer
**Status:** ✅ Production Ready | **Version:** 1.0

LLM optimization, prompt engineering patterns, evaluation, and production LLM systems.

**What's Included:**
- **Prompt Tester** - Test prompt variations and compare outputs (Python CLI)
- **LLM Evaluator** - Evaluate LLM response quality metrics (Python CLI)
- **Prompt Patterns** - Chain-of-thought, few-shot, self-consistency
- **Prompt Chaining** - Multi-step reasoning and agent workflows
- **Evaluation Frameworks** - BLEU, ROUGE, human evaluation rubrics
- **RAG Patterns** - Retrieval-augmented generation architecture
- **LLM Orchestration** - LangChain, LlamaIndex, Semantic Kernel

**Learn More:** [skills/engineering-team/senior-prompt-engineer/SKILL.md](../skills/engineering-team/senior-prompt-engineer/SKILL.md)

---

### 💼 CTO Advisor
**Status:** ✅ Production Ready | **Version:** 1.0

Technical leadership, engineering strategy, team scaling, and CTO decision-making frameworks.

**What's Included:**
- **Tech Debt Analyzer** - Quantify technical debt and prioritization (Python CLI)
- **Team Capacity Planner** - Engineering hiring and scaling models (Python CLI)
- **Engineering Strategy** - Build vs buy, tech stack selection, architecture decisions
- **Team Scaling** - Hiring, onboarding, org structure (teams of 5-100+)
- **Engineering Metrics** - DORA metrics, velocity, quality indicators
- **Technology Radar** - Adopt, Trial, Assess, Hold framework
- **Risk Management** - Technical risk assessment and mitigation

**Learn More:** [skills/engineering-team/cto-advisor/SKILL.md](../skills/engineering-team/cto-advisor/SKILL.md)

---

## Delivery Team Skills

**4 comprehensive delivery skills** covering Atlassian tools (Jira, Confluence) and agile delivery practices.

### 📋 Jira Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Jira workflows, automation, JQL queries, and project management best practices.

**What's Included:**
- **JQL Query Builder** - Generate complex JQL queries (Python CLI)
- **Workflow Templates** - Issue types, transitions, automation rules
- **Board Configuration** - Scrum, Kanban, custom board setup
- **Automation Rules** - Trigger-action automation patterns
- **Reporting** - Burndown, velocity, cumulative flow diagrams
- **Integration** - GitHub, Slack, Confluence, CI/CD tools
- **Advanced JQL** - Complex queries for reporting and filtering

**Learn More:** [skills/delivery-team/jira-expert/SKILL.md](../skills/delivery-team/jira-expert/SKILL.md)

---

### 📚 Confluence Expert
**Status:** ✅ Production Ready | **Version:** 1.0

Documentation strategy, space templates, macros, and knowledge management.

**What's Included:**
- **Template Generator** - Create custom Confluence templates (Python CLI)
- **Space Architecture** - Documentation hierarchy and organization
- **Page Templates** - Meeting notes, RFCs, runbooks, post-mortems
- **Macros & Formatting** - Advanced Confluence markup
- **Search Optimization** - Improve content discoverability
- **Access Control** - Space permissions and restrictions
- **Integration** - Jira, Slack, draw.io, Gliffy

**Learn More:** [skills/delivery-team/confluence-expert/SKILL.md](../skills/delivery-team/confluence-expert/SKILL.md)

---

### 🏃 Scrum Master
**Status:** ✅ Production Ready | **Version:** 1.0

Scrum ceremonies, team facilitation, impediment removal, and agile coaching.

**What's Included:**
- **Sprint Retrospective Generator** - Retrospective formats and activities (Python CLI)
- **Velocity Tracker** - Team velocity and forecasting (Python CLI)
- **Scrum Ceremonies** - Sprint planning, daily standup, review, retro
- **Facilitation Techniques** - Dot voting, 1-2-4-All, lean coffee
- **Impediment Tracking** - Blocker identification and resolution
- **Metrics** - Velocity, sprint goals, team health
- **Team Building** - Psychological safety, team agreements

**Learn More:** [skills/delivery-team/scrum-master/SKILL.md](../skills/delivery-team/scrum-master/SKILL.md)

---

### 📊 Senior PM (Delivery)
**Status:** ✅ Production Ready | **Version:** 1.0

Project management, resource planning, stakeholder management, and delivery excellence.

**What's Included:**
- **Resource Planner** - Team capacity and allocation planning (Python CLI)
- **Risk Register** - Risk identification and mitigation tracking (Python CLI)
- **Project Planning** - Gantt charts, critical path, dependencies
- **Resource Management** - Capacity planning, allocation optimization
- **Stakeholder Management** - Communication plans, RACI matrices
- **Status Reporting** - Executive dashboards, progress tracking
- **Change Management** - Change request process and impact analysis

**Learn More:** [skills/delivery-team/senior-pm/SKILL.md](../skills/delivery-team/senior-pm/SKILL.md)

---

## Related Documentation

- [Quick Start Guide](QUICK_START.md) - Get started in 5 minutes
- [Usage Guide](USAGE.md) - Detailed usage examples and workflows
- [Agent Catalog](AGENTS_CATALOG.md) - 27 workflow orchestrator agents
- [Installation Guide](INSTALL.md) - Complete setup instructions

---

**Last Updated:** November 17, 2025
**Total Skills:** 42 production-ready skills
**Total CLI Tools:** 53 Python automation tools
