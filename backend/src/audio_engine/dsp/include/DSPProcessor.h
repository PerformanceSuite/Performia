#pragma once
#include <JuceHeader.h>

class DSPProcessor {
public:
    DSPProcessor();
    ~DSPProcessor();

    void prepare(double sampleRate, int maxBlockSize);
    void process(float* buffer, int numSamples);
    void reset();

private:
    // DSP implementation
};
