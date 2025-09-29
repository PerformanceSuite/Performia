#!/bin/bash
# Quick Phase 1 analysis script

echo "🔍 Phase 1: Repository Analysis"
echo "================================"
echo ""

# Check git status in both repos
echo "📋 Git Status - Performia:"
cd /Users/danielconnolly/Projects/Performia
git status --short

echo ""
echo "📋 Git Status - Performia-front:"
cd /Users/danielconnolly/Projects/Performia-front
git status --short

echo ""
echo "📁 Directory Structure - Performia:"
cd /Users/danielconnolly/Projects/Performia
find . -type d -name node_modules -prune -o -type d -name .git -prune -o -type d -print | head -30

echo ""
echo "📁 Directory Structure - Performia-front/performia---living-chart:"
cd /Users/danielconnolly/Projects/Performia-front/performia---living-chart
find . -type d -name node_modules -prune -o -type d -name .git -prune -o -type d -print | head -30
