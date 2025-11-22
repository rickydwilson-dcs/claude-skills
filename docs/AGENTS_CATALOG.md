# Agent Catalog

**Complete catalog of 28 production agents for Pandora's SDLC (v2.0)**

Agents are workflow orchestrators that intelligently invoke skills, coordinate Python tools, and guide you through complex multi-step processes. While skills provide the tools and knowledge, agents provide the intelligence to use them effectively.

**Validation Status**: 28/28 passing (100%)
**Last Validated**: November 22, 2025

## Validation

All agents pass 9 validation checks:
- ✓ Valid YAML frontmatter with required fields
- ✓ Correct relative paths (`../../skills/`)
- ✓ 4+ documented workflows
- ✓ 2+ integration examples
- ✓ 3+ success metric categories
- ✓ Complete markdown structure
- ✓ Cross-references to related agents

Use `python3 scripts/agent_builder.py --validate <agent-file>` to validate agents.

See [Builder Standards](standards/builder-standards.md) for complete validation criteria.

---

## Table of Contents

- [What Are Agents?](#what-are-agents)
- [Agents vs Skills](#agents-vs-skills)
- [Marketing Agents](#marketing-agents) - 3 agents
- [Product Agents](#product-agents) - 6 agents
- [Engineering Agents](#engineering-agents) - 15 agents
- [Delivery Agents](#delivery-agents) - 4 agents

---

## What Are Agents?

Agents are specialized workflow orchestrators that:
- **Guide multi-step processes** - Walk you through complex tasks step-by-step
- **Invoke skills intelligently** - Know when and how to use the right tools
- **Coordinate Python tools** - Run analysis tools and interpret results
- **Apply domain expertise** - Use knowledge bases to provide context-aware guidance

## Agents vs Skills

| | Skills | Agents |
|---|--------|--------|
| **Purpose** | Provide tools + knowledge + templates | Orchestrate workflows and processes |
| **Scope** | 43 Pandora-focused skills | 28 production agents |
| **Content** | 53 Python CLI tools, 60+ knowledge bases | Guided workflows invoking skills |
| **Usage** | Direct tool execution | Intelligent workflow orchestration |
| **Best For** | Quick analysis, standalone tools | Complex multi-step processes |

**Example:**
- **Skill:** [senior-architect](../skills/engineering-team/senior-architect/SKILL.md) provides `project_architect.py` tool and architecture patterns
- **Agent:** [cs-architect](../agents/engineering/cs-architect.md) guides you through architecture review by intelligently running `project_architect.py`, interpreting results, recommending patterns, and creating ADRs

---

## Marketing Agents

**3 marketing agents** for content creation, demand generation, and product marketing.

### 📝 cs-content-creator
**Domain:** Marketing | **Skills Used:** content-creator

Create SEO-optimized marketing content with brand voice consistency. Guides you through content creation workflows using brand voice analysis, SEO optimization, and platform-specific frameworks.

**Key Workflows:**
- Blog post creation with SEO optimization
- Social media content generation (LinkedIn, Twitter, etc.)
- Email campaign development
- Brand voice analysis and consistency checks

**Python Tools Used:**
- `brand_voice_analyzer.py` - Analyze tone, formality, readability
- `seo_optimizer.py` - SEO scoring and recommendations

[View Agent →](../agents/marketing/cs-content-creator.md)

---

### 🎯 cs-demand-gen-specialist
**Domain:** Marketing | **Skills Used:** marketing-demand-acquisition

Lead generation and conversion funnel optimization for B2B SaaS. Specializes in paid media, SEO strategy, and partnership development.

**Key Workflows:**
- Demand generation campaign planning
- CAC calculation and optimization
- Channel mix strategy (LinkedIn, Google, Meta)
- Conversion funnel analysis

**Python Tools Used:**
- `cac_calculator.py` - Calculate customer acquisition cost

[View Agent →](../agents/marketing/cs-demand-gen-specialist.md)

---

### 🚀 cs-product-marketer
**Domain:** Marketing | **Skills Used:** marketing-strategy-product-marketing

Product positioning, go-to-market strategy, and competitive intelligence. Applies April Dunford positioning methodology and strategic frameworks.

**Key Workflows:**
- Product positioning and messaging
- Go-to-market strategy development
- Competitive battle cards creation
- Launch planning (Tier 1/2/3)

[View Agent →](../agents/marketing/cs-product-marketer.md)

---

## Product Agents

**6 product agents** covering product management, agile practices, strategy, UX research, UI design, and business analysis.

### 📊 cs-product-manager
**Domain:** Product | **Skills Used:** product-manager-toolkit

RICE prioritization, roadmap generation, and customer discovery. Data-driven product decision-making with Python-powered analysis tools.

**Key Workflows:**
- Feature prioritization using RICE framework
- Customer interview analysis
- Product roadmap creation
- OKR development

**Python Tools Used:**
- `rice_prioritizer.py` - RICE scoring and portfolio analysis
- `customer_interview_analyzer.py` - Extract pain points and features

[View Agent →](../agents/product/cs-product-manager.md)

---

### 📋 cs-agile-product-owner
**Domain:** Product | **Skills Used:** agile-product-owner

User story generation, backlog management, and sprint planning. Guides agile ceremonies and best practices.

**Key Workflows:**
- User story generation with acceptance criteria
- Sprint planning and capacity calculation
- Backlog refinement and prioritization
- Velocity tracking and forecasting

**Python Tools Used:**
- `user_story_generator.py` - Generate well-formed user stories
- `story_point_estimator.py` - Story point estimation

[View Agent →](../agents/product/cs-agile-product-owner.md)

---

### 🎯 cs-product-strategist
**Domain:** Product | **Skills Used:** product-strategist

Market analysis, competitive intelligence, product vision, and strategic planning. Applies Porter's Five Forces and Business Model Canvas.

**Key Workflows:**
- Market opportunity assessment (TAM/SAM/SOM)
- Competitive analysis and SWOT
- Product vision development
- Go-to-market strategy

**Python Tools Used:**
- `market_opportunity_calculator.py` - TAM/SAM/SOM analysis

[View Agent →](../agents/product/cs-product-strategist.md)

---

### 🔍 cs-ux-researcher
**Domain:** Product | **Skills Used:** ux-researcher

User research, usability testing, interview guides, and insight synthesis. Guides research planning and execution.

**Key Workflows:**
- Research plan creation
- Interview guide generation
- Usability test script development
- Affinity mapping and insight synthesis

**Python Tools Used:**
- `interview_guide_generator.py` - Create structured interview scripts

[View Agent →](../agents/product/cs-ux-researcher.md)

---

### 🎨 cs-ui-designer
**Domain:** Product | **Skills Used:** ui-designer

Design systems, component libraries, accessibility standards, and visual design. Ensures WCAG 2.1 AA compliance.

**Key Workflows:**
- Design system creation
- Component library development
- Accessibility compliance checking
- Design token management

**Python Tools Used:**
- `accessibility_checker.py` - WCAG 2.1 AA compliance verification

[View Agent →](../agents/product/cs-ui-designer.md)

---

### 📊 cs-business-analyst
**Domain:** Product | **Skills Used:** business-analyst-toolkit

Business process analysis, workflow mapping, gap identification, and improvement planning using systematic frameworks and automation tools.

**Key Workflows:**
- End-to-end process improvement analysis
- Cross-functional process design with RACI clarity
- Process performance monitoring and continuous improvement
- Rapid process assessment and prioritization

**Python Tools Used:**
- `process_parser.py` - Parse process documentation and extract structured workflow data
- `gap_analyzer.py` - Identify gaps in process documentation with severity scoring
- `stakeholder_mapper.py` - Map stakeholders and generate engagement strategies
- `raci_generator.py` - Create RACI matrices for role clarity
- `charter_builder.py` - Generate comprehensive process improvement charters
- `improvement_planner.py` - Build phased improvement roadmaps
- `kpi_calculator.py` - Calculate process KPIs and efficiency metrics

[View Agent →](../agents/product/cs-business-analyst.md)

---

## Engineering Agents

**15 engineering agents** covering code review, architecture, backend, frontend, fullstack, DevOps, security, QA, AI/ML, data, and CTO advisory.

### 🔍 cs-code-reviewer
**Domain:** Engineering | **Skills Used:** code-reviewer

Code quality analysis, standards enforcement, and pull request reviews. Systematic 50-point review checklist including security, performance, and architecture.

**Key Workflows:**
- Code quality assessment
- Pull request review
- Security vulnerability detection
- Performance analysis

**Python Tools Used:**
- `code_quality_analyzer.py` - Analyze complexity, maintainability, security

[View Agent →](../agents/engineering/cs-code-reviewer.md)

---

### 🏗️ cs-architect
**Domain:** Engineering | **Skills Used:** senior-architect

System design, architecture patterns, technology evaluation, and technical decision-making. Creates ADRs and C4 diagrams.

**Key Workflows:**
- Architecture review and analysis
- System design and patterns
- Dependency analysis
- ADR (Architecture Decision Records) creation

**Python Tools Used:**
- `project_architect.py` - Analyze codebase structure and patterns
- `dependency_analyzer.py` - Identify circular dependencies

[View Agent →](../agents/engineering/cs-architect.md)

---

### ⚙️ cs-backend-engineer
**Domain:** Engineering | **Skills Used:** senior-backend

API design, database optimization, caching strategies, and backend best practices. RESTful and GraphQL patterns.

**Key Workflows:**
- API design and development
- Database schema design and optimization
- Performance profiling and optimization
- Background job implementation

**Python Tools Used:**
- `database_schema_validator.py` - Schema design review
- `performance_profiler.py` - Query optimization

[View Agent →](../agents/engineering/cs-backend-engineer.md)

---

### 🎨 cs-frontend-engineer
**Domain:** Engineering | **Skills Used:** senior-frontend

React/Vue/Angular patterns, state management, performance optimization, and accessibility. Modern frontend architecture.

**Key Workflows:**
- Component development (React/Vue/Angular)
- State management implementation
- Bundle size optimization
- Accessibility compliance

**Python Tools Used:**
- `component_library_generator.py` - Scaffold component structure
- `bundle_analyzer.py` - Webpack/Vite bundle optimization

[View Agent →](../agents/engineering/cs-frontend-engineer.md)

---

### 🌐 cs-fullstack-engineer
**Domain:** Engineering | **Skills Used:** senior-fullstack

Full-stack architecture, API integration, database design, and deployment automation. Next.js, Remix, T3 Stack expertise.

**Key Workflows:**
- Full-stack project scaffolding
- API integration (REST, GraphQL, tRPC)
- Authentication implementation
- Deployment and DevOps

**Python Tools Used:**
- `project_scaffolder.py` - Generate full-stack project structure
- `code_quality_analyzer.py` - Comprehensive quality assessment

[View Agent →](../agents/engineering/cs-fullstack-engineer.md)

---

### ☁️ cs-devops-engineer
**Domain:** Engineering | **Skills Used:** senior-devops

CI/CD pipelines, infrastructure as code, monitoring, and reliability engineering. Docker, Kubernetes, Terraform expertise.

**Key Workflows:**
- CI/CD pipeline creation (GitHub Actions, GitLab CI)
- Infrastructure as code (Terraform, CloudFormation)
- Monitoring stack setup (Prometheus, Grafana)
- Incident response and SRE practices

**Python Tools Used:**
- `ci_cd_pipeline_generator.py` - Generate pipeline templates
- `infrastructure_validator.py` - Validate IaC configurations

[View Agent →](../agents/engineering/cs-devops-engineer.md)

---

### 🔒 cs-security-engineer
**Domain:** Engineering | **Skills Used:** senior-security

Security auditing, vulnerability scanning, penetration testing, and secure coding practices. OWASP Top 10 expertise.

**Key Workflows:**
- Security audit and vulnerability scanning
- Secure coding review
- Penetration testing
- Threat modeling (STRIDE framework)

**Python Tools Used:**
- `security_auditor.py` - OWASP Top 10 vulnerability scanning
- `dependency_scanner.py` - CVE detection and SBOM generation

[View Agent →](../agents/engineering/cs-security-engineer.md)

---

### 🛡️ cs-secops-engineer
**Domain:** Engineering | **Skills Used:** senior-secops

Security operations, incident response, threat hunting, and compliance automation. SOC 2, ISO 27001, GDPR expertise.

**Key Workflows:**
- Incident response and handling
- Security log analysis
- Threat intelligence integration
- Compliance automation (SOC 2, ISO 27001)

**Python Tools Used:**
- `log_analyzer.py` - Security log analysis and anomaly detection

[View Agent →](../agents/engineering/cs-secops-engineer.md)

---

### ✅ cs-qa-engineer
**Domain:** Engineering | **Skills Used:** senior-qa

Test automation, quality gates, regression testing, and QA strategy. Testing pyramid and automation frameworks.

**Key Workflows:**
- Test plan creation
- Test automation (Selenium, Playwright, Cypress)
- API testing (Postman, REST Assured)
- Performance testing (JMeter, k6)

**Python Tools Used:**
- `test_plan_generator.py` - Create comprehensive test plans
- `coverage_analyzer.py` - Identify untested code paths

[View Agent →](../agents/engineering/cs-qa-engineer.md)

---

### 🤖 cs-ml-engineer
**Domain:** Engineering | **Skills Used:** senior-ml-engineer

Machine learning pipelines, model training, MLOps, and production ML systems. Kubeflow, MLflow expertise.

**Key Workflows:**
- ML pipeline development
- Model training and evaluation
- Model serving and deployment
- Experiment tracking and versioning

**Python Tools Used:**
- `model_evaluator.py` - Evaluate model performance metrics

[View Agent →](../agents/engineering/cs-ml-engineer.md)

---

### 📊 cs-data-engineer
**Domain:** Engineering | **Skills Used:** senior-data-engineer

Data pipelines, ETL/ELT, data warehousing, and analytics engineering. Airflow, Snowflake, BigQuery expertise.

**Key Workflows:**
- Data pipeline development
- ETL/ELT implementation
- Data warehouse design
- Data quality and governance

**Python Tools Used:**
- `pipeline_generator.py` - Create data pipeline scaffolding
- `data_quality_checker.py` - Data validation and profiling

[View Agent →](../agents/engineering/cs-data-engineer.md)

---

### 📈 cs-data-scientist
**Domain:** Engineering | **Skills Used:** senior-data-scientist

Statistical analysis, predictive modeling, experimentation, and data storytelling. A/B testing and causal inference.

**Key Workflows:**
- Statistical hypothesis testing
- A/B test design and analysis
- Predictive modeling
- Data visualization and reporting

**Python Tools Used:**
- `statistical_test_runner.py` - Hypothesis testing automation
- `experiment_designer.py` - A/B test sample size calculation

[View Agent →](../agents/engineering/cs-data-scientist.md)

---

### 👁️ cs-computer-vision
**Domain:** Engineering | **Skills Used:** senior-computer-vision

Image processing, object detection, segmentation, and production CV systems. YOLO, Mask R-CNN, Vision Transformers.

**Key Workflows:**
- Object detection implementation
- Image segmentation
- Video processing
- Edge deployment optimization

**Python Tools Used:**
- `image_augmentation_pipeline.py` - Data augmentation strategies
- `model_benchmarking.py` - Compare CV model performance

[View Agent →](../agents/engineering/cs-computer-vision.md)

---

### ✍️ cs-prompt-engineer
**Domain:** Engineering | **Skills Used:** senior-prompt-engineer

LLM optimization, prompt engineering patterns, evaluation, and production LLM systems. RAG and agent workflows.

**Key Workflows:**
- Prompt engineering and optimization
- LLM evaluation
- RAG (Retrieval-Augmented Generation) implementation
- LLM orchestration (LangChain, LlamaIndex)

**Python Tools Used:**
- `prompt_tester.py` - Test prompt variations
- `llm_evaluator.py` - Evaluate LLM response quality

[View Agent →](../agents/engineering/cs-prompt-engineer.md)

---

### 💼 cs-cto-advisor
**Domain:** Engineering | **Skills Used:** cto-advisor

Technical leadership, engineering strategy, team scaling, and CTO decision-making frameworks. DORA metrics and technology radar.

**Key Workflows:**
- Technical strategy development
- Engineering team scaling
- Tech debt analysis and prioritization
- Engineering metrics (DORA, velocity)

**Python Tools Used:**
- `tech_debt_analyzer.py` - Quantify technical debt
- `team_capacity_planner.py` - Engineering hiring models

[View Agent →](../agents/engineering/cs-cto-advisor.md)

---

## Delivery Agents

**4 delivery agents** covering Atlassian tools (Jira, Confluence) and agile delivery practices.

### 📋 cs-jira-expert
**Domain:** Delivery | **Skills Used:** jira-expert

Jira workflows, automation, JQL queries, and project management best practices. Advanced automation and reporting.

**Key Workflows:**
- Jira workflow configuration
- JQL query building
- Board setup (Scrum, Kanban)
- Automation rule creation

**Python Tools Used:**
- `jql_query_builder.py` - Generate complex JQL queries

[View Agent →](../agents/delivery/cs-jira-expert.md)

---

### 📚 cs-confluence-expert
**Domain:** Delivery | **Skills Used:** confluence-expert

Documentation strategy, space templates, macros, and knowledge management. Advanced Confluence architecture.

**Key Workflows:**
- Space architecture design
- Documentation template creation
- Confluence macro usage
- Search optimization

**Python Tools Used:**
- `template_generator.py` - Create custom Confluence templates

[View Agent →](../agents/delivery/cs-confluence-expert.md)

---

### 🏃 cs-scrum-master
**Domain:** Delivery | **Skills Used:** scrum-master

Scrum ceremonies, team facilitation, impediment removal, and agile coaching. Psychological safety and team health.

**Key Workflows:**
- Scrum ceremony facilitation
- Sprint retrospective facilitation
- Velocity tracking and forecasting
- Team building and coaching

**Python Tools Used:**
- `sprint_retrospective_generator.py` - Retrospective formats
- `velocity_tracker.py` - Team velocity analysis

[View Agent →](../agents/delivery/cs-scrum-master.md)

---

### 📊 cs-senior-pm
**Domain:** Delivery | **Skills Used:** senior-pm

Project management, resource planning, stakeholder management, and delivery excellence. RACI matrices and status reporting.

**Key Workflows:**
- Project planning and scheduling
- Resource allocation and capacity planning
- Risk management
- Stakeholder communication

**Python Tools Used:**
- `resource_planner.py` - Team capacity and allocation planning
- `risk_register.py` - Risk identification and tracking

[View Agent →](../agents/delivery/cs-senior-pm.md)

---

## Related Documentation

- [Skills Catalog](SKILLS_CATALOG.md) - 42 production-ready skills with Python tools
- [Agent Development Guide](../agents/CLAUDE.md) - How to create new agents
- [Agent Template](../templates/agent-template.md) - Agent creation template
- [Usage Guide](USAGE.md) - Detailed usage examples and workflows

---

**Last Updated:** November 22, 2025
**Total Agents:** 28 production agents (v2.0)
**Agent Naming:** cs-* prefix (claude-skills)
