#pragma once

// When JUCE is available, uncomment this:
// #include <JuceHeader.h>

// For now, we'll define the color values for reference
namespace PerformiaColors {
    // These will become juce::Colour objects when JUCE is integrated
    // const juce::Colour background   = juce::Colour::fromString("#0A0E27");
    // const juce::Colour surface      = juce::Colour::fromString("#1C2341");
    // const juce::Colour primary      = juce::Colour::fromString("#00D4FF");
    // const juce::Colour secondary    = juce::Colour::fromString("#FF00AA");
    // const juce::Colour success      = juce::Colour::fromString("#00FF88");
    // const juce::Colour warning      = juce::Colour::fromString("#FFB800");
    // const juce::Colour error        = juce::Colour::fromString("#FF3366");
    // const juce::Colour text         = juce::Colour::fromString("#D0D0D0");
    // const juce::Colour textDim      = juce::Colour::fromString("#808080");
    
    // Color values for reference
    constexpr const char* BACKGROUND = "#0A0E27";  // Dark blue-black
    constexpr const char* SURFACE    = "#1C2341";  // Lighter surface
    constexpr const char* PRIMARY    = "#00D4FF";  // Cyan
    constexpr const char* SECONDARY  = "#FF00AA";  // Magenta
    constexpr const char* SUCCESS    = "#00FF88";  // Green
    constexpr const char* WARNING    = "#FFB800";  // Orange
    constexpr const char* ERROR      = "#FF3366";  // Red
    constexpr const char* TEXT       = "#D0D0D0";  // Light gray
    constexpr const char* TEXT_DIM   = "#808080";  // Dim gray
    
    // Semantic colors
    constexpr const char* AGENT_BASS   = "#00D4FF";  // Cyan
    constexpr const char* AGENT_DRUMS  = "#FF00AA";  // Magenta
    constexpr const char* AGENT_KEYS   = "#00FF88";  // Green
    constexpr const char* AGENT_MELODY = "#FFB800";  // Orange
    
    // UI element colors
    constexpr const char* KNOB_GLOW      = "#00D4FF";
    constexpr const char* SLIDER_TRACK   = "#1C2341";
    constexpr const char* SLIDER_THUMB   = "#00D4FF";
    constexpr const char* BUTTON_NORMAL  = "#1C2341";
    constexpr const char* BUTTON_HOVER   = "#2C3351";
    constexpr const char* BUTTON_ACTIVE  = "#00D4FF";
    
    // Visualization colors
    constexpr const char* VIZ_WAVEFORM   = "#00D4FF";
    constexpr const char* VIZ_SPECTRUM   = "#FF00AA";
    constexpr const char* VIZ_NEURAL     = "#00FF88";
}

namespace PerformiaSizes {
    // Component dimensions
    constexpr int KNOB_SIZE = 64;
    constexpr int SLIDER_WIDTH = 40;
    constexpr int SLIDER_HEIGHT = 120;
    constexpr int BUTTON_WIDTH = 80;
    constexpr int BUTTON_HEIGHT = 32;
    
    // Layout dimensions
    constexpr int TOP_BAR_HEIGHT = 60;
    constexpr int NAV_RAIL_WIDTH = 80;
    constexpr int STATUS_BAR_HEIGHT = 30;
    
    // Spacing
    constexpr int PADDING_SMALL = 8;
    constexpr int PADDING_MEDIUM = 16;
    constexpr int PADDING_LARGE = 24;
    
    // Border radius
    constexpr int CORNER_RADIUS_SMALL = 4;
    constexpr int CORNER_RADIUS_MEDIUM = 8;
    constexpr int CORNER_RADIUS_LARGE = 12;
}

namespace PerformiaFonts {
    // Font families (will use JUCE's font system)
    constexpr const char* FONT_REGULAR = "Inter";
    constexpr const char* FONT_MONO = "JetBrains Mono";
    
    // Font sizes
    constexpr float SIZE_SMALL = 11.0f;
    constexpr float SIZE_NORMAL = 13.0f;
    constexpr float SIZE_MEDIUM = 15.0f;
    constexpr float SIZE_LARGE = 18.0f;
    constexpr float SIZE_XLARGE = 24.0f;
}

namespace PerformiaAnimation {
    // Animation durations (in milliseconds)
    constexpr int HOVER_FADE = 150;
    constexpr int CLICK_RESPONSE = 50;
    constexpr int MODE_SWITCH = 300;
    constexpr int GLOW_PULSE = 2000;
    
    // Frame rates
    constexpr int UI_FPS = 60;
    constexpr int VIZ_FPS = 30;
}