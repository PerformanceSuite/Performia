# Claude Code File Paths Reference

**CRITICAL**: This document defines the correct file paths for Claude Code configuration and custom commands.

## Global Configuration Paths

### Custom Slash Commands
**Location**: `~/.claude/commands/*.md`
- **NOT** `~/.config/claude/commands/`
- Each `.md` file defines a custom slash command
- Files are instructions for Claude to follow when command is invoked

**Examples**:
- `~/.claude/commands/start-session.md` - Session initialization
- `~/.claude/commands/end-session.md` - Session cleanup

### Claude Configuration
**Location**: `~/.claude/`
- `~/.claude/history.jsonl` - Command history
- `~/.claude/commands/` - Custom slash commands
- `~/.claude/file-history/` - File version history
- `~/.claude/projects/` - Project-specific data
- `~/.claude/todos/` - Todo items

### Other Config (MCP, GitHub, etc.)
**Location**: `~/.config/claude/`
- `~/.config/claude/mcp_servers.json` - MCP server configuration
- `~/.config/claude/github_accounts.json` - GitHub account settings

## Project-Specific Paths

### Claude Project Directory
**Location**: `./.claude/` (in project root)
- `.claude/CLAUDE.md` - Project context for agents
- `.claude/memory.md` - Project memory and session history
- `.claude/SESSION_SUMMARY.md` - Latest session summary
- `.claude/cleanup.sh` - Project-specific cleanup script
- `.claude/hooks.json` - Event hooks configuration
- `.claude/settings.json` - Project-specific settings
- `.claude/commands/` - Project-specific custom commands (optional)

### Knowledge Base
**Location**: `./knowledge-base/` (in project root)
- `knowledge-base/claude-code/` - Claude Code documentation
- `knowledge-base/audio-dsp/` - Audio domain knowledge
- `knowledge-base/project/` - Project-specific docs
- `knowledge-base/mistakes/` - Common errors and solutions

## Common Mistakes

### ❌ WRONG: Looking in `~/.config/claude/commands/`
Custom slash commands are **NOT** stored in `~/.config/claude/`

### ✅ CORRECT: Looking in `~/.claude/commands/`
Custom slash commands are stored in `~/.claude/commands/`

### How to Verify
```bash
# Check for custom commands
ls -la ~/.claude/commands/

# NOT this
ls -la ~/.config/claude/commands/  # This directory may not even exist
```

## Quick Reference

| Purpose | Correct Path | Wrong Path |
|---------|-------------|------------|
| Custom commands | `~/.claude/commands/` | `~/.config/claude/commands/` |
| MCP servers | `~/.config/claude/mcp_servers.json` | `~/.claude/mcp_servers.json` |
| Project memory | `./.claude/memory.md` | `./memory.md` |
| Cleanup script | `./.claude/cleanup.sh` | `./cleanup.sh` |
| Project context | `./.claude/CLAUDE.md` | `./CLAUDE.md` |

---

**Last Updated**: October 4, 2025
**Purpose**: Prevent directory confusion errors
