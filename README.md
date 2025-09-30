# Performia - Unified Platform

**Interactive Performance Management Platform with Living Chart Visualization**

## 🎯 Overview

Performia is a comprehensive performance management platform that combines:
- **Modern React Frontend** - Interactive Living Chart visualization with Tailwind CSS
- **Powerful Python Backend** - Audio processing, ML/AI agents, and data pipeline
- **C++ Audio Engine** - JUCE-based low-latency audio processing
- **24/7 Autonomous Agents** - Compute-maxing with Goose and custom MCP servers

## 📁 Project Structure

```
Performia/
├── frontend/                  # React + TypeScript + Vite
│   ├── src/                  # React components & services
│   ├── components/           # Living Chart, Blueprint View
│   ├── services/             # Library service, WebSocket
│   └── package.json          # Frontend dependencies
│
├── backend/                   # Python + C++ backend
│   ├── src/
│   │   ├── services/         # Audio analysis services
│   │   │   ├── asr/          # Speech recognition
│   │   │   ├── beats_key/    # Beat & key detection
│   │   │   ├── chords/       # Chord analysis
│   │   │   ├── melody_bass/  # Melody extraction
│   │   │   ├── packager/     # Song Map generator
│   │   │   └── orchestrator/ # AI orchestration
│   │   ├── audio_engine/     # Audio processing utilities
│   │   ├── models/           # ML models
│   │   └── utils/            # Shared utilities
│   ├── JuceLibraryCode/      # C++ JUCE audio engine
│   ├── scripts/              # Backend scripts
│   ├── tests/                # Backend tests
│   └── requirements.txt      # Python dependencies
│
├── shared/                    # Shared types & configs
│   ├── types/                # TypeScript/Python types
│   ├── config/               # Shared configuration
│   ├── utils/                # Cross-platform utilities
│   └── assets/               # Shared assets
│
├── tests/                     # Integration tests
│   ├── e2e/                  # End-to-end tests
│   ├── integration/          # Integration tests
│   └── performance/          # Performance benchmarks
│
├── scripts/                   # Build & deploy scripts
│   ├── build/                # Build scripts
│   ├── deploy/               # Deployment scripts
│   └── dev/                  # Development utilities
│
├── config/                    # Environment configs
│   ├── development/          # Dev configuration
│   ├── production/           # Prod configuration
│   └── kubernetes/           # K8s manifests
│
├── docs/                      # Documentation
│   ├── api/                  # API documentation
│   ├── architecture/         # Architecture docs
│   ├── deployment/           # Deployment guides
│   └── development/          # Development guides
│
└── .claude/                   # Agent SDK configuration
    ├── agents/               # Agent definitions
    ├── commands/             # Custom commands
    ├── CLAUDE.md             # Project context
    ├── memory.md             # Project memory
    └── settings.json         # Agent settings
```

## 🚀 Quick Start

### Prerequisites
- Node.js 20+
- Python 3.12+
- Git
- GitHub CLI (`gh`)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/PerformanceSuite/Performia.git
cd Performia
```

2. **Install all dependencies:**
```bash
npm run install:all
```

3. **Set up environment variables:**
```bash
cp shared/.env.template .env
# Edit .env with your API keys
```

4. **Start development servers:**

Frontend:
```bash
npm run dev:frontend
```

Backend:
```bash
npm run dev:backend
```

## 🤖 Agent-Driven Development

This project uses the **Claude Agent SDK** for autonomous development:

### Working with Agents
```bash
# Start Claude Code
claude

# Invoke an agent
"Act as the frontend development agent and improve Living Chart performance"

# View available agents
ls .claude/agents/
```

See [AGENT_ROADMAP.md](./AGENT_ROADMAP.md) for the complete agent ecosystem plan.

## 🛠️ Technology Stack

### Frontend
- React 19.1.1
- TypeScript 5.8.2
- Vite 6.2.0
- Tailwind CSS 4.1.13
- Immer (state management)

### Backend
- Python 3.12
- JUCE (C++ audio)
- SuperCollider
- TensorFlow/PyTorch (ML)
- FastAPI

### Infrastructure
- Google Cloud Platform
- GitHub Actions CI/CD
- MCP Servers (filesystem, GitHub, memory)
- Goose CLI for autonomous development

## 📊 Features

- **Living Chart** - Real-time interactive performance visualization
- **Library Service** - Comprehensive music library management
- **Audio Processing** - Low-latency C++ audio engine
- **AI Agents** - Autonomous performance analysis
- **Data Pipeline** - Ingestion and analysis pipeline

## 🧪 Testing

```bash
# Run all tests
npm test

# Frontend only
npm run test:frontend

# Backend only
npm run test:backend
```

## 📝 Documentation

- [Agent Roadmap](./AGENT_ROADMAP.md) - Agent development plan
- [Agent Status](./AGENT_STATUS.md) - Current agent status
- [Project Context](./.claude/CLAUDE.md) - Project context for agents
- [Architecture](./docs/ARCHITECTURE.md) - System architecture

## 🔄 Development Status

✅ **Phase 1 & 2**: Infrastructure & Migration - Complete
✅ **Codebase Cleanup**: Unified structure established (Sep 30, 2024)
🎯 **Phase 3**: Core Development Agents - **IN PROGRESS**

### Next Steps
1. Create Frontend Development Agent
2. Build Audio Pipeline Agent
3. Integrate Voice Control (Whisper API)

See [AGENT_ROADMAP.md](./AGENT_ROADMAP.md) for detailed agent development plan.

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

## 🔗 Links

- [GitHub Repository](https://github.com/PerformanceSuite/Performia)
- [Documentation](./docs/)
- [Issue Tracker](https://github.com/PerformanceSuite/Performia/issues)

---

*Built with 🤖 Agentic Engineering - "What if your codebase could ship itself?"*
