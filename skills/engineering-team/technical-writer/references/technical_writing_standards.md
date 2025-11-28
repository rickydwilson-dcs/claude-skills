# Technical Writing Standards

## Voice and Tone Framework

### 1. Voice Principles

#### Active Voice
Use active voice for 80%+ of sentences. Active voice makes documentation clearer and more direct.

**Active voice pattern:** Subject → Verb → Object

**Examples:**
- Good: "The API returns a JSON response."
- Avoid: "A JSON response is returned by the API."
- Good: "You can configure the timeout value."
- Avoid: "The timeout value can be configured."

**When to use passive voice (20%):**
- Focus on the action, not the actor: "The data is encrypted at rest."
- Unknown or irrelevant actor: "The service was deployed in 2020."
- Technical necessity: "Memory is allocated automatically."

#### Second Person for Instructions
Use "you" when giving instructions. This creates direct engagement.

**Examples:**
- Good: "You should install the dependencies first."
- Avoid: "Users should install the dependencies first."
- Good: "Run the following command:"
- Avoid: "The following command should be run:"

#### Present Tense
Use present tense for current actions and states. It's more immediate and clearer.

**Examples:**
- Good: "The function returns an array."
- Avoid: "The function will return an array."
- Good: "When you click Submit, the form validates."
- Avoid: "When you click Submit, the form will validate."

**Use future tense only for:**
- Explicit future events: "Version 2.0 will be released in Q1."
- Consequences of actions: "If you delete this file, the app will fail to start."

### 2. Tone Attributes

#### Professional but Approachable
- Clear and confident without being condescending
- Helpful without being patronizing
- Technical without being unnecessarily complex

**Examples:**
- Good: "This section explains how authentication works."
- Avoid: "Obviously, you need to understand authentication."
- Good: "The build process takes about 5 minutes."
- Avoid: "Unfortunately, the build process is slow."

#### Neutral and Objective
- Avoid opinions and subjective language
- State facts, provide evidence
- Let users draw their own conclusions

**Examples:**
- Good: "The API has a rate limit of 1000 requests per hour."
- Avoid: "The API has a generous rate limit."
- Good: "The function executes in O(n) time."
- Avoid: "The function is very fast."

#### Encouraging but Not Promotional
- Support users without overselling
- Acknowledge complexity when it exists
- Be honest about limitations

**Examples:**
- Good: "This feature simplifies user authentication."
- Avoid: "This revolutionary feature makes authentication effortless!"
- Good: "Currently, batch processing is not supported."
- Avoid: "Batch processing will be added soon!" (unless scheduled)

## Grammar Standards

### 1. Punctuation

#### Oxford Comma (Serial Comma)
Always use the Oxford comma for clarity.

**Examples:**
- Good: "The API supports JSON, XML, and YAML."
- Avoid: "The API supports JSON, XML and YAML."
- Good: "Initialize the database, run migrations, and start the server."
- Avoid: "Initialize the database, run migrations and start the server."

#### Hyphens and Dashes
- **Hyphen (-)**: Compound modifiers before nouns: "real-time processing", "two-factor authentication"
- **En dash (–)**: Ranges: "pages 10–20", "versions 1.0–2.0"
- **Em dash (—)**: Parenthetical statements: "The API—unlike the previous version—supports webhooks"

#### Semicolons
Use semicolons to connect closely related independent clauses.

**Examples:**
- Good: "The function returns true on success; it returns false on failure."
- Good: "Install Node.js 18 or higher; version 20 is recommended."

**Avoid semicolons in:**
- Lists with commas (use bullets instead)
- After headings
- In place of periods for unrelated statements

#### Colons
Use colons to introduce lists, examples, or explanations.

**Examples:**
- "The API requires three parameters: username, password, and token."
- "Note the following limitation: Batch operations are not supported."

#### Apostrophes
- **Possessive**: "the user's profile", "the API's response"
- **Contractions**: Avoid in formal documentation; use "do not" instead of "don't"

#### Quotation Marks
- Use for UI elements: Click the "Submit" button
- Use for exact code output: The error message "Connection timeout" appears
- Avoid scare quotes for emphasis; use **bold** or *italics* instead

### 2. Capitalization

#### Headings
- **H1 (Page title)**: Title Case: "Getting Started with the API"
- **H2-H6 (Section headings)**: Sentence case: "Install the dependencies"

#### Product Names
Follow official capitalization:
- "GitHub Actions", "Docker", "PostgreSQL", "JavaScript", "Node.js"

