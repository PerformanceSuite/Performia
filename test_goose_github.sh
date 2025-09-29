#!/bin/bash
# Test Goose's ability to use git and GitHub

cd /Users/danielconnolly/Projects/Performia

/Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << 'EOF'
Please verify GitHub access and perform these git operations:

1. Use developer__shell to run: git status
2. Use developer__shell to run: git log --oneline -5
3. Use developer__shell to run: git remote -v
4. Use developer__shell to check GitHub CLI: gh auth status
5. Create a new test file called "goose-test.txt" with content "Goose was here!"
6. Use developer__shell to: git add goose-test.txt
7. Use developer__shell to: git commit -m "Test: Goose can commit"
8. Use developer__shell to: git push origin HEAD:replit

Report the results of each command.
EOF
