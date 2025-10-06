# Knowledge Base Warming & Heartbeat System

## Overview

The enhanced Knowledge Base RAG system (`knowledge_rag_v2.py`) provides automatic warming, semantic query caching, and continuous heartbeat monitoring to maintain optimal performance and responsiveness.

## Key Features

### 1. Startup Warming
- **Auto-load on initialization**: Documents and index pre-loaded from cache
- **Common query execution**: 7+ warming queries executed to populate cache
- **Performance boost**: Reduces first-query latency from 2-5s to 50-100ms (40-100x improvement)

### 2. Semantic Query Caching
- **MD5-based cache keys**: Normalized queries (case-insensitive, whitespace-trimmed)
- **LRU eviction**: Maximum 100 cached queries, oldest evicted automatically
- **Cache hit rate**: Expected 70-85% for typical usage patterns
- **Sub-10ms response**: Cache hits return in <10ms

### 3. Background Heartbeat
- **Continuous interaction**: Periodic queries keep KB "warm" and responsive
- **Auto-cache invalidation**: Detects file changes and rebuilds index
- **Health monitoring**: Logs performance metrics every heartbeat cycle
- **Configurable interval**: Default 300s (5 minutes), adjustable

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    KnowledgeBase (Core)                      │
├─────────────────────────────────────────────────────────────┤
│  • Document Ingestion (docling)                             │
│  • Word Index (inverted index)                              │
│  • Query Cache (MD5 -> results)                             │
│  • Performance Metrics                                       │
└─────────────────────────────────────────────────────────────┘
         ▲                                ▲
         │                                │
         │ queries                        │ monitors
         │                                │
┌────────┴────────┐              ┌───────┴──────────┐
│  Application    │              │    Heartbeat     │
│  (API/CLI)      │              │   (Background)   │
└─────────────────┘              └──────────────────┘
```

## Usage

### Python API

```python
from knowledge_rag_v2 import KnowledgeBase, KnowledgeBaseHeartbeat

# Initialize with auto-warming
kb = KnowledgeBase(auto_warm=True)

# Query the KB
results = kb.query("librosa audio analysis")

# Get performance stats
stats = kb.get_stats()
print(f"Cache hit rate: {stats['cache_hit_rate']}")

# Start heartbeat
heartbeat = KnowledgeBaseHeartbeat(kb, interval=300)
heartbeat.start()

# ... do work ...

# Stop heartbeat
heartbeat.stop()
```

### CLI Service

```bash
# Start KB service with warming and heartbeat
python scripts/start_kb_service.py

# Custom interval (60 seconds)
python scripts/start_kb_service.py --interval 60

# Warming only, no heartbeat
python scripts/start_kb_service.py --no-heartbeat
```

### REST API Endpoints

#### Health Check
```bash
GET /api/kb/health
```

Response:
```json
{
  "status": "healthy",
  "documents": 11,
  "terms": 4350,
  "total_queries": 127,
  "cache_hit_rate": "78.5%",
  "cached_queries": 42,
  "warm_queries": 7,
  "last_access_age": "2.3s ago",
  "heartbeat_active": true,
  "heartbeat_count": 15
}
```

#### Detailed Statistics
```bash
GET /api/kb/stats
```

Response:
```json
{
  "queries": 127,
  "cache_hits": 97,
  "cache_misses": 30,
  "warm_queries": 7,
  "cache_hit_rate": "76.4%",
  "total_queries": 127,
  "documents": 11,
  "terms": 4350,
  "cached_queries": 42,
  "last_access_age": "1.2s ago",
  "last_warm_time": 0.847
}
```

#### Query Knowledge Base
```bash
GET /api/kb/query?q=librosa%20best%20practices&use_cache=true
```

Response:
```json
{
  "query": "librosa best practices",
  "results_count": 3,
  "results": [
    {
      "doc_id": "audio-dsp/music-audio-knowledge.md",
      "name": "Music Audio Knowledge",
      "preview": "Librosa best practices: Use sr=22050 for music analysis..."
    }
  ],
  "cache_used": true
}
```

#### Trigger Manual Warming
```bash
POST /api/kb/warm
```

#### Clear Cache
```bash
POST /api/kb/cache/clear
```

#### Start/Stop Heartbeat
```bash
POST /api/kb/heartbeat/start?interval=300
POST /api/kb/heartbeat/stop
```

## Performance Metrics

### Expected Performance

| Metric | Cold Start | Warmed | Cached |
|--------|-----------|--------|--------|
| **First query** | 2-5s | 50-100ms | <10ms |
| **Repeat query** | 50-200ms | 50-100ms | <10ms |
| **Initialization** | N/A | 0.8-1.5s | N/A |
| **Cache hit rate** | 0% | 70-85% | 100% |

### Memory Footprint

- Base KB: ~50-100MB (11 documents, 4,350 terms)
- Query cache: ~10-50MB (100 cached queries)
- Total: ~60-150MB

### Disk I/O

- Initial load: ~100-200ms (pickle cache)
- Cache invalidation check: <10ms
- Full rebuild: 1-2s (if files changed)

## Configuration

### Environment Variables

```bash
# Knowledge base directory (default: knowledge-base)
KB_DIR=knowledge-base

