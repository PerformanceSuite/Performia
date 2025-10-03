"""Beat and key detection service using librosa."""
import logging
from typing import Dict, List, Tuple, Optional
import librosa
import numpy as np

logging.basicConfig(level=logging.INFO)


class BeatsKeyService:
    """Beat tracking and key detection using librosa."""

    def __init__(self):
        """Initialize service."""
        self.logger = logging.getLogger(__name__)

    def analyze_audio(self, audio_path: str) -> Dict:
        """
        Analyze audio for beats, tempo, and key.

        Args:
            audio_path: Path to audio file

        Returns:
            Dictionary with:
            - tempo: Dict with bpm_global, curve, confidence
            - beats: List of beat times in seconds
            - downbeats: List of downbeat times in seconds
            - key: List of key segments with tonic, mode, confidence
        """
        self.logger.info(f"Loading audio: {audio_path}")
        y, sr = librosa.load(audio_path, sr=22050)
        duration = librosa.get_duration(y=y, sr=sr)

        # Beat tracking
        self.logger.info("Detecting beats...")
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='frames')
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        # Tempo curve (simplified - using global tempo)
        tempo_curve = [[0.0, float(tempo)], [duration, float(tempo)]]

        # Downbeat detection (every 4th beat as approximation)
        downbeat_times = beat_times[::4]

        # Key detection
        self.logger.info("Detecting key...")
        key_info = self._detect_key(y, sr)

        return {
            "tempo": {
                "bpm_global": float(tempo),
                "curve": tempo_curve,
                "confidence": 0.8,  # librosa beat tracking is generally reliable
            },
            "beats": [round(float(t), 3) for t in beat_times],
            "downbeats": [round(float(t), 3) for t in downbeat_times],
            "key": [{
                "start": 0.0,
                "end": duration,
                "tonic": key_info["tonic"],
                "mode": key_info["mode"],
                "conf": key_info["confidence"]
            }],
            "duration": duration
        }

    def _detect_key(self, y: np.ndarray, sr: int) -> Dict:
        """
        Detect musical key using chroma features.

        Args:
            y: Audio time series
            sr: Sample rate

        Returns:
            Dict with tonic, mode, confidence
        """
        # Extract chroma features
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

        # Average chroma across time
        chroma_mean = np.mean(chroma, axis=1)

        # Key profiles (Krumhansl-Schmuckler)
        major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

        # Normalize
        major_profile = major_profile / np.sum(major_profile)
        minor_profile = minor_profile / np.sum(minor_profile)
        chroma_mean = chroma_mean / np.sum(chroma_mean)

        # Correlate with all 24 keys
        pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        max_corr = -1
        best_key = "C"
        best_mode = "major"

        for shift in range(12):
            shifted_chroma = np.roll(chroma_mean, shift)

            # Major correlation
            major_corr = np.corrcoef(shifted_chroma, major_profile)[0, 1]
            if major_corr > max_corr:
                max_corr = major_corr
                best_key = pitch_classes[shift]
                best_mode = "major"

            # Minor correlation
            minor_corr = np.corrcoef(shifted_chroma, minor_profile)[0, 1]
            if minor_corr > max_corr:
                max_corr = minor_corr
                best_key = pitch_classes[shift]
                best_mode = "minor"

        # Map correlation to confidence (0.5-0.95 range)
        confidence = min(0.95, max(0.5, (max_corr + 1) / 2))

        return {
            "tonic": best_key,
            "mode": best_mode,
            "confidence": round(float(confidence), 2)
        }


# Singleton pattern
_beats_key_instance: Optional[BeatsKeyService] = None


def get_beats_key_service() -> BeatsKeyService:
    """Get or create BeatsKeyService instance."""
    global _beats_key_instance
    if _beats_key_instance is None:
        _beats_key_instance = BeatsKeyService()
    return _beats_key_instance