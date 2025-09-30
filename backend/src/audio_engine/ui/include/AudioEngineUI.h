#pragma once
#include <JuceHeader.h>

class AudioEngineUI : public juce::Component {
public:
    AudioEngineUI();
    ~AudioEngineUI();

    void paint(juce::Graphics& g) override;
    void resized() override;

private:
    // UI components
};
