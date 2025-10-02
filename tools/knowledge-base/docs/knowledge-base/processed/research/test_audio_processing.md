# Audio Processing in JUCE

## Overview

JUCE is a cross-platform C++ framework for audio applications. It provides classes for real-time audio processing, MIDI handling, and plugin development.

## AudioProcessor Class

The AudioProcessor class is the core of JUCE audio processing. Key methods:

### processBlock()

Called by the host to process audio buffers:

```
void processBlock(AudioBuffer<float>& buffer, MidiBuffer& midiMessages) {
    // Process audio here
    for (int channel = 0; channel < buffer.getNumChannels(); ++channel) {
        float* channelData = buffer.getWritePointer(channel);
        for (int sample = 0; sample < buffer.getNumSamples(); ++sample) {
            channelData[sample] *= 0.5f; // Example: reduce volume
        }
    }
}
```

### Threading Model

- Audio thread: Real-time priority, no allocations allowed
- Message thread: UI updates and non-real-time operations
- Background threads: File loading, analysis

## Best Practices

1. Never allocate memory in processBlock()
2. Use lock-free data structures for thread communication
3. Implement prepareToPlay() for initialization
4. Use AudioBuffer methods for efficiency

## Real-Time Safety

Critical rules:

- No malloc/new in audio thread
- No system calls (file I/O, networking)
- No locks that might block
- Pre-allocate all buffers in prepareToPlay()

## SuperCollider Integration

SuperCollider can communicate with JUCE via OSC:

```
// JUCE sends OSC message
OSCSender sender;
sender.connect("127.0.0.1", 57120);
sender.send("/note", 440.0f, 0.5f);
```

SuperCollider receives:

```
OSCdef(\juceNote, { |msg|
    var freq = msg[1];
    var amp = msg[2];
    Synth(\sine, [\freq, freq, \amp, amp]);
}, '/note');
```

## Performance Tips

- Use SIMD operations for vector math
- Minimize branching in inner loops
- Cache-friendly data layout
- Profile with Instruments (macOS) or Valgrind (Linux)

## References

- JUCE Documentation: https://docs.juce.com
- Audio Programmer Forums: https://forum.juce.com
- Real-Time Audio Programming 101: Must avoid allocations!