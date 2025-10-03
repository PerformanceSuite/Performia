"""
Message Bus Validation Suite

Comprehensive validation tests that can be run directly without pytest.
Tests all critical functionality and performance targets.
"""

import asyncio
import time
import sys
from typing import List

from message_bus import (
    AgentMessageBus,
    AgentMessage,
    MessagePriority,
    MessageStats
)


class ValidationSuite:
    """Test suite for message bus validation."""

    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0

    def assert_equal(self, actual, expected, test_name):
        """Assert equality."""
        self.tests_run += 1
        if actual == expected:
            self.tests_passed += 1
            print(f"  ✅ {test_name}")
            return True
        else:
            self.tests_failed += 1
            print(f"  ❌ {test_name}: expected {expected}, got {actual}")
            return False

    def assert_true(self, condition, test_name):
        """Assert condition is true."""
        self.tests_run += 1
        if condition:
            self.tests_passed += 1
            print(f"  ✅ {test_name}")
            return True
        else:
            self.tests_failed += 1
            print(f"  ❌ {test_name}: condition failed")
            return False

    def assert_less(self, actual, threshold, test_name):
        """Assert actual < threshold."""
        self.tests_run += 1
        if actual < threshold:
            self.tests_passed += 1
            print(f"  ✅ {test_name}: {actual} < {threshold}")
            return True
        else:
            self.tests_failed += 1
            print(f"  ❌ {test_name}: {actual} >= {threshold}")
            return False

    def assert_greater(self, actual, threshold, test_name):
        """Assert actual > threshold."""
        self.tests_run += 1
        if actual > threshold:
            self.tests_passed += 1
            print(f"  ✅ {test_name}: {actual} > {threshold}")
            return True
        else:
            self.tests_failed += 1
            print(f"  ❌ {test_name}: {actual} <= {threshold}")
            return False

    def print_summary(self):
        """Print test summary."""
        print(f"\n{'='*70}")
        print(f"TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Tests run: {self.tests_run}")
        print(f"Tests passed: {self.tests_passed} ✅")
        print(f"Tests failed: {self.tests_failed} {'❌' if self.tests_failed > 0 else ''}")
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"Success rate: {success_rate:.1f}%")
        print(f"{'='*70}\n")
        return self.tests_failed == 0


async def test_message_creation(suite: ValidationSuite):
    """Test message creation and properties."""
    print("\n🧪 Test: Message Creation")

    msg = AgentMessage(
        from_agent="test_agent",
        to_agent="target_agent",
        message_type="test_message",
        payload={"data": "test"},
        priority=MessagePriority.NORMAL,
        timestamp=time.time()
    )

    suite.assert_equal(msg.from_agent, "test_agent", "from_agent set correctly")
    suite.assert_equal(msg.to_agent, "target_agent", "to_agent set correctly")
    suite.assert_equal(msg.message_type, "test_message", "message_type set correctly")
    suite.assert_equal(msg.payload["data"], "test", "payload set correctly")
    suite.assert_true(msg.message_id != "", "message_id auto-generated")


async def test_message_priority_ordering(suite: ValidationSuite):
    """Test message priority ordering."""
    print("\n🧪 Test: Message Priority Ordering")

    critical = AgentMessage(
        from_agent="a", to_agent="b", message_type="test",
        priority=MessagePriority.CRITICAL, timestamp=time.time()
    )
    high = AgentMessage(
        from_agent="a", to_agent="b", message_type="test",
        priority=MessagePriority.HIGH, timestamp=time.time()
    )
    normal = AgentMessage(
        from_agent="a", to_agent="b", message_type="test",
        priority=MessagePriority.NORMAL, timestamp=time.time()
    )
    low = AgentMessage(
        from_agent="a", to_agent="b", message_type="test",
        priority=MessagePriority.LOW, timestamp=time.time()
    )

    suite.assert_true(critical < high, "CRITICAL < HIGH")
    suite.assert_true(high < normal, "HIGH < NORMAL")
    suite.assert_true(normal < low, "NORMAL < LOW")


