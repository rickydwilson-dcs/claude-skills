# Root Cause Analysis Methodologies

Comprehensive guide to RCA techniques for CAPA investigations.

## RCA Method Selection Framework

### 1. 5 Why Analysis
**Best for:** Straightforward process issues with linear causation

**Process:**
1. State the problem clearly
2. Ask "Why did this happen?" - Record answer
3. For each answer, ask "Why?" again
4. Continue for 5 iterations (or until root cause identified)
5. Verify root cause with evidence

**Example:**
```
Problem: Product failed final inspection
Why 1: Incorrect assembly procedure followed
Why 2: Work instruction was outdated
Why 3: Document control process missed update
Why 4: Change notification system failed
Why 5: No automated workflow for doc updates
Root Cause: Manual document control process prone to errors
```

**When to use:**
- Simple, linear problems
- Process-related issues
- Quick investigations needed
- Single failure mode

### 2. Fishbone Diagram (Ishikawa)
**Best for:** Complex multi-factor problems with multiple contributors

**Categories (6M Framework):**
- **Man/People:** Human factors, training, competency
- **Machine/Equipment:** Equipment malfunction, calibration, maintenance
- **Material:** Raw material quality, supplier issues, specifications
- **Method/Process:** Procedures, work instructions, process design
- **Measurement:** Testing, validation, verification methods
- **Management/Environment:** Management systems, work environment, organizational factors

**Process:**
1. Define problem statement (fish head)
2. Identify main cause categories (major bones)
3. Brainstorm contributing factors for each category (minor bones)
4. Analyze relationships and patterns
5. Verify most significant contributors

**When to use:**
- Complex problems with multiple factors
- Cross-functional issues
- Team-based investigations
- Pattern identification needed

### 3. Fault Tree Analysis (FTA)
**Best for:** Safety-critical system failures requiring systematic analysis

**Process:**
1. Define top-level undesired event
2. Identify immediate causes using logic gates:
   - **AND gate:** All inputs must occur
   - **OR gate:** Any input can cause event
3. Continue decomposition to basic events
4. Calculate probability if data available
5. Identify critical paths and single points of failure

**Logic Gates:**
```
TOP EVENT: Patient injury from device failure
         |
      [OR gate]
    /    |    \
   /     |     \
Software  Hardware  Human
Failure   Failure   Error
```

**When to use:**
- Safety-critical failures
- System-level analysis
- Multiple failure modes
- Probability analysis needed

### 4. Human Factors Analysis
**Best for:** Procedure or training-related issues with human performance factors

**Analysis Framework:**
```
Human Factors Hierarchy:
├── Organizational Factors
│   ├── Safety culture and management
│   ├── Resource allocation
│   └── Organizational processes
├── Supervision Factors
│   ├── Inadequate supervision
│   ├── Planned inappropriate operations
│   └── Failed to correct known problems
├── Preconditions
│   ├── Substandard conditions (fatigue, stress)
│   ├── Substandard practices (shortcuts, violations)
│   └── Personnel factors (training, experience)
└── Unsafe Acts
    ├── Errors (skill-based, decision, perceptual)
    └── Violations (routine, exceptional)
```

**Investigation Areas:**
- Work environment and ergonomics
- Training adequacy and competency verification
- Procedure clarity and usability
- Communication effectiveness
- Workload and time pressure
- Safety culture and reporting

**When to use:**
- Human error involved
- Training effectiveness questions
- Procedure design issues
- Repeated human performance problems

### 5. Failure Mode and Effects Analysis (FMEA)
**Best for:** Systematic risk assessment of potential failures

**FMEA Process:**
1. **Identify potential failure modes** for each process step/component
2. **Assess effects** of each failure mode
3. **Determine severity** (1-10 scale)
4. **Identify causes** of each failure mode
5. **Determine occurrence** probability (1-10 scale)
6. **Identify current controls** and detection methods
7. **Determine detection** rating (1-10 scale)
8. **Calculate Risk Priority Number (RPN):** Severity × Occurrence × Detection
9. **Prioritize actions** based on RPN
10. **Implement improvements** and recalculate RPN

**FMEA Table:**
| Process Step | Failure Mode | Effects | Severity | Causes | Occurrence | Current Controls | Detection | RPN | Actions |
|--------------|--------------|---------|----------|--------|------------|------------------|-----------|-----|---------|
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**When to use:**
- Systematic risk assessment
- Process improvement initiatives
- Design phase analysis
- Preventive action planning

## Investigation Protocol

### Phase 1: Problem Definition
**Objective:** Clear, specific problem statement with scope

**Activities:**
- Document initial trigger event
- Define problem boundaries and scope
- Assess immediate impact and severity
- Determine investigation urgency
- Select appropriate RCA methodology

**Output:** Problem statement, investigation plan, team assignment

### Phase 2: Data Collection
**Objective:** Gather factual evidence supporting investigation

