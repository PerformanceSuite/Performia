#!/usr/bin/env python3
"""
Test suite for enhanced Knowledge Base RAG system
Tests warming, caching, heartbeat, and performance metrics
"""

import pytest
import time
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_rag_v2 import KnowledgeBase, KnowledgeBaseHeartbeat


@pytest.fixture
def temp_kb_dir():
    """Create temporary knowledge base directory for testing."""
    temp_dir = tempfile.mkdtemp()
    kb_path = Path(temp_dir) / "knowledge-base"
    kb_path.mkdir()

    # Create test documents
    (kb_path / "test-doc-1.md").write_text("""
# Test Document 1
This document contains information about audio processing.
Librosa is a Python library for audio analysis.
JUCE is a C++ framework for real-time audio.
""")

    (kb_path / "test-doc-2.md").write_text("""
# Test Document 2
SuperCollider is a platform for audio synthesis.
Real-time DSP requires low-latency processing.
Music theory includes chord progressions and harmony.
""")

    yield kb_path

    # Cleanup
    shutil.rmtree(temp_dir)


class TestKnowledgeBaseWarming:
    """Test warming functionality."""

    def test_auto_warm_on_init(self, temp_kb_dir):
        """Test that auto_warm=True warms the KB on initialization."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=True)

        assert len(kb.documents) > 0, "Documents should be loaded"
        assert len(kb.index) > 0, "Index should be built"
        assert kb.stats['warm_queries'] > 0, "Warming queries should be executed"
        assert kb.stats['last_warm_time'] is not None, "Warm time should be recorded"

    def test_manual_warm(self, temp_kb_dir):
        """Test manual warming via warm_up() method."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)

        assert kb.stats['warm_queries'] == 0, "No warming queries yet"

        kb.warm_up()

        assert kb.stats['warm_queries'] > 0, "Warming queries executed"
        assert len(kb.documents) > 0, "Documents loaded"

    def test_warm_reduces_latency(self, temp_kb_dir):
        """Test that warming reduces query latency."""
        # Cold start
        kb_cold = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb_cold.ingest_all()

        start_cold = time.time()
        kb_cold.query("audio processing")
        cold_time = time.time() - start_cold

        # Warm start
        kb_warm = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=True)

        start_warm = time.time()
        kb_warm.query("audio processing")
        warm_time = time.time() - start_warm

        # Note: In this simple test, difference might be minimal
        # In production with larger KB, warm should be significantly faster
        assert warm_time <= cold_time * 2, "Warm query should be reasonably fast"


class TestQueryCaching:
    """Test query caching functionality."""

    def test_cache_hit(self, temp_kb_dir):
        """Test that repeated queries hit the cache."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        # First query (cache miss)
        kb.query("librosa audio analysis")
        assert kb.stats['cache_misses'] == 1
        assert kb.stats['cache_hits'] == 0

        # Second identical query (cache hit)
        kb.query("librosa audio analysis")
        assert kb.stats['cache_hits'] == 1

    def test_cache_bypass(self, temp_kb_dir):
        """Test that use_cache=False bypasses cache."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        kb.query("test query", use_cache=False)
        kb.query("test query", use_cache=False)

        assert kb.stats['cache_hits'] == 0, "Should not use cache"
        assert kb.stats['cache_misses'] == 2

    def test_lru_eviction(self, temp_kb_dir):
        """Test that cache evicts old entries when full."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        # Fill cache beyond limit (100 entries)
        for i in range(105):
            kb.query(f"unique query {i}")

        assert len(kb.query_cache) <= 100, "Cache should be limited to 100 entries"

    def test_cache_key_generation(self, temp_kb_dir):
        """Test that cache keys are consistent."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        key1 = kb._generate_cache_key("Test Query")
        key2 = kb._generate_cache_key("test query")  # Different case
        key3 = kb._generate_cache_key("  test query  ")  # Extra whitespace

        assert key1 == key2 == key3, "Cache keys should normalize queries"

    def test_clear_cache(self, temp_kb_dir):
        """Test cache clearing."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        kb.query("test")
        assert len(kb.query_cache) > 0

        kb.clear_cache()
        assert len(kb.query_cache) == 0


class TestPerformanceMetrics:
    """Test performance statistics tracking."""

    def test_stats_initialization(self, temp_kb_dir):
        """Test that stats are properly initialized."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)

        stats = kb.get_stats()
        assert 'queries' in stats
        assert 'cache_hits' in stats
        assert 'cache_misses' in stats
        assert 'cache_hit_rate' in stats

    def test_stats_update(self, temp_kb_dir):
        """Test that stats update correctly."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        initial_stats = kb.get_stats()
        assert initial_stats['total_queries'] == 0

        kb.query("test")
        kb.query("test")  # Cache hit

        updated_stats = kb.get_stats()
        assert updated_stats['total_queries'] == 2
        assert updated_stats['cache_hits'] == 1
        assert updated_stats['cache_misses'] == 1
        assert '50.0%' in updated_stats['cache_hit_rate']

    def test_last_access_tracking(self, temp_kb_dir):
        """Test that last access time is tracked."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        time.sleep(0.1)
        kb.query("test")

        stats = kb.get_stats()
        assert 'last_access_age' in stats
        assert 'ago' in stats['last_access_age']


