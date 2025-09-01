cmake_minimum_required(VERSION 3.15)
project(PERFORMIA_UI_CLEAN VERSION 2.0.0)

# Add JUCE as a subdirectory (you'll need to add JUCE to the project)
# add_subdirectory(JUCE)

# For now, we'll set up the structure for when JUCE is added
# This CMakeLists.txt is ready for JUCE integration

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add executable target (will be converted to juce_add_gui_app when JUCE is added)
add_executable(Performia
    src/main/Main.cpp
)

# Include directories
target_include_directories(Performia PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}/src/core
    ${CMAKE_CURRENT_SOURCE_DIR}/src/components
    ${CMAKE_CURRENT_SOURCE_DIR}/src/modes
    ${CMAKE_CURRENT_SOURCE_DIR}/src/layouts
    ${CMAKE_CURRENT_SOURCE_DIR}/src/utils
)

# When JUCE is added, uncomment and modify:
# juce_add_gui_app(Performia
#     PRODUCT_NAME "Performia UI"
#     COMPANY_NAME "Performia Audio"
#     BUNDLE_ID "com.performia.ui"
#     NEEDS_MIDI_INPUT TRUE
#     NEEDS_MIDI_OUTPUT TRUE
# )

# juce_generate_juce_header(Performia)

# target_sources(Performia
#     PRIVATE
#         src/main/Main.cpp
#         src/core/AudioEngine.cpp
#         src/core/OSCManager.cpp
#         src/core/IPCManager.cpp
#         # Add more source files as they're created
# )

# target_link_libraries(Performia
#     PRIVATE
#         juce::juce_audio_basics
#         juce::juce_audio_devices
#         juce::juce_audio_formats
#         juce::juce_audio_processors
#         juce::juce_core
#         juce::juce_data_structures
#         juce::juce_events
#         juce::juce_graphics
#         juce::juce_gui_basics
#         juce::juce_gui_extra
#         juce::juce_osc
#     PUBLIC
#         juce::juce_recommended_config_flags
#         juce::juce_recommended_lto_flags
#         juce::juce_recommended_warning_flags
# )

# Platform-specific settings
if(APPLE)
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.15")
endif()

# Output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)