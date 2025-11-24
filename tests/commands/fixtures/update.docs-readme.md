---
name: update.docs-readme
description: Updates README.md with latest agent and skill counts
category: update
pattern: simple
---

# Update README Command

## Usage

```bash
/update.docs-readme
```

## What This Command Does

### Context
Gathers current statistics about agents and skills in the repository.

### Task
Updates the README.md file with the latest counts.

### Output
Updated README file with current information.

## Examples

### Example 1: Basic Usage

```bash
/update.docs-readme
```

Updates README with current counts automatically.

### Example 2: Verify Updates

```bash
/update.docs-readme --verify
```

Performs update and verifies all links are working.
