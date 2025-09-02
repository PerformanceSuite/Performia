#!/bin/bash

# Performia GitHub Migration Script
# Migrates current projects to PerformanceSuite/Performia repository

echo "🚀 Performia GitHub Repository Migration"
echo "========================================"
echo "Target: https://github.com/PerformanceSuite/Performia"
echo ""

# Configuration
REPO_URL="https://github.com/PerformanceSuite/Performia.git"
UI_SOURCE="/Users/danielconnolly/Projects/Performia/Performia-UI-Clean"
BACKEND_SOURCE="/Users/danielconnolly/Projects/Performia/Performia-system"
TARGET_DIR="/Users/danielconnolly/Projects/Performia/Performia-GitHub"

echo "📁 Source Directories:"
echo "   UI:      $UI_SOURCE"
echo "   Backend: $BACKEND_SOURCE"
echo "   Target:  $TARGET_DIR"
echo ""

# Step 1: Clone repository
echo "Step 1: Cloning repository..."
echo "-----------------------------"
if [ ! -d "$TARGET_DIR" ]; then
    git clone $REPO_URL $TARGET_DIR
    echo "✅ Repository cloned"
else
    echo "⚠️  Directory exists, pulling latest..."
    cd $TARGET_DIR
    git pull origin main
fi

cd $TARGET_DIR

# Step 2: Create branch structure
echo ""
echo "Step 2: Creating branches..."
echo "----------------------------"

# Create ui-clean branch
echo "Creating ui-clean branch..."
git checkout -b ui-clean 2>/dev/null || git checkout ui-clean
git pull origin ui-clean 2>/dev/null || echo "New branch"

# Create backend-core branch  
echo "Creating backend-core branch..."
git checkout -b backend-core 2>/dev/null || git checkout backend-core
git pull origin backend-core 2>/dev/null || echo "New branch"

# Create legacy-archive branch
echo "Creating legacy-archive branch..."
git checkout -b legacy-archive 2>/dev/null || git checkout legacy-archive
git pull origin legacy-archive 2>/dev/null || echo "New branch"

# Step 3: Migrate UI-Clean
echo ""
echo "Step 3: Migrating UI-Clean..."
echo "-----------------------------"
git checkout ui-clean

# Archive existing files to legacy if needed
if [ "$(ls -A .)" ]; then
    echo "Moving existing files to legacy..."
    git checkout legacy-archive
    cp -r . ../legacy-temp 2>/dev/null || true
    git checkout ui-clean
fi

# Clear and copy UI-Clean
echo "Copying UI-Clean project..."
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} \;
cp -r $UI_SOURCE/* .
cp -r $UI_SOURCE/.* . 2>/dev/null || true

# Clean up
rm -rf .git 2>/dev/null || true
rm -rf Performia-GitHub 2>/dev/null || true

echo "✅ UI-Clean migrated"

# Step 4: Prepare Backend-Core
echo ""
echo "Step 4: Preparing Backend-Core..."
echo "---------------------------------"
git checkout backend-core

# Clear branch
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} \;

# Create backend extraction script
cat > extract_backend.sh << 'EXTRACT'
#!/bin/bash
# Extract only backend components from Performia-system

SOURCE="/Users/danielconnolly/Projects/Performia/Performia-system"
TARGET="."

echo "Extracting backend components..."

# Core backend files
mkdir -p src/core
cp -r $SOURCE/src/core/*.py $TARGET/src/core/ 2>/dev/null || true
cp -r $SOURCE/src/agents $TARGET/src/ 2>/dev/null || true
cp -r $SOURCE/src/memory $TARGET/src/ 2>/dev/null || true

# Configuration
mkdir -p config
cp -r $SOURCE/config/* $TARGET/config/ 2>/dev/null || true

# Scripts
mkdir -p scripts
cp $SOURCE/scripts/*.py $TARGET/scripts/ 2>/dev/null || true
cp $SOURCE/scripts/*.sh $TARGET/scripts/ 2>/dev/null || true

# Requirements
cp $SOURCE/requirements.txt $TARGET/ 2>/dev/null || true

# SuperCollider files
mkdir -p sc
cp -r $SOURCE/sc/* $TARGET/sc/ 2>/dev/null || true

# Create backend-specific README
cat > README.md << 'README'
# Performia Backend Core

## Overview
Core backend system for Performia, providing:
- Audio engine with low latency
- AI agents (Bass, Drums, Keys, Melody)
- OSC server (port 7772)
- SuperCollider integration

## Requirements
- Python 3.9+
- SuperCollider
- OSC libraries

## Running
```bash
./run_backend.sh
```

## API
OSC endpoints on port 7772:
- /agent/[name]/enable
- /agent/[name]/volume
- /transport/play
- /transport/stop
README

echo "✅ Backend structure created"
EXTRACT

chmod +x extract_backend.sh
./extract_backend.sh
rm extract_backend.sh

echo "✅ Backend-Core prepared"

# Step 5: Create main branch README
echo ""
echo "Step 5: Updating main branch..."
echo "-------------------------------"
git checkout main 2>/dev/null || git checkout -b main

# Clear everything except .git
find . -maxdepth 1 ! -name '.git' ! -name '.' ! -name '..' -exec rm -rf {} \;

# Copy the README we created
cp /Users/danielconnolly/Projects/Performia/setup-github-repo.sh .
mv README-main.md README.md

# Add essential files
cat > .gitignore << 'IGNORE'
.DS_Store
node_modules/
build/
dist/
*.log
.env
__pycache__/
*.pyc
IGNORE

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

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
LICENSE

echo "✅ Main branch updated"

# Step 6: Show status
echo ""
echo "📊 Repository Status:"
echo "--------------------"
git branch -a

echo ""
echo "📝 Next Steps:"
echo "-------------"
echo "1. Review the branches:"
echo "   git checkout ui-clean     # Check UI"
echo "   git checkout backend-core # Check backend"
echo "   git checkout main         # Check documentation"
echo ""
echo "2. Commit and push all branches:"
echo "   git checkout ui-clean && git add . && git commit -m 'feat: Complete UI implementation'"
echo "   git push origin ui-clean"
echo ""
echo "   git checkout backend-core && git add . && git commit -m 'feat: Clean backend extraction'"
echo "   git push origin backend-core"
echo ""
echo "   git checkout main && git add . && git commit -m 'docs: Update repository structure'"
echo "   git push origin main"
echo ""
echo "3. Go to GitHub and set default branch:"
echo "   Settings -> Branches -> Default branch -> ui-clean"
echo ""
echo "✅ Migration script complete!"