# Content Examples and Templates

Practical examples, templates, and quick reference guides for content creation.

## Quick Start Examples

### Brand Voice Development Example

**Scenario:** Tech startup needs consistent brand voice

**Process:**
1. Analyze 3-5 existing pieces of content
2. Identify patterns in formality, tone, perspective
3. Select brand archetype (e.g., "Innovator" + "Guide")
4. Create voice sample and test with analyzer

**Example Voice Profile:**
```
Brand: TechFlow (B2B SaaS)
Archetype: Expert + Guide
Formality: Semi-formal (60-70/100)
Tone: Professional but approachable
Perspective: 2nd person ("you"), some 1st person plural ("we")
Readability: College level (60-70 Flesch score)
```

### Blog Post Creation Example

**Topic:** How to Optimize API Performance

**Keyword Research:**
- Primary: "API performance optimization" (1,200/month)
- Secondary: "API speed", "reduce API latency", "API monitoring"
- LSI: response time, caching, rate limiting, load balancing

**Structure Applied:**
1. Introduction with problem statement (200 words)
2. Background on API performance (300 words)
3. 7 optimization techniques (1,400 words)
4. Monitoring and testing section (300 words)
5. Conclusion with CTA (150 words)

**SEO Results:**
- Length: 2,350 words
- Primary keyword density: 1.8%
- SEO score: 82/100
- Readability: 65 (Standard)

### Social Media Adaptation Example

**Original:** 2,000-word blog post on API optimization

**LinkedIn Post (1,300 characters):**
```
API performance can make or break user experience. Here are 7 proven techniques we use at TechFlow:

1. Implement smart caching strategies
   - Cache frequently accessed data
   - Use Redis or Memcached
   - Set appropriate TTL values

2. Optimize database queries
   - Index critical fields
   - Use query analysis tools
   - Avoid N+1 query problems

[Continue with remaining techniques...]

Which technique has had the biggest impact for you?

#APIOptimization #WebPerformance #SoftwareDevelopment
```

**Twitter Thread (280 chars per tweet):**
```
Tweet 1: API running slow? 7 techniques that improved our API response time by 60% 🧵

Tweet 2: 1/ Implement smart caching. We use Redis for frequently accessed data. Response times dropped from 800ms to 200ms. Game changer.

Tweet 3: 2/ Optimize your database queries. Index critical fields and watch for N+1 problems. Use EXPLAIN to analyze query performance.

[Continue thread...]

Tweet 8: Want the complete guide? Link in bio 🔗

#API #WebDev #Performance
```

## Reference Guide Templates

### When to Use Each Reference File

**brand_guidelines.md**
- **Use When:**
  - Setting up new brand voice
  - Onboarding new team members
  - Resolving tone/voice questions
  - Ensuring cross-channel consistency

- **Don't Use When:**
  - Creating one-off social posts (use frameworks instead)
  - Making minor copy edits
  - Internal documentation

**content_frameworks.md**
- **Use When:**
  - Starting any new content piece
  - Planning content structure
  - Creating content templates
  - Repurposing content across platforms

- **Don't Use When:**
  - Brand voice questions (use brand_guidelines)
  - Platform-specific optimization (use social_media_optimization)

**social_media_optimization.md**
- **Use When:**
  - Optimizing for specific platforms
  - Developing hashtag strategy
  - Planning posting schedules
  - Setting up analytics tracking

- **Don't Use When:**
  - Creating blog content structure
  - General SEO optimization
  - Brand voice development

## Content Templates

### Email Newsletter Template

**Subject Line:** [Benefit] in [Time Period] - [Number] Tips

**Preview Text:** [Expand on benefit, create curiosity]

**Body:**
```
Hi [FirstName],

[Opening hook - relate to pain point]

[Main content - 3-5 tips/insights]

Tip 1: [Headline]
[Brief explanation with example]
[CTA to relevant resource]

Tip 2: [Headline]
[Brief explanation with example]
[CTA to relevant resource]

[Continue with remaining tips...]

[Closing with clear CTA]

Best regards,
[Signature]

P.S. [Secondary CTA or additional value]
```

### Landing Page Copy Template

**Above the Fold:**
```
[Compelling Headline - Primary Benefit]
[Subheadline - Expand on benefit, add specificity]
[CTA Button] [Trust indicator]
[Hero image/video]
```

**Problem Section:**
```
[Headline: State the problem clearly]
[2-3 pain points your audience faces]
```

**Solution Section:**
```
[Headline: Introduce your solution]
[How it works - 3-4 steps]
[Visual demonstration]
```

**Features/Benefits:**
```
[3-6 key features with icons]
Feature 1: [Name]
[Benefit-focused description]

[Repeat for each feature...]
```

