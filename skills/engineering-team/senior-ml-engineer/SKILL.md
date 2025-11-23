---
name: senior-ml-engineer
description: World-class ML engineering skill for productionizing ML models, MLOps, and building scalable ML systems. Expertise in PyTorch, TensorFlow, model deployment, feature stores, model monitoring, and ML infrastructure. Includes LLM integration, fine-tuning, RAG systems, and agentic AI. Use when deploying ML models, building ML platforms, implementing MLOps, or integrating LLMs into production systems.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: Engineering
  domain: engineering
  updated: 2025-11-23
  keywords:
  - engineering
  - senior
  - engineer
  tech-stack:
  - Python 3.8+
  - Markdown
  python-tools:
  - ml_monitoring_suite.py
  - model_deployment_pipeline.py
  - rag_system_builder.py
---


license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: engineering
  domain: ml-engineering
  updated: 2025-11-08
  keywords:
    - machine learning
    - ML engineering
    - MLOps
    - model deployment
    - LLM integration
    - PyTorch
    - TensorFlow
    - model monitoring
    - feature stores
    - RAG systems
    - model serving
    - deep learning
    - production ML
    - model scaling
    - agentic AI
  tech-stack:
    - Python
    - PyTorch
    - TensorFlow
    - LangChain
    - LlamaIndex
    - MLflow
    - Docker
    - Kubernetes
    - AWS SageMaker
    - Weights & Biases
  python-tools:
    - model_deployment_pipeline.py
    - rag_system_builder.py
    - ml_monitoring_suite.py

# Senior ML/AI Engineer

World-class senior ml/ai engineer skill for production-grade AI/ML/Data systems.

## Overview

This skill provides world-class ML engineering capabilities through three core Python automation tools and comprehensive reference documentation. Whether productionizing ML models, building MLOps platforms, implementing LLM systems, or deploying scalable ML infrastructure, this skill delivers expert-level solutions.

Senior ML engineers use this skill for model deployment, MLOps pipeline automation, feature stores, model monitoring, LLM integration, fine-tuning, RAG systems, and agentic AI. Expertise covers PyTorch, TensorFlow, LangChain, LlamaIndex, MLflow, model serving, and production ML infrastructure at scale.

**Core Value:** Accelerate ML deployment by 70%+ while improving model reliability, monitoring, and production performance through proven MLOps patterns and automated pipelines.

## Quick Start

### Main Capabilities

```bash
# Core Tool 1
python scripts/model_deployment_pipeline.py --input data/ --output results/

# Core Tool 2  
python scripts/rag_system_builder.py --target project/ --analyze

# Core Tool 3
python scripts/ml_monitoring_suite.py --config config.yaml --deploy
```

## Core Capabilities

- **ML Model Deployment** - Containerized model serving, REST/gRPC APIs, batch inference, real-time prediction pipelines
- **MLOps Infrastructure** - MLflow setup, model versioning, experiment tracking, feature stores, model registry
- **LLM Integration** - OpenAI, Anthropic, open-source LLMs, prompt engineering, fine-tuning, evaluation
- **RAG System Architecture** - Vector databases (Pinecone, Weaviate), embedding generation, retrieval strategies, chunking
- **Model Monitoring** - Drift detection, performance tracking, A/B testing, automated retraining triggers
- **Agentic AI Systems** - Multi-agent workflows, tool calling, state management, LangChain/LlamaIndex orchestration

## Python Tools

### 1. Model Deployment Pipeline

Automate ML model deployment with production-ready serving infrastructure.

**Key Features:**
- Containerized model serving (Docker, Kubernetes)
- REST API generation with FastAPI
- Batch inference pipelines
- Load balancing configuration
- Health checks and monitoring
- Multi-model serving support

**Common Usage:**
```bash
# Deploy model as REST API
python scripts/model_deployment_pipeline.py --model model.pkl --framework sklearn --port 8000

# Deploy to Kubernetes
python scripts/model_deployment_pipeline.py --model model.pth --framework pytorch --deploy k8s

# Batch inference
python scripts/model_deployment_pipeline.py --model model.pkl --batch --input data.csv --output predictions.csv

# Help
python scripts/model_deployment_pipeline.py --help
```

**Use Cases:**
- Deploying trained models to production
- Setting up model serving infrastructure
- Implementing batch prediction pipelines

### 2. RAG System Builder

Build production-ready RAG (Retrieval Augmented Generation) systems.

**Key Features:**
- Vector database setup (Pinecone, Weaviate, Chroma)
- Document chunking strategies
- Embedding generation (OpenAI, Sentence Transformers)
- Retrieval pipeline configuration
- Query optimization
- LLM integration (OpenAI, Anthropic, open-source)

**Common Usage:**
```bash
# Build RAG system
python scripts/rag_system_builder.py --docs ./documents --vector-db pinecone --llm openai

# Custom chunking
python scripts/rag_system_builder.py --docs ./documents --chunk-size 500 --overlap 50

# Local embeddings
python scripts/rag_system_builder.py --docs ./documents --embeddings sentence-transformers --model all-MiniLM-L6-v2

# Help
python scripts/rag_system_builder.py --help
```

**Use Cases:**
- Building knowledge-base Q&A systems
- Document search and retrieval
- Chatbots with domain knowledge

### 3. ML Monitoring Suite

Comprehensive model monitoring with drift detection and alerting.