#### Job Titles and Roles
Lowercase unless preceding a name:
- "Talk to your system administrator"
- "Contact Administrator Jane Smith"

#### Technical Terms
- **Programming languages**: JavaScript, Python, Go, C++
- **Protocols**: HTTP, HTTPS, TCP/IP, REST
- **File formats**: JSON, XML, YAML, CSV
- **Technologies**: Follow official branding

#### Interface Elements
Use Title Case for menu items and buttons:
- "Click the File menu"
- "Select Edit Settings"
- "Click the Submit button"

### 3. Numbers and Units

#### Spell Out vs. Numerals

**Spell out:**
- One through nine (except for technical values)
- Numbers at the start of sentences: "Ten users can access..."

**Use numerals for:**
- 10 and above
- All technical values: "3 parameters", "5 MB", "2 seconds"
- Percentages: "5% of users"
- Versions: "version 2.1"
- Measurements: "8 CPU cores"

#### Units
- Use standard abbreviations: MB, GB, TB, KB/s, ms, sec
- Include space between number and unit: "10 MB", "5 seconds"
- Exceptions: "10%", "5GB" (when space-constrained)

#### Dates and Times
- **Date format**: YYYY-MM-DD (ISO 8601): "2025-11-28"
- **Alternative**: Month DD, YYYY: "November 28, 2025"
- **Time format**: 24-hour (HH:MM): "14:30" or 12-hour with AM/PM: "2:30 PM"
- **Time zones**: Always specify: "2:00 PM EST", "14:00 UTC"

## Sentence Structure

### 1. Sentence Length

**Target:** 15-25 words per sentence
**Maximum:** 30 words before considering a split

**Long sentence example:**
"When you configure the database connection, you need to specify the host, port, username, password, and database name in the configuration file, which is located in the config directory."

**Better (split into two):**
"Configure the database connection by specifying the host, port, username, password, and database name. Update the configuration file located in the config directory."

### 2. Paragraph Length

**Target:** 3-5 sentences per paragraph
**Maximum:** 7 sentences before considering a split

**Single-sentence paragraphs:**
- Use sparingly for emphasis
- Appropriate for warnings or critical information
- Follow with longer paragraph

### 3. Parallel Structure

Use parallel grammatical structure in lists and series.

**Examples:**
- Good: "Install the package, configure the settings, and start the server."
- Avoid: "Install the package, configuration of settings, and then you start the server."

**In bullet lists:**
- Start each item with the same part of speech
- Use all fragments or all complete sentences
- Maintain consistent verb tense

### 4. One Main Idea Per Sentence

Each sentence should convey one primary concept.

**Examples:**
- Avoid: "The API returns JSON and you should parse it with a JSON library and handle errors appropriately."
- Good: "The API returns JSON. Parse the response using a JSON library. Handle parsing errors appropriately."

## Document Structure

### 1. Heading Hierarchy

#### H1: Page Title Only
- One H1 per page
- Describes the entire page content
- Front matter for SEO and navigation

**Examples:**
- "Getting Started Guide"
- "API Reference: Authentication"
- "Installation Instructions"

#### H2: Major Sections
- Primary content divisions
- 3-7 H2 sections per page (optimal)
- Parallel structure in H2 titles

**Examples:**
- "Prerequisites"
- "Installation steps"
- "Configuration options"

#### H3: Subsections
- Break down H2 content
- Use when H2 section exceeds 500 words
- Maximum 3-5 H3s per H2

#### H4-H6: Rare Usage
- H4: Sub-subsections (use sparingly)
- H5-H6: Almost never needed; consider restructuring instead

**Heading hierarchy rule:** Never skip levels. If you have H3, you must have H2 above it.

### 2. Lists vs. Tables

#### Use Bulleted Lists When:
- Order doesn't matter
- Items are roughly equal in importance
- Each item is 1-2 lines
- 3-7 items (optimal)

#### Use Numbered Lists When:
- Order matters (steps, rankings)
- Referencing specific items: "See step 3"
- Sequential process

#### Use Tables When:
- Comparing multiple attributes across items
- Showing relationships between data
- Reference material (parameters, options)
- 3+ columns of structured data

**Table best practices:**
- Maximum 5 columns (for readability)
- Keep cell content concise (under 15 words)
- Use consistent formatting
- Include header row
- Consider responsive design for narrow screens

### 3. Introduction Pattern

Every document should include an introduction that answers:
1. **What** is this document about?
2. **Why** should you read it?
3. **Who** is it for?
4. **How long** will it take?

