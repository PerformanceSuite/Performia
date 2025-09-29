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
