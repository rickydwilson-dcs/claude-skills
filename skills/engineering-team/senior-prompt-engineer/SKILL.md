---

# === CORE IDENTITY ===
name: senior-prompt-engineer
title: Senior Prompt Engineer Skill Package
description: World-class prompt engineering skill for LLM optimization, prompt patterns, structured outputs, and AI product development. Expertise in Claude, GPT-4, prompt design patterns, few-shot learning, chain-of-thought, and AI evaluation. Includes RAG optimization, agent design, and LLM system architecture. Use when building AI products, optimizing LLM performance, designing agentic systems, or implementing advanced prompting techniques.
domain: engineering
subdomain: prompt-engineering

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: "TODO: Quantify time savings"
frequency: "TODO: Estimate usage frequency"
use-cases:
  - Primary workflow for Senior Prompt Engineer
  - Analysis and recommendations for senior prompt engineer tasks
  - Best practices implementation for senior prompt engineer
  - Integration with related skills and workflows

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
tech-stack:
  - Python
  - Claude API
  - GPT-4 API
  - LangChain
  - LlamaIndex
  - Vector databases
  - Pinecone
  - Anthropic SDK
  - OpenAI SDK

# === EXAMPLES ===
examples:
  -
    title: Example Usage
    input: "TODO: Add example input for senior-prompt-engineer"
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
created: 2025-10-20
updated: 2025-11-23
license: MIT

# === DISCOVERABILITY ===
tags:
  - architecture
  - design
  - development
  - engineer
  - engineering
  - optimization
  - performance
  - product
  - prompt
  - senior
featured: false
verified: true
---

# Senior Prompt Engineer

World-class prompt engineering skill for LLM optimization, agentic systems, and AI product development.

## Overview

The Senior Prompt Engineer skill provides comprehensive frameworks, tools, and best practices for building production-grade AI applications with large language models. This skill covers advanced prompting techniques, RAG system optimization, agentic workflows, and LLM evaluation methodologies used by leading AI engineering teams.

Designed for senior engineers building AI products, this skill includes proven patterns for Claude and GPT-4, structured output generation, chain-of-thought reasoning, few-shot learning, and agent orchestration. All content is production-focused with real-world examples from high-scale AI systems.

**Core Value:** Build reliable, high-performance AI applications using advanced prompt engineering, RAG optimization, and agentic architectures that scale to millions of users.

## Core Capabilities

- **Advanced Prompt Patterns** - Chain-of-thought, few-shot learning, structured outputs, role-based prompting, and meta-prompting techniques
- **RAG System Optimization** - Retrieval strategies, chunking algorithms, embedding models, vector database optimization, and relevance scoring
- **Agentic Workflows** - Multi-agent orchestration, tool calling, state management, error handling, and agent evaluation frameworks
- **LLM Evaluation** - Metrics design, benchmark creation, human-in-the-loop evaluation, A/B testing, and performance monitoring
- **Production Best Practices** - Prompt versioning, cost optimization, latency reduction, failover strategies, and observability
- **Model Selection & Tuning** - Claude vs GPT-4 trade-offs, parameter optimization, fine-tuning strategies, and model routing

## Quick Start

### Prompt Optimization
```bash
# Optimize prompts for better performance and cost
python scripts/prompt_optimizer.py --input prompts/ --model claude-3-5-sonnet

# Test prompt variants with A/B testing
python scripts/prompt_optimizer.py --test variants.json --metrics accuracy,cost
```

### RAG System Evaluation
```bash
# Evaluate RAG system performance
python scripts/rag_evaluator.py --target project/ --analyze

# Benchmark retrieval quality
python scripts/rag_evaluator.py --benchmark --dataset eval_data.json
```

### Agent Orchestration
```bash
# Deploy multi-agent workflow
python scripts/agent_orchestrator.py --config config.yaml --deploy

# Monitor agent performance
python scripts/agent_orchestrator.py --monitor --dashboard
```

## Key Workflows

### 1. Optimize Prompt Performance

**Time:** 2-4 hours for comprehensive optimization

1. **Baseline Current Prompt** - Measure existing performance
   - Test with representative dataset (50-100 examples)
   - Measure accuracy, latency, and cost
   - Document failure modes and edge cases

2. **Apply Optimization Techniques** - Improve prompt systematically
   ```bash
   python scripts/prompt_optimizer.py --input current_prompt.txt --optimize
   ```
   - Reduce token count (remove redundancy)
   - Add chain-of-thought reasoning
   - Include few-shot examples
   - Structure output format

3. **A/B Test Variants** - Compare prompt versions
   - Test 3-5 variants with same dataset
   - Measure statistical significance
   - Consider accuracy vs. cost trade-offs

4. **Deploy Winner** - Roll out optimized prompt
   - Implement prompt versioning
   - Set up monitoring and alerts
   - Plan rollback strategy

**Expected Output:** 20-40% cost reduction, 10-25% accuracy improvement, versioned prompt with monitoring.

### 2. Build Production RAG System

**Time:** 1-2 weeks for initial implementation

