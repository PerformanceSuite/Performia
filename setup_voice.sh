#!/bin/bash
echo "Setting up voice control..."

# For Mac users
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "
    For Mac users:
    1. Download Super Whisper: https://superwhisper.com
    2. Set hotkey to Cmd+Shift+Space
    3. Enable 'Smart silence detection'
    4. Test with: 'Create a performance review for John Smith'
    "
    open https://superwhisper.com
else
    echo "
    For all platforms:
    1. Download Wispr Flow: https://wisprflow.ai
    2. It works with Cursor, Windsurf, and terminal
    3. Free tier available
    4. Press hotkey and start speaking your commands
    "
    open https://wisprflow.ai
fi
