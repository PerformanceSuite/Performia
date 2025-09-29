#!/bin/bash
# Test Goose with developer extension

cd /Users/danielconnolly/Projects/Performia

# Start Goose with developer extension explicitly
/Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << 'EOF'
list available tools
EOF
