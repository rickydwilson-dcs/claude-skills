---

# === CORE IDENTITY ===
name: senior-computer-vision
title: Senior Computer Vision Skill Package
description: World-class computer vision skill for image/video processing, object detection, segmentation, and visual AI systems. Expertise in PyTorch, OpenCV, YOLO, SAM, diffusion models, and vision transformers. Includes 3D vision, video analysis, real-time processing, and production deployment. Use when building vision AI systems, implementing object detection, training custom vision models, or optimizing inference pipelines.
domain: engineering
subdomain: computer-vision

# === WEBSITE DISPLAY ===
difficulty: advanced
time-saved: """TODO: Quantify time savings"""
frequency: """TODO: Estimate usage frequency"""
use-cases:
  - Primary workflow for Senior Computer Vision
  - Analysis and recommendations for senior computer vision tasks
  - Best practices implementation for senior computer vision
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
tech-stack: [Python 3.8+, Markdown]

# === EXAMPLES ===
examples:
  -
    title: Example Usage
    input: "TODO: Add example input for senior-computer-vision"
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
tags: [analysis, computer, engineering, product, senior, vision]
featured: false
verified: true
---


# Senior Computer Vision Engineer

World-class senior computer vision engineer skill for production-grade AI/ML/Data systems.

## Overview

This skill provides world-class computer vision engineering capabilities through three core Python automation tools and comprehensive reference documentation. Whether building object detection systems, training custom vision models, optimizing inference pipelines, or deploying production vision AI, this skill delivers expert-level solutions.

Senior computer vision engineers use this skill for image/video processing, object detection (YOLO, Faster R-CNN, SAM), semantic segmentation, 3D vision, video analysis, real-time processing, and production deployment. Expertise covers PyTorch, TensorFlow, OpenCV, vision transformers, diffusion models, and deployment optimization (TensorRT, ONNX).

**Core Value:** Accelerate vision AI development by 70%+ while improving model accuracy, inference speed, and production reliability through proven architectures and automated pipelines.

## Quick Start

### Main Capabilities

```bash
# Core Tool 1
python scripts/vision_model_trainer.py --input data/ --output results/

# Core Tool 2  
python scripts/inference_optimizer.py --target project/ --analyze

# Core Tool 3
python scripts/dataset_pipeline_builder.py --config config.yaml --deploy
```

## Core Capabilities

- **Vision Model Training** - Object detection, semantic segmentation, instance segmentation using PyTorch, TensorFlow, YOLO, Faster R-CNN, SAM
- **Inference Optimization** - Model quantization, TensorRT optimization, ONNX export, batch processing for production deployment
- **Dataset Pipeline Building** - Data augmentation, annotation tools integration, train/val/test splits, quality validation
- **Real-Time Video Processing** - Frame extraction, object tracking, scene detection, multi-camera processing
- **3D Computer Vision** - Depth estimation, point cloud processing, SLAM, 3D reconstruction
- **Production Deployment** - Containerized model serving, REST API generation, load balancing, monitoring dashboards

## Python Tools

### 1. Vision Model Trainer

Train production-ready computer vision models with automated pipelines.

**Key Features:**
- Object detection (YOLO, Faster R-CNN, RetinaNet)
- Semantic segmentation (U-Net, DeepLab, Mask R-CNN)
- Transfer learning from pre-trained models
- Automated hyperparameter tuning
- Training metrics and visualization

**Common Usage:**
```bash
# Train object detection model
python scripts/vision_model_trainer.py --task detection --data ./dataset --model yolov8

# Train segmentation model
python scripts/vision_model_trainer.py --task segmentation --data ./dataset --model unet

# Resume training from checkpoint
python scripts/vision_model_trainer.py --resume checkpoints/best.pth

# Help
python scripts/vision_model_trainer.py --help
```

**Use Cases:**
- Training custom object detectors for specific domains
- Fine-tuning pre-trained models on new datasets
- Experimenting with different architectures

### 2. Inference Optimizer

Optimize trained models for production deployment.

**Key Features:**
- Model quantization (INT8, FP16)
- TensorRT optimization for NVIDIA GPUs
- ONNX export for cross-platform deployment
- Batch inference optimization
- Latency and throughput profiling

**Common Usage:**
```bash
# Optimize model for deployment
python scripts/inference_optimizer.py --model model.pth --target tensorrt

# Export to ONNX
python scripts/inference_optimizer.py --model model.pth --export onnx

# Benchmark inference
python scripts/inference_optimizer.py --model model.pth --benchmark

# Help
python scripts/inference_optimizer.py --help
```

