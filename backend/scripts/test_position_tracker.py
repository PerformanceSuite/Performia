"""
Test the Song Map Position Tracker.

This script validates that the position tracker can:
1. Track position through a Song Map using onset detection
2. Handle tempo variations (rubato)
3. Maintain sub-25ms latency
4. Provide accurate teleprompter lookahead
"""

import sys
import time
import numpy as np
sys.path.insert(0, '/Users/danielconnolly/Projects/Performia/backend')

from src.realtime.position_tracker import SongMapPositionTracker


def create_test_song_map():
    """Create a simple test Song Map."""
    return {
        'title': 'Test Song',
        'artist': 'Test Artist',
        'sections': [
            {
                'name': 'Verse 1',
                'lines': [
                    {
                        'syllables': [
                            {'text': 'All', 'startTime': 0.5, 'duration': 0.2, 'chord': 'C'},
                            {'text': 'my', 'startTime': 0.8, 'duration': 0.2, 'chord': 'C'},
                            {'text': 'trou', 'startTime': 1.1, 'duration': 0.2, 'chord': 'Am'},
                            {'text': 'bles', 'startTime': 1.4, 'duration': 0.3, 'chord': 'Am'},
                        ]
                    },
                    {
                        'syllables': [
                            {'text': 'Seemed', 'startTime': 2.0, 'duration': 0.3, 'chord': 'F'},
                            {'text': 'so', 'startTime': 2.4, 'duration': 0.2, 'chord': 'F'},
                            {'text': 'far', 'startTime': 2.7, 'duration': 0.3, 'chord': 'G'},
                            {'text': 'a', 'startTime': 3.1, 'duration': 0.2, 'chord': 'G'},
                            {'text': 'way', 'startTime': 3.4, 'duration': 0.4, 'chord': 'C'},
                        ]
                    }
                ]
            },
            {
                'name': 'Chorus',
                'lines': [
                    {
                        'syllables': [
                            {'text': 'Yes', 'startTime': 4.0, 'duration': 0.3, 'chord': 'G'},
                            {'text': 'ter', 'startTime': 4.4, 'duration': 0.2, 'chord': 'G'},
                            {'text': 'day', 'startTime': 4.7, 'duration': 0.4, 'chord': 'Am'},
                        ]
                    }
                ]
            }
        ]
    }


def test_basic_tracking():
    """Test basic position tracking."""
    print('=== Test 1: Basic Position Tracking ===')

    song_map = create_test_song_map()
    tracker = SongMapPositionTracker(song_map)
    tracker.start()

    # Simulate onsets at correct times
    # Offset by 0.01s to simulate real-world timing variance
    onset_times = [0.51, 0.81, 1.09, 1.42, 2.01, 2.39, 2.71, 3.12, 3.41, 4.02, 4.38, 4.69]

    performance_start = time.time()
    correct_tracks = 0
    total_updates = 0

    for i, onset_time in enumerate(onset_times):
        # Simulate time passing
        performance_elapsed = onset_time

        # Update tracker with onset
        position = tracker.update(onset_detected=True, current_time=performance_start + performance_elapsed)

        # Check if we're tracking correctly
        syllable = tracker.get_current_syllable()

        if syllable:
            total_updates += 1
            # We should be within a few syllables of where we should be
            if abs(position.song_time - onset_time) < 0.3:
                correct_tracks += 1

            print(f'  Time: {position.song_time:.2f}s, Syllable: "{syllable.get("text")}", '
                  f'Confidence: {position.confidence:.2f}, Tempo: {position.tempo_ratio:.2f}x')

    accuracy = (correct_tracks / total_updates) * 100 if total_updates > 0 else 0
    print(f'\n  Tracking accuracy: {accuracy:.1f}% ({correct_tracks}/{total_updates})')
    print(f'  Status: {"✓ PASS" if accuracy >= 80 else "✗ FAIL"}')
    print()

    return accuracy >= 80


