# Frontend Agent Tasks

## 🎯 Current Sprint: Living Chart Performance Audit

### Task 1: Component Audit ✅ START HERE
**Goal**: Identify performance bottlenecks in Living Chart

**Steps**:
1. Audit `frontend/src/components/LivingChart/` components
2. Check for:
   - Missing React.memo on components
   - Missing useMemo/useCallback optimizations
   - Unnecessary re-renders
   - Large bundle sizes
   - Inline function definitions in JSX

3. Create audit report: `frontend/PERFORMANCE_AUDIT.md`

**Expected Output**:
- List of components needing optimization
- Severity ratings (high/medium/low)
- Estimated impact of fixes
- Recommended approach for each issue

---

### Task 2: Implement Quick Wins
After audit, implement highest-impact optimizations:
- Add React.memo where needed
- Memoize expensive calculations
- Optimize re-render triggers

---

### Task 3: Performance Testing
- Benchmark before/after changes
- Verify 60fps target met
- Test with large song files

---

## 📝 Notes for Agent

You have access to:
- Full frontend codebase
- Agent definition: `.claude/agents/frontend-dev.md`
- Project context: `.claude/CLAUDE.md`
- Memory: `.claude/memory.md`

**Performance Targets**:
- 60fps during playback
- <50ms UI update latency
- Smooth scrolling on Living Chart

**Branch**: `feature/frontend-optimization`

Start with Task 1 and commit your audit report when complete!