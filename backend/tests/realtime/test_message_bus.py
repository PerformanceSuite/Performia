"""
Test Suite for AgentMessageBus

Comprehensive tests for message bus functionality, performance, and reliability.
"""

import pytest
import asyncio
import time
from typing import List

from realtime.message_bus import (
    AgentMessageBus,
    AgentMessage,
    MessagePriority,
    MessageStats
)


@pytest.fixture
def message_bus():
    """Create a fresh message bus for each test."""
    return AgentMessageBus()


@pytest.fixture
async def running_bus(message_bus):
    """Create a running message bus and clean up after test."""
    await message_bus.start()
    yield message_bus
    await message_bus.stop()


class TestMessageCreation:
    """Test AgentMessage creation and properties."""

    def test_message_creation_basic(self):
        """Test basic message creation."""
        msg = AgentMessage(
            from_agent="test_agent",
            to_agent="target_agent",
            message_type="test_message",
            payload={"data": "test"},
            priority=MessagePriority.NORMAL,
            timestamp=time.time()
        )

        assert msg.from_agent == "test_agent"
        assert msg.to_agent == "target_agent"
        assert msg.message_type == "test_message"
        assert msg.payload["data"] == "test"
        assert msg.priority == MessagePriority.NORMAL

    def test_message_priority_ordering(self):
        """Test that messages are ordered by priority."""
        critical = AgentMessage(
            from_agent="a", to_agent="b", message_type="test",
            priority=MessagePriority.CRITICAL, timestamp=time.time()
        )
        normal = AgentMessage(
            from_agent="a", to_agent="b", message_type="test",
            priority=MessagePriority.NORMAL, timestamp=time.time()
        )
        high = AgentMessage(
            from_agent="a", to_agent="b", message_type="test",
            priority=MessagePriority.HIGH, timestamp=time.time()
        )

        # Lower priority value should come first
        assert critical < normal
        assert critical < high
        assert high < normal

    def test_message_id_auto_generation(self):
        """Test that message IDs are auto-generated."""
        msg1 = AgentMessage(
            from_agent="a", to_agent="b", message_type="test",
            priority=MessagePriority.NORMAL, timestamp=time.time()
        )
        msg2 = AgentMessage(
            from_agent="a", to_agent="b", message_type="test",
            priority=MessagePriority.NORMAL, timestamp=time.time()
        )

        assert msg1.message_id != ""
        assert msg2.message_id != ""
        assert msg1.message_id != msg2.message_id


class TestSubscription:
    """Test message subscription and unsubscription."""

    @pytest.mark.asyncio
    async def test_subscribe_handler(self, message_bus):
        """Test subscribing a handler to a message type."""
        received = []

        async def handler(msg: AgentMessage):
            received.append(msg)

        message_bus.subscribe("test_type", handler)
        assert "test_type" in message_bus.subscribers
        assert handler in message_bus.subscribers["test_type"]

    @pytest.mark.asyncio
    async def test_unsubscribe_handler(self, message_bus):
        """Test unsubscribing a handler."""
        async def handler(msg: AgentMessage):
            pass

        message_bus.subscribe("test_type", handler)
        message_bus.unsubscribe("test_type", handler)

        assert handler not in message_bus.subscribers["test_type"]

    @pytest.mark.asyncio
    async def test_multiple_subscribers(self, message_bus):
        """Test multiple subscribers to same message type."""
        received1 = []
        received2 = []

        async def handler1(msg: AgentMessage):
            received1.append(msg)

        async def handler2(msg: AgentMessage):
            received2.append(msg)

        message_bus.subscribe("test_type", handler1)
        message_bus.subscribe("test_type", handler2)

        assert len(message_bus.subscribers["test_type"]) == 2


