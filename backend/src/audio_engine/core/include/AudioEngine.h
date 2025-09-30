#pragma once
#include <JuceHeader.h>

class AudioEngine {
public:
    AudioEngine();
    ~AudioEngine();

    void initialize();
    void process(float* buffer, int numSamples);
    void shutdown();

private:
    // Implementation details
};
