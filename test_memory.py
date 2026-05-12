# tests/test_memory.py

"""Basic smoke test for MetaMemory."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.meta_memory import MetaMemory


async def test_set_get():
    memory = MetaMemory()
    await memory.set("test:key", {"hello": "world"})
    result = await memory.get("test:key")
    assert result == {"hello": "world"}, f"Expected {{'hello': 'world'}}, got {result}"
    print("✅ Memory set/get test passed")


async def test_search():
    memory = MetaMemory()
    await memory.set("agent:black:001", {"type": "black"})
    await memory.set("agent:red:001", {"type": "red"})
    results = await memory.search("agent")
    assert len(results) >= 2
    print("✅ Memory search test passed")


async def test_delete():
    memory = MetaMemory()
    await memory.set("test:delete", {"data": "to_delete"})
    await memory.delete("test:delete")
    result = await memory.get("test:delete")
    assert result is None
    print("✅ Memory delete test passed")


def run_tests():
    asyncio.run(test_set_get())
    asyncio.run(test_search())
    asyncio.run(test_delete())


if __name__ == "__main__":
    run_tests()
