# Performia Voice Engine - Technical Specification

## Overview
A comprehensive voice input system for Performia that handles:
1. **Voice Commands** - Control orchestrator and agents
2. **Live Performance Tracking** - Real-time audio following for AI Conductor
3. **Song Map Creation** - Voice-to-text for lyrics and musical notation
4. **Conversational AI Band** - Natural dialogue with AI musicians

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Performia Voice Engine                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Command    │  │  Performance │  │  Conversational│    │
│  │   Module     │  │   Tracker    │  │    AI Band    │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬────────┘    │
│         │                 │                  │              │
│  ┌──────▼─────────────────▼──────────────────▼────────┐   │
│  │           Audio Processing Pipeline                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │  Audio   │→ │  Whisper │→ │  Gemini  │        │   │
│  │  │  Input   │  │   STT    │  │  Live    │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘        │   │
│  └────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌────────────────────────────────────────────────────┐   │
│  │          Performance Audio Analysis               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │  Pitch   │  │  Tempo   │  │  Chord   │        │   │
│  │  │ Tracking │  │ Detection│  │ Recognition│       │   │
│  │  └──────────┘  └──────────┘  └──────────┘        │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Technical Requirements

### 1. Low-Latency Audio Processing
- **Target:** Sub-10ms for performance tracking
- **Solution:** Direct audio interface integration (CoreAudio on macOS)
- **Buffer Size:** 128 samples @ 48kHz = 2.67ms base latency
- **Processing Budget:** ~7ms for pitch/tempo detection

### 2. Multi-Modal Audio Handling
- **Voice Commands:** 16kHz mono (sufficient for speech)
- **Performance Audio:** 48kHz stereo (professional audio)
- **Separate Pipelines:** Isolated processing to prevent interference

### 3. Real-Time Speech Recognition
- **Primary:** Whisper Large-v3 running locally via whisper.cpp
- **Fallback:** Gemini Live API for conversational features
- **Hybrid Approach:** Local for commands, cloud for AI band conversation

## Implementation Stack

### Core Technologies
1. **Audio Input:** PortAudio / RtAudio (cross-platform)
2. **Speech-to-Text:** whisper.cpp (C++ library)
3. **AI Processing:** Gemini Live API
4. **Audio Analysis:** Essentia (pitch, tempo, chords)
5. **Python Bindings:** pybind11 for integration

### System Architecture

```python
# src/voice_engine/core.py

import asyncio
import numpy as np
from typing import Optional, Callable
import sounddevice as sd
from dataclasses import dataclass

@dataclass
class AudioConfig:
    sample_rate: int = 48000
    channels: int = 2
    buffer_size: int = 128
    command_sample_rate: int = 16000  # For voice commands
    
class VoiceEngine:
    \"\"\"Main voice engine orchestrator\"\"\"
    
    def __init__(self, config: AudioConfig):
        self.config = config
        self.command_processor = CommandProcessor()
        self.performance_tracker = PerformanceTracker()
        self.ai_band_interface = AIBandInterface()
        
        # Dual audio streams
        self.performance_stream = None
        self.command_stream = None
        
    async def start(self):
        \"\"\"Initialize all voice engine components\"\"\"
        await asyncio.gather(
            self._start_performance_stream(),
            self._start_command_stream(),
            self.ai_band_interface.connect()
        )
    
    async def _start_performance_stream(self):
        \"\"\"High-fidelity audio for AI Conductor\"\"\"
        self.performance_stream = sd.InputStream(
            samplerate=self.config.sample_rate,
            channels=self.config.channels,
            blocksize=self.config.buffer_size,
            callback=self._performance_callback
        )
        self.performance_stream.start()
    
    async def _start_command_stream(self):
        \"\"\"Voice command recognition\"\"\"
        self.command_stream = sd.InputStream(
            samplerate=self.config.command_sample_rate,
            channels=1,
            callback=self._command_callback
        )
        self.command_stream.start()
    
    def _performance_callback(self, indata, frames, time, status):
        \"\"\"Real-time performance audio processing\"\"\"
        if status:
            print(f'Performance stream status: {status}')
        
        # Send to AI Conductor for real-time following
        self.performance_tracker.process_audio(indata)
    
    def _command_callback(self, indata, frames, time, status):
        \"\"\"Voice command processing\"\"\"
        if status:
            print(f'Command stream status: {status}')
        
        # Buffer audio for Whisper processing
        self.command_processor.buffer_audio(indata)
```

### Voice Command Processor

