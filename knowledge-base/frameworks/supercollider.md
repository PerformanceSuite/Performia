# SuperCollider Knowledge Base

**Purpose:** Real-time audio synthesis and algorithmic composition for Performia's AI accompaniment

**Last Updated:** October 4, 2025

---

## 🎹 What is SuperCollider?

SuperCollider is a platform for **audio synthesis** and **algorithmic composition**, used by musicians, artists, and researchers working with sound.

**Official Site:** https://supercollider.github.io/
**GitHub:** https://github.com/supercollider/supercollider

---

## 🏗️ Architecture

SuperCollider consists of three main components:

### 1. **scsynth** (Audio Server)
- Real-time audio synthesis engine
- Runs as separate process
- Low-latency audio I/O
- Hundreds of built-in UGens (Unit Generators)

### 2. **sclang** (Interpreted Language)
- Object-oriented programming language
- Controls scsynth via OSC (Open Sound Control)
- Smalltalk-inspired syntax
- Real-time evaluation (live coding)

### 3. **scide** (IDE)
- Integrated development environment
- Code editor with syntax highlighting
- Help browser
- Built-in documentation

---

## 🎛️ UGens (Unit Generators)

**UGens** are the building blocks of sound synthesis in SuperCollider.

### Categories of UGens:

#### 1. **Oscillators**
- `SinOsc` - Sine wave
- `Saw` - Sawtooth wave
- `Pulse` - Pulse/square wave
- `LFNoise0/1/2` - Low-frequency noise (modulation)

#### 2. **Filters**
- `LPF` - Low-pass filter
- `HPF` - High-pass filter
- `BPF` - Band-pass filter
- `Resonz` - Resonant filter
- `RLPF/RHPF` - Resonant low/high-pass

#### 3. **Envelopes**
- `EnvGen` - Envelope generator
- `Line/XLine` - Linear/exponential ramps
- `Decay/Decay2` - Exponential decay

#### 4. **Effects**
- `FreeVerb` - Reverb
- `CombN/CombL/CombC` - Comb delay (echo)
- `AllpassN/L/C` - Allpass filter (chorus/flanger)
- `PitchShift` - Pitch shifting

#### 5. **Analysis**
- `Pitch` - Pitch detection
- `Amplitude` - Amplitude follower
- `FFT/IFFT` - Spectral analysis
- `Onsets` - Onset detection (beat tracking)

---

## 🎵 Synthesis Techniques

### 1. Additive Synthesis
```supercollider
// Multiple sine waves create complex timbre
(
{
    var fundamental = 220; // A3
    var harmonics = [1, 2, 3, 4, 5];  // Harmonic series
    var amps = [1.0, 0.5, 0.33, 0.25, 0.2];  // Decreasing amplitudes

    Mix.ar(
        harmonics.collect { |harm, i|
            SinOsc.ar(fundamental * harm) * amps[i]
        }
    ) * 0.1
}.play;
)
```

### 2. Subtractive Synthesis
```supercollider
// Rich waveform → filter → shaped sound
(
{
    var freq = 110;
    var saw = Saw.ar(freq);
    var filtered = RLPF.ar(saw, freq * 4, 0.3);  // Resonant low-pass
    var env = EnvGen.kr(Env.perc(0.01, 1.0), doneAction: 2);

    filtered * env * 0.3
}.play;
)
```

### 3. FM Synthesis (Frequency Modulation)
```supercollider
// Carrier frequency modulated by modulator
(
{
    var carFreq = 440;
    var modFreq = 200;
    var modIndex = 5;  // Depth of modulation

    var modulator = SinOsc.ar(modFreq) * modIndex * modFreq;
    var carrier = SinOsc.ar(carFreq + modulator);

    carrier * 0.3
}.play;
)
```

### 4. Granular Synthesis
```supercollider
// Small grains of sound create texture
(
{
    var buf = Buffer.read(s, Platform.resourceDir +/+ "sounds/a11wlk01.wav");
    TGrains.ar(
        numChannels: 2,
        trigger: Impulse.ar(10),  // 10 grains/sec
        dur: 0.1,                 // Grain duration
        sndbuf: buf,
        rate: 1.0,
        centerPos: LFNoise1.kr(1).range(0, BufDur.kr(buf))
    ) * 0.5
}.play;
)
```

### 5. Physical Modeling (Karplus-Strong)
```supercollider
// Plucked string synthesis
(
{
    var freq = 220;
    var trigger = Impulse.kr(2);  // Pluck every 0.5 sec

    Pluck.ar(
        in: WhiteNoise.ar(0.1),
        trig: trigger,
        maxdelaytime: 0.1,
        delaytime: freq.reciprocal,
        decaytime: 5,
        coef: 0.5
    )
}.play;
)
```

---

## 🎯 SuperCollider for Performia

### Use Cases:

#### 1. **AI Accompaniment Synthesis**
Generate backing tracks in real-time based on Song Map chords:

