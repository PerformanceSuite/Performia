#!/bin/bash

# Quick Goose MCP Setup for Performia
# This script backs up your current config and installs the properly configured version

set -e  # Exit on error

echo "🦆 Quick Goose MCP Setup"
echo "======================="
echo ""

# Create backup
BACKUP_FILE=~/.config/goose/config.yaml.backup-$(date +%Y%m%d-%H%M%S)
echo "📦 Creating backup: $BACKUP_FILE"
cp ~/.config/goose/config.yaml "$BACKUP_FILE"
echo "   ✅ Backup created"
echo ""

# Install new config
echo "🔧 Installing properly configured MCP setup..."
cp ~/.config/goose/config-properly-configured.yaml ~/.config/goose/config.yaml
echo "   ✅ Configuration updated"
echo ""

# Check secrets
echo "🔑 Checking API keys..."
if [ ! -f ~/.config/goose/secrets.yaml ]; then
    echo "   ⚠️  secrets.yaml not found, creating template..."
    cat > ~/.config/goose/secrets.yaml << 'EOSECRETS'
# Goose API Keys
# Fill in your actual keys below

ANTHROPIC_API_KEY: sk-ant-your-key-here
OPENROUTER_API_KEY: sk-or-your-key-here
GITHUB_PERSONAL_ACCESS_TOKEN: github_pat_your-token-here
EOSECRETS
    echo "   📝 Created secrets.yaml template"
    echo "   ⚠️  Please edit ~/.config/goose/secrets.yaml with your actual API keys"
else
    echo "   ✅ secrets.yaml exists"
fi
echo ""

# Verify NPX
echo "🔍 Verifying dependencies..."
if command -v npx &> /dev/null; then
    echo "   ✅ npx is available"
else
    echo "   ❌ npx not found - MCP servers require Node.js"
    echo "   Install Node.js: https://nodejs.org/"
    exit 1
fi
echo ""

# Test configuration
echo "🧪 Testing Goose configuration..."
if goose --version &> /dev/null; then
    echo "   ✅ Goose is working"
else
    echo "   ⚠️  Goose may have issues, check installation"
fi
echo ""

echo "✨ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Edit your API keys (if needed):"
echo "   nano ~/.config/goose/secrets.yaml"
echo ""
echo "2. Start a Goose session to test:"
echo "   cd /Users/danielconnolly/Projects/Performia"
echo "   goose session start"
echo ""
echo "3. In Goose, test MCP servers with:"
echo "   list available tools"
echo ""
echo "4. Begin the migration:"
echo "   Read MIGRATION_PLAN.md and execute Phase 1"
echo ""
echo "💾 Your old config is backed up at:"
echo "   $BACKUP_FILE"
echo ""
