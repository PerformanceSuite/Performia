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

### Phase 3: Core Development Agents (ACTIVE)
**Priority Agents to Build**:
1. **Frontend Development Agent** - Living Chart/Blueprint View improvements
2. **Audio Pipeline Agent** - Song Map generation optimization
3. **Voice Control Agent** - Whisper API integration

### Recent Changes
- ✅ Committed cleanup of 161 old migration files (Sep 30, 2024)
- ✅ Removed duplicate directories: performia/, performia---living-chart/, sdk-agents/
- ✅ Cleaned root directory clutter
- ✅ Git state is clean

## Performance Targets
- **Audio Latency**: <10ms round-trip
- **UI Updates**: <50ms real-time refresh
- **Song Map Generation**: <30 seconds per song
- **Beat Detection Accuracy**: 95%+
- **Frame Rate**: Smooth 60fps animations

## Critical Files to Remember
- `backend/schemas/song_map.schema.json` - Song Map schema definition
- `frontend/src/types.ts` - TypeScript type definitions
- `frontend/services/libraryService.ts` - Song library management
- `.claude/CLAUDE.md` - Project context for agents
- `AGENT_ROADMAP.md` - Agent development plan

## Development Patterns
- Use Claude Agent SDK for autonomous development
- Test after every significant change
- Commit at logical checkpoints with descriptive messages
- Document architectural decisions in appropriate files

## Known Issues & Constraints
- None currently blocking development

## Next Actions
1. Create Frontend Development Agent definition file
2. Test agent with Living Chart performance improvements
3. Build out Audio Pipeline and Voice Control agents
4. Establish CI/CD automation

## Voice Integration (Planned)
- OpenAI Whisper API for speech-to-text
- Voice commands for development workflow
- Voice control during live performance
- Voice input for Song Map editing

---
*Last Updated*: September 30, 2024