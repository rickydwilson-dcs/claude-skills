#!/bin/bash
# Update commands/CATALOG.md to remove speckit and fix statistics

FILE="commands/CATALOG.md"

# Backup original
cp "$FILE" "output/2025-11-24_20-33-06_docs-reorganization/CATALOG-original.md"

# Update total commands: 20 → 12
sed -i '' 's/\*\*Total Commands:\*\* 20/\*\*Total Commands:\*\* 12/' "$FILE"

# The main update will be done manually due to complexity
echo "Created backup and updated total. Manual updates needed for:"
echo "1. Remove General Category (Speckit Workflow) section (lines ~39-56)"
echo "2. Remove speckit from Browse by Pattern section"
echo "3. Update statistics tables"