```supercollider
// Piano-like accompaniment
(
SynthDef(\pianoChord, {
    arg out=0, freq=440, amp=0.3, gate=1;
    var sig, env;

    // Multiple detuned oscillators for richness
    sig = Mix.ar(
        Array.fill(3, { |i|
            SinOsc.ar(freq * (1 + (i * 0.01))) * (1/3)
        })
    );

    // Piano-like envelope
    env = EnvGen.kr(Env.adsr(0.001, 0.3, 0.5, 2.0), gate, doneAction: 2);

    Out.ar(out, sig * env * amp ! 2);  // Stereo output
}).add;
)

// Play C major chord (C-E-G)
x = Synth(\pianoChord, [\freq, 261.63]);  // C4
y = Synth(\pianoChord, [\freq, 329.63]);  // E4
z = Synth(\pianoChord, [\freq, 392.00]);  // G4

// Release after 2 seconds
{ x.release; y.release; z.release }.defer(2);
```

#### 2. **Real-Time Chord Changes**
```supercollider
// Chord progression: C → Am → F → G
(
var chordProgression = [
    [261.63, 329.63, 392.00],  // C major
    [220.00, 261.63, 329.63],  // A minor
    [174.61, 220.00, 261.63],  // F major
    [196.00, 246.94, 293.66]   // G major
];

var routine = Routine {
    chordProgression.do { |chord|
        var synths = chord.collect { |freq|
            Synth(\pianoChord, [\freq, freq, \amp, 0.2]);
        };

        2.wait;  // Hold chord for 2 seconds

        synths.do { |s| s.release };
        0.1.wait;  // Short gap
    };
};

routine.play;
)
```

#### 3. **Beat-Synced Drums**
```supercollider
// Drum machine synced to BPM
(
var bpm = 120;
var beatDuration = 60 / bpm;

// Kick drum
SynthDef(\kick, {
    var sig = SinOsc.ar(XLine.kr(120, 40, 0.1));
    var env = EnvGen.kr(Env.perc(0.001, 0.3), doneAction: 2);
    Out.ar(0, sig * env * 0.8 ! 2);
}).add;

// Snare drum
SynthDef(\snare, {
    var sig = Mix.ar([
        WhiteNoise.ar(0.3),
        SinOsc.ar(180) * 0.2
    ]);
    var env = EnvGen.kr(Env.perc(0.001, 0.15), doneAction: 2);
    Out.ar(0, sig * env * 0.6 ! 2);
}).add;

// Hi-hat
SynthDef(\hihat, {
    var sig = HPF.ar(WhiteNoise.ar(1), 7000);
    var env = EnvGen.kr(Env.perc(0.001, 0.05), doneAction: 2);
    Out.ar(0, sig * env * 0.3 ! 2);
}).add;

// Pattern
Routine {
    inf.do { |beat|
        // Kick on beats 0, 2
        if (beat % 4 == 0 or: { beat % 4 == 2 }) {
            Synth(\kick);
        };

        // Snare on beats 1, 3
        if (beat % 4 == 1 or: { beat % 4 == 3 }) {
            Synth(\snare);
        };

        // Hi-hat every beat
        Synth(\hihat);

        beatDuration.wait;
    }
}.play;
)
```

---

## 🔌 OSC (Open Sound Control) Integration

SuperCollider communicates via **OSC** - perfect for integrating with Performia!

### Python → SuperCollider (OSC)

**Python side (Performia backend):**
```python
from pythonosc import udp_client

# Connect to SuperCollider
sc_client = udp_client.SimpleUDPClient("127.0.0.1", 57120)

# Send chord change message
def play_chord(chord_name, frequencies):
    sc_client.send_message("/chord/play", [chord_name] + frequencies)

# Example: Play C major
play_chord("C", [261.63, 329.63, 392.00])
```

**SuperCollider side:**
```supercollider
(
OSCdef(\chordReceiver, { |msg, time, addr, recvPort|
    var chordName = msg[1];
    var freqs = msg[2..];  // Remaining arguments

    ("Playing chord: " ++ chordName).postln;

    // Create synths for each note
    freqs.do { |freq|
        Synth(\pianoChord, [\freq, freq]);
    };
}, '/chord/play');
)
```

---

## 📚 Learning Resources

### Official Documentation
- **SuperCollider Tutorial** by Nick Collins
  https://composerprogrammer.com/teaching/supercollider/sctutorial/tutorial.html
  - Sound synthesis (additive, subtractive, modulation, granular)
  - Sequencing and algorithmic composition
  - Open Sound Control

### Free Ebook
- **"A Gentle Introduction to SuperCollider"** by Bruno Ruviaro
  https://ccrma.stanford.edu/~ruviaro/texts/A_Gentle_Introduction_To_SuperCollider.pdf
  - Comprehensive tutorial from basics to advanced
  - Recommended by Stanford CCRMA

