# UI Improvement System - Quick Start Guide

## 5-Minute Setup

### 1. Verify Installation

```bash
# Check you're in the project root
cd /Users/danielconnolly/Projects/Performia

# Verify directory structure
ls .claude/agents/ui-*.md
ls backend/scripts/ui_improvement_orchestrator.py
ls backend/config/ui_scoring_rubric.json
```

### 2. Install Dependencies

```bash
# Backend (if not already installed)
cd backend
pip install -r requirements.txt

# Frontend (if not already installed)
cd ../frontend
npm install
```

### 3. Start Frontend Dev Server

```bash
cd frontend
npm run dev
```

Keep this running in a separate terminal. The system needs the frontend accessible at `http://localhost:5173`.

### 4. Run the Orchestrator

```bash
cd backend/scripts
python ui_improvement_orchestrator.py
```

## What Happens Next

The orchestrator will:

1. ✅ Initialize and verify project structure
2. 📸 Capture current upload UI screenshot
3. 🎨 Invoke design agent to analyze and propose improvements
4. ⚙️ Invoke implementation agent to apply changes
5. 🔨 Build frontend to verify no breaking changes
6. 📸 Capture updated UI screenshot
7. 📊 Invoke evaluation agent to score design (8 dimensions)
8. 🔄 Repeat until target score (8.5/10) reached or max iterations (5)
9. 📝 Generate comprehensive final report

## Manual Agent Usage

If you prefer to run agents manually:

### Design Agent
```bash
# Via Claude CLI or API
claude "Act as the ui-design-agent and analyze this screenshot:
[screenshot path or image]

Provide detailed design specification for the Performia upload UI."
```

### Implementation Agent
```bash
claude "Act as the ui-implementation-agent and implement this design:

[paste design specification]

Files to modify:
- /Users/danielconnolly/Projects/Performia/frontend/App.tsx

Preserve all functionality."
```

### Evaluation Agent
```bash
claude "Act as the ui-evaluation-agent and evaluate this screenshot:
[screenshot path or image]

Score across all 8 dimensions and calculate composite score."
```

## Expected Output

After completion, check:

```bash
frontend/design_iterations/
├── iteration_0/
│   ├── before.png
│   ├── after.png
│   ├── design_spec.md
│   ├── implementation.md
│   ├── evaluation.json
│   └── evaluation.md
├── iteration_1/
│   └── ...
└── final_report.md    # <-- Read this!
```

## Example Final Report

```markdown
# Performia Upload UI Improvement Report

## Executive Summary
- Starting Score: 6.2/10
- Final Score: 8.7/10
- Improvement: +2.5 points
- Iterations Completed: 3
- Target Reached: ✅ YES

## Key Achievements
1. Improved visual hierarchy (+3.2 points)
2. Enhanced accessibility to WCAG AA (+2.8 points)
3. Refined spacing and layout (+2.1 points)

[Full details in report...]
```

## Troubleshooting

### Frontend Not Running
```bash
# Error: Cannot capture screenshot
# Solution: Ensure dev server running
cd frontend && npm run dev
```

### Build Failures
```bash
# Error: Frontend build failed
# Solution: Check TypeScript errors
cd frontend && npm run build
```

### Screenshot Capture
```bash
# Error: Puppeteer MCP unavailable
# Solution: Use manual screenshots temporarily
# Place in frontend/design_iterations/iteration_N/
```

## Customization

### Change Target Score
```bash
python ui_improvement_orchestrator.py --target-score 9.0
```

### Change Max Iterations
```bash
python ui_improvement_orchestrator.py --max-iterations 3
```

### Custom Project Root
```bash
python ui_improvement_orchestrator.py --project-root /path/to/project
```

## Next Steps

After system completes:

1. **Review Final Report**
   - Read `frontend/design_iterations/final_report.md`
   - Compare before/after screenshots
   - Review score progression

2. **Test Functionality**
   - Upload a test file
   - Verify progress tracking
   - Check error handling

3. **Deploy Changes**
   - Commit improvements
   - Push to repository
   - Deploy to production

4. **Optional: Additional Iterations**
   - If target not reached
   - Run orchestrator again
   - Focus on specific dimensions

## Key Files

- **Orchestrator**: `backend/scripts/ui_improvement_orchestrator.py`
- **Design Agent**: `.claude/agents/ui-design-agent.md`
- **Implementation Agent**: `.claude/agents/ui-implementation-agent.md`
- **Evaluation Agent**: `.claude/agents/ui-evaluation-agent.md`
- **Scoring Rubric**: `backend/config/ui_scoring_rubric.json`
- **Full Docs**: `backend/scripts/UI_IMPROVEMENT_SYSTEM.md`

## Support

Questions? Check:
1. Full documentation: `UI_IMPROVEMENT_SYSTEM.md`
2. Agent specifications: `.claude/agents/ui-*.md`
3. Scoring rubric: `backend/config/ui_scoring_rubric.json`

---

**Ready to improve your UI?** Run `python ui_improvement_orchestrator.py` and watch the magic happen! ✨
