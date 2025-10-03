#!/usr/bin/env python3
"""
Comprehensive test suite for melody/bass extraction service.

Tests:
- Pitch tracking accuracy
- Note segmentation
- MIDI output format
- Stem integration
- Performance benchmarks
- Edge cases
"""

import json
import os
import subprocess
import sys
import time
import wave
from io import BytesIO
from pathlib import Path
from typing import List, Dict

import pytest
import numpy as np

# Add backend to path
BACKEND_ROOT = Path(__file__).resolve().parents[3]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from src.services.melody_bass.main import (
    extract_pitch_track,
    segment_notes,
    smooth_and_merge_notes,
    extract_melody_and_bass,
    hz_to_midi,
    get_separation_stems
)


# ==============================================================================
# Helper functions for generating test audio
# ==============================================================================

def generate_sine_wave(frequency_hz: float, duration_sec: float,
                      sample_rate: int = 22050) -> np.ndarray:
    """Generate a sine wave at a specific frequency."""
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec), False)
    wave = np.sin(2 * np.pi * frequency_hz * t)
    return wave.astype(np.float32)


def save_audio_to_wav(audio: np.ndarray, output_path: Path,
                      sample_rate: int = 22050):
    """Save numpy audio array to WAV file."""
    # Normalize to 16-bit int range
    audio_int16 = (audio * 32767).astype(np.int16)

    with wave.open(str(output_path), 'wb') as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)
        wav.writeframes(audio_int16.tobytes())


def generate_test_melody(tmp_path: Path) -> Path:
    """
    Generate a simple test melody with known notes.
    C4 (261.63 Hz) -> E4 (329.63 Hz) -> G4 (392.00 Hz)
    Each note 0.5 seconds
    """
    sr = 22050
    notes = [
        (261.63, 0.5),  # C4
        (329.63, 0.5),  # E4
        (392.00, 0.5),  # G4
    ]

    audio = np.concatenate([generate_sine_wave(freq, dur, sr)
                           for freq, dur in notes])

    output_path = tmp_path / "test_melody.wav"
    save_audio_to_wav(audio, output_path, sr)
    return output_path


def generate_test_bass(tmp_path: Path) -> Path:
    """
    Generate a simple test bass line with known notes.
    E2 (82.41 Hz) -> A2 (110.00 Hz) -> E2 (82.41 Hz)
    Each note 0.5 seconds
    """
    sr = 22050
    notes = [
        (82.41, 0.5),   # E2
        (110.00, 0.5),  # A2
        (82.41, 0.5),   # E2
    ]

    audio = np.concatenate([generate_sine_wave(freq, dur, sr)
                           for freq, dur in notes])

    output_path = tmp_path / "test_bass.wav"
    save_audio_to_wav(audio, output_path, sr)
    return output_path


def generate_silence(tmp_path: Path, duration_sec: float = 2.0) -> Path:
    """Generate silent audio file."""
    sr = 22050
    audio = np.zeros(int(sr * duration_sec), dtype=np.float32)

    output_path = tmp_path / "test_silence.wav"
    save_audio_to_wav(audio, output_path, sr)
    return output_path


def generate_polyphonic(tmp_path: Path) -> Path:
    """
    Generate polyphonic audio (multiple simultaneous pitches).
    Tests algorithm's ability to handle complex audio.
    """
    sr = 22050
    duration = 1.0

    # Mix three frequencies (C4, E4, G4 major chord)
    wave1 = generate_sine_wave(261.63, duration, sr)
    wave2 = generate_sine_wave(329.63, duration, sr)
    wave3 = generate_sine_wave(392.00, duration, sr)

    audio = (wave1 + wave2 + wave3) / 3.0  # Mix and normalize

    output_path = tmp_path / "test_polyphonic.wav"
    save_audio_to_wav(audio, output_path, sr)
    return output_path


# ==============================================================================
# Unit Tests: Core Functions
# ==============================================================================