**Social Proof:**
```
[Testimonials - 2-3 with names/photos]
[Company logos]
[Statistics/results]
```

**CTA Section:**
```
[Compelling headline]
[Final CTA button]
[Risk reversal/guarantee]
```

### Social Media Post Templates

**LinkedIn Educational Post:**
```
[Hook - question or bold statement]

[Context - 2-3 sentences]

[Main content - 3-5 tips/insights with line breaks]

[Conclusion with question for engagement]

[2-3 relevant hashtags]
```

**Instagram Carousel Template:**
```
Slide 1: [Eye-catching title + visual]
"[Main headline]"

Slide 2-6: [One tip per slide]
"[Tip number]: [Headline]"
[Brief explanation]
[Simple visual/icon]

Slide 7: [CTA slide]
"Ready to [benefit]?"
[Clear action step]

Caption: [Expand on topic, add context, include CTA]
[8-15 relevant hashtags]
```

**Twitter Thread Template:**
```
Tweet 1: [Hook + thread indicator 🧵]
[Promise value or tease insight]

Tweet 2-8: [One point per tweet]
[Number]/[Total]: [Insight]
[Brief explanation]
[Optional: emoji for emphasis]

Final Tweet: [Summary + CTA]
[Link if applicable]
[2-3 hashtags]
```

## Workflow Examples

### First-Time Brand Voice Setup

**Time Required:** 4-6 hours

**Process:**

**Step 1: Gather Existing Content (30 min)**
- Collect 5-10 pieces of existing content
- Include various formats (blog, social, email)
- Save as plain text files

**Step 2: Analyze Content (45 min)**
```bash
# Run analyzer on each piece
python scripts/brand_voice_analyzer.py content1.txt
python scripts/brand_voice_analyzer.py content2.txt
# ... repeat for all pieces

# Look for patterns in:
# - Formality scores (target range?)
# - Tone descriptions (consistent?)
# - Perspective usage (1st/2nd/3rd person?)
# - Readability levels (appropriate for audience?)
```

**Step 3: Define Voice Attributes (1 hour)**
- Review brand personality archetypes
- Select primary archetype (e.g., Expert)
- Select secondary archetype (e.g., Guide)
- Choose 3-5 tone attributes:
  - Professional
  - Approachable
  - Confident
  - Educational
  - Practical

**Step 4: Document Guidelines (1 hour)**
- Create voice description
- Define do's and don'ts
- Provide examples of each tone attribute
- Set formality range (e.g., 60-70/100)
- Set readability target (e.g., 60-70 Flesch)

**Step 5: Create Test Samples (2 hours)**
- Write 3 sample pieces in chosen voice
- Different formats (blog intro, social post, email)
- Test with analyzer
- Refine until consistent

**Step 6: Validate (30 min)**
```bash
# Analyze samples
python scripts/brand_voice_analyzer.py sample1.txt
python scripts/brand_voice_analyzer.py sample2.txt
python scripts/brand_voice_analyzer.py sample3.txt

# Check consistency:
# - Formality scores within 10 points?
# - Similar tone descriptions?
# - Consistent perspective?
# - Readability in target range?
```

### SEO Blog Post Workflow

**Time Required:** 4-5 hours for 2,000-word post

**Step 1: Keyword Research (45 min)**
- Identify primary keyword (500-5,000 search volume)
- Find 3-5 secondary keywords
- List 10-15 LSI keywords
- Analyze top 5 competing articles

**Step 2: Outline Creation (30 min)**
- Choose template from frameworks.md
- Map keyword placement
- Plan visual elements
- Define CTAs

**Step 3: First Draft (2 hours)**
- Write without editing
- Focus on value and completeness
- Natural keyword usage
- Target 1,500-2,500 words

**Step 4: SEO Optimization (45 min)**
```bash
# Run initial analysis
python scripts/seo_optimizer.py draft.md --keyword "primary keyword" --secondary "keyword1,keyword2,keyword3"

# Review recommendations
# - Keyword density issues?
# - Heading structure problems?
# - Meta description needed?
# - Internal links missing?

# Make adjustments based on feedback
# Re-run optimizer to verify improvements
```

**Step 5: Voice Consistency Check (30 min)**
```bash
# Analyze brand voice
python scripts/brand_voice_analyzer.py draft.md

# Compare to brand guidelines
# - Formality in range?
# - Tone matches brand?
# - Readability appropriate?

# Refine language if needed
```

**Step 6: Final Review (30 min)**
- Proofread for errors
- Fact-check statistics
- Test all links
- Review formatting
- Check visual elements
- Verify CTAs are clear

