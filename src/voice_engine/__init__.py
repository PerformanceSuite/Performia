"""
Performia Voice Engine
A comprehensive voice input system for real-time audio processing and AI interaction
"""

__version__ = "1.0.0"

from .core import VoiceEngine, AudioConfig
from .command_processor import CommandProcessor
from .performance_tracker import PerformanceTracker
from .ai_band_interface import AIBandInterface

__all__ = [
    'VoiceEngine',
    'AudioConfig',
    'CommandProcessor',
    'PerformanceTracker',
    'AIBandInterface',
]