class TestHzToMidi:
    """Test frequency to MIDI conversion."""

    def test_a440_returns_69(self):
        """A4 (440 Hz) should be MIDI 69."""
        assert hz_to_midi(440.0) == 69

    def test_c4_returns_60(self):
        """C4 (261.63 Hz) should be MIDI 60."""
        assert hz_to_midi(261.63) == 60

    def test_zero_frequency_returns_zero(self):
        """Zero frequency should return 0."""
        assert hz_to_midi(0.0) == 0

    def test_negative_frequency_returns_zero(self):
        """Negative frequency should return 0."""
        assert hz_to_midi(-100.0) == 0

    def test_e2_bass_note(self):
        """E2 (82.41 Hz) should be MIDI 40."""
        assert hz_to_midi(82.41) == 40


class TestPitchTracking:
    """Test pitch tracking with librosa pyin."""

    def test_tracks_single_note(self, tmp_path):
        """Should correctly track a single sustained note."""
        # Generate C4 (261.63 Hz) for 2 seconds (librosa pyin needs longer audio)
        audio_path = tmp_path / "single_note.wav"
        audio = generate_sine_wave(261.63, 2.0, sample_rate=22050)
        save_audio_to_wav(audio, audio_path)

        f0, voiced_probs = extract_pitch_track(audio_path, sr=22050,
                                               fmin=200, fmax=500)

        # Should detect frequencies
        assert len(f0) > 0
        assert len(voiced_probs) > 0

        # Most frames should be voiced
        voiced_ratio = np.sum(voiced_probs > 0.5) / len(voiced_probs)
        assert voiced_ratio > 0.5, f"Only {voiced_ratio:.1%} frames voiced"

        # Median frequency should be close to C4
        valid_f0 = f0[f0 > 0]
        if len(valid_f0) > 0:
            median_freq = np.median(valid_f0)
            midi_note = hz_to_midi(median_freq)
            assert midi_note == 60, f"Expected MIDI 60 (C4), got {midi_note}"

    def test_silence_produces_low_confidence(self, tmp_path):
        """Silence should produce low voiced probabilities."""
        silence_path = generate_silence(tmp_path)
        f0, voiced_probs = extract_pitch_track(silence_path)

        # Should have very few voiced frames
        voiced_ratio = np.sum(voiced_probs > 0.5) / len(voiced_probs)
        assert voiced_ratio < 0.1, f"Silence had {voiced_ratio:.1%} voiced frames"


class TestNoteSegmentation:
    """Test note segmentation from pitch tracks."""

    def test_segments_single_note(self):
        """Should create one note from continuous pitch."""
        # Simulate 1 second of continuous C4 at 22050 Hz, hop_length=512
        # ~43 frames (1.0s / (512/22050))
        num_frames = 43
        f0 = np.full(num_frames, 261.63)  # C4
        voiced_probs = np.full(num_frames, 0.9)

        notes = segment_notes(f0, voiced_probs, hop_length=512, sr=22050,
                            min_duration=0.1, confidence_threshold=0.5)

        assert len(notes) >= 1, "Should detect at least one note"

        note = notes[0]
        assert note["midi"] == 60, f"Expected MIDI 60 (C4), got {note['midi']}"
        assert note["duration"] > 0.5, f"Duration too short: {note['duration']}"
        assert 0.0 <= note["confidence"] <= 1.0
        assert 0 <= note["velocity"] <= 127

    def test_filters_short_notes(self):
        """Should filter out notes shorter than min_duration."""
        # Very short note (2 frames = ~23ms at hop_length=512, sr=22050)
        f0 = np.array([261.63, 261.63])
        voiced_probs = np.array([0.9, 0.9])

        notes = segment_notes(f0, voiced_probs, hop_length=512, sr=22050,
                            min_duration=0.1, confidence_threshold=0.5)

        # Should be filtered out
        assert len(notes) == 0, "Short note should be filtered"

    def test_segments_multiple_notes(self):
        """Should segment multiple distinct notes."""
        # C4 for 20 frames, silence for 5 frames, E4 for 20 frames
        f0 = np.concatenate([
            np.full(20, 261.63),  # C4
            np.zeros(5),          # Silence
            np.full(20, 329.63),  # E4
        ])
        voiced_probs = np.concatenate([
            np.full(20, 0.9),
            np.full(5, 0.1),
            np.full(20, 0.9),
        ])

        notes = segment_notes(f0, voiced_probs, hop_length=512, sr=22050,
                            min_duration=0.1, confidence_threshold=0.5)

        assert len(notes) >= 2, f"Should detect 2 notes, got {len(notes)}"
        assert notes[0]["midi"] == 60  # C4
        assert notes[1]["midi"] == 64  # E4

    def test_filters_low_confidence(self):
        """Should filter notes below confidence threshold."""
        f0 = np.full(20, 261.63)
        voiced_probs = np.full(20, 0.3)  # Low confidence

        notes = segment_notes(f0, voiced_probs, hop_length=512, sr=22050,
                            min_duration=0.1, confidence_threshold=0.5)

        assert len(notes) == 0, "Low confidence note should be filtered"