**Step 7: Final SEO Check (15 min)**
```bash
# Final optimization check
python scripts/seo_optimizer.py final.md --keyword "primary keyword" --secondary "keyword1,keyword2,keyword3"

# Target: SEO score 75+
# Verify all recommendations addressed
```

### Social Media Content Batch Creation

**Time Required:** 3-4 hours for one week of content

**Step 1: Plan Content Mix (30 min)**
- Follow 40/25/25/10 pillar ratio
- 40% educational
- 25% promotional
- 25% engagement
- 10% entertainment

**Step 2: Create Educational Content (60 min)**
- 2-3 how-to posts
- Industry insights
- Tips and best practices
- Reference frameworks.md for structure

**Step 3: Create Promotional Content (45 min)**
- Product highlights
- Case study snippets
- Customer testimonials
- Special offers

**Step 4: Create Engagement Content (45 min)**
- Polls and questions
- Behind-the-scenes
- User-generated content
- Interactive posts

**Step 5: Create Entertainment Content (30 min)**
- Relevant humor
- Inspirational quotes
- Industry memes

**Step 6: Optimize for Platforms (30 min)**
- Review social_media_optimization.md
- Adapt copy for each platform
- Adjust length, tone, hashtags
- Prepare visual requirements

**Step 7: Schedule Posts (30 min)**
- Use content calendar template
- Follow optimal posting times
- Balance content types throughout week
- Set up tracking

## Quick Commands Reference

### Brand Voice Analysis Commands

```bash
# Basic text analysis (human-readable)
python scripts/brand_voice_analyzer.py content.txt

# JSON output for integration
python scripts/brand_voice_analyzer.py content.txt --output json

# Save results to file
python scripts/brand_voice_analyzer.py content.txt --file results.txt

# Verbose mode with progress
python scripts/brand_voice_analyzer.py content.txt --verbose

# Get version info
python scripts/brand_voice_analyzer.py --version

# Show help
python scripts/brand_voice_analyzer.py --help
```

### SEO Optimizer Commands

```bash
# Basic SEO analysis (no keywords)
python scripts/seo_optimizer.py article.md

# With primary keyword
python scripts/seo_optimizer.py article.md --keyword "python programming"

# With primary and secondary keywords
python scripts/seo_optimizer.py article.md -k "python" -s "coding,development,tutorial"

# JSON output for automation
python scripts/seo_optimizer.py article.md -k "python" --output json

# Save to file with verbose output
python scripts/seo_optimizer.py article.md -k "python" -f results.json -v

# Get version info
python scripts/seo_optimizer.py --version

# Show help
python scripts/seo_optimizer.py --help
```

### Content Management Commands

```bash
# Check content against brand guidelines
grep -i "professional" content.txt
grep -i "approachable" content.txt

# Create monthly calendar from template
cp assets/content_calendar_template.md november_2025_calendar.md

# Count words in draft
wc -w blog_draft.md

# Extract keywords from content
grep -o '\b\w\{5,\}\b' content.txt | sort | uniq -c | sort -rn | head -20
```

## Integration Examples

### Automation Script Example

```bash
#!/bin/bash
# Batch analyze all blog posts for brand consistency

echo "Analyzing all blog posts for brand voice consistency..."

for file in blog_posts/*.md; do
    echo "Analyzing: $file"
    python scripts/brand_voice_analyzer.py "$file" --output json > "analysis/$(basename "$file" .md).json"
done

echo "Analysis complete. Results saved to analysis/ directory."
```

### CI/CD Integration Example

```yaml
# GitHub Actions workflow example
name: Content Quality Check

on:
  pull_request:
    paths:
      - 'content/**/*.md'

jobs:
  check-content:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Run SEO Optimizer
        run: |
          for file in content/**/*.md; do
            python scripts/seo_optimizer.py "$file" --output json
          done

      - name: Run Brand Voice Analyzer
        run: |
          for file in content/**/*.md; do
            python scripts/brand_voice_analyzer.py "$file" --output json
          done
```

## Troubleshooting Examples

### Common Issues and Solutions

**Issue:** SEO score below 70
- Check keyword density (should be 1-3%)
- Verify heading structure (H1 > H2 > H3)
- Add internal/external links
- Optimize meta description
- Increase content length if thin

**Issue:** Inconsistent brand voice
- Run analyzer on recent content
- Compare formality scores (should be within 10 points)
- Review tone descriptions
- Reference brand guidelines
- Create consistent style samples

**Issue:** Low engagement on social media
- Review platform-specific guidelines
- Check posting times (test optimal windows)
- Increase visual content
- Add more engagement elements (polls, questions)
- Analyze successful posts for patterns

**Issue:** Poor SEO performance despite high score
- Review search intent match
- Check for technical SEO issues
- Verify backlink quality
- Analyze competing content
- Consider content freshness/updates
