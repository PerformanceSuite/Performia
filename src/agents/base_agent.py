"""
Base Musical Agent class with personality and memory capabilities
"""

import asyncio
import numpy as np
import time
from collections import deque
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class BaseMusicalAgent:
    """Base class for musical agents with personality and memory
    
    Note: Removed AutoGen dependency since we're not using LLM capabilities,
    just the multi-agent coordination pattern.
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        personality,
        shared_context,
        event_buffer,
        sc_engine
    ):
        self.name = name
        
        self.role = role
        self.personality = personality
        self.shared_context = shared_context
        self.event_buffer = event_buffer
        self.sc_engine = sc_engine
        
        # Agent-specific memory
        self.short_term_memory = deque(maxlen=32)
        self.current_pattern = []
        self.last_note_time = 0
        
        # Performance state
        self.active_notes = {}
        self.agent_id = f"{name}_{id(self)}"
        
        # Musical state
        self.current_scale = self.determine_scale()
        self.rhythm_pattern = self.generate_rhythm_pattern()
        
        logger.info(f"✓ Created {role} agent: {name}")
    
    def determine_scale(self) -> List[int]:
        """Determine scale based on current key and mode"""
        key = self.shared_context.key_signature.value
        mode = self.shared_context.mode.value
        
        # Scale patterns
        scales = {
            0: [0, 2, 4, 5, 7, 9, 11],  # Major
            1: [0, 2, 3, 5, 7, 8, 10],  # Natural Minor
            2: [0, 2, 3, 5, 7, 9, 10],  # Dorian
            3: [0, 1, 3, 5, 7, 8, 10],  # Phrygian
            4: [0, 2, 4, 6, 7, 9, 11],  # Lydian
            5: [0, 2, 4, 5, 7, 9, 10],  # Mixolydian
        }
        
        intervals = scales.get(mode, scales[0])
        return [(key + i) % 12 for i in intervals]
    
    def generate_rhythm_pattern(self) -> List[int]:
        """Generate rhythm pattern based on personality"""
        pattern = []
        density = self.personality.aggression * 0.5 + 0.3
        
        for i in range(16):
            if self.personality.preferred_rhythm == "syncopated":
                if i % 3 == 0 or (i + 1) % 4 == 0:
                    pattern.append(1 if np.random.random() < density else 0)
                else:
                    pattern.append(0)
            else:
                if i % 4 == 0:
                    pattern.append(1)
                elif i % 2 == 0 and np.random.random() < density:
                    pattern.append(1)
                else:
                    pattern.append(0)
        
        return pattern
    
    async def listen_and_respond(self):
        """Main loop: listen to other agents and respond musically"""
        while True:
            # Check for new events from other agents
            event = self.event_buffer.read(self.agent_id)
            
            if event and event['agent_id'] != self.agent_id:
                # Process musical event from another agent
                await self.process_musical_event(event)
            
            # Generate own musical contribution based on context
            current_time = time.perf_counter()
            if current_time - self.last_note_time > self.get_next_note_timing():
                await self.generate_and_play()
                self.last_note_time = current_time
            
            # Ultra-short sleep to prevent CPU spinning
            await asyncio.sleep(0.001)
    
    async def process_musical_event(self, event: dict):
        """Process and respond to another agent's musical event"""
        self.short_term_memory.append(event)
        
        # Handle guitar input events
        if event.get('source') == 'guitar_input':
            await self.process_guitar_input(event.get('data', {}))
            return
        
        # Analyze musical content
        if 'note' in event:
            note = event['note']
            
            # Check if we should respond
            if np.random.random() < self.personality.responsiveness:
                if self.personality.call_response and event.get('is_call'):
                    await self.generate_response(note)
    
    async def process_guitar_input(self, analysis_data: dict):
        """Process guitar input and respond musically"""
        # Extract relevant features
        pitch = analysis_data.get('pitch')
        chord = analysis_data.get('chord')
        onset_strength = analysis_data.get('onset_strength', 0)
        
        # Only respond to significant events
        if onset_strength > 0.3 or chord:
            # Different responses based on role
            if self.role == "drums" and onset_strength > 0.5:
                # Drums follow the rhythm
                self.sc_engine.play_drum("kick", velocity=min(onset_strength, 1.0))
            elif self.role == "bass" and pitch:
                # Bass follows the root note
                bass_note = int(pitch // 1) % 12 + 36  # Convert to bass range
                self.sc_engine.play_bass(bass_note, velocity=0.5)
            elif self.role == "harmony" and chord:
                # Harmony plays supporting chords
                # Simple chord following for now
                root = 60 + (chord.get('root', 0) if isinstance(chord, dict) else 0)
                chord_notes = [root, root + 4, root + 7]  # Major triad
                self.sc_engine.play_chord(chord_notes, velocity=0.3)
            elif self.role == "melody" and pitch:
                # Melody responds with complementary notes
                melody_note = int(pitch)
                if 60 <= melody_note <= 84:  # Reasonable range
                    self.sc_engine.play_lead(melody_note, velocity=0.4)
    
    async def generate_and_play(self):
        """Generate and play musical content based on agent role"""
        if self.role == "drums":
            await self.play_drum_pattern()
        elif self.role == "bass":
            await self.play_bass_line()
        elif self.role == "melody":
            await self.play_melody()
        elif self.role == "harmony":
            await self.play_harmony()
        elif self.role == "listener":
            # Listener agent doesn't generate its own music
            pass
    
    async def play_drum_pattern(self):
        """Play a drum pattern based on rhythm pattern"""
        beat_index = int(time.time() * 4) % 16  # 16th notes
        
        if self.rhythm_pattern[beat_index]:
            # Vary drum sounds based on beat position
            if beat_index % 4 == 0:  # Kick on downbeats
                self.sc_engine.play_drum("kick", velocity=0.8)
            elif beat_index % 8 == 4:  # Snare on backbeats
                self.sc_engine.play_drum("snare", velocity=0.6)
            else:  # Hi-hat fills
                self.sc_engine.play_drum("hihat", velocity=0.3)
            
            # Add to event buffer for other agents
            event = {
                'agent_id': self.agent_id,
                'role': self.role,
                'type': 'drum',
                'beat': beat_index,
                'timestamp': time.perf_counter()
            }
            self.event_buffer.write(self.agent_id, event)
    
    async def play_bass_line(self):
        """Play a bass line following the scale"""
        # Use root note and fifth primarily
        note_options = [60 + self.current_scale[0], 60 + self.current_scale[4]]  # Root and fifth
        note = int(np.random.choice(note_options))  # Convert to Python int
        
        self.sc_engine.play_bass(note, velocity=0.5, duration=0.5)
        
        event = {
            'agent_id': self.agent_id,
            'role': self.role,
            'type': 'bass',
            'note': note,
            'timestamp': time.perf_counter()
        }
        self.event_buffer.write(self.agent_id, event)
    
    async def play_melody(self):
        """Play melodic lines"""
        # Choose notes from the scale with some randomness
        octave = 72  # Higher octave for melody
        note = octave + int(np.random.choice(self.current_scale))  # Convert to Python int
        
        # Add some variation in rhythm
        if np.random.random() < self.personality.creativity:
            duration = np.random.choice([0.25, 0.5, 0.75])
        else:
            duration = 0.5
        
        self.sc_engine.play_lead(note, velocity=0.4, duration=duration)
        
        event = {
            'agent_id': self.agent_id,
            'role': self.role,
            'type': 'melody',
            'note': note,
            'timestamp': time.perf_counter()
        }
        self.event_buffer.write(self.agent_id, event)
    
    async def play_harmony(self):
        """Play harmonic support"""
        # Build chords from the scale
        root_index = int(np.random.choice([0, 3, 4]))  # I, IV, or V - convert to Python int
        chord_notes = [
            60 + self.current_scale[root_index],
            60 + self.current_scale[(root_index + 2) % 7],
            60 + self.current_scale[(root_index + 4) % 7]
        ]
        
        self.sc_engine.play_chord(chord_notes, velocity=0.3)
        
        event = {
            'agent_id': self.agent_id,
            'role': self.role,
            'type': 'harmony',
            'notes': chord_notes,
            'timestamp': time.perf_counter()
        }
        self.event_buffer.write(self.agent_id, event)
    
    async def generate_response(self, note):
        """Generate a response to another agent's note"""
        pass
    
    def get_next_note_timing(self) -> float:
        """Determine when to play next note"""
        tempo = self.shared_context.tempo.value
        beat_duration = 60.0 / tempo
        
        if self.personality.stability > 0.8:
            return beat_duration / 4
        else:
            base_time = beat_duration / 4
            variation = (1 - self.personality.stability) * 0.02
            return base_time + np.random.uniform(-variation, variation)
    
    def midi_to_freq(self, midi_note: int) -> float:
        """Convert MIDI note to frequency"""
        return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))
