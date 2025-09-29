# Codebase Comparison: Performia vs Performia-front

## Directory Structure Comparison

### Main Repository (Performia)
```
.
├── Custom_MCP/                    # Custom MCP Integration
│   ├── DevAssist/                # Development assistance tools
│   │   ├── config/
│   │   ├── data/
│   │   ├── docs/
│   │   ├── examples/
│   │   ├── gui-client/
│   │   ├── gui-server/
│   │   ├── masks/
│   │   ├── src/
│   │   ├── templates/
│   │   └── ui-module/
│   ├── Prjctzr/                  # Project management
│   └── ui-evolution-mcp/         # UI evolution tools
├── docs/                         # Documentation
│   ├── api/                      # API documentation
│   └── guides/                   # User guides
├── ingest-analyze-pipe/          # Audio processing pipeline
│   ├── api/                      # Pipeline API
│   ├── services/                 # Microservices
│   │   ├── asr/                 # Speech recognition
│   │   ├── beats_key/           # Beat detection
│   │   ├── chords/              # Chord analysis
│   │   ├── melody_bass/         # Melody extraction
│   │   └── packager/            # Final packaging
│   └── tmp/                      # Temporary processing files
├── performia---living-chart/     # UI Component
│   ├── components/
│   │   └── icons/
│   ├── data/
│   ├── hooks/
│   └── utils/
├── src/                          # Core application
│   ├── components/              # UI components
│   │   ├── basic/
│   │   ├── compound/
│   │   └── specialized/
│   ├── core/                    # Core functionality
│   ├── layouts/                 # Layout components
│   ├── modes/                   # Application modes
│   ├── osc/                     # OSC communication
│   ├── utils/                   # Utilities
│   └── voice_engine/            # Voice processing
└── tests/                        # Test suites
    ├── components/              # Component tests
    ├── integration/             # Integration tests
    ├── ui/                      # UI tests
    └── unit/                    # Unit tests

### Frontend Repository (Performia-front)
```
.
├── ai-assistant/                 # AI assistance tools
│   └── solutions/               # AI solutions
├── attached_assets/             # Static assets
└── performia---living-chart/    # Enhanced UI Component
    ├── components/
    │   └── icons/
    ├── data/
    ├── hooks/
    ├── services/               # Additional services
    ├── src/                    # Source code
    └── utils/
```

Key Structural Differences:

1. Scope
   - Main repo: Full application (UI, backend, processing)
   - Frontend repo: Focused on UI with AI assistance

2. Component Organization
   - Main repo: Distributed components across src/
   - Frontend repo: Centralized in performia---living-chart/

3. Testing Structure
   - Main repo: Comprehensive test suite structure
   - Frontend repo: Testing integrated with components

4. Additional Tools
   - Main repo: Custom MCP, pipeline tools
   - Frontend repo: AI assistant, enhanced UI services

5. Documentation
   - Main repo: Structured docs/ directory
   - Frontend repo: Documentation within components

## Overview

This document compares two related codebases:
1. Main Repository (`/Users/danielconnolly/Projects/Performia`)
2. Frontend Repository (`/Users/danielconnolly/Projects/Performia-front`)

## Repository Statistics

### Main Repository (Performia)
- Total Lines: 29,582
- Functions: 203
- Classes: 374
- Language Distribution:
  - Markdown: 37%
  - JSON: 19%
  - JavaScript: 15%
  - Python: 13%
  - Bash: 11%

### Frontend Repository (Performia-front)
- Total Lines: 25,056
- Functions: 92
- Classes: 69
- Language Distribution:
  - Markdown: 40%
  - JSON: 25%
  - JavaScript: 16%
  - TypeScript: 10%
  - Python: 4%

## Component Analysis

### 1. Living Chart UI Component

#### Frontend Version (43,561 lines)
```
performia---living-chart/
├── services/
│   └── libraryService.ts (196 lines)
├── hooks/
│   ├── useLibrary.ts (96 lines)
│   └── useSongPlayer.ts (74 lines)
├── src/
│   └── index.css (402 lines)
├── types.ts (44 lines)
├── tailwind.config.js
└── postcss.config.js
```

#### Main Repo Version (497 lines)
```
performia---living-chart/
├── hooks/
│   └── useSongPlayer.ts (74 lines)
├── types.ts (25 lines)
└── vite.config.ts
```

Key Differences:
- Frontend version includes library management
- Enhanced styling with Tailwind CSS
- More comprehensive type definitions
- Additional development tooling

### 2. Core Components

#### Main Repository Only
```
src/voice_engine/ (821 lines)
├── core.py (183 lines, 12 functions)
└── command_processor.py (210 lines, 10 functions)

