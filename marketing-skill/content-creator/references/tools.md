# Python Tools Reference

Comprehensive documentation for the content-creator Python automation tools.

## Overview

The content-creator skill includes two powerful Python CLI tools for content analysis:

1. **brand_voice_analyzer.py** - Analyzes text for voice characteristics and consistency
2. **seo_optimizer.py** - Comprehensive SEO analysis with actionable recommendations

Both tools are designed to:
- Work offline (no API calls or external dependencies)
- Process files locally for speed and privacy
- Provide both human-readable and JSON output
- Support automation and CI/CD integration
- Use only Python standard library

## Tool 1: Brand Voice Analyzer

### Purpose

Analyzes text content to identify voice characteristics including formality, tone, perspective, and readability. Essential for maintaining brand consistency across all content.

### Features

**Voice Profile Analysis:**
- Formality scoring (0-100 scale)
- Tone detection and classification
- Perspective analysis (1st/2nd/3rd person)
- Readability assessment (Flesch Reading Ease formula)

**Output Formats:**
- Human-readable text (default)
- JSON for programmatic integration
- File output for record-keeping

**Analysis Metrics:**
- Sentence structure patterns
- Word choice characteristics
- Reading level assessment
- Improvement recommendations

### Usage

**Basic Syntax:**
```bash
python scripts/brand_voice_analyzer.py <input_file> [options]
```

**Arguments:**
- `input_file` (required): Path to text file to analyze
- `--output`, `-o`: Output format (text or json)
- `--file`, `-f`: Write output to file instead of stdout
- `--verbose`, `-v`: Show detailed processing information
- `--version`: Display version information
- `--help`: Show usage instructions

### Examples

**Basic Analysis:**
```bash
python scripts/brand_voice_analyzer.py content.txt
```

**Output:**
```
Brand Voice Analysis Results:
============================

Voice Profile:
- Formality Score: 65/100 (Semi-formal)
- Tone: Professional with conversational elements
- Perspective: 2nd person (you-focused)
- Readability: 72 (College level)

Sentence Structure:
- Average sentence length: 18 words
- Complex sentences: 35%
- Simple sentences: 45%
- Compound sentences: 20%

Recommendations:
1. Maintain current formality level for B2B audience
2. Consider varying sentence length for better flow
3. Current readability appropriate for target audience
```

**JSON Output:**
```bash
python scripts/brand_voice_analyzer.py content.txt --output json
```

**Output:**
```json
{
  "formality_score": 65,
  "formality_level": "Semi-formal",
  "tone": "Professional with conversational elements",
  "perspective": {
    "primary": "2nd person",
    "first_person": 12,
    "second_person": 45,
    "third_person": 8
  },
  "readability": {
    "flesch_score": 72,
    "level": "College level",
    "avg_sentence_length": 18,
    "avg_syllables_per_word": 1.6
  },
  "sentence_structure": {
    "complex": 35,
    "simple": 45,
    "compound": 20
  },
  "recommendations": [
    "Maintain current formality level for B2B audience",
    "Consider varying sentence length for better flow",
    "Current readability appropriate for target audience"
  ]
}
```

**Save to File:**
```bash
python scripts/brand_voice_analyzer.py content.txt --file analysis_results.txt
```

**Verbose Mode:**
```bash
python scripts/brand_voice_analyzer.py content.txt --verbose
```

**Get Help:**
```bash
python scripts/brand_voice_analyzer.py --help
```

### Understanding Results

**Formality Score (0-100):**
- 0-30: Very casual (social media, personal blog)
- 31-50: Casual (lifestyle content, B2C marketing)
- 51-70: Semi-formal (business content, B2B marketing)
- 71-90: Formal (professional services, enterprise)
- 91-100: Very formal (legal, academic, technical)

**Readability (Flesch Reading Ease):**
- 90-100: Very easy (5th grade)
- 80-89: Easy (6th grade)
- 70-79: Fairly easy (7th grade)
- 60-69: Standard (8th-9th grade)
- 50-59: Fairly difficult (10th-12th grade)
- 30-49: Difficult (College level)
- 0-29: Very difficult (College graduate)

**Perspective Guidelines:**
- 1st person (I/we): Best for storytelling, personal brand
- 2nd person (you): Best for instructional, engagement-focused
- 3rd person (they/it): Best for objective, news-style content

### Use Cases

**Brand Voice Establishment:**
```bash
# Analyze existing content to identify patterns
python scripts/brand_voice_analyzer.py blog_post_1.txt
python scripts/brand_voice_analyzer.py blog_post_2.txt
python scripts/brand_voice_analyzer.py blog_post_3.txt

# Look for consistency in formality, tone, perspective
# Use insights to define brand voice guidelines
```

