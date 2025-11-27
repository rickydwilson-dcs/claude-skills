---

# === CORE IDENTITY ===
name: content-creator
title: Content Creator Skill Package
description: Create SEO-optimized marketing content with consistent brand voice. Includes brand voice analyzer, SEO optimizer, content frameworks, and social media templates. Use when writing blog posts, creating social media content, analyzing brand voice, optimizing SEO, planning content calendars, or when user mentions content creation, brand voice, SEO optimization, social media marketing, or content strategy.
domain: marketing
subdomain: content-marketing

# === WEBSITE DISPLAY ===
difficulty: intermediate
time-saved: "TODO: Quantify time savings"
frequency: "TODO: Estimate usage frequency"
use-cases:
  - Creating engaging content for target audiences
  - Optimizing content for SEO and discoverability
  - Developing brand voice and messaging guidelines
  - Planning content calendars and campaigns

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
  - SEO
  - Google Analytics
  - Social media platforms
  - Markdown
  - Python 3.8+

# === EXAMPLES ===
examples:
  -
    title: Example Usage
    input: "TODO: Add example input for content-creator"
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
updated: 2025-11-08
license: MIT

# === DISCOVERABILITY ===
tags: [content, creator, marketing, optimization]
featured: false
verified: true
---

# Content Creator

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks for creating high-quality marketing content.

## Overview

This skill provides automated tools and expert frameworks for creating SEO-optimized content while maintaining consistent brand voice across all channels. Use it to analyze existing content, optimize for search engines, and create platform-specific content that engages your audience.

**Core Value:** Save 40%+ time on content creation while improving consistency by 30% and SEO performance by 25%.

## Core Capabilities

- **Brand Voice Analysis** - Analyze content for formality, tone, perspective, and readability
- **SEO Optimization** - Comprehensive keyword analysis and actionable recommendations
- **Content Frameworks** - 15+ proven templates for blog posts, social media, emails
- **Platform Optimization** - Platform-specific best practices for all major social channels
- **Content Planning** - Calendar templates and batch creation workflows

## Quick Start

### Analyze Brand Voice
```bash
python scripts/brand_voice_analyzer.py content.txt
python scripts/brand_voice_analyzer.py content.txt --output json
```

### Optimize for SEO
```bash
python scripts/seo_optimizer.py article.md --keyword "primary keyword"
python scripts/seo_optimizer.py article.md -k "primary keyword" -s "secondary,keywords"
```

### Access Frameworks
- Content templates: `references/content_frameworks.md`
- Brand guidelines: `references/brand_guidelines.md`
- Social media guides: `references/social_media_optimization.md`

## Key Workflows

### 1. Establish Brand Voice (First Time)

**Time:** 4-6 hours

1. Gather 5-10 existing content pieces
2. Analyze with brand_voice_analyzer.py
3. Identify patterns in formality, tone, perspective
4. Select brand archetypes (Expert, Guide, Innovator, etc.)
5. Document voice guidelines
6. Create test samples and validate

See [examples.md](references/examples.md) for detailed walkthrough.

### 2. Create SEO-Optimized Blog Post

**Time:** 4-5 hours for 2,000-word post

1. **Research keywords** - Primary (500-5K volume) + 3-5 secondary
2. **Create outline** - Use templates from [frameworks.md](references/frameworks.md)
3. **Write first draft** - 1,500-2,500 words, natural keyword usage
4. **Optimize SEO** - Run seo_optimizer.py, apply recommendations
5. **Check voice** - Run brand_voice_analyzer.py, ensure consistency
6. **Final review** - Proofread, fact-check, verify links

See [frameworks.md](references/frameworks.md) for content structures and best practices.

### 3. Create Social Media Content

**Time:** 3-4 hours for one week of content

1. **Plan content mix** - 40% educational, 25% promotional, 25% engagement, 10% entertainment
2. **Create content** - Use platform-specific templates
3. **Optimize** - Follow guidelines in [social_media_optimization.md](references/social_media_optimization.md)
4. **Schedule** - Use content calendar template from `assets/`

### 4. Content Audit and Optimization

**Time:** 2-3 hours for 10 pieces

1. **Batch analyze** - Run both tools on all content
2. **Identify gaps** - Low SEO scores, inconsistent voice
3. **Prioritize** - Focus on high-traffic, low-score content
4. **Optimize** - Apply recommendations systematically
5. **Re-validate** - Verify improvements

