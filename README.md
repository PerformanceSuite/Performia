# Performia

**AI-Powered Music Performance System with Real-Time Analysis & Interactive Visualization**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

---

## Overview

Performia is a revolutionary music performance platform that combines real-time audio analysis, AI-powered accompaniment, and an interactive "Living Chart" teleprompter interface. Musicians can perform songs while the system follows along in real-time, providing visual feedback and intelligent audio processing.

**Core Value Proposition:** *"Never forget lyrics or chords again. Performia follows YOU in real-time."*

### Key Features

- **Living Chart** - Real-time interactive performance visualization with syllable-level precision
- **Audio Analysis Pipeline** - ASR, beat detection, chord analysis, and melody extraction
- **Song Map Generation** - Precise timing maps with millisecond accuracy
- **JUCE Audio Engine** - Low-latency C++ audio processing for live performance
- **AI Orchestration** - Intelligent performance analysis and accompaniment
- **Library Management** - Comprehensive song library with search, sort, and tagging
- **Knowledge Base RAG** - AI agent knowledge retrieval system to prevent recurring mistakes

---

## Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Git**
- **Docker** (optional, recommended for production)

### Installation

**Option 1: Quick Start (Recommended)**

```bash
# Clone the repository
git clone https://github.com/PerformanceSuite/Performia.git
cd Performia

# Install dependencies
pip install -r requirements.txt
cd frontend && npm install && cd ..

# Start backend
python backend/src/services/api/main.py

# In another terminal, start frontend
cd frontend && npm run dev
```

**Option 2: Docker**

```bash
# Run with Docker Compose (coming soon)
docker-compose up
```

For detailed installation instructions, see [INSTALLATION.md](./INSTALLATION.md).

### First-Time User Flow

1. **Open Performia** → Navigate to `http://localhost:5001`
2. **Demo Song Loads** → "Yesterday" by The Beatles loads automatically
3. **Adjust Settings** → Click Settings (gear icon) to adjust font size, transpose
4. **Play Demo** → Click Play and watch syllables highlight in real-time
5. **Upload Your Song** → Drop an audio file, wait ~30s for analysis
6. **Perform** → Fullscreen lyrics with chords, zero distractions

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     PERFORMIA SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐         ┌──────────────────────────┐    │
│  │   Frontend   │◄────────┤   Backend API Server     │    │
│  │  React + TS  │ WebSocket   FastAPI + Python       │    │
│  │  Vite + Tail │         │   http://localhost:8000  │    │
│  │  Port 5001   │         └──────────┬───────────────┘    │
│  └──────┬───────┘                    │                     │
│         │                            │                     │
│         │                   ┌────────▼────────┐            │
│  ┌──────▼──────────┐        │  Audio Pipeline │            │
│  │  Living Chart   │        ├─────────────────┤            │
│  │  Blueprint View │        │ • ASR (Whisper) │            │
│  │  Library        │        │ • Beat Detection│            │
│  └─────────────────┘        │ • Chord Analysis│            │
│                             │ • Melody Extract│            │
│                             │ • Demucs (Stems)│            │
│                             └────────┬────────┘            │
│                                      │                     │
│                             ┌────────▼────────┐            │
│                             │  Song Map JSON  │            │
│                             │  Packager       │            │
│                             └────────┬────────┘            │
│                                      │                     │
│                             ┌────────▼────────┐            │
│                             │  SQLite Job DB  │            │
│                             │  Output Storage │            │
│                             └─────────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend**
- React 19
- TypeScript 5
- Vite 6
- Tailwind CSS 4
- Immer (state management)

**Backend**
- Python 3.12
- FastAPI (REST API)
- Whisper (ASR)
- Librosa (audio analysis)
- Demucs (source separation)
- JUCE (C++ audio engine)

**Infrastructure**
- SQLite (job storage)
- Docling (RAG knowledge base)
- ChromaDB (vector storage)
- Google Cloud Platform (deployment)
- GitHub Actions (CI/CD)
- Claude Agent SDK (autonomous development)

### Core Data Structure: Song Map

The Song Map is the central data structure representing a song with precise timing:

