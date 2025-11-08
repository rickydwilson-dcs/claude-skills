# CEO Python Tools Documentation

Comprehensive guide to CEO advisory Python tools for strategic analysis and financial modeling.

## Strategy Analyzer

**Script:** `scripts/strategy_analyzer.py`

### Purpose

Analyzes company strategic position using multiple frameworks:
- SWOT Analysis
- Porter's Five Forces
- BCG Matrix positioning
- Strategic recommendations with prioritization

### Installation

```bash
# No additional dependencies required (uses Python standard library)
python --version  # Requires Python 3.8+
```

### Input Format

The tool accepts JSON input with company data:

```json
{
  "name": "Company Name",
  "market_position": {
    "market_share": 35,
    "brand_strength": 65,
    "competitive_advantage": 70
  },
  "financial_health": {
    "revenue_growth": 45,
    "profitability": 40,
    "cash_flow": 55
  },
  "organizational_capability": {
    "talent": 70,
    "culture": 65,
    "leadership": 75
  },
  "growth_potential": {
    "market_size": 80,
    "expansion_opportunities": 70
  },
  "competitive_forces": {
    "rivalry": 70,
    "suppliers": 40,
    "buyers": 60,
    "new_entrants": 50,
    "substitutes": 45
  },
  "context": {
    "industry_disruption": true,
    "cash_available": 150000000,
    "regulatory_pressure": false
  },
  "timeline": 18
}
```

### Field Definitions

**market_position** (scores 0-100)
- `market_share`: Company's market share percentage
- `brand_strength`: Brand recognition and reputation
- `competitive_advantage`: Unique competitive differentiators

**financial_health** (scores 0-100)
- `revenue_growth`: Revenue growth rate percentage
- `profitability`: Profit margin level
- `cash_flow`: Cash flow health and runway

**organizational_capability** (scores 0-100)
- `talent`: Quality and depth of talent
- `culture`: Organizational culture strength
- `leadership`: Leadership team effectiveness

**growth_potential** (scores 0-100)
- `market_size`: Total addressable market size
- `expansion_opportunities`: Available growth channels

**competitive_forces** (scores 0-100, higher = more intense)
- `rivalry`: Intensity of competitive rivalry
- `suppliers`: Bargaining power of suppliers
- `buyers`: Bargaining power of buyers
- `new_entrants`: Threat of new entrants (optional)
- `substitutes`: Threat of substitutes (optional)

**context** (boolean or numeric)
- `industry_disruption`: Is industry facing disruption? (true/false)
- `cash_available`: Cash available for investments ($)
- `regulatory_pressure`: Facing regulatory challenges? (true/false, optional)

**timeline**
- Number of months for strategic planning horizon

### Usage Examples

**Basic Analysis (Human-Readable Output)**
```bash
python scripts/strategy_analyzer.py company_data.json
```

Output includes:
- Executive summary
- SWOT analysis with specific items
- Porter's Five Forces assessment
- BCG Matrix positioning
- Strategic recommendations with priorities

**JSON Output (For Dashboards/Integration)**
```bash
python scripts/strategy_analyzer.py company_data.json --output json
```

Returns structured JSON with all analysis results.

**Save to File**
```bash
python scripts/strategy_analyzer.py company_data.json -o json -f strategy_report.json
```

**View Help and Schema**
```bash
python scripts/strategy_analyzer.py --help
```

### Output Interpretation

**SWOT Analysis**
- **Strengths**: Internal positive attributes (>70 scores)
- **Weaknesses**: Internal limitations (<50 scores)
- **Opportunities**: External positive factors
- **Threats**: External risks

**Porter's Five Forces**
- Each force rated as: Weak, Moderate, Strong, Very Strong
- Overall competitive intensity: Low, Moderate, High, Very High
- Lower scores = more favorable competitive position

**BCG Matrix**
- **Star**: High growth, high share → Invest for dominance
- **Cash Cow**: Low growth, high share → Maximize cash generation
- **Question Mark**: High growth, low share → Selective investment
- **Dog**: Low growth, low share → Harvest or divest

