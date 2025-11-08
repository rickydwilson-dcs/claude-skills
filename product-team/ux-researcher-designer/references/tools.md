# UX Research Tools Documentation

Complete documentation for UX research Python tools.

## persona_generator.py

Data-driven persona generation from user research.

### Overview

**Purpose:** Generate research-backed personas from user data, interviews, and behavioral analysis.

**Key Capabilities:**
- Demographic and psychographic profiling
- Goals and pain points extraction
- Behavior pattern identification
- Jobs-to-be-done analysis
- User journey mapping integration
- Confidence scoring based on sample size

### Usage

```bash
# Interactive persona creation
python3 scripts/persona_generator.py

# From JSON data file
python3 scripts/persona_generator.py --data user_research.json

# Filter by segment
python3 scripts/persona_generator.py --data user_data.json --segment "premium"

# JSON output
python3 scripts/persona_generator.py --data user_research.json --output json

# Save to file
python3 scripts/persona_generator.py --data user_research.json -o json -f personas.json

# Verbose mode
python3 scripts/persona_generator.py --data user_research.json -v
```

### Command-Line Options

```
usage: persona_generator.py [-h] [--data DATA] [--segment SEGMENT]
                            [--output {text,json,csv}] [--file FILE]
                            [--verbose] [--version]

Generate data-driven personas from user research

optional arguments:
  -h, --help            show help message
  --data DATA           User research data file (JSON format)
  --segment SEGMENT     Filter by user segment
  --output {text,json,csv}, -o {text,json,csv}
                        Output format (default: text)
  --file FILE, -f FILE  Write output to file
  --verbose, -v         Enable detailed output
  --version             show version
```

### Input Format

**User Research JSON:**
```json
{
  "users": [
    {
      "id": "user_001",
      "demographics": {
        "age": 32,
        "role": "Product Manager",
        "company_size": "50-200",
        "industry": "SaaS"
      },
      "behaviors": {
        "frequency": "daily",
        "primary_use_case": "project tracking",
        "tools_used": ["Jira", "Notion", "Slack"]
      },
      "goals": [
        "Track team progress",
        "Identify bottlenecks",
        "Report to stakeholders"
      ],
      "pain_points": [
        "Too many tools",
        "Data scattered",
        "Manual reporting"
      ],
      "quotes": [
        "I spend 2 hours a day just updating status"
      ]
    }
  ]
}
```

### Generated Persona Format

**Text Output:**
```
PERSONA: Sarah - The Organized Product Manager

DEMOGRAPHICS:
- Age: 32
- Role: Product Manager
- Company Size: 50-200 employees
- Industry: SaaS
- Technical Proficiency: High

GOALS:
1. Track team progress efficiently
2. Identify bottlenecks early
3. Report to stakeholders confidently

PAIN POINTS:
1. Too many disconnected tools
2. Data scattered across platforms
3. Manual reporting takes hours

BEHAVIORS:
- Uses product daily
- Primary use: Project tracking
- Current tools: Jira, Notion, Slack

JOBS-TO-BE-DONE:
When tracking project progress
Sarah wants to see all tasks in one view
So she can identify bottlenecks quickly

REPRESENTATIVE QUOTE:
"I spend 2 hours a day just updating status reports"

CONFIDENCE: High (based on 25 interviews)
```

**JSON Output:**
```json
{
  "persona": {
    "name": "Sarah",
    "archetype": "Organized Product Manager",
    "demographics": {...},
    "goals": [...],
    "pain_points": [...],
    "behaviors": {...},
    "jtbd": {...},
    "quote": "...",
    "confidence": "high",
    "sample_size": 25
  }
}
```

### Integration Patterns

**Figma Integration:**
```bash
# Generate personas
python3 scripts/persona_generator.py --data research.json -o json -f personas.json

# Import to Figma as design specs
# Use personas to inform design decisions
```

**Documentation:**
```bash
# Generate text output
python3 scripts/persona_generator.py --data research.json -v

# Copy to Confluence/Notion
# Share with product and design teams
```

**Research Synthesis:**
```bash
# Generate multiple personas by segment
python3 scripts/persona_generator.py --data research.json --segment "enterprise" -f enterprise_personas.json
python3 scripts/persona_generator.py --data research.json --segment "smb" -f smb_personas.json

# Compare segments
# Identify unique needs per segment
```

### Best Practices

**DO:**
- Base personas on real user data (minimum 5 interviews per persona)
- Include direct quotes from research
- Update personas quarterly with new data
- Focus on goals and behaviors, not demographics alone
- Use personas in design critiques and planning

**DON'T:**
- Create personas from assumptions
- Make personas too detailed (focus on what matters)
- Treat personas as fixed (update with learnings)
- Create too many personas (3-5 primary personas max)
- Skip validation with real users

---

**Last Updated:** 2025-11-08
**Tool Version:** 1.0.0
**Related Files:**
- [frameworks.md](frameworks.md) - Persona development framework and research methods
- [templates.md](templates.md) - Interview scripts and persona templates
