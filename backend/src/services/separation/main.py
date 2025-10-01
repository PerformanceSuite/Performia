#!/usr/bin/env python3
"""
Source Separation Service - Demucs Implementation

Uses the state-of-the-art Demucs hybrid transformer model (htdemucs) to separate
audio into 4 stems: vocals, drums, bass, and other instruments.

PERFORMANCE:
- Target: <30s for 3-minute song on GPU
- Fallback: <2min on CPU
- Supports CUDA (NVIDIA), MPS (Apple Silicon), and CPU

MODEL: htdemucs (Hybrid Transformer Demucs)
- Best quality for music source separation
- 4 stems: drums, bass, other, vocals
- Pre-trained on large music dataset
"""
import argparse
import json
import pathlib
import shutil
import time
import warnings
from typing import Dict

import torch
import torchaudio
import numpy as np

from services.common.utils import write_partial

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

def detect_device() -> str:
    """
    Detect best available device for processing.
    Priority: CUDA (NVIDIA) > MPS (Apple Silicon) > CPU
    """
    if torch.cuda.is_available():
        device = "cuda"
        device_name = torch.cuda.get_device_name(0)
        print(f"Using CUDA GPU: {device_name}")
    elif torch.backends.mps.is_available():
        device = "mps"
        print("Using Apple Silicon GPU (MPS)")
    else:
        device = "cpu"
        print("Using CPU (consider GPU for faster processing)")

    return device

def load_audio(audio_path: pathlib.Path, device: str) -> tuple:
    """
    Load audio file and prepare for Demucs processing.
    Returns (audio_tensor, sample_rate)
    """
    print(f"Loading audio from: {audio_path}")

    # Load audio with torchaudio
    audio, sr = torchaudio.load(str(audio_path))

    print(f"Audio loaded: {audio.shape[1]/sr:.2f}s, {sr}Hz, {audio.shape[0]} channels")

    # Ensure stereo (Demucs expects 2 channels)
    if audio.shape[0] == 1:
        # Mono to stereo
        audio = torch.cat([audio, audio], dim=0)
        print("Converted mono to stereo")
    elif audio.shape[0] > 2:
        # Take first 2 channels
        audio = audio[:2]
        print(f"Reduced {audio.shape[0]} channels to stereo")

    # Move to device
    audio = audio.to(device)

    return audio, sr

def separate_sources(audio: torch.Tensor, device: str) -> torch.Tensor:
    """
    Perform source separation using Demucs htdemucs model.
    Returns tensor of shape [4, 2, samples] for 4 stems (drums, bass, other, vocals)
    """
    print("Loading Demucs htdemucs model...")

    # Import demucs here to catch import errors gracefully
    try:
        from demucs.pretrained import get_model
        from demucs.apply import apply_model
    except ImportError as e:
        raise ImportError(
            "Demucs not installed. Run: pip install demucs\n"
            f"Original error: {e}"
        )

    # Load pre-trained htdemucs model
    model = get_model('htdemucs')
    model.to(device)
    model.eval()

    print(f"Model loaded on {device}. Starting separation...")

    # Apply model
    # Input: [channels, samples]
    # Output: [sources, channels, samples] where sources = [drums, bass, other, vocals]
    with torch.no_grad():
        # Add batch dimension: [1, channels, samples]
        audio_batch = audio.unsqueeze(0)

        # Separate - returns [batch, sources, channels, samples]
        stems = apply_model(model, audio_batch, device=device)

        # Remove batch dimension: [sources, channels, samples]
        stems = stems[0]

    print("Separation complete!")
    return stems

def save_stems(stems: torch.Tensor, sr: int, stems_dir: pathlib.Path,
               original_path: pathlib.Path) -> Dict[str, str]:
    """
    Save separated stems to individual WAV files.
    Returns dict mapping stem names to file paths.
    """
    # Demucs htdemucs output order: drums, bass, other, vocals
    stem_names = ["drums", "bass", "other", "vocals"]
    stem_paths = {}

    print(f"Saving stems to: {stems_dir}")

    # Save original mix
    mix_path = stems_dir / "mix.wav"
    shutil.copyfile(original_path, mix_path)
    stem_paths["mix"] = str(mix_path)
    print(f"  Saved: mix.wav")

    # Save each separated stem
    for idx, name in enumerate(stem_names):
        stem_audio = stems[idx].cpu()  # Move to CPU for saving

        # Ensure audio is in correct range [-1, 1]
        stem_audio = torch.clamp(stem_audio, -1.0, 1.0)

        stem_path = stems_dir / f"{name}.wav"
        torchaudio.save(
            str(stem_path),
            stem_audio,
            sr,
            encoding="PCM_S",
            bits_per_sample=16
        )

        stem_paths[name] = str(stem_path)
        print(f"  Saved: {name}.wav")

    return stem_paths

def main():
    start_time = time.time()

    parser = argparse.ArgumentParser(description="Source Separation with Demucs")
    parser.add_argument("--id", required=True, help="Job ID")
    parser.add_argument("--infile", required=True, help="Input audio file (local path)")
    parser.add_argument("--out", required=True, help="Output folder")
    parser.add_argument("--stems-dir", default="tmp/stems", help="Destination for separated stems")
    args = parser.parse_args()

    payload: Dict[str, object] = {
        "id": args.id,
        "service": "separation",
        "model": "htdemucs",
        "status": "processing"
    }

    try:
        # Setup
        stems_root = pathlib.Path(args.stems_dir).expanduser().resolve()
        stems_dir = stems_root / args.id
        stems_dir.mkdir(parents=True, exist_ok=True)

        src = pathlib.Path(args.infile).expanduser().resolve()

        if not src.exists():
            raise FileNotFoundError(f"Input file not found: {src}")

        payload["source_path"] = str(src)

        # Detect device
        device = detect_device()
        payload["device"] = device

        # Load audio
        load_start = time.time()
        audio, sr = load_audio(src, device)
        load_time = time.time() - load_start
        payload["load_time_seconds"] = round(load_time, 4)

        # Separate sources
        separation_start = time.time()
        stems = separate_sources(audio, device)
        separation_time = time.time() - separation_start
        payload["separation_time_seconds"] = round(separation_time, 4)

        # Save stems
        save_start = time.time()
        stem_paths = save_stems(stems, sr, stems_dir, src)
        save_time = time.time() - save_start
        payload["save_time_seconds"] = round(save_time, 4)

        payload["stems"] = stem_paths
        payload["sample_rate"] = sr
        payload["status"] = "success"

        # Cleanup GPU memory
        del audio, stems
        if device in ["cuda", "mps"]:
            torch.cuda.empty_cache() if device == "cuda" else None

    except Exception as e:
        payload["status"] = "error"
        payload["error"] = str(e)
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

    elapsed_time = time.time() - start_time
    payload["processing_time_seconds"] = round(elapsed_time, 4)

    write_partial(args.out, args.id, "separation", payload)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()
