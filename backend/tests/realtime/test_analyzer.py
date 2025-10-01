"""
Unit tests for real-time audio analyzer.

Tests pitch detection accuracy, onset detection, beat tracking,
and performance benchmarks.
"""

import pytest
import numpy as np
import time
import os
import sys

# Add src to path for imports
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src'))
sys.path.insert(0, src_path)

from realtime.analyzer import RealtimeAnalyzer, RingBuffer


class TestRingBuffer:
    """Test the RingBuffer implementation."""

    def test_basic_write_read(self):
        """Test basic write and read operations."""
        buffer = RingBuffer(size=1024)

        # Write some data
        data = np.array([1, 2, 3, 4, 5], dtype=np.float32)
        buffer.write(data)

        # Read it back
        result = buffer.read(5)
        np.testing.assert_array_almost_equal(result, data)

    def test_wraparound(self):
        """Test buffer wraparound behavior."""
        buffer = RingBuffer(size=10)

        # Write more than buffer size
        data1 = np.arange(15, dtype=np.float32)
        buffer.write(data1)

        # Should only keep the last 10 samples
        result = buffer.read(10)
        expected = data1[-10:]
        np.testing.assert_array_almost_equal(result, expected)

    def test_multiple_writes(self):
        """Test multiple sequential writes."""
        buffer = RingBuffer(size=20)

        # Write in chunks
        data1 = np.array([1, 2, 3], dtype=np.float32)
        data2 = np.array([4, 5, 6], dtype=np.float32)
        data3 = np.array([7, 8, 9], dtype=np.float32)

        buffer.write(data1)
        buffer.write(data2)
        buffer.write(data3)

        # Read back
        result = buffer.read(9)
        expected = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.float32)
        np.testing.assert_array_almost_equal(result, expected)


class TestPitchDetection:
    """Test pitch detection accuracy."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return RealtimeAnalyzer(sample_rate=44100)

    def generate_sine_wave(self, frequency: float, duration: float = 0.1, sample_rate: int = 44100):
        """Generate a pure sine wave at a specific frequency."""
        t = np.linspace(0, duration, int(sample_rate * duration))
        return np.sin(2 * np.pi * frequency * t).astype(np.float32)

    def test_pitch_detection_a440(self, analyzer):
        """Test pitch detection at A440 (concert A)."""
        # Generate A440 (440 Hz)
        audio = self.generate_sine_wave(440.0, duration=0.2)

        # Process in blocks
        block_size = 512
        detected_pitches = []

        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]
            pitch = analyzer.analyze_pitch(block)
            if pitch is not None:
                detected_pitches.append(pitch)

        # Should detect pitches
        assert len(detected_pitches) > 0, "No pitches detected"

        # Check accuracy (within +/- 10 cents)
        # 10 cents = 0.5946% frequency difference
        median_pitch = np.median(detected_pitches)
        error_cents = 1200 * np.log2(median_pitch / 440.0)

        print(f"A440 test: Detected {median_pitch:.2f}Hz, Error: {error_cents:.2f} cents")
        assert abs(error_cents) < 10, f"Pitch error {error_cents:.2f} cents exceeds +/- 10 cents"

    def test_pitch_detection_c4(self, analyzer):
        """Test pitch detection at middle C (C4 = 261.63 Hz)."""
        # Generate C4
        audio = self.generate_sine_wave(261.63, duration=0.2)

        # Process in blocks
        block_size = 512
        detected_pitches = []

        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]
            pitch = analyzer.analyze_pitch(block)
            if pitch is not None:
                detected_pitches.append(pitch)

        assert len(detected_pitches) > 0, "No pitches detected"

        median_pitch = np.median(detected_pitches)
        error_cents = 1200 * np.log2(median_pitch / 261.63)

        print(f"C4 test: Detected {median_pitch:.2f}Hz, Error: {error_cents:.2f} cents")
        assert abs(error_cents) < 10, f"Pitch error {error_cents:.2f} cents exceeds +/- 10 cents"

    def test_pitch_detection_e4(self, analyzer):
        """Test pitch detection at E4 (329.63 Hz)."""
        audio = self.generate_sine_wave(329.63, duration=0.2)

        block_size = 512
        detected_pitches = []

        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]
            pitch = analyzer.analyze_pitch(block)
            if pitch is not None:
                detected_pitches.append(pitch)

        assert len(detected_pitches) > 0

        median_pitch = np.median(detected_pitches)
        error_cents = 1200 * np.log2(median_pitch / 329.63)

        print(f"E4 test: Detected {median_pitch:.2f}Hz, Error: {error_cents:.2f} cents")
        assert abs(error_cents) < 10

    def test_no_pitch_on_silence(self, analyzer):
        """Test that silence doesn't produce pitch detections."""
        silence = np.zeros(2048, dtype=np.float32)

        pitch = analyzer.analyze_pitch(silence)
        assert pitch is None, "Pitch detected in silence"


