cmake_minimum_required(VERSION 3.15)
project(Performia VERSION 1.0.0)

# Add JUCE as a subdirectory
add_subdirectory(JuceLibraryCode)

# Audio Engine target
add_library(PerformiaAudioEngine
    src/audio_engine/core/src/AudioEngine.cpp
    src/audio_engine/dsp/src/DSPProcessor.cpp
    src/audio_engine/ui/src/AudioEngineUI.cpp
)

target_include_directories(PerformiaAudioEngine PUBLIC
    src/audio_engine/core/include
    src/audio_engine/dsp/include
    src/audio_engine/ui/include
)

target_link_libraries(PerformiaAudioEngine PRIVATE
    juce::juce_audio_basics
    juce::juce_audio_devices
    juce::juce_audio_formats
    juce::juce_audio_processors
    juce::juce_audio_utils
    juce::juce_core
    juce::juce_data_structures
    juce::juce_events
    juce::juce_graphics
    juce::juce_gui_basics
    juce::juce_gui_extra
)
