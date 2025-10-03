# Audio Pipeline Architecture Analysis
**Date**: September 30, 2024
**Agent**: Audio Pipeline Development Agent
**Branch**: feature/audio-pipeline-optimization

## Executive Summary

Analyzed the Song Map generation pipeline architecture. Current implementation consists of **stub services** with minimal functionality. This analysis provides the foundation for building out a production-ready pipeline targeting <30 second processing time for 3-minute songs.

---

## Current Architecture

### Service Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     INPUT: Audio File (WAV/MP3)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
┌─────────▼─────────┐    ┌─────────▼──────────┐
│   INGEST SERVICE   │    │  SEPARATION SERVICE│
│  (Format Convert)  │    │  (Stem Isolation)  │
└─────────┬──────────┘    └─────────┬──────────┘
          │                         │
          └────────────┬────────────┘
                       │
          ┌────────────┴────────────────────────┐
          │                                      │
┌─────────▼────────┐  ┌────────────────────┐   │
│   ASR SERVICE    │  │  BEATS/KEY SERVICE │   │
│  (Lyrics+Time)   │  │  (Tempo+Key+Beats) │   │
└─────────┬────────┘  └────────┬───────────┘   │
          │                    │                │
          │           ┌────────▼───────────┐    │
          │           │   CHORDS SERVICE   │    │
          │           │  (Chord Progress.) │    │
          │           └────────┬───────────┘    │
          │                    │                │
          │           ┌────────▼───────────┐    │
          │           │ MELODY/BASS SERV.  │    │
          │           │   (Pitch Track)    │    │
          │           └────────┬───────────┘    │
          │                    │                │
          │           ┌────────▼────────────┐   │
          │           │ STRUCTURE SERVICE   │   │
          │           │ (Section Detect)    │   │
          │           └────────┬────────────┘   │
          │                    │                │
          └────────────┬───────┴────────────────┘
                       │
             ┌─────────▼─────────┐
             │  PACKAGER SERVICE │
             │  (Merge Partials) │
             └─────────┬─────────┘
                       │
          ┌────────────▼────────────┐
          │  OUTPUT: Song Map JSON  │
          └─────────────────────────┘
```

### Service Details

| Service | Purpose | Status | Dependencies | Est. Time |
|---------|---------|--------|--------------|-----------|
| **ingest** | Audio format conversion | Stub | None | 1-2s |
| **separation** | Stem separation (vocals, drums, etc.) | Stub | ingest | 5-10s |
| **asr** | Speech-to-text with timing | Stub | separation | 3-5s |
| **beats_key** | Beat detection, tempo, key | Stub | ingest | 2-4s |
| **chords** | Chord recognition | Stub | beats_key | 3-5s |
| **melody_bass** | Pitch tracking | Stub | separation | 2-4s |
| **structure** | Section boundaries | Stub | beats_key, asr | 1-2s |
| **packager** | Merge all partial results | Minimal | All above | <1s |
| **orchestrator** | Coordinate pipeline | Minimal | All | - |

---

## Current Implementation Status

### ✅ What Exists

1. **Service Structure**: All 9 services have directories and entry points
2. **Basic I/O**: Services can read/write JSON partials
3. **Packager**: Minimal implementation exists for merging results
4. **Common Utilities**: Shared audio loading and JSON writing

### ⚠️ What's Missing (Critical)

1. **Actual ML Models**: All services return stub data ("la di da" lyrics)
2. **Librosa Integration**: No audio analysis implemented
3. **Whisper Integration**: ASR service doesn't call Whisper
4. **Async/Parallel Processing**: Sequential execution only
5. **Error Handling**: Minimal error checking
6. **Caching**: No intermediate result caching
7. **Progress Reporting**: No progress callbacks
8. **Performance Monitoring**: No timing metrics

---

## Processing Flow Analysis

### Current Sequential Flow (Estimated)
```
ingest (2s)
  → separation (10s)
    → asr (5s)
    → beats_key (4s)
      → chords (5s)
      → melody_bass (4s)
      → structure (2s)
    → packager (1s)