```json
{
  "title": "Yesterday",
  "artist": "The Beatles",
  "key": "F",
  "tempo": 90,
  "sections": [
    {
      "name": "Verse 1",
      "startTime": 0.0,
      "lines": [
        {
          "syllables": [
            {
              "text": "Yes",
              "startTime": 0.5,
              "duration": 0.3,
              "chord": "F",
              "pitch": 65.4
            },
            {
              "text": "ter",
              "startTime": 0.8,
              "duration": 0.2,
              "chord": "F",
              "pitch": 69.3
            },
            {
              "text": "day",
              "startTime": 1.0,
              "duration": 0.4,
              "chord": "Em7",
              "pitch": 67.8
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Project Structure

```
Performia/
├── frontend/                   # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/         # Living Chart, Blueprint View
│   │   ├── services/           # Library service, WebSocket
│   │   ├── hooks/              # React hooks
│   │   └── types.ts            # TypeScript definitions
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                    # Python + C++ backend
│   ├── src/services/
│   │   ├── asr/                # Automatic Speech Recognition
│   │   ├── beats_key/          # Beat and key detection
│   │   ├── chords/             # Chord analysis
│   │   ├── melody_bass/        # Melody extraction
│   │   ├── separation/         # Demucs stem separation
│   │   ├── structure/          # Song structure detection
│   │   ├── packager/           # Song Map generation
│   │   ├── orchestrator/       # AI orchestration
│   │   └── api/                # REST API server
│   ├── JuceLibraryCode/        # C++ JUCE audio engine
│   └── requirements.txt
│
├── shared/                     # Shared types & configuration
│   ├── schemas/                # Song Map schema definitions
│   └── config/                 # Environment configuration
│
├── knowledge-base/             # RAG knowledge base
│   ├── audio-dsp/              # DSP research
│   ├── frameworks/             # JUCE, SuperCollider docs
│   └── project/                # Project-specific knowledge
│
├── scripts/                    # Build & deployment scripts
│   ├── check_docling.py        # Verify RAG dependencies
│   └── generate_secrets.py     # Generate secure secrets
│
├── docs/                       # Documentation
│   ├── INSTALLATION.md         # Setup instructions
│   ├── USAGE.md                # User guide
│   ├── ARCHITECTURE.md         # Technical architecture
│   ├── API.md                  # API reference
│   └── CONTRIBUTING.md         # Development guide
│
├── .claude/                    # Agent SDK configuration
│   ├── CLAUDE.md               # Project context
│   └── agents/                 # Specialized agents
│
├── .env.template               # Environment variables template
├── requirements.txt            # Python dependencies
├── knowledge_rag.py            # RAG knowledge base system
└── README.md                   # This file
```

---

## Documentation

### Primary Documentation
- **[Installation Guide](./INSTALLATION.md)** - Detailed setup instructions
- **[Usage Guide](./USAGE.md)** - Step-by-step user guide
- **[Architecture](./ARCHITECTURE.md)** - System design and technical details
- **[API Reference](./API.md)** - Complete API documentation
- **[Contributing Guide](./CONTRIBUTING.md)** - Development guidelines

### Supplemental Docs
- **[Master Documentation](./PERFORMIA_MASTER_DOCS.md)** - Complete system documentation
- **[Project Context](./.claude/CLAUDE.md)** - Claude Agent SDK configuration
- **[Sprint 2 Report](./docs/sprint2/SPRINT2_COMPLETE.md)** - Sprint 2 completion summary
- **[AI Research](./docs/research/AI_MUSIC_AGENT_RESEARCH.md)** - AI accompaniment research

---

## Performance Targets

- **Audio Latency**: < 10ms for live performance
- **Animation**: 60fps in Living Chart
- **Song Map Generation**: < 30 seconds per song
- **Real-time Tracking**: Syllable-level precision
- **API Response Time**: < 100ms for status checks

---

## Development

### Running Tests

```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
pytest

# Run specific test
pytest tests/test_pipeline.py::test_full_pipeline
```

### Agent-Driven Development

This project uses the Claude Agent SDK for autonomous development:

```bash
# Start Claude Code
claude

# Example agent invocation
"Act as the frontend-dev agent and optimize Living Chart performance"
```

Available agents:
- **frontend-dev** - Frontend development and optimization
- **audio-pipeline-dev** - Audio analysis pipeline
- **voice-control** - Voice command integration

See `.claude/agents/` for all available agents.

### Development Workflow

1. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
2. **Make Changes**: Follow code style guidelines
3. **Run Tests**: Ensure all tests pass
4. **Commit Changes**: `git commit -m 'Add amazing feature'`
5. **Push Branch**: `git push origin feature/amazing-feature`
6. **Create Pull Request**: Open PR with detailed description

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

### Code Style

- **Python**: Follow PEP 8, use type hints
- **TypeScript**: Use strict mode, prefer functional components
- **Git Commits**: Use conventional commits (feat:, fix:, docs:, etc.)

---

## Roadmap

### Current Sprint (Sprint 3)
- Enhanced Living Chart performance
- Voice control integration
- Real-time performance tracking

### Upcoming Features
- Multi-user collaboration
- Cloud song library
- Mobile app (iOS/Android)
- Hardware integration (MIDI controllers)
- AI-generated accompaniment

See [docs/STATUS.md](./docs/STATUS.md) for current status.

---

## License

MIT License - see [LICENSE](./LICENSE) for details.

---

## Links

- **GitHub Repository**: [github.com/PerformanceSuite/Performia](https://github.com/PerformanceSuite/Performia)
- **Issue Tracker**: [github.com/PerformanceSuite/Performia/issues](https://github.com/PerformanceSuite/Performia/issues)
- **Documentation**: [Complete Docs](./PERFORMIA_MASTER_DOCS.md)

---

## Support

For questions, issues, or feature requests:

- **Issues**: [GitHub Issues](https://github.com/PerformanceSuite/Performia/issues)
- **Discussions**: [GitHub Discussions](https://github.com/PerformanceSuite/Performia/discussions)

---

## Acknowledgments

- **OpenAI Whisper** - Speech recognition
- **Meta Demucs** - Source separation
- **JUCE Framework** - Audio processing
- **Anthropic Claude** - AI-assisted development

---

*Built with AI-assisted development using Claude Agent SDK*
