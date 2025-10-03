# Performia Song Map API

FastAPI REST service for generating Song Maps from audio files using the async pipeline orchestrator.

## Features

- **Async File Upload**: Non-blocking audio file upload
- **Background Processing**: Pipeline runs in background tasks
- **Job Tracking**: Real-time status and progress monitoring
- **Song Map Delivery**: JSON API for retrieving completed Song Maps

## API Endpoints

### 1. Upload Audio File

```bash
POST /api/analyze
```

Upload an audio file and start Song Map generation.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (audio file - WAV, MP3, etc.)

**Response:**
```json
{
  "job_id": "abc123",
  "status": "pending",
  "message": "Analysis started for test_music.wav"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F 'file=@/path/to/audio.wav' \
  -H 'accept: application/json'
```

### 2. Check Job Status

```bash
GET /api/status/{job_id}
```

Get real-time status of a Song Map generation job.

**Response:**
```json
{
  "job_id": "abc123",
  "status": "processing",
  "progress": 0.65,
  "elapsed": 12.5,
  "estimated_remaining": 7.2,
  "error_message": null,
  "created_at": "2025-09-30T14:16:33.196327",
  "started_at": "2025-09-30T14:16:33.196510",
  "completed_at": null
}
```

**Status Values:**
- `pending`: Job created, waiting to start
- `processing`: Pipeline running
- `complete`: Song Map generated successfully
- `error`: Pipeline failed

**Example:**
```bash
curl http://localhost:8000/api/status/abc123
```

### 3. Download Song Map

```bash
GET /api/songmap/{job_id}
```

Retrieve the complete Song Map JSON for a finished job.

**Response:**
```json
{
  "job_id": "abc123",
  "song_map": {
    "id": "abc123",
    "duration_sec": 8.0,
    "tempo": {
      "bpm_global": 117.45,
      "curve": [[0.0, 117.45], [8.0, 117.45]],
      "confidence": 0.8
    },
    "meter": {"numerator": 4, "denominator": 4},
    "beats": [0.534, 1.045, 1.533, ...],
    "downbeats": [0.534, 2.531, 4.528, ...],
    "key": [...],
    "chords": [...],
    "sections": [...],
    "lyrics": [...]
  },
  "elapsed": 4.42
}
```

**Example:**
```bash
curl http://localhost:8000/api/songmap/abc123
```

### 4. List All Jobs

```bash
GET /api/jobs
```

Get list of all jobs (useful for debugging).

**Response:**
```json
{
  "count": 2,
  "jobs": [
    {
      "job_id": "abc123",
      "status": "complete",
      "progress": 1.0,
      ...
    },
    {
      "job_id": "xyz789",
      "status": "processing",
      "progress": 0.5,
      ...
    }
  ]
}
```

### 5. Delete Job

```bash
DELETE /api/jobs/{job_id}
```

Delete a job and clean up its files.

**Response:**
```json
{
  "message": "Job abc123 deleted",
  "job_id": "abc123"
}
```

### 6. Health Check

```bash
GET /health
```

Check API server health.

**Response:**
```json
{
  "status": "healthy",
  "jobs_count": 3
}
```

## Running the Server

### Development

```bash
# Activate virtual environment
source venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/Users/danielconnolly/Projects/Performia/backend/src

# Run server
python src/services/api/main.py
```

Server runs on `http://0.0.0.0:8000`

### Production

```bash
# Using uvicorn directly
uvicorn services.api.main:app --host 0.0.0.0 --port 8000

# With workers
uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing

Run the comprehensive test suite:

```bash
python test_api.py
```

The test suite:
1. Uploads `test_music.wav`
2. Polls job status until complete
3. Downloads and validates Song Map
4. Saves output to `songmap_{job_id}.json`

## Architecture

### Components

1. **main.py**: FastAPI application with REST endpoints
2. **job_manager.py**: Job tracking and status management
3. **async_pipeline.py**: Audio analysis orchestrator (in ../orchestrator/)

### Data Flow

```
Audio Upload → Job Created (pending)
    ↓
Background Task → Pipeline Started (processing)
    ↓
Services Run → Progress Updates
    ↓
Packager → Song Map Generated (complete)
    ↓