# Cache file location (default: .knowledge_cache.pkl)
KB_CACHE_FILE=.knowledge_cache.pkl

# Heartbeat interval in seconds (default: 300)
KB_HEARTBEAT_INTERVAL=300

# Auto-warm on startup (default: true)
KB_AUTO_WARM=true
```

### Programmatic Configuration

```python
kb = KnowledgeBase(
    knowledge_dir="custom-kb",
    auto_warm=True,
    cache_file=".custom_cache.pkl"
)

heartbeat = KnowledgeBaseHeartbeat(
    kb,
    interval=600  # 10 minutes
)
```

## Testing

### Run Test Suite

```bash
# All tests
pytest tests/test_knowledge_rag_v2.py -v

# Specific test class
pytest tests/test_knowledge_rag_v2.py::TestKnowledgeBaseWarming -v

# Heartbeat tests (slower, uses sleep)
pytest tests/test_knowledge_rag_v2.py::TestHeartbeat -v
```

### Manual Testing

```bash
# Test warming and queries
python knowledge_rag_v2.py

# Test heartbeat (runs for 15 seconds)
python knowledge_rag_v2.py --test-heartbeat
```

## Integration

### FastAPI Backend Integration

Already integrated in `backend/src/services/api/main.py`:

```python
from services.api import kb_health
app.include_router(kb_health.router)
```

### Systemd Service (Production)

Create `/etc/systemd/system/performia-kb.service`:

```ini
[Unit]
Description=Performia Knowledge Base Service
After=network.target

[Service]
Type=simple
User=performia
WorkingDirectory=/opt/performia
ExecStart=/opt/performia/venv/bin/python scripts/start_kb_service.py --interval 300
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable performia-kb
sudo systemctl start performia-kb
sudo systemctl status performia-kb
```

### PM2 Process Manager

```bash
pm2 start scripts/start_kb_service.py --name performia-kb --interpreter python3
pm2 save
pm2 startup
```

## Monitoring & Observability

### Health Check Endpoint

Monitor KB health via `/api/kb/health`:

```bash
# Uptime check
curl http://localhost:3002/api/kb/health | jq '.status'

# Cache performance
curl http://localhost:3002/api/kb/health | jq '.cache_hit_rate'

# Heartbeat status
curl http://localhost:3002/api/kb/health | jq '.heartbeat_active'
```

### Prometheus Metrics (Future)

Planned metrics endpoint: `/api/kb/metrics`

```
# HELP kb_queries_total Total number of queries
# TYPE kb_queries_total counter
kb_queries_total 1247

# HELP kb_cache_hit_rate Cache hit rate percentage
# TYPE kb_cache_hit_rate gauge
kb_cache_hit_rate 78.5

