# .claude Directory

This directory contains Claude Code configuration, project context, and automated maintenance for Performia.

**Last Updated**: October 3, 2025

---

## 📋 Directory Contents

### Core Documentation
- **`CLAUDE.md`** - Project context and architecture for AI agents
- **`memory.md`** - Current project status, decisions, and next steps
- **`SESSION_SUMMARY.md`** - Latest session work details
- **`sprint_status.md`** - Current sprint progress

### Scripts & Tools 🛠️
- **`cleanup.sh`** - Automated repository cleanup (runs via hooks)
- **`hooks.json`** - Claude Code session hooks configuration

### Agents & Commands
- **`agents/`** - Specialized agent definitions
- **`commands/`** - Custom Claude Code commands
- **`logs/`** - Agent execution logs

### Configuration
- **`settings.json`** - Claude Code settings
- **`settings.local.json`** - Local overrides

---

## 🚀 Quick Start

### Starting a Claude Code Session
```bash
/start-session
```
This universal command:
- Loads `.claude/memory.md` context (if it exists)
- Checks git status
- Reviews recent commits
- Suggests actionable next steps

### Ending a Claude Code Session
```bash
/end-session
```
This universal command:
- Updates `.claude/memory.md` with session work (if it exists)
- Runs `.claude/cleanup.sh` to clean repo (if it exists)
- Prepares for next session
- You manually exit after this completes

### Manual Cleanup (if needed)
```bash
./.claude/cleanup.sh
```

### View Project Information
```bash
# View project memory
cat .claude/memory.md

# View project status
cat docs/STATUS.md

# Update memory via Claude Code
# Just say: "Update memory with [information]"
```

---

## 📚 Documentation Structure

### For New Sessions
**Start here** to understand current state:
1. Read `SESSION_SUMMARY.md` - What was just completed
2. Read `memory.md` - Current status and decisions
3. Check `../docs/STATUS.md` - Overall project status

### For Project Context
**Start here** to understand the project:
1. Read `CLAUDE.md` - Architecture and requirements
2. Read `../README.md` - Project overview
3. Check available `agents/` - Specialized capabilities

### For Development Workflow
**Simple workflow**:
1. Work normally in Claude Code
2. Make regular git commits as you progress
3. When you end the session (close Claude Code), cleanup runs automatically
4. Repository stays clean and organized - no manual intervention needed

---

## 🤖 Available Agents

Specialized agents for different development tasks. See `agents/` directory.

### Core Agents
- **frontend-dev** - React/TypeScript UI development
- **audio-pipeline-dev** - Audio processing pipeline
- **voice-control** - Voice command integration

### Legacy Agents
- **migration-specialist** - Codebase unification (complete)
- **ui-ux-developer** - UI/UX improvements

---

## 📝 Key Files Reference

### Must Read Before Coding
1. **`CLAUDE.md`** - Project architecture, requirements, data structures
2. **`memory.md`** - Current status, recent decisions, next steps

### Must Update After Coding
1. **`SESSION_SUMMARY.md`** - Document what was completed
2. **`memory.md`** - Update timestamp and current status
3. **`../docs/STATUS.md`** - Update project status

### Automation Handles These
- `.gitignore` updates
- Archive organization
- Temporary file cleanup
- Git operations

---

## 🔧 Automated Cleanup

### cleanup.sh ⚙️
**Purpose**: Automatic repository maintenance

**What it does** (automatically on session end):
- ✅ Removes temporary files (*.tmp, *.log, .DS_Store, etc.)
- ✅ Cleans Python cache (__pycache__, *.pyc)
- ✅ Updates timestamps in memory.md and STATUS.md
- ✅ Removes empty directories
- ✅ Archives old documentation (>30 days)
- ✅ **Silent operation** - no prompts or output

**Runs via**: `.claude/hooks.json` SessionEnd hook

**Manual run** (if needed):
```bash
./.claude/cleanup.sh
```

### hooks.json 🪝
**Purpose**: Claude Code session lifecycle automation

**What it does**:
- Triggers cleanup.sh when sessions end
- No user interaction required
- Keeps repository clean automatically

---

## 📊 Development Workflow

### Standard Development Session

```bash
# 1. Start Claude Code
# - Review .claude/memory.md for context
# - Check docs/STATUS.md for current state

# 2. Work on features
# - Develop normally
# - Make git commits as you go
# - Update .claude/memory.md with major decisions

# 3. End session
# - Close Claude Code
# - cleanup.sh runs automatically via hook
# - Repository is cleaned and timestamps updated
# - No manual intervention needed!
```

---

## 🎯 Best Practices

### Daily Development
- ✅ Review `.claude/memory.md` at session start for context
- ✅ Make regular git commits during work
- ✅ Update `.claude/memory.md` for major architectural decisions (just ask Claude!)
- ✅ Trust the automatic cleanup - no manual intervention needed

### Memory Management
- ✅ Use `/memory` command in Claude Code to update project memory
- ✅ Keep `.claude/CLAUDE.md` updated with project instructions
- ✅ Keep `.claude/memory.md` updated with current state and decisions
- ✅ Use `docs/STATUS.md` for high-level project status

### Repository Hygiene
- ✅ Cleanup happens automatically via hooks (SessionEnd)
- ✅ Manual cleanup available: `./.claude/cleanup.sh`
- ✅ Old docs auto-archived after 30 days
- ✅ Temp files removed automatically

### Quick Tips
- 💡 No scripts to remember - everything is automatic
- 💡 Just work normally and let hooks handle maintenance
- 💡 Use Claude Code's built-in memory features
- 💡 RAG knowledge base in `tools/knowledge-base/` for technical docs

---

## 📖 Complete Documentation Map

```
.claude/
├── README.md                    # This file - directory overview
├── CLAUDE.md                    # Project context for agents
├── memory.md                    # Current status and decisions
├── sprint_status.md            # Sprint tracking
├── cleanup.sh                   # Automated cleanup script
├── hooks.json                   # Claude Code session hooks
├── agents/                      # Specialized agent definitions
├── commands/                    # Custom commands
└── logs/                        # Log files (gitignored)

../docs/
├── STATUS.md                    # Overall project status
├── README.md                    # Project overview
└── archive/                     # Historical documentation

../tools/knowledge-base/
└── ...                          # RAG system for technical docs
```

---

## 🔍 Troubleshooting

### Scripts won't run
```bash
chmod +x ./.claude/*.sh
```

### Can't find session summary
```bash
cat ./.claude/SESSION_SUMMARY.md
```

### Need project context
```bash
cat ./.claude/CLAUDE.md
cat ./.claude/memory.md
```

### Need to review session history
```bash
./session-last
ls -la .claude/logs/sessions/
```

---

## 📞 Help & Resources

### Quick Commands
```bash
# View this guide
cat ./.claude/README.md

# View scripts guide
cat ./.claude/SCRIPTS_GUIDE.md

# View project context
cat ./.claude/CLAUDE.md

# View current status
cat ./.claude/memory.md
cat ../docs/STATUS.md
```

### Documentation Links
- **Project Status**: `../docs/STATUS.md`
- **Main README**: `../README.md`
- **Scripts Guide**: `SCRIPTS_GUIDE.md`
- **Project Context**: `CLAUDE.md`

---

**Remember**: Everything is automatic now! ✨

**Zero commands needed**:
- Just work normally in Claude Code
- Cleanup happens automatically via hooks
- Use built-in `/memory` command for updates

---

*Last Updated: October 3, 2025*
