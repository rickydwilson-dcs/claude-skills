# Content Creator - Sample Assets

This directory contains sample input files for testing and understanding the Python tools in the `../scripts/` directory.

## Sample Files

### 1. sample-content.txt
**Purpose:** Text content for brand voice analysis and SEO optimization testing

**Description:** A realistic blog post about strategic content marketing with approximately 600 words covering:
- Main brand voice characteristics (formality, tone, perspective)
- Readable paragraphs with varying lengths
- Professional but accessible language
- Industry-relevant terminology

**How to Use:**
```bash
# Analyze brand voice
python ../scripts/brand_voice_analyzer.py sample-content.txt

# Optimize for SEO
python ../scripts/seo_optimizer.py sample-content.txt "content marketing"

# Get JSON output
python ../scripts/seo_optimizer.py sample-content.txt "content marketing" --output json
```

**What to Expect:**
- Brand voice analysis showing formality, tone, and perspective scores
- Readability score (Flesch Reading Ease format)
- SEO recommendations for content optimization

---

### 2. sample-article.md
**Purpose:** Markdown article for comprehensive SEO analysis testing

**Description:** A technical guide about "Customer-Centric Product Strategy" with:
- Markdown headers (H1, H2, H3 structure)
- Multiple paragraphs with varying lengths
- Lists and formatted content
- ~1,200 words of realistic product/marketing content

**How to Use:**
```bash
# Analyze for SEO with multiple keywords
python ../scripts/seo_optimizer.py sample-article.md "product strategy" "customer research,product development"

# Get JSON output for integration
python ../scripts/seo_optimizer.py sample-article.md "product strategy" --output json --file results.json
```

**What to Expect:**
- Content structure analysis (headings, paragraphs, links)
- Keyword density calculations
- Meta tag suggestions
- Actionable SEO recommendations
- Overall SEO score (0-100)

---

## Using These Samples

### Quick Start - Brand Voice Analysis
```bash
cd /Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My\ Drive/Websites/GitHub/claude-skills/marketing-skill/content-creator/

# Test basic analysis
python scripts/brand_voice_analyzer.py assets/sample-content.txt

# Test with different output formats
python scripts/brand_voice_analyzer.py assets/sample-content.txt --output json
python scripts/brand_voice_analyzer.py assets/sample-article.md --output json
```

### Quick Start - SEO Optimization
```bash
cd /Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My\ Drive/Websites/GitHub/claude-skills/marketing-skill/content-creator/

# Basic SEO analysis
python scripts/seo_optimizer.py assets/sample-content.txt "marketing strategy"

# With secondary keywords
python scripts/seo_optimizer.py assets/sample-article.md "customer research" "personas,interviews,engagement"

# Full report with JSON output
python scripts/seo_optimizer.py assets/sample-article.md "product strategy" -o json -f seo-report.json
```

---

## Creating Your Own Sample Files

### For Brand Voice Analysis
Your content should:
- Be at least 200 words (ideally 400-800)
- Include varied sentence lengths
- Mix of formal and casual elements (if testing flexibility)
- Clear topic focus

Example:
```
Your content here...
This should demonstrate brand voice characteristics.
```

### For SEO Optimization
Your article should include:
- H1 and H2 headers
- 3+ paragraphs
- 300+ words total
- Relevant keywords for testing
- Links (internal and/or external) if testing structure

Example:
```markdown
# Main Title
Introductory paragraph...

## Subheading
More content...
```

---

## File Format Notes

### Text Files (.txt)
- Plain text format
- UTF-8 encoding
- No special formatting
- Works best for brand voice analysis

### Markdown Files (.md)
- Markdown syntax with headers
- UTF-8 encoding
- Supports structured content
- Best for comprehensive SEO analysis

---

## Integration with Scripts

### Brand Voice Analyzer
**Input:** Text file (any encoding, UTF-8 recommended)
**Output:** JSON or human-readable text
**Key Metrics:**
- Formality score (formal vs casual)
- Tone analysis (professional vs friendly)
- Perspective analysis (authoritative vs conversational)
- Readability score (Flesch Reading Ease)
- Voice consistency recommendations

### SEO Optimizer
**Input:** Text or Markdown file
**Output:** JSON or human-readable report
**Key Metrics:**
- Content length analysis
- Keyword density
- Content structure (headings, paragraphs)
- Meta suggestions (title, description, URL slug)
- Overall SEO score
- Specific recommendations

---

## Tips for Best Results

1. **Use Realistic Content:** The tools work best with actual marketing/content samples
2. **Vary Content Length:** Test with 200-word pieces and 2,000+ word pieces
3. **Include Keywords:** For SEO analysis, use actual target keywords
4. **Check Output Formats:** Try both JSON and text outputs to understand the data
5. **Iterate:** Use the recommendations to improve your content

---

## Troubleshooting

**Issue:** Script returns "File not found"
- Make sure you're in the correct directory or use absolute paths
- Check file encoding (should be UTF-8)

**Issue:** JSON output is malformed
- Ensure the input file is valid UTF-8 text
- Check for special characters that might need escaping

**Issue:** Readability score seems off
- This uses Flesch Reading Ease (0-100 scale)
- Scores depend on word/sentence length and syllable count
- Technical content often scores lower (25-45)

**Issue:** SEO recommendations seem generic
- Run analysis with specific keywords for better recommendations
- Include more structured content (headers, lists)
- Use 500+ word samples for best analysis

---

## Related Documentation

- **Brand Voice Guide:** [../references/brand_guidelines.md](../references/brand_guidelines.md)
- **Content Frameworks:** [../references/content_frameworks.md](../references/content_frameworks.md)
- **SEO Best Practices:** [../references/](../references/)
- **Skill Documentation:** [../SKILL.md](../SKILL.md)

---

**Last Updated:** November 5, 2025
**Format:** Sample Assets README
**Included Files:** 2 (sample-content.txt, sample-article.md)
