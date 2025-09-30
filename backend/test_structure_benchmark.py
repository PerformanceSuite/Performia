#!/usr/bin/env python3
"""Benchmark structure detection performance."""
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.structure.structure_detection import detect_structure

def benchmark_structure_detection(audio_path: str, iterations: int = 3):
    """Benchmark structure detection performance."""
    print(f"Benchmarking structure detection on: {audio_path}")
    print(f"Running {iterations} iterations...\n")

    times = []

    for i in range(iterations):
        start = time.time()
        sections = detect_structure(audio_path)
        elapsed = time.time() - start
        times.append(elapsed)

        print(f"Iteration {i+1}: {elapsed:.3f}s - {len(sections)} sections detected")

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"\nPerformance Summary:")
    print(f"  Average: {avg_time:.3f}s")
    print(f"  Min: {min_time:.3f}s")
    print(f"  Max: {max_time:.3f}s")

    # Estimate for 3-minute song
    import librosa
    duration = librosa.get_duration(path=audio_path)
    estimated_180s = (avg_time / duration) * 180.0

    print(f"\nEstimated time for 3-minute song: {estimated_180s:.3f}s")

    if estimated_180s < 2.0:
        print("PASS: Performance target met (<2s for 3-minute song)")
        return True
    else:
        print("FAIL: Performance target not met")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_structure_benchmark.py <audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    success = benchmark_structure_detection(audio_path)
    sys.exit(0 if success else 1)