class TestNoteSmoothingAndMerging:
    """Test note smoothing and merging."""

    def test_merges_close_notes(self):
        """Should merge notes that are close in time and pitch."""
        notes = [
            {"time": 0.0, "midi": 60, "duration": 0.3, "confidence": 0.8, "velocity": 100},
            {"time": 0.35, "midi": 60, "duration": 0.3, "confidence": 0.8, "velocity": 100},
        ]

        smoothed = smooth_and_merge_notes(notes, max_gap=0.15, semitone_threshold=2)

        # Should merge into one longer note
        assert len(smoothed) == 1, f"Should merge into 1 note, got {len(smoothed)}"
        assert smoothed[0]["duration"] >= 0.5, "Merged note should be longer"

    def test_doesnt_merge_distant_pitches(self):
        """Should not merge notes with different pitches."""
        notes = [
            {"time": 0.0, "midi": 60, "duration": 0.3, "confidence": 0.8, "velocity": 100},
            {"time": 0.35, "midi": 67, "duration": 0.3, "confidence": 0.8, "velocity": 100},
        ]

        smoothed = smooth_and_merge_notes(notes, max_gap=0.15, semitone_threshold=2)

        # Should keep separate (7 semitones apart)
        assert len(smoothed) == 2, "Should not merge distant pitches"

    def test_doesnt_merge_distant_times(self):
        """Should not merge notes with large time gaps."""
        notes = [
            {"time": 0.0, "midi": 60, "duration": 0.3, "confidence": 0.8, "velocity": 100},
            {"time": 1.0, "midi": 60, "duration": 0.3, "confidence": 0.8, "velocity": 100},
        ]

        smoothed = smooth_and_merge_notes(notes, max_gap=0.15, semitone_threshold=2)

        # Should keep separate (large gap)
        assert len(smoothed) == 2, "Should not merge distant notes"


# ==============================================================================
# Integration Tests: Full Extraction
# ==============================================================================

class TestMelodyExtraction:
    """Test full melody extraction pipeline."""

    def test_extracts_melody_from_test_audio(self, tmp_path):
        """Should extract melody from generated test audio."""
        melody_path = generate_test_melody(tmp_path)

        melody, _ = extract_melody_and_bass(melody_path, stems_dir=None)

        # Should detect notes
        assert len(melody) > 0, "Should detect melody notes"

        # Check output format
        for note in melody:
            assert "time" in note
            assert "midi" in note
            assert "duration" in note
            assert "velocity" in note
            assert "confidence" in note

            # Validate ranges
            assert note["time"] >= 0.0
            assert 0 < note["duration"] < 10.0
            assert 0 <= note["midi"] <= 127
            assert 0 <= note["velocity"] <= 127
            assert 0.0 <= note["confidence"] <= 1.0

    def test_melody_notes_in_expected_range(self, tmp_path):
        """Melody notes should be in vocal range (C3-C6)."""
        melody_path = generate_test_melody(tmp_path)
        melody, _ = extract_melody_and_bass(melody_path, stems_dir=None)

        for note in melody:
            # C3 = MIDI 48, C6 = MIDI 84
            assert 48 <= note["midi"] <= 84, \
                f"Melody note {note['midi']} outside vocal range"


