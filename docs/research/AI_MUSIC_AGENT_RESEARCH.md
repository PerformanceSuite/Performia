# AI Music Agent System Research for Performia
## Comprehensive Analysis and Recommendations

**Date:** October 1, 2025
**Author:** Research Agent
**Version:** 1.0

---

## Executive Summary

This research analyzes state-of-the-art AI music performance systems to guide Performia's development of virtual musician agents capable of listening, learning, and performing adaptively in real-time. Based on comprehensive analysis of current systems, academic research, and technical constraints, this document provides clear architectural recommendations.

### Key Recommendations

1. **Start with Drums:** Begin with a drum agent as the MVP, leveraging mature pattern generation models and simpler musical complexity
2. **Hybrid Architecture:** Combine rule-based systems with small ML models (<500MB) for optimal latency and adaptability
3. **Symbolic MIDI Generation:** Use MIDI-based generation with VST/AU synthesis for low latency and high editability
4. **SQLite Storage:** Leverage embedded database for song knowledge, performance history, and agent configuration
5. **OSC Communication:** Use Open Sound Control for flexible, low-latency communication between Python agents and JUCE audio engine
6. **Pre-trained + Fine-tuning:** Adapt existing models (Magenta GrooVAE, Music Transformer) rather than training from scratch
7. **Target Latency:** Achieve <20ms total system latency for professional-quality real-time performance

---

## 1. Survey of Existing Systems

### 1.1 Google Magenta

**Overview:**
Google's Magenta project is the leading open-source platform for AI music generation, with multiple models suited for different musical tasks.

**Key Technologies:**

- **Performance RNN:** Generates expressive MIDI with timing and dynamics
  - Architecture: LSTM-based recurrent neural network
  - Time resolution: 10ms steps
  - Output: Symbolic MIDI with velocity and timing variations
  - Browser capability: Runs in browser via deeplearn.js (GPU-accelerated)

- **Magenta RealTime (2025):** Breakthrough real-time music generation model
  - Architecture: 800M parameter Transformer with block autoregression
  - Audio codec: 48kHz stereo via neural codec (EnCodec)
  - Latency: 1.25 seconds to generate 2 seconds of audio (RTF 1.6x on TPU v2-8)
  - License: Apache 2.0 (open weights)
  - Output: Raw audio (not MIDI)

- **Music Transformer:** Long-term structure in MIDI generation
  - Architecture: Transformer with Relative Self-Attention
  - Strengths: 4+ minute compositions with coherent structure
  - Training data: Classical MIDI archives
  - Generation speed: Fast (symbolic domain)

- **GrooVAE:** Drum pattern generation with expressiveness control
  - Architecture: Variational Autoencoder
  - Training: 15 hours of professional MIDI drummers
  - Controls: Rhythm complexity, humanization, timing variation
  - Output: MIDI drum patterns
  - Integration: Available as Magenta Studio VST/AU plugin

**Latency Analysis:**
- Symbolic models (Performance RNN, Music Transformer): <100ms inference (real-time capable)
- Neural audio (Magenta RealTime): 625ms+ latency (not real-time for live performance)

**Performia Relevance:** ⭐⭐⭐⭐⭐
- GrooVAE is ideal for MVP drum agent
- Performance RNN suitable for melodic instruments
- Open-source models enable local deployment and fine-tuning

### 1.2 OpenAI Jukebox & MuseNet

**Jukebox:**
- Architecture: Hierarchical VQ-VAE + autoregressive transformers
- Output: Raw audio with vocals
- Quality: High fidelity, realistic singing
- Latency: **9 hours to generate 1 minute** of audio
- Status: Research prototype, not real-time capable

**MuseNet:**
- Architecture: GPT-2-style transformer (72-layer, 800M+ parameters)
- Output: Symbolic MIDI
- Instruments: Piano, drums, bass, guitar, strings
- Training: Classical Archives, BitMidi, jazz, pop, world music
- Generation: Advanced mode requires extended processing time
- Status: Discontinued December 2022

**Latency Analysis:**
- Jukebox: **NOT real-time** (hours per minute)
- MuseNet: Minutes for multi-minute compositions (not interactive)

**Performia Relevance:** ⭐⭐
- Too slow for real-time performance
- Useful for understanding multi-instrument modeling
- Training data sources informative

### 1.3 Meta MusicGen

**Overview:**
Single-stage autoregressive Transformer for text-to-music generation.

**Architecture:**
- Model: Transformer language model (1.5B-3.5B parameters)
- Audio codec: EnCodec (32kHz, 4 codebooks @ 50Hz)
- Innovation: Delay pattern for parallel codebook prediction
- Efficiency: 50 autoregressive steps per second of audio

**Performance:**
- Generation time: 60+ seconds for typical outputs
- Latency optimization: Block processing reduces steps vs. traditional
- Deployment: Cloud-based (AWS SageMaker async inference recommended)

**Synthesis:**
- Raw neural audio (not MIDI)
- Stereo output at 32kHz

**Performia Relevance:** ⭐⭐
- Too computationally expensive for real-time
- Delay pattern technique useful for optimization
- Better suited for composition than live performance

### 1.4 Academic Real-Time Accompaniment Systems

**RL-Duet (2020):**
- Approach: Deep reinforcement learning for online accompaniment
- Architecture: Policy network learns to generate notes (actions) from context (state)
- Reward: Compatibility with both human and machine-generated context
- Capability: Real-time interactive duet improvisation
- Limitation: Specific to monophonic/polyphonic melody accompaniment

**ReaLJam (2025):**
- Description: First system achieving live jamming with large Transformers
- Architecture: Transformer + reinforcement learning fine-tuning
- Features: Anticipatory generation (predicts and displays plan to user)
- Interface: Web-based with visual feedback
- Latency: Low enough for interactive jamming
- Innovation: RL enables tight synchronization with human performer

**ReaLchords:**
- Task: Real-time chord accompaniment generation
- Method: Transformer fine-tuned with RL
- Training: Two-stage (supervised pre-training → RL adaptation)
- Capability: Responds adaptively to melody in real-time

**SongDriver:**
- Goal: Real-time accompaniment without logical latency or exposure bias
- Innovation: Addresses trade-off between latency and model quality
- Status: Research prototype (2022)

**Orchestra in a Box:**
- Components: Listen (HMM audio analysis) → Anticipate → Synthesize
- Approach: Follow soloist using hidden Markov models
- Era: Pre-deep learning (1990s-2000s research)

**Yamaha AI Music Ensemble:**
- Capability: Compares live performance to sheet music in real-time
- Analysis: Position, speed, musical expression
- Application: Ensemble partner for practice

**Performia Relevance:** ⭐⭐⭐⭐⭐
- **RL-Duet and ReaLJam demonstrate feasibility** of real-time AI accompaniment
- **Two-stage training (supervised → RL)** is proven approach for adaptation
- ReaLJam's anticipatory UI aligns with Living Chart concept
- These systems prove <50ms latency is achievable with modern models

### 1.5 Commercial DAW Drummer Agents

**Logic Pro Drummer:**
- History: First generative drummer (2013), AI upgrade (May 2024)
- Training: Collaboration with professional drummers + advanced AI
- Capability: Analyzes song (tempo, instrumentation, vibe) to select styles/patterns
- Adaptation: Responds to chord progressions and musical context
- Architecture: Proprietary (not documented publicly)
- Format: Built-in (not available as standalone VST)
- Synthesis: High-quality sample-based drum kits
- Real-time: Yes, plays back immediately

**Logic Pro Bass Player (2024):**
- Training: Collaboration with professional bassists
- Technology: AI + advanced sampling
- Input: Chord progressions (project-level configuration)
- Output: Expressive, stylistically appropriate basslines
- Quality: "Much higher caliber" than earlier generative instruments

**Alternative Tools:**
- **Jamstix 4:** AI-powered auto-accompaniment drummer (cross-DAW compatible)
- **EZDrummer/Superior Drummer:** Sample playback (not true AI generation)

**Performia Relevance:** ⭐⭐⭐⭐
- Proves commercial viability of AI session musicians
- Sample-based synthesis provides high quality with low latency
- Chord progression as input works for bass, keys, potentially guitar
- User expectations set by Logic's quality bar

---

## 2. Technical Architecture Options

### 2.1 Audio Synthesis Methods

#### A. VST/AU Plugin Hosting (in JUCE) ⭐⭐⭐⭐⭐

**How it works:**
- JUCE application loads commercial/free VST3/AU plugins
- Agent generates MIDI events in real-time
- JUCE routes MIDI to plugin, streams audio output

**Advantages:**
- ✅ **Lowest latency:** Modern plugins achieve <5ms processing
- ✅ **Professional quality:** Access to world-class instruments (Kontakt, Abbey Road, etc.)
- ✅ **User customization:** Musicians can choose their preferred sounds
- ✅ **Proven technology:** JUCE plugin hosting is mature and stable
- ✅ **No training required:** Synthesis is handled by existing tools
- ✅ **Immediate compatibility:** Works with user's existing plugin library

**Challenges:**
- ⚠️ Plugin loading/scanning can be slow at startup
- ⚠️ Some plugins report variable latency (need compensation)
- ⚠️ Licensing (user must own plugins)
- ⚠️ 7x CPU overhead reported for JUCE VST3 hosting (optimization needed)

**Best for:** Drums, bass, keys, guitar - all instruments

**Performia Implementation:**
```
[Python Agent] → MIDI Events → [JUCE Host] → [VST Plugin] → Audio Out
                                     ↓
                              Latency: <10ms total
```

#### B. Neural Audio Synthesis (WaveNet, SampleRNN) ⭐

**How it works:**
- Deep neural network generates raw audio waveforms sample-by-sample
- Models trained on audio recordings of instruments

**Advantages:**
- ✅ Novel timbres and sounds not possible with samples
- ✅ No sample library storage requirements

**Challenges:**
- ❌ **Extremely high latency:** WaveNet/SampleRNN not real-time on commodity hardware
- ❌ **GPU required:** Several GFLOPS of computation
- ❌ **Training complexity:** Requires large audio datasets and weeks of training
- ❌ Model size: Hundreds of MB to GB

**Modern alternatives:**
- WaveRNN: 4x faster than real-time on GPU (still not <10ms)
- DDSP vocoder: 340x fewer FLOPS than MB-MelGAN (promising for future)
- DLL-APNet (2024): Low-latency neural vocoder (research stage)

**Best for:** Sound design, special effects (not real-time performance)

#### C. Sample-Based Playback ⭐⭐⭐⭐

**How it works:**
- Agent triggers pre-recorded audio samples (drum hits, bass notes, etc.)
- Velocity/timing modulate playback

**Advantages:**
- ✅ **Very low latency:** Direct sample playback <1ms
- ✅ **High realism:** Actual instrument recordings
- ✅ **Predictable CPU:** Straightforward mixing/playback

**Challenges:**
- ⚠️ Large sample libraries (GB of storage)
- ⚠️ Limited expressiveness compared to synthesis
- ⚠️ Must build or license sample sets

**Best for:** Drums (highest realism, simplest approach)

#### D. Physical Modeling Synthesis ⭐⭐⭐

**How it works:**
- Mathematical simulation of instrument physics (string vibration, air columns, etc.)
- Real-time parameter control (pluck position, bow pressure, etc.)

**Advantages:**
- ✅ Real-time capable (designed for low latency)
- ✅ Expressive control via continuous parameters
- ✅ Small storage footprint (code + parameters)

**Challenges:**
- ⚠️ CPU intensive for realistic models
- ⚠️ Uncanny valley - can sound artificial
- ⚠️ Complex to design convincing models

**Best for:** Bass, guitar (Piano Teq, Applied Acoustics Chromaphone)

#### E. MIDI → Software Instruments ⭐⭐⭐⭐⭐

**How it works:**
- Agent generates MIDI note events
- Standard software synth/sampler plays back
- Could be plugin, OS synth, or custom JUCE synthesizer

