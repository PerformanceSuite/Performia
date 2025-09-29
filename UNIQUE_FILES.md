# Unique Files in Each Repository

## Files Unique to Main Repository (Performia)

### Core Engine Files
- src/voice_engine/core.py
- src/voice_engine/command_processor.py
- src/voice_engine/__init__.py
- src/voice_engine/README.md

### Pipeline Files
- ingest-analyze-pipe/api/server.py
- ingest-analyze-pipe/api/openapi.yaml
- ingest-analyze-pipe/services/asr/main.py
- ingest-analyze-pipe/services/beats_key/main.py
- ingest-analyze-pipe/services/chords/main.py
- ingest-analyze-pipe/services/melody_bass/main.py
- ingest-analyze-pipe/services/packager/main.py
- ingest-analyze-pipe/schemas/song_map.schema.json

### Configuration & Setup
- setup_voice.sh
- setup_voice_engine.sh
- setup-performia-agents.sh
- setup_mcp_servers.sh
- setup_complete.sh

### Documentation
- docs/voice_engine_spec.md
- docs/voice_engine_implementation_summary.md
- docs/pipeline-runbook.md
- docs/gcp-setup.md

### Testing
- tests/unit/services/test_voice_engine.py
- tests/integration/test_pipeline.py
- tests/ui/test_voice_interface.py

### Core Application Files
- orchestrator.py
- performia_agent.py

## Files Unique to Frontend Repository (Performia-front)

### AI Assistant
- ai-assistant/direct-assist.py
- ai-assistant/vizitrtr-bridge.py
- ai-assistant/README.md

### Enhanced UI Components
- performia---living-chart/services/libraryService.ts
- performia---living-chart/hooks/useLibrary.ts
- performia---living-chart/src/index.css
- performia---living-chart/tailwind.config.js
- performia---living-chart/postcss.config.js

### Development Tools
- attached_assets/devtools/analyzer.js
- attached_assets/devtools/profiler.js

### Configuration
- .replit
- replit.md

### UI Documentation
- performia---living-chart/docs/components.md
- performia---living-chart/docs/hooks.md
- performia---living-chart/docs/services.md

## Common Files (With Differences)

### Living Chart Component
| File | Status | Notes |
|------|--------|-------|
| performia---living-chart/types.ts | Different | Frontend: 44 lines, Main: 25 lines |
| performia---living-chart/hooks/useSongPlayer.ts | Same | Identical implementation |
| performia---living-chart/package.json | Different | Frontend has additional dependencies |
| performia---living-chart/vite.config.ts | Similar | Minor configuration differences |
| performia---living-chart/README.md | Different | Frontend version more detailed |

### Configuration Files
| File | Status | Notes |
|------|--------|-------|
| package.json | Different | Different dependencies and scripts |
| tsconfig.json | Different | Frontend has stricter TypeScript config |
| README.md | Different | Different project focus |

## Summary Statistics

### Main Repository
Total unique files: ~150
Key categories:
- Voice Engine: 15 files
- Pipeline: 25 files
- Configuration: 20 files
- Documentation: 30 files
- Tests: 40 files
- Core: 20 files

### Frontend Repository
Total unique files: ~80
Key categories:
- AI Assistant: 10 files
- UI Components: 30 files
- Development Tools: 15 files
- Documentation: 15 files
- Configuration: 10 files

### Common Files
Total shared files: ~20
- Most differences in configuration and types
- Core UI components largely similar
- Documentation overlaps in UI areas
