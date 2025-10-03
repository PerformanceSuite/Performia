# Performia Master Development Plan
**World-Class Agentic Engineering Strategy**

**Created**: October 1, 2025
**Architect**: Senior Agentic Systems Engineer
**Status**: APPROVED - Execute Immediately
**Timeline**: 16 weeks to production-grade real-time system

---

## Executive Decision: The Optimal Path Forward

After analyzing the codebase, dependencies, and technical requirements, here is my expert recommendation:

### **We build in this EXACT order, no deviations:**

```
Phase 1: Python-Native Real-Time (Weeks 1-4)
    ↓
Phase 2: Musical Intelligence Layer (Weeks 5-10)
    ↓
Phase 3: Production Optimization (Weeks 11-16)
```

**Why NOT start with SuperCollider or JUCE?**

1. **SuperCollider** is not installed, requires separate runtime, adds deployment complexity
2. **JUCE C++** requires complete rewrite, 2-3 week learning curve, testing overhead
3. **Python + PyAudio + librosa** can achieve 20-50ms latency - good enough for MVP
4. **We already have** torch, librosa, demucs, asyncio - leverage what's installed

**The Rule**: Build working functionality first, optimize latency second.

---

## Phase 1: Python-Native Real-Time Foundation (4 weeks)

### Architecture Decision: Pure Python Stack

```
Live Audio Input (PyAudio/sounddevice)
         ↓
Real-Time Analysis Thread (20-50ms chunks)
    - Pitch detection (librosa.pyin)
    - Onset detection (librosa.onset)
    - Beat tracking (librosa.beat)
         ↓
Agent Message Bus (asyncio.Queue)
         ↓
Musical Agents (async decision makers)
    - Bass Agent
    - Drum Agent
    - Harmony Agent
         ↓
Audio Output Thread (sounddevice)
    - Mix agent outputs
    - Real-time synthesis
         ↓
WebSocket to Frontend
    - Visual feedback
    - Context updates
```

**Latency Budget:**
- Audio input: 10-20ms (PyAudio, 512 sample buffer @ 44.1kHz)
- Analysis: 5-15ms (librosa optimized)
- Agent decision: 5-10ms (simple rules initially)
- Audio output: 10-20ms (output buffer)
- **Total: 30-65ms** ← Acceptable for v1.0 (acoustic musicians naturally have 20-40ms timing variance)

### Sprint 2: Real-Time Audio Pipeline (Week 1-2)

**Goal**: Live audio input → pitch/beat detection → console output

**Deliverables:**
1. `backend/src/realtime/audio_input.py` - PyAudio wrapper for live input
2. `backend/src/realtime/analyzer.py` - Real-time pitch/onset/beat detection
3. `backend/src/realtime/message_bus.py` - AsyncIO message queue for events
4. Integration test: Sing into mic → see pitch values in real-time

**Dependencies to add:**
```bash
pip install pyaudio sounddevice python-osc websockets
```

**Success Criteria:**
- ✅ 44.1kHz audio input with <20ms latency
- ✅ Pitch detection updating 20x per second
- ✅ Beat detection within ±50ms accuracy
- ✅ Console showing real-time values

**Code Template:**
```python
# backend/src/realtime/audio_input.py
import sounddevice as sd
import numpy as np
import asyncio
from queue import Queue

class RealtimeAudioInput:
    """Real-time audio input with minimal latency."""

    def __init__(self, sample_rate=44100, block_size=512):
        self.sample_rate = sample_rate
        self.block_size = block_size  # 11.6ms latency at 44.1kHz
        self.audio_queue = Queue(maxsize=10)

    def callback(self, indata, frames, time, status):
        """Audio callback - runs in separate thread."""
        if status:
            print(f'Audio input error: {status}')
        self.audio_queue.put(indata.copy())

    def start(self):
        """Start audio stream."""
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            channels=1,
            callback=self.callback
        )
        self.stream.start()
        print(f"✅ Audio input started: {self.sample_rate}Hz, {self.block_size} samples")

    def get_block(self):
        """Get next audio block (blocking)."""
        return self.audio_queue.get()
```

