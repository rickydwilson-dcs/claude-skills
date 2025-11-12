# Product Manager Toolkit - Sample Assets

This directory contains sample files for RICE prioritization and customer interview analysis tools.

## Sample Files

### 1. sample-features.csv
**Purpose:** Feature list for RICE prioritization framework analysis

**Description:** Realistic set of 15 product features with RICE components:
- Feature names and descriptions
- Reach (affected users per quarter)
- Impact (business value: massive/high/medium/low/minimal)
- Confidence (1.0=high, 0.8=medium, 0.5=low)
- Effort (person-months: xl/l/m/s/xs)

**How to Use:**
```bash
# Run RICE prioritization
python ../scripts/rice_prioritizer.py sample-features.csv

# With capacity planning
python ../scripts/rice_prioritizer.py sample-features.csv --capacity 20

# JSON output
python ../scripts/rice_prioritizer.py sample-features.csv --output json

# Save to file
python ../scripts/rice_prioritizer.py sample-features.csv --output json -f prioritized.json
```

**What to Expect:**
- Ranked features by RICE score (highest priority first)
- Portfolio analysis (quick wins vs big bets)
- Capacity-based roadmap
- RICE score formula: (Reach × Impact × Confidence) / Effort

---

### 2. sample-interview.txt
**Purpose:** Customer interview transcript for sentiment and insights analysis

**Description:** Realistic 45-minute customer interview with:
- Natural conversation flow
- Mix of pain points and positive feedback
- Feature requests and suggestions
- Business context and constraints
- Clear customer needs and priorities

**How to Use:**
```bash
# Analyze interview for insights
python ../scripts/customer_interview_analyzer.py sample-interview.txt

# Get JSON output
python ../scripts/customer_interview_analyzer.py sample-interview.txt --output json

# Save detailed analysis
python ../scripts/customer_interview_analyzer.py sample-interview.txt --output json --file analysis.json
```

**What to Expect:**
- Extracted pain points with severity
- Positive feedback (delight indicators)
- Feature requests identified
- Jobs-to-be-done patterns
- Sentiment analysis score
- Key themes and quotes
- Actionable insights

---

## Using These Samples

### Quick Start

```bash
cd /Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My\ Drive/Websites/GitHub/claude-skills/product-team/product-manager-toolkit/

# RICE prioritization
python scripts/rice_prioritizer.py assets/sample-features.csv

# With capacity planning (20 story points)
python scripts/rice_prioritizer.py assets/sample-features.csv --capacity 20

# Interview analysis
python scripts/customer_interview_analyzer.py assets/sample-interview.txt

# Full analysis with JSON
python scripts/customer_interview_analyzer.py assets/sample-interview.txt -o json -f interview-insights.json
```

---

## RICE Prioritization Guide

### RICE Formula
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

### Component Definitions

**Reach:** Users affected per quarter
- Small: 100-500 users
- Medium: 500-2,000 users
- Large: 2,000-5,000 users
- Very Large: 5,000+ users

**Impact:** Business value
- Massive: 3.0x multiplier
- High: 2.0x multiplier
- Medium: 1.0x multiplier
- Low: 0.5x multiplier
- Minimal: 0.25x multiplier

**Confidence:** Certainty about estimates
- High: 100% (1.0)
- Medium: 80% (0.8)
- Low: 50% (0.5)

**Effort:** Person-months to complete
- XS (Extra Small): 1 month
- S (Small): 3 months
- M (Medium): 5 months
- L (Large): 8 months
- XL (Extra Large): 13 months

### Interpreting RICE Scores

| Score | Priority | Action |
|-------|----------|--------|
| 100+ | Critical | Build immediately |
| 50-100 | High | Schedule for next quarter |
| 20-50 | Medium | Plan for backlog |
| <20 | Low | Consider or defer |

### CSV Format Example

```csv
feature,reach,impact,confidence,effort
Mobile App Login,5000,high,1.0,5
Push Notifications,3000,medium,0.8,3
Dark Mode,1500,low,1.0,2
```

---

## Interview Analysis Guide

### Sentiment Scoring
- **-1.0**: Very negative, serious issues
- **-0.5**: Somewhat negative, minor complaints
- **0**: Neutral, factual feedback
- **+0.5**: Somewhat positive
- **+1.0**: Very positive, delighted

### Pain Point Categories

**Severity Levels:**
- **Critical**: Blocks work or causes data loss
- **High**: Significant productivity impact
- **Medium**: Annoying but workaround exists
- **Low**: Nice to have

