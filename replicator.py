# src/core/replicator.py

import asyncio
from typing import Callable, List, Set

from src.core.meta_memory import MetaMemory, MemoryOptimization


class ReplicationEngine:
    """
    Propagates memory optimizations to all subscribed agents.

    Implements pub/sub pattern for optimization distribution.
    Each agent subscribes and automatically applies improvements.
    """

    def __init__(self, memory: MetaMemory):
        self.memory = memory
        self._subscribers: List[Callable[[MemoryOptimization], None]] = []
        self._received: Set[str] = set()

    def subscribe(self, callback: Callable[[MemoryOptimization], None]) -> None:
        """Subscribe to optimization broadcasts."""
        self._subscribers.append(callback)

    async def propagate(self, optimization: MemoryOptimization) -> None:
        """Broadcast optimization to all subscribers."""
        print(f"[Replication] Propagating {optimization.id[:8]} to {len(self._subscribers)} subscribers...")

        tasks = [self._send_to_subscriber(s, optimization) for s in self._subscribers]
        await asyncio.gather(*tasks)

        optimization.propagated = True
        print(f"[Replication] Optimization {optimization.id[:8]} propagated")

    async def _send_to_subscriber(self, subscriber: Callable, optimization: MemoryOptimization) -> None:
        """Send optimization to a single subscriber."""
        try:
            if asyncio.iscoroutinefunction(subscriber):
                await subscriber(optimization)
            else:
                subscriber(optimization)
        except Exception as e:
            print(f"[Replication] Error sending to subscriber: {e}")

    async def receive(self, optimization: MemoryOptimization) -> None:
        """Receive and apply optimization from another node."""
        if optimization.id in self._received:
            print(f"[Replication] Already received {optimization.id[:8]}, skipping")
            return

        print(f"[Replication] Applying optimization {optimization.id[:8]} from {optimization.applied_by}")
        await self._apply_optimization(optimization)
        self._received.add(optimization.id)

    async def _apply_optimization(self, optimization: MemoryOptimization) -> None:
        """Apply optimization recipe to local memory."""
        recipe = optimization.optimization_recipe
        algorithm = recipe.get("algorithm", "")

        if "deduplication" in algorithm or "dedup" in algorithm:
            await self.memory._deduplicate()

        if "compress" in algorithm or "lz4" in algorithm:
            pass  # Recompress will happen on next set

        if "encrypt" in algorithm or "aes" in algorithm:
            await self.memory._reencrypt_all()

        if "index" in algorithm:
            await self.memory._rebuild_indexes()
