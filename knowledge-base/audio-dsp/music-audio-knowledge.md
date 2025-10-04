# Music & Audio Knowledge Base for AI Agents

**Purpose:** This document provides music-specific knowledge for AI development agents working on Performia's audio analysis pipeline.

**Last Updated:** October 4, 2025

---

## 🎵 Music Theory Fundamentals

### Chord Construction
```
Major Triads: Root + Major 3rd + Perfect 5th
  - C major: C, E, G
  - G major: G, B, D

Minor Triads: Root + Minor 3rd + Perfect 5th
  - Am: A, C, E
  - Em: E, G, B

7th Chords: Add 7th interval
  - Cmaj7: C, E, G, B (major 7th)
  - C7: C, E, G, Bb (dominant 7th)
  - Cm7: C, Eb, G, Bb (minor 7th)

Extensions: 9th, 11th, 13th intervals
  - C9, C11, C13, etc.
```

### Common Chord Progressions
```
I-IV-V-I (e.g., C-F-G-C) - Most common in pop/rock
I-V-vi-IV (e.g., C-G-Am-F) - "Axis of Awesome" progression
ii-V-I (e.g., Dm-G-C) - Jazz standard
I-vi-IV-V (e.g., C-Am-F-G) - 50s progression
```

### Key Signatures
```
Circle of Fifths (Major Keys):
C (0♯/♭) → G (1♯) → D (2♯) → A (3♯) → E (4♯) → B (5♯) → F♯ (6♯)
C (0♯/♭) → F (1♭) → Bb (2♭) → Eb (3♭) → Ab (4♭) → Db (5♭) → Gb (6♭)

Relative Minors:
C major ↔ A minor
G major ↔ E minor
F major ↔ D minor
```

### Song Structure Terms
```
Intro - Opening section (4-8 bars)
Verse - Story/narrative section (8-16 bars)
Pre-Chorus - Build-up to chorus (4-8 bars)
Chorus - Main hook/refrain (8-16 bars)
Bridge - Contrasting section (8-16 bars)
Outro/Coda - Ending section (4-8 bars)
```

---

## 🔊 Audio Analysis Best Practices

### Librosa: Critical Parameters

#### Beat Tracking
```python
# BASIC (current implementation):
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

# IMPROVED (more accurate for complex music):
onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
tempo, beats = librosa.beat.beat_track(
    onset_envelope=onset_env,
    sr=sr,
    start_bpm=120,  # Initial tempo estimate
    tightness=100,  # Higher = more strict tempo adherence
    trim=True,      # Remove silence at start/end
    bpm=None,       # Let it detect tempo
    prior=None      # No prior tempo knowledge
)

# For songs with tempo changes:
dtempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr, aggregate=None)
# Returns tempo over time, not single value
```

#### Chord Detection
```python
# BASIC (less accurate):
chroma = librosa.feature.chroma_stft(y=y, sr=sr)

# IMPROVED (harmonic-percussive separation first):
y_harmonic, y_percussive = librosa.effects.hpss(y)
chroma = librosa.feature.chroma_cqt(
    y=y_harmonic,     # Use only harmonic component
    sr=sr,
    hop_length=512,   # Time resolution
    norm=2,           # L2 normalization
    threshold=0.0     # No amplitude threshold
)

# Even better: Use CQT (Constant-Q Transform) instead of STFT
# CQT is better for music because it uses logarithmic frequency spacing
chroma_cqt = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
```

#### Key Detection (Krumhansl-Schmuckler)
```python
# Extract chroma features
chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

# Average over time to get key profile
chroma_mean = np.mean(chroma, axis=1)

# Krumhansl-Schmuckler key profiles (correlation method)
major_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
minor_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

# Correlate with all 24 keys, pick highest correlation
```

#### Structure Detection
```python
# Method 1: Novelty-based (current)
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
novelty = librosa.onset.onset_strength(S=librosa.power_to_db(mfcc))
boundaries = librosa.segment.agglomerative(mfcc, k=8)  # 8 segments

# Method 2: Self-similarity matrix
S = librosa.feature.melspectrogram(y=y, sr=sr)
R = librosa.segment.recurrence_matrix(S, mode='affinity')
boundaries = librosa.segment.agglomerative(R, k=None)  # Auto-detect

# Method 3: Laplacian segmentation (best for verse/chorus)
boundaries = librosa.segment.agglomerative(S, k=None, clusterer='laplacian')
```

#### Melody Extraction
```python
# Use pyin (probabilistic YIN) for pitch detection
f0, voiced_flag, voiced_probs = librosa.pyin(
    y=y,
    fmin=librosa.note_to_hz('C2'),  # Lowest expected pitch
    fmax=librosa.note_to_hz('C7'),  # Highest expected pitch
    sr=sr,
    frame_length=2048,
    win_length=None,
    hop_length=512,
    n_thresholds=100,
    beta_parameters=(2, 18),
    boltzmann_parameter=2,
    resolution=0.1,
    max_transition_rate=35.92,
    switch_prob=0.01,
    no_trough_prob=0.01
)

# Filter out unvoiced regions
f0_filtered = f0[voiced_flag]
```

