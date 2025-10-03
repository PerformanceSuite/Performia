#!/usr/bin/env python3
"""
Quick integration test for melody/bass service with full pipeline.
"""

import json
import subprocess
import sys
from pathlib import Path
import time

def test_cli_standalone():
    """Test CLI produces valid output."""
    print("\n=== Testing CLI Standalone ===")

    cmd = [
        sys.executable,
        "-m", "src.services.melody_bass.main",
        "--id", "integration_test",
        "--infile", "test_3min.wav",
        "--out", "test_output/"
    ]

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start

    print(f"Exit code: {result.returncode}")
    print(f"Processing time: {elapsed:.2f}s")

    if result.returncode == 0:
        output = json.loads(result.stdout)
        print(f"Melody notes: {len(output['performance']['melody'])}")
        print(f"Bass notes: {len(output['performance']['bass'])}")

        # Check partial file
        partial = Path("test_output/integration_test/integration_test.melody_bass.json")
        if partial.exists():
            print(f"✓ Partial file created: {partial}")
        else:
            print(f"✗ Partial file missing")

        return True
    else:
        print(f"✗ CLI failed: {result.stderr}")
        return False


def test_with_stems():
    """Test with pre-separated stems."""
    print("\n=== Testing with Stems ===")

    # Create separation.json pointing to stems
    test_dir = Path("test_output/stem_test")
    test_dir.mkdir(parents=True, exist_ok=True)

    sep_json = {
        "status": "success",
        "stems": {
            "vocals": "test_output/stems/test_mono/vocals.wav",
            "bass": "test_output/stems/test_mono/bass.wav"
        }
    }

    sep_file = test_dir / "stem_test.separation.json"
    sep_file.write_text(json.dumps(sep_json, indent=2))

    cmd = [
        sys.executable,
        "-m", "src.services.melody_bass.main",
        "--id", "stem_test",
        "--infile", "test_3min.wav",
        "--out", "test_output/"
    ]

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start

    print(f"Processing time with stems: {elapsed:.2f}s")

    if result.returncode == 0:
        output = json.loads(result.stdout)
        print(f"Melody notes: {len(output['performance']['melody'])}")
        print(f"Bass notes: {len(output['performance']['bass'])}")
        return True
    else:
        print(f"✗ Failed: {result.stderr}")
        return False


def check_output_format():
    """Verify output format matches expected schema."""
    print("\n=== Checking Output Format ===")

    partial = Path("test_output/integration_test/integration_test.melody_bass.json")
    if not partial.exists():
        print("✗ No output file to check")
        return False

    data = json.loads(partial.read_text())

    required_fields = ["id", "service", "performance", "duration_sec"]
    for field in required_fields:
        if field in data:
            print(f"✓ Has field: {field}")
        else:
            print(f"✗ Missing field: {field}")
            return False

    # Check performance structure
    perf = data.get("performance", {})
    if "melody" in perf and "bass" in perf:
        print(f"✓ Has melody and bass in performance")

        # Check note format
        for note in perf["melody"][:3]:  # Check first 3 notes
            required = ["time", "midi", "duration", "velocity", "confidence"]
            if all(k in note for k in required):
                print(f"✓ Note has all required fields: {note}")
            else:
                print(f"✗ Note missing fields: {note}")
                return False
    else:
        print(f"✗ Performance missing melody or bass")
        return False

    return True


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("MELODY/BASS SERVICE INTEGRATION TEST")
    print("=" * 60)

    results = []

    # Test 1: CLI standalone
    results.append(("CLI Standalone", test_cli_standalone()))

    # Test 2: With stems
    results.append(("With Stems", test_with_stems()))

    # Test 3: Output format
    results.append(("Output Format", check_output_format()))

    # Summary
    print("\n" + "=" * 60)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 60)

    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8} {name}")

    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
