# 🎨 Performia - AI-Powered Music Performance System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/PerformanceSuite/Performia)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![UI](https://img.shields.io/badge/UI-JUCE-orange.svg)](../../tree/ui-clean)
[![Backend](https://img.shields.io/badge/Backend-Python-blue.svg)](../../tree/backend-core)

## Overview

Performia is a professional audio interface for AI-powered music performance, featuring intelligent agents that collaborate with human musicians in real-time.

## 🌳 Repository Structure

### Active Branches

#### [`ui-clean`](../../tree/ui-clean) - Modern User Interface
- JUCE-based professional audio interface
- 6 operational modes (Studio, Live, Settings, Library, Display, Room)
- Dark theme with cyan accent colors
- Multi-model AI integration for development

#### [`backend-core`](../../tree/backend-core) - Core Backend System
- High-performance audio engine (<10ms latency)
- 4 AI music agents (Bass, Drums, Keys, Melody)
- OSC communication protocol (port 7772)
- SuperCollider synthesis engine

## 🚀 Quick Start

### Prerequisites
- JUCE 7.x Framework
- Python 3.9+
- SuperCollider 3.12+
- Node.js 18+ (for development tools)

### Installation

1. **Clone and select branch:**
```bash
git clone https://github.com/PerformanceSuite/Performia.git
cd Performia
```

2. **For UI development:**
```bash
git checkout ui-clean
# Follow UI setup instructions in branch README
```

3. **For backend development:**
```bash
git checkout backend-core
# Follow backend setup instructions in branch README
```

### Running the Complete System

```bash
# Terminal 1: Start backend
git checkout backend-core
python scripts/start_backend.py

# Terminal 2: Start UI
git checkout ui-clean
./build/Performia
```

## 📚 Documentation

- [UI Documentation](../../tree/ui-clean/docs)
- [Backend API](../../tree/backend-core/docs)
- [Wiki](../../wiki)

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- JUCE Framework by ROLI
- SuperCollider Community
- Claude Flow by rUv (development tool)

---

**Project Status**: Active Development

**Latest Release**: v2.0.0-alpha