class TestOnsetDetection:
    """Test onset detection."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return RealtimeAnalyzer(sample_rate=44100)

    def generate_click_train(self, click_times: list, duration: float = 2.0, sample_rate: int = 44100):
        """Generate a series of clicks at specified times."""
        audio = np.zeros(int(sample_rate * duration), dtype=np.float32)

        for click_time in click_times:
            idx = int(click_time * sample_rate)
            if idx < len(audio) - 100:
                # Generate a short click (100 samples)
                t = np.linspace(0, 0.01, 100)
                click = np.sin(2 * np.pi * 1000 * t) * np.exp(-t * 200)
                audio[idx:idx + 100] += click

        return audio

    def test_onset_detection_single_click(self, analyzer):
        """Test detection of a single onset."""
        # Generate a click at 0.5 seconds
        audio = self.generate_click_train([0.5], duration=1.0)

        block_size = 512
        onset_detected = False

        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]
            if analyzer.detect_onset(block):
                onset_detected = True
                onset_time = i / 44100
                print(f"Onset detected at {onset_time:.3f}s (expected 0.500s)")
                # Check latency (<50ms)
                latency = abs(onset_time - 0.5)
                assert latency < 0.050, f"Onset latency {latency*1000:.1f}ms exceeds 50ms"
                break

        assert onset_detected, "Failed to detect onset"

    def test_onset_detection_multiple_clicks(self, analyzer):
        """Test detection of multiple onsets."""
        # Generate clicks every 0.5 seconds
        click_times = [0.5, 1.0, 1.5, 2.0]
        audio = self.generate_click_train(click_times, duration=2.5)

        block_size = 512
        detected_onsets = []

        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]
            if analyzer.detect_onset(block):
                onset_time = i / 44100
                detected_onsets.append(onset_time)

        print(f"Detected {len(detected_onsets)} onsets (expected {len(click_times)})")

        # Should detect at least 3 of the 4 clicks
        assert len(detected_onsets) >= 3, f"Only detected {len(detected_onsets)} of {len(click_times)} onsets"

    def test_no_onset_on_silence(self, analyzer):
        """Test that silence doesn't produce onset detections."""
        silence = np.zeros(4096, dtype=np.float32)

        block_size = 512
        onsets_detected = 0

        for i in range(0, len(silence) - block_size, block_size):
            block = silence[i:i + block_size]
            if analyzer.detect_onset(block):
                onsets_detected += 1

        assert onsets_detected == 0, f"Detected {onsets_detected} onsets in silence"


