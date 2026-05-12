# src/agents/red_agent.py

import asyncio
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from src.agents.base_agent import EvolvableAgent
from src.core.meta_memory import MemoryOptimization
from src.simulation.sandbox import Sandbox, Target


class RedAgent(EvolvableAgent):
    """
    RED TEAM — Observer & Creator.

    Observes Black attacks, simulates them, captures compromised machines,
    builds adaptation packets for Blue, and creates new Black when needed.
    """

    def __init__(self, agent_id: str, memory, replicator, sandbox: Sandbox):
        super().__init__(agent_id, "red", memory, replicator)
        self.controlled_machines: List[Target] = []
        self.collected_attacks: List[dict] = []
        self.adaptation_packets: List[dict] = []
        self.can_create_black: bool = True
        self.generation: int = 0
        self.sandbox = sandbox

    async def run(self) -> None:
        print(f"[RED:{self.id[:8]}] Supervisor activated. Observing and regulating evolution...")

        while self._running:
            await self._observation_phase()
            await self._simulation_phase()
            await self._build_adaptation_packets()
            await self._hunting_phase()
            await self._check_and_create_black()
            await asyncio.sleep(5)

    async def _observation_phase(self) -> None:
        successes = await self.memory.search("black:success")
        for key in successes:
            data = await self.memory.get(key)
            if data and data not in self.collected_attacks:
                self.collected_attacks.append(data)
                print(f"[RED:{self.id[:8]}] Captured attack: {key}")

    async def _simulation_phase(self) -> None:
        for attack in self.collected_attacks[-5:]:
            if "simulated" not in attack:
                print(f"[RED:{self.id[:8]}] Simulating attack...")
                result = await self.sandbox.simulate_attack(attack)
                attack["simulated"] = True
                attack["simulation_result"] = {
                    "success": result.success,
                    "reason": result.reason,
                }
                if result.success:
                    print(f"[RED:{self.id[:8]}] ✅ Simulation successful")
                else:
                    print(f"[RED:{self.id[:8]}] ⚠️ Simulation revealed issues")

    async def _build_adaptation_packets(self) -> None:
        if not self.collected_attacks:
            return

        packet = {
            "id": str(uuid4()),
            "generated_at": datetime.now().isoformat(),
            "for_blue": True,
            "content": {
                "vulnerabilities": self._extract_vulnerabilities(),
                "techniques": self._extract_techniques(),
                "iocs": self._extract_iocs(),
                "recommended_patches": self._extract_patches(),
            },
        }
        self.adaptation_packets.append(packet)
        await self.memory.set(f"red:adaptation:{packet['id']}", packet, source="red")
        print(f"[RED:{self.id[:8]}] Built adaptation packet {packet['id'][:8]}")

    def _extract_vulnerabilities(self) -> List[str]:
        vulns = []
        for attack in self.collected_attacks[-10:]:
            if "cve" in attack:
                vulns.append(attack["cve"])
        return list(set(vulns))[:5]

    def _extract_techniques(self) -> List[str]:
        return ["T1059.001", "T1003.001", "T1047"]

    def _extract_iocs(self) -> List[str]:
        return ["192.168.1.100", "malware.exe", "suspicious.dll"]

    def _extract_patches(self) -> List[str]:
        return ["KB123456", "KB789012"]

    async def _hunting_phase(self) -> None:
        black_targets = await self.memory.search("black:controlled")
        for target_key in black_targets:
            target_data = await self.memory.get(target_key)
            if target_data and target_data.get("controlled_by") == "black":
                blue_check = await self.memory.get(f"blue:jurisdiction:{target_data['ip']}")
                if not blue_check or not blue_check.get("controlled"):
                    print(f"[RED:{self.id[:8]}] Capturing {target_data['ip']} from Black...")
                    await self.sandbox.capture_machine(target_data["ip"])
                    self.controlled_machines.append(Target(
                        ip=target_data["ip"],
                        port=target_data.get("port", 0),
                        service=target_data.get("service", "unknown")
                    ))
                    await self.memory.set(
                        f"red:captured:{target_data['ip']}",
                        {"ip": target_data["ip"], "captured_at": datetime.now().isoformat()},
                        source="red",
                    )

    async def _check_and_create_black(self) -> None:
        reinforcement_needed = await self.memory.get("black:reinforcement_needed")
        if reinforcement_needed or await self._is_black_extinct():
            print(f"[RED:{self.id[:8]}] Creating new Black agent...")
            new_black = {
                "id": str(uuid4()),
                "genome": {
                    "scan_preference": "adaptive",
                    "exploits": self._extract_techniques(),
                    "exploit_creation_skill": 75,
                },
            }
            await self.memory.set("black:new_agent", new_black, source="red")
            await self.memory.set("black:reinforcement_needed", False, source="red")
            self.generation += 1
            print(f"[RED:{self.id[:8]}] ✅ New Black agent created. Generation {self.generation}")

    async def _is_black_extinct(self) -> bool:
        successes = await self.memory.search("black:success")
        if not successes:
            return True
        last_success = await self.memory.get(successes[-1]) if successes else None
        if last_success:
            last_time = datetime.fromisoformat(last_success.get("timestamp", "2000-01-01"))
            return (datetime.now() - last_time).days > 30
        return False

    async def apply_optimization_locally(self, optimization: MemoryOptimization) -> None:
        if len(self.collected_attacks) > 1000:
            self.collected_attacks = self.collected_attacks[-500:]
        print(f"[RED:{self.id[:8]}] Applied optimization {optimization.id[:8]}")
