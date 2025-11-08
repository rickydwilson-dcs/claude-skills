# Product Management Tools & Integrations

Detailed documentation for Python CLI tools and integration patterns with product management platforms.

## Python CLI Tools

### rice_prioritizer.py

Advanced RICE framework implementation with portfolio analysis.

**Installation:**
```bash
# No dependencies required - uses Python standard library
python3 --version  # Requires Python 3.8+
```

**Full Usage:**
```bash
# Create sample CSV with example features
python3 scripts/rice_prioritizer.py sample

# Basic prioritization
python3 scripts/rice_prioritizer.py features.csv

# With custom team capacity (person-months per quarter)
python3 scripts/rice_prioritizer.py features.csv --capacity 20

# JSON output for tool integration
python3 scripts/rice_prioritizer.py features.csv --output json

# CSV output for spreadsheet import
python3 scripts/rice_prioritizer.py features.csv --output csv

# Save to file instead of stdout
python3 scripts/rice_prioritizer.py features.csv -o json -f roadmap.json

# Verbose mode for debugging
python3 scripts/rice_prioritizer.py features.csv -v
```

**Available Options:**
- `input`: Input CSV file path (required unless using `sample`)
- `sample`: Generate sample CSV file (no other args needed)
- `--capacity`: Team capacity in person-months (default: 15)
- `--output/-o`: Output format (text, json, csv) - default: text
- `--file/-f`: Write output to file instead of stdout
- `--verbose/-v`: Enable detailed output with explanations
- `--help`: Show complete help message with examples

**Input CSV Format:**
```csv
name,reach,impact,confidence,effort
Feature Name,500,2,0.8,5
```

**Fields:**
- `name`: Feature name (string)
- `reach`: Users affected per quarter (integer)
- `impact`: massive=3, high=2, medium=1, low=0.5, minimal=0.25
- `confidence`: high=1.0, medium=0.8, low=0.5
- `effort`: Person-months (float: 0.5, 1, 2, 5, 8+)

**Output Formats:**

**Text Output (Human-Readable):**
```
RICE Prioritization Results
===========================

Top Priorities:
1. Feature A (Score: 240.0)
   - Reach: 500 users/quarter
   - Impact: High (2x)
   - Confidence: 80%
   - Effort: 5 person-months

Portfolio Analysis:
- Quick Wins (high value, low effort): 3 features
- Big Bets (high value, high effort): 2 features
- Fill-Ins (low value, low effort): 1 feature
- Time Sinks (low value, high effort): 0 features

Quarterly Roadmap (15 person-months capacity):
Q1: Feature A, Feature B (14 person-months)
Q2: Feature C (12 person-months)
```

**JSON Output (Tool Integration):**
```json
{
  "features": [
    {
      "name": "Feature A",
      "reach": 500,
      "impact": 2,
      "impact_label": "high",
      "confidence": 0.8,
      "confidence_label": "medium",
      "effort": 5,
      "rice_score": 240.0,
      "rank": 1,
      "category": "quick_win"
    }
  ],
  "portfolio": {
    "quick_wins": 3,
    "big_bets": 2,
    "fill_ins": 1,
    "time_sinks": 0
  },
  "roadmap": {
    "q1": ["Feature A", "Feature B"],
    "q2": ["Feature C"]
  },
  "capacity": {
    "total": 15,
    "used_q1": 14,
    "used_q2": 12
  }
}
```

**Features:**
- RICE score calculation with formula validation
- Portfolio categorization (2x2 matrix)
- Capacity-based roadmap generation
- Flexible output formats for different workflows

**Common Workflows:**

**Weekly Prioritization Review:**
```bash
# Update features.csv with latest data
# Run prioritization
python3 scripts/rice_prioritizer.py features.csv

# Export for presentation
python3 scripts/rice_prioritizer.py features.csv -o json -f weekly-priorities.json
```

**Quarterly Planning:**
```bash
# Set team capacity for quarter
python3 scripts/rice_prioritizer.py features.csv --capacity 30 -v

# Generate roadmap
python3 scripts/rice_prioritizer.py features.csv --capacity 30 -o csv -f q2-roadmap.csv
```

---

### customer_interview_analyzer.py

NLP-based interview transcript analysis for extracting actionable insights.

**Installation:**
```bash
# No dependencies required - uses Python standard library
python3 --version  # Requires Python 3.8+
```

