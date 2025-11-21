# Business Analysis Tools Reference

## Table of Contents

1. [Lucidchart Integration Guide](#lucidchart-integration-guide)
2. [Miro Collaboration Patterns](#miro-collaboration-patterns)
3. [Confluence Publishing](#confluence-publishing)
4. [Jira Workflow Mapping](#jira-workflow-mapping)
5. [Tool Integration Patterns](#tool-integration-patterns)

---

## Lucidchart Integration Guide

### Overview

Lucidchart is a web-based diagramming tool optimized for creating professional process diagrams, flowcharts, BPMN models, and organizational charts. It's particularly valuable for business analysts due to its collaboration features, template library, and integration capabilities.

### Getting Started with Lucidchart

#### Account Setup

**Individual Account:**
1. Sign up at https://www.lucidchart.com
2. Choose appropriate plan:
   - Free: Basic diagrams, limited shapes (60 objects)
   - Individual: Unlimited diagrams and shapes ($7.95/month)
   - Team: Collaboration features ($9/user/month)
   - Enterprise: Advanced integrations and management

**Team Best Practices:**
- Use organization email for account
- Join company team workspace
- Set up folders by project/department
- Enable team shape libraries
- Configure default templates

#### Interface Navigation

**Canvas:**
- Infinite canvas for large diagrams
- Grid and snap-to-grid (toggle with View > Grid)
- Zoom: Ctrl + scroll or zoom controls
- Pan: Space + drag or trackpad

**Shape Libraries:**
- Standard shapes (left panel)
- BPMN 2.0
- Flowchart
- UML
- AWS, Azure, GCP architectures
- Custom shape libraries (create your own)

**Quick Actions:**
- Duplicate: Ctrl/Cmd + D
- Group: Ctrl/Cmd + G
- Align: Use alignment tools (top toolbar)
- Distribute: Spacing tools
- Send to back/front: Right-click > Order

### Creating Process Diagrams

#### Starting a New Diagram

**Method 1: From Template**
1. Click "New Document"
2. Select "Templates" tab
3. Search for:
   - "Process Flow"
   - "BPMN"
   - "Swimlane"
   - "Value Stream Map"
4. Click template > "Use Template"
5. Customize with your process details

**Method 2: Blank Canvas**
1. Click "New Document" > "Blank"
2. Add shape library: Bottom left > "More Shapes"
3. Enable relevant libraries:
   - Standard Flowchart
   - BPMN 2.0
   - Swimlanes
   - AWS/Cloud (if needed)
4. Start diagramming

#### BPMN Diagrams in Lucidchart

**Setting Up:**
1. Enable "BPMN 2.0" shape library
2. Drag pool to canvas (represents organization)
3. Add lanes inside pool (represents roles)
4. Build process flow with BPMN shapes

**BPMN Shape Guide:**

Start Events:
- Drag "Start Event" (thin circle)
- Label appropriately
- Connect to first activity

Activities:
- Drag "Task" (rounded rectangle)
- Name with Verb + Object format
- Types available:
  - User Task (person icon)
  - Service Task (gear icon)
  - Script Task (scroll icon)

Gateways:
- Exclusive Gateway (X) - one path chosen
- Parallel Gateway (+) - all paths taken
- Inclusive Gateway (O) - one or more paths

Events:
- Intermediate events (double circle)
- End events (thick circle)
- Boundary events (attach to activities)

**Best Practices:**
- Use containers for sub-processes
- Add data objects for inputs/outputs
- Sequence flows: solid arrows
- Message flows: dashed arrows across pools
- Keep diagram readable (max 15-20 shapes per level)

#### Swimlane Diagrams

**Creating Swimlanes:**
1. Method A: Use template "Cross-Functional Flowchart"
2. Method B: Draw manually
   - Insert > Shape Library > "Swimlanes"
   - Drag horizontal/vertical swimlane container
   - Adjust number of lanes

**Customizing:**
- Resize lanes: Drag lane divider
- Add lanes: Right-click divider > "Insert Lane Before/After"
- Delete lanes: Right-click > "Delete Lane"
- Change orientation: Right-click > "Change Orientation"
- Style lanes: Different colors per lane for clarity

**Adding Content:**
1. Place shapes within appropriate lanes
2. Draw connectors crossing lanes (handoffs)
3. Label connectors with what's transferred
4. Use colors to highlight value-add vs waste

**Example Structure:**
```
Lane: Customer
- [Submit Request] → [Receive Response]

Lane: Sales Team
- [Review Request] → [Create Quote] → [Send Quote]

Lane: Operations
- [Process Order] → [Fulfill Order]

Lane: Systems
- [Update CRM] → [Generate Invoice]
```

#### Value Stream Maps

**VSM Symbols in Lucidchart:**

Process Boxes:
- Use rectangles with data box below
- Include metrics:
  - C/T (Cycle Time)
  - C/O (Changeover Time)
  - Uptime %
  - # of people

Inventory Triangles:
- Use triangle shape
- Label with wait time/WIP count

Information Flow:
- Dashed lines for electronic
- Paper symbol + arrow for manual

Timeline:
- Draw at bottom
- Value-add time: Solid boxes
- Wait time: Dashed lines

**Creating VSM Step-by-Step:**
1. Enable custom shape library or use standard shapes
2. Start with customer (right side)
3. Work backwards through process
4. Add each process box with metrics
5. Add inventory/wait time between processes
6. Map information flow (top)
7. Create timeline at bottom
8. Calculate:
   - Total lead time
   - Total value-add time
   - Process cycle efficiency

### Styling and Formatting

#### Visual Consistency

**Color Coding:**
- Define color scheme:
  - Green: Value-adding activities
  - Yellow: Non-value but necessary
  - Red: Waste/problems
  - Blue: Automated processes
  - Gray: External/out of scope

**Shape Styling:**
1. Select shape
2. Right panel > Style
3. Set:
   - Fill color
   - Line color and weight
   - Font and size
   - Rounded corners

**Create Style Guide:**
1. Style one shape perfectly
2. Right-click > "Set Default Style"
3. OR create shape library with pre-styled shapes

#### Text and Labeling

**Shape Labels:**
- Double-click shape to edit
- Use clear, concise names
- Activities: Verb + Object ("Review Application")
- Events: Object + State ("Order Received")
- Gateways: Questions ("Approved?")

**Additional Text:**
- Text Box: Insert > Text
- Use for:
  - Annotations
  - Legends
  - Notes
  - Metrics

**Formatting Text:**
- Font size hierarchy:
  - Title: 18-24pt
  - Section headers: 14-16pt
  - Shape labels: 10-12pt
  - Notes: 8-10pt
- Consistent font family (Helvetica or Arial)
- Bold for emphasis, not underline

#### Layout and Alignment

**Automatic Layout:**
1. Select shapes to align
2. Top toolbar > Align
3. Options:
   - Align left/center/right
   - Align top/middle/bottom
   - Distribute horizontally/vertically

**Manual Spacing:**
- Use grid (View > Grid)
- Set grid size (typically 10-20px)
- Enable snap-to-grid
- Consistent spacing between shapes

**Reading Order:**
- Primary flow: Left to right
- Alternative paths: Top to bottom
- Minimize line crossings
- Use straight lines where possible

### Collaboration Features

#### Sharing Diagrams

**Share Methods:**

1. **Direct Share:**
   - Click "Share" button (top right)
   - Enter email addresses
   - Set permissions:
     - Can edit (full access)
     - Can comment (add comments only)
     - Can view (read-only)
   - Add message
   - Send invitation

2. **Link Sharing:**
   - Share button > "Get shareable link"
   - Choose access level
   - Copy link
   - Share via email/Slack/Teams

3. **Embed:**
   - Share > "Embed"
   - Copy embed code
   - Paste into Confluence, website, or other tool

**Permission Levels:**
- Admin: Full control including sharing
- Editor: Edit and comment
- Commenter: Add comments only
- Viewer: View only

#### Real-Time Collaboration

**Working Together:**
- Multiple users can edit simultaneously
- See collaborators' cursors in real-time
- Changes save automatically
- Presence indicators show who's viewing

**Best Practices:**
- Assign sections to team members
- Use comments for questions (don't edit directly)
- Lock completed sections (right-click > Lock)
- Schedule working sessions for complex diagrams

#### Comments and Feedback

**Adding Comments:**
1. Select shape or area
2. Right-click > "Add Comment"
3. Type comment
4. Tag team members with @mention
5. Click "Post"

**Comment Types:**
- Questions: "Is this step necessary?"
- Suggestions: "Consider combining these steps"
- Approvals: "Looks good, approved"
- Issues: "This doesn't reflect current process"

**Managing Comments:**
- View all: Comments panel (right side)
- Filter: By user, status, date
- Resolve: Check "Resolve" when addressed
- Reply: Thread conversations

**Review Workflow:**
1. Creator shares diagram
2. Reviewers add comments
3. Creator addresses comments
4. Reviewers mark resolved
5. Final approval comment
6. Archive or publish

#### Version Control

**Revision History:**
- File > Revision History
- View all saved versions
- See who made changes and when
- Restore previous version if needed

**Best Practices:**
- Save manually at major milestones
- Name versions descriptively
- Before big changes, duplicate document
- Use naming: "Process_Name_v1.0_YYYY-MM-DD"

### Advanced Features

#### Data Linking

**Link Data to Shapes:**
1. Select shape
2. Right panel > "Data"
3. Click "Link Data"
4. Import from:
   - Google Sheets
   - Excel
   - CSV
5. Map columns to shape properties

**Use Cases:**
- Org charts: Link to employee data
- Process maps: Link to performance metrics
- Network diagrams: Link to asset inventory

**Dynamic Updates:**
- Change source data
- Refresh in Lucidchart
- Diagram updates automatically

#### Conditional Formatting

**Apply Rules:**
1. Select shapes
2. Right panel > "Data" > "Conditional Formatting"
3. Create rule:
   - IF [data field] [condition] [value]
   - THEN [apply style]

**Example Rules:**
- IF Cycle Time > 24 hours THEN Fill = Red
- IF FTT % < 90% THEN Border = Thick Red
- IF Status = "Complete" THEN Fill = Green

**Benefits:**
- Visual highlighting of problems
- Automatic color coding
- Live dashboard effect

#### Custom Shape Libraries

**Create Custom Library:**
1. Create shapes with standard styling
2. Add your logo, colors, fonts
3. Drag shapes to "My Shapes" panel
4. Name library (e.g., "Company Process Shapes")
5. Share library with team

**What to Include:**
- Branded process shapes
- Standard icons
- Frequently used symbols
- Templates elements
- Color palette

**Sharing Libraries:**
1. Click "..." on library name
2. "Share Shape Library"
3. Enter team members' emails
4. Library appears in their accounts

### Integration Capabilities

#### Google Workspace

**Google Drive:**
- Save diagrams to Google Drive
- Auto-sync between Lucidchart and Drive
- Access from Drive interface
- Maintain Drive permissions

**Google Docs/Sheets:**
- Insert diagrams as images
- Add-on: Lucidchart Diagrams
- Embed live diagram (updates when diagram changes)
- Link data from Sheets

**Setup:**
1. Lucidchart Settings > Integrations
2. Enable Google Drive integration
3. Authorize access
4. Choose default save location

#### Microsoft Office

**Integration Points:**
- Word: Insert diagrams
- Excel: Link data
- PowerPoint: Insert diagrams
- Outlook: Share via email
- Teams: Preview and edit
- SharePoint: Embed diagrams

**Add-ins:**
1. Download Lucidchart add-ins
2. Install in Office applications
3. Insert > Add-ins > Lucidchart
4. Select diagram to insert

**Best Practices:**
- Insert as image for presentations
- Embed for living documents
- Update links before sharing

#### Atlassian Integration

**Confluence:**
- Native integration
- Embed diagrams in pages
- Edit directly from Confluence
- Version control maintained

**Jira:**
- Attach diagrams to issues
- Link process to stories
- Visual workflow documentation

**Setup:**
1. Confluence/Jira admin
2. Install Lucidchart app from marketplace
3. Configure permissions
4. Use macro to insert diagrams

### Export and Publishing

#### Export Formats

**Static Exports:**
- PNG: High-quality images (use for presentations)
- JPEG: Compressed images
- PDF: Document format (preserves layout)
- SVG: Scalable vector (use for web)

**Export Settings:**
1. File > Download
2. Choose format
3. Set options:
   - Resolution (for PNG/JPEG)
   - Transparent background
   - Include/exclude specific layers
4. Download

**Recommendations:**
- Presentations: PNG at 300 DPI
- Web: SVG for scalability
- Printing: PDF
- Documentation: PNG or PDF

#### Publishing Options

**Public Link:**
- File > Publish
- Generate public URL
- Anyone with link can view
- Update published version anytime

**Website Embed:**
- File > Publish > Embed
- Copy iframe code
- Paste in website HTML
- Diagram loads in page

**Export to Visio:**
- File > Export > Visio (.vsdx)
- Maintains shapes and connections
- For users who prefer Visio

### Templates and Shortcuts

#### Recommended Templates

**For Business Analysts:**
1. **Process Flow Chart**
   - Basic process documentation
   - Start with this for most processes

2. **BPMN 2.0**
   - Standard compliant process models
   - Use for formal documentation

3. **Cross-Functional Flowchart**
   - Swimlane diagrams
   - Show handoffs between teams

4. **Value Stream Map**
   - Lean analysis
   - Identify waste and delays

5. **Decision Tree**
   - Complex decision logic
   - Multiple branches and outcomes

6. **Org Chart**
   - Team structures
   - Reporting relationships

#### Keyboard Shortcuts

**Essential Shortcuts:**

Navigation:
- `Space + Drag`: Pan canvas
- `Ctrl/Cmd + Scroll`: Zoom in/out
- `Ctrl/Cmd + 0`: Fit to page
- `Ctrl/Cmd + 1`: Zoom to 100%

Editing:
- `Ctrl/Cmd + D`: Duplicate selected
- `Ctrl/Cmd + G`: Group selected
- `Ctrl/Cmd + Shift + G`: Ungroup
- `Ctrl/Cmd + Z`: Undo
- `Ctrl/Cmd + Y`: Redo

Selection:
- `Ctrl/Cmd + A`: Select all
- `Ctrl/Cmd + Click`: Add to selection
- `Shift + Click`: Range select

Shapes:
- `S`: Create sticky note
- `L`: Create line
- `T`: Create text box
- `Enter`: Edit selected shape text

Alignment:
- `Ctrl/Cmd + Shift + Arrow`: Align shapes
- `Alt + Drag`: Duplicate while moving

**Pro Tips:**
- Press and hold `Alt` while dragging to duplicate
- Double-click line to add text
- Hold `Shift` while drawing lines for straight lines
- Use `Tab` to cycle through shapes

---

## Miro Collaboration Patterns

### Overview

Miro is an infinite online whiteboard platform designed for visual collaboration. Unlike Lucidchart's focus on formal diagrams, Miro excels at brainstorming, workshops, and collaborative analysis sessions.

### When to Use Miro vs. Lucidchart

**Use Miro for:**
- Brainstorming sessions
- Workshops and facilitation
- Design thinking activities
- Collaborative analysis (affinity mapping)
- Agile ceremonies (retrospectives, planning)
- Early-stage process discovery
- Real-time collaboration with large groups

**Use Lucidchart for:**
- Formal process documentation
- BPMN-compliant diagrams
- Final documentation
- Detailed technical diagrams
- Export to other tools
- Standardized templates

### Setting Up Miro for Business Analysis

#### Board Organization

**Creating Project Structure:**

1. **Main Project Board** (hub)
   - Links to all related boards
   - Project overview and status
   - Key stakeholders and timeline
   - Document repository

2. **Discovery Boards**
   - Current state process mapping
   - Pain point collection
   - Stakeholder interviews
   - Data gathering

3. **Analysis Boards**
   - Root cause analysis
   - Process comparison
   - Gap analysis
   - Prioritization

4. **Design Boards**
   - Future state design
   - Solution brainstorming
   - Prototyping

**Folder Structure:**
```
Project Name/
├── 00_Project Hub
├── 01_Discovery/
│   ├── Current State Process
│   ├── Stakeholder Interviews
│   └── Pain Points
├── 02_Analysis/
│   ├── Root Cause Analysis
│   ├── Value Stream Map
│   └── Prioritization Matrix
├── 03_Design/
│   ├── Future State Process
│   ├── Solution Options
│   └── Implementation Plan
└── 04_Archive/
    └── [Completed boards]
```

#### Template Library

**Essential Templates for BAs:**

1. **Process Mapping**
   - Miro's "User Story Map"
   - Custom SIPOC template
   - Swimlane template

2. **Analysis**
   - Fishbone diagram (Ishikawa)
   - 5 Whys
   - Affinity mapping
   - Impact/Effort matrix

3. **Workshops**
   - Retrospective templates
   - SWOT analysis
   - Design thinking canvas
   - Stakeholder mapping

**Creating Custom Templates:**
1. Build board with your standard setup
2. Add frames for different sections
3. Include instructions as sticky notes
4. Save as template
5. Share with team

### Collaborative Process Mapping

#### Live Process Discovery Sessions

**Pre-Session Setup:**
1. Create board from template
2. Add frames for each process area
3. Prepare sticky note colors:
   - Blue: Activities
   - Yellow: Decisions
   - Pink: Pain points
   - Green: Ideas/opportunities
4. Share link with participants
5. Test access and permissions

**During Session:**

**Facilitator Role:**
- Welcome participants (introduce Miro if needed)
- Explain board layout and color coding
- Set timer for activities (use Miro timer feature)
- Capture process steps as participants describe
- Use voting for prioritization
- Summarize and confirm understanding

**Step-by-Step Process:**

1. **Ice Breaker (5 min)**
   - Everyone adds sticky note with name and role
   - Quick Miro feature tour

2. **Current State (30 min)**
   - Participants add sticky notes for steps
   - Arrange in sequence left to right
   - Add decisions as diamonds
   - Draw arrows to connect

3. **Pain Points (20 min)**
   - Pink sticky notes for problems
   - Place near related process steps
   - Vote on biggest pain points (use Miro voting)

4. **Data Capture (15 min)**
   - Add text boxes for metrics
   - Document cycle times
   - Note volumes and frequencies

5. **Clarification (15 min)**
   - Review flow together
   - Ask questions
   - Resolve conflicts
   - Take screenshots

**Miro Features to Use:**
- Timer: Keep sessions moving
- Voting: Prioritize pain points
- Comments: Tag individuals with questions
- Cursor names: See who's contributing
- Frames: Organize sections
- Lock: Prevent accidental changes to completed areas

#### Asynchronous Collaboration

**When to Use:**
- Distributed teams across time zones
- Complex analysis requiring deep thought
- Sensitive topics (people may be more candid)
- Documentation review

**Structure for Async Work:**

1. **Clear Instructions**
   - Frame with large text: "Instructions"
   - Numbered steps
   - Due dates
   - Examples

2. **Structured Input Areas**
   - Clearly labeled frames
   - One topic per frame
   - Templates for consistency

3. **Comment Protocol**
   - Tag people with @mentions
   - Use comment threads
   - Set notifications

**Example Async Process:**

Day 1: Facilitator sets up board
- Creates frames for each process area
- Adds instruction sticky notes
- Shares link with request to add steps

Days 2-3: Participants add content
- Add process steps in their area
- Comment on others' contributions
- Flag questions or conflicts

Day 4: Facilitator reviews
- Consolidates duplicate items
- Organizes flow
- Adds follow-up questions as comments

Day 5: Participants respond
- Answer questions
- Resolve conflicts
- Vote on priorities

Day 6: Facilitator finalizes
- Create clean version
- Document decisions
- Plan next steps

### Workshop Facilitation Patterns

#### Root Cause Analysis Workshop

**Setup:**
1. Draw large fishbone diagram
2. Label "Problem" at fish head
3. Add 6 M categories as bones
4. Prepare sticky note supply

**90-Minute Workshop:**

**Phase 1: Problem Definition (15 min)**
- Agree on problem statement
- Write in fish head
- Confirm metrics (how big is problem?)

**Phase 2: Brainstorm Causes (30 min)**
- Each participant adds sticky notes
- 5 minutes silent generation
- Place notes on fishbone under relevant category
- Discuss and clarify
- Move notes if needed

**Phase 3: Drill Down (20 min)**
- Select top 3-5 causes (vote)
- For each, ask "Why?" 5 times
- Document chain of reasoning
- Identify root cause

**Phase 4: Validation (15 min)**
- Review root causes
- Check if they're addressable
- Rate confidence (High/Medium/Low)
- Assign investigation tasks

**Phase 5: Next Steps (10 min)**
- Agree on actions
- Assign owners
- Set deadlines
- Schedule follow-up

**Miro Features:**
- Voting: Prioritize causes
- Timer: Keep phases on track
- Tags: Assign action items
- Export: Save as PDF for documentation

#### Prioritization Workshop

**Impact vs. Effort Matrix:**

**Setup:**
```
High Impact
   │
   │  [Consider]  │  [DO IT!]
   │              │
───┼──────────────┼─────────
   │              │
   │  [Skip]      │  [Easy Wins]
   │              │
Low Impact        High Effort  Low Effort
```

**Process:**
1. List all improvement ideas on sticky notes
2. Each participant places their idea on matrix
3. Discussion and adjustment
4. Cluster similar items
5. Vote if disagreement
6. Document quadrants

**Outcomes:**
- Quick Wins: Do immediately
- Big Bets: Plan carefully, high ROI
- Fill-ins: Do if time/resources available
- Thankless Tasks: Avoid unless required

#### Future State Design Session

**Structure:**
1. Frame: Current State (left side)
2. Frame: Problems and Requirements (center)
3. Frame: Future State (right side)
4. Frame: Open Questions (bottom)

**Brainstorming Phase:**
- Time-boxed idea generation (10 min)
- Everyone adds sticky notes
- No criticism, all ideas welcome
- Build on others' ideas

**Grouping Phase:**
- Cluster similar ideas
- Name each cluster
- Identify themes

**Design Phase:**
- Sketch future state process
- Use different color for new elements
- Draw connections
- Add annotations

**Validation Phase:**
- Walk through future state
- Check against requirements
- Identify gaps
- Rate feasibility

### Advanced Miro Features for BAs

#### Smart Frameworks

**Pre-built Analysis Tools:**
- SWOT Analysis
- Porter's Five Forces
- Business Model Canvas
- Lean Canvas
- Customer Journey Map

**Using Frameworks:**
1. Search templates: "SWOT" or "Business Model"
2. Add to board
3. Invite stakeholders to fill sections
4. Export as image for reports

#### Integrations

**Connect Miro to:**

**Jira:**
- Import issues as cards
- Update status in Miro
- Sync back to Jira
- Visual sprint planning

**Confluence:**
- Embed boards in pages
- Keep documentation visual
- Link process to requirements

**Slack/Teams:**
- Share boards in channels
- Notifications for updates
- Quick access from chat

**Google/Microsoft:**
- Import docs and sheets
- Embed files in board
- Two-way updates

**Setup:**
1. Miro Settings > Apps & Integrations
2. Select tool to integrate
3. Authorize connection
4. Configure sync settings

#### Video and Audio

**Built-in Features:**
- Video chat while working
- Screen sharing
- Recording sessions
- Transcription (some plans)

**Best Practices:**
- Turn on video for engagement
- Use screen share to guide
- Record important sessions
- Download recording after

#### Smart Meeting

**Before Meeting:**
1. Create agenda frame
2. Add timer widgets
3. Prepare templates in frames
4. Share link in calendar invite

**During Meeting:**
1. Start with board tour
2. Use cursor to point/highlight
3. Enable "Bring everyone to me" feature
4. Use timer for time-boxing
5. Assign action items with tags

**After Meeting:**
1. Export board as PDF
2. Screenshot key areas
3. Extract action items (use Tags)
4. Share summary
5. Archive board or prepare for next session

### Miro Best Practices

#### Visual Organization

**Frame Usage:**
- One topic per frame
- Clear frame titles
- Color code frames by phase
- Lock completed frames

**Sticky Note Hygiene:**
- One idea per note
- Readable font size
- Consistent colors
- Group related notes

**Connection Lines:**
- Use arrows to show flow
- Avoid crossing lines
- Bold for important paths
- Color code relationships

#### Collaboration Etiquette

**Do:**
- Introduce yourself (name sticky note)
- Ask questions in comments
- Build on others' ideas
- Use voting respectfully
- Stay in designated areas
- Save frequently (auto-saves, but manual save before closing)

**Don't:**
- Delete others' contributions without asking
- Work in same area as someone actively working
- Move locked items
- Change board structure during live session
- Ignore comments directed at you

#### Performance Optimization

**Keep Boards Fast:**
- Limit board size (use multiple boards if needed)
- Compress uploaded images
- Remove unused elements
- Archive completed work
- Don't embed too many videos

**Loading Issues:**
- Clear browser cache
- Use desktop app for large boards
- Close other tabs
- Check internet connection
- Use lower quality setting if slow

---

## Confluence Publishing

### Overview

Confluence is a team workspace platform where knowledge and collaboration meet. For business analysts, it's the primary tool for publishing process documentation, requirements, and analysis artifacts.

### Setting Up Confluence for BA Work

#### Space Structure

**Recommended Hierarchy:**

```
Business Analysis Space
├── Home (overview and navigation)
├── Process Documentation/
│   ├── Order-to-Cash
│   ├── Procure-to-Pay
│   ├── Hire-to-Retire
│   └── [Other processes]
├── Requirements/
│   ├── Project A Requirements
│   ├── Project B Requirements
│   └── [Other projects]
├── Analysis & Design/
│   ├── Current State Analysis
│   ├── Gap Analysis
│   ├── Solution Options
│   └── Future State Design
├── Standards & Templates/
│   ├── Process Doc Template
│   ├── Requirements Template
│   ├── Analysis Template
│   └── Naming Conventions
└── Archive/
    └── [Outdated documentation]
```

**Page Hierarchy Best Practices:**
- Maximum 3-4 levels deep
- Group related pages
- Use consistent naming
- Include dates in version-specific pages
- Archive old versions, don't delete

#### Page Templates

**Creating BA Templates:**

1. **Process Documentation Template:**
```
# [Process Name]

## Overview
**Process Owner:** [Name]
**Last Updated:** [Date]
**Status:** [Draft | Active | Under Review]

## Purpose
[Why this process exists]

## Scope
**Includes:** [List]
**Excludes:** [List]

## Process Flow
[Embed Lucidchart diagram]

## Detailed Steps
[Table or numbered list]

## Roles & Responsibilities
[RACI table]

## Metrics
[KPIs and targets]

## Related Pages
[Links]
```

2. **Requirements Document Template:**
```
# Requirements: [Project Name]

## Document Info
**Author:** [Name]
**Status:** [Draft | Review | Approved]
**Last Updated:** [Date]

## Business Objectives
[Goals this project supports]

## Functional Requirements
[Detailed requirements]

## Non-Functional Requirements
[Performance, security, etc.]

## User Stories
[Jira links or embedded filter]

## Acceptance Criteria
[How to verify]

## Approvals
[Approval macro]
```

**Setting as Template:**
1. Create page with structure
2. Page menu > Templates
3. "Save as Template"
4. Name template
5. Set permissions
6. Share with team

### Publishing Process Documentation

#### From Lucidchart to Confluence

**Method 1: Embed Live Diagram**
1. In Confluence, edit page
2. Type `/lucid` and press Enter
3. Select Lucidchart macro
4. Choose diagram from Lucidchart library
5. Set display size
6. Save page

**Benefits:**
- Diagram updates automatically
- Always current version
- No manual updates needed

**Method 2: Insert as Image**
1. Export diagram from Lucidchart as PNG
2. In Confluence, edit page
3. Drag image file onto page
4. Resize as needed
5. Save page

**When to Use:**
- Final, stable diagrams
- Faster page load
- No Lucidchart access required

#### Creating Interactive Documentation

**Expand Macros:**
```
<expand>
  <expand-heading>Detailed Steps</expand-heading>
  <expand-content>
    [Detailed content here]
  </expand-content>
</expand>
```

Use for:
- Detailed procedures
- Additional context
- Examples
- Historical information

**Tabs:**
Create tabbed sections:
- Tab 1: Overview
- Tab 2: Detailed Process
- Tab 3: Exceptions
- Tab 4: Metrics

**Panel Macros:**
- Info panel: General information
- Note panel: Important notes
- Warning panel: Cautions
- Error panel: Critical issues
- Success panel: Best practices

**Example Usage:**
```markdown
{info}
This process was updated on [date] to reflect new compliance requirements.
{info}

{warning}
Skipping the approval step violates policy and will be flagged in audit.
{warning}
```

#### Table of Contents and Navigation

**Auto Table of Contents:**
1. Type `/table of contents`
2. Select macro
3. Choose style:
   - List style: Nested bullet list
   - Flat: Single level
   - Indent: Hierarchical
4. Set max level (typically 3)
5. Save page

**Page Tree:**
Shows page hierarchy:
1. Type `/page tree`
2. Select starting page (usually current)
3. Set depth
4. Configure display options

**Breadcrumbs:**
Automatically appears at top of page showing:
- Space Home > Parent Page > Current Page
- Click any level to navigate up

**Children Display:**
List child pages:
1. Type `/children`
2. Select macro
3. Choose display style
4. Excerpt, labels, or page titles only

### Linking and Cross-Referencing

#### Internal Links

**Link to Page:**
1. Type `[` while editing
2. Start typing page name
3. Select from dropdown
4. Press Enter

**Link to Heading:**
1. Link to page first
2. Add `#heading-name` after page name
3. Example: `[Requirements Page#functional-requirements]`

**Link to Space:**
- `[PageName|SpaceKey:PageTitle]`

#### Link Strategies

**For Process Documentation:**
- Link SOPs to related procedures
- Link to requirements documents
- Link to Jira workflows
- Link to training materials
- Link to forms and templates

**For Requirements:**
- Link to Jira epics/stories
- Link to current state analysis
- Link to solution design
- Link to test cases
- Link to deployment docs

**For Analysis:**
- Link to data sources
- Link to stakeholder interviews
- Link to current process docs
- Link to competitive analysis
- Link to research findings

### Version Control

#### Page Versions

**View History:**
1. Page menu > Page History
2. See all saved versions
3. Compare versions side-by-side
4. Restore previous version if needed

**Version Comments:**
- Always add comment when saving major changes
- Describe what changed
- Example: "Updated approval process to reflect new policy"

**Best Practices:**
- Save manually at milestones
- Minor edits can auto-save
- Use version labels for releases
- Review history before major changes

#### Content Archiving

**When to Archive:**
- Process no longer used
- Replaced by new version
- Project completed
- Outdated requirements

**How to Archive:**
1. Create "Archive" space or section
2. Move page to archive
3. Update links from active pages
4. Add "ARCHIVED" label
5. Remove from search (if needed)
6. Keep for records retention period

**Archive Label:**
Add to top of archived pages:
```
{info}
**ARCHIVED:** This document is no longer active.
See [New Version] for current information.
Archived Date: [Date]
{info}
```

### Collaboration and Review

#### Comments

**Page Comments:**
- Bottom of page for general discussion
- Threaded conversations
- @ mention to notify people
- Like comments to show agreement

**Inline Comments:**
- Highlight text while editing
- Add comment
- Pin to specific content
- Resolve when addressed

**Review Workflow:**
1. Author creates draft
2. Shares link with reviewers
3. Reviewers add inline comments
4. Author addresses comments
5. Reviewers resolve comments
6. Final approval

#### Approval Workflow

**Simple Approval:**
1. Edit page
2. Type `/approval`
3. Add approvers
4. Save page
5. Approvers notified
6. Track status in macro

**Formal Review:**
1. Set page restriction: "Can edit: [Specific people]"
2. Add workflow macro
3. Define states: Draft > Review > Approved
4. Progress through states
5. Publish when approved

### Advanced Features

#### Page Properties

**Create Data Tables:**
1. Type `/page properties`
2. Define properties (fields)
3. Fill in values
4. Link pages with same properties

**Example Properties:**
- Process Owner
- Last Review Date
- Status
- Priority
- Department

**Page Properties Report:**
- Aggregate properties from multiple pages
- Create dashboards
- Filter and sort
- Export to Excel

**Use Case:**
Create process inventory:
- List all processes
- Show owners
- Track review dates
- Filter by department

#### Custom Macros

**Useful Macros for BAs:**

1. **Jira Issues:**
   - Embed Jira issues/filters
   - Show project progress
   - Link requirements to stories

2. **Roadmap Planner:**
   - Visual timeline
   - Show project phases
   - Track milestones

3. **Status:**
   - Visual status indicators
   - Color coded
   - Examples: Green (Active), Yellow (Under Review), Red (Outdated)

4. **Excerpt:**
   - Define page summary
   - Reuse in other pages
   - Consistent descriptions

5. **Content by Label:**
   - Dynamic content
   - Auto-update
   - Group related pages

#### Labels and Organization

**Labeling Strategy:**

**By Type:**
- process-doc
- requirements
- analysis
- design
- template

**By Status:**
- draft
- in-review
- approved
- archived

**By Project:**
- project-alpha
- project-beta

**By Department:**
- sales
- operations
- finance
- it

**Search and Filter:**
- Click label to see all pages with that label
- Combine labels in search
- Create label dashboards
- Auto-generate content lists

### Publishing Standards

#### Documentation Standards

**Naming Conventions:**
- Use clear, descriptive titles
- Include version if multiple versions
- Date for point-in-time documents
- Examples:
  - "Order to Cash Process"
  - "Q4 2025 Requirements - Customer Portal"
  - "Current State Analysis - Inventory Management"

**Formatting Consistency:**
- H1: Page title (automatic)
- H2: Major sections
- H3: Subsections
- H4: Details

**Visual Elements:**
- One primary diagram per page
- Tables for structured data
- Panels for highlights
- Bullet lists for items

**Metadata:**
Every page should include:
- Owner/Author
- Last Updated date
- Status
- Related links
- Labels

#### Quality Checklist

Before publishing:
- [ ] Title is clear and descriptive
- [ ] Metadata is complete
- [ ] All links work
- [ ] Diagrams are legible
- [ ] Tables are formatted
- [ ] Spelling checked
- [ ] Proper labels applied
- [ ] Permissions set correctly
- [ ] Related pages linked
- [ ] Version comment added

---

## Jira Workflow Mapping

### Overview

Jira is the standard tool for issue tracking and agile project management. For business analysts, mapping business processes to Jira workflows ensures traceability from requirements to implementation.

### Understanding Jira Workflows

#### Workflow Components

**Statuses:**
- Current state of an issue
- Examples: To Do, In Progress, Done
- Appears in issue view
- Used for reporting

**Transitions:**
- Actions that move issue between statuses
- Can have conditions and validators
- Examples: Start Progress, Resolve, Close
- Buttons in Jira interface

**Resolution:**
- Why issue was closed
- Examples: Done, Won't Do, Duplicate
- Set when resolving
- Used for metrics

**Basic Workflow Example:**
```
[To Do] --Start Progress--> [In Progress] --Done--> [Done]
                                   │
                                   └--Block--> [Blocked] --Unblock--> [In Progress]
```

#### Mapping Process to Workflow

**Process Step → Jira Status:**

Example: Software Development Process

| Process Step | Jira Status | Entry Criteria | Exit Criteria |
|--------------|-------------|----------------|---------------|
| Backlog | To Do | Story created | Sprint assigned |
| In Development | In Progress | Developer assigned | Code complete |
| Code Review | In Review | PR created | Approved |
| QA Testing | In QA | Deployed to QA | Tests pass |
| UAT | In UAT | Business tester assigned | Acceptance |
| Deploy | Ready for Prod | QA signed off | Deployed |
| Complete | Done | In production | Verified |

**Decision Points → Transitions:**
- Approval/Rejection → Approve/Reject transitions
- Quality Gates → Pass/Fail transitions
- Escalation → Escalate transition

### Creating Workflows in Jira

#### Workflow Design Process

**Step 1: Document Current Process**
- Map as-is process (use Lucidchart/Miro)
- Identify steps and decision points
- Note who does what
- Understand exceptions

**Step 2: Define Statuses**
- One status per distinct state
- Use clear, meaningful names
- Group by workflow stage (To Do, In Progress, Done categories)
- Consider reporting needs

**Example Statuses:**
```
TO DO category:
- Backlog
- Ready for Dev

IN PROGRESS category:
- In Development
- Code Review
- In QA
- In UAT

DONE category:
- Done
- Won't Do
- Duplicate
```

**Step 3: Define Transitions**
- How to move between statuses
- Name with action verbs
- Consider who can perform
- Add validation rules

**Example Transitions:**
- Start Development (To Do → In Progress)
- Submit for Review (In Progress → Code Review)
- Approve (Code Review → In QA)
- Request Changes (Code Review → In Development)
- Pass QA (In QA → In UAT)
- Fail QA (In QA → In Development)
- Deploy (In UAT → Done)

**Step 4: Add Conditions**
- Who can perform transition
- Required fields
- Permission checks
- Custom conditions

**Example Conditions:**
- Only assignee can start progress
- Must have fix version to deploy
- QA role required to pass QA

**Step 5: Add Validators**
- Check before allowing transition
- Ensure data quality
- Examples:
  - Description must be filled
  - Subtasks must be done
  - Approval given

**Step 6: Add Post Functions**
- Automated actions after transition
- Examples:
  - Assign to reporter when rejected
  - Clear assignee when done
  - Update custom field
  - Trigger webhook

#### Implementing Workflows

**Navigate to Workflow:**
1. Settings (gear icon) > Issues
2. Workflows
3. Add workflow
4. Name workflow
5. Choose: Diagram (visual) or Text (list)

**Diagram Editor:**
1. Drag statuses onto canvas
2. Draw transitions between statuses
3. Label transitions
4. Configure each transition:
   - Conditions
   - Validators
   - Post functions
5. Publish workflow
6. Associate with issue types

**Best Practices:**
- Start simple, add complexity as needed
- Test with sample project first
- Get team feedback
- Document workflow in Confluence
- Include diagram

### Workflow Schemes

#### What Are Schemes?

**Workflow Scheme:**
- Maps issue types to workflows
- One scheme per project
- Different workflows for different issue types

**Example Scheme:**
```
Project: Customer Portal Development

Issue Type --> Workflow
- Story --> Development Workflow
- Bug --> Bug Workflow
- Epic --> Epic Workflow
- Task --> Simple Workflow
```

#### Creating Schemes

**Setup:**
1. Settings > Issues > Workflow Schemes
2. Add workflow scheme
3. Name it
4. Add workflow mappings:
   - Issue Type: Story → Workflow: Development Workflow
   - Issue Type: Bug → Workflow: Bug Workflow
5. Associate scheme with project

**Why Use Multiple Workflows:**
- Different process for bugs vs. features
- Simpler workflow for tasks
- Complex workflow for change requests
- Compliance workflow for specific types

### Advanced Workflow Features

#### Automation Rules

**Trigger → Condition → Action**

**Example Rules:**

1. **Auto-assign based on component:**
   - Trigger: Issue created
   - Condition: Component = "Frontend"
   - Action: Assign to Frontend Team

2. **Reminder for stale issues:**
   - Trigger: Scheduled (daily)
   - Condition: Status = In Progress AND Updated < 7 days ago
   - Action: Comment and @ mention assignee

3. **Auto-transition on PR merge:**
   - Trigger: Commit/PR merged (via webhook)
   - Condition: Issue in "In Development"
   - Action: Transition to "Code Review"

**Creating Automation:**
1. Project Settings > Automation
2. Create rule
3. Choose trigger
4. Add conditions (optional)
5. Add actions
6. Name and enable rule

#### Status Categories

**Three Categories:**
- To Do (blue)
- In Progress (yellow)
- Done (green)

**Why It Matters:**
- Boards use categories
- Reports aggregate by category
- Simplifies views
- Standardizes across projects

**Mapping Statuses:**
1. Workflows > View workflow
2. Each status has category
3. Assign appropriately
4. Affects kanban/scrum boards

#### Parallel Approvals

**Scenario:** Need approval from multiple stakeholders

**Approach 1: Parallel Statuses**
```
[In Review] --Request Approval--> [Pending Manager Approval]
                                 [Pending Legal Approval]
                                 [Pending Security Approval]
                                        ↓ (All approved)
                                    [Approved]
```

**Approach 2: Sub-tasks**
```
Story: [Main Issue]
  Sub-task: Manager Approval [Approved]
  Sub-task: Legal Approval [Approved]
  Sub-task: Security Approval [In Progress]

Validator on main issue transition:
"All sub-tasks must be resolved"
```

**Approach 3: Custom Fields + Automation**
- Add approval fields (checkboxes or status)
- Automation checks all approvals
- Auto-transitions when all approved

### Process Documentation Integration

#### Linking Processes to Jira

**From Confluence:**
1. Document process in Confluence
2. Add Jira workflow diagram
3. Create table mapping:
   - Process step
   - Jira status
   - Who performs
   - Expected duration

**From Lucidchart:**
1. Create swimlane with process
2. Annotate with Jira statuses
3. Export and embed in Confluence
4. Link from Jira project

**Jira Issue Links:**
- Add "process-doc" link type
- Link stories to process doc
- View from issue
- Traceability maintained

#### Workflow Reporting

**Built-in Reports:**

1. **Control Chart:**
   - Cycle time per issue
   - Identify outliers
   - Process capability

2. **Cumulative Flow Diagram:**
   - Issues in each status over time
   - Spot bottlenecks
   - Capacity planning

3. **Cycle Time Report:**
   - Time spent in each status
   - Median/average/percentiles
   - Process improvement data

**Custom Dashboards:**

**Process Health Dashboard:**
- Gadget: Filter results (all issues)
- Gadget: Average age by status
- Gadget: Status pie chart
- Gadget: Issues in status (table)

**Setup:**
1. Dashboards > Create dashboard
2. Add gadgets
3. Configure filters
4. Share with team

### Integration with BA Tools

#### Lucidchart + Jira

**Embed Jira in Lucidchart:**
- Pull issue details into diagram
- Show current status
- Visual project tracking

**Workflow Visualization:**
1. Create Jira workflow in Lucidchart
2. Use BPMN notation
3. Add data linking to actual Jira workflow
4. Export and share

#### Miro + Jira

**Import Jira Issues:**
1. Miro board > Add app
2. Select Jira
3. Choose filter or project
4. Import as cards
5. Manipulate visually

**Use Cases:**
- Sprint planning (move cards between swim lanes)
- Story mapping (arrange by theme and priority)
- Dependency mapping (draw connections)

**Sync Back:**
- Some changes sync back to Jira
- Status updates
- Priority changes
- Check Miro docs for current capabilities

#### Confluence + Jira

**Jira Macros in Confluence:**

1. **Jira Issues Macro:**
   - Embed single issue
   - JQL filter results
   - Always current data

2. **Roadmap Planner:**
   - Timeline view
   - Show epics/stories
   - Visual planning

3. **Status by Project:**
   - Dashboard in Confluence
   - Multiple projects
   - Executive view

**Process Documentation Template:**
```markdown
# Process Name

## Workflow
[Jira workflow diagram image]

## Current Work
{jira-issues:jql=project = PROJ AND status != Done}

## Recent Completions
{jira-issues:jql=project = PROJ AND resolved >= -7d}
```

### Best Practices

#### Workflow Design

**Keep It Simple:**
- Start with minimum statuses
- Add complexity only when needed
- Don't model every micro-step
- Focus on reportable stages

**Clear Naming:**
- Use active verbs for transitions
- Clear status names (avoid jargon)
- Consistent with process docs
- Team can understand immediately

**Validation:**
- Test workflow with real scenarios
- Pilot with small team
- Gather feedback
- Iterate

**Documentation:**
- Document workflow in Confluence
- Include diagram
- Explain each status and transition
- Link from Jira project

#### Governance

**Change Control:**
- Don't change live workflows without notice
- Test changes in test project
- Communicate to team
- Update documentation

**Regular Review:**
- Quarterly workflow review
- Check if still matches process
- Gather team feedback
- Optimize based on metrics

**Training:**
- Onboard new team members
- Explain workflow meaning
- When to use each status
- How to escalate

---

## Tool Integration Patterns

### End-to-End Workflow

**Discovery → Analysis → Design → Implementation → Documentation**

#### Phase 1: Discovery (Miro)
- Collaborative process mapping
- Stakeholder interviews
- Pain point collection
- Export: Screenshots to Confluence

#### Phase 2: Analysis (Lucidchart + Confluence)
- Formal process diagrams (BPMN)
- Value stream mapping
- Root cause analysis
- Publish: Embed in Confluence

#### Phase 3: Design (Lucidchart + Miro)
- Future state design
- Workflow design
- Solution brainstorming
- Document: Link from Confluence

#### Phase 4: Implementation (Jira)
- Create workflow in Jira
- Map to process steps
- Track implementation
- Update: Status in dashboard

#### Phase 5: Documentation (Confluence)
- Publish final process docs
- Embed Lucidchart diagrams
- Link Jira workflows
- Maintain: Living documentation

### Tool Selection Matrix

| Activity | Primary Tool | Secondary Tool | Output |
|----------|--------------|----------------|--------|
| Brainstorming | Miro | - | Screenshots, ideas |
| Process Discovery | Miro | - | Current state notes |
| Formal Diagrams | Lucidchart | - | BPMN, VSM |
| Collaboration | Miro | Confluence | Workshop results |
| Documentation | Confluence | - | Published docs |
| Workflow Implementation | Jira | - | Live workflow |
| Requirements | Confluence | Jira | Req docs + stories |
| Project Tracking | Jira | Confluence | Dashboards |
| Presentations | PowerPoint | Lucidchart | Export diagrams |
| Data Analysis | Excel/Sheets | Lucidchart | Linked data viz |

### Common Integration Scenarios

#### Scenario 1: New Process Documentation

1. **Miro:** Facilitate discovery workshop
2. **Export:** Save board as PDF
3. **Lucidchart:** Create formal BPMN diagram
4. **Confluence:** Create process doc page
5. **Embed:** Add Lucidchart diagram
6. **Link:** Reference from related pages
7. **Jira:** Create workflow matching process
8. **Update:** Confluence doc with Jira workflow link

#### Scenario 2: Process Improvement Project

1. **Confluence:** Create project space
2. **Miro:** Map current state
3. **Export:** Screenshots to Confluence
4. **Analysis:** Use Miro for root cause analysis
5. **Design:** Future state in Lucidchart
6. **Confluence:** Improvement proposal document
7. **Jira:** Track improvement tasks
8. **Update:** Confluence with new process

#### Scenario 3: Requirements to Implementation

1. **Miro:** User story mapping workshop
2. **Confluence:** Requirements document
3. **Jira:** Create epics and stories
4. **Link:** Confluence pages to Jira issues
5. **Lucidchart:** System design diagrams
6. **Embed:** In Confluence architecture page
7. **Jira:** Track development with workflow
8. **Report:** Dashboard in Confluence

### Tips for Seamless Integration

**Naming Consistency:**
- Use same process names across tools
- Consistent project codes
- Standard abbreviations

**Linking Strategy:**
- Always link Confluence to Jira
- Reference diagrams in Jira descriptions
- Create "Resources" section in Confluence

**Single Source of Truth:**
- Confluence: Documentation and requirements
- Jira: Workflow and implementation tracking
- Lucidchart: Formal diagrams (live embed)
- Miro: Collaboration and working sessions

**Update Cadence:**
- Miro: During active work
- Lucidchart: When process stabilizes
- Confluence: When ready to publish
- Jira: Continuous

**Permission Alignment:**
- Match access across tools
- Same team in all tools
- Consistent sharing settings

---

**Document Version:** 1.0
**Last Updated:** November 21, 2025
**Total Lines:** 300+
