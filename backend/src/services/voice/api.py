"""FastAPI service for voice control integration."""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
import tempfile
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Performia Voice Control API",
    description="Voice command interface for Performia development and performance",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class VoiceCommand(BaseModel):
    """Voice command request."""
    text: str
    context: Optional[str] = None


class CommandResponse(BaseModel):
    """Voice command response."""
    success: bool
    action: str
    message: str
    data: Optional[Dict] = None


class TranscriptionResponse(BaseModel):
    """Audio transcription response."""
    text: str
    confidence: float
    segments: Optional[List[Dict]] = None


# Command processor
class VoiceCommandProcessor:
    """Process voice commands for Performia."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def parse_command(self, text: str, context: Optional[str] = None) -> CommandResponse:
        """
        Parse and execute voice command.

        Args:
            text: Command text
            context: Optional context (e.g., "development", "performance")

        Returns:
            CommandResponse with action taken
        """
        text_lower = text.lower().strip()
        self.logger.info(f"Processing command: {text} (context: {context})")

        # Development commands
        if "run" in text_lower and "test" in text_lower:
            return CommandResponse(
                success=True,
                action="run_tests",
                message="Running tests",
                data={"command": "npm test"}
            )

        if "build" in text_lower:
            return CommandResponse(
                success=True,
                action="build",
                message="Building project",
                data={"command": "npm run build"}
            )

        if "start" in text_lower and "dev" in text_lower:
            return CommandResponse(
                success=True,
                action="dev_server",
                message="Starting development server",
                data={"command": "npm run dev"}
            )

        # Performance commands
        if "play" in text_lower or "start" in text_lower:
            if "song" in text_lower or "performance" in text_lower:
                return CommandResponse(
                    success=True,
                    action="start_performance",
                    message="Starting performance mode"
                )

        if "stop" in text_lower or "pause" in text_lower:
            return CommandResponse(
                success=True,
                action="stop_performance",
                message="Stopping performance"
            )

        if "transpose" in text_lower:
            # Extract number if present
            words = text_lower.split()
            try:
                semitones = int([w for w in words if w.lstrip('-').isdigit()][0])
                return CommandResponse(
                    success=True,
                    action="transpose",
                    message=f"Transposing by {semitones} semitones",
                    data={"semitones": semitones}
                )
            except (IndexError, ValueError):
                return CommandResponse(
                    success=False,
                    action="transpose",
                    message="Could not parse transpose value"
                )

        if "tempo" in text_lower or "speed" in text_lower:
            # Extract BPM if present
            words = text_lower.split()
            try:
                bpm = int([w for w in words if w.isdigit()][0])
                return CommandResponse(
                    success=True,
                    action="set_tempo",
                    message=f"Setting tempo to {bpm} BPM",
                    data={"bpm": bpm}
                )
            except (IndexError, ValueError):
                return CommandResponse(
                    success=False,
                    action="set_tempo",
                    message="Could not parse tempo value"
                )

        # Library commands
        if "load" in text_lower or "open" in text_lower:
            song_name = text_lower.replace("load", "").replace("open", "").strip()
            return CommandResponse(
                success=True,
                action="load_song",
                message=f"Loading song: {song_name}",
                data={"song_name": song_name}
            )

        # Unknown command
        return CommandResponse(
            success=False,
            action="unknown",
            message=f"Command not recognized: {text}"
        )


# Global processor instance
processor = VoiceCommandProcessor()


# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "Performia Voice Control API"}


@app.post("/command", response_model=CommandResponse)
async def process_command(command: VoiceCommand):
    """
    Process voice command.

    Args:
        command: Voice command text and optional context

    Returns:
        CommandResponse with action taken
    """
    try:
        return processor.parse_command(command.text, command.context)
    except Exception as e:
        logger.error(f"Command processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: str = "en"
):
    """
    Transcribe audio file to text.

    Args:
        file: Audio file upload
        language: Language code (default: en)

    Returns:
        Transcription with confidence score
    """
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Import here to avoid loading models at startup
        from services.asr.whisper_service import get_whisper_service

        # Transcribe
        whisper = get_whisper_service()
        result = whisper.transcribe(tmp_path, language=language)

        # Cleanup
        os.unlink(tmp_path)

        # Calculate average confidence
        words = result.get("words", [])
        avg_confidence = sum(w["confidence"] for w in words) / len(words) if words else 0.5

        return TranscriptionResponse(
            text=result["text"],
            confidence=avg_confidence,
            segments=result.get("segments", [])
        )

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/commands/list")
async def list_commands():
    """List available voice commands."""
    return {
        "development": [
            "run tests",
            "build project",
            "start dev server"
        ],
        "performance": [
            "play song",
            "stop performance",
            "transpose [number]",
            "set tempo [bpm]"
        ],
        "library": [
            "load [song name]",
            "open [song name]"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)