"""
End-to-End Tests for API Upload and Song Map Generation.

Tests the complete flow:
1. Upload audio file via /api/analyze
2. Poll job status until completion
3. Retrieve and validate Song Map
4. Verify all pipeline outputs (beats, chords, lyrics, etc.)
"""
import asyncio
import json
import shutil
from pathlib import Path
from typing import Dict

import pytest
from httpx import AsyncClient, ASGITransport

# Import FastAPI app
from services.api.main import app, UPLOAD_DIR, OUTPUT_DIR


@pytest.fixture
def test_audio_file() -> Path:
    """Provide path to test audio file."""
    # Use existing test file
    audio_file = Path(__file__).parent.parent.parent / "uploads" / "32193cf0.wav"
    assert audio_file.exists(), f"Test audio file not found: {audio_file}"
    return audio_file


@pytest.fixture
def cleanup_test_outputs():
    """Cleanup test outputs after tests."""
    test_job_ids = []

    def register_job(job_id: str):
        """Register a job ID for cleanup after test."""
        test_job_ids.append(job_id)
        return job_id

    yield register_job

    # Cleanup after test completes
    for job_id in test_job_ids:
        # Remove job output directory
        job_dir = OUTPUT_DIR / job_id
        if job_dir.exists():
            shutil.rmtree(job_dir, ignore_errors=True)

        # Remove uploaded audio files
        for ext in ['.wav', '.mp3', '.m4a', '.flac']:
            upload_file = UPLOAD_DIR / f"{job_id}{ext}"
            if upload_file.exists():
                upload_file.unlink()


@pytest.mark.asyncio
async def test_upload_audio_creates_job(test_audio_file: Path, cleanup_test_outputs):
    """Test that uploading audio creates a job and returns job_id."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # Upload audio file
        with open(test_audio_file, "rb") as f:
            response = await client.post(
                "/api/analyze",
                files={"file": (test_audio_file.name, f, "audio/wav")}
            )

        # Verify response
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert "status" in data
        assert data["status"] == "pending"
        assert "message" in data

        # Verify job_id format (8 character UUID)
        job_id = data["job_id"]
        cleanup_test_outputs(job_id)  # Register for cleanup
        assert len(job_id) == 8
        assert job_id.replace("-", "").isalnum()


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.skip(reason="Requires full pipeline services to be running - use for manual integration testing")
async def test_full_pipeline_generates_song_map(test_audio_file: Path, cleanup_test_outputs):
    """
    Test complete pipeline: upload → processing → Song Map generation.

    This is a comprehensive E2E test that validates:
    - File upload
    - Job creation and status tracking
    - Pipeline processing
    - Song Map generation with all required fields

    NOTE: This test requires all pipeline services (ASR, beats, chords, etc.) to be functional.
    Use this for full integration testing when the backend is fully operational.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        timeout=120.0  # Allow up to 2 minutes for processing
    ) as client:
        # 1. Upload audio file
        with open(test_audio_file, "rb") as f:
            upload_response = await client.post(
                "/api/analyze",
                files={"file": (test_audio_file.name, f, "audio/wav")}
            )

        assert upload_response.status_code == 200
        job_id = upload_response.json()["job_id"]

        # 2. Poll job status until complete or error
        max_polls = 60  # 60 polls * 2 seconds = 2 minutes max
        poll_count = 0
        final_status = None

        while poll_count < max_polls:
            status_response = await client.get(f"/api/status/{job_id}")
            assert status_response.status_code == 200

            status_data = status_response.json()
            final_status = status_data["status"]

            if final_status in ["complete", "error"]:
                break

            # Wait before next poll
            await asyncio.sleep(2)
            poll_count += 1

        # 3. Verify job completed successfully
        assert final_status == "complete", f"Job did not complete. Status: {final_status}"

        # 4. Retrieve Song Map
        songmap_response = await client.get(f"/api/songmap/{job_id}")
        assert songmap_response.status_code == 200

        song_map = songmap_response.json()

        # 5. Validate Song Map structure
        assert_valid_song_map(song_map)


