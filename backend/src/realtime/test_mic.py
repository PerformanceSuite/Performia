#!/usr/bin/env python3
"""
Simple microphone test script with visual level meter.

Captures live audio from default microphone and displays
RMS amplitude with a console-based level meter.
"""

import sys
import time
import numpy as np
from audio_input import RealtimeAudioInput, list_audio_devices, get_default_device


def calculate_rms(audio_block: np.ndarray) -> float:
    """Calculate RMS (Root Mean Square) amplitude.

    Args:
        audio_block: Audio data as numpy array

    Returns:
        RMS amplitude (0.0 to 1.0)
    """
    return np.sqrt(np.mean(audio_block ** 2))


def db_from_amplitude(amplitude: float) -> float:
    """Convert amplitude to decibels.

    Args:
        amplitude: Linear amplitude (0.0 to 1.0)

    Returns:
        Decibels (dB), or -96 for very quiet signals
    """
    if amplitude < 1e-6:
        return -96.0
    return 20 * np.log10(amplitude)


def draw_level_meter(amplitude: float, width: int = 50) -> str:
    """Draw ASCII level meter.

    Args:
        amplitude: Audio amplitude (0.0 to 1.0)
        width: Width of meter in characters

    Returns:
        ASCII meter string
    """
    # Map amplitude to meter width (with some headroom)
    # 0.5 amplitude = full meter
    level = min(amplitude * 2.0, 1.0)
    filled = int(level * width)
    empty = width - filled

    # Color coding (using ANSI escape codes)
    if level < 0.4:
        color = '\033[32m'  # Green
    elif level < 0.7:
        color = '\033[33m'  # Yellow
    else:
        color = '\033[31m'  # Red

    reset = '\033[0m'

    meter = f"{color}{'█' * filled}{reset}{'░' * empty}"
    return meter


def main():
    """Run microphone test for 10 seconds."""
    print("=" * 70)
    print("Performia Real-Time Audio Input Test")
    print("=" * 70)
    print()

    # List available devices
    print("Available audio input devices:")
    devices = list_audio_devices()
    if not devices:
        print("  ❌ No audio input devices found!")
        return 1

    for device in devices:
        print(f"  [{device['index']}] {device['name']}")
        print(f"      {device['channels']} channels @ {device['sample_rate']:.0f} Hz ({device['host_api']})")

    print()

    # Show default device
    default = get_default_device()
    if default:
        print(f"Using default device: {default['name']}")
    else:
        print("⚠️  No default device found, using system default")

    print()
    print("Starting audio capture for 10 seconds...")
    print("(Speak, sing, or make sounds into your microphone)")
    print()

    # Start audio input
    try:
        audio_input = RealtimeAudioInput(
            sample_rate=44100,
            block_size=512,
            channels=1
        )
        audio_input.start()

    except Exception as e:
        print(f"❌ Failed to start audio input: {e}")
        return 1

    # Capture for 10 seconds
    start_time = time.time()
    duration = 10.0
    update_interval = 0.1  # Update meter every 100ms

    last_update = start_time
    blocks_in_interval = []

    try:
        while time.time() - start_time < duration:
            try:
                # Get audio block (with timeout)
                block = audio_input.get_block(timeout=0.1)
                blocks_in_interval.append(block)

                # Check if it's time to update display
                now = time.time()
                if now - last_update >= update_interval:
                    # Concatenate all blocks in this interval
                    if blocks_in_interval:
                        interval_audio = np.concatenate(blocks_in_interval)
                        amplitude = calculate_rms(interval_audio)
                        db = db_from_amplitude(amplitude)
                        meter = draw_level_meter(amplitude)

                        # Clear line and draw meter
                        elapsed = now - start_time
                        remaining = duration - elapsed

                        sys.stdout.write(f"\r[{elapsed:4.1f}s] {meter} | {amplitude:5.3f} ({db:5.1f} dB) | {remaining:4.1f}s left ")
                        sys.stdout.flush()

                        # Reset for next interval
                        blocks_in_interval = []
                        last_update = now

            except Exception as e:
                # Timeout or error - continue
                pass

        # Newline after meter
        print()
        print()

        # Print final statistics
        stats = audio_input.get_stats()
        print("=" * 70)
        print("Test completed successfully!")
        print("=" * 70)
        print(f"Blocks captured: {stats['blocks_captured']}")
        print(f"Blocks dropped:  {stats['blocks_dropped']}")
        if 'drop_rate' in stats:
            print(f"Drop rate:       {stats['drop_rate']:.2f}%")
        print(f"Queue status:    {stats['queue_size']}/{stats['queue_max']} blocks")
        print()

        if stats['blocks_dropped'] > 0:
            print("⚠️  Some audio blocks were dropped. This may indicate:")
            print("   - CPU overload")
            print("   - Slower processing than capture rate")
            print("   - Need to increase queue size")
        else:
            print("✅ No blocks dropped - audio capture working perfectly!")

        print()

    except KeyboardInterrupt:
        print()
        print()
        print("Interrupted by user")

    finally:
        audio_input.stop()

    return 0


if __name__ == '__main__':
    sys.exit(main())