─────────────────
Total: ~33 seconds
```

**Status**: ⚠️ **Above 30s target**

### Optimized Parallel Flow (Target)
```
ingest (2s)
  → separation (10s)
    ├─ asr (5s) ────────────┐
    ├─ beats_key (4s)       │
    │    ├─ chords (5s)     │
    │    └─ structure (2s)  │
    └─ melody_bass (4s) ────┘
      → packager (1s)
─────────────────────────
Total: ~22-24 seconds
```

**Improvement**: 9-11 seconds saved (27-33% faster)

---

## Parallelization Opportunities

### HIGH PRIORITY: Independent Services

These can run in parallel after `separation`:

1. **asr** (vocals stem) - No dependencies
2. **beats_key** (full mix) - No dependencies
3. **melody_bass** (stems) - No dependencies

**Implementation**:
```python
async def process_song(audio_path: str) -> SongMap:
    # Sequential: ingest and separation
    audio = await ingest_service(audio_path)
    stems = await separation_service(audio)

    # PARALLEL: independent analyses
    results = await asyncio.gather(
        asr_service(stems['vocals']),
        beats_key_service(audio),
        melody_bass_service(stems)
    )

    asr, beats_key, melody_bass = results

    # Sequential: dependent analyses
    chords = await chords_service(audio, beats_key)
    structure = await structure_service(beats_key, asr)

    # Final assembly
    return packager_service(asr, beats_key, chords, melody_bass, structure)
```

**Estimated Time Savings**: 9-11 seconds

### MEDIUM PRIORITY: Dependent Services

These require sequential execution but can be optimized:

1. **chords** depends on `beats_key` (beat grid for alignment)
2. **structure** depends on `beats_key` + `asr` (timing anchors)

**Optimization**: Preload models, cache beat grid

---

## Bottleneck Analysis

### Service Time Breakdown (Estimated with Real Implementations)

| Service | Time | % of Total | Bottleneck Reason |
|---------|------|-----------|-------------------|
| **separation** | 10s | 30% | Deep learning model inference (Demucs/Spleeter) |
| **asr** | 5s | 15% | Whisper model inference |
| **chords** | 5s | 15% | Chromagram + HMM/CRF inference |
| **beats_key** | 4s | 12% | Beat tracking + key detection |
| **melody_bass** | 4s | 12% | Pitch tracking (CREPE/PYIN) |
| **structure** | 2s | 6% | Novelty detection |
| **ingest** | 2s | 6% | Audio loading/resampling |
| **packager** | 1s | 3% | JSON merging |

### Critical Path
```
ingest → separation → [asr | beats_key → chords | melody_bass] → structure → packager
        2s      10s         5s    4s+5s=9s         4s              2s         1s

Longest path: 2 + 10 + 9 + 2 + 1 = 24s (with parallelization)
```

---

## Optimization Recommendations

### 🔴 Phase 1: Foundation (Week 1-2)

#### 1.1 Implement Core Services
- **asr**: Integrate Whisper API or local model
- **beats_key**: Implement using librosa.beat.beat_track()
- **chords**: Basic chord recognition with librosa chroma
- **melody_bass**: Basic pitch tracking with librosa.pyin()

**Priority**: CRITICAL
**Impact**: Functional pipeline
**Time**: 20-30 hours

#### 1.2 Add Async/Parallel Processing
```python
# Create async wrappers for all services
async def async_asr(audio_path: str) -> Dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_asr, audio_path)

# Orchestrator coordinates parallel execution
async def orchestrate(audio_path: str) -> SongMap:
    # ... parallel execution as shown above
```

**Priority**: HIGH
**Impact**: 30-40% time reduction
**Time**: 8-12 hours

#### 1.3 Add Error Handling
```python
try:
    result = await service_call(audio)