### Sprint 3: First Musical Agent (Week 3-4)

**Goal**: Bass agent that plays along with live singing

**Deliverables:**
1. `backend/src/agents/base_agent.py` - Agent framework
2. `backend/src/agents/bass_agent.py` - Simple bass agent
3. `backend/src/agents/conductor.py` - Master coordinator
4. `backend/src/realtime/audio_output.py` - Synthesizer for agent notes
5. Integration test: Sing → bass agent plays root notes in key

**Agent Architecture:**
```python
# backend/src/agents/base_agent.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any
import asyncio

@dataclass
class MusicalContext:
    """Shared musical state."""
    beat: float          # Current beat (0, 1, 2, 3...)
    tempo: float         # BPM
    key: str            # "C", "Dm", etc.
    chord: str          # Current chord
    section: str        # "verse", "chorus"
    pitch_detected: float  # Hz from live input

class MusicalAgent(ABC):
    """Base class for all musical agents."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.enabled = True

    @abstractmethod
    async def decide(self, context: MusicalContext) -> List[Dict[str, Any]]:
        """Make musical decision based on context.

        Returns:
            List of note events: [{'midi': 60, 'velocity': 0.8, 'duration': 0.5}, ...]
        """
        pass

    async def play(self, notes: List[Dict], output_device):
        """Send notes to audio output."""
        for note in notes:
            await output_device.play_note(
                note['midi'],
                note['velocity'],
                note['duration']
            )
```

**Simple Bass Agent:**
```python
# backend/src/agents/bass_agent.py
class BassAgent(MusicalAgent):
    """Bass agent plays root notes on downbeats."""

    async def decide(self, context: MusicalContext):
        # Only play on beat 0 (downbeat)
        if context.beat % 4 != 0:
            return []

        # Get root note of current chord
        root_midi = self._chord_to_root(context.chord)

        return [{
            'midi': root_midi - 24,  # Two octaves down
            'velocity': 0.7,
            'duration': 0.9  # Slightly detached
        }]

    def _chord_to_root(self, chord: str) -> int:
        """Convert chord name to MIDI root note."""
        roots = {
            'C': 60, 'C#': 61, 'D': 62, 'Eb': 63,
            'E': 64, 'F': 65, 'F#': 66, 'G': 67,
            'Ab': 68, 'A': 69, 'Bb': 70, 'B': 71
        }
        # Simple parsing (e.g., "Cmaj7" -> "C")
        root_letter = chord[0:2] if len(chord) > 1 and chord[1] in ['#', 'b'] else chord[0]
        return roots.get(root_letter, 60)
```

**Success Criteria:**
- ✅ Bass agent plays root notes on downbeats
- ✅ Follows Song Map chord progression
- ✅ Audible synthesis (sine wave or simple synth)
- ✅ Timing within ±100ms of beat

---

## Phase 2: Musical Intelligence (6 weeks)

### Sprint 4: Multi-Agent Ensemble (Week 5-6)

**Goal**: Bass + Drums + Harmony playing together

**Deliverables:**
1. `backend/src/agents/drum_agent.py` - Basic drum patterns
2. `backend/src/agents/harmony_agent.py` - Chord voicings
3. Enhanced conductor with agent coordination
4. Improved synthesizer with multiple timbres

**Drum Agent Patterns:**
```python
class DrumAgent(MusicalAgent):
    """Drum agent plays rhythmic patterns."""

    def __init__(self, agent_id: str, pattern_style="basic_rock"):
        super().__init__(agent_id)
        self.pattern_style = pattern_style

    async def decide(self, context: MusicalContext):
        beat_position = context.beat % 4
        hits = []

        # Kick on 1 and 3
        if beat_position in [0, 2]:
            hits.append({'drum': 'kick', 'velocity': 0.8})

        # Snare on 2 and 4
        if beat_position in [1, 3]:
            hits.append({'drum': 'snare', 'velocity': 0.7})

        # Hi-hat on every beat
        hits.append({'drum': 'hihat', 'velocity': 0.5})

        return hits
```