@pytest.mark.asyncio
async def test_job_status_endpoint(test_audio_file: Path, cleanup_test_outputs):
    """Test that job status endpoint returns correct information."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # Upload file
        with open(test_audio_file, "rb") as f:
            upload_response = await client.post(
                "/api/analyze",
                files={"file": (test_audio_file.name, f, "audio/wav")}
            )

        job_id = upload_response.json()["job_id"]
        cleanup_test_outputs(job_id)  # Register for cleanup

        # Check status
        status_response = await client.get(f"/api/status/{job_id}")
        assert status_response.status_code == 200

        status_data = status_response.json()
        assert "job_id" in status_data
        assert "status" in status_data
        assert status_data["job_id"] == job_id
        assert status_data["status"] in ["pending", "processing", "complete", "error"]


@pytest.mark.asyncio
async def test_invalid_job_id_returns_404():
    """Test that requesting invalid job_id returns 404."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/status/invalid-job-id")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_upload_without_file_returns_400():
    """Test that uploading without file returns 400 error."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.post("/api/analyze")
        assert response.status_code == 422  # FastAPI validation error


@pytest.mark.asyncio
async def test_songmap_retrieval_for_nonexistent_job():
    """Test that retrieving Song Map for non-existent job returns 404."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/songmap/nonexist")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_audio_retrieval_for_nonexistent_job():
    """Test that retrieving audio for non-existent job returns 404."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        response = await client.get("/api/audio/nonexist/original")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_invalid_stem_type_returns_error():
    """Test that requesting invalid stem type returns 400 error."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        # Try to get invalid stem type
        response = await client.get("/api/audio/somejob/invalid-stem")
        # Should return 400 or 404 depending on implementation
        assert response.status_code in [400, 404]


@pytest.mark.asyncio
@pytest.mark.slow
@pytest.mark.skip(reason="Requires full pipeline to complete - use for manual integration testing")
async def test_retrieve_audio_file(test_audio_file: Path, cleanup_test_outputs):
    """Test that uploaded audio can be retrieved.

    NOTE: This test requires the pipeline to complete successfully.
    Use for integration testing when backend services are operational.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        timeout=120.0
    ) as client:
        # Upload file
        with open(test_audio_file, "rb") as f:
            upload_response = await client.post(
                "/api/analyze",
                files={"file": (test_audio_file.name, f, "audio/wav")}
            )

        job_id = upload_response.json()["job_id"]

        # Poll until complete
        max_polls = 60
        for _ in range(max_polls):
            status_response = await client.get(f"/api/status/{job_id}")
            if status_response.json()["status"] == "complete":
                break
            await asyncio.sleep(2)

        # Retrieve audio file
        audio_response = await client.get(f"/api/audio/{job_id}/original")
        assert audio_response.status_code == 200
        assert audio_response.headers["content-type"] in ["audio/wav", "audio/x-wav", "audio/wave"]


# Helper functions

def assert_valid_song_map(song_map: Dict):
    """
    Validate Song Map structure and required fields.

    Checks that Song Map contains all required fields from the schema:
    - metadata (title, artist, etc.)
    - beats
    - chords
    - sections
    - lyrics
    - performance (melody, bass)
    """
    # Metadata
    assert "metadata" in song_map or "title" in song_map, "Song Map missing metadata"

    # Audio analysis data
    assert "beats" in song_map, "Song Map missing beats"
    assert isinstance(song_map["beats"], list), "Beats should be a list"
    assert len(song_map["beats"]) > 0, "Beats should not be empty"

    assert "chords" in song_map, "Song Map missing chords"
    assert isinstance(song_map["chords"], list), "Chords should be a list"

    assert "sections" in song_map, "Song Map missing sections"
    assert isinstance(song_map["sections"], list), "Sections should be a list"

    assert "lyrics" in song_map, "Song Map missing lyrics"
    assert isinstance(song_map["lyrics"], list), "Lyrics should be a list"

    # Performance data
    assert "performance" in song_map, "Song Map missing performance data"
    assert "melody" in song_map["performance"], "Song Map missing melody data"
    assert "bass" in song_map["performance"], "Song Map missing bass data"

    # Validate beat structure
    if song_map["beats"]:
        beat = song_map["beats"][0]
        assert "time" in beat, "Beat missing time field"
        assert isinstance(beat["time"], (int, float)), "Beat time should be numeric"

    # Validate chord structure
    if song_map["chords"]:
        chord = song_map["chords"][0]
        assert "time" in chord, "Chord missing time field"
        assert "label" in chord or "chord" in chord, "Chord missing label field"

    # Validate section structure
    if song_map["sections"]:
        section = song_map["sections"][0]
        assert "start" in section, "Section missing start field"
        assert "label" in section or "name" in section, "Section missing label field"

    # Validate lyrics structure
    if song_map["lyrics"]:
        lyric = song_map["lyrics"][0]
        assert "start" in lyric or "time" in lyric, "Lyric missing start time"
        assert "text" in lyric or "word" in lyric, "Lyric missing text"