except ServiceError as e:
    logger.error(f"Service failed: {e}")
    # Return partial results or retry
    result = fallback_result()
```

**Priority**: HIGH
**Impact**: Production reliability
**Time**: 4-6 hours

---

### 🟡 Phase 2: Performance (Week 3-4)

#### 2.1 Model Caching
```python
# Load models once, reuse across requests
class ServiceCache:
    def __init__(self):
        self.whisper_model = None
        self.demucs_model = None

    def get_whisper(self):
        if not self.whisper_model:
            self.whisper_model = whisper.load_model("base")
        return self.whisper_model
```

**Impact**: Eliminate model load time (2-5s per request)
**Time**: 4-6 hours

#### 2.2 Optimize Separation
- Use quantized models (INT8)
- GPU acceleration if available
- Consider faster alternatives (e.g., Open-Unmix)

**Impact**: 3-5 second reduction
**Time**: 6-8 hours

#### 2.3 Intermediate Caching
```python
@lru_cache(maxsize=100)
def get_beat_grid(audio_hash: str) -> np.ndarray:
    # Cache expensive beat detection results
    return librosa.beat.beat_track(audio)
```

**Impact**: Faster retries, development iteration
**Time**: 3-4 hours

---

### 🟢 Phase 3: Advanced (Week 5-6)

#### 3.1 GPU Acceleration
- CUDA-enabled Demucs for separation
- GPU-accelerated librosa operations
- Batch processing for multiple songs

**Impact**: 40-50% time reduction with GPU
**Time**: 8-12 hours

#### 3.2 Streaming Processing
- Process audio in chunks
- Start downstream services before full audio processed
- Real-time progress updates

**Impact**: Perceived latency reduction, better UX
**Time**: 12-16 hours

#### 3.3 Performance Monitoring
```python
@timed
async def process_step(name: str, func: Callable):
    start = time.time()
    result = await func()
    elapsed = time.time() - start
    metrics.record(name, elapsed)
    return result
```

**Impact**: Identify bottlenecks, track improvements
**Time**: 4-6 hours

---

## Performance Projections

### Baseline (Current Stubs)
- **Time**: 33s (sequential, no real processing)
- **Accuracy**: N/A (stub data)
- **Reliability**: Low (no error handling)

### After Phase 1 (Foundation)
- **Time**: 22-24s (with parallelization)
- **Accuracy**: 70-80% (basic models)
- **Reliability**: Medium (error handling added)
- **✅ Meets <30s target**

### After Phase 2 (Performance)
- **Time**: 16-20s (optimized models, caching)
- **Accuracy**: 85-90% (better models, tuning)
- **Reliability**: High (robust error handling)
- **✅ Exceeds target by 30-40%**

### After Phase 3 (Advanced)
- **Time**: 10-14s (GPU acceleration, streaming)
- **Accuracy**: 90-95% (ensemble methods, refinement)
- **Reliability**: Very High (comprehensive monitoring)
- **✅ 2x faster than target**

---

## Technology Stack Recommendations

### Core Dependencies
```python
# requirements.txt additions
librosa>=0.10.0        # Audio analysis
whisper>=1.0.0         # Speech recognition (or openai API)
demucs>=4.0.0         # Stem separation
madmom>=0.16.1        # Advanced beat tracking
crepe>=0.0.12         # Pitch detection
numpy>=1.24.0
scipy>=1.10.0
fastapi>=0.100.0      # Service endpoints
aiofiles>=23.0.0      # Async file I/O
redis>=4.5.0          # Caching (optional)
```

### Model Selection

| Task | Recommended Model | Alternative | Trade-off |
|------|-------------------|-------------|-----------|
| Separation | Demucs v4 | Spleeter | Quality vs Speed |
| ASR | Whisper base | Whisper API | Local vs Cloud |
| Beat Tracking | madmom DBN | librosa | Accuracy vs Speed |
| Chord Recognition | madmom DeepChroma | librosa chroma | Accuracy vs Speed |
| Pitch Tracking | CREPE | pYIN | Accuracy vs Speed |

---

## Risk Assessment

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| Separation model too slow | HIGH | MEDIUM | Use GPU, quantization, or faster model |
| Whisper API rate limits | MEDIUM | LOW | Use local model or implement retry logic |
| Memory overflow on long songs | MEDIUM | MEDIUM | Implement chunked processing |
| Poor accuracy on certain genres | MEDIUM | MEDIUM | Genre-specific model tuning |

### Operational Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|------------|
| No GPU available | HIGH | LOW | Ensure CPU-optimized code path |
| Large model downloads | LOW | HIGH | Pre-download in deployment |
| Service crashes | MEDIUM | MEDIUM | Implement comprehensive error handling |

---

## Testing Strategy

### Unit Tests
```python
def test_beat_detection():
    """Test beat detection on known tempo"""
    audio = load_test_audio("120bpm.wav")
    beats, tempo = detect_beats(audio)
    assert 118 <= tempo <= 122
    assert len(beats) > 0