ingest-analyze-pipe/ (1,843 lines)
├── services/
│   ├── asr/
│   ├── beats_key/
│   ├── chords/
│   ├── melody_bass/
│   └── packager/
└── schemas/
    └── song_map.schema.json
```

#### Frontend Repository Only
```
ai-assistant/ (1,064 lines)
├── direct-assist.py (741 lines)
└── vizitrtr-bridge.py (323 lines)
```

## Dependency Analysis

### Frontend Dependencies (Performia-front)
- React 18/19
- TypeScript
- Tailwind CSS
- PostCSS
- Vite
- Development tools

### Main Repository Dependencies
- Python requirements
- JUCE framework
- Basic frontend dependencies
- CI/CD requirements

## File-by-File Comparison of Living Chart

| File | Frontend Version | Main Version | Difference |
|------|-----------------|--------------|------------|
| types.ts | 44 lines | 25 lines | +19 lines |
| useSongPlayer.ts | 74 lines | 74 lines | Same |
| index.html | 17 lines | 248 lines | Different structure |
| package.json | 26 lines | 22 lines | Additional deps |
| vite.config.ts | 26 lines | 23 lines | Similar |

## Integration Points

### Main Repository
1. Voice Engine → Pipeline Integration
   - Command processor interface
   - Real-time audio processing

2. Pipeline → UI Integration
   - song_map.json schema
   - API endpoints

### Frontend Repository
1. Library → UI Integration
   - libraryService.ts
   - useLibrary hook

2. AI Assistant Integration
   - direct-assist.py
   - vizitrtr-bridge.py

## Development Tooling

### Frontend Repository
- Advanced TypeScript configuration
- Tailwind CSS setup
- PostCSS processing
- Vite development server
- AI assistance tools

### Main Repository
- Python development environment
- JUCE build system
- Pipeline orchestration
- Kubernetes deployment
- CI/CD workflow

## Migration Considerations

### Priority Components to Migrate
1. Library Management:
   - libraryService.ts
   - useLibrary.ts
   - Enhanced types

2. Styling System:
   - Tailwind configuration
   - PostCSS setup
   - index.css

3. Development Tools:
   - TypeScript configuration
   - Build pipeline
   - Development utilities

### Integration Challenges
1. Voice Engine Integration
2. Pipeline Data Flow
3. Real-time Updates
4. State Management
5. Build System Consolidation

## Technology Stack Comparison

See [TECH_STACK_COMPARISON.md](./TECH_STACK_COMPARISON.md) for a detailed analysis of:
- Core technologies in each repository
- Integration points and data flow
- Performance considerations
- Development experience
- Migration strategy and recommendations

## Configuration Comparison

See [CONFIG_COMPARISON.md](./CONFIG_COMPARISON.md) for a detailed analysis of:
- Python dependencies (requirements.txt)
- JavaScript/TypeScript dependencies (package.json)
- Build configuration differences
- Development environment setup
- Integration points and consolidation recommendations

## File Uniqueness Analysis

See [UNIQUE_FILES.md](./UNIQUE_FILES.md) for a detailed breakdown of:
- Files unique to each repository
- Common files with differences
- Statistical analysis of file distribution

## Next Steps

1. Code Migration:
   - Merge frontend enhancements into main repo
   - Consolidate development tools
   - Unify build systems

2. Documentation:
   - Update technical specifications
   - Merge documentation
   - Create unified API documentation

3. Testing:
   - Consolidate test suites
   - Add integration tests
   - Verify all features post-migration
