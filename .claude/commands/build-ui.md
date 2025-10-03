# Build UI from PRD

Autonomous UI/UX development with visual self-review and iteration.

## Usage

```
/build-ui component=LivingChart prd="Performia UI PRD.md"
```

Or:

```
/build-ui
# Then provide: component name and PRD file
```

## What This Does

This command activates the UI/UX development agent which will:

1. **Read the PRD** - Understand all requirements and design specs
2. **Implement the UI** - Build React + TypeScript + Tailwind components
3. **Self-Review** - Use Puppeteer to screenshot and analyze
4. **Iterate** - Fix issues and re-review until perfect
5. **Finalize** - Test, commit, and report completion

## The Autonomous Loop

```
Read PRD → Implement → Screenshot → Analyze → Fix → Repeat → Commit
```

The agent will:
- Take screenshots at multiple viewport sizes
- Compare against PRD requirements
- Identify discrepancies automatically
- Fix issues and re-screenshot
- Iterate up to 5 times before asking for help

## Arguments

- `component` - Name of the component to build (e.g., "LivingChart")
- `prd` - Path to PRD file (e.g., "Performia UI PRD.md")
- `iterations` - Max iterations (default: 5)
- `viewports` - Viewport sizes to test (default: desktop, tablet, mobile)

## Example Session

```bash
# In Performia directory
claude-danger

# In Claude Code:
/build-ui component=LivingChart prd="Performia UI PRD.md"
```

The agent will:
1. Read the PRD section on Living Chart
2. Create `frontend/src/components/LivingChart.tsx`
3. Start dev server
4. Navigate to http://localhost:5173
5. Take screenshots
6. Analyze: "Cyan wipe animation needs smoother timing"
7. Fix the timing
8. Screenshot again
9. Verify: "✓ Matches PRD!"
10. Commit: "feat: implement Living Chart with smooth animations"

## Visual Review Process

For each iteration:
- **Desktop** (1920x1080) - Full layout check
- **Tablet** (768x1024) - Responsive behavior
- **Mobile** (375x667) - Touch-friendly UI

The agent compares each screenshot against:
- Color accuracy
- Layout alignment
- Animation smoothness
- Typography
- Spacing
- Interactive elements

## When It Asks for Help

After 5 iterations, if not perfect, the agent will:
- Show you all screenshots
- Explain what's still not matching
- Ask for guidance on how to proceed

## Success Indicators

You'll know it's done when you see:
```
✅ UI Development Complete!
   - Component: LivingChart
   - Iterations: 3
   - Screenshots: 9 (3 viewports x 3 iterations)
   - Commit: abc123f
   - Status: All criteria met!
```

## Tips

1. **Detailed PRDs** - More detail = better results
2. **Reference Images** - Include mockups if you have them
3. **Success Criteria** - List exact requirements
4. **Let it iterate** - Don't interrupt the loop
5. **Review screenshots** - Check the final visual proofs

## Related Commands

- `/merge-frontend` - Merge Performia-Front UI improvements
- `/test-ui` - Run UI tests
- `/screenshot component` - Take a quick screenshot

## Performance Focus

For Performia's music performance UI:
- 60fps animations are critical
- Sub-10ms latency for audio sync
- Smooth scrolling for Living Chart
- Natural timing for syllable highlighting

The agent knows these requirements and will verify them!
