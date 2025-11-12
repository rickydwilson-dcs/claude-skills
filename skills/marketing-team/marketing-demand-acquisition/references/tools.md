# Python Tools Documentation

## calculate_cac.py

### Overview

Calculate blended and channel-specific Customer Acquisition Cost (CAC) with comprehensive metrics and analysis.

### Purpose

Automate CAC calculation across multiple channels, providing actionable insights for demand generation optimization. Essential for budget allocation, channel performance evaluation, and ROI tracking.

### Features

- **Multi-Channel Support** - Analyze CAC for LinkedIn, Google Ads, Facebook, SEO, Partnerships
- **Blended CAC** - Overall customer acquisition cost across all channels
- **Efficiency Metrics** - CAC by channel, CAC payback period, LTV:CAC ratio
- **Trend Analysis** - Month-over-month and quarter-over-quarter comparisons
- **JSON Output** - Machine-readable format for dashboards and reporting
- **Validation** - Input data validation and error handling
- **Recommendations** - Automated suggestions for budget optimization

### Installation

```bash
# No external dependencies - uses Python standard library only
python3 calculate_cac.py --help
```

### Usage

#### Basic Usage

```bash
# Calculate CAC from CSV file
python scripts/calculate_cac.py data/campaign-results.csv

# Calculate with specific time period
python scripts/calculate_cac.py data/q2-2025.csv --period "Q2 2025"

# Output as JSON
python scripts/calculate_cac.py data/results.csv --output json

# Save to file
python scripts/calculate_cac.py data/results.csv --file cac-report.txt
```

#### Advanced Usage

```bash
# Compare multiple periods
python scripts/calculate_cac.py data/q1-2025.csv --compare data/q2-2025.csv

# Set CAC target for recommendations
python scripts/calculate_cac.py data/results.csv --target-cac 500

# Include LTV for ratio calculation
python scripts/calculate_cac.py data/results.csv --ltv 2500

# Full analysis with all options
python scripts/calculate_cac.py data/results.csv \
  --target-cac 500 \
  --ltv 2500 \
  --period "Q2 2025" \
  --output json \
  --file report.json
```

### Input Format

**CSV Structure:**

```csv
channel,spend,customers_acquired,leads,conversions
LinkedIn,20000,32,280,32
Google Search,15000,20,180,20
Google Display,5000,8,120,8
Meta Ads,5000,10,100,10
SEO,2000,15,60,15
Partnerships,3000,10,20,10
Email,1000,5,40,5
```

**Required Columns:**
- `channel` (string) - Marketing channel name
- `spend` (float) - Total spend in dollars
- `customers_acquired` (int) - Number of customers acquired
- `leads` (int) - Number of leads generated (MQLs)
- `conversions` (int) - Number of conversions (SQLs or customers)

**Optional Columns:**
- `impressions` (int) - Ad impressions
- `clicks` (int) - Ad clicks
- `ctr` (float) - Click-through rate
- `cvr` (float) - Conversion rate

### Output Format

#### Human-Readable Output

```
CAC Analysis Report
Period: Q2 2025
Generated: 2025-06-30 14:32:00

BLENDED METRICS
Total Spend: $51,000
Total Customers: 100
Blended CAC: $510

CHANNEL BREAKDOWN
Channel          Spend      Customers    CAC        % of Total
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LinkedIn         $20,000    32           $625       32.0%
Google Search    $15,000    20           $750       20.0%
Meta Ads         $5,000     10           $500       10.0%
SEO              $2,000     15           $133       15.0%
Partnerships     $3,000     10           $300       10.0%

EFFICIENCY METRICS
Top Performing Channels (by CAC):
1. SEO: $133 CAC (lowest)
2. Partnerships: $300 CAC
3. Meta Ads: $500 CAC

Underperforming Channels:
1. Google Search: $750 CAC (target: $500)
2. LinkedIn: $625 CAC (target: $500)

RECOMMENDATIONS
✓ SEO is most efficient channel - consider increasing investment
✓ Partnerships showing strong ROI - expand partner network
⚠ Google Search CAC 50% above target - optimize or reduce spend
⚠ LinkedIn CAC 25% above target - review targeting and creative

BUDGET ALLOCATION SUGGESTION
Based on efficiency, recommended allocation:
- SEO: 30% ($15,300)
- Partnerships: 25% ($12,750)
- Meta Ads: 20% ($10,200)
- LinkedIn: 15% ($7,650)
- Google Search: 10% ($5,100)
```

#### JSON Output

