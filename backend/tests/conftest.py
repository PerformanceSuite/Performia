"""
Pytest configuration for backend tests.
"""

import sys
import os

# Add backend/src to Python path for imports
backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
backend_src = os.path.join(backend_root, 'src')

if backend_src not in sys.path:
    sys.path.insert(0, backend_src)
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)
