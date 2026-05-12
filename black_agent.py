# src/agents/black_agent.py

import asyncio
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional

from src.agents.base_agent import EvolvableAgent
from src.core.meta_memory import MemoryOptimization
from src.simulation.sandbox import Sandbox, Target


@dataclass
class BlackGenome:
    """The 'DNA' of a Black agent — determines behavior."""

    scan_preference: str = "adaptive"
    scan_ports: List[int] = field(default_factory=lambda: [22, 80, 443, 445, 3389, 8080])
    scan_delay_ms: int = 60000
    scan_subnets: List[str] = field(default_factory=lambda: ["192.168.1.0/24", "10.0.0.0/24"])
    exploit_ids: List[str] = field(default_factory=list)
    exploit_creation_skill: float = 50.0
    attack_style: str = "adaptive"
    max_retries: int = 3
    mutation_rate: float = 15.0
    fuzzing_enabled: bool = True


class BlackAgent(EvolvableAgent):
    """
    BLACK TEAM — Eternal Predator.

    Scans continuously, attacks discovered targets, records successes,
    and mutates its genome on failures.
    """

    def __init__(self, agent_id: str, memory, replicator, sandbox: Sandbox):
        super().__init__(agent_id, "black", memory, replicator)
        self.genome = BlackGenome()
        self.controlled_machines: List[Target] = []
        self.consecutive_failures: int = 0
        self.starvation_timer: Optional[datetime] = None
        self.sandbox = sandbox

    async def run(self) -> None:
        print(f"[BLACK:{self.id[:8]}] Activated. Starting eternal hunt...")
        self.starvation_timer = datetime.now()

        while self._running:
            try:
                targets = await self._scan_phase()
                success = await self._attack_phase(targets)

                if success:
                    await self._record_success_procedure()
                    await self._create_new_exploits()
                    self.starvation_timer = datetime.now()
                    self.consecutive_failures = 0
                else:
                    self.consecutive_failures += 1
                    await self._mutate_phase()

                if self._is_starving():
                    await self._signal_red_for_reinforcement()

            except Exception as e:
                print(f"[BLACK:{self.id[:8]}] Error: {e}")
                await self._mutate_phase()

            await asyncio.sleep(self.genome.scan_delay_ms / 1000)

    async def _scan_phase(self) -> List[Target]:
        print(f"[BLACK:{self.id[:8]}] Scanning {len(self.genome.scan_subnets)} subnets...")
        targets = []
        for subnet in self.genome.scan_subnets:
            discovered = await self.sandbox.scan(subnet, self.genome.scan_ports)
            targets.extend(discovered)
        print(f"[BLACK:{self.id[:8]}] Found {len(targets)} potential targets")
        return targets

    async def _attack_phase(self, targets: List[Target]) -> bool:
        for target in targets:
            if any(m.ip == target.ip for m in self.controlled_machines):
                continue
            for exploit_id in self.genome.exploit_ids:
                print(f"[BLACK:{self.id[:8]}] Attacking {target.ip}:{target.port} with {exploit_id}")
                result = await self.sandbox.run_exploit(exploit_id, target)
                if result.success:
                    print(f"[BLACK:{self.id[:8]}] ✅ SUCCESS! {target.ip} compromised")
                    target.controlled_by = "black"
                    self.controlled_machines.append(target)
                    return True
                else:
                    print(f"[BLACK:{self.id[:8]}] ❌ Failed: {result.error}")
        return False

    async def _record_success_procedure(self) -> None:
        procedure = {
            "timestamp": datetime.now().isoformat(),
            "attacker_id": self.id,
            "genome": {
                "scan_preference": self.genome.scan_preference,
                "exploits": self.genome.exploit_ids[:5],
            },
            "steps": ["scan", "exploit", "persist"],
            "success": True,
        }
        await self.memory.set(f"black:success:{datetime.now().timestamp()}", procedure, source="black")
        print(f"[BLACK:{self.id[:8]}] Success procedure recorded")

    async def _create_new_exploits(self) -> None:
        successes = await self.memory.search("black:success")
        new_exploits = []
        for success_key in successes[:5]:
            data = await self.memory.get(success_key)
            if data and "genome" in data and data["genome"].get("exploits"):
                base = data["genome"]["exploits"][0] if data["genome"]["exploits"] else "exploit"
                new_exploit = f"mutated_{base}_{random.randint(1000, 9999)}"
                new_exploits.append(new_exploit)
        self.genome.exploit_ids.extend(new_exploits)
        print(f"[BLACK:{self.id[:8]}] Created {len(new_exploits)} new exploits")

    async def _mutate_phase(self) -> None:
        intensity = min(100, self.consecutive_failures * 10)
        print(f"[BLACK:{self.id[:8]}] Mutating (intensity={intensity})...")
        if random.random() * 100 < intensity:
            self.genome.scan_preference = random.choice(["aggressive", "stealth", "random", "adaptive"])
        if random.random() * 100 < intensity:
            self.genome.attack_style = random.choice(["loud", "quiet", "adaptive"])
        await self.memory.set(
            f"black:mutation:{datetime.now().timestamp()}",
            {
                "agent_id": self.id,
                "intensity": intensity,
                "new_genome": {
                    "scan_preference": self.genome.scan_preference,
                    "attack_style": self.genome.attack_style,
                    "exploit_count": len(self.genome.exploit_ids),
                },
            },
            source="black",
        )

    def _is_starving(self) -> bool:
        if self.starvation_timer is None:
            return False
        return (datetime.now() - self.starvation_timer) > timedelta(days=30)

    async def _signal_red_for_reinforcement(self) -> None:
        await self.memory.set("black:reinforcement_needed", True, source="black")
        print(f"[BLACK:{self.id[:8]}] ⚠️ STARVING — Signaled Red for reinforcement")

    async def apply_optimization_locally(self, optimization: MemoryOptimization) -> None:
        print(f"[BLACK:{self.id[:8]}] Applied optimization {optimization.id[:8]}")
        if optimization.optimization_recipe.get("algorithm") == "lz4+bloom":
            self._exploit_cache = set(self.genome.exploit_ids)
