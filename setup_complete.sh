#!/bin/bash

# Performia Complete Setup Script
# Sets up voice control, MCP servers, and multi-agent orchestration

echo "
╔══════════════════════════════════════════════════════════════╗
║           PERFORMIA AGENTIC ENGINEERING SETUP               ║
║                                                              ║
║  Setting up:                                                 ║
║  1. Voice Control (Wispr Flow / Super Whisper)              ║
║  2. MCP Servers (GitHub, Filesystem, Memory, etc.)          ║
║  3. Custom Performia Agent                                  ║
║  4. Multi-Agent Orchestrator (24/7 operation)               ║
╚══════════════════════════════════════════════════════════════╝
"

# Step 1: Check prerequisites
echo "📋 Checking prerequisites..."

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first."
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3 first."
    exit 1
fi

echo "✅ Prerequisites satisfied"

# Step 2: Install MCP servers
echo "
📦 Installing MCP servers..."
chmod +x setup_mcp_servers.sh
./setup_mcp_servers.sh

# Step 3: Install Python dependencies
echo "
🐍 Installing Python dependencies..."
pip3 install -r requirements.txt

# Step 4: Initialize the database
echo "
💾 Initializing Performia database..."
python3 -c "from performia_agent import init_db; init_db()"

# Step 5: Create launch scripts
echo "
🚀 Creating launch scripts..."

# Create agent launcher
cat > launch_agent.sh << 'EOF'
#!/bin/bash
echo "Starting Performia Agent..."
python3 performia_agent.py
EOF
chmod +x launch_agent.sh

# Create orchestrator launcher
cat > launch_orchestrator.sh << 'EOF'
#!/bin/bash
echo "Starting Multi-Agent Orchestrator (24/7 mode)..."
python3 orchestrator.py
EOF
chmod +x launch_orchestrator.sh

# Create voice launcher
cat > setup_voice.sh << 'EOF'
#!/bin/bash
echo "Setting up voice control..."

# For Mac users
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "
    For Mac users:
    1. Download Super Whisper: https://superwhisper.com
    2. Set hotkey to Cmd+Shift+Space
    3. Enable 'Smart silence detection'
    4. Test with: 'Create a performance review for John Smith'
    "
    open https://superwhisper.com
else
    echo "
    For all platforms:
    1. Download Wispr Flow: https://wisprflow.ai
    2. It works with Cursor, Windsurf, and terminal
    3. Free tier available
    4. Press hotkey and start speaking your commands
    "
    open https://wisprflow.ai
fi
EOF
chmod +x setup_voice.sh

# Step 6: Create .env template
echo "
🔐 Creating environment template..."
cat > .env.template << 'EOF'
# GitHub Integration
GITHUB_TOKEN=your-github-personal-access-token

# Database
DATABASE_URL=postgresql://user:password@localhost/performia

# Slack Integration (optional)
SLACK_TOKEN=your-slack-bot-token

# AI Models
ANTHROPIC_API_KEY=your-anthropic-api-key
OPENAI_API_KEY=your-openai-api-key

# MCP Memory Storage
MCP_MEMORY_DIR=/Users/danielconnolly/.mcp-memory
EOF

# Step 7: Create README
cat > README.md << 'EOF'
# Performia - Agentic Performance Management System

## Quick Start

### 1. Set up environment variables
```bash
cp .env.template .env
# Edit .env with your actual tokens
```

### 2. Install voice control
```bash
./setup_voice.sh
```

### 3. Launch the agent
```bash
./launch_agent.sh
```

### 4. Start 24/7 orchestrator
```bash
./launch_orchestrator.sh
```

## Voice Commands

With voice control active, you can say:

- "Analyze performance trends for the engineering team"
- "Generate weekly performance report"
- "Schedule performance review for next Tuesday"
- "Create development plan for Sarah Johnson"
- "Show me productivity metrics for last month"

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│  Voice Control  │────▶│   Orchestrator  │
└─────────────────┘     └─────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Data Agent   │     │ Analysis     │     │ Feedback     │
│              │────▶│ Agent        │────▶│ Agent        │
└──────────────┘     └──────────────┘     └──────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               ▼
                        ┌──────────────┐
                        │   Reports    │
                        └──────────────┘
```

## MCP Servers Active

- GitHub: Code metrics and PR analysis
- Filesystem: Document management
- Memory: Persistent agent memory
- PostgreSQL: Performance data storage
- Slack: Team communication metrics
- Playwright: Web automation for dashboards

## Continuous Operation

The orchestrator runs 24/7 and automatically:
- Collects performance data every 5 minutes
- Runs daily analysis at 9 AM
- Generates weekly reports on Mondays at 10 AM
- Creates monthly summaries on the 1st at 11 AM
- Monitors for anomalies in real-time

## Development

To add new agents:
1. Create a new agent class in `orchestrator.py`
2. Register it with the orchestrator
3. Define workflow patterns
4. Test with voice commands

## Troubleshooting

- Check logs: `tail -f ~/.local/state/goose/logs/server/*/*`
- Verify MCP servers: `goose --list-servers`
- Test voice: Press hotkey and say "Test voice input"
EOF

echo "
✨ ════════════════════════════════════════════════════════ ✨
   SETUP COMPLETE! You're ready for Agentic Engineering!
✨ ════════════════════════════════════════════════════════ ✨

Next steps:

1. Set up your environment variables:
   cp .env.template .env
   # Edit .env with your actual tokens

2. Install voice control:
   ./setup_voice.sh

3. Launch the Performia agent:
   ./launch_agent.sh

4. Start the 24/7 orchestrator:
   ./launch_orchestrator.sh

5. Test with voice:
   Press your hotkey and say:
   'Analyze performance trends for last month'

Your agents will now:
✓ Collect data continuously
✓ Analyze performance metrics
✓ Generate personalized feedback
✓ Create and distribute reports
✓ Run 24/7 without your intervention

Remember: You are no longer the bottleneck!
The agents work while you sleep. 🚀
"
