#!/usr/bin/env python3
"""Test script for Song Map API.

This script tests all three endpoints:
1. POST /api/analyze - Upload audio file
2. GET /api/status/{job_id} - Check progress
3. GET /api/songmap/{job_id} - Download Song Map
"""
import requests
import time
import json
from pathlib import Path

API_BASE = "http://localhost:8000"
TEST_AUDIO = Path(__file__).parent / "test_music.wav"


def test_upload():
    """Test audio file upload."""
    print("=" * 60)
    print("TEST 1: Upload audio file")
    print("=" * 60)

    if not TEST_AUDIO.exists():
        print(f"ERROR: Test audio file not found: {TEST_AUDIO}")
        return None

    with open(TEST_AUDIO, 'rb') as f:
        files = {'file': (TEST_AUDIO.name, f, 'audio/wav')}
        response = requests.post(f"{API_BASE}/api/analyze", files=files)

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        job_id = response.json().get('job_id')
        print(f"\nJob ID: {job_id}")
        return job_id
    else:
        print(f"Upload failed!")
        return None


def test_status(job_id):
    """Test status endpoint."""
    print("\n" + "=" * 60)
    print(f"TEST 2: Check job status")
    print("=" * 60)

    while True:
        response = requests.get(f"{API_BASE}/api/status/{job_id}")
        status_data = response.json()

        print(f"\nStatus: {response.status_code}")
        print(f"Job Status: {status_data.get('status')}")
        print(f"Progress: {status_data.get('progress', 0) * 100:.1f}%")
        print(f"Elapsed: {status_data.get('elapsed', 0):.1f}s")

        if status_data.get('estimated_remaining'):
            print(f"Est. Remaining: {status_data['estimated_remaining']:.1f}s")

        # Check if complete or error
        if status_data.get('status') in ['complete', 'error']:
            if status_data.get('status') == 'error':
                print(f"\nERROR: {status_data.get('error_message')}")
                return False
            print("\nJob complete!")
            return True

        # Wait before next check
        time.sleep(2)


def test_songmap(job_id):
    """Test Song Map download."""
    print("\n" + "=" * 60)
    print(f"TEST 3: Download Song Map")
    print("=" * 60)

    response = requests.get(f"{API_BASE}/api/songmap/{job_id}")

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        song_map = data.get('song_map')

        # Print Song Map summary
        print("\nSong Map Summary:")
        print(f"  ID: {song_map.get('id')}")
        print(f"  Duration: {song_map.get('duration_sec', 0):.1f}s")
        print(f"  Tempo: {song_map.get('tempo', {}).get('bpm_global', 0):.1f} BPM")
        print(f"  Meter: {song_map.get('meter', {}).get('numerator')}/{song_map.get('meter', {}).get('denominator')}")
        print(f"  Beats: {len(song_map.get('beats', []))}")
        print(f"  Chords: {len(song_map.get('chords', []))}")
        print(f"  Lyrics: {len(song_map.get('lyrics', []))}")

        # Save to file
        output_file = Path(f"songmap_{job_id}.json")
        with open(output_file, 'w') as f:
            json.dump(song_map, f, indent=2)
        print(f"\nSaved Song Map to: {output_file}")

        return True
    else:
        print(f"Failed to download Song Map: {response.json()}")
        return False


def test_curl_examples(job_id):
    """Print curl examples for the API."""
    print("\n" + "=" * 60)
    print("CURL EXAMPLES")
    print("=" * 60)

    print("\n1. Upload audio file:")
    print(f"curl -X POST {API_BASE}/api/analyze \\")
    print(f"  -F 'file=@{TEST_AUDIO}' \\")
    print(f"  -H 'accept: application/json'")

    print("\n2. Check job status:")
    print(f"curl {API_BASE}/api/status/{job_id}")

    print("\n3. Download Song Map:")
    print(f"curl {API_BASE}/api/songmap/{job_id}")

    print("\n4. List all jobs:")
    print(f"curl {API_BASE}/api/jobs")

    print("\n5. Health check:")
    print(f"curl {API_BASE}/health")


def main():
    """Run all tests."""
    print("Song Map API Test Suite")
    print("=" * 60)
    print(f"API Base: {API_BASE}")
    print(f"Test Audio: {TEST_AUDIO}")
    print()

    # Check server health
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Server health: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to API server!")
        print(f"Make sure the server is running: python src/services/api/main.py")
        return

    # Test 1: Upload
    job_id = test_upload()
    if not job_id:
        return

    # Test 2: Status polling
    success = test_status(job_id)
    if not success:
        return

    # Test 3: Download Song Map
    test_songmap(job_id)

    # Print curl examples
    test_curl_examples(job_id)

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
