#!/bin/bash
# Full GitHub workflow test with Goose

cd /Users/danielconnolly/Projects/Performia

/Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << 'EOF'
Complete GitHub workflow test:

1. Use developer__text_editor to create a file called "goose-github-test.md" with:
   # Goose GitHub Test
   This file was created and committed by Goose AI agent.
   Timestamp: $(date)

2. Use developer__shell to: git add goose-github-test.md

3. Use developer__shell to: git commit -m "Test: Goose autonomous git operations"

4. Use developer__shell to: git push origin HEAD:replit

5. Use memory__remember_memory to save:
   Category: git_capabilities
   Tags: github, push, verified
   Memory: Successfully tested git operations including push to GitHub

Report success or any errors encountered.
EOF
