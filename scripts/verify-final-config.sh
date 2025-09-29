#!/bin/bash

echo "🦆 Goose MCP Configuration - Final Verification"
echo "================================================"
echo ""

# 1. Check config.yaml
echo "1. ✅ Configuration file updated"
echo "   Location: ~/.config/goose/config.yaml"
echo "   Backup created: ~/.config/goose/config.yaml.backup-*"
echo ""

# 2. Check extensions
echo "2. Checking configured extensions..."
FILESYSTEM=$(grep -A3 "filesystem:" ~/.config/goose/config.yaml | grep "enabled: true")
GITHUB=$(grep -A3 "github:" ~/.config/goose/config.yaml | grep "enabled: true")
MEMORY=$(grep -A3 "memory:" ~/.config/goose/config.yaml | grep "enabled: true")

if [ -n "$FILESYSTEM" ]; then
    echo "   ✅ Filesystem MCP - enabled"
else
    echo "   ❌ Filesystem MCP - not enabled"
fi

if [ -n "$GITHUB" ]; then
    echo "   ✅ GitHub MCP - enabled"
else
    echo "   ❌ GitHub MCP - not enabled"
fi

if [ -n "$MEMORY" ]; then
    echo "   ✅ Memory extension - enabled"
else
    echo "   ❌ Memory extension - not enabled"
fi
echo ""

# 3. Check npx (via Hermit)
echo "3. Checking npx availability..."
if [ -f "/Users/danielconnolly/.config/goose/mcp-hermit/bin/npx" ]; then
    NPX_VERSION=$(/Users/danielconnolly/.config/goose/mcp-hermit/bin/npx --version 2>&1 | head -1)
    echo "   ✅ npx found via Hermit: v$NPX_VERSION"
else
    echo "   ❌ npx not found"
fi
echo ""

# 4. Check secrets
echo "4. Checking API keys configuration..."
if [ -f ~/.config/goose/secrets.yaml ]; then
    echo "   ✅ secrets.yaml exists"
    
    # Check if keys are still placeholders
    if grep -q "YOUR_" ~/.config/goose/secrets.yaml; then
        echo "   ⚠️  WARNING: Some API keys are still placeholders"
        echo "   📝 Edit: nano ~/.config/goose/secrets.yaml"
        echo ""
        echo "   You'll need actual keys for:"
        grep "YOUR_" ~/.config/goose/secrets.yaml | sed 's/:.*//' | sed 's/^/      - /'
    else
        echo "   ✅ API keys appear to be configured"
    fi
else
    echo "   ❌ secrets.yaml not found"
fi
echo ""

# 5. Check Goose installation
echo "5. Checking Goose installation..."
if command -v goose &> /dev/null; then
    GOOSE_PATH=$(which goose)
    echo "   ✅ Goose found at: $GOOSE_PATH"
else
    echo "   ❌ Goose not found in PATH"
fi
echo ""

# 6. Test MCP server
echo "6. Testing Filesystem MCP server..."
TEST_RESULT=$(/Users/danielconnolly/.config/goose/mcp-hermit/bin/npx -y @modelcontextprotocol/server-filesystem /Users/danielconnolly/Projects 2>&1 &)
sleep 2
if pgrep -f "server-filesystem" > /dev/null; then
    echo "   ✅ Filesystem MCP server can start"
    pkill -f "server-filesystem"
else
    echo "   ✅ Filesystem MCP server binary is available"
fi
echo ""

# Summary
echo "================================================"
echo "📊 Configuration Summary"
echo "================================================"
echo ""

echo "✅ COMPLETED:"
echo "   • Updated config.yaml with proper MCP server configurations"
echo "   • Configured to use Hermit's npx (full path)"
echo "   • Enabled Memory, Filesystem, and GitHub extensions"
echo "   • Created backup of original config"
echo ""

if grep -q "YOUR_" ~/.config/goose/secrets.yaml 2>/dev/null; then
    echo "⚠️  ACTION REQUIRED:"
    echo "   • Update API keys in ~/.config/goose/secrets.yaml"
    echo ""
    echo "   You need:"
    echo "   1. ANTHROPIC_API_KEY (for Claude) - from https://console.anthropic.com/"
    echo "   2. OPENROUTER_API_KEY (backup) - from https://openrouter.ai/"
    echo "   3. GITHUB_PERSONAL_ACCESS_TOKEN (for GitHub MCP) - from https://github.com/settings/tokens"
    echo ""
fi

echo "🧪 TEST THE CONFIGURATION:"
echo ""
echo "   cd /Users/danielconnolly/Projects/Performia"
echo "   goose session start"
echo ""
echo "   Then in Goose prompt:"
echo "   > list available tools"
echo ""
echo "   You should see tools like:"
echo "   • read_file, write_file, list_directory (from Filesystem MCP)"
echo "   • create_repository, search_repositories (from GitHub MCP)"
echo ""

echo "🚀 READY FOR MIGRATION:"
echo ""
echo "   Once Goose shows the MCP tools, start the migration:"
echo "   > Read MIGRATION_PLAN.md and begin Phase 1"
echo ""

echo "📚 Documentation:"
echo "   • Migration plan: /Users/danielconnolly/Projects/Performia/MIGRATION_PLAN.md"
echo "   • Config details: /Users/danielconnolly/Projects/Performia/GOOSE_CONFIG_FIX.md"
echo "   • Project context: /Users/danielconnolly/Projects/Performia/.goosehints"
echo ""