def test_asr_accuracy():
    """Test ASR on known lyrics"""
    audio = load_test_audio("known_lyrics.wav")
    result = asr_service(audio)
    assert word_error_rate(result, GROUND_TRUTH) < 0.05
```

### Integration Tests
```python
async def test_full_pipeline():
    """Test complete pipeline"""
    song_map = await process_song("test_song.wav")
    assert song_map["tempo"]["bpm_global"] > 0
    assert len(song_map["lyrics"]) > 0
    assert len(song_map["beats"]) > 0
```

### Performance Tests
```python
def test_performance_target():
    """Ensure <30s processing time"""
    start = time.time()
    song_map = process_song("3min_song.wav")
    elapsed = time.time() - start
    assert elapsed < 30.0
```

---

## Implementation Roadmap

### Week 1-2: Foundation
- [ ] Implement ASR service with Whisper
- [ ] Implement beats/key service with librosa
- [ ] Implement basic chord recognition
- [ ] Add async/parallel orchestration
- [ ] Add error handling

**Milestone**: Functional pipeline, meets 30s target

### Week 3-4: Performance
- [ ] Add model caching
- [ ] Optimize separation service
- [ ] Implement intermediate result caching
- [ ] Add performance monitoring
- [ ] Tune model parameters

**Milestone**: <20s processing time, 85%+ accuracy

### Week 5-6: Advanced
- [ ] GPU acceleration
- [ ] Streaming processing
- [ ] Advanced performance monitoring
- [ ] Ensemble methods for accuracy
- [ ] Production deployment prep

**Milestone**: <15s processing time, 90%+ accuracy

---

## Next Steps

### Immediate Actions (This Week)
1. **Set up development environment** with all dependencies
2. **Create performance benchmark suite** with test audio files
3. **Implement ASR service** with Whisper (highest value)
4. **Implement beats/key service** with librosa
5. **Add async orchestration** for parallel processing

### Success Criteria
- ✅ Pipeline processes 3-minute song in <30 seconds
- ✅ ASR achieves >90% word accuracy
- ✅ Beat detection achieves >95% accuracy
- ✅ All services have error handling
- ✅ Pipeline is reliable (no crashes)

---

## Conclusion

The current pipeline consists of well-structured stub services ready for implementation. With Phase 1 (Foundation), we can achieve the <30 second target. Phases 2-3 will provide headroom for more complex songs and better accuracy.

**Key Insights**:
1. Parallelization alone saves 9-11 seconds (30%)
2. Separation is the biggest bottleneck (30% of time)
3. Model caching eliminates 2-5s overhead
4. GPU acceleration can provide 2x speedup

**Recommendation**: Start with Phase 1 implementation. Focus on ASR and beats/key services first, as they unblock downstream services.

---

**Analyzed by**: Audio Pipeline Development Agent
**Branch**: `feature/audio-pipeline-optimization`
**Ready for**: Phase 1 Implementation