#!/bin/bash

# Performia GitHub Repository - Clean Migration Script
# Creates a focused, production-ready repository structure

echo "🎯 Performia Clean Repository Migration"
echo "======================================="
echo "Target: https://github.com/PerformanceSuite/Performia"
echo ""

# Configuration
REPO_URL="https://github.com/PerformanceSuite/Performia.git"
UI_SOURCE="/Users/danielconnolly/Projects/Performia/Performia-UI-Clean"
BACKEND_SOURCE="/Users/danielconnolly/Projects/Performia/Performia-system"
TARGET_DIR="/Users/danielconnolly/Projects/Performia/Performia-GitHub"

echo "📋 Migration Plan:"
echo "  • main branch: Documentation only"
echo "  • ui-clean branch: Complete UI with necessary Claude Flow configs"
echo "  • backend-core branch: ONLY working backend components"
echo "  • NO legacy branch (keeping local only)"
echo ""

# Step 1: Clone repository
echo "Step 1: Repository Setup"
echo "------------------------"
if [ ! -d "$TARGET_DIR" ]; then
    git clone $REPO_URL $TARGET_DIR
    echo "✅ Repository cloned"
else
    echo "⚠️  Directory exists, pulling latest..."
    cd $TARGET_DIR
    git pull origin main 2>/dev/null || true
fi

cd $TARGET_DIR

# Step 2: Create ui-clean branch
echo ""
echo "Step 2: UI-Clean Branch"
echo "-----------------------"
git checkout -b ui-clean 2>/dev/null || git checkout ui-clean

# Clear branch
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} \;

