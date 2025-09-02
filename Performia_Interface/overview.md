### Overall Aesthetic:
A dark theme with subtle gradients and glowing elements to represent real-time activity. Clean, modern typography. Focus on intuitive visual feedback.

### Main Screen Layout (Consistent across modes, with dynamic content):
*   **Top Bar:**
    *   System Logo/Title ("PERFORMIA")
    *   Global Transport Controls (Play, Pause, Stop, Record, Tempo display/BPM slider)
    *   Master Volume & Output Meter
    *   Current Mode Indicator (Studio, Live, Settings)
    *   User Profile/Login (if applicable)

*   **Left Navigation Rail (Collapsible/Expandable):**
    *   **Studio Mode** (Icon: Metronome or Pencil/Edit)
    *   **Live Mode** (Icon: Microphone or Stage)
    *   **Settings** (Icon: Gear)
    *   (Optional) Help/Tutorial
    *   (Optional) Save/Load Project

*   **Main Content Area:** This will dynamically change based on the selected mode.

### 1. Studio Mode UI

This mode is designed for teaching, fine-tuning, and composing with the AI agents. It's more detailed and offers granular control.
**Main Content Area Breakdown for Studio Mode:**

*   **Individual Agent Control Panels (Stacked Vertically):** Each agent (Bass, Drums, Keys) gets its own expandable panel.
    *   **Agent Status:** Name (e.g., "AI Bass Agent"), Status Indicator (e.g., "Learning," "Performing"), CPU/Memory usage.
    *   **Input/Output:** Volume Slider, Mute/Solo button, Input Meter (for human input if that agent is learning from it).
    *   **"Personality" / Style Sliders:**
        *   **Bass:** Root Focus, Complexity, Groove Emphasis.
        *   **Drums:** Beat Sync (On/Off), Swing, Fill Probability, Kit Selection.
        *   **Keys:** Arpeggiator (On/Off, Type), Voicing/Chords (Simple/Complex), Harmonic Density.
    *   **Learning Controls:**
        *   "Learn from Input" button (activates listening to human input).
        *   "Suggest Ideas" button (AI generates new patterns based on current style).
        *   Visual representation of learned patterns/neural network activity (subtle, evolving graph).
        *   **Feedback System:** Thumbs Up/Down or a "Refine" button for learned phrases/rhythms.
        *   **Genre/Style Presets:** Dropdowns for Jazz, Rock, Funk, Electronic, etc.
    *   **Musical Theory Visualizer:** For Keys agent, maybe a circle of fifths or chord progression display.
    *   **MIDI/Pattern Editor (Collapsible):** A mini piano roll or drum sequencer to visualize and directly edit agent-generated parts.

*   **Timeline/Arrangement View:**
    *   A horizontal timeline showing the overall song structure.
    *   Colored tracks for each agent (Bass, Drums, Keys) and human performers.
    *   Drag-and-drop sections, loop markers.
    *   Visual indicators of AI-generated improvisations or variations.

*   **Human Input Monitoring Panel:**
    *   Displays real-time analysis of human performance (e.g., "Human Guitar Input: Playing a C minor progression," "Human Drums: Strong backbeat detected").
    *   Agent Responses: "AI Bass is adapting to new root note." "AI Drums suggested a fill after your last phrase."

### 2. Live Performance Mode UI

This mode is optimized for minimal distraction and maximum responsiveness during a live show, focusing on high-level control and visual feedback.



**Main Content Area Breakdown for Live Mode:**

*   **Large, Central Agent Status Panels (Side-by-Side):**
    *   **Agent Name & Activity Visual:**
        *   **Bass:** Dynamic waveform display, perhaps subtly changing color based on its activity.
        *   **Drums:** Network graph or particle system reacting to beat intensity.
        *   **Keys:** Animated keyboard or abstract harmonic visualizer.
    *   **Key Parameters (Large Sliders/Knobs):** Only the most critical, performable parameters are exposed.
        *   **Bass:** "Groove Intensity," "Harmonic Variation."
        *   **Drums:** "Beat Sync On/Off," "Fill Density," "Energy."
        *   **Keys:** "Arpeggiator On/Off," "Chord Voicing Complexity," "Modulation Depth."
    *   **Textual Status Updates:** "Responding to human guitar lead," "Adding rhythmic variations," "Suggesting new chord inversions."
    *   **Quick Swap Presets:** Small buttons to quickly switch between learned styles or song sections.

*   **Human Input Monitor (Bottom Bar):**
    *   Real-time audio waveform of the human performer.
    *   Textual feedback: "Human Guitar Input: Playing a C minor progression," "AI Bass is adapting to your phrasing."

*   **Minimal Global Controls:** Only play/stop, master volume, and perhaps a global "intensity" slider are easily accessible.

### 3. Settings Panel UI

This panel focuses on system-level configurations and diagnostics.



**Main Content Area Breakdown for Settings Panel:**

*   **Audio Interface Setup:**
    *   Dropdown for Input/Output Device selection.
    *   Sample Rate, Buffer Size sliders.
    *   ASIO/Core Audio Driver Status.
    *   Input/Output level meters.

*   **Latency Calibration:**
    *   Visual representation of round-trip latency (mic to internal processing to output).
    *   Big, clear number displaying current latency (e.g., "4.7 ms").
    *   "Run Calibration" button.
    *   Graph showing historical latency or real-time jitters.

*   **AI Agent Preferences:**
    *   Individual toggles for each agent (On/Off).
    *   Global "AI Sensitivity" slider (how quickly agents react/change).
    *   "Reset Learned Data" button (for all or individual agents).
    *   "Agent Performance Profiles" (e.g., "CPU Saver," "High Performance").

*   **Interface Customization:**
    *   Theme Selector (Dark/Light/Custom).
    *   Accent Color picker.
    *   UI Animation Speed slider.
    *   Font Size/Scale options.

*   **System Diagnostics:**
    *   CPU/GPU usage display.
    *   Memory usage.
    *   Disk I/O (for loading samples, etc.).
    *   Log Viewer (for debugging).
