# 🎨 PERFORMIA UI CLEAN - CLAUDE CODE ASSISTANT GUIDE
Version: 2.0 | Date: September 1, 2025 | Project: Professional Audio Interface

## 🎯 PROJECT OVERVIEW

You are building **Performia UI Clean**, a professional-grade audio interface for an AI-powered music performance system. This is a complete rebuild after previous attempts failed due to poor integration and lack of orchestration.

### Current Status
- ✅ Claude Flow initialized with hive-mind system
- ✅ Project structure created
- ✅ Requirements documented in PRD
- ⏳ Ready to begin Phase 1: Foundation

### Key Technologies
- **Framework**: JUCE 7.x (C++ audio framework)
- **Build System**: CMake
- **Communication**: OSC (port 7772), SharedMemory IPC
- **AI Orchestration**: Claude Flow v2.0.0
- **Theme**: Dark (#0A0E27) with cyan (#00D4FF) accents

## 📋 SLASH COMMANDS FOR CLAUDE CODE

### Session Management Commands
```
/session new [name]        - Start a new development session
/session continue         - Continue the last session
/session list            - Show all sessions
/session load [id]       - Load a specific session
/session save            - Save current session state
/session status          - Show current session info
```

### Development Commands
```
/mode [studio|live|settings|library|display|room]  - Switch to mode development
/component [name]        - Create a new component
/test [component|mode]   - Run tests
/build                   - Build the project
/run                     - Run the application
/debug                   - Start with debugger
```

### Claude Flow Integration
```
/flow status             - Check Claude Flow hive-mind status
/flow spawn [task]       - Spawn a new swarm task
/flow memory [query]     - Query Claude Flow memory
/flow agents            - List active agents
```

### Git Commands
```
/git status             - Check git status
/git checkpoint [msg]   - Create a checkpoint
/git rollback          - Rollback to last checkpoint
```

## 🏗️ PROJECT STRUCTURE

```
Performia-UI-Clean/
├── src/
│   ├── core/              # Backend integration (OSC, IPC, Audio)
│   ├── components/        # UI components
│   │   ├── basic/        # Knobs, sliders, buttons
│   │   ├── compound/     # Agent panels, transport
│   │   └── specialized/  # Visualizers, avatars
│   ├── modes/            # The 6 main modes
│   ├── layouts/          # Window layouts
│   └── main/             # Application entry
├── resources/            # Images, shaders, presets
├── docs/                # Documentation
├── tests/               # Test files
├── .sessions/           # Session management
└── .claude/             # Claude Flow configuration
```

## 🎨 DESIGN SYSTEM

### Color Palette
```cpp
namespace PerformiaColors {
    const Colour background   = Colour::fromString("#0A0E27");  // Dark blue-black
    const Colour surface      = Colour::fromString("#1C2341");  // Lighter surface
    const Colour primary      = Colour::fromString("#00D4FF");  // Cyan
    const Colour secondary    = Colour::fromString("#FF00AA");  // Magenta
    const Colour success      = Colour::fromString("#00FF88");  // Green
    const Colour warning      = Colour::fromString("#FFB800");  // Orange
    const Colour error        = Colour::fromString("#FF3366");  // Red
    const Colour text         = Colour::fromString("#D0D0D0");  // Light gray
    const Colour textDim      = Colour::fromString("#808080");  // Dim gray
}
```

### Component Specifications
- **Knobs**: 64x64px default, cyan glow on hover, smooth rotation
- **Sliders**: Vertical with LED meter, 40x120px default
- **Buttons**: 80x32px default, state animations
- **Panels**: Rounded corners (8px), subtle drop shadow

## 🚀 IMPLEMENTATION PHASES

### Phase 1: Foundation ✅ CURRENT
- [ ] Create main window with proper sizing (1280x800 default)
- [ ] Implement navigation between 6 modes
- [ ] Apply dark theme globally
- [ ] Create top bar with transport controls
- [ ] Add status bar with system info

### Phase 2: Basic Components
- [ ] PerformiaKnob with glow effect
- [ ] PerformiaSlider with LED meter
- [ ] PerformiaButton with states
- [ ] PerformiaMeter for levels
- [ ] TransportControl component

### Phase 3: Studio Mode
- [ ] 4 Agent control panels
- [ ] Personality sliders
- [ ] Learning interface
- [ ] Timeline view
- [ ] Human input monitor

### Phase 4: Live Mode
- [ ] Large agent cards
- [ ] Activity visualizers
- [ ] Essential controls
- [ ] Performance strip

### Phase 5: Backend Integration
- [ ] OSC communication (port 7772)
- [ ] IPC implementation
- [ ] Agent synchronization
- [ ] Latency measurement

### Phase 6: Extended Modes
- [ ] Settings panel
- [ ] Library browser
- [ ] Display configuration
- [ ] Room setup

### Phase 7: Polish
- [ ] Animations (60 FPS)
- [ ] Performance optimization
- [ ] Memory management
- [ ] Final testing

## 🔧 KEY BACKEND INTERFACES

### OSC Messages (Port 7772)
```cpp
// Agent control
/agent/[drums|bass|keys|melody]/enable [0|1]
/agent/[name]/volume [0.0-1.0]
/agent/[name]/parameter/[param] [value]

// Transport
/transport/play
/transport/stop
/transport/tempo [60-200]

// System
/system/latency
/system/cpu
```

### IPC Shared Memory
```cpp
// Audio buffer structure
struct AudioBuffer {
    float samples[BUFFER_SIZE];
    uint32_t writePos;
    uint32_t readPos;
    std::atomic<bool> dataAvailable;
};
```

## 🐛 COMMON ISSUES & SOLUTIONS

### Issue: UI doesn't update
**Solution**: Check timer callback, ensure `repaint()` is called

### Issue: OSC not connecting
**Solution**: Verify port 7772 is free, check firewall

### Issue: High CPU usage
**Solution**: Reduce timer frequency, optimize paint methods

### Issue: Components not visible
**Solution**: Check `addAndMakeVisible()`, verify bounds

## 📊 PERFORMANCE TARGETS

- **Latency**: <10ms round-trip
- **Frame Rate**: 60 FPS consistent
- **CPU Usage**: <30% idle, <50% active
- **Memory**: <500MB base usage
- **Startup**: <3 seconds

## 🎯 CURRENT FOCUS

**TODAY'S GOAL**: Create the foundation with working navigation between all 6 modes.

**Key Tasks**:
1. Set up main window
2. Create mode enum and switcher
3. Implement navigation rail
4. Add top bar with mode indicator
5. Test mode switching

## 💡 IMPORTANT REMINDERS

1. **Always reference the PRD** at `/docs/requirements/PERFORMIA_COMPLETE_PRD.md`
2. **Test visually** - Take screenshots to verify appearance
3. **Use Claude Flow memory** to track what works
4. **Commit working code** frequently
5. **One component at a time** - Don't try to build everything at once

## 🔄 SESSION CONTINUITY

When starting a new session, ALWAYS:
1. Check current phase status
2. Review last session's work
3. Load session state: `/session continue`
4. Verify backend is running
5. Check Claude Flow status: `/flow status`

## 🆘 GETTING HELP

If stuck:
1. Query Claude Flow memory: `/flow memory "last working"`
2. Check implementation strategy: `/docs/PERFORMIA_IMPLEMENTATION_STRATEGY.md`
3. Review PRD requirements: `/docs/PERFORMIA_COMPLETE_PRD.md`
4. Use swarm for help: `/flow spawn "debug [specific issue]"`

## 🎨 QUICK COMPONENT TEMPLATE

```cpp
// PerformiaComponent.h
#pragma once
#include <JuceHeader.h>
#include "PerformiaColors.h"

class PerformiaComponent : public juce::Component {
public:
    PerformiaComponent();
    ~PerformiaComponent() override;
    
    void paint(juce::Graphics& g) override;
    void resized() override;
    
private:
    // Add member variables
    
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PerformiaComponent)
};
```

## ✅ SUCCESS CHECKLIST

Before claiming any component/feature is complete:
- [ ] Visually matches PRD specifications
- [ ] Smooth animations at 60 FPS
- [ ] Proper hover/click feedback
- [ ] No memory leaks
- [ ] OSC messages working (if applicable)
- [ ] Screenshot taken for verification
- [ ] Code committed to git

---

**Remember**: This is a fresh start. We have all the requirements, proper orchestration via Claude Flow, and a clear plan. Follow the phases, test everything visually, and build one piece at a time.