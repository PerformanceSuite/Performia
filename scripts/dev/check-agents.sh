#!/usr/bin/env bash

# Quick agent status check
# Usage: ./scripts/dev/check-agents.sh

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

cd "$PROJECT_ROOT"
CURRENT_BRANCH=$(git branch --show-current)

echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Agent Status - $(date '+%H:%M:%S')${NC}"
echo -e "${BLUE}════════════════════════════════════════════${NC}\n"

# Check each branch
for branch in feature/frontend-optimization feature/audio-pipeline-optimization feature/voice-control-integration; do
    git checkout "$branch" 2>/dev/null >&2

    commits=$(git rev-list --count main..$branch 2>/dev/null || echo "0")
    files=$(git diff --name-only main..$branch 2>/dev/null | wc -l | tr -d ' ')
    unstaged=$(git status -s 2>/dev/null | wc -l | tr -d ' ')
    recent=$(find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" \) -mmin -5 2>/dev/null | grep -v node_modules | grep -v .git | wc -l | tr -d ' ')

    if [ "$commits" -gt 0 ]; then
        last_commit=$(git log -1 --format="%ar" 2>/dev/null)
    else
        last_commit="no commits"
    fi

    # Status indicator
    if [ "$recent" -gt 0 ]; then
        status="${GREEN}⚡ ACTIVE${NC}"
    else
        status="${YELLOW}⏸ Idle${NC}"
    fi

    echo -e "${CYAN}${branch}${NC}"
    echo -e "  Commits: ${GREEN}$commits${NC} | Files: $files | Unstaged: $unstaged"
    echo -e "  Last: $last_commit"
    echo -e "  Status: $status"
    echo ""
done

# Restore original branch
git checkout "$CURRENT_BRANCH" 2>/dev/null >&2

echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo -e "Recent commits across all branches:"
git log --all --oneline --decorate -3
echo ""