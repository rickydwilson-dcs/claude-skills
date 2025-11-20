# Sample Data Files

This directory contains sample data files for testing and demonstrating the Claude Skills Library tools.

## Files

### sample-features.csv

**Purpose:** Sample feature backlog for testing the RICE prioritization framework.

**Use Case:** Product management feature prioritization using the product-manager-toolkit skill.

**Usage:**
```bash
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  docs/examples/sample-features.csv --capacity 20
```

**Contents:** 14 sample features for the Claude Skills repository including:
- Agent Discovery System
- Skills Documentation Portal
- Python Tool Testing Framework
- Agent Performance Analytics
- Multi-Model Agent Support
- And more...

Each feature includes:
- **Reach:** Number of users affected per quarter
- **Impact:** Scale from 0.5 (minimal) to 3 (massive)
- **Confidence:** Scale from 0.4 (low) to 1.0 (high)
- **Effort:** Person-months required (1-15 months)

**Expected Output:** RICE scores, portfolio analysis (Quick Wins, Big Bets, Fill-Ins, Money Pits), and quarterly roadmap recommendations.

---

### sample-interview.txt

**Purpose:** Sample customer interview transcript for testing interview analysis tools.

**Use Case:** Customer discovery and user research synthesis using the product-manager-toolkit skill.

**Usage:**
```bash
python3 skills/product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py \
  docs/examples/sample-interview.txt
```

**Contents:** Realistic customer interview with an Engineering Team Lead discussing their experience with the Claude Skills repository, including:
- Pain points around agent discovery and documentation
- Feature requests for testing frameworks and workflow automation
- Feedback on tool reliability and cross-skill integration
- Positive feedback on core value proposition

**Expected Output:**
- Pain points extracted with severity ratings
- Feature requests identified from transcript
- Jobs-to-be-done patterns
- Sentiment analysis
- Theme extraction

---

## Context

Both sample files are based on the Claude Skills repository itself, making them realistic examples that demonstrate how these tools can be used for actual product management work on this codebase.

### Sample Features Context

The features in `sample-features.csv` represent potential improvements to the Claude Skills repository:
- **High-reach features:** Skills Marketplace Integration (1000 users), Skills Documentation Portal (800 users)
- **High-impact features:** Multi-Model Agent Support (3.0), Real-time Agent Collaboration (3.0)
- **Quick wins:** Documentation Auto-Sync (0.9 confidence, 1 month effort)
- **Big bets:** Real-time Agent Collaboration (3.0 impact, 12 months effort)

### Sample Interview Context

The interview in `sample-interview.txt` captures common user pain points:
1. **Discovery Challenge:** Overwhelming number of agents without clear guidance
2. **Testing Gap:** Lack of visibility into tool reliability and performance
3. **Documentation Drift:** Outdated references causing confusion
4. **Integration Friction:** Difficulty chaining multiple skills together
5. **UX Opportunities:** Need for workflow automation and monitoring

---

## Creating Your Own Sample Data

### For RICE Prioritization

Create a CSV file with this structure:
```csv
feature,reach,impact,confidence,effort
Your Feature Name,500,2,0.8,3
```

**Guidelines:**
- **Reach:** Estimate users affected per quarter (50-10,000+)
- **Impact:** Use scale: 3 (massive), 2 (high), 1.5 (medium), 1 (low), 0.5 (minimal)
- **Confidence:** Use scale: 1.0 (high), 0.8 (medium), 0.5 (low)
- **Effort:** Person-months (0.25 for XS, 0.5 for S, 1 for M, 3 for L, 6+ for XL)

### For Interview Analysis

Create a text file with:
- Natural conversation format
- Clear pain points and feature requests embedded in user feedback
- Contextual information (role, date, project)
- Both positive and negative feedback

**Example structure:**
```
Customer Interview Transcript
Interviewer: [Your Name]
Interviewee: [Customer Name] ([Role])
Date: YYYY-MM-DD
Project: [Project Name]

[Natural conversation with pain points, feature requests, and feedback...]
```

---

## Testing the Tools

After installation, verify the tools work with these samples:

```bash
# Test RICE prioritizer
python3 skills/product-team/product-manager-toolkit/scripts/rice_prioritizer.py \
  docs/examples/sample-features.csv --capacity 20

# Test interview analyzer
python3 skills/product-team/product-manager-toolkit/scripts/customer_interview_analyzer.py \
  docs/examples/sample-interview.txt
```

Both tools should produce detailed analysis output. See [INSTALL.md](../INSTALL.md) for complete installation and testing instructions.

---

**Last Updated:** November 20, 2025
**Maintained By:** Claude Skills Library Team
