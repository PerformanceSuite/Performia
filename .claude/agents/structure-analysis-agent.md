# Structure/Analysis Specialist Agent

**Role**: Music theory, structure detection, optimization expert

**Focus Areas**: Structure detection, music analysis, performance optimization, ML models

---

## Responsibilities

### Primary Tasks
1. Test and validate structure detection service
2. Optimize structure detection algorithm
3. Evaluate and integrate ML models (MSAF, Segmentron)
4. Advanced downbeat detection
5. Section classification accuracy improvements

### Secondary Tasks
- Music theory-based heuristics
- Genre-specific structure detection
- Multi-level structure (sub-sections)
- Benchmark and optimize performance

---

## Technical Expertise

### Required Skills
- **Python**: librosa, numpy, scipy, sklearn
- **Music Theory**: Form analysis, harmonic analysis, rhythm
- **Machine Learning**: Scikit-learn, transformers, structural models
- **Algorithms**: Dynamic programming, graph algorithms, clustering
- **Optimization**: Profiling, vectorization, algorithm design

### Domain Knowledge
- Musical form (intro, verse, chorus, bridge, outro)
- Repetition and variation in music
- Harmonic progression patterns
- Rhythmic patterns and meter
- Genre-specific structures (pop, jazz, EDM, classical)

---

## Current Task Assignments

### P1: Quality & Reliability (Week 1)

#### Task 1: Test Structure Detection Service [1 day]
**Priority**: HIGH
**File**: `src/services/structure/structure_detection.py`

**Current Status**: 80% complete, MOST COMPLEX SERVICE (359 LOC), UNVALIDATED

**Implementation Features** (Already Present):
```python
class StructureDetectionService:
    def detect_structure(self, audio_path, asr_data, chord_data, beat_data):
        # Multi-modal boundary detection
        boundaries = self._detect_boundaries_multimodal(...)

        # Section classification
        sections = self._classify_sections(boundaries, ...)

        # Confidence scoring
        for section in sections:
            section['confidence'] = self._calculate_confidence(...)
```

**Test Plan**:

**Phase 1: Boundary Detection Accuracy** [4 hours]
```python
# tests/unit/test_structure.py

# Test dataset: 20+ songs with hand-labeled sections
TEST_SONGS = [
    {
        'file': 'test_audio/pop_verse_chorus.wav',
        'ground_truth': [
            {'start': 0.0, 'end': 8.0, 'label': 'intro'},
            {'start': 8.0, 'end': 24.0, 'label': 'verse'},
            {'start': 24.0, 'end': 40.0, 'label': 'chorus'},
            # ...
        ]
    },
    # More songs across genres
]

def test_boundary_detection_accuracy():
    """Measure boundary detection accuracy with ±2s tolerance."""
    for song in TEST_SONGS:
        detected = service.detect_structure(song['file'])
        accuracy = compute_boundary_f1(detected, song['ground_truth'], tolerance=2.0)

        assert accuracy > 0.70, f"Boundary accuracy {accuracy} below 70% threshold"

def compute_boundary_f1(detected, ground_truth, tolerance):
    """Compute F1 score for boundary detection."""
    # True positive: detected boundary within ±tolerance of ground truth
    # False positive: detected boundary with no nearby ground truth
    # False negative: ground truth boundary with no nearby detection
    pass
```

**Phase 2: Section Label Accuracy** [4 hours]
```python
def test_section_classification_accuracy():
    """Measure section label accuracy."""
    correct = 0
    total = 0

    for song in TEST_SONGS:
        detected = service.detect_structure(song['file'])

        for gt_section in song['ground_truth']:
            # Find matching detected section (by time overlap)
            detected_section = find_overlapping_section(detected, gt_section)

            if detected_section and detected_section['label'] == gt_section['label']:
                correct += 1
            total += 1

    accuracy = correct / total
    assert accuracy > 0.60, f"Label accuracy {accuracy} below 60% threshold"
```