**Content Review:**
```bash
# Check new content against brand guidelines
python scripts/brand_voice_analyzer.py new_draft.txt

# Verify formality score matches target range
# Confirm tone aligns with brand attributes
# Ensure readability appropriate for audience
```

**Team Onboarding:**
```bash
# Show new writers examples of brand voice
python scripts/brand_voice_analyzer.py brand_sample_1.txt
python scripts/brand_voice_analyzer.py brand_sample_2.txt

# Have them analyze their own writing
python scripts/brand_voice_analyzer.py writer_sample.txt

# Compare results to identify adjustments needed
```

**Batch Analysis:**
```bash
# Analyze all content for consistency audit
for file in content/*.txt; do
    echo "Analyzing: $file"
    python scripts/brand_voice_analyzer.py "$file" --output json > "analysis/$(basename "$file" .txt).json"
done
```

## Tool 2: SEO Optimizer

### Purpose

Analyzes content for search engine optimization and provides specific, actionable recommendations to improve rankings and organic traffic.

### Features

**Comprehensive SEO Analysis:**
- Content length and structure evaluation
- Keyword density analysis (primary and secondary)
- LSI keyword suggestions
- Heading hierarchy validation
- Meta tag recommendations
- Overall SEO score (0-100)

**Keyword Analysis:**
- Primary keyword placement and frequency
- Secondary keyword usage
- Natural keyword integration assessment
- Over-optimization detection

**Content Structure:**
- Paragraph distribution
- Sentence variation
- List usage
- Internal linking opportunities

**Readability Assessment:**
- Flesch Reading Ease score
- Grade level appropriateness
- Sentence complexity analysis

### Usage

**Basic Syntax:**
```bash
python scripts/seo_optimizer.py <input_file> [options]
```

**Arguments:**
- `input_file` (required): Path to markdown or text file
- `--keyword`, `-k`: Primary keyword for optimization
- `--secondary`, `-s`: Comma-separated secondary keywords
- `--output`, `-o`: Output format (text or json)
- `--file`, `-f`: Write output to file instead of stdout
- `--verbose`, `-v`: Show detailed processing information
- `--version`: Display version information
- `--help`: Show usage instructions

### Examples

**Basic SEO Analysis (No Keywords):**
```bash
python scripts/seo_optimizer.py article.md
```

**Output:**
```
SEO Analysis Results:
====================

Overall SEO Score: 65/100

Content Analysis:
- Word count: 1,847
- Paragraphs: 24
- Headings: 8 (H2: 5, H3: 3)
- Lists: 3

Readability:
- Flesch Reading Ease: 68 (Standard)
- Recommended for general audience

Recommendations:
1. Increase content length to 2,000+ words
2. Add primary keyword for optimization
3. Include more internal links (3-5 recommended)
4. Add meta description
```

**With Primary Keyword:**
```bash
python scripts/seo_optimizer.py article.md --keyword "API performance optimization"
```

**Output:**
```
SEO Analysis Results:
====================

Overall SEO Score: 78/100

Content Analysis:
- Word count: 2,350
- Primary keyword: "API performance optimization"
- Keyword density: 1.8% (Good)
- Keyword in title: Yes
- Keyword in first paragraph: Yes
- Keyword in headings: 3/5 H2s

Keyword Analysis:
- Primary keyword count: 7 occurrences
- First appearance: Paragraph 1 (Good)
- Distribution: Well-distributed
- Density assessment: Optimal range (1-2%)

Content Structure:
- Paragraphs: 32 (Good)
- Headings: 12 (H2: 7, H3: 5)
- Lists: 5 (Good for scannability)
- Internal links: 2 (Add 1-3 more)

Recommendations:
1. Add keyword to 2 more H2 headings
2. Increase internal links to 5
3. Add 2-3 external authoritative links
4. Optimize meta description with keyword
5. Consider adding FAQ section
```

**With Primary and Secondary Keywords:**
```bash
python scripts/seo_optimizer.py article.md -k "API optimization" -s "API speed,reduce latency,performance monitoring"
```

**Output:**
```
SEO Analysis Results:
====================

Overall SEO Score: 82/100

Primary Keyword Analysis:
- Keyword: "API optimization"
- Count: 9 occurrences
- Density: 1.6% (Optimal)
- Title: Yes
- First paragraph: Yes
- Headings: 4/7 H2s

Secondary Keywords Analysis:
- "API speed": 6 occurrences (Good)
- "reduce latency": 4 occurrences (Good)
- "performance monitoring": 3 occurrences (Add 1-2 more)

LSI Keyword Suggestions:
- response time
- caching strategies
- database optimization
- load balancing
- API gateway
- rate limiting
- query optimization
- CDN integration

Content Quality Indicators:
- Length: 2,350 words (Excellent)
- Readability: 65 (Standard - appropriate)
- Structure: Well-organized with clear hierarchy
- Scannability: Good (lists, headings, short paragraphs)

Meta Recommendations:
- Title: "7 Proven API Optimization Techniques to Boost Performance"
- Description: "Learn how to optimize API performance with expert techniques for API speed, reducing latency, and performance monitoring. Improve response times by 60%."
- URL Slug: "api-optimization-techniques-performance"

Recommendations:
1. Increase usage of "performance monitoring" by 1-2 instances
2. Add 3-5 LSI keywords naturally in content
3. Ensure title contains primary keyword at beginning
4. Add schema markup for technical article
5. Include comparison table for optimization techniques
```

