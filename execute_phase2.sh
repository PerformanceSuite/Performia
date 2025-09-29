#!/bin/bash
# Phase 2: Create Unified Structure - Let Goose handle everything

echo "🚀 Phase 2: Creating Unified Structure with Goose"
echo "=================================================="
echo ""

cd /Users/danielconnolly/Projects/Performia

/Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << 'EOF'
PHASE 2: CREATE UNIFIED STRUCTURE

You are executing Phase 2 of the Performia migration. Based on the CODEBASE_COMPARISON.md, create the unified directory structure.

TASKS TO EXECUTE:

1. First, verify our current location:
   - Use developer__shell: pwd
   - Use developer__shell: ls -la

2. Create the new directory structure:
   - Use developer__shell: mkdir -p frontend
   - Use developer__shell: mkdir -p backend
   - Use developer__shell: mkdir -p shared

3. Move the better frontend from Performia-front:
   - Use developer__shell: cp -r /Users/danielconnolly/Projects/Performia-front/performia---living-chart/* ./frontend/
   - Use developer__shell: ls -la ./frontend/

4. Move backend components to backend directory:
   - Use developer__shell: mv JuceLibraryCode backend/
   - Use developer__shell: mv src backend/
   - Use developer__shell: mv sc backend/
   - Use developer__shell: mv ingest-analyze-pipe backend/
   - Use developer__shell: mv performia_agent.py backend/
   - Use developer__shell: mv orchestrator.py backend/
   - Use developer__shell: ls -la backend/

5. Move shared configurations:
   - Use developer__shell: mv requirements.txt shared/
   - Use developer__shell: cp frontend/package.json shared/frontend-package.json
   - Use developer__shell: ls -la shared/

6. Remember the migration status:
   - Use memory__remember_memory:
     Category: migration_status
     Tags: phase2, structure_created
     Memory: Phase 2 complete. Unified structure created with frontend/, backend/, and shared/ directories.

7. Create a summary report:
   - Use developer__text_editor to create "PHASE2_COMPLETE.md" with a summary of what was moved

Report each step's success or failure.
EOF
