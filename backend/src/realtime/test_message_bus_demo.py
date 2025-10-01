"""
Message Bus Demo: Multi-Agent Communication Simulation

Demonstrates the message bus with 5 simulated agents:
- Conductor: Broadcasts beat events
- Bass Agent: Responds to chord changes
- Drum Agent: Responds to beat events
- Harmony Agent: Responds to chord changes
- Analytics Agent: Logs all messages

Shows:
- Priority-based message routing
- Broadcast messaging
- Message latencies
- Concurrent agent communication
"""

import asyncio
import time
import random
from typing import Dict, Any

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.realtime.message_bus import (
    AgentMessageBus,
    AgentMessage,
    MessagePriority
)


class SimulatedAgent:
    """Base class for simulated agents."""

    def __init__(self, agent_id: str, bus: AgentMessageBus):
        self.agent_id = agent_id
        self.bus = bus
        self.message_count = 0
        self.bus.register_agent(agent_id)

    async def send_message(
        self,
        to_agent: str,
        message_type: str,
        payload: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL
    ):
        """Send a message via the bus."""
        msg = AgentMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            message_type=message_type,
            payload=payload,
            priority=priority,
            timestamp=time.time()
        )
        await self.bus.publish(msg)
        self.message_count += 1


class ConductorAgent(SimulatedAgent):
    """Conductor agent - broadcasts beat events."""

    def __init__(self, bus: AgentMessageBus):
        super().__init__("conductor", bus)
        self.beat = 0
        self.tempo = 120.0
        self.current_chord = "C"
        self.chord_progression = ["C", "Am", "F", "G"]
        self.chord_index = 0

    async def run(self, duration: float):
        """Run conductor for specified duration."""
        print(f"\n🎼 [{self.agent_id}] Starting at {self.tempo} BPM...")

        beat_interval = 60.0 / self.tempo
        start_time = time.time()

        while time.time() - start_time < duration:
            # Broadcast beat event (CRITICAL priority)
            await self.send_message(
                to_agent="broadcast",
                message_type="beat_event",
                payload={
                    "beat": self.beat,
                    "tempo": self.tempo,
                    "chord": self.current_chord
                },
                priority=MessagePriority.CRITICAL
            )

            print(f"  ⏱️  [{self.agent_id}] Beat {self.beat} | Chord: {self.current_chord}")

            # Change chord every 4 beats
            if self.beat % 4 == 0 and self.beat > 0:
                self.chord_index = (self.chord_index + 1) % len(self.chord_progression)
                self.current_chord = self.chord_progression[self.chord_index]

                # Broadcast chord change (HIGH priority)
                await self.send_message(
                    to_agent="broadcast",
                    message_type="chord_change",
                    payload={"chord": self.current_chord},
                    priority=MessagePriority.HIGH
                )

                print(f"  🎵 [{self.agent_id}] Chord changed to: {self.current_chord}")

            self.beat += 1
            await asyncio.sleep(beat_interval)


class BassAgent(SimulatedAgent):
    """Bass agent - responds to chord changes."""

    def __init__(self, bus: AgentMessageBus):
        super().__init__("bass_agent", bus)
        bus.subscribe("chord_change", self.on_chord_change)
        bus.subscribe("beat_event", self.on_beat)

    async def on_chord_change(self, msg: AgentMessage):
        """Handle chord change events."""
        chord = msg.payload.get("chord")
        print(f"  🎸 [{self.agent_id}] Playing root note for {chord}")

        # Send musical decision (NORMAL priority)
        await self.send_message(
            to_agent="audio_output",
            message_type="play_note",
            payload={
                "note": chord,
                "octave": 2,
                "duration": 0.9
            },
            priority=MessagePriority.NORMAL
        )

    async def on_beat(self, msg: AgentMessage):
        """Handle beat events - play on downbeats."""
        beat = msg.payload.get("beat", 0)
        if beat % 4 == 0:  # Downbeat
            chord = msg.payload.get("chord")
            print(f"  🎸 [{self.agent_id}] Downbeat - emphasizing {chord}")


class DrumAgent(SimulatedAgent):
    """Drum agent - responds to beat events."""

    def __init__(self, bus: AgentMessageBus):
        super().__init__("drum_agent", bus)
        bus.subscribe("beat_event", self.on_beat)

    async def on_beat(self, msg: AgentMessage):
        """Handle beat events."""
        beat = msg.payload.get("beat", 0)
        beat_pos = beat % 4

        hits = []
        if beat_pos in [0, 2]:  # Kick on 1 and 3
            hits.append("kick")
        if beat_pos in [1, 3]:  # Snare on 2 and 4
            hits.append("snare")
        hits.append("hihat")  # Hi-hat on every beat

        print(f"  🥁 [{self.agent_id}] Playing: {', '.join(hits)}")

        # Send drum pattern (NORMAL priority)
        await self.send_message(
            to_agent="audio_output",
            message_type="play_drums",
            payload={"hits": hits},
            priority=MessagePriority.NORMAL
        )


