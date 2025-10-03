# Performia JUCE Audio Engine - Detailed Implementation Plan

**Created**: October 1, 2025
**Status**: Pre-Committee Review
**Target**: Sub-10ms audio latency for professional live performance
**Timeline**: 3 weeks to production-ready engine

---

## Executive Summary

This plan details the implementation of a JUCE-based C++ audio engine that will replace the Python audio I/O layer, achieving the required sub-10ms latency for professional live performance while maintaining seamless integration with the existing Python agent system.

**Key Decision**: Hybrid architecture - JUCE for audio, Python for AI, SuperCollider for synthesis.

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    JUCE C++ Audio Engine                      │
│                  (Core Audio / ASIO Driver)                   │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Audio Input Thread (Real-Time, Lock-Free)                   │
│    ├─ Audio I/O Callback (64 samples = 1.45ms @ 44.1kHz)   │
│    ├─ Pitch Detection (YIN algorithm ~3-5ms)                │
│    ├─ Onset Detection (Spectral Flux ~1-2ms)               │
│    └─ Beat Tracking (Autocorrelation ~2-3ms)               │
│         │                                                     │
│         ▼                                                     │
│  Lock-Free Ring Buffer (Audio Thread → OSC Thread)          │
│         │                                                     │
│         ▼                                                     │
│  OSC Sender Thread (Non-Real-Time)                          │
│    └─ Send events to Python (UDP, ~0.5ms)                  │
│                                                               │
└───────────────────────┬───────────────────────────────────────┘
                        │ OSC over UDP (localhost)
                        ▼
┌──────────────────────────────────────────────────────────────┐
│                 Python Agent Layer (asyncio)                  │
│                                                               │
│  OSC Receiver (Non-Real-Time)                                │
│    └─ Pitch, Onset, Beat events                             │
│         │                                                     │
│         ▼                                                     │
│  Message Bus (Already Built ✅)                              │
│         │                                                     │
│         ▼                                                     │
│  Musical Agents (5-20ms decision time acceptable)           │
│    ├─ Bass Agent                                            │
│    ├─ Drum Agent                                            │
│    ├─ Harmony Agent                                         │
│    └─ AI Conductor                                          │
│         │                                                     │
│         ▼                                                     │
│  OSC Sender to SuperCollider                                │
│                                                               │
└───────────────────────┬───────────────────────────────────────┘
                        │ OSC over UDP
                        ▼
┌──────────────────────────────────────────────────────────────┐
│              SuperCollider Synthesis Engine                   │
│                                                               │
│  SynthDefs (Already Exist ✅)                                │
│    ├─ Bass synth                                            │
│    ├─ Drum synth                                            │
│    └─ Harmony synth                                         │
│         │                                                     │
│         ▼                                                     │
│  Audio Output (2-5ms synthesis + output)                    │
│                                                               │
└──────────────────────────────────────────────────────────────┘