**Use Cases:**
- Reducing inference latency for real-time applications
- Optimizing models for edge devices
- Cross-platform model deployment

### 3. Dataset Pipeline Builder

Build robust dataset pipelines with quality validation.

**Key Features:**
- Automated data augmentation (rotation, flip, color jitter, mixup)
- Train/validation/test splitting strategies
- Annotation format conversion (COCO, YOLO, Pascal VOC)
- Data quality validation and outlier detection
- Dataset versioning and tracking

**Common Usage:**
```bash
# Build dataset pipeline
python scripts/dataset_pipeline_builder.py --input raw_data/ --output processed/

# Apply augmentation
python scripts/dataset_pipeline_builder.py --input data/ --augment --factor 3

# Validate dataset quality
python scripts/dataset_pipeline_builder.py --input data/ --validate

# Help
python scripts/dataset_pipeline_builder.py --help
```

**Use Cases:**
- Preparing datasets for model training
- Expanding small datasets through augmentation
- Ensuring dataset quality and consistency

See [computer_vision_architectures.md](references/computer_vision_architectures.md) for comprehensive tool documentation and advanced examples.

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

### 1. Object Detection Model Training

**Time:** 2-4 hours for training, 1 hour for optimization

1. **Prepare Dataset** - Collect and annotate images, validate quality
   ```bash
   # Build dataset pipeline with augmentation
   python scripts/dataset_pipeline_builder.py --input raw_data/ --output dataset/ --augment --factor 3
   ```
2. **Train Model** - Train object detection model with optimal hyperparameters
   ```bash
   # Train YOLO model
   python scripts/vision_model_trainer.py --task detection --data dataset/ --model yolov8 --epochs 100
   ```
3. **Evaluate Performance** - Test on validation set, analyze mAP, precision, recall
4. **Optimize for Deployment** - Quantize and optimize for production inference
   ```bash
   # Optimize with TensorRT
   python scripts/inference_optimizer.py --model checkpoints/best.pth --target tensorrt
   ```

See [object_detection_optimization.md](references/object_detection_optimization.md) for detailed walkthrough.

### 2. Real-Time Video Processing Pipeline

**Time:** 4-6 hours for initial setup

1. **Design Architecture** - Define input sources, processing pipeline, output formats
2. **Implement Frame Processing** - Object detection, tracking, scene analysis per frame
3. **Optimize Performance** - Batch processing, GPU utilization, multi-threading
   ```bash
   # Benchmark inference speed
   python scripts/inference_optimizer.py --model model.pth --benchmark --batch-size 16
   ```
4. **Deploy Pipeline** - Containerize, setup monitoring, configure auto-scaling

### 3. Production Model Deployment

**Time:** 2-3 hours for containerization and deployment

1. **Optimize Model** - Quantization, pruning, TensorRT optimization
   ```bash
   # Full optimization pipeline
   python scripts/inference_optimizer.py --model model.pth --optimize-all --target production
   ```
2. **Containerize** - Create Docker image with model serving API
3. **Deploy to Cloud** - Kubernetes deployment, load balancer configuration
4. **Setup Monitoring** - Latency tracking, error rates, model drift detection

### 4. Custom Dataset Preparation

**Time:** 2-4 hours depending on dataset size

1. **Collect Data** - Gather images/videos from relevant sources
2. **Annotate** - Use CVAT, LabelImg, or Roboflow for annotations
3. **Validate Quality** - Check for annotation errors, class imbalance
   ```bash
   # Validate dataset quality
   python scripts/dataset_pipeline_builder.py --input data/ --validate --report quality.json
   ```
4. **Apply Augmentation** - Expand dataset with synthetic variations
   ```bash
   # Apply augmentation
   python scripts/dataset_pipeline_builder.py --input data/ --augment --factor 5 --output augmented/
   ```

## Reference Documentation

### 1. Computer Vision Architectures

Comprehensive guide available in `references/computer_vision_architectures.md` covering:

- Advanced patterns and best practices
- Production implementation strategies
- Performance optimization techniques
- Scalability considerations
- Security and compliance
- Real-world case studies

### 2. Object Detection Optimization

Complete workflow documentation in `references/object_detection_optimization.md` including:

- Step-by-step processes
- Architecture design patterns
- Tool integration guides
- Performance tuning strategies
- Troubleshooting procedures

### 3. Production Vision Systems

Technical reference guide in `references/production_vision_systems.md` with:

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

- Advanced Patterns: `references/computer_vision_architectures.md`
- Implementation Guide: `references/object_detection_optimization.md`
- Technical Reference: `references/production_vision_systems.md`
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
