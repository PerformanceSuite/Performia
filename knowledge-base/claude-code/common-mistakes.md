# Common Mistakes & How to Prevent Them

This file documents recurring mistakes and their solutions to prevent repetition.

## Directory Locations - CRITICAL

### ❌ MISTAKE: Looking in wrong config directory
**What happened (Oct 4, 2025)**: Searched `~/.config/claude/commands/` for custom slash commands when they were actually in `~/.claude/commands/`

**Correct locations:**
- Custom slash commands: `~/.claude/commands/*.md` (NOT ~/.config/claude/)
- Claude history: `~/.claude/history.jsonl`
- Claude config: `~/.config/claude/` (for MCP servers, GitHub accounts, etc.)
- Project-specific: `./.claude/` (cleanup.sh, memory.md, hooks.json, etc.)

**Prevention:**
1. ALWAYS check `~/.claude/` FIRST for slash commands
2. Use `ls ~/.claude/commands/` before claiming commands don't exist
3. Reference this file when confused about paths

## Session Management Workflow

### ❌ MISTAKE: Not running cleanup script during /end-session
**What happened (Oct 4, 2025)**: Created `.claude/cleanup.sh` but didn't execute it

**Correct workflow:**
1. `/start-session` → Read memory.md, check git status, suggest next steps
2. `/end-session` →
   - Update memory.md
   - Create cleanup.sh if missing
   - **EXECUTE `bash .claude/cleanup.sh`** ← THIS WAS SKIPPED
   - Confirm completion

**Prevention:**
1. The command file at `~/.claude/commands/end-session.md` now has **CRITICAL** warning
2. This mistake is documented in project memory.md
3. Always verify cleanup ran by checking git status after `/end-session`

## Learning from Mistakes

### The Problem
Memory alone isn't sufficient. We've made the same mistakes multiple times:
- Wrong directory paths
- Skipping cleanup execution
- Not following command instructions completely

### Proposed Solutions
1. **This file** - Central mistake documentation
2. **Docling integration** - Ingest official Claude Code docs for accurate information
3. **Checklist approach** - Create explicit checklists for common workflows
4. **Cross-reference** - When confused, check multiple sources (history, memory, this file, actual files)

---

*Last Updated*: October 4, 2025
*Purpose*: Prevent recurring mistakes through explicit documentation
