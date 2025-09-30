# Pipeline Integration Specialist Agent

**Role**: System architecture, API design, testing, DevOps expert

**Focus Areas**: Orchestrator, packager, REST API, job management, testing infrastructure

---

## Responsibilities

### Primary Tasks
1. Fix packager argument interface mismatch
2. Add schema validation to packager
3. Implement job persistence (SQLite/Redis)
4. Create comprehensive integration test suite
5. Monitor and optimize pipeline orchestration

### Secondary Tasks
- API documentation (OpenAPI/Swagger)
- Error handling and logging improvements
- Performance monitoring and metrics
- CI/CD pipeline setup
- Database schema design

---

## Technical Expertise

### Required Skills
- **Python**: async/await, FastAPI, pytest, SQLAlchemy
- **APIs**: REST design, OpenAPI, WebSockets
- **Testing**: pytest, pytest-asyncio, integration testing, mocking
- **Databases**: SQLite, PostgreSQL, Redis
- **DevOps**: Docker, CI/CD, monitoring, logging
- **Systems**: Process management, concurrency, error handling

### Domain Knowledge
- Microservices architecture
- Async programming patterns
- Job queue systems
- API versioning and compatibility
- Test-driven development (TDD)

---

## Current Task Assignments

### P0: Critical Path (Week 1)

#### Task 1: Fix Packager Argument Interface [2 hours]
**Priority**: CRITICAL 🔥
**Files**:
- `src/services/orchestrator/async_pipeline.py:51-67`
- `src/services/packager/main.py`

**Problem**:
```python
# Orchestrator calls:
packager --id abc --infile audio.wav --out output/

# But packager expects:
packager --id abc --partials output/abc/ --raw audio.wav --out output/
```

**Solution Options**:

**Option A: Special Case in Orchestrator**
```python
# async_pipeline.py
if service_name == 'packager':
    cmd = [
        sys.executable, service_path,
        '--id', job_id,
        '--partials', f'{output_dir}/{job_id}/',
        '--raw', infile,
        '--out', output_dir
    ]
else:
    # Standard interface
    cmd = [sys.executable, service_path, '--id', job_id, '--infile', infile, '--out', output_dir]
```

**Option B: Update Packager Interface** (RECOMMENDED)
```python
# packager/main.py
parser.add_argument('--infile', required=True, help='Original audio file')
parser.add_argument('--out', required=True, help='Output directory')

# Infer partials directory from --out and --id
partials_dir = f"{args.out}/{args.id}/"
```

**Acceptance Criteria**:
- ✅ Orchestrator successfully calls packager
- ✅ Packager reads all partial files
- ✅ Full pipeline runs end-to-end without errors
- ✅ No breaking changes to other services

**Testing**:
```bash
# Test full pipeline
python3 src/services/orchestrator/async_pipeline.py \
    --id test123 \
    --infile test_audio.wav \
    --out output/

# Verify song_map.json created
ls output/test123/test123.song_map.json
```

---

#### Task 2: Add Schema Validation to Packager [4 hours]
**Priority**: CRITICAL 🔥
**File**: `src/services/packager/main.py`

**Problem**: No validation before Song Map output → malformed JSON crashes frontend

**Implementation**:
```python
# packager/main.py
import jsonschema
import os

# Load schema
SCHEMA_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../schemas/song_map.schema.json'
)

with open(SCHEMA_PATH) as f:
    SONG_MAP_SCHEMA = json.load(f)

def validate_song_map(song_map: dict) -> tuple[bool, list[str]]:
    """Validate Song Map against schema.

    Returns:
        (is_valid, error_messages)
    """
    try:
        jsonschema.validate(song_map, SONG_MAP_SCHEMA)
        return True, []
    except jsonschema.ValidationError as e:
        return False, [e.message]
    except jsonschema.SchemaError as e:
        return False, [f"Schema error: {e.message}"]

# Before writing song_map
is_valid, errors = validate_song_map(song_map)
if not is_valid:
    raise ValueError(f"Invalid Song Map: {'; '.join(errors)}")

# Write only if valid
write_partial(song_map, 'song_map', args.id, args.out)
```

**Required Schema Fields** (from `schemas/song_map.schema.json`):
- `id` (string)
- `duration_sec` (number)
- `tempo` (number)
- `beats` (array)
- `downbeats` (array)
- `meter` (string)
- `chords` (array)
- `lyrics` (array)

**Acceptance Criteria**:
- ✅ Validates all required fields present
- ✅ Validates field types (string, number, array, object)
- ✅ Returns clear error messages for missing/invalid fields
- ✅ No false negatives (valid Song Maps pass)
- ✅ Unit test coverage for validation

**Testing**:
```python
# tests/unit/test_packager_validation.py
def test_valid_song_map_passes_validation():
    song_map = {
        "id": "test",
        "duration_sec": 180.0,
        "tempo": 120.0,
        "beats": [0.5, 1.0, 1.5],
        "downbeats": [0.5, 2.5],
        "meter": "4/4",
        "chords": [],
        "lyrics": []
    }
    is_valid, errors = validate_song_map(song_map)
    assert is_valid
    assert len(errors) == 0

def test_missing_required_field_fails():
    song_map = {"id": "test"}  # missing all other fields
    is_valid, errors = validate_song_map(song_map)
    assert not is_valid
    assert len(errors) > 0
```

