#!/usr/bin/env python3
"""Generate a small sine-wave demo file for local pipeline testing."""
import argparse
import math
import wave
from pathlib import Path

SAMPLE_RATE = 44100
FREQUENCY = 440.0
AMPLITUDE = 0.3
DURATION_SEC = 2.0


def write_demo_wav(path: Path) -> None:
    total_frames = int(SAMPLE_RATE * DURATION_SEC)
    path.parent.mkdir(parents=True, exist_ok=True)

    with wave.open(str(path), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        for i in range(total_frames):
            sample = AMPLITUDE * math.sin(2 * math.pi * FREQUENCY * (i / SAMPLE_RATE))
            value = max(-1.0, min(1.0, sample))
            wav.writeframesraw(int(value * 32767).to_bytes(2, byteorder="little", signed=True))

        wav.writeframes(b"")  # flush frame count to header


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate demo WAV audio for local testing.")
    parser.add_argument(
        "--out",
        default="tmp/raw/demo.wav",
        help="Output WAV path relative to repo root (default: tmp/raw/demo.wav)",
    )
    args = parser.parse_args()

    dest = Path(args.out).expanduser().resolve()
    write_demo_wav(dest)
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
