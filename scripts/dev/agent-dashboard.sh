#!/bin/bash

# Real-time dashboard for parallel Claude Code agents
# Usage: ./scripts/dev/agent-dashboard.sh

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/.claude/logs"

# Colors and formatting
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

# Function to draw box
draw_box() {
    local title=$1
    local width=60
    echo -e "${BLUE}╔$(printf '═%.0s' $(seq 1 $width))╗${NC}"
    printf "${BLUE}║${NC} ${BOLD}%-${width}s${NC} ${BLUE}║${NC}\n" "$title"
    echo -e "${BLUE}╠$(printf '═%.0s' $(seq 1 $width))╣${NC}"
}

draw_box_end() {
    local width=60
    echo -e "${BLUE}╚$(printf '═%.0s' $(seq 1 $width))╝${NC}"
}

# Function to get agent progress
get_agent_progress() {
    local branch=$1
    cd "$PROJECT_ROOT"

    if git show-ref --verify --quiet "refs/heads/$branch" 2>/dev/null; then
        git checkout "$branch" 2>/dev/null >&2

        # Count commits
        COMMITS=$(git rev-list --count main..$branch 2>/dev/null || echo "0")

        # Count file changes
        CHANGES=$(git diff --name-only main..$branch 2>/dev/null | wc -l)

        # Count uncommitted changes
        UNSTAGED=$(git status -s | wc -l)

        # Get last commit message
        LAST_COMMIT=$(git log -1 --pretty=format:"%s" 2>/dev/null || echo "No commits")

        # Check for recent activity (files modified in last 10 min)
        RECENT=$(find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" \) \
                 -mmin -10 2>/dev/null | grep -v node_modules | wc -l)

        echo "$COMMITS|$CHANGES|$UNSTAGED|$LAST_COMMIT|$RECENT"
    else
        echo "0|0|0|Branch not found|0"
    fi
}

# Function to get status indicator
get_status_icon() {
    local recent=$1

    if [ "$recent" -gt 0 ]; then
        echo -e "${GREEN}●${NC}" # Active
    else
        echo -e "${YELLOW}○${NC}" # Idle
    fi
}

# Function to display agent card
display_agent_card() {
    local name=$1
    local branch=$2
    local icon=$3

    IFS='|' read -r commits changes unstaged last_commit recent <<< "$(get_agent_progress "$branch")"

    local status=$(get_status_icon "$recent")

    echo -e "${BLUE}║${NC} $status ${BOLD}$icon $name${NC}"
    echo -e "${BLUE}║${NC}   Branch: ${CYAN}$branch${NC}"
    echo -e "${BLUE}║${NC}   Commits: ${GREEN}$commits${NC} | Files: ${YELLOW}$changes${NC} | Unstaged: ${RED}$unstaged${NC}"

    if [ "$recent" -gt 0 ]; then
        echo -e "${BLUE}║${NC}   ${GREEN}⚡ Active${NC} ($recent files modified recently)"
    else
        echo -e "${BLUE}║${NC}   ${YELLOW}⏸ Idle${NC}"
    fi

    if [ ${#last_commit} -gt 50 ]; then
        last_commit="${last_commit:0:47}..."
    fi
    echo -e "${BLUE}║${NC}   Last: $last_commit"
    echo -e "${BLUE}║${NC}"
}

# Function to show system info
show_system_info() {
    cd "$PROJECT_ROOT"

    # Current branch in main window
    MAIN_BRANCH=$(git branch --show-current)

    # Total branches
    TOTAL_BRANCHES=$(git branch | wc -l)

    # Git status
    if [[ -n $(git status -s) ]]; then
        GIT_STATUS="${YELLOW}⚠ Changes present${NC}"
    else
        GIT_STATUS="${GREEN}✓ Clean${NC}"
    fi

    echo -e "${BLUE}║${NC} ${BOLD}System Status${NC}"
    echo -e "${BLUE}║${NC}   Main branch: ${CYAN}$MAIN_BRANCH${NC}"
    echo -e "${BLUE}║${NC}   Total branches: $TOTAL_BRANCHES"
    echo -e "${BLUE}║${NC}   Status: $GIT_STATUS"
    echo -e "${BLUE}║${NC}"
}

# Main dashboard loop
while true; do
    clear

    # Header
    echo -e "${BOLD}${BLUE}"
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║        🤖  Performia Agent Orchestra Dashboard  🤖         ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""

    # Timestamp
    echo -e "${CYAN}⏰ $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo ""

    # System info
    draw_box "SYSTEM STATUS"
    show_system_info
    draw_box_end
    echo ""

    # Agent cards
    draw_box "ACTIVE AGENTS"
    display_agent_card "Frontend Agent" "feature/frontend-optimization" "🎨"
    display_agent_card "Audio Pipeline" "feature/audio-pipeline-optimization" "🎵"
    display_agent_card "Voice Control" "feature/voice-control-integration" "🎤"
    draw_box_end
    echo ""

    # Recent commits across all branches
    draw_box "RECENT ACTIVITY (Last 5 commits)"
    cd "$PROJECT_ROOT"
    git log --all --oneline -5 --decorate --color=always | while IFS= read -r line; do
        echo -e "${BLUE}║${NC} $line"
    done
    draw_box_end
    echo ""

    # Instructions
    echo -e "${YELLOW}Commands:${NC}"
    echo -e "  ${CYAN}./scripts/dev/orchestrate-agents.sh status${NC}  - Detailed status"
    echo -e "  ${CYAN}./scripts/dev/orchestrate-agents.sh merge <agent>${NC} - Merge agent work"
    echo -e "  ${CYAN}Ctrl+C${NC} - Exit dashboard"
    echo ""

    # Refresh countdown
    for i in {10..1}; do
        echo -ne "\r${YELLOW}Refreshing in $i seconds...${NC} "
        sleep 1
    done
    echo -ne "\r                                 \r"
done