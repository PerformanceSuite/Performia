#!/bin/bash

# Performia UI Clean - Project Structure Setup Script
# This script creates the complete directory structure for the Performia UI project

echo "🎨 Setting up Performia UI Clean project structure..."

# Create main source directories
mkdir -p src/core
mkdir -p src/components/basic
mkdir -p src/components/compound
mkdir -p src/components/specialized
mkdir -p src/modes
mkdir -p src/layouts
mkdir -p src/main
mkdir -p src/utils

# Create resource directories
mkdir -p resources/images
mkdir -p resources/shaders
mkdir -p resources/presets
mkdir -p resources/themes

# Create documentation directories
mkdir -p docs/api
mkdir -p docs/guides
mkdir -p docs/requirements

# Create test directories
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/ui

# Create build directories
mkdir -p build/debug
mkdir -p build/release

# Create session management directories
mkdir -p .sessions
mkdir -p .state
mkdir -p .cache

# Create JUCE specific directories
mkdir -p JuceLibraryCode
mkdir -p Builds

echo "✅ Directory structure created successfully!"
echo ""
echo "📁 Project structure:"
echo "   src/          - Source code"
echo "   resources/    - Assets and resources"
echo "   docs/         - Documentation"
echo "   tests/        - Test files"
echo "   build/        - Build outputs"
echo "   .sessions/    - Session management"
echo ""
echo "🚀 Ready for development!"