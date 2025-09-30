"""Chord recognition using chroma features and template matching."""
import logging
from typing import Dict, List
import librosa
import numpy as np

logging.basicConfig(level=logging.INFO)


class ChordRecognitionService:
    """Basic chord recognition using chroma features."""

    # Major and minor chord templates (12-dimensional chroma vectors)
    CHORD_TEMPLATES = {
        'C': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],   # C major: C E G
        'C#': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # C# major
        'D': [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],   # D major
        'D#': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],  # D# major
        'E': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],   # E major
        'F': [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],   # F major
        'F#': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],  # F# major
        'G': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],   # G major
        'G#': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # G# major
        'A': [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],   # A major
        'A#': [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],  # A# major
        'B': [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],   # B major
        'Cm': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],  # C minor: C Eb G
        'C#m': [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], # C# minor
        'Dm': [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],  # D minor
        'D#m': [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0], # D# minor
        'Em': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],  # E minor
        'Fm': [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],  # F minor
        'F#m': [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0], # F# minor
        'Gm': [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],  # G minor
        'G#m': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], # G# minor
        'Am': [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],  # A minor
        'A#m': [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0], # A# minor
        'Bm': [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1],  # B minor
    }

    def __init__(self):
        """Initialize chord recognition service."""
        self.logger = logging.getLogger(__name__)

        # Convert templates to numpy arrays and normalize
        self.templates = {}
        for name, template in self.CHORD_TEMPLATES.items():
            arr = np.array(template, dtype=float)
            self.templates[name] = arr / np.linalg.norm(arr)

    def analyze_audio(self, audio_path: str, hop_length: float = 0.5) -> Dict:
        """
        Detect chords in audio file.

        Args:
            audio_path: Path to audio file
            hop_length: Time between chord estimates in seconds

        Returns:
            Dictionary with chords list
        """
        self.logger.info(f"Analyzing chords: {audio_path}")

        # Load audio
        y, sr = librosa.load(audio_path, sr=22050)
        duration = librosa.get_duration(y=y, sr=sr)

        # Extract chroma features
        hop_samples = int(hop_length * sr)
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_samples)

        # Detect chord for each frame
        chords = []
        for i in range(chroma.shape[1]):
            frame_chroma = chroma[:, i]

            # Normalize
            if np.sum(frame_chroma) > 0:
                frame_chroma = frame_chroma / np.linalg.norm(frame_chroma)

            # Find best matching chord template
            best_chord = "N"  # No chord
            best_score = 0.0

            for chord_name, template in self.templates.items():
                # Cosine similarity
                score = np.dot(frame_chroma, template)
                if score > best_score:
                    best_score = score
                    best_chord = chord_name

            # Convert to Song Map format (C:maj, Dm:min, etc.)
            if best_chord != "N":
                if 'm' in best_chord:
                    root = best_chord.replace('m', '')
                    quality = 'min'
                else:
                    root = best_chord
                    quality = 'maj'
                label = f"{root}:{quality}"
            else:
                label = "N"

            start_time = i * hop_length
            end_time = min((i + 1) * hop_length, duration)
            confidence = float(best_score)

            chords.append({
                "start": round(start_time, 3),
                "end": round(end_time, 3),
                "label": label,
                "conf": round(confidence, 2)
            })

        # Merge consecutive identical chords
        merged = self._merge_chords(chords)

        self.logger.info(f"Detected {len(merged)} chord segments")
        return {"chords": merged, "duration": duration}

    def _merge_chords(self, chords: List[Dict]) -> List[Dict]:
        """Merge consecutive identical chord labels."""
        if not chords:
            return []

        merged = []
        current = chords[0].copy()

        for chord in chords[1:]:
            if chord["label"] == current["label"]:
                # Extend current chord
                current["end"] = chord["end"]
                current["conf"] = max(current["conf"], chord["conf"])
            else:
                # Save current and start new
                merged.append(current)
                current = chord.copy()

        merged.append(current)
        return merged


# Singleton
_chord_instance = None


def get_chord_service():
    """Get or create chord recognition service instance."""
    global _chord_instance
    if _chord_instance is None:
        _chord_instance = ChordRecognitionService()
    return _chord_instance
