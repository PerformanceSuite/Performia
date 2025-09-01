# 🎯 MULTI-MODEL WORKFLOW GUIDE FOR PERFORMIA UI

## Quick Start: Creating Your First Component

### Step 1: Launch the Workflow
```bash
./create-knob-multimodel.sh
```

### Step 2: When Prompted for Gemini Design
In Claude Code, execute:
```
gemini:ask-gemini --changeMode true --prompt @.workflows/components/knob/design-prompt.txt
```

### Step 3: Store Gemini's Output
Copy Gemini's response and store it:
```bash
npx claude-flow@alpha memory store "knob_design_visual" "[PASTE GEMINI OUTPUT]" --namespace performia-components
```

### Step 4: Let Claude Implement
The workflow automatically spawns Claude to implement based on Gemini's design.

## 🎨 How the Multi-Model System Works

### Architecture
```
┌─────────────────────────────────────────────┐
│            ORCHESTRATOR (Claude Flow)        │
├─────────────┬───────────────┬────────────────┤
│   GEMINI    │  MEMORY STORE │    CLAUDE     │
│   (Design)  │   (Context)   │ (Implementation)│
├─────────────┼───────────────┼────────────────┤
│ • Visuals   │ • Persistence │ • JUCE Code   │
│ • Colors    │ • Sharing     │ • Logic       │
│ • Animation │ • Versioning  │ • Integration │
└─────────────┴───────────────┴────────────────┘
```

### Workflow Phases

#### Phase 1: Design (Gemini)
- Creates visual specifications
- Defines animations and interactions
- Specifies exact colors and gradients
- Provides implementation hints

#### Phase 2: Memory (Claude Flow)
- Stores Gemini's design
- Makes it accessible to all agents
- Maintains version history
- Enables cross-model collaboration

#### Phase 3: Implementation (Claude)
- Reads design from memory
- Generates JUCE C++ code
- Follows design specifications exactly
- Optimizes for performance

#### Phase 4: Validation (Both)
- Gemini validates visual compliance
- Claude validates code quality
- Both check integration points

## 📝 Component Templates

### For Rotary Knob
```cpp
// PerformiaKnob.h
class PerformiaKnob : public juce::Slider {
    // Gemini designs the visual aspects
    // Claude implements the functionality
};
```

### For Slider
```cpp
// PerformiaSlider.h  
class PerformiaSlider : public juce::Slider {
    // Vertical with LED meter
    // Gemini: Visual design
    // Claude: Audio integration
};
```

### For Button
```cpp
// PerformiaButton.h
class PerformiaButton : public juce::TextButton {
    // State animations
    // Gemini: State visuals
    // Claude: Event handling
};
```

## 🔧 Manual Commands

### Ask Gemini for Design
```bash
# Direct Gemini call
gemini:ask-gemini "Design a professional audio knob with dark theme #0A0E27 and cyan glow #00D4FF"

# With change mode for structured output
gemini:ask-gemini --changeMode true --prompt "Create JUCE knob component"

# Using a file
gemini:ask-gemini --prompt @design-spec.txt
```

### Store in Memory
```bash
# Store design
npx claude-flow@alpha memory store "component_design" "DESIGN_CONTENT" --namespace performia-ui

# Query stored designs
npx claude-flow@alpha memory query "design" --namespace performia-ui

# List all stored items
npx claude-flow@alpha memory list --namespace performia-ui
```

### Spawn Implementation
```bash
# Claude implements from memory
npx claude-flow@alpha swarm "Implement component from stored design" --memory-context "component_design" --claude

# With specific agents
npx claude-flow@alpha hive-mind spawn "Build UI component" --agents ui-designer-gemini,juce-developer --claude
```

## 🎯 Best Practices

### 1. Clear Separation of Concerns
- **Gemini**: Visual design, aesthetics, animations
- **Claude**: Code structure, logic, optimization
- **Never**: Mix responsibilities

### 2. Use Memory as Bridge
- Always store Gemini designs in memory
- Reference memory in Claude prompts
- Keep namespace organized

### 3. Validate Iteratively
- Test each component in isolation
- Get visual confirmation from Gemini
- Code review from Claude
- Integration test with both

### 4. Document the Pipeline
```bash
# After creating a component, document it
python3 session.py note "Created PerformiaKnob using Gemini design + Claude implementation"
python3 session.py checkpoint "Added rotary knob component"
```

## 🚀 Advanced Orchestration

### Parallel Component Creation
```python
# Use the orchestrator for multiple components
python3 .workflows/multi-model-orchestrator.py
# Select multiple components to build in parallel
```

### Batch Processing
```bash
# Create all basic components at once
for component in knob slider button meter; do
    npx claude-flow@alpha hive-mind spawn "Create $component with multi-model approach" --claude
done
```

### Continuous Improvement
```bash
# Gemini reviews implementation
gemini:ask-gemini "Review this component and suggest improvements" @src/components/basic/PerformiaKnob.cpp

# Store feedback
npx claude-flow@alpha memory store "knob_feedback" "GEMINI_FEEDBACK"

# Claude refines based on feedback
npx claude-flow@alpha swarm "Refine knob based on feedback" --memory-context "knob_feedback"
```

## 📊 Tracking Progress

### Check Component Status
```bash
# See what's been created
ls -la src/components/basic/

# Check memory for designs
npx claude-flow@alpha memory list --namespace performia-components

# Review session progress
python3 session.py status
```

### Validate Quality
```bash
# Run component tests
.workflows/components/knob/test-knob.sh

# Visual validation with Gemini
gemini:ask-gemini "Rate this UI component's professional quality from 1-10" @screenshot.png
```

## 🎨 Component Specifications

### Standard Sizes
- **Knob**: 64x64px
- **Slider**: 40x120px  
- **Button**: 80x32px
- **Meter**: 20x100px

### Color System
- **Background**: #0A0E27
- **Surface**: #1C2341
- **Primary**: #00D4FF (cyan)
- **Secondary**: #FF00AA (magenta)

### Animation Timings
- **Hover**: 150ms fade
- **Click**: 50ms response
- **Glow**: 2000ms pulse

## 💡 Tips for Success

1. **Always start with Gemini design** - Visual first, code second
2. **Store everything in memory** - Create audit trail
3. **Use changeMode for structure** - Gemini outputs clean code
4. **Validate visually** - Screenshots to Gemini for review
5. **Iterate quickly** - Small improvements, frequent validation

## 🔄 Workflow Commands Summary

```bash
# Complete workflow for one component
./create-knob-multimodel.sh

# Manual Gemini design
gemini:ask-gemini --changeMode true --prompt @design-prompt.txt

# Store design
npx claude-flow@alpha memory store "design" "CONTENT" --namespace performia-components

# Implement with Claude
npx claude-flow@alpha swarm "Implement from design" --memory-context "design" --claude

# Validate
gemini:ask-gemini "Validate implementation" @component.cpp
```

---

**Remember**: The power of this system is that Gemini excels at visual design while Claude excels at implementation. By orchestrating both through Claude Flow, you get the best of both worlds!