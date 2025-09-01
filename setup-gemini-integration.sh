#!/bin/bash

# Performia UI - Gemini Integration for Claude Flow Hive-Mind
# This script shows how to use Gemini within the Claude Flow orchestration

echo "🎨 Gemini + Claude Flow Integration Setup"
echo "========================================="
echo ""

# Method 1: Direct Gemini calls for UI components
echo "Method 1: Direct Gemini Calls"
echo "------------------------------"
echo "You can call Gemini directly from Claude Flow tasks:"
echo ""
echo "Example command:"
echo 'npx claude-flow@alpha swarm "Use Gemini to design a professional rotary knob" --hook-pre "gemini:ask-gemini --prompt \"Create JUCE rotary knob with cyan glow\""'
echo ""

# Method 2: Create a Gemini-powered agent
echo "Method 2: Gemini-Powered Agent"
echo "-------------------------------"
cat > .claude/agents/ui-designer-gemini.md << 'EOF'
---
name: ui-designer-gemini
type: designer
color: "#FF6B6B"
description: UI design specialist powered by Gemini
capabilities:
  - visual_design
  - component_generation
  - ui_mockups
  - style_systems
  - animation_design
priority: high
model: gemini-nano-banana
hooks:
  pre: |
    echo "🎨 Gemini UI Designer activating..."
  post: |
    echo "✨ Gemini design complete"
---

# Gemini-Powered UI Designer Agent

You are a UI design specialist that leverages Gemini's visual capabilities for creating beautiful interfaces.

## Integration with Gemini

When designing UI components, use Gemini's strengths:
1. Visual design generation
2. Color scheme creation
3. Component styling
4. Animation patterns
5. Layout optimization

## Workflow

1. Receive design requirements
2. Generate design with Gemini
3. Convert to JUCE implementation
4. Validate against PRD

## Gemini Prompts

For rotary knobs:
```
Create a professional audio interface rotary knob with:
- Dark background #0A0E27
- Cyan glow effect #00D4FF on interaction
- Smooth rotation animation
- Professional DAW quality like Ableton/Native Instruments
- JUCE C++ implementation
```

For sliders:
```
Design a vertical slider for audio interface with:
- LED meter visualization
- Dark theme with cyan accents
- Smooth thumb movement
- Professional appearance
- JUCE framework compatible
```
EOF

echo "✅ Created Gemini-powered UI designer agent"
echo ""

# Method 3: Hybrid orchestration
echo "Method 3: Hybrid Orchestration"
echo "-------------------------------"
echo "Use Claude Flow to orchestrate both Claude and Gemini:"
echo ""
cat > .claude-flow/gemini-integration.js << 'EOF'
// Gemini Integration for Claude Flow
// This allows the hive-mind to use Gemini for specific tasks

const geminiTasks = {
  uiDesign: {
    prompt: "Create beautiful UI component",
    model: "gemini-2.5-flash",
    changeMode: true
  },
  colorScheme: {
    prompt: "Generate professional color palette",
    model: "gemini-2.5-flash"
  },
  animation: {
    prompt: "Design smooth animation patterns",
    model: "gemini-2.5-flash"
  }
};

// Export for Claude Flow integration
module.exports = { geminiTasks };
EOF

echo "✅ Created Gemini integration config"
echo ""

# Method 4: Memory sharing between models
echo "Method 4: Cross-Model Memory"
echo "-----------------------------"
echo "Share context between Claude and Gemini:"
echo ""
echo "# Store Gemini's output in Claude Flow memory:"
echo 'GEMINI_OUTPUT=$(gemini:ask-gemini "Design knob")'
echo 'npx claude-flow@alpha memory store "gemini_design" "$GEMINI_OUTPUT"'
echo ""
echo "# Retrieve in Claude Flow:"
echo 'npx claude-flow@alpha memory query "gemini_design"'
echo ""

# Show current MCP servers
echo "📊 Current MCP Servers Available:"
echo "---------------------------------"
cat .claude.json 2>/dev/null | grep -A 1 '"command"' | grep -v "^--$" || echo "No MCP servers configured yet"
echo ""

echo "🚀 Recommended Workflow:"
echo "------------------------"
echo "1. Use Gemini for visual design generation"
echo "2. Use Claude for logic and integration"
echo "3. Use Claude Flow to orchestrate both"
echo ""
echo "Example combined command:"
echo 'npx claude-flow@alpha hive-mind spawn "Build UI with Gemini design and Claude logic" --agents ui-designer-gemini,juce-developer --claude'
echo ""
echo "✨ Gemini integration ready!"