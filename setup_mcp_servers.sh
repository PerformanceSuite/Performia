#!/bin/bash

# MCP Server Setup Script for Agentic Engineering
# This script installs essential MCP servers for your workflow

echo "🚀 Setting up MCP servers for Agentic Engineering..."

# Create MCP servers directory if it doesn't exist
mkdir -p ~/.config/mcp-servers

# Install core MCP servers using npm
echo "📦 Installing essential MCP servers..."

# GitHub MCP server for code management
npm install -g @modelcontextprotocol/server-github

# Filesystem MCP server for file operations
npm install -g @modelcontextprotocol/server-filesystem

# Memory MCP server for persistent memory
npm install -g @modelcontextprotocol/server-memory

# PostgreSQL MCP server for database operations
npm install -g @modelcontextprotocol/server-postgres

# Slack MCP server for communications
npm install -g @modelcontextprotocol/server-slack

# Playwright MCP server for web automation
npm install -g @modelcontextprotocol/server-playwright

# Create MCP configuration file
cat > ~/.config/mcp-servers/config.json << 'EOF'
{
  "servers": {
    "github": {
      "command": "mcp-server-github",
      "args": [],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["--allowed-dir", "/Users/danielconnolly/Projects"]
    },
    "memory": {
      "command": "mcp-server-memory",
      "args": ["--memory-dir", "/Users/danielconnolly/.mcp-memory"]
    },
    "postgres": {
      "command": "mcp-server-postgres",
      "args": [],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "slack": {
      "command": "mcp-server-slack",
      "args": [],
      "env": {
        "SLACK_TOKEN": "${SLACK_TOKEN}"
      }
    },
    "playwright": {
      "command": "mcp-server-playwright",
      "args": ["--headless", "false"]
    }
  }
}
EOF

echo "✅ MCP servers configuration created at ~/.config/mcp-servers/config.json"

# Configure for Goose
echo "🦆 Configuring Goose..."
cat > ~/.config/goose/config.yaml << 'EOF'
server:
  mcp:
    enabled: true
    servers:
      - github
      - filesystem
      - memory
      - postgres
      - slack
      - playwright

extensions:
  developer:
    enabled: true
  mcpgateway:
    enabled: true
    bundled: false
    description: 'MCP gateway for all servers'

models:
  default: claude-3-5-sonnet-20241022
  providers:
    anthropic:
      api_key: ${ANTHROPIC_API_KEY}
EOF

echo "✅ Goose configuration updated"

# Configure for Windsurf/Cursor
echo "🌊 Setting up Windsurf/Cursor MCP integration..."
cat > ~/.cursor/mcp-config.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "enabled": true,
      "provider": "mcp-server-github"
    },
    "filesystem": {
      "enabled": true,
      "provider": "mcp-server-filesystem"
    },
    "memory": {
      "enabled": true,
      "provider": "mcp-server-memory"
    }
  }
}
EOF

echo "✅ Windsurf/Cursor MCP configuration created"

echo "
🎉 MCP Server setup complete!

Next steps:
1. Set your environment variables:
   export GITHUB_TOKEN='your-github-token'
   export DATABASE_URL='postgresql://user:pass@localhost/performia'
   export SLACK_TOKEN='your-slack-token'
   export ANTHROPIC_API_KEY='your-anthropic-key'

2. Add these to your ~/.zshrc or ~/.bashrc for persistence

3. Restart your terminals and development tools

4. Test the setup:
   goose --list-servers
"