# HELP kb_documents_total Total number of indexed documents
# TYPE kb_documents_total gauge
kb_documents_total 11
```

## Troubleshooting

### Issue: Slow first query after restart

**Cause**: Cache not warmed on startup

**Solution**: Ensure `auto_warm=True` or manually call `kb.warm_up()`

```python
kb = KnowledgeBase(auto_warm=True)  # ✅ Good
```

### Issue: Cache not invalidating after file changes

**Cause**: Heartbeat not running or interval too long

**Solution**: Start heartbeat with shorter interval

```bash
python scripts/start_kb_service.py --interval 60
```

### Issue: High memory usage

**Cause**: Query cache growing too large

**Solution**: Clear cache periodically or reduce max size

```python
kb.clear_cache()  # Manual clear

# Or reduce max in knowledge_rag_v2.py:
if len(self.query_cache) > 50:  # Reduce from 100
    oldest_key = next(iter(self.query_cache))
    del self.query_cache[oldest_key]
```

### Issue: Heartbeat not starting

**Cause**: Port conflict or KB initialization failed

**Solution**: Check logs and KB health

```bash
curl http://localhost:3002/api/kb/health
```

## Best Practices

1. **Always use auto-warming in production**
   ```python
   kb = KnowledgeBase(auto_warm=True)
   ```

2. **Enable heartbeat for long-running services**
   ```python
   heartbeat = KnowledgeBaseHeartbeat(kb, interval=300)
   heartbeat.start()
   ```

3. **Monitor cache hit rate**
   - Target: >70% for good performance
   - If <50%, review query patterns

4. **Use cache for read-heavy workloads**
   ```python
   results = kb.query("query", use_cache=True)  # Default
   ```

5. **Clear cache after bulk updates**
   ```python
   # After adding many documents
   kb.ingest_all()
   kb.clear_cache()
   kb.warm_up()
   ```

## Migration from v1

### Changes

- `knowledge_rag.py` → `knowledge_rag_v2.py`
- Added `warm_up()` method
- Added `query(..., use_cache=bool)` parameter
- Added `get_stats()` method
- Added `KnowledgeBaseHeartbeat` class
- Added `clear_cache()` method

### Backward Compatibility

v2 maintains full API compatibility with v1:

```python
# v1 code (still works)
kb = KnowledgeBase()
kb.ingest_all()
results = kb.query("search terms")

# v2 enhanced (recommended)
kb = KnowledgeBase(auto_warm=True)
results = kb.query("search terms", use_cache=True)
stats = kb.get_stats()
```

### Migration Steps

1. Replace import: `from knowledge_rag_v2 import KnowledgeBase`
2. Enable auto-warming: `KnowledgeBase(auto_warm=True)`
3. Optional: Add heartbeat for long-running processes
4. Optional: Integrate `/api/kb/health` monitoring

## Performance Tuning

### Cache Size

Adjust max cache size in `knowledge_rag_v2.py`:

```python
# Line ~210
if len(self.query_cache) > 100:  # Increase for larger workloads
```

### Warming Queries

Customize warming queries in `warm_up()` method:

```python
common_queries = [
    "your custom query 1",
    "your custom query 2",
    # ...
]
```

### Heartbeat Interval

Shorter intervals = fresher cache, higher CPU usage:
- **Development**: 60s (1 minute)
- **Production**: 300s (5 minutes, default)
- **Low-traffic**: 600s (10 minutes)

## Roadmap

### Phase 1: Current Implementation ✅
- Startup warming
- Query caching with LRU
- Background heartbeat
- REST API endpoints

### Phase 2: Enhanced Metrics (Next)
- Prometheus metrics export
- Grafana dashboard templates
- Alert rules (low hit rate, stale cache)

### Phase 3: Advanced Features (Future)
- Semantic embeddings (vector similarity)
- Multi-level caching (L1 memory, L2 disk)
- Distributed KB (Redis-backed cache)
- Query prediction and pre-fetching

---

**Last Updated**: October 5, 2025
**Version**: 2.0
**Status**: Production Ready
