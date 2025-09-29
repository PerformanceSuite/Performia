#!/bin/bash
# Goose Recipe Runner - Executes recipes with proper context

RECIPE=$1
PHASE=$2

echo "🦆 Goose Recipe Runner"
echo "====================="
echo "Recipe: $RECIPE"
echo ""

# Load API keys
source ~/.config/api-keys/.env.api-keys 2>/dev/null

# Change to project directory
cd /Users/danielconnolly/Projects/Performia

case "$RECIPE" in
  "migrate-phase")
    echo "📦 Executing Migration Phase $PHASE"
    /Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << EOF
Read MIGRATION_PLAN.md and understand Phase $PHASE completely.

Now execute Phase $PHASE following these principles:
1. You are autonomous - make decisions and execute
2. Use developer__shell for git operations
3. Use developer__text_editor to read and modify files  
4. Use developer__analyze to understand code structure
5. Use memory__remember_memory to track progress
6. Test everything you change
7. Commit your work with clear messages

Start by checking current status:
- What files exist in frontend/ and backend/?
- What's the git status?
- What does Phase $PHASE require?

Then execute ALL tasks for Phase $PHASE autonomously.
Do not ask for permission - just execute.
If you encounter errors, debug and fix them.
Continue until Phase $PHASE is complete.

Remember: You're building a system that can ship itself.
EOF
    ;;
    
  "test-and-fix")
    echo "🧪 Running Test & Fix Cycle"
    /Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << EOF
Execute comprehensive testing:

1. Frontend tests:
   - cd frontend && npm test
   - If no test script, create one
   - Fix any failing tests

2. Backend tests:
   - cd backend && python -m pytest
   - Fix any failing tests
   
3. Integration tests:
   - Test frontend can connect to backend
   - Test all API endpoints
   
Document all fixes in memory and commit changes.
EOF
    ;;
    
  "analyze-codebase")
    echo "🔍 Analyzing Codebase"
    /Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << EOF
Perform deep codebase analysis:

1. Use developer__analyze on frontend/ and backend/
2. Create ANALYSIS_REPORT.md with:
   - File count and structure
   - Dependency analysis  
   - Code quality metrics
   - Missing pieces
   - Integration points
3. Use memory__remember_memory to store key findings
4. Identify next actions needed
EOF
    ;;
    
  "dependency-install")
    echo "📚 Installing Dependencies"
    /Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << EOF
Install and verify all dependencies:

1. Frontend:
   - cd frontend
   - Check package.json exists
   - Run: npm install
   - Verify: npm list

2. Backend:
   - cd backend  
   - Check requirements.txt exists
   - Run: pip install -r requirements.txt
   - Verify imports work

3. Document any issues found
4. Fix any dependency conflicts
EOF
    ;;
    
  "continuous-improvement")
    echo "♾️ Starting Continuous Improvement Cycle"
    /Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << EOF
Autonomous improvement cycle:

1. Analyze code quality:
   - Check for code duplication
   - Find unused imports
   - Identify refactoring opportunities

2. Improve documentation:
   - Add missing docstrings
   - Update outdated comments
   - Ensure README is current

3. Optimize performance:
   - Find slow functions
   - Optimize algorithms
   - Reduce bundle size

4. Create improvements on feature branch
5. Test all changes
6. Commit with clear messages

Work for 30 minutes then summarize improvements made.
EOF
    ;;
    
  "create-agent")
    AGENT_NAME=$2
    DOMAIN=$3
    echo "🤖 Creating Agent: $AGENT_NAME for domain: $DOMAIN"
    /Users/danielconnolly/bin/goose-smart session --with-builtin developer,memory << EOF
Create new autonomous agent:

1. Create backend/agents/${AGENT_NAME}_agent.py with:
   - Base agent class
   - Domain: $DOMAIN
   - Core methods for the domain
   - Integration with orchestrator

2. Create backend/agents/launch_${AGENT_NAME}.sh

3. Test the agent works

4. Add to orchestrator.py

5. Document in AGENTS.md
EOF
    ;;
    
  *)
    echo "❌ Unknown recipe: $RECIPE"
    echo ""
    echo "Available recipes:"
    echo "  - migrate-phase <number>"
    echo "  - test-and-fix"
    echo "  - analyze-codebase"
    echo "  - dependency-install"
    echo "  - continuous-improvement"
    echo "  - create-agent <name> <domain>"
    exit 1
    ;;
esac

echo ""
echo "✅ Recipe execution complete"
