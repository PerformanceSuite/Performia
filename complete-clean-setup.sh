#!/bin/bash

# Performia GitHub Repository - Complete Clean & Setup
# This script completely cleans the existing repo and sets up fresh branches

echo "🧹 Performia Repository Complete Clean & Setup"
echo "=============================================="
echo "Target: https://github.com/PerformanceSuite/Performia"
echo ""
echo "⚠️  WARNING: This will completely clean the repository!"
echo "   - Remove all existing files"
echo "   - Delete unnecessary branches"
echo "   - Create fresh branch structure"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Configuration
REPO_URL="https://github.com/PerformanceSuite/Performia.git"
UI_SOURCE="/Users/danielconnolly/Projects/Performia/Performia-UI-Clean"
BACKEND_SOURCE="/Users/danielconnolly/Projects/Performia/Performia-system"
TARGET_DIR="/Users/danielconnolly/Projects/Performia/Performia-GitHub"

# Step 1: Clone and clean repository
echo ""
echo "Step 1: Cloning and Cleaning Repository"
echo "---------------------------------------"

# Remove old clone if exists
rm -rf $TARGET_DIR

# Fresh clone
git clone $REPO_URL $TARGET_DIR
cd $TARGET_DIR

# Delete the stray branch
echo "Cleaning old branches..."
git push origin --delete add-claude-github-actions-1756086580114 2>/dev/null || true

# Clean main branch completely
echo "Cleaning main branch..."
git checkout main
# Remove everything except .git
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} \;

