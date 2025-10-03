#!/bin/bash
#
# Quick Song Map validation script
# Activates venv and runs validator
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Run validator with all arguments passed through
python validate_song_map.py "$@"
