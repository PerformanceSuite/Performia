#!/usr/bin/env bash

# Simple parallel agent starter
# Usage: ./scripts/dev/start-parallel.sh

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/.claude/logs"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create log directory
mkdir -p "$LOG_DIR"

cd "$PROJECT_ROOT"

echo -e "${BLUE}════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Performia Parallel Agent Setup${NC}"
echo -e "${BLUE}════════════════════════════════════════════${NC}\n"

# Create branches if they don't exist
BRANCHES=(
    "feature/frontend-optimization"
    "feature/audio-pipeline-optimization"
    "feature/voice-control-integration"
)

for branch in "${BRANCHES[@]}"; do
    if ! git show-ref --verify --quiet "refs/heads/$branch"; then
        echo -e "${GREEN}✓ Creating branch: $branch${NC}"
        git branch "$branch"
    else
        echo -e "${YELLOW}○ Branch exists: $branch${NC}"
    fi
done

echo ""
echo -e "${GREEN}✓ Branches ready!${NC}\n"

echo -e "${BLUE}Next steps:${NC}"
echo -e "1. Open 3 terminal windows"
echo -e "2. In each terminal, run:\n"

echo -e "   ${YELLOW}Terminal 1 (Frontend):${NC}"
echo -e "   cd $PROJECT_ROOT"
echo -e "   git checkout feature/frontend-optimization"
echo -e "   claude\n"

echo -e "   ${YELLOW}Terminal 2 (Audio):${NC}"
echo -e "   cd $PROJECT_ROOT"
echo -e "   git checkout feature/audio-pipeline-optimization"
echo -e "   claude\n"

echo -e "   ${YELLOW}Terminal 3 (Voice):${NC}"
echo -e "   cd $PROJECT_ROOT"
echo -e "   git checkout feature/voice-control-integration"
echo -e "   claude\n"

echo -e "3. ${BLUE}Start dashboard:${NC}"
echo -e "   ./scripts/dev/agent-dashboard.sh\n"

# Log session start
echo "$(date): Initialized parallel agent setup" >> "$LOG_DIR/sessions.log"