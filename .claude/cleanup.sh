#!/bin/bash
# Performia Auto-Cleanup - Runs automatically on session end
# No prompts, no interaction, just clean

set -e

# Silent mode - no output unless errors
SILENT=true

log() {
    if [ "$SILENT" != "true" ]; then
        echo "$1"
    fi
}

# 1. Remove temporary files
log "Cleaning temporary files..."
find . -type f \( \
    -name "*.tmp" \
    -o -name "*.log" \
    -o -name ".DS_Store" \
    -o -name "*.pyc" \
    -o -name "*.pyo" \
    -o -name "*~" \
    -o -name "*.swp" \
    -o -name "*.swo" \
    -o -name "*.orig" \
    \) \
    -not -path "./node_modules/*" \
    -not -path "./.git/*" \
    -not -path "./backend/venv/*" \
    -not -path "./tools/knowledge-base/venv/*" \
    -not -path "./frontend/node_modules/*" \
    -delete 2>/dev/null || true

# 2. Remove Python cache directories
log "Cleaning Python cache..."
find . -type d -name "__pycache__" \
    -not -path "./backend/venv/*" \
    -not -path "./tools/knowledge-base/venv/*" \
    -exec rm -rf {} + 2>/dev/null || true

# 3. Update .gitignore timestamp
log "Updating timestamps..."
DATE=$(date +"%B %d, %Y")

# Update memory.md timestamp
if [ -f ".claude/memory.md" ]; then
    if grep -q "Last Updated" .claude/memory.md; then
        sed -i.bak "s/\*Last Updated\*:.*/\*Last Updated\*: $DATE/" .claude/memory.md 2>/dev/null || \
        sed -i '' "s/\*Last Updated\*:.*/\*Last Updated\*: $DATE/" .claude/memory.md 2>/dev/null || true
        rm .claude/memory.md.bak 2>/dev/null || true
    fi
fi

# Update STATUS.md timestamp
if [ -f "docs/STATUS.md" ]; then
    if grep -q "Last Updated" docs/STATUS.md; then
        sed -i.bak "s/\*\*Last Updated\*\*:.*/\*\*Last Updated:\*\* $DATE/" docs/STATUS.md 2>/dev/null || \
        sed -i '' "s/\*\*Last Updated\*\*:.*/\*\*Last Updated:\*\* $DATE/" docs/STATUS.md 2>/dev/null || true
        rm docs/STATUS.md.bak 2>/dev/null || true
    fi
fi

# 4. Clean empty directories (except protected ones)
log "Removing empty directories..."
find . -type d -empty \
    -not -path "./.git/*" \
    -not -path "./node_modules/*" \
    -not -path "./backend/venv/*" \
    -not -path "./tools/knowledge-base/venv/*" \
    -not -path "./.claude/logs/*" \
    -delete 2>/dev/null || true

# 5. Organize docs (move old files to archive)
log "Organizing documentation..."
DATE_CUTOFF=$(date -v-30d +%Y-%m-%d 2>/dev/null || date -d '30 days ago' +%Y-%m-%d 2>/dev/null || echo "2024-09-01")

# Archive old markdown files in root (except important ones)
if [ -d "docs/archive" ]; then
    for file in *.md; do
        if [ -f "$file" ] && [ "$file" != "README.md" ] && [ "$file" != "PERFORMIA_MASTER_DOCS.md" ]; then
            # Check if file is older than 30 days
            if [ "$(stat -f %Sm -t %Y-%m-%d "$file" 2>/dev/null || stat -c %y "$file" 2>/dev/null | cut -d' ' -f1)" \< "$DATE_CUTOFF" ]; then
                mv "$file" "docs/archive/" 2>/dev/null || true
            fi
        fi
    done
fi

log "Cleanup complete"
exit 0