class TestBassExtraction:
    """Test full bass extraction pipeline."""

    def test_extracts_bass_from_test_audio(self, tmp_path):
        """Should extract bass from generated test audio."""
        bass_path = generate_test_bass(tmp_path)

        _, bass = extract_melody_and_bass(bass_path, stems_dir=None)

        # Should detect notes
        assert len(bass) > 0, "Should detect bass notes"

        # Check output format
        for note in bass:
            assert "time" in note
            assert "midi" in note
            assert "duration" in note
            assert "velocity" in note
            assert "confidence" in note

    def test_bass_notes_in_expected_range(self, tmp_path):
        """Bass notes should be in bass range (E1-E3)."""
        bass_path = generate_test_bass(tmp_path)
        _, bass = extract_melody_and_bass(bass_path, stems_dir=None)

        for note in bass:
            # E1 = MIDI 28, E3 = MIDI 52
            assert 28 <= note["midi"] <= 52, \
                f"Bass note {note['midi']} outside bass range"


class TestStemIntegration:
    """Test integration with separated stems."""

    def test_uses_vocal_stem_when_available(self, tmp_path):
        """Should use vocal stem for melody extraction."""
        # Create stems directory
        stems_dir = tmp_path / "stems"
        stems_dir.mkdir()

        # Generate vocal and bass stems
        vocal_path = generate_test_melody(tmp_path)
        bass_path = generate_test_bass(tmp_path)

        # Copy to stems directory
        (stems_dir / "vocals.wav").write_bytes(vocal_path.read_bytes())
        (stems_dir / "bass.wav").write_bytes(bass_path.read_bytes())

        # Create dummy full mix
        full_mix = tmp_path / "full_mix.wav"
        full_mix.write_bytes(vocal_path.read_bytes())

        melody, bass = extract_melody_and_bass(full_mix, stems_dir=stems_dir)

        assert len(melody) > 0, "Should extract melody from vocal stem"
        assert len(bass) > 0, "Should extract bass from bass stem"

    def test_reads_separation_json(self, tmp_path):
        """Should read stems from separation.json output."""
        # Create output structure
        job_id = "test_sep_001"
        output_dir = tmp_path / "output"
        job_dir = output_dir / job_id
        stems_dir = output_dir / "stems" / job_id

        output_dir.mkdir()
        job_dir.mkdir()
        stems_dir.mkdir(parents=True)

        # Create separation.json
        sep_json = {
            "status": "success",
            "stems": {
                "vocals": str(stems_dir / "vocals.wav"),
                "bass": str(stems_dir / "bass.wav"),
            }
        }
        (job_dir / f"{job_id}.separation.json").write_text(json.dumps(sep_json))

        # Create actual stem files
        vocal_path = generate_test_melody(tmp_path)
        (stems_dir / "vocals.wav").write_bytes(vocal_path.read_bytes())

        # Test get_separation_stems function
        result = get_separation_stems(job_id, str(output_dir))

        assert result is not None, "Should find stems"
        assert result == stems_dir


# ==============================================================================
# Edge Case Tests
# ==============================================================================

class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_handles_silence_gracefully(self, tmp_path):
        """Should handle silent audio without crashing."""
        silence_path = generate_silence(tmp_path)

        melody, bass = extract_melody_and_bass(silence_path, stems_dir=None)

        # Should return empty or very few notes
        assert isinstance(melody, list)
        assert isinstance(bass, list)
        assert len(melody) < 5, "Silence should produce few melody notes"
        assert len(bass) < 5, "Silence should produce few bass notes"

    def test_handles_polyphonic_audio(self, tmp_path):
        """Should handle polyphonic audio without crashing."""
        poly_path = generate_polyphonic(tmp_path)

        melody, bass = extract_melody_and_bass(poly_path, stems_dir=None)

        # Should return some result (may not be accurate)
        assert isinstance(melody, list)
        assert isinstance(bass, list)

    def test_handles_missing_stems_directory(self, tmp_path):
        """Should fallback to full mix if stems missing."""
        audio_path = generate_test_melody(tmp_path)
        non_existent_stems = tmp_path / "nonexistent"

        melody, bass = extract_melody_and_bass(audio_path,
                                              stems_dir=non_existent_stems)

        # Should still work (fallback to full mix)
        assert isinstance(melody, list)
        assert isinstance(bass, list)

    def test_handles_very_short_audio(self, tmp_path):
        """Should handle very short audio (< 1 second)."""
        sr = 22050
        audio = generate_sine_wave(440.0, 0.2, sr)  # 200ms

        short_path = tmp_path / "very_short.wav"
        save_audio_to_wav(audio, short_path, sr)

        melody, bass = extract_melody_and_bass(short_path, stems_dir=None)

        # Should not crash
        assert isinstance(melody, list)
        assert isinstance(bass, list)


