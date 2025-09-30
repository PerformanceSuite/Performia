#!/bin/bash

# Monitor multiple Claude Code sessions in parallel
# Usage: ./scripts/dev/monitor-sessions.sh

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SESSION_DIR="$HOME/.cache/claude-code/sessions"
LOG_DIR="$PROJECT_ROOT/.claude/logs"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Create log directory
mkdir -p "$LOG_DIR"

echo -e "${BLUE}=== Performia Session Monitor ===${NC}"
echo -e "Monitoring Claude Code sessions...\n"

# Function to get active sessions
get_active_sessions() {
    if [ -d "$SESSION_DIR" ]; then
        find "$SESSION_DIR" -type f -name "*.json" -mmin -60 | wc -l
    else
        echo "0"
    fi
}

# Function to check git status
check_git_status() {
    cd "$PROJECT_ROOT"

    # Check for uncommitted changes
    if [[ -n $(git status -s) ]]; then
        echo -e "${YELLOW}⚠ Uncommitted changes detected${NC}"
        git status -s | head -5
        echo ""
    fi

    # Check current branch
    BRANCH=$(git branch --show-current)
    echo -e "${GREEN}📍 Current branch: $BRANCH${NC}\n"
}

# Function to show recent activity
show_recent_activity() {
    cd "$PROJECT_ROOT"

    echo -e "${BLUE}Recent commits (last 3):${NC}"
    git log --oneline -3
    echo ""
}

# Function to monitor file changes
monitor_changes() {
    echo -e "${BLUE}Files modified in last 5 minutes:${NC}"
    find "$PROJECT_ROOT" -type f \
        -name "*.ts" -o -name "*.tsx" -o -name "*.py" -o -name "*.md" \
        -mmin -5 2>/dev/null | grep -v node_modules | grep -v .git | head -10
    echo ""
}

# Function to check for conflicts
check_conflicts() {
    cd "$PROJECT_ROOT"

    if git ls-files -u | grep -q .; then
        echo -e "${RED}⚠️  MERGE CONFLICTS DETECTED${NC}"
        git ls-files -u | cut -f 2 | sort -u
        echo ""
    fi
}

# Function to show agent status
show_agent_status() {
    echo -e "${BLUE}=== Agent Status ===${NC}"

    # Check for feature branches
    cd "$PROJECT_ROOT"
    BRANCHES=$(git branch | grep feature/ | wc -l)
    echo -e "Active feature branches: ${GREEN}$BRANCHES${NC}"
    git branch | grep feature/ || echo "No feature branches"
    echo ""
}

# Main monitoring loop
while true; do
    clear
    echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Performia Parallel Session Monitor     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
    echo ""

    # Show timestamp
    echo -e "${GREEN}⏰ $(date '+%Y-%m-%d %H:%M:%S')${NC}\n"

    # Active sessions
    SESSIONS=$(get_active_sessions)
    echo -e "${GREEN}🤖 Active Claude sessions: $SESSIONS${NC}\n"

    # Show agent status
    show_agent_status

    # Git status
    check_git_status

    # Recent activity
    show_recent_activity

    # Recent changes
    monitor_changes

    # Check for conflicts
    check_conflicts

    echo -e "${YELLOW}Press Ctrl+C to stop monitoring${NC}"
    echo -e "Refreshing in 10 seconds...\n"

    # Wait 10 seconds before next update
    sleep 10
done