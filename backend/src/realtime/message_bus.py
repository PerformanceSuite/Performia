"""
Async Message Bus for Inter-Agent Communication

High-performance message bus using asyncio for real-time agent communication.
Supports priority-based routing, pub/sub patterns, and broadcast messaging.

Performance targets:
- Message publish latency: <0.1ms
- Message delivery latency: <1ms
- Throughput: >10,000 messages/second
- Memory: <10MB for 10,000 queued messages
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set
from enum import IntEnum
import asyncio
import time
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessagePriority(IntEnum):
    """Message priority levels for queue ordering."""
    CRITICAL = 0   # Beat events, timing-critical updates
    HIGH = 1       # Musical decisions, chord changes
    NORMAL = 2     # Context updates, state changes
    LOW = 3        # Logging, analytics, non-critical


@dataclass(order=True)
class AgentMessage:
    """Message passed between agents.

    Uses dataclass ordering based on priority for PriorityQueue.
    The priority field comes first for proper sorting.
    """
    priority: MessagePriority
    timestamp: float = field(compare=False)
    from_agent: str = field(compare=False)
    to_agent: str = field(compare=False)  # or "broadcast" for all agents
    message_type: str = field(compare=False)
    payload: Dict[str, Any] = field(default_factory=dict, compare=False)
    message_id: str = field(default="", compare=False)

    def __post_init__(self):
        """Generate message ID if not provided."""
        if not self.message_id:
            self.message_id = f"{self.from_agent}_{self.timestamp}_{id(self)}"


class MessageStats:
    """Performance monitoring for message bus."""

    def __init__(self):
        self.messages_published = 0
        self.messages_delivered = 0
        self.total_publish_time = 0.0
        self.total_delivery_time = 0.0
        self.message_type_counts: Dict[str, int] = defaultdict(int)
        self.priority_counts: Dict[MessagePriority, int] = defaultdict(int)

    def record_publish(self, message: AgentMessage, duration: float):
        """Record message publish metrics."""
        self.messages_published += 1
        self.total_publish_time += duration
        self.message_type_counts[message.message_type] += 1
        self.priority_counts[message.priority] += 1

    def record_delivery(self, duration: float):
        """Record message delivery metrics."""
        self.messages_delivered += 1
        self.total_delivery_time += duration

    def get_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        return {
            'messages_published': self.messages_published,
            'messages_delivered': self.messages_delivered,
            'avg_publish_latency_ms': (
                (self.total_publish_time / self.messages_published * 1000)
                if self.messages_published > 0 else 0
            ),
            'avg_delivery_latency_ms': (
                (self.total_delivery_time / self.messages_delivered * 1000)
                if self.messages_delivered > 0 else 0
            ),
            'message_types': dict(self.message_type_counts),
            'priority_distribution': {
                p.name: count for p, count in self.priority_counts.items()
            }
        }

    def reset(self):
        """Reset all statistics."""
        self.__init__()


class AgentMessageBus:
    """
    High-performance async message bus for agent communication.

    Features:
    - Priority-based message delivery
    - Type-based pub/sub routing
    - Broadcast messaging to all agents
    - Message filtering by priority
    - Performance monitoring and metrics
    - Non-blocking publish with async processing

    Usage:
        bus = AgentMessageBus()

        # Subscribe to message types
        bus.subscribe("beat_event", beat_handler)
        bus.subscribe("chord_change", chord_handler)

        # Publish messages
        await bus.publish(AgentMessage(
            from_agent="conductor",
            to_agent="bass_agent",
            message_type="chord_change",
            payload={"chord": "Cmaj7"},
            priority=MessagePriority.HIGH,
            timestamp=time.time()
        ))

        # Start processing
        asyncio.create_task(bus.process_messages())
    """

    def __init__(self, max_queue_size: int = 10000):
        """
        Initialize message bus.

        Args:
            max_queue_size: Maximum messages in queue (prevents memory overflow)
        """
        # Priority queue for messages (lower priority value = higher priority)
        self.message_queue: asyncio.PriorityQueue = asyncio.PriorityQueue(
            maxsize=max_queue_size
        )

        # Subscribers by message type
        self.subscribers: Dict[str, List[Callable]] = defaultdict(list)

        # Registered agents for broadcast
        self.registered_agents: Set[str] = set()

        # Performance stats
        self.stats = MessageStats()

        # Control flags
        self.running = False
        self.processing_task: Optional[asyncio.Task] = None

    def register_agent(self, agent_id: str):
        """Register an agent for broadcast messages."""
        self.registered_agents.add(agent_id)
        logger.info(f"Agent registered: {agent_id}")

    def unregister_agent(self, agent_id: str):
        """Unregister an agent from broadcast."""
        self.registered_agents.discard(agent_id)
        logger.info(f"Agent unregistered: {agent_id}")

    def subscribe(
        self,
        message_type: str,
        handler: Callable,
        min_priority: MessagePriority = MessagePriority.LOW
    ):
        """
        Subscribe to a message type.

        Args:
            message_type: Type of message to listen for
            handler: Async function to handle message (receives AgentMessage)
            min_priority: Minimum priority level to receive (filters lower priority)
        """
        # Wrap handler with priority filter if needed
        if min_priority != MessagePriority.LOW:
            original_handler = handler
            async def filtered_handler(message: AgentMessage):
                if message.priority <= min_priority:
                    await original_handler(message)
            handler = filtered_handler

        self.subscribers[message_type].append(handler)
        logger.debug(f"Subscribed to '{message_type}' (min_priority={min_priority.name})")

    def unsubscribe(self, message_type: str, handler: Callable):
        """Unsubscribe a handler from a message type."""
        if message_type in self.subscribers:
            try:
                self.subscribers[message_type].remove(handler)
                logger.debug(f"Unsubscribed from '{message_type}'")
            except ValueError:
                pass

    async def publish(self, message: AgentMessage):
        """
        Publish a message to the bus (non-blocking).

        Args:
            message: AgentMessage to publish

        Raises:
            asyncio.QueueFull: If message queue is full
        """
        start_time = time.perf_counter()

        try:
            # Put message in priority queue (non-blocking)
            self.message_queue.put_nowait(message)

            # Record metrics
            publish_duration = time.perf_counter() - start_time
            self.stats.record_publish(message, publish_duration)

            logger.debug(
                f"Published: {message.from_agent} -> {message.to_agent} "
                f"[{message.message_type}] priority={message.priority.name}"
            )

        except asyncio.QueueFull:
            logger.error(
                f"Message queue full! Dropping message: "
                f"{message.message_type} from {message.from_agent}"
            )
            raise

    async def process_messages(self):
        """
        Process messages from queue in priority order.

        This is the main message processing loop. Should be run as a task:
            asyncio.create_task(bus.process_messages())
        """
        self.running = True
        logger.info("Message bus processing started")

        try:
            while self.running:
                # Get highest priority message
                message = await self.message_queue.get()

                # Record delivery time
                delivery_start = time.perf_counter()

                # Deliver to subscribers
                await self._deliver_message(message)

                # Record delivery metrics
                delivery_duration = time.perf_counter() - delivery_start
                self.stats.record_delivery(delivery_duration)

                # Mark task as done
                self.message_queue.task_done()

        except asyncio.CancelledError:
            logger.info("Message bus processing cancelled")
            raise
        except Exception as e:
            logger.error(f"Error in message processing: {e}", exc_info=True)
            raise
        finally:
            self.running = False

    async def _deliver_message(self, message: AgentMessage):
        """
        Deliver message to appropriate subscribers.

        Handles both direct messages and broadcasts.
        """
        handlers = self.subscribers.get(message.message_type, [])

        if not handlers:
            logger.debug(f"No subscribers for message type: {message.message_type}")
            return

        # Check if broadcast or direct
        if message.to_agent == "broadcast":
            # Deliver to all subscribers
            delivery_tasks = [handler(message) for handler in handlers]
        else:
            # In a more advanced system, we might filter by to_agent
            # For now, all subscribers get the message
            delivery_tasks = [handler(message) for handler in handlers]

        # Execute all handlers concurrently
        if delivery_tasks:
            await asyncio.gather(*delivery_tasks, return_exceptions=True)

    async def start(self):
        """Start the message bus processing task."""
        if not self.running:
            self.processing_task = asyncio.create_task(self.process_messages())

    async def stop(self):
        """Stop the message bus and wait for queue to drain."""
        logger.info("Stopping message bus...")
        self.running = False

        if self.processing_task:
            # Wait for current message to finish
            await asyncio.wait_for(self.message_queue.join(), timeout=5.0)

            # Cancel processing task
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass

        logger.info("Message bus stopped")

    def get_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        return {
            **self.stats.get_stats(),
            'queue_size': self.message_queue.qsize(),
            'registered_agents': len(self.registered_agents),
            'subscriber_types': len(self.subscribers),
            'running': self.running
        }

    def reset_stats(self):
        """Reset performance statistics."""
        self.stats.reset()
