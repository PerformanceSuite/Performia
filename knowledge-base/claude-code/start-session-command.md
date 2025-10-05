# start-session - Session Initialization

Universal session starter for any project with Claude Code.

## What it does

1. Check if `.claude/memory.md` exists and read it for:
   - Recent work and current status
   - Action items marked as ⏳ (pending)
   - "Next Session Recommendations" section
2. Check `git status` for uncommitted changes and current branch
   - Look for new/untracked files in `.claude/` that may need review
3. Review recent commits for context
4. Check for pending review tasks:
   - Files with "REVIEW" or "TODO" in name
   - Uncommitted documents in `.claude/`
   - Action items from memory.md
5. Synthesize a concise status report
6. Suggest actionable next steps based on current state

## Usage

```bash
/start-session
```

## Output Format

```
📍 Current Status:
- Branch: [branch-name]
- Last work: [from memory.md if exists]
- Uncommitted: [file count]

🎯 Suggested Next Steps:
1. [Priority task based on memory/git status]
2. [Second priority]
3. [Third priority]
```

## Notes

- **Universal command** - works on any project
- Keep output concise (< 10 lines)
- Focus on actionable next steps
- Don't repeat full memory.md, just summarize
- If no `.claude/memory.md` exists, just show git status and recent commits
