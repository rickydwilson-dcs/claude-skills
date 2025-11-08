---
name: content-creator
description: Create SEO-optimized marketing content with consistent brand voice. Includes brand voice analyzer, SEO optimizer, content frameworks, and social media templates. Use when writing blog posts, creating social media content, analyzing brand voice, optimizing SEO, planning content calendars, or when user mentions content creation, brand voice, SEO optimization, social media marketing, or content strategy.
license: MIT
metadata:
  version: 1.0.0
  author: Claude Skills Team
  category: marketing
  domain: content-marketing
  updated: 2025-11-08
  keywords:
    - content creation
    - blog writing
    - SEO optimization
    - brand voice
    - social media marketing
    - content strategy
    - copywriting
    - keyword research
    - content calendar
    - marketing content
    - SEO copywriting
    - brand consistency
    - content marketing
    - audience engagement
    - content planning
    - editorial calendar
    - tone of voice
    - search engine optimization
    - organic traffic
    - content distribution
  tech-stack:
    - SEO
    - Google Analytics
    - Social media platforms
    - Markdown
    - Python 3.8+
  python-tools:
    - brand_voice_analyzer.py
    - seo_optimizer.py
---

# Content Creator

Professional-grade brand voice analysis, SEO optimization, and platform-specific content frameworks.

## Keywords
content creation, blog posts, SEO, brand voice, social media, content calendar, marketing content, content strategy, content marketing, brand consistency, content optimization, social media marketing, content planning, blog writing, content frameworks, brand guidelines, social media strategy

## Quick Start

### For Brand Voice Development
1. Run `scripts/brand_voice_analyzer.py` on existing content to establish baseline
2. Review `references/brand_guidelines.md` to select voice attributes
3. Apply chosen voice consistently across all content

### For Blog Content Creation
1. Choose template from `references/content_frameworks.md`
2. Research keywords for topic
3. Write content following template structure
4. Run `scripts/seo_optimizer.py [file] --keyword "primary-keyword"` to optimize
5. Apply recommendations before publishing

### For Social Media Content
1. Review platform best practices in `references/social_media_optimization.md`
2. Use appropriate template from `references/content_frameworks.md`
3. Optimize based on platform-specific guidelines
4. Schedule using `assets/content_calendar_template.md`

## Core Workflows

### Establishing Brand Voice (First Time Setup)

When creating content for a new brand or client:

1. **Analyze Existing Content** (if available)
   ```bash
   python scripts/brand_voice_analyzer.py existing_content.txt
   # Or get JSON output for integration
   python scripts/brand_voice_analyzer.py existing_content.txt --output json
   ```
   
2. **Define Voice Attributes**
   - Review brand personality archetypes in `references/brand_guidelines.md`
   - Select primary and secondary archetypes
   - Choose 3-5 tone attributes
   - Document in brand guidelines

3. **Create Voice Sample**
   - Write 3 sample pieces in chosen voice
   - Test consistency using analyzer
   - Refine based on results

### Creating SEO-Optimized Blog Posts

1. **Keyword Research**
   - Identify primary keyword (search volume 500-5000/month)
   - Find 3-5 secondary keywords
   - List 10-15 LSI keywords

2. **Content Structure**
   - Use blog template from `references/content_frameworks.md`
   - Include keyword in title, first paragraph, and 2-3 H2s
   - Aim for 1,500-2,500 words for comprehensive coverage

3. **Optimization Check**
   ```bash
   # Basic SEO analysis
   python scripts/seo_optimizer.py blog_post.md --keyword "primary keyword"

   # With secondary keywords
   python scripts/seo_optimizer.py blog_post.md --keyword "primary keyword" --secondary "keyword1,keyword2,keyword3"

   # Get JSON output for automation
   python scripts/seo_optimizer.py blog_post.md -k "primary keyword" -o json
   ```

4. **Apply SEO Recommendations**
   - Adjust keyword density to 1-3%
   - Ensure proper heading structure
   - Add internal and external links
   - Optimize meta description

### Social Media Content Creation

1. **Platform Selection**
   - Identify primary platforms based on audience
   - Review platform-specific guidelines in `references/social_media_optimization.md`

2. **Content Adaptation**
   - Start with blog post or core message
   - Use repurposing matrix from `references/content_frameworks.md`
   - Adapt for each platform following templates

3. **Optimization Checklist**
   - Platform-appropriate length
   - Optimal posting time
   - Correct image dimensions
   - Platform-specific hashtags
   - Engagement elements (polls, questions)

### Content Calendar Planning

1. **Monthly Planning**
   - Copy `assets/content_calendar_template.md`
   - Set monthly goals and KPIs
   - Identify key campaigns/themes

2. **Weekly Distribution**
   - Follow 40/25/25/10 content pillar ratio
   - Balance platforms throughout week
   - Align with optimal posting times

3. **Batch Creation**
   - Create all weekly content in one session
   - Maintain consistent voice across pieces
   - Prepare all visual assets together

## Key Scripts