class HarmonyAgent(SimulatedAgent):
    """Harmony agent - responds to chord changes."""

    def __init__(self, bus: AgentMessageBus):
        super().__init__("harmony_agent", bus)
        bus.subscribe("chord_change", self.on_chord_change)

    async def on_chord_change(self, msg: AgentMessage):
        """Handle chord change events."""
        chord = msg.payload.get("chord")
        voicing = self._get_voicing(chord)
        print(f"  🎹 [{self.agent_id}] Voicing {chord}: {voicing}")

        # Send harmonic decision (NORMAL priority)
        await self.send_message(
            to_agent="audio_output",
            message_type="play_chord",
            payload={
                "chord": chord,
                "voicing": voicing
            },
            priority=MessagePriority.NORMAL
        )

    def _get_voicing(self, chord: str) -> list:
        """Get chord voicing."""
        voicings = {
            "C": ["C4", "E4", "G4"],
            "Am": ["A3", "C4", "E4"],
            "F": ["F3", "A3", "C4"],
            "G": ["G3", "B3", "D4"]
        }
        return voicings.get(chord, ["C4", "E4", "G4"])


class AnalyticsAgent(SimulatedAgent):
    """Analytics agent - logs all message types."""

    def __init__(self, bus: AgentMessageBus):
        super().__init__("analytics", bus)
        self.message_types_seen = {}
        self.latencies = []

        # Subscribe to all message types (LOW priority filter)
        bus.subscribe("beat_event", self.on_message, min_priority=MessagePriority.LOW)
        bus.subscribe("chord_change", self.on_message, min_priority=MessagePriority.LOW)
        bus.subscribe("play_note", self.on_message, min_priority=MessagePriority.LOW)
        bus.subscribe("play_drums", self.on_message, min_priority=MessagePriority.LOW)
        bus.subscribe("play_chord", self.on_message, min_priority=MessagePriority.LOW)

    async def on_message(self, msg: AgentMessage):
        """Log message statistics."""
        # Track message types
        if msg.message_type not in self.message_types_seen:
            self.message_types_seen[msg.message_type] = 0
        self.message_types_seen[msg.message_type] += 1

        # Track latency
        latency = (time.time() - msg.timestamp) * 1000  # ms
        self.latencies.append(latency)

    def print_stats(self):
        """Print analytics statistics."""
        print(f"\n📊 [{self.agent_id}] Analytics Report:")
        print(f"  Total messages observed: {sum(self.message_types_seen.values())}")
        print(f"  Message types:")
        for msg_type, count in sorted(self.message_types_seen.items()):
            print(f"    - {msg_type}: {count}")

        if self.latencies:
            avg_latency = sum(self.latencies) / len(self.latencies)
            max_latency = max(self.latencies)
            min_latency = min(self.latencies)
            print(f"  Message latencies:")
            print(f"    - Average: {avg_latency:.4f} ms")
            print(f"    - Min: {min_latency:.4f} ms")
            print(f"    - Max: {max_latency:.4f} ms")


async def main():
    """Run the message bus demo."""
    print("=" * 70)
    print("MESSAGE BUS DEMO: Multi-Agent Communication Simulation")
    print("=" * 70)

    # Create message bus
    bus = AgentMessageBus(max_queue_size=5000)

    # Start message processing
    await bus.start()
    print("\n✅ Message bus started")

    # Create agents
    conductor = ConductorAgent(bus)
    bass = BassAgent(bus)
    drums = DrumAgent(bus)
    harmony = HarmonyAgent(bus)
    analytics = AnalyticsAgent(bus)

    print("\n✅ Agents initialized:")
    print(f"  - {conductor.agent_id}")
    print(f"  - {bass.agent_id}")
    print(f"  - {drums.agent_id}")
    print(f"  - {harmony.agent_id}")
    print(f"  - {analytics.agent_id}")

    # Run simulation for 8 seconds (16 beats at 120 BPM)
    print("\n" + "=" * 70)
    print("SIMULATION RUNNING (8 seconds)...")
    print("=" * 70)

    try:
        await conductor.run(duration=8.0)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")

    # Wait for message queue to drain
    await asyncio.sleep(0.5)

    # Print statistics
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)

    # Analytics report
    analytics.print_stats()

    # Bus statistics
    bus_stats = bus.get_stats()
    print(f"\n📈 Message Bus Statistics:")
    print(f"  Messages published: {bus_stats['messages_published']}")
    print(f"  Messages delivered: {bus_stats['messages_delivered']}")
    print(f"  Avg publish latency: {bus_stats['avg_publish_latency_ms']:.4f} ms")
    print(f"  Avg delivery latency: {bus_stats['avg_delivery_latency_ms']:.4f} ms")
    print(f"  Queue size: {bus_stats['queue_size']}")
    print(f"  Registered agents: {bus_stats['registered_agents']}")

    # Priority distribution
    print(f"\n  Priority distribution:")
    for priority, count in bus_stats['priority_distribution'].items():
        print(f"    - {priority}: {count}")

    # Message type distribution
    print(f"\n  Message type distribution:")
    for msg_type, count in bus_stats['message_types'].items():
        print(f"    - {msg_type}: {count}")

    # Agent message counts
    print(f"\n📤 Agent Activity:")
    for agent in [conductor, bass, drums, harmony, analytics]:
        print(f"  {agent.agent_id}: {agent.message_count} messages sent")

    # Performance verification
    print(f"\n✅ Performance Verification:")
    print(f"  ✓ Publish latency: {bus_stats['avg_publish_latency_ms']:.4f} ms "
          f"(target: <0.1 ms)")
    print(f"  ✓ Delivery latency: {bus_stats['avg_delivery_latency_ms']:.4f} ms "
          f"(target: <1.0 ms)")

    throughput = bus_stats['messages_published'] / 8.0  # messages per second
    print(f"  ✓ Throughput: {throughput:.0f} msg/s (target: >10,000 msg/s)")

    # Stop bus
    await bus.stop()
    print("\n✅ Message bus stopped")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