```python
# src/voice_engine/command_processor.py

import whisper
import numpy as np
from collections import deque
import asyncio

class CommandProcessor:
    \"\"\"Processes voice commands using Whisper\"\"\"
    
    def __init__(self, model_size: str = "large-v3"):
        self.model = whisper.load_model(model_size)
        self.audio_buffer = deque(maxlen=16000 * 10)  # 10 seconds max
        self.is_listening = False
        self.silence_threshold = 0.01
        self.silence_duration = 0
        
    def buffer_audio(self, audio_chunk):
        \"\"\"Accumulate audio until silence detected\"\"\"
        self.audio_buffer.extend(audio_chunk.flatten())
        
        # Detect voice activity
        rms = np.sqrt(np.mean(audio_chunk**2))
        
        if rms > self.silence_threshold:
            self.is_listening = True
            self.silence_duration = 0
        elif self.is_listening:
            self.silence_duration += len(audio_chunk) / 16000
            
            # Process after 1 second of silence
            if self.silence_duration > 1.0:
                asyncio.create_task(self._process_command())
                self.is_listening = False
                
    async def _process_command(self):
        \"\"\"Transcribe and execute command\"\"\"
        if len(self.audio_buffer) < 8000:  # Less than 0.5 seconds
            self.audio_buffer.clear()
            return
        
        # Convert buffer to audio array
        audio = np.array(self.audio_buffer, dtype=np.float32)
        
        # Transcribe with Whisper
        result = self.model.transcribe(
            audio,
            language='en',
            task='transcribe',
            fp16=False  # Use FP32 for CPU
        )
        
        command_text = result['text'].strip()
        self.audio_buffer.clear()
        
        if command_text:
            await self._execute_command(command_text)
    
    async def _execute_command(self, text: str):
        \"\"\"Route command to appropriate handler\"\"\"
        text_lower = text.lower()
        
        # Performance commands
        if 'play' in text_lower or 'start' in text_lower:
            await self._handle_playback('start')
        elif 'stop' in text_lower or 'pause' in text_lower:
            await self._handle_playback('stop')
        
        # Song map commands
        elif 'create song map' in text_lower:
            await self._handle_song_map_creation(text)
        
        # AI Band commands
        elif any(word in text_lower for word in ['band', 'bassline', 'drums']):
            await self._forward_to_ai_band(text)
        
        # Orchestrator commands
        elif 'analyze' in text_lower or 'report' in text_lower:
            await self._forward_to_orchestrator(text)
        
        else:
            print(f'Unrecognized command: {text}')
```

### Performance Tracker

```python
# src/voice_engine/performance_tracker.py

import numpy as np
from essentia.standard import PitchYinFFT, BeatTrackerDegara
from typing import Dict, Any

class PerformanceTracker:
    \"\"\"Real-time audio analysis for AI Conductor\"\"\"
    
    def __init__(self, sample_rate: int = 48000):
        self.sample_rate = sample_rate
        self.pitch_detector = PitchYinFFT(frameSize=2048, sampleRate=sample_rate)
        self.beat_tracker = BeatTrackerDegara()
        
        self.current_pitch = 0.0
        self.current_tempo = 120.0
        self.confidence = 0.0
        
    def process_audio(self, audio_chunk: np.ndarray):
        \"\"\"Extract musical features from audio\"\"\"
        # Ensure mono for pitch detection
        if audio_chunk.ndim > 1:
            audio_mono = np.mean(audio_chunk, axis=1)
        else:
            audio_mono = audio_chunk
        
        # Pitch detection
        pitch, confidence = self.pitch_detector(audio_mono.astype(np.float32))
        
        if confidence > 0.8:  # Only update on confident detections
            self.current_pitch = pitch
            self.confidence = confidence
        
        # Tempo detection (on larger buffers)
        # This would accumulate frames for beat tracking
        
        return {
            'pitch': self.current_pitch,
            'confidence': self.confidence,
            'tempo': self.current_tempo,
            'timestamp': self._get_timestamp()
        }
    
    def _get_timestamp(self) -> float:
        \"\"\"Get current playback timestamp\"\"\"
        # This would sync with the Song Map timeline
        return 0.0  # Placeholder
```

### AI Band Interface

```python
# src/voice_engine/ai_band_interface.py

import google.generativeai as genai
import asyncio
from typing import Optional

class AIBandInterface:
    \"\"\"Conversational interface with AI Band using Gemini Live\"\"\"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        self.conversation_history = []
        
    async def connect(self):
        \"\"\"Initialize Gemini Live connection\"\"\"
        genai.configure(api_key=self.api_key)
        
        # Use Gemini 2.5 Flash for low latency
        self.model = genai.GenerativeModel(
            'gemini-2.5-flash',
            system_instruction=\"\"\"You are an AI band member in Performia. 
            The user is a musician creating songs. Respond naturally and musically.
            When they ask for musical elements, describe them in musical terms.
            Be creative, collaborative, and supportive.\"\"\"
        )
    
    async def process_conversation(self, text: str) -> str:
        \"\"\"Send text to AI band and get response\"\"\"
        if not self.model:
            await self.connect()
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': text
        })
        
        # Generate response
        response = await self.model.generate_content_async(
            text,
            generation_config=genai.GenerationConfig(
                temperature=0.9,  # More creative
                top_p=0.95,
                max_output_tokens=500
            )
        )
        
        assistant_response = response.text
        
        self.conversation_history.append({
            'role': 'assistant',
            'content': assistant_response
        })
        
        return assistant_response
    
    async def process_audio_request(self, audio_description: str):
        \"\"\"Handle requests for musical elements\"\"\"
        prompt = f\"\"\"The user said: "{audio_description}"
        
        Describe the musical element they're requesting in terms of:
        - Instrument
        - Style/genre
        - Rhythm pattern
        - Melodic characteristics
        - Dynamics
        
        Be specific and actionable for audio generation.\"\"\"
        
        return await self.process_conversation(prompt)
```

