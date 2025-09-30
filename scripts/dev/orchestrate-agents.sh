#!/usr/bin/env bash

# Orchestrate multiple Claude Code agent sessions
# Usage: ./scripts/dev/orchestrate-agents.sh [start|stop|status]

set -e

# Require bash 4+ for associative arrays
if [ "${BASH_VERSINFO[0]}" -lt 4 ]; then
    echo "Error: This script requires bash 4.0 or later"
    echo "macOS default bash is 3.2. Install bash via Homebrew: brew install bash"
    exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/.claude/logs"
SESSION_LOG="$LOG_DIR/sessions.log"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Create log directory
mkdir -p "$LOG_DIR"

# Agent definitions
declare -A AGENTS=(
    ["frontend"]="feature/frontend-optimization"
    ["audio"]="feature/audio-pipeline-optimization"
    ["voice"]="feature/voice-control-integration"
)

# Function to start an agent session
start_agent() {
    local agent_name=$1
    local branch=$2
    local log_file="$LOG_DIR/${agent_name}-session.log"

    echo -e "${BLUE}Starting $agent_name agent on branch $branch${NC}"

    # Create branch if it doesn't exist
    cd "$PROJECT_ROOT"
    if ! git show-ref --verify --quiet "refs/heads/$branch"; then
        git checkout -b "$branch"
        echo "$(date): Created branch $branch" >> "$SESSION_LOG"
    fi

    # Log session start
    echo "$(date): Started $agent_name agent session on $branch" >> "$SESSION_LOG"
    echo -e "${GREEN}✓ $agent_name agent ready${NC}"
}

# Function to show status
show_status() {
    echo -e "${BLUE}=== Agent Session Status ===${NC}\n"

    cd "$PROJECT_ROOT"

    for agent in "${!AGENTS[@]}"; do
        branch="${AGENTS[$agent]}"

        if git show-ref --verify --quiet "refs/heads/$branch"; then
            echo -e "${GREEN}✓ $agent agent${NC}"
            echo -e "  Branch: $branch"

            # Check for commits
            COMMITS=$(git rev-list --count main..$branch 2>/dev/null || echo "0")
            echo -e "  Commits: $COMMITS"

            # Check for uncommitted changes
            git checkout "$branch" 2>/dev/null
            if [[ -n $(git status -s) ]]; then
                CHANGES=$(git status -s | wc -l)
                echo -e "  Uncommitted changes: ${YELLOW}$CHANGES files${NC}"
            else
                echo -e "  Uncommitted changes: ${GREEN}0${NC}"
            fi
            echo ""
        else
            echo -e "${YELLOW}○ $agent agent${NC}"
            echo -e "  Branch: $branch (not created)"
            echo ""
        fi
    done

    # Show recent activity
    echo -e "${BLUE}=== Recent Activity ===${NC}"
    if [ -f "$SESSION_LOG" ]; then
        tail -10 "$SESSION_LOG"
    else
        echo "No activity logged yet"
    fi
}

# Function to initialize all agents
start_all() {
    echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   Starting Performia Agent Orchestra     ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}\n"

    cd "$PROJECT_ROOT"

    # Ensure we're on main
    git checkout main 2>/dev/null || git checkout master 2>/dev/null

    # Start each agent
    for agent in "${!AGENTS[@]}"; do
        start_agent "$agent" "${AGENTS[$agent]}"
    done

    echo ""
    echo -e "${GREEN}✓ All agents initialized${NC}\n"
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "1. Open 3 terminal windows"
    echo -e "2. In each terminal, run: ${BLUE}cd $PROJECT_ROOT && git checkout <branch> && claude${NC}"
    echo -e "3. Start monitoring: ${BLUE}./scripts/dev/monitor-sessions.sh${NC}"
    echo ""
    echo -e "${BLUE}Branches:${NC}"
    for agent in "${!AGENTS[@]}"; do
        echo -e "  $agent: ${GREEN}${AGENTS[$agent]}${NC}"
    done
}

# Function to merge agent work
merge_agent() {
    local agent_name=$1
    local branch="${AGENTS[$agent_name]}"

    if [ -z "$branch" ]; then
        echo -e "${RED}Unknown agent: $agent_name${NC}"
        exit 1
    fi

    cd "$PROJECT_ROOT"

    echo -e "${BLUE}Merging $agent_name agent work from $branch${NC}"

    # Switch to main
    git checkout main

    # Merge
    if git merge --no-ff "$branch" -m "feat: merge $agent_name agent work from $branch"; then
        echo -e "${GREEN}✓ Successfully merged $agent_name agent work${NC}"
        echo "$(date): Merged $agent_name from $branch" >> "$SESSION_LOG"
    else
        echo -e "${RED}✗ Merge conflicts detected${NC}"
        echo -e "${YELLOW}Resolve conflicts and run: git merge --continue${NC}"
    fi
}

# Function to stop all agents
stop_all() {
    echo -e "${YELLOW}Stopping all agent sessions...${NC}"
    echo "$(date): Stopped all agent sessions" >> "$SESSION_LOG"
    echo -e "${GREEN}✓ Agents stopped${NC}"
    echo -e "\n${YELLOW}Note: Close your terminal windows manually${NC}"
}

# Main command handler
case "${1:-status}" in
    start)
        start_all
        ;;
    stop)
        stop_all
        ;;
    status)
        show_status
        ;;
    merge)
        if [ -z "$2" ]; then
            echo -e "${RED}Usage: $0 merge <agent-name>${NC}"
            echo -e "Available agents: ${!AGENTS[@]}"
            exit 1
        fi
        merge_agent "$2"
        ;;
    *)
        echo "Usage: $0 {start|stop|status|merge <agent>}"
        exit 1
        ;;
esac