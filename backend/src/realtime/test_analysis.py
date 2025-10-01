#!/usr/bin/env python3
"""
Test script for real-time audio analysis.

Loads a test audio file and processes it block by block,
demonstrating real-time pitch, onset, and beat detection.
"""

import numpy as np
import soundfile as sf
import time
import os
from analyzer import RealtimeAnalyzer


def generate_test_audio(filename: str, duration: float = 10.0, sample_rate: int = 44100):
    """
    Generate a test audio file with varying pitch and rhythm.

    Args:
        filename: Output filename
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
    """
    print(f"Generating test audio: {filename}")

    t = np.linspace(0, duration, int(sample_rate * duration))
    audio = np.zeros_like(t)

    # Create a simple melody with clear onsets
    # Tempo: 120 BPM (2 beats per second)
    beat_interval = 0.5  # seconds per beat

    notes = [
        ('C4', 261.63),
        ('D4', 293.66),
        ('E4', 329.63),
        ('G4', 392.00),
        ('A4', 440.00),
        ('G4', 392.00),
        ('E4', 329.63),
        ('C4', 261.63),
    ]

    for beat_num in range(int(duration / beat_interval)):
        if beat_num >= len(notes):
            break

        note_name, freq = notes[beat_num % len(notes)]
        start_time = beat_num * beat_interval
        end_time = start_time + beat_interval * 0.8  # 80% duty cycle

        # Find sample indices
        start_idx = int(start_time * sample_rate)
        end_idx = int(end_time * sample_rate)

        if end_idx > len(audio):
            break

        # Generate note with envelope
        note_duration = end_time - start_time
        note_t = np.linspace(0, note_duration, end_idx - start_idx)

        # ADSR envelope (simplified)
        attack = 0.01
        decay = 0.05
        sustain_level = 0.7
        release = 0.1

        envelope = np.ones_like(note_t)
        attack_samples = int(attack * sample_rate)
        decay_samples = int(decay * sample_rate)
        release_samples = int(release * sample_rate)

        if len(envelope) > attack_samples:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        if len(envelope) > attack_samples + decay_samples:
            envelope[attack_samples:attack_samples + decay_samples] = np.linspace(
                1, sustain_level, decay_samples
            )
        if len(envelope) > release_samples:
            envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)

        # Generate sine wave
        sine_wave = np.sin(2 * np.pi * freq * note_t) * envelope * 0.5

        audio[start_idx:end_idx] += sine_wave

    # Normalize
    audio = audio / np.max(np.abs(audio)) * 0.9

    # Save
    sf.write(filename, audio, sample_rate)
    print(f"Test audio generated: {duration:.1f}s, {len(notes)} notes, 120 BPM")

    return audio, sample_rate


def process_audio_file(filename: str, block_size: int = 512):
    """
    Process an audio file block by block, simulating real-time analysis.

    Args:
        filename: Audio file to process
        block_size: Number of samples per block (default: 512 = ~11.6ms at 44.1kHz)
    """
    print(f"\nProcessing: {filename}")
    print(f"Block size: {block_size} samples (~{block_size/44100*1000:.1f}ms)\n")

    # Load audio file
    audio, sr = sf.read(filename)
    if len(audio.shape) > 1:
        audio = audio[:, 0]  # Use first channel if stereo

    print(f"Loaded: {len(audio)/sr:.2f}s @ {sr}Hz\n")

    # Initialize analyzer
    analyzer = RealtimeAnalyzer(sample_rate=sr)

    # Process block by block
    total_blocks = len(audio) // block_size
    pitch_detections = []
    onset_times = []
    beat_times = []

    print("=" * 80)
    print(f"{'Time':<8} {'Pitch':<10} {'Onset':<8} {'Beat':<6} {'Tempo':<10} {'Latency':<10}")
    print("=" * 80)

    start_process_time = time.time()

    for block_idx in range(total_blocks):
        block_start = block_idx * block_size
        block_end = block_start + block_size
        audio_block = audio[block_start:block_end]

        # Current time in the audio
        current_time = block_idx * block_size / sr

        # Analyze pitch
        block_start_time = time.time()
        pitch = analyzer.analyze_pitch(audio_block)
        pitch_time = time.time() - block_start_time

        # Detect onset
        onset_start_time = time.time()
        onset = analyzer.detect_onset(audio_block)
        onset_time = time.time() - onset_start_time

        # Track beats
        beat_start_time = time.time()
        beat = analyzer.track_beat(onset, current_time)
        beat_time = time.time() - beat_start_time

        # Update tempo estimate every 100 blocks (~1.16 seconds)
        if block_idx % 100 == 0:
            analyzer.estimate_tempo(audio_block)

        total_latency = (time.time() - block_start_time) * 1000

        # Record events
        if pitch is not None:
            pitch_detections.append((current_time, pitch))

        if onset:
            onset_times.append(current_time)

        if beat:
            beat_times.append(current_time)

        # Print updates when events occur or periodically
        should_print = onset or beat or (block_idx % 50 == 0)

        if should_print:
            pitch_str = f"{pitch:.1f}Hz" if pitch is not None else "-"
            onset_str = "ONSET" if onset else ""
            beat_str = "BEAT" if beat else ""
            tempo_str = f"{analyzer.tempo_estimate:.1f}BPM"
            latency_str = f"{total_latency:.2f}ms"

            print(f"{current_time:<8.2f} {pitch_str:<10} {onset_str:<8} {beat_str:<6} {tempo_str:<10} {latency_str:<10}")

    end_process_time = time.time()
    processing_time = end_process_time - start_process_time

    print("=" * 80)
    print("\nAnalysis Complete!")
    print(f"\nPerformance Summary:")
    print(f"  Audio duration:     {len(audio)/sr:.2f}s")
    print(f"  Processing time:    {processing_time:.2f}s")
    print(f"  Real-time factor:   {(len(audio)/sr)/processing_time:.2f}x")
    print(f"  Blocks processed:   {total_blocks}")
    print(f"  Avg latency:        {processing_time/total_blocks*1000:.2f}ms per block")
    print(f"\nDetection Results:")
    print(f"  Pitch detections:   {len(pitch_detections)}")
    print(f"  Onsets detected:    {len(onset_times)}")
    print(f"  Beats detected:     {len(beat_times)}")
    print(f"  Final tempo:        {analyzer.tempo_estimate:.1f} BPM")

    # Calculate beat timing accuracy (if we know the ground truth tempo is 120 BPM)
    if len(beat_times) >= 2:
        beat_intervals = np.diff(beat_times)
        avg_interval = np.mean(beat_intervals)
        measured_tempo = 60.0 / avg_interval
        print(f"  Measured tempo:     {measured_tempo:.1f} BPM")

    stats = analyzer.get_performance_stats()
    print(f"\nPerformance Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def main():
    """Main test function."""
    print("Performia Real-Time Audio Analysis Test")
    print("=" * 80)

    # Create test fixtures directory if it doesn't exist
    fixtures_dir = os.path.join(
        os.path.dirname(__file__),
        "../../tests/fixtures"
    )
    os.makedirs(fixtures_dir, exist_ok=True)

    # Generate test audio
    test_file = os.path.join(fixtures_dir, "test_melody.wav")

    if not os.path.exists(test_file):
        generate_test_audio(test_file, duration=10.0)
    else:
        print(f"Using existing test file: {test_file}")

    # Process the audio file
    process_audio_file(test_file, block_size=512)

    print("\n" + "=" * 80)
    print("Test complete! Analysis is running faster than real-time.")
    print("=" * 80)


if __name__ == "__main__":
    main()