**Full Usage:**
```bash
# Analyze single interview transcript
python3 scripts/customer_interview_analyzer.py interview.txt

# JSON output for research tools
python3 scripts/customer_interview_analyzer.py interview.txt --output json

# Save analysis to file
python3 scripts/customer_interview_analyzer.py interview.txt -o json -f analysis.json

# Verbose mode for debugging
python3 scripts/customer_interview_analyzer.py interview.txt -v
```

**Available Options:**
- `input`: Input transcript file path (required)
- `--output/-o`: Output format (text, json, csv) - default: text
- `--file/-f`: Write output to file instead of stdout
- `--verbose/-v`: Enable detailed output with pattern matching details
- `--help`: Show complete help message with examples

**Input Format:**
Plain text transcript file. Works best with:
- Interview transcripts (verbatim)
- Customer feedback emails
- Support ticket conversations
- Survey responses (long-form)

**Analysis Capabilities:**

**1. Pain Point Extraction**
- Detects frustration language
- Severity scoring (high/medium/low)
- Context extraction

**2. Feature Request Identification**
- Recognizes "I wish," "It would be great if" patterns
- Priority classification
- Groups similar requests

**3. Jobs-to-be-Done Recognition**
- Identifies goal-oriented language
- Extracts user objectives
- Maps to JTBD framework

**4. Sentiment Analysis**
- Overall sentiment (positive/negative/neutral)
- Sentiment per topic
- Emotional intensity scoring

**5. Theme Extraction**
- Clusters similar topics
- Frequency counting
- Key concept identification

**6. Competitor Mentions**
- Detects brand names
- Comparison context
- Feature gaps identified

**7. Key Quote Identification**
- Finds impactful quotes
- Prioritizes for storytelling
- Tags by theme

**Output Formats:**

**Text Output (Human-Readable):**
```
Customer Interview Analysis
===========================

PAIN POINTS (3 identified):
1. [HIGH] Data export takes too long
   Quote: "I have to wait 5 minutes for a CSV export, which breaks my flow"

2. [MEDIUM] Search results not relevant
   Quote: "When I search, I get results from archived projects"

FEATURE REQUESTS (2 identified):
1. [HIGH PRIORITY] Real-time collaboration
   Quote: "I wish I could see what my teammate is editing"

JOBS TO BE DONE:
- Analyze weekly sales data quickly
- Share insights with stakeholders
- Track changes over time

SENTIMENT: Mostly Positive (7/10)
Positive aspects: Ease of use, reliability
Negative aspects: Performance, search quality

KEY THEMES:
- Performance (mentioned 5 times)
- Collaboration (mentioned 3 times)
- Data export (mentioned 4 times)

COMPETITOR MENTIONS:
- Excel: "Excel is faster for large datasets"
- Tableau: "Tableau has better visualizations"
```

**JSON Output (Tool Integration):**
```json
{
  "pain_points": [
    {
      "text": "Data export takes too long",
      "severity": "high",
      "frequency": 3,
      "context": "CSV export workflow",
      "quotes": ["I have to wait 5 minutes..."]
    }
  ],
  "feature_requests": [
    {
      "text": "Real-time collaboration",
      "priority": "high",
      "mentions": 2,
      "quotes": ["I wish I could see what my teammate is editing"]
    }
  ],
  "jobs_to_be_done": [
    "Analyze weekly sales data quickly",
    "Share insights with stakeholders"
  ],
  "sentiment": {
    "overall": "positive",
    "score": 0.7,
    "positive_aspects": ["ease of use", "reliability"],
    "negative_aspects": ["performance", "search quality"]
  },
  "themes": [
    {"theme": "performance", "frequency": 5},
    {"theme": "collaboration", "frequency": 3}
  ],
  "competitors": [
    {"name": "Excel", "context": "faster for large datasets"},
    {"name": "Tableau", "context": "better visualizations"}
  ]
}
```

**Common Workflows:**

**Post-Interview Analysis:**
```bash
# Transcribe interview (use Otter.ai, etc.)
# Save as interview-001.txt

# Run analysis
python3 scripts/customer_interview_analyzer.py interview-001.txt

# Export for research tool
python3 scripts/customer_interview_analyzer.py interview-001.txt -o json -f interview-001-analysis.json
```