**Advantages:**
- ✅ **Standard workflow:** Musicians understand MIDI
- ✅ **Editable:** MIDI can be modified, exported, saved
- ✅ **Flexible:** Swap instruments without regenerating
- ✅ **Low data:** MIDI is tiny compared to audio
- ✅ **Low latency:** <5ms with modern synths

**Challenges:**
- ⚠️ Quality depends on synth/plugin choice
- ⚠️ Requires instrument plugin or built-in synth

**Best for:** All instruments (industry standard)

### 2.2 Agent Intelligence Architecture

#### A. Transformer-based Music Models (Fine-tuned) ⭐⭐⭐⭐⭐

**Approach:**
- Start with pre-trained model (Music Transformer, MuseNet, etc.)
- Fine-tune on specific songs/styles
- Generate MIDI in real-time via inference

**Architecture Example:**
```
Song stems → Feature extraction → Fine-tuning dataset
Pre-trained Transformer → Fine-tune → Song-specific agent model
Live audio input → Beat/chord detection → Conditioning → MIDI generation
```

**Latency:**
- Small models (<100M params): <10ms inference on GPU
- Medium models (100-500M params): 10-50ms on GPU
- Quantized models: Can run on CPU with <20ms latency

**Model sizes:**
- Music Transformer: ~200M parameters (~800MB FP32, ~200MB INT8)
- DistilHuBERT: ~100M parameters (music understanding)
- Custom small transformer: 10-50M parameters (<100MB)

**Advantages:**
- ✅ **Proven approach:** Music Transformer generates coherent long-form music
- ✅ **Pre-training available:** Leverage existing trained models
- ✅ **Adaptable:** Fine-tune per song or style
- ✅ **Rich generation:** Learns complex patterns and variations
- ✅ **Open source:** Magenta models available

**Challenges:**
- ⚠️ Inference latency with large models
- ⚠️ GPU recommended for real-time performance
- ⚠️ Fine-tuning requires computational resources

**Performia Application:**
- **MVP:** Use Magenta GrooVAE for drums (already trained, proven)
- **Enhanced:** Fine-tune Music Transformer on song stems
- **Production:** Quantize models for CPU inference

#### B. Specialized Small Models per Instrument (<100MB) ⭐⭐⭐⭐⭐

**Approach:**
- Train or fine-tune tiny models for each instrument
- Optimize for low latency and specific task

**Examples:**
- Drum model: 20M params (~40MB quantized)
- Bass model: 30M params (~60MB quantized)
- Keys model: 50M params (~100MB quantized)

**Advantages:**
- ✅ **Fast inference:** <5ms on modern CPU
- ✅ **Low memory:** Can load all agents simultaneously
- ✅ **Parallel processing:** Each agent runs independently
- ✅ **Edge deployment:** Runs on laptop/desktop without cloud

**Challenges:**
- ⚠️ May lack sophistication of large models
- ⚠️ Requires careful architecture design for quality
- ⚠️ Need to train/fine-tune each instrument separately

**Performia Application:**
- Distill large Music Transformer into instrument-specific small models
- Use quantization (INT8) and pruning for size reduction
- Run multiple agents simultaneously on user's machine

#### C. Rule-Based + ML Hybrid ⭐⭐⭐⭐⭐ **RECOMMENDED**

**Approach:**
- ML model learns patterns, feel, and variations from stems
- Rule-based system ensures musical correctness (stay in key, follow chord changes, etc.)
- Combine both for reliable, adaptive performance

**Architecture:**
```
Rules Layer (fast, deterministic):
- Chord progression following
- Key/scale constraints
- Rhythmic quantization
- Dynamic range limiting

ML Layer (adaptive, expressive):
- Pattern variation generation
- Humanization (timing, velocity)
- Style adaptation
- Contextual decision-making

Output: Musical + Expressive
```

**Examples from research:**
- HARMONET: RNN generates notes + rule checker prevents parallel fifths
- HMM + rules: HMM selects chords/note length, rules determine tempo/mode
- Logic Drummer: Likely uses ML for variation + rules for musical coherence

**Advantages:**
- ✅ **Best of both worlds:** ML creativity + rule reliability
- ✅ **Guaranteed correctness:** Won't play "wrong" notes
- ✅ **Lower latency:** Simple rules are fast, ML only for complex decisions
- ✅ **Easier debugging:** Rules are transparent and controllable
- ✅ **Graceful degradation:** Falls back to rules if ML fails

**Challenges:**
- ⚠️ More complex architecture to maintain
- ⚠️ Need to design rule system per instrument

**Performia Application (Recommended):**
1. **Rules ensure:**
   - Bass plays root/5th/3rd of current chord
   - Drums maintain consistent tempo
   - Keys voice chords correctly

2. **ML provides:**
   - Walking bass patterns vs. root notes
   - Drum fills and variations
   - Voicing inversions and substitutions

#### D. Reinforcement Learning for Adaptation ⭐⭐⭐⭐

**Approach:**
- Pre-train with supervised learning (learn song)
- Fine-tune with RL to follow human performer in real-time

**RL Framework:**
- **State:** Recent audio features (beat position, current chord, human dynamics)
- **Action:** Next MIDI note(s) to generate
- **Reward:** Synchronization quality + musical appropriateness

**Evidence:**
- ReaLJam: First real-time Transformer jamming with RL fine-tuning
- ReaLchords: RL enabled tight synchronization with melody
- RL-Duet: Policy learning for human-machine improvisation

**Advantages:**
- ✅ **Adaptive:** Learns to respond to human performer's variations
- ✅ **Proven:** Multiple research systems demonstrate success
- ✅ **Continuous improvement:** Can improve through practice/performance

**Challenges:**
- ⚠️ Complex training pipeline (supervised → RL)
- ⚠️ Requires reward function design
- ⚠️ Training time and computational cost

**Performia Application:**
- Phase 2 enhancement after MVP
- Use supervised learning to learn song initially
- Apply RL to improve real-time following of human performer

#### E. Symbolic Music Representation vs. Raw Audio ⭐⭐⭐⭐⭐

**Symbolic (MIDI) - RECOMMENDED:**

**Advantages:**
- ✅ **Efficient:** 1000x data compression vs. audio
- ✅ **Fast generation:** Music Transformer creates 4-minute MIDI in seconds
- ✅ **Interpretable:** Notes, timing, velocity are explicit
- ✅ **Editable:** Can modify, save, export MIDI
- ✅ **Low latency:** Small data to process
- ✅ **Better long-term structure:** Models learn musical form easily

**Disadvantages:**
- ❌ Can't capture timbral nuance (tone color, articulation)
- ❌ Requires separate synthesis step

**Raw Audio:**

**Advantages:**
- ✅ **Complete output:** Audio is ready to play
- ✅ **Timbral control:** Can generate novel sounds

**Disadvantages:**
- ❌ **High computational cost:** Requires massive models
- ❌ **Slow generation:** Jukebox takes hours, MusicGen takes minutes
- ❌ **Not real-time capable:** 10ms latency impossible with current tech
- ❌ **Not editable:** Can't modify generated audio easily

**Performia Recommendation:**
**Use symbolic MIDI generation** for all agents. This enables:
1. <10ms generation latency (Transformer inference)
2. Flexible synthesis (user chooses instruments)
3. Exportable, editable performance data
4. Alignment with Song Map symbolic representation

### 2.3 Real-Time Communication Protocols

#### A. OSC (Open Sound Control) ⭐⭐⭐⭐⭐ **RECOMMENDED**