**Strategic Recommendations**
- Prioritized by: Critical, High Priority, Medium Priority
- Each includes specific actions and rationale
- Timeline considerations included

### Example Analysis Session

```bash
# 1. Create input file
cat > techcorp.json << 'EOF'
{
  "name": "TechCorp Inc.",
  "market_position": {"market_share": 35, "brand_strength": 65, "competitive_advantage": 70},
  "financial_health": {"revenue_growth": 45, "profitability": 40, "cash_flow": 55},
  "organizational_capability": {"talent": 70, "culture": 65, "leadership": 75},
  "growth_potential": {"market_size": 80, "expansion_opportunities": 70},
  "competitive_forces": {"rivalry": 70, "suppliers": 40, "buyers": 60},
  "context": {"industry_disruption": true, "cash_available": 150000000},
  "timeline": 18
}
EOF

# 2. Run analysis
python scripts/strategy_analyzer.py techcorp.json

# 3. Generate JSON for board presentation
python scripts/strategy_analyzer.py techcorp.json -o json -f board_strategy.json

# 4. Review results
cat board_strategy.json | python -m json.tool
```

## Financial Scenario Analyzer

**Script:** `scripts/financial_scenario_analyzer.py`

### Purpose

Models multiple financial scenarios with:
- Revenue projections (linear or exponential growth)
- Profitability analysis
- Cash runway calculations
- NPV and IRR calculations
- Risk-adjusted scenario analysis
- Comparative scenario recommendations

### Installation

```bash
# No additional dependencies required (uses Python standard library)
python --version  # Requires Python 3.8+
```

### Input Format

```json
{
  "base_case": {
    "revenue": 5000000,
    "cogs": 1500000,
    "operating_expenses": 3000000,
    "cash": 2000000,
    "burn_rate": 200000,
    "valuation": 20000000
  },
  "scenarios": [
    {
      "name": "Aggressive Growth",
      "probability": 0.3,
      "growth_model": "exponential",
      "growth_rate": 0.5,
      "cogs_ratio": 0.25,
      "opex_growth": 0.3,
      "discount_rate": 0.12
    },
    {
      "name": "Moderate Growth",
      "probability": 0.5,
      "growth_rate": 0.3,
      "cogs_ratio": 0.3,
      "discount_rate": 0.10
    },
    {
      "name": "Conservative",
      "probability": 0.2,
      "growth_rate": 0.15,
      "cogs_ratio": 0.28,
      "discount_rate": 0.08
    }
  ],
  "projection_years": 3
}
```

### Field Definitions

**base_case** (all values in dollars unless noted)
- `revenue`: Current annual revenue
- `cogs`: Cost of goods sold
- `operating_expenses`: Operating expenses (salaries, marketing, etc.)
- `cash`: Current cash balance
- `burn_rate`: Monthly cash burn
- `valuation`: Current company valuation

**scenarios** (array of scenario objects)
- `name`: Scenario name
- `probability`: Probability of scenario (0-1, should sum to 1.0)
- `growth_model`: "linear" or "exponential" (default: linear)
- `growth_rate`: Annual growth rate (0.3 = 30%)
- `cogs_ratio`: COGS as ratio of revenue (0.25 = 25%)
- `opex_growth`: Operating expense growth rate (optional, defaults to 0.15)
- `discount_rate`: Discount rate for NPV calculation (0.12 = 12%)

**projection_years** (optional)
- Number of years to project (default: 3)

### Usage Examples

**Basic Analysis**
```bash
python scripts/financial_scenario_analyzer.py scenarios.json
```

**JSON Output**
```bash
python scripts/financial_scenario_analyzer.py scenarios.json --output json
```

**Save Analysis**
```bash
python scripts/financial_scenario_analyzer.py scenarios.json -o json -f financial_analysis.json
```

