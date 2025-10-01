#!/usr/bin/env python3
"""Unit tests for Song Map validation in packager."""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

from services.packager.main import validate_song_map, build_minimal_song_map


class TestSongMapValidation:
    """Test Song Map schema validation."""

    def test_valid_minimal_song_map_passes(self):
        """Test that a minimal valid song map passes validation."""
        song_map = {
            "id": "test",
            "duration_sec": 180.0,
            "tempo": {"bpm_global": 120.0},
            "beats": [0.5, 1.0, 1.5],
            "downbeats": [0.5, 2.5],
            "meter": {"numerator": 4, "denominator": 4},
            "chords": [],
            "lyrics": []
        }
        is_valid, errors = validate_song_map(song_map)
        assert is_valid, f"Expected valid, got errors: {errors}"
        assert len(errors) == 0

    def test_valid_full_song_map_passes(self):
        """Test that a fully populated song map passes validation."""
        song_map = {
            "id": "full_test",
            "duration_sec": 200.0,
            "tempo": {
                "bpm_global": 128.0,
                "curve": [[0.0, 128.0], [100.0, 130.0]],
                "confidence": 0.9
            },
            "beats": [0.5, 1.0, 1.5, 2.0],
            "downbeats": [0.5, 2.5],
            "meter": {"numerator": 4, "denominator": 4},
            "key": [
                {
                    "start": 0.0,
                    "end": 100.0,
                    "tonic": "C",
                    "mode": "major",
                    "conf": 0.85
                }
            ],
            "chords": [
                {
                    "start": 0.0,
                    "end": 4.0,
                    "label": "C:maj",
                    "conf": 0.8
                }
            ],
            "sections": [
                {
                    "start": 0.0,
                    "end": 50.0,
                    "label": "verse"
                }
            ],
            "lyrics": [
                {
                    "start": 0.5,
                    "end": 1.5,
                    "text": "Hello",
                    "conf": 0.95
                }
            ],
            "performance": {
                "melody": [
                    {
                        "time": 0.5,
                        "midi": 60,
                        "velocity": 100,
                        "duration": 0.5,
                        "confidence": 0.9
                    }
                ],
                "bass": []
            },
            "provenance": {
                "separation": "complete",
                "asr": "complete",
                "harmony": "complete",
                "git_sha": "abc123",
                "created_at": "2025-09-30T00:00:00Z"
            }
        }
        is_valid, errors = validate_song_map(song_map)
        assert is_valid, f"Expected valid, got errors: {errors}"
        assert len(errors) == 0

    def test_missing_required_field_id_fails(self):
        """Test that missing 'id' field fails validation."""
        song_map = {
            # "id": "test",  # Missing
            "duration_sec": 180.0,
            "tempo": {"bpm_global": 120.0},
            "beats": [],
            "downbeats": [],
            "meter": {"numerator": 4, "denominator": 4},
            "chords": [],
            "lyrics": []
        }
        is_valid, errors = validate_song_map(song_map)
        assert not is_valid
        assert len(errors) > 0
        assert "'id' is a required property" in errors[0]

    def test_missing_required_field_tempo_fails(self):
        """Test that missing 'tempo' field fails validation."""
        song_map = {
            "id": "test",
            "duration_sec": 180.0,
            # "tempo": {"bpm_global": 120.0},  # Missing
            "beats": [],
            "downbeats": [],
            "meter": {"numerator": 4, "denominator": 4},
            "chords": [],
            "lyrics": []
        }
        is_valid, errors = validate_song_map(song_map)
        assert not is_valid
        assert len(errors) > 0
        assert "'tempo' is a required property" in errors[0]

    def test_missing_required_field_beats_fails(self):
        """Test that missing 'beats' field fails validation."""
        song_map = {
            "id": "test",
            "duration_sec": 180.0,
            "tempo": {"bpm_global": 120.0},
            # "beats": [],  # Missing
            "downbeats": [],
            "meter": {"numerator": 4, "denominator": 4},
            "chords": [],
            "lyrics": []
        }
        is_valid, errors = validate_song_map(song_map)
        assert not is_valid
        assert len(errors) > 0
        assert "'beats' is a required property" in errors[0]

    def test_invalid_type_duration_fails(self):
        """Test that invalid duration type fails validation."""
        song_map = {
            "id": "test",
            "duration_sec": "not_a_number",  # Should be number
            "tempo": {"bpm_global": 120.0},
            "beats": [],
            "downbeats": [],
            "meter": {"numerator": 4, "denominator": 4},
            "chords": [],
            "lyrics": []
        }
        is_valid, errors = validate_song_map(song_map)
        assert not is_valid
        assert len(errors) > 0

    def test_invalid_meter_structure_fails(self):
        """Test that invalid meter structure fails validation."""
        song_map = {
            "id": "test",
            "duration_sec": 180.0,
            "tempo": {"bpm_global": 120.0},
            "beats": [],
            "downbeats": [],
            "meter": {"numerator": 4},  # Missing denominator
            "chords": [],
            "lyrics": []
        }
        is_valid, errors = validate_song_map(song_map)
        assert not is_valid
        assert len(errors) > 0

    def test_invalid_chord_structure_fails(self):
        """Test that invalid chord structure fails validation."""
        song_map = {
            "id": "test",
            "duration_sec": 180.0,
            "tempo": {"bpm_global": 120.0},
            "beats": [],
            "downbeats": [],
            "meter": {"numerator": 4, "denominator": 4},
            "chords": [
                {
                    "start": 0.0,
                    "end": 4.0
                    # Missing 'label'
                }
            ],
            "lyrics": []
        }
        is_valid, errors = validate_song_map(song_map)
        assert not is_valid
        assert len(errors) > 0

    def test_invalid_lyrics_structure_fails(self):
        """Test that invalid lyrics structure fails validation."""
        song_map = {
            "id": "test",
            "duration_sec": 180.0,
            "tempo": {"bpm_global": 120.0},
            "beats": [],
            "downbeats": [],
            "meter": {"numerator": 4, "denominator": 4},
            "chords": [],
            "lyrics": [
                {
                    "start": 0.0,
                    "end": 1.0
                    # Missing 'text'
                }
            ]
        }
        is_valid, errors = validate_song_map(song_map)
        assert not is_valid
        assert len(errors) > 0

    def test_build_minimal_song_map_is_valid(self):
        """Test that build_minimal_song_map produces valid output."""
        song_map = build_minimal_song_map("test_id", None)
        is_valid, errors = validate_song_map(song_map)
        assert is_valid, f"build_minimal_song_map should produce valid output, got errors: {errors}"
        assert len(errors) == 0
        assert song_map["id"] == "test_id"
        assert song_map["duration_sec"] == 0.0

    def test_invalid_key_structure_fails(self):
        """Test that invalid key structure fails validation."""
        song_map = {
            "id": "test",
            "duration_sec": 180.0,
            "tempo": {"bpm_global": 120.0},
            "beats": [],
            "downbeats": [],
            "meter": {"numerator": 4, "denominator": 4},
            "chords": [],
            "lyrics": [],
            "key": [
                {
                    "start": 0.0,
                    "end": 100.0,
                    "tonic": "C"
                    # Missing 'mode'
                }
            ]
        }
        is_valid, errors = validate_song_map(song_map)
        assert not is_valid
        assert len(errors) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
