"""Job manager for tracking Song Map generation tasks."""
import asyncio
import json
import logging
import sqlite3
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta

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
    """Manages Song Map generation jobs with SQLite persistence."""

    def __init__(self, output_dir: Path, upload_dir: Path, db_path: Optional[str] = None):
        """
        Initialize job manager.

        Args:
            output_dir: Directory for pipeline outputs
            upload_dir: Directory for uploaded audio files
            db_path: Path to SQLite database (default: output_dir/jobs.db)
        """
        self.output_dir = output_dir
        self.upload_dir = upload_dir
        self.db_path = db_path or str(output_dir / "jobs.db")
        self.lock = asyncio.Lock()

        # Ensure directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_db()

        logger.info(f"JobManager initialized: output={output_dir}, upload={upload_dir}, db={self.db_path}")

    def _init_db(self):
        """Initialize SQLite database with jobs table."""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                created_at REAL NOT NULL,
                started_at REAL,
                completed_at REAL,
                progress REAL DEFAULT 0.0,
                error_message TEXT,
                song_map_path TEXT,
                input_file TEXT
            )
        ''')
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")

    def _serialize_job(self, job: JobInfo) -> tuple:
        """Serialize JobInfo to database row."""
        return (
            job.job_id,
            job.status.value,
            job.created_at,
            job.started_at,
            job.completed_at,
            job.progress,
            job.error_message,
            job.song_map_path,
            job.input_file
        )

    def _deserialize_job(self, row: tuple) -> JobInfo:
        """Deserialize database row to JobInfo."""
        return JobInfo(
            job_id=row[0],
            status=JobStatus(row[1]),
            created_at=row[2],
            started_at=row[3],
            completed_at=row[4],
            progress=row[5],
            error_message=row[6],
            song_map_path=row[7],
            input_file=row[8]
        )

    async def create_job(self, job_id: str, input_file: str) -> JobInfo:
        """
        Create a new job and persist to database.

        Args:
            job_id: Unique job identifier
            input_file: Path to input audio file

        Returns:
            JobInfo object
        """
        async with self.lock:
            # Check if job already exists in DB
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT job_id FROM jobs WHERE job_id = ?", (job_id,))
            if cursor.fetchone():
                conn.close()
                raise ValueError(f"Job {job_id} already exists")

            # Create job object
            job = JobInfo(
                job_id=job_id,
                status=JobStatus.PENDING,
                input_file=input_file
            )

            # Persist to database
            conn.execute(
                """INSERT INTO jobs
                   (job_id, status, created_at, started_at, completed_at,
                    progress, error_message, song_map_path, input_file)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                self._serialize_job(job)
            )
            conn.commit()
            conn.close()

            logger.info(f"Created job {job_id} (persisted to DB)")
            return job

    async def get_job(self, job_id: str) -> Optional[JobInfo]:
        """
        Get job information from database.

        Args:
            job_id: Job identifier

        Returns:
            JobInfo or None if not found
        """
        async with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
            row = cursor.fetchone()
            conn.close()

            if not row:
                return None

            return self._deserialize_job(row)

    async def update_job_status(
        self,
        job_id: str,
        status: JobStatus,
        progress: Optional[float] = None,
        error_message: Optional[str] = None,
        song_map_path: Optional[str] = None
    ):
        """
        Update job status in database.

        Args:
            job_id: Job identifier
            status: New status
            progress: Progress percentage (0.0-1.0)
            error_message: Error message if status is ERROR
            song_map_path: Path to generated Song Map
        """
        async with self.lock:
            # Get current job from DB
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
            row = cursor.fetchone()

            if not row:
                conn.close()
                raise ValueError(f"Job {job_id} not found")

            job = self._deserialize_job(row)

            # Update job fields
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

            # Persist to database
            conn.execute(
                """UPDATE jobs SET
                   status = ?, started_at = ?, completed_at = ?,
                   progress = ?, error_message = ?, song_map_path = ?
                   WHERE job_id = ?""",
                (job.status.value, job.started_at, job.completed_at,
                 job.progress, job.error_message, job.song_map_path, job_id)
            )
            conn.commit()
            conn.close()

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
            # Optionally delete uploaded audio and intermediate files
            # This could be called after Song Map is downloaded
            logger.info(f"Cleanup job {job_id} (not implemented)")

    async def delete_job(self, job_id: str):
        """
        Delete job from database.

        Args:
            job_id: Job identifier
        """
        async with self.lock:
            conn = sqlite3.connect(self.db_path)
            conn.execute("DELETE FROM jobs WHERE job_id = ?", (job_id,))
            conn.commit()
            conn.close()
            logger.info(f"Deleted job {job_id} from database")

    async def list_all_jobs(self) -> list[JobInfo]:
        """
        List all jobs from database.

        Returns:
            List of all JobInfo objects
        """
        async with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC")
            rows = cursor.fetchall()
            conn.close()

            return [self._deserialize_job(row) for row in rows]

    async def cleanup_old_jobs(self, days: int = 7):
        """
        Delete jobs older than N days from database.

        Args:
            days: Number of days to keep jobs (default: 7)

        Returns:
            Number of jobs deleted
        """
        async with self.lock:
            cutoff_time = time.time() - (days * 24 * 60 * 60)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.execute("SELECT COUNT(*) FROM jobs WHERE created_at < ?", (cutoff_time,))
            count = cursor.fetchone()[0]

            conn.execute("DELETE FROM jobs WHERE created_at < ?", (cutoff_time,))
            conn.commit()
            conn.close()

            logger.info(f"Cleaned up {count} jobs older than {days} days")
            return count
