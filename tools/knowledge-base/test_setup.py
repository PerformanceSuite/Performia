#!/usr/bin/env python3
"""
Test Docling knowledge base setup

This script tests the complete pipeline:
1. Document processing (using a test markdown file)
2. Vector database storage
3. Similarity search retrieval
"""

import sys
from pathlib import Path
from process_docs import PerformiaKnowledgeProcessor


def create_test_document():
    """Create a test document for processing"""
    test_dir = Path("docs/knowledge-base/research")
    test_dir.mkdir(parents=True, exist_ok=True)

    test_file = test_dir / "test_audio_processing.md"

    content = """# Audio Processing in JUCE

## Overview
JUCE is a cross-platform C++ framework for audio applications. It provides classes for real-time audio processing, MIDI handling, and plugin development.

## AudioProcessor Class
The AudioProcessor class is the core of JUCE audio processing. Key methods:

### processBlock()
Called by the host to process audio buffers:
```cpp
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
```cpp
// JUCE sends OSC message
OSCSender sender;
sender.connect("127.0.0.1", 57120);
sender.send("/note", 440.0f, 0.5f);
```

SuperCollider receives:
```supercollider
OSCdef(\\juceNote, { |msg|
    var freq = msg[1];
    var amp = msg[2];
    Synth(\\sine, [\\freq, freq, \\amp, amp]);
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
"""

    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return test_file


def test_pipeline():
    """Test the complete knowledge base pipeline"""
    print("=== Performia Knowledge Base Test ===\n")

    # 1. Create test document
    print("1. Creating test document...")
    test_file = create_test_document()
    print(f"   ✅ Created: {test_file}\n")

    # 2. Initialize processor
    print("2. Initializing knowledge processor...")
    processor = PerformiaKnowledgeProcessor(db_path="docs/knowledge-base/chromadb")
    print("   ✅ Processor initialized\n")

    # 3. Process document
    print("3. Processing test document...")
    try:
        chunks = processor.process_file(
            str(test_file),
            category="research",
            metadata={"test": True, "type": "audio_processing"}
        )
        print(f"   ✅ Processed successfully: {chunks} chunks\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return False

    # 4. Test queries
    print("4. Testing queries...\n")

    test_queries = [
        "How do I implement processBlock in JUCE?",
        "What are the rules for real-time audio processing?",
        "How can JUCE communicate with SuperCollider?",
        "What is the JUCE threading model?"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"   Query {i}: {query}")
        try:
            results = processor.query(query, k=2)

            if results:
                best_result = results[0]
                print(f"   Score: {best_result['score']:.4f}")
                print(f"   Category: {best_result['metadata']['category']}")
                print(f"   Preview: {best_result['content'][:150]}...")
                print()
            else:
                print("   ⚠️ No results found\n")

        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            return False

    print("=== All Tests Passed! ===\n")
    return True


if __name__ == "__main__":
    success = test_pipeline()
    sys.exit(0 if success else 1)