**Key Features:**
- Data drift detection (KS test, PSI, KL divergence)
- Model performance tracking
- Prediction distribution monitoring
- Automated alerting thresholds
- Dashboard generation
- Integration with MLflow and Weights & Biases

**Common Usage:**
```bash
# Monitor deployed model
python scripts/ml_monitoring_suite.py --model-endpoint http://api/predict --baseline baseline.csv

# Drift detection
python scripts/ml_monitoring_suite.py --production prod.csv --reference ref.csv --detect-drift

# Setup monitoring dashboard
python scripts/ml_monitoring_suite.py --model model.pkl --deploy-monitoring --grafana

# Help
python scripts/ml_monitoring_suite.py --help
```

**Use Cases:**
- Monitoring production models for drift
- Detecting performance degradation
- Triggering automated retraining

See [mlops_production_patterns.md](references/mlops_production_patterns.md) for comprehensive documentation.

## Core Expertise

This skill covers world-class capabilities in:

- Advanced production patterns and architectures
- Scalable system design and implementation
- Performance optimization at scale
- MLOps and DataOps best practices
- Real-time processing and inference
- Distributed computing frameworks
- Model deployment and monitoring
- Security and compliance
- Cost optimization
- Team leadership and mentoring

## Tech Stack

**Languages:** Python, SQL, R, Scala, Go
**ML Frameworks:** PyTorch, TensorFlow, Scikit-learn, XGBoost
**Data Tools:** Spark, Airflow, dbt, Kafka, Databricks
**LLM Frameworks:** LangChain, LlamaIndex, DSPy
**Deployment:** Docker, Kubernetes, AWS/GCP/Azure
**Monitoring:** MLflow, Weights & Biases, Prometheus
**Databases:** PostgreSQL, BigQuery, Snowflake, Pinecone

## Key Workflows

### 1. ML Model Deployment to Production

**Time:** 2-4 hours for initial deployment

1. **Prepare Model for Deployment** - Save model, dependencies, preprocessing pipelines
2. **Containerize Model** - Create Docker image with serving infrastructure
   ```bash
   # Deploy as REST API
   python scripts/model_deployment_pipeline.py --model model.pkl --framework sklearn --port 8000
   ```
3. **Deploy to Kubernetes** - Setup load balancer, autoscaling, health checks
   ```bash
   # Deploy to K8s
   python scripts/model_deployment_pipeline.py --model model.pth --framework pytorch --deploy k8s
   ```
4. **Setup Monitoring** - Configure drift detection, performance tracking
   ```bash
   # Setup monitoring
   python scripts/ml_monitoring_suite.py --model-endpoint http://api/predict --deploy-monitoring
   ```
5. **Load Testing** - Validate latency, throughput, resource usage

See [mlops_production_patterns.md](references/mlops_production_patterns.md) for deployment patterns.

### 2. RAG System Implementation

**Time:** 3-5 hours for complete system

1. **Prepare Documents** - Collect and preprocess knowledge base
2. **Build RAG Pipeline** - Setup vector DB, embeddings, retrieval
   ```bash
   # Build RAG system
   python scripts/rag_system_builder.py --docs ./documents --vector-db pinecone --llm openai
   ```
3. **Optimize Retrieval** - Tune chunking, embedding models, top-k
4. **LLM Integration** - Connect to LLM API, implement prompt templates
5. **Evaluate Performance** - Test retrieval accuracy, answer quality

See [rag_system_architecture.md](references/rag_system_architecture.md) for RAG patterns.

### 3. MLOps Platform Setup

**Time:** 1-2 days for complete platform

1. **Setup Experiment Tracking** - Configure MLflow or Weights & Biases
2. **Implement Feature Store** - Design feature pipelines, versioning
3. **Create Model Registry** - Centralize model storage, versioning, metadata
4. **Build CI/CD Pipeline** - Automated training, testing, deployment
5. **Deploy Monitoring** - Dashboards, alerting, drift detection
   ```bash
   # Setup monitoring suite
   python scripts/ml_monitoring_suite.py --deploy-monitoring --grafana
   ```

### 4. LLM Fine-Tuning and Deployment

**Time:** 4-8 hours depending on dataset size

1. **Prepare Training Data** - Collect examples, format for fine-tuning
2. **Fine-Tune Model** - Use OpenAI fine-tuning API or local training
3. **Evaluate Performance** - Compare to base model, test on validation set
4. **Deploy Fine-Tuned Model** - Setup serving infrastructure
   ```bash
   # Deploy custom LLM
   python scripts/model_deployment_pipeline.py --model finetuned-model --framework transformers
   ```
5. **Monitor Usage** - Track costs, latency, quality metrics

See [llm_integration_guide.md](references/llm_integration_guide.md) for LLM deployment strategies.

## Reference Documentation

### 1. Mlops Production Patterns

Comprehensive guide available in `references/mlops_production_patterns.md` covering:

- Advanced patterns and best practices
- Production implementation strategies
- Performance optimization techniques
- Scalability considerations
- Security and compliance
- Real-world case studies

### 2. Llm Integration Guide

Complete workflow documentation in `references/llm_integration_guide.md` including:

- Step-by-step processes
- Architecture design patterns
- Tool integration guides
- Performance tuning strategies
- Troubleshooting procedures

### 3. Rag System Architecture

Technical reference guide in `references/rag_system_architecture.md` with:

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

- Advanced Patterns: `references/mlops_production_patterns.md`
- Implementation Guide: `references/llm_integration_guide.md`
- Technical Reference: `references/rag_system_architecture.md`
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
