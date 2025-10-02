# Performia Backend Development Roadmap

**Status**: 70% Production-Ready | **Critical Blockers**: 3 | **Timeline**: 1-2 weeks to MVP

---

## Executive Summary

### Current State
- ✅ **Working**: ASR, Beats/Key, Chords, Voice API, Orchestrator, REST API
- ⚠️ **Untested**: Melody/Bass (75% impl), Structure (80% impl)
- ❌ **Stub**: Source Separation (5% impl)
- 🐛 **Broken**: Packager argument interface

### Critical Path to Production
1. **Fix Packager** (2 hours) → Unblock pipeline
2. **Implement Separation** (2 days) → Quality boost
3. **Add Validation** (4 hours) → Data integrity
4. **Test Unvalidated Services** (2 days) → Risk mitigation

### Performance Status
- ASR: 0.34x realtime ✅ (exceeds 2x target)
- Beats/Key: 0.16x realtime ✅ (exceeds 2x target)
- Chords: 0.11x realtime ✅ (exceeds 2x target)
- Pipeline: 135% speedup ✅ (exceeds 30% target)
- **Projected Full Pipeline**: 0.22-0.25x realtime ✅

---

## Priority Matrix

### P0: Critical Path Blockers (Do First - 3-4 days)

#### 1. Fix Packager Argument Interface [2 hours] 🔥
**Problem**: Orchestrator calls `packager --infile` but packager expects `--partials --raw --out`

**Files**:
- `src/services/orchestrator/async_pipeline.py:51-67`
- `src/services/packager/main.py`

**Solution Options**:
- Option A: Add special case in orchestrator for packager
- Option B: Update packager to accept `--infile` and infer partials dir
- **Recommended**: Option B (cleaner interface)

**Impact**: Unblocks entire end-to-end pipeline

---

#### 2. Implement Source Separation [1-2 days] 🔥
**Problem**: Stub returns same file for all stems (vocals, drums, bass, other)

**Files**:
- `src/services/separation/main.py` (currently 50 LOC stub)

**Implementation**:
```python
# Use Demucs (state-of-the-art)
import demucs.separate
model = demucs.pretrained.get_model('htdemucs')
stems = demucs.apply_model(model, audio)
# Write: vocals.wav, drums.wav, bass.wav, other.wav
```

**Dependencies**: `pip install demucs torch`

**Performance Target**: <30s for 3-minute song

**Impact**:
- 2-3x quality improvement for chords (clean harmonic content)
- Critical for melody/bass accuracy (isolated stems)
- Enables karaoke features (vocal removal)

**Alternative**: Spleeter (faster but lower quality)

---

#### 3. Add Schema Validation to Packager [4 hours] 🔥
**Problem**: No validation before Song Map output → malformed JSON crashes frontend

**Files**:
- `src/services/packager/main.py`
- `schemas/song_map.schema.json`

**Implementation**:
```python
import jsonschema

with open('schemas/song_map.schema.json') as f:
    schema = json.load(f)

# Before writing song_map
jsonschema.validate(song_map, schema)
```

**Required Fields**: id, duration_sec, tempo, beats, downbeats, meter, chords, lyrics

**Impact**: Prevents invalid data from reaching frontend

---

### P1: Quality & Reliability (Do Next - 3-4 days)

#### 4. Test Melody/Bass Service [1 day]
**Status**: 75% complete, implementation done but UNVALIDATED

**Files**:
- `src/services/melody_bass/main.py` (complete pitch tracking)

**Test Plan**:
- Test with 10+ vocal recordings (diverse pitch ranges)
- Validate MIDI note accuracy (pitch, timing, duration)
- Benchmark performance (target: <10s per 3-min song)
- Test stem integration (separated vocals vs full mix)

**Success Criteria**: >80% note accuracy, <10s processing time

---

#### 5. Test Structure Detection [1 day]
**Status**: 80% complete, MOST COMPLEX SERVICE, unvalidated

**Files**:
- `src/services/structure/structure_detection.py` (359 LOC, multi-modal)

**Test Plan**:
- Test with 20+ songs across genres (pop, rock, jazz, EDM)
- Measure section boundary accuracy (±2s tolerance)
- Validate section labels (intro, verse, chorus, bridge, outro)
- Test lyric repetition detection
- Benchmark performance

**Success Criteria**: >70% boundary accuracy, >60% label accuracy

---

#### 6. Add Job Persistence to API [1 day]
**Problem**: Jobs lost on API restart (in-memory only)

**Files**:
- `src/services/api/job_manager.py`