**Batch Analysis:**
```bash
# Analyze multiple interviews
for file in interviews/*.txt; do
  python3 scripts/customer_interview_analyzer.py "$file" -o json -f "analysis/$(basename $file .txt).json"
done

# Combine insights manually or with custom script
```

---

## Integration Patterns

### Jira/Linear Integration

Export RICE prioritization to issue tracking tools.

**Workflow:**
```bash
# 1. Generate JSON output
python3 scripts/rice_prioritizer.py features.csv -o json -f priorities.json

# 2. Import to Jira using API
curl -X POST https://your-domain.atlassian.net/rest/api/3/issue/bulk \
  -H "Authorization: Bearer $JIRA_TOKEN" \
  -H "Content-Type: application/json" \
  -d @priorities.json

# 3. Or use Jira CSV import
python3 scripts/rice_prioritizer.py features.csv -o csv -f jira-import.csv
# Import via Jira UI: Issues > Import issues from CSV
```

**Jira Custom Fields:**
- RICE Score: Number field
- Reach: Number field
- Impact: Select (Massive, High, Medium, Low, Minimal)
- Confidence: Select (High, Medium, Low)
- Effort: Number field (person-months)

**Automation:**
```bash
# Create weekly cron job
0 9 * * 1 cd /path/to/product-manager-toolkit && python3 scripts/rice_prioritizer.py features.csv -o json -f /path/to/output/weekly-priorities.json
```

---

### ProductBoard Integration

Sync features and user insights.

**User Insights from Interviews:**
```bash
# Analyze interview
python3 scripts/customer_interview_analyzer.py interview.txt -o json -f insights.json

# Import to ProductBoard via API
curl -X POST https://api.productboard.com/insights \
  -H "Authorization: Bearer $PB_TOKEN" \
  -H "Content-Type: application/json" \
  -d @insights.json
```

**Feature Prioritization Sync:**
```bash
# Export RICE scores
python3 scripts/rice_prioritizer.py features.csv -o json -f rice-scores.json

# Update ProductBoard feature scores
# (Use ProductBoard API or Zapier integration)
```

---

### Amplitude/Mixpanel Analytics

Track feature adoption and success metrics.

**Post-Launch Analysis:**
```bash
# Export feature list with metrics
python3 scripts/rice_prioritizer.py features.csv -o json -f features.json

# Track in analytics (example event structure)
{
  "event": "feature_used",
  "properties": {
    "feature_name": "Feature A",
    "rice_score": 240.0,
    "category": "quick_win",
    "user_id": "user123"
  }
}
```

**Success Metrics Dashboard:**
- Filter events by feature_name
- Calculate adoption rate (% of users)
- Compare predicted RICE score vs actual usage
- Validate reach estimates

---

### Figma/Design Tools

Use prioritization data in design handoff.

**Design Handoff Workflow:**
```bash
# Generate roadmap
python3 scripts/rice_prioritizer.py features.csv -o json -f roadmap.json

# Share with design team
# Include RICE scores in Figma files
# Prioritize design work based on roadmap
```

**FigJam Planning:**
- Import roadmap.json
- Create prioritization matrix visual
- Tag designs with RICE categories

---

### Dovetail/UserVoice Research Tools

Import interview analysis for synthesis.

**Interview Import:**
```bash
# Analyze transcript
python3 scripts/customer_interview_analyzer.py interview.txt -o json -f analysis.json

# Import to Dovetail via API
curl -X POST https://api.dovetailapp.com/v1/notes \
  -H "Authorization: Bearer $DOVETAIL_TOKEN" \
  -H "Content-Type: application/json" \
  -d @analysis.json
```

**Synthesis Workflow:**
1. Conduct interviews
2. Run analyzer on transcripts
3. Import pain points as "tags" in Dovetail
4. Import feature requests as separate notes
5. Create affinity map from themes

---

### Slack/Notion Communication

Share prioritization decisions with team.

**Slack Bot Integration:**
```bash
# Send weekly priorities to Slack
python3 scripts/rice_prioritizer.py features.csv -o json | \
  jq -r '.features[:5] | .[] | "• \(.name) (Score: \(.rice_score))"' | \
  curl -X POST $SLACK_WEBHOOK_URL \
    -H "Content-Type: application/json" \
    -d '{"text": "Top 5 Priorities This Week", "blocks": [...]}'
```

