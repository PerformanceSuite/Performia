# API Reference

Complete REST API reference for Performia Song Map generation and management.

---

## Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Endpoints](#endpoints)
  - [Health & Info](#health--info)
  - [Song Analysis](#song-analysis)
  - [Job Management](#job-management)
  - [Song Maps](#song-maps)
  - [Audio Streaming](#audio-streaming)
- [WebSocket API](#websocket-api)
- [Examples](#examples)

---

## Base URL

**Development**:
```
http://localhost:8000
```

**Production**:
```
https://api.performia.app
```

**API Version**: v1 (implicit in current paths)

---

## Authentication

Currently, the API is **unauthenticated** for development.

**Future**: API keys will be required for production deployments:

```http
Authorization: Bearer YOUR_API_KEY
```

---

## Response Format

All responses are in JSON format with appropriate HTTP status codes.

### Success Response

```json
{
  "data": { ... },
  "message": "Success message",
  "timestamp": "2025-10-05T12:00:00Z"
}
```

### Error Response

```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "timestamp": "2025-10-05T12:00:00Z"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET request |
| 201 | Created | Successful POST (resource created) |
| 202 | Accepted | Job accepted for processing |
| 400 | Bad Request | Invalid input |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

### Common Errors

**Invalid File Format**:
```json
{
  "error": "Invalid file format",
  "detail": "Only MP3, WAV, M4A, FLAC, and OGG formats are supported"
}
```

**Job Not Found**:
```json
{
  "error": "Job not found",
  "detail": "Job d4e5f6g7 not found"
}
```

**Processing Error**:
```json
{
  "error": "Processing failed",
  "detail": "Whisper transcription failed: timeout after 300s"
}
```

---

## Rate Limiting

**Current**: No rate limiting (development)

**Future**: Production rate limits:
- 100 requests per minute per IP
- 10 concurrent jobs per user
- 1GB total upload per day

---

## Endpoints

### Health & Info

#### GET /

Get API information.

**Request**:
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "name": "Performia Song Map API",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": {
    "analyze": "POST /api/analyze",
    "status": "GET /api/status/{job_id}",
    "songmap": "GET /api/songmap/{job_id}"
  }
}
```

#### GET /health

Health check endpoint.

**Request**:
```http
GET /health HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "status": "healthy",
  "jobs_count": 42,
  "database": "performia.db"
}
```

---

### Song Analysis

#### POST /api/analyze

Upload audio file for Song Map generation.

**Request**:
```http
POST /api/analyze HTTP/1.1
Host: localhost:8000
Content-Type: multipart/form-data

file: (audio file binary)
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@/path/to/song.mp3"
```

**Python Example**:
```python
import requests

with open('song.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/analyze',
        files={'file': f}
    )

job_id = response.json()['job_id']
print(f"Job created: {job_id}")
```

**JavaScript Example**:
```javascript
const formData = new FormData();
formData.append('file', audioFile);

const response = await fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  body: formData
});

const { job_id } = await response.json();
console.log(`Job created: ${job_id}`);
```

**Response** (202 Accepted):
```json
{
  "job_id": "d4e5f6g7",
  "status": "pending",
  "message": "Analysis started for song.mp3"
}
```

**Supported Formats**:
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- FLAC (.flac)
- OGG (.ogg)

**File Size Limit**: 100 MB (recommended)

---

### Job Management

#### GET /api/status/{job_id}

Get job status and progress.

**Request**:
```http
GET /api/status/d4e5f6g7 HTTP/1.1
Host: localhost:8000
```

**Response** (Processing):
```json
{
  "job_id": "d4e5f6g7",
  "status": "processing",
  "progress": 0.65,
  "created_at": "2025-10-05T12:00:00Z",
  "updated_at": "2025-10-05T12:00:20Z",
  "elapsed": 20.5,
  "audio_path": "/uploads/d4e5f6g7.mp3"
}
```

**Response** (Complete):
```json
{
  "job_id": "d4e5f6g7",
  "status": "complete",
  "progress": 1.0,
  "created_at": "2025-10-05T12:00:00Z",
  "updated_at": "2025-10-05T12:00:30Z",
  "elapsed": 30.2,
  "audio_path": "/uploads/d4e5f6g7.mp3",
  "song_map_path": "/output/d4e5f6g7/d4e5f6g7.song_map.json"
}
```

**Response** (Error):
```json
{
  "job_id": "d4e5f6g7",
  "status": "error",
  "progress": 0.4,
  "error_message": "Whisper transcription failed: timeout",
  "created_at": "2025-10-05T12:00:00Z",
  "updated_at": "2025-10-05T12:05:00Z",
  "elapsed": 300.0
}
```

**Job Statuses**:
- `pending`: Job created, waiting to start
- `processing`: Analysis in progress
- `complete`: Song Map generated successfully
- `error`: Processing failed

#### GET /api/jobs

List all jobs.

**Request**:
```http
GET /api/jobs HTTP/1.1
Host: localhost:8000
```

**Query Parameters**:
- `status` (optional): Filter by status (pending, processing, complete, error)
- `limit` (optional): Max number of results (default: 100)
- `offset` (optional): Pagination offset (default: 0)

**Response**:
```json
{
  "count": 2,
  "jobs": [
    {
      "job_id": "d4e5f6g7",
      "status": "complete",
      "progress": 1.0,
      "created_at": "2025-10-05T12:00:00Z",
      "elapsed": 30.2
    },
    {
      "job_id": "a1b2c3d4",
      "status": "processing",
      "progress": 0.5,
      "created_at": "2025-10-05T12:01:00Z",
      "elapsed": 15.0
    }
  ]
}
```

#### DELETE /api/jobs/{job_id}

Delete a job and its files.

**Request**:
```http
DELETE /api/jobs/d4e5f6g7 HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "message": "Job d4e5f6g7 deleted",
  "job_id": "d4e5f6g7"
}
```

**What Gets Deleted**:
- Job record from database
- Uploaded audio file
- Song Map JSON
- Separated stems (if any)
- Analysis intermediates

#### DELETE /api/jobs/cleanup

Clean up old jobs.

**Request**:
```http
DELETE /api/jobs/cleanup?days=7 HTTP/1.1
Host: localhost:8000
```

**Query Parameters**:
- `days` (optional): Delete jobs older than N days (default: 7)

**Response**:
```json
{
  "message": "Cleaned up 15 jobs older than 7 days",
  "deleted_count": 15,
  "retention_days": 7
}
```

---

### Song Maps

#### GET /api/songmap/{job_id}

Get Song Map JSON for completed job.

**Request**:
```http
GET /api/songmap/d4e5f6g7 HTTP/1.1
Host: localhost:8000
```

**Response** (Complete):
```json
{
  "job_id": "d4e5f6g7",
  "elapsed": 30.2,
  "song_map": {
    "title": "Yesterday",
    "artist": "The Beatles",
    "album": "Help!",
    "key": "F",
    "tempo": 97.5,
    "duration": 125.3,
    "sections": [
      {
        "name": "Verse 1",
        "startTime": 5.2,
        "lines": [
          {
            "syllables": [
              {
                "text": "Yes",
                "startTime": 5.2,
                "duration": 0.15,
                "chord": "F",
                "pitch": 65.4
              },
              {
                "text": "ter",
                "startTime": 5.35,
                "duration": 0.12,
                "chord": "F",
                "pitch": 69.3
              },
              {
                "text": "day",
                "startTime": 5.47,
                "duration": 0.38,
                "chord": "Em7",
                "pitch": 67.8
              }
            ]
          }
        ]
      }
    ]
  }
}
```

**Response** (Processing - 202):
```json
{
  "error": "Job still processing",
  "detail": "Job d4e5f6g7 is still processing (progress: 65%)",
  "progress": 0.65
}
```

**Response** (Error - 500):
```json
{
  "error": "Job failed",
  "detail": "Job d4e5f6g7 failed: Whisper transcription timeout"
}
```

---

### Audio Streaming

#### GET /api/audio/{job_id}/original

Stream original uploaded audio.

**Request**:
```http
GET /api/audio/d4e5f6g7/original HTTP/1.1
Host: localhost:8000
Range: bytes=0-1023
```

**Response**:
```http
HTTP/1.1 206 Partial Content
Content-Type: audio/mpeg
Content-Length: 1024
Accept-Ranges: bytes
Content-Range: bytes 0-1023/5242880

(audio binary data)
```

**Supported Media Types**:
- `audio/mpeg` (.mp3)
- `audio/wav` (.wav)
- `audio/mp4` (.m4a)
- `audio/flac` (.flac)
- `audio/ogg` (.ogg)

#### GET /api/audio/{job_id}/stem/{stem_name}

Stream separated audio stem.

**Request**:
```http
GET /api/audio/d4e5f6g7/stem/vocals HTTP/1.1
Host: localhost:8000
```

**Stem Names**:
- `vocals` - Isolated vocals
- `bass` - Bass track
- `drums` - Drum track
- `other` - Other instruments

**Response**:
```http
HTTP/1.1 200 OK
Content-Type: audio/wav
Accept-Ranges: bytes

(WAV audio data)
```

**Note**: Stems are only available if separation was enabled during processing.

---

## WebSocket API

Real-time job progress updates via WebSocket.

### Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/jobs/{job_id}');

ws.onopen = () => {
  console.log('Connected to job updates');
};

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('Progress:', update.progress);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected');
};
```

### Messages

**Progress Update**:
```json
{
  "type": "progress",
  "job_id": "d4e5f6g7",
  "status": "processing",
  "progress": 0.65,
  "current_service": "chords",
  "message": "Analyzing chord progressions..."
}
```

**Completion**:
```json
{
  "type": "complete",
  "job_id": "d4e5f6g7",
  "status": "complete",
  "progress": 1.0,
  "elapsed": 30.2,
  "song_map_path": "/output/d4e5f6g7/d4e5f6g7.song_map.json"
}
```

**Error**:
```json
{
  "type": "error",
  "job_id": "d4e5f6g7",
  "status": "error",
  "error_message": "Processing failed: timeout"
}
```

---

## Examples

### Complete Workflow (Python)

```python
import requests
import time

# 1. Upload audio
with open('song.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/analyze',
        files={'file': f}
    )

job_id = response.json()['job_id']
print(f"Job created: {job_id}")

# 2. Poll for completion
while True:
    status_response = requests.get(
        f'http://localhost:8000/api/status/{job_id}'
    )
    status = status_response.json()

    print(f"Progress: {status['progress']*100:.0f}%")

    if status['status'] == 'complete':
        print(f"Complete! Elapsed: {status['elapsed']:.1f}s")
        break
    elif status['status'] == 'error':
        print(f"Error: {status['error_message']}")
        break

    time.sleep(2)

# 3. Get Song Map
songmap_response = requests.get(
    f'http://localhost:8000/api/songmap/{job_id}'
)
song_map = songmap_response.json()['song_map']

print(f"Title: {song_map['title']}")
print(f"Artist: {song_map['artist']}")
print(f"Sections: {len(song_map['sections'])}")
```

### Complete Workflow (JavaScript)

```javascript
// 1. Upload audio
async function uploadSong(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('http://localhost:8000/api/analyze', {
    method: 'POST',
    body: formData
  });

  const { job_id } = await response.json();
  console.log(`Job created: ${job_id}`);
  return job_id;
}

// 2. Poll for completion
async function pollJobStatus(jobId) {
  while (true) {
    const response = await fetch(
      `http://localhost:8000/api/status/${jobId}`
    );
    const status = await response.json();

    console.log(`Progress: ${status.progress * 100}%`);

    if (status.status === 'complete') {
      console.log(`Complete! Elapsed: ${status.elapsed}s`);
      return status;
    } else if (status.status === 'error') {
      throw new Error(status.error_message);
    }

    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

// 3. Get Song Map
async function getSongMap(jobId) {
  const response = await fetch(
    `http://localhost:8000/api/songmap/${jobId}`
  );
  const { song_map } = await response.json();
  return song_map;
}

// Complete workflow
const fileInput = document.querySelector('#audio-file');
const file = fileInput.files[0];

const jobId = await uploadSong(file);
await pollJobStatus(jobId);
const songMap = await getSongMap(jobId);

console.log('Song Map:', songMap);
```

### WebSocket Real-Time Updates

```javascript
function subscribeToJob(jobId) {
  const ws = new WebSocket(`ws://localhost:8000/ws/jobs/${jobId}`);

  ws.onmessage = (event) => {
    const update = JSON.parse(event.data);

    switch (update.type) {
      case 'progress':
        updateProgressBar(update.progress);
        updateStatus(update.message);
        break;

      case 'complete':
        showSuccess('Song Map generated!');
        loadSongMap(update.job_id);
        ws.close();
        break;

      case 'error':
        showError(update.error_message);
        ws.close();
        break;
    }
  };

  return ws;
}

// Usage
const jobId = await uploadSong(file);
const ws = subscribeToJob(jobId);
```

### Batch Processing

```python
import requests
import asyncio

async def process_song(filepath):
    """Process a single song."""
    with open(filepath, 'rb') as f:
        response = requests.post(
            'http://localhost:8000/api/analyze',
            files={'file': f}
        )
    job_id = response.json()['job_id']

    # Wait for completion
    while True:
        status = requests.get(f'/api/status/{job_id}').json()
        if status['status'] in ['complete', 'error']:
            return status
        await asyncio.sleep(2)

async def process_batch(filepaths):
    """Process multiple songs concurrently."""
    tasks = [process_song(fp) for fp in filepaths]
    results = await asyncio.gather(*tasks)
    return results

# Process 10 songs concurrently
songs = ['song1.mp3', 'song2.mp3', ..., 'song10.mp3']
results = asyncio.run(process_batch(songs))

for result in results:
    if result['status'] == 'complete':
        print(f"Success: {result['job_id']}")
    else:
        print(f"Failed: {result['error_message']}")
```

---

## OpenAPI Specification

Interactive API documentation available at:

**Swagger UI**:
```
http://localhost:8000/docs
```

**ReDoc**:
```
http://localhost:8000/redoc
```

**OpenAPI JSON**:
```
http://localhost:8000/openapi.json
```

---

## Versioning

Current API version: **v1**

Breaking changes will be introduced in new versions (v2, v3, etc.).

**Version Format**:
```
/api/v1/analyze
/api/v2/analyze  (future)
```

---

## Support

For API questions or issues:

- **Documentation**: [INSTALLATION.md](./INSTALLATION.md), [USAGE.md](./USAGE.md)
- **GitHub Issues**: [Report bugs or request features](https://github.com/PerformanceSuite/Performia/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/PerformanceSuite/Performia/discussions)

---

*Last updated: October 2025*
