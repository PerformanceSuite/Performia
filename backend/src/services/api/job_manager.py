"""Job manager for tracking Song Map generation tasks."""
import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class JobStatus(str, Enum):
    """Job status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class JobInfo:
    """Information about a Song Map generation job."""
    job_id: str
    status: JobStatus
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    progress: float = 0.0
    error_message: Optional[str] = None
    song_map_path: Optional[str] = None
    input_file: Optional[str] = None

    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.started_at is None:
            return 0.0
        end_time = self.completed_at if self.completed_at else time.time()
        return end_time - self.started_at

    @property
    def estimated_remaining(self) -> Optional[float]:
        """Estimate remaining time based on progress."""
        if self.progress <= 0.0 or self.started_at is None:
            return None
        if self.status == JobStatus.COMPLETE:
            return 0.0

        elapsed = self.elapsed
        total_estimated = elapsed / self.progress
        return total_estimated - elapsed

    def to_dict(self) -> Dict:
        """Convert to dictionary for API response."""
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "progress": self.progress,
            "elapsed": self.elapsed,
            "estimated_remaining": self.estimated_remaining,
            "error_message": self.error_message,
            "created_at": datetime.fromtimestamp(self.created_at).isoformat(),
            "started_at": datetime.fromtimestamp(self.started_at).isoformat() if self.started_at else None,
            "completed_at": datetime.fromtimestamp(self.completed_at).isoformat() if self.completed_at else None
        }


class JobManager:
    """Manages Song Map generation jobs."""

    def __init__(self, output_dir: Path, upload_dir: Path):
        """
        Initialize job manager.

        Args:
            output_dir: Directory for pipeline outputs
            upload_dir: Directory for uploaded audio files
        """
        self.output_dir = output_dir
        self.upload_dir = upload_dir
        self.jobs: Dict[str, JobInfo] = {}
        self.lock = asyncio.Lock()

        # Ensure directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"JobManager initialized: output={output_dir}, upload={upload_dir}")

    async def create_job(self, job_id: str, input_file: str) -> JobInfo:
        """
        Create a new job.

        Args:
            job_id: Unique job identifier
            input_file: Path to input audio file

        Returns:
            JobInfo object
        """
        async with self.lock:
            if job_id in self.jobs:
                raise ValueError(f"Job {job_id} already exists")

            job = JobInfo(
                job_id=job_id,
                status=JobStatus.PENDING,
                input_file=input_file
            )
            self.jobs[job_id] = job
            logger.info(f"Created job {job_id}")
            return job

    async def get_job(self, job_id: str) -> Optional[JobInfo]:
        """
        Get job information.

        Args:
            job_id: Job identifier

        Returns:
            JobInfo or None if not found
        """
        async with self.lock:
            return self.jobs.get(job_id)

    async def update_job_status(
        self,
        job_id: str,
        status: JobStatus,
        progress: Optional[float] = None,
        error_message: Optional[str] = None,
        song_map_path: Optional[str] = None
    ):
        """
        Update job status.

        Args:
            job_id: Job identifier
            status: New status
            progress: Progress percentage (0.0-1.0)
            error_message: Error message if status is ERROR
            song_map_path: Path to generated Song Map
        """
        async with self.lock:
            job = self.jobs.get(job_id)
            if not job:
                raise ValueError(f"Job {job_id} not found")

            job.status = status

            if progress is not None:
                job.progress = progress

            if status == JobStatus.PROCESSING and job.started_at is None:
                job.started_at = time.time()

            if status == JobStatus.COMPLETE:
                job.completed_at = time.time()
                job.progress = 1.0
                if song_map_path:
                    job.song_map_path = song_map_path

            if status == JobStatus.ERROR:
                job.completed_at = time.time()
                job.error_message = error_message

            logger.info(f"Updated job {job_id}: status={status.value}, progress={progress}")

    async def load_song_map(self, job_id: str) -> Optional[Dict]:
        """
        Load Song Map JSON for a completed job.

        Args:
            job_id: Job identifier

        Returns:
            Song Map dict or None if not available
        """
        job = await self.get_job(job_id)

        if not job:
            return None

        if job.status != JobStatus.COMPLETE:
            return None

        # Try to load from saved path
        if job.song_map_path and Path(job.song_map_path).exists():
            with open(job.song_map_path, 'r') as f:
                return json.load(f)

        # Try default location (packager saves as {job_id}.song_map.json)
        default_path = self.output_dir / job_id / f"{job_id}.song_map.json"
        if default_path.exists():
            with open(default_path, 'r') as f:
                return json.load(f)

        return None

    async def cleanup_job(self, job_id: str):
        """
        Clean up job files (optional - for resource management).

        Args:
            job_id: Job identifier
        """
        async with self.lock:
            job = self.jobs.get(job_id)
            if not job:
                return

            # Optionally delete uploaded audio and intermediate files
            # This could be called after Song Map is downloaded
            logger.info(f"Cleanup job {job_id} (not implemented)")