1. **Design RAG Architecture** - Choose components
   - Vector database (Pinecone, Weaviate, Chroma)
   - Embedding model (OpenAI, Cohere, sentence-transformers)
   - Chunking strategy (semantic, fixed, recursive)
   - Retrieval algorithm (similarity, hybrid, re-ranking)

2. **Implement and Index** - Build RAG pipeline
   - Chunk documents with optimal size (200-500 tokens)
   - Generate embeddings and index
   - Implement retrieval with top-k tuning

3. **Evaluate Performance** - Measure RAG quality
   ```bash
   python scripts/rag_evaluator.py --target rag_system/ --benchmark
   ```
   - Retrieval accuracy (relevant docs in top-k)
   - Answer quality (factual correctness)
   - Latency (end-to-end response time)

4. **Optimize and Deploy** - Improve and launch
   - Tune chunk size and overlap
   - Optimize embedding model and vector DB
   - Implement caching for frequent queries
   - Set up monitoring for retrieval quality

**Expected Output:** Production RAG system with >80% retrieval accuracy, <2s latency, monitoring dashboard.

### 3. Design Multi-Agent System

**Time:** 2-3 weeks for complete implementation

1. **Define Agent Architecture** - Plan agent roles
   - Identify specialized agents (research, writing, coding, QA)
   - Define agent responsibilities and boundaries
   - Design communication protocols
   - Plan state management strategy

2. **Implement Agent Orchestrator** - Build coordination layer
   ```bash
   python scripts/agent_orchestrator.py --config agents.yaml --build
   ```
   - Task routing logic
   - Error handling and retries
   - Agent monitoring and logging
   - Tool calling infrastructure

3. **Test Agent Workflows** - Validate multi-agent behavior
   - Unit test individual agents
   - Integration test agent communication
   - Load test under production conditions
   - Measure end-to-end latency

4. **Deploy and Monitor** - Launch agentic system
   - Gradual rollout with feature flags
   - Real-time monitoring dashboard
   - Alert on agent failures or timeouts
   - Track success rate and user satisfaction

**Expected Output:** Production multi-agent system with orchestration, monitoring, and >95% success rate.

### 4. Evaluate LLM Performance

**Time:** 1 week for comprehensive evaluation

1. **Design Evaluation Framework** - Define metrics
   - Task-specific accuracy metrics
   - Latency and cost budgets
   - Edge case coverage
   - Human evaluation criteria

2. **Create Evaluation Dataset** - Build test set
   - Representative examples (200-500 samples)
   - Edge cases and failure modes
   - Ground truth labels or rubrics
   - Diverse input distributions

3. **Run Automated Evaluation** - Benchmark models
   ```bash
   python scripts/prompt_optimizer.py --eval dataset.json --models claude,gpt4
   ```
   - Compare Claude vs GPT-4 vs other models
   - Measure accuracy, latency, cost
   - Identify model-specific strengths

