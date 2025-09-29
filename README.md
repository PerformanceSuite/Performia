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
├── frontend/                  # React + TypeScript + Vite frontend
│   ├── src/                  # React source code
│   ├── components/           # UI components
│   ├── services/             # API services
│   └── package.json          # Frontend dependencies
│
├── backend/                   # Python + C++ backend
│   ├── src/                  # Python source code
│   ├── JuceLibraryCode/      # C++ audio engine
│   ├── ingest-analyze-pipe/  # Data pipeline
│   ├── performia_agent.py    # AI agent
│   ├── orchestrator.py       # 24/7 orchestrator
│   └── requirements.txt      # Python dependencies
│
├── shared/                    # Shared configurations
│   └── .env.template         # Environment variables template
│
├── scripts/                   # Utility scripts
├── docs/                      # Documentation
└── .github/                   # GitHub Actions workflows
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

## 🤖 Agentic Workflow

This project follows the **Agentic Engineering** paradigm:

### Using Goose
```bash
goose session
# In Goose: Read MIGRATION_PLAN.md for current tasks
```

### 24/7 Autonomous Agents
```bash
./backend/launch_orchestrator.sh
```

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

- [Migration Plan](./MIGRATION_PLAN.md) - Current migration status
- [Architecture](./docs/ARCHITECTURE.md) - System architecture
- [API Documentation](./backend/api/openapi.yaml)
- [Contributing](./CONTRIBUTING.md) - How to contribute

## 🔄 Migration Status

✅ **Phase 1**: Repository Analysis & Backup - Complete
✅ **Phase 2**: Create Unified Structure - Complete
⏳ **Phase 3**: Dependency Consolidation - Next
⏳ **Phase 4**: Configuration Merge
⏳ **Phase 5**: Git & GitHub Migration
⏳ **Phase 6**: GCP Consolidation
⏳ **Phase 7**: Testing & Validation
⏳ **Phase 8**: Compute Maxing Setup
⏳ **Phase 9**: Documentation
⏳ **Phase 10**: Cleanup

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