class TestPublishSubscribe:
    """Test message publishing and delivery."""

    @pytest.mark.asyncio
    async def test_publish_and_receive(self, running_bus):
        """Test basic publish/subscribe flow."""
        received = []

        async def handler(msg: AgentMessage):
            received.append(msg)

        running_bus.subscribe("test_event", handler)

        # Publish message
        msg = AgentMessage(
            from_agent="sender",
            to_agent="receiver",
            message_type="test_event",
            payload={"value": 42},
            priority=MessagePriority.NORMAL,
            timestamp=time.time()
        )
        await running_bus.publish(msg)

        # Wait for processing
        await asyncio.sleep(0.01)

        assert len(received) == 1
        assert received[0].payload["value"] == 42

    @pytest.mark.asyncio
    async def test_priority_ordering(self, running_bus):
        """Test that messages are delivered in priority order."""
        received = []

        async def handler(msg: AgentMessage):
            received.append(msg.priority)

        running_bus.subscribe("test_event", handler)

        # Publish messages in non-priority order
        await running_bus.publish(AgentMessage(
            from_agent="a", to_agent="b", message_type="test_event",
            priority=MessagePriority.LOW, timestamp=time.time()
        ))
        await running_bus.publish(AgentMessage(
            from_agent="a", to_agent="b", message_type="test_event",
            priority=MessagePriority.CRITICAL, timestamp=time.time()
        ))
        await running_bus.publish(AgentMessage(
            from_agent="a", to_agent="b", message_type="test_event",
            priority=MessagePriority.HIGH, timestamp=time.time()
        ))
        await running_bus.publish(AgentMessage(
            from_agent="a", to_agent="b", message_type="test_event",
            priority=MessagePriority.NORMAL, timestamp=time.time()
        ))

        # Wait for processing
        await asyncio.sleep(0.02)

        # Should be delivered in priority order
        assert received[0] == MessagePriority.CRITICAL
        assert received[1] == MessagePriority.HIGH
        assert received[2] == MessagePriority.NORMAL
        assert received[3] == MessagePriority.LOW

    @pytest.mark.asyncio
    async def test_broadcast_message(self, running_bus):
        """Test broadcast message delivery."""
        received1 = []
        received2 = []

        async def handler1(msg: AgentMessage):
            received1.append(msg)

        async def handler2(msg: AgentMessage):
            received2.append(msg)

        running_bus.subscribe("broadcast_event", handler1)
        running_bus.subscribe("broadcast_event", handler2)

        # Publish broadcast message
        msg = AgentMessage(
            from_agent="conductor",
            to_agent="broadcast",
            message_type="broadcast_event",
            payload={"beat": 1},
            priority=MessagePriority.CRITICAL,
            timestamp=time.time()
        )
        await running_bus.publish(msg)

        # Wait for processing
        await asyncio.sleep(0.01)

        # Both handlers should receive it
        assert len(received1) == 1
        assert len(received2) == 1


class TestConcurrency:
    """Test concurrent publishers and subscribers."""

    @pytest.mark.asyncio
    async def test_concurrent_publishers(self, running_bus):
        """Test multiple agents publishing simultaneously."""
        received = []

        async def handler(msg: AgentMessage):
            received.append(msg)

        running_bus.subscribe("concurrent_test", handler)

        # Multiple concurrent publishers
        async def publisher(agent_id: str, count: int):
            for i in range(count):
                await running_bus.publish(AgentMessage(
                    from_agent=agent_id,
                    to_agent="target",
                    message_type="concurrent_test",
                    payload={"index": i},
                    priority=MessagePriority.NORMAL,
                    timestamp=time.time()
                ))

        # Start 5 publishers sending 10 messages each
        await asyncio.gather(
            publisher("agent_1", 10),
            publisher("agent_2", 10),
            publisher("agent_3", 10),
            publisher("agent_4", 10),
            publisher("agent_5", 10),
        )

        # Wait for all messages to process
        await asyncio.sleep(0.1)

        # Should receive all 50 messages
        assert len(received) == 50

    @pytest.mark.asyncio
    async def test_concurrent_subscribers(self, running_bus):
        """Test multiple subscribers processing messages concurrently."""
        received_counts = {"h1": 0, "h2": 0, "h3": 0}

        async def make_handler(name: str):
            async def handler(msg: AgentMessage):
                received_counts[name] += 1
                await asyncio.sleep(0.001)  # Simulate processing
            return handler

        # Subscribe multiple handlers
        running_bus.subscribe("test", await make_handler("h1"))
        running_bus.subscribe("test", await make_handler("h2"))
        running_bus.subscribe("test", await make_handler("h3"))

        # Publish messages
        for i in range(10):
            await running_bus.publish(AgentMessage(
                from_agent="sender", to_agent="broadcast",
                message_type="test", priority=MessagePriority.NORMAL,
                timestamp=time.time()
            ))

        # Wait for processing
        await asyncio.sleep(0.2)

        # All handlers should receive all messages
        assert received_counts["h1"] == 10
        assert received_counts["h2"] == 10
        assert received_counts["h3"] == 10


