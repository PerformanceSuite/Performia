# Super Whisper Configuration Guide

## Quick Setup for Each App

### 🎯 Speaking to Claude (Browser/Desktop App)

1. **Set Your Mode:**
   - Open Super Whisper preferences
   - Choose Mode: "Focus App Mode" (recommended)
   - This means it only transcribes when Claude is the active window

2. **Configure Hotkey:**
   - Set to: Cmd+Shift+Space (or your preference)
   - Enable: "Hold to record" OR "Press to start/stop"

3. **Text Input Method:**
   - Select: "Type to focused app"
   - Enable: "Auto-send with Enter" (optional but recommended)

4. **To speak to Claude:**
   - Click on Claude's input field first
   - Press and hold Cmd+Shift+Space
   - Speak your command
   - Release to send
   - Text appears instantly in Claude

### 🚀 Speaking to Terminal/Goose

1. **Terminal-Specific Settings:**
   - Mode: "Focus App Mode" 
   - Custom command: Add Terminal to "Allowed Apps"
   
2. **For Goose commands:**
   - Focus Terminal window
   - Type "goose " first
   - Press hotkey
   - Say: "analyze performance metrics for last month"
   - It types: "analyze performance metrics for last month"
   - Press Enter to execute

### 💻 Speaking to Cursor/Windsurf

1. **IDE Configuration:**
   - Add Cursor/Windsurf to "Allowed Apps"
   - Enable: "Paste as single line" (for commands)
   - Disable: "Paste as single line" (for code generation)

2. **Two ways to use:**

   **For Chat/Cascade:**
   - Click in the AI chat panel
   - Hold hotkey
   - Say: "refactor this function to use async await"
   
   **For Inline Editing:**
   - Select code
   - Press Cmd+K (Cursor) or Ctrl+I (Windsurf)
   - Hold Super Whisper hotkey
   - Say your instruction

### 🎤 Advanced Super Whisper Settings

**Recommended Global Settings:**
```
General:
- Default Mode: Focus App Mode
- Hotkey: Cmd+Shift+Space
- Recording: Hold to record (more control)

Transcription:
- Model: "Accurate" (best for technical terms)
- Language: English
- Show transcription window: ON

Advanced:
- Silence threshold: 2 seconds
- Max recording time: 2 minutes
- Process while recording: ON (see text as you speak)
```

### 📝 Custom Replacements for Technical Terms

Add these in Preferences → Replacements:
- "MCP" → "MCP" (not "NCP")
- "goose" → "goose" (not "geese")
- "npm" → "npm" (not "NPM")
- "API" → "API"
- "UI" → "UI"
- "async" → "async"
- "Performia" → "Performia"

### 🔥 Pro Tips

1. **App-Specific Profiles:**
   Create different profiles for different workflows:
   - "Coding" - single line off, technical vocabulary
   - "Chat" - single line on, natural language
   - "Commands" - adds semicolon at end

2. **Quick App Switching:**
   - Use Cmd+Tab to switch apps
   - Super Whisper follows focus automatically
   - No need to reconfigure between apps

3. **Voice Commands That Work Best:**
   - Be explicit: "Create a function that..." not just "function"
   - Pause briefly between thoughts
   - Say punctuation: "comma", "period", "new line"

4. **For Complex Commands:**
   Instead of: "Make a performance review"
   Say: "Create a comprehensive performance review for John Smith including productivity metrics comma collaboration scores comma and three development goals period"

## Testing Your Setup

### Test with Each App:

1. **Claude Test:**
   - Focus this window
   - Hold Cmd+Shift+Space
   - Say: "What are the best practices for multi-agent orchestration?"
   - Release and watch it type

2. **Terminal Test:**
   - Open Terminal
   - Type: `goose "`
   - Hold hotkey
   - Say: "analyze team productivity"
   - Release, then press Enter

3. **Cursor/Windsurf Test:**
   - Open editor
   - Press Cmd+K or open Cascade
   - Hold hotkey
   - Say: "Generate a Python function to calculate fibonacci numbers"

## Troubleshooting

- **Nothing happens:** Check if app is in "Allowed Apps" list
- **Wrong text:** Adjust vocabulary in Replacements
- **Too slow:** Switch to "Fast" model for quick commands
- **Cuts off:** Increase silence threshold to 3-4 seconds
