# Competitive Gap Closure Roadmap

**Based on:** Competitive Analysis vs wshobson/agents (85+ agents, 66 plugins)
**Generated:** December 2, 2025

---

## Priority Framework

| Priority | Criteria | Action Timeline |
|----------|----------|-----------------|
| **CRITICAL** | Missing entire domain, large market | This Sprint |
| **HIGH** | Strategic capability gap | This Quarter |
| **MEDIUM** | Enhancement opportunity | Next Quarter |
| **LOW** | Nice to have | Backlog |
| **IRRELEVANT** | Outside our market | Never |

---

## Phase 1: Critical Gaps (This Sprint)

### 1.1 Mobile Development Suite

**Gap:** Zero mobile coverage vs their 4 mobile agents

| New Agent | Description | Effort | Skills to Create |
|-----------|-------------|--------|------------------|
| `cs-mobile-engineer` | React Native + Flutter cross-platform | 13 SP | `senior-mobile` |
| `cs-ios-engineer` | Native Swift/SwiftUI specialist | 8 SP | `senior-ios` |
| `cs-flutter-engineer` | Flutter/Dart multi-platform | 8 SP | `senior-flutter` |

**Python Tools to Build:**
- `mobile_scaffolder.py` - Project structure generation
- `platform_detector.py` - iOS/Android capability detection
- `app_store_validator.py` - Pre-submission checks

**Total Effort:** 29 SP

---

### 1.2 AI-Enhanced Code Review

**Gap:** No AI tool integration (SonarQube, CodeQL, Semgrep references)

| Enhancement | Target Agent | Effort |
|-------------|--------------|--------|
| Add AI-powered patterns section | cs-code-reviewer | 5 SP |
| Add SonarQube/CodeQL/Semgrep integration examples | cs-code-reviewer | 3 SP |
| Document modern AI code review tools | code-reviewer skill references | 2 SP |

**Total Effort:** 10 SP

---

### 1.3 Real-time Streaming for Data

**Gap:** No Kafka/Flink streaming patterns

| Enhancement | Target Agent | Effort |
|-------------|--------------|--------|
| Add Kafka streaming workflows | cs-data-engineer | 5 SP |
| Add Flink processing patterns | cs-data-engineer | 3 SP |
| Create `streaming_pipeline_builder.py` | senior-data-engineer skill | 5 SP |

**Total Effort:** 13 SP

---

## Phase 2: High Priority (This Quarter)

### 2.1 GraphQL Specialist

| New Agent | Description | Effort |
|-----------|-------------|--------|
| `cs-graphql-architect` | Apollo Federation v2, schema design, DataLoader | 8 SP |

**Key Capabilities:**
- Apollo Federation v2 subgraph design
- Schema stitching across teams
- DataLoader N+1 prevention
- Subscription infrastructure
- Field-level authorization

**Python Tools:**
- `schema_analyzer.py` - GraphQL schema validation
- `federation_scaffolder.py` - Subgraph project setup

---

### 2.2 Legacy Modernization

| New Agent | Description | Effort |
|-----------|-------------|--------|
| `cs-legacy-modernizer` | Framework migrations, strangler fig pattern | 8 SP |

**Key Capabilities:**
- Strangler fig pattern implementation
- Framework migrations (jQuery→React, Python 2→3, Java 8→17)
- Monolith to microservices decomposition
- Backward compatibility layers
- Incremental modernization planning

**Python Tools:**
- `migration_analyzer.py` - Codebase migration assessment
- `compatibility_checker.py` - Breaking change detection

---

### 2.3 Observability Engineering

| New Agent | Description | Effort |
|-----------|-------------|--------|
| `cs-observability-engineer` | Prometheus, Grafana, Jaeger, ELK, SLI/SLO | 13 SP |

**Key Capabilities:**
- OpenTelemetry instrumentation
- SLI/SLO/Error budget definition
- Prometheus + Grafana dashboards
- Distributed tracing (Jaeger)
- Log aggregation (ELK/Loki)
- Alerting strategies

**Python Tools:**
- `sli_calculator.py` - Service level indicator computation
- `dashboard_generator.py` - Grafana dashboard scaffolding
- `alert_rule_builder.py` - Prometheus alert configuration

---

### 2.4 Incident Response

| New Agent | Description | Effort |
|-----------|-------------|--------|
| `cs-incident-responder` | Rapid response, SLA tracking, postmortems | 8 SP |

**Key Capabilities:**
- <5 minute initial response workflows
- Severity classification (P0-P4)
- Structured communication templates
- SLA tracking and escalation
- Blameless postmortem facilitation
- Runbook creation

**Python Tools:**
- `incident_tracker.py` - Incident lifecycle management
- `postmortem_generator.py` - Structured postmortem creation
- `sla_monitor.py` - SLA compliance tracking

---

### 2.5 Enterprise Language Specialists

| New Agent | Description | Effort |
|-----------|-------------|--------|
| `cs-java-engineer` | Spring Boot 3.x, virtual threads, enterprise patterns | 13 SP |
| `cs-dotnet-engineer` | C# modern features, .NET 8+, Azure integration | 13 SP |

**Java Capabilities:**
- Spring Boot 3.x / WebFlux
- Virtual threads (Project Loom)
- GraalVM Native Image
- JUnit 5, Testcontainers
- Microservices patterns

**C# Capabilities:**
- C# 12+ modern features
- .NET 8+ patterns
- Azure ecosystem integration
- Entity Framework Core
- xUnit/NUnit testing

---

## Phase 3: Medium Priority (Next Quarter)

### 3.1 Network Engineering

| New Agent | Description | Effort |
|-----------|-------------|--------|
| `cs-network-engineer` | VPC/VNet, service mesh, zero-trust | 8 SP |

