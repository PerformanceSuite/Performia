#!/bin/bash
# Quick script to run the Song Map API server

echo "Starting Performia Song Map API..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/Users/danielconnolly/Projects/Performia/backend/src

# Run server
echo "Server starting at http://localhost:8000"
echo "Interactive docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python src/services/api/main.py
