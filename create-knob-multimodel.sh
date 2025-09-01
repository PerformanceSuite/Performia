#!/bin/bash

# Quick Launcher for Multi-Model Knob Creation
echo "🎯 Creating Professional Rotary Knob with Multi-Model Workflow"
echo "=============================================================="
echo ""
echo "This workflow will:"
echo "1. Use Gemini to design the visual appearance"
echo "2. Store the design in Claude Flow memory"
echo "3. Use Claude to implement the JUCE component"
echo "4. Validate with both models"
echo ""
echo "Ready to start?"
read -p "Press Enter to begin..."

# Execute the workflow
.workflows/components/knob/create-knob.sh

echo ""
echo "✨ Workflow complete!"
echo ""
echo "Next steps:"
echo "1. Review generated files in src/components/basic/"
echo "2. Run tests with: .workflows/components/knob/test-knob.sh"
echo "3. Integrate into main application"
