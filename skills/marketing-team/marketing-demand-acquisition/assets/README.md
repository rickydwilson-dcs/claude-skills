# Marketing Demand Acquisition - Sample Assets

This directory contains sample input files for testing the Customer Acquisition Cost (CAC) calculator and demand generation analysis tools.

## Sample Files

### 1. sample-channels.json
**Purpose:** Marketing channel data for CAC calculation and channel performance analysis

**Description:** Realistic Q4 2025 marketing performance data including:
- 7 marketing channels (LinkedIn, Google Search, SEO, Partnerships, Content, Email, Trade Shows)
- Spend amounts (realistic B2B SaaS ranges)
- Customer acquisition counts
- Channel-specific notes and targeting info
- Metadata about company performance

**Data Fields:**
- `channel`: Marketing channel name
- `spend`: Total spend for the period (USD)
- `customers`: Number of customers acquired
- `period`: Time period covered
- `notes`: Context about the channel performance

**How to Use:**
```bash
# Calculate CAC by channel
python ../scripts/calculate_cac.py sample-channels.json

# Get JSON output
python ../scripts/calculate_cac.py sample-channels.json --output json

# Save results to file
python ../scripts/calculate_cac.py sample-channels.json --output json -f cac-report.json

# Include benchmarks comparison
python ../scripts/calculate_cac.py sample-channels.json --benchmarks
```

**What to Expect:**
- Individual CAC for each channel
- Blended CAC (total spend / total customers)
- Channel performance comparison
- Benchmark data for Series A/B SaaS companies
- Insight into which channels are most efficient

---

## Using This Sample

### Quick Start
```bash
cd /Users/ricky/Library/CloudStorage/GoogleDrive-rickydwilson@gmail.com/My\ Drive/Websites/GitHub/claude-skills/marketing-skill/marketing-demand-acquisition/

# Basic CAC analysis
python scripts/calculate_cac.py assets/sample-channels.json

# With benchmarks for comparison
python scripts/calculate_cac.py assets/sample-channels.json --benchmarks

# Full JSON export
python scripts/calculate_cac.py assets/sample-channels.json -o json -f analysis.json
```

### Understanding the Output

The script calculates:
1. **Individual CAC per channel** = Spend / Customers Acquired
2. **Blended CAC** = Total Spend / Total Customers
3. **Comparison to benchmarks** = How your channels compare to industry standards

**Example Output Interpretation:**
```
LinkedIn Ads:   $556 CAC
Google Search:  $290 CAC  ✓ (Below average)
SEO/Organic:    $229 CAC  ✓ (Efficient)
Partnerships:   $278 CAC
Content:        $429 CAC
Email:          $200 CAC  ✓ (Most efficient)
Trade Shows:    $682 CAC  (Highest, review ROI)

Blended CAC: $382
Target (B2B SaaS): <$300

Action Items:
- Increase SEO/organic investment (most efficient)
- Review trade show ROI
- Scale email and organic strategies
```

---

## Creating Your Own Sample Data

### Format Requirements

Your JSON file should include a "channels" array with objects containing:

**Option 1: Simple array format**
```json
[
  {
    "channel": "Channel Name",
    "spend": 10000,
    "customers": 20
  }
]
```

**Option 2: Object with metadata**
```json
{
  "channels": [
    {
      "channel": "Channel Name",
      "spend": 10000,
      "customers": 20,
      "period": "Q4 2025",
      "notes": "Optional context"
    }
  ],
  "metadata": {
    "company": "Company Name",
    "fiscal_quarter": "Q4 2025"
  }
}
```

### Data Tips

1. **Spend Values:**
   - Use realistic amounts for your business
   - Include all direct costs (ads, tools, labor if applicable)
   - Use consistent currency (USD, EUR, etc.)

2. **Customer Counts:**
   - Track customers from each channel using UTM parameters or tracking codes
   - Be consistent with your definition (leads, trials, paid customers)
   - Document your attribution model

