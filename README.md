# Backend-Core Branch

Clean backend implementation for Performia.

## Components
- Audio engine (<10ms latency)
- 4 AI agents
- OSC server (port 7772)
- SuperCollider synthesis

## Running
```bash
pip install -r requirements.txt
python scripts/start_backend.py
```

## API
See [docs/API.md](docs/API.md) for OSC protocol documentation.