### Key Themes to Extract

1. **Jobs to be Done**: What is customer trying to accomplish?
2. **Current Workarounds**: How do they solve it now?
3. **Barriers**: What prevents adoption?
4. **Success Metrics**: How do they measure success?
5. **Competitors**: Who else are they considering?

---

## Creating Your Own Files

### CSV for RICE Prioritization

Template:
```csv
feature,reach,impact,confidence,effort
Your Feature Name,5000,high,0.8,5
```

Tips:
- Use consistent reach numbers (user count per quarter)
- Impact should match business goals (revenue, retention, engagement)
- Confidence reflects team certainty (~50-100%)
- Effort in person-months (be realistic)

### Interview Transcript Format

Guidelines:
- Natural conversation (not Q&A format)
- Include context (customer role, company size)
- Quote customer directly
- Note body language or emphasis if relevant
- 30-60 minutes is ideal length

Format:
```
Customer Interview: [Name], [Role] at [Company]
Date: [Date]
Duration: [Minutes]

---

Interviewer: Opening question?

Customer: Answer with details...

Interviewer: Follow-up question?

Customer: Response mentioning pain points, needs, etc.
```

---

## Workflow: From Interview to Prioritization

### Process

1. **Conduct Interview** (40-60 min)
   - Record audio/video if possible
   - Take detailed notes
   - Capture verbatim quotes

2. **Transcribe**
   - Create text transcript
   - Clean up but keep natural language
   - Add context notes

3. **Analyze with Tool**
   ```bash
   python scripts/customer_interview_analyzer.py transcript.txt --output json
   ```

4. **Extract Insights**
   - Pain points
   - Feature requests
   - Sentiment
   - Jobs-to-be-done

5. **Add to Feature List**
   - Create new features if needed
   - Adjust Reach based on interview evidence
   - Increase Confidence if multiple customers mention

6. **Reprioritize**
   ```bash
   python scripts/rice_prioritizer.py features.csv --capacity 30
   ```

---

## Integration with Product Workflow

### Monthly Cycle

1. **Week 1**: Conduct 3-5 customer interviews
2. **Week 2**: Analyze transcripts, extract insights
3. **Week 3**: Update feature list with learnings
4. **Week 4**: Run RICE prioritization, plan next quarter

### Data Aggregation

- Run interview analysis on 5-10 transcripts per quarter
- Look for patterns across customers
- Weight by customer size/importance
- Track changes over time

---

## Troubleshooting

**RICE Issues:**

- Score seems too high/low → Check if effort is realistic
- Scores all bunched together → Ensure sufficient range in components
- Winner is obvious → May indicate strong priorities already

**Interview Analysis Issues:**

- Missing pain points → Check if keywords are industry-specific
- Sentiment seems off → Review if sarcasm or domain language present
- Few feature requests extracted → Transcript may be too sales-focused

---

## Best Practices

1. **RICE Calibration**
   - Review past features with actual outcomes
   - Adjust confidence scores based on accuracy
   - Recalibrate effort estimates quarterly

2. **Interview Conduct**
   - Ask open-ended questions
   - Listen for problems, not solutions
   - Probe into context and workflows
   - Record for accuracy

3. **Aggregation**
   - Interview 8-12 customers per quarter minimum
   - Across different segments (size, industry, use case)
   - Include both customers and prospects

---

## File Specifications

**sample-features.csv:**
- Format: CSV with headers
- Encoding: UTF-8
- Columns: feature, reach, impact, confidence, effort
- Comments: Start with #
- Numeric fields: No currency symbols or units

**sample-interview.txt:**
- Format: Plain text
- Encoding: UTF-8
- Length: 2,000-5,000 words (30-60 min interview)
- Format: Conversational transcript with labels
- Include names and roles for context

---

## Related Documentation

- **RICE Prioritizer:** [../scripts/rice_prioritizer.py](../scripts/rice_prioritizer.py)
- **Customer Interview Analyzer:** [../scripts/customer_interview_analyzer.py](../scripts/customer_interview_analyzer.py)
- **Product Management Guide:** [../SKILL.md](../SKILL.md)

---

**Last Updated:** November 5, 2025
**Format:** Sample Assets README
**Included Files:** 2 (sample-features.csv, sample-interview.txt)
**Script Versions:** rice_prioritizer.py 1.0.0, customer_interview_analyzer.py 1.0.0