**Key Capabilities:**
- Multi-cloud networking (AWS VPC, Azure VNet, GCP VPC)
- Service mesh architecture (Istio, Linkerd)
- Zero-trust network design
- CDN strategy
- Network diagnostics (tcpdump, Wireshark patterns)

---

### 3.2 Interactive Documentation

| Enhancement | Target Agent | Effort |
|-------------|--------------|--------|
| Add Docusaurus/Mintlify integration | cs-technical-writer | 3 SP |
| Add Mermaid diagram generation | cs-technical-writer | 5 SP |
| Create `interactive_docs_builder.py` | technical-writer skill | 5 SP |

---

### 3.3 SEO Content Architecture

| New Agent | Description | Effort |
|-----------|-------------|--------|
| `cs-seo-strategist` | Pillar/cluster model, topic architecture | 5 SP |

**Key Capabilities:**
- Pillar page + topic cluster design
- Internal linking blueprints
- Content gap analysis
- 30-60 day content calendars
- E-E-A-T signal optimization

---

### 3.4 Data Governance

| Enhancement | Target Agent | Effort |
|-------------|--------------|--------|
| Add DataHub/lineage tracking | cs-data-engineer | 5 SP |
| Add metadata management patterns | cs-data-engineer | 3 SP |
| Create `lineage_tracker.py` | senior-data-engineer skill | 5 SP |

---

## Phase 4: Low Priority (Backlog)

| Item | Description | Effort | Notes |
|------|-------------|--------|-------|
| Frontend security specialist | XSS, CSP, clickjacking depth | 5 SP | Could enhance cs-frontend-engineer |
| Performance engineering agent | Load testing, Core Web Vitals | 8 SP | Could enhance cs-qa-engineer |
| Terraform specialist | Dedicated IaC with Terratest | 5 SP | Could enhance cs-devops-engineer |
| Tutorial engineer | Pedagogical content design | 5 SP | Niche use case |
| Hybrid cloud architect | Azure Arc, AWS Outposts | 8 SP | Enterprise niche |
| Feature store patterns | Feast/Tecton integration | 3 SP | Add to cs-ml-engineer |

---

## Explicitly Out of Scope (IRRELEVANT)

These domains are **intentionally not pursued**:

| Domain | Competitor Agents | Rationale |
|--------|-------------------|-----------|
| **Game Development** | minecraft-bukkit-pro, unity-developer | Different market (game studios), different toolchains (Unity, Unreal), different buyer persona |
| **Blockchain/Web3** | blockchain-developer | Niche crypto market, limited enterprise adoption, regulatory uncertainty, specialized smart contract expertise required |
| **Systems Programming** | c-pro, cpp-pro, rust-pro, golang-pro | Targets kernel developers, infrastructure engineers - not product teams. Different skill set, different hiring profile |
| **Embedded/IoT** | arm-cortex-expert | Hardware/firmware market requires physical devices, specialized toolchains (JTAG, oscilloscopes), safety certifications |
| **Quantitative Trading** | quant-analyst, risk-manager | Finance niche with regulatory requirements, specialized math (stochastic calculus), different buyer (hedge funds) |
| **HR/Legal** | hr-pro, legal-advisor | Outside engineering scope, serves HR/legal teams not product teams |
| **Customer/Sales Ops** | customer-support, sales-automator | Not aligned with engineering/product focus, different buyer persona |

**Business Rationale:**
> claude-skills serves **enterprise product teams** building web applications, SaaS products, and business software. Our 4 domains (Engineering, Product, Marketing, Delivery) cover the full product development lifecycle for this audience. Expanding into game dev, crypto, embedded systems, or finance would dilute focus and require expertise we don't have.

---

## Effort Summary

| Phase | Items | Total Effort | Timeline |
|-------|-------|--------------|----------|
| **Phase 1: Critical** | Mobile suite + AI code review + Streaming | 52 SP | This Sprint |
| **Phase 2: High** | GraphQL + Legacy + Observability + Incident + Enterprise langs | 63 SP | This Quarter |
| **Phase 3: Medium** | Network + Docs + SEO + Data governance | 34 SP | Next Quarter |
| **Phase 4: Low** | Backlog items | 34 SP | As capacity allows |

**Grand Total:** 183 SP (~9-12 months at full velocity)

---

## Quick Wins (< 5 SP each)

These can be done immediately with minimal effort:

| Enhancement | Target | Effort |
|-------------|--------|--------|
| Add AI tool references to cs-code-reviewer | References section | 2 SP |
| Add SIEM/SOAR patterns to cs-secops-engineer | References section | 2 SP |
| Add WebAuthn/FIDO2 to cs-security-engineer | References section | 2 SP |
| Add Constitutional AI to cs-prompt-engineer | Workflows section | 3 SP |
| Add Lakehouse patterns to cs-data-engineer | References section | 3 SP |

**Quick Wins Total:** 12 SP (can be done in parallel with Phase 1)

---

## Success Metrics

After completing Phase 1-2:

| Metric | Current | Target |
|--------|---------|--------|
| Strategic gaps | 10 | 3 |
| Domain coverage vs competitor | 60% | 85% |
| Mobile coverage | 0% | 100% |
| Enterprise language coverage | 40% | 80% |
| Agents total | 30 | 40 |
| Python tools total | 82 | 100+ |

---

## Next Steps

1. **Immediate:** Create `cs-mobile-engineer` agent and `senior-mobile` skill
2. **This Week:** Enhance cs-code-reviewer with AI tool patterns
3. **This Sprint:** Add Kafka/Flink streaming to cs-data-engineer
4. **Planning:** Prioritize Phase 2 agents based on user demand signals

---

**Roadmap Owner:** Engineering Team
**Review Cadence:** Monthly
**Last Updated:** December 2, 2025
