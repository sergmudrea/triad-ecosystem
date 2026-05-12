#!/usr/bin/env python3
# src/orchestrator.py

"""
TRIAD Ecosystem Orchestrator
Manages all agents and their lifecycle.
"""

import asyncio
import signal
import argparse
from datetime import datetime
from typing import Optional

from src.core.meta_memory import MetaMemory
from src.core.replicator import ReplicationEngine
from src.simulation.sandbox import Sandbox
from src.agents.black_agent import BlackAgent
from src.agents.red_agent import RedAgent
from src.agents.blue_agent import BlueAgent
from src.evolution.parameters import (
    EvolutionParameters,
    AGGRESSIVE_PARAMETERS,
    CONSERVATIVE_PARAMETERS,
    RESEARCH_PARAMETERS
)

BANNER = r"""
    ████████╗██████╗ ██╗ █████╗ ██████╗ 
    ╚══██╔══╝██╔══██╗██║██╔══██╗██╔══██╗
       ██║   ██████╔╝██║███████║██║  ██║
       ██║   ██╔══██╗██║██╔══██║██║  ██║
       ██║   ██║  ██║██║██║  ██║██████╔╝
       ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ 
    
    BLACK-RED-BLUE Autonomous Cyber Ecosystem
    =========================================
    [CONCEPT] Evolutionary cluster simulation
    [ISOLATION] Sandboxed — no real network access
"""

PRESETS = {
    "default": EvolutionParameters(),
    "aggressive": AGGRESSIVE_PARAMETERS,
    "conservative": CONSERVATIVE_PARAMETERS,
    "research": RESEARCH_PARAMETERS,
}


async def main():
    parser = argparse.ArgumentParser(description="TRIAD Autonomous Ecosystem")
    parser.add_argument("--preset", choices=PRESETS.keys(), default="default")
    parser.add_argument("--no-dashboard", action="store_true")
    parser.add_argument("--redis-url", default="redis://localhost:6379")
    args = parser.parse_args()

    print(BANNER)
    params = PRESETS[args.preset]
    print(f"[TRIAD] Preset: {args.preset}")
    print(f"[TRIAD] Mutation rate: {params.mutation_rate_min}-{params.mutation_rate_max}%")
    print(f"[TRIAD] Population: {params.population_min}-{params.population_max}")
    print()

    print("[TRIAD] Initializing Meta-Memory...")
    memory = MetaMemory(redis_url=args.redis_url)

    print("[TRIAD] Initializing Replication Engine...")
    replicator = ReplicationEngine(memory)

    print("[TRIAD] Initializing Sandbox...")
    sandbox = Sandbox(isolated=True)

    print("[TRIAD] Creating agents...")
    black = BlackAgent("black-001", memory, replicator, sandbox)
    red = RedAgent("red-001", memory, replicator, sandbox)
    blue = BlueAgent("blue-001", memory, replicator, sandbox)

    print("\n" + "=" * 50)
    print("[TRIAD] LAUNCHING ECOSYSTEM")
    print("=" * 50 + "\n")

    tasks = [
        asyncio.create_task(black.run()),
        asyncio.create_task(red.run()),
        asyncio.create_task(blue.run()),
    ]

    def shutdown():
        print("\n[TRIAD] Shutting down...")
        for t in tasks:
            t.cancel()

    signal.signal(signal.SIGINT, lambda s, f: shutdown())
    signal.signal(signal.SIGTERM, lambda s, f: shutdown())

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass
    finally:
        await memory.close()
        print("[TRIAD] Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
