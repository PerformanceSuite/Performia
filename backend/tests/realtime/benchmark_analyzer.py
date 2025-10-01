#!/usr/bin/env python3
"""
Performance benchmarks for real-time audio analyzer.
"""
import sys
import os
import numpy as np
import time

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/realtime')))
from analyzer import RealtimeAnalyzer

def benchmark_pitch_detection():
    """Benchmark pitch detection performance."""
    print("\nBenchmark 1: Pitch Detection Performance")
    print("-" * 60)
    
    analyzer = RealtimeAnalyzer(sample_rate=44100)
    
    # Generate test audio at different frequencies
    frequencies = [130.81, 261.63, 440.0, 880.0, 1046.50]  # C3, C4, A4, A5, C6
    block_size = 512
    
    for freq in frequencies:
        t = np.linspace(0, 0.5, int(44100 * 0.5))
        audio = np.sin(2 * np.pi * freq * t).astype(np.float32)
        
        latencies = []
        detected_pitches = []
        
        # Warm up
        for _ in range(5):
            analyzer.analyze_pitch(audio[:block_size])
        
        # Measure
        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]
            
            start = time.perf_counter()
            pitch = analyzer.analyze_pitch(block)
            end = time.perf_counter()
            
            latencies.append((end - start) * 1000)
            if pitch is not None:
                detected_pitches.append(pitch)
        
        avg_latency = np.mean(latencies)
        p50 = np.percentile(latencies, 50)
        p95 = np.percentile(latencies, 95)
        p99 = np.percentile(latencies, 99)
        
        if detected_pitches:
            median_pitch = np.median(detected_pitches)
            error_cents = 1200 * np.log2(median_pitch / freq)
        else:
            median_pitch = 0
            error_cents = 999
        
        print(f"  {freq:7.2f}Hz: avg={avg_latency:5.2f}ms p50={p50:5.2f}ms "
              f"p95={p95:5.2f}ms p99={p99:5.2f}ms | "
              f"detected={median_pitch:7.2f}Hz error={error_cents:+6.2f}c")
    
    print("  Target: <10ms average latency")

def benchmark_onset_detection():
    """Benchmark onset detection performance."""
    print("\nBenchmark 2: Onset Detection Performance")
    print("-" * 60)
    
    analyzer = RealtimeAnalyzer(sample_rate=44100)
    block_size = 512
    
    # Generate test audio with onsets
    duration = 2.0
    audio = np.zeros(int(44100 * duration), dtype=np.float32)
    
    # Add clicks every 0.25s
    for click_time in np.arange(0.25, duration, 0.25):
        idx = int(click_time * 44100)
        t = np.linspace(0, 0.01, 100)
        click = np.sin(2 * np.pi * 1000 * t) * np.exp(-t * 200)
        audio[idx:idx + 100] += click
    
    latencies = []
    onsets_detected = 0
    
    # Warm up
    for _ in range(5):
        analyzer.detect_onset(audio[:block_size])
    
    # Measure
    for i in range(0, len(audio) - block_size, block_size):
        block = audio[i:i + block_size]
        
        start = time.perf_counter()
        onset = analyzer.detect_onset(block)
        end = time.perf_counter()
        
        latencies.append((end - start) * 1000)
        if onset:
            onsets_detected += 1
    
    avg_latency = np.mean(latencies)
    p50 = np.percentile(latencies, 50)
    p95 = np.percentile(latencies, 95)
    p99 = np.percentile(latencies, 99)
    
    print(f"  Avg: {avg_latency:.2f}ms | P50: {p50:.2f}ms | P95: {p95:.2f}ms | P99: {p99:.2f}ms")
    print(f"  Onsets detected: {onsets_detected} (expected ~7)")
    print("  Target: <5ms average latency")

def benchmark_combined_pipeline():
    """Benchmark complete analysis pipeline."""
    print("\nBenchmark 3: Complete Analysis Pipeline")
    print("-" * 60)
    
    analyzer = RealtimeAnalyzer(sample_rate=44100)
    block_size = 512
    
    # Generate realistic musical audio
    duration = 5.0
    t = np.linspace(0, duration, int(44100 * duration))
    
    # Musical signal: melody with rhythm
    audio = np.zeros_like(t, dtype=np.float32)
    for note_time, freq in [(0.0, 440), (0.5, 494), (1.0, 523), (1.5, 440)]:
        note_start = int(note_time * 44100)
        note_end = note_start + int(0.4 * 44100)
        if note_end > len(audio):
            break
        note_t = np.linspace(0, 0.4, note_end - note_start)
        # ADSR envelope
        envelope = np.concatenate([
            np.linspace(0, 1, 441),  # attack
            np.ones(len(note_t) - 441 - 441),  # sustain
            np.linspace(1, 0, 441)  # release
        ])
        audio[note_start:note_end] += np.sin(2 * np.pi * freq * note_t) * envelope * 0.5
    
    pitch_latencies = []
    onset_latencies = []
    beat_latencies = []
    total_latencies = []
    
    # Warm up
    for _ in range(10):
        block = audio[:block_size]
        analyzer.analyze_pitch(block)
        analyzer.detect_onset(block)
    
    # Measure complete pipeline
    for i in range(0, len(audio) - block_size, block_size):
        block = audio[i:i + block_size]
        current_time = i / 44100
        
        # Measure each component
        start_pitch = time.perf_counter()
        pitch = analyzer.analyze_pitch(block)
        end_pitch = time.perf_counter()
        
        start_onset = time.perf_counter()
        onset = analyzer.detect_onset(block)
        end_onset = time.perf_counter()
        
        start_beat = time.perf_counter()
        beat = analyzer.track_beat(onset, current_time)
        end_beat = time.perf_counter()
        
        pitch_latencies.append((end_pitch - start_pitch) * 1000)
        onset_latencies.append((end_onset - start_onset) * 1000)
        beat_latencies.append((end_beat - start_beat) * 1000)
        total_latencies.append((end_beat - start_pitch) * 1000)
    
    def print_stats(name, latencies, target):
        avg = np.mean(latencies)
        p50 = np.percentile(latencies, 50)
        p95 = np.percentile(latencies, 95)
        p99 = np.percentile(latencies, 99)
        max_lat = np.max(latencies)
        
        status = "PASS" if avg < target else "FAIL"
        print(f"  {name:12s}: avg={avg:5.2f}ms p50={p50:5.2f}ms "
              f"p95={p95:5.2f}ms p99={p99:5.2f}ms max={max_lat:5.2f}ms "
              f"[target <{target}ms] {status}")
    
    print_stats("Pitch", pitch_latencies, 10.0)
    print_stats("Onset", onset_latencies, 5.0)
    print_stats("Beat", beat_latencies, 2.0)
    print_stats("TOTAL", total_latencies, 15.0)
    
    print(f"\n  Blocks processed: {len(total_latencies)}")
    print(f"  Processing time: {sum(total_latencies)/1000:.2f}s")
    print(f"  Audio duration: {duration:.2f}s")
    print(f"  Real-time factor: {duration / (sum(total_latencies)/1000):.2f}x")

def main():
    """Run all benchmarks."""
    print("=" * 80)
    print("Performia Real-Time Analyzer Performance Benchmarks")
    print("=" * 80)
    
    benchmark_pitch_detection()
    benchmark_onset_detection()
    benchmark_combined_pipeline()
    
    print("\n" + "=" * 80)
    print("Benchmarks Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
