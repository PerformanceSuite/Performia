#!/bin/bash

# Performia Repository Reorganization Script
# Sets up the PerformanceSuite/Performia repo with proper branch structure

echo "🎯 Performia Repository Setup for GitHub"
echo "========================================"
echo "Repository: https://github.com/PerformanceSuite/Performia"
echo ""

# Step 1: Clone and prepare
echo "📦 Step 1: Clone and Prepare"
echo "----------------------------"
echo "Commands to run:"
echo ""
cat << 'SETUP'
# Clone the repository
git clone https://github.com/PerformanceSuite/Performia.git Performia-Main
cd Performia-Main

# Create branch structure
git checkout -b main  # or master, depending on default
git checkout -b ui-clean
git checkout -b backend-core
git checkout -b legacy-archive

SETUP

# Step 2: Branch Strategy
echo ""
echo "🌳 Step 2: Branch Strategy"
echo "-------------------------"
cat << 'BRANCHES'
Branch Structure:
├── main (or master)
│   └── README.md pointing to active branches
│   └── Documentation only
│
├── ui-clean
│   └── Complete Performia-UI-Clean project
│   └── Beautiful JUCE interface
│   └── Multi-model workflows
│
├── backend-core  
│   └── Cleaned backend from Performia-system
│   └── Audio engine, AI agents, OSC
│   └── No UI code
│
└── legacy-archive
    └── Old files for reference
    └── Not actively maintained

BRANCHES