**Success Criteria:**
- ✅ 3 agents playing simultaneously without conflicts
- ✅ Musical output sounds "together" (tight timing)
- ✅ Can toggle agents on/off during performance
- ✅ CPU usage <30% on modern hardware

### Sprint 5: Adaptive Following (Week 7-8)

**Goal**: Agents follow live performer's tempo and dynamics

**Deliverables:**
1. `backend/src/realtime/tempo_tracker.py` - Live tempo detection
2. Enhanced conductor with tempo adaptation
3. Dynamic following modes (click, adaptive, free)
4. Visual tempo indicator in frontend

**Adaptive Tempo Logic:**
```python
class AdaptiveConductor:
    """Conductor that follows human performer."""

    def __init__(self, song_map: Dict):
        self.song_map = song_map
        self.tempo = 120.0  # Initial tempo
        self.follow_mode = "adaptive"  # click, adaptive, free
        self.tempo_history = []

    async def process_beat_detection(self, detected_tempo: float):
        """Adapt to live performer's tempo."""
        if self.follow_mode == "click":
            # Ignore detected tempo, use fixed
            return

        if self.follow_mode == "adaptive":
            # Smooth adaptation (low-pass filter)
            self.tempo_history.append(detected_tempo)
            if len(self.tempo_history) > 8:
                self.tempo_history.pop(0)

            # Use median of recent tempos (robust to outliers)
            self.tempo = np.median(self.tempo_history)

        elif self.follow_mode == "free":
            # Immediate following
            self.tempo = detected_tempo
```

**Success Criteria:**
- ✅ Agents adapt to tempo changes within 2-3 beats
- ✅ Stable following (no jitter or oscillation)
- ✅ Works with ±20% tempo variation
- ✅ Graceful handling of missed beats

### Sprint 6: Advanced Musical Intelligence (Week 9-10)

**Goal**: Musically sophisticated agent decisions

**Deliverables:**
1. **Improved Bass Agent**: Walking bass, inversions, passing tones
2. **Improved Harmony Agent**: Jazz voicings, voice leading, tensions
3. **Improved Drum Agent**: Fills, dynamics, groove variations
4. **Style System**: Jazz, Pop, Rock, Classical patterns

**Jazz Bass Walking Pattern:**
```python
class JazzBassAgent(BassAgent):
    """Jazz walking bass lines."""

    async def decide(self, context: MusicalContext):
        beat_pos = context.beat % 4
        current_chord = context.chord
        next_chord = self._get_next_chord(context)

        # Walking bass plays on every beat
        if beat_pos == 0:
            # Root
            note = self._chord_to_root(current_chord)
        elif beat_pos == 1:
            # Chord tone (3rd or 5th)
            note = self._chord_to_third(current_chord)
        elif beat_pos == 2:
            # Chord tone (5th or 7th)
            note = self._chord_to_fifth(current_chord)
        elif beat_pos == 3:
            # Approach note to next chord
            next_root = self._chord_to_root(next_chord)
            note = next_root - 1  # Chromatic approach from below

        return [{'midi': note - 24, 'velocity': 0.7, 'duration': 0.95}]
```

**Success Criteria:**
- ✅ Bass lines sound musical (passing tones, voice leading)
- ✅ Chord voicings appropriate for style
- ✅ Drum patterns vary with section intensity
- ✅ Multiple style presets working

---

## Phase 3: Production Polish (6 weeks)

### Sprint 7: Performance Optimization (Week 11-12)

**Goal**: Reduce latency, increase reliability

**Deliverables:**
1. Profiling and bottleneck identification
2. Multi-threading for audio I/O
3. Optimized DSP routines (Cython/Numba)
4. Memory pool management (reduce GC)
5. Latency measurement dashboard

**Optimization Strategy:**
```python
# Use Numba JIT for hot paths
from numba import jit

@jit(nopython=True, cache=True)
def fast_pitch_detection(audio_block, sample_rate):
    """JIT-compiled pitch detection for 5-10x speedup."""
    # Autocorrelation method
    # ... optimized implementation
    return pitch_hz

# Use shared memory for zero-copy audio
import multiprocessing as mp
audio_buffer = mp.Array('f', buffer_size)
```