class TestBeatTracking:
    """Test beat tracking and tempo estimation."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return RealtimeAnalyzer(sample_rate=44100)

    def generate_metronome(self, tempo_bpm: float, duration: float = 4.0, sample_rate: int = 44100):
        """Generate a metronome click track at specified tempo."""
        audio = np.zeros(int(sample_rate * duration), dtype=np.float32)
        beat_interval = 60.0 / tempo_bpm  # seconds per beat

        current_time = 0.0
        while current_time < duration:
            idx = int(current_time * sample_rate)
            if idx < len(audio) - 100:
                # Generate click
                t = np.linspace(0, 0.01, 100)
                click = np.sin(2 * np.pi * 1000 * t) * np.exp(-t * 200)
                audio[idx:idx + 100] += click

            current_time += beat_interval

        return audio

    def test_tempo_estimation_120bpm(self, analyzer):
        """Test tempo estimation at 120 BPM."""
        audio = self.generate_metronome(tempo_bpm=120.0, duration=4.0)

        block_size = 512
        beat_count = 0
        current_time = 0.0

        # Process audio
        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]
            current_time = i / 44100

            onset = analyzer.detect_onset(block)
            if analyzer.track_beat(onset, current_time):
                beat_count += 1

            # Update tempo estimate periodically
            if i % 2048 == 0:
                analyzer.estimate_tempo(block)

        # After processing, check tempo estimate
        estimated_tempo = analyzer.tempo_estimate

        print(f"120 BPM test: Estimated tempo = {estimated_tempo:.1f} BPM")
        print(f"Detected {beat_count} beats in 4 seconds")

        # Should be within +/- 2 BPM
        assert abs(estimated_tempo - 120.0) < 2.0, f"Tempo error: {abs(estimated_tempo - 120.0):.1f} BPM"

    def test_tempo_estimation_90bpm(self, analyzer):
        """Test tempo estimation at 90 BPM."""
        audio = self.generate_metronome(tempo_bpm=90.0, duration=4.0)

        block_size = 512
        beat_count = 0
        current_time = 0.0

        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]
            current_time = i / 44100

            onset = analyzer.detect_onset(block)
            if analyzer.track_beat(onset, current_time):
                beat_count += 1

            if i % 2048 == 0:
                analyzer.estimate_tempo(block)

        estimated_tempo = analyzer.tempo_estimate

        print(f"90 BPM test: Estimated tempo = {estimated_tempo:.1f} BPM")

        assert abs(estimated_tempo - 90.0) < 2.0


class TestPerformance:
    """Performance benchmarks."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return RealtimeAnalyzer(sample_rate=44100)

    def test_pitch_detection_latency(self, analyzer):
        """Test that pitch detection meets latency requirements (<10ms)."""
        # Generate test signal
        t = np.linspace(0, 0.1, 4410)
        audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)

        block_size = 512
        latencies = []

        # Warm up
        for _ in range(5):
            block = audio[:block_size]
            analyzer.analyze_pitch(block)

        # Measure
        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]

            start = time.perf_counter()
            pitch = analyzer.analyze_pitch(block)
            end = time.perf_counter()

            latencies.append((end - start) * 1000)  # ms

        avg_latency = np.mean(latencies)
        max_latency = np.max(latencies)

        print(f"Pitch detection latency: avg={avg_latency:.2f}ms, max={max_latency:.2f}ms")

        assert avg_latency < 10.0, f"Average latency {avg_latency:.2f}ms exceeds 10ms"

    def test_onset_detection_latency(self, analyzer):
        """Test that onset detection meets latency requirements (<5ms)."""
        # Generate test signal with onset
        t = np.linspace(0, 0.1, 4410)
        audio = np.sin(2 * np.pi * 1000 * t).astype(np.float32)

        block_size = 512
        latencies = []

        # Warm up
        for _ in range(5):
            block = audio[:block_size]
            analyzer.detect_onset(block)

        # Measure
        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]

            start = time.perf_counter()
            onset = analyzer.detect_onset(block)
            end = time.perf_counter()

            latencies.append((end - start) * 1000)

        avg_latency = np.mean(latencies)
        max_latency = np.max(latencies)

        print(f"Onset detection latency: avg={avg_latency:.2f}ms, max={max_latency:.2f}ms")

        assert avg_latency < 5.0, f"Average latency {avg_latency:.2f}ms exceeds 5ms"

    def test_total_analysis_budget(self, analyzer):
        """Test that total analysis meets <15ms average budget."""
        # Generate realistic audio
        t = np.linspace(0, 1.0, 44100)
        audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)

        block_size = 512
        total_latencies = []

        # Warm up
        for _ in range(10):
            block = audio[:block_size]
            analyzer.analyze_pitch(block)
            analyzer.detect_onset(block)

        # Measure complete analysis pipeline
        for i in range(0, len(audio) - block_size, block_size):
            block = audio[i:i + block_size]
            current_time = i / 44100

            start = time.perf_counter()

            # Full analysis
            pitch = analyzer.analyze_pitch(block)
            onset = analyzer.detect_onset(block)
            beat = analyzer.track_beat(onset, current_time)

            end = time.perf_counter()

            total_latencies.append((end - start) * 1000)

        avg_latency = np.mean(total_latencies)
        max_latency = np.max(total_latencies)

        print(f"Total analysis latency: avg={avg_latency:.2f}ms, max={max_latency:.2f}ms")

        assert avg_latency < 15.0, f"Average total latency {avg_latency:.2f}ms exceeds 15ms"


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