**Evidence Types:**
- Physical evidence (failed parts, products)
- Documentary evidence (records, procedures, training)
- Testimonial evidence (interviews, observations)
- Digital evidence (logs, electronic records)

**Data Quality Criteria:**
- Objective and verifiable
- Complete and comprehensive
- Timely and relevant
- Properly documented and traceable

### Phase 3: Root Cause Identification
**Objective:** Identify true root causes, not just symptoms

**Analysis Levels:**
1. **Immediate Causes:** Direct causes of the problem
2. **Contributing Causes:** Factors that contributed or enabled
3. **Root Causes:** Underlying system factors enabling occurrence

**Verification:**
- Would fixing this cause prevent recurrence?
- Is this within organizational control?
- Is there evidence supporting this conclusion?
- Have alternative explanations been considered?

### Phase 4: Solution Development
**Objective:** Develop effective, sustainable corrective actions

**Solution Criteria:**
- Addresses identified root cause
- Prevents recurrence
- Feasible to implement
- Cost-effective
- Verifiable effectiveness

**Action Hierarchy:**
1. **Elimination:** Remove the hazard/problem source (most effective)
2. **Substitution:** Replace with less hazardous option
3. **Engineering Controls:** Physical changes to reduce risk
4. **Administrative Controls:** Procedures, training, work practices
5. **PPE/Detection:** Personal protective equipment or monitoring (least effective)

### Phase 5: Effectiveness Verification
**Objective:** Confirm actions achieved intended results

**Verification Methods:**
- Data analysis (metrics, trends)
- Process monitoring
- Audit findings
- Recurrence tracking

**Verification Timeline:**
- Short-term (1-3 months): Initial effectiveness
- Long-term (6-12 months): Sustained effectiveness
- Ongoing: Continuous monitoring

## RCA Documentation Requirements

### Investigation Report Contents

**1. Executive Summary**
- Problem statement and impact
- Root cause(s) identified
- Corrective actions planned
- Expected outcomes

**2. Background and Scope**
- Trigger event description
- Investigation scope and boundaries
- Investigation team composition
- Timeline and methodology

**3. Investigation Details**
- Data collection methods and sources
- Analysis performed (include diagrams)
- Evidence reviewed
- Interviews conducted

**4. Root Cause Analysis**
- Methodology used and rationale
- Immediate causes identified
- Contributing factors
- Root cause determination
- Verification of root cause

**5. Corrective and Preventive Actions**
- Immediate containment actions
- Corrective actions addressing root causes
- Preventive actions for similar issues
- Implementation timeline
- Responsible parties

**6. Effectiveness Verification Plan**
- Verification methods and metrics
- Verification timeline
- Success criteria
- Monitoring plan

**7. Appendices**
- Supporting data and evidence
- Interview summaries
- Analysis worksheets
- Risk assessment updates

## Common Investigation Pitfalls

**Stopping too early:**
- Identifying symptoms rather than root causes
- Accepting first plausible explanation
- Insufficient verification of conclusions

**Bias and assumptions:**
- Confirmation bias (seeking supporting evidence only)
- Jumping to conclusions without evidence
- Blaming individuals rather than systems

**Incomplete investigation:**
- Missing key evidence or data
- Inadequate stakeholder involvement
- Rushing to closure under time pressure

**Weak corrective actions:**
- Addressing symptoms not causes
- Relying solely on administrative controls
- Failing to prevent similar issues elsewhere

**Poor documentation:**
- Incomplete investigation records
- Missing evidence chain
- Inadequate action tracking
- No effectiveness verification

## RCA Best Practices

1. **Form diverse investigation teams** - Multiple perspectives improve analysis
2. **Focus on systems, not individuals** - Human error often reflects system design
3. **Use multiple RCA methods** - Different techniques reveal different insights
4. **Verify root causes rigorously** - Test conclusions against evidence
5. **Develop sustainable solutions** - Prefer permanent fixes over workarounds
6. **Document thoroughly** - Clear records support learning and compliance
7. **Follow up diligently** - Verify effectiveness and sustained improvement
8. **Share lessons learned** - Prevent similar issues organization-wide

## RCA Method Selection Decision Tree

```
START: New CAPA Investigation
    |
    ├─ Is it a simple, linear problem?
    │   └─ YES → Use 5 Why Analysis
    │
    ├─ Is it a complex, multi-factor problem?
    │   └─ YES → Use Fishbone Diagram
    │
    ├─ Is it safety-critical with system failures?
    │   └─ YES → Use Fault Tree Analysis
    │
    ├─ Does it involve human performance/training?
    │   └─ YES → Use Human Factors Analysis
    │
    └─ Does it require systematic risk assessment?
        └─ YES → Use FMEA
```

## Additional Resources

- **Investigation Templates:** See `../assets/capa-templates/`
- **RCA Worksheets:** See `../assets/rca-tools/`
- **Training Materials:** See `../assets/training-materials/`
- **Python Tools:** See `../scripts/rca-analysis-tool.py`
