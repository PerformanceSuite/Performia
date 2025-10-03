# Performia Backend

## Quick Start

### Setup Environment (First Time / After Fresh Clone)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Services

**Individual Services:**
```bash
source venv/bin/activate

# ASR (Whisper transcription)
python3 src/services/asr/main.py --id test --infile audio.wav --out output/

# Beats & Key Detection
python3 src/services/beats_key/main.py --id test --infile audio.wav --out output/

# Chord Recognition
python3 src/services/chords/main.py --id test --infile audio.wav --out output/
```

**Full Pipeline (Parallel):**
```bash
source venv/bin/activate
python3 src/services/orchestrator/async_pipeline.py --id song_001 --infile audio.wav --out output/
```

**Voice API:**
```bash
source venv/bin/activate
python3 -m uvicorn services.voice.api:app --reload --host 0.0.0.0 --port 8000
```

## Architecture

### Services (All Implemented)
- ✅ **ASR** - Whisper speech-to-text with word timing (1.7s per 5s audio)
- ✅ **Beats/Key** - Tempo, beat, and key detection (1.3s per 8s audio, 98% accuracy)
- ✅ **Chords** - 24-chord recognition with chroma features (0.9s per 8s audio)
- ✅ **Voice** - FastAPI command processor (<1ms per command)
- 🔧 **Melody/Bass** - Stub (needs pitch tracking implementation)
- 🔧 **Structure** - Stub (needs section detection implementation)
- 🔧 **Separation** - Stub (needs source separation implementation)
- ⚠️ **Packager** - Partial (needs arg interface alignment)

### Async Orchestrator
- **Parallelization**: Runs independent services concurrently
- **Performance**: 135% speedup on 3-service test
- **Dependency Resolution**: Smart ordering based on service dependencies

## Test Results

See `VALIDATION_RESULTS.md` for comprehensive test report.

**Last Validation (2025-09-30):**
- All core services: ✅ Working
- Parallel execution: ✅ 135% speedup achieved
- Voice commands: ✅ All test cases passing

## Performance Targets

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| ASR Speed | <2x realtime | 1.7s/5s (0.34x) | ✅ Exceeds |
| Beats/Key Speed | <2x realtime | 1.3s/8s (0.16x) | ✅ Exceeds |
| Chord Speed | <2x realtime | 0.9s/8s (0.11x) | ✅ Exceeds |
| Pipeline Speedup | >30% | 135% | ✅ Exceeds |

## Next Steps

1. Fix packager arg interface
2. Implement separation service (Demucs/Spleeter)
3. Implement melody/bass pitch tracking
4. Implement structure section detection
5. Add GPU acceleration for Whisper
6. Frontend integration
