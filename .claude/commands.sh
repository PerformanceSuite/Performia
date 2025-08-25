#!/bin/bash

# Claude Code Session Management Commands
# This script provides /start and /end commands for project sessions

PROJECT_ROOT="/Users/danielconnolly/Projects/Performia"
SESSION_FILE="$PROJECT_ROOT/.claude/session.json"
CLAUDE_DIR="$PROJECT_ROOT/.claude"

# Create .claude directory if it doesn't exist
mkdir -p "$CLAUDE_DIR"

# Function to start a new session
start_session() {
    local session_name="${1:-default}"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Create or update session file
    cat > "$SESSION_FILE" <<EOF
{
    "name": "$session_name",
    "started_at": "$timestamp",
    "status": "active",
    "project": "Performia",
    "working_directory": "$PROJECT_ROOT"
}
EOF
    
    echo "✅ Session '$session_name' started at $timestamp"
    echo "📁 Working directory: $PROJECT_ROOT"
    echo ""
    echo "Session context saved to: $SESSION_FILE"
}

# Function to end the current session
end_session() {
    if [ ! -f "$SESSION_FILE" ]; then
        echo "❌ No active session found"
        return 1
    fi
    
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local session_name=$(grep '"name"' "$SESSION_FILE" | cut -d'"' -f4)
    local start_time=$(grep '"started_at"' "$SESSION_FILE" | cut -d'"' -f4)
    
    # Archive the session
    local archive_dir="$CLAUDE_DIR/archives"
    mkdir -p "$archive_dir"
    local archive_file="$archive_dir/session_$(date +%Y%m%d_%H%M%S).json"
    
    # Update session file with end time
    cp "$SESSION_FILE" "$archive_file"
    
    # Add end time to archive
    sed -i '' "s/\"status\": \"active\"/\"status\": \"completed\"/g" "$archive_file"
    sed -i '' "s/}$/,\n    \"ended_at\": \"$timestamp\"\n}/" "$archive_file"
    
    # Remove active session file
    rm "$SESSION_FILE"
    
    echo "✅ Session '$session_name' ended at $timestamp"
    echo "📁 Session archived to: $archive_file"
    echo ""
    echo "Session started: $start_time"
    echo "Session ended:   $timestamp"
}

# Function to check session status
session_status() {
    if [ -f "$SESSION_FILE" ]; then
        echo "📊 Active Session Status:"
        echo "========================"
        cat "$SESSION_FILE" | python3 -m json.tool
    else
        echo "❌ No active session"
        echo ""
        echo "Use '/start [session-name]' to begin a new session"
    fi
}

# Main command handler
case "$1" in
    start)
        start_session "$2"
        ;;
    end)
        end_session
        ;;
    status)
        session_status
        ;;
    *)
        echo "Performia Session Management"
        echo "============================"
        echo ""
        echo "Usage:"
        echo "  /start [session-name]  - Start a new work session"
        echo "  /end                   - End the current session"  
        echo "  /status                - Check current session status"
        echo ""
        echo "Examples:"
        echo "  /start feature-xyz    - Start session named 'feature-xyz'"
        echo "  /start                - Start default session"
        echo "  /end                  - End current session and archive it"
        echo "  /status               - View current session details"
        ;;
esac