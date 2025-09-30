#!/usr/bin/env python3
"""
Song Map Schema Validator

Validates Song Map JSON files against the official schema.
Reports detailed validation results and schema mismatches.

Usage:
    python validate_song_map.py <song_map_file>
    python validate_song_map.py --all  # Validate all Song Maps in test_output/
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from jsonschema import validate, ValidationError, Draft7Validator
from jsonschema.exceptions import SchemaError


class SongMapValidator:
    """Validates Song Map JSON files against the schema."""

    def __init__(self, schema_path: Path):
        """Initialize validator with schema."""
        self.schema_path = schema_path
        self.schema = self._load_schema()
        self.validator = Draft7Validator(self.schema)

    def _load_schema(self) -> Dict:
        """Load the Song Map schema."""
        try:
            with open(self.schema_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERROR: Schema file not found: {self.schema_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in schema file: {e}")
            sys.exit(1)

    def _load_song_map(self, song_map_path: Path) -> Dict:
        """Load a Song Map JSON file."""
        try:
            with open(song_map_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERROR: Song Map file not found: {song_map_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in Song Map file: {e}")
            return None

    def validate_song_map(self, song_map_path: Path) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a Song Map against the schema.

        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        song_map = self._load_song_map(song_map_path)
        if song_map is None:
            return False, [f"Failed to load Song Map: {song_map_path}"], []

        errors = []
        warnings = []

        # Validate against schema
        try:
            self.validator.validate(song_map)
            is_valid = True
        except ValidationError as e:
            is_valid = False
            errors.append(self._format_validation_error(e))

            # Collect all validation errors
            for error in self.validator.iter_errors(song_map):
                error_msg = self._format_validation_error(error)
                if error_msg not in errors:
                    errors.append(error_msg)

        # Additional semantic validation
        semantic_issues = self._semantic_validation(song_map)
        warnings.extend(semantic_issues)

        return is_valid, errors, warnings

    def _format_validation_error(self, error: ValidationError) -> str:
        """Format a validation error for display."""
        path = " -> ".join(str(p) for p in error.absolute_path) if error.absolute_path else "root"
        return f"Field: {path}\n  Error: {error.message}\n  Value: {error.instance}"

    def _semantic_validation(self, song_map: Dict) -> List[str]:
        """Perform semantic validation beyond schema checking."""
        warnings = []

        # Check if duration_sec matches actual data
        if "duration_sec" in song_map:
            duration = song_map["duration_sec"]

            # Check beats don't exceed duration
            if "beats" in song_map and song_map["beats"]:
                max_beat = max(song_map["beats"])
                if max_beat > duration:
                    warnings.append(f"Beat time {max_beat}s exceeds duration {duration}s")

            # Check downbeats don't exceed duration
            if "downbeats" in song_map and song_map["downbeats"]:
                max_downbeat = max(song_map["downbeats"])
                if max_downbeat > duration:
                    warnings.append(f"Downbeat time {max_downbeat}s exceeds duration {duration}s")

            # Check chords don't exceed duration
            if "chords" in song_map:
                for i, chord in enumerate(song_map["chords"]):
                    if chord["end"] > duration:
                        warnings.append(f"Chord {i} end time {chord['end']}s exceeds duration {duration}s")

        # Check downbeats are subset of beats
        if "beats" in song_map and "downbeats" in song_map:
            beats = set(song_map["beats"])
            downbeats = set(song_map["downbeats"])
            non_beat_downbeats = downbeats - beats
            if non_beat_downbeats:
                warnings.append(f"Downbeats not in beats list: {sorted(non_beat_downbeats)}")

        # Check chord time ranges
        if "chords" in song_map:
            for i, chord in enumerate(song_map["chords"]):
                if chord["start"] > chord["end"]:
                    warnings.append(f"Chord {i} has start > end: {chord['start']} > {chord['end']}")
                if chord["start"] == chord["end"]:
                    warnings.append(f"Chord {i} has zero duration: {chord}")

        # Check section time ranges
        if "sections" in song_map:
            for i, section in enumerate(song_map["sections"]):
                if section["start"] > section["end"]:
                    warnings.append(f"Section {i} has start > end: {section['start']} > {section['end']}")

        # Check lyrics time ranges
        if "lyrics" in song_map:
            for i, lyric in enumerate(song_map["lyrics"]):
                if lyric["start"] > lyric["end"]:
                    warnings.append(f"Lyric {i} has start > end: {lyric['start']} > {lyric['end']}")

        # Check key time ranges
        if "key" in song_map:
            for i, key in enumerate(song_map["key"]):
                if key["start"] > key["end"]:
                    warnings.append(f"Key {i} has start > end: {key['start']} > {key['end']}")

        # Check confidence values are in [0, 1]
        if "tempo" in song_map and "confidence" in song_map["tempo"]:
            conf = song_map["tempo"]["confidence"]
            if conf < 0 or conf > 1:
                warnings.append(f"Tempo confidence out of range [0,1]: {conf}")

        if "chords" in song_map:
            for i, chord in enumerate(song_map["chords"]):
                if "conf" in chord:
                    conf = chord["conf"]
                    if conf < 0 or conf > 1:
                        warnings.append(f"Chord {i} confidence out of range [0,1]: {conf}")

        # Check for empty required arrays
        if "lyrics" in song_map and len(song_map["lyrics"]) == 0:
            warnings.append("Lyrics array is empty - no lyrics detected")

        # Check sections field vs schema (schema has confidence, but not required)
        if "sections" in song_map:
            for i, section in enumerate(song_map["sections"]):
                if "confidence" in section:
                    # Schema doesn't define confidence field for sections
                    warnings.append(f"Section {i} has 'confidence' field not defined in schema")

        return warnings

    def print_report(self, song_map_path: Path, is_valid: bool, errors: List[str], warnings: List[str]):
        """Print a formatted validation report."""
        print(f"\n{'='*80}")
        print(f"VALIDATION REPORT: {song_map_path.name}")
        print(f"{'='*80}")

        if is_valid:
            print(f"✓ VALID - Song Map passes schema validation")
        else:
            print(f"✗ INVALID - Song Map fails schema validation")

        if errors:
            print(f"\nERRORS ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                print(f"\n{i}. {error}")

        if warnings:
            print(f"\nWARNINGS ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. {warning}")
        else:
            print(f"\nNo warnings detected.")

        print(f"\n{'='*80}\n")


def main():
    """Main entry point."""
    # Get paths
    backend_dir = Path(__file__).parent
    schema_path = backend_dir / "schemas" / "song_map.schema.json"
    test_output_dir = backend_dir / "test_output"

    # Initialize validator
    validator = SongMapValidator(schema_path)

    # Determine which files to validate
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Validate all Song Map files
        song_map_files = list(test_output_dir.glob("*.song_map.json"))
        if not song_map_files:
            print(f"No Song Map files found in {test_output_dir}")
            sys.exit(1)
    elif len(sys.argv) > 1:
        # Validate specific file
        song_map_files = [Path(sys.argv[1])]
    else:
        # Default to the complete_test Song Map
        song_map_files = [test_output_dir / "complete_test.song_map.json"]

    # Validate each file
    total_valid = 0
    total_invalid = 0

    for song_map_file in song_map_files:
        is_valid, errors, warnings = validator.validate_song_map(song_map_file)
        validator.print_report(song_map_file, is_valid, errors, warnings)

        if is_valid:
            total_valid += 1
        else:
            total_invalid += 1

    # Print summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total files validated: {len(song_map_files)}")
    print(f"Valid: {total_valid}")
    print(f"Invalid: {total_invalid}")
    print(f"{'='*80}\n")

    # Exit with appropriate code
    sys.exit(0 if total_invalid == 0 else 1)


if __name__ == "__main__":
    main()
