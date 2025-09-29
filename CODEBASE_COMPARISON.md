# Performia Codebase Comparison Report

**Generated:** September 29, 2025  
**Purpose:** Migration Phase 1 - Repository Analysis & Backup

## Executive Summary

Two repositories need consolidation:
1. **Performia** - Backend-focused with Python, C++ audio engine, and older frontend
2. **Performia-front** - Modern React frontend with better UI implementation

## Repository Status

### Performia Repository
- **Location:** `/Users/danielconnolly/Projects/Performia`
- **Git Status:** Multiple uncommitted files (migration scripts, configs, agents)
- **Primary Focus:** Backend infrastructure, audio processing, ML/AI components

### Performia-front Repository  
- **Location:** `/Users/danielconnolly/Projects/Performia-front`
- **Git Status:** Some uncommitted files (node_modules, scripts)
- **Primary Focus:** Modern React frontend with Living Chart visualization

## Directory Structure Comparison

### Performia (Backend-Heavy)
```
Performia/
├── performia---living-chart/     # Older frontend (less developed)
├── JuceLibraryCode/             # C++ audio processing engine
├── src/                         # Backend source code
├── sc/                          # SuperCollider audio files
├── ingest-analyze-pipe/         # Data ingestion pipeline
├── resources/                   # Assets and configurations
├── tests/                       # Test suites
├── config/                      # Configuration files
├── memory/                      # Session/state management
├── Custom_MCP/                  # MCP server configurations
├── scripts/                     # Utility scripts
└── docs/                        # Documentation
```

### Performia-front (Frontend-Focused)
```
Performia-front/
└── performia---living-chart/     # Modern React frontend
    ├── src/                     # React source code
    ├── components/              # React components
    ├── services/                # API services (Library service)
    ├── hooks/                   # React hooks
    ├── utils/                   # Utility functions
    └── data/                    # Static data files
```

## Technology Stack Comparison

### Performia Backend Stack
- **Languages:** Python, C++, SuperCollider
- **Audio:** JUCE Framework (C++)
- **ML/AI:** Custom agents (performia_agent.py, orchestrator.py)
- **Data Pipeline:** ingest-analyze-pipe with schemas
- **Infrastructure:** MCP servers, Goose integration

### Performia-front Frontend Stack
- **Framework:** React 19.1.1 with TypeScript
- **Build Tool:** Vite 6.2.0
- **Styling:** Tailwind CSS 4.1.13
- **State Management:** Immer 10.1.3
- **Dev Tools:** PostCSS, Autoprefixer

### Common Frontend Dependencies
Both `performia---living-chart` directories have similar package.json, but Performia-front has:
- ✅ Tailwind CSS (missing in Performia)
- ✅ PostCSS and Autoprefixer
- ✅ More complete TypeScript configuration

## Unique Files Analysis

### Unique to Performia (Backend)
- **Audio Processing:**
  - JuceLibraryCode/* (C++ audio engine)
  - sc/synthdefs/* (SuperCollider definitions)
  
- **ML/AI Infrastructure:**
  - performia_agent.py
  - orchestrator.py
  - Custom_MCP/* (MCP server configs)
  
- **Data Pipeline:**
  - ingest-analyze-pipe/* (data ingestion)
  
- **Documentation:**
  - Performia UI PRD.md
  - CONTRIBUTING.md
  - LICENSE

### Unique to Performia-front
- **Modern Frontend Structure:**
  - components/icons/* (icon components)
  - hooks/* (React hooks)
  - services/* (API integration)
  - utils/* (utility functions)
  
- **Configuration:**
  - .env.local (environment variables)
  - tailwind.config.js
  - postcss.config.js
  - vite.config.ts (more complete)

## Configuration Differences

### Package.json Comparison
| Feature | Performia | Performia-front |
|---------|-----------|-----------------|
| React Version | 19.1.1 | 19.1.1 |
| TypeScript | 5.8.2 | 5.8.2 |
| Vite | 6.2.0 | 6.2.0 |
| Tailwind CSS | ❌ | ✅ 4.1.13 |
| PostCSS | ❌ | ✅ 8.5.6 |
| Autoprefixer | ❌ | ✅ 10.4.21 |

### Environment Variables
- **Performia:** Has .env.template (new, for migration)
- **Performia-front:** Has .env.local (active configuration)

## Migration Recommendations

### Phase 2 Actions Required
1. **Use Performia-front's frontend** as the base (better UI, Tailwind configured)
2. **Preserve all Performia backend** infrastructure
3. **Merge environment configurations** (.env.local + .env.template)
4. **Update import paths** in frontend to connect to backend

### Critical Files to Preserve
From **Performia**:
- All JuceLibraryCode/* (audio engine)
- All src/* (backend logic)
- performia_agent.py and orchestrator.py
- ingest-analyze-pipe/*
- All test suites

From **Performia-front**:
- All components/*, hooks/*, services/*, utils/*
- Tailwind and PostCSS configurations
- TypeScript configurations

### Potential Conflicts
1. **package.json** - Need to merge dependencies
2. **tsconfig.json** - May have different compiler options
3. **vite.config.ts** - Different build configurations
4. **.gitignore** - Need to combine exclusion rules

## Next Steps (Phase 2)

1. Create unified directory structure in Performia/
2. Move Performia-front/performia---living-chart/* → Performia/frontend/
3. Move Performia backend files → Performia/backend/
4. Merge configuration files
5. Update import paths and dependencies
6. Test integration between frontend and backend

## Backup Status

✅ Both repositories have local copies
⚠️ Uncommitted changes in both repos - need to commit or stash before major changes
📝 This comparison document serves as restoration reference

---
*End of Phase 1 Analysis Report*
