---

# === CORE IDENTITY ===
name: senior-architect
title: Senior Architect Skill Package
description: Comprehensive software architecture skill for designing scalable, maintainable systems using ReactJS, NextJS, NodeJS, Express, React Native, Swift, Kotlin, Flutter, Postgres, GraphQL, Go, Python. Includes architecture diagram generation, system design patterns, tech stack decision frameworks, and dependency analysis. Use when designing system architecture, making technical decisions, creating architecture diagrams, evaluating trade-offs, or defining integration patterns.
domain: engineering
subdomain: system-architecture

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "TODO: Quantify time savings"
frequency: "TODO: Estimate usage frequency"
use-cases:
  - Designing scalable system architectures for cloud-native applications
  - Evaluating technology stacks and making evidence-based decisions
  - Creating comprehensive architecture documentation with diagrams
  - Reviewing existing architectures for performance and security

# === RELATIONSHIPS ===
related-agents: []
related-skills: []
related-commands: []
orchestrated-by: []

# === TECHNICAL ===
dependencies:
  scripts: []
  references: []
  assets: []
compatibility:
  python-version: 3.8+
  platforms: [macos, linux, windows]
tech-stack: [Python 3.8+, Markdown]

# === EXAMPLES ===
examples:
  -
    title: Example Usage
    input: "TODO: Add example input for senior-architect"
    output: "TODO: Add expected output"

# === ANALYTICS ===
stats:
  downloads: 0
  stars: 0
  rating: 0.0
  reviews: 0

# === VERSIONING ===
version: v1.0.0
author: Claude Skills Team
contributors: []
created: 2025-10-19
updated: 2025-11-23
license: MIT

# === DISCOVERABILITY ===
tags:
  - analysis
  - architect
  - architecture
  - design
  - engineering
  - senior
featured: false
verified: true
---


# Senior Architect

Complete toolkit for senior architect with modern tools and best practices.

## Overview

This skill provides comprehensive system architecture capabilities through three core Python automation tools and extensive reference documentation. Whether designing microservices architectures, making technology stack decisions, or optimizing system performance, this skill delivers production-ready architectural patterns and automated analysis.

Senior architects use this skill to design scalable, maintainable systems across modern tech stacks including React, Next.js, Node.js, GraphQL, PostgreSQL, Go, Python, and cloud platforms (AWS, GCP, Azure). The skill covers microservices, clean architecture, domain-driven design, API design, performance optimization, and infrastructure planning.

**Core Value:** Accelerate architecture design by 60%+ while improving system scalability, maintainability, and performance through proven patterns and automated analysis tools.

## Quick Start

### Main Capabilities

This skill provides three core capabilities through automated scripts:

```bash
# Script 1: Architecture Diagram Generator
python scripts/architecture_diagram_generator.py [options]

# Script 2: Project Architect
python scripts/project_architect.py [options]

# Script 3: Dependency Analyzer
python scripts/dependency_analyzer.py [options]
```

## Core Capabilities

- **System Architecture Design** - Design scalable, maintainable systems using microservices, clean architecture, and domain-driven design patterns
- **Technology Stack Decision Making** - Evaluate and select optimal technologies (React, Next.js, Node.js, GraphQL, PostgreSQL, Go, Python) based on requirements
- **Architecture Diagram Generation** - Automated creation of system architecture diagrams showing components, data flow, and integration patterns
- **Dependency Analysis** - Analyze and optimize service dependencies, identify circular dependencies, and improve modularity
- **Performance & Scalability Planning** - Design for horizontal scaling, caching strategies, database optimization, and load balancing
- **Integration Pattern Design** - Define API contracts, event-driven architectures, and service communication patterns

## Python Tools

### 1. Architecture Diagram Generator

Automated tool for architecture diagram generator tasks.

**Features:**
- Automated scaffolding
- Best practices built-in
- Configurable templates
- Quality checks

**Usage:**
```bash
python scripts/architecture_diagram_generator.py <project-path> [options]
```

### 2. Project Architect

Comprehensive analysis and optimization tool.

**Features:**
- Deep analysis
- Performance metrics
- Recommendations
- Automated fixes

**Usage:**
```bash
python scripts/project_architect.py <target-path> [--verbose]
```

### 3. Dependency Analyzer

Advanced tooling for specialized tasks.

**Features:**
- Expert-level automation
- Custom configurations
- Integration ready
- Production-grade output

**Usage:**
```bash
python scripts/dependency_analyzer.py [arguments] [options]
```

## Reference Documentation

### Architecture Patterns

Comprehensive guide available in `references/architecture_patterns.md`:

- Detailed patterns and practices
- Code examples
- Best practices
- Anti-patterns to avoid
- Real-world scenarios

### System Design Workflows