---

## 🎹 Music Information Retrieval (MIR) Standards

### Tempo Ranges
```
Largo: 40-60 BPM (very slow)
Adagio: 60-80 BPM (slow)
Andante: 80-100 BPM (walking pace)
Moderato: 100-120 BPM (moderate)
Allegro: 120-140 BPM (fast)
Presto: 140-200 BPM (very fast)

Common Pop/Rock: 90-140 BPM
EDM/Dance: 120-140 BPM
Hip-Hop: 60-100 BPM (often half-time feel)
```

### Time Signatures
```
4/4 - Common time (most pop/rock)
3/4 - Waltz time
6/8 - Compound duple (feels like 2 beats)
12/8 - Compound quadruple (shuffle feel)
5/4 - Asymmetric (prog rock, jazz)
7/8 - Complex asymmetric
```

### Frequency Ranges
```
Sub-bass: 20-60 Hz
Bass: 60-250 Hz
Low Mids: 250-500 Hz
Mids: 500-2,000 Hz
High Mids: 2,000-4,000 Hz
Presence: 4,000-6,000 Hz
Brilliance: 6,000-20,000 Hz

Vocal Range:
  Bass: E2-E4
  Tenor: C3-C5
  Alto: F3-F5
  Soprano: C4-C6
```

---

## 🛠️ Essential Libraries & When to Use Them

### Librosa (Primary - Always Use)
```
✅ USE FOR:
- Beat tracking (librosa.beat.beat_track)
- Tempo estimation (librosa.beat.tempo)
- Onset detection (librosa.onset)
- Chroma features (librosa.feature.chroma_*)
- MFCC features (librosa.feature.mfcc)
- Spectrograms (librosa.feature.melspectrogram)
- Harmonic-percussive separation (librosa.effects.hpss)
- Time stretching (librosa.effects.time_stretch)
- Pitch shifting (librosa.effects.pitch_shift)

❌ DON'T USE FOR:
- Real-time processing (too slow)
- Chord recognition (basic templates only)
- Source separation (use Demucs)
```

### Essentia (Alternative - Evaluate)
```
✅ USE FOR:
- Chord detection (better pre-trained models)
- Key detection (superior algorithms)
- Mood/genre classification
- Rhythm analysis

WHEN TO PREFER OVER LIBROSA:
- Need higher chord accuracy
- Want pre-trained ML models
- Doing genre classification
```

### Music21 (Theory Validation)
```
✅ USE FOR:
- Validating chord progressions
- Key analysis
- Roman numeral analysis
- MIDI conversion
- Music notation

❌ DON'T USE FOR:
- Audio analysis (it's symbolic music)
- Real-time processing
```

### Madmom (Advanced Beat Tracking)
```
✅ USE FOR:
- Complex rhythm detection
- Multi-tempo tracking
- Downbeat detection
- Bar tracking

WHEN TO PREFER OVER LIBROSA:
- Polyrhythmic music
- Tempo changes mid-song
- Need downbeat accuracy
```

### Demucs (Source Separation - Already Using)
```
✅ USE FOR:
- Vocals/instrumental separation
- 4-stem separation (vocals, drums, bass, other)
- Improving chord detection (use bass stem)
- Improving melody extraction (use vocal stem)

CURRENT IMPLEMENTATION: ✅
Location: backend/src/services/separation/main.py
Model: htdemucs (hybrid transformer)
```

### Whisper (ASR - Already Using)
```
✅ USE FOR:
- Speech-to-text (lyrics transcription)
- Word-level timestamps
- Multi-language support

CURRENT IMPLEMENTATION: ✅
Location: backend/src/services/asr/main.py
Model: OpenAI Whisper
```

---

## 📊 Performance Benchmarks

### Processing Time Targets
```
3-minute song should complete in <30 seconds total

Service breakdown (target times):
- Separation (Demucs): ~7s (23%)
- ASR (Whisper): ~5s (17%)
- Beats/Key: ~2s (7%)
- Chords: ~3s (10%)
- Melody/Bass: ~2s (7%)
- Structure: ~1s (3%)
- Packager: <1s (3%)
- Overhead: ~9s (30%)

Optimization priorities:
1. Demucs (biggest bottleneck - GPU helps)
2. ASR (use Whisper tiny/base for faster processing)
3. Chords (optimize chord templates)
```

