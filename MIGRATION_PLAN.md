# Performia Unified Codebase Migration Plan

**Date:** September 29, 2025  
**Goal:** Merge Performia and Performia-front into a single unified repository with one GitHub repo and one Google Cloud project

## Objectives

1. Consolidate two codebases (Performia + Performia-front) into Performia/
2. Use the better frontend from Performia-front
3. Maintain all backend infrastructure from Performia
4. Single GitHub repository
5. Single Google Cloud project
6. Setup 24/7 agentic compute-maxing workflow

## Pre-Migration Checklist

- [ ] Verify Goose MCP servers are functional
- [ ] Enable Goose memory extension for persistent context
- [ ] Create backup of both repositories
- [ ] Verify GitHub and GCP credentials
- [ ] Document current state of both repos

## Phase 1: Repository Analysis & Backup

**Executor: Goose CLI**

```bash
# Analyze current state
goose session start --profile migration

# In Goose session:
analyze the directory structure of /Users/danielconnolly/Projects/Performia and /Users/danielconnolly/Projects/Performia-front
identify all differences between the two performia---living-chart directories
create a detailed comparison report in /Users/danielconnolly/Projects/Performia/CODEBASE_COMPARISON.md
```

**Tasks:**
- [ ] Compare directory structures
- [ ] Identify duplicate files
- [ ] Document unique files in each repo
- [ ] Identify configuration differences
- [ ] Check for uncommitted changes in both repos
- [ ] Create backup branches

## Phase 2: Create Unified Structure

**Executor: Goose CLI**

**Target Structure:**
```
Performia/
├── backend/                    # From Performia/
│   ├── src/
│   ├── JuceLibraryCode/       # C++ audio engine
│   ├── config/
│   ├── scripts/
│   ├── requirements.txt
│   └── README.md
├── frontend/                   # From Performia-front/performia---living-chart
│   ├── src/
│   ├── components/
│   ├── services/              # Library service, etc.
│   ├── package.json
│   └── README.md
├── shared/                     # Shared types and interfaces
│   ├── types/
│   └── interfaces/
├── .github/                    # CI/CD workflows
│   └── workflows/
├── docs/                       # Unified documentation
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   └── API.md
├── scripts/                    # Build and deployment
│   ├── setup.sh
│   ├── dev.sh
│   └── deploy.sh
├── .goosehints                 # Goose context hints
├── docker-compose.yml          # Local development
├── package.json               # Root package.json for monorepo
└── README.md                   # Main project README
```

**Goose Tasks:**
```bash
# Create new structure
create directory structure as specified above in Performia/

# Move backend files (already in place, just reorganize)
move all Python backend code to backend/src/
move JUCE code to backend/JuceLibraryCode/ (already there)
consolidate backend scripts to backend/scripts/

# Move frontend files from Performia-front
copy the entire performia---living-chart directory from Performia-front to Performia/frontend/
ensure all node_modules are excluded
copy package.json, tsconfig.json, vite.config.ts

# Create shared types
identify common types between backend and frontend
extract shared types to shared/types/
update imports in both backend and frontend
```

**Tasks:**
- [ ] Create unified directory structure
- [ ] Move backend code into backend/
- [ ] Copy improved frontend from Performia-front
- [ ] Extract shared types to shared/
- [ ] Update all import paths

## Phase 3: Dependency Management

**Executor: Goose CLI**

```bash
# Frontend dependencies
cd /Users/danielconnolly/Projects/Performia/frontend
merge dependencies from both package.json files
ensure Tailwind, React, and all services are included
run npm install to verify

# Backend dependencies  
cd /Users/danielconnolly/Projects/Performia/backend
verify all Python dependencies in requirements.txt
ensure JUCE dependencies are documented

# Root monorepo setup
create root package.json with workspaces
add scripts for running both frontend and backend
```

**Tasks:**
- [ ] Merge frontend package.json files
- [ ] Install and verify frontend dependencies
- [ ] Verify backend requirements.txt
- [ ] Create root package.json with workspaces
- [ ] Test dev scripts

## Phase 4: Configuration Consolidation

**Executor: Goose CLI**

**Files to consolidate:**
- `.env.template` files
- GitHub workflows
- Docker configurations
- API configurations
- Build scripts

```bash
# Merge environment configs
create unified .env.template combining both projects
document all required API keys (Gemini, Anthropic, GCP, etc.)

# GitHub repository consolidation
verify current git remotes
create new branch 'unified-migration'
prepare to archive Performia-front repo

# GCP Project setup
document current GCP resources from both projects
create migration plan for GCP resources
```

**Tasks:**
- [ ] Create unified .env.template
- [ ] Consolidate Git configuration
- [ ] Merge .gitignore files
- [ ] Setup GitHub Actions workflow
- [ ] Document GCP migration steps

## Phase 5: Git & GitHub Migration

**Executor: Goose CLI**

