"""
Knowledge Base Health Monitoring API
Provides endpoints for KB stats, health checks, and warming triggers
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import sys
import os
import logging
from pathlib import Path
from threading import Lock

# Add root to path for KB imports
root_dir = Path(os.getenv('PERFORMIA_ROOT', Path(__file__).parent.parent.parent.parent.parent))
sys.path.insert(0, str(root_dir))

from knowledge_rag_v2 import KnowledgeBase, KnowledgeBaseHeartbeat

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/kb", tags=["knowledge-base"])

# Global KB instance (initialized on startup) with thread safety
_kb_instance: Optional[KnowledgeBase] = None
_heartbeat_instance: Optional[KnowledgeBaseHeartbeat] = None
_kb_lock = Lock()
_heartbeat_lock = Lock()


class KBHealthResponse(BaseModel):
    """Health check response model."""
    status: str
    documents: int
    terms: int
    total_queries: int
    cache_hit_rate: str
    cached_queries: int
    warm_queries: int
    last_access_age: str
    heartbeat_active: bool
    heartbeat_count: Optional[int] = None


class KBStatsResponse(BaseModel):
    """Detailed statistics response model."""
    queries: int
    cache_hits: int
    cache_misses: int
    warm_queries: int
    cache_hit_rate: str
    total_queries: int
    documents: int
    terms: int
    cached_queries: int
    last_access_age: str
    last_warm_time: Optional[float]


class WarmResponse(BaseModel):
    """Warming operation response."""
    status: str
    warm_time: float
    warm_queries: int


def get_kb() -> KnowledgeBase:
    """Get or initialize KB instance with thread safety (double-check locking)."""
    global _kb_instance
    if _kb_instance is None:
        with _kb_lock:
            if _kb_instance is None:  # Double-check locking pattern
                logger.info("Initializing Knowledge Base with auto-warming...")
                _kb_instance = KnowledgeBase(auto_warm=True)
                logger.info("Knowledge Base initialized successfully")
    return _kb_instance


def get_heartbeat() -> Optional[KnowledgeBaseHeartbeat]:
    """Get heartbeat instance if running."""
    return _heartbeat_instance


@router.get("/health", response_model=KBHealthResponse)
async def kb_health():
    """
    Get knowledge base health status.

    Returns:
        Health metrics including document count, query stats, and heartbeat status
    """
    try:
        kb = get_kb()
        stats = kb.get_stats()
        heartbeat = get_heartbeat()

        return KBHealthResponse(
            status="healthy",
            documents=stats['documents'],
            terms=stats['terms'],
            total_queries=stats['total_queries'],
            cache_hit_rate=stats['cache_hit_rate'],
            cached_queries=stats['cached_queries'],
            warm_queries=stats['warm_queries'],
            last_access_age=stats['last_access_age'],
            heartbeat_active=heartbeat is not None and heartbeat.running,
            heartbeat_count=heartbeat.heartbeat_count if heartbeat else None
        )
    except Exception as e:
        logger.error(f"KB health check failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Health check failed")


@router.get("/stats", response_model=KBStatsResponse)
async def kb_stats():
    """
    Get detailed knowledge base statistics.

    Returns:
        Comprehensive performance metrics
    """
    try:
        kb = get_kb()
        stats = kb.get_stats()

        return KBStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get KB stats: {str(e)}")


@router.post("/warm", response_model=WarmResponse)
async def trigger_warm():
    """
    Manually trigger KB warming.

    Returns:
        Warming operation results
    """
    try:
        kb = get_kb()
        import time

        start = time.time()
        kb.warm_up()
        elapsed = time.time() - start

        return WarmResponse(
            status="success",
            warm_time=elapsed,
            warm_queries=kb.stats['warm_queries']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Warming failed: {str(e)}")


@router.post("/cache/clear")
async def clear_cache():
    """
    Clear query cache.

    Returns:
        Success message
    """
    try:
        kb = get_kb()
        kb.clear_cache()

        return {"status": "success", "message": "Query cache cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache clear failed: {str(e)}")


@router.post("/heartbeat/start")
async def start_heartbeat(interval: int = 300):
    """
    Start knowledge base heartbeat.

    Args:
        interval: Heartbeat interval in seconds (default: 300, min: 10, max: 86400)

    Returns:
        Success message
    """
    global _heartbeat_instance

    # Input validation
    if interval < 10:
        raise HTTPException(
            status_code=400,
            detail="Interval must be at least 10 seconds to avoid excessive CPU usage"
        )
    if interval > 86400:
        raise HTTPException(
            status_code=400,
            detail="Interval must be at most 24 hours (86400 seconds)"
        )

    try:
        kb = get_kb()

        with _heartbeat_lock:
            if _heartbeat_instance and _heartbeat_instance.running:
                return {"status": "already_running", "message": "Heartbeat already active"}

            _heartbeat_instance = KnowledgeBaseHeartbeat(kb, interval=interval)
            _heartbeat_instance.start()
            logger.info(f"Heartbeat started with {interval}s interval")

        return {
            "status": "success",
            "message": f"Heartbeat started with {interval}s interval"
        }
    except Exception as e:
        logger.error(f"Heartbeat start failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to start heartbeat")


@router.post("/heartbeat/stop")
async def stop_heartbeat():
    """
    Stop knowledge base heartbeat.

    Returns:
        Success message with heartbeat count
    """
    global _heartbeat_instance

    try:
        with _heartbeat_lock:
            if not _heartbeat_instance or not _heartbeat_instance.running:
                return {"status": "not_running", "message": "Heartbeat not active"}

            count = _heartbeat_instance.heartbeat_count
            _heartbeat_instance.stop()
            logger.info(f"Heartbeat stopped after {count} cycles")

        return {
            "status": "success",
            "message": f"Heartbeat stopped after {count} cycles"
        }
    except Exception as e:
        logger.error(f"Heartbeat stop failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to stop heartbeat")


@router.get("/query")
async def query_kb(q: str, use_cache: bool = True):
    """
    Query the knowledge base.

    Args:
        q: Query string
        use_cache: Whether to use cached results (default: True)

    Returns:
        Query results with document matches
    """
    try:
        kb = get_kb()
        results = kb.query(q, use_cache=use_cache)

        # Format results
        formatted_results = []
        for doc_id, doc in results[:5]:  # Top 5 results
            formatted_results.append({
                "doc_id": doc_id,
                "name": doc['name'],
                "preview": doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']
            })

        return {
            "query": q,
            "results_count": len(results),
            "results": formatted_results,
            "cache_used": use_cache
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")
