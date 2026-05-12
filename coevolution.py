# src/evolution/coevolution.py

"""
Coevolution: Black agents compete against Blue agents.
Both evolve in response to each other (arms race).
"""

import asyncio
import random
from typing import Dict, List, Any
from datetime import datetime


class CoevolutionOrchestrator:
    """
    Manages competitive coevolution between Black and Blue.
    Black gets fitness from evading Blue.
    Blue gets fitness from detecting Black.
    """

    def __init__(self, memory):
        self.memory = memory
        self.generation = 0
        self.match_history: List[Dict] = []

    async def evaluate_match(self, black_id: str, blue_id: str,
                             black_genome: Dict, blue_defense: Dict) -> Dict:
        """
        Run a match between a Black and Blue agent.
        Returns scores for both.
        """
        # Black attempts an attack
        black_success = await self._simulate_attack(black_genome, blue_defense)

        # Blue attempts to detect
        blue_detection = await self._simulate_detection(black_genome, blue_defense)

        # Fitness calculation (relative)
        black_fitness = 0.0
        blue_fitness = 0.0

        if black_success and not blue_detection:
            black_fitness = 100.0
            blue_fitness = 0.0
        elif black_success and blue_detection:
            black_fitness = 50.0
            blue_fitness = 50.0
        elif not black_success and blue_detection:
            black_fitness = 0.0
            blue_fitness = 100.0
        else:
            black_fitness = 25.0
            blue_fitness = 25.0

        return {
            "black_id": black_id,
            "blue_id": blue_id,
            "black_fitness": black_fitness,
            "blue_fitness": blue_fitness,
            "black_success": black_success,
            "blue_detection": blue_detection,
            "timestamp": datetime.now().isoformat(),
        }

    async def _simulate_attack(self, black_genome: Dict, blue_defense: Dict) -> bool:
        """Simulate attack success."""
        black_power = black_genome.get("exploit_count", 10)
        blue_defense_level = blue_defense.get("defense_level", 50)
        success_prob = max(0, min(100, black_power - blue_defense_level + 50))
        return random.random() * 100 < success_prob

    async def _simulate_detection(self, black_genome: Dict, blue_defense: Dict) -> bool:
        """Simulate detection success."""
        black_stealth = black_genome.get("stealth", 50)
        blue_detection_level = blue_defense.get("detection_level", 50)
        detection_prob = max(0, min(100, blue_detection_level - black_stealth + 30))
        return random.random() * 100 < detection_prob

    async def run_coevolution_round(self, black_agents: List[Dict], blue_agents: List[Dict]) -> None:
        """Run a full round of coevolution."""
        self.generation += 1
        print(f"\n🔄 COEVOLUTION ROUND {self.generation}")

        if not black_agents or not blue_agents:
            print("   ⚠️ Not enough agents for coevolution")
            return

        round_results = []

        for black in black_agents[:10]:
            for blue in blue_agents[:5]:
                black_genome = black.get("genome", {"exploit_count": 10, "stealth": 50})
                blue_defense = blue.get("defense", {"defense_level": 50, "detection_level": 50})

                result = await self.evaluate_match(
                    black["id"], blue["id"],
                    black_genome, blue_defense
                )
                round_results.append(result)

                # Store result
                await self.memory.set(
                    f"coevolution:match:{black['id']}:{blue['id']}:{self.generation}",
                    result,
                    source="coevolution",
                    ttl=3600000
                )

        self.match_history.extend(round_results)

        # Keep only last 1000 matches
        if len(self.match_history) > 1000:
            self.match_history = self.match_history[-1000:]

        # Store generation data
        await self.memory.set(
            f"coevolution:generation:{self.generation}",
            {
                "generation": self.generation,
                "matches": len(round_results),
                "timestamp": datetime.now().isoformat(),
            },
            source="coevolution"
        )

        print(f"   ✅ Completed {len(round_results)} matches")

    def get_black_advantage(self) -> float:
        """Calculate Black's advantage over Blue (0-100)."""
        if not self.match_history:
            return 50.0

        black_wins = sum(
            1 for m in self.match_history
            if m["black_success"] and not m["blue_detection"]
        )
        total = len(self.match_history)
        return (black_wins / total * 100) if total > 0 else 50.0

    def get_blue_advantage(self) -> float:
        """Calculate Blue's advantage over Black (0-100)."""
        if not self.match_history:
            return 50.0

        blue_wins = sum(
            1 for m in self.match_history
            if not m["black_success"] and m["blue_detection"]
        )
        total = len(self.match_history)
        return (blue_wins / total * 100) if total > 0 else 50.0