Complete workflow documentation in `references/system_design_workflows.md`:

- Step-by-step processes
- Optimization strategies
- Tool integrations
- Performance tuning
- Troubleshooting guide

### Tech Decision Guide

Technical reference guide in `references/tech_decision_guide.md`:

- Technology stack details
- Configuration examples
- Integration patterns
- Security considerations
- Scalability guidelines

## Tech Stack

**Languages:** TypeScript, JavaScript, Python, Go, Swift, Kotlin
**Frontend:** React, Next.js, React Native, Flutter
**Backend:** Node.js, Express, GraphQL, REST APIs
**Database:** PostgreSQL, Prisma, NeonDB, Supabase
**DevOps:** Docker, Kubernetes, Terraform, GitHub Actions, CircleCI
**Cloud:** AWS, GCP, Azure

## Key Workflows

### 1. System Architecture Design

**Time:** 2-4 hours for initial design

1. **Gather Requirements** - Understand functional and non-functional requirements, constraints, and success criteria
2. **Identify Components** - Break system into services, databases, queues, caches, and external integrations
   ```bash
   # Generate architecture diagram
   python scripts/architecture_diagram_generator.py --requirements requirements.md
   ```
3. **Define Integration Patterns** - Specify API contracts, event schemas, and communication protocols
4. **Analyze Dependencies** - Review service dependencies and data flows
   ```bash
   # Analyze dependencies
   python scripts/dependency_analyzer.py --services services/
   ```
5. **Document Architecture** - Create comprehensive architecture documentation with diagrams and decision records

See [architecture_patterns.md](references/architecture_patterns.md) for detailed patterns and examples.

### 2. Technology Stack Selection

**Time:** 1-2 hours per major technology decision

1. **Define Criteria** - List requirements (performance, scalability, team expertise, ecosystem, cost)
2. **Research Options** - Evaluate 3-5 technology options against criteria
3. **Prototype & Benchmark** - Build proof-of-concept implementations
4. **Document Decision** - Create Architecture Decision Record (ADR) with rationale

See [tech_decision_guide.md](references/tech_decision_guide.md) for evaluation frameworks.

### 3. Microservices Architecture Implementation

**Time:** 1-2 weeks for initial setup

1. **Service Boundary Definition** - Apply domain-driven design to identify bounded contexts
2. **Infrastructure Setup** - Configure Docker, Kubernetes, service mesh, and observability
   ```bash
   # Generate project architecture
   python scripts/project_architect.py --pattern microservices
   ```
3. **API Gateway Configuration** - Setup routing, authentication, rate limiting
4. **Deploy & Monitor** - Deploy services and establish monitoring dashboards

### 4. Performance Optimization

**Time:** 2-3 days per optimization cycle

1. **Establish Baselines** - Measure current performance metrics (latency, throughput, resource usage)
2. **Identify Bottlenecks** - Use profiling tools and analysis scripts
   ```bash
   # Analyze system dependencies and bottlenecks
   python scripts/dependency_analyzer.py --analyze-performance
   ```
3. **Implement Optimizations** - Apply caching, database indexing, query optimization, code improvements
4. **Validate Improvements** - Measure impact and document optimizations

## Development Workflow

### 1. Setup and Configuration

```bash
# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### 2. Run Quality Checks

```bash
# Use the analyzer script
python scripts/project_architect.py .

# Review recommendations
# Apply fixes
```

### 3. Implement Best Practices

Follow the patterns and practices documented in:
- `references/architecture_patterns.md`
- `references/system_design_workflows.md`
- `references/tech_decision_guide.md`

## Best Practices Summary

### Code Quality
- Follow established patterns
- Write comprehensive tests
- Document decisions
- Review regularly

### Performance
- Measure before optimizing
- Use appropriate caching
- Optimize critical paths
- Monitor in production

### Security
- Validate all inputs
- Use parameterized queries
- Implement proper authentication
- Keep dependencies updated

### Maintainability
- Write clear code
- Use consistent naming
- Add helpful comments
- Keep it simple

## Common Commands

```bash
# Development
npm run dev
npm run build
npm run test
npm run lint

# Analysis
python scripts/project_architect.py .
python scripts/dependency_analyzer.py --analyze

# Deployment
docker build -t app:latest .
docker-compose up -d
kubectl apply -f k8s/
```

## Troubleshooting

### Common Issues

Check the comprehensive troubleshooting section in `references/tech_decision_guide.md`.

### Getting Help

- Review reference documentation
- Check script output messages
- Consult tech stack documentation
- Review error logs

## Resources

- Pattern Reference: `references/architecture_patterns.md`
- Workflow Guide: `references/system_design_workflows.md`
- Technical Guide: `references/tech_decision_guide.md`
- Tool Scripts: `scripts/` directory