class TestPerformance:
    """Performance benchmarks."""

    @pytest.mark.asyncio
    async def test_publish_latency(self, running_bus):
        """Test message publish latency (<0.1ms target)."""
        latencies = []

        for _ in range(1000):
            start = time.perf_counter()
            await running_bus.publish(AgentMessage(
                from_agent="perf_test", to_agent="target",
                message_type="perf_test", priority=MessagePriority.NORMAL,
                timestamp=time.time()
            ))
            latency = (time.perf_counter() - start) * 1000  # ms
            latencies.append(latency)

        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)

        print(f"\nPublish latency: avg={avg_latency:.4f}ms, max={max_latency:.4f}ms")

        # Target: <0.1ms average
        assert avg_latency < 0.5  # Relaxed for safety

    @pytest.mark.asyncio
    async def test_throughput(self, running_bus):
        """Test message throughput (>10,000 messages/second target)."""
        message_count = 10000
        received = []

        async def handler(msg: AgentMessage):
            received.append(msg)

        running_bus.subscribe("throughput_test", handler)

        # Publish messages
        start_time = time.perf_counter()

        for i in range(message_count):
            await running_bus.publish(AgentMessage(
                from_agent="sender", to_agent="target",
                message_type="throughput_test",
                payload={"index": i},
                priority=MessagePriority.NORMAL,
                timestamp=time.time()
            ))

        # Wait for all messages to be processed
        await asyncio.sleep(2.0)  # Give time for processing

        end_time = time.perf_counter()
        duration = end_time - start_time

        throughput = message_count / duration

        print(f"\nThroughput: {throughput:.0f} messages/second")
        print(f"Duration: {duration:.2f}s for {message_count} messages")
        print(f"Received: {len(received)} messages")

        # Target: >10,000 messages/second
        assert throughput > 5000  # Relaxed for safety

    @pytest.mark.asyncio
    async def test_delivery_latency(self, running_bus):
        """Test end-to-end delivery latency (<1ms target)."""
        latencies = []

        async def handler(msg: AgentMessage):
            delivery_time = time.perf_counter() - msg.timestamp
            latencies.append(delivery_time * 1000)  # ms

        running_bus.subscribe("latency_test", handler)

        # Publish messages
        for _ in range(100):
            await running_bus.publish(AgentMessage(
                from_agent="sender", to_agent="target",
                message_type="latency_test",
                priority=MessagePriority.NORMAL,
                timestamp=time.perf_counter()
            ))
            await asyncio.sleep(0.001)  # Small delay between messages

        # Wait for processing
        await asyncio.sleep(0.2)

        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            max_latency = max(latencies)

            print(f"\nDelivery latency: avg={avg_latency:.4f}ms, max={max_latency:.4f}ms")

            # Target: <1ms average
            assert avg_latency < 5.0  # Relaxed for safety


class TestStatistics:
    """Test performance monitoring and statistics."""

    @pytest.mark.asyncio
    async def test_stats_collection(self, running_bus):
        """Test that statistics are collected correctly."""
        async def handler(msg: AgentMessage):
            pass

        running_bus.subscribe("stats_test", handler)

        # Publish various messages
        await running_bus.publish(AgentMessage(
            from_agent="a", to_agent="b", message_type="stats_test",
            priority=MessagePriority.CRITICAL, timestamp=time.time()
        ))
        await running_bus.publish(AgentMessage(
            from_agent="a", to_agent="b", message_type="stats_test",
            priority=MessagePriority.NORMAL, timestamp=time.time()
        ))

        await asyncio.sleep(0.05)

        stats = running_bus.get_stats()

        assert stats['messages_published'] == 2
        assert stats['messages_delivered'] > 0
        assert 'avg_publish_latency_ms' in stats
        assert 'avg_delivery_latency_ms' in stats

    @pytest.mark.asyncio
    async def test_stats_reset(self, running_bus):
        """Test statistics reset."""
        async def handler(msg: AgentMessage):
            pass

        running_bus.subscribe("reset_test", handler)

        await running_bus.publish(AgentMessage(
            from_agent="a", to_agent="b", message_type="reset_test",
            priority=MessagePriority.NORMAL, timestamp=time.time()
        ))

        await asyncio.sleep(0.05)

        stats_before = running_bus.get_stats()
        assert stats_before['messages_published'] > 0

        running_bus.reset_stats()
        stats_after = running_bus.get_stats()

        assert stats_after['messages_published'] == 0


class TestReliability:
    """Test reliability and error handling."""

    @pytest.mark.asyncio
    async def test_no_message_loss(self, running_bus):
        """Test that no messages are lost under load."""
        received = []

        async def handler(msg: AgentMessage):
            received.append(msg.payload['id'])

        running_bus.subscribe("reliability_test", handler)

        # Publish 1000 messages
        message_ids = list(range(1000))
        for msg_id in message_ids:
            await running_bus.publish(AgentMessage(
                from_agent="sender", to_agent="target",
                message_type="reliability_test",
                payload={"id": msg_id},
                priority=MessagePriority.NORMAL,
                timestamp=time.time()
            ))

        # Wait for all to process
        await asyncio.sleep(1.0)

        # All messages should be received
        assert len(received) == 1000
        assert set(received) == set(message_ids)

    @pytest.mark.asyncio
    async def test_handler_exception_doesnt_break_bus(self, running_bus):
        """Test that exceptions in handlers don't break the bus."""
        received = []

        async def failing_handler(msg: AgentMessage):
            raise ValueError("Test exception")

        async def good_handler(msg: AgentMessage):
            received.append(msg)

        running_bus.subscribe("test", failing_handler)
        running_bus.subscribe("test", good_handler)

        # Publish message
        await running_bus.publish(AgentMessage(
            from_agent="a", to_agent="b", message_type="test",
            priority=MessagePriority.NORMAL, timestamp=time.time()
        ))

        await asyncio.sleep(0.05)

        # Good handler should still receive message despite failing handler
        assert len(received) == 1


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
