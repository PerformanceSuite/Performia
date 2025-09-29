#!/bin/bash
# Simple Git test for Goose

cd /Users/danielconnolly/Projects/Performia

/Users/danielconnolly/bin/goose-smart session --with-builtin developer << 'EOF'
Use developer__shell to run: git status
EOF
