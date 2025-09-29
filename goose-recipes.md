# Goose Recipes for Performia Development

## Core Principle
**You orchestrate, Goose executes.** These recipes enable autonomous development.

## 📋 Available Recipes

### 1. analyze-codebase
**Purpose:** Deep analysis of project structure and dependencies
```yaml
name: analyze-codebase
description: Analyze project structure, dependencies, and create reports
steps:
  - Use developer__shell to check git status
  - Use developer__analyze to examine directory structure
  - Create detailed markdown reports in docs/analysis/
  - Use memory__remember_memory to persist findings
```

### 2. migrate-phase
**Purpose:** Execute migration phases autonomously
```yaml
name: migrate-phase
description: Execute a specific migration phase from MIGRATION_PLAN.md
parameters:
  phase_number: integer (1-10)
steps:
  - Read MIGRATION_PLAN.md
  - Execute all tasks for specified phase
  - Test changes
  - Commit with descriptive message
  - Update phase status in memory
```

### 3. test-and-fix
**Purpose:** Run tests and automatically fix issues
```yaml
name: test-and-fix
description: Run test suites and fix failing tests
steps:
  - Run frontend tests with npm
  - Run backend tests with pytest
  - Analyze failures
  - Propose and implement fixes
  - Re-run tests until passing
  - Commit fixes
```

### 4. dependency-install
**Purpose:** Install and verify all dependencies
```yaml
name: dependency-install
description: Install all project dependencies and verify
steps:
  - Check for package.json in frontend/
  - Check for requirements.txt in backend/
  - Run npm install in appropriate directories
  - Run pip install for Python dependencies
  - Verify all imports work
  - Document any issues
```

### 5. create-agent
**Purpose:** Create new autonomous agents
```yaml
name: create-agent
description: Create a new MCP agent for specific domain tasks
parameters:
  agent_name: string
  domain: string (e.g., "testing", "documentation", "refactoring")
steps:
  - Create agent Python file in backend/agents/
  - Implement base agent class
  - Add domain-specific methods
  - Create launch script
  - Test agent functionality
  - Add to orchestrator
```

### 6. continuous-improvement
**Purpose:** 24/7 improvement cycle
```yaml
name: continuous-improvement
description: Autonomously improve codebase while you sleep
steps:
  - Analyze code quality metrics
  - Identify improvement opportunities
  - Create feature branch
  - Implement improvements
  - Run comprehensive tests
  - Create pull request
  - Document changes
```

### 7. documentation-sync
**Purpose:** Keep documentation in sync with code
```yaml
name: documentation-sync
description: Update all documentation to match current code
steps:
  - Scan all code files
  - Update API documentation
  - Update README files
  - Create missing documentation
  - Update MIGRATION_PLAN.md status
  - Commit documentation updates
```

## 🚀 Usage

### In Goose Session
```bash
# Start Goose with memory and developer extensions
goose session --with-builtin developer,memory

# In Goose prompt:
Execute recipe: migrate-phase with phase_number=3
```

### Via Script
```bash
./scripts/run-recipe.sh migrate-phase 3
```

## 📝 Creating New Recipes

Template for new recipes:
```yaml
name: recipe-name
description: What this recipe does
parameters:
  param1: type
  param2: type
steps:
  - Step 1 with specific tool usage
  - Step 2 with validation
  - Step 3 with memory persistence
  - Commit and document
```

## 🧠 Memory Patterns

Each recipe should:
1. Check memory for previous state
2. Execute tasks
3. Update memory with results
4. Persist important findings

Example:
```
memory__retrieve_memories category="migration_status"
# Do work
memory__remember_memory category="migration_status" tags="phase3,complete"
```

## 🔄 Continuous Patterns

### Morning Routine
```bash
goose recipe documentation-sync
goose recipe test-and-fix
goose recipe analyze-codebase
```

### Evening Routine
```bash
goose recipe continuous-improvement
```

### Migration Routine
```bash
goose recipe migrate-phase 3
goose recipe test-and-fix
goose recipe documentation-sync
```

## 📊 Success Metrics

- Lines of code written by Goose vs. human
- Tests passing automatically
- Documentation coverage
- Migration phases completed autonomously
- Time saved through automation

## 🎯 Goal

**"What if your codebase could ship itself?"**

Every recipe moves us closer to fully autonomous development where:
- Goose handles implementation
- Agents handle specialized tasks
- You handle architecture and vision
- The system improves continuously

---
*These recipes implement the Agentic Engineering paradigm from the whitepaper*
