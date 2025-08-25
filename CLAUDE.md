# Claude Code Session Management

## Quick Start

Use these commands to manage your work sessions:

```bash
# Start a new session
/start [session-name]

# End current session
/end

# Check session status
/status
```

## Usage Examples

### Starting a Session
```bash
# Start with custom name
/start audio-controls-feature

# Start default session
/start
```

### Ending a Session
```bash
# End and archive current session
/end
```

### Checking Status
```bash
# View current session details
/status
```

## Session Files

- Active session: `.claude/session.json`
- Archived sessions: `.claude/archives/`

## Implementation

The session management system is implemented in `.claude/commands.sh` and provides:

1. **Session tracking** - Records start/end times and session metadata
2. **Session archiving** - Automatically archives completed sessions
3. **Status monitoring** - Check current session status anytime

## Running Commands

From the project root, run:
```bash
.claude/commands.sh start [name]
.claude/commands.sh end
.claude/commands.sh status
```

Or create aliases in your shell:
```bash
alias /start='.claude/commands.sh start'
alias /end='.claude/commands.sh end'
alias /status='.claude/commands.sh status'
```