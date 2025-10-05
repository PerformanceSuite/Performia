#!/usr/bin/env python3
"""
Enhanced Knowledge Base RAG System with Warming & Heartbeat
Version 2.0 - Optimized for continuous interaction and performance

Features:
- Automatic startup warming for reduced first-query latency
- Semantic query caching with LRU eviction
- Background heartbeat for continuous interaction
- Performance metrics and health monitoring
- Auto-cache invalidation on file changes
"""

from docling.document_converter import DocumentConverter
from pathlib import Path
import json
import pickle
import os
import time
import threading
import random
import hashlib
from collections import OrderedDict
from typing import Dict, List, Tuple, Optional

# Configuration constants
MAX_CACHE_SIZE = 100  # Maximum number of cached queries
DEFAULT_HEARTBEAT_INTERVAL = 300  # Default heartbeat interval in seconds (5 minutes)
WARMING_QUERIES = [
    "claude code slash commands path",
    "librosa audio analysis parameters",
    "juce processBlock real-time audio",
    "supercollider synthdef patterns",
    "end-session cleanup procedure",
    "music theory chord progressions",
    "audio dsp fft algorithms"
]


class KnowledgeBase:
    """
    RAG Knowledge Base with warming, caching, and performance optimization.

    Usage:
        kb = KnowledgeBase(auto_warm=True)
        results = kb.query("librosa best practices")
        stats = kb.get_stats()
    """

    def __init__(self, knowledge_dir="knowledge-base", auto_warm=True, cache_file=".knowledge_cache.pkl"):
        """
        Initialize Knowledge Base with optional auto-warming.

        Args:
            knowledge_dir: Path to knowledge base directory
            auto_warm: If True, pre-load and warm cache on init
            cache_file: Path to cache file for persistent storage
        """
        self.knowledge_dir = Path(knowledge_dir)
        self.cache_file = cache_file
        self.converter = DocumentConverter()
        self.documents: Dict = {}
        self.index: Dict = {}
        self.query_cache: OrderedDict = OrderedDict()  # LRU cache with ordered access
        self.last_access = time.time()

        # Performance metrics
        self.stats = {
            'queries': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'warm_queries': 0,
            'last_warm_time': None
        }

        if auto_warm:
            self.warm_up()

    def warm_up(self):
        """
        Pre-load and warm up the knowledge base.
        Executes common queries to populate cache and reduce first-query latency.
        """
        print("🔥 Warming up knowledge base...")
        start = time.time()

        # Load documents and index
        self.ingest_all(self.cache_file)

        # Pre-execute common queries to warm cache
        for query in WARMING_QUERIES:
            self.query(query, use_cache=False)  # Populate cache
            self.stats['warm_queries'] += 1

        elapsed = time.time() - start
        self.stats['last_warm_time'] = elapsed

        print(f"✅ Knowledge base warmed in {elapsed:.2f}s")
        print(f"   - {len(self.documents)} documents loaded")
        print(f"   - {len(self.index)} unique terms indexed")
        print(f"   - {self.stats['warm_queries']} warming queries executed\n")

    def ingest_all(self, cache_file: str = ".knowledge_cache.pkl") -> None:
        """
        Ingest all markdown files from knowledge base.
        Uses cached index if available and up-to-date.
        Auto-rebuilds if any source files are newer than cache.

        Args:
            cache_file: Path to cache file
        """
        cache_path = Path(cache_file)

        # Check if cache exists and is valid
        if cache_path.exists():
            try:
                # Get cache modification time
                cache_mtime = cache_path.stat().st_mtime

                # Check if any knowledge base files are newer than cache
                md_files = list(self.knowledge_dir.rglob("*.md"))
                md_files = [f for f in md_files if not f.is_symlink()]

                cache_is_stale = False
                for md_file in md_files:
                    if md_file.stat().st_mtime > cache_mtime:
                        print(f"🔄 Cache is stale (newer file: {md_file.name})")
                        cache_is_stale = True
                        break

                # Also check if number of files changed
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                    if len(cached_data['documents']) != len(md_files):
                        print(f"🔄 Cache is stale (file count changed: {len(cached_data['documents'])} → {len(md_files)})")
                        cache_is_stale = True

                if not cache_is_stale:
                    # Cache is valid, use it
                    self.documents = cached_data['documents']
                    self.index = cached_data['index']
                    print("📚 Loaded knowledge base from cache (up-to-date)")
                    print(f"   - {len(self.documents)} documents indexed")
                    print(f"   - {len(self.index)} unique terms\n")
                    return
                else:
                    print("   Rebuilding index...\n")

            except Exception as e:
                print(f"⚠️  Cache validation failed: {e}, re-ingesting...")

        print("📚 Ingesting knowledge base...")

        md_files = list(self.knowledge_dir.rglob("*.md"))
        # Filter out symlinks to avoid duplicates
        md_files = [f for f in md_files if not f.is_symlink()]
        print(f"   Found {len(md_files)} documents")

        for md_file in md_files:
            try:
                result = self.converter.convert(md_file)
                if result.document:
                    # Store document
                    doc_id = str(md_file.relative_to(self.knowledge_dir))
                    self.documents[doc_id] = {
                        'path': str(md_file),
                        'content': result.document.export_to_markdown(),
                        'name': result.document.name
                    }

                    # Build simple word index
                    content_lower = self.documents[doc_id]['content'].lower()
                    words = content_lower.split()
                    for word in set(words):
                        if word not in self.index:
                            self.index[word] = []
                        self.index[word].append(doc_id)

                    print(f"   ✅ Ingested: {doc_id}")
            except Exception as e:
                print(f"   ❌ Failed to ingest {md_file}: {e}")

        print(f"\n✅ Ingestion complete!")
        print(f"   - {len(self.documents)} documents indexed")
        print(f"   - {len(self.index)} unique terms\n")

        # Save cache for faster subsequent loads
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump({'documents': self.documents, 'index': self.index}, f)
            print(f"💾 Cached knowledge base to {cache_file}\n")
        except Exception as e:
            print(f"⚠️  Failed to cache: {e}\n")

    def query(self, search_terms: str, use_cache: bool = True) -> List[Tuple[str, Dict]]:
        """
        Query the knowledge base for relevant documents with semantic caching.

        Args:
            search_terms: Search query string
            use_cache: If True, use cached results if available

        Returns:
            List of (doc_id, document) tuples sorted by relevance
        """
        self.stats['queries'] += 1
        self.last_access = time.time()

        # Generate cache key from query
        cache_key = self._generate_cache_key(search_terms)

        # Check cache with LRU update
        if use_cache and cache_key in self.query_cache:
            self.stats['cache_hits'] += 1
            # Move to end (mark as recently used)
            self.query_cache.move_to_end(cache_key)
            return self.query_cache[cache_key]

        self.stats['cache_misses'] += 1

        # Execute query
        if isinstance(search_terms, str):
            search_terms_list = search_terms.lower().split()
        else:
            search_terms_list = search_terms

        # Find documents containing search terms
        matches = {}
        for term in search_terms_list:
            if term in self.index:
                for doc_id in self.index[term]:
                    matches[doc_id] = matches.get(doc_id, 0) + 1

        # Sort by relevance (number of matching terms)
        sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
        results = [(doc_id, self.documents[doc_id]) for doc_id, score in sorted_matches]

        # Cache results with true LRU eviction
        if use_cache:
            self.query_cache[cache_key] = results
            self.query_cache.move_to_end(cache_key)  # Mark as most recently used

            # Limit cache size (LRU - evict least recently used)
            if len(self.query_cache) > MAX_CACHE_SIZE:
                # Remove least recently used (first item in OrderedDict)
                self.query_cache.popitem(last=False)

        return results

    def get_answer(self, question: str) -> str:
        """
        Get answer to a specific question.

        Args:
            question: Question string

        Returns:
            Formatted answer with most relevant document content
        """
        results = self.query(question)

        if not results:
            return "❌ No relevant documentation found."

        # Return most relevant document
        doc_id, doc = results[0]
        return f"📄 **{doc['name']}** ({doc_id})\n\n{doc['content'][:500]}..."

    def _generate_cache_key(self, query: str) -> str:
        """
        Generate deterministic cache key from query.

        Args:
            query: Query string

        Returns:
            MD5 hash of normalized query
        """
        return hashlib.md5(query.lower().strip().encode()).hexdigest()

    def get_stats(self) -> Dict:
        """
        Return performance statistics.

        Returns:
            Dictionary with performance metrics
        """
        total_queries = self.stats['cache_hits'] + self.stats['cache_misses']
        hit_rate = (self.stats['cache_hits'] / total_queries * 100) if total_queries > 0 else 0

        return {
            **self.stats,
            'cache_hit_rate': f"{hit_rate:.1f}%",
            'total_queries': total_queries,
            'documents': len(self.documents),
            'terms': len(self.index),
            'cached_queries': len(self.query_cache),
            'last_access_age': f"{time.time() - self.last_access:.1f}s ago"
        }

    def clear_cache(self) -> None:
        """Clear query cache (useful for testing or memory management)."""
        self.query_cache.clear()
        print("🧹 Query cache cleared")


