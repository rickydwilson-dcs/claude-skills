# Contract: Workflow Completeness

**Date**: November 12, 2025
**Purpose**: Define validation rules for agent workflow documentation

## Contract Overview

Every agent MUST document exactly 4 workflows with 5 required fields each (Goal, Steps, Expected Output, Time Estimate, Example).

## Workflow Count Requirement

**Mandatory:** Exactly 4 workflows per agent

**Why 4:** Based on analysis of 8 existing production agents - 100% have exactly 4 workflows.

## Workflow Types (Recommended Pattern)

1. **Workflow 1: Primary Use Case**
   - Most common scenario
   - Single tool focus
   - Entry point for new users

2. **Workflow 2: Advanced Use Case**
   - Complex scenario
   - Multiple tool integration
   - For experienced users

3. **Workflow 3: Integration Use Case**
   - Cross-functional workflow
   - Tool orchestration
   - Combines multiple capabilities

4. **Workflow 4: Automation Use Case**
   - Scriptable workflow
   - Batch processing
   - Ongoing automation

## Required Workflow Structure

### Complete Workflow Template

```markdown
### Workflow [1-4]: [Clear Descriptive Name]

**Goal:** One-sentence description of what this workflow accomplishes

**Steps:**
1. **[Action Verb + Object]** - Clear description
   ```bash
   # Optional command example
   python ../../skills/domain-team/skill-name/scripts/tool.py input
   ```
2. **[Action Verb + Object]** - Clear description
3. **[Action Verb + Object]** - Clear description
4. **[Action Verb + Object]** - Clear description
5. **[Action Verb + Object]** - Clear description

**Expected Output:** Concrete deliverable or measurable result

**Time Estimate:** Realistic duration (e.g., "2-3 hours", "30-45 minutes")

**Example:**
```bash
# Complete workflow example with real commands
cd /path/to/project
python ../../skills/domain-team/skill-name/scripts/tool.py input.txt
# Review output
```
```

## Field Specifications

### 1. Goal Field (REQUIRED)

**Format:** One-sentence outcome description

**Rules:**
- MUST be a single sentence
- SHOULD focus on outcome, not process
- SHOULD use active voice
- MUST be specific and measurable

**Valid Examples:**
```markdown
**Goal:** Create SEO-optimized blog post with consistent brand voice

**Goal:** Generate production-ready REST API with authentication and database integration

**Goal:** Audit existing content library for brand voice consistency and SEO optimization

**Goal:** Set up automated weekly security scanning workflow
```

**Invalid Examples:**
```markdown
**Goal:** Help with content                                    # ❌ Too vague
**Goal:** Use tools to create content and optimize SEO        # ❌ Process-focused, not outcome-focused
**Goal:** This workflow will help you create blog posts...    # ❌ Not a concise statement
```

### 2. Steps Field (REQUIRED)

**Format:** 4-7 numbered steps with action verb + description

**Rules:**
- MUST have 4-7 steps (average 6 based on existing agents)
- EACH step MUST start with action verb (bold)
- EACH step SHOULD have clear description
- Steps MAY include optional code examples
- Steps MUST be sequential

**Step Format:**
```markdown
**Steps:**
1. **[Action Verb + Object]** - Description
   ```bash
   # Optional command
   ```
2. **[Action Verb + Object]** - Description
```

**Action Verbs (Examples):**
- Create, Generate, Build, Initialize
- Analyze, Review, Validate, Check
- Configure, Set up, Install, Deploy
- Run, Execute, Process, Transform
- Update, Modify, Refactor, Optimize

**Valid Example:**
```markdown
**Steps:**
1. **Draft Content** - Write initial blog post draft in markdown format
2. **Analyze Brand Voice** - Run brand voice analyzer to check tone and readability
   ```bash
   python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py draft-post.md
   ```
3. **Review Feedback** - Adjust content based on formality score, tone, and readability metrics
4. **Optimize for SEO** - Run SEO optimizer with target keywords
   ```bash
   python ../../skills/marketing-team/content-creator/scripts/seo_optimizer.py draft-post.md "target keyword"
   ```
5. **Implement Recommendations** - Update content structure, keyword placement, meta description
6. **Final Validation** - Re-run both analyzers to verify improvements
```

**Invalid Examples:**
```markdown
**Steps:**
1. Run tool                                    # ❌ Not bold, too vague
2. **review output**                           # ❌ Not capitalized
3. **The user should analyze the results**     # ❌ Not imperative form
```

### 3. Expected Output Field (REQUIRED)

**Format:** Concrete deliverable or measurable result

**Rules:**
- MUST describe specific deliverable OR measurable outcome
- SHOULD include success criteria where applicable
- SHOULD be verifiable
- MAY include metrics or quality thresholds

