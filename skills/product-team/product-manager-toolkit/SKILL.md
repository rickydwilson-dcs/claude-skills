---
name: product-manager-toolkit
description: Comprehensive toolkit for product managers including RICE prioritization, customer interview analysis, PRD templates, discovery frameworks, and go-to-market strategies. Use for feature prioritization, user research synthesis, requirement documentation, and product strategy development.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: product
  domain: product-management
  updated: 2025-11-08
  keywords:
    - RICE prioritization
    - customer interviews
    - feature prioritization
    - PRD templates
    - product discovery
    - go-to-market strategy
    - user research
    - interview analysis
    - sentiment analysis
    - pain points extraction
    - feature requests
    - jobs-to-be-done
    - roadmap planning
    - stakeholder management
    - product strategy
    - opportunity tree
  tech-stack:
    - Python 3.8+
    - CLI
    - CSV processing
    - JSON export
    - NLP sentiment analysis
  python-tools:
    - rice_prioritizer.py
    - customer_interview_analyzer.py
---

# Product Manager Toolkit

Essential tools and frameworks for modern product management, from discovery to delivery. This toolkit provides Python automation tools for prioritization and interview analysis, comprehensive frameworks for decision-making, and battle-tested templates for product documentation.

**What This Skill Provides:**
- RICE prioritization engine with portfolio analysis
- NLP-based customer interview analyzer
- Complete PRD templates and interview guides
- Discovery frameworks (JTBD, Opportunity Trees)
- Metrics frameworks (North Star, Funnels)

**Best For:**
- Feature prioritization and roadmap planning
- User research synthesis and insight extraction
- Requirements documentation (PRDs, user stories)
- Discovery planning and stakeholder alignment

## Quick Start

### Feature Prioritization
```bash
python scripts/rice_prioritizer.py sample  # Create sample CSV
python scripts/rice_prioritizer.py sample_features.csv --capacity 15
```

### Interview Analysis
```bash
python scripts/customer_interview_analyzer.py interview_transcript.txt
```

### PRD Creation
1. Choose template: Standard, One-Page, Agile Epic, or Feature Brief
2. See [templates.md](references/templates.md) for complete formats
3. Fill sections based on discovery work
4. Review with stakeholders and version control

## Core Workflows

### 1. Feature Prioritization Process

**Steps:**
1. Gather feature requests (customer feedback, sales, tech debt, strategic)
2. Score with RICE: `python scripts/rice_prioritizer.py features.csv`
   - Reach: Users affected per quarter
   - Impact: massive/high/medium/low/minimal (3x/2x/1x/0.5x/0.25x)
   - Confidence: high/medium/low (100%/80%/50%)
   - Effort: Person-months
3. Analyze portfolio (quick wins vs big bets)
4. Generate roadmap with capacity planning

**Detailed Methodology:** See [frameworks.md](references/frameworks.md) for RICE, Value vs Effort Matrix, MoSCoW, and Kano Model.

### 2. Customer Discovery Process

**Steps:**
1. Conduct interviews using semi-structured format
2. Analyze insights: `python scripts/customer_interview_analyzer.py transcript.txt`
   - Extracts pain points, feature requests, JTBD, sentiment, themes
3. Synthesize findings across interviews
4. Validate solutions with prototypes

**Interview Scripts:** See [templates.md](references/templates.md) for complete discovery and validation interview guides.

**Discovery Frameworks:** See [frameworks.md](references/frameworks.md) for Customer Interview Guide, Hypothesis Template, and Opportunity Solution Tree.

### 3. PRD Development Process

**Steps:**
1. Choose template based on project size:
   - Standard PRD: Complex features (6-8 weeks)
   - One-Page PRD: Simple features (2-4 weeks)
   - Feature Brief: Exploration phase (1 week)
   - Agile Epic: Sprint-based delivery
2. Structure: Problem → Solution → Success Metrics
3. Collaborate with engineering, design, sales, support

**Complete Templates:** See [templates.md](references/templates.md) for all PRD formats with examples.

## Python Tools

### rice_prioritizer.py
RICE framework implementation with portfolio analysis and roadmap generation.

**Key Features:**
- RICE score calculation
- Portfolio balance (quick wins, big bets, fill-ins, time sinks)
- Quarterly roadmap with capacity planning
- Multiple output formats (text/json/csv)

**Usage:**
```bash
# Basic prioritization
python3 scripts/rice_prioritizer.py features.csv

# With team capacity
python3 scripts/rice_prioritizer.py features.csv --capacity 20

# JSON output for tool integration
python3 scripts/rice_prioritizer.py features.csv --output json -f roadmap.json
```

**CSV Format:**
```csv
name,reach,impact,confidence,effort
User Dashboard,500,2,0.8,5
API Rate Limiting,1000,2,0.9,3
```

**Complete Documentation:** See [tools.md](references/tools.md) for full options, output formats, and integration patterns.

### customer_interview_analyzer.py
NLP-based interview analysis for extracting actionable insights.

**Capabilities:**
- Pain point extraction with severity assessment
- Feature request identification and classification
- Jobs-to-be-done pattern recognition
- Sentiment analysis
- Theme extraction and competitor mentions

**Usage:**
```bash
# Analyze interview
python3 scripts/customer_interview_analyzer.py interview.txt

# JSON output for research tools
python3 scripts/customer_interview_analyzer.py interview.txt --output json -f analysis.json
```

**Complete Documentation:** See [tools.md](references/tools.md) for full capabilities, output formats, and batch analysis workflows.

## Reference Documentation

### Frameworks ([frameworks.md](references/frameworks.md))
Detailed frameworks and methodologies:
- Prioritization: RICE (detailed), Value vs Effort Matrix, MoSCoW, Kano Model
- Discovery: Customer Interview Guide, Hypothesis Template, Opportunity Solution Tree
- Metrics: North Star Framework, Funnel Analysis (AARRR), Feature Success Metrics, Cohort Analysis

### Templates ([templates.md](references/templates.md))
Complete templates and best practices:
- PRD Templates: Standard, One-Page, Agile Epic, Feature Brief
- Interview Guides: Discovery interviews, solution validation
- Best Practices: Writing PRDs, prioritization, discovery, stakeholder management
- Common Pitfalls: What to avoid and how to fix

### Tools ([tools.md](references/tools.md))
Python tool documentation and integrations:
- rice_prioritizer.py: Complete usage, options, output formats
- customer_interview_analyzer.py: Full capabilities and workflows
- Integration Patterns: Jira, ProductBoard, Amplitude, Figma, Dovetail, Slack
- Platform Setup: Step-by-step for each tool
- Troubleshooting: Common issues and solutions

## Integration Points

This toolkit integrates with:
- **Analytics:** Amplitude, Mixpanel, Google Analytics
- **Roadmapping:** ProductBoard, Aha!, Roadmunk
- **Design:** Figma, Sketch, Miro
- **Development:** Jira, Linear, GitHub
- **Research:** Dovetail, UserVoice, Pendo
- **Communication:** Slack, Notion, Confluence

See [tools.md](references/tools.md) for detailed integration workflows and platform-specific setup guides.

## Quick Commands

```bash
# Prioritization
python scripts/rice_prioritizer.py features.csv --capacity 15

# Interview Analysis
python scripts/customer_interview_analyzer.py interview.txt

# Create sample data
python scripts/rice_prioritizer.py sample

# JSON outputs for integration
python scripts/rice_prioritizer.py features.csv --output json
python scripts/customer_interview_analyzer.py interview.txt --output json
```
