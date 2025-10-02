# Performia

**AI-Powered Music Performance System with Real-Time Analysis & Interactive Visualization**

## Overview

Performia is a revolutionary music performance platform that combines real-time audio analysis, AI-powered accompaniment, and an interactive "Living Chart" teleprompter interface. Musicians can perform songs while the system follows along in real-time, providing visual feedback and intelligent accompaniment.

## Key Features

- **Living Chart**: Real-time interactive performance visualization with syllable-level precision
- **Audio Analysis Pipeline**: ASR, beat detection, chord analysis, and melody extraction
- **Song Map Generation**: Precise timing maps with millisecond accuracy
- **JUCE Audio Engine**: Low-latency C++ audio processing for live performance
- **AI Orchestration**: Intelligent performance analysis and accompaniment
- **Library Management**: Comprehensive song library with search, sort, and tagging

## Project Structure

```
Performia/
├── frontend/                   # React + TypeScript + Vite
│   ├── src/
│   ├── components/             # Living Chart, Blueprint View
│   ├── services/               # Library service, WebSocket
│   └── package.json
│
├── backend/                    # Python + C++ backend
│   ├── src/services/
│   │   ├── asr/                # Automatic Speech Recognition
│   │   ├── beats_key/          # Beat and key detection
│   │   ├── chords/             # Chord analysis
│   │   ├── melody_bass/        # Melody extraction
│   │   ├── packager/           # Song Map generation
│   │   └── orchestrator/       # AI orchestration
│   ├── JuceLibraryCode/        # C++ JUCE audio engine
│   └── requirements.txt
│
├── shared/                     # Shared types & configuration
├── docs/                       # Documentation
├── scripts/                    # Build & deployment scripts
├── config/                     # Environment configuration
└── .claude/                    # Agent SDK configuration
```

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- Git

### Running Performia

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```
Backend runs on: `http://localhost:8000`

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: `http://localhost:5001`

### First-Time User Flow

1. Open `http://localhost:5001`
2. Demo song "Yesterday" loads automatically
3. Click Settings (gear icon) → Adjust font size, transpose
4. Click Play → Watch syllables highlight in real-time
5. Upload your own song → Wait ~30s for analysis → Perform!

## Technology Stack

### Frontend
- React 19
- TypeScript 5
- Vite 6
- Tailwind CSS 4
- Immer (state management)

### Backend
- Python 3.12
- JUCE (C++ audio)
- Librosa (audio analysis)
- Whisper (ASR)
- FastAPI

### Infrastructure
- Google Cloud Platform
- GitHub Actions CI/CD
- Claude Agent SDK for autonomous development

## Core Concepts

### Song Map
The Song Map is the central data structure that represents a song with precise timing information:

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

### Audio Pipeline
1. **Audio Input** → Analysis services (ASR, beats, chords, melody)
2. **Analysis Results** → Song Map generation
3. **Song Map** → Living Chart visualization
4. **Live Performance** → Real-time tracking and accompaniment

## Documentation

### Primary Documentation
- **[Complete Documentation](./PERFORMIA_MASTER_DOCS.md)** - Single source of truth for all Performia documentation
- **[Current Status](./docs/STATUS.md)** - Current sprint status, roadmap, and known issues

### Supplemental Docs
- [Project Context](./.claude/CLAUDE.md) - Claude Agent SDK configuration
- [Sprint 2 Report](./docs/sprint2/SPRINT2_COMPLETE.md) - Sprint 2 completion summary
- [AI Research](./docs/research/AI_MUSIC_AGENT_RESEARCH.md) - AI accompaniment research
- [Archived Docs](./docs/archive/) - Historical documentation and roadmaps

## Development

### Running Tests
```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
pytest
```

### Agent-Driven Development
This project uses the Claude Agent SDK for autonomous development:

```bash
# Start Claude Code
claude

# Example agent invocation
"Act as the frontend-dev agent and optimize Living Chart performance"
```

See `.claude/agents/` for available agents.

## Performance Targets

- **Audio Latency**: < 10ms for live performance
- **Animation**: 60fps in Living Chart
- **Song Map Generation**: < 30 seconds per song
- **Real-time Tracking**: Syllable-level precision

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](./LICENSE) for details.

## Links

- [GitHub Repository](https://github.com/PerformanceSuite/Performia)
- [Issue Tracker](https://github.com/PerformanceSuite/Performia/issues)

---

*Built with AI-assisted development using Claude Agent SDK*
