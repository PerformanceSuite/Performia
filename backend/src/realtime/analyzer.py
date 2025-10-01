"""
Real-time audio analysis for Performia.

Provides low-latency pitch detection, onset detection, and beat tracking
for live performance applications.
"""

import numpy as np
import librosa
from typing import Optional, Tuple, List
from collections import deque
import time


class RingBuffer:
    """Efficient ring buffer for audio data."""

    def __init__(self, size: int):
        self.size = size
        self.buffer = np.zeros(size, dtype=np.float32)
        self.write_pos = 0

    def write(self, data: np.ndarray):
        """Write data to the ring buffer."""
        data_len = len(data)

        if data_len > self.size:
            # If data is larger than buffer, only keep the most recent
            data = data[-self.size:]
            data_len = self.size

        # Handle wrap-around
        space_to_end = self.size - self.write_pos

        if data_len <= space_to_end:
            # Data fits without wrapping
            self.buffer[self.write_pos:self.write_pos + data_len] = data
            self.write_pos = (self.write_pos + data_len) % self.size
        else:
            # Data wraps around
            self.buffer[self.write_pos:] = data[:space_to_end]
            remaining = data_len - space_to_end
            self.buffer[:remaining] = data[space_to_end:]
            self.write_pos = remaining

    def read(self, n_samples: Optional[int] = None) -> np.ndarray:
        """Read most recent n_samples from the buffer (in chronological order)."""
        if n_samples is None:
            n_samples = self.size

        n_samples = min(n_samples, self.size)

        # Read in chronological order (oldest to newest)
        if self.write_pos >= n_samples:
            # No wrap-around needed
            return self.buffer[self.write_pos - n_samples:self.write_pos].copy()
        else:
            # Wrap-around needed
            part1_size = n_samples - self.write_pos
            part1 = self.buffer[-part1_size:]
            part2 = self.buffer[:self.write_pos]
            return np.concatenate([part1, part2])