**Success Criteria:**
- ✅ Total latency <30ms (down from 50-65ms)
- ✅ CPU usage <25% (down from 30%)
- ✅ Zero audio dropouts in 10-minute test
- ✅ Supports 6+ agents simultaneously

### Sprint 8: Frontend Integration (Week 13-14)

**Goal**: Real-time visual feedback in Living Chart

**Deliverables:**
1. WebSocket server for real-time updates
2. Frontend visualizations for agent activity
3. Performance controls (enable/disable agents, tempo, style)
4. Latency monitoring UI
5. Recording/playback of sessions

**WebSocket Server:**
```python
# backend/src/realtime/websocket_server.py
from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

class RealtimeServer:
    def __init__(self):
        self.connections = []

    async def broadcast_context(self, context: MusicalContext):
        """Broadcast to all connected frontends."""
        message = {
            'type': 'context_update',
            'beat': context.beat,
            'chord': context.chord,
            'tempo': context.tempo,
            'section': context.section
        }

        for ws in self.connections:
            await ws.send_json(message)

    async def broadcast_agent_event(self, agent_id: str, notes: List):
        """Show agent playing notes."""
        message = {
            'type': 'agent_event',
            'agent': agent_id,
            'notes': notes,
            'timestamp': time.time()
        }

        for ws in self.connections:
            await ws.send_json(message)

@app.websocket("/realtime")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    server.connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    finally:
        server.connections.remove(websocket)
```

**Success Criteria:**
- ✅ Real-time beat indicator in UI (<50ms delay)
- ✅ Agent activity visualizations
- ✅ Performance controls working
- ✅ Smooth 60fps animations

### Sprint 9: Testing & Hardening (Week 15-16)

**Goal**: Production-ready reliability

**Deliverables:**
1. Comprehensive integration tests
2. Error recovery mechanisms
3. Audio device handling (hot-plug, sample rate mismatch)
4. Performance testing with musicians
5. Documentation and deployment guide

**Test Coverage:**
```python
# backend/tests/integration/test_realtime_system.py
import pytest
import asyncio

@pytest.mark.asyncio
async def test_full_performance_flow():
    """Test complete performance from input to output."""

    # Start system
    conductor = AdaptiveConductor(song_map)
    bass_agent = BassAgent("bass-1")
    drum_agent = DrumAgent("drums-1")

    # Simulate audio input
    audio_input = SimulatedAudioInput(test_file="test_vocals.wav")

    # Run for 30 seconds
    start_time = time.time()
    while time.time() - start_time < 30:
        # Process audio block
        audio_block = audio_input.get_block()

        # Analyze
        pitch = analyzer.detect_pitch(audio_block)
        beat_detected = analyzer.detect_beat(audio_block)

        # Update context
        if beat_detected:
            context.beat += 1

        # Agents decide and play
        bass_notes = await bass_agent.decide(context)
        drum_hits = await drum_agent.decide(context)

        await audio_output.render(bass_notes + drum_hits)

    # Assertions
    assert context.beat > 100  # At least 100 beats in 30s
    assert len(bass_notes_played) > 25  # Bass played on downbeats
    assert no_audio_dropouts
```

**Success Criteria:**
- ✅ 95%+ test coverage on critical paths
- ✅ Graceful degradation on errors
- ✅ Works on macOS, Linux, Windows
- ✅ Real musicians rate system as "usable"

---

## Technology Stack (Final)

### Core Audio
- **sounddevice** - Low-latency audio I/O (replaces PyAudio for better performance)
- **librosa** - Pitch/beat/onset detection
- **numpy/scipy** - DSP fundamentals

### Real-Time Processing
- **asyncio** - Async event loop for agents
- **multiprocessing** - Parallel audio I/O thread
- **numba** - JIT compilation for hot paths

### Synthesis
- **pyo** - Real-time audio synthesis in Python (simpler than SuperCollider for MVP)
- OR **synthesizer** package - Simple MIDI-like synthesis

### Communication
- **websockets** - Frontend real-time updates
- **FastAPI** - WebSocket server

