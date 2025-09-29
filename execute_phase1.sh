#!/bin/bash
# Execute Phase 1 of the Performia migration

echo "🦆 Starting Performia Migration - Phase 1"
echo "=========================================="
echo ""

cd /Users/danielconnolly/Projects/Performia

# Start Goose with necessary extensions and execute Phase 1
/Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << 'EOF'
Phase 1: Repository Analysis & Backup

Please execute the following tasks:

1. Use developer__shell to check for uncommitted changes in both directories:
   - /Users/danielconnolly/Projects/Performia
   - /Users/danielconnolly/Projects/Performia-front

2. Use developer__analyze to get a directory overview of both:
   - /Users/danielconnolly/Projects/Performia
   - /Users/danielconnolly/Projects/Performia-front/performia---living-chart

3. Create a CODEBASE_COMPARISON.md file with:
   - Directory structure comparison
   - List of unique files in each repo
   - Configuration file differences (package.json, requirements.txt, etc.)
   - Technology stack differences

4. Remember the analysis in memory for future phases

Start with checking git status in both repositories.
EOF
