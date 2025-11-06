# Usage Guide

Comprehensive examples and workflows for using the Claude Skills Library with Claude AI and Claude Code.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Using Skills Directly](#using-skills-directly)
- [Using Agents](#using-agents)
- [Multi-Agent Workflows](#multi-agent-workflows)
- [CLI Tool Usage](#cli-tool-usage)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Tips & Tricks](#tips--tricks)

---

## Quick Start

### Option 1: Use a Skill Directly (Claude AI)

```markdown
I need help creating marketing content.

Please use the Content Creator skill located at:
marketing-skill/content-creator/SKILL.md

Analyze my brand voice and suggest improvements for this text:
[paste your content]
```

### Option 2: Use an Agent (Claude Code)

```markdown
@cs-content-creator

I need to create a blog post about our new product launch.
The target audience is B2B SaaS companies.
```

### Option 3: Use CLI Tools

```bash
# Analyze brand voice
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  your-content.txt --output json

# Get SEO recommendations
python3 marketing-skill/content-creator/scripts/seo_optimizer.py \
  your-article.md "primary keyword" --output json
```

---

## Using Skills Directly

### With Claude AI

Skills can be used in any Claude AI conversation by referencing the skill documentation:

#### Example 1: Brand Voice Analysis

```markdown
Please reference the Content Creator skill:
File: marketing-skill/content-creator/SKILL.md

Analyze this email for brand voice consistency:

[Email content]

Provide:
1. Tone analysis
2. Formality level
3. Readability score
4. Recommendations
```

#### Example 2: Strategic Planning

```markdown
Use the CEO Advisor skill:
File: c-level-advisor/ceo-advisor/SKILL.md

Help me create an OKR framework for Q1 2026:
- Company goal: Achieve product-market fit
- Team size: 25 people
- ARR target: $2M
```

#### Example 3: Product Prioritization

```markdown
Reference the Product Manager Toolkit skill:
File: product-team/product-manager-toolkit/SKILL.md

I need to prioritize these features using RICE scoring:
1. [Feature description]
2. [Feature description]
3. [Feature description]
```

---

## Using Agents

Agents provide guided workflows and orchestrate skills automatically.

### Available Agents

| Agent | Best For | Example Use Case |
|-------|----------|------------------|
| `cs-content-creator` | Content creation | "Create a blog post about AI" |
| `cs-demand-gen-specialist` | Lead generation | "Plan a demand gen campaign" |
| `cs-ceo-advisor` | Strategic decisions | "Help me set Q1 OKRs" |
| `cs-cto-advisor` | Technical leadership | "Assess our tech debt" |
| `cs-product-manager` | Product decisions | "Prioritize my roadmap" |

### Agent Invocation Examples

#### Marketing Agent: Content Creation

```markdown
@cs-content-creator

Create a blog post about "The Future of AI in Healthcare"

Requirements:
- Target audience: Healthcare CIOs
- Tone: Professional but accessible
- Length: 1200-1500 words
- Include: 2-3 case studies, actionable takeaways
- SEO keyword: "AI healthcare solutions"
```

**What the agent does:**
1. Analyzes your requirements
2. Runs brand voice analyzer on existing content
3. Creates content outline
4. Writes draft
5. Runs SEO optimizer
6. Provides optimization recommendations

#### Marketing Agent: Demand Generation

```markdown
@cs-demand-gen-specialist

Plan a demand generation campaign for our new product launch

Context:
- Product: B2B SaaS analytics platform
- Target: Series A+ startups
- Budget: $50K/month
- Goal: 200 qualified leads/month
- Timeline: Q1 2026
```

**What the agent does:**
1. Analyzes target market
2. Recommends channel mix
3. Calculates CAC expectations
4. Creates funnel strategy
5. Provides campaign timeline
6. Sets up tracking framework

#### C-Level Agent: Strategic Planning

```markdown
@cs-ceo-advisor

Help me prepare for our Q1 board meeting

Context:
- Current ARR: $8M
- Team: 75 people
- Burn rate: $800K/month
- Runway: 18 months
- Goal: Plan for Series B ($25M raise)
```

**What the agent does:**
1. Runs financial scenario analyzer
2. Creates board deck outline
3. Identifies key metrics to highlight
4. Suggests strategic initiatives
5. Provides talking points
6. Creates risk mitigation plan

#### C-Level Agent: Technical Leadership

```markdown
@cs-cto-advisor

We're experiencing scaling issues. Help me assess our architecture.

Context:
- Current users: 50K
- Target: 500K by EOY
- Tech stack: Rails monolith
- Team: 15 engineers
- Pain points: Slow deploys, frequent outages
```

**What the agent does:**
1. Runs tech debt analyzer
2. Identifies architectural bottlenecks
3. Proposes migration strategy
4. Calculates team scaling needs
5. Creates implementation roadmap
6. Provides DORA metrics tracking

#### Product Agent: Feature Prioritization

```markdown
@cs-product-manager

Prioritize my Q1 roadmap using RICE scoring

Features:
1. Advanced analytics dashboard
2. Mobile app
3. API v2
4. Custom integrations
5. SSO/SAML support
```

**What the agent does:**
1. Guides RICE scoring process
2. Runs rice_prioritizer.py tool
3. Analyzes customer interview data
4. Creates prioritized roadmap
5. Generates PRD templates
6. Provides stakeholder communication

---

## Multi-Agent Workflows

Combine multiple agents for complex workflows.

### Workflow 1: Product Launch (3 Agents)

```markdown
# Step 1: Strategic Planning (@cs-ceo-advisor)
@cs-ceo-advisor help me plan our Q1 product launch strategy

# Step 2: Feature Prioritization (@cs-product-manager)
@cs-product-manager prioritize launch features based on strategy

# Step 3: Launch Content (@cs-content-creator)
@cs-content-creator create launch announcement and marketing content
```

### Workflow 2: Fundraising Campaign (2 Agents)

```markdown
# Step 1: Financial Modeling (@cs-ceo-advisor)
@cs-ceo-advisor create financial scenarios for Series B pitch

# Step 2: Marketing Materials (@cs-content-creator)
@cs-content-creator create investor deck content and one-pager
```

### Workflow 3: Tech Debt Resolution (2 Agents)

```markdown
# Step 1: Tech Assessment (@cs-cto-advisor)
@cs-cto-advisor assess our tech debt and scaling needs

# Step 2: Roadmap Planning (@cs-product-manager)
@cs-product-manager prioritize tech debt items in roadmap
```

---

## CLI Tool Usage

### Basic Patterns

#### Pattern 1: Analyze → Report

```bash
# Run analysis
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  content.txt --output json --file analysis.json

# Review results
cat analysis.json | python3 -m json.tool
```

#### Pattern 2: Batch Processing

```bash
# Process multiple files
for file in content/*.txt; do
  python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
    "$file" --output json --file "results/$(basename $file .txt).json"
done
```

#### Pattern 3: Pipeline Integration

```bash
# Export to CSV for Excel/Sheets
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  features.csv --output csv --file priorities.csv

# Open in spreadsheet
open priorities.csv
```

### Advanced Usage

#### Using Multiple Output Formats

```bash
# Get human-readable output
python3 marketing-skill/content-creator/scripts/seo_optimizer.py article.md "keyword"

# Get machine-readable output
python3 marketing-skill/content-creator/scripts/seo_optimizer.py \
  article.md "keyword" --output json

# Export for analysis
python3 marketing-skill/content-creator/scripts/seo_optimizer.py \
  article.md "keyword" --output csv --file seo-analysis.csv
```

#### Verbose Mode for Debugging

```bash
# See detailed execution
python3 c-level-advisor/ceo-advisor/scripts/financial_scenario_analyzer.py \
  scenarios.json --verbose
```

#### Integrating with CI/CD

```bash
# In GitHub Actions or Jenkins
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py \
  docs/content.md --output json | \
  jq '.consistency_score' | \
  awk '{if ($1 < 80) exit 1}'  # Fail if score < 80
```

---

## Best Practices

### 1. Start with Agents for Guidance

```markdown
# Good: Use agent for workflow guidance
@cs-product-manager help me prioritize features

# Also Good: Use skill directly if you know what you want
[Use Product Manager Toolkit skill to run RICE scoring]
```

### 2. Provide Context

```markdown
# Good: Detailed context
@cs-content-creator create a blog post

Context:
- Audience: Technical founders
- Tone: Authoritative but friendly
- Length: 1500 words
- SEO focus: "startup scaling"

# Less Effective: Minimal context
@cs-content-creator write a blog post about scaling
```

### 3. Iterate with Feedback

```markdown
# First attempt
@cs-content-creator [initial request]

# Provide feedback
The tone is too formal. Make it more conversational and add code examples.

# Agent adjusts approach
```

### 4. Combine Tools and Knowledge

```markdown
@cs-ceo-advisor

1. Run financial scenario analyzer on these projections
2. Review strategic frameworks in CEO Advisor skill
3. Create board deck following templates
4. Highlight key metrics for investors
```

### 5. Save and Reuse Workflows

```markdown
# Save successful prompts
I need to repeat this content creation workflow:

@cs-content-creator
[Your proven prompt]

# Modify for new content
```

---

## Common Patterns

### Pattern 1: Content Quality Check

```bash
# 1. Write content
# 2. Check brand voice
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py content.md

# 3. Optimize SEO
python3 marketing-skill/content-creator/scripts/seo_optimizer.py content.md "keyword"

# 4. Iterate based on results
```

### Pattern 2: Strategic Decision Making

```markdown
@cs-ceo-advisor

1. Analyze 3 strategic options
2. Run financial scenarios
3. Identify risks
4. Recommend approach
5. Create communication plan
```

### Pattern 3: Technical Assessment

```markdown
@cs-cto-advisor

1. Assess current architecture
2. Identify tech debt
3. Calculate scaling needs
4. Create migration roadmap
5. Estimate team requirements
```

### Pattern 4: Product Discovery

```markdown
@cs-product-manager

1. Analyze customer interviews
2. Extract feature requests
3. Run RICE scoring
4. Create PRD
5. Generate roadmap
```

---

## Tips & Tricks

### Efficiency Tips

1. **Use shortcuts for common tasks**
   ```bash
   # Create alias for frequently used tools
   alias brand-check="python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py"
   brand-check content.txt
   ```

2. **Save agent prompts as templates**
   ```markdown
   # Save this as content-creation-template.md
   @cs-content-creator

   Create [TYPE] about [TOPIC]
   - Audience: [AUDIENCE]
   - Tone: [TONE]
   - Length: [LENGTH]
   - SEO keyword: [KEYWORD]
   ```

3. **Chain commands for automation**
   ```bash
   # Analyze → Report → Notify
   python3 script.py input.txt --output json && \
   echo "Analysis complete" | mail -s "Report" user@example.com
   ```

### Quality Tips

1. **Always provide context**
   - Industry/domain
   - Target audience
   - Desired outcome
   - Constraints (time, budget, resources)

2. **Use verbose mode when learning**
   ```bash
   python3 script.py input.txt --verbose
   ```

3. **Validate results**
   ```bash
   # Check JSON validity
   python3 script.py input.txt --output json | python3 -m json.tool
   ```

### Collaboration Tips

1. **Share agent workflows with team**
   ```markdown
   # Document your successful prompts
   Team-Proven-Workflows.md:
   - Content creation workflow
   - Product prioritization workflow
   - Strategic planning workflow
   ```

2. **Export results for sharing**
   ```bash
   # CSV for non-technical stakeholders
   python3 script.py input.csv --output csv --file results.csv
   ```

3. **Version control your inputs**
   ```bash
   git add features.csv scenarios.json
   git commit -m "Q1 prioritization inputs"
   ```

---

## Getting Help

### Documentation

- **Agent Documentation:** Check `agents/*/CLAUDE.md` files
- **Skill Documentation:** See `*/SKILL.md` files in each skill directory
- **Testing:** Review [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **CLI Standards:** See [documentation/standards/cli-standards.md](documentation/standards/cli-standards.md)

### Support Channels

- **Bug Reports:** [GitHub Issues](https://github.com/alirezarezvani/claude-skills/issues)
- **Questions:** [GitHub Discussions](https://github.com/alirezarezvani/claude-skills/discussions)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Next Steps

1. **Try the examples** above
2. **Explore agent workflows** in `agents/` directory
3. **Review skill documentation** for specific use cases
4. **Share your workflows** with the community
5. **Contribute improvements** via pull requests

---

**Version:** 1.0.0
**Last Updated:** November 6, 2025
**Compatible With:** Claude AI, Claude Code, Python 3.8+