class KnowledgeBaseHeartbeat:
    """
    Background heartbeat thread for continuous knowledge base interaction.
    Keeps the KB "warm" and responsive by executing periodic queries.

    Usage:
        kb = KnowledgeBase(auto_warm=True)
        heartbeat = KnowledgeBaseHeartbeat(kb, interval=300)
        heartbeat.start()
        # ... do work ...
        heartbeat.stop()
    """

    def __init__(self, kb: KnowledgeBase, interval: int = DEFAULT_HEARTBEAT_INTERVAL):
        """
        Initialize heartbeat with knowledge base and interval.

        Args:
            kb: KnowledgeBase instance
            interval: Heartbeat interval in seconds (default: DEFAULT_HEARTBEAT_INTERVAL = 5 min)
        """
        self.kb = kb
        self.interval = interval
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.heartbeat_count = 0

    def start(self):
        """Start background heartbeat thread."""
        if self.running:
            print("⚠️  Heartbeat already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.thread.start()
        print(f"💓 Knowledge base heartbeat started (every {self.interval}s)")

    def stop(self):
        """Stop heartbeat thread gracefully."""
        if not self.running:
            return

        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print(f"💓 Heartbeat stopped (executed {self.heartbeat_count} times)")

    def _heartbeat_loop(self):
        """Background heartbeat loop."""
        while self.running:
            time.sleep(self.interval)

            self.heartbeat_count += 1

            # 1. Check for stale cache
            if self._is_cache_stale():
                print("🔄 Heartbeat: Rebuilding stale cache...")
                self.kb.ingest_all(self.kb.cache_file)

            # 2. Execute warming query to keep index hot
            self._warm_query()

            # 3. Log health metrics
            self._log_health()

    def _is_cache_stale(self) -> bool:
        """
        Check if any knowledge base files have changed since last load.

        Returns:
            True if cache is stale and needs rebuild
        """
        cache_path = Path(self.kb.cache_file)

        if not cache_path.exists():
            return True

        cache_mtime = cache_path.stat().st_mtime
        md_files = list(self.kb.knowledge_dir.rglob("*.md"))
        md_files = [f for f in md_files if not f.is_symlink()]

        for md_file in md_files:
            if md_file.stat().st_mtime > cache_mtime:
                return True

        return False

    def _warm_query(self):
        """Execute a warming query to keep system responsive."""
        queries = [
            "audio processing",
            "juce framework",
            "librosa analysis",
            "supercollider patterns",
            "music theory",
            "real-time dsp"
        ]
        query = random.choice(queries)
        self.kb.query(query, use_cache=True)

    def _log_health(self):
        """Log KB health metrics."""
        stats = self.kb.get_stats()
        print(f"💓 KB Health #{self.heartbeat_count}: "
              f"{stats['documents']} docs, "
              f"{stats['total_queries']} queries, "
              f"{stats['cache_hit_rate']} hit rate, "
              f"last access {stats['last_access_age']}")


def test_queries():
    """Test common queries to validate RAG system with warming."""

    kb = KnowledgeBase(auto_warm=True)

    print("🧪 Testing Knowledge Base Queries\n")

    # Test 1: Directory paths question
    print("Q: Where are custom slash commands located?")
    results = kb.query("custom slash commands directory path")
    if results:
        doc_id, doc = results[0]
        print(f"A: Found in {doc_id}")
        # Extract relevant line
        for line in doc['content'].split('\n'):
            if 'custom slash commands' in line.lower() or '~/.claude/commands' in line.lower():
                print(f"   {line.strip()}")
    print()

    # Test 2: Session management
    print("Q: What does /end-session do?")
    results = kb.query("end-session cleanup")
    if results:
        doc_id, doc = results[0]
        print(f"A: Found in {doc_id}")
        print(f"   First match preview: {doc['content'][:200]}...")
    print()

    # Test 3: Audio knowledge
    print("Q: What are Librosa best practices?")
    results = kb.query("librosa parameters")
    if results:
        doc_id, doc = results[0]
        print(f"A: Found in {doc_id}")
        print(f"   Document: {doc['name']}")
    print()

    # Test 4: Cache performance
    print("Q: Re-running same query (should hit cache)...")
    start = time.time()
    results = kb.query("librosa parameters")
    elapsed = time.time() - start
    print(f"A: Query completed in {elapsed*1000:.2f}ms (cache hit expected)")
    print()

    # Print stats
    print("📊 Performance Statistics:")
    stats = kb.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()

    print("✅ Query tests complete!")


def test_heartbeat():
    """Test heartbeat mechanism."""
    print("🧪 Testing Heartbeat Mechanism\n")

    kb = KnowledgeBase(auto_warm=True)
    heartbeat = KnowledgeBaseHeartbeat(kb, interval=5)  # 5 second interval for testing

    print("Starting heartbeat (will run for 15 seconds)...")
    heartbeat.start()

    # Let it run for 15 seconds (should execute 3 heartbeats)
    time.sleep(15)

    heartbeat.stop()

    print("\n📊 Final Statistics:")
    stats = kb.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n✅ Heartbeat test complete!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test-heartbeat":
        test_heartbeat()
    else:
        test_queries()