**Phase 3: Genre Diversity** [2 hours]
```python
# Test across genres
GENRES = ['pop', 'rock', 'jazz', 'edm', 'classical']

def test_structure_detection_across_genres():
    """Verify algorithm works across diverse genres."""
    for genre in GENRES:
        songs = get_test_songs_for_genre(genre)

        for song in songs:
            detected = service.detect_structure(song)

            # Should detect at least 2 sections
            assert len(detected['sections']) >= 2

            # Sections should cover full duration
            total_duration = sum(s['end'] - s['start'] for s in detected['sections'])
            assert total_duration > song['duration'] * 0.9  # 90% coverage
```

**Performance Benchmark** [1 hour]
```python
import time

def test_structure_detection_performance():
    """Benchmark processing time."""
    test_file = 'test_audio/3min_song.wav'  # 180 seconds

    start = time.time()
    result = service.detect_structure(test_file)
    elapsed = time.time() - start

    # Target: <15s for 3-minute song (0.083x realtime)
    assert elapsed < 15.0, f"Processing took {elapsed}s, exceeds 15s target"
```

**Acceptance Criteria**:
- ✅ Boundary detection F1 score: >0.70 (±2s tolerance)
- ✅ Section label accuracy: >0.60
- ✅ Works across 5+ diverse genres
- ✅ Performance: <15s per 3-minute song
- ✅ No crashes on edge cases (silence, noise, single-section)

---

### P2: Optimization & Enhancement (Week 2)

#### Task 2: Optimize Structure Detection Algorithm [2 days]
**Priority**: MEDIUM
**Current Performance**: Unknown (estimated 10-15s per song)
**Target**: <10s per song (0.056x realtime for 3-minute song)

**Profiling** [4 hours]
```python
import cProfile
import pstats

# Profile the service
profiler = cProfile.Profile()
profiler.enable()

result = service.detect_structure('test_audio/song.wav')

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 functions by time
```

**Expected Bottlenecks**:
1. **Novelty curve computation** - Multiple STFT calculations
2. **Self-similarity matrix** - O(n²) complexity
3. **Lyric repetition analysis** - String matching

**Optimization Strategies**:

**Strategy 1: Reduce Audio Sample Rate**
```python
# Current: sr=22050 (default librosa)
# Optimized: sr=16000 or sr=11025 for structure analysis

audio, sr = librosa.load(audio_path, sr=16000)  # 30% speedup
```

**Strategy 2: Reduce Hop Length**
```python
# Current: hop_length=512 (default)
# Optimized: hop_length=1024 or hop_length=2048

# Doubles speed, minimal accuracy loss for structure detection
```

**Strategy 3: Cache Intermediate Results**
```python
# Cache beat-synchronous chroma for self-similarity
chroma_sync = librosa.util.sync(chroma, beat_frames)
# Reuse for both boundary detection and classification
```

**Strategy 4: Parallelize Independent Computations**
```python
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor() as executor:
    # Run novelty and self-similarity in parallel
    novelty_future = executor.submit(compute_novelty, audio)
    similarity_future = executor.submit(compute_self_similarity, chroma)

    novelty = novelty_future.result()
    similarity = similarity_future.result()
```

**Acceptance Criteria**:
- ✅ Performance: <10s per 3-minute song
- ✅ Accuracy maintained: >0.65 boundary F1, >0.55 label accuracy
- ✅ Memory usage: <2GB peak

---

#### Task 3: Evaluate ML Models for Structure Detection [2-3 days]
**Priority**: MEDIUM
**Goal**: Improve accuracy from ~70% to >80% with deep learning

**Model Options**:

**Option A: MSAF (Music Structure Analysis Framework)**
```python
import msaf

# Pre-trained models available
boundaries, labels = msaf.process('song.wav', boundaries_id='sf')

# Models:
# - 'sf' - Spectral clustering (fast, decent)
# - 'cnmf' - Convex NMF (slower, better)
# - '2dfmc' - 2D Fourier Magnitude Coefficients
```

**Pros**:
- Established library, well-tested
- Multiple algorithms to choose from
- Good documentation

**Cons**:
- Not state-of-the-art (pre-deep learning)
- May not beat current multi-modal approach

---

**Option B: Segmentron (Transformer-based)**
```python
# State-of-the-art deep learning model
from transformers import AutoModel

model = AutoModel.from_pretrained('allenai/segmentron')
sections = model.predict('song.wav')
```

