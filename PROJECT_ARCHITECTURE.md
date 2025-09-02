# PERFORMIA PROJECT ARCHITECTURE ANALYSIS
Date: September 1, 2025

## 🎯 Current Situation

### Performia-UI-Clean Status
- **Type**: Frontend UI application (JUCE-based)
- **Dependencies**: Needs backend for AI agents
- **Communication**: OSC (port 7772) and IPC
- **Status**: Clean slate, ready for development

### Performia-system Status
- **Type**: Backend + old UI (messy)
- **Contains**: Working audio engine, OSC server, AI agent system
- **Problem**: UI is broken/messy but backend works
- **Ports**: OSC on 7772, Agents on 8001-8004

## 🏗️ Architecture Options

### Option 1: SEPARATED ARCHITECTURE (Recommended) ✅
```
┌─────────────────────────┐     ┌─────────────────────────┐
│   Performia-UI-Clean    │     │    Performia-system     │
│     (Frontend Only)     │ OSC │   (Backend Only)        │
│                         │<--->│                         │
│  - Beautiful JUCE UI    │7772 │  - Audio Engine         │
│  - 6 Modes              │     │  - AI Agents            │
│  - Visualization        │ IPC │  - OSC Server           │
│  - No audio processing  │<--->│  - SuperCollider        │
└─────────────────────────┘     └─────────────────────────┘
```

**Pros:**
- Clean separation of concerns
- Can develop/test independently
- Backend already works
- UI can be shipped separately
- Multiple UIs possible (web, mobile)

**Cons:**
- Requires both running
- Network communication overhead

### Option 2: MONOLITHIC ARCHITECTURE
```
┌─────────────────────────────────────┐
│        Performia-Complete           │
│                                     │
│  - UI (from UI-Clean)               │
│  - Audio Engine (from system)       │
│  - AI Agents (from system)          │
│  - Everything in one app            │
└─────────────────────────────────────┘
```

**Pros:**
- Single executable
- No network communication
- Easier deployment

**Cons:**
- Need to merge codebases
- Risk breaking working backend
- Harder to maintain

### Option 3: HYBRID ARCHITECTURE (Best Long-term) 🌟
```
┌─────────────────────────────────────┐
│        Performia-UI-Clean           │
│                                     │
│  UI Layer (JUCE)                    │
│  ├── Optional: Embedded Backend     │
│  │   (compile-time flag)            │
│  └── Or: OSC Client Mode            │
│      (connect to external backend)  │
└─────────────────────────────────────┘
```

**Pros:**
- Flexible deployment
- Can run standalone or connected
- Single codebase for UI
- Progressive migration path

**Cons:**
- More complex build system
- Need conditional compilation

## 📋 What Needs to Be Done

### For SEPARATED Architecture (Quickest Path):

#### 1. In Performia-UI-Clean:
```cpp
// src/core/OSCClient.cpp - NEW
class OSCClient {
    void connectToBackend(port=7772);
    void sendAgentCommand(agent, command);
    void receiveAudioData();
};
```

#### 2. In Performia-system:
```bash
# Just run the backend without UI
./run_performia.sh --headless
```

### For GitHub Repository:

#### Create Two Repos:
1. **performia-ui** (from Performia-UI-Clean)
   - Pure UI repository
   - README explains backend dependency
   - Releases as standalone UI

2. **performia-backend** (cleaned from Performia-system)
   - Remove broken UI code
   - Keep audio engine and agents
   - Run as service/daemon

#### Or One Monorepo:
```
performia/
├── packages/
│   ├── ui/          (Performia-UI-Clean)
│   ├── backend/     (Performia-system core)
│   └── shared/      (Common types/protocols)
├── README.md
└── package.json
```

## 🚀 Recommended Action Plan

### Phase 1: Get It Working (Separated)
1. **Keep projects separate initially**
2. **Copy needed interfaces** from Performia-system:
   ```bash
   # Copy only what's needed
   cp Performia-system/src/core/AudioEngine.h Performia-UI-Clean/src/core/
   cp Performia-system/src/core/OSCProtocol.h Performia-UI-Clean/src/core/
   ```

3. **Implement OSC client** in UI-Clean:
   ```cpp
   // Minimal connection to backend
   class BackendConnection {
       bool connect();
       void sendCommand(string cmd);
       AudioData receiveAudio();
   };
   ```

4. **Run both for testing**:
   ```bash
   # Terminal 1: Backend
   cd Performia-system && ./run_performia.sh --headless
   
   # Terminal 2: UI
   cd Performia-UI-Clean && ./Performia
   ```

### Phase 2: GitHub Setup
```bash
# Create new repo for UI
cd Performia-UI-Clean
git remote add origin https://github.com/yourusername/performia-ui.git
git push -u origin main

# Create backend repo (cleaned)
cd Performia-system
# Remove UI files first
rm -rf gui/ PerformiaJUCE/Source/Main* 
git init
git remote add origin https://github.com/yourusername/performia-backend.git
```

### Phase 3: Integration (Later)
- Add backend as submodule
- Or create unified build system
- Docker compose for both

## 🎯 Answer to Your Questions

### Q: Does Performia-UI-Clean contain everything to run?
**A: No**, currently it's just the UI structure. It needs:
1. OSC client implementation (not done yet)
2. Backend running (from Performia-system)
3. JUCE framework added to project

### Q: Does it refer to Performia-system?
**A: Not directly**, but it expects:
- OSC server on port 7772
- AI agents on ports 8001-8004
- Same protocol/message format

### Q: Do you need a new GitHub repo?
**A: Yes**, recommended structure:
- `performia-ui` - The clean UI (from UI-Clean)
- `performia-backend` - The working backend (from system)
- Later: `performia` - Unified version

## 📝 Immediate Next Steps

1. **Decide on architecture** (I recommend Separated for now)

2. **Copy minimal backend interfaces**:
   ```bash
   cd Performia-UI-Clean
   mkdir -p src/core/interfaces
   # Copy only header files for OSC protocol
   ```

3. **Implement OSC client stub**:
   ```cpp
   // Just enough to connect
   class MockBackend {
       // For UI development without backend
   };
   ```

4. **Create GitHub repos**:
   ```bash
   # UI repo (clean, new)
   gh repo create performia-ui --public
   
   # Backend repo (extract from system)
   gh repo create performia-backend --public
   ```

## 🔄 Migration Path

```
Current State:
- Performia-system (messy but working backend + broken UI)
- Performia-UI-Clean (clean UI structure, no implementation)

Step 1: Separated Development
- UI-Clean connects to system via OSC
- Develop UI against working backend

Step 2: Clean Separation  
- Extract backend from system
- Remove broken UI from system
- Two clean repos

Step 3: Future Integration
- Combine into single app
- Or keep as microservices
- Your choice based on needs
```

## ✅ Summary

**Performia-UI-Clean is NOT standalone yet**. It needs:
1. OSC client implementation (~200 lines of code)
2. Backend running (use Performia-system for now)
3. JUCE framework integration

**Recommended approach:**
1. Keep them separate initially
2. Develop UI against existing backend
3. Create two GitHub repos
4. Later decide on monolithic vs microservices

The separation is actually GOOD - it forces clean architecture!