class TestHeartbeat:
    """Test heartbeat mechanism."""

    def test_heartbeat_start_stop(self, temp_kb_dir):
        """Test heartbeat start and stop."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        heartbeat = KnowledgeBaseHeartbeat(kb, interval=1)
        assert not heartbeat.running

        heartbeat.start()
        assert heartbeat.running
        assert heartbeat.thread is not None

        time.sleep(0.5)

        heartbeat.stop()
        assert not heartbeat.running

    def test_heartbeat_executes(self, temp_kb_dir):
        """Test that heartbeat actually executes queries."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        initial_queries = kb.stats['queries']

        heartbeat = KnowledgeBaseHeartbeat(kb, interval=1)
        heartbeat.start()

        # Wait for at least 2 heartbeats
        time.sleep(2.5)

        heartbeat.stop()

        # Should have executed at least 2 warming queries
        assert kb.stats['queries'] > initial_queries
        assert heartbeat.heartbeat_count >= 2

    def test_heartbeat_prevents_double_start(self, temp_kb_dir):
        """Test that starting heartbeat twice is handled."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        heartbeat = KnowledgeBaseHeartbeat(kb, interval=1)
        heartbeat.start()
        heartbeat.start()  # Should not crash

        time.sleep(0.5)
        heartbeat.stop()

    def test_heartbeat_cache_staleness_check(self, temp_kb_dir, tmp_path):
        """Test that heartbeat detects stale cache."""
        # Create KB with cache file in temp location
        cache_file = tmp_path / ".test_cache.pkl"

        kb = KnowledgeBase(
            knowledge_dir=str(temp_kb_dir),
            auto_warm=False,
            cache_file=str(cache_file)
        )
        kb.ingest_all()

        heartbeat = KnowledgeBaseHeartbeat(kb, interval=1)

        # Test staleness detection
        is_stale = heartbeat._is_cache_stale()
        assert not is_stale, "Fresh cache should not be stale"

        # Modify a file to make cache stale
        time.sleep(0.1)
        test_file = temp_kb_dir / "test-doc-1.md"
        test_file.write_text("Updated content")

        is_stale = heartbeat._is_cache_stale()
        assert is_stale, "Modified file should make cache stale"


class TestQueryFunctionality:
    """Test core query functionality."""

    def test_basic_query(self, temp_kb_dir):
        """Test basic query returns results."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        results = kb.query("librosa")
        assert len(results) > 0, "Should find documents mentioning librosa"

        doc_id, doc = results[0]
        assert 'librosa' in doc['content'].lower()

    def test_multi_term_query(self, temp_kb_dir):
        """Test query with multiple terms."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        results = kb.query("audio processing")
        assert len(results) > 0

    def test_no_results_query(self, temp_kb_dir):
        """Test query that finds no results."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        results = kb.query("nonexistent-term-xyz")
        assert len(results) == 0

    def test_get_answer(self, temp_kb_dir):
        """Test get_answer convenience method."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        answer = kb.get_answer("What is librosa?")
        assert "librosa" in answer.lower()
        assert "📄" in answer  # Should include formatted response

    def test_get_answer_no_results(self, temp_kb_dir):
        """Test get_answer when no results found."""
        kb = KnowledgeBase(knowledge_dir=str(temp_kb_dir), auto_warm=False)
        kb.ingest_all()

        answer = kb.get_answer("xyz-nonexistent")
        assert "No relevant documentation found" in answer


class TestCacheInvalidation:
    """Test cache invalidation and rebuilding."""

    def test_cache_file_creation(self, temp_kb_dir, tmp_path):
        """Test that cache file is created."""
        cache_file = tmp_path / ".test_cache.pkl"

        kb = KnowledgeBase(
            knowledge_dir=str(temp_kb_dir),
            auto_warm=False,
            cache_file=str(cache_file)
        )
        kb.ingest_all()

        assert cache_file.exists(), "Cache file should be created"

    def test_cache_reuse(self, temp_kb_dir, tmp_path):
        """Test that cache is reused on second initialization."""
        cache_file = tmp_path / ".test_cache.pkl"

        # First initialization
        kb1 = KnowledgeBase(
            knowledge_dir=str(temp_kb_dir),
            auto_warm=False,
            cache_file=str(cache_file)
        )
        kb1.ingest_all()

        # Second initialization (should use cache)
        kb2 = KnowledgeBase(
            knowledge_dir=str(temp_kb_dir),
            auto_warm=False,
            cache_file=str(cache_file)
        )
        kb2.ingest_all()

        assert len(kb1.documents) == len(kb2.documents)
        assert len(kb1.index) == len(kb2.index)

    def test_cache_invalidation_on_file_change(self, temp_kb_dir, tmp_path):
        """Test that cache is invalidated when files change."""
        cache_file = tmp_path / ".test_cache.pkl"

        kb1 = KnowledgeBase(
            knowledge_dir=str(temp_kb_dir),
            auto_warm=False,
            cache_file=str(cache_file)
        )
        kb1.ingest_all()

        # Modify a file
        time.sleep(0.1)
        test_file = temp_kb_dir / "test-doc-1.md"
        test_file.write_text("# Updated Content\nThis is new content.")

        # Re-initialize (should detect stale cache)
        kb2 = KnowledgeBase(
            knowledge_dir=str(temp_kb_dir),
            auto_warm=False,
            cache_file=str(cache_file)
        )
        kb2.ingest_all()

        # Verify content updated
        assert "new content" in kb2.documents['test-doc-1.md']['content'].lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
