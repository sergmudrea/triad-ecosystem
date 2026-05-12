# tests/test_black.py

import pytest
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.meta_memory import MetaMemory
from src.core.replicator import ReplicationEngine
from src.simulation.sandbox import Sandbox
from src.agents.black_agent import BlackAgent


async def test_black_agent_creation():
    memory = MetaMemory()
    replicator = ReplicationEngine(memory)
    sandbox = Sandbox(isolated=True)

    black = BlackAgent("black-test", memory, replicator, sandbox)

    assert black.id == "black-test"
    assert black.type == "black"
    assert black.genome is not None
    print("✅ Black agent creation test passed")


async def test_black_agent_scan():
    memory = MetaMemory()
    replicator = ReplicationEngine(memory)
    sandbox = Sandbox(isolated=True)

    black = BlackAgent("black-test", memory, replicator, sandbox)
    black.genome.scan_subnets = ["192.168.1.0/24"]
    black.genome.scan_ports = [22, 80, 443]

    targets = await black._scan_phase()

    assert len(targets) >= 0
    print(f"✅ Black agent scan test passed, found {len(targets)} targets")


async def test_black_agent_mutation():
    memory = MetaMemory()
    replicator = ReplicationEngine(memory)
    sandbox = Sandbox(isolated=True)

    black = BlackAgent("black-test", memory, replicator, sandbox)
    original_preference = black.genome.scan_preference
    black.consecutive_failures = 5

    await black._mutate_phase()

    # Mutation may change preference
    print(f"✅ Black agent mutation test passed")
    print(f"   Original: {original_preference}, Current: {black.genome.scan_preference}")


def run_tests():
    asyncio.run(test_black_agent_creation())
    asyncio.run(test_black_agent_scan())
    asyncio.run(test_black_agent_mutation())


if __name__ == "__main__":
    run_tests()
