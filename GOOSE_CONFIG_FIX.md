# Goose Configuration Issue & Resolution

## Problem Identified

Your Goose config has MCP servers **listed** but not **properly configured as extensions**. This is why they don't appear in the extension pane.

### What You Had:
```yaml
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
```

This just lists server names - Goose doesn't know HOW to run them.

### What You Need:
```yaml
extensions:
  filesystem:
    enabled: true
    type: commandline
    name: filesystem
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-filesystem"
      - "/Users/danielconnolly/Projects"
```

Each MCP server needs to be configured as a **command-line extension** with:
- Command to run (npx)
- Arguments
- Environment variables
- Proper paths

## Solutions Available

### Option 1: Quick Setup (Recommended) ⚡

Run the automated setup script:

```bash
cd /Users/danielconnolly/Projects/Performia
./scripts/quick-goose-setup.sh
```

This will:
- ✅ Backup your current config
- ✅ Install properly configured MCP servers
- ✅ Create secrets.yaml template if needed
- ✅ Verify all dependencies

### Option 2: Manual Configuration 🔧

1. Backup your current config:
```bash
cp ~/.config/goose/config.yaml ~/.config/goose/config.yaml.backup
```

2. Use the new config:
```bash
cp ~/.config/goose/config-properly-configured.yaml ~/.config/goose/config.yaml
```

3. Edit your API keys:
```bash
nano ~/.config/goose/secrets.yaml
```

### Option 3: Interactive Configuration 🎮

Use Goose's built-in configuration tool:

```bash
goose configure
```

Then:
1. Select "Add Extension"
2. Choose "Command-line Extension"
3. For Filesystem:
   - Name: `filesystem`
   - Command: `npx`
   - Args: `-y @modelcontextprotocol/server-filesystem /Users/danielconnolly/Projects`
4. Repeat for GitHub and other servers

## Verification

After setup, verify everything works:

```bash
./scripts/verify-goose-config.sh
```

Or manually test:

```bash
cd /Users/danielconnolly/Projects/Performia
goose session start
```

In the Goose prompt:
```
list available tools
```

You should see tools like:
- `read_file` (from filesystem)
- `list_directory` (from filesystem)
- `create_repository` (from github)
- `search_repositories` (from github)

## What MCP Servers Do

### Filesystem MCP
- Read/write files
- List directories
- Search files
- Create directories
- **Critical for the migration** - Goose needs this to move files

### GitHub MCP
- Create/manage repositories
- Create branches
- Manage issues and PRs
- Commit code
- **Useful for migration** - Can help consolidate Git repos

### Memory MCP (Built-in)
- Persistent context across sessions
- Remembers conversation history
- **Critical for compute maxing** - Allows Goose to maintain state

## Why This Matters for Performia Migration

The migration plan requires Goose to:
1. **Read and analyze** both codebases (needs filesystem)
2. **Move and reorganize** hundreds of files (needs filesystem)
3. **Update Git repositories** (needs github)
4. **Remember context** between phases (needs memory)

Without properly configured MCP servers, Goose is just a chatbot. With them, it becomes an autonomous agent that can execute the entire migration plan.

## Current Status

✅ Created files:
- `/Users/danielconnolly/Projects/Performia/MIGRATION_PLAN.md`
- `/Users/danielconnolly/Projects/Performia/.goosehints`
- `~/.config/goose/config-properly-configured.yaml`
- `/Users/danielconnolly/Projects/Performia/scripts/quick-goose-setup.sh`
- `/Users/danielconnolly/Projects/Performia/scripts/verify-goose-config.sh`
- `/Users/danielconnolly/Projects/Performia/scripts/setup-goose-mcp.sh`

🎯 Next Action:

**Run the quick setup:**
```bash
cd /Users/danielconnolly/Projects/Performia
./scripts/quick-goose-setup.sh
```

Then test with:
```bash
goose session start
```

## Additional Notes

- **Memory extension**: Now enabled in new config (you were right, it wasn't working before)
- **Computer Controller**: Also enabled for automation tasks
- **npx requirement**: MCP servers run via npx, so Node.js must be installed
- **API Keys**: Stored in `~/.config/goose/secrets.yaml`, referenced in config.yaml

## Troubleshooting

If you see "Failed to start MCP server":
1. Check that npx is installed: `which npx`
2. Check API keys in secrets.yaml
3. Try running the MCP server manually:
   ```bash
   npx -y @modelcontextprotocol/server-filesystem /Users/danielconnolly/Projects
   ```

If extensions don't appear:
1. Verify config.yaml has `type: commandline` entries
2. Restart Goose completely
3. Check Goose logs: `tail -f ~/.local/state/goose/logs/server/*/*`