**Technical Specs:**
- Transport: UDP/IP (10+ Mbps Ethernet)
- Data format: Human-readable path + typed arguments
- Latency: ~1ms on local network
- Resolution: 32-bit float/int (vs. MIDI's 7-bit)

**Advantages:**
- ✅ **Low latency:** Designed for real-time performance
- ✅ **High resolution:** No 0-127 limitation
- ✅ **Flexible addressing:** Symbolic paths (e.g., `/drums/snare/velocity`)
- ✅ **Bidirectional:** Easy two-way communication
- ✅ **Network ready:** Works over Ethernet/Wi-Fi
- ✅ **Open standard:** Wide support in audio software

**Challenges:**
- ⚠️ UDP = no guaranteed delivery (acceptable for real-time audio)
- ⚠️ Human-readable = slightly larger packets than binary
- ⚠️ Less mature than MIDI for some applications

**Performia Application:**
```python
# Python agent sends OSC messages to JUCE
osc_client.send_message("/bass/note_on", [pitch, velocity, timestamp])
osc_client.send_message("/drums/pattern", [pattern_id, variation])

# JUCE receives and triggers MIDI/audio
OSCReceiver receives → Maps to internal events → Triggers VST plugins
```

**Libraries:**
- Python: `python-osc`
- C++ JUCE: `juce_osc` module (built-in)

#### B. MIDI over Network ⭐⭐⭐

**Technical Specs:**
- Protocol: RTP-MIDI, Network MIDI (various standards)
- Data: Standard MIDI messages
- Latency: 5-20ms depending on implementation

**Advantages:**
- ✅ **Standard protocol:** MIDI is universal
- ✅ **Wide support:** Every DAW and plugin understands MIDI
- ✅ **Proven:** Decades of use

**Challenges:**
- ❌ **7-bit resolution:** Only 0-127 values
- ❌ **Network MIDI complexity:** Multiple competing standards
- ❌ **Latency variability:** Can be unpredictable over Wi-Fi

**Performia Application:**
- Suitable but OSC provides more flexibility
- Consider if targeting existing MIDI infrastructure

#### C. WebSocket Audio Streaming ⭐⭐

**Technical Specs:**
- Transport: TCP/HTTP (persistent connection)
- Data: Binary audio or JSON MIDI
- Latency: 10-50ms depending on buffer size

**Advantages:**
- ✅ **Bidirectional:** Full-duplex communication
- ✅ **Web compatible:** Can stream to browser
- ✅ **Reliable:** TCP guarantees delivery

**Challenges:**
- ❌ **Higher latency than UDP:** TCP overhead + buffering
- ❌ **Bandwidth intensive if streaming audio**
- ❌ **Not designed for ultra-low latency**

**Performia Application:**
- Better for UI communication than agent→audio
- Consider for Living Chart updates, not performance audio

#### D. Shared Memory IPC ⭐⭐⭐⭐

**Technical Specs:**
- Mechanism: OS-level shared memory region
- Access: Direct memory read/write
- Latency: <0.1ms (fastest possible IPC)

**Advantages:**
- ✅ **Lowest possible latency:** Direct memory access
- ✅ **High throughput:** No network/serialization overhead
- ✅ **Local communication:** Perfect for single-machine processes

**Challenges:**
- ❌ **Complex synchronization:** Race conditions, explicit locking
- ❌ **Not network-capable:** Only works on same machine
- ❌ **OS-specific:** Different APIs for macOS/Windows/Linux
- ❌ **Fails in sandboxed environments**

**Performia Application:**
- Use for high-frequency data (audio buffers, beat sync)
- Combine with OSC for command/control messages

#### E. gRPC ⭐⭐⭐

**Technical Specs:**
- Transport: HTTP/2
- Serialization: Protocol Buffers (binary)
- Latency: 5-15ms for local communication

**Advantages:**
- ✅ **Efficient binary encoding:** Smaller than JSON
- ✅ **Multiplexing:** Multiple requests over one connection
- ✅ **Typed API:** Strong contracts via protobuf

**Challenges:**
- ❌ **HTTP/2 overhead:** Heavier than UDP
- ❌ **Not designed for audio:** Better for API calls
- ❌ **More complex than OSC**

**Performia Application:**
- Better for backend microservices than real-time audio
- Overkill for agent communication

### Recommendation: **OSC + Shared Memory Hybrid**

**Architecture:**
```
Python Agent Process                    JUCE Audio Engine Process
│                                       │
├─ OSC Client ──────────────────────────→ OSC Receiver
│  (Control messages)                      │
│  - Start/stop                           │
│  - Pattern changes                      │
│  - Parameter updates                    │
│                                          │
├─ Shared Memory Writer ────────────────→ Shared Memory Reader
   (High-frequency data)                   (Beat clock, audio features)
   - MIDI events
   - Timing sync

Latency: <2ms total round-trip
```

**Benefits:**
- OSC handles control plane (flexible, easy to debug)
- Shared memory handles data plane (ultra-low latency)
- Best of both worlds

---

## 3. Storage & Memory Recommendations

### 3.1 What to Store

**Song Understanding:**
- Original stems (audio files): Filesystem (large binary data)
- Extracted features (chords, beats, melody): Database (queryable metadata)
- Learned patterns (model embeddings): Vector DB or filesystem (depends on retrieval needs)
- Agent-specific knowledge (bass walks, drum patterns): SQLite JSON blobs or separate files

**Performance History:**
- MIDI performances: Filesystem (`.mid` files) + DB (metadata)
- Performance metrics (tempo stability, dynamics): Database (time-series data)
- User ratings/feedback: Database (relational data)

**Instrument Configuration:**
- VST plugin paths/settings: Database or config files
- Agent parameters (temperature, creativity): Database
- Tone/effects chains: JSON files referenced by DB

### 3.2 Storage Technology Comparison

#### A. Filesystem (JSON/MIDI Files) ⭐⭐⭐⭐

**Structure:**
```
songs/
├── song_abc123/
│   ├── song_map.json          # Song structure
│   ├── stems/
│   │   ├── bass.wav
│   │   ├── drums.wav
│   │   └── vocals.wav
│   ├── agents/
│   │   ├── drums_config.json
│   │   ├── bass_patterns.json
│   │   └── keys_voicings.json
│   └── performances/
│       ├── 2025-10-01_001.mid
│       └── 2025-10-01_002.mid
```

**Advantages:**
- ✅ **Simple:** No DB setup, easy to inspect
- ✅ **Version control:** Git-friendly
- ✅ **Portable:** Copy folder = copy song
- ✅ **Backup:** Standard filesystem tools

**Challenges:**
- ❌ **Limited queries:** Can't search "all songs in key of C" easily
- ❌ **No indexing:** Slow for large libraries
- ❌ **Concurrency:** Manual locking for multi-process access

**Best for:** Audio stems, MIDI performances, configuration files

#### B. SQLite ⭐⭐⭐⭐⭐ **RECOMMENDED**

**Schema Example:**
```sql
CREATE TABLE songs (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT,
    bpm INTEGER,
    key TEXT,
    time_signature TEXT,
    duration_seconds REAL,
    song_map_path TEXT,  -- Filesystem reference
    created_at TIMESTAMP,
    last_performed TIMESTAMP
);

CREATE TABLE agent_configs (
    song_id TEXT,
    instrument TEXT,  -- 'drums', 'bass', 'keys'
    config_json TEXT,  -- JSON blob of agent parameters
    model_path TEXT,   -- Filesystem reference to model file
    FOREIGN KEY (song_id) REFERENCES songs(id)
);

CREATE TABLE performances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_id TEXT,
    timestamp TIMESTAMP,
    midi_path TEXT,  -- Filesystem reference
    duration_seconds REAL,
    tempo_stability REAL,
    user_rating INTEGER,
    FOREIGN KEY (song_id) REFERENCES songs(id)
);

CREATE TABLE song_features (
    song_id TEXT,
    feature_type TEXT,  -- 'chords', 'beats', 'melody'
    timestamp_ms INTEGER,
    value TEXT,  -- JSON or simple value
    FOREIGN KEY (song_id) REFERENCES songs(id)
);

CREATE INDEX idx_songs_key ON songs(key);
CREATE INDEX idx_performances_timestamp ON performances(timestamp);
```

**Advantages:**
- ✅ **Embedded:** No server process, zero configuration
- ✅ **Fast:** Excellent query performance for 1000s of songs
- ✅ **ACID:** Reliable transactions
- ✅ **SQL:** Powerful queries (filter, join, aggregate)
- ✅ **Small footprint:** <1MB library
- ✅ **Single file:** Easy backup (copy `.db` file)
- ✅ **Python support:** `sqlite3` built-in

**Challenges:**
- ⚠️ Limited concurrency (one writer at a time)
- ⚠️ Not ideal for >100GB data (but Performia won't hit this)

**Best for:** Metadata, song features, performance history, agent configs

**Performia Application:**
- **Primary database for all structured data**
- Beets music manager proves this approach works excellently
- Single-user, read-heavy workload is perfect for SQLite

#### C. PostgreSQL ⭐⭐

**When to use:**
- Multi-user scenarios (collaboration, cloud deployment)
- Need advanced features (full-text search, geographic data)
- Data >100GB

**Challenges for Performia:**
- ❌ **Overkill:** Requires server setup, management
- ❌ **Complexity:** Connection pooling, authentication
- ❌ **Resource overhead:** Background processes

**Performia Recommendation:**
- Start with SQLite
- Migrate to PostgreSQL only if scaling to cloud/multi-user

#### D. Vector Database (Pinecone, Weaviate) ⭐⭐⭐

**Use case:** Semantic search over music

**How it works:**
```python
# Store song embeddings
song_embedding = audio_model.encode(stems)  # → 2048-dim vector
vector_db.upsert("song_abc123", song_embedding, metadata={"title": "...", "key": "C"})

# Find similar songs
similar = vector_db.query(new_song_embedding, top_k=10)
# Returns: Songs with similar sound/feel/style
```

**When useful:**
- "Find songs similar to this one" (for agent learning)
- "What songs have this bass feel?"
- Recommendation systems

**Options:**
- **Pinecone:** Managed cloud ($70+/month), simple API
- **Weaviate:** Self-hosted or cloud, open source
- **ChromaDB:** Lightweight, embeddable (like SQLite for vectors)
- **FAISS:** Facebook's library, no server (can embed in app)

**Performia Recommendation:**
- **Phase 1 (MVP):** Skip vector DB, not critical
- **Phase 2:** Add ChromaDB or FAISS for "similar song" agent learning
- **Phase 3:** Consider Weaviate if building large training corpus

#### E. Redis ⭐⭐

**Use case:** In-memory caching, real-time state

**Examples:**
- Current playback state (beat position, active agents)
- Real-time metrics (latency, CPU usage)
- Pub/sub for live updates to UI

**Challenges:**
- ❌ In-memory = lost on restart (need persistence layer)
- ❌ Another service to run and manage
- ❌ Overkill for single-user desktop app

**Performia Recommendation:**
- Not needed for MVP
- Consider if building web/cloud version

### 3.3 Recommended Hybrid Architecture

```
Storage Layer:

1. SQLite Database (song_library.db)
   ├─ Songs table (metadata)
   ├─ Agent configs table
   ├─ Performance history table
   └─ Features table (chords, beats)

2. Filesystem
   ├─ /audio_stems/          (large binary audio)
   ├─ /song_maps/            (JSON Song Maps)
   ├─ /agent_models/         (trained model files .pt, .onnx)
   ├─ /midi_performances/    (recorded MIDI .mid)
   └─ /vst_plugins/          (user's plugin library)

3. Optional: ChromaDB (Phase 2)
   └─ Song embeddings for similarity search

Access Pattern:
- SQLite for all queries/filters
- Filesystem for bulk data retrieval
- Files referenced by path in SQLite
```

**Benefits:**
- Fast queries (SQLite indexes)
- Simple backup (copy DB + folder)
- Git-friendly for song maps
- No server management
- Scales to 10,000+ songs easily

---

## 4. Latency & Performance Analysis

### 4.1 Target Latency: <10ms for Professional Performance

**Human Perception Research:**
- **Zero latency perceived as highest quality** by professional percussionists
- **10ms latency:** No significant quality difference from zero (study: percussionists + amateurs)
- **20-30ms:** "Perfectly acceptable for typical musical applications"
- **40-160ms:** Tolerable for ensemble synchronization (synchronization with metronome)
- **42ms:** Perceptual asynchrony threshold for active interaction (drumming study)

**Instrument-specific tolerance:**
- **Least tolerant:** Vocalists, saxophonists (need <10ms)
- **Most tolerant:** Keyboardists, drummers (accept 20-30ms)
- **Mid-range:** Guitar players

**Performia Target:** **<20ms total system latency**
- Vocalists perform with accompaniment → need low latency
- 20ms ensures professional quality for all instruments
- Leaves headroom for system variation

### 4.2 Latency Sources & Budget

**Total latency budget: 20ms**

| Component | Latency | Optimization Strategy |
|-----------|---------|----------------------|
| **Audio input** | 2-5ms | Small buffer (64-128 samples @ 48kHz) |
| **Beat/chord detection** | 2-5ms | Lightweight DSP, pre-computed features |
| **AI model inference** | 5-10ms | Quantized small model, GPU/optimized CPU |
| **MIDI generation** | <1ms | Direct event creation |
| **OSC transmission** | <1ms | Local UDP (microseconds) |
| **VST plugin processing** | 2-5ms | Modern plugins, PDC (plugin delay compensation) |
| **Audio output** | 2-5ms | Small buffer |
| **TOTAL** | **13-27ms** | **Target: <20ms avg** |

### 4.3 AI Model Inference Optimization

**Goal:** <10ms inference time for agent decision-making

**Model Size vs. Latency (on M3 MacBook Pro):**
| Model Size | Precision | CPU Latency | GPU Latency | Notes |
|------------|-----------|-------------|-------------|-------|
| 10M params | FP32 | ~2ms | ~1ms | Tiny, limited capability |
| 50M params | FP32 | ~8ms | ~3ms | Sweet spot for instruments |
| 100M params | FP32 | ~15ms | ~5ms | Larger capacity |
| 50M params | INT8 | ~3ms | ~2ms | Quantized (4x smaller) |
| 200M params | INT8 | ~10ms | ~4ms | Music Transformer size |

**Optimization Techniques:**

1. **Quantization (INT8):**
   - Convert FP32 → INT8 (4x size reduction)
   - ONNX Runtime: up to 6x speedup on VNNI CPUs
   - Minimal quality loss (<2% accuracy drop)
   - Tools: ONNX Runtime, TensorFlow Lite

2. **Model Distillation:**
   - Train small "student" model to mimic large "teacher"
   - DistilHuBERT: 73% faster training, preserved performance
   - GrooVAE: Already small enough (~20M params)

3. **Pruning:**
   - Remove unnecessary weights/connections
   - 30-50% size reduction with <1% quality loss
   - Structured pruning = faster inference

4. **Hardware Acceleration:**
   - **GPU:** 2-4x faster than CPU for medium models
   - **Edge TPU:** 4 TOPS @ 2W (excellent efficiency)
   - **CPU SIMD:** AVX2/VNNI on Intel, NEON on ARM
   - **Neural Engine:** M1/M2/M3 chips (16 TOPS on M3 Pro)

**Recommended Stack:**
```
Model: 20-50M parameter Transformer (per instrument)
Precision: INT8 quantization via ONNX Runtime
Hardware: M1/M2/M3 Neural Engine or NVIDIA GPU (GTX 1660+)
Inference latency: 3-8ms average
```

### 4.4 Deployment Strategy

**Local (Recommended for MVP):**
- ✅ <10ms latency (no network)
- ✅ Privacy (no data sent to cloud)
- ✅ Reliability (works offline)
- ✅ Cost (no cloud inference fees)
- ❌ Requires user hardware (GPU recommended)

**Hardware Requirements:**
- **Minimum:** M1 MacBook Air, Intel i5 + GTX 1650
- **Recommended:** M2/M3 Mac, Intel i7 + RTX 3060
- **Target latency achieved:** <15ms on recommended hardware

**Edge (Future):**
- Coral Edge TPU USB stick ($60)
- 4 TOPS, 2W power
- INT8 models optimized for EdgeTPU
- <5ms inference for small models
- **Challenge:** TensorFlow Lite format (need to convert from PyTorch)

**Cloud (Not Recommended for Real-Time):**
- ❌ Network latency: 20-100ms (disqualifies for real-time)
- ✅ Could use for preprocessing (Song Map generation, model training)
- ✅ Useful for collaborative features (share performances)

### 4.5 Latency Monitoring & Compensation

**Implementation:**
```python
class LatencyMonitor:
    def __init__(self):
        self.inference_times = []
        self.total_latency = []

    def measure_inference(self, model_fn):
        start = time.perf_counter()
        result = model_fn()
        latency_ms = (time.perf_counter() - start) * 1000
        self.inference_times.append(latency_ms)
        return result, latency_ms

    def get_stats(self):
        return {
            'mean': np.mean(self.inference_times),
            'p95': np.percentile(self.inference_times, 95),
            'p99': np.percentile(self.inference_times, 99)
        }
```

**Plugin Delay Compensation (PDC):**
- JUCE provides automatic PDC via `setLatencySamples()`
- VST plugins report their processing delay
- Host compensates by aligning tracks

**Adaptive Buffering:**
- Monitor inference time variability
- Increase buffer if p99 latency exceeds target
- Display warning if latency >20ms sustained

---

## 5. Training Strategy

### 5.1 Pre-trained Models to Leverage

**Magenta Models (Open Source, Apache 2.0):**

| Model | Task | Size | Pre-trained | Fine-tunable | Performia Use |
|-------|------|------|-------------|--------------|---------------|
| **GrooVAE** | Drum patterns | ~20M | ✅ Yes | ✅ Yes | **MVP Drums** |
| **Performance RNN** | Expressive MIDI | ~50M | ✅ Yes | ✅ Yes | Bass, keys |
| **Music Transformer** | Long-form composition | ~200M | ✅ Yes | ✅ Yes | Enhanced agents |
| **Coconet** | Bach-style harmony | ~30M | ✅ Yes | ✅ Yes | Keys voicings |

**Hugging Face Models:**

| Model | Task | Size | Hub Link | Performia Use |
|-------|------|------|----------|---------------|
| **DistilHuBERT** | Audio understanding | ~100M | `ntu-spml/distilhubert` | Feature extraction |
| **MusicGen** | Audio generation | 1.5B+ | `facebook/musicgen-large` | **Not real-time** |
| **Pop2Piano** | Lead sheet → piano | ~300M | `sweetcocoa/pop2piano` | Keys agent |

**Datasets for Fine-tuning:**

| Dataset | Content | Size | License | Use Case |
|---------|---------|------|---------|----------|
| **Lakh MIDI** | 174K multi-track | ~20GB | MIT | General training |
| **MAESTRO** | Classical piano | 200hrs | CC-BY-NC-SA | Piano performance |
| **Groove MIDI** | Professional drums | 1,150 bars | CC-BY-4.0 | **Drum training** |
| **DadaGP** | GuitarPro tabs | 26K songs | Research | Multi-instrument |
| **GTZAN** | Genre classification | 1K songs | Research | Style detection |

### 5.2 Training Approach: Three-Tier Strategy

#### Tier 1: Pre-trained Models (No Training) - **MVP**

**Approach:**
- Use Magenta GrooVAE for drums as-is
- Use Performance RNN for bass/keys
- No custom training required

**Steps:**
```python
# Load pre-trained GrooVAE
import magenta
model = magenta.models.groovae.load_checkpoint('pretrained')

# Condition on tempo, style
drums_midi = model.generate(
    temperature=0.8,
    steps=16,  # 1 bar
    primer=[],  # Start from scratch or use seed
)

# Convert to MIDI events → OSC → JUCE
```

**Advantages:**
- ✅ **Zero training time:** Start building immediately
- ✅ **Proven quality:** Models already generate good music
- ✅ **Low risk:** Known to work

**Limitations:**
- ⚠️ Generic style (not song-specific)
- ⚠️ May not capture unique feel of each song

**Timeline:** Day 1 - working drum agent

#### Tier 2: Fine-tuning on Song Stems - **Enhanced**

**Approach:**
- Extract MIDI from song stems using source separation + transcription
- Fine-tune pre-trained model on song-specific patterns

**Workflow:**
```
1. Source separation:
   Demucs(full_mix) → bass.wav, drums.wav, keys.wav

2. Audio-to-MIDI transcription:
   Drums: Aubio onset detection + beat tracking
   Bass: Crepe pitch tracking + onset detection
   Keys: Piano transcription model (e.g., Pop2Piano, Onsets & Frames)

3. Create fine-tuning dataset:
   - Original song MIDI patterns
   - Augmented variations (transposed, tempo-shifted)
   - Total: 50-200 bars per instrument

4. Fine-tune:
   base_model = load_pretrained('groovae')
   fine_tuned = fine_tune(
       base_model,
       song_midi,
       epochs=50,
       learning_rate=1e-4
   )

5. Save song-specific agent:
   save_model(f'agents/{song_id}_drums.onnx')
```

**Tools:**
- **Demucs v4:** State-of-the-art source separation (9.20 dB SDR)
- **Crepe:** Monophonic pitch tracking (bass)
- **Aubio:** Real-time onset/beat detection
- **Basic Pitch (Spotify):** Multi-pitch transcription

**Timeline:**
- Transcription: 5-10 min per song (automated)
- Fine-tuning: 10-30 min per instrument on GPU
- Total: <1 hour per song to create all agents

**Advantages:**
- ✅ **Song-specific style:** Agents learn the exact feel
- ✅ **Moderate effort:** Mostly automated
- ✅ **Better quality:** Closer to original performance

**Challenges:**
- ⚠️ Transcription errors (especially for complex music)
- ⚠️ Requires GPU for fine-tuning
- ⚠️ Need to build transcription pipeline

#### Tier 3: Custom Training from Scratch - **Future**

**When to consider:**
- Need specialized architecture (e.g., multi-agent coordination)
- Pre-trained models don't capture required behavior
- Have large custom dataset (1000+ songs)

**Approach:**
- Design custom Transformer architecture
- Train on large corpus (Lakh MIDI + Groove MIDI + custom data)
- Weeks of GPU training (V100/A100)

**Performia Recommendation:**
- **Not needed for MVP or enhanced version**
- Pre-trained + fine-tuning is sufficient
- Only consider if building commercial product with unique IP

### 5.3 Recommended Training Pipeline (Tier 2)

**Phase 1: Offline Song Analysis (When song added to library)**
```python
def prepare_song_agents(song_path):
    # 1. Source separation
    stems = demucs.separate(song_path)  # 3-5 minutes

    # 2. Feature extraction
    chords = librosa.chord_detection(stems['vocals'])
    beats = librosa.beat_track(stems['drums'])

    # 3. MIDI transcription
    drums_midi = transcribe_drums(stems['drums'])  # Aubio
    bass_midi = transcribe_bass(stems['bass'])      # Crepe
    keys_midi = transcribe_keys(stems['other'])    # BasicPitch

    # 4. Create training data
    dataset = {
        'drums': drums_midi,
        'bass': bass_midi,
        'keys': keys_midi,
        'chords': chords,
        'beats': beats
    }

    return dataset

def fine_tune_agents(song_id, dataset):
    # 5. Fine-tune each instrument (parallel)
    with ThreadPoolExecutor() as executor:
        drums_future = executor.submit(
            fine_tune_model,
            'groovae', dataset['drums'], f'{song_id}_drums'
        )
        bass_future = executor.submit(
            fine_tune_model,
            'performance_rnn', dataset['bass'], f'{song_id}_bass'
        )
        keys_future = executor.submit(
            fine_tune_model,
            'coconet', dataset['keys'], f'{song_id}_keys'
        )

    # 6. Quantize models for inference
    for model_name in ['drums', 'bass', 'keys']:
        quantize_to_int8(f'{song_id}_{model_name}.pt')

    # 7. Store in database
    db.store_agent_config(song_id, {
        'drums': f'agents/{song_id}_drums.onnx',
        'bass': f'agents/{song_id}_bass.onnx',
        'keys': f'agents/{song_id}_keys.onnx'
    })
```

**Phase 2: Real-time Inference (During performance)**
```python
# Load quantized models once at startup
agents = {
    'drums': load_onnx_model(f'{song_id}_drums.onnx'),
    'bass': load_onnx_model(f'{song_id}_bass.onnx'),
    'keys': load_onnx_model(f'{song_id}_keys.onnx')
}

# Real-time generation loop (<10ms)
def generate_next_beat(current_beat, current_chord):
    # Parallel inference for all instruments
    drums_events = agents['drums'].generate(
        conditioning={'beat': current_beat}
    )
    bass_events = agents['bass'].generate(
        conditioning={'chord': current_chord, 'beat': current_beat}
    )
    keys_events = agents['keys'].generate(
        conditioning={'chord': current_chord, 'voicing': 'close'}
    )

    # Send via OSC to JUCE
    send_midi_events([drums_events, bass_events, keys_events])
```

### 5.4 Local vs. Cloud Training

**Training (Offline):**
- **Local GPU:** Fine-tuning takes 10-30 min → acceptable on user's machine
- **Cloud GPU:** Use if user has no GPU (AWS/GCP spot instances ~$0.50/hr)
- **Recommendation:** Offer both options

**Inference (Real-time):**
- **Must be local** for <10ms latency
- Cloud inference adds 20-100ms network latency → unacceptable

---

## 6. Specific Recommendations for Performia

### 6.1 Best First Instrument: **Drums** 🥁

**Why drums first:**

1. **Musical Simplicity:**
   - Fixed pitches (no need to follow complex harmonies)
   - Rhythmic focus (one primary task: keep time)
   - Forgiving of variation (humans expect drum fills/changes)

2. **Technical Advantages:**
   - **Mature models:** GrooVAE is proven and ready-to-use
   - **Rich training data:** Groove MIDI dataset (professional drummers)
   - **Easy transcription:** Onset detection is more reliable than pitch tracking
   - **Simple MIDI:** General MIDI drum map is standardized

3. **User Value:**
   - **Most requested:** Drummers are expensive/hard to find for practice
   - **High impact:** Solid drums make any song feel professional
   - **Practice tool:** Musicians want to play along with realistic drums

4. **Performance:**
   - **Low latency:** Pattern-based generation is fast
   - **VST ecosystem:** Excellent drum VSTs (Superior Drummer, Addictive Drums, etc.)

**Why not bass first:**
- Requires chord following (more complex)
- Pitch tracking less reliable than onset detection
- Less forgiving of wrong notes

**Why not keys first:**
- Complex voicings and inversions
- Harder to transcribe from audio
- Can be optional in many songs (drums are essential)

### 6.2 Storage Solution: **SQLite + Filesystem**

**Architecture:**
```
Performia/
├── data/
│   ├── performia.db              # SQLite database
│   ├── songs/
│   │   ├── {song_id}/
│   │   │   ├── stems/            # Audio files
│   │   │   ├── song_map.json     # Song structure
│   │   │   └── features.json     # Chords, beats
│   ├── agents/
│   │   └── {song_id}_{instrument}.onnx
│   └── performances/
│       └── {song_id}_{timestamp}.mid
```

**SQLite Schema:**
```sql
-- Core tables
CREATE TABLE songs (...);          -- Metadata
CREATE TABLE agent_configs (...);  -- Model configurations
CREATE TABLE performances (...);   -- Performance history
CREATE TABLE song_features (...);  -- Chords, beats, melody

-- Indexes for fast queries
CREATE INDEX idx_songs_key ON songs(key);
CREATE INDEX idx_songs_bpm ON songs(bpm);
```

**Why this choice:**
- ✅ Single-user app → SQLite is perfect
- ✅ Beets proves it works for music libraries
- ✅ Zero configuration, embedded
- ✅ Fast queries for library UI
- ✅ Large files in filesystem (Git-friendly, portable)

### 6.3 Audio Synthesis: **VST Hosting in JUCE**

**Approach:**
```
[Python Agent] → MIDI → [OSC] → [JUCE Host] → [VST Plugin] → [Audio Out]
                                       ↓
                              Hosts user's drum VST
                              (Superior Drummer, etc.)
```

**Implementation:**
```cpp
// JUCE plugin hosting
AudioPluginFormatManager formatManager;
formatManager.addDefaultFormats();  // VST3, AU, etc.

// Load user's chosen drum plugin
auto pluginDescription = KnownPluginList::getTypeForFile(vst_path);
String errorMessage;
auto plugin = formatManager.createPluginInstance(
    *pluginDescription,
    sampleRate,
    bufferSize,
    errorMessage
);

// Receive OSC MIDI events from Python agent
OSCReceiver osc;
osc.addListener(this);
osc.connect(9000);

void oscMessageReceived(const OSCMessage& message) {
    if (message.getAddressPattern() == "/drums/note_on") {
        int note = message[0].getInt32();
        int velocity = message[1].getInt32();

        // Create MIDI event
        MidiMessage midi = MidiMessage::noteOn(1, note, (uint8)velocity);

        // Send to VST plugin
        plugin->processBlock(audioBuffer, midiBuffer);
    }
}
```

**Why this choice:**
- ✅ **Professional quality:** Users choose their favorite drum sounds
- ✅ **Low latency:** Modern VSTs add <5ms
- ✅ **Flexibility:** Works with any VST3/AU plugin
- ✅ **JUCE ecosystem:** Mature plugin hosting support
- ✅ **No training:** Synthesis handled by professional tools

**Challenges:**
- ⚠️ Plugin scanning at startup (can be slow → cache results)
- ⚠️ Latency reporting variability (implement PDC)
- ⚠️ 7x CPU overhead (optimize JUCE wrapper)

**Mitigation:**
- Cache plugin scan results
- Pre-load plugins at app startup
- Implement automatic plugin delay compensation
- Benchmark and optimize wrapper (consider direct VST3 SDK)

### 6.4 Agent Architecture: **Hybrid Rule-Based + Small Transformer**

**Drums Agent Architecture:**
```
┌─────────────────────────────────────────────┐
│           DRUMS AGENT (Python)              │
├─────────────────────────────────────────────┤
│                                             │
│  Rules Engine (Fast, Deterministic)         │
│  ├─ Tempo tracking (follow beat clock)     │
│  ├─ Time signature enforcement              │
│  ├─ Quantization (snap to grid)             │
│  └─ Dynamic range limiting                  │
│                                             │
│  ML Model (GrooVAE - 20M params, INT8)      │
│  ├─ Pattern generation                      │
│  ├─ Fill detection & execution              │
│  ├─ Humanization (timing, velocity)         │
│  └─ Style variation                         │
│                                             │
│  Decision Fusion:                           │
│  ├─ ML generates candidate patterns         │
│  ├─ Rules validate & constrain             │
│  └─ Output: Musical + Expressive MIDI       │
│                                             │
└─────────────────────────────────────────────┘
        ↓ OSC (MIDI events)
┌─────────────────────────────────────────────┐
│         JUCE AUDIO ENGINE (C++)             │
├─────────────────────────────────────────────┤
│  ├─ Receive OSC MIDI events                 │
│  ├─ Route to Superior Drummer VST           │
│  └─ Mix audio output                        │
└─────────────────────────────────────────────┘
```

**Code Example:**
```python
class DrumsAgent:
    def __init__(self, song_id):
        # Load fine-tuned model
        self.model = load_onnx_model(f'agents/{song_id}_drums.onnx')

        # Load song knowledge
        self.song_map = load_song_map(song_id)
        self.tempo = self.song_map['bpm']
        self.time_signature = self.song_map['time_signature']

        # Rules
        self.rules = DrumRules(tempo=self.tempo, time_sig=self.time_signature)

    def generate_bar(self, current_section, intensity):
        # ML generates pattern candidates
        candidates = self.model.sample(
            temperature=0.8,
            num_samples=5,
            conditioning={'section': current_section, 'intensity': intensity}
        )

        # Rules validate and select best
        valid_patterns = [
            p for p in candidates
            if self.rules.is_valid(p)
        ]

        if not valid_patterns:
            # Fallback: Use rule-based basic pattern
            return self.rules.generate_fallback_pattern()

        # Select most appropriate pattern
        best_pattern = self.rules.rank_patterns(valid_patterns)[0]

        # Humanize (slight timing/velocity variation)
        humanized = self.rules.humanize(best_pattern)

        return humanized

class DrumRules:
    def is_valid(self, pattern):
        # Ensure kick on downbeat
        if not self.has_kick_on_beat_1(pattern):
            return False

        # Ensure hi-hat maintains groove
        if not self.has_consistent_hihat(pattern):
            return False

        # Check dynamic range
        if not self.is_dynamic_range_reasonable(pattern):
            return False

        return True

    def humanize(self, pattern):
        # Add slight timing variation (±5ms)
        for note in pattern:
            note.timing += random.gauss(0, 0.005)  # seconds
            note.velocity += random.randint(-3, 3)  # MIDI velocity

        return pattern
```

**Why hybrid:**
- ✅ **Reliability:** Never plays "wrong" (rules ensure musicality)
- ✅ **Creativity:** ML provides variation and adaptation
- ✅ **Low latency:** Simple rules are fast (<1ms)
- ✅ **Debuggable:** Can inspect and adjust rules
- ✅ **Graceful degradation:** Falls back to rules if ML fails

### 6.5 Communication Protocol: **OSC + Shared Memory**

**Primary: OSC for MIDI Events**
```python
# Python agent
from pythonosc import udp_client

osc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

# Send note events
osc_client.send_message("/drums/note_on", [note, velocity, timestamp])
osc_client.send_message("/drums/note_off", [note, timestamp])

# Send control messages
osc_client.send_message("/drums/set_pattern", [pattern_id])
osc_client.send_message("/drums/intensity", [0.8])  # 0.0-1.0
```

```cpp
// JUCE receiver
OSCReceiver receiver;
receiver.addListener(this);
receiver.connect(9000);

void oscMessageReceived(const OSCMessage& msg) {
    if (msg.getAddressPattern().toString() == "/drums/note_on") {
        int note = msg[0].getInt32();
        int velocity = msg[1].getInt32();
        float timestamp = msg[2].getFloat32();

        // Create MIDI and schedule
        MidiMessage midiMsg = MidiMessage::noteOn(10, note, (uint8)velocity);
        scheduleMidiEvent(midiMsg, timestamp);
    }
}
```

**Secondary: Shared Memory for Beat Clock (High-Frequency Sync)**
```cpp
// JUCE writes beat position to shared memory
struct BeatClock {
    double beat_position;      // 0.0 to song_length_beats
    double timestamp_ms;       // High-precision time
    bool is_playing;
};

// Update every audio callback
void audioDeviceIOCallback(...) {
    sharedMemory->beat_position = currentBeat;
    sharedMemory->timestamp_ms = Time::getMillisecondCounterHiRes();
}
```

```python
# Python reads beat position
import mmap
import struct

# Map shared memory
shm = mmap.mmap(-1, 24, "PerformiaBeatClock")

def get_current_beat():
    shm.seek(0)
    beat_pos, timestamp, playing = struct.unpack('ddb', shm.read(24))
    return beat_pos, timestamp, bool(playing)

# Sync agent generation to beat
while True:
    beat, timestamp, playing = get_current_beat()
    if beat % 1.0 < 0.01:  # On downbeat
        next_pattern = agent.generate_bar(beat)
        send_pattern_via_osc(next_pattern)
```

**Why OSC + Shared Memory:**
- ✅ **OSC:** Flexible, debuggable, human-readable
- ✅ **Shared Memory:** <0.1ms latency for beat sync
- ✅ **Best of both:** Control plane (OSC) + data plane (shared mem)
- ✅ **Proven:** Standard in music software (TouchOSC, Lemur, etc.)

### 6.6 Training Approach: **Pre-trained + Fine-tuning**

**Phase 1: MVP (No Training)**
```python
# Use Magenta GrooVAE pre-trained model
from magenta.models import groovae

model = groovae.load_checkpoint('pretrained')

# Generate generic drum patterns
drums = model.sample(temperature=0.8)

# Send to JUCE
send_midi(drums)
```
**Timeline:** Immediate - working drum agent

**Phase 2: Enhanced (Fine-tuning per Song)**
```python
# 1. Transcribe drums from song
drum_midi = transcribe_drums(song_stems['drums'])  # 5 min

# 2. Fine-tune GrooVAE on song-specific patterns
fine_tuned_model = groovae.fine_tune(
    base_checkpoint='pretrained',
    train_data=drum_midi,
    steps=5000,  # 20 min on GPU
    learning_rate=1e-4
)

# 3. Quantize for inference
onnx_model = convert_to_onnx(fine_tuned_model)
quantized_model = quantize_int8(onnx_model)  # <50MB

# 4. Save song-specific agent
save_model(f'agents/{song_id}_drums.onnx')
```
**Timeline:** 30 min per song (automated)

**Phase 3: Continuous Improvement (Reinforcement Learning)**
```python
# After initial fine-tuning, use RL to improve live following

# Reward function
def compute_reward(agent_performance, human_performance):
    sync_score = measure_synchronization(agent, human)
    musical_score = measure_musicality(agent_output)
    return 0.7 * sync_score + 0.3 * musical_score

# RL fine-tuning (optional, advanced)
rl_agent = reinforce(
    base_model=fine_tuned_model,
    reward_fn=compute_reward,
    episodes=100  # 100 practice sessions
)
```
**Timeline:** Future enhancement (Phase 3)

**Recommendation:**
- **Start:** Phase 1 (pre-trained, generic)
- **Enhance:** Phase 2 (fine-tuned, song-specific) after MVP proves concept
- **Advanced:** Phase 3 (RL adaptation) for version 2.0

---

## 7. Implementation Phases

### Phase 1: MVP - Drum Agent with Pre-trained Model

**Goal:** Working drum agent that follows tempo and plays patterns

**Timeline:** 2-3 weeks

**Tech Stack:**
- **Agent:** Python + Magenta GrooVAE (pre-trained)
- **Communication:** OSC (pythonosc → JUCE)
- **Synthesis:** JUCE VST host + free drum VST (MT Power Drumkit)
- **Storage:** SQLite (songs table) + filesystem (song maps)
- **No training:** Use model as-is

**Deliverables:**
1. Python agent that loads GrooVAE and generates 4-bar drum patterns
2. JUCE application that:
   - Receives OSC MIDI events
   - Hosts VST drum plugin
   - Plays audio output
3. Beat clock synchronization (shared memory or OSC)
4. Basic UI: Start/stop, tempo, intensity slider

**Success Criteria:**
- ✅ Drum agent plays realistic patterns in time
- ✅ Total latency <20ms
- ✅ User can start/stop and adjust intensity
- ✅ Works with user's drum VST plugin

**Architecture:**
```
┌──────────────────┐
│  Living Chart    │ (Existing Performia frontend)
│  (React/Vite)    │
└────────┬─────────┘
         │ WebSocket (beat position, playback state)
         ↓
┌──────────────────┐
│  Python Backend  │
│  ─────────────   │
│  Drum Agent      │ ← Magenta GrooVAE (pre-trained)
│  Beat Tracker    │
│  OSC Sender      │
└────────┬─────────┘
         │ OSC (MIDI events: /drums/note_on)
         ↓
┌──────────────────┐
│  JUCE Audio      │
│  ─────────────   │
│  OSC Receiver    │
│  VST Host        │ → MT Power Drumkit (free VST)
│  Audio Output    │
└──────────────────┘
```

**Code Scaffolding:**

*Python Agent (drums_agent.py):*
```python
from magenta.models import groovae
from pythonosc import udp_client
import time

class DrumsAgent:
    def __init__(self, bpm=120):
        self.model = groovae.load_checkpoint('pretrained')
        self.osc = udp_client.SimpleUDPClient("127.0.0.1", 9000)
        self.bpm = bpm
        self.beat_duration = 60.0 / bpm

    def generate_pattern(self, num_bars=4):
        # Generate drum pattern
        pattern = self.model.sample(temperature=0.8, num_steps=num_bars*16)
        return pattern

    def play_pattern(self, pattern):
        for note in pattern:
            # Send OSC note_on
            self.osc.send_message("/drums/note_on",
                [note.pitch, note.velocity, note.timing])

            # Wait until note time
            time.sleep(note.timing)

            # Send note_off
            self.osc.send_message("/drums/note_off", [note.pitch])

    def run(self):
        while True:
            pattern = self.generate_pattern()
            self.play_pattern(pattern)

if __name__ == "__main__":
    agent = DrumsAgent(bpm=120)
    agent.run()
```

*JUCE Audio Engine (Main.cpp):*
```cpp
class PerformiaAudioEngine : public AudioIODeviceCallback,
                              public OSCReceiver::Listener<OSCReceiver::RealtimeCallback>
{
public:
    PerformiaAudioEngine() {
        // Setup OSC
        oscReceiver.connect(9000);
        oscReceiver.addListener(this);

        // Load VST plugin
        formatManager.addDefaultFormats();
        loadDrumPlugin("MT Power Drumkit.vst3");
    }

    void oscMessageReceived(const OSCMessage& message) override {
        if (message.getAddressPattern() == "/drums/note_on") {
            int note = message[0].getInt32();
            int velocity = message[1].getInt32();

            MidiMessage midi = MidiMessage::noteOn(10, note, (uint8)velocity);
            midiBuffer.addEvent(midi, 0);
        }
    }

    void audioDeviceIOCallback(const float** inputChannelData,
                                int numInputChannels,
                                float** outputChannelData,
                                int numOutputChannels,
                                int numSamples) override {
        // Process VST plugin
        AudioBuffer<float> buffer(outputChannelData, numOutputChannels, numSamples);
        drumPlugin->processBlock(buffer, midiBuffer);
        midiBuffer.clear();
    }

private:
    OSCReceiver oscReceiver;
    AudioPluginFormatManager formatManager;
    std::unique_ptr<AudioPluginInstance> drumPlugin;
    MidiBuffer midiBuffer;
};
```

**Dependencies:**
```bash
# Python
pip install magenta pythonosc numpy

# JUCE modules
JUCE (OSC, AudioPluginHost, Audio)

# VST Plugin (free)
MT Power Drumkit or Steven Slate Drums Free
```

---

### Phase 2: Enhanced - Song-Specific Fine-Tuning

**Goal:** Drums agent learns each song's specific feel and patterns

**Timeline:** 4-6 weeks (after MVP)

**New Components:**
1. **Source separation:** Demucs integration
2. **Drum transcription:** Aubio onset detection + beat tracking
3. **Fine-tuning pipeline:** Song-specific model training
4. **Model management:** Store/load per-song agents

**Workflow:**
```
User adds song to library:
  1. Upload audio file (full mix)
  2. Demucs separates stems (3-5 min)
  3. Transcribe drums to MIDI (2 min)
  4. Fine-tune GrooVAE on drum MIDI (20 min on GPU)
  5. Quantize model to INT8 (1 min)
  6. Save to agents/{song_id}_drums.onnx
  7. Store config in SQLite

User performs song:
  1. Load song-specific agent from disk
  2. Agent generates patterns matching original feel
  3. More realistic, song-appropriate performance
```

**New Code:**

*Transcription Pipeline (transcribe.py):*
```python
import demucs
import aubio
import librosa

def transcribe_song(audio_path):
    # 1. Separate stems
    stems = demucs.separate(audio_path)  # Returns dict: {drums, bass, vocals, other}

    # 2. Transcribe drums
    drums_audio = stems['drums']

    # Beat tracking
    tempo, beats = librosa.beat.beat_track(y=drums_audio, sr=44100)

    # Onset detection for each drum sound
    onset_detector = aubio.onset("default", 1024, 512, 44100)
    onsets = []
    for frame in drums_audio:
        if onset_detector(frame):
            onsets.append(onset_detector.get_last())

    # Map onsets to MIDI notes (heuristics based on frequency)
    midi_notes = map_onsets_to_midi(onsets, drums_audio)

    # 3. Create MIDI file
    midi_file = create_midi_from_notes(midi_notes, tempo)

    return midi_file

def fine_tune_drums_agent(song_id, midi_file):
    # Load pre-trained GrooVAE
    base_model = groovae.load_checkpoint('pretrained')

    # Fine-tune on song MIDI
    fine_tuned = groovae.train(
        base_checkpoint=base_model,
        train_data=midi_file,
        num_steps=5000,
        learning_rate=1e-4,
        checkpoint_dir=f'checkpoints/{song_id}'
    )

    # Convert to ONNX
    onnx_model = convert_to_onnx(fine_tuned)

    # Quantize to INT8
    quantized = quantize_int8(onnx_model)

    # Save
    save_path = f'agents/{song_id}_drums.onnx'
    save_model(quantized, save_path)

    # Store in database
    db.execute('''
        INSERT INTO agent_configs (song_id, instrument, model_path)
        VALUES (?, 'drums', ?)
    ''', (song_id, save_path))

    return save_path
```

**Enhanced Agent Loader:**
```python
class EnhancedDrumsAgent:
    def __init__(self, song_id, bpm):
        # Load song-specific model if available
        model_path = db.get_agent_model(song_id, 'drums')

        if model_path and os.path.exists(model_path):
            print(f"Loading song-specific model: {model_path}")
            self.model = load_onnx_model(model_path)
        else:
            print("Using pre-trained generic model")
            self.model = groovae.load_checkpoint('pretrained')

        self.bpm = bpm
        self.osc = udp_client.SimpleUDPClient("127.0.0.1", 9000)
```

**Success Criteria:**
- ✅ Agent captures song-specific drum style
- ✅ Transcription → fine-tuning → deployment pipeline is automated
- ✅ <1 hour total processing per song
- ✅ Inference latency still <10ms (quantized models)

---

### Phase 3: Production - Multi-Instrument + RL Adaptation

**Goal:** Full band (drums, bass, keys) with real-time adaptation

**Timeline:** 8-12 weeks (after Enhanced)

**New Instruments:**
1. **Bass Agent:**
   - Model: Performance RNN (fine-tuned on Lakh MIDI bass tracks)
   - Input: Chord progression from Song Map
   - Output: Walking bass, root notes, fills
   - VST: User's bass plugin (Trilian, Modo Bass, etc.)

2. **Keys Agent:**
   - Model: Coconet (Bach-style harmonization, adapted for pop/rock)
   - Input: Chord progression + melody
   - Output: Piano/organ/synth voicings
   - VST: User's keys plugin (Keyscape, Omnisphere, etc.)

**Reinforcement Learning for Adaptation:**

*Problem:* Pre-trained + fine-tuned models play the song "correctly," but don't adapt to *live* human performance (tempo changes, dynamics, variations)

*Solution:* RL fine-tuning for real-time following

**RL Architecture:**
```
State:
  - Last 4 beats of human performance (audio features)
  - Current beat position
  - Current chord
  - Human dynamics (loud/soft)

Action:
  - Next 1 bar of agent MIDI

Reward:
  - Synchronization score (agent in time with human)
  - Musical appropriateness (plays right notes)
  - Dynamic matching (loud when human is loud)

Policy Network:
  - Transformer encoder (state → embedding)
  - Transformer decoder (embedding → MIDI events)
  - Trained with PPO (Proximal Policy Optimization)
```

**Training:**
```python
# Stage 1: Supervised learning (learns song)
base_model = train_supervised(song_midi)

# Stage 2: RL fine-tuning (learns to follow)
rl_model = train_rl(
    base_model=base_model,
    reward_function=compute_reward,
    num_episodes=100,  # 100 simulated performances
    max_steps_per_episode=1000  # ~4 minute song
)

def compute_reward(agent_midi, human_audio):
    # Synchronization: Are agent events aligned with human beats?
    sync_score = measure_beat_alignment(agent_midi, human_audio)

    # Musicality: Does agent play correct notes?
    music_score = measure_note_correctness(agent_midi, song_chords)

    # Dynamics: Does agent match human volume?
    dynamics_score = measure_dynamic_match(agent_midi, human_audio)

    # Weighted combination
    return 0.5*sync_score + 0.3*music_score + 0.2*dynamics_score
```

**Human-in-the-Loop Training:**
- User performs song with agent
- Agent records performance + user feedback ("that fill was great!" or "too busy")
- RL uses feedback as reward signal
- Agent improves over time with user

**Infrastructure:**
1. **Multi-agent coordination:** All instruments listen to same beat clock
2. **Dynamic mixing:** JUCE balances agent volumes based on user preferences
3. **Export:** Save agent performances as MIDI + audio stems
4. **Cloud sync:** (Optional) Share trained agents across devices

**Success Criteria:**
- ✅ Drums, bass, and keys playing together cohesively
- ✅ Agents adapt to tempo changes in real-time (<500ms reaction)
- ✅ Total system latency <20ms
- ✅ Professional-quality output (indistinguishable from session musicians)
- ✅ User can customize and improve agents through practice

---

## 8. Trade-Off Matrices

### 8.1 Synthesis Method Comparison

| Method | Latency | Quality | Flexibility | Cost | Performia Fit |
|--------|---------|---------|-------------|------|---------------|
| **VST Hosting** | ⭐⭐⭐⭐⭐ <5ms | ⭐⭐⭐⭐⭐ Professional | ⭐⭐⭐⭐⭐ User choice | Free-$500 plugins | **BEST** |
| **Sample Playback** | ⭐⭐⭐⭐⭐ <1ms | ⭐⭐⭐⭐ Realistic | ⭐⭐⭐ Fixed samples | 1-10GB storage | Good for drums |
| **Physical Modeling** | ⭐⭐⭐⭐ 2-10ms | ⭐⭐⭐ Can sound synthetic | ⭐⭐⭐⭐ Expressive | CPU intensive | Good for bass |
| **Neural Audio** | ⭐ 100ms+ | ⭐⭐⭐⭐ Novel sounds | ⭐⭐⭐⭐⭐ Unlimited | GPU required | NOT real-time |
| **MIDI → Synth** | ⭐⭐⭐⭐⭐ <5ms | ⭐⭐⭐ Depends on synth | ⭐⭐⭐⭐⭐ Standard | Varies | Fallback option |

**Recommendation:** **VST Hosting** for all instruments

### 8.2 Agent Intelligence Comparison

| Approach | Latency | Adaptability | Musical Quality | Training Effort | Performia Fit |
|----------|---------|--------------|-----------------|-----------------|---------------|
| **Pre-trained Transformer** | ⭐⭐⭐⭐ <10ms | ⭐⭐⭐ Good | ⭐⭐⭐⭐ Great | ⭐⭐⭐⭐⭐ None | **MVP** |
| **Fine-tuned Small Model** | ⭐⭐⭐⭐⭐ <5ms | ⭐⭐⭐⭐ Very good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Moderate | **Enhanced** |
| **Rule-based Only** | ⭐⭐⭐⭐⭐ <1ms | ⭐ Poor | ⭐⭐ Robotic | ⭐⭐⭐⭐⭐ None | Fallback only |
| **Hybrid (Rules+ML)** | ⭐⭐⭐⭐⭐ <8ms | ⭐⭐⭐⭐ Great | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐ Low | **BEST** |
| **RL-adapted** | ⭐⭐⭐⭐ <10ms | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐⭐⭐ Superb | ⭐⭐ High | **Production** |
| **Large Transformer** | ⭐⭐ 50ms+ | ⭐⭐⭐⭐⭐ Best | ⭐⭐⭐⭐⭐ Amazing | ⭐⭐ High | Too slow |

**Recommendation:** **Hybrid (Rules + Fine-tuned Small Transformer)** with **RL** in Phase 3

### 8.3 Communication Protocol Comparison

| Protocol | Latency | Bandwidth | Complexity | Flexibility | Performia Fit |
|----------|---------|-----------|------------|-------------|---------------|
| **OSC** | ⭐⭐⭐⭐⭐ ~1ms | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐ Simple | ⭐⭐⭐⭐⭐ Excellent | **PRIMARY** |
| **MIDI (Network)** | ⭐⭐⭐ 5-20ms | ⭐⭐⭐⭐⭐ Tiny | ⭐⭐⭐ Moderate | ⭐⭐⭐ Limited (7-bit) | Alternative |
| **WebSocket** | ⭐⭐ 10-50ms | ⭐⭐⭐ OK | ⭐⭐⭐ Moderate | ⭐⭐⭐⭐ Good | UI only |
| **Shared Memory** | ⭐⭐⭐⭐⭐ <0.1ms | ⭐⭐⭐⭐⭐ Unlimited | ⭐⭐ Complex | ⭐⭐ Local only | **HIGH-FREQ DATA** |
| **gRPC** | ⭐⭐⭐ 5-15ms | ⭐⭐⭐⭐ Efficient | ⭐⭐ Complex | ⭐⭐⭐⭐ Typed API | Overkill |

**Recommendation:** **OSC (control plane) + Shared Memory (data plane)**

### 8.4 Storage Solution Comparison

| Solution | Query Speed | Scalability | Complexity | Portability | Performia Fit |
|----------|-------------|-------------|------------|-------------|---------------|
| **SQLite** | ⭐⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐ 10K+ songs | ⭐⭐⭐⭐⭐ Zero setup | ⭐⭐⭐⭐⭐ Single file | **BEST** |
| **Filesystem (JSON)** | ⭐⭐ Slow search | ⭐⭐⭐ OK | ⭐⭐⭐⭐⭐ Simple | ⭐⭐⭐⭐⭐ Copy folder | Config files |
| **PostgreSQL** | ⭐⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐⭐ Unlimited | ⭐⭐ Server setup | ⭐⭐ Network DB | Future (cloud) |
| **Vector DB** | ⭐⭐⭐⭐ Fast (similarity) | ⭐⭐⭐⭐ Large | ⭐⭐⭐ Moderate | ⭐⭐⭐ Varies | Phase 2+ |
| **Redis** | ⭐⭐⭐⭐⭐ Fastest | ⭐⭐⭐ RAM limited | ⭐⭐⭐ Moderate | ⭐⭐ Volatile | Not needed |

**Recommendation:** **SQLite (metadata) + Filesystem (audio/MIDI) + ChromaDB (Phase 2, optional)**

---

## 9. Recommended Tech Stack

### 9.1 MVP (Phase 1) - Drum Agent

**Agent Intelligence:**
```
Language: Python 3.10+
ML Framework: TensorFlow 2.x (for Magenta models)
Models: Magenta GrooVAE (pre-trained)
Inference: TensorFlow CPU/GPU (no quantization yet)
```

**Communication:**
```
Protocol: OSC (Open Sound Control)
Python Library: python-osc
JUCE Module: juce_osc (built-in)
```

**Audio Synthesis:**
```
Framework: JUCE 7.x
Plugin Format: VST3, AU
Hosting: AudioPluginHost (JUCE built-in)
Free VST: MT Power Drumkit or Steven Slate Drums Free
```

**Storage:**
```
Database: SQLite 3
Python Library: sqlite3 (built-in)
File Format: JSON (Song Maps)
Audio Storage: Filesystem (WAV/MP3)
```

**Development Tools:**
```
Python IDE: VS Code + Python extension
C++ IDE: VS Code + C++ extension / Xcode (macOS)
Version Control: Git
Dependencies: pip (Python), CMake (JUCE)
```

### 9.2 Enhanced (Phase 2) - Song-Specific Agents

**New Components:**

**Source Separation:**
```
Library: Demucs v4 (Meta)
Installation: pip install demucs
Speed: 3-5 min per song (GPU), 10-20 min (CPU)
Quality: 9.20 dB SDR (state-of-the-art)
```

**Audio Transcription:**
```
Drums: Aubio (onset detection, beat tracking)
Bass: Crepe (pitch tracking) + Aubio (onsets)
Keys: BasicPitch (Spotify, multi-pitch transcription)
Installation: pip install aubio crepe basic-pitch
```

**Model Fine-Tuning:**
```
Training: TensorFlow 2.x (Magenta)
GPU: NVIDIA CUDA (GTX 1660+, RTX 3060 recommended)
Cloud Alternative: Google Colab (free GPU)
Training Time: 10-30 min per instrument
```

**Model Optimization:**
```
Format: ONNX (cross-platform)
Quantization: ONNX Runtime (INT8)
Inference: ONNX Runtime (CPU/GPU)
Model Size: 20-50MB (quantized)
```

### 9.3 Production (Phase 3) - Multi-Instrument + RL

**Additional Models:**
```
Bass: Performance RNN (Magenta) or Music Transformer
Keys: Coconet (Magenta) or custom Transformer
RL Framework: Stable Baselines 3 (PPO)
```

**Reinforcement Learning:**
```
Library: Stable Baselines 3
Algorithm: PPO (Proximal Policy Optimization)
Environment: Custom Gym environment (music performance)
Training: 100+ episodes (~10 hours practice sessions)
```

**Multi-Agent Coordination:**
```
Beat Clock: Shared memory (mmap) or OSC broadcast
Synchronization: Sub-millisecond precision
Agent Communication: Optional (agents can listen to each other)
```

**Advanced Storage (Optional):**
```
Vector DB: ChromaDB (embedded) or FAISS
Purpose: Song similarity search, agent learning
Embeddings: 2048-dim audio feature vectors
Model: Pre-trained audio embedding model (VGGish, etc.)
```

---

## 10. Architecture Diagrams

### 10.1 System Architecture (ASCII)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PERFORMIA SYSTEM ARCHITECTURE                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐        │
│  │  Living Chart  │  │  Blueprint     │  │  Library UI    │        │
│  │  (React/Vite)  │  │  View          │  │  (Song Search) │        │
│  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘        │
│          │                   │                    │                  │
│          └───────────────────┴────────────────────┘                  │
│                              │                                       │
│                         WebSocket                                    │
│                              │                                       │
└──────────────────────────────┼───────────────────────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        BACKEND LAYER (Python)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    AI AGENT ORCHESTRA                          │  │
│  ├───────────────────────────────────────────────────────────────┤  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │  │
│  │  │ Drums Agent  │  │ Bass Agent   │  │ Keys Agent   │       │  │
│  │  │ (GrooVAE)    │  │ (Perf RNN)   │  │ (Coconet)    │       │  │
│  │  │ 20M params   │  │ 30M params   │  │ 50M params   │       │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │  │
│  │         │                 │                  │                │  │
│  │         └─────────────────┴──────────────────┘                │  │
│  │                           │                                   │  │
│  │                    Hybrid Controller                          │  │
│  │               (Rules + ML Decision Fusion)                    │  │
│  │                           │                                   │  │
│  └───────────────────────────┼───────────────────────────────────┘  │
│                              │                                       │
│  ┌───────────────────────────┼───────────────────────────────────┐  │
│  │         AUDIO ANALYSIS    │      ORCHESTRATOR                 │  │
│  ├───────────────────────────┼───────────────────────────────────┤  │
│  │  • Beat Tracker           │  • Agent Coordinator              │  │
│  │  • Chord Detector         │  • Pattern Scheduler              │  │
│  │  • Melody Extractor       │  • Dynamic Controller             │  │
│  │  • Tempo Estimator        │  • MIDI Event Generator           │  │
│  └───────────────────────────┴───────────────────────────────────┘  │
│                              │                                       │
│                        OSC Sender                                    │
│                      (MIDI Events)                                   │
│                              │                                       │
└──────────────────────────────┼───────────────────────────────────────┘
                               │
                          OSC Protocol
                        UDP Port 9000
                               │
                               ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    AUDIO ENGINE LAYER (JUCE/C++)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                      OSC RECEIVER                              │  │
│  │              (Receives MIDI events from agents)                │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │                                       │
│  ┌───────────────────────────┼───────────────────────────────────┐  │
│  │                    MIDI ROUTER                                 │  │
│  │         (Routes events to appropriate plugins)                 │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │                                       │
│  ┌──────────────┬────────────┴────────────┬──────────────┐         │
│  │              │                         │              │          │
│  ↓              ↓                         ↓              ↓          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  Drums   │  │  Bass    │  │  Keys    │  │  Guitar  │           │
│  │  VST     │  │  VST     │  │  VST     │  │  VST     │           │
│  │ Plugin   │  │ Plugin   │  │ Plugin   │  │ Plugin   │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
│       │             │              │             │                  │
│       └─────────────┴──────────────┴─────────────┘                  │
│                              │                                       │
│  ┌───────────────────────────┼───────────────────────────────────┐  │
│  │                      AUDIO MIXER                               │  │
│  │             (Balances levels, applies effects)                 │  │
│  └───────────────────────────┬───────────────────────────────────┘  │
│                              │                                       │
│  ┌───────────────────────────┼───────────────────────────────────┐  │
│  │                    AUDIO OUTPUT                                │  │
│  │              (System audio device, <5ms buffer)                │  │
│  └───────────────────────────┴───────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        STORAGE LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────┐         ┌─────────────────────────────┐    │
│  │   SQLite Database  │         │      Filesystem             │    │
│  ├────────────────────┤         ├─────────────────────────────┤    │
│  │ • Songs metadata   │         │ • Audio stems (WAV)         │    │
│  │ • Agent configs    │         │ • Song Maps (JSON)          │    │
│  │ • Performance logs │         │ • Agent models (ONNX)       │    │
│  │ • Song features    │         │ • MIDI performances (.mid)  │    │
│  └────────────────────┘         └─────────────────────────────┘    │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │           ChromaDB (Optional - Phase 2)                      │    │
│  │         Song embeddings for similarity search                │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

                        LATENCY BUDGET
┌─────────────────────────────────────────────────────────────────────┐
│  Component                              Latency                      │
├─────────────────────────────────────────────────────────────────────┤
│  Audio input buffer                     2-5ms                        │
│  Python agent inference (INT8)          3-8ms                        │
│  OSC transmission (local UDP)           <1ms                         │
│  JUCE MIDI routing                      <1ms                         │
│  VST plugin processing                  2-5ms                        │
│  Audio output buffer                    2-5ms                        │
├─────────────────────────────────────────────────────────────────────┤
│  TOTAL END-TO-END LATENCY               10-25ms (Target: <20ms)     │
└─────────────────────────────────────────────────────────────────────┘
```

### 10.2 Agent Intelligence Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                  HYBRID AGENT INTELLIGENCE FLOW                      │
└─────────────────────────────────────────────────────────────────────┘

                         INPUTS
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ↓                  ↓                  ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Current Beat │  │ Current Chord│  │ Live Audio   │
│  Position    │  │  (from Song  │  │  Features    │
│              │  │   Map)       │  │ (dynamics)   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │
       └─────────────────┴──────────────────┘
                         │
                         ↓
             ┌───────────────────────┐
             │  RULES ENGINE (Fast)  │
             ├───────────────────────┤
             │ • Tempo constraints   │
             │ • Key/scale limits    │
             │ • Chord tones         │
             │ • Dynamic range       │
             │ • Time signature      │
             └───────────┬───────────┘
                         │
                         ↓
              ┌──────────────────────┐
              │  ML MODEL INFERENCE  │
              │  (3-8ms on GPU/CPU)  │
              ├──────────────────────┤
              │ Input: Beat context  │
              │ Model: Transformer   │
              │ Output: 5 candidates │
              └──────────┬───────────┘
                         │
                         ↓
              ┌──────────────────────┐
              │  CANDIDATE PATTERNS  │
              │  [P1, P2, P3, P4, P5]│
              └──────────┬───────────┘
                         │
                         ↓
              ┌──────────────────────┐
              │  RULES VALIDATION    │
              │  (Filter invalid)    │
              ├──────────────────────┤
              │ P1: ✓ Valid          │
              │ P2: ✗ Wrong notes    │
              │ P3: ✓ Valid          │
              │ P4: ✗ Too sparse     │
              │ P5: ✓ Valid          │
              └──────────┬───────────┘
                         │
                  Valid: [P1, P3, P5]
                         │
                         ↓
              ┌──────────────────────┐
              │   PATTERN RANKING    │
              │  (Musical heuristics)│
              ├──────────────────────┤
              │ P1: Score 0.92       │
              │ P3: Score 0.88       │
              │ P5: Score 0.75       │
              └──────────┬───────────┘
                         │
                  Select: P1 (highest)
                         │
                         ↓
              ┌──────────────────────┐
              │   HUMANIZATION       │
              │  (Micro-timing)      │
              ├──────────────────────┤
              │ • Timing ±5ms jitter │
              │ • Velocity ±3 MIDI   │
              │ • Swing feel         │
              └──────────┬───────────┘
                         │
                         ↓
              ┌──────────────────────┐
              │   FINAL MIDI OUTPUT  │
              │  (Expressive pattern)│
              └──────────┬───────────┘
                         │
                         ↓
                    OSC SENDER
                         │
                         ↓
                   JUCE → VST
                         │
                         ↓
                  🎵 AUDIO OUTPUT
```

### 10.3 Training Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│              SONG-SPECIFIC AGENT TRAINING PIPELINE                   │
└─────────────────────────────────────────────────────────────────────┘

USER ACTION: Add song to library
         │
         ↓
┌─────────────────────┐
│   Upload Audio      │  full_mix.wav (stereo, 3-5 minutes)
│   (Full Mix)        │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Source Separation  │  Demucs v4 (3-5 min on GPU)
│  (Demucs)           │
└──────────┬──────────┘
           │
           ├────┬────┬────┬────┐
           ↓    ↓    ↓    ↓    ↓
        drums bass vocals keys other
         .wav .wav  .wav  .wav .wav
           │
┌──────────┴──────────────────────────────────────────────┐
│                                                          │
│  PARALLEL TRANSCRIPTION (2-5 min total)                 │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Drums      │  │   Bass       │  │   Keys       │  │
│  │  (Aubio)     │  │  (Crepe)     │  │ (BasicPitch) │  │
│  │              │  │              │  │              │  │
│  │ • Onsets     │  │ • Pitch      │  │ • Multi-pitch│  │
│  │ • Beats      │  │ • Onsets     │  │ • Onsets     │  │
│  │ • Classify   │  │ • Duration   │  │ • Chords     │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                  │          │
│         ↓                 ↓                  ↓          │
│    drums.mid         bass.mid           keys.mid       │
│                                                          │
└──────────────────────────────────────────────────────────┘
           │
           ↓
┌─────────────────────┐
│  Feature Extraction │
│  (Librosa)          │
├─────────────────────┤
│ • Chords            │
│ • Beats             │
│ • Tempo             │
│ • Key               │
│ • Structure         │
└──────────┬──────────┘
           │
           ↓
    features.json
           │
           ↓
┌──────────────────────────────────────────────────────────┐
│                                                           │
│  PARALLEL FINE-TUNING (10-30 min each on GPU)            │
│                                                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────┐ │
│  │ Drums Agent    │  │ Bass Agent     │  │ Keys Agent │ │
│  ├────────────────┤  ├────────────────┤  ├────────────┤ │
│  │ Base: GrooVAE  │  │ Base: Perf RNN │  │ Base:      │ │
│  │ Train: drums   │  │ Train: bass    │  │ Coconet    │ │
│  │ .mid           │  │ .mid           │  │ Train: keys│ │
│  │                │  │                │  │ .mid       │ │
│  │ Epochs: 5000   │  │ Epochs: 5000   │  │ Epochs:    │ │
│  │ LR: 1e-4       │  │ LR: 1e-4       │  │ 5000       │ │
│  └────────┬───────┘  └────────┬───────┘  └──────┬─────┘ │
│           │                   │                  │       │
│           ↓                   ↓                  ↓       │
│     drums_ft.pt         bass_ft.pt         keys_ft.pt   │
│                                                           │
└───────────────────────────────────────────────────────────┘
           │
           ↓
┌─────────────────────┐
│  Model Optimization │
├─────────────────────┤
│ 1. Export to ONNX   │
│ 2. Quantize to INT8 │
│ 3. Test inference   │
└──────────┬──────────┘
           │
           ↓
    ┌──────┴──────┬──────────┐
    ↓             ↓          ↓
drums.onnx   bass.onnx   keys.onnx
 (40MB)       (60MB)      (100MB)
    │             │          │
    └──────┬──────┴──────────┘
           │
           ↓
┌─────────────────────┐
│  Store in Database  │
├─────────────────────┤
│ INSERT INTO         │
│ agent_configs       │
│ (song_id,           │
│  instrument,        │
│  model_path,        │
│  config_json)       │
└──────────┬──────────┘
           │
           ↓
    ✅ READY TO PERFORM

    Load models:
    agents = {
      'drums': load('drums.onnx'),
      'bass': load('bass.onnx'),
      'keys': load('keys.onnx')
    }

    Real-time inference: <10ms
```

---

## 11. References and Citations

### Academic Papers

1. **RL-Duet: Online Music Accompaniment Generation Using Deep Reinforcement Learning**
   AAAI Conference on Artificial Intelligence, 2020
   https://ojs.aaai.org/index.php/AAAI/article/view/5413

2. **ReaLJam: Real-Time Human-AI Music Jamming with Reinforcement Learning-Tuned Transformers**
   CHI Conference on Human Factors in Computing Systems, 2025
   https://arxiv.org/abs/2502.21267

3. **SongDriver: Real-time Music Accompaniment Generation without Logical Latency nor Exposure Bias**
   ACM International Conference on Multimedia, 2022
   https://dl.acm.org/doi/abs/10.1145/3503161.3548368

4. **Action-sound Latency and the Perceived Quality of Digital Musical Instruments**
   Music Perception, 2018
   https://online.ucpress.edu/mp/article/36/1/109/92063

5. **Local deployment of large-scale music AI models on commodity hardware**
   ArXiv preprint, 2024
   https://arxiv.org/abs/2411.09625

### Technical Documentation

6. **Google Magenta - Performance RNN**
   https://magenta.tensorflow.org/performance-rnn

7. **Google Magenta - GrooVAE**
   https://magenta.tensorflow.org/groovae

8. **Google Magenta - Music Transformer**
   https://magenta.tensorflow.org/music-transformer

9. **Meta MusicGen Documentation**
   https://github.com/facebookresearch/audiocraft

10. **Demucs v4 - Music Source Separation**
    https://github.com/facebookresearch/demucs

11. **JUCE Framework Documentation**
    https://juce.com/learn/documentation

12. **OSC (Open Sound Control) Specification**
    https://ccrma.stanford.edu/groups/osc/index.html

### Datasets

13. **Lakh MIDI Dataset**
    174K multi-track MIDI files
    https://colinraffel.com/projects/lmd/

14. **Groove MIDI Dataset**
    Professional drummer performances
    https://magenta.tensorflow.org/datasets/groove

15. **MAESTRO Dataset**
    Classical piano performances
    https://magenta.tensorflow.org/datasets/maestro

### Tools and Libraries

16. **ONNX Runtime**
    https://onnxruntime.ai/

17. **Aubio - Audio Labeling**
    https://aubio.org/

18. **Crepe - Monophonic Pitch Tracking**
    https://github.com/marl/crepe

19. **BasicPitch - Audio to MIDI**
    https://github.com/spotify/basic-pitch

20. **SQLite Documentation**
    https://www.sqlite.org/

### Industry Examples

21. **Logic Pro - AI Session Musicians**
    Apple announcement, May 2024
    https://www.apple.com/newsroom/2024/05/logic-pro-takes-music-making-to-the-next-level-with-new-ai-features/

22. **Yamaha AI Music Ensemble**
    https://www.yamaha.com/en/tech-design/research/technologies/muens/

### Blog Posts and Tutorials

23. **Hugging Face Audio Course - Fine-tuning for Music Classification**
    https://huggingface.co/learn/audio-course/en/chapter4/fine-tuning

24. **Beets Music Library Management - SQLite Performance**
    https://beets.io/blog/sqlite-performance.html

---

## 12. Appendix: Quick Reference

### Key Metrics Summary

| Metric | Target | Rationale |
|--------|--------|-----------|
| **Total Latency** | <20ms | Professional quality (vocalists need <10ms) |
| **AI Inference** | <10ms | Fits within latency budget |
| **Model Size** | <100MB | Fast loading, low memory |
| **Training Time** | <30 min/song | Acceptable user wait time |
| **Accuracy** | >90% note correctness | Musical quality threshold |

### Technology Choices at a Glance

| Component | Technology | Why |
|-----------|-----------|-----|
| **First Instrument** | Drums | Simpler musicality, mature models, high user value |
| **ML Framework** | TensorFlow + Magenta | Pre-trained models, proven for music |
| **Inference Engine** | ONNX Runtime | Cross-platform, quantization support |
| **Audio Synthesis** | VST Hosting (JUCE) | Professional quality, user choice, low latency |
| **Communication** | OSC + Shared Memory | Flexible control + ultra-low latency data |
| **Storage** | SQLite + Filesystem | Zero config, fast queries, portable |
| **Training** | Pre-trained + Fine-tuning | Best quality-effort trade-off |

### Phase Roadmap Summary

| Phase | Timeline | Key Deliverable | Success Metric |
|-------|----------|-----------------|----------------|
| **MVP** | 2-3 weeks | Generic drum agent | <20ms latency, works with user VST |
| **Enhanced** | 4-6 weeks | Song-specific agents | Captures original feel |
| **Production** | 8-12 weeks | Multi-instrument + RL | Full band, adaptive performance |

### Critical Dependencies

**MVP:**
- Python 3.10+, TensorFlow 2.x
- JUCE 7.x, VST3 SDK
- python-osc, juce_osc
- Free drum VST (MT Power Drumkit)

**Enhanced:**
- Demucs v4, Aubio, Crepe, BasicPitch
- ONNX Runtime, CUDA (optional)
- SQLite 3

**Production:**
- Stable Baselines 3 (RL)
- ChromaDB or FAISS (similarity search)
- Multiple VST plugins

---

## Conclusion

This research provides Performia with a comprehensive roadmap for building world-class AI music agents. The recommended approach—starting with a **hybrid drums agent** using **pre-trained Magenta models**, **VST synthesis**, **OSC communication**, and **SQLite storage**—balances technical feasibility, professional quality, and rapid development.

The three-phase implementation plan allows for incremental value delivery:
1. **MVP** proves the concept and delivers immediate user value
2. **Enhanced** adds song-specific fine-tuning for authentic performance
3. **Production** scales to full band with real-time adaptation

All technical choices are grounded in current research, with latency budgets meeting professional requirements (<20ms) and clear paths to optimization. The architecture is designed for local deployment (no cloud dependency), privacy, and offline capability.

**Next Steps:**
1. Review this document with the development team
2. Set up development environment (Python + JUCE)
3. Begin MVP implementation with drums agent
4. Test latency and quality with real musicians
5. Iterate based on user feedback

Performia is well-positioned to create a revolutionary music performance system that combines the expressiveness of human musicians with the consistency and adaptability of AI agents.

---

**Document Version:** 1.0
**Last Updated:** October 1, 2025
**Contact:** Research Agent via Performia Development Team
