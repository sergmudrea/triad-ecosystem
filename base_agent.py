# src/agents/base_agent.py

from abc import ABC, abstractmethod
from uuid import uuid4

from src.core.meta_memory import MetaMemory, MemoryOptimization
from src.core.replicator import ReplicationEngine


class EvolvableAgent(ABC):
    """
    Base class for all evolvable agents (Black, Red, Blue).

    Provides:
    - Subscription to memory optimizations
    - Automatic application of optimizations
    - Local state management
    """

    def __init__(self, agent_id: str, agent_type: str, memory: MetaMemory, replicator: ReplicationEngine):
        self.id = agent_id or str(uuid4())
        self.type = agent_type  # "black", "red", "blue"
        self.memory = memory
        self.replicator = replicator
        self._running = False

        # Subscribe to memory optimizations
        self.replicator.subscribe(self._on_optimization_received)

    async def _on_optimization_received(self, optimization: MemoryOptimization) -> None:
        """Called when a new memory optimization is broadcast."""
        print(f"[{self.type.upper()}:{self.id[:8]}] Received optimization {optimization.id[:8]}")
        await self.apply_optimization_locally(optimization)

    @abstractmethod
    async def apply_optimization_locally(self, optimization: MemoryOptimization) -> None:
        """Apply optimization to local agent state."""
        pass

    @abstractmethod
    async def run(self) -> None:
        """Main agent loop."""
        pass

    async def start(self) -> None:
        """Start the agent."""
        self._running = True
        await self.run()

    async def stop(self) -> None:
        """Stop the agent."""
        self._running = False