**JSON Output:**
```bash
python scripts/seo_optimizer.py article.md -k "API optimization" --output json
```

**Output:**
```json
{
  "seo_score": 82,
  "content_analysis": {
    "word_count": 2350,
    "paragraph_count": 32,
    "heading_count": 12,
    "headings": {
      "h2": 7,
      "h3": 5
    },
    "list_count": 5,
    "internal_links": 4,
    "external_links": 2
  },
  "primary_keyword": {
    "keyword": "API optimization",
    "count": 9,
    "density": 1.6,
    "in_title": true,
    "in_first_paragraph": true,
    "in_headings": 4,
    "distribution": "well-distributed"
  },
  "secondary_keywords": [
    {
      "keyword": "API speed",
      "count": 6,
      "status": "good"
    },
    {
      "keyword": "reduce latency",
      "count": 4,
      "status": "good"
    },
    {
      "keyword": "performance monitoring",
      "count": 3,
      "status": "needs_improvement"
    }
  ],
  "lsi_keywords": [
    "response time",
    "caching strategies",
    "database optimization",
    "load balancing",
    "API gateway"
  ],
  "readability": {
    "flesch_score": 65,
    "level": "Standard",
    "appropriate": true
  },
  "meta_recommendations": {
    "title": "7 Proven API Optimization Techniques to Boost Performance",
    "description": "Learn how to optimize API performance with expert techniques for API speed, reducing latency, and performance monitoring. Improve response times by 60%.",
    "url_slug": "api-optimization-techniques-performance"
  },
  "recommendations": [
    "Increase usage of 'performance monitoring' by 1-2 instances",
    "Add 3-5 LSI keywords naturally in content",
    "Ensure title contains primary keyword at beginning",
    "Add schema markup for technical article",
    "Include comparison table for optimization techniques"
  ]
}
```

**Save Results to File:**
```bash
python scripts/seo_optimizer.py article.md -k "API optimization" -f seo_report.json -o json
```

**Verbose Mode:**
```bash
python scripts/seo_optimizer.py article.md -k "keyword" -v
```

### Understanding Results

**SEO Score Interpretation:**
- 0-40: Poor (major improvements needed)
- 41-60: Fair (significant optimization required)
- 61-75: Good (some improvements recommended)
- 76-85: Very good (minor tweaks)
- 86-100: Excellent (well-optimized)

**Keyword Density Guidelines:**
- Under 1%: Too low, increase usage
- 1-2%: Optimal range
- 2-3%: Acceptable but monitor
- Over 3%: Risk of over-optimization

**Content Length Guidelines:**
- Under 500 words: Too thin for most topics
- 500-1,000: Minimum for basic topics
- 1,000-1,500: Good for standard topics
- 1,500-2,500: Excellent for comprehensive coverage
- 2,500+: Pillar content, ultimate guides

### Use Cases

**Pre-Publishing SEO Check:**
```bash
# Analyze draft before publishing
python scripts/seo_optimizer.py draft.md -k "target keyword" -s "related,keywords"

# Review SEO score and recommendations
# Make adjustments to improve score
# Re-run until score is 75+

python scripts/seo_optimizer.py revised.md -k "target keyword" -s "related,keywords"
```

**Content Optimization Workflow:**
```bash
# 1. Initial draft (no keywords)
python scripts/seo_optimizer.py draft.md

# 2. Keyword research and second draft
python scripts/seo_optimizer.py draft_v2.md -k "primary keyword"

# 3. Final optimization with all keywords
python scripts/seo_optimizer.py final.md -k "primary keyword" -s "keyword1,keyword2,keyword3"

# 4. Verify improvements
python scripts/seo_optimizer.py final.md -k "primary keyword" -s "keyword1,keyword2,keyword3" -o json -f seo_final_report.json
```

**Batch Content Audit:**
```bash
# Audit all blog posts for SEO quality
for file in blog/*.md; do
    echo "Analyzing: $file"
    python scripts/seo_optimizer.py "$file" -o json > "audit/$(basename "$file" .md)_seo.json"
done

# Review JSON files to identify low-scoring content
# Prioritize optimization based on scores
```

