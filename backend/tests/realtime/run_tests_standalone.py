#!/usr/bin/env python3
"""Standalone test runner for analyzer tests."""
import sys
import os
import numpy as np
import time

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# Direct import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/realtime')))
from analyzer import RealtimeAnalyzer, RingBuffer

print("Performia Real-Time Analyzer Tests")
print("=" * 80)

# Test 1: RingBuffer basic operations
print("\n1. Testing RingBuffer...")
buffer = RingBuffer(size=1024)
data = np.array([1, 2, 3, 4, 5], dtype=np.float32)
buffer.write(data)
result = buffer.read(5)
assert np.allclose(result, data), "RingBuffer basic write/read failed"
print("   PASS: Basic write/read")

# Test 2: Pitch detection at A440
print("\n2. Testing pitch detection at A440...")
analyzer = RealtimeAnalyzer(sample_rate=44100)
t = np.linspace(0, 0.2, int(44100 * 0.2))
audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)

block_size = 512
detected_pitches = []

for i in range(0, len(audio) - block_size, block_size):
    block = audio[i:i + block_size]
    pitch = analyzer.analyze_pitch(block)
    if pitch is not None:
        detected_pitches.append(pitch)

assert len(detected_pitches) > 0, "No pitches detected"
median_pitch = np.median(detected_pitches)
error_cents = 1200 * np.log2(median_pitch / 440.0)
print(f"   Detected: {median_pitch:.2f}Hz, Error: {error_cents:.2f} cents")
assert abs(error_cents) < 10, f"Pitch error {error_cents:.2f} cents exceeds +/- 10 cents"
print("   PASS: Pitch detection within +/- 10 cents")

# Test 3: Onset detection
print("\n3. Testing onset detection...")
analyzer2 = RealtimeAnalyzer(sample_rate=44100)
audio_silence = np.zeros(int(44100 * 0.5), dtype=np.float32)
# Add a click at 0.25s
click_idx = int(0.25 * 44100)
t_click = np.linspace(0, 0.01, 100)
click = np.sin(2 * np.pi * 1000 * t_click) * np.exp(-t_click * 200)
audio_silence[click_idx:click_idx + 100] = click

onset_detected = False
for i in range(0, len(audio_silence) - block_size, block_size):
    block = audio_silence[i:i + block_size]
    if analyzer2.detect_onset(block):
        onset_time = i / 44100
        print(f"   Onset detected at {onset_time:.3f}s (expected 0.250s)")
        latency = abs(onset_time - 0.25)
        assert latency < 0.050, f"Onset latency {latency*1000:.1f}ms exceeds 50ms"
        onset_detected = True
        break

assert onset_detected, "Failed to detect onset"
print("   PASS: Onset detection with <50ms latency")

# Test 4: Performance benchmark
print("\n4. Testing performance (latency)...")
analyzer3 = RealtimeAnalyzer(sample_rate=44100)
t = np.linspace(0, 0.1, 4410)
audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)

latencies = []

# Warm up
for _ in range(5):
    block = audio[:block_size]
    analyzer3.analyze_pitch(block)
    analyzer3.detect_onset(block)

# Measure
for i in range(0, len(audio) - block_size, block_size):
    block = audio[i:i + block_size]
    current_time = i / 44100
    
    start = time.perf_counter()
    pitch = analyzer3.analyze_pitch(block)
    onset = analyzer3.detect_onset(block)
    beat = analyzer3.track_beat(onset, current_time)
    end = time.perf_counter()
    
    latencies.append((end - start) * 1000)

avg_latency = np.mean(latencies)
max_latency = np.max(latencies)

print(f"   Total analysis: avg={avg_latency:.2f}ms, max={max_latency:.2f}ms")
assert avg_latency < 15.0, f"Average latency {avg_latency:.2f}ms exceeds 15ms"
print("   PASS: Average latency <15ms")

print("\n" + "=" * 80)
print("All tests PASSED!")
print("=" * 80)