3. **Channel Selection:**
   - Include all major channels
   - Add secondary channels for comprehensive view
   - Include organic/free channels for baseline

4. **Example Channel Definitions:**

| Channel | Typical Spend Range | Typical CAC Range |
|---------|-------------------|------------------|
| LinkedIn Ads | $10K-$50K/quarter | $100-$500 |
| Google Search | $5K-$30K/quarter | $50-$300 |
| SEO/Organic | $2K-$15K/quarter | $50-$200 |
| Partnerships | $2K-$20K/quarter | $100-$400 |
| Content Marketing | $5K-$25K/quarter | $100-$500 |
| Email Marketing | $1K-$10K/quarter | $50-$300 |
| Trade Shows | $10K-$50K/quarter | $300-$1000 |

---

## Interpreting Results

### CAC Benchmarks (B2B SaaS - Series A)
- **LinkedIn Ads:** $150-$400
- **Google Search:** $80-$250
- **SEO/Organic:** $50-$150
- **Partnerships:** $100-$300
- **Blended Target:** <$300

### Key Metrics to Track
- **CAC**: Customer acquisition cost per channel
- **CAC Payback Period**: How long to recoup acquisition costs
- **LTV:CAC Ratio**: Should be 3:1 or higher (LTV = CAC * 3 minimum)
- **Channel Efficiency**: Lower CAC = more efficient

### When to Optimize Channels

**Increase Investment If:**
- CAC is below your target
- Channel has highest conversion rate
- Customer quality is highest (lower churn)
- Good brand fit

**Reduce or Audit If:**
- CAC is 2x+ your target
- Conversion rate declining
- Customer quality issues
- Poor channel fit

---

## Advanced Use Cases

### 1. Quarterly Trend Analysis
Create sample-channels.json for each quarter to track:
- Channel efficiency trends
- Seasonal variations
- Impact of campaigns

### 2. Channel Comparison
Use the same time period but different channels:
- Identify best performing channels
- Allocate budget based on efficiency
- Plan channel mix optimization

### 3. Scenario Planning
Create multiple versions with different assumptions:
- What if we 2x LinkedIn spend?
- What if organic grows 30%?
- What if we exit a low-performing channel?

---

## Integration Tips

### With Product Team
Link CAC data to:
- Product adoption metrics
- Retention rates
- LTV calculations
- Revenue impact

### With Financial Planning
Use CAC for:
- Marketing budget allocation
- Profitability analysis
- Unit economics modeling
- Growth scenario planning

### With Sales Team
Share insights about:
- Best-performing channels
- Customer quality by channel
- Pipeline source attribution
- Quota sizing by channel

---

## Troubleshooting

**Issue:** "Error: JSON file must contain 'channels'"
- Make sure your JSON has a "channels" array or is itself an array
- Check file is valid JSON (use jsonlint.com to validate)

**Issue:** "Missing values" warning
- Ensure all channels have 'channel', 'spend', 'customers' fields
- Check for typos or empty fields

**Issue:** CAC seems unrealistic
- Verify spend amounts are complete (include all costs)
- Check customer count attribution is correct
- Review whether you're using right customer definition

**Issue:** Can't run the script
- Ensure Python 3.8+ is installed
- Check file path is correct
- Verify JSON file is readable

---

## File Specifications

- **File Format:** JSON
- **Encoding:** UTF-8
- **Max File Size:** 10MB (easily handles 1000+ channels)
- **Structure:** Array or object with "channels" key
- **Validation:** Must be valid JSON

---

## Related Documentation

- **CAC Calculator Details:** [../scripts/calculate_cac.py](../scripts/calculate_cac.py)
- **Demand Generation Strategy:** [../SKILL.md](../SKILL.md)
- **Marketing Metrics Guide:** [../references/](../references/)

---

**Last Updated:** November 5, 2025
**Format:** Sample Assets README
**Included Files:** 1 (sample-channels.json)
**Python Script Version:** calculate_cac.py 1.0.0