**Competitive Analysis:**
```bash
# Analyze competitor content
python scripts/seo_optimizer.py competitor_article.txt -k "target keyword"

# Compare their keyword usage, structure, length
# Use insights to inform your content strategy
```

## Integration Patterns

### CI/CD Integration

**GitHub Actions Example:**
```yaml
name: Content SEO Check

on:
  pull_request:
    paths:
      - 'blog/**/*.md'

jobs:
  seo-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: SEO Analysis
        run: |
          python scripts/seo_optimizer.py ${{ github.event.pull_request.changed_files }} --output json

      - name: Check SEO Score
        run: |
          score=$(python scripts/seo_optimizer.py ${{ github.event.pull_request.changed_files }} --output json | jq '.seo_score')
          if [ $score -lt 70 ]; then
            echo "SEO score too low: $score"
            exit 1
          fi
```

### Content Management System Integration

**Example: Analyze content before publishing**
```python
import subprocess
import json

def check_content_quality(file_path, primary_keyword, secondary_keywords):
    """Run both analyzers and return combined results"""

    # Brand voice analysis
    voice_result = subprocess.run(
        ['python', 'scripts/brand_voice_analyzer.py', file_path, '--output', 'json'],
        capture_output=True,
        text=True
    )
    voice_data = json.loads(voice_result.stdout)

    # SEO analysis
    seo_result = subprocess.run(
        ['python', 'scripts/seo_optimizer.py', file_path, '-k', primary_keyword, '-s', secondary_keywords, '-o', 'json'],
        capture_output=True,
        text=True
    )
    seo_data = json.loads(seo_result.stdout)

    return {
        'voice': voice_data,
        'seo': seo_data,
        'quality_score': (voice_data['formality_score'] * 0.3 + seo_data['seo_score'] * 0.7)
    }

# Usage
result = check_content_quality('draft.md', 'API optimization', 'API speed,performance')
if result['quality_score'] < 70:
    print("Content needs improvement before publishing")
    print(f"Voice score: {result['voice']['formality_score']}")
    print(f"SEO score: {result['seo']['seo_score']}")
```

### Automated Reporting

**Weekly Content Quality Report:**
```bash
#!/bin/bash
# Generate weekly content quality report

echo "Weekly Content Quality Report" > weekly_report.txt
echo "=============================" >> weekly_report.txt
echo "" >> weekly_report.txt

total_score=0
count=0

for file in content/this_week/*.md; do
    echo "Analyzing: $file" >> weekly_report.txt

    # Voice analysis
    python scripts/brand_voice_analyzer.py "$file" >> weekly_report.txt
    echo "" >> weekly_report.txt

    # SEO analysis
    python scripts/seo_optimizer.py "$file" -k "keyword" >> weekly_report.txt
    echo "" >> weekly_report.txt
    echo "---" >> weekly_report.txt

    count=$((count + 1))
done

echo "Analyzed $count pieces of content" >> weekly_report.txt

# Email report or save to dashboard
```

## Troubleshooting

### Common Issues

**Issue: "File not found" error**
- Verify file path is correct
- Use absolute paths if needed
- Check file permissions

**Issue: Low formality score when expecting high**
- Review word choice (use more formal vocabulary)
- Reduce contractions (don't → do not)
- Increase sentence complexity
- Use third person perspective

**Issue: Low SEO score despite good content**
- Verify keyword appears in title and first paragraph
- Check keyword density (aim for 1-2%)
- Add more headings with keywords
- Increase content length
- Add internal and external links

**Issue: JSON output not parsing**
- Ensure using --output json flag
- Check for special characters in content
- Verify Python version (3.8+ required)

**Issue: Keyword density too high**
- Remove some keyword instances
- Use variations and synonyms
- Focus on natural language
- Add more supporting content

### Performance Tips

**For Large Files:**
- Files under 10MB process in <1 second
- For larger files, consider splitting
- Use verbose mode to monitor progress

**For Batch Processing:**
- Process files in parallel if possible
- Use JSON output for automated parsing
- Save results to files to avoid memory issues

**For Automation:**
- Set appropriate timeout values
- Handle errors gracefully
- Log results for debugging
- Use exit codes to check success

## Version Information

**brand_voice_analyzer.py:**
- Version: 1.0.0
- Python requirement: 3.8+
- Dependencies: Standard library only
- Last updated: 2025-11-08

**seo_optimizer.py:**
- Version: 1.0.0
- Python requirement: 3.8+
- Dependencies: Standard library only
- Last updated: 2025-11-08

## Support and Updates

For issues, feature requests, or updates:
- Check SKILL.md for workflow guidance
- Review examples.md for practical use cases
- See frameworks.md for content strategy

All tools are open source and can be modified for specific needs.