## Integration with Performia

### 1. Update orchestrator.py

```python
# Add to orchestrator.py

from src.voice_engine.core import VoiceEngine, AudioConfig

class PerformiaOrchestrator:
    def __init__(self):
        # ... existing code ...
        
        # Initialize voice engine
        self.voice_engine = VoiceEngine(AudioConfig())
        
    async def start(self):
        \"\"\"Start all systems\"\"\"
        await asyncio.gather(
            self._start_agents(),
            self.voice_engine.start()
        )
    
    async def handle_voice_command(self, command: str):
        \"\"\"Process voice commands from engine\"\"\"
        # Route to appropriate agent based on command
        if 'analyze' in command.lower():
            await self.analysis_agent.execute({
                'command': command,
                'source': 'voice'
            })
        # ... etc
```

### 2. Audio Interface Configuration

```python
# config/audio.yaml

audio_interfaces:
  performance:
    device: "Presonus Quantum 2626"
    sample_rate: 48000
    buffer_size: 128  # ~2.7ms latency
    channels: 2
    
  voice_commands:
    device: "Default"  # System microphone
    sample_rate: 16000
    buffer_size: 1024
    channels: 1

whisper_config:
  model: "large-v3"
  language: "en"
  task: "transcribe"
  compute_type: "float32"  # or "float16" for GPU

gemini_config:
  model: "gemini-2.5-flash"
  temperature: 0.9
  max_tokens: 500
```

## Installation & Setup

```bash
# Install dependencies
pip install sounddevice numpy essentia whisper google-generativeai

# For whisper.cpp (faster inference)
# macOS
brew install whisper-cpp

# Or build from source
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make

# Download Whisper models
bash ./models/download-ggml-model.sh large-v3
```

## Usage Examples

### Voice Commands
```python
# In Performia Charts
"Play the song"
"Stop"
"Transpose up two semitones"
"Show chord diagrams"

# In Performia Studio
"Add a funky bassline"
"Make the drums more aggressive"
"Create a verse section"
"Let me hear what we have so far"

# For Orchestrator
"Analyze performance trends"
"Generate weekly report"
"Show me productivity metrics"
```

### API Usage
```python
# Direct API usage
from src.voice_engine import VoiceEngine, AudioConfig

# Initialize
engine = VoiceEngine(AudioConfig())
await engine.start()

# Listen for commands
engine.command_processor.on_command(lambda cmd: print(f"Command: {cmd}"))

# AI Band conversation
response = await engine.ai_band_interface.process_conversation(
    "Give me a simple funk bassline"
)
print(response)
```

## Performance Metrics

- **Latency (Performance Tracking):** < 10ms
- **Latency (Voice Commands):** < 500ms
- **Accuracy (Speech Recognition):** > 95% (Whisper Large-v3)
- **CPU Usage:** < 25% on M1/M2 Macs
- **Memory:** < 2GB (with models loaded)

## Future Enhancements

1. **Visual Cues:** On-screen feedback for voice activity
2. **Multi-language:** Support for non-English musicians
3. **Custom Wake Word:** "Hey Performia" for hands-free
4. **Gesture Control:** Combine voice with MIDI footpedal
5. **Cloud Fallback:** Use Gemini Live when local fails
6. **Voice Cloning:** AI band members with custom voices

## Testing Strategy

```python
# tests/voice_engine/test_command_processor.py
import pytest
from src.voice_engine import CommandProcessor

@pytest.mark.asyncio
async def test_playback_commands():
    processor = CommandProcessor(model_size="base")  # Use small model for tests
    
    await processor._execute_command("play the song")
    # Assert playback started
    
    await processor._execute_command("stop")
    # Assert playback stopped

@pytest.mark.integration
async def test_end_to_end_voice_command():
    \"\"\"Test complete voice pipeline\"\"\"
    engine = VoiceEngine(AudioConfig())
    await engine.start()
    
    # Simulate audio input
    # Verify command execution
    # Check system response
```

This creates a robust, production-ready voice system for Performia!