**Valid Examples:**
```markdown
**Expected Output:** SEO score 80+ with consistent brand voice alignment

**Expected Output:** Fully scaffolded API with 5+ endpoints, authentication, and test suite

**Expected Output:** Comprehensive audit report with prioritized improvement list for 20+ content pieces

**Expected Output:** Automated workflow running daily, generating reports in Slack channel
```

**Invalid Examples:**
```markdown
**Expected Output:** Success                           # ❌ Too vague
**Expected Output:** The tool will finish running      # ❌ Not outcome-focused
**Expected Output:** Various improvements              # ❌ Not specific
```

### 4. Time Estimate Field (REQUIRED)

**Format:** Realistic duration range

**Rules:**
- MUST include time estimate
- SHOULD use range format (e.g., "2-3 hours")
- SHOULD be realistic based on workflow complexity
- MAY differentiate setup vs ongoing time

**Valid Examples:**
```markdown
**Time Estimate:** 2-3 hours for 1,500-word blog post

**Time Estimate:** 45-60 minutes for initial setup

**Time Estimate:** 30-45 minutes

**Time Estimate:** 4-6 hours for full security audit

**Time Estimate:** 15-20 minutes per iteration
```

**Invalid Examples:**
```markdown
**Time Estimate:** Fast                    # ❌ Not specific
**Time Estimate:** Depends                 # ❌ Not helpful
**Time Estimate:** 2.5 hours              # ❌ Use range (2-3 hours better)
```

### 5. Example Field (REQUIRED)

**Format:** Bash code block with complete workflow commands

**Rules:**
- MUST be a code block (triple backticks with `bash`)
- MUST include actual commands
- SHOULD include comments for clarity
- SHOULD be copy-paste ready
- MUST use relative paths (`../../skills/`)

**Valid Example:**
```markdown
**Example:**
```bash
# Complete workflow for blog post optimization
cd /path/to/content

# Step 1: Analyze brand voice
python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py draft-post.md

# Step 2: Optimize for SEO
python ../../skills/marketing-team/content-creator/scripts/seo_optimizer.py draft-post.md "target keyword" "secondary,keywords"

# Step 3: Review results
cat draft-post.md
```
```

**Invalid Examples:**
```markdown
**Example:**
See above steps                          # ❌ Not a code example

**Example:**
Run the tools                            # ❌ Not specific

**Example:**
```
python tool.py input.txt                  # ❌ Not a complete bash block, wrong path
```
```

## Workflow Validation Checklist

Use this checklist for EACH of the 4 workflows:

**Structure:**
- [ ] Workflow has clear descriptive name
- [ ] All 5 fields present (Goal, Steps, Output, Time, Example)
- [ ] Fields appear in correct order

**Goal:**
- [ ] Goal is a single sentence
- [ ] Goal is outcome-focused
- [ ] Goal is specific and measurable

**Steps:**
- [ ] 4-7 steps documented
- [ ] Each step starts with bold action verb
- [ ] Each step has clear description
- [ ] Steps are sequential
- [ ] Optional code examples use `../../skills/` paths

**Expected Output:**
- [ ] Output is concrete/specific
- [ ] Output is measurable or verifiable
- [ ] Success criteria included (if applicable)

**Time Estimate:**
- [ ] Time estimate provided
- [ ] Estimate is realistic
- [ ] Estimate uses range format

**Example:**
- [ ] Example is bash code block
- [ ] Example includes real commands
- [ ] Example uses relative paths
- [ ] Example is copy-paste ready
- [ ] Comments provide context

## Complete Workflow Example (Valid)

```markdown
### Workflow 1: Blog Post Creation & Optimization

**Goal:** Create SEO-optimized blog post with consistent brand voice

**Steps:**
1. **Draft Content** - Write initial blog post draft in markdown format
2. **Analyze Brand Voice** - Run brand voice analyzer to check tone and readability
   ```bash
   python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py draft-post.md
   ```
3. **Review Feedback** - Adjust content based on formality score, tone, and readability metrics
4. **Optimize for SEO** - Run SEO optimizer with target keywords
   ```bash
   python ../../skills/marketing-team/content-creator/scripts/seo_optimizer.py draft-post.md "target keyword" "secondary,keywords,here"
   ```
5. **Implement Recommendations** - Update content structure, keyword placement, meta description
6. **Final Validation** - Re-run both analyzers to verify improvements

**Expected Output:** SEO score 80+ with consistent brand voice alignment

**Time Estimate:** 2-3 hours for 1,500-word blog post

**Example:**
```bash
# Complete workflow
echo "# Blog Post Draft" > post.md
python ../../skills/marketing-team/content-creator/scripts/brand_voice_analyzer.py post.md
python ../../skills/marketing-team/content-creator/scripts/seo_optimizer.py post.md "content marketing" "SEO,strategy"
```
```

## Workflow Count Validation

### Exact Count Requirement

```bash
# Count workflows in agent file
grep -c "^### Workflow [0-9]:" agents/domain/cs-agent.md

# Expected output: 4
```