### Accuracy Targets
```
Beat Detection: 95%+ (F1 score)
Tempo Estimation: ±5 BPM
Chord Recognition: 85%+ (frame-level)
Key Detection: 90%+ (song-level)
Structure Boundaries: 70%+ (within 2 seconds)
Melody F0: 80%+ (voiced frames)
ASR Word Error Rate: <10%
```

---

## 🚨 Common Pitfalls & How to Avoid

### Pitfall 1: Using Default Parameters
```python
# ❌ BAD (default parameters often suboptimal):
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

# ✅ GOOD (tuned for music analysis):
onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
tempo, beats = librosa.beat.beat_track(
    onset_envelope=onset_env,
    sr=sr,
    start_bpm=120,
    tightness=100
)
```

### Pitfall 2: Ignoring Harmonic-Percussive Separation
```python
# ❌ BAD (drums interfere with chord detection):
chroma = librosa.feature.chroma_stft(y=y, sr=sr)

# ✅ GOOD (remove percussion first):
y_harm, y_perc = librosa.effects.hpss(y)
chroma = librosa.feature.chroma_cqt(y=y_harm, sr=sr)
```

### Pitfall 3: Wrong Frequency Resolution
```python
# ❌ BAD (STFT has linear frequency spacing):
chroma = librosa.feature.chroma_stft(y=y, sr=sr)

# ✅ GOOD (CQT has logarithmic spacing, better for music):
chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
```

### Pitfall 4: Not Using Stems for Analysis
```python
# ❌ BAD (analyzing full mix):
chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

# ✅ GOOD (use separated bass stem if available):
if os.path.exists('bass.wav'):
    y_bass, sr = librosa.load('bass.wav')
    chroma = librosa.feature.chroma_cqt(y=y_bass, sr=sr)
```

### Pitfall 5: Ignoring Silence/Noise
```python
# ❌ BAD (silence at start/end throws off beat detection):
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

# ✅ GOOD (trim silence first):
y_trimmed, _ = librosa.effects.trim(y, top_db=20)
tempo, beats = librosa.beat.beat_track(y=y_trimmed, sr=sr)
```

---

## 📚 Reference Resources

### Official Documentation
```
Librosa: https://librosa.org/doc/latest/
Essentia: https://essentia.upf.edu/documentation/
Music21: https://web.mit.edu/music21/doc/
Madmom: https://madmom.readthedocs.io/
Demucs: https://github.com/facebookresearch/demucs
Whisper: https://github.com/openai/whisper
```

### Research Papers (State-of-the-Art)
```
Beat Tracking:
- "Joint Beat and Downbeat Tracking with Recurrent Neural Networks" (Böck et al., 2016)
- ISMIR proceedings: https://ismir.net/resources/

Chord Recognition:
- "Automatic Chord Estimation from Audio" (McVicar et al., 2014)
- "Deep Chroma Extraction" (Korzeniowski & Widmer, 2016)

Structure Analysis:
- "Structural Segmentation of Musical Audio" (Paulus et al., 2010)
```

### Music Theory
```
musictheory.net - Free online lessons
Hooktheory - Chord progression database
Wikipedia: List of chord progressions
```

---

## 🎯 Agent Guidelines

### When Working on Audio Services

**ALWAYS:**
1. Use harmonic-percussive separation for chord/melody tasks
2. Use CQT instead of STFT for chroma features
3. Trim silence before beat detection
4. Use separated stems when available (from Demucs)
5. Validate output with music theory (via music21)
6. Benchmark against test set after changes
7. Document parameter choices in code comments

**NEVER:**
8. Use default librosa parameters without justification
9. Assume 4/4 time signature
10. Ignore genre-specific characteristics
11. Skip validation against known-good test cases
12. Commit code without testing on real audio files

### When Improving Accuracy

**Priority order:**
1. Use better algorithms (CQT vs STFT)
2. Pre-process audio (HPSS, trim, normalize)
3. Use separated stems (Demucs output)
4. Tune parameters (onset strength, beat tightness)
5. Post-process results (smooth, validate)
6. Only then consider ML/training

### When Optimizing Performance

**Check in order:**
1. Profile to find bottleneck
2. Use faster librosa functions (if available)
3. Reduce audio sample rate if acceptable
4. Parallel processing (if independent tasks)
5. GPU acceleration (Demucs, Whisper)
6. Caching (if same file analyzed multiple times)

---

## ✅ Checklist for Audio Code Changes

Before committing changes to audio services:

- [ ] Tested on at least 10 diverse songs
- [ ] Compared accuracy with previous version
- [ ] Documented why parameters were chosen
- [ ] Added/updated unit tests
- [ ] Profiled performance impact
- [ ] Updated this knowledge base if discovered new insights
- [ ] Validated output with music theory (if applicable)
- [ ] Checked edge cases (silence, noise, tempo changes)

---

**End of Music & Audio Knowledge Base**

*For AI agents: Use this as authoritative reference when working on Performia's audio analysis pipeline.*
