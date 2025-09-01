#!/bin/bash

# Performia UI - Multi-Model Workflow for Professional Rotary Knob
# This creates a complete knob component using Gemini for design and Claude for implementation

echo "🎯 Multi-Model Component Creation Workflow"
echo "=========================================="
echo "Component: Professional Rotary Knob"
echo "Models: Gemini (Design) + Claude (Implementation)"
echo ""

# Step 1: Create workflow directory
echo "📁 Setting up workflow structure..."
mkdir -p .workflows/components/knob
mkdir -p src/components/basic
mkdir -p tests/components
mkdir -p resources/designs

# Step 2: Create the multi-model workflow script
cat > .workflows/components/knob/create-knob.sh << 'WORKFLOW'
#!/bin/bash

# Professional Rotary Knob - Multi-Model Creation Workflow
echo "🎨 Starting Multi-Model Knob Creation"
echo "======================================"

# Phase 1: Gemini Design Generation
echo ""
echo "🎨 PHASE 1: Gemini Design Generation"
echo "-------------------------------------"

# Create design prompt for Gemini
DESIGN_PROMPT=$(cat << 'PROMPT'
Create a professional audio interface rotary knob component with these exact specifications:

VISUAL DESIGN:
- Size: 64x64 pixels
- Background: Dark circular gradient from #1C2341 (center) to #0A0E27 (edge)
- Knob body: Subtle metallic texture with slight bevel
- Indicator: Bright cyan dot (#00D4FF) that follows rotation
- Glow effect: Soft cyan aura when hovered (8px blur, 30% opacity)
- Active state: Brighter glow (50% opacity) when being adjusted

INTERACTION DESIGN:
- Rotation range: 270 degrees (135° on each side from bottom)
- Value display: Percentage or decibel text below knob
- Hover animation: Glow fades in over 150ms
- Drag behavior: Vertical drag for adjustment
- Sensitivity: 100 pixels = full range

TECHNICAL REQUIREMENTS:
- Framework: JUCE C++
- Anti-aliasing: High quality
- Frame rate: 60 FPS minimum
- Shadow: Subtle drop shadow (2px blur, 20% opacity)

Provide:
1. Exact color values and gradients
2. Animation timing specifications
3. Shadow and glow parameters
4. Complete JUCE C++ implementation
5. Paint method optimization tips
PROMPT
)

echo "$DESIGN_PROMPT" > .workflows/components/knob/design-prompt.txt
echo "✅ Design prompt created"

# Call Gemini for design
echo "🤖 Calling Gemini for visual design..."
echo ""
echo "Execute this command manually:"
echo "gemini:ask-gemini --changeMode true --prompt @.workflows/components/knob/design-prompt.txt"
echo ""
echo "Press Enter after Gemini responds with the design..."
read -p ""

# Phase 2: Store Design in Claude Flow Memory
echo ""
echo "💾 PHASE 2: Storing Design in Memory"
echo "------------------------------------"

echo "Store Gemini's design in memory with:"
echo 'npx claude-flow@alpha memory store "knob_design_visual" "GEMINI_OUTPUT_HERE" --namespace performia-components'
echo ""
echo "Press Enter after storing..."
read -p ""

# Phase 3: Claude Implementation
echo ""
echo "🔧 PHASE 3: Claude Implementation"
echo "---------------------------------"

# Create implementation prompt for Claude
IMPLEMENTATION_PROMPT=$(cat << 'IMPL'
Using the visual design specifications from Gemini (stored in memory as knob_design_visual), 
create a complete JUCE component implementation for PerformiaKnob.

Requirements:
1. Create both .h and .cpp files
2. Inherit from juce::Slider
3. Override paint() method with Gemini's exact design
4. Implement smooth animations using Timer
5. Add hover and drag interaction
6. Include value change callback
7. Optimize for 60 FPS performance
8. Follow JUCE best practices

The component should integrate with our existing PerformiaColors system:
- Background: #0A0E27
- Surface: #1C2341
- Primary (cyan): #00D4FF
- Secondary (magenta): #FF00AA

Include:
- Proper JUCE component lifecycle
- Memory management with JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR
- Smooth value interpolation
- Accessible via keyboard
IMPL
)

echo "$IMPLEMENTATION_PROMPT" > .workflows/components/knob/implementation-prompt.txt
echo "✅ Implementation prompt created"

echo ""
echo "🤖 Spawning Claude for implementation..."
npx claude-flow@alpha swarm "Implement PerformiaKnob component based on Gemini design in memory" \
  --namespace performia-components \
  --memory-context "knob_design_visual" \
  --output-dir "src/components/basic" \
  --claude

WORKFLOW

chmod +x .workflows/components/knob/create-knob.sh

# Step 3: Create test workflow
cat > .workflows/components/knob/test-knob.sh << 'TESTFLOW'
#!/bin/bash

# Test Workflow for PerformiaKnob
echo "🧪 Testing PerformiaKnob Component"
echo "==================================="

# Phase 1: Visual validation
echo ""
echo "👁️ PHASE 1: Visual Validation"
echo "-----------------------------"
echo "Ask Gemini to validate the implementation:"
echo 'gemini:ask-gemini "Review this JUCE knob implementation and verify it matches the design spec" @src/components/basic/PerformiaKnob.cpp'

# Phase 2: Code review
echo ""
echo "📝 PHASE 2: Code Review"
echo "----------------------"
npx claude-flow@alpha swarm "Review PerformiaKnob for JUCE best practices and performance" \
  --agents reviewer,tester \
  --namespace performia-components

# Phase 3: Integration test
echo ""
echo "🔌 PHASE 3: Integration Test"
echo "----------------------------"
echo "Create test harness..."

cat > tests/components/TestPerformiaKnob.cpp << 'TEST'
#include "../../src/components/basic/PerformiaKnob.h"
#include <juce_core/juce_core.h>

class PerformiaKnobTest : public juce::UnitTest
{
public:
    PerformiaKnobTest() : UnitTest("PerformiaKnob") {}
    
    void runTest() override
    {
        beginTest("Creation");
        PerformiaKnob knob;
        expect(knob.getWidth() == 64);
        expect(knob.getHeight() == 64);
        
        beginTest("Value Range");
        knob.setRange(0.0, 100.0);
        knob.setValue(50.0);
        expectEquals(knob.getValue(), 50.0);
        
        beginTest("Visual Properties");
        expect(knob.getLookAndFeel() != nullptr);
    }
};

static PerformiaKnobTest performiaKnobTest;
TEST

echo "✅ Test harness created"
TESTFLOW

chmod +x .workflows/components/knob/test-knob.sh

# Step 4: Create the orchestration manager
cat > .workflows/multi-model-orchestrator.py << 'ORCHESTRATOR'
#!/usr/bin/env python3
"""
Multi-Model Orchestrator for Performia UI Components
Coordinates between Gemini (design) and Claude (implementation)
"""

import subprocess
import json
import time
from pathlib import Path

class MultiModelOrchestrator:
    def __init__(self):
        self.workflow_dir = Path(".workflows")
        self.memory_namespace = "performia-components"
        
    def create_component(self, component_type="knob"):
        """Orchestrate multi-model component creation"""
        
        print(f"🎭 Multi-Model Orchestration: {component_type.upper()}")
        print("=" * 50)
        
        # Step 1: Design with Gemini
        print("\n📐 Step 1: Design Generation (Gemini)")
        print("-" * 40)
        self.design_with_gemini(component_type)
        
        # Step 2: Store in memory
        print("\n💾 Step 2: Memory Storage (Claude Flow)")
        print("-" * 40)
        self.store_in_memory(component_type)
        
        # Step 3: Implement with Claude
        print("\n🔨 Step 3: Implementation (Claude)")
        print("-" * 40)
        self.implement_with_claude(component_type)
        
        # Step 4: Validate with both
        print("\n✅ Step 4: Validation (Both Models)")
        print("-" * 40)
        self.validate_component(component_type)
        
    def design_with_gemini(self, component_type):
        """Use Gemini for visual design"""
        
        prompt_file = self.workflow_dir / f"components/{component_type}/design-prompt.txt"
        
        if not prompt_file.exists():
            print(f"❌ Design prompt not found: {prompt_file}")
            return
            
        print(f"📄 Design prompt: {prompt_file}")
        print("🤖 Calling Gemini for design...")
        print("\nManual step required:")
        print(f"gemini:ask-gemini --changeMode true --prompt @{prompt_file}")
        print("\nWaiting for manual execution...")
        input("Press Enter when complete...")
        
    def store_in_memory(self, component_type):
        """Store design in Claude Flow memory"""
        
        print("📝 Enter Gemini's design output (end with 'END' on new line):")
        lines = []
        while True:
            line = input()
            if line == "END":
                break
            lines.append(line)
        
        design_output = "\n".join(lines)
        
        # Store in Claude Flow memory
        cmd = [
            "npx", "claude-flow@alpha", "memory", "store",
            f"{component_type}_design", design_output,
            "--namespace", self.memory_namespace
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Design stored in memory")
            else:
                print(f"❌ Failed to store: {result.stderr}")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def implement_with_claude(self, component_type):
        """Use Claude for implementation"""
        
        print("🔧 Spawning Claude for implementation...")
        
        cmd = [
            "npx", "claude-flow@alpha", "swarm",
            f"Implement Performia{component_type.title()} based on stored design",
            "--namespace", self.memory_namespace,
            "--memory-context", f"{component_type}_design",
            "--claude"
        ]
        
        try:
            subprocess.run(cmd)
            print("✅ Implementation task spawned")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def validate_component(self, component_type):
        """Validate with both models"""
        
        print("🧪 Validation workflow:")
        print("1. Gemini validates visual compliance")
        print("2. Claude validates code quality")
        print("3. Both validate integration")
        
        test_script = self.workflow_dir / f"components/{component_type}/test-{component_type}.sh"
        
        if test_script.exists():
            print(f"\n▶️ Run: {test_script}")
        else:
            print("⚠️ No test script found")

def main():
    orchestrator = MultiModelOrchestrator()
    
    print("🎯 Performia UI - Multi-Model Component Builder")
    print("=" * 50)
    print("\nAvailable components:")
    print("1. Knob (rotary control)")
    print("2. Slider (vertical fader)")
    print("3. Button (state toggle)")
    print("4. Meter (level display)")
    
    choice = input("\nSelect component (1-4): ")
    
    components = {
        "1": "knob",
        "2": "slider", 
        "3": "button",
        "4": "meter"
    }
    
    if choice in components:
        orchestrator.create_component(components[choice])
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
ORCHESTRATOR

chmod +x .workflows/multi-model-orchestrator.py

# Step 5: Create quick launcher
cat > create-knob-multimodel.sh << 'LAUNCHER'
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
LAUNCHER

chmod +x create-knob-multimodel.sh

echo ""
echo "✅ Multi-Model Workflow Setup Complete!"
echo ""
echo "📁 Created Structure:"
echo "   .workflows/components/knob/     - Knob-specific workflows"
echo "   .workflows/multi-model-orchestrator.py - General orchestrator"
echo "   create-knob-multimodel.sh       - Quick launcher"
echo ""
echo "🚀 To create your first knob component:"
echo "   ./create-knob-multimodel.sh"
echo ""
echo "This will guide you through:"
echo "1. Gemini designing the visual appearance"
echo "2. Claude implementing the JUCE code"
echo "3. Both models validating the result"
echo ""
echo "Ready to create beautiful UI components!"