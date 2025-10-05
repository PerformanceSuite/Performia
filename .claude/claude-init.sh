#!/bin/bash
# Claude Code Initialization Script
# Run this in any project root to set up .claude/ directory with smart cleanup

set -e

PROJECT_ROOT="$(pwd)"
CLAUDE_DIR="$PROJECT_ROOT/.claude"

echo "🤖 Initializing Claude Code directory in: $PROJECT_ROOT"

# Create .claude directory if it doesn't exist
mkdir -p "$CLAUDE_DIR"

# Create smart cleanup script
cat > "$CLAUDE_DIR/cleanup.sh" << 'EOF'
#!/bin/bash
# Smart Context-Aware Cleanup Script
# Reads .claude/CLAUDE.md to determine project type and cleanup needs

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="$PROJECT_ROOT/.claude"
CLAUDE_MD="$CLAUDE_DIR/CLAUDE.md"

# Silent operation - only show errors
exec 2>&1

echo "🧹 Running smart cleanup..."

# Always clean these universal temp files
find "$PROJECT_ROOT" -type f \( \
  -name ".DS_Store" \
  -o -name "*.tmp" \
  -o -name "*.swp" \
  -o -name "*~" \
  -o -name ".*.swp" \
\) -delete 2>/dev/null || true

# Detect project type and clean accordingly
if [ -f "$CLAUDE_MD" ]; then
  CONTENT=$(cat "$CLAUDE_MD")

  # Python project
  if echo "$CONTENT" | grep -qi "python\|\.py\|backend"; then
    echo "  → Python cleanup"
    find "$PROJECT_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "*.pyo" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
  fi

  # Node.js/Frontend project
  if echo "$CONTENT" | grep -qi "node\|npm\|frontend\|react\|vite"; then
    echo "  → Node.js cleanup"
    find "$PROJECT_ROOT" -type f -name "*.log" -not -path "*/node_modules/*" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -type d -name ".vite" -exec rm -rf {} + 2>/dev/null || true
    find "$PROJECT_ROOT" -type d -name "dist" -path "*/tmp/*" -exec rm -rf {} + 2>/dev/null || true
  fi

  # C++ project
  if echo "$CONTENT" | grep -qi "c++\|juce\|\.cpp"; then
    echo "  → C++ cleanup"
    find "$PROJECT_ROOT" -type f -name "*.o" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "*.obj" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -type d -name "build" -path "*/tmp/*" -exec rm -rf {} + 2>/dev/null || true
  fi

  # Audio project
  if echo "$CONTENT" | grep -qi "audio\|wav\|mp3\|song"; then
    echo "  → Audio temp cleanup"
    find "$PROJECT_ROOT" -type f -name "*.tmp.wav" -delete 2>/dev/null || true
    find "$PROJECT_ROOT" -type f -name "*.tmp.mp3" -delete 2>/dev/null || true
  fi
fi

# Update timestamps in memory.md and STATUS.md if they exist
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
if [ -f "$CLAUDE_DIR/memory.md" ]; then
  sed -i.bak "s/Last Updated:.*/Last Updated: $TIMESTAMP/" "$CLAUDE_DIR/memory.md" 2>/dev/null || true
  rm -f "$CLAUDE_DIR/memory.md.bak"
fi

if [ -f "$PROJECT_ROOT/docs/STATUS.md" ]; then
  sed -i.bak "s/Last Updated:.*/Last Updated: $TIMESTAMP/" "$PROJECT_ROOT/docs/STATUS.md" 2>/dev/null || true
  rm -f "$PROJECT_ROOT/docs/STATUS.md.bak"
fi

# Remove empty directories (except protected ones)
find "$PROJECT_ROOT" -type d -empty \
  -not -path "*/.git/*" \
  -not -path "*/node_modules/*" \
  -not -path "*/venv/*" \
  -not -path "*/__pycache__/*" \
  -delete 2>/dev/null || true

# Archive old markdown docs (>30 days) if docs/ exists
if [ -d "$PROJECT_ROOT/docs" ]; then
  mkdir -p "$PROJECT_ROOT/docs/archive"
  find "$PROJECT_ROOT/docs" -maxdepth 1 -type f -name "*.md" \
    ! -name "README.md" \
    ! -name "STATUS.md" \
    -mtime +30 \
    -exec mv {} "$PROJECT_ROOT/docs/archive/" \; 2>/dev/null || true
fi

echo "✅ Cleanup complete"
EOF

chmod +x "$CLAUDE_DIR/cleanup.sh"

# Create hooks.json
cat > "$CLAUDE_DIR/hooks.json" << 'EOF'
{
  "UserPromptSubmit": {
    "command": "./.claude/cleanup.sh",
    "description": "Automatic repository cleanup and organization",
    "matchers": ["/exit", "/quit", "exit", "quit"]
  }
}
EOF

# Create template CLAUDE.md if it doesn't exist
if [ ! -f "$CLAUDE_DIR/CLAUDE.md" ]; then
  cat > "$CLAUDE_DIR/CLAUDE.md" << 'EOF'
# Project Context

## Project Overview
[Describe your project here]

## Tech Stack
- [ ] Python
- [ ] Node.js/Frontend (React, Vite, etc.)
- [ ] C++
- [ ] Audio processing

## Architecture
[Describe your architecture]

## Key Files
[List important files and their purposes]

## Development Workflow
[Describe your workflow]

---
*Last Updated: $(date "+%Y-%m-%d")*
EOF
fi

# Create README.md to explain the setup
cat > "$CLAUDE_DIR/README.md" << 'EOF'
# Claude Code Configuration

This directory contains Claude Code configuration for this project.

## Files

- **`cleanup.sh`** - Smart cleanup script that runs on `/exit`
  - Context-aware: reads `CLAUDE.md` to detect project type
  - Cleans temp files, cache, build artifacts
  - Updates timestamps in memory.md and STATUS.md

- **`hooks.json`** - Hook configuration
  - Triggers cleanup on `/exit`, `/quit`, `exit`, `quit`

- **`CLAUDE.md`** - Project context for Claude Code
  - Update this with project details
  - Used by cleanup script to determine what to clean

## Usage

When you type `/exit` in Claude Code, the cleanup script runs automatically.

To manually run cleanup:
```bash
./.claude/cleanup.sh
```

## Customization

Edit `CLAUDE.md` to describe your project. The cleanup script will adapt based on keywords:
- Python → cleans `__pycache__`, `.pyc` files
- Node.js → cleans `.log`, `.vite` cache
- C++ → cleans `.o`, build artifacts
- Audio → cleans temporary audio files
EOF

echo ""
echo "✅ Claude Code initialization complete!"
echo ""
echo "📁 Created in $CLAUDE_DIR:"
echo "   - cleanup.sh (smart, context-aware)"
echo "   - hooks.json (triggers on /exit)"
echo "   - CLAUDE.md (edit with your project details)"
echo "   - README.md (documentation)"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .claude/CLAUDE.md with your project details"
echo "   2. The cleanup script will automatically adapt to your project"
echo "   3. Type /exit in Claude Code to trigger automatic cleanup"
echo ""
echo "💡 To use this in other projects:"
echo "   cp .claude/claude-init.sh /path/to/other/project/"
echo "   cd /path/to/other/project && ./claude-init.sh"
echo ""
