"""Whisper-based ASR service for speech-to-text with timing."""
import os
from typing import Dict, List, Optional
import whisper
import numpy as np


class WhisperService:
    """Wrapper for OpenAI Whisper ASR."""

    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model.

        Args:
            model_size: One of ["tiny", "base", "small", "medium", "large"]
                       - tiny: fastest, least accurate
                       - base: balanced (recommended)
                       - small: better accuracy, slower
                       - medium/large: best accuracy, slowest
        """
        self.model = whisper.load_model(model_size)
        self.model_size = model_size

    def transcribe(
        self,
        audio_path: str,
        language: str = "en",
        word_timestamps: bool = True
    ) -> Dict:
        """
        Transcribe audio file with word-level timing.

        Args:
            audio_path: Path to audio file
            language: Language code (e.g., "en", "es")
            word_timestamps: Whether to return word-level timing

        Returns:
            Dictionary with:
            - text: Full transcription
            - segments: List of segments with timing
            - words: List of words with timing (if word_timestamps=True)
            - language: Detected/specified language
        """
        result = self.model.transcribe(
            audio_path,
            language=language,
            word_timestamps=word_timestamps,
            verbose=False
        )

        # Extract word-level timing if available
        words = []
        if word_timestamps and "segments" in result:
            for segment in result["segments"]:
                if "words" in segment:
                    for word_data in segment["words"]:
                        words.append({
                            "text": word_data.get("word", "").strip(),
                            "start": word_data.get("start", 0.0),
                            "end": word_data.get("end", 0.0),
                            "confidence": word_data.get("probability", 1.0)
                        })

        return {
            "text": result.get("text", ""),
            "segments": result.get("segments", []),
            "words": words,
            "language": result.get("language", language)
        }

    def transcribe_to_phrases(
        self,
        audio_path: str,
        language: str = "en"
    ) -> List[Dict]:
        """
        Transcribe and return phrase-level segments (for Song Map format).

        Args:
            audio_path: Path to audio file
            language: Language code

        Returns:
            List of phrases with format:
            [
                {"text": "word", "start": 0.5, "end": 1.2},
                ...
            ]
        """
        result = self.transcribe(audio_path, language=language, word_timestamps=True)

        phrases = []
        for word in result.get("words", []):
            if word["text"]:  # Skip empty strings
                phrases.append({
                    "text": word["text"],
                    "start": word["start"],
                    "end": word["end"]
                })

        return phrases


# Global instance (loaded once per process)
_whisper_instance: Optional[WhisperService] = None


def get_whisper_service(model_size: str = "base") -> WhisperService:
    """
    Get or create Whisper service instance (singleton pattern).

    Args:
        model_size: Whisper model size

    Returns:
        WhisperService instance
    """
    global _whisper_instance
    if _whisper_instance is None:
        _whisper_instance = WhisperService(model_size)
    return _whisper_instance