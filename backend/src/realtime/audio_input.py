"""
Real-time audio input with minimal latency.

Provides thread-safe audio capture from microphone using sounddevice
with configurable buffer sizes for low-latency applications.
"""

import sounddevice as sd
import numpy as np
from queue import Queue, Full
from typing import Optional, List, Dict, Any
import threading
import time


class RealtimeAudioInput:
    """Real-time audio input with minimal latency.

    Uses sounddevice for cross-platform audio capture with thread-safe
    queuing for downstream processing.

    Args:
        sample_rate: Audio sample rate in Hz (default: 44100)
        block_size: Number of samples per block (default: 512, ~11.6ms at 44.1kHz)
        channels: Number of audio channels (default: 1 for mono)
        device: Input device ID or None for default
        queue_size: Maximum number of blocks to buffer (default: 10)

    Example:
        >>> audio_input = RealtimeAudioInput()
        >>> audio_input.start()
        >>> while True:
        ...     block = audio_input.get_block()
        ...     # Process audio block
        >>> audio_input.stop()
    """

    def __init__(
        self,
        sample_rate: int = 44100,
        block_size: int = 512,
        channels: int = 1,
        device: Optional[int] = None,
        queue_size: int = 10
    ):
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.channels = channels
        self.device = device
        self.queue_size = queue_size

        # Thread-safe audio queue
        self.audio_queue = Queue(maxsize=queue_size)

        # Stream state
        self.stream: Optional[sd.InputStream] = None
        self.is_running = False
        self.lock = threading.Lock()

        # Statistics
        self.blocks_captured = 0
        self.blocks_dropped = 0
        self.last_error: Optional[str] = None
        self.start_time: Optional[float] = None

    def callback(self, indata: np.ndarray, frames: int, time_info: Any, status: sd.CallbackFlags) -> None:
        """Audio callback - runs in separate thread.

        This callback is invoked by sounddevice in a separate audio thread.
        It must be fast and non-blocking to avoid audio dropouts.

        Args:
            indata: Input audio data as numpy array
            frames: Number of frames in this callback
            time_info: Timing information
            status: Status flags indicating any issues
        """
        if status:
            self.last_error = str(status)
            print(f'⚠️  Audio input warning: {status}')

        try:
            # Copy data to avoid race conditions
            audio_copy = indata.copy()

            # Try to add to queue without blocking
            self.audio_queue.put_nowait(audio_copy)
            self.blocks_captured += 1

        except Full:
            # Queue is full - drop this block
            self.blocks_dropped += 1
            if self.blocks_dropped % 10 == 0:
                print(f'⚠️  Dropped {self.blocks_dropped} audio blocks (queue full)')

    def start(self) -> None:
        """Start audio stream.

        Raises:
            RuntimeError: If stream is already running
            sd.PortAudioError: If audio device cannot be opened
        """
        with self.lock:
            if self.is_running:
                raise RuntimeError("Audio stream is already running")

            try:
                # Create and start stream
                self.stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    blocksize=self.block_size,
                    channels=self.channels,
                    device=self.device,
                    callback=self.callback,
                    dtype=np.float32
                )
                self.stream.start()

                self.is_running = True
                self.start_time = time.time()
                self.blocks_captured = 0
                self.blocks_dropped = 0

                # Calculate latency
                latency_ms = (self.block_size / self.sample_rate) * 1000

                print(f"✅ Audio input started:")
                print(f"   Sample rate: {self.sample_rate} Hz")
                print(f"   Block size: {self.block_size} samples ({latency_ms:.1f}ms)")
                print(f"   Channels: {self.channels}")
                print(f"   Device: {self.device if self.device else 'default'}")

            except Exception as e:
                self.last_error = str(e)
                print(f"❌ Failed to start audio stream: {e}")
                raise

    def stop(self) -> None:
        """Stop audio stream."""
        with self.lock:
            if not self.is_running:
                return

            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None

            self.is_running = False

            # Print statistics
            if self.start_time:
                duration = time.time() - self.start_time
                print(f"✅ Audio input stopped:")
                print(f"   Duration: {duration:.1f}s")
                print(f"   Blocks captured: {self.blocks_captured}")
                print(f"   Blocks dropped: {self.blocks_dropped}")
                if self.blocks_captured > 0:
                    drop_rate = (self.blocks_dropped / (self.blocks_captured + self.blocks_dropped)) * 100
                    print(f"   Drop rate: {drop_rate:.2f}%")

    def get_block(self, timeout: Optional[float] = None) -> np.ndarray:
        """Get next audio block (blocking).

        Args:
            timeout: Maximum time to wait in seconds, or None to wait forever

        Returns:
            Audio block as numpy array of shape (block_size, channels)

        Raises:
            RuntimeError: If stream is not running
            queue.Empty: If timeout expires before block is available
        """
        if not self.is_running:
            raise RuntimeError("Audio stream is not running. Call start() first.")

        return self.audio_queue.get(timeout=timeout)

    def get_block_nowait(self) -> Optional[np.ndarray]:
        """Get next audio block without blocking.

        Returns:
            Audio block if available, None otherwise
        """
        if not self.is_running:
            return None

        try:
            return self.audio_queue.get_nowait()
        except:
            return None

    def clear_queue(self) -> int:
        """Clear all pending blocks from queue.

        Returns:
            Number of blocks cleared
        """
        cleared = 0
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
                cleared += 1
            except:
                break
        return cleared

    def get_stats(self) -> Dict[str, Any]:
        """Get current statistics.

        Returns:
            Dictionary containing stream statistics
        """
        stats = {
            'is_running': self.is_running,
            'sample_rate': self.sample_rate,
            'block_size': self.block_size,
            'channels': self.channels,
            'blocks_captured': self.blocks_captured,
            'blocks_dropped': self.blocks_dropped,
            'queue_size': self.audio_queue.qsize(),
            'queue_max': self.queue_size,
            'last_error': self.last_error
        }

        if self.start_time and self.is_running:
            stats['uptime'] = time.time() - self.start_time
            if self.blocks_captured > 0:
                stats['drop_rate'] = (self.blocks_dropped / (self.blocks_captured + self.blocks_dropped)) * 100

        return stats

    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False


def list_audio_devices() -> List[Dict[str, Any]]:
    """List all available audio input devices.

    Returns:
        List of device info dictionaries
    """
    devices = []
    for idx, device in enumerate(sd.query_devices()):
        if device['max_input_channels'] > 0:
            devices.append({
                'index': idx,
                'name': device['name'],
                'channels': device['max_input_channels'],
                'sample_rate': device['default_samplerate'],
                'host_api': sd.query_hostapis(device['hostapi'])['name']
            })
    return devices


def get_default_device() -> Optional[Dict[str, Any]]:
    """Get default audio input device.

    Returns:
        Device info dictionary or None if no default device
    """
    try:
        device_id = sd.default.device[0]  # Input device
        device = sd.query_devices(device_id)
        return {
            'index': device_id,
            'name': device['name'],
            'channels': device['max_input_channels'],
            'sample_rate': device['default_samplerate'],
            'host_api': sd.query_hostapis(device['hostapi'])['name']
        }
    except:
        return None
