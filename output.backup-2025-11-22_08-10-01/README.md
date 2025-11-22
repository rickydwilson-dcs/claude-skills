# Agent Output Directory

This directory stores all agent-generated reports, analyses, and outputs from the claude-skills repository.

## Directory Structure

```
output/
├── architecture/       # Architecture reviews, diagrams, design docs
├── reviews/           # Code reviews, PR reviews, quality assessments
├── analysis/          # Dependency analysis, performance analysis, security scans
├── reports/           # General reports, summaries, audits
└── README.md          # This file
```

## File Naming Convention

All agent outputs follow this naming pattern:

```
YYYY-MM-DD_HH-MM-SS_<topic>_<agent-name>.md
```

**Examples:**
- `2025-11-13_08-30-45_architecture-review_cs-architect.md`
- `2025-11-13_14-22-10_code-review_cs-code-reviewer.md`
- `2025-11-13_16-45-30_dependency-analysis_cs-architect.md`
- `2025-11-13_09-15-00_security-scan_cs-secops.md`

## Naming Components

### Date/Timestamp
- **Format:** `YYYY-MM-DD_HH-MM-SS`
- **Purpose:** Chronological sorting and version tracking
- **Example:** `2025-11-13_08-30-45`

### Topic
- **Format:** Kebab-case (lowercase with hyphens)
- **Purpose:** Describes the content/type of analysis
- **Examples:**
  - `architecture-review`
  - `code-review`
  - `dependency-analysis`
  - `security-scan`
  - `performance-audit`
  - `technical-debt-assessment`

### Agent Name
- **Format:** cs-agent-name (must match agent file in `agents/`)
- **Purpose:** Identifies which agent generated the output
- **Examples:**
  - `cs-architect`
  - `cs-code-reviewer`
  - `cs-secops`
  - `cs-backend`
  - `cs-devops`

## Usage

### Creating Agent Outputs

When agents generate reports, save them using this pattern:

```bash
# Get current timestamp
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Save architecture review
echo "Architecture analysis..." > output/architecture/${TIMESTAMP}_architecture-review_cs-architect.md

# Save code review
echo "Code review results..." > output/reviews/${TIMESTAMP}_code-review_cs-code-reviewer.md

# Save security scan
echo "Security scan results..." > output/analysis/${TIMESTAMP}_security-scan_cs-secops.md
```

### Agent Output Templates

Each agent output should include:

1. **Header Section**
   - Title
   - Agent name
   - Timestamp
   - Repository/target path
   - Executive summary

2. **Analysis Section**
   - Detailed findings
   - Metrics and data
   - Visualizations (diagrams, tables)

3. **Recommendations Section**
   - Actionable items
   - Prioritization
   - Implementation guidance

4. **Conclusion Section**
   - Overall assessment
   - Next steps
   - References

## Git Workflow

**Default Behavior:** All files in `output/` are gitignored by default.

**Rationale:** Agent outputs are typically ephemeral working files. Users can review them locally without cluttering git history.

**Committing Important Reports:**

If you want to commit a specific report to version control:

```bash
# Force-add specific report
git add -f output/architecture/2025-11-13_08-30-45_architecture-review_cs-architect.md

# Commit with descriptive message
git commit -m "docs(architecture): add architecture review from cs-architect"
```

## Directory Categories

### architecture/
- System architecture reviews
- Architecture diagrams and visualizations
- Design decision records (ADRs)
- Technology stack evaluations
- Scalability assessments

### reviews/
- Code review reports
- Pull request reviews
- Quality assessments
- Best practice compliance checks

### analysis/
- Dependency analysis
- Performance analysis
- Security vulnerability scans
- Technical debt assessments
- Complexity metrics

### reports/
- General reports and summaries
- Audit reports
- Status reports
- Comparative analyses
- Benchmark results

## Integration with Agents

### Architecture Agent (cs-architect)
```bash
python3 skills/engineering-team/senior-architect/scripts/project_architect.py --input . > output/architecture/$(date +"%Y-%m-%d_%H-%M-%S")_architecture-review_cs-architect.md
```

### Code Reviewer Agent (cs-code-reviewer)
```bash
python3 skills/engineering-team/code-reviewer/scripts/code_quality_checker.py ./src > output/reviews/$(date +"%Y-%m-%d_%H-%M-%S")_code-review_cs-code-reviewer.md
```

### Security Agent (cs-secops)
```bash
python3 skills/engineering-team/senior-secops/scripts/security_scanner.py --input . > output/analysis/$(date +"%Y-%m-%d_%H-%M-%S")_security-scan_cs-secops.md
```

## Maintenance

### Cleanup Old Reports

```bash
# Remove reports older than 30 days
find output/ -name "*.md" -mtime +30 -delete

# Remove all reports except README
find output/ -name "*.md" ! -name "README.md" -delete
```

### Archiving

For long-term storage of important reports:

```bash
# Create archive directory
mkdir -p archives/2025-Q4/

# Move important reports
mv output/architecture/2025-11-13_*_architecture-review_*.md archives/2025-Q4/
```

## Best Practices

1. **Timestamp Precision** - Always use full timestamp (date + time) for unique filenames
2. **Descriptive Topics** - Use clear, searchable topic names
3. **Agent Attribution** - Always include agent name for traceability
4. **Consistent Format** - Follow markdown formatting for all reports
5. **Executive Summaries** - Always include a summary at the top
6. **Actionable Recommendations** - Provide clear next steps
7. **Version Context** - Include git commit hash or branch name in reports

## Examples

### Good Filenames ✅
- `2025-11-13_08-30-45_architecture-review_cs-architect.md`
- `2025-11-13_14-22-10_dependency-analysis_cs-architect.md`
- `2025-11-13_16-45-30_security-vulnerability-scan_cs-secops.md`
- `2025-11-13_09-15-00_code-quality-assessment_cs-code-reviewer.md`

### Bad Filenames ❌
- `architecture-review.md` (no timestamp, no agent)
- `review_11-13.md` (ambiguous, no agent, incomplete date)
- `cs-architect-output.md` (no topic, no timestamp)
- `2025-11-13-report.md` (no time, vague topic, no agent)

---

**Last Updated:** 2025-11-13
**Version:** 1.0.0
**Status:** ✅ Ready to use

**Keep your agent outputs organized and discoverable!** 🚀