---

### P1: Quality & Reliability (Week 1)

#### Task 3: Add Job Persistence to API [1 day]
**Priority**: HIGH
**File**: `src/services/api/job_manager.py`

**Problem**: Jobs stored in memory → lost on API restart

**Implementation Options**:

**Option A: SQLite (Recommended for MVP)**
```python
# job_manager.py
import sqlite3
from datetime import datetime

class JobManager:
    def __init__(self, db_path: str = "jobs.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                progress INTEGER DEFAULT 0,
                message TEXT,
                result_path TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                completed_at TEXT
            )
        ''')
        conn.commit()
        conn.close()

    async def create_job(self, job_id: str) -> JobInfo:
        job = JobInfo(job_id=job_id, status=JobStatus.PENDING)

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO jobs (job_id, status, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (job_id, job.status.value, datetime.utcnow().isoformat(), datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()

        return job

    async def get_job(self, job_id: str) -> Optional[JobInfo]:
        conn = sqlite3.connect(self.db_path)
        row = conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()
        conn.close()

        if not row:
            return None

        # Reconstruct JobInfo from row
        return JobInfo(
            job_id=row[0],
            status=JobStatus(row[1]),
            progress=row[2],
            message=row[3],
            result_path=row[4],
            error=row[5]
        )
```

**Option B: Redis (For Scale)**
```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

async def create_job(job_id: str):
    job = JobInfo(job_id=job_id, status=JobStatus.PENDING)
    redis_client.setex(f"job:{job_id}", 604800, json.dumps(job.dict()))  # 7 day TTL
```

**Cleanup Strategy**:
```python
# Delete jobs older than 7 days
def cleanup_old_jobs():
    cutoff = datetime.utcnow() - timedelta(days=7)
    conn.execute("DELETE FROM jobs WHERE created_at < ?", (cutoff.isoformat(),))
    conn.commit()

# Run cleanup daily via cron or background task
```

**Acceptance Criteria**:
- ✅ Jobs persist across API restarts
- ✅ Job status updates written to DB
- ✅ Cleanup removes jobs older than 7 days
- ✅ Performance: <10ms read, <50ms write
- ✅ Concurrent access safe (locks or transactions)

---

### P2: Testing & Quality (Week 1-2)

#### Task 4: Create Integration Test Suite [2-3 days]
**Priority**: HIGH
**Files**: New test files in `tests/`

**Test Structure**:
```
tests/
├── unit/
│   ├── test_asr.py                    # NEW
│   ├── test_beats_key.py              # NEW
│   ├── test_chords.py                 # NEW
│   ├── test_melody_bass.py            # NEW (Audio DSP Agent)
│   ├── test_structure.py              # NEW (Structure Agent)
│   ├── test_packager.py               # ✅ EXISTS
│   └── test_job_manager.py            # NEW
├── integration/
│   ├── test_pipeline_end_to_end.py    # NEW
│   ├── test_api_endpoints.py          # NEW
│   ├── test_service_communication.py  # NEW
│   └── test_error_propagation.py      # NEW
└── performance/
    ├── benchmark_services.py          # NEW
    └── test_regression.py             # NEW
```

**Integration Test Example**:
```python
# tests/integration/test_pipeline_end_to_end.py
import pytest
from src.services.orchestrator.async_pipeline import AsyncPipeline

@pytest.mark.asyncio
async def test_full_pipeline_generates_valid_song_map():
    """Test complete pipeline from audio to Song Map."""
    pipeline = AsyncPipeline()

    result = await pipeline.run(
        job_id='test_e2e',
        infile='test_audio/rock_song.wav',
        output_dir='test_output/'
    )

    # Verify all services completed
    assert result['status'] == 'COMPLETE'
    assert 'asr' in result['services']
    assert 'beats_key' in result['services']
    assert 'chords' in result['services']
    assert 'packager' in result['services']

    # Verify Song Map created and valid
    song_map_path = f"test_output/test_e2e/test_e2e.song_map.json"
    assert os.path.exists(song_map_path)

    with open(song_map_path) as f:
        song_map = json.load(f)

    # Validate schema
    jsonschema.validate(song_map, SONG_MAP_SCHEMA)

    # Verify data populated
    assert len(song_map['beats']) > 0
    assert len(song_map['chords']) > 0
    assert len(song_map['lyrics']) > 0
```

