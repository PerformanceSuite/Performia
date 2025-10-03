# Real-Time Audio Analysis System

## Quick Start

```python
from realtime.analyzer import RealtimeAnalyzer
import numpy as np

# Initialize analyzer
analyzer = RealtimeAnalyzer(sample_rate=44100)

# Process audio block by block (512 samples = ~11.6ms at 44.1kHz)
block_size = 512
for block in audio_stream:
    # Detect pitch
    pitch = analyzer.analyze_pitch(block)  # Returns Hz or None
    
    # Detect onsets (note attacks)
    onset = analyzer.detect_onset(block)  # Returns True/False
    
    # Track beats
    current_time = get_current_time()  # seconds
    beat = analyzer.track_beat(onset, current_time)  # Returns True on beat
    
    # Get tempo estimate
    tempo = analyzer.estimate_tempo()  # Returns BPM
```

## Performance

- **Total latency**: ~14ms average
- **Pitch accuracy**: ±10 cents
- **Onset detection**: <1ms
- **Real-time factor**: 0.83x (faster than real-time)

## Testing

```bash
# Run manual test
cd backend/src/realtime
python test_analysis.py

# Run unit tests
cd backend/tests/realtime
python run_tests_standalone.py

# Run benchmarks
python benchmark_analyzer.py
```

## API Reference

### RealtimeAnalyzer

#### `__init__(sample_rate=44100)`
Initialize the analyzer.

#### `analyze_pitch(audio_block) -> Optional[float]`
Detect pitch in Hz. Returns None if no pitch detected.
- Input: numpy array of audio samples
- Output: frequency in Hz or None
- Latency: ~13ms

#### `detect_onset(audio_block) -> bool`
Detect note attacks/onsets.
- Input: numpy array of audio samples  
- Output: True if onset detected
- Latency: <1ms

#### `track_beat(onset_detected, current_time) -> bool`
Track beats based on onsets.
- Input: onset detection result, current time in seconds
- Output: True if beat detected
- Latency: <0.01ms

#### `estimate_tempo() -> float`
Get current tempo estimate.
- Output: tempo in BPM
- Updates every 2 seconds

#### `get_performance_stats() -> dict`
Get performance metrics for monitoring.

## Configuration

```python
analyzer = RealtimeAnalyzer(sample_rate=44100)

# Adjust pitch detection range
analyzer.fmin = librosa.note_to_hz('C2')  # 65 Hz
analyzer.fmax = librosa.note_to_hz('C7')  # 2093 Hz

# Adjust onset sensitivity
analyzer.onset_threshold = 0.3  # Lower = more sensitive

# Adjust tempo estimate
analyzer.tempo_estimate = 120.0  # Initial BPM guess
```

## Integration Example

```python
# Complete analysis pipeline
from realtime.audio_input import RealtimeAudioInput
from realtime.analyzer import RealtimeAnalyzer

# Setup
audio_input = RealtimeAudioInput(sample_rate=44100, block_size=512)
analyzer = RealtimeAnalyzer(sample_rate=44100)

# Start streaming
audio_input.start()

while True:
    # Get audio block
    block = audio_input.get_block()
    
    # Analyze
    pitch = analyzer.analyze_pitch(block)
    onset = analyzer.detect_onset(block)
    
    # Get context
    current_time = time.time()
    beat = analyzer.track_beat(onset, current_time)
    tempo = analyzer.estimate_tempo()
    
    # Use results
    if pitch:
        print(f"Pitch: {pitch:.1f}Hz")
    if onset:
        print("Onset detected!")
    if beat:
        print(f"Beat! (tempo: {tempo:.1f} BPM)")
```

## Files

- `analyzer.py` - Main analyzer implementation
- `test_analysis.py` - Manual test script
- `../tests/realtime/test_analyzer.py` - Unit tests (pytest)
- `../tests/realtime/run_tests_standalone.py` - Standalone test runner
- `../tests/realtime/benchmark_analyzer.py` - Performance benchmarks
- `../tests/realtime/ANALYZER_RESULTS.md` - Detailed results

## See Also

- `audio_input.py` - Audio capture
- `message_bus.py` - Event distribution
- `PERFORMIA_MASTER_PLAN.md` - Overall architecture
