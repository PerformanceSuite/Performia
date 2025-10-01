# Demucs Source Separation Service

This service uses the state-of-the-art Demucs hybrid transformer model (htdemucs) to separate audio into 4 high-quality stems.

## Features

- **Model**: htdemucs (Hybrid Transformer Demucs)
- **Output**: 4 stems - vocals, drums, bass, other
- **GPU Support**: CUDA (NVIDIA), MPS (Apple Silicon), CPU fallback
- **Performance**: ~1s for 5s audio on Apple Silicon GPU

## Installation

Dependencies are already in `backend/requirements.txt`:

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

Key dependencies:
- `demucs>=4.0.0` - Source separation model
- `torch>=2.0.0` - PyTorch framework
- `torchaudio>=2.0.0` - Audio I/O

## Usage

### Via Python Module

```bash
cd backend
source venv/bin/activate
PYTHONPATH=/path/to/backend/src python -m services.separation.main \
  --id job_001 \
  --infile /path/to/audio.wav \
  --out /path/to/output \
  --stems-dir /path/to/stems
```

### Via Pipeline

```bash
cd backend
python scripts/run_pipeline.py --id demo --raw /path/to/audio.wav
```

## Output

### Stem Files

The service generates 5 WAV files in `stems-dir/job_id/`:

- `mix.wav` - Original audio (copy)
- `vocals.wav` - Isolated vocals
- `drums.wav` - Isolated drums
- `bass.wav` - Isolated bass
- `other.wav` - Other instruments (guitars, keys, etc.)

### Partial JSON

Output JSON saved to `output_dir/job_id/job_id.separation.json`:

```json
{
  "id": "job_001",
  "service": "separation",
  "model": "htdemucs",
  "status": "success",
  "device": "mps",
  "load_time_seconds": 0.0057,
  "separation_time_seconds": 0.983,
  "save_time_seconds": 0.0068,
  "stems": {
    "mix": "/path/to/stems/job_001/mix.wav",
    "vocals": "/path/to/stems/job_001/vocals.wav",
    "drums": "/path/to/stems/job_001/drums.wav",
    "bass": "/path/to/stems/job_001/bass.wav",
    "other": "/path/to/stems/job_001/other.wav"
  },
  "sample_rate": 22050,
  "processing_time_seconds": 1.0053
}
```

## Performance Benchmarks

Tested on Apple M-series (MPS):
- 5-second audio: ~1.0s total processing
- Separation time: ~0.98s
- Load + Save: ~0.01s

Expected performance targets:
- **GPU (CUDA/MPS)**: <30s for 3-minute song
- **CPU**: <2min for 3-minute song

## Technical Details

### Device Selection

The service automatically detects the best available device:

1. CUDA (NVIDIA GPU) - if available
2. MPS (Apple Silicon GPU) - if available
3. CPU - fallback

### Audio Processing

- Automatically converts mono → stereo
- Handles multi-channel audio (uses first 2 channels)
- Output: 16-bit PCM WAV files
- Sample rate: Preserves input sample rate

### Model Architecture

htdemucs (Hybrid Transformer Demucs):
- Combines transformer and convolutional architectures
- Pre-trained on large music dataset
- Best-in-class separation quality
- Stem order: drums, bass, other, vocals

## Troubleshooting

### Import Errors

Make sure PYTHONPATH includes the src directory:

```bash
export PYTHONPATH=/path/to/backend/src:$PYTHONPATH
```

### GPU Not Detected

Check PyTorch installation:

```python
import torch
print(torch.cuda.is_available())  # NVIDIA
print(torch.backends.mps.is_available())  # Apple Silicon
```

### Model Download

On first run, Demucs downloads the htdemucs model (~1GB). This is cached for future use in:
- Linux/Mac: `~/.cache/torch/hub/checkpoints/`
- Windows: `%USERPROFILE%\.cache\torch\hub\checkpoints\`

## Integration with Other Services

The separated stems are used by:

- **Chord Recognition** (`services/chords/`) - Uses bass + other stems
- **Melody Extraction** (`services/melody_bass/`) - Uses vocals + melody stems
- **Song Map Generation** (`services/packager/`) - Orchestrates all services

## Migration from Stub

This implementation replaces the stub that returned the original audio for all stems. The stub behavior is preserved in git history if needed for testing.