API Response → Song Map JSON
```

### File Structure

```
backend/
├── uploads/          # Uploaded audio files
│   └── {job_id}.wav
├── output/           # Pipeline outputs
│   └── {job_id}/
│       ├── {job_id}.asr.json
│       ├── {job_id}.beats_key.json
│       ├── {job_id}.chords.json
│       ├── {job_id}.melody_bass.json
│       ├── {job_id}.structure.json
│       └── {job_id}.song_map.json  ← Final output
└── src/services/api/
    ├── main.py
    └── job_manager.py
```

## WebSocket Integration (Next Phase)

### Planned Enhancement

For real-time progress updates, the next phase will add WebSocket support:

#### WebSocket Endpoint

```bash
WS /ws/analyze/{job_id}
```

#### Real-Time Updates

The WebSocket connection will stream updates during pipeline execution:

```json
{
  "type": "progress",
  "job_id": "abc123",
  "service": "separation",
  "status": "running",
  "progress": 0.15,
  "message": "Separating audio stems..."
}
```

#### Implementation Notes

1. **Per-Service Progress**: Track progress for each service in the pipeline
   - separation: 0.0 → 0.14
   - beats_key: 0.14 → 0.28
   - asr: 0.28 → 0.42
   - chords: 0.42 → 0.56
   - melody_bass: 0.56 → 0.70
   - structure: 0.70 → 0.85
   - packager: 0.85 → 1.0

2. **Event Types**:
   - `connected`: WebSocket connection established
   - `started`: Job started processing
   - `progress`: Service progress update
   - `service_complete`: Individual service finished
   - `complete`: Full pipeline finished
   - `error`: Pipeline or service error

3. **FastAPI WebSocket Implementation**:
```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/analyze/{job_id}")
async def websocket_analyze(websocket: WebSocket, job_id: str):
    await websocket.accept()
    try:
        # Stream progress updates
        async for update in pipeline_progress_stream(job_id):
            await websocket.send_json(update)
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for job {job_id}")
```

4. **Frontend Integration**:
```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/analyze/${jobId}`);

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  if (update.type === 'progress') {
    updateProgressBar(update.progress);
    displayMessage(update.message);
  }
};
```

5. **Benefits**:
   - Real-time UI updates without polling
   - Lower server load (no repeated GET requests)
   - Better UX with live progress tracking
   - Service-level granularity for detailed feedback

6. **Considerations**:
   - Connection management (reconnection on disconnect)
   - Multiple clients per job support
   - Broadcasting to all connected clients
   - Cleanup on job completion

## Dependencies

```
fastapi>=0.109.0
uvicorn>=0.27.0
python-multipart>=0.0.6
aiofiles>=23.0.0
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `202`: Accepted (job still processing)
- `400`: Bad request (invalid input)
- `404`: Job not found
- `500`: Internal server error (pipeline failure)

Example error response:
```json
{
  "error": "Internal server error",
  "detail": "Pipeline failed: Service timeout"
}
```

## CORS Configuration

The API includes CORS middleware for frontend integration. Update `allow_origins` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Performance Notes

- **Sub-10ms Latency**: Audio pipeline targeting <10ms latency for live performance
- **Parallel Processing**: Services run in parallel where dependencies allow
- **Typical Pipeline Time**: 4-5 seconds for 8-second audio clip
- **Scalability**: Can handle multiple concurrent jobs via background tasks

## Monitoring

Monitor server logs for pipeline execution:

```bash
tail -f logs/api.log
```

Key metrics:
- Job creation rate
- Pipeline completion time
- Error rate
- Active jobs count

## Future Enhancements

1. **WebSocket Support**: Real-time progress streaming
2. **Job Persistence**: Save jobs to database (Redis/PostgreSQL)
3. **Authentication**: API key or JWT authentication
4. **Rate Limiting**: Prevent abuse
5. **File Validation**: Audio format/duration validation
6. **Cleanup Jobs**: Automatic cleanup of old jobs
7. **Batch Processing**: Multiple files in one request
8. **Priority Queue**: Priority levels for different users
9. **Caching**: Cache Song Maps for identical audio
10. **Metrics**: Prometheus metrics endpoint
