# 🎨 Performia UI Clean

## Professional Audio Interface for AI-Powered Music Performance System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/performia/ui-clean)
[![JUCE](https://img.shields.io/badge/JUCE-7.x-orange.svg)](https://juce.com)
[![Claude Flow](https://img.shields.io/badge/Claude%20Flow-2.0.0-green.svg)](https://github.com/ruvnet/claude-flow)

## 🎯 Overview

Performia UI Clean is a complete rebuild of the Performia audio interface, designed to provide professional-grade control over AI-powered music agents. The system features six specialized modes for different use cases, from studio composition to live performance.

## ✨ Features

### 🎹 Six Specialized Modes
- **Studio Mode**: Detailed control for teaching and composing with AI agents
- **Live Mode**: Streamlined interface for stage performance
- **Settings Mode**: System configuration and audio setup
- **Library Mode**: Manage songs, patterns, and presets
- **Display Mode**: Configure visual output for performances
- **Room Mode**: Physical space setup and calibration

### 🤖 Four AI Agents
- **Bass Agent**: Intelligent bass lines with groove control
- **Drums Agent**: Adaptive rhythm generation
- **Keys/Harmony Agent**: Chord progressions and harmonization
- **Melody Agent**: Lead lines and melodic phrases

### 🎨 Professional Design
- Dark theme optimized for stage and studio use
- Smooth 60 FPS animations
- Responsive controls with visual feedback
- DAW-quality interface comparable to Ableton/Logic

## 🚀 Quick Start

### Prerequisites
- macOS 10.15+ or Windows 10+
- JUCE 7.x framework
- CMake 3.15+
- C++17 compatible compiler
- Node.js 18+ (for Claude Flow)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Performia-UI-Clean.git
cd Performia-UI-Clean
```

2. Initialize Claude Flow (for AI development assistance):
```bash
npx claude-flow@alpha init --force
```

3. Build the project:
```bash
mkdir build && cd build
cmake ..
make -j4
```

4. Run the application:
```bash
./Performia
```

## 🏗️ Project Structure

```
Performia-UI-Clean/
├── src/
│   ├── core/              # Backend integration
│   ├── components/        # UI components
│   ├── modes/            # Application modes
│   ├── layouts/          # Window layouts
│   └── main/             # Entry point
├── resources/            # Assets
├── docs/                # Documentation
├── tests/               # Test suite
└── .claude/             # AI assistance config
```

## 🔧 Development

### Using Claude Code

This project is optimized for development with Claude Code. See [CLAUDE.md](CLAUDE.md) for:
- Slash commands for session management
- Development workflow
- Component templates
- Troubleshooting guide

### Using Claude Flow

The project uses Claude Flow's hive-mind system for orchestrated development:

```bash
# Check status
npx claude-flow@alpha hive-mind status

# Spawn a task
npx claude-flow@alpha swarm "implement bass agent panel" --claude

# Query memory
npx claude-flow@alpha memory query "working components"
```

## 📊 Technical Specifications

### Performance Targets
- **Latency**: <10ms round-trip audio
- **Frame Rate**: 60 FPS UI rendering
- **CPU Usage**: <30% idle, <50% active
- **Memory**: <500MB base footprint

### Communication
- **OSC**: Port 7772 for real-time control
- **IPC**: Shared memory for audio buffers
- **MIDI**: Full MIDI I/O support

## 🎨 Design System

### Color Palette
- **Background**: `#0A0E27` (Dark blue-black)
- **Primary**: `#00D4FF` (Cyan)
- **Secondary**: `#FF00AA` (Magenta)
- **Success**: `#00FF88` (Green)
- **Warning**: `#FFB800` (Orange)
- **Error**: `#FF3366` (Red)

### Components
- Custom rotary knobs with glow effects
- Vertical sliders with LED meters
- Animated buttons with state feedback
- Real-time audio visualizers

## 📚 Documentation

- [Complete PRD](docs/requirements/PERFORMIA_COMPLETE_PRD.md) - Full product requirements
- [Implementation Strategy](docs/PERFORMIA_IMPLEMENTATION_STRATEGY.md) - Development roadmap
- [API Documentation](docs/api/README.md) - Component APIs
- [User Guide](docs/guides/USER_GUIDE.md) - End-user documentation

## 🧪 Testing

Run the test suite:
```bash
# Unit tests
npm test

# UI tests
npm run test:ui

# Integration tests
npm run test:integration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- JUCE framework by ROLI
- Claude Flow by rUv
- Audio engine based on SuperCollider
- UI inspired by Ableton Live and Native Instruments

## 🆘 Support

- [Issue Tracker](https://github.com/yourusername/Performia-UI-Clean/issues)
- [Discord Community](https://discord.gg/performia)
- [Documentation Wiki](https://github.com/yourusername/Performia-UI-Clean/wiki)

## 🚦 Project Status

| Phase | Status | Progress |
|-------|--------|----------|
| Foundation | 🟡 In Progress | 0% |
| Basic Components | ⏳ Pending | 0% |
| Studio Mode | ⏳ Pending | 0% |
| Live Mode | ⏳ Pending | 0% |
| Backend Integration | ⏳ Pending | 0% |
| Extended Modes | ⏳ Pending | 0% |
| Polish & Optimization | ⏳ Pending | 0% |

---

**Current Focus**: Building foundation with navigation between all 6 modes

**Last Updated**: September 1, 2025