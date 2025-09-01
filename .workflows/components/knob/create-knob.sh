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

