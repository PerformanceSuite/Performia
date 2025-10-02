"""FastAPI REST API for Song Map generation.

This service provides REST endpoints for uploading audio files and
generating Song Maps using the async pipeline orchestrator.
"""
import asyncio
import logging
import uuid
from pathlib import Path
from typing import Dict, Optional
import os
import sys
import json

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles

# Add src to path for imports
backend_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(backend_root / 'src'))

from services.api.job_manager import JobManager, JobStatus
from services.orchestrator.async_pipeline import AsyncPipeline
# from services.api import performance  # Temporarily disabled - import issue

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Performia Song Map API",
    description="REST API for generating Song Maps from audio files",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include performance router
# app.include_router(performance.router)  # Temporarily disabled

# Configure directories
BASE_DIR = Path(__file__).parent.parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"

# Initialize job manager
job_manager = JobManager(output_dir=OUTPUT_DIR, upload_dir=UPLOAD_DIR)

logger.info(f"API initialized: upload_dir={UPLOAD_DIR}, output_dir={OUTPUT_DIR}")


async def run_pipeline(job_id: str, audio_path: str):
    """
    Run the audio analysis pipeline for a job.

    This runs in a background task and updates job status.

    Args:
        job_id: Job identifier
        audio_path: Path to uploaded audio file
    """
    try:
        # Update to processing
        await job_manager.update_job_status(job_id, JobStatus.PROCESSING, progress=0.0)
        logger.info(f"Starting pipeline for job {job_id}")

        # Create pipeline instance
        pipeline = AsyncPipeline(str(OUTPUT_DIR / job_id))

        # Run full pipeline
        # Note: Progress tracking could be enhanced by monitoring service completion
        results = await pipeline.run_full_pipeline(job_id, audio_path)

        # Extract Song Map path from packager results
        # Packager saves as {job_id}.song_map.json
        packager_output = results.get("results", {}).get("packager", {})
        song_map_path = OUTPUT_DIR / job_id / f"{job_id}.song_map.json"

        if not song_map_path.exists():
            raise RuntimeError(f"Song Map not generated at {song_map_path}")

        # Update to complete
        await job_manager.update_job_status(
            job_id,
            JobStatus.COMPLETE,
            progress=1.0,
            song_map_path=str(song_map_path)
        )

        logger.info(f"Pipeline completed for job {job_id} in {results['total_elapsed']:.1f}s")

    except Exception as e:
        logger.error(f"Pipeline failed for job {job_id}: {e}", exc_info=True)
        await job_manager.update_job_status(
            job_id,
            JobStatus.ERROR,
            error_message=str(e)
        )