async def test_publish_subscribe(suite: ValidationSuite):
    """Test basic publish/subscribe."""
    print("\n🧪 Test: Publish/Subscribe")

    bus = AgentMessageBus()
    received = []

    async def handler(msg: AgentMessage):
        received.append(msg)

    bus.subscribe("test_event", handler)
    await bus.start()

    msg = AgentMessage(
        from_agent="sender",
        to_agent="receiver",
        message_type="test_event",
        payload={"value": 42},
        priority=MessagePriority.NORMAL,
        timestamp=time.time()
    )
    await bus.publish(msg)
    await asyncio.sleep(0.05)

    suite.assert_equal(len(received), 1, "Message received")
    suite.assert_equal(received[0].payload["value"], 42, "Payload correct")

    await bus.stop()


async def test_priority_delivery(suite: ValidationSuite):
    """Test messages delivered in priority order."""
    print("\n🧪 Test: Priority-Based Delivery")

    bus = AgentMessageBus()
    received_priorities = []

    async def handler(msg: AgentMessage):
        received_priorities.append(msg.priority)

    bus.subscribe("test_event", handler)
    await bus.start()

    # Publish in non-priority order
    await bus.publish(AgentMessage(
        from_agent="a", to_agent="b", message_type="test_event",
        priority=MessagePriority.LOW, timestamp=time.time()
    ))
    await bus.publish(AgentMessage(
        from_agent="a", to_agent="b", message_type="test_event",
        priority=MessagePriority.CRITICAL, timestamp=time.time()
    ))
    await bus.publish(AgentMessage(
        from_agent="a", to_agent="b", message_type="test_event",
        priority=MessagePriority.HIGH, timestamp=time.time()
    ))

    await asyncio.sleep(0.05)

    suite.assert_equal(received_priorities[0], MessagePriority.CRITICAL, "CRITICAL delivered first")
    suite.assert_equal(received_priorities[1], MessagePriority.HIGH, "HIGH delivered second")
    suite.assert_equal(received_priorities[2], MessagePriority.LOW, "LOW delivered last")

    await bus.stop()


async def test_broadcast(suite: ValidationSuite):
    """Test broadcast messaging."""
    print("\n🧪 Test: Broadcast Messaging")

    bus = AgentMessageBus()
    received1 = []
    received2 = []

    async def handler1(msg: AgentMessage):
        received1.append(msg)

    async def handler2(msg: AgentMessage):
        received2.append(msg)

    bus.subscribe("broadcast_event", handler1)
    bus.subscribe("broadcast_event", handler2)
    await bus.start()

    msg = AgentMessage(
        from_agent="conductor",
        to_agent="broadcast",
        message_type="broadcast_event",
        payload={"beat": 1},
        priority=MessagePriority.CRITICAL,
        timestamp=time.time()
    )
    await bus.publish(msg)
    await asyncio.sleep(0.05)

    suite.assert_equal(len(received1), 1, "Handler 1 received broadcast")
    suite.assert_equal(len(received2), 1, "Handler 2 received broadcast")

    await bus.stop()


async def test_concurrent_publishers(suite: ValidationSuite):
    """Test concurrent publishers."""
    print("\n🧪 Test: Concurrent Publishers")

    bus = AgentMessageBus()
    received = []

    async def handler(msg: AgentMessage):
        received.append(msg)

    bus.subscribe("concurrent_test", handler)
    await bus.start()

    async def publisher(agent_id: str, count: int):
        for i in range(count):
            await bus.publish(AgentMessage(
                from_agent=agent_id,
                to_agent="target",
                message_type="concurrent_test",
                payload={"index": i},
                priority=MessagePriority.NORMAL,
                timestamp=time.time()
            ))

    # 5 publishers, 10 messages each = 50 total
    await asyncio.gather(
        publisher("agent_1", 10),
        publisher("agent_2", 10),
        publisher("agent_3", 10),
        publisher("agent_4", 10),
        publisher("agent_5", 10),
    )

    await asyncio.sleep(0.2)

    suite.assert_equal(len(received), 50, "All 50 messages received")

    await bus.stop()


