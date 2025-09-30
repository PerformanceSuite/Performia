#!/usr/bin/env bash

# Automated agent progress watcher
# Reports to coordinator session every 30 seconds

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$PROJECT_ROOT/.claude/logs"
REPORT_FILE="$LOG_DIR/agent-report.txt"

# Colors
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

mkdir -p "$LOG_DIR"

# Function to check branch activity
check_branch() {
    local branch=$1
    cd "$PROJECT_ROOT"

    if ! git show-ref --verify --quiet "refs/heads/$branch" 2>/dev/null; then
        echo "NOTFOUND|0|0|0|Branch not found"
        return
    fi

    git checkout "$branch" 2>/dev/null >&2

    # Count commits since main
    local commits=$(git rev-list --count main..$branch 2>/dev/null || echo "0")

    # Count changed files
    local files=$(git diff --name-only main..$branch 2>/dev/null | wc -l | tr -d ' ')

    # Count unstaged changes
    local unstaged=$(git status -s 2>/dev/null | wc -l | tr -d ' ')

    # Get last commit time (if any)
    local last_commit_time=""
    if [ "$commits" -gt 0 ]; then
        last_commit_time=$(git log -1 --format="%ar" 2>/dev/null || echo "unknown")
    else
        last_commit_time="no commits"
    fi

    # Check recent file activity (last 5 minutes)
    local recent=$(find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.py" -o -name "*.md" -o -name "*.sh" \) \
                   -mmin -5 2>/dev/null | grep -v node_modules | grep -v .git | wc -l | tr -d ' ')

    echo "$commits|$files|$unstaged|$last_commit_time|$recent"
}

# Function to generate report
generate_report() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    {
        echo "════════════════════════════════════════════"
        echo "  Agent Progress Report"
        echo "  $timestamp"
        echo "════════════════════════════════════════════"
        echo ""

        # Check each agent
        local agents=("Frontend:feature/frontend-optimization:🎨"
                     "Audio Pipeline:feature/audio-pipeline-optimization:🎵"
                     "Voice Control:feature/voice-control-integration:🎤")

        for agent_info in "${agents[@]}"; do
            IFS=':' read -r name branch icon <<< "$agent_info"

            IFS='|' read -r commits files unstaged last_commit recent <<< "$(check_branch "$branch")"

            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "$icon $name"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "Branch: $branch"
            echo "Commits: $commits | Files Changed: $files | Unstaged: $unstaged"
            echo "Last Activity: $last_commit"

            if [ "$recent" -gt 0 ]; then
                echo "Status: ⚡ ACTIVE ($recent files modified in last 5 min)"
            else
                echo "Status: ⏸ Idle (no recent changes)"
            fi
            echo ""
        done

        # Show recent commits across all branches
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Recent Commits (All Branches)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        cd "$PROJECT_ROOT"
        git log --all --oneline --decorate -5 2>/dev/null || echo "No commits yet"
        echo ""

        echo "════════════════════════════════════════════"
        echo "Next update in 30 seconds..."
        echo "Press Ctrl+C to stop"
        echo "════════════════════════════════════════════"

    } > "$REPORT_FILE"
}

# Function to display colored report
display_report() {
    if [ -f "$REPORT_FILE" ]; then
        clear
        cat "$REPORT_FILE"
    fi
}

# Main watch loop
echo "Starting agent watcher..."
echo "Monitoring: frontend-optimization, audio-pipeline-optimization, voice-control-integration"
echo ""

ITERATION=0
while true; do
    ITERATION=$((ITERATION + 1))

    # Generate report
    generate_report

    # Display report
    display_report

    # Log to file with timestamp
    echo "$(date): Iteration $ITERATION - Report generated" >> "$LOG_DIR/watcher.log"

    # Wait 30 seconds
    sleep 30
done