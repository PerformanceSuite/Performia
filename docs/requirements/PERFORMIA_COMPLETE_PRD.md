# PERFORMIA COMPLETE PRODUCT REQUIREMENTS DOCUMENT (PRD)
Version 2.0 | Date: September 1, 2025

## 🎯 PRODUCT VISION

Performia is an AI-powered music performance and composition system that enables musicians to collaborate with intelligent AI agents in real-time. The system features multiple specialized AI agents (Bass, Drums, Keys/Harmony, Melody) that can learn from human performers, suggest musical ideas, and perform alongside humans in both studio and live settings.

## 🎨 DESIGN PHILOSOPHY

### Visual Aesthetic
- **Dark Theme Base**: Background #0A0E27 with subtle gradients
- **Glowing Elements**: Cyan (#00D4FF) primary, Magenta (#FF00AA) secondary accents
- **Real-time Feedback**: Visual elements that respond to audio/MIDI activity
- **Professional DAW Quality**: Similar to Ableton Live, Logic Pro, Native Instruments
- **Clean Typography**: Modern, readable fonts with clear hierarchy
- **Intuitive Visual Feedback**: Immediate response to all user interactions

### User Experience Principles
- **Mode-Based Interface**: Different UI layouts optimized for different use cases
- **Progressive Disclosure**: Simple surface with advanced features available on demand
- **Visual Performance Feedback**: Users should "see" the music and AI activity
- **Minimal Cognitive Load**: Critical controls prominent, advanced features tucked away
- **Responsive Design**: Scalable interface that works on different screen sizes

## 🏗️ SYSTEM ARCHITECTURE

### Core Components
1. **AI Agents** (4 total)
   - Bass Agent (Port 8001)
   - Drums Agent (Port 8002)
   - Keys/Harmony Agent (Port 8003)
   - Melody Agent (Port 8004)

2. **Communication Layer**
   - OSC for real-time control (Port 7772)
   - SharedMemory IPC for audio data
   - MIDI I/O for hardware integration

3. **Audio Engine**
   - Low-latency audio processing (<10ms target)
   - Multi-channel I/O support
   - Real-time effects processing

4. **Visualization System**
   - Waveform displays
   - Spectrum analyzers
   - Neural network activity visualizers
   - Avatar animation system

## 📐 INTERFACE LAYOUT

### Global Structure (Persistent Across All Modes)

```
┌─────────────────────────────────────────────────────────────────┐
│                          TOP BAR                                │
│  [Logo] [Transport] [BPM] [Master Vol] [Mode] [User]           │
├─────┬───────────────────────────────────────────────────────────┤
│     │                                                           │
│  N  │                                                           │
│  A  │                    MAIN CONTENT AREA                     │
│  V  │                  (Mode-Specific Content)                  │
│     │                                                           │
│  R  │                                                           │
│  A  │                                                           │
│  I  │                                                           │
│  L  │                                                           │
│     │                                                           │
├─────┴───────────────────────────────────────────────────────────┤
│                         STATUS BAR                              │
│  [System Status] [CPU/Memory] [Latency] [Messages]             │
└─────────────────────────────────────────────────────────────────┘
```

### Top Bar Components
- **System Logo**: "PERFORMIA" branding
- **Global Transport**: Play, Pause, Stop, Record buttons
- **Tempo Control**: BPM display with tap tempo and slider
- **Master Volume**: Output level with LED meter
- **Mode Selector**: Studio | Live | Settings | Library | Display | Room
- **User Profile**: Login/preferences access

### Navigation Rail (Collapsible)
- **Primary Modes**:
  - 🎹 Studio Mode (Teaching/Composing)
  - 🎤 Live Mode (Performance)
  - ⚙️ Settings (System Config)
- **Extended Modes**:
  - 📚 Library (Songs/Patterns)
  - 🖥️ Display (Visual Output)
  - 🏠 Room (Physical Setup)
- **Additional**:
  - 👤 Avatars (Agent Visuals)
  - ❓ Help/Tutorial
  - 💾 Project Management

## 🎹 MODE 1: STUDIO MODE

### Purpose
Detailed control for teaching agents, composing, and fine-tuning musical arrangements.

### Layout Structure

#### A. Agent Control Matrix (Main Area - 60% width)
Each agent gets an expandable control panel with:

**Header Section**:
- Agent name and avatar thumbnail
- Status indicator (Learning/Performing/Idle)
- CPU/Memory usage meter
- Minimize/Maximize toggle

**Audio Controls**:
- Volume fader with LED meter
- Pan knob
- Mute/Solo buttons
- Input monitoring (if learning)
- Send levels (to effects/other agents)

**Personality Controls** (Agent-Specific):

*Bass Agent*:
- Root Focus (0-100): How closely to follow root notes
- Complexity (0-100): From simple roots to walking bass
- Groove Emphasis (0-100): Rhythmic vs melodic focus
- Swing Amount (0-100): Straight to heavily swung

*Drums Agent*:
- Beat Sync: Lock to grid vs human feel
- Swing (0-100): Timing adjustment
- Fill Probability (0-100): How often to add fills
- Intensity (0-100): From minimal to busy
- Kit Selection: Dropdown with preview

*Keys/Harmony Agent*:
- Arpeggiator: On/Off with pattern selector
- Voicing Complexity: Simple triads to extended chords
- Harmonic Density: Sparse to rich
- Rhythm Pattern: Whole notes to 16ths
- Inversion Preference: Root position to complex

*Melody Agent*:
- Note Density (0-100): Sparse to virtuosic
- Range (Low/Mid/High): Octave preference
- Articulation: Legato to staccato
- Phrase Length: Short motifs to long lines
- Call/Response: Interaction with human input

**Learning Interface**:
- "Learn from Input" toggle button (glowing when active)
- "Generate Ideas" button with variation count
- Neural network visualization (animated nodes/connections)
- Pattern history (last 5 learned patterns)
- Feedback buttons: 👍 Keep | 👎 Discard | 🔄 Refine
- Genre preset selector: Jazz, Rock, Funk, Electronic, Classical, etc.

**Theory Visualizer** (Collapsible):
- Circle of fifths with current position highlighted
- Chord progression display (Roman numerals)
- Scale/mode indicator
- Tension/resolution meter

**Pattern Editor** (Collapsible):
- Mini piano roll (8 bars visible)
- Velocity editor below
- Quantize controls
- Loop region selector

#### B. Timeline/Arrangement View (Bottom 30%)
- Horizontal timeline with measure numbers
- Color-coded tracks per agent
- Waveform/MIDI display
- Section markers (Intro, Verse, Chorus, etc.)
- Loop brackets
- Automation lanes (collapsible)

#### C. Human Input Monitor (Right Panel - 20% width)
- Real-time waveform display
- Note/chord detection display
- Performance analysis text:
  - "Detecting: Am - F - C - G progression"
  - "Tempo: 120 BPM (steady)"
  - "Dynamics: Building intensity"
- Agent response feed:
  - "Bass: Following root movement"
  - "Drums: Matching energy increase"
  - "Keys: Adding tension chords"

## 🎤 MODE 2: LIVE PERFORMANCE MODE

### Purpose
Streamlined interface for real-time performance with minimal distraction.

### Layout Structure

#### A. Agent Performance Cards (Grid Layout)
Large, visual cards for each agent (2x2 grid or 4x1 depending on screen):

**Visual Feedback**:
- Agent avatar (animated based on activity)
- Activity visualizer:
  - Bass: Pulsing waveform
  - Drums: Particle burst on hits
  - Keys: Harmonic spectrum
  - Melody: Flowing note trail
- Intensity meter (vertical bar)

**Essential Controls** (Large, Touch-Friendly):
- Main Parameter Knob (agent-specific):
  - Bass: Groove Intensity
  - Drums: Fill Density
  - Keys: Complexity
  - Melody: Activity Level
- Secondary Parameter:
  - Bass: Variation
  - Drums: Energy
  - Keys: Modulation
  - Melody: Range
- Mute button (large, obvious)
- Preset selector (1-8 quick access)

**Status Display**:
- Current action: "Following guitar lead"
- Musical context: "Playing in Am"
- Sync status: "Locked to human tempo"

#### B. Performance Overview (Bottom Strip)
- Master waveform of full mix
- Section indicator (where in song structure)
- Next section countdown
- Global intensity slider
- Panic button (reset all agents)

#### C. Human Input Monitor (Collapsible Top Bar)
- Compact waveform
- Detected key/tempo
- Recording indicator

## ⚙️ MODE 3: SETTINGS PANEL

### Purpose
System configuration, audio setup, and diagnostics.

### Layout Structure (Tabbed Interface)

#### Tab 1: Audio Configuration
**Interface Setup**:
- Input device selector with channel routing
- Output device selector with channel routing
- Sample rate selector (44.1, 48, 96, 192 kHz)
- Buffer size (64, 128, 256, 512, 1024 samples)
- Driver selection (ASIO, Core Audio, WASAPI)

**Level Management**:
- Input gain controls per channel
- Output level controls
- LED meters for all channels
- Clipping indicators

#### Tab 2: Latency Optimization
**Calibration Display**:
- Large latency readout (e.g., "4.7 ms")
- Round-trip latency graph
- Jitter visualization
- "Run Calibration" wizard
- Automatic optimization suggestions

**Compensation Settings**:
- Plugin delay compensation
- Recording offset
- Lookahead buffer

#### Tab 3: AI Agent Configuration
**Global Settings**:
- AI Response Time (Fast/Balanced/Smooth)
- Learning Rate (Conservative/Normal/Aggressive)
- Memory Management (RAM allocation)

**Per-Agent Settings**:
- Enable/Disable toggle
- Processing priority
- Neural network model selection
- Training data management
- "Reset Learning" buttons

#### Tab 4: Interface Customization
**Appearance**:
- Theme selector with preview
- Accent color picker
- Font size scaling
- Animation speed
- Widget density

**Layout Options**:
- Mode arrangement
- Panel docking preferences
- Keyboard shortcuts editor

#### Tab 5: System Diagnostics
**Performance Monitoring**:
- CPU usage (per core)
- GPU usage
- RAM usage
- Disk I/O
- Network activity (OSC/MIDI)

**Debug Tools**:
- Log viewer with filters
- Message inspector
- Performance profiler
- Crash reports

## 📚 MODE 4: LIBRARY PANEL

### Purpose
Manage songs, patterns, presets, and media content.

### Layout Structure

#### A. Content Browser (Left Panel - 30%)
**Categories**:
- 🎵 Songs (Complete arrangements)
- 🎹 Patterns (Loops/phrases)
- 🎛️ Presets (Agent configurations)
- 🎬 Videos (Background content)
- 🎨 Visuals (Static backgrounds)
- 📝 Chord Charts
- 🥁 Drum Patterns

**Filters**:
- Genre tags
- Tempo range
- Key signature
- Time signature
- Difficulty level
- User ratings

#### B. Preview Area (Center - 50%)
**Song/Pattern Preview**:
- Waveform overview
- Play/pause controls
- Tempo adjustment
- Key transpose
- Section markers

**Metadata Display**:
- Title, artist, duration
- Original tempo/key
- Included agents
- Difficulty rating
- User notes

#### C. Agent Assignment (Right Panel - 20%)
**Quick Setup**:
- Drag patterns to agents
- Auto-assign by genre
- Complexity matching
- "Load into Studio" button

## 🖥️ MODE 5: DISPLAY CONFIGURATION

### Purpose
Configure visual output for performances and streaming.

### Layout Structure

#### A. Display Setup (Main Area)
**Output Configuration**:
- Display selection (multiple monitors)
- Resolution settings
- Fullscreen/windowed mode
- Output routing (NDI, Syphon, etc.)

#### B. Content Mixer
**Visual Layers** (with opacity/blend modes):
1. Background (static image/video)
2. Avatar layer (agent animations)
3. Live camera feeds
4. Particle effects
5. Audio visualizers
6. Lyrics/text overlay

**Per-Layer Controls**:
- Visibility toggle
- Opacity slider
- Blend mode selector
- Position/scale controls
- Effects (blur, glow, etc.)

#### C. Avatar Configuration
**Per-Agent Avatar Settings**:
- Avatar model selection
- Animation style (subtle to energetic)
- Position on screen
- Size scaling
- Reaction sensitivity to audio

**Animation Triggers**:
- Note onset detection
- Amplitude following
- Frequency response
- Beat sync

#### D. Scene Management
**Scene Presets**:
- Store complete visual configurations
- Transition effects between scenes
- MIDI/OSC triggering
- Timeline automation

## 🏠 MODE 6: ROOM SETUP

### Purpose
Configure physical space for optimal recording and performance.

### Layout Structure

#### A. Room Visualization (Main Area)
**2D/3D Room View**:
- Draggable room layout
- Mic placement indicators
- Camera positions
- Monitor placement
- Instrument zones

#### B. Microphone Configuration
**Per-Mic Settings**:
- Input channel assignment
- Gain staging
- Polar pattern display
- Phase alignment tools
- Room correction EQ

**Mic Array Patterns**:
- Stereo pair configurations
- Surround setups
- Ambisonic arrays

#### C. Camera Setup
**Camera Management**:
- Camera feed preview grid
- Resolution/framerate settings
- Auto-switching rules
- Motion detection zones
- PTZ control (if supported)

#### D. Acoustic Analysis
**Room Measurement**:
- RT60 analysis
- Frequency response
- Standing wave detection
- Treatment suggestions
- Before/after comparison

## 👤 AVATARS PANEL (Sub-Mode)

### Purpose
Detailed avatar customization for each AI agent.

### Features
**Avatar Selection**:
- Character library (humanoid, abstract, robotic)
- Custom model import (FBX, OBJ)
- Texture/material editor

**Animation Behavior**:
- Idle animations
- Performance animations
- Transition smoothness
- Audio-reactive parameters
- Facial expressions (if applicable)

**Visual Style**:
- Rendering style (realistic, cartoon, abstract)
- Shader effects
- Particle systems
- Aura/glow effects

## 🔧 TECHNICAL SPECIFICATIONS

### Performance Requirements
- **Latency**: <10ms round-trip audio
- **Frame Rate**: 60 FPS UI minimum
- **CPU Usage**: <50% on modern quad-core
- **Memory**: <2GB RAM base usage
- **Startup Time**: <5 seconds

### Audio Specifications
- **Sample Rates**: 44.1, 48, 96, 192 kHz
- **Bit Depth**: 24-bit, 32-bit float
- **Channel Count**: Up to 32 in/out
- **Plugin Format**: VST3, AU (future)

### Network Protocols
- **OSC**: Primary control protocol
- **MIDI**: Hardware integration
- **WebSocket**: Remote control
- **NDI/Syphon**: Video output

### File Formats
- **Audio**: WAV, AIFF, FLAC, MP3
- **MIDI**: Type 0, Type 1
- **Presets**: JSON
- **Projects**: Custom binary or XML

## 🎯 INTERACTION PATTERNS

### Mouse/Trackpad
- **Click**: Select/activate
- **Drag**: Adjust values/move items
- **Right-click**: Context menu
- **Scroll**: Zoom/scroll views
- **Modifier keys**: Fine adjustment (Shift), reset (Ctrl/Cmd)

### Keyboard Shortcuts
- **Space**: Play/pause
- **R**: Record
- **Tab**: Next agent
- **1-6**: Mode switching
- **Ctrl/Cmd+S**: Save project
- **Ctrl/Cmd+Z**: Undo

### Touch (Future)
- **Tap**: Select
- **Drag**: Adjust
- **Pinch**: Zoom
- **Two-finger drag**: Pan
- **Long press**: Context menu

### MIDI Control
- **CC Mapping**: All parameters mappable
- **Note Input**: Trigger functions
- **Program Change**: Preset selection
- **MMC**: Transport control

## 🚀 IMPLEMENTATION PRIORITIES

### Phase 1: Core Functionality (MVP)
1. Studio Mode with basic agent controls
2. Audio I/O configuration
3. OSC communication
4. Basic visualization

### Phase 2: Performance Features
1. Live Mode interface
2. Preset management
3. MIDI integration
4. Latency optimization

### Phase 3: Advanced Features
1. Library system
2. Avatar system
3. Display configuration
4. Room setup tools

### Phase 4: Polish & Enhancement
1. Advanced visualizations
2. Machine learning improvements
3. Cloud sync
4. Mobile control app

## 📊 SUCCESS METRICS

### User Experience
- Setup time: <5 minutes
- Time to first sound: <30 seconds
- Mode switch time: <100ms
- Parameter adjustment latency: <16ms

### Technical Performance
- Audio dropouts: <1 per hour
- UI frame drops: <1%
- Memory leaks: None
- Crash rate: <0.1%

### User Satisfaction
- Intuitive rating: >4/5
- Professional appearance: >4.5/5
- Feature completeness: >4/5
- Stability rating: >4.5/5

## 🔄 REVISION HISTORY

- v2.0 (Current): Complete PRD with all panels
- v1.0: Initial three-mode design
- v0.5: Concept draft

---

**Note**: This PRD represents the complete vision for Performia. Implementation should be approached incrementally, starting with core functionality and expanding based on user feedback and technical constraints.