async def test_throughput(suite: ValidationSuite):
    """Test message throughput."""
    print("\n🧪 Test: Throughput Performance")

    bus = AgentMessageBus(max_queue_size=15000)
    received = []

    async def handler(msg: AgentMessage):
        received.append(msg)

    bus.subscribe("throughput_test", handler)
    await bus.start()

    message_count = 10000
    start_time = time.perf_counter()

    for i in range(message_count):
        await bus.publish(AgentMessage(
            from_agent="sender",
            to_agent="target",
            message_type="throughput_test",
            payload={"index": i},
            priority=MessagePriority.NORMAL,
            timestamp=time.time()
        ))

    publish_duration = time.perf_counter() - start_time
    await asyncio.sleep(2.0)  # Allow processing

    stats = bus.get_stats()
    throughput = stats['messages_published'] / publish_duration

    suite.assert_equal(stats['messages_published'], message_count, f"Published {message_count} messages")
    suite.assert_greater(throughput, 5000, "Throughput > 5,000 msg/s")

    print(f"    Throughput: {throughput:.0f} messages/second")

    await bus.stop()


async def test_latency(suite: ValidationSuite):
    """Test message latency."""
    print("\n🧪 Test: Latency Performance")

    bus = AgentMessageBus()
    await bus.start()

    # Publish latency test
    latencies = []
    for _ in range(100):
        start = time.perf_counter()
        await bus.publish(AgentMessage(
            from_agent="sender", to_agent="target",
            message_type="latency_test", priority=MessagePriority.NORMAL,
            timestamp=time.time()
        ))
        latency = (time.perf_counter() - start) * 1000  # ms
        latencies.append(latency)

    avg_publish_latency = sum(latencies) / len(latencies)
    suite.assert_less(avg_publish_latency, 0.5, "Avg publish latency < 0.5ms")

    print(f"    Avg publish latency: {avg_publish_latency:.4f} ms")

    await asyncio.sleep(0.1)

    stats = bus.get_stats()
    suite.assert_less(stats['avg_delivery_latency_ms'], 5.0, "Avg delivery latency < 5ms")

    print(f"    Avg delivery latency: {stats['avg_delivery_latency_ms']:.4f} ms")

    await bus.stop()


async def test_no_message_loss(suite: ValidationSuite):
    """Test no messages are lost."""
    print("\n🧪 Test: Message Reliability (No Loss)")

    bus = AgentMessageBus()
    received_ids = []

    async def handler(msg: AgentMessage):
        received_ids.append(msg.payload['id'])

    bus.subscribe("reliability_test", handler)
    await bus.start()

    message_ids = list(range(1000))
    for msg_id in message_ids:
        await bus.publish(AgentMessage(
            from_agent="sender",
            to_agent="target",
            message_type="reliability_test",
            payload={"id": msg_id},
            priority=MessagePriority.NORMAL,
            timestamp=time.time()
        ))

    await asyncio.sleep(1.0)

    suite.assert_equal(len(received_ids), 1000, "All 1000 messages received")
    suite.assert_equal(set(received_ids), set(message_ids), "All message IDs present")

    await bus.stop()


async def main():
    """Run all validation tests."""
    print("="*70)
    print("MESSAGE BUS VALIDATION SUITE")
    print("="*70)

    suite = ValidationSuite()

    # Run all tests
    await test_message_creation(suite)
    await test_message_priority_ordering(suite)
    await test_publish_subscribe(suite)
    await test_priority_delivery(suite)
    await test_broadcast(suite)
    await test_concurrent_publishers(suite)
    await test_throughput(suite)
    await test_latency(suite)
    await test_no_message_loss(suite)

    # Print summary
    all_passed = suite.print_summary()

    if all_passed:
        print("🎉 ALL TESTS PASSED! Message bus is production-ready.")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED. Review failures above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
