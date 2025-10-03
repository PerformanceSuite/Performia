#!/usr/bin/env python3
"""Test script for structure detection service."""
import json
import sys
from pathlib import Path

def validate_structure_output(output_file: str) -> bool:
    """Validate structure detection output against schema."""
    with open(output_file, 'r') as f:
        data = json.load(f)

    # Check required fields
    required_fields = ["id", "service", "sections"]
    for field in required_fields:
        if field not in data:
            print(f"ERROR: Missing required field: {field}")
            return False

    # Validate service name
    if data["service"] != "structure":
        print(f"ERROR: Invalid service name: {data['service']}")
        return False

    # Validate sections
    sections = data["sections"]
    if not isinstance(sections, list):
        print("ERROR: sections must be a list")
        return False

    if len(sections) == 0:
        print("WARNING: No sections detected")

    # Validate each section
    for i, section in enumerate(sections):
        required_section_fields = ["start", "end", "label"]
        for field in required_section_fields:
            if field not in section:
                print(f"ERROR: Section {i} missing field: {field}")
                return False

        # Validate timing
        if section["start"] >= section["end"]:
            print(f"ERROR: Section {i} has invalid timing: start={section['start']}, end={section['end']}")
            return False

        # Validate label
        valid_labels = ["intro", "verse", "chorus", "bridge", "outro"]
        if section["label"] not in valid_labels:
            print(f"WARNING: Section {i} has unusual label: {section['label']}")

        # Check confidence if present
        if "confidence" in section:
            conf = section["confidence"]
            if not (0.0 <= conf <= 1.0):
                print(f"ERROR: Section {i} has invalid confidence: {conf}")
                return False

    # Validate section continuity
    for i in range(len(sections) - 1):
        if sections[i]["end"] != sections[i + 1]["start"]:
            gap = sections[i + 1]["start"] - sections[i]["end"]
            print(f"WARNING: Gap of {gap:.3f}s between section {i} and {i+1}")

    print(f"SUCCESS: Validated {len(sections)} sections")
    print(f"Sections: {[s['label'] for s in sections]}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_structure.py <output_file>")
        sys.exit(1)

    output_file = sys.argv[1]
    if not Path(output_file).exists():
        print(f"ERROR: File not found: {output_file}")
        sys.exit(1)

    if validate_structure_output(output_file):
        print("\nValidation PASSED")
        sys.exit(0)
    else:
        print("\nValidation FAILED")
        sys.exit(1)