**Implementation**:
```python
import sqlite3
# OR
import redis

# Store job state: id, status, progress, result_path, timestamps
# Resume jobs on startup
# Cleanup strategy: delete jobs > 7 days old
```

**Impact**: Production reliability, user experience

---

### P2: Optimization & Scale (Later - 1 week)

#### 7. GPU Acceleration for Whisper [4 hours]
**Performance Gain**: 5-10x speedup (1.7s → 0.17-0.34s per 5s audio)

```python
import torch
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
model = whisper.load_model("base", device=device)
```

---

#### 8. Extended Chord Vocabulary [1-2 days]
**Current**: 24 chords (12 major + 12 minor)
**Target**: 72+ chords (7th, sus, aug, dim, inversions)

**Options**:
- Extend template matching (medium quality, fast)
- Integrate deep learning model: BTC, Chordino (high quality, slower)

**Impact**: Better support for jazz, R&B, complex harmony

---

#### 9. Improve Structure Detection [2-3 days]
**Options**:
- Integrate MSAF (Music Structure Analysis Framework)
- Integrate Segmentron (transformer-based)
- Add genre-specific heuristics
- Multi-level structure (sub-sections)

**Impact**: More accurate section labels, better user experience

---

#### 10. Integration Test Suite [2-3 days]
**Current Coverage**: ~15% (2 services tested)

**Test Plan**:
```
tests/
├── unit/
│   ├── test_asr.py
│   ├── test_beats_key.py
│   ├── test_chords.py
│   ├── test_melody_bass.py
│   ├── test_structure.py
│   └── test_packager.py ✅ (exists)
├── integration/
│   ├── test_pipeline.py ✅ (exists but broken)
│   ├── test_api_endpoints.py
│   ├── test_service_communication.py
│   └── test_error_propagation.py
└── performance/
    ├── benchmark_services.py
    └── regression_tests.py
```

**Impact**: Catch integration bugs early, prevent regressions

---

### P3: Future Enhancements (Backlog)

#### 11. Real-time Streaming [1-2 weeks]
- Streaming ASR for live performance
- Progressive beat detection
- Real-time chord recognition
- WebSocket updates to frontend

**Impact**: Live performance mode

---

#### 12. Advanced Downbeat Detection [3-4 days]
**Current**: Approximation (every 4th beat)
**Target**: Accurate downbeat detection with madmom or librosa.beat.plp

**Impact**: Better structure detection, improved Song Map quality

---

## Service Status Table

| Service | Completion | Status | Performance | Priority |
|---------|-----------|--------|-------------|----------|
| ASR (Whisper) | 95% | ✅ Production | 0.34x realtime | P2 (GPU) |
| Beats/Key | 90% | ✅ Production | 0.16x realtime | P3 (Downbeats) |
| Chords | 85% | ✅ Production | 0.11x realtime | P2 (Extended) |
| Melody/Bass | 75% | ⚠️ Untested | Unknown | **P1** |
| Structure | 80% | ⚠️ Untested | Unknown | **P1** |
| Separation | 5% | ❌ Stub | N/A | **P0** |
| Packager | 60% | 🐛 Broken | <1s | **P0** |
| Orchestrator | 85% | ✅ Working | 135% speedup | P0 (Packager) |
| Voice API | 95% | ✅ Production | <1ms | P3 |
| REST API | 90% | ✅ Working | N/A | **P1** (Persistence) |

---

## Agent Specialization Strategy

### 🤖 Agent 1: Audio DSP Specialist
**Focus**: Low-level audio processing, ML models, signal processing

**Assigned Tasks**:
- P0.2: Implement Demucs separation
- P1.4: Test melody/bass extraction
- P2.8: Extended chord vocabulary
- P2.7: GPU acceleration

**Skills**: Python, librosa, Demucs, PyTorch, signal processing, MIDI

**Estimated Time**: 1 week for P0-P1

---

### 🤖 Agent 2: Pipeline Integration Specialist
**Focus**: System architecture, API design, testing, DevOps

**Assigned Tasks**:
- P0.1: Fix packager argument interface
- P0.3: Add schema validation
- P1.6: Add job persistence
- P2.10: Integration test suite

**Skills**: Python, async, FastAPI, pytest, SQLite, systems integration

**Estimated Time**: 1 week for P0-P1

---

### 🤖 Agent 3: Structure/Analysis Specialist
**Focus**: Music theory, structure detection, optimization

**Assigned Tasks**:
- P1.5: Test structure detection
- P2.9: Improve structure detection (MSAF, Segmentron)
- P3.12: Advanced downbeat detection

**Skills**: Python, music theory, machine learning, algorithms, optimization

