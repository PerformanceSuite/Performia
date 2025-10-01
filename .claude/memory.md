# Performia Project Memory

## Project Identity
**Name**: Performia
**Purpose**: Revolutionary music performance system with AI-powered accompaniment and real-time Living Chart teleprompter
**Status**: Phase 3 - Core Development Agents (Infrastructure Complete)

## Key Technical Facts

### Architecture
- **Backend**: Python 3.12 + C++ (JUCE Framework)
- **Frontend**: React 19 + TypeScript 5 + Vite 6 + Tailwind CSS 4
- **Audio Engine**: JUCE for sub-10ms latency live performance
- **Data Format**: Song Map JSON (syllable-level timing with chords)

### Core Components
1. **Living Chart**: Real-time teleprompter that follows live performance
2. **Blueprint View**: Document-style editor for song structure
3. **Audio Pipeline**: ASR, beat detection, chord analysis, melody extraction
4. **AI Conductor**: Real-time performance following and accompaniment

### Directory Structure
```
Performia/
├── frontend/          # React + TypeScript UI
├── backend/           # Python services + JUCE audio engine
│   ├── src/services/  # Audio analysis services
│   ├── JuceLibraryCode/ # C++ audio engine
│   └── requirements.txt
├── shared/            # Shared types and utilities
├── tests/             # All test suites
├── scripts/           # Build/deploy scripts
├── config/            # Environment configs
└── .claude/           # Agent SDK configuration
```

## Current Development Phase

### Sprint 2: Schema Integration & Adapter Layer (ACTIVE)
**Dates:** October 1-7, 2024
**Active Agent:** `frontend-dev`
**Sprint Goal:** Enable seamless backend → frontend data flow via adapter layer

**See:** `SPRINT_ROADMAP.md` for full Q4 2024 - Q1 2025 roadmap

### Recent Changes (October 1, 2024)
- ✅ Sprint 1 COMPLETE: Backend realtime infrastructure (52/55 tests passing)
- ✅ Emergency stabilization: VIZTRITR artifacts removed, Living Chart restored
- ✅ Comprehensive sprint roadmap created (5 sprints through Q1 2025)
- ✅ Sprint status tracking system initialized (`.claude/sprint_status.md`)
- 🎯 Sprint 2 Day 1: Schema integration work begins

## Performance Targets
- **Audio Latency**: <10ms round-trip
- **UI Updates**: <50ms real-time refresh
- **Song Map Generation**: <30 seconds per song
- **Beat Detection Accuracy**: 95%+
- **Frame Rate**: Smooth 60fps animations

## Critical Files to Remember
- `SPRINT_ROADMAP.md` - Q4 2024 - Q1 2025 sprint plan (5 sprints)
- `.claude/sprint_status.md` - Daily sprint tracking and agent updates
- `RESTORATION_REPORT.md` - Sprint 1 completion report
- `backend/schemas/song_map.schema.json` - Backend Song Map schema
- `frontend/types.ts` - Frontend TypeScript definitions
- `.claude/CLAUDE.md` - Project context for agents

## Development Patterns
- Use Claude Agent SDK for autonomous development
- Test after every significant change
- Commit at logical checkpoints with descriptive messages
- Document architectural decisions in appropriate files

## Known Issues & Constraints
- None currently blocking development

## Next Actions (Sprint 2 - This Week)
1. **Day 1-2:** Analyze backend Song Map structure and design adapter algorithm
2. **Day 3-4:** Implement TypeScript adapter with comprehensive tests
3. **Day 5-6:** E2E integration testing and performance validation
4. **Day 7:** Documentation (ADR-001) and sprint review

**Agent to Invoke:** `frontend-dev` for all Sprint 2 stories

**Track Progress:** `.claude/sprint_status.md` (updated daily)

## Voice Integration (Planned)
- OpenAI Whisper API for speech-to-text
- Voice commands for development workflow
- Voice control during live performance
- Voice input for Song Map editing

## Sprint Overview (Q4 2024 - Q1 2025)
| Sprint | Dates | Focus | Agent | Status |
|--------|-------|-------|-------|--------|
| Sprint 1 | Sep 29 - Oct 1 | Backend Realtime + Emergency Stabilization | audio-pipeline-dev | ✅ COMPLETE |
| Sprint 2 | Oct 1-7 | Schema Integration & Adapter Layer | frontend-dev | 🟡 ACTIVE (Day 1) |
| Sprint 3 | Oct 8-21 | Performance & Quality Optimization | frontend-dev + audio-pipeline-dev | 📅 PLANNED |
| Sprint 4 | Oct 22 - Nov 4 | Production Readiness & Deployment | ALL | 📅 PLANNED |
| Sprint 5 | Nov 5-18 | Advanced Features (Voice Control) | voice-control + ALL | 📅 PLANNED |

---
*Last Updated*: October 1, 2024