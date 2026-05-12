# src/simulation/sandbox.py

import asyncio
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Target:
    """A target machine in the simulated environment."""

    ip: str
    port: int
    service: str
    os: str = "linux"
    vulnerable: bool = True
    controlled_by: Optional[str] = None


@dataclass
class ExploitResult:
    """Result of an exploit attempt."""

    success: bool
    error: Optional[str] = None
    output: Optional[str] = None


@dataclass
class SimulationResult:
    """Result of a simulation."""

    success: bool
    reason: Optional[str] = None


class Sandbox:
    """
    Isolated sandbox for executing attacks and simulations.

    NO REAL NETWORK ACCESS — everything is simulated.
    """

    def __init__(self, isolated: bool = True):
        self.isolated = isolated
        self._targets: List[Target] = []
        self._initialize_targets()

    def _initialize_targets(self):
        """Initialize simulated target machines."""
        self._targets = [
            Target(ip="192.168.1.10", port=22, service="ssh", os="linux", vulnerable=True),
            Target(ip="192.168.1.20", port=445, service="smb", os="windows", vulnerable=True),
            Target(ip="192.168.1.30", port=80, service="http", os="linux", vulnerable=True),
            Target(ip="192.168.1.40", port=3389, service="rdp", os="windows", vulnerable=False),
            Target(ip="192.168.1.50", port=8080, service="tomcat", os="linux", vulnerable=True),
            Target(ip="10.0.0.10", port=22, service="ssh", os="linux", vulnerable=True),
            Target(ip="10.0.0.20", port=443, service="https", os="linux", vulnerable=True),
            Target(ip="10.0.0.30", port=3306, service="mysql", os="linux", vulnerable=True),
            Target(ip="172.16.0.10", port=6379, service="redis", os="linux", vulnerable=True),
            Target(ip="172.16.0.20", port=27017, service="mongodb", os="linux", vulnerable=True),
        ]

    async def scan(self, subnet: str, ports: List[int]) -> List[Target]:
        """Simulate network scan."""
        await asyncio.sleep(0.5)

        results = []
        prefix = subnet.replace("/24", "").replace("/16", "")
        for target in self._targets:
            if target.ip.startswith(prefix) or subnet == "0.0.0.0/0":
                if target.port in ports or not ports:
                    results.append(target)

        return results

    async def run_exploit(self, exploit_id: str, target: Target) -> ExploitResult:
        """Simulate running an exploit."""
        await asyncio.sleep(0.3)

        if target.vulnerable and random.random() < 0.7:
            target.controlled_by = "black"
            return ExploitResult(
                success=True,
                output=f"Exploit {exploit_id} succeeded on {target.ip}"
            )
        else:
            return ExploitResult(
                success=False,
                error=f"Exploit {exploit_id} failed on {target.ip}"
            )

    async def simulate_attack(self, attack: dict) -> SimulationResult:
        """Simulate an attack for Red team analysis."""
        await asyncio.sleep(0.2)
        return SimulationResult(success=True, reason="Simulation completed")

    async def capture_machine(self, ip: str) -> bool:
        """Capture a machine (Red taking control)."""
        for target in self._targets:
            if target.ip == ip:
                target.controlled_by = "red"
                return True
        return False

    async def deploy_rules(self, machine: Target, rules: List[dict]) -> bool:
        """Deploy detection rules to a machine (Blue)."""
        await asyncio.sleep(0.1)
        print(f"   Deployed {len(rules)} rules to {machine.ip}")
        return True

    async def clean_machine(self, ip: str) -> bool:
        """Clean a compromised machine (Blue)."""
        for target in self._targets:
            if target.ip == ip:
                target.controlled_by = "blue"
                target.vulnerable = False
                return True
        return False

    async def add_target(self, target: Target) -> None:
        """Add a new target to the sandbox."""
        self._targets.append(target)

    def get_all_targets(self) -> List[Target]:
        """Get all targets in the sandbox."""
        return self._targets.copy()

    def get_controlled_by(self, controller: str) -> List[Target]:
        """Get targets controlled by specific agent."""
        return [t for t in self._targets if t.controlled_by == controller]
