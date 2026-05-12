# src/evolution/analytics.py

"""Evolution analytics and trend tracking."""

import numpy as np
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import deque
from datetime import datetime


@dataclass
class EvolutionSnapshot:
    """A snapshot of evolution state at a point in time."""

    generation: int
    timestamp: datetime
    best_fitness: float
    avg_fitness: float
    population_size: int
    diversity_score: float
    mutation_rate: float


class EvolutionAnalytics:
    """
    Tracks and analyzes evolution progress over time.
    Provides insights for parameter tuning.
    """

    def __init__(self, window_size: int = 100):
        self.snapshots: deque = deque(maxlen=window_size)
        self.generation_counter = 0

    def record_snapshot(self, metrics: Dict[str, Any]) -> None:
        """Record an evolution snapshot."""
        snapshot = EvolutionSnapshot(
            generation=self.generation_counter,
            timestamp=datetime.now(),
            best_fitness=metrics.get("best_fitness", 0),
            avg_fitness=metrics.get("average_fitness", 0),
            population_size=metrics.get("population_size", 0),
            diversity_score=metrics.get("diversity_score", 0),
            mutation_rate=metrics.get("mutation_rate", 15),
        )
        self.snapshots.append(snapshot)
        self.generation_counter += 1

    def get_trend(self) -> str:
        """Determine evolution trend."""
        if len(self.snapshots) < 10:
            return "insufficient_data"

        recent = [s.avg_fitness for s in list(self.snapshots)[-10:]]
        slope = np.polyfit(range(len(recent)), recent, 1)[0]

        if slope > 1:
            return "rapid_improvement"
        elif slope > 0.1:
            return "gradual_improvement"
        elif slope > -0.1:
            return "stagnation"
        else:
            return "decline"

    def get_stagnation_warning(self) -> bool:
        """Check if evolution has stagnated."""
        if len(self.snapshots) < 20:
            return False

        last_20 = [s.avg_fitness for s in list(self.snapshots)[-20:]]
        improvement = max(last_20) - min(last_20)

        return improvement < 5

    def get_decline_warning(self) -> bool:
        """Check if evolution is declining."""
        if len(self.snapshots) < 15:
            return False

        last_10 = [s.avg_fitness for s in list(self.snapshots)[-10:]]
        first_10 = [s.avg_fitness for s in list(self.snapshots)[-20:-10]]

        avg_last = np.mean(last_10)
        avg_first = np.mean(first_10)

        return avg_last < avg_first * 0.9

    def recommend_parameter_adjustments(self) -> Dict[str, float]:
        """Recommend parameter changes based on analytics."""
        recommendations = {}
        trend = self.get_trend()

        if trend == "stagnation":
            recommendations["mutation_rate_max"] = 50.0
            recommendations["immigrant_rate"] = 20.0
            recommendations["selection_pressure"] = 5.0
        elif trend == "decline":
            recommendations["mutation_rate_max"] = 30.0
            recommendations["fitness_threshold_cull"] = 20.0
            recommendations["elitism_count"] = 5
        elif trend == "rapid_improvement":
            recommendations["mutation_rate_max"] = 20.0
            recommendations["selection_pressure"] = 8.0

        if self.get_stagnation_warning():
            recommendations["novelty_weight"] = 0.5
            recommendations["crossover_rate"] = 60.0

        return recommendations

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a summary of evolution performance."""
        if not self.snapshots:
            return {"status": "no_data"}

        best_snapshot = max(self.snapshots, key=lambda s: s.best_fitness)
        latest = self.snapshots[-1]

        return {
            "status": "active",
            "total_generations": self.generation_counter,
            "current_best_fitness": latest.best_fitness,
            "current_avg_fitness": latest.avg_fitness,
            "all_time_best_fitness": best_snapshot.best_fitness,
            "best_generation": best_snapshot.generation,
            "trend": self.get_trend(),
            "stagnation_warning": self.get_stagnation_warning(),
            "population_size": latest.population_size,
            "diversity_score": latest.diversity_score,
        }

    def get_fitness_history(self) -> List[Dict]:
        """Get fitness history for charting."""
        return [
            {
                "generation": s.generation,
                "best_fitness": s.best_fitness,
                "avg_fitness": s.avg_fitness,
            }
            for s in self.snapshots
        ]

    def get_diversity_history(self) -> List[Dict]:
        """Get diversity history for charting."""
        return [
            {
                "generation": s.generation,
                "diversity_score": s.diversity_score,
            }
            for s in self.snapshots
        ]
