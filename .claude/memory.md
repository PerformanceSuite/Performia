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
**Status:** Ready for parallel development
**Split Work:** Backend (Claude) + Frontend (Daniel)

**Backend Track (Claude - Sprint 2):**
- Build TypeScript adapter (backend Song Map → frontend SongMap)
- Stories 1-12 in SPRINT_ROADMAP.md
- Track progress in `.claude/sprint_status.md`

**Frontend Track (Daniel - Parallel):**
- Review FRONTEND_UX_DESIGN_SPEC.md
- Implement accessibility improvements (Sprint 3 prep)
- Plan UX enhancements (double-tap, autocomplete)

### Recent Changes (October 1, 2024)
- ✅ Sprint 1 COMPLETE: Backend realtime (52/55 tests, 94.5% pass rate)
- ✅ Emergency stabilization: Living Chart restored, VIZTRITR removed
- ✅ Sprint roadmap created: 5 sprints through Q1 2025
- ✅ **FRONTEND UX SPEC COMPLETE**: 965-line definitive design doc
- ✅ Sprint tracking system ready (`.claude/sprint_status.md`)
- 🎯 Ready for parallel backend/frontend development

## Performance Targets
- **Audio Latency**: <10ms round-trip
- **UI Updates**: <50ms real-time refresh
- **Song Map Generation**: <30 seconds per song
- **Beat Detection Accuracy**: 95%+
- **Frame Rate**: Smooth 60fps animations

## Critical Files to Remember

### Planning & Roadmap
- `SPRINT_ROADMAP.md` - Q4 2024 - Q1 2025 sprint plan (5 sprints, 897 lines)
- `.claude/sprint_status.md` - Daily sprint tracking template
- `QUICKSTART_SPRINT2.md` - Sprint 2 getting started guide
- `RESTORATION_REPORT.md` - Sprint 1 completion report

### Design Specifications
- **`FRONTEND_UX_DESIGN_SPEC.md`** - Definitive UX spec (965 lines, COMPLETE)
  - User personas & workflows
  - Visual design system (colors, typography, spacing)
  - Detailed view specifications (Teleprompter, Blueprint, Library)
  - Accessibility requirements (WCAG AAA)
  - Performance targets (60fps, <100ms)
  - Component API reference

### Technical Schemas
- `backend/schemas/song_map.schema.json` - Backend Song Map schema
- `frontend/types.ts` - Frontend TypeScript definitions
- `.claude/CLAUDE.md` - Project context for agents

## Development Patterns
- Use Claude Agent SDK for autonomous development
- Test after every significant change
- Commit at logical checkpoints with descriptive messages
- Document architectural decisions in appropriate files

## Key Decisions Made (October 1, 2024)

### Architecture Decisions
1. **Schema Integration Strategy:** Adapter layer approach
   - Backend outputs time-series data (lyrics[], chords[], beats[])
   - Frontend needs hierarchical (sections → lines → syllables)
   - Solution: TypeScript adapter transforms backend → frontend
   - Location: `frontend/src/utils/songMapAdapter.ts`

2. **Parallel Development Model:** Split Sprint 2 work
   - Backend: Claude builds adapter (Stories 1-12)
   - Frontend: Daniel implements UX improvements from spec
   - Integration: End of Sprint 2 (E2E testing)

3. **UX Design Philosophy:** Performance-first, musician-focused
   - UI disappears during performance (fullscreen, zero chrome)
   - Emergency controls (double-tap for font adjust)
   - Accessibility AAA for lyrics, AA for UI
   - Target: <30s setup, <100ms interactions, 60fps

### Design Specifications Finalized
- FRONTEND_UX_DESIGN_SPEC.md: 965 lines, definitive
- 3 user personas with detailed workflows
- Complete visual design system (colors, typography, spacing)
- Performance targets: 60fps, <16ms highlight latency
- Accessibility: WCAG AAA for critical elements

## Known Issues & Constraints
- Schema mismatch resolved via adapter (in progress)
- VIZTRITR experiment archived (lesson learned)
- No blocking issues for Sprint 2 start

## Next Actions

### When Session Reopens

**First Command:**
```
"Act as the frontend-dev agent working on Sprint 2, Story 1:
Analyze Backend Song Map Structure.

Read backend/schemas/song_map.schema.json and
backend/output/*.song_map.json. Create analysis document
explaining transformation requirements for adapter layer.

Save analysis as docs/sprint2_backend_analysis.md"
```

### Sprint 2 Backend Work (Days 1-7)
1. **Days 1-2:** Analyze backend structure, design adapter algorithm
2. **Days 3-4:** Implement TypeScript adapter with tests (>90% coverage)
3. **Days 5-6:** E2E integration testing, performance validation
4. **Day 7:** Documentation (ADR-001), sprint review

**Agent:** `frontend-dev` handles all 12 stories
**Track:** `.claude/sprint_status.md` (update daily)

### Frontend Work (Daniel - Parallel)
1. Review FRONTEND_UX_DESIGN_SPEC.md thoroughly
2. Sketch mockups for critical workflows
3. Plan Sprint 3 accessibility improvements
4. Identify quick wins (contrast, focus indicators)

## Voice Integration (Planned)
- OpenAI Whisper API for speech-to-text
- Voice commands for development workflow
- Voice control during live performance
- Voice input for Song Map editing

## Sprint Overview (Q4 2024 - Q1 2025)
| Sprint | Dates | Focus | Work Split | Status |
|--------|-------|-------|------------|--------|
| Sprint 1 | Sep 29 - Oct 1 | Backend Realtime + Stabilization | audio-pipeline-dev | ✅ COMPLETE (52/55 tests) |
| **Sprint 2** | **Oct 1-7** | **Schema Integration & Adapter** | **Backend: frontend-dev agent<br/>Frontend: Daniel (UX spec)** | **🟡 READY TO START** |
| Sprint 3 | Oct 8-21 | Performance & Quality | frontend-dev + audio-pipeline-dev | 📅 PLANNED |
| Sprint 4 | Oct 22 - Nov 4 | Production Deployment | ALL agents | 📅 PLANNED |
| Sprint 5 | Nov 5-18 | Advanced Features | voice-control + ALL | 📅 PLANNED |

**Current Milestone:** Sprint 2 ready for parallel development

---
*Last Updated*: October 1, 2024