4. **Conduct Human Evaluation** - Validate with humans
   - HITL evaluation on 50-100 samples
   - Inter-rater reliability (Fleiss' kappa >0.6)
   - Qualitative feedback on failure modes
   - Iterate on prompts based on insights

**Expected Output:** Model selection decision with quantified accuracy/cost trade-offs and evaluation pipeline.

## Python Tools

### prompt_optimizer.py

Optimizes prompts for better accuracy, lower cost, and reduced latency using automated testing and A/B comparison.

**Key Features:**
- Token reduction algorithms (remove redundancy, compress instructions)
- Chain-of-thought injection for complex reasoning
- Few-shot example optimization (select most effective examples)
- Structured output formatting (JSON, XML, YAML)
- A/B testing framework with statistical significance
- Multi-model benchmarking (Claude, GPT-4, custom models)
- Cost and latency profiling

**Common Usage:**
```bash
# Optimize existing prompt
python scripts/prompt_optimizer.py --input prompt.txt --optimize

# A/B test prompt variants
python scripts/prompt_optimizer.py --test variants.json --dataset eval.json

# Benchmark across models
python scripts/prompt_optimizer.py --eval prompt.txt --models claude-3-5-sonnet,gpt-4

# Help and examples
python scripts/prompt_optimizer.py --help
```

**Use Cases:**
- Reducing prompt token count by 30-50% while maintaining accuracy
- Finding optimal few-shot examples from large candidate set
- Comparing Claude vs GPT-4 for specific use case
- Implementing structured JSON outputs reliably

### rag_evaluator.py

Evaluates RAG system performance across retrieval accuracy, answer quality, and latency dimensions.

**Key Features:**
- Retrieval quality metrics (precision@k, recall@k, MRR, NDCG)
- Answer quality evaluation (factual correctness, relevance, completeness)
- Latency profiling (embedding, retrieval, generation breakdown)
- Chunking strategy comparison (semantic vs fixed vs recursive)
- Embedding model benchmarking
- Vector database optimization recommendations
- End-to-end RAG pipeline testing

**Common Usage:**
```bash
# Evaluate RAG system
python scripts/rag_evaluator.py --target rag_project/ --analyze

# Benchmark retrieval quality
python scripts/rag_evaluator.py --benchmark --dataset eval_data.json

# Compare chunking strategies
python scripts/rag_evaluator.py --compare-chunking --sizes 200,500,1000

# Help and examples
python scripts/rag_evaluator.py --help
```

**Use Cases:**
- Diagnosing poor RAG answer quality (retrieval vs generation issues)
- Tuning chunk size and overlap for optimal performance
- Comparing embedding models (OpenAI, Cohere, open-source)
- Identifying retrieval bottlenecks in production

### agent_orchestrator.py

Orchestrates multi-agent workflows with task routing, state management, and error handling for production agentic systems.

**Key Features:**
- Multi-agent coordination (sequential, parallel, hierarchical)
- Tool calling integration (function calling, external APIs)
- State management across agent interactions
- Error handling and retry logic with exponential backoff
- Agent monitoring and observability
- Task routing based on agent specialization
- Cost tracking per agent and workflow

**Common Usage:**
```bash
# Deploy agent system
python scripts/agent_orchestrator.py --config agents.yaml --deploy

# Monitor agent performance
python scripts/agent_orchestrator.py --monitor --dashboard

# Test agent workflow
python scripts/agent_orchestrator.py --test workflow.json --verbose

# Help and examples
python scripts/agent_orchestrator.py --help
```

**Use Cases:**
- Building research assistant with specialized agents (search, summarize, synthesize)
- Implementing code generation pipeline (plan, write, test, review agents)
- Creating customer support system with routing and escalation
- Orchestrating complex multi-step workflows with decision points

## Reference Documentation

### 1. Prompt Engineering Patterns

Comprehensive guide available in `references/prompt_engineering_patterns.md` covering:

- Advanced patterns and best practices
- Production implementation strategies
- Performance optimization techniques
- Scalability considerations
- Security and compliance
- Real-world case studies

### 2. Llm Evaluation Frameworks

Complete workflow documentation in `references/llm_evaluation_frameworks.md` including:

- Step-by-step processes
- Architecture design patterns
- Tool integration guides
- Performance tuning strategies
- Troubleshooting procedures

### 3. Agentic System Design

Technical reference guide in `references/agentic_system_design.md` with:

- System design principles
- Implementation examples
- Configuration best practices
- Deployment strategies
- Monitoring and observability

## Production Patterns

### Pattern 1: Scalable Data Processing

Enterprise-scale data processing with distributed computing:

- Horizontal scaling architecture
- Fault-tolerant design
- Real-time and batch processing
- Data quality validation
- Performance monitoring

### Pattern 2: ML Model Deployment

Production ML system with high availability:

- Model serving with low latency
- A/B testing infrastructure
- Feature store integration
- Model monitoring and drift detection
- Automated retraining pipelines

### Pattern 3: Real-Time Inference

High-throughput inference system:

- Batching and caching strategies
- Load balancing
- Auto-scaling
- Latency optimization
- Cost optimization

## Best Practices

### Development

- Test-driven development
- Code reviews and pair programming
- Documentation as code
- Version control everything
- Continuous integration

### Production

- Monitor everything critical
- Automate deployments
- Feature flags for releases
- Canary deployments
- Comprehensive logging

### Team Leadership

- Mentor junior engineers
- Drive technical decisions
- Establish coding standards
- Foster learning culture
- Cross-functional collaboration

## Performance Targets

**Latency:**
- P50: < 50ms
- P95: < 100ms
- P99: < 200ms

**Throughput:**
- Requests/second: > 1000
- Concurrent users: > 10,000

**Availability:**
- Uptime: 99.9%
- Error rate: < 0.1%

## Security & Compliance

- Authentication & authorization
- Data encryption (at rest & in transit)
- PII handling and anonymization
- GDPR/CCPA compliance
- Regular security audits
- Vulnerability management

## Common Commands

```bash
# Development
python -m pytest tests/ -v --cov
python -m black src/
python -m pylint src/

# Training
python scripts/train.py --config prod.yaml
python scripts/evaluate.py --model best.pth

# Deployment
docker build -t service:v1 .
kubectl apply -f k8s/
helm upgrade service ./charts/

# Monitoring
kubectl logs -f deployment/service
python scripts/health_check.py
```

## Resources

- Advanced Patterns: `references/prompt_engineering_patterns.md`
- Implementation Guide: `references/llm_evaluation_frameworks.md`
- Technical Reference: `references/agentic_system_design.md`
- Automation Scripts: `scripts/` directory

## Senior-Level Responsibilities

As a world-class senior professional:

1. **Technical Leadership**
   - Drive architectural decisions
   - Mentor team members
   - Establish best practices
   - Ensure code quality

2. **Strategic Thinking**
   - Align with business goals
   - Evaluate trade-offs
   - Plan for scale
   - Manage technical debt

3. **Collaboration**
   - Work across teams
   - Communicate effectively
   - Build consensus
   - Share knowledge

4. **Innovation**
   - Stay current with research
   - Experiment with new approaches
   - Contribute to community
   - Drive continuous improvement

5. **Production Excellence**
   - Ensure high availability
   - Monitor proactively
   - Optimize performance
   - Respond to incidents