**Example:**
"This guide explains how to install and configure the authentication module. You'll learn how to set up OAuth 2.0, configure user permissions, and troubleshoot common issues. This guide is for developers implementing authentication in their applications. Estimated time: 20 minutes."

### 4. Conclusion Pattern

Every document should conclude with:
- Summary of key points
- Next steps or related resources
- Where to get help

**Example:**
"You've successfully configured authentication. Next, explore the [User Management API](#) to create and manage user accounts. For questions, visit our [support forum](https://example.com/support)."

## Code Examples

### 1. Language Tags

Always specify the language for syntax highlighting.

**Examples:**
````markdown
```javascript
const result = await fetchData();
```

```python
def calculate_total(items):
    return sum(items)
```

```bash
npm install package-name
```
````

### 2. Complete and Runnable

Code examples should be:
- **Complete**: Include all necessary imports and setup
- **Runnable**: Copy-paste should work without modification
- **Realistic**: Use realistic variable names and data

**Bad example:**
```javascript
// Incomplete
const data = fetch(url);
```

**Good example:**
```javascript
// Complete and runnable
const fetch = require('node-fetch');

async function getData() {
  const response = await fetch('https://api.example.com/data');
  const data = await response.json();
  return data;
}

getData().then(console.log);
```

### 3. Comments

**Use comments to:**
- Explain non-obvious logic
- Highlight important lines
- Provide context for code blocks

**Don't comment:**
- Obvious operations
- Every line (creates noise)
- Poor variable names (improve names instead)

**Examples:**
```javascript
// Good: Explains why
// Retry up to 3 times for transient network errors
const maxRetries = 3;

// Bad: States the obvious
// Set maxRetries to 3
const maxRetries = 3;
```

### 4. Highlighting Changes

Use comments to indicate additions, changes, or focus areas.

**Examples:**
```javascript
const config = {
  host: 'localhost',
  port: 3000,
  timeout: 5000,  // Add this line
};
```

### 5. Output Examples

Show both input and output when relevant.

**Example:**
```bash
$ npm install express

added 50 packages, and audited 51 packages in 2s
found 0 vulnerabilities
```

### 6. Error Handling

Include error handling in production-ready examples.

**Example:**
```javascript
try {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  const data = await response.json();
  return data;
} catch (error) {
  console.error('Failed to fetch data:', error);
  throw error;
}
```

## Formatting Standards

### 1. Admonition Blocks

Use admonition blocks to highlight important information.

#### Note
For supplementary information that adds context.

**Example:**
> **Note:** The API rate limit applies per API key, not per user.

#### Warning
For actions that could cause problems or data loss.

**Example:**
> **Warning:** Deleting this resource is permanent and cannot be undone.

#### Tip
For helpful suggestions or best practices.

**Example:**
> **Tip:** Use environment variables to store sensitive credentials instead of hardcoding them.

#### Important
For critical information that users must know.

**Example:**
> **Important:** This feature requires version 2.0 or higher.

**Formatting:**
- Bold the label: **Note:**, **Warning:**
- Follow with space, then content
- Keep to 1-2 sentences when possible

### 2. Inline Formatting

#### Code Elements
Use backticks for:
- Function names: `getData()`
- Variable names: `userId`
- Parameter names: `timeout`
- File names: `config.json`
- Command names: `npm install`
- HTTP methods: `GET`, `POST`

#### Bold
Use bold for:
- UI elements: Click the **Save** button
- Important terms on first use: **OAuth 2.0** is an authorization framework
- Emphasis (use sparingly)

#### Italics
Use italics for:
- Emphasis (rare in technical writing)
- Placeholders: Replace *your-api-key* with your actual key
- Book titles, RFC names: See *RFC 2616*

### 3. Link Text

Use descriptive link text that makes sense out of context.

**Examples:**
- Good: "See the [authentication guide](url) for details."
- Avoid: "See [here](url) for details."
- Good: "Learn more about [API rate limits](url)."
- Avoid: "Click [this link](url) to learn more."

**Link best practices:**
- Don't use "click here" or "this link"
- Keep link text under 8 words
- Make link text unique within a page
- Avoid full URLs in body text; use descriptive links

### 4. Screenshots and Images

**When to use:**
- Complex UI workflows
- Visual concepts (architecture diagrams)
- Before/after comparisons
- Error messages (when text description insufficient)

**Best practices:**
- Include alt text for accessibility: `![Dashboard overview](image.png)`
- Keep file sizes under 500 KB (optimize images)
- Use PNG for screenshots, SVG for diagrams
- Highlight relevant areas with arrows or boxes
- Include caption below image
- Don't rely solely on images; describe in text too