class RealtimeAnalyzer:
    """
    Real-time audio analyzer for pitch, onset, and beat detection.

    Optimized for low-latency live performance (<15ms per block).
    """

    def __init__(self, sample_rate: int = 44100):
        """
        Initialize the analyzer.

        Args:
            sample_rate: Audio sample rate in Hz (default: 44100)
        """
        self.sample_rate = sample_rate
        self.hop_length = 512  # ~11.6ms at 44.1kHz
        self.frame_length = 2048  # ~46ms at 44.1kHz

        # Buffer for accumulating audio for analysis
        self.buffer = RingBuffer(size=8192)  # ~185ms of audio

        # Onset detection state
        self.onset_buffer = RingBuffer(size=4096)
        self.prev_onset_strength = 0.0
        self.onset_threshold = 0.3

        # Beat tracking state
        self.beat_times = deque(maxlen=8)  # Store last 8 beat times
        self.tempo_estimate = 120.0  # BPM
        self.last_tempo_update = time.time()
        self.beat_buffer = RingBuffer(size=self.sample_rate * 4)  # 4 seconds

        # Pitch detection configuration
        self.fmin = librosa.note_to_hz('C2')  # ~65 Hz
        self.fmax = librosa.note_to_hz('C7')  # ~2093 Hz

        # Performance tracking
        self.last_analysis_time = 0.0

    def analyze_pitch(self, audio_block: np.ndarray) -> Optional[float]:
        """
        Detect pitch in the audio block using librosa's pyin algorithm.

        Args:
            audio_block: Audio samples (mono)

        Returns:
            Detected pitch in Hz, or None if no pitch detected
        """
        start_time = time.time()

        # Add to buffer
        self.buffer.write(audio_block)

        # Get enough samples for pitch detection
        analysis_samples = self.buffer.read(self.frame_length)

        if len(analysis_samples) < self.frame_length:
            return None

        try:
            # Use pyin for robust pitch detection
            # Lower frame_length for lower latency
            f0, voiced_flag, voiced_probs = librosa.pyin(
                analysis_samples,
                fmin=self.fmin,
                fmax=self.fmax,
                sr=self.sample_rate,
                frame_length=self.frame_length,
                hop_length=self.hop_length,
                center=False  # Don't center for lower latency
            )

            # Get most recent pitch estimate
            if f0 is not None and len(f0) > 0:
                # Use the last (most recent) frame
                recent_f0 = f0[-1]
                recent_prob = voiced_probs[-1] if voiced_probs is not None else 0.0

                # Only return pitch if confidence is high enough
                if not np.isnan(recent_f0) and recent_prob > 0.5:
                    self.last_analysis_time = time.time() - start_time
                    return float(recent_f0)

        except Exception as e:
            # Don't crash on analysis errors
            pass

        self.last_analysis_time = time.time() - start_time
        return None

    def detect_onset(self, audio_block: np.ndarray) -> bool:
        """
        Detect onsets (note attacks) in the audio block.

        Args:
            audio_block: Audio samples (mono)

        Returns:
            True if onset detected in this block
        """
        # Add to onset buffer
        self.onset_buffer.write(audio_block)

        # Get samples for onset detection
        analysis_samples = self.onset_buffer.read(self.frame_length)

        if len(analysis_samples) < self.frame_length:
            return False

        try:
            # Compute onset strength
            onset_env = librosa.onset.onset_strength(
                y=analysis_samples,
                sr=self.sample_rate,
                hop_length=self.hop_length,
                aggregate=np.median  # More robust than mean
            )

            # Get most recent onset strength
            current_strength = onset_env[-1] if len(onset_env) > 0 else 0.0

            # Detect onset using threshold and peak detection
            # Onset occurs when strength rises above threshold and previous value
            is_onset = (
                current_strength > self.onset_threshold and
                current_strength > self.prev_onset_strength * 1.5
            )

            self.prev_onset_strength = current_strength

            return is_onset

        except Exception as e:
            return False

    def estimate_tempo(self, audio_block: Optional[np.ndarray] = None) -> float:
        """
        Estimate current tempo in BPM.

        This is called less frequently than pitch/onset detection.

        Args:
            audio_block: Optional audio block to add to buffer

        Returns:
            Estimated tempo in BPM
        """
        # Only update tempo every 2 seconds to avoid jitter
        current_time = time.time()
        if current_time - self.last_tempo_update < 2.0:
            return self.tempo_estimate

        if audio_block is not None:
            self.beat_buffer.write(audio_block)

        # Get 4 seconds of audio for tempo estimation
        analysis_samples = self.beat_buffer.read()

        if len(analysis_samples) < self.sample_rate:  # Need at least 1 second
            return self.tempo_estimate

        try:
            # Use librosa's tempo estimation
            tempo, beats = librosa.beat.beat_track(
                y=analysis_samples,
                sr=self.sample_rate,
                hop_length=self.hop_length,
                start_bpm=self.tempo_estimate  # Use previous estimate as prior
            )

            if tempo is not None and tempo > 0:
                # Smooth tempo estimate (low-pass filter)
                # Don't change tempo too drastically
                if isinstance(tempo, np.ndarray):
                    tempo = tempo[0]

                # Limit tempo changes to ±20 BPM per update
                tempo_diff = tempo - self.tempo_estimate
                tempo_diff = np.clip(tempo_diff, -20, 20)

                self.tempo_estimate = self.tempo_estimate + tempo_diff * 0.3
                self.last_tempo_update = current_time

        except Exception as e:
            pass

        return self.tempo_estimate

    def track_beat(self, onset_detected: bool, current_time: float) -> bool:
        """
        Track beats based on onset detection and tempo estimate.

        Args:
            onset_detected: Whether an onset was detected
            current_time: Current time in seconds

        Returns:
            True if a beat is detected
        """
        if not onset_detected:
            return False

        # Calculate expected beat interval
        beat_interval = 60.0 / self.tempo_estimate  # seconds per beat

        if len(self.beat_times) == 0:
            # First beat
            self.beat_times.append(current_time)
            return True

        # Check if enough time has passed since last beat
        time_since_last_beat = current_time - self.beat_times[-1]

        # Accept beat if it's within ±30% of expected interval
        if time_since_last_beat >= beat_interval * 0.7:
            self.beat_times.append(current_time)

            # Update tempo estimate based on recent beats
            if len(self.beat_times) >= 4:
                recent_intervals = []
                for i in range(len(self.beat_times) - 1):
                    interval = self.beat_times[i + 1] - self.beat_times[i]
                    recent_intervals.append(interval)

                # Calculate tempo from median interval
                median_interval = np.median(recent_intervals)
                if median_interval > 0:
                    measured_tempo = 60.0 / median_interval
                    # Smooth with current estimate
                    self.tempo_estimate = 0.7 * self.tempo_estimate + 0.3 * measured_tempo

            return True

        return False

    def get_performance_stats(self) -> dict:
        """
        Get performance statistics for monitoring.

        Returns:
            Dictionary with performance metrics
        """
        return {
            'last_analysis_time_ms': self.last_analysis_time * 1000,
            'tempo_bpm': self.tempo_estimate,
            'beats_tracked': len(self.beat_times),
            'onset_threshold': self.onset_threshold
        }