**Notion Database Sync:**
```bash
# Export to CSV
python3 scripts/rice_prioritizer.py features.csv -o csv -f notion-import.csv

# Import to Notion database
# Use Notion CSV import feature
```

---

### GitHub/GitLab Project Management

Track feature development with RICE context.

**Issue Template:**
```markdown
## Feature: [Name]
**RICE Score:** [240.0]
- Reach: [500 users/quarter]
- Impact: [High (2x)]
- Confidence: [Medium (80%)]
- Effort: [5 person-months]

**Priority:** [Quick Win]

**Problem:**
[Description]

**Success Metrics:**
[Metrics from PRD]
```

**Automation with GitHub Actions:**
```yaml
name: Update Prioritization
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday

jobs:
  prioritize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run RICE Prioritization
        run: |
          python3 scripts/rice_prioritizer.py features.csv -o json -f priorities.json
      - name: Update Issues
        run: |
          # Script to update GitHub issues with priorities
```

---

## Quick Commands Cheat Sheet

```bash
# Generate sample data for testing
python scripts/rice_prioritizer.py sample

# Basic prioritization
python scripts/rice_prioritizer.py features.csv

# Quarterly planning with capacity
python scripts/rice_prioritizer.py features.csv --capacity 30

# Export for Jira
python scripts/rice_prioritizer.py features.csv -o csv -f jira-import.csv

# Interview analysis
python scripts/customer_interview_analyzer.py interview.txt

# Batch interview analysis
for f in interviews/*.txt; do
  python scripts/customer_interview_analyzer.py "$f" -o json -f "analysis/$(basename $f .txt).json"
done

# JSON outputs for tool integration
python scripts/rice_prioritizer.py features.csv --output json -f priorities.json
python scripts/customer_interview_analyzer.py interview.txt -o json -f insights.json
```

---

## Platform-Specific Setup

### Jira Cloud Setup

**Step 1: Create Custom Fields**
1. Go to Jira Settings > Issues > Custom fields
2. Create fields:
   - RICE Score (Number)
   - Reach (Number)
   - Impact (Single Select: Massive/High/Medium/Low/Minimal)
   - Confidence (Single Select: High/Medium/Low)
   - Effort (Number)

**Step 2: Add to Screen**
1. Go to Screens
2. Add custom fields to "Create/Edit Issue" screen

**Step 3: Export/Import**
```bash
# Export from tool
python scripts/rice_prioritizer.py features.csv -o csv -f jira-import.csv

# Import via Jira
# Issues > Import issues from CSV
```

---

### ProductBoard Setup

**Step 1: API Key**
1. Settings > Integrations > API
2. Generate API token
3. Export to environment: `export PB_TOKEN=your_token`

**Step 2: Import Features**
```bash
python scripts/rice_prioritizer.py features.csv -o json -f features.json

# Use ProductBoard API or Zapier
```

---

### Amplitude Setup

**Step 1: Define Events**
```javascript
amplitude.track('feature_prioritized', {
  feature_name: 'Feature A',
  rice_score: 240.0,
  category: 'quick_win',
  quarter: 'Q2 2025'
});
```

**Step 2: Create Dashboard**
- Chart 1: Features by RICE score
- Chart 2: Quick wins vs big bets distribution
- Chart 3: Quarterly capacity usage

---

## Troubleshooting

### Common Issues

**Issue: "No module named 'csv'"**
```bash
# Solution: Update Python version (requires 3.8+)
python3 --version
# If < 3.8, install latest Python
```

**Issue: "CSV parse error"**
```bash
# Solution: Check CSV format
head -5 features.csv

# Ensure format matches:
# name,reach,impact,confidence,effort
# Feature A,500,2,0.8,5
```

**Issue: "Invalid impact value"**
```bash
# Solution: Use numeric values
# massive=3, high=2, medium=1, low=0.5, minimal=0.25
```

**Issue: "Interview analyzer returns empty"**
```bash
# Solution: Check transcript format
# - Should be plain text
# - Remove timestamps/speaker labels
# - One paragraph per line
```

---

**Last Updated:** 2025-11-08
**Related Files:**
- [frameworks.md](frameworks.md) - RICE methodology, discovery frameworks
- [templates.md](templates.md) - PRD templates, interview scripts
