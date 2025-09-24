#!/bin/bash

# Performia Session Manager
# Manages DevAssist sessions with warm-up and checkpoints

PROJECT_DIR="/Users/danielconnolly/Projects/Performia"
SESSION_DIR="$PROJECT_DIR/.sessions"
DEVASSIST_DIR="$PROJECT_DIR/.devassist"

case "$1" in
  start)
    echo "🎵 Starting Performia development session..."
    SESSION_ID="session_$(date +%s)"
    echo "$SESSION_ID" > "$DEVASSIST_DIR/current_session"
    
    # Create session file
    cat > "$SESSION_DIR/$SESSION_ID.json" << JSON
{
  "id": "$SESSION_ID",
  "project": "Performia",
  "started_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "context": {
    "focus": "music performance analytics",
    "current_sprint": "audio pipeline implementation",
    "active_agents": ["music-analyst", "audio-pipeline", "ml-specialist"]
  }
}
JSON
    
    echo "✅ Session started: $SESSION_ID"
    echo "🔥 Warm-up enabled for optimal performance"
    ;;
    
  checkpoint)
    echo "💾 Creating checkpoint..."
    SESSION_ID=$(cat "$DEVASSIST_DIR/current_session" 2>/dev/null)
    if [ -z "$SESSION_ID" ]; then
      echo "❌ No active session"
      exit 1
    fi
    
    CHECKPOINT_ID="checkpoint_$(date +%s)"
    sqlite3 "$DEVASSIST_DIR/data/sqlite/Performia.db" \
      "UPDATE sessions SET checkpoints = checkpoints || ',$CHECKPOINT_ID' WHERE id = '$SESSION_ID';"
    
    echo "✅ Checkpoint saved: $CHECKPOINT_ID"
    ;;
    
  end)
    echo "📋 Ending session..."
    SESSION_ID=$(cat "$DEVASSIST_DIR/current_session" 2>/dev/null)
    if [ -z "$SESSION_ID" ]; then
      echo "❌ No active session"
      exit 1
    fi
    
    # Update session end time
    sqlite3 "$DEVASSIST_DIR/data/sqlite/Performia.db" \
      "UPDATE sessions SET ended_at = CURRENT_TIMESTAMP WHERE id = '$SESSION_ID';"
    
    rm -f "$DEVASSIST_DIR/current_session"
    echo "✅ Session ended: $SESSION_ID"
    ;;
    
  status)
    SESSION_ID=$(cat "$DEVASSIST_DIR/current_session" 2>/dev/null)
    if [ -z "$SESSION_ID" ]; then
      echo "❌ No active session"
    else
      echo "✅ Active session: $SESSION_ID"
      echo "📊 Progress:"
      sqlite3 "$DEVASSIST_DIR/data/sqlite/Performia.db" \
        "SELECT milestone, status FROM progress WHERE project_name = 'Performia';"
    fi
    ;;
    
  *)
    echo "Usage: $0 {start|checkpoint|end|status}"
    exit 1
    ;;
esac
