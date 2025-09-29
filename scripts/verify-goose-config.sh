#!/bin/bash

echo "🦆 Goose MCP Configuration Verification"
echo "========================================"
echo ""

# Check Goose installation
echo "1. Checking Goose installation..."
if command -v goose &> /dev/null; then
    echo "   ✅ Goose is installed: $(which goose)"
    goose --version 2>/dev/null || echo "   Version: unknown"
else
    echo "   ❌ Goose is not installed"
    exit 1
fi
echo ""

# Check config files
echo "2. Checking configuration files..."
if [ -f ~/.config/goose/config.yaml ]; then
    echo "   ✅ config.yaml exists"
else
    echo "   ❌ config.yaml not found"
fi

if [ -f ~/.config/goose/config-properly-configured.yaml ]; then
    echo "   ✅ config-properly-configured.yaml exists (backup)"
fi

if [ -f ~/.config/goose/secrets.yaml ]; then
    echo "   ✅ secrets.yaml exists"
else
    echo "   ⚠️  secrets.yaml not found (API keys may not be configured)"
fi
echo ""

# Check for API keys
echo "3. Checking for API keys in secrets.yaml..."
if [ -f ~/.config/goose/secrets.yaml ]; then
    if grep -q "ANTHROPIC_API_KEY" ~/.config/goose/secrets.yaml; then
        echo "   ✅ ANTHROPIC_API_KEY found"
    else
        echo "   ❌ ANTHROPIC_API_KEY not found"
    fi
    
    if grep -q "OPENROUTER_API_KEY" ~/.config/goose/secrets.yaml; then
        echo "   ✅ OPENROUTER_API_KEY found"
    else
        echo "   ⚠️  OPENROUTER_API_KEY not found"
    fi
    
    if grep -q "GITHUB_PERSONAL_ACCESS_TOKEN" ~/.config/goose/secrets.yaml; then
        echo "   ✅ GITHUB_PERSONAL_ACCESS_TOKEN found"
    else
        echo "   ⚠️  GITHUB_PERSONAL_ACCESS_TOKEN not found"
    fi
fi
echo ""

# Check current config
echo "4. Current configuration analysis..."
echo "   Extensions enabled in config.yaml:"
grep "enabled: true" ~/.config/goose/config.yaml | grep -v "#" | while read line; do
    echo "      • $line"
done
echo ""

# Check for MCP servers in config
echo "5. MCP Server configuration..."
if grep -q "type: commandline" ~/.config/goose/config.yaml; then
    echo "   ✅ Command-line MCP servers configured"
    echo "   Servers found:"
    grep -A2 "type: commandline" ~/.config/goose/config.yaml | grep "name:" | sed 's/.*name: /      • /'
else
    echo "   ❌ No command-line MCP servers configured"
    echo "   ⚠️  Your MCP servers are listed but not properly configured as extensions"
    echo ""
    echo "   📝 To fix this:"
    echo "      Option 1: Use the new config file:"
    echo "         cp ~/.config/goose/config.yaml ~/.config/goose/config.yaml.backup"
    echo "         cp ~/.config/goose/config-properly-configured.yaml ~/.config/goose/config.yaml"
    echo ""
    echo "      Option 2: Run goose configure and add extensions manually"
fi
echo ""

# Check node/npx for MCP servers
echo "6. Checking dependencies for MCP servers..."
if command -v npx &> /dev/null; then
    echo "   ✅ npx is available (needed for MCP servers)"
else
    echo "   ❌ npx not found - MCP servers won't work"
    echo "      Install Node.js to fix this"
fi
echo ""

echo "========================================"
echo "🎯 Recommended Actions:"
echo ""

if ! grep -q "type: commandline" ~/.config/goose/config.yaml; then
    echo "1. 🔧 Update config to properly configure MCP servers:"
    echo "   cp ~/.config/goose/config-properly-configured.yaml ~/.config/goose/config.yaml"
    echo ""
fi

if ! grep -q "GITHUB_PERSONAL_ACCESS_TOKEN" ~/.config/goose/secrets.yaml 2>/dev/null; then
    echo "2. 🔑 Add GitHub token to secrets.yaml:"
    echo "   echo 'GITHUB_PERSONAL_ACCESS_TOKEN: your_token_here' >> ~/.config/goose/secrets.yaml"
    echo ""
fi

echo "3. 🧪 Test the configuration:"
echo "   goose session start"
echo "   Then in Goose prompt type: list available tools"
echo ""

echo "4. 📖 View the migration plan:"
echo "   cd /Users/danielconnolly/Projects/Performia"
echo "   cat MIGRATION_PLAN.md"
echo ""
