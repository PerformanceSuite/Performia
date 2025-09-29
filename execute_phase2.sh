#!/bin/bash
# Execute Phase 2 of the Performia migration - Create Unified Structure

echo "🚀 Starting Performia Migration - Phase 2"
echo "=========================================="
echo "Creating Unified Directory Structure"
echo ""

cd /Users/danielconnolly/Projects/Performia

# Use Goose to create the unified structure
/Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << 'EOF'
Phase 2: Create Unified Directory Structure

Based on the CODEBASE_COMPARISON.md analysis, let's create the unified structure:

1. First, use developer__shell to create the new directories:
   mkdir -p frontend
   mkdir -p backend
   mkdir -p shared

2. Move the better frontend from Performia-front:
   Use developer__shell to copy:
   cp -r /Users/danielconnolly/Projects/Performia-front/performia---living-chart/* ./frontend/
   
3. Move backend components to backend/:
   - Move src/ to backend/src/
   - Move JuceLibraryCode/ to backend/JuceLibraryCode/
   - Move sc/ to backend/sc/
   - Move ingest-analyze-pipe/ to backend/ingest-analyze-pipe/
   - Move performia_agent.py to backend/
   - Move orchestrator.py to backend/
   
4. Keep the following in root:
   - .git/
   - .github/
   - scripts/
   - docs/
   - MIGRATION_PLAN.md
   - README.md
   - .goosehints
   
5. Create a new unified package.json in frontend/ that merges dependencies

Start by creating the directories and listing current structure.
EOF