## Common Mistakes to Avoid

### 1. Passive Voice Overuse

**Problem:** Makes writing indirect and harder to follow.

**Examples:**
- Weak: "The request is sent to the server."
- Strong: "The client sends the request to the server."
- Weak: "An error will be returned if validation fails."
- Strong: "The API returns an error if validation fails."

### 2. Unclear Antecedents

**Problem:** Pronouns without clear references confuse readers.

**Examples:**
- Unclear: "The API calls the service, and it returns data."
- Clear: "The API calls the service, and the service returns data."
- Unclear: "This improves performance."
- Clear: "This caching mechanism improves performance."

### 3. Missing Prerequisites

**Problem:** Assuming knowledge or setup that readers may not have.

**Solution:** Always include a "Prerequisites" section listing:
- Required software versions
- Account requirements
- Prior knowledge needed
- Estimated time

### 4. Vague Instructions

**Problem:** Instructions that are too general or ambiguous.

**Examples:**
- Vague: "Configure the database."
- Specific: "Update the `DB_HOST` variable in `.env` to your database URL."
- Vague: "Make sure authentication is set up."
- Specific: "Create an API key in the dashboard and add it to your environment variables."

### 5. Inconsistent Terminology

**Problem:** Using different terms for the same concept.

**Solution:**
- Create a terminology glossary
- Use find-and-replace for consistency
- Document preferred terms

**Examples:**
- Don't mix: "log in", "sign in", "authenticate"
- Choose one: "log in" (and use consistently)

### 6. Overusing Jargon

**Problem:** Alienating readers with unnecessary technical terms.

**Solution:**
- Define technical terms on first use
- Link to glossary for complex concepts
- Use simpler alternatives when possible

**Examples:**
- Jargon: "Leverage the SDK to instantiate the client."
- Better: "Use the SDK to create the client."

### 7. Burying the Lead

**Problem:** Important information appears too late in document.

**Solution:**
- Lead with most important information
- Use inverted pyramid structure
- Put warnings and prerequisites early

### 8. Wall of Text

**Problem:** Long paragraphs and sections without visual breaks.

**Solution:**
- Break into shorter paragraphs (3-5 sentences)
- Use subheadings every 300-500 words
- Add lists, code blocks, and tables for variety
- Use white space intentionally

## Quality Checklist

Before publishing any technical documentation, verify:

### Content Quality
- [ ] Accurate and up-to-date information
- [ ] All code examples tested and working
- [ ] Technical terms defined on first use
- [ ] Prerequisites clearly stated
- [ ] No assumptions about reader knowledge

### Structure
- [ ] Clear H1 page title
- [ ] Logical heading hierarchy (no skipped levels)
- [ ] Introduction explains what, why, who, how long
- [ ] Conclusion with next steps
- [ ] Each section focused on one topic

### Clarity
- [ ] Active voice used in 80%+ of sentences
- [ ] Second person ("you") in instructions
- [ ] Present tense for current actions
- [ ] Sentences under 25 words average
- [ ] Paragraphs 3-5 sentences
- [ ] Clear antecedents for all pronouns

### Style
- [ ] Oxford comma used consistently
- [ ] Title Case for H1, Sentence case for H2-H6
- [ ] Numbers 1-9 spelled out (except technical)
- [ ] Consistent terminology throughout
- [ ] No jargon without definitions

### Formatting
- [ ] Code blocks have language tags
- [ ] Inline code for technical terms
- [ ] Descriptive link text (no "click here")
- [ ] Screenshots optimized and have alt text
- [ ] Lists and tables used appropriately
- [ ] Admonition blocks for important info

### Accessibility
- [ ] Alt text for all images
- [ ] Meaningful link text
- [ ] Proper heading hierarchy
- [ ] Color not sole indicator of meaning
- [ ] Readable contrast ratios

### Completeness
- [ ] All placeholders replaced
- [ ] All TODOs resolved
- [ ] Related documentation linked
- [ ] Support contact provided
- [ ] Version/date documented

### Final Polish
- [ ] Spell check completed
- [ ] Grammar check completed
- [ ] Peer review conducted
- [ ] Technical review by SME
- [ ] Tested by someone unfamiliar with topic

---

**Last Updated:** November 28, 2025
**Applies To:** All technical documentation (guides, tutorials, API docs, README files)
**Related:** api_documentation_patterns.md, developer_documentation_guide.md
