"""
Core Voice Engine Module
Orchestrates all voice processing components
"""

import asyncio
import numpy as np
import sounddevice as sd
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass
import logging

from .command_processor import CommandProcessor
from .performance_tracker import PerformanceTracker
from .ai_band_interface import AIBandInterface

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AudioConfig:
    """Configuration for audio processing"""
    sample_rate: int = 48000
    channels: int = 2
    buffer_size: int = 128
    command_sample_rate: int = 16000
    device: Optional[str] = None  # None = default device
    command_device: Optional[str] = None


class VoiceEngine:
    """Main voice engine orchestrator for Performia"""
    
    def __init__(self, config: Optional[AudioConfig] = None):
        self.config = config or AudioConfig()
        
        # Initialize components
        self.command_processor = CommandProcessor()
        self.performance_tracker = PerformanceTracker(self.config.sample_rate)
        self.ai_band_interface = AIBandInterface()
        
        # Audio streams
        self.performance_stream: Optional[sd.InputStream] = None
        self.command_stream: Optional[sd.InputStream] = None
        
        # Callbacks
        self.command_callback: Optional[Callable] = None
        self.performance_callback: Optional[Callable] = None
        
        # State
        self.is_running = False
        
    async def start(self):
        """Initialize and start all voice engine components"""
        logger.info("Starting Performia Voice Engine...")
        
        try:
            await asyncio.gather(
                self._start_performance_stream(),
                self._start_command_stream(),
                self.ai_band_interface.connect()
            )
            self.is_running = True
            logger.info("Voice Engine started successfully")
        except Exception as e:
            logger.error(f"Failed to start Voice Engine: {e}")
            raise
    
    async def stop(self):
        """Stop all voice engine components"""
        logger.info("Stopping Voice Engine...")
        
        if self.performance_stream:
            self.performance_stream.stop()
            self.performance_stream.close()
        
        if self.command_stream:
            self.command_stream.stop()
            self.command_stream.close()
        
        self.is_running = False
        logger.info("Voice Engine stopped")
    
    async def _start_performance_stream(self):
        """Start high-fidelity audio stream for AI Conductor"""
        logger.info(
            f"Starting performance stream: {self.config.sample_rate}Hz, "
            f"{self.config.channels}ch, buffer={self.config.buffer_size}"
        )
        
        self.performance_stream = sd.InputStream(
            samplerate=self.config.sample_rate,
            channels=self.config.channels,
            blocksize=self.config.buffer_size,
            device=self.config.device,
            callback=self._performance_audio_callback
        )
        self.performance_stream.start()
    
    async def _start_command_stream(self):
        """Start voice command recognition stream"""
        logger.info(
            f"Starting command stream: {self.config.command_sample_rate}Hz, mono"
        )
        
        self.command_stream = sd.InputStream(
            samplerate=self.config.command_sample_rate,
            channels=1,
            device=self.config.command_device,
            callback=self._command_audio_callback
        )
        self.command_stream.start()
    
    def _performance_audio_callback(self, indata, frames, time, status):
        """Real-time performance audio processing"""
        if status:
            logger.warning(f'Performance stream status: {status}')
        
        try:
            # Process audio for AI Conductor
            features = self.performance_tracker.process_audio(indata.copy())
            
            # Call user-defined callback if set
            if self.performance_callback:
                self.performance_callback(features)
                
        except Exception as e:
            logger.error(f"Error in performance callback: {e}")
    
    def _command_audio_callback(self, indata, frames, time, status):
        """Voice command audio processing"""
        if status:
            logger.warning(f'Command stream status: {status}')
        
        try:
            # Buffer audio for Whisper processing
            self.command_processor.buffer_audio(indata.copy())
        except Exception as e:
            logger.error(f"Error in command callback: {e}")
    
    def on_command(self, callback: Callable[[str], None]):
        """Register callback for voice commands"""
        self.command_processor.on_command(callback)
    
    def on_performance_update(self, callback: Callable[[Dict[str, Any]], None]):
        """Register callback for performance updates"""
        self.performance_callback = callback
    
    async def send_to_ai_band(self, message: str) -> str:
        """Send message to AI Band and get response"""
        return await self.ai_band_interface.process_conversation(message)
    
    def get_audio_devices(self) -> Dict[str, Any]:
        """List available audio devices"""
        devices = sd.query_devices()
        return {
            'devices': devices,
            'default_input': sd.default.device[0],
            'default_output': sd.default.device[1]
        }


if __name__ == "__main__":
    # Example usage
    async def main():
        # Create engine
        engine = VoiceEngine()
        
        # Register callbacks
        engine.on_command(lambda cmd: print(f"Command received: {cmd}"))
        engine.on_performance_update(lambda features: print(f"Pitch: {features['pitch']:.2f}Hz"))
        
        # Start engine
        await engine.start()
        
        # Run for 30 seconds
        await asyncio.sleep(30)
        
        # Stop engine
        await engine.stop()
    
    asyncio.run(main())