```json
{
  "period": "Q2 2025",
  "generated_at": "2025-06-30T14:32:00Z",
  "blended_metrics": {
    "total_spend": 51000,
    "total_customers": 100,
    "blended_cac": 510,
    "total_leads": 800,
    "total_conversions": 100,
    "overall_conversion_rate": 0.125
  },
  "channels": [
    {
      "name": "LinkedIn",
      "spend": 20000,
      "customers": 32,
      "cac": 625,
      "percentage_of_customers": 32.0,
      "leads": 280,
      "conversion_rate": 0.114,
      "efficiency_score": 0.82
    },
    {
      "name": "SEO",
      "spend": 2000,
      "customers": 15,
      "cac": 133,
      "percentage_of_customers": 15.0,
      "leads": 60,
      "conversion_rate": 0.25,
      "efficiency_score": 3.83
    }
  ],
  "top_performers": [
    {"channel": "SEO", "cac": 133, "reason": "lowest_cac"},
    {"channel": "Partnerships", "cac": 300, "reason": "high_efficiency"}
  ],
  "underperformers": [
    {"channel": "Google Search", "cac": 750, "reason": "above_target", "delta": 250},
    {"channel": "LinkedIn", "cac": 625, "reason": "above_target", "delta": 125}
  ],
  "recommendations": [
    "Increase SEO investment - most efficient channel at $133 CAC",
    "Expand partnership network - strong ROI at $300 CAC",
    "Optimize Google Search targeting - 50% above target CAC",
    "Review LinkedIn creative and audience - 25% above target"
  ]
}
```

### Common Use Cases

#### 1. Monthly Performance Review

```bash
# Generate monthly CAC report
python scripts/calculate_cac.py data/june-2025.csv --period "June 2025"

# Compare to previous month
python scripts/calculate_cac.py data/june-2025.csv \
  --compare data/may-2025.csv \
  --period "June 2025"
```

#### 2. Budget Planning

```bash
# Calculate CAC with target for planning
python scripts/calculate_cac.py data/current-quarter.csv \
  --target-cac 500 \
  --ltv 2500 \
  --output json \
  --file budget-plan.json
```

#### 3. Channel Optimization

```bash
# Identify underperforming channels
python scripts/calculate_cac.py data/all-channels.csv \
  --target-cac 500

# Review recommendations for optimization
```

#### 4. Executive Reporting

```bash
# Generate quarterly report for leadership
python scripts/calculate_cac.py data/q2-2025.csv \
  --period "Q2 2025" \
  --ltv 2500 \
  --file q2-cac-report.txt
```

#### 5. Dashboard Integration

```bash
# Export JSON for dashboard
python scripts/calculate_cac.py data/current.csv \
  --output json \
  --file cac-dashboard.json

# Integrate with BI tool or custom dashboard
```

### Metrics Explained

#### Blended CAC

**Formula:** Total Marketing Spend ÷ Total Customers Acquired

**Definition:** Average cost to acquire a customer across all channels

**Usage:** High-level efficiency metric for overall marketing performance

**Target:** Varies by industry and business model
- B2B SaaS Series A: $500-$1,000
- B2B SaaS Scale-up: $300-$800
- B2C: $50-$300

#### Channel-Specific CAC

**Formula:** Channel Spend ÷ Channel Customers Acquired

**Definition:** Cost to acquire a customer from a specific channel

**Usage:** Channel efficiency comparison, budget allocation decisions

**Benchmarks (B2B SaaS):**
- LinkedIn: $150-$400
- Google Search: $80-$250
- SEO: $50-$150
- Email: $20-$80
- Partnerships: $100-$300

#### Efficiency Score

**Formula:** (Blended CAC ÷ Channel CAC) × Channel % of Customers

**Definition:** Relative efficiency of a channel compared to blended average

**Interpretation:**
- Score > 1.0: More efficient than average
- Score = 1.0: Average efficiency
- Score < 1.0: Less efficient than average

#### LTV:CAC Ratio

**Formula:** Customer Lifetime Value ÷ Customer Acquisition Cost

**Definition:** Return on acquisition investment

**Targets:**
- 3:1 = Minimum acceptable
- 4:1 = Good
- 5:1+ = Excellent
- <3:1 = Unprofitable (need optimization)

#### CAC Payback Period

**Formula:** CAC ÷ (Average Monthly Revenue per Customer × Gross Margin %)

**Definition:** Months to recover customer acquisition cost

**Targets:**
- <12 months = Excellent
- 12-18 months = Good
- 18-24 months = Acceptable
- >24 months = Concerning

### Troubleshooting

#### Issue: "Invalid CSV format"

**Cause:** Missing required columns or incorrect format

**Solution:**
```bash
# Verify CSV has required columns
head -1 data/results.csv

# Required: channel,spend,customers_acquired,leads,conversions
```

#### Issue: "Division by zero error"

**Cause:** Channel has spend but zero customers acquired

**Solution:**
- Review data accuracy
- Consider marking as "test" period
- Use `--min-customers 1` flag to exclude channels with 0 customers

#### Issue: "CAC seems unrealistically low/high"

**Cause:** Data entry error or attribution issue

**Solution:**
```bash
# Verify data
cat data/results.csv

# Check for:
# - Decimal errors (e.g., 20000 vs 20)
# - Attribution issues (customers counted multiple times)
# - Missing spend or customers
```

