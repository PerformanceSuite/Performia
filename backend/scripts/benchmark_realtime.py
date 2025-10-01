"""
Benchmark the existing Python real-time system to measure actual latency.

This script measures:
1. Audio input latency
2. Analysis latency (pitch, onset, beat)
3. Total round-trip latency estimate
"""

import time
import numpy as np
import sys
sys.path.insert(0, '/Users/danielconnolly/Projects/Performia/backend')

from src.realtime.audio_input import RealtimeAudioInput
from src.realtime.analyzer import RealtimeAnalyzer


def benchmark_audio_input():
    """Benchmark audio input latency."""
    print('=== Test 1: Audio Input Latency ===')

    with RealtimeAudioInput(block_size=512) as audio_input:
        # Consume blocks to prevent queue from filling
        for _ in range(200):
            try:
                audio_input.get_block(timeout=0.1)
            except:
                break

        stats = audio_input.get_stats()

        # Calculate latency from block size
        latency_ms = (stats['block_size'] / stats['sample_rate']) * 1000

        print(f'  Block size: {stats["block_size"]} samples')
        print(f'  Latency: {latency_ms:.2f}ms')
        print(f'  Blocks captured: {stats["blocks_captured"]}')
        print(f'  Blocks dropped: {stats["blocks_dropped"]}')
        print(f'  Drop rate: {stats.get("drop_rate", 0):.2f}%')
        print()

        return latency_ms


def benchmark_analysis():
    """Benchmark audio analysis latency."""
    print('=== Test 2: Audio Analysis Latency ===')

    analyzer = RealtimeAnalyzer(sample_rate=44100)
    test_audio = np.random.randn(512).astype(np.float32) * 0.1  # Quiet signal

    # Warm up
    for _ in range(10):
        analyzer.analyze_pitch(test_audio)
        analyzer.detect_onset(test_audio)

    # Benchmark pitch detection
    pitch_latencies = []
    for _ in range(100):
        start = time.perf_counter()
        pitch = analyzer.analyze_pitch(test_audio)
        end = time.perf_counter()
        pitch_latencies.append((end - start) * 1000)

    # Benchmark onset detection
    onset_latencies = []
    for _ in range(100):
        start = time.perf_counter()
        onset = analyzer.detect_onset(test_audio)
        end = time.perf_counter()
        onset_latencies.append((end - start) * 1000)

    print('Pitch Detection:')
    print(f'  Mean: {np.mean(pitch_latencies):.2f}ms')
    print(f'  Min: {np.min(pitch_latencies):.2f}ms')
    print(f'  Max: {np.max(pitch_latencies):.2f}ms')
    print(f'  P95: {np.percentile(pitch_latencies, 95):.2f}ms')
    print(f'  P99: {np.percentile(pitch_latencies, 99):.2f}ms')
    print()

    print('Onset Detection:')
    print(f'  Mean: {np.mean(onset_latencies):.2f}ms')
    print(f'  Min: {np.min(onset_latencies):.2f}ms')
    print(f'  Max: {np.max(onset_latencies):.2f}ms')
    print(f'  P95: {np.percentile(onset_latencies, 95):.2f}ms')
    print(f'  P99: {np.percentile(onset_latencies, 99):.2f}ms')
    print()

    return {
        'pitch_mean': np.mean(pitch_latencies),
        'onset_mean': np.mean(onset_latencies)
    }


def benchmark_total_latency(input_latency, analysis_latency):
    """Calculate total round-trip latency estimate."""
    print('=== Test 3: Estimated Total Round-Trip Latency ===')

    # For Song Map position tracking, we only need onset detection
    # not continuous pitch detection
    onset_latency = analysis_latency['onset_mean']

    # Estimated output latency (symmetric with input)
    output_latency = input_latency

    total = input_latency + onset_latency + output_latency

    print(f'  Audio input: {input_latency:.2f}ms')
    print(f'  Onset detection: {onset_latency:.2f}ms')
    print(f'  Audio output: {output_latency:.2f}ms')
    print(f'  Total (onset-based): {total:.2f}ms')
    print()

    print('Targets:')
    print(f'  Sub-10ms (original target): {"✗ EXCEEDS" if total > 10 else "✓ MEETS"}')
    print(f'  20-30ms (committee target): {"✗ EXCEEDS" if total > 30 else "✓ MEETS"}')
    print()

    # Show pitch-based latency for comparison
    pitch_latency = analysis_latency['pitch_mean']
    total_pitch = input_latency + pitch_latency + output_latency
    print(f'For comparison, with continuous pitch detection:')
    print(f'  Total (pitch-based): {total_pitch:.2f}ms')
    print()

    return total


def main():
    """Run all benchmarks."""
    print('╔══════════════════════════════════════════════════════╗')
    print('║  Python Real-Time System Benchmark                  ║')
    print('║  Committee Recommendation: Song Map Position Tracker ║')
    print('╚══════════════════════════════════════════════════════╝')
    print()

    try:
        # Run benchmarks
        input_latency = benchmark_audio_input()
        analysis_latency = benchmark_analysis()
        total_latency = benchmark_total_latency(input_latency, analysis_latency)

        print('=== Summary ===')
        print(f'Current Python system achieves {total_latency:.2f}ms total latency')
        print(f'with onset-based position tracking (recommended approach).')
        print()
        print('Next Steps (per committee recommendation):')
        print('  1. Build Song Map position tracker using onset detection')
        print('  2. Optimize with smaller buffer sizes (256 or 128 samples)')
        print('  3. Add Numba JIT compilation to hot paths')
        print('  4. Target: 15-25ms total latency')

    except KeyboardInterrupt:
        print('\n\nBenchmark interrupted.')
    except Exception as e:
        print(f'\n\nError running benchmark: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