# Create minimal main branch
cat > README.md << 'README'
# 🎨 Performia - AI-Powered Music Performance System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/PerformanceSuite/Performia)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![UI](https://img.shields.io/badge/UI-JUCE-orange.svg)](../../tree/ui-clean)
[![Backend](https://img.shields.io/badge/Backend-Python-blue.svg)](../../tree/backend-core)

## Overview

Performia is a professional audio interface for AI-powered music performance, featuring intelligent agents that collaborate with human musicians in real-time.

## 🌳 Repository Structure

### Active Branches

#### [`ui-clean`](../../tree/ui-clean) - Modern User Interface
- JUCE-based professional audio interface
- 6 operational modes (Studio, Live, Settings, Library, Display, Room)
- Dark theme with cyan accent colors
- Multi-model AI integration for development

#### [`backend-core`](../../tree/backend-core) - Core Backend System
- High-performance audio engine (<10ms latency)
- 4 AI music agents (Bass, Drums, Keys, Melody)
- OSC communication protocol (port 7772)
- SuperCollider synthesis engine

## 🚀 Quick Start

### Prerequisites
- JUCE 7.x Framework
- Python 3.9+
- SuperCollider 3.12+
- Node.js 18+ (for development tools)

### Installation

1. **Clone and select branch:**
```bash
git clone https://github.com/PerformanceSuite/Performia.git
cd Performia
```

2. **For UI development:**
```bash
git checkout ui-clean
# Follow UI setup instructions in branch README
```

3. **For backend development:**
```bash
git checkout backend-core
# Follow backend setup instructions in branch README
```

### Running the Complete System

```bash
# Terminal 1: Start backend
git checkout backend-core
python scripts/start_backend.py

# Terminal 2: Start UI
git checkout ui-clean
./build/Performia
```

## 📚 Documentation

- [UI Documentation](../../tree/ui-clean/docs)
- [Backend API](../../tree/backend-core/docs)
- [Wiki](../../wiki)

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- JUCE Framework by ROLI
- SuperCollider Community
- Claude Flow by rUv (development tool)

---

**Project Status**: Active Development

**Latest Release**: v2.0.0-alpha
README

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

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
LICENSE

cat > .gitignore << 'IGNORE'
.DS_Store
Thumbs.db
*.log
IGNORE

cat > CONTRIBUTING.md << 'CONTRIB'
# Contributing to Performia

## Branch Strategy

- `main` - Documentation only
- `ui-clean` - UI development
- `backend-core` - Backend development

## Development Workflow

1. Fork the repository
2. Create your feature branch from the appropriate base branch
3. Commit your changes with descriptive messages
4. Push to your fork
5. Create a Pull Request to the appropriate branch

## Code Style

- UI: Follow JUCE conventions
- Backend: Follow PEP 8
- Comments: Clear and concise
- Documentation: Update with changes

## Testing

- UI: Test all 6 modes
- Backend: Ensure <10ms latency
- Integration: Test OSC communication
CONTRIB

# Commit clean main
git add .
git commit -m "chore: Clean repository structure - documentation only in main"

# Step 2: Create ui-clean branch
echo ""
echo "Step 2: Creating ui-clean Branch"
echo "--------------------------------"
git checkout -b ui-clean

# Remove main branch files
rm -f README.md LICENSE .gitignore CONTRIBUTING.md

# Copy entire UI-Clean project
echo "Copying UI-Clean project..."
cp -r $UI_SOURCE/* .
cp -r $UI_SOURCE/.* . 2>/dev/null || true

# Clean up Claude Flow runtime files
echo "Cleaning Claude Flow runtime files..."
rm -rf .hive-mind/sessions/ 2>/dev/null || true
rm -rf .swarm/*.db 2>/dev/null || true
rm -rf .sessions/* 2>/dev/null || true
rm -rf memory/sessions/* 2>/dev/null || true
rm -rf .claude-flow/metrics/*.json 2>/dev/null || true
rm -rf node_modules/ 2>/dev/null || true
rm -f .current-session 2>/dev/null || true

# Update .gitignore
cat >> .gitignore << 'IGNORE'

# Claude Flow Runtime (not for repo)
.hive-mind/sessions/
.swarm/*.db
.sessions/*
.current-session
memory/sessions/
.claude-flow/metrics/
node_modules/
.state/
.cache/
IGNORE

# Create branch-specific README
cat > BRANCH_README.md << 'README'
# UI-Clean Branch

This branch contains the complete JUCE-based user interface for Performia.

## Features
- 6 operational modes
- Professional dark theme
- Multi-model AI development workflows
- Real-time visualization

## Development
See [CLAUDE.md](CLAUDE.md) for AI-assisted development workflows.

## Building
```bash
mkdir build && cd build
cmake ..
make -j4
```
README

git add .
git commit -m "feat: Complete UI implementation with multi-model workflows"

# Step 3: Create backend-core branch
echo ""
echo "Step 3: Creating backend-core Branch"
echo "------------------------------------"
git checkout main
git checkout -b backend-core

# Remove main branch files
rm -f README.md LICENSE .gitignore CONTRIBUTING.md

# Create clean backend structure
echo "Extracting clean backend..."
mkdir -p src/{core,agents,osc,memory}
mkdir -p config
mkdir -p scripts
mkdir -p sc/synthdefs

# Extract ONLY working backend components
echo "Copying essential backend files..."

# Core audio engine (only the working parts)
if [ -f "$BACKEND_SOURCE/src/core/audio_engine.py" ]; then
    cp $BACKEND_SOURCE/src/core/audio_engine.py src/core/
fi
if [ -f "$BACKEND_SOURCE/src/core/audio_processor.py" ]; then
    cp $BACKEND_SOURCE/src/core/audio_processor.py src/core/
fi

# AI agents (remove UI-related files)
if [ -d "$BACKEND_SOURCE/src/agents" ]; then
    cp $BACKEND_SOURCE/src/agents/*.py src/agents/ 2>/dev/null || true
    find src/agents -name "*ui*" -delete 2>/dev/null || true
    find src/agents -name "*gui*" -delete 2>/dev/null || true
    find src/agents -name "*visual*" -delete 2>/dev/null || true
fi

# OSC server
if [ -f "$BACKEND_SOURCE/src/osc_server.py" ]; then
    cp $BACKEND_SOURCE/src/osc_server.py src/osc/
fi

# SuperCollider files
if [ -d "$BACKEND_SOURCE/sc" ]; then
    cp $BACKEND_SOURCE/sc/*.scd sc/ 2>/dev/null || true
fi

# Essential scripts only
if [ -f "$BACKEND_SOURCE/scripts/start_backend.py" ]; then
    cp $BACKEND_SOURCE/scripts/start_backend.py scripts/
fi

# Create requirements.txt
cat > requirements.txt << 'REQS'
# Core
python-osc==1.8.0
numpy==1.24.0
scipy==1.10.0

# Audio
soundfile==0.12.1
pyaudio==0.2.11

# IPC
posix-ipc==1.0.5

# Utils
pyyaml==6.0
python-dotenv==1.0.0
REQS

# Create clean README
cat > README.md << 'README'
# Backend-Core Branch

Clean backend implementation for Performia.

## Components
- Audio engine (<10ms latency)
- 4 AI agents
- OSC server (port 7772)
- SuperCollider synthesis

## Running
```bash
pip install -r requirements.txt
python scripts/start_backend.py
```

## API
See [docs/API.md](docs/API.md) for OSC protocol documentation.
README

# Create .gitignore
cat > .gitignore << 'IGNORE'
__pycache__/
*.pyc
.env
*.log
.DS_Store
build/
dist/
*.shm
IGNORE

git add .
git commit -m "feat: Clean backend extraction - essential components only"

# Step 4: Push everything
echo ""
echo "Step 4: Pushing to GitHub"
echo "------------------------"
echo ""
echo "Ready to push all branches. This will:"
echo "  • Push cleaned main branch"
echo "  • Push complete ui-clean branch"
echo "  • Push minimal backend-core branch"
echo ""
read -p "Push to GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git checkout main
    git push origin main --force
    
    git checkout ui-clean
    git push origin ui-clean --force
    
    git checkout backend-core
    git push origin backend-core --force
    
    echo "✅ All branches pushed!"
else
    echo "Skipped pushing. You can push manually with:"
    echo "  git push origin main --force"
    echo "  git push origin ui-clean --force"
    echo "  git push origin backend-core --force"
fi

# Step 5: Summary
echo ""
echo "🎉 Repository Cleanup Complete!"
echo "==============================="
echo ""
echo "✅ What was done:"
echo "  • Cleaned main branch (documentation only)"
echo "  • Created ui-clean branch (complete UI)"
echo "  • Created backend-core branch (clean backend)"
echo "  • Removed unnecessary files and branches"
echo ""
echo "📊 Repository structure:"
echo "  main → Documentation"
echo "  ui-clean → Complete UI with development tools"
echo "  backend-core → Essential backend only"
echo ""
echo "🔧 Next steps:"
echo "  1. Go to GitHub settings"
echo "  2. Set 'ui-clean' as default branch"
echo "  3. Add branch protection rules"
echo "  4. Update repository description"
echo ""
echo "🚀 Ready for development!"