### Why NOT SuperCollider/JUCE (for now)
1. **SuperCollider** - External dependency, deployment complexity, OSC overhead
2. **JUCE C++** - Complete rewrite, longer timeline, testing overhead
3. **Python stack** - Already installed, proven tools, faster iteration

**We can optimize to C++/SuperCollider in Phase 4 (post-v1.0) if needed.**

---

## Development Process

### Daily Workflow
1. **Morning standup** (async via commit messages)
2. **Code in 4-hour blocks** with tests
3. **Commit every working feature** (small, atomic commits)
4. **Evening review** of what worked, what didn't

### Weekly Milestones
- **Week 1**: Audio input working
- **Week 2**: Real-time analysis working
- **Week 3**: First agent playing notes
- **Week 4**: Bass agent following Song Map
- **Week 6**: Multi-agent ensemble
- **Week 8**: Adaptive following
- **Week 10**: Musical intelligence complete
- **Week 12**: Performance optimized
- **Week 14**: Frontend integrated
- **Week 16**: Production ready

### Quality Gates
Each sprint must pass:
- ✅ All tests passing
- ✅ Latency within budget
- ✅ CPU usage acceptable
- ✅ Demo working end-to-end

**No moving to next sprint until current sprint passes gates.**

---

## Risk Mitigation

### Technical Risks

**Risk**: Python too slow for real-time
- **Mitigation**: Use Numba JIT, profiling, multi-threading
- **Fallback**: Move hot paths to Cython or C++

**Risk**: Audio latency too high
- **Mitigation**: Small buffer sizes, optimized DSP
- **Fallback**: JUCE implementation (add 3-4 weeks)

**Risk**: Beat detection unreliable
- **Mitigation**: Multiple detection methods, smoothing
- **Fallback**: Click track mode only

**Risk**: Agents sound robotic/unmusical
- **Mitigation**: Study real performances, add humanization
- **Fallback**: Simplified patterns that work

### Process Risks

**Risk**: Scope creep
- **Mitigation**: Strict sprint boundaries, defer features
- **No new features until Phase 3 complete**

**Risk**: Getting stuck on optimization
- **Mitigation**: "Make it work, make it right, make it fast" - in that order
- **Ship working MVP, optimize later**

---

## Success Definition

### Minimum Viable Product (Week 16)
- ✅ Live audio input with pitch/beat detection
- ✅ 3 agents (bass, drums, harmony) playing together
- ✅ Follows Song Map structure
- ✅ Adapts to live performer tempo
- ✅ <50ms total latency
- ✅ Frontend shows real-time context
- ✅ Works on macOS/Linux/Windows
- ✅ Musicians can perform with it

### Nice to Have (Phase 4+)
- SuperCollider integration for professional synthesis
- JUCE engine for <10ms latency
- Machine learning for improvisation
- Multi-performer support
- Cloud deployment
- Mobile app

---

## The Plan in One Sentence

**Build a working Python-based real-time musical AI system in 16 weeks, then optimize to C++/SuperCollider if needed.**

---

## Commitment

I will execute this plan with:
- **No scope changes** until Phase 3 complete
- **Daily progress** with working code
- **Weekly demos** showing new capabilities
- **Transparent communication** when blocked
- **Quality over speed** - each sprint must work before moving on

---

## Next Action (Right Now)

**Sprint 2 starts immediately:**

1. Create `backend/src/realtime/` directory structure
2. Install dependencies: `pip install sounddevice numba pyo websockets`
3. Implement `audio_input.py` with live microphone input
4. Test: Sing into mic, see waveform data in console
5. Implement `analyzer.py` with real-time pitch detection
6. Test: Sing notes, see pitch values updating 20x/second

**Timeline**: This should take 2-3 days.

**I will not proceed to anything else until audio input and pitch detection are working perfectly.**

---

*This is the plan. We stick to it. No heroics, no shortcuts, no distractions.*

**Let's build Performia the right way.**

---

**Status**: READY TO EXECUTE
**First Commit**: Real-time audio input implementation
**Target**: Working demo by end of Week 2
