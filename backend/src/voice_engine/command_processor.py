"""
Command Processor Module
Handles voice command recognition using Whisper
"""

import whisper
import numpy as np
from collections import deque
import asyncio
import threading
import logging
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class CommandProcessor:
    """Processes voice commands using OpenAI Whisper"""
    
    def __init__(self, model_size: str = "medium"):
        """
        Initialize command processor
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large, large-v3)
        """
        logger.info(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        logger.info("Whisper model loaded")
        
        # Audio buffer (10 seconds max @ 16kHz)
        self.audio_buffer = deque(maxlen=16000 * 10)
        
        # Voice activity detection
        self.is_listening = False
        self.silence_threshold = 0.01
        self.silence_duration = 0.0
        self.min_audio_length = 0.5  # Minimum 0.5 seconds of audio
        
        # Command callback
        self._command_callback: Optional[Callable[[str], None]] = None
        
        # Processing lock
        self._processing_lock = threading.Lock()
        self._is_processing = False
        
    def buffer_audio(self, audio_chunk: np.ndarray):
        """
        Accumulate audio until silence detected
        
        Args:
            audio_chunk: Audio data as numpy array
        """
        # Flatten if stereo
        if audio_chunk.ndim > 1:
            audio_chunk = audio_chunk.flatten()
        
        self.audio_buffer.extend(audio_chunk)
        
        # Calculate RMS for voice activity detection
        rms = np.sqrt(np.mean(audio_chunk**2))
        
        if rms > self.silence_threshold:
            self.is_listening = True
            self.silence_duration = 0.0
        elif self.is_listening:
            # Accumulate silence duration
            self.silence_duration += len(audio_chunk) / 16000
            
            # Process after 1 second of silence
            if self.silence_duration > 1.0 and not self._is_processing:
                asyncio.create_task(self._process_command())
                self.is_listening = False
    
    async def _process_command(self):
        """Transcribe and execute command"""
        with self._processing_lock:
            if self._is_processing:
                return
            self._is_processing = True
        
        try:
            # Check minimum length
            audio_duration = len(self.audio_buffer) / 16000
            if audio_duration < self.min_audio_length:
                logger.debug(f"Audio too short: {audio_duration:.2f}s")
                self.audio_buffer.clear()
                return
            
            # Convert buffer to numpy array
            audio = np.array(list(self.audio_buffer), dtype=np.float32)
            
            # Clear buffer before processing
            self.audio_buffer.clear()
            
            logger.info(f"Transcribing {audio_duration:.2f}s of audio...")
            
            # Transcribe with Whisper
            result = await asyncio.to_thread(
                self._transcribe,
                audio
            )
            
            command_text = result['text'].strip()
            
            if command_text:
                logger.info(f"Command recognized: '{command_text}'")
                
                # Execute callback if set
                if self._command_callback:
                    self._command_callback(command_text)
                else:
                    logger.warning("No command callback registered")
            else:
                logger.debug("Empty transcription result")
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")
        finally:
            self._is_processing = False
    
    def _transcribe(self, audio: np.ndarray) -> dict:
        """
        Transcribe audio using Whisper
        
        Args:
            audio: Audio data as numpy array
            
        Returns:
            Transcription result dictionary
        """
        return self.model.transcribe(
            audio,
            language='en',
            task='transcribe',
            fp16=False,  # Use FP32 for CPU compatibility
            temperature=0.0,  # Deterministic output
            compression_ratio_threshold=2.4,
            logprob_threshold=-1.0,
            no_speech_threshold=0.6
        )
    
    def on_command(self, callback: Callable[[str], None]):
        """
        Register callback for recognized commands
        
        Args:
            callback: Function to call with recognized command text
        """
        self._command_callback = callback
        logger.info("Command callback registered")


# Command routing and execution
class CommandRouter:
    """Routes voice commands to appropriate handlers"""
    
    def __init__(self):
        self.handlers = {}
        
    def register(self, pattern: str, handler: Callable):
        """Register a command handler"""
        self.handlers[pattern] = handler
    
    async def route(self, command: str):
        """Route command to appropriate handler"""
        command_lower = command.lower()
        
        for pattern, handler in self.handlers.items():
            if pattern.lower() in command_lower:
                await handler(command)
                return
        
        logger.warning(f"No handler found for command: {command}")


if __name__ == "__main__":
    # Test the command processor
    import sounddevice as sd
    
    async def test():
        processor = CommandProcessor(model_size="base")  # Use smaller model for testing
        
        def on_command(text):
            print(f"\n🎤 Command: {text}\n")
        
        processor.on_command(on_command)
        
        print("Recording for 10 seconds... Speak now!")
        
        # Record audio
        recording = sd.rec(
            int(10 * 16000),
            samplerate=16000,
            channels=1,
            dtype=np.float32
        )
        sd.wait()
        
        # Process in chunks
        chunk_size = 1600  # 0.1 seconds
        for i in range(0, len(recording), chunk_size):
            chunk = recording[i:i+chunk_size]
            processor.buffer_audio(chunk)
            await asyncio.sleep(0.1)
        
        # Wait for processing
        await asyncio.sleep(3)
    
    asyncio.run(test())
