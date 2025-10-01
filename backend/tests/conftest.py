"""
Pytest configuration for backend tests.
"""

import sys
import os

# Add backend/src to Python path for imports
backend_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
if backend_src not in sys.path:
    sys.path.insert(0, backend_src)