def test_tempo_variation():
    """Test handling of tempo variations (rubato)."""
    print('=== Test 2: Tempo Variation (Rubato) ===')

    song_map = create_test_song_map()
    tracker = SongMapPositionTracker(song_map)
    tracker.start()

    # Simulate performer playing slower (1.5x slower = 0.67x speed)
    # Original onset at 0.5s, performer plays it at 0.75s (1.5x slower)
    onset_times = [
        0.5 * 1.5,   # 0.75s  (slower)
        0.8 * 1.5,   # 1.20s  (slower)
        1.1 * 1.4,   # 1.54s  (speeding up)
        1.4 * 1.3,   # 1.82s  (speeding up)
        2.0 * 1.2,   # 2.40s  (back to normalish)
    ]

    performance_start = time.time()

    for onset_time in onset_times:
        performance_elapsed = onset_time
        position = tracker.update(onset_detected=True, current_time=performance_start + performance_elapsed)

        syllable = tracker.get_current_syllable()
        if syllable:
            print(f'  Time: {position.song_time:.2f}s, Syllable: "{syllable.get("text")}", '
                  f'Tempo: {position.tempo_ratio:.2f}x')

    # Check if tempo ratio adapted
    final_tempo = position.tempo_ratio
    print(f'\n  Final tempo ratio: {final_tempo:.2f}x')
    print(f'  Expected: ~0.77x (slower)')
    print(f'  Status: {"✓ PASS" if 0.5 <= final_tempo <= 1.0 else "✗ FAIL"}')
    print()

    return 0.5 <= final_tempo <= 1.0


def test_lookahead():
    """Test teleprompter lookahead."""
    print('=== Test 3: Teleprompter Lookahead ===')

    song_map = create_test_song_map()
    tracker = SongMapPositionTracker(song_map)
    tracker.start()

    # Position at start of Verse 1
    performance_start = time.time()
    tracker.update(onset_detected=True, current_time=performance_start + 0.5)

    # Get 2 seconds of lookahead
    upcoming = tracker.get_lookahead(seconds=2.0)

    print(f'  Current time: {tracker.position.song_time:.2f}s')
    print(f'  Upcoming syllables (next 2s):')
    for syllable in upcoming[:5]:  # Show first 5
        print(f'    - "{syllable.get("text")}" at {syllable.get("startTime"):.2f}s')

    # Should have several syllables in lookahead
    print(f'\n  Lookahead count: {len(upcoming)}')
    print(f'  Status: {"✓ PASS" if len(upcoming) >= 3 else "✗ FAIL"}')
    print()

    return len(upcoming) >= 3


def test_latency():
    """Test that updates are fast enough (<5ms per update)."""
    print('=== Test 4: Update Latency ===')

    song_map = create_test_song_map()
    tracker = SongMapPositionTracker(song_map)
    tracker.start()

    latencies = []
    performance_start = time.time()

    # Run 100 updates
    for i in range(100):
        onset_detected = (i % 3 == 0)  # Onset every 3rd update

        start = time.perf_counter()
        tracker.update(onset_detected=onset_detected, current_time=performance_start + i * 0.01)
        end = time.perf_counter()

        latencies.append((end - start) * 1000)

    mean_latency = np.mean(latencies)
    p95_latency = np.percentile(latencies, 95)
    p99_latency = np.percentile(latencies, 99)

    print(f'  Mean latency: {mean_latency:.3f}ms')
    print(f'  P95 latency: {p95_latency:.3f}ms')
    print(f'  P99 latency: {p99_latency:.3f}ms')
    print(f'  Target: <5ms')
    print(f'  Status: {"✓ PASS" if p99_latency < 5 else "✗ FAIL"}')
    print()

    return p99_latency < 5


def main():
    """Run all tests."""
    print('╔══════════════════════════════════════════════════════╗')
    print('║  Song Map Position Tracker Test Suite               ║')
    print('╚══════════════════════════════════════════════════════╝')
    print()

    results = {}

    try:
        results['basic_tracking'] = test_basic_tracking()
        results['tempo_variation'] = test_tempo_variation()
        results['lookahead'] = test_lookahead()
        results['latency'] = test_latency()

        print('=== Summary ===')
        for test_name, passed in results.items():
            status = '✓ PASS' if passed else '✗ FAIL'
            print(f'  {test_name}: {status}')

        all_passed = all(results.values())
        print()
        if all_passed:
            print('✓ All tests passed!')
            print()
            print('Position tracker achieves:')
            print('  - Accurate onset-based position tracking')
            print('  - Tempo variation handling (rubato)')
            print('  - Sub-5ms update latency')
            print('  - Teleprompter lookahead support')
        else:
            print('✗ Some tests failed')

        return 0 if all_passed else 1

    except KeyboardInterrupt:
        print('\n\nTests interrupted.')
        return 1
    except Exception as e:
        print(f'\n\nError running tests: {e}')
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