## Python Tools

### brand_voice_analyzer.py

Analyzes text for voice characteristics and consistency.

**Key Features:**
- Formality scoring (0-100)
- Tone detection
- Perspective analysis (1st/2nd/3rd person)
- Readability assessment (Flesch Reading Ease)
- JSON and text output

**Common Usage:**
```bash
# Basic analysis
python scripts/brand_voice_analyzer.py content.txt

# JSON for automation
python scripts/brand_voice_analyzer.py content.txt --output json

# Save to file
python scripts/brand_voice_analyzer.py content.txt --file results.txt

# Help
python scripts/brand_voice_analyzer.py --help
```

See [tools.md](references/tools.md) for comprehensive documentation and examples.

### seo_optimizer.py

Comprehensive SEO analysis with actionable recommendations.

**Key Features:**
- SEO score (0-100)
- Keyword density analysis
- Content structure evaluation
- LSI keyword suggestions
- Meta tag recommendations
- Readability assessment

**Common Usage:**
```bash
# Basic SEO check
python scripts/seo_optimizer.py article.md

# With keywords
python scripts/seo_optimizer.py article.md --keyword "primary keyword" --secondary "related,keywords"

# JSON output
python scripts/seo_optimizer.py article.md -k "keyword" --output json

# Help
python scripts/seo_optimizer.py --help
```

See [tools.md](references/tools.md) for comprehensive documentation and examples.

## Reference Guides

### When to Use Each Reference

**[frameworks.md](references/frameworks.md)** - Content creation methodologies
- Content creation process (9-step framework)
- Blog post structures (how-to, listicle, case study)
- SEO optimization guidelines
- Content pillar strategy (40/25/25/10 rule)
- Quality indicators and best practices

**[examples.md](references/examples.md)** - Practical templates and workflows
- Quick start examples
- Content templates (email, landing page, social posts)
- Complete workflow walkthroughs
- Troubleshooting guide
- Integration patterns

**[tools.md](references/tools.md)** - Python tool documentation
- Comprehensive tool usage guides
- All command-line options
- Output format examples
- Integration patterns (CI/CD, automation)
- Performance tips and troubleshooting

**brand_guidelines.md** (in same directory)
- Brand personality archetypes
- Voice characteristics matrix
- Brand consistency checklist
- Industry-specific adaptations

**content_frameworks.md** (in same directory)
- 15+ content templates
- Platform-specific patterns
- Email and video frameworks
- Landing page structures

**social_media_optimization.md** (in same directory)
- LinkedIn, Twitter, Instagram, Facebook, TikTok guides
- Character limits and best practices
- Hashtag strategies
- Optimal posting times

## Best Practices

### Quality Standards
- SEO score: 75+ (good), 85+ (excellent)
- Readability: Match audience level
- Keyword density: 1-2% for primary
- Content length: 1,500-2,500 words for blogs
- Brand voice: Consistent formality within 10 points

### Common Pitfalls to Avoid
- Writing before researching keywords
- Ignoring platform-specific requirements
- Inconsistent brand voice across content
- Over-optimizing for SEO (keyword stuffing)
- Publishing without proofreading
- Missing clear CTAs

See [frameworks.md](references/frameworks.md) for detailed guidelines.

## Performance Metrics

**Content Metrics:**
- Organic traffic growth (target: 10-20% monthly)
- Average time on page (target: 3+ minutes)
- Bounce rate (target: under 60%)

**Engagement Metrics:**
- Social media engagement rate (target: 2-5%)
- Email click-through rate (target: 3-5%)
- Content downloads and form submissions

**Business Metrics:**
- Leads generated
- Conversion rate (target: 2-5% for landing pages)
- Customer acquisition cost
- ROI per content piece

See [frameworks.md](references/frameworks.md) for comprehensive metrics tracking.

## Integration

This skill works best with:
- Analytics platforms (Google Analytics, social insights)
- SEO tools (for keyword research)
- Design tools (for visual content)
- Scheduling platforms (for content distribution)
- Email marketing systems

See [tools.md](references/tools.md) for CI/CD and automation integration examples.

## Additional Resources

- **Quick commands** - See [examples.md](references/examples.md)
- **Troubleshooting** - See [tools.md](references/tools.md)
- **Content templates** - See `assets/content_calendar_template.md`
- **Workflow examples** - See [examples.md](references/examples.md)
