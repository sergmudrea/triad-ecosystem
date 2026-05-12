# src/agents/blue_agent.py

import asyncio
from datetime import datetime
from typing import List

from src.agents.base_agent import EvolvableAgent
from src.core.meta_memory import MemoryOptimization
from src.simulation.sandbox import Sandbox, Target


class BlueAgent(EvolvableAgent):
    """
    BLUE TEAM — Immune System & Memory Optimizer.

    Receives adaptation packets from Red, patches vulnerabilities,
    continuously optimizes memory (encryption, deduplication, compression),
    and broadcasts optimizations to all agents.
    """

    def __init__(self, agent_id: str, memory, replicator, sandbox: Sandbox):
        super().__init__(agent_id, "blue", memory, replicator)
        self.controlled_machines: List[Target] = []
        self.patched_vulnerabilities: List[str] = []
        self.detection_rules: List[dict] = []
        self.optimization_counter: int = 0
        self.sandbox = sandbox

    async def run(self) -> None:
        print(f"[BLUE:{self.id[:8]}] Activated. Defending and optimizing...")

        while self._running:
            await self._receive_adaptation_packets()
            await self._adapt_defenses()
            await self._audit_phase()
            await self._cleanup_phase()
            await self._optimize_memory_phase()
            await self._broadcast_optimizations()
            await asyncio.sleep(10)

    async def _receive_adaptation_packets(self) -> None:
        packets = await self.memory.search("red:adaptation")
        for packet_key in packets:
            packet = await self.memory.get(packet_key)
            if packet and not packet.get("processed_by_blue"):
                print(f"[BLUE:{self.id[:8]}] Processing adaptation packet {packet['id'][:8]}")

                for vuln in packet["content"]["vulnerabilities"]:
                    if vuln not in self.patched_vulnerabilities:
                        await self._apply_patch(vuln)
                        self.patched_vulnerabilities.append(vuln)

                for technique in packet["content"]["techniques"]:
                    rule = self._generate_rule(technique)
                    if rule not in self.detection_rules:
                        self.detection_rules.append(rule)

                packet["processed_by_blue"] = True
                await self.memory.set(packet_key, packet, source="blue")

    async def _apply_patch(self, vuln: str) -> None:
        print(f"[BLUE:{self.id[:8]}] 🔒 Patching {vuln}...")
        await asyncio.sleep(0.5)
        await self.memory.set(
            f"blue:patched:{vuln}",
            {"patched_at": datetime.now().isoformat()},
            source="blue",
        )

    def _generate_rule(self, technique: str) -> dict:
        return {
            "id": f"RULE_{technique}",
            "technique": technique,
            "rule_type": "sigma",
            "rule_content": f"detection:\n  selection:\n    technique: {technique}\n  condition: selection",
        }

    async def _adapt_defenses(self) -> None:
        for machine in self.controlled_machines[:5]:
            print(f"[BLUE:{self.id[:8]}] Deploying {len(self.detection_rules)} rules to {machine.ip}")
            await self.sandbox.deploy_rules(machine, self.detection_rules)

    async def _audit_phase(self) -> None:
        all_targets = await self.memory.search("target")
        for target_key in all_targets[:10]:
            target_data = await self.memory.get(target_key)
            if target_data and not target_data.get("controlled_by"):
                target = Target(
                    ip=target_data["ip"],
                    port=target_data["port"],
                    service=target_data["service"],
                )
                self.controlled_machines.append(target)
                await self.memory.set(
                    f"blue:controlled:{target.ip}",
                    {"ip": target.ip, "controlled_at": datetime.now().isoformat()},
                    source="blue",
                )
                print(f"[BLUE:{self.id[:8]}] 🛡️ Secured {target.ip}")

    async def _cleanup_phase(self) -> None:
        for controller in ["black", "red"]:
            controlled = await self.memory.search(f"{controller}:controlled")
            for machine_key in controlled:
                machine_data = await self.memory.get(machine_key)
                if machine_data:
                    print(f"[BLUE:{self.id[:8]}] 🧹 Cleaning {machine_data['ip']} (controlled by {controller})")
                    await self.sandbox.clean_machine(machine_data["ip"])
                    self.controlled_machines.append(
                        Target(ip=machine_data["ip"], port=0, service="unknown")
                    )
                    await self.memory.set(
                        f"blue:cleaned:{machine_data['ip']}",
                        {"ip": machine_data["ip"], "cleaned_at": datetime.now().isoformat()},
                        source="blue",
                    )

    async def _optimize_memory_phase(self) -> None:
        self.optimization_counter += 1
        print(f"[BLUE:{self.id[:8]}] 🧬 Optimizing memory (cycle {self.optimization_counter})...")
        optimization = await self.memory.optimize(optimizer="blue")
        print(f"[BLUE:{self.id[:8]}] 📊 Compression ratio: {optimization.compression_ratio:.2%}")
        await self.memory.set(
            f"blue:optimization:{optimization.id}",
            {
                "id": optimization.id,
                "timestamp": optimization.timestamp.isoformat(),
                "compression_ratio": optimization.compression_ratio,
                "keys_optimized": len(optimization.target_keys),
            },
            source="blue",
        )

    async def _broadcast_optimizations(self) -> None:
        optimizations = await self.memory.search("blue:optimization")
        if optimizations:
            last_opt_data = await self.memory.get(optimizations[-1])
            if last_opt_data and not last_opt_data.get("broadcasted"):
                print(f"[BLUE:{self.id[:8]}] 📡 Broadcasting optimization {last_opt_data['id'][:8]} to cluster...")
                optimization = MemoryOptimization(
                    id=last_opt_data["id"],
                    applied_by="blue",
                    timestamp=datetime.fromisoformat(last_opt_data["timestamp"]),
                    type="full_optimization",
                    target_keys=[],
                    original_size=0,
                    optimized_size=0,
                    compression_ratio=last_opt_data["compression_ratio"],
                    optimization_recipe={"algorithm": "lz4+aes256+bloom", "parameters": {}},
                )
                await self.replicator.propagate(optimization)
                last_opt_data["broadcasted"] = True
                await self.memory.set(optimizations[-1], last_opt_data, source="blue")

    async def apply_optimization_locally(self, optimization: MemoryOptimization) -> None:
        print(f"[BLUE:{self.id[:8]}] Applied optimization {optimization.id[:8]} locally")
        await self._sync_local_cache()

    async def _sync_local_cache(self) -> None:
        self.detection_rules = []
        rules = await self.memory.search("rule")
        for rule_key in rules[:100]:
            rule = await self.memory.get(rule_key)
            if rule:
                self.detection_rules.append(rule)
