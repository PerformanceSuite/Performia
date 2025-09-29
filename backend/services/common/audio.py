from __future__ import annotations

from pathlib import Path


def guess_duration_sec(wav_path: str | Path) -> float:
    path = Path(wav_path)
    if not path.exists():
        return 0.0
    try:
        import soundfile as sf

        with sf.SoundFile(str(path)) as f:
            return len(f) / float(f.samplerate)
    except Exception:
        return 0.0
