# Song Map API - Quick Start Guide

## Run the API Server

```bash
# Activate environment
source venv/bin/activate

# Set PYTHONPATH
export PYTHONPATH=/Users/danielconnolly/Projects/Performia/backend/src

# Start server
python src/services/api/main.py
```

Server runs at: `http://localhost:8000`

## Test with curl

### 1. Upload Audio
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F 'file=@test_music.wav' \
  -H 'accept: application/json'
```

Returns:
```json
{"job_id": "abc123", "status": "pending"}
```

### 2. Check Status
```bash
curl http://localhost:8000/api/status/abc123
```

### 3. Get Song Map
```bash
curl http://localhost:8000/api/songmap/abc123
```

## Test with Python

```bash
python test_api.py
```

## API Documentation

Interactive docs: http://localhost:8000/docs

Full documentation: [src/services/api/README.md](src/services/api/README.md)