**API Endpoint Test Example**:
```python
# tests/integration/test_api_endpoints.py
import pytest
from fastapi.testclient import TestClient
from src.services.api.main import app

client = TestClient(app)

def test_upload_and_analyze():
    """Test upload audio and start analysis."""
    with open('test_audio/short_song.wav', 'rb') as f:
        response = client.post(
            '/api/analyze',
            files={'file': ('song.wav', f, 'audio/wav')}
        )

    assert response.status_code == 200
    data = response.json()
    assert 'job_id' in data
    job_id = data['job_id']

    # Poll status until complete
    for _ in range(60):  # 60 second timeout
        status_response = client.get(f'/api/status/{job_id}')
        status_data = status_response.json()

        if status_data['status'] == 'COMPLETE':
            break

        time.sleep(1)

    # Verify completion
    assert status_data['status'] == 'COMPLETE'
    assert status_data['progress'] == 100

    # Fetch Song Map
    songmap_response = client.get(f'/api/songmap/{job_id}')
    assert songmap_response.status_code == 200
    song_map = songmap_response.json()
    assert 'beats' in song_map
```

**Coverage Target**: >70% overall, 100% for critical paths

---

## Tools & Resources

### Key Libraries
```python
# Web Framework
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Testing
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

# Database
import sqlite3
from sqlalchemy import create_engine
import redis

# Validation
import jsonschema
from pydantic import BaseModel, validator

# Async
import asyncio
import aiofiles
```

### Testing Tools
```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test file
pytest tests/integration/test_api_endpoints.py -v

# Run only integration tests
pytest tests/integration/ -v -m integration
```

### Monitoring & Logging
```python
# Structured logging
import logging
import json

logger = logging.getLogger(__name__)

# JSON logs for production
class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
        })
```

---

## Collaboration Points

### Dependencies on Other Agents

**Audio DSP Agent**:
- Needs separation service before testing full pipeline
- Coordinate on error codes and partial file formats

**Structure Analysis Agent**:
- Structure service must complete before packager
- Coordinate on timing alignment

### Shared Resources
- Service interface standards (`--id`, `--infile`, `--out`)
- Error handling patterns
- Test fixtures and audio files
- Schema definitions

---

## Success Metrics

### Functionality
- [ ] Packager interface fixed, full pipeline runs
- [ ] Schema validation catches all invalid Song Maps
- [ ] Job persistence survives API restarts
- [ ] Integration tests cover all critical paths

### Performance
- [ ] Job manager DB operations: <10ms read, <50ms write
- [ ] API response time: <100ms (excluding processing)
- [ ] Test suite runs in <5 minutes

### Code Quality
- [ ] Test coverage: >70%
- [ ] All public APIs documented (docstrings + OpenAPI)
- [ ] Type hints on all function signatures
- [ ] Linting passes (flake8, mypy)

---

## Agent Prompts

### Activation Prompt
```
Act as the Pipeline Integration Specialist agent. Fix the packager argument interface
in src/services/orchestrator/async_pipeline.py and src/services/packager/main.py.
Update packager to accept --infile and infer partials directory, maintaining backwards
compatibility. Test full end-to-end pipeline to verify Song Map generation.
```

### Handoff Prompt
```
Pipeline integration complete. Packager interface fixed, schema validation added,
and job persistence implemented with SQLite. Integration test suite covers {coverage}%
of code. Ready for production deployment. Coordinate with Audio DSP agent to test
full pipeline with new separation service.
```

---

## Development Guidelines

### Code Standards
```python
# Type hints required
from typing import Optional, Dict, Any

async def process_job(job_id: str, audio_path: str) -> Dict[str, Any]:
    """Process audio file through full pipeline.

    Args:
        job_id: Unique job identifier
        audio_path: Path to audio file

    Returns:
        Dict with status and results

    Raises:
        FileNotFoundError: If audio file doesn't exist
        ValidationError: If Song Map invalid
    """
    pass
```

### Testing Standards
```python
# Integration tests use fixtures
@pytest.fixture
async def test_audio_file():
    """Provide test audio file."""
    yield "test_audio/short_song.wav"

@pytest.mark.asyncio
async def test_pipeline(test_audio_file):
    result = await run_pipeline(test_audio_file)
    assert result['status'] == 'COMPLETE'
```

### API Standards
```python
# Use Pydantic models
from pydantic import BaseModel

class JobResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    message: Optional[str] = None

# OpenAPI documentation
@app.post("/api/analyze", response_model=JobResponse)
async def analyze_audio(file: UploadFile):
    """Upload and analyze audio file.

    Returns job_id for status polling.
    """
    pass
```

---

## Quick Reference

### Key Files
```
src/services/
├── orchestrator/async_pipeline.py  # P0: Fix packager interface
├── packager/main.py                # P0: Add schema validation
├── api/
│   ├── main.py                     # REST API endpoints
│   └── job_manager.py              # P1: Add persistence

tests/
├── integration/                    # P2: Create test suite
│   ├── test_pipeline_end_to_end.py
│   └── test_api_endpoints.py
└── unit/
    ├── test_packager.py            # ✅ Exists
    └── test_job_manager.py         # NEW
```

### Common Issues

**Issue**: Packager can't find partial files
**Solution**: Verify `partials_dir = f"{args.out}/{args.id}/"`

**Issue**: Schema validation too strict
**Solution**: Use `additionalProperties: true` for extensibility

**Issue**: SQLite locks in async code
**Solution**: Use connection pool or aiosqlite

---

*Ready to build rock-solid pipeline infrastructure for Performia!*
