#!/usr/bin/env python3
"""
Simple test runner for audio input tests.

This runner allows tests to execute without pytest configuration issues.
"""

import sys
import os

# Add backend/src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

# Now run tests using pytest
import pytest

if __name__ == '__main__':
    # Run with verbose output
    sys.exit(pytest.main([__file__.replace('run_tests.py', 'test_audio_input.py'), '-v', '-s']))
