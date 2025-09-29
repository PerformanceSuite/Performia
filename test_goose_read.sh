#!/bin/bash
# Test Goose can read our migration plan

cd /Users/danielconnolly/Projects/Performia

# Start Goose with developer and memory extensions
/Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << 'EOF'
Use developer__text_editor to view the MIGRATION_PLAN.md file and tell me what Phase 1 entails
EOF