### brand_voice_analyzer.py
Analyzes text content for voice characteristics, readability, and consistency.

**Usage**:
```bash
# Basic analysis (text output)
python scripts/brand_voice_analyzer.py content.txt

# JSON output for integration
python scripts/brand_voice_analyzer.py content.txt --output json

# Save results to file
python scripts/brand_voice_analyzer.py content.txt --file results.txt

# Verbose mode with progress updates
python scripts/brand_voice_analyzer.py content.txt --verbose
```

**Returns**:
- Voice profile (formality, tone, perspective)
- Readability score (Flesch Reading Ease)
- Sentence structure analysis
- Improvement recommendations

**Available Options**:
- `--output`, `-o`: Choose output format (text or json)
- `--file`, `-f`: Write output to file instead of stdout
- `--verbose`, `-v`: Show detailed processing information
- `--version`: Display version information
- `--help`: Show usage instructions

### seo_optimizer.py
Analyzes content for SEO optimization and provides actionable recommendations.

**Usage**:
```bash
# Basic SEO analysis
python scripts/seo_optimizer.py article.md

# With primary keyword
python scripts/seo_optimizer.py article.md --keyword "python programming"

# With secondary keywords
python scripts/seo_optimizer.py article.md -k "python" -s "coding,development,tutorial"

# JSON output for automation
python scripts/seo_optimizer.py article.md -k "python" --output json

# Save results to file with verbose output
python scripts/seo_optimizer.py article.md -k "python" -f results.json -v
```

**Returns**:
- SEO score (0-100)
- Content length and structure analysis
- Keyword density analysis (primary and secondary)
- LSI keyword suggestions
- Readability assessment
- Meta tag suggestions (title, description, URL slug)
- Specific optimization recommendations

**Available Options**:
- `--keyword`, `-k`: Primary keyword for optimization
- `--secondary`, `-s`: Comma-separated secondary keywords
- `--output`, `-o`: Choose output format (text or json)
- `--file`, `-f`: Write output to file instead of stdout
- `--verbose`, `-v`: Show detailed processing information
- `--version`: Display version information
- `--help`: Show usage instructions

## Reference Guides

### When to Use Each Reference

**references/brand_guidelines.md**
- Setting up new brand voice
- Ensuring consistency across content
- Training new team members
- Resolving voice/tone questions

**references/content_frameworks.md**
- Starting any new content piece
- Structuring different content types
- Creating content templates
- Planning content repurposing

**references/social_media_optimization.md**
- Platform-specific optimization
- Hashtag strategy development
- Understanding algorithm factors
- Setting up analytics tracking

## Best Practices

### Content Creation Process
1. Always start with audience need/pain point
2. Research before writing
3. Create outline using templates
4. Write first draft without editing
5. Optimize for SEO
6. Edit for brand voice
7. Proofread and fact-check
8. Optimize for platform
9. Schedule strategically

### Quality Indicators
- SEO score above 75/100
- Readability appropriate for audience
- Consistent brand voice throughout
- Clear value proposition
- Actionable takeaways
- Proper visual formatting
- Platform-optimized

### Common Pitfalls to Avoid
- Writing before researching keywords
- Ignoring platform-specific requirements
- Inconsistent brand voice
- Over-optimizing for SEO (keyword stuffing)
- Missing clear CTAs
- Publishing without proofreading
- Ignoring analytics feedback

## Performance Metrics

Track these KPIs for content success:

### Content Metrics
- Organic traffic growth
- Average time on page
- Bounce rate
- Social shares
- Backlinks earned

### Engagement Metrics
- Comments and discussions
- Email click-through rates
- Social media engagement rate
- Content downloads
- Form submissions

### Business Metrics
- Leads generated
- Conversion rate
- Customer acquisition cost
- Revenue attribution
- ROI per content piece

## Integration Points

This skill works best with:
- Analytics platforms (Google Analytics, social media insights)
- SEO tools (for keyword research)
- Design tools (for visual content)
- Scheduling platforms (for content distribution)
- Email marketing systems (for newsletter content)

## Quick Commands

```bash
# Analyze brand voice (text output)
python scripts/brand_voice_analyzer.py content.txt

# Analyze brand voice (JSON output)
python scripts/brand_voice_analyzer.py content.txt --output json

# Basic SEO analysis
python scripts/seo_optimizer.py article.md

# SEO optimization with keywords
python scripts/seo_optimizer.py article.md --keyword "main keyword" --secondary "related,keywords"

# SEO analysis with JSON output
python scripts/seo_optimizer.py article.md -k "main keyword" -o json

# Save results to file
python scripts/brand_voice_analyzer.py content.txt -f voice_analysis.txt
python scripts/seo_optimizer.py article.md -k "keyword" -f seo_report.json -o json

# Get help for any script
python scripts/brand_voice_analyzer.py --help
python scripts/seo_optimizer.py --help

# Check content against brand guidelines
grep -f references/brand_guidelines.md content.txt

# Create monthly calendar
cp assets/content_calendar_template.md this_month_calendar.md
```
