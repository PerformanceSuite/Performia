"""
Real-time performance API endpoints.

Provides WebSocket connection for Living Chart teleprompter updates
using the Song Map position tracker.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict, Optional, List
import asyncio
import time
import json
import logging

from ...realtime.audio_input import RealtimeAudioInput
from ...realtime.analyzer import RealtimeAnalyzer
from ...realtime.position_tracker import SongMapPositionTracker

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/performance", tags=["performance"])


class PerformanceSession:
    """Manages a single live performance session."""

    def __init__(self, song_map: Dict):
        self.song_map = song_map
        self.audio_input: Optional[RealtimeAudioInput] = None
        self.analyzer: Optional[RealtimeAnalyzer] = None
        self.tracker: Optional[SongMapPositionTracker] = None
        self.is_running = False
        self.websocket: Optional[WebSocket] = None

    async def start(self, websocket: WebSocket):
        """Start performance session."""
        self.websocket = websocket

        # Initialize components
        self.audio_input = RealtimeAudioInput(
            block_size=512,  # 11.6ms latency
            sample_rate=44100,
            channels=1
        )
        self.analyzer = RealtimeAnalyzer(sample_rate=44100)
        self.tracker = SongMapPositionTracker(self.song_map)

        # Start audio input
        self.audio_input.start()
        self.tracker.start()

        self.is_running = True

        # Send initial position
        await self._send_position_update()

        logger.info("Performance session started")

    async def stop(self):
        """Stop performance session."""
        self.is_running = False

        if self.audio_input:
            self.audio_input.stop()

        logger.info("Performance session stopped")

    async def process_audio_loop(self):
        """Main audio processing loop."""
        try:
            while self.is_running:
                # Get audio block
                try:
                    audio_block = self.audio_input.get_block(timeout=0.1)

                    # Flatten to mono if needed
                    if len(audio_block.shape) > 1:
                        audio_block = audio_block.mean(axis=1)

                    # Detect onset
                    onset_detected = self.analyzer.detect_onset(audio_block)

                    # Update position
                    position = self.tracker.update(onset_detected=onset_detected)

                    # Send update to frontend if onset detected or every 10th block
                    if onset_detected or (self.audio_input.blocks_captured % 10 == 0):
                        await self._send_position_update()

                except Exception as e:
                    logger.error(f"Error processing audio block: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error in audio loop: {e}")
            raise

    async def _send_position_update(self):
        """Send position update to frontend via WebSocket."""
        if not self.websocket or not self.tracker:
            return

        position = self.tracker.position
        current_syllable = self.tracker.get_current_syllable()
        current_section = self.tracker.get_current_section()
        upcoming = self.tracker.get_lookahead(seconds=3.0)

        update = {
            'type': 'position_update',
            'timestamp': time.time(),
            'position': {
                'song_time': position.song_time,
                'section_index': position.section_index,
                'line_index': position.line_index,
                'syllable_index': position.syllable_index,
                'confidence': position.confidence,
                'tempo_ratio': position.tempo_ratio
            },
            'current': {
                'syllable': current_syllable,
                'section': current_section.name if current_section else None
            },
            'upcoming': upcoming[:10],  # Next 10 syllables
            'stats': self.tracker.get_stats()
        }

        try:
            await self.websocket.send_json(update)
        except Exception as e:
            logger.error(f"Error sending position update: {e}")


# Global session storage (in production, use Redis or similar)
active_sessions: Dict[str, PerformanceSession] = {}


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time performance updates.

    The frontend connects to this endpoint and receives:
    - Real-time position updates
    - Current syllable/line/section
    - Upcoming syllables for teleprompter
    - Tracking statistics

    Message format:
    {
        "type": "position_update",
        "timestamp": 1234567890.123,
        "position": {
            "song_time": 2.5,
            "section_index": 0,
            "line_index": 1,
            "syllable_index": 3,
            "confidence": 0.95,
            "tempo_ratio": 1.05
        },
        "current": {
            "syllable": {"text": "way", "startTime": 2.5, "chord": "C"},
            "section": "Verse 1"
        },
        "upcoming": [...],
        "stats": {...}
    }
    """
    await websocket.accept()

    session = active_sessions.get(session_id)
    if not session:
        await websocket.send_json({
            'type': 'error',
            'message': f'Session {session_id} not found. Start a session first.'
        })
        await websocket.close()
        return

    try:
        # Start session
        await session.start(websocket)

        # Send session started message
        await websocket.send_json({
            'type': 'session_started',
            'session_id': session_id,
            'song_title': session.song_map.get('title', 'Unknown')
        })

        # Run audio processing loop
        await session.process_audio_loop()

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"Error in WebSocket handler: {e}")
        await websocket.send_json({
            'type': 'error',
            'message': str(e)
        })
    finally:
        await session.stop()


@router.post("/sessions")
async def create_session(song_id: str):
    """
    Create a new performance session for a song.

    Args:
        song_id: ID of the song to perform

    Returns:
        Session ID for WebSocket connection
    """
    # Load Song Map from database/filesystem
    # For now, use a placeholder
    # TODO: Integrate with library service to load Song Map

    song_map = {
        'title': 'Test Song',
        'artist': 'Test Artist',
        'sections': []
    }

    # Generate session ID
    session_id = f"session_{int(time.time() * 1000)}"

    # Create session
    session = PerformanceSession(song_map)
    active_sessions[session_id] = session

    return {
        'session_id': session_id,
        'song_id': song_id,
        'websocket_url': f'/performance/ws/{session_id}'
    }


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a performance session.

    Args:
        session_id: ID of session to delete
    """
    session = active_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    await session.stop()
    del active_sessions[session_id]

    return {'message': 'Session deleted'}


@router.get("/sessions/{session_id}/status")
async def get_session_status(session_id: str):
    """
    Get status of a performance session.

    Args:
        session_id: ID of session

    Returns:
        Session status and statistics
    """
    session = active_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    stats = {}
    if session.tracker:
        stats = session.tracker.get_stats()

    audio_stats = {}
    if session.audio_input:
        audio_stats = session.audio_input.get_stats()

    return {
        'session_id': session_id,
        'is_running': session.is_running,
        'tracking_stats': stats,
        'audio_stats': audio_stats
    }
