#!/bin/bash
# Test Goose with extensions

cd /Users/danielconnolly/Projects/Performia

# Start Goose and test filesystem access
/Users/danielconnolly/bin/goose-smart session << 'EOF'
Read the MIGRATION_PLAN.md file in the current directory
EOF