**Pros**:
- State-of-the-art accuracy (>85% on benchmarks)
- Handles complex structures (jazz, progressive rock)

**Cons**:
- Requires GPU for inference
- Slower than rule-based (5-10s per song)
- May require fine-tuning on Performia's domain

---

**Evaluation Protocol**:
```python
# Benchmark current vs MSAF vs Segmentron

results = {
    'current': evaluate_model(current_service, TEST_SONGS),
    'msaf_sf': evaluate_model(msaf_sf, TEST_SONGS),
    'msaf_cnmf': evaluate_model(msaf_cnmf, TEST_SONGS),
    'segmentron': evaluate_model(segmentron, TEST_SONGS),
}

# Compare:
# - Boundary F1 score
# - Label accuracy
# - Processing time
# - Memory usage

print_comparison_table(results)
```

**Decision Criteria**:
- If MSAF/Segmentron >10% better accuracy → integrate
- If <5% better → stick with current (simpler, faster)
- If 5-10% better → A/B test with users

---

### P3: Advanced Features (Backlog)

#### Task 4: Advanced Downbeat Detection [3-4 days]
**Current**: Approximation (every 4th beat)
**Target**: Accurate downbeat detection with >85% accuracy

**Implementation**:
```python
from madmom.features.downbeats import DBNDownBeatTrackingProcessor

# Replace approximation in beats_key service
processor = DBNDownBeatTrackingProcessor(fps=100)
downbeats = processor('song.wav')

# Returns: [(time, position)]
# position=1 indicates downbeat (start of bar)
```

**Alternative**: librosa.beat.plp (Predominant Local Pulse)
```python
import librosa

tempo, beats = librosa.beat.beat_track(y=audio, sr=sr)
downbeats = librosa.beat.plp(y=audio, sr=sr)[::4]  # Every 4th beat
```

**Testing**:
```python
def test_downbeat_accuracy():
    """Measure downbeat detection accuracy."""
    for song in TEST_SONGS_WITH_DOWNBEATS:
        detected = service.detect_downbeats(song['file'])
        ground_truth = song['downbeats']

        accuracy = compute_hit_rate(detected, ground_truth, tolerance=0.07)
        assert accuracy > 0.85
```

---

#### Task 5: Multi-Level Structure [2 days]
**Goal**: Detect sub-sections (verse 1a, verse 1b, chorus pre, chorus main)

**Implementation**:
```python
def detect_multi_level_structure(audio_path):
    # Level 1: Major sections (intro, verse, chorus)
    major_sections = detect_structure(audio_path)

    # Level 2: Sub-sections within each major section
    for section in major_sections:
        sub_sections = detect_sub_sections(
            audio_path,
            start=section['start'],
            end=section['end']
        )
        section['sub_sections'] = sub_sections

    return major_sections
```

**Use Cases**:
- Pre-chorus detection
- Bridge vs solo distinction
- Verse variation (verse 1 vs verse 2)

---

## Tools & Resources

### Key Libraries
```python
# Structure Analysis
import librosa
import librosa.segment
import msaf
from madmom.features import downbeats

# Machine Learning
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import numpy as np

# Music Theory
import music21  # For harmonic analysis
```

### Test Data
```bash
# Download benchmark datasets
# SALAMI - Structural Analysis of Large Amounts of Music Information
# MIREX - Music Information Retrieval Evaluation eXchange

# Or create custom test set
test_audio/
├── pop_verse_chorus.wav
├── rock_intro_verse_chorus_bridge.wav
├── jazz_aaba_form.wav
├── edm_buildup_drop.wav
└── classical_sonata_form.wav
```

### Evaluation Metrics
```python
def boundary_precision_recall_f1(detected, ground_truth, tolerance=2.0):
    """Compute P/R/F1 for boundary detection."""
    tp = 0  # True positives
    fp = 0  # False positives
    fn = 0  # False negatives

    for d in detected:
        if any(abs(d - g) <= tolerance for g in ground_truth):
            tp += 1
        else:
            fp += 1

    fn = len(ground_truth) - tp

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1
```