### Community Resources
- **Official Docs:** https://doc.sccode.org
- **Forum:** https://scsynth.org
- **Code Examples:** https://sccode.org (user-contributed)
- **Slack Channel:** Active community support

---

## 🎯 Integration Plan for Performia

### Phase 1: Prototype (Standalone SC)
1. Install SuperCollider
2. Create basic chord synth (`SynthDef`)
3. Test OSC communication from Python
4. Build simple chord progression player

### Phase 2: Backend Integration
1. Add `python-osc` to Performia backend
2. Create `SuperColliderService` class
3. Map Song Map chords → SC frequency arrays
4. Send chord changes via OSC

### Phase 3: Real-Time Accompaniment
1. Sync to Song Map timing
2. Dynamic tempo following (adjust BPM)
3. Multiple instrument tracks (piano, bass, drums)
4. Mix with original audio stems

### Phase 4: AI-Enhanced Synthesis
1. ML-generated synthesis parameters
2. Style-aware accompaniment (jazz, rock, etc.)
3. Performer-responsive dynamics
4. Live effect modulation

---

## 🔧 Installation & Setup

### macOS
```bash
brew install supercollider
```

### Ubuntu/Debian
```bash
sudo apt-get install supercollider
```

### Windows
Download from https://supercollider.github.io/downloads.html

### Running the Server
```supercollider
// Start audio server
s.boot;

// Test audio
{ SinOsc.ar(440) * 0.2 ! 2 }.play;

// Stop audio
s.quit;
```

---

## ⚡ Performance Considerations

### Low-Latency Configuration
```supercollider
(
// Set server options for low latency
s.options.blockSize = 128;        // Small buffer
s.options.numBuffers = 2048;      // More buffers
s.options.memSize = 8192 * 32;    // More memory
s.options.sampleRate = 48000;     // Pro audio standard

s.boot;
)
```

### Real-Time Safety
- Pre-allocate `SynthDef`s before performance
- Use `Routine` for timing (not `SystemClock`)
- Avoid creating synths in tight loops
- Use `Server.sync` for sequential operations

---

## 🎼 Example: Complete Backing Track Generator

```supercollider
(
// 1. Define instruments
SynthDef(\bass, {
    arg out=0, freq=110, amp=0.5, gate=1;
    var sig, env, filter;

    sig = Saw.ar(freq) + Pulse.ar(freq * 0.5, 0.3);
    filter = RLPF.ar(sig, freq * 2, 0.5);
    env = EnvGen.kr(Env.adsr(0.01, 0.3, 0.7, 0.5), gate, doneAction: 2);

    Out.ar(out, filter * env * amp ! 2);
}).add;

SynthDef(\pad, {
    arg out=0, freq=440, amp=0.2, gate=1;
    var sig, env;

    sig = Mix.ar(
        Array.fill(5, { |i|
            SinOsc.ar(freq * (i + 1) * LFNoise1.kr(0.1).range(0.98, 1.02))
        })
    ) * 0.2;

    sig = FreeVerb.ar(sig, 0.7, 0.9);  // Add reverb
    env = EnvGen.kr(Env.asr(0.5, 1, 1), gate, doneAction: 2);

    Out.ar(out, sig * env * amp ! 2);
}).add;

// 2. Chord progression (I-vi-IV-V in C)
var chords = [
    [\C, [261.63, 329.63, 392.00]],
    [\Am, [220.00, 261.63, 329.63]],
    [\F, [174.61, 220.00, 261.63]],
    [\G, [196.00, 246.94, 293.66]]
];

// 3. Sequencer
Routine {
    chords.do { |chord|
        var chordName = chord[0];
        var freqs = chord[1];

        // Bass plays root
        Synth(\bass, [\freq, freqs[0], \amp, 0.4]);

        // Pad plays full chord
        freqs.do { |freq|
            Synth(\pad, [\freq, freq, \amp, 0.15]);
        };

        2.wait;  // 2 second chord duration
    };
}.play;
)
```

---

## 🚀 Next Steps

1. **Install SuperCollider** and complete basic tutorials
2. **Test OSC communication** with Python backend
3. **Create Performia SynthDef library** (piano, bass, drums, pads)
4. **Build OSC handler** for real-time chord changes
5. **Integrate with Song Map** timing engine
6. **Profile latency** (target < 10ms from OSC → audio output)

---

**Key Advantages for Performia:**
- ✅ **Real-time synthesis** - Generate accompaniment on the fly
- ✅ **Low latency** - < 10ms achievable
- ✅ **Flexible** - Unlimited synthesis techniques
- ✅ **Cross-platform** - macOS, Windows, Linux
- ✅ **OSC integration** - Easy Python communication
- ✅ **Live coding** - Modify synthesis during performance
- ✅ **Open source** - No licensing fees

**Comparison to JUCE:**
- **SuperCollider:** Higher-level, faster prototyping, live coding
- **JUCE:** Lower-level, more control, better for plugins
- **Best approach:** Use both! SC for synthesis, JUCE for audio I/O and DSP
