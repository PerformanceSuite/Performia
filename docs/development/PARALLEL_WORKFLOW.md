# Parallel Agent Development Workflow

This guide explains how to run multiple Claude Code agents in parallel for maximum development velocity.

## 🚀 Quick Start

### 1. Initialize Agent Branches

```bash
cd ~/Projects/Performia
./scripts/dev/orchestrate-agents.sh start
```

This creates three feature branches:
- `feature/frontend-optimization` - Frontend agent work
- `feature/audio-pipeline-optimization` - Audio pipeline agent work
- `feature/voice-control-integration` - Voice control agent work

### 2. Open 3 Terminal Windows

**Terminal 1: Frontend Agent**
```bash
cd ~/Projects/Performia
git checkout feature/frontend-optimization
claude
```
Then say:
```
"Act as the frontend-dev agent and audit the Living Chart component for performance bottlenecks"
```

**Terminal 2: Audio Pipeline Agent**
```bash
cd ~/Projects/Performia
git checkout feature/audio-pipeline-optimization
claude
```
Then say:
```
"Act as the audio-pipeline-dev agent and review the Song Map generation pipeline"
```

**Terminal 3: Voice Control Agent**
```bash
cd ~/Projects/Performia
git checkout feature/voice-control-integration
claude
```
Then say:
```
"Act as the voice-control agent and create a plan for integrating Whisper API"
```

### 3. Start Monitoring Dashboard

**Terminal 4: Dashboard** (optional but recommended)
```bash
cd ~/Projects/Performia
./scripts/dev/agent-dashboard.sh
```

This displays a real-time dashboard showing:
- Agent activity status (active/idle)
- Commits per branch
- File changes
- Recent activity
- Git status

## 📊 Monitoring Tools

### Real-time Dashboard
```bash
./scripts/dev/agent-dashboard.sh
```
Shows live status of all agents with color-coded activity indicators.

### Detailed Status
```bash
./scripts/dev/orchestrate-agents.sh status
```
Shows detailed information about each agent's progress.

### Session Monitor
```bash
./scripts/dev/monitor-sessions.sh
```
Monitors active Claude Code sessions and file changes.

## 🔄 Workflow Patterns

### Pattern 1: Independent Feature Development

Each agent works on completely separate features:

```
Frontend Agent → UI improvements
Audio Agent → Beat detection optimization
Voice Agent → Whisper integration
```

**Merging:**
```bash
# Merge each agent's work when complete
./scripts/dev/orchestrate-agents.sh merge frontend
./scripts/dev/orchestrate-agents.sh merge audio
./scripts/dev/orchestrate-agents.sh merge voice
```

### Pattern 2: Coordinated Development

Agents work on related features that need coordination:

```
Frontend Agent → Add voice control UI
Voice Agent → Implement voice backend
Audio Agent → Add audio feedback
```

**Coordination:** Use this coordinator session to:
- Review work across agents
- Resolve conflicts
- Ensure integration works

### Pattern 3: Research + Implementation

One agent researches while others implement:

```
Agent 1 → Research best practices
Agent 2 → Implement based on findings
Agent 3 → Write tests
```

## 🎯 Best Practices

### Branch Strategy
- Keep feature branches focused and short-lived
- Merge to main frequently (daily if possible)
- Use descriptive branch names
- Delete branches after merging

### Communication
- Each agent commits with clear messages
- Use conventional commits format:
  - `feat:` new features
  - `fix:` bug fixes
  - `perf:` performance improvements
  - `refactor:` code refactoring
  - `test:` adding tests
  - `docs:` documentation

### Conflict Resolution
If merge conflicts occur:
```bash
# Manual resolution
git checkout main
git merge feature/agent-branch
# Resolve conflicts in your editor
git add .
git commit -m "chore: resolve merge conflicts from agent work"
```

Or ask the coordinator (this session) to help resolve.

### Code Review
Before merging agent work:
1. Check the agent's commits: `git log main..feature/agent-branch`
2. Review changed files: `git diff main..feature/agent-branch`
3. Run tests: `npm test` or `pytest`
4. Check for conflicts: `git merge-base --is-ancestor main feature/agent-branch`

## 📈 Monitoring Agent Progress

### Activity Indicators
- 🟢 **Green (●)** - Agent is actively working (files modified in last 10 min)
- 🟡 **Yellow (○)** - Agent is idle
- 🔴 **Red** - Agent has errors or conflicts

### Metrics Tracked
- **Commits**: Number of commits on the branch
- **Files Changed**: Total files modified
- **Unstaged Changes**: Work in progress
- **Recent Activity**: Files modified recently

## 🛠️ Troubleshooting

### Agent Not Making Progress
1. Check the agent's terminal for errors
2. Verify the agent has the correct context
3. Re-invoke the agent with clearer instructions

### Merge Conflicts
1. Use the dashboard to see which files conflict
2. Ask coordinator session to help resolve
3. Or manually resolve and commit

### Git State Issues
```bash
# Reset to clean state if needed
git checkout main
git branch -D feature/problematic-branch
./scripts/dev/orchestrate-agents.sh start
```

## 🎬 Example Session

### Starting Work
```bash
# Terminal 1 - Start orchestration
./scripts/dev/orchestrate-agents.sh start

# Terminal 2 - Dashboard
./scripts/dev/agent-dashboard.sh

# Terminals 3-5 - Launch agents
# (checkout branches and start claude in each)
```

### During Work
- Watch dashboard for agent activity
- Review commits as they happen
- Coordinate between agents if needed

### Finishing Work
```bash
# Check status
./scripts/dev/orchestrate-agents.sh status

# Merge completed work
./scripts/dev/orchestrate-agents.sh merge frontend
./scripts/dev/orchestrate-agents.sh merge audio
./scripts/dev/orchestrate-agents.sh merge voice

# Push to remote
git push origin main
```

## 📝 Tips

1. **Start with clear tasks** - Give each agent a specific, focused goal
2. **Monitor regularly** - Keep the dashboard open to catch issues early
3. **Commit often** - Each agent should commit small, logical changes
4. **Test incrementally** - Run tests as changes are made
5. **Coordinate through main session** - Use this session to review and coordinate

## 🚦 Status Commands

```bash
# Check all agents
./scripts/dev/orchestrate-agents.sh status

# Start new session
./scripts/dev/orchestrate-agents.sh start

# Merge agent work
./scripts/dev/orchestrate-agents.sh merge <agent-name>

# Stop all agents
./scripts/dev/orchestrate-agents.sh stop
```

## 🎯 Success Metrics

Your parallel workflow is successful when:
- ✅ All 3 agents are making progress simultaneously
- ✅ Commits are happening regularly across branches
- ✅ No merge conflicts (or resolved quickly)
- ✅ Tests pass on all branches
- ✅ Features integrate smoothly when merged

---

**Ready to go parallel!** 🚀

Start your agents and watch the velocity increase!