@app.get("/")
async def root():
    """Root endpoint - API info."""
    return {
        "name": "Performia Song Map API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "analyze": "POST /api/analyze",
            "status": "GET /api/status/{job_id}",
            "songmap": "GET /api/songmap/{job_id}"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    jobs = await job_manager.list_all_jobs()
    return {
        "status": "healthy",
        "jobs_count": len(jobs),
        "database": job_manager.db_path
    }


@app.post("/api/analyze")
async def analyze_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
) -> Dict:
    """
    Upload audio file for Song Map generation.

    Args:
        file: Audio file (WAV, MP3, etc.)

    Returns:
        Job information with job_id and status
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        # Generate unique job ID
        job_id = str(uuid.uuid4())[:8]

        # Save uploaded file
        file_ext = Path(file.filename).suffix
        upload_path = UPLOAD_DIR / f"{job_id}{file_ext}"

        logger.info(f"Uploading file for job {job_id}: {file.filename}")

        # Save file asynchronously
        async with aiofiles.open(upload_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        logger.info(f"Saved upload to {upload_path}")

        # Create job
        job = await job_manager.create_job(job_id, str(upload_path))

        # Start pipeline in background
        background_tasks.add_task(run_pipeline, job_id, str(upload_path))

        return {
            "job_id": job_id,
            "status": job.status.value,
            "message": f"Analysis started for {file.filename}"
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Upload failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str) -> Dict:
    """
    Get analysis job status.

    Args:
        job_id: Job identifier

    Returns:
        Job status information including progress and timing
    """
    job = await job_manager.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    return job.to_dict()


@app.get("/api/songmap/{job_id}")
async def get_song_map(job_id: str) -> Dict:
    """
    Get Song Map JSON for a completed job.

    Args:
        job_id: Job identifier

    Returns:
        Complete Song Map JSON
    """
    job = await job_manager.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    if job.status == JobStatus.PENDING or job.status == JobStatus.PROCESSING:
        raise HTTPException(
            status_code=202,
            detail=f"Job {job_id} is still processing (progress: {job.progress:.1%})"
        )

    if job.status == JobStatus.ERROR:
        raise HTTPException(
            status_code=500,
            detail=f"Job {job_id} failed: {job.error_message}"
        )

    # Load Song Map
    song_map = await job_manager.load_song_map(job_id)

    if not song_map:
        raise HTTPException(
            status_code=500,
            detail=f"Song Map not found for job {job_id}"
        )

    return {
        "job_id": job_id,
        "song_map": song_map,
        "elapsed": job.elapsed
    }


@app.get("/api/jobs")
async def list_jobs() -> Dict:
    """
    List all jobs from database.

    Returns:
        List of all jobs with their status
    """
    jobs = await job_manager.list_all_jobs()
    jobs_dict = [job.to_dict() for job in jobs]

    return {
        "count": len(jobs_dict),
        "jobs": jobs_dict
    }


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str) -> Dict:
    """
    Delete a job and clean up its files.

    Args:
        job_id: Job identifier

    Returns:
        Deletion confirmation
    """
    job = await job_manager.get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    await job_manager.cleanup_job(job_id)
    await job_manager.delete_job(job_id)

    return {
        "message": f"Job {job_id} deleted",
        "job_id": job_id
    }


@app.delete("/api/jobs/cleanup")
async def cleanup_old_jobs(days: int = 7) -> Dict:
    """
    Delete jobs older than N days from database.

    Args:
        days: Number of days to keep jobs (default: 7)

    Returns:
        Cleanup summary
    """
    count = await job_manager.cleanup_old_jobs(days)

    return {
        "message": f"Cleaned up {count} jobs older than {days} days",
        "deleted_count": count,
        "retention_days": days
    }


@app.get("/api/audio/{job_id}/original")
async def get_original_audio(job_id: str):
    """
    Serve original uploaded audio file.

    Args:
        job_id: Job identifier

    Returns:
        Audio file response with proper media type and range support
    """
    # Try common audio extensions
    audio_path = None
    for ext in ['.mp3', '.wav', '.m4a', '.flac', '.ogg']:
        candidate_path = UPLOAD_DIR / f"{job_id}{ext}"
        if candidate_path.exists():
            audio_path = candidate_path
            break

    if not audio_path or not audio_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")

    # Determine media type based on extension
    media_types = {
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.m4a': 'audio/mp4',
        '.flac': 'audio/flac',
        '.ogg': 'audio/ogg'
    }
    media_type = media_types.get(audio_path.suffix, 'audio/mpeg')

    logger.info(f"Serving audio file: {audio_path}")

    return FileResponse(
        str(audio_path),
        media_type=media_type,
        headers={"Accept-Ranges": "bytes"}
    )


@app.get("/api/audio/{job_id}/stem/{stem_name}")
async def get_stem_audio(job_id: str, stem_name: str):
    """
    Serve separated stem audio (vocals, bass, drums, other).

    Args:
        job_id: Job identifier
        stem_name: Name of the stem (vocals, bass, drums, other)

    Returns:
        Stem audio file response
    """
    # Validate stem name
    valid_stems = ['vocals', 'bass', 'drums', 'other']
    if stem_name not in valid_stems:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid stem name. Must be one of: {', '.join(valid_stems)}"
        )

    # Look for stem file in output directory
    # Stems are typically saved as {job_id}.{stem_name}.wav
    stem_path = OUTPUT_DIR / job_id / f"{job_id}.{stem_name}.wav"

    if not stem_path.exists():
        # Try alternative naming convention
        alt_stem_path = OUTPUT_DIR / job_id / f"{stem_name}.wav"
        if alt_stem_path.exists():
            stem_path = alt_stem_path
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Stem '{stem_name}' not found for job {job_id}"
            )

    logger.info(f"Serving stem file: {stem_path}")

    return FileResponse(
        str(stem_path),
        media_type="audio/wav",
        headers={"Accept-Ranges": "bytes"}
    )


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn

    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