# ==============================================================================
# CLI Tests
# ==============================================================================

class TestCLI:
    """Test command-line interface."""

    def test_cli_produces_valid_json(self, tmp_path):
        """Should produce valid JSON output."""
        audio_path = generate_test_melody(tmp_path)
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        cmd = [
            sys.executable,
            "-m",
            "src.services.melody_bass.main",
            "--id", "cli_test",
            "--infile", str(audio_path),
            "--out", str(output_dir),
        ]

        env = os.environ.copy()
        env["PYTHONPATH"] = str(BACKEND_ROOT)

        result = subprocess.run(cmd, capture_output=True, text=True, env=env)

        assert result.returncode == 0, f"CLI failed: {result.stderr}"

        # Should produce JSON output
        output = json.loads(result.stdout)

        assert output["id"] == "cli_test"
        assert output["service"] == "melody_bass"
        assert "performance" in output
        assert "melody" in output["performance"]
        assert "bass" in output["performance"]

    def test_cli_writes_partial_file(self, tmp_path):
        """Should write partial output file."""
        audio_path = generate_test_melody(tmp_path)
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        cmd = [
            sys.executable,
            "-m",
            "src.services.melody_bass.main",
            "--id", "partial_test",
            "--infile", str(audio_path),
            "--out", str(output_dir),
        ]

        env = os.environ.copy()
        env["PYTHONPATH"] = str(BACKEND_ROOT)

        subprocess.run(cmd, check=True, env=env)

        # Check for partial file
        partial_dir = output_dir / "partial_test"
        partial_file = partial_dir / "partial_test.melody_bass.json"

        assert partial_file.exists(), "Partial file not created"

        data = json.loads(partial_file.read_text())
        assert "performance" in data


# ==============================================================================
# Performance Tests (run separately if needed)
# ==============================================================================

@pytest.mark.slow
class TestPerformance:
    """Performance benchmarking tests."""

    def test_processing_speed_3min_audio(self, tmp_path):
        """Should process 3-minute audio in < 10 seconds."""
        # This test requires a real 3-minute audio file
        test_audio = Path("/Users/danielconnolly/Projects/Performia/backend/test_3min.wav")

        if not test_audio.exists():
            pytest.skip("3-minute test audio not available")

        start = time.time()
        melody, bass = extract_melody_and_bass(test_audio, stems_dir=None)
        elapsed = time.time() - start

        print(f"\nProcessing time: {elapsed:.2f}s")
        print(f"Melody notes: {len(melody)}")
        print(f"Bass notes: {len(bass)}")

        assert elapsed < 10.0, f"Too slow: {elapsed:.2f}s (target: < 10s)"

    def test_processing_speed_with_stems(self, tmp_path):
        """Should process faster with pre-separated stems."""
        test_audio = Path("/Users/danielconnolly/Projects/Performia/backend/test_3min.wav")
        stems_dir = Path("/Users/danielconnolly/Projects/Performia/backend/test_output/stems/test_mono")

        if not test_audio.exists() or not stems_dir.exists():
            pytest.skip("Test files not available")

        start = time.time()
        melody, bass = extract_melody_and_bass(test_audio, stems_dir=stems_dir)
        elapsed = time.time() - start

        print(f"\nProcessing time with stems: {elapsed:.2f}s")
        print(f"Melody notes: {len(melody)}")
        print(f"Bass notes: {len(bass)}")

        assert elapsed < 8.0, f"Too slow even with stems: {elapsed:.2f}s"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