# Copy UI-Clean project
echo "Copying UI components..."
cp -r $UI_SOURCE/* .

# Create .gitignore for UI
cat > .gitignore << 'IGNORE'
# Dependencies
node_modules/
.npm/

# Build outputs
build/
dist/
*.o
*.dylib

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Project specific
.sessions/
.current-session
.state/
.cache/

# Claude Flow (keep only configs)
.hive-mind/sessions/
.swarm/*.db
.claude-flow/metrics/
memory/sessions/

# Logs
*.log
npm-debug.log*

# Environment
.env
.env.local

# JUCE
JuceLibraryCode/
Builds/
IGNORE

# Decide what Claude Flow parts to keep
echo ""
echo "Configuring Claude Flow for production..."
cat > CLAUDEFLOW_CONFIG.md << 'CFCONFIG'
# Claude Flow Configuration for Performia

## What's Included in Repo:

### Configuration Files (INCLUDED)
- `.claude/` - Command documentation
- `claude-flow.config.json` - Base configuration
- `.workflows/` - Multi-model workflows
- `MULTIMODEL_WORKFLOW.md` - Documentation

### Session/Memory (EXCLUDED - User-specific)
- `.hive-mind/sessions/` - Gitignored
- `.swarm/*.db` - Gitignored  
- `.sessions/` - Gitignored
- `memory/sessions/` - Gitignored

## Studio Mode Integration

The AI agents in Studio Mode will use Claude Flow's neural capabilities:

1. **Pattern Learning**: Agents learn from user input
2. **Style Transfer**: Apply learned patterns across genres
3. **Neural Visualization**: Show AI thinking process

### Implementation:
```javascript
// src/studio/AIAgentController.js
import { ClaudeFlowIntegration } from './claudeflow/integration';

class StudioAIAgent {
    constructor() {
        this.neural = new ClaudeFlowIntegration({
            mode: 'embedded',
            features: ['pattern-learning', 'style-transfer']
        });
    }
}
```

## Installation for Users:
```bash
# Users need to install Claude Flow separately
npm install -g claude-flow@alpha

# Then initialize in project
npx claude-flow@alpha init --embedded
```
CFCONFIG

# Clean up Claude Flow files for repo
echo "Cleaning Claude Flow for repository..."
rm -rf .hive-mind/sessions/
rm -rf .swarm/*.db
rm -rf .sessions/*
rm -rf memory/sessions/*
rm -rf .claude-flow/metrics/*.json

# Keep only essential Claude Flow configs
mkdir -p .repo-configs
mv .claude/agents/ui-designer-gemini.md .repo-configs/ 2>/dev/null || true
mv .workflows .repo-configs/workflows 2>/dev/null || true

echo "✅ UI-Clean branch prepared"

# Step 3: Create backend-core branch
echo ""
echo "Step 3: Backend-Core Branch (CLEAN)"
echo "-----------------------------------"
git checkout -b backend-core 2>/dev/null || git checkout backend-core

# Clear branch
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} \;

# Extract ONLY the working backend components
echo "Extracting ONLY essential backend components..."

# Create clean backend structure
mkdir -p src/{core,agents,osc,memory}
mkdir -p config
mkdir -p scripts
mkdir -p sc/synthdefs

# Copy ONLY working backend files from Performia-system
echo "Copying core audio engine..."
cp $BACKEND_SOURCE/src/core/audio_engine.py src/core/ 2>/dev/null || true
cp $BACKEND_SOURCE/src/core/audio_processor.py src/core/ 2>/dev/null || true
cp $BACKEND_SOURCE/src/core/buffer_manager.py src/core/ 2>/dev/null || true

echo "Copying AI agents..."
cp -r $BACKEND_SOURCE/src/agents/*.py src/agents/ 2>/dev/null || true
# Remove any UI-related agent files
find src/agents -name "*ui*" -delete 2>/dev/null || true
find src/agents -name "*visual*" -delete 2>/dev/null || true

echo "Copying OSC server..."
cp $BACKEND_SOURCE/src/osc_server.py src/osc/ 2>/dev/null || true
cp $BACKEND_SOURCE/src/osc_handler.py src/osc/ 2>/dev/null || true

echo "Copying memory system..."
cp $BACKEND_SOURCE/src/memory/SharedMemoryRingBuffer.cpp src/memory/ 2>/dev/null || true
cp $BACKEND_SOURCE/src/memory/*.py src/memory/ 2>/dev/null || true

echo "Copying SuperCollider files..."
cp $BACKEND_SOURCE/sc/*.scd sc/ 2>/dev/null || true
cp $BACKEND_SOURCE/sc/synthdefs/*.scsyndef sc/synthdefs/ 2>/dev/null || true

echo "Copying essential scripts..."
cp $BACKEND_SOURCE/scripts/start_backend.py scripts/ 2>/dev/null || true
cp $BACKEND_SOURCE/scripts/osc_test.py scripts/ 2>/dev/null || true

# Create requirements.txt with ONLY backend dependencies
cat > requirements.txt << 'REQS'
# Core
python-osc==1.8.0
numpy==1.24.0
scipy==1.10.0

# Audio
soundfile==0.12.1
pyaudio==0.2.11

# Memory/IPC
posix-ipc==1.0.5

# Utilities
pyyaml==6.0
python-dotenv==1.0.0
REQS

# Create clean backend README
cat > README.md << 'README'
# Performia Backend Core

## Overview
Minimal, clean backend for Performia providing:
- Audio engine (<10ms latency)
- 4 AI agents (Bass, Drums, Keys, Melody)
- OSC server on port 7772
- Shared memory IPC for audio
- SuperCollider synthesis engine

## Structure
```
src/
├── core/       # Audio engine
├── agents/     # AI agents
├── osc/        # OSC communication
└── memory/     # Shared memory IPC

sc/             # SuperCollider files
scripts/        # Startup scripts
config/         # Configuration
```

## Requirements
- Python 3.9+
- SuperCollider 3.12+
- POSIX shared memory support

## Installation
```bash
pip install -r requirements.txt
```

## Running
```bash
# Start complete backend
python scripts/start_backend.py

# Or components individually:
python src/osc/osc_server.py &
sclang sc/main.scd &
```

## OSC API

### Agent Control
- `/agent/bass/enable [0|1]`
- `/agent/bass/volume [0.0-1.0]`
- `/agent/bass/parameter [param] [value]`

### Transport
- `/transport/play`
- `/transport/stop`
- `/transport/tempo [bpm]`

### System
- `/system/status`
- `/system/latency`

## IPC Interface
Shared memory ring buffer at `/performia_audio`
- 48kHz stereo float32 audio
- 64 sample buffer size
- Lock-free write, wait-free read
README

# Create .gitignore for backend
cat > .gitignore << 'IGNORE'
# Python
__pycache__/
*.py[cod]
*.so
venv/
.env

# SuperCollider
*.scsyndef.bak

# Logs
*.log

# OS
.DS_Store

# Build
build/
dist/

# Memory files
*.shm
IGNORE

echo "✅ Backend-Core branch prepared (clean)"

# Step 4: Create main branch with documentation
echo ""
echo "Step 4: Main Branch (Documentation)"
echo "-----------------------------------"
git checkout main 2>/dev/null || git checkout -b main

# Clear everything except .git
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} \;

# Create comprehensive README
cat > README.md << 'README'
# 🎨 Performia - AI-Powered Music Performance System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/PerformanceSuite/Performia)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

Performia is a professional audio interface for AI-powered music performance, featuring intelligent agents that collaborate with human musicians in real-time.

## 🌳 Repository Structure

This repository uses a branch-based architecture:

### [`ui-clean`](../../tree/ui-clean) - User Interface
The modern JUCE-based interface with:
- 6 operational modes (Studio, Live, Settings, Library, Display, Room)
- Professional dark theme with cyan accents
- Multi-model AI integration (Claude + Gemini)
- Real-time audio visualization

### [`backend-core`](../../tree/backend-core) - Backend System
Clean, minimal backend with:
- Audio engine (<10ms latency)
- 4 AI agents (Bass, Drums, Keys, Melody)
- OSC server (port 7772)
- SuperCollider synthesis

## 🚀 Quick Start

### Complete System Setup

1. **Install Dependencies:**
```bash
# UI dependencies
git checkout ui-clean
npm install

# Backend dependencies
git checkout backend-core
pip install -r requirements.txt
```

2. **Start Backend:**
```bash
git checkout backend-core
python scripts/start_backend.py
```

3. **Start UI (new terminal):**
```bash
git checkout ui-clean
npm run build
./build/Performia
```

## 🏗️ Architecture

```
┌─────────────────────────┐     ┌─────────────────────────┐
│      UI (ui-clean)      │ OSC │  Backend (backend-core) │
│                         │<--->│                         │
│  JUCE Interface         │7772 │  Audio Engine           │
│  6 Operating Modes      │     │  AI Agents              │
│  Visualization          │     │  SuperCollider          │
└─────────────────────────┘     └─────────────────────────┘
```

## 📚 Documentation

- [UI Documentation](../../tree/ui-clean/docs)
- [Backend API](../../tree/backend-core/README.md)
- [User Guide](../../wiki)

## 🛠️ Development

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

## 🤖 AI Integration

Performia uses multiple AI models:
- **Claude**: Logic and code implementation
- **Gemini**: Visual design and UI components
- **Neural Networks**: Pattern learning in Studio Mode

### Claude Flow Integration
The project includes Claude Flow configurations for development assistance. Users can optionally install Claude Flow for enhanced AI agent capabilities in Studio Mode.

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- JUCE Framework
- SuperCollider Community
- Claude Flow by rUv
README

# Add LICENSE
cat > LICENSE << 'LICENSE'
MIT License

Copyright (c) 2025 Performance Suite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.
LICENSE

# Create .gitignore for main
cat > .gitignore << 'IGNORE'
.DS_Store
IGNORE

echo "✅ Main branch prepared"

# Step 5: Summary
echo ""
echo "📊 Repository Structure Summary:"
echo "--------------------------------"
echo ""
echo "main branch:"
echo "  └── README.md (documentation)"
echo "  └── LICENSE"
echo ""
echo "ui-clean branch:"
echo "  └── Complete UI from Performia-UI-Clean"
echo "  └── Claude Flow configs (for development)"
echo "  └── Multi-model workflows"
echo "  └── NO database files or sessions"
echo ""
echo "backend-core branch:"
echo "  └── src/core/ (audio engine only)"
echo "  └── src/agents/ (AI agents only)"
echo "  └── src/osc/ (OSC server only)"
echo "  └── sc/ (SuperCollider files)"
echo "  └── NO old GUI attempts"
echo "  └── NO broken components"
echo ""
echo "✅ Clean migration complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Review each branch:"
echo "   git branch"
echo ""
echo "2. Commit and push:"
echo "   git checkout ui-clean && git add . && git commit -m 'feat: Complete UI implementation'"
echo "   git push origin ui-clean"
echo ""
echo "   git checkout backend-core && git add . && git commit -m 'feat: Clean backend extraction'"
echo "   git push origin backend-core"
echo ""
echo "   git checkout main && git add . && git commit -m 'docs: Repository structure'"
echo "   git push origin main"
echo ""
echo "3. Set default branch on GitHub to 'ui-clean'"