---

## Collaboration Points

### Dependencies on Other Agents

**Audio DSP Agent**:
- Requires chord service output for harmonic analysis
- Coordinate on audio processing parameters (sr, hop_length)

**Pipeline Integration Agent**:
- Structure service must complete before packager
- Coordinate on error handling and partial file format

### Shared Resources
- Beat detection output from beats_key service
- Chord progression from chords service
- Lyrics from ASR service
- Test audio files

---

## Success Metrics

### Accuracy Targets
- [ ] Boundary detection F1: >0.70 (baseline), >0.80 (with ML)
- [ ] Section label accuracy: >0.60 (baseline), >0.75 (with ML)
- [ ] Downbeat accuracy: >0.85 (if implemented)
- [ ] Works across 5+ genres

### Performance Targets
- [ ] Processing time: <15s per 3-min song (baseline), <10s (optimized)
- [ ] Memory usage: <2GB peak
- [ ] Real-time factor: <0.1x (1s processing per 10s audio)

### Code Quality
- [ ] Unit tests for all detection methods
- [ ] Integration tests with diverse music
- [ ] Performance benchmarks documented
- [ ] Algorithm explanations in docstrings

---

## Agent Prompts

### Activation Prompt
```
Act as the Structure/Analysis Specialist agent. Test the structure detection service
in src/services/structure/structure_detection.py with 20+ diverse songs. Measure
boundary detection F1 and section label accuracy. Create comprehensive test suite
and document results. Target >70% boundary F1 and >60% label accuracy.
```

### Handoff Prompt
```
Structure analysis complete. Service tested with {accuracy}% boundary F1 and
{label_accuracy}% section label accuracy across {num_songs} songs. Performance
optimized to {time}s per 3-minute song. Ready for production. Consider evaluating
MSAF or Segmentron for further accuracy improvements.
```

---

## Development Guidelines

### Code Standards
```python
# Type hints and docstrings
from typing import List, Dict, Tuple

def detect_boundaries(
    audio: np.ndarray,
    sr: int,
    beat_times: List[float]
) -> List[float]:
    """Detect structural boundaries in audio.

    Args:
        audio: Audio time series
        sr: Sample rate in Hz
        beat_times: Beat timestamps in seconds

    Returns:
        List of boundary timestamps in seconds

    Algorithm:
        1. Compute novelty curve (spectral + harmonic)
        2. Peak picking with adaptive threshold
        3. Align to nearest beat
    """
    pass
```

### Testing Standards
```python
# Ground truth comparison
def test_structure_on_known_song():
    """Test with hand-labeled structure."""
    result = service.detect_structure('test_audio/song_with_labels.wav')

    # Verify intro detected
    assert result['sections'][0]['label'] == 'intro'
    assert abs(result['sections'][0]['start'] - 0.0) < 1.0

    # Verify verse detected
    assert result['sections'][1]['label'] == 'verse'
```

### Performance Standards
```python
# Always benchmark
import time

def benchmark_structure_detection():
    songs = ['3min.wav', '4min.wav', '5min.wav']

    for song in songs:
        start = time.time()
        result = service.detect_structure(song)
        elapsed = time.time() - start

        duration = librosa.get_duration(path=song)
        realtime_factor = elapsed / duration

        print(f"{song}: {elapsed:.2f}s ({realtime_factor:.3f}x realtime)")
```

---

## Quick Reference

### Key Files
```
src/services/
└── structure/
    ├── structure_detection.py  # P1: Test this (359 LOC)
    └── main.py                 # CLI interface

tests/unit/
└── test_structure.py           # P1: Create comprehensive tests

benchmarks/
└── structure_accuracy.py       # P1: Accuracy evaluation
```

### Common Issues

**Issue**: False boundaries in sustained sections
**Solution**: Increase peak picking threshold, use median filtering

**Issue**: Missed boundaries in dense sections
**Solution**: Combine multiple novelty features (spectral + harmonic + timbral)

**Issue**: Incorrect labels (verse/chorus confusion)
**Solution**: Use lyric repetition + harmonic similarity for classification

---

*Ready to unlock deep musical understanding for Performia!*