**View Help**
```bash
python scripts/financial_scenario_analyzer.py --help
```

### Output Interpretation

**For Each Scenario:**

1. **Revenue Projections**
   - Year-by-year revenue growth
   - Comparison to base case
   - Growth trajectory visualization

2. **Profitability Analysis**
   - Gross margin trends
   - EBITDA progression
   - Path to profitability

3. **Cash Position**
   - Cash runway calculation
   - Burn rate evolution
   - Capital requirements

4. **Investment Metrics**
   - NPV (Net Present Value)
   - IRR (Internal Rate of Return)
   - Payback period

5. **Risk Assessment**
   - Probability-weighted outcomes
   - Downside protection
   - Sensitivity analysis

**Comparative Analysis:**
- Side-by-side scenario comparison
- Risk-adjusted recommendations
- Decision framework for capital allocation

### Example Scenarios

**SaaS Company Example**
```bash
cat > saas_scenarios.json << 'EOF'
{
  "base_case": {
    "revenue": 10000000,
    "cogs": 2000000,
    "operating_expenses": 7000000,
    "cash": 5000000,
    "burn_rate": 500000,
    "valuation": 50000000
  },
  "scenarios": [
    {
      "name": "Triple Down on Growth",
      "probability": 0.25,
      "growth_model": "exponential",
      "growth_rate": 0.80,
      "cogs_ratio": 0.20,
      "opex_growth": 0.50,
      "discount_rate": 0.15
    },
    {
      "name": "Balanced Growth",
      "probability": 0.50,
      "growth_rate": 0.40,
      "cogs_ratio": 0.20,
      "opex_growth": 0.25,
      "discount_rate": 0.12
    },
    {
      "name": "Path to Profitability",
      "probability": 0.25,
      "growth_rate": 0.20,
      "cogs_ratio": 0.18,
      "opex_growth": 0.10,
      "discount_rate": 0.08
    }
  ],
  "projection_years": 5
}
EOF

python scripts/financial_scenario_analyzer.py saas_scenarios.json
```

**Hardware Startup Example**
```bash
cat > hardware_scenarios.json << 'EOF'
{
  "base_case": {
    "revenue": 3000000,
    "cogs": 1500000,
    "operating_expenses": 2000000,
    "cash": 8000000,
    "burn_rate": 300000,
    "valuation": 30000000
  },
  "scenarios": [
    {
      "name": "Manufacturing Scale",
      "probability": 0.30,
      "growth_rate": 1.0,
      "cogs_ratio": 0.40,
      "opex_growth": 0.40,
      "discount_rate": 0.15
    },
    {
      "name": "Controlled Growth",
      "probability": 0.50,
      "growth_rate": 0.50,
      "cogs_ratio": 0.45,
      "opex_growth": 0.20,
      "discount_rate": 0.12
    },
    {
      "name": "Conservative Ramp",
      "probability": 0.20,
      "growth_rate": 0.25,
      "cogs_ratio": 0.48,
      "opex_growth": 0.10,
      "discount_rate": 0.10
    }
  ],
  "projection_years": 3
}
EOF

python scripts/financial_scenario_analyzer.py hardware_scenarios.json
```

### Best Practices

**Scenario Design**
1. Always include at least 3 scenarios (upside, base, downside)
2. Ensure probabilities sum to 1.0
3. Use realistic growth rates based on industry benchmarks
4. Adjust COGS ratios based on business model and scale
5. Factor in increased opex for growth scenarios

**Data Quality**
1. Use actual financial data for base case
2. Validate assumptions with historical performance
3. Benchmark against comparable companies
4. Stress test with extreme scenarios
5. Update models quarterly

**Interpretation**
1. Focus on range of outcomes, not single point estimates
2. Consider probability-weighted expected values
3. Assess cash requirements under different scenarios
4. Identify key assumptions driving results
5. Plan for downside scenarios

## Integration Workflows

### Board Meeting Preparation

