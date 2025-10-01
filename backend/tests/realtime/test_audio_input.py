"""
Unit tests for real-time audio input.

Tests the RealtimeAudioInput class for correct behavior,
error handling, and performance characteristics.
"""

import pytest
import numpy as np
import time
import sys
import os
from queue import Empty

# Add backend/src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from realtime.audio_input import (
    RealtimeAudioInput,
    list_audio_devices,
    get_default_device
)


class TestAudioDeviceEnumeration:
    """Test audio device detection and enumeration."""

    def test_list_audio_devices(self):
        """Test that we can list audio input devices."""
        devices = list_audio_devices()

        # Should return a list (may be empty on headless systems)
        assert isinstance(devices, list)

        # If devices exist, check structure
        if devices:
            device = devices[0]
            assert 'index' in device
            assert 'name' in device
            assert 'channels' in device
            assert 'sample_rate' in device
            assert 'host_api' in device

            # Validate types
            assert isinstance(device['index'], int)
            assert isinstance(device['name'], str)
            assert isinstance(device['channels'], int)
            assert isinstance(device['sample_rate'], float)
            assert isinstance(device['host_api'], str)

            # Channels should be positive
            assert device['channels'] > 0

            print(f"✅ Found {len(devices)} audio input device(s)")
            for d in devices:
                print(f"   [{d['index']}] {d['name']} - {d['channels']} ch @ {d['sample_rate']:.0f} Hz")

    def test_get_default_device(self):
        """Test getting default audio input device."""
        device = get_default_device()

        # May be None on headless systems
        if device:
            assert isinstance(device, dict)
            assert 'index' in device
            assert 'name' in device
            assert 'channels' in device
            assert 'sample_rate' in device

            print(f"✅ Default device: {device['name']}")
        else:
            print("⚠️  No default audio device (headless system?)")


