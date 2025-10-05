#!/usr/bin/env python3
"""
Knowledge Base Service Startup Script
Launches KB with warming and heartbeat for continuous availability

Usage:
    python scripts/start_kb_service.py [--interval SECONDS]

Options:
    --interval: Heartbeat interval in seconds (default: 300)
"""

import sys
import signal
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from knowledge_rag_v2 import KnowledgeBase, KnowledgeBaseHeartbeat
import argparse
import time


def signal_handler(sig, frame):
    """Handle graceful shutdown on SIGINT/SIGTERM."""
    print("\n\n🛑 Shutdown signal received...")
    if 'heartbeat' in globals():
        heartbeat.stop()
    print("✅ Knowledge Base service stopped cleanly")
    sys.exit(0)


def main():
    """Start KB service with warming and heartbeat."""
    parser = argparse.ArgumentParser(description='Knowledge Base Service')
    parser.add_argument('--interval', type=int, default=300,
                        help='Heartbeat interval in seconds (default: 300)')
    parser.add_argument('--no-heartbeat', action='store_true',
                        help='Disable heartbeat (only warm on startup)')
    args = parser.parse_args()

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("=" * 60)
    print("🚀 Knowledge Base Service Starting")
    print("=" * 60)
    print()

    # Initialize Knowledge Base with auto-warming
    kb = KnowledgeBase(auto_warm=True)

    print()
    print("=" * 60)
    print("✅ Knowledge Base Ready")
    print("=" * 60)
    print()

    # Print initial stats
    stats = kb.get_stats()
    print("📊 Initial Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    print()

    if not args.no_heartbeat:
        # Start heartbeat
        global heartbeat
        heartbeat = KnowledgeBaseHeartbeat(kb, interval=args.interval)
        heartbeat.start()

        print(f"🔄 Service running... (Ctrl+C to stop)")
        print(f"   Heartbeat interval: {args.interval}s")
        print()

        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(None, None)
    else:
        print("✅ KB warmed and ready (no heartbeat)")
        print("   Knowledge base is loaded in memory for this session")


if __name__ == "__main__":
    main()
