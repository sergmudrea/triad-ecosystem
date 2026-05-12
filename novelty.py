# src/evolution/novelty.py

"""
Novelty search encourages behavioral diversity, not just fitness.
Prevents premature convergence to local optima.
"""

import numpy as np
from typing import List, Dict
from collections import deque


class NoveltyArchive:
    """
    Stores unique behaviors to encourage exploration.
    Agents are rewarded for doing something NEW, not just something GOOD.
    """

    def __init__(self, archive_size: int = 100, k_nearest: int = 15):
        self.archive: deque = deque(maxlen=archive_size)
        self.k_nearest = k_nearest

    def behavior_vector(self, agent_history: List[Dict]) -> np.ndarray:
        """Convert agent history to behavior vector."""
        techniques_used = set()
        success_count = 0

        for event in agent_history[-50:]:
            if event.get("technique"):
                techniques_used.add(event.get("technique"))
            if event.get("success"):
                success_count += 1

        success_rate = success_count / max(1, len(agent_history))
        technique_diversity = len(techniques_used) / 20

        return np.array([success_rate, technique_diversity])

    def novelty_score(self, behavior: np.ndarray) -> float:
        """Calculate novelty as average distance to k nearest neighbors."""
        if len(self.archive) < self.k_nearest:
            return 1.0

        distances = [np.linalg.norm(behavior - a) for a in self.archive]
        distances.sort()
        avg_distance = np.mean(distances[:self.k_nearest])

        return avg_distance

    def add_to_archive(self, behavior: np.ndarray):
        """Add behavior to archive if sufficiently novel."""
        if len(self.archive) < self.archive.maxlen:
            self.archive.append(behavior)
        else:
            scores = [self.novelty_score(b) for b in self.archive]
            min_idx = np.argmin(scores)
            self.archive[min_idx] = behavior


class NoveltyEnhancedFitness:
    """
    Combines traditional fitness with novelty for better exploration.
    """

    def __init__(self, novelty_weight: float = 0.3):
        self.novelty_archive = NoveltyArchive()
        self.novelty_weight = novelty_weight

    def calculate(self, fitness: float, agent_history: List[Dict]) -> float:
        """Calculate novelty-enhanced fitness."""
        behavior = self.novelty_archive.behavior_vector(agent_history)
        novelty = self.novelty_archive.novelty_score(behavior)

        self.novelty_archive.add_to_archive(behavior)

        enhanced = (1 - self.novelty_weight) * fitness + self.novelty_weight * (novelty * 100)

        return min(100, max(0, enhanced))
