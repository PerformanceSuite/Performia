#!/usr/bin/env python3
"""
Example API usage - demonstrates all endpoints in sequence.
"""
import requests
import time

API_BASE = "http://localhost:8000"

def example_workflow(audio_file_path):
    """Complete workflow example."""
    
    print("=== Performia Song Map API Example ===\n")
    
    # 1. Upload audio file
    print("1. Uploading audio file...")
    with open(audio_file_path, 'rb') as f:
        response = requests.post(
            f"{API_BASE}/api/analyze",
            files={'file': f}
        )
    
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return
    
    job_data = response.json()
    job_id = job_data['job_id']
    print(f"   Job created: {job_id}\n")
    
    # 2. Monitor progress
    print("2. Monitoring progress...")
    while True:
        response = requests.get(f"{API_BASE}/api/status/{job_id}")
        status = response.json()
        
        print(f"   Status: {status['status']} | Progress: {status['progress']*100:.0f}% | Elapsed: {status['elapsed']:.1f}s")
        
        if status['status'] == 'complete':
            print("   Analysis complete!\n")
            break
        elif status['status'] == 'error':
            print(f"   Error: {status['error_message']}\n")
            return
        
        time.sleep(1)
    
    # 3. Retrieve Song Map
    print("3. Retrieving Song Map...")
    response = requests.get(f"{API_BASE}/api/songmap/{job_id}")
    
    if response.status_code == 200:
        data = response.json()
        song_map = data['song_map']
        
        print(f"   Duration: {song_map['duration_sec']}s")
        print(f"   Tempo: {song_map['tempo']['bpm_global']:.1f} BPM")
        print(f"   Key: {song_map['key'][0]['tonic']} {song_map['key'][0]['mode']}")
        print(f"   Beats: {len(song_map['beats'])}")
        print(f"   Chords: {len(song_map['chords'])}")
        print(f"\n   Song Map ready for Living Chart!\n")
    else:
        print(f"   Error retrieving Song Map: {response.text}\n")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
    else:
        audio_file = "test_music.wav"
    
    example_workflow(audio_file)
