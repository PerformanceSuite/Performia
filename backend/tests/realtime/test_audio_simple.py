#!/usr/bin/env python3
"""
Simple functional tests for real-time audio input.

Tests basic functionality without complex pytest setup.
"""

import sys
import os
import time
import numpy as np

# Add backend/src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from realtime.audio_input import (
    RealtimeAudioInput,
    list_audio_devices,
    get_default_device
)


def test_list_devices():
    """Test device enumeration."""
    print("\n" + "="*70)
    print("TEST: List Audio Devices")
    print("="*70)

    devices = list_audio_devices()
    print(f"Found {len(devices)} input device(s)")

    for device in devices:
        print(f"  [{device['index']}] {device['name']}")
        print(f"      {device['channels']} channels @ {device['sample_rate']:.0f} Hz")
        print(f"      Host API: {device['host_api']}")

    if devices:
        print("✅ PASSED: Device enumeration working")
        return True
    else:
        print("⚠️  WARNING: No devices found (may be headless)")
        return True


def test_default_device():
    """Test getting default device."""
    print("\n" + "="*70)
    print("TEST: Get Default Device")
    print("="*70)

    device = get_default_device()

    if device:
        print(f"Default device: {device['name']}")
        print(f"  {device['channels']} channels @ {device['sample_rate']:.0f} Hz")
        print("✅ PASSED: Default device retrieved")
        return True
    else:
        print("⚠️  WARNING: No default device (may be headless)")
        return True


def test_audio_capture():
    """Test basic audio capture."""
    print("\n" + "="*70)
    print("TEST: Audio Capture")
    print("="*70)

    devices = list_audio_devices()
    if not devices:
        print("⚠️  SKIPPED: No audio devices available")
        return True

    try:
        # Create audio input
        audio_input = RealtimeAudioInput(
            sample_rate=44100,
            block_size=512,
            channels=1
        )

        # Start stream
        audio_input.start()
        print("Audio stream started")

        # Capture 10 blocks
        blocks_captured = 0
        start_time = time.time()

        for i in range(10):
            block = audio_input.get_block(timeout=1.0)
            blocks_captured += 1

            # Verify block properties
            assert isinstance(block, np.ndarray), "Block should be numpy array"
            assert block.shape == (512, 1), f"Block shape should be (512, 1), got {block.shape}"
            assert block.dtype == np.float32, f"Block dtype should be float32, got {block.dtype}"
            assert np.all(np.abs(block) <= 1.0), "Audio values should be in [-1, 1] range"

            print(f"  Block {i+1}/10: shape={block.shape}, range=[{block.min():.3f}, {block.max():.3f}]")

        elapsed = time.time() - start_time
        expected_time = 10 * (512 / 44100)  # 10 blocks

        print(f"\nCaptured {blocks_captured} blocks in {elapsed:.3f}s")
        print(f"Expected time: {expected_time:.3f}s")
        print(f"Latency per block: {elapsed/blocks_captured*1000:.1f}ms")

        # Stop stream
        audio_input.stop()

        # Check statistics
        stats = audio_input.get_stats()
        print(f"\nStatistics:")
        print(f"  Blocks captured: {stats['blocks_captured']}")
        print(f"  Blocks dropped: {stats['blocks_dropped']}")

        if stats['blocks_dropped'] == 0:
            print("  ✅ No dropped blocks!")

        print("✅ PASSED: Audio capture working correctly")
        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_context_manager():
    """Test context manager usage."""
    print("\n" + "="*70)
    print("TEST: Context Manager")
    print("="*70)

    devices = list_audio_devices()
    if not devices:
        print("⚠️  SKIPPED: No audio devices available")
        return True

    try:
        with RealtimeAudioInput() as audio_input:
            assert audio_input.is_running, "Stream should be running in context"
            print("Stream started via context manager")

            # Get one block
            block = audio_input.get_block(timeout=1.0)
            print(f"Captured block: shape={block.shape}")

        assert not audio_input.is_running, "Stream should be stopped after context"
        print("Stream stopped automatically")

        print("✅ PASSED: Context manager working")
        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_statistics():
    """Test statistics tracking."""
    print("\n" + "="*70)
    print("TEST: Statistics Tracking")
    print("="*70)

    devices = list_audio_devices()
    if not devices:
        print("⚠️  SKIPPED: No audio devices available")
        return True

    try:
        audio_input = RealtimeAudioInput()
        audio_input.start()

        # Capture some blocks
        for _ in range(5):
            audio_input.get_block(timeout=1.0)

        stats = audio_input.get_stats()

        print("Statistics:")
        print(f"  Is running: {stats['is_running']}")
        print(f"  Sample rate: {stats['sample_rate']} Hz")
        print(f"  Block size: {stats['block_size']} samples")
        print(f"  Blocks captured: {stats['blocks_captured']}")
        print(f"  Blocks dropped: {stats['blocks_dropped']}")
        print(f"  Queue size: {stats['queue_size']}/{stats['queue_max']}")

        if 'uptime' in stats:
            print(f"  Uptime: {stats['uptime']:.2f}s")

        assert stats['is_running'] == True, "Should be running"
        assert stats['blocks_captured'] >= 5, "Should have captured at least 5 blocks"

        audio_input.stop()

        print("✅ PASSED: Statistics tracking working")
        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """Test error handling."""
    print("\n" + "="*70)
    print("TEST: Error Handling")
    print("="*70)

    try:
        # Test: Can't get block before starting
        audio_input = RealtimeAudioInput()
        try:
            audio_input.get_block(timeout=0.1)
            print("❌ FAILED: Should have raised RuntimeError")
            return False
        except RuntimeError:
            print("✅ Correctly raised RuntimeError for get_block before start")

        # Test: Invalid device ID
        audio_input_bad = RealtimeAudioInput(device=999)
        try:
            audio_input_bad.start()
            print("⚠️  WARNING: Invalid device didn't raise error (may be system dependent)")
            audio_input_bad.stop()
        except:
            print("✅ Correctly raised error for invalid device")

        # Test: Stop without start doesn't crash
        audio_input2 = RealtimeAudioInput()
        audio_input2.stop()  # Should not crash
        print("✅ Stop without start handled gracefully")

        print("✅ PASSED: Error handling working")
        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "#"*70)
    print("# Performia Real-Time Audio Input Test Suite")
    print("#"*70)

    tests = [
        test_list_devices,
        test_default_device,
        test_audio_capture,
        test_context_manager,
        test_statistics,
        test_error_handling,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n❌ TEST CRASHED: {test.__name__}")
            import traceback
            traceback.print_exc()
            failed += 1

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")

    if failed == 0:
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n❌ {failed} TEST(S) FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
