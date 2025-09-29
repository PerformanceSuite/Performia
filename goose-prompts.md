# Reusable Goose Prompts

## 🎯 Core Principles
Every prompt should emphasize:
1. **Autonomy** - Goose makes decisions
2. **Completion** - Finish the entire task
3. **Testing** - Verify everything works
4. **Documentation** - Document what was done
5. **Memory** - Remember important information

## 📝 Prompt Templates

### 1. Autonomous Executor
```
You are an autonomous AI developer. Execute [TASK] completely without asking for permission.
Make decisions, implement solutions, test them, and commit your work.
If you encounter errors, debug and fix them yourself.
Continue until the task is 100% complete.
```

### 2. Migration Phase Executor
```
Read MIGRATION_PLAN.md and execute Phase [N] completely.
You have full autonomy to:
- Move files
- Update configurations  
- Resolve conflicts
- Test changes
- Commit work
Do not stop until all Phase [N] tasks are complete.
```

### 3. Test-Driven Fixer
```
Find all failing tests and fix them:
1. Run test suites
2. Analyze failures
3. Implement fixes
4. Verify tests pass
5. Commit fixes
Continue until all tests are green.
```

### 4. Dependency Manager
```
Ensure all dependencies are properly installed:
1. Check package.json and requirements.txt
2. Install missing dependencies
3. Resolve version conflicts
4. Test all imports work
5. Update lock files
6. Document the dependency tree
```

### 5. Code Quality Improver
```
Improve code quality for [DIRECTORY]:
1. Fix linting errors
2. Add missing type annotations
3. Remove dead code
4. Optimize performance bottlenecks
5. Add comprehensive docstrings
6. Commit improvements
Work autonomously for 30 minutes.
```

### 6. Documentation Generator
```
Generate complete documentation for [COMPONENT]:
1. Analyze code structure
2. Create API documentation
3. Write usage examples
4. Add inline comments
5. Update README
6. Create diagrams if needed
```

### 7. Agent Creator
```
Create an autonomous agent for [DOMAIN]:
1. Design agent architecture
2. Implement core functionality
3. Add domain-specific methods
4. Create launch script
5. Integrate with orchestrator
6. Test agent operation
7. Document capabilities
```

### 8. Continuous Monitor
```
Monitor and improve [ASPECT] continuously:
1. Set up monitoring metrics
2. Identify issues or opportunities
3. Implement improvements
4. Test changes
5. Commit if successful
6. Report status to memory
Repeat cycle every 30 minutes.
```

### 9. Integration Builder
```
Build integration between [COMPONENT_A] and [COMPONENT_B]:
1. Analyze both components
2. Design integration approach
3. Implement connection layer
4. Add error handling
5. Test end-to-end flow
6. Document integration
```

### 10. Performance Optimizer
```
Optimize performance of [COMPONENT]:
1. Profile current performance
2. Identify bottlenecks
3. Implement optimizations
4. Measure improvements
5. Ensure no regressions
6. Document changes and results
```

## 🔄 Composite Prompts

### Full Migration Automation
```
Execute the complete migration plan autonomously:
For each phase in MIGRATION_PLAN.md:
  1. Read phase requirements
  2. Execute all tasks
  3. Test changes
  4. Commit work
  5. Update status
  6. Move to next phase
Continue until all phases complete.
```

### 24/7 Development Cycle
```
Implement continuous development cycle:
Every 30 minutes:
  1. Check for new issues
  2. Run test suites
  3. Improve documentation
  4. Optimize performance
  5. Clean up code
  6. Commit improvements
Continue indefinitely.
```

### Domain Expert Builder
```
Become a domain expert for [DOMAIN]:
1. Analyze all [DOMAIN] code
2. Identify patterns and anti-patterns
3. Create best practices guide
4. Refactor to follow best practices
5. Create domain-specific tools
6. Document expertise
```

## 💡 Prompt Engineering Tips

### DO:
- Be specific about autonomy level
- Include success criteria
- Specify tools to use (developer__, memory__)
- Set time bounds for long tasks
- Request memory updates

### DON'T:
- Ask Goose to ask permission
- Leave tasks open-ended
- Forget testing requirements
- Skip documentation
- Ignore error handling

## 📊 Effectiveness Patterns

### Most Effective:
```
"Execute [SPECIFIC_TASK] autonomously using [SPECIFIC_TOOLS].
Success criteria: [MEASURABLE_OUTCOME].
Time limit: [DURATION].
Document in: [LOCATION]."
```

### Least Effective:
```
"Can you help with [VAGUE_TASK]?"
"Please check if [UNCERTAIN_CONDITION]"
"Let me know if [OPEN_ENDED]"
```

## 🎯 Goal-Oriented Prompts

### Ship Feature X
```
Ship feature [X] end-to-end:
1. Design implementation
2. Write code
3. Add tests  
4. Update documentation
5. Deploy
6. Verify working
You have full autonomy. Ship it.
```

### Fix Bug Y
```
Fix bug [Y] completely:
1. Reproduce the bug
2. Find root cause
3. Implement fix
4. Add regression test
5. Verify fix works
6. Commit with explanation
```

### Build System Z
```
Build system [Z] from scratch:
1. Design architecture
2. Implement core
3. Add features
4. Write tests
5. Document usage
6. Create examples
Make all decisions autonomously.
```

## 🚀 Meta-Prompts

### Improve Yourself
```
Improve your own effectiveness:
1. Analyze your recent actions
2. Identify inefficiencies
3. Create better patterns
4. Document learnings
5. Update recipes
```

### Teach Another Agent
```
Teach another agent to do [TASK]:
1. Document process
2. Create examples
3. Write tests
4. Create recipe
5. Verify agent can execute
```

---
*Use these prompts to maximize Goose's autonomous capabilities*