Total Latency Budget:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Input → JUCE analysis:           5-8ms   (real-time thread)
JUCE → Python (OSC):            0.5ms   (UDP localhost)
Python agent decision:          5-10ms  (non-real-time)
Python → SuperCollider (OSC):   0.5ms   (UDP localhost)
SuperCollider synthesis:        2-5ms   (real-time thread)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL:                         13-24ms  (Target: <10ms)
```

**Critical Optimization Needed**: We need to reduce Python agent decision time or parallelize it.

---

## Phase 1: JUCE Project Setup (Days 1-2)

### Goals
- ✅ JUCE framework installed and configured
- ✅ CMake build system working
- ✅ Basic audio I/O callback functioning
- ✅ Cross-platform build (macOS, Linux, Windows)

### Deliverables

#### 1. Project Structure
```
backend/juce/
├── CMakeLists.txt                    # CMake build configuration
├── Source/
│   ├── Main.cpp                      # Application entry point
│   ├── PerformiaAudioEngine.h        # Main audio engine class
│   ├── PerformiaAudioEngine.cpp      # Implementation
│   ├── AudioAnalyzer.h               # Real-time analysis
│   ├── AudioAnalyzer.cpp
│   ├── OSCCommunicator.h             # OSC send/receive
│   └── OSCCommunicator.cpp
├── Builds/                           # Generated by Projucer
│   ├── MacOSX/
│   ├── Linux/
│   └── VisualStudio2022/
└── JuceLibraryCode/                  # JUCE modules (auto-generated)
```

#### 2. CMakeLists.txt Template
```cmake
cmake_minimum_required(VERSION 3.22)
project(PerformiaEngine VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# JUCE setup
add_subdirectory(JUCE)

juce_add_console_app(PerformiaEngine
    PRODUCT_NAME "Performia Audio Engine"
    COMPANY_NAME "Performia"
)

target_sources(PerformiaEngine PRIVATE
    Source/Main.cpp
    Source/PerformiaAudioEngine.cpp
    Source/AudioAnalyzer.cpp
    Source/OSCCommunicator.cpp
)

target_compile_definitions(PerformiaEngine PRIVATE
    JUCE_USE_CURL=0
    JUCE_WEB_BROWSER=0
    JUCE_VST3_CAN_REPLACE_VST2=0
)

target_link_libraries(PerformiaEngine PRIVATE
    juce::juce_audio_basics
    juce::juce_audio_devices
    juce::juce_audio_formats
    juce::juce_audio_processors
    juce::juce_core
    juce::juce_dsp
    juce::juce_events
    juce::juce_osc
)
```

#### 3. Initial PerformiaAudioEngine.h
```cpp
#pragma once
#include <JuceHeader.h>

class PerformiaAudioEngine : public juce::AudioIODeviceCallback
{
public:
    PerformiaAudioEngine();
    ~PerformiaAudioEngine() override;

    // Start/stop the engine
    bool start();
    void stop();

    // AudioIODeviceCallback interface
    void audioDeviceIOCallback(
        const float** inputChannelData,
        int numInputChannels,
        float** outputChannelData,
        int numOutputChannels,
        int numSamples
    ) override;

    void audioDeviceAboutToStart(juce::AudioIODevice* device) override;
    void audioDeviceStopped() override;

private:
    juce::AudioDeviceManager deviceManager;

    // Audio settings
    int sampleRate{44100};
    int bufferSize{64};  // 1.45ms at 44.1kHz

    // Statistics
    std::atomic<uint64_t> callbackCount{0};
    std::atomic<uint64_t> dropoutCount{0};

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(PerformiaAudioEngine)
};
```

#### 4. Build and Test
```bash
# macOS
cd backend/juce
cmake -B build -G Xcode
cmake --build build --config Release

# Linux
cmake -B build -G "Unix Makefiles"
cmake --build build --config Release

# Test
./build/Release/PerformiaEngine
```

**Success Criteria**:
- ✅ Audio devices enumerated
- ✅ Audio callback receiving input
- ✅ No crashes or buffer overruns
- ✅ Builds on macOS, Linux, Windows

---

## Phase 2: Real-Time Audio Analysis (Days 3-7)

### Goals
- ✅ Pitch detection with YIN algorithm (<5ms)
- ✅ Onset detection with spectral flux (<2ms)
- ✅ Beat tracking (<3ms)
- ✅ Total analysis time: <10ms per callback

### Component 1: Pitch Detection (YIN Algorithm)

**Why YIN?**
- Industry standard for monophonic pitch detection
- Better than autocorrelation for music
- ~3-5ms on modern CPUs
- Used in Antares Auto-Tune, Melodyne

**Implementation: AudioAnalyzer.h**
```cpp
class AudioAnalyzer
{
public:
    struct AnalysisResult
    {
        float pitch{0.0f};           // Hz (0 if no pitch)
        float pitchConfidence{0.0f}; // 0-1
        bool onsetDetected{false};
        float tempo{120.0f};         // BPM
        int64_t timestamp{0};        // Sample count
    };

    AudioAnalyzer(int sampleRate);

    // Real-time analysis (must complete in <10ms)
    AnalysisResult analyze(
        const float* audioData,
        int numSamples
    );

private:
    // YIN pitch detection
    float detectPitchYIN(const float* audioData, int numSamples);

    // Spectral flux onset detection
    bool detectOnset(const float* audioData, int numSamples);

    // Autocorrelation beat tracking
    float detectTempo(const float* audioData, int numSamples);

    int sampleRate_;

    // Buffers for analysis
    std::vector<float> yinBuffer_;
    std::vector<float> fftBuffer_;
    std::vector<float> previousSpectrum_;

    // FFT for spectral analysis
    std::unique_ptr<juce::dsp::FFT> fft_;

    // Onset detection state
    float onsetThreshold_{0.3f};
    float previousFlux_{0.0f};

    // Tempo tracking state
    std::vector<float> beatHistory_;
    float currentTempo_{120.0f};
};
```

**YIN Algorithm Pseudocode**:
```cpp
float AudioAnalyzer::detectPitchYIN(const float* audio, int N)
{
    // 1. Difference function
    for (int tau = 0; tau < N/2; tau++) {
        float sum = 0.0f;
        for (int i = 0; i < N/2; i++) {
            float delta = audio[i] - audio[i + tau];
            sum += delta * delta;
        }
        yinBuffer_[tau] = sum;
    }

    // 2. Cumulative mean normalized difference
    yinBuffer_[0] = 1.0f;
    float runningSum = 0.0f;
    for (int tau = 1; tau < N/2; tau++) {
        runningSum += yinBuffer_[tau];
        yinBuffer_[tau] *= tau / runningSum;
    }

    // 3. Absolute threshold
    const float threshold = 0.1f;
    int tau = 2; // Start at minimum period (avoid DC)
    while (tau < N/2) {
        if (yinBuffer_[tau] < threshold) {
            // 4. Parabolic interpolation for sub-sample accuracy
            float betterTau = parabolicInterpolation(yinBuffer_, tau);
            return sampleRate_ / betterTau; // Convert to Hz
        }
        tau++;
    }

    return 0.0f; // No pitch detected
}
```

**Performance Target**: 3-5ms for 2048 samples

### Component 2: Onset Detection (Spectral Flux)

```cpp
bool AudioAnalyzer::detectOnset(const float* audio, int N)
{
    // 1. Compute FFT
    fft_->performRealOnlyForwardTransform(fftBuffer_.data());

    // 2. Compute magnitude spectrum
    std::vector<float> spectrum(N/2);
    for (int i = 0; i < N/2; i++) {
        float re = fftBuffer_[i*2];
        float im = fftBuffer_[i*2 + 1];
        spectrum[i] = std::sqrt(re*re + im*im);
    }

    // 3. Spectral flux (sum of positive differences)
    float flux = 0.0f;
    for (int i = 0; i < N/2; i++) {
        float diff = spectrum[i] - previousSpectrum_[i];
        if (diff > 0) flux += diff;
    }

    // 4. Onset if flux exceeds threshold * average
    bool onset = flux > (onsetThreshold_ * previousFlux_ * 1.5f);

    // 5. Update state
    previousSpectrum_ = spectrum;
    previousFlux_ = flux * 0.9f + previousFlux_ * 0.1f; // Smooth

    return onset;
}
```

**Performance Target**: 1-2ms for 1024 samples

### Component 3: Beat Tracking

```cpp
float AudioAnalyzer::detectTempo(const float* audio, int N)
{
    // Simplified autocorrelation-based tempo detection
    // Run every 4096 samples (~93ms) to save CPU

    if (sampleCount_ % 4096 != 0) {
        return currentTempo_; // Return cached value
    }

    // 1. Onset envelope (sum of onsets over time)
    // 2. Autocorrelation of onset envelope
    // 3. Find peak between 60-180 BPM (0.33-3.0 sec period)
    // 4. Smooth with previous tempo estimates

    // ... implementation details ...

    return currentTempo_;
}
```

**Performance Target**: <20ms (but run infrequently)

### Integration with Audio Callback

```cpp
void PerformiaAudioEngine::audioDeviceIOCallback(
    const float** input, int numInputs,
    float** output, int numOutputs,
    int numSamples)
{
    // CRITICAL: This runs in real-time audio thread
    // NO locks, NO allocations, NO blocking calls

    juce::ScopedNoDenormals noDenormals;

    auto startTime = juce::Time::getHighResolutionTicks();

    // 1. Analyze input
    if (numInputs > 0) {
        auto result = analyzer_.analyze(input[0], numSamples);

        // 2. Push result to lock-free queue
        if (result.pitch > 0.0f || result.onsetDetected) {
            analysisQueue_.push(result);
        }
    }

    // 3. Pass through for monitoring (optional)
    for (int ch = 0; ch < numOutputs; ++ch) {
        if (ch < numInputs) {
            std::memcpy(output[ch], input[ch], numSamples * sizeof(float));
        }
    }

    auto endTime = juce::Time::getHighResolutionTicks();
    auto elapsedUs = juce::Time::highResolutionTicksToSeconds(endTime - startTime) * 1e6;

    // Track max latency
    maxLatencyUs_.store(std::max(maxLatencyUs_.load(), (int64_t)elapsedUs));

    // Detect dropouts (callback took too long)
    if (elapsedUs > (numSamples * 1e6 / sampleRate_)) {
        dropoutCount_++;
    }
}
```

**Success Criteria**:
- ✅ Pitch detection: ±10 cents accuracy
- ✅ Onset detection: <50ms latency
- ✅ Total callback time: <10ms (for 64-sample buffer)
- ✅ Zero dropouts under normal load

---

## Phase 3: OSC Communication (Days 8-10)

### Goals
- ✅ Lock-free queue from audio thread to OSC thread
- ✅ OSC sender to Python (<0.5ms overhead)
- ✅ OSC receiver from Python (for future commands)

### OSC Message Format

**JUCE → Python Messages:**
```
/performia/pitch           f,f    [pitch_hz, confidence]
/performia/onset           i      [timestamp_samples]
/performia/beat            f,f    [tempo_bpm, beat_number]
/performia/statistics      i,i,f  [callbacks, dropouts, max_latency_ms]
```

**Python → JUCE Messages (future):**
```
/performia/control/start
/performia/control/stop
/performia/control/reset
```

### Implementation: OSCCommunicator.h

```cpp
class OSCCommunicator
{
public:
    OSCCommunicator(const juce::String& pythonHost = "127.0.0.1",
                    int pythonPort = 57120);
    ~OSCCommunicator();

    // Start OSC sender thread
    void start();
    void stop();

    // Send analysis results (called from non-real-time thread)
    void sendPitchEvent(float pitchHz, float confidence, int64_t timestamp);
    void sendOnsetEvent(int64_t timestamp);
    void sendBeatEvent(float tempo, float beatNumber);
    void sendStatistics(uint64_t callbacks, uint64_t dropouts, double maxLatencyMs);

private:
    juce::OSCSender oscSender_;
    juce::String pythonHost_;
    int pythonPort_;

    // Thread for processing analysis queue
    class SenderThread : public juce::Thread
    {
    public:
        SenderThread(OSCCommunicator* owner);
        void run() override;
    private:
        OSCCommunicator* owner_;
    };

    std::unique_ptr<SenderThread> senderThread_;

    // Lock-free queue from audio thread
    juce::AbstractFifo analysisFifo_{1024};
    std::vector<AudioAnalyzer::AnalysisResult> analysisBuffer_;
};
```

### Lock-Free Queue Pattern

```cpp
// Audio thread (real-time) - PRODUCER
void PerformiaAudioEngine::audioDeviceIOCallback(...)
{
    auto result = analyzer_.analyze(input[0], numSamples);

    // Try to push to queue (non-blocking)
    int start1, size1, start2, size2;
    analysisFifo_.prepareToWrite(1, start1, size1, start2, size2);

    if (size1 > 0) {
        analysisBuffer_[start1] = result;
        analysisFifo_.finishedWrite(1);
    } else {
        // Queue full - drop (should never happen with 1024 slots)
        queueOverflowCount_++;
    }
}

// OSC thread (non-real-time) - CONSUMER
void OSCCommunicator::SenderThread::run()
{
    while (!threadShouldExit()) {
        int start1, size1, start2, size2;
        owner_->analysisFifo_.prepareToRead(1, start1, size1, start2, size2);

        if (size1 > 0) {
            auto& result = owner_->analysisBuffer_[start1];

            // Send OSC messages
            if (result.pitch > 0.0f) {
                owner_->sendPitchEvent(result.pitch, result.pitchConfidence, result.timestamp);
            }
            if (result.onsetDetected) {
                owner_->sendOnsetEvent(result.timestamp);
            }

            owner_->analysisFifo_.finishedRead(1);
        } else {
            // No data - sleep briefly
            juce::Thread::sleep(1); // 1ms
        }
    }
}
```

**Success Criteria**:
- ✅ OSC messages arrive at Python <1ms after analysis
- ✅ Zero message loss under normal load
- ✅ Lock-free queue prevents audio thread blocking

---

## Phase 4: Python Integration (Days 11-14)

### Goals
- ✅ Python receives OSC messages from JUCE
- ✅ Existing agents use new event stream
- ✅ End-to-end latency measured

### Python OSC Receiver

```python
# backend/src/realtime/juce_bridge.py
from pythonosc import dispatcher, osc_server
import asyncio
from typing import Callable

class JUCEBridge:
    """Receives analysis events from JUCE audio engine."""

    def __init__(self, listen_port=57120):
        self.dispatcher = dispatcher.Dispatcher()
        self.server = None
        self.callbacks = {}

    def on_pitch(self, callback: Callable):
        """Register callback for pitch events."""
        self.callbacks['pitch'] = callback
        self.dispatcher.map("/performia/pitch", self._handle_pitch)

    def on_onset(self, callback: Callable):
        """Register callback for onset events."""
        self.callbacks['onset'] = callback
        self.dispatcher.map("/performia/onset", self._handle_onset)

    def on_beat(self, callback: Callable):
        """Register callback for beat events."""
        self.callbacks['beat'] = callback
        self.dispatcher.map("/performia/beat", self._handle_beat)

    def _handle_pitch(self, address, *args):
        pitch_hz, confidence = args
        if 'pitch' in self.callbacks:
            self.callbacks['pitch'](pitch_hz, confidence)

    def _handle_onset(self, address, *args):
        timestamp = args[0]
        if 'onset' in self.callbacks:
            self.callbacks['onset'](timestamp)

    def _handle_beat(self, address, *args):
        tempo, beat_num = args
        if 'beat' in self.callbacks:
            self.callbacks['beat'](tempo, beat_num)

    async def start(self, port=57120):
        """Start OSC server."""
        self.server = osc_server.AsyncIOOSCUDPServer(
            ('127.0.0.1', port),
            self.dispatcher,
            asyncio.get_event_loop()
        )
        transport, protocol = await self.server.create_serve_endpoint()
        print(f"✅ JUCE Bridge listening on port {port}")
```

### Integration with Existing Agents

```python
# backend/src/realtime/live_performance.py
import asyncio
from realtime.juce_bridge import JUCEBridge
from realtime.message_bus import AgentMessageBus, AgentMessage, MessagePriority
from agents.bass_agent import BassAgent
from agents.drum_agent import DrumAgent
from agents.conductor import ConductorAgent

async def main():
    # Initialize components
    juce = JUCEBridge()
    bus = AgentMessageBus()

    # Create agents
    conductor = ConductorAgent(bus)
    bass = BassAgent(bus)
    drums = DrumAgent(bus)

    # Connect JUCE events to message bus
    juce.on_pitch(lambda hz, conf: asyncio.create_task(
        bus.publish(AgentMessage(
            from_agent="juce",
            to_agent="broadcast",
            message_type="pitch_detected",
            payload={"pitch_hz": hz, "confidence": conf},
            priority=MessagePriority.HIGH
        ))
    ))

    juce.on_beat(lambda tempo, beat: asyncio.create_task(
        bus.publish(AgentMessage(
            from_agent="juce",
            to_agent="broadcast",
            message_type="beat_event",
            payload={"tempo": tempo, "beat": beat},
            priority=MessagePriority.CRITICAL
        ))
    ))

    # Start everything
    await juce.start()
    await bus.start()
    await conductor.start()
    await bass.start()
    await drums.start()

    print("🎼 Performia Live Performance System Running")
    print("Sing or play into microphone...")

    # Run forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
```

**Success Criteria**:
- ✅ Python receives all events from JUCE
- ✅ Agents respond to events correctly
- ✅ End-to-end latency: JUCE input → Python agent → OSC output <25ms

---

## Phase 5: SuperCollider Integration (Days 15-17)

### Goals
- ✅ Python sends note events to SuperCollider
- ✅ SC SynthDefs playing notes
- ✅ Full pipeline: Mic → JUCE → Python → SC → Speakers

### Python → SuperCollider Bridge

```python
# backend/src/realtime/sc_bridge.py
from pythonosc import udp_client

class SuperColliderBridge:
    """Sends musical events to SuperCollider synthesis engine."""

    def __init__(self, sc_host='127.0.0.1', sc_port=57110):
        self.client = udp_client.SimpleUDPClient(sc_host, sc_port)

    def play_note(self, synth_name: str, midi_note: int, velocity: float, duration: float):
        """Play a single note."""
        self.client.send_message(f"/synth/{synth_name}/note", [midi_note, velocity, duration])

    def play_chord(self, synth_name: str, midi_notes: list, velocity: float, duration: float):
        """Play multiple notes simultaneously."""
        self.client.send_message(f"/synth/{synth_name}/chord", midi_notes + [velocity, duration])

    def set_parameter(self, synth_name: str, param_name: str, value: float):
        """Set synth parameter."""
        self.client.send_message(f"/synth/{synth_name}/{param_name}", [value])
```

### SuperCollider OSC Responders

```supercollider
// backend/sc/osc_responders.scd
(
// Bass note
OSCdef(\bassNote, {
    arg msg;
    var midi, velocity, duration;
    #midi, velocity, duration = msg[1..3];

    Synth(\performiaBass, [
        \freq, midi.midicps,
        \amp, velocity,
        \gate, 1
    ]);
}, '/synth/bass/note');

// Drum hit
OSCdef(\drumHit, {
    arg msg;
    var drumType, velocity;
    #drumType, velocity = msg[1..2];

    switch(drumType,
        \kick, { Synth(\kick, [\amp, velocity]) },
        \snare, { Synth(\snare, [\amp, velocity]) },
        \hihat, { Synth(\hihat, [\amp, velocity]) }
    );
}, '/synth/drums/hit');

// Chord voicing
OSCdef(\harmonyChord, {
    arg msg;
    var notes = msg[1..msg.size-3];
    var velocity = msg[msg.size-2];
    var duration = msg[msg.size-1];

    notes.do { |midi|
        Synth(\performiaVoice, [
            \freq, midi.midicps,
            \amp, velocity,
            \gate, 1
        ]);
    };
}, '/synth/harmony/chord');

"✅ SuperCollider OSC responders ready".postln;
)
```

**Success Criteria**:
- ✅ Agents can trigger SC synths
- ✅ Audio output audible and musical
- ✅ SC synthesis latency <5ms

---

## Phase 6: Performance Optimization (Days 18-21)

### Goals
- ✅ Achieve <10ms total latency
- ✅ Zero dropouts under continuous use
- ✅ CPU usage <30%

### Optimization Strategies

#### 1. **Reduce JUCE Buffer Size**
```cpp
// Try progressively smaller buffers
bufferSize = 32;  // 0.73ms @ 44.1kHz (aggressive)
bufferSize = 64;  // 1.45ms @ 44.1kHz (recommended)
bufferSize = 128; // 2.90ms @ 44.1kHz (safe)
```

#### 2. **SIMD Optimization for YIN**
```cpp
// Use juce::FloatVectorOperations for SIMD
void computeDifference(const float* audio, float* diff, int N) {
    // Auto-vectorized by compiler
    juce::FloatVectorOperations::subtract(diff, audio, audio + tau, N);
    juce::FloatVectorOperations::multiply(diff, diff, N); // Square
}
```

#### 3. **Agent Decision Parallelization**
```python
# Run agents in parallel
async def process_beat(beat_num):
    results = await asyncio.gather(
        bass_agent.decide(context),
        drum_agent.decide(context),
        harmony_agent.decide(context)
    )
    # All agents decided in parallel
```

#### 4. **Adaptive Complexity**
```cpp
// Skip beat tracking if tempo is stable
if (abs(currentTempo - previousTempo) < 2.0) {
    // Don't recompute, save 2-3ms
    return currentTempo;
}
```

**Success Criteria**:
- ✅ Total latency: Input → SC output <10ms
- ✅ Consistent performance over 1 hour continuous use
- ✅ CPU <30% on modern hardware

---

## Testing Strategy

### Unit Tests (C++)
```cpp
// backend/juce/Tests/AudioAnalyzerTest.cpp
TEST_CASE("YIN pitch detection accuracy") {
    AudioAnalyzer analyzer(44100);

    // Generate 440Hz sine wave
    auto audio = generateSineWave(440.0f, 2048, 44100);

    auto result = analyzer.analyze(audio.data(), 2048);

    REQUIRE(result.pitch > 430.0f);
    REQUIRE(result.pitch < 450.0f); // Within ±10 cents
}

TEST_CASE("Onset detection on transient") {
    // ... test with click ...
}

TEST_CASE("Callback performance <10ms") {
    // ... measure callback time ...
}
```

### Integration Tests (Python)
```python
# backend/tests/integration/test_full_pipeline.py
@pytest.mark.asyncio
async def test_microphone_to_supercollider():
    """Test full pipeline latency."""

    # Start JUCE engine
    juce_process = subprocess.Popen(['./PerformiaEngine'])

    # Start Python agents
    # ... setup ...

    # Play test tone into microphone
    # Measure time until SC plays note

    assert latency_ms < 25  # Initial target
```

### Performance Benchmarks
```cpp
// Measure actual latency with loopback test
// 1. Output test signal
// 2. Measure time to detection
// 3. Report total round-trip
```

---

## Risk Mitigation

### Risk 1: JUCE Learning Curve
- **Mitigation**: Start with simple audio I/O, add complexity incrementally
- **Fallback**: Use JUCE examples and community support

### Risk 2: Platform-Specific Issues
- **Mitigation**: Test on macOS first (best CoreAudio support), then Linux/Windows
- **Fallback**: Document platform quirks, provide platform-specific guides

### Risk 3: <10ms Latency Unachievable
- **Mitigation**: Optimize aggressively, profile continuously
- **Fallback**: <15ms is still excellent for live performance

### Risk 4: OSC Overhead
- **Mitigation**: Measure OSC latency separately, optimize message size
- **Fallback**: Use shared memory if OSC too slow (unlikely)

---

## Success Metrics

### Performance
- ✅ Audio input latency: <2ms
- ✅ Analysis latency: <8ms
- ✅ Total JUCE latency: <10ms
- ✅ End-to-end (JUCE→Python→SC): <25ms (stretch goal: <15ms)
- ✅ CPU usage: <30%
- ✅ Zero dropouts: 99.9% uptime

### Quality
- ✅ Pitch accuracy: ±10 cents
- ✅ Onset detection: <50ms latency
- ✅ Tempo tracking: ±2 BPM

### Integration
- ✅ Python agents work unchanged
- ✅ Message bus integration seamless
- ✅ SuperCollider synthesis working

---

## Deliverables Checklist

- [ ] JUCE project compiling on macOS/Linux/Windows
- [ ] Audio I/O callback working (<2ms)
- [ ] YIN pitch detection implemented (<5ms)
- [ ] Onset detection implemented (<2ms)
- [ ] Beat tracking implemented (<3ms)
- [ ] OSC sender to Python working
- [ ] Python OSC receiver working
- [ ] Integration with existing agents
- [ ] SuperCollider synthesis working
- [ ] End-to-end tests passing
- [ ] Performance benchmarks met
- [ ] Documentation complete

---

## Timeline Summary

| Week | Focus | Deliverable |
|------|-------|-------------|
| **Week 1** | JUCE Setup & Audio I/O | Audio callback working, OSC sending |
| **Week 2** | Real-Time Analysis | Pitch/onset/beat detection <10ms |
| **Week 3** | Integration & Optimization | Full pipeline, performance tuned |

**Target Completion**: End of Week 3 (21 days)

---

## Post-Implementation Plan

Once JUCE engine is working:

1. **Deprecate Python audio code** (keep as reference)
2. **Update PERFORMIA_MASTER_PLAN.md** with actual latencies
3. **Create user guide** for JUCE engine
4. **Document build process** for all platforms
5. **Create installer** (bundle JUCE + Python + SC)

---

## Open Questions for Committee Review

1. **Buffer size trade-off**: 32 vs 64 vs 128 samples?
2. **Pitch detection**: YIN vs pYIN vs SWIPE++?
3. **OSC vs Shared Memory**: Which for Python communication?
4. **Agent parallelization**: How much can we parallelize decisions?
5. **Fallback strategy**: What if we can't hit <10ms?
6. **Testing infrastructure**: What CI/CD for C++ + Python?
7. **Cross-platform priority**: Mac first, or all platforms simultaneously?

---

**Status**: Ready for Committee Review
**Next Step**: Convene expert committee to challenge assumptions and refine plan