# Step 3: Migration commands
echo ""
echo "🚀 Step 3: Migration Commands"
echo "-----------------------------"
cat << 'MIGRATE'
# For UI-Clean branch
git checkout ui-clean
rm -rf *  # Clear branch (careful!)
cp -r ../Performia-UI-Clean/* .
git add .
git commit -m "feat: Complete UI-Clean implementation with multi-model support"
git push origin ui-clean

# For Backend-Core branch  
git checkout backend-core
rm -rf *  # Clear branch
# Copy only backend files from Performia-system
cp -r ../Performia-system/src/core .
cp -r ../Performia-system/src/agents .
cp -r ../Performia-system/scripts .
cp ../Performia-system/requirements.txt .
# Remove UI-related files
find . -name "*UI*" -delete
find . -name "*Component*" -delete
find . -name "Main*" -delete
git add .
git commit -m "feat: Clean backend implementation without UI"
git push origin backend-core

# For Legacy-Archive branch
git checkout legacy-archive
# Move old files here
git add .
git commit -m "archive: Legacy files for reference"
git push origin legacy-archive

# Update main branch
git checkout main
MIGRATE

# Step 4: Create main branch README
echo ""
echo "📝 Step 4: Main Branch README"
echo "-----------------------------"
cat > README-main.md << 'README'
# 🎨 Performia - AI-Powered Music Performance System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/PerformanceSuite/Performia)
[![UI](https://img.shields.io/badge/UI-JUCE-orange.svg)](https://github.com/PerformanceSuite/Performia/tree/ui-clean)
[![Backend](https://img.shields.io/badge/Backend-SuperCollider-green.svg)](https://github.com/PerformanceSuite/Performia/tree/backend-core)

## 🎯 Overview

Performia is a professional audio interface for AI-powered music performance, featuring intelligent agents that collaborate with human musicians in real-time.

## 🌳 Repository Structure

This repository uses a branch-based architecture to separate concerns:

### Active Branches

#### 🎨 [`ui-clean`](https://github.com/PerformanceSuite/Performia/tree/ui-clean)
The modern, beautiful JUCE-based user interface.
- Professional dark theme with cyan accents
- 6 specialized modes (Studio, Live, Settings, Library, Display, Room)
- Multi-model AI integration (Claude + Gemini)
- [View UI Documentation](https://github.com/PerformanceSuite/Performia/blob/ui-clean/README.md)

```bash
git checkout ui-clean
```

#### 🔧 [`backend-core`](https://github.com/PerformanceSuite/Performia/tree/backend-core)
The core backend system with AI agents.
- Audio engine with <10ms latency
- 4 AI agents (Bass, Drums, Keys, Melody)
- OSC communication (port 7772)
- SuperCollider integration
- [View Backend Documentation](https://github.com/PerformanceSuite/Performia/blob/backend-core/README.md)

```bash
git checkout backend-core
```

#### 📦 [`legacy-archive`](https://github.com/PerformanceSuite/Performia/tree/legacy-archive)
Historical code for reference only.

## 🚀 Quick Start

### Run Complete System

1. **Start Backend:**
```bash
git checkout backend-core
./run_backend.sh
```

2. **Start UI (separate terminal):**
```bash
git checkout ui-clean
./build_and_run.sh
```

### Development Setup

```bash
# Clone repository
git clone https://github.com/PerformanceSuite/Performia.git
cd Performia

# For UI development
git checkout ui-clean
npm install
./setup.sh

# For backend development
git checkout backend-core
pip install -r requirements.txt
./setup_backend.sh
```

## 🏗️ Architecture

```
┌─────────────────────────┐     ┌─────────────────────────┐
│      UI (ui-clean)      │ OSC │  Backend (backend-core) │
│                         │<--->│                         │
│  - JUCE Interface       │7772 │  - Audio Engine         │
│  - 6 Operating Modes    │     │  - AI Agents            │
│  - Visualization        │ IPC │  - SuperCollider        │
│  - Multi-Model AI       │<--->│  - OSC Server           │
└─────────────────────────┘     └─────────────────────────┘
```

## 📊 Features

### UI Features (ui-clean branch)
- ✅ Professional DAW-quality interface
- ✅ Real-time audio visualization
- ✅ AI agent control panels
- ✅ Multi-model orchestration (Claude + Gemini)
- ✅ 60 FPS animations

### Backend Features (backend-core branch)
- ✅ Low-latency audio processing
- ✅ 4 intelligent AI agents
- ✅ OSC/MIDI communication
- ✅ SuperCollider synthesis
- ✅ Pattern learning system

## 🔄 Development Workflow

### Working on UI
```bash
git checkout ui-clean
# Make changes
git commit -m "feat(ui): description"
git push origin ui-clean
```

### Working on Backend
```bash
git checkout backend-core
# Make changes
git commit -m "feat(backend): description"
git push origin backend-core
```

### Creating a Release
```bash
# Merge both branches into a release branch
git checkout -b release/v2.0.0
git merge ui-clean
git merge backend-core
git tag v2.0.0
git push origin release/v2.0.0 --tags
```

## 📚 Documentation

- [UI Documentation](https://github.com/PerformanceSuite/Performia/blob/ui-clean/docs/README.md)
- [Backend Documentation](https://github.com/PerformanceSuite/Performia/blob/backend-core/docs/README.md)
- [API Reference](https://github.com/PerformanceSuite/Performia/wiki/API-Reference)
- [User Guide](https://github.com/PerformanceSuite/Performia/wiki/User-Guide)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch from the appropriate base branch
3. Make your changes
4. Submit a pull request to the correct branch

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- JUCE Framework by ROLI
- SuperCollider Community
- Claude Flow by rUv
- OpenAI and Anthropic for AI capabilities

---

**Current Status**: Active development on both UI and Backend branches

**Latest Release**: v2.0.0-alpha (September 2025)
README

echo "✅ Main README created"

# Step 5: GitHub Actions for CI/CD
echo ""
echo "🔧 Step 5: GitHub Actions Setup"
echo "-------------------------------"
cat > .github-workflows-ci.yml << 'ACTIONS'
name: Performia CI/CD

on:
  push:
    branches: [ main, ui-clean, backend-core ]
  pull_request:
    branches: [ main, ui-clean, backend-core ]

jobs:
  ui-tests:
    if: github.ref == 'refs/heads/ui-clean'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
      - run: npm test
      
  backend-tests:
    if: github.ref == 'refs/heads/backend-core'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: pytest
ACTIONS

echo "✅ GitHub Actions workflow created"

# Step 6: Gitignore for main branch
echo ""
echo "📝 Step 6: Global .gitignore"
echo "---------------------------"
cat > .gitignore-main << 'IGNORE'
# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Build
build/
dist/
*.o
*.so
*.dylib
*.dll

# Dependencies
node_modules/
venv/
__pycache__/

# Logs
*.log
npm-debug.log*

# Environment
.env
.env.local

# Project specific
.sessions/
.cache/
*.backup
IGNORE

echo "✅ Gitignore created"

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Clone https://github.com/PerformanceSuite/Performia.git"
echo "2. Create branches as shown above"
echo "3. Copy Performia-UI-Clean to ui-clean branch"
echo "4. Extract backend from Performia-system to backend-core branch"
echo "5. Push all branches"
echo "6. Set ui-clean as default branch in GitHub settings"
echo ""
echo "This gives you:"
echo "✅ Single repository"
echo "✅ Clean separation"
echo "✅ Easy to manage"
echo "✅ Professional structure"