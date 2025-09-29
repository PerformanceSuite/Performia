#!/bin/bash

# Setup Goose MCP Servers for Performia Migration
# This script properly configures all needed MCP servers

echo "🦆 Setting up Goose MCP Servers..."
echo ""

# Check if goose is installed
if ! command -v goose &> /dev/null; then
    echo "❌ Goose is not installed. Please install it first:"
    echo "   pip install goose-ai"
    exit 1
fi

echo "✅ Goose is installed"
echo ""

# Backup current config
echo "📦 Backing up current Goose config..."
cp ~/.config/goose/config.yaml ~/.config/goose/config.yaml.backup-$(date +%s)

echo "🔧 Setting up MCP Servers..."
echo ""
echo "We'll add the following MCP servers:"
echo "  1. Filesystem - for file operations"
echo "  2. GitHub - for repository management"  
echo "  3. Memory - for persistent context"
echo ""

# The proper way to add MCP servers is through goose configure
# But we can also manually edit the config if needed

echo "📝 Creating proper MCP server configurations..."
echo ""

# Create a temporary configuration script
cat > /tmp/setup_mcp_servers.md << 'EOCONF'
# MCP Server Configuration Guide

To properly configure MCP servers in Goose, use the interactive configure command:

```bash
goose configure
```

Then select "Add Extension" and choose "Command-line Extension" for each server:

## 1. Filesystem MCP Server

- Extension name: `filesystem`
- Command: `npx`
- Args: `-y @modelcontextprotocol/server-filesystem /Users/danielconnolly/Projects`

This gives Goose access to your Projects directory.

## 2. GitHub MCP Server  

- Extension name: `github`
- Command: `npx`
- Args: `-y @modelcontextprotocol/server-github`
- Environment Variables:
  - GITHUB_PERSONAL_ACCESS_TOKEN: (from your .env or secrets.yaml)

## 3. Memory MCP Server (Built-in)

Memory is a built-in extension, just enable it in config.yaml:

```yaml
extensions:
  memory:
    enabled: true
```

## Verification

After adding servers, verify they're working:

```bash
goose session start
# In the Goose prompt:
list available tools
```

You should see tools from each MCP server.

EOCONF

cat /tmp/setup_mcp_servers.md

echo ""
echo "🎯 Next Steps:"
echo ""
echo "1. Run: goose configure"
echo "2. Select 'Add Extension' → 'Command-line Extension'"
echo "3. Add each MCP server following the guide above"
echo "4. Or run the automatic setup below..."
echo ""
echo "Would you like me to attempt automatic configuration? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "🤖 Attempting automatic MCP server setup..."
    
    # Create a new config with proper MCP server definitions
    cat > ~/.config/goose/config-with-mcp.yaml << 'ENDCONFIG'
extensions:
  computercontroller:
    enabled: true
    type: builtin
    name: computercontroller
  developer:
    enabled: true
    type: builtin
    name: developer
  memory:
    enabled: true
    type: builtin
    name: memory
  filesystem:
    enabled: true
    type: commandline
    name: filesystem
    display_name: Filesystem
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-filesystem"
      - "/Users/danielconnolly/Projects"
  github:
    enabled: true
    type: commandline
    name: github
    display_name: GitHub
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-github"
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: ${GITHUB_PERSONAL_ACCESS_TOKEN}

GOOSE_PROVIDER: openrouter
GOOSE_MODEL: anthropic/claude-sonnet-4

models:
  default: claude-3-5-sonnet-20241022
  providers:
    anthropic:
      api_key: ${ANTHROPIC_API_KEY}
    openrouter:
      api_key: ${OPENROUTER_API_KEY}
ENDCONFIG

    echo "✅ Created config-with-mcp.yaml"
    echo ""
    echo "To activate this configuration:"
    echo "  mv ~/.config/goose/config.yaml ~/.config/goose/config.yaml.old"
    echo "  mv ~/.config/goose/config-with-mcp.yaml ~/.config/goose/config.yaml"
    echo ""
    echo "Or manually run: goose configure"
else
    echo "👍 Run 'goose configure' manually when ready"
fi

echo ""
echo "📚 Configuration guide saved to: /tmp/setup_mcp_servers.md"
echo "🦆 Setup script complete!"
