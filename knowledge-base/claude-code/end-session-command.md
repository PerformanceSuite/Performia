# end-session - Session Cleanup

Universal session cleanup for any project with Claude Code.

## What it does

1. Update `.claude/memory.md` with:
   - Work completed this session
   - Current status
   - Next steps for next session
   - Creates `.claude/memory.md` if it doesn't exist
2. Create `.claude/cleanup.sh` if it doesn't exist (auto-generates sensible defaults)
3. **CRITICAL: Execute `bash .claude/cleanup.sh` to clean project-specific files**
4. Confirm cleanup completion

## ⚠️ IMPORTANT EXECUTION STEP

**YOU MUST RUN THE CLEANUP SCRIPT** - This is not optional!

After creating or verifying `.claude/cleanup.sh` exists, you MUST execute it:

```bash
bash .claude/cleanup.sh
```

This removes cache files, temporary files, and updates timestamps. DO NOT skip this step!

## Usage

```bash
/end-session
```

## Auto-Generated Cleanup Script

If `.claude/cleanup.sh` doesn't exist, this command will automatically create one with sensible defaults:
- Removes common temporary files (*.tmp, *.log, *.swp, .DS_Store, etc.)
- Cleans Python cache (__pycache__, *.pyc)
- Cleans Node.js cache (if package.json exists)
- Updates timestamps in .claude/memory.md
- Removes empty directories

The generated script is **safe** and only removes common temporary files. You can customize it after it's created.

## Notes

- **Universal command** - works on any project
- **Auto-creates** cleanup.sh and memory.md if they don't exist
- Generated cleanup script only removes safe temporary files
- You can customize the generated cleanup.sh for project-specific needs
- User should manually exit Claude Code after this command completes

## Implementation Details

When creating `.claude/cleanup.sh`, the command should:
1. Detect project type (check for package.json, requirements.txt, etc.)
2. Generate appropriate cleanup rules based on detected languages
3. Make the script executable (chmod +x)
4. Include safe defaults that won't harm the project
