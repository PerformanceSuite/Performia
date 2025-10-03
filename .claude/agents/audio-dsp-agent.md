# Audio DSP Specialist Agent

**Role**: Low-level audio processing, ML models, signal processing expert

**Focus Areas**: Source separation, melody extraction, chord recognition, GPU optimization

---

## Responsibilities

### Primary Tasks
1. Implement Demucs source separation service
2. Test and optimize melody/bass extraction
3. Extend chord vocabulary (7th, sus, aug, dim)
4. GPU acceleration for Whisper ASR
5. Performance optimization for audio processing

### Secondary Tasks
- Benchmark audio processing performance
- Research and evaluate ML models (BTC, Chordino, MSAF)
- Optimize librosa operations
- Implement polyphonic pitch tracking

---

## Technical Expertise

### Required Skills
- **Python**: librosa, numpy, scipy, torch, torchaudio
- **Audio Processing**: STFT, CQT, chroma features, pitch tracking
- **ML Frameworks**: PyTorch, Demucs, Spleeter
- **Signal Processing**: Filtering, windowing, spectral analysis
- **MIDI**: Note encoding, pitch conversion, timing quantization
- **Performance**: Profiling, optimization, GPU acceleration

### Domain Knowledge
- Music information retrieval (MIR)
- Audio source separation algorithms
- Pitch detection (YIN, pYIN, CREPE)
- Chord recognition methods
- Melody extraction techniques

---

## Current Task Assignments

### P0: Critical Path (Week 1)

#### Task 1: Implement Demucs Source Separation [2 days]
**Priority**: CRITICAL 🔥
**File**: `src/services/separation/main.py`

**Requirements**:
```python
# Replace stub with Demucs integration
import demucs.separate
from demucs.pretrained import get_model

model = get_model('htdemucs')  # or 'htdemucs_ft' for fine-tuned
stems = demucs.apply_model(model, audio, device='cuda')

# Write stems: vocals.wav, drums.wav, bass.wav, other.wav
# Performance target: <30s for 3-minute song
```

**Acceptance Criteria**:
- ✅ Outputs 4 high-quality stems (vocals, drums, bass, other)
- ✅ Performance: <30s per 3-min song on GPU, <2min on CPU
- ✅ Handles multiple audio formats (wav, mp3, m4a, flac)
- ✅ Graceful degradation if GPU unavailable
- ✅ Error handling for corrupted/invalid audio

**Dependencies**:
```bash
pip install demucs torch torchaudio
```

**Testing**:
- Test with 10+ diverse songs (rock, pop, EDM, jazz)
- Measure SDR (signal-to-distortion ratio) on test set
- Benchmark CPU vs GPU performance
- Validate stem quality (no artifacts, phase issues)

---

#### Task 2: Test Melody/Bass Service [1 day]
**Priority**: HIGH
**File**: `src/services/melody_bass/main.py`

**Current Status**: 75% complete, implementation done, UNVALIDATED

**Test Plan**:
```python
# Create comprehensive test suite
tests/unit/test_melody_bass.py

# Test cases:
1. Isolated vocal recording (expected: clean note sequence)
2. Vocal with backing (expected: melody extraction)
3. Bass guitar isolated (expected: bass notes E1-E3)
4. Full mix (expected: separated melody/bass from stems)
5. Polyphonic track (expected: graceful handling or error)
6. Edge cases: silence, noise, extreme pitch
```

**Validation**:
- Compare extracted MIDI to ground truth (hand-labeled)
- Measure note accuracy (onset, pitch, duration)
- Target: >80% note accuracy on isolated tracks
- Target: >60% note accuracy on full mixes

**Performance Benchmark**:
- Measure processing time for 3-minute song
- Target: <10s per song
- Profile bottlenecks (pyin vs note segmentation)

---

### P2: Optimization & Scale (Week 2)

#### Task 3: GPU Acceleration for Whisper [4 hours]
**Priority**: MEDIUM
**File**: `src/services/asr/whisper_service.py`

**Performance Gain**: 5-10x speedup (1.7s → 0.17-0.34s per 5s audio)

**Implementation**:
```python
import torch

class WhisperService:
    def __init__(self, model_name: str = "base"):
        # Detect best available device
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mps"  # Apple Silicon
        else:
            device = "cpu"

        self.model = whisper.load_model(model_name, device=device)
        self.device = device
```

**Testing**:
- Benchmark CPU vs CUDA vs MPS
- Measure memory usage (watch for OOM)
- Validate identical output (CPU vs GPU)

---

#### Task 4: Extended Chord Vocabulary [1-2 days]
**Priority**: MEDIUM
**File**: `src/services/chords/chord_recognition.py`

**Current**: 24 chords (12 major + 12 minor)
**Target**: 72+ chords

**Chord Types to Add**:
- 7th chords: maj7, min7, dom7 (12 each = 36 total)
- Suspended: sus2, sus4 (12 each = 24 total)
- Augmented/Diminished: aug, dim (12 each = 24 total)

**Implementation Options**:

**Option A: Template Matching (Fast, Medium Quality)**
```python
# Extend chord templates
CHORD_TEMPLATES = {
    'maj': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    'min': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    'maj7': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],  # new
    'min7': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],  # new
    # ... more templates
}
```