```bash
# In Performia directory
create new branch 'unified-migration'
commit all new structure changes
verify .gitignore excludes node_modules, build artifacts, etc.

# GitHub operations
verify Performia GitHub repo URL
prepare to push unified codebase
create migration documentation in repo
```

**Tasks:**
- [ ] Create migration branch
- [ ] Commit unified structure
- [ ] Push to GitHub
- [ ] Update GitHub repo description
- [ ] Archive Performia-front repo
- [ ] Update README with new structure

## Phase 6: Google Cloud Project Consolidation

**Executor: Goose + Manual Review**

```bash
# Audit GCP resources
list all resources in both GCP projects
identify which resources belong to Performia
create migration checklist for GCP resources

# Document new GCP setup
create GCP deployment guide
setup Cloud Build for CI/CD
configure Cloud Run or App Engine for hosting
```

**Tasks:**
- [ ] List all GCP resources from both projects
- [ ] Choose primary GCP project
- [ ] Migrate/recreate necessary resources
- [ ] Update API keys and service accounts
- [ ] Test GCP deployments
- [ ] Archive old GCP project

## Phase 7: Testing & Validation

**Executor: Goose CLI**

```bash
# Frontend testing
cd frontend
npm run dev
verify all components load correctly
test Living Chart functionality
verify Library service works

# Backend testing
cd backend
verify Python scripts run
test JUCE audio engine compilation
verify API endpoints

# Integration testing
verify frontend can communicate with backend
test end-to-end workflows
```

**Tasks:**
- [ ] Test frontend locally
- [ ] Test backend locally
- [ ] Test frontend-backend integration
- [ ] Verify all environment variables
- [ ] Test build process
- [ ] Run existing test suites

## Phase 8: Compute Maxing Setup (Agentic Workflow)

**Executor: Goose CLI + Custom Scripts**

Per the whitepaper - setup "living software that works while you sleep":

```bash
# Create 24/7 monitoring agents
setup GitHub Actions for continuous testing
create Goose recipes for automated code review
setup automated dependency updates
configure performance monitoring

# Agentic development workflow
create .goosehints file with project context
setup Goose sessions for different workflows:
  - Feature development
  - Bug fixing  
  - Performance optimization
  - Documentation
```

**Tasks:**
- [ ] Setup GitHub Actions CI/CD
- [ ] Create Goose recipes for common tasks
- [ ] Configure automated testing
- [ ] Setup code quality monitoring
- [ ] Create .goosehints with project context
- [ ] Document agentic workflow patterns

## Phase 9: Documentation & Handoff

**Executor: You + Goose CLI**

```bash
# Generate documentation
create comprehensive README.md
document architecture in ARCHITECTURE.md
update PRD with unified structure
create developer onboarding guide
document agentic workflow usage
```

**Tasks:**
- [ ] Update main README.md
- [ ] Create ARCHITECTURE.md
- [ ] Update PRD location
- [ ] Create CONTRIBUTING.md
- [ ] Document Goose usage
- [ ] Create troubleshooting guide

## Phase 10: Cleanup

**Executor: Goose CLI**

```bash
# Clean up old artifacts
remove duplicate files
verify no broken imports
clean up old branches
update all documentation references
```

**Tasks:**
- [ ] Remove Performia-front directory (after backup)
- [ ] Clean up unused files
- [ ] Remove old configuration files
- [ ] Verify no broken links in docs
- [ ] Tag release: v1.0-unified

## Success Criteria

- [ ] All frontend features working from new location
- [ ] All backend services operational
- [ ] Single GitHub repository active
- [ ] Single GCP project configured
- [ ] CI/CD pipeline operational
- [ ] Documentation complete
- [ ] Goose can navigate and modify codebase
- [ ] 24/7 compute-maxing agents active

## Rollback Plan

If migration fails:
1. Both original directories remain intact until Phase 10
2. Git branches allow easy revert
3. GCP resources duplicated, not moved initially
4. Can return to original setup at any checkpoint

## Goose CLI Commands Reference

```bash
# Start migration session
goose session start --profile migration

# Load this plan into Goose context
goose session load MIGRATION_PLAN.md

# Execute a phase
goose session resume --continue-from "Phase 2"

# Review progress
goose session status

# Commit checkpoint
goose session checkpoint "Completed Phase 3"
```

## Next Steps

1. **Enable Goose Memory Extension** - for persistent context across sessions
2. **Run Phase 1** - Let Goose analyze both codebases
3. **Review Goose's analysis** - Approve migration approach
4. **Execute Phases 2-5** - Let Goose do the heavy lifting
5. **Manual review at checkpoints** - Verify critical changes
6. **Test thoroughly** - Phase 7
7. **Setup compute maxing** - Phase 8

---

**Notes:**
- Goose will execute most tasks autonomously
- Human review required at phase transitions
- Keep both original directories until Phase 10
- Document any deviations from plan