class TestRealtimeAudioInput:
    """Test RealtimeAudioInput class."""

    def test_initialization(self):
        """Test audio input initialization."""
        audio_input = RealtimeAudioInput(
            sample_rate=44100,
            block_size=512,
            channels=1
        )

        assert audio_input.sample_rate == 44100
        assert audio_input.block_size == 512
        assert audio_input.channels == 1
        assert audio_input.is_running is False
        assert audio_input.blocks_captured == 0
        assert audio_input.blocks_dropped == 0

        print("✅ Audio input initialized with correct parameters")

    def test_custom_parameters(self):
        """Test initialization with custom parameters."""
        audio_input = RealtimeAudioInput(
            sample_rate=48000,
            block_size=256,
            channels=2,
            queue_size=20
        )

        assert audio_input.sample_rate == 48000
        assert audio_input.block_size == 256
        assert audio_input.channels == 2
        assert audio_input.queue_size == 20

        print("✅ Custom parameters accepted")

    def test_start_stop(self):
        """Test starting and stopping audio stream."""
        devices = list_audio_devices()
        if not devices:
            pytest.skip("No audio input devices available")

        audio_input = RealtimeAudioInput()

        # Should not be running initially
        assert audio_input.is_running is False

        # Start stream
        audio_input.start()
        assert audio_input.is_running is True

        # Let it run briefly
        time.sleep(0.5)

        # Stop stream
        audio_input.stop()
        assert audio_input.is_running is False

        print("✅ Audio stream started and stopped successfully")

    def test_context_manager(self):
        """Test using audio input as context manager."""
        devices = list_audio_devices()
        if not devices:
            pytest.skip("No audio input devices available")

        with RealtimeAudioInput() as audio_input:
            assert audio_input.is_running is True
            time.sleep(0.2)

        # Should be stopped after exiting context
        assert audio_input.is_running is False

        print("✅ Context manager working correctly")

    def test_double_start_error(self):
        """Test that starting an already running stream raises error."""
        devices = list_audio_devices()
        if not devices:
            pytest.skip("No audio input devices available")

        audio_input = RealtimeAudioInput()
        audio_input.start()

        try:
            # Should raise RuntimeError
            with pytest.raises(RuntimeError):
                audio_input.start()

            print("✅ Double start correctly raises RuntimeError")

        finally:
            audio_input.stop()

    def test_get_block_before_start(self):
        """Test that getting blocks before starting raises error."""
        audio_input = RealtimeAudioInput()

        with pytest.raises(RuntimeError):
            audio_input.get_block(timeout=0.1)

        print("✅ Getting block before start correctly raises RuntimeError")

    def test_audio_block_delivery(self):
        """Test that audio blocks are delivered correctly."""
        devices = list_audio_devices()
        if not devices:
            pytest.skip("No audio input devices available")

        audio_input = RealtimeAudioInput(
            sample_rate=44100,
            block_size=512,
            channels=1
        )

        audio_input.start()

        try:
            # Collect several blocks
            blocks = []
            for _ in range(10):
                block = audio_input.get_block(timeout=1.0)
                blocks.append(block)

            # Verify block properties
            for block in blocks:
                assert isinstance(block, np.ndarray)
                assert block.shape == (512, 1)  # (block_size, channels)
                assert block.dtype == np.float32

                # Audio data should be in reasonable range (-1.0 to 1.0)
                assert np.all(np.abs(block) <= 1.0)

            print(f"✅ Successfully received {len(blocks)} audio blocks")
            print(f"   Block shape: {blocks[0].shape}")
            print(f"   Data type: {blocks[0].dtype}")
            print(f"   Value range: [{blocks[0].min():.3f}, {blocks[0].max():.3f}]")

        finally:
            audio_input.stop()

    def test_block_timing(self):
        """Test that blocks are delivered at expected rate."""
        devices = list_audio_devices()
        if not devices:
            pytest.skip("No audio input devices available")

        audio_input = RealtimeAudioInput(
            sample_rate=44100,
            block_size=512
        )

        # Expected time per block
        expected_block_time = 512 / 44100  # ~11.6ms

        audio_input.start()

        try:
            start_time = time.time()
            num_blocks = 20

            for _ in range(num_blocks):
                audio_input.get_block(timeout=1.0)

            elapsed = time.time() - start_time
            expected_time = num_blocks * expected_block_time

            # Should be close to expected (within 50% tolerance for test reliability)
            assert elapsed < expected_time * 1.5

            print(f"✅ Block timing correct:")
            print(f"   Expected: {expected_time:.3f}s for {num_blocks} blocks")
            print(f"   Actual: {elapsed:.3f}s")
            print(f"   Latency per block: {elapsed/num_blocks*1000:.1f}ms")

        finally:
            audio_input.stop()

    def test_get_block_nowait(self):
        """Test non-blocking get_block_nowait method."""
        devices = list_audio_devices()
        if not devices:
            pytest.skip("No audio input devices available")

        audio_input = RealtimeAudioInput()
        audio_input.start()

        try:
            # Wait a bit for queue to fill
            time.sleep(0.1)

            # Should get blocks without blocking
            blocks_retrieved = 0
            for _ in range(5):
                block = audio_input.get_block_nowait()
                if block is not None:
                    blocks_retrieved += 1

            assert blocks_retrieved > 0

            print(f"✅ Retrieved {blocks_retrieved} blocks without blocking")

        finally:
            audio_input.stop()

    def test_clear_queue(self):
        """Test clearing the audio queue."""
        devices = list_audio_devices()
        if not devices:
            pytest.skip("No audio input devices available")

        audio_input = RealtimeAudioInput()
        audio_input.start()

        try:
            # Let some blocks accumulate
            time.sleep(0.2)

            # Clear queue
            cleared = audio_input.clear_queue()
            assert cleared >= 0

            print(f"✅ Cleared {cleared} blocks from queue")

        finally:
            audio_input.stop()

    def test_statistics(self):
        """Test that statistics are tracked correctly."""
        devices = list_audio_devices()
        if not devices:
            pytest.skip("No audio input devices available")

        audio_input = RealtimeAudioInput()
        audio_input.start()

        try:
            # Get some blocks
            for _ in range(5):
                audio_input.get_block(timeout=1.0)

            # Check statistics
            stats = audio_input.get_stats()

            assert stats['is_running'] is True
            assert stats['sample_rate'] == 44100
            assert stats['block_size'] == 512
            assert stats['blocks_captured'] >= 5
            assert 'uptime' in stats
            assert stats['uptime'] > 0

            print("✅ Statistics tracking working:")
            print(f"   Blocks captured: {stats['blocks_captured']}")
            print(f"   Blocks dropped: {stats['blocks_dropped']}")
            print(f"   Queue size: {stats['queue_size']}/{stats['queue_max']}")
            print(f"   Uptime: {stats['uptime']:.2f}s")

        finally:
            audio_input.stop()


class TestErrorRecovery:
    """Test error handling and recovery."""

    def test_invalid_sample_rate(self):
        """Test handling of invalid sample rate."""
        # Some systems may reject unusual sample rates
        audio_input = RealtimeAudioInput(sample_rate=99999)

        # May fail on start (expected)
        try:
            audio_input.start()
            audio_input.stop()
        except:
            print("✅ Invalid sample rate handled gracefully")

    def test_invalid_device(self):
        """Test handling of invalid device ID."""
        audio_input = RealtimeAudioInput(device=999)

        # Should raise error on start
        with pytest.raises(Exception):
            audio_input.start()

        print("✅ Invalid device ID raises exception")

    def test_stop_without_start(self):
        """Test that stopping without starting doesn't crash."""
        audio_input = RealtimeAudioInput()

        # Should handle gracefully
        audio_input.stop()

        print("✅ Stop without start handled gracefully")


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v', '-s'])
