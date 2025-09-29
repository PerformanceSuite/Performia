#!/bin/bash

echo "========================================="
echo "Performia Voice Engine Setup"
echo "========================================="
echo

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

echo
echo "Installing dependencies..."
echo "-------------------------------------------"

# Core dependencies
pip install numpy
pip install sounddevice
pip install openai-whisper
pip install google-generativeai

# Audio analysis
pip install essentia

# Optional: Install whisper.cpp for faster inference
echo
echo "Would you like to install whisper.cpp for faster inference? (y/n)"
read -r install_whisper_cpp

if [ "$install_whisper_cpp" = "y" ]; then
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing whisper.cpp via Homebrew..."
        brew install whisper-cpp
    else
        echo "Building whisper.cpp from source..."
        git clone https://github.com/ggerganov/whisper.cpp
        cd whisper.cpp
        make
        bash ./models/download-ggml-model.sh large-v3
        cd ..
    fi
fi

echo
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo
echo "Next steps:"
echo "1. Set your Gemini API key:"
echo "   export GEMINI_API_KEY='your-api-key'"
echo
echo "2. Test the voice engine:"
echo "   python src/voice_engine/core.py"
echo
echo "3. Configure audio devices in config/audio.yaml"
echo
echo "For documentation, see: docs/voice_engine_spec.md"
echo