#### Issue: "JSON output not parsing"

**Cause:** Invalid JSON format or encoding issue

**Solution:**
```bash
# Validate JSON
python -m json.tool cac-report.json

# Check encoding
file cac-report.json
```

### Best Practices

#### 1. Data Collection

- **Consistency:** Use same time period for all channels
- **Attribution:** Single attribution model across channels (first-touch or multi-touch)
- **Completeness:** Include all marketing spend (ads, tools, agencies)
- **Accuracy:** Verify customer counts match CRM records

#### 2. Analysis Frequency

- **Daily:** Monitor major campaigns
- **Weekly:** Review channel performance
- **Monthly:** Calculate CAC and optimize
- **Quarterly:** Deep dive and strategic planning

#### 3. Segmentation

```bash
# Analyze by customer segment
python scripts/calculate_cac.py data/enterprise-customers.csv --period "Enterprise"
python scripts/calculate_cac.py data/smb-customers.csv --period "SMB"

# Compare segments
python scripts/calculate_cac.py data/enterprise.csv --compare data/smb.csv
```

#### 4. Integration with HubSpot

```bash
# Export from HubSpot
# Reports → Custom Report → Export CSV

# Format data for calculate_cac.py
# Match column names: channel, spend, customers_acquired, leads, conversions

# Run analysis
python scripts/calculate_cac.py hubspot-export.csv --period "Current Month"
```

#### 5. Automated Reporting

```bash
#!/bin/bash
# cac-monthly-report.sh

# Set variables
MONTH=$(date +%B-%Y)
DATA_FILE="data/${MONTH}.csv"
REPORT_FILE="reports/cac-${MONTH}.txt"

# Run analysis
python scripts/calculate_cac.py "$DATA_FILE" \
  --period "$MONTH" \
  --target-cac 500 \
  --ltv 2500 \
  --file "$REPORT_FILE"

# Email report (optional)
mail -s "CAC Report: $MONTH" team@company.com < "$REPORT_FILE"
```

### Advanced Features

#### Trend Analysis

```bash
# Compare multiple periods
python scripts/calculate_cac.py data/q1-2025.csv \
  --compare data/q2-2025.csv \
  --trend-analysis

# Output shows:
# - CAC change over time
# - Channel performance trends
# - Growth rates
# - Efficiency improvements
```

#### Cohort Analysis

```bash
# Analyze by customer cohort
python scripts/calculate_cac.py data/january-cohort.csv --cohort "January 2025"

# Compare cohorts
python scripts/calculate_cac.py data/january-cohort.csv \
  --compare data/february-cohort.csv
```

#### Scenario Planning

```bash
# Model different budget allocations
python scripts/calculate_cac.py data/current.csv \
  --scenario "Optimize for LTV" \
  --target-ltv-cac-ratio 5
```

### Performance

**Execution Time:**
- Small dataset (5 channels, 1 month): <0.1 seconds
- Medium dataset (10 channels, 3 months): <0.5 seconds
- Large dataset (20 channels, 12 months): <2 seconds

**Memory Usage:**
- Minimal - processes CSV line by line
- Typical usage: <50MB RAM

**Limitations:**
- Maximum channels: 100
- Maximum data points: 10,000 rows
- File size limit: 50MB

### Integration Examples

#### Automated Dashboard Update

```python
import subprocess
import json

# Run CAC calculation
result = subprocess.run(
    ["python", "scripts/calculate_cac.py", "data/current.csv", "--output", "json"],
    capture_output=True,
    text=True
)

# Parse JSON output
cac_data = json.loads(result.stdout)

# Update dashboard
update_dashboard(cac_data)
```

#### Slack Notification

```bash
#!/bin/bash
# cac-slack-alert.sh

# Calculate CAC
CAC=$(python scripts/calculate_cac.py data/current.csv --output json | jq '.blended_metrics.blended_cac')

# Send alert if CAC exceeds threshold
if (( $(echo "$CAC > 500" | bc -l) )); then
    curl -X POST "$SLACK_WEBHOOK_URL" \
      -H 'Content-Type: application/json' \
      -d "{\"text\":\"⚠️ CAC Alert: Current CAC is \$$CAC (target: \$500)\"}"
fi
```

#### CI/CD Integration

```yaml
# .github/workflows/cac-report.yml
name: Monthly CAC Report

on:
  schedule:
    - cron: '0 9 1 * *'  # First day of month at 9am

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run CAC Analysis
        run: |
          python scripts/calculate_cac.py data/current-month.csv \
            --output json \
            --file cac-report.json
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: cac-report
          path: cac-report.json
```

## Future Enhancements

**Planned Features:**
- Multi-currency support
- Cohort retention analysis
- Predictive CAC modeling
- Integration with common BI tools (Tableau, Looker)
- Real-time monitoring mode
- Custom alert thresholds
- Automated optimization recommendations

**Contribution:**
See repository guidelines for submitting feature requests or improvements.
