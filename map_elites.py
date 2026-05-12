# src/evolution/map_elites.py

"""
MAP-Elites algorithm: maintains a map of high-performing agents
across different behavior niches.
"""

import numpy as np
from typing import Dict, List, Tuple, Any


class MAPElites:
    """
    Maintains an archive of the best agent in each behavior niche.
    Ensures diversity while preserving quality.
    """

    def __init__(self, resolution: Tuple[int, int] = (20, 20)):
        self.resolution = resolution
        self.archive: Dict[Tuple[int, int], Dict] = {}
        self._grid_size = resolution

    def _behavior_to_grid(self, behavior: np.ndarray) -> Tuple[int, int]:
        """Convert continuous behavior to discrete grid coordinates."""
        x = min(self._grid_size[0] - 1, int(behavior[0] / 100 * self._grid_size[0]))
        y = min(self._grid_size[1] - 1, int(behavior[1] * self._grid_size[1]))
        return (x, y)

    def add_agent(self, agent_id: str, fitness: float, behavior: np.ndarray,
                  agent_data: Dict) -> bool:
        """Add agent to archive if it's the best in its niche."""
        cell = self._behavior_to_grid(behavior)

        if cell not in self.archive or self.archive[cell]["fitness"] < fitness:
            self.archive[cell] = {
                "agent_id": agent_id,
                "fitness": fitness,
                "behavior": behavior.tolist(),
                "data": agent_data,
                "cell": cell,
                "added_at": __import__('datetime').datetime.now().isoformat(),
            }
            return True
        return False

    def get_elite_agents(self) -> List[Dict]:
        """Get all archived agents for reproduction."""
        return list(self.archive.values())

    def get_best_agent(self) -> Dict:
        """Get the agent with highest fitness across all niches."""
        if not self.archive:
            return None
        return max(self.archive.values(), key=lambda x: x["fitness"])

    def coverage(self) -> float:
        """Percentage of cells filled in archive."""
        total_cells = self._grid_size[0] * self._grid_size[1]
        return len(self.archive) / total_cells * 100

    def get_heatmap_data(self) -> List[List[float]]:
        """Generate heatmap data for visualization."""
        heatmap = np.zeros(self._grid_size)
        for (x, y), agent in self.archive.items():
            heatmap[x, y] = agent["fitness"]
        return heatmap.tolist()

    def get_niche_fitness(self, cell: Tuple[int, int]) -> float:
        """Get fitness of agent in specific niche."""
        if cell in self.archive:
            return self.archive[cell]["fitness"]
        return 0.0

    def clear(self) -> None:
        """Clear the archive."""
        self.archive.clear()
