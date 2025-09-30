"""Audio utility functions."""
import librosa
from pathlib import Path


def guess_duration_sec(audio_path: Path) -> float:
    """
    Get audio duration in seconds.

    Args:
        audio_path: Path to audio file

    Returns:
        Duration in seconds
    """
    try:
        duration = librosa.get_duration(path=str(audio_path))
        return float(duration)
    except Exception as e:
        # Fallback: return 0 if cannot determine
        return 0.0