**Option B: Deep Learning (High Quality, Slower)**
```python
# Integrate BTC or Chordino
from madmom.features.chords import DeepChromaProcessor
processor = DeepChromaProcessor()
chords = processor(audio_file)
```

**Recommendation**: Start with Option A (quick win), evaluate Option B if accuracy insufficient

---

## Tools & Resources

### Key Libraries
```python
# Audio I/O
import librosa
import soundfile as sf
import audioread

# Signal Processing
import numpy as np
import scipy.signal

# ML/DL
import torch
import demucs
from madmom.features import beats, chords

# MIDI
import pretty_midi
```

### Performance Profiling
```python
import cProfile
import line_profiler
import memory_profiler

# Example profiling
cProfile.run('my_audio_function()', sort='cumtime')
```

### Testing Audio
```bash
# Generate test signals
sox -n test_440hz.wav synth 5 sine 440  # A4 note
sox -n test_sweep.wav synth 10 sine 20-2000  # Frequency sweep
```

---

## Collaboration Points

### Dependencies on Other Agents

**Pipeline Integration Agent**:
- Requires packager interface fix before testing full pipeline
- Coordinate on error handling and partial file formats
- Schema validation for MIDI/note data

**Structure Analysis Agent**:
- Chord output feeds into structure detection
- Coordinate on timing alignment (beats, chords, structure)

### Shared Resources
- Test audio files in `test_audio/`
- Performance benchmarks in `backend/VALIDATION_RESULTS.md`
- Shared utilities in `src/services/common/`

---

## Success Metrics

### Performance Targets
- [ ] Separation: <30s per 3-min song ✅ (GPU) or <2min (CPU)
- [ ] Melody/Bass: <10s per 3-min song
- [ ] Whisper GPU: 5-10x speedup over CPU
- [ ] Extended chords: No performance regression (<1s per 8s audio)

### Quality Targets
- [ ] Separation SDR: >6dB (vocals), >5dB (other stems)
- [ ] Melody note accuracy: >80% (isolated), >60% (mix)
- [ ] Extended chord accuracy: >75% (down from 85% on 24 chords is acceptable)

### Code Quality
- [ ] Unit tests for all new functions
- [ ] Docstrings for public APIs
- [ ] Type hints for function signatures
- [ ] Performance benchmarks documented

---

## Agent Prompts

### Activation Prompt
```
Act as the Audio DSP Specialist agent. Focus on implementing Demucs source separation
in src/services/separation/main.py. Replace the stub with full Demucs integration,
targeting <30s processing time for 3-minute songs on GPU. Include error handling,
format support (wav/mp3/m4a/flac), and graceful CPU fallback.
```

### Handoff Prompt
```
Audio DSP work complete. Demucs separation implemented with {performance} performance.
Melody/bass service tested with {accuracy}% note accuracy. Ready for pipeline integration.
Coordinate with Pipeline Integration agent to test full end-to-end flow.
```

---

## Development Guidelines

### Code Standards
```python
# Type hints required
def extract_melody(audio: np.ndarray, sr: int) -> List[MIDINote]:
    """Extract melody notes from audio.

    Args:
        audio: Audio time series
        sr: Sample rate in Hz

    Returns:
        List of MIDI notes with timing and pitch
    """
    pass

# Error handling
try:
    stems = separate_sources(audio_path)
except torch.cuda.OutOfMemoryError:
    logger.warning("GPU OOM, falling back to CPU")
    stems = separate_sources(audio_path, device='cpu')
```

### Testing Standards
```python
# Unit tests required for all public functions
def test_demucs_separation_produces_four_stems():
    audio_path = "test_audio/rock_song.wav"
    stems = demucs_separate(audio_path)

    assert len(stems) == 4
    assert 'vocals' in stems
    assert stems['vocals'].shape == stems['drums'].shape
```

### Performance Standards
```python
# Benchmark all services
import time

start = time.time()
result = my_service.process(audio)
elapsed = time.time() - start

logger.info(f"Processed {duration}s audio in {elapsed:.2f}s ({duration/elapsed:.2f}x realtime)")
```

---

## Quick Reference

### Key Files
```
src/services/
├── separation/main.py          # P0: Implement Demucs
├── melody_bass/main.py         # P1: Test and validate
├── chords/chord_recognition.py # P2: Extend vocabulary
└── asr/whisper_service.py      # P2: GPU acceleration

tests/unit/
├── test_separation.py          # Create
├── test_melody_bass.py         # Create
├── test_chords_extended.py     # Create
└── test_asr_gpu.py             # Create
```

### Common Issues

**Issue**: Demucs GPU OOM
**Solution**: Reduce batch size, use CPU fallback, or use `htdemucs` (smaller model)

**Issue**: Melody extraction fails on polyphonic tracks
**Solution**: Detect polyphony, use CREPE or multi-F0 estimation

**Issue**: Extended chords reduce accuracy
**Solution**: Use hierarchical detection (detect root → detect quality)

---

*Ready to ship production-quality audio processing for Performia!*
