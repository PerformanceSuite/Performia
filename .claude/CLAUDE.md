# Performia Project Context

## Project Overview
Performia is a revolutionary music performance system that combines real-time audio analysis, AI-powered accompaniment, and an interactive "Living Chart" teleprompter interface.

## Current Status: Codebase Unification
We are merging two repositories into one unified codebase:
- **Main repo**: `/Users/danielconnolly/Projects/Performia` (backend + older frontend)
- **Frontend repo**: `/Users/danielconnolly/Projects/Performia-Front` (enhanced Living Chart UI)

## Architecture

### Backend (Python + C++)
- **Audio Pipeline**: ASR, beat detection, chord analysis, melody extraction
- **Song Map Generation**: Precise timing maps with syllable-level accuracy
- **JUCE Audio Engine**: Low-latency C++ audio processing for live performance
- **Services**: Located in `backend/src/services/`
  - `asr/` - Automatic Speech Recognition
  - `beats_key/` - Beat and key detection
  - `chords/` - Chord analysis
  - `melody_bass/` - Melody and bassline extraction
  - `packager/` - Song Map packaging
  - `orchestrator/` - AI orchestration

### Frontend (React + TypeScript + Vite)
- **Living Chart**: Real-time teleprompter that follows live performance
- **Blueprint View**: Document-style editor for song structure
- **Library Service**: Song management with search/sort/tags
- **Tech Stack**: React 19, TypeScript 5, Vite 6, Tailwind CSS 4

### Core Data Structure: Song Map
```json
{
  "title": "Song Title",
  "artist": "Artist Name",
  "sections": [
    {
      "name": "Verse 1",
      "lines": [
        {
          "syllables": [
            {
              "text": "Hello",
              "startTime": 0.5,
              "duration": 0.3,
              "chord": "C"
            }
          ]
        }
      ]
    }
  ]
}
```

## Target Structure
```
Performia/
├── frontend/                   # Enhanced UI from Performia-Front
│   ├── src/
│   ├── components/
│   ├── services/              # Library service, etc.
│   └── package.json
├── backend/                    # Python + C++ backend
│   ├── src/services/
│   ├── JuceLibraryCode/       # C++ audio engine
│   └── requirements.txt
├── shared/                     # Shared types/interfaces
└── .claude/                    # Agent SDK configuration
```

## Key Technical Requirements

### Performance
- **Sub-10ms audio latency** for live performance
- Smooth 60fps animations in Living Chart
- Real-time syllable highlighting

### Data Flow
1. Audio file → Analysis Pipeline → Song Map JSON
2. Song Map → Living Chart → Real-time display
3. Live audio input → AI Conductor → Follow performer

### Critical Files
- `backend/schemas/song_map.schema.json` - Song Map schema
- `frontend/src/types.ts` - TypeScript definitions
- `frontend/services/libraryService.ts` - Library management
- `backend/src/services/packager/` - Song Map generation

## Development Workflow
- Use Claude Agent SDK for autonomous development
- Run tests after every change
- Create git commits at logical checkpoints
- Document all architectural decisions

## Migration Priorities
1. Copy enhanced frontend from Performia-Front
2. Merge dependencies (package.json, requirements.txt)
3. Update import paths
4. Ensure Living Chart functionality
5. Verify Song Map pipeline
6. Test end-to-end workflow

## Voice Integration (Future)
- Whisper API for voice commands
- Voice control for development workflow
- Voice input for Song Map editing