**Estimated Time**: 1 week for P1-P2

---

## Timeline Estimates

### Sprint 1: Critical Path (Week 1)
**Goal**: Working end-to-end pipeline

| Day | Agent 1 (DSP) | Agent 2 (Integration) | Agent 3 (Structure) |
|-----|--------------|---------------------|-------------------|
| Mon | P0.2: Start Demucs | P0.1: Fix packager | - |
| Tue | P0.2: Demucs testing | P0.3: Schema validation | - |
| Wed | P0.2: Optimize | P1.6: Start persistence | P1.5: Structure tests |
| Thu | P1.4: Melody/bass tests | P1.6: Persistence | P1.5: Structure tests |
| Fri | P1.4: Melody/bass tests | Integration testing | P1.5: Analysis |

**Deliverables**:
- ✅ Working packager
- ✅ Demucs separation
- ✅ Schema validation
- ✅ Tested melody/bass
- ✅ Tested structure
- ✅ Job persistence

---

### Sprint 2: Quality & Scale (Week 2)
**Goal**: Production-ready with optimizations

| Day | Agent 1 (DSP) | Agent 2 (Integration) | Agent 3 (Structure) |
|-----|--------------|---------------------|-------------------|
| Mon | P2.7: GPU acceleration | P2.10: Unit tests | P2.9: MSAF research |
| Tue | P2.8: Extended chords | P2.10: Integration tests | P2.9: MSAF integration |
| Wed | P2.8: Chord testing | P2.10: Performance tests | P2.9: Testing |
| Thu | Documentation | Documentation | Documentation |
| Fri | **Demo & validation** | **Demo & validation** | **Demo & validation** |

**Deliverables**:
- ✅ GPU-accelerated Whisper
- ✅ Extended chord vocabulary
- ✅ Improved structure detection
- ✅ Comprehensive test suite
- ✅ Full documentation
- ✅ Production deployment

---

## Success Metrics

### Performance Targets
- [x] ASR: <2x realtime (actual: 0.34x) ✅
- [x] Beats/Key: <2x realtime (actual: 0.16x) ✅
- [x] Chords: <2x realtime (actual: 0.11x) ✅
- [ ] Separation: <30s per 3-min song
- [ ] Melody/Bass: <10s per 3-min song
- [ ] Structure: <15s per 3-min song
- [ ] **Full Pipeline**: <45s per 3-min song (0.25x realtime)

### Quality Targets
- [ ] Chord accuracy: >85% (currently ~70% estimated)
- [ ] Melody note accuracy: >80%
- [ ] Structure boundary accuracy: >70%
- [ ] Section label accuracy: >60%

### System Targets
- [ ] Test coverage: >70% (currently ~15%)
- [ ] API uptime: >99.5%
- [ ] Job completion rate: >95%
- [ ] Zero data corruption (schema validation)

---

## Risk Assessment

### High Risk Items
1. **Demucs GPU Memory**: May OOM on large files → implement batch processing
2. **Structure Detection Accuracy**: Complex algorithm, may need ML models
3. **Melody/Bass Polyphonic Tracks**: Single-note assumption breaks on harmonies

### Mitigation Strategies
- Add memory monitoring and graceful degradation
- Implement fallback models (simpler algorithms if ML fails)
- Add polyphony detection and multi-pitch tracking

---

## Dependencies & Prerequisites

### Python Packages (add to requirements.txt)
```
demucs>=4.0.0
torch>=2.0.0
jsonschema>=4.0.0
sqlalchemy>=2.0.0  # for persistence
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

### System Requirements
- Python 3.12+
- 16GB RAM (for Demucs)
- CUDA/MPS for GPU acceleration (optional but recommended)
- 10GB disk space for models

---

## Documentation Needs

### Service READMEs (missing)
- [ ] ASR service README
- [ ] Beats/Key service README
- [ ] Chords service README
- [ ] Melody/Bass service README
- [ ] Structure service README
- [ ] Separation service README
- [ ] Packager service README

### API Documentation
- [ ] OpenAPI/Swagger spec
- [ ] API usage examples
- [ ] Error code reference

### Developer Guides
- [ ] Service development guide
- [ ] Testing guide
- [ ] Deployment guide

---

## Next Actions (Starting Now)

1. **Create 3 specialized agents** (Agent 2 can do this)
2. **Kick off Sprint 1** with parallel execution
3. **Daily standups** to coordinate cross-agent dependencies
4. **End-of-sprint demo** to validate full pipeline

**Estimated Completion**: 2 weeks from today → Production-ready backend

---

*Generated by Claude Code Agent Analysis - 2025-09-30*