**If count ≠ 4:**
- Count < 4: Add more workflows
- Count > 4: Consolidate or remove workflows

**Why exactly 4:** All 8 existing production agents have exactly 4 workflows - this is the validated pattern.

## Common Workflow Violations

### Violation 1: Missing Fields

```markdown
<!-- ❌ WRONG - missing Time Estimate and Example -->
### Workflow 1: Blog Post Creation

**Goal:** Create blog post

**Steps:**
1. Draft content
2. Optimize content

**Expected Output:** Blog post
```

**Fix:** Add all 5 required fields

### Violation 2: Too Few Steps

```markdown
<!-- ❌ WRONG - only 2 steps (need 4-7) -->
**Steps:**
1. **Run Tool** - Execute the tool
2. **Review Output** - Look at results
```

**Fix:** Break down into 4-7 steps with more detail

### Violation 3: Vague Steps

```markdown
<!-- ❌ WRONG - steps too vague -->
**Steps:**
1. **Do Setup** - Set things up
2. **Run Stuff** - Run the tools
3. **Check** - Check if it worked
```

**Fix:** Use specific action verbs and clear descriptions

### Violation 4: No Code Example

```markdown
<!-- ❌ WRONG - example is not a code block -->
**Example:**
Use the tools mentioned above
```

**Fix:** Provide bash code block with real commands

### Violation 5: Absolute Paths in Example

```markdown
<!-- ❌ WRONG - absolute path -->
**Example:**
```bash
python /Users/name/claude-skills/skills/marketing-team/content-creator/scripts/tool.py
```
```

**Fix:** Use relative paths

## Workflow Quality Standards

### Minimum Quality Requirements

Each workflow MUST meet these standards:

1. **Clarity:** Steps are clear enough for user to execute without additional guidance
2. **Completeness:** All 5 fields present and properly formatted
3. **Specificity:** No vague language ("do stuff", "run things")
4. **Testability:** Example can be copied and executed
5. **Realism:** Time estimate reflects actual duration

### Workflow Length Standards

Based on existing agent analysis:

- **Minimum steps:** 4
- **Maximum steps:** 7
- **Average steps:** 6
- **Sweet spot:** 5-6 steps per workflow

### Workflow Complexity Distribution

Recommended complexity across 4 workflows:

1. **Workflow 1 (Simple):** 4-5 steps, single tool, 30-60 minutes
2. **Workflow 2 (Moderate):** 5-6 steps, 2 tools, 1-2 hours
3. **Workflow 3 (Complex):** 6-7 steps, multiple tools, 2-4 hours
4. **Workflow 4 (Automated):** 3-5 steps, scripted, setup time + ongoing

## Automated Workflow Validation Script

```python
#!/usr/bin/env python3
"""
Validate agent workflow completeness
"""
import re
import sys
from pathlib import Path

def validate_workflows(agent_file):
    """Validate workflow documentation"""
    content = Path(agent_file).read_text()

    # Find workflow sections
    workflows = re.findall(r'### Workflow \d+:.*?(?=### Workflow \d+:|## Integration Examples|$)', content, re.DOTALL)

    if len(workflows) != 4:
        return False, f"Expected 4 workflows, found {len(workflows)}"

    errors = []
    for i, workflow in enumerate(workflows, 1):
        # Check required fields
        if '**Goal:**' not in workflow:
            errors.append(f"Workflow {i}: Missing Goal field")
        if '**Steps:**' not in workflow:
            errors.append(f"Workflow {i}: Missing Steps field")
        if '**Expected Output:**' not in workflow:
            errors.append(f"Workflow {i}: Missing Expected Output field")
        if '**Time Estimate:**' not in workflow:
            errors.append(f"Workflow {i}: Missing Time Estimate field")
        if '**Example:**' not in workflow:
            errors.append(f"Workflow {i}: Missing Example field")

        # Count steps
        steps = re.findall(r'^\d+\. \*\*', workflow, re.MULTILINE)
        if len(steps) < 4 or len(steps) > 7:
            errors.append(f"Workflow {i}: Has {len(steps)} steps (need 4-7)")

        # Check for code example
        if '```bash' not in workflow and '```' not in workflow:
            errors.append(f"Workflow {i}: Missing bash code example")

    if errors:
        return False, "\n".join(errors)

    return True, "All workflows valid"

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: validate_workflows.py <agent-file.md>")
        sys.exit(1)

    valid, message = validate_workflows(sys.argv[1])
    print(f"{'✅' if valid else '❌'} {message}")
    sys.exit(0 if valid else 1)
```

**Usage:**
```bash
python validate_workflows.py agents/engineering/cs-backend-engineer.md
```

---

**Last Updated:** November 12, 2025
**Contract Status:** Mandatory for all agents
**Validation:** Must have exactly 4 complete workflows before marking production-ready