```bash
# 1. Strategic analysis
python scripts/strategy_analyzer.py company_data.json -o json -f strategy.json

# 2. Financial scenarios
python scripts/financial_scenario_analyzer.py scenarios.json -o json -f financials.json

# 3. Use outputs in board deck
# - Strategy slides from strategy.json
# - Financial projections from financials.json
```

### Quarterly Planning

```bash
# 1. Analyze current position
python scripts/strategy_analyzer.py q4_data.json

# 2. Model next year scenarios
python scripts/financial_scenario_analyzer.py fy2025_scenarios.json

# 3. Generate OKRs based on analysis
# Use insights to set realistic but ambitious goals
```

### Fundraising Preparation

```bash
# 1. Strategic positioning
python scripts/strategy_analyzer.py market_analysis.json -o json

# 2. Financial projections for deck
python scripts/financial_scenario_analyzer.py raise_scenarios.json -o json -f projections.json

# 3. Incorporate into pitch deck
# Use for market opportunity and financial slides
```

## Troubleshooting

### Common Issues

**Issue: "File not found" error**
```bash
# Solution: Use absolute path or ensure you're in correct directory
python scripts/strategy_analyzer.py /full/path/to/data.json
```

**Issue: "Invalid JSON" error**
```bash
# Solution: Validate JSON syntax
python -m json.tool your_file.json
# Fix any syntax errors shown
```

**Issue: Unexpected results**
```bash
# Solution: Verify input data ranges
# - Scores should be 0-100
# - Probabilities should sum to 1.0
# - Growth rates are decimals (0.5 = 50%)
```

**Issue: Script won't execute**
```bash
# Solution: Make script executable
chmod +x scripts/strategy_analyzer.py

# Or run with python explicitly
python scripts/strategy_analyzer.py data.json
```

### Getting Help

```bash
# View detailed help
python scripts/strategy_analyzer.py --help
python scripts/financial_scenario_analyzer.py --help

# Check Python version
python --version  # Should be 3.8+

# Verify script location
ls -la scripts/*.py
```

## Tool Comparison

| Feature | Strategy Analyzer | Financial Scenario Analyzer |
|---------|------------------|---------------------------|
| **Primary Use** | Strategic positioning | Financial planning |
| **Frameworks** | SWOT, Porter's, BCG | NPV, IRR, Cash flow |
| **Time Horizon** | Long-term strategy | 3-5 year projections |
| **Input Type** | Qualitative + metrics | Quantitative financials |
| **Output** | Strategic recommendations | Financial scenarios |
| **Best For** | Annual planning, board strategy | Budgeting, fundraising |
| **Update Frequency** | Quarterly | Monthly/Quarterly |

## Advanced Usage

### Batch Processing

```bash
# Process multiple companies
for file in companies/*.json; do
    python scripts/strategy_analyzer.py "$file" -o json -f "results/$(basename $file)"
done
```

### Integration with Other Tools

```bash
# Pipe to other analysis tools
python scripts/strategy_analyzer.py data.json -o json | jq '.recommendations'

# Combine with OKR generation
python scripts/strategy_analyzer.py data.json -o json > strategy.json
python ../product-team/product-strategist/scripts/okr_cascade_generator.py strategy.json
```

### Custom Scripting

```python
import json
import subprocess

# Run analysis programmatically
result = subprocess.run(
    ['python', 'scripts/strategy_analyzer.py', 'data.json', '-o', 'json'],
    capture_output=True,
    text=True
)

analysis = json.loads(result.stdout)
# Process results...
```

## Data Privacy & Security

- All processing is local (no external API calls)
- No data transmitted to external services
- Input files may contain sensitive financial data
- Recommended: Encrypt storage, restrict file permissions
- Add to .gitignore if version controlling

```bash
# Secure file permissions
chmod 600 company_data.json
chmod 600 scenarios.json

# Add to .gitignore
echo "*_data.json" >> .gitignore
echo "*_scenarios.json" >> .gitignore
```
