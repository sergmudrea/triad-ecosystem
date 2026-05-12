# src/evolution/fitness.py

"""Fitness calculation for Black agents."""

import numpy as np
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any

from src.evolution.parameters import EvolutionParameters


@dataclass
class FitnessMetrics:
    """Complete fitness measurement for an agent."""

    agent_id: str
    timestamp: datetime = field(default_factory=datetime.now)

    # Success metrics
    success_rate: float = 0.0
    exploit_effectiveness: float = 0.0
    persistence_duration_hours: float = 0.0

    # Stealth metrics
    detection_rate: float = 0.0
    trace_cleanliness: float = 0.0

    # Efficiency metrics
    time_to_compromise_seconds: float = 0.0
    resource_usage: float = 0.0

    # Evolution metrics
    mutation_count: int = 0
    exploit_generation_rate: float = 0.0

    # Raw data
    total_attempts: int = 0
    successful_attempts: int = 0
    detections: int = 0
    exploits_created: int = 0

    # Computed
    overall_fitness: float = 0.0

    def compute_overall_fitness(self, weights: Dict[str, float]) -> float:
        """Calculate overall fitness using weighted components."""
        normalized = {
            "success_rate": self.success_rate,
            "stealth": 100 - self.detection_rate,
            "speed": max(0, 100 - (self.time_to_compromise_seconds / 3600 * 10)),
            "adaptability": min(100, self.exploit_generation_rate * 20),
            "resource_usage": 100 - self.resource_usage,
        }

        total = 0.0
        for key, weight in weights.items():
            if key in normalized:
                total += normalized[key] * weight

        self.overall_fitness = min(100, max(0, total))
        return self.overall_fitness

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "timestamp": self.timestamp.isoformat(),
            "success_rate": self.success_rate,
            "detection_rate": self.detection_rate,
            "overall_fitness": self.overall_fitness,
            "total_attempts": self.total_attempts,
            "exploits_created": self.exploits_created,
        }


class FitnessCalculator:
    """Calculates fitness metrics for agents based on historical data."""

    def __init__(self, parameters: EvolutionParameters):
        self.parameters = parameters

    def calculate(self, agent_id: str, history: List[Dict]) -> FitnessMetrics:
        """Calculate fitness from agent's action history."""
        if not history:
            return FitnessMetrics(agent_id=agent_id, overall_fitness=0.0)

        # Success rate
        total = len(history)
        successful = sum(1 for h in history if h.get("success", False))
        success_rate = (successful / total * 100) if total > 0 else 0.0

        # Detection rate
        detections = sum(1 for h in history if h.get("detected", False))
        detection_rate = (detections / total * 100) if total > 0 else 0.0

        # Average time to compromise
        times = [h.get("duration_seconds", 0) for h in history if h.get("success")]
        avg_time = np.mean(times) if times else 3600.0

        # Exploit effectiveness
        exploit_attempts: Dict[str, Dict] = {}
        for h in history:
            exploit_id = h.get("exploit_id", "unknown")
            if exploit_id not in exploit_attempts:
                exploit_attempts[exploit_id] = {"success": 0, "total": 0}
            exploit_attempts[exploit_id]["total"] += 1
            if h.get("success"):
                exploit_attempts[exploit_id]["success"] += 1

        effectiveness = 0.0
        if exploit_attempts:
            effectiveness = np.mean([
                (data["success"] / data["total"] * 100)
                for data in exploit_attempts.values()
            ])

        # Exploit generation rate
        exploits_created = sum(h.get("exploits_created", 0) for h in history)
        if history:
            first_time = history[0].get("timestamp", datetime.now())
            if isinstance(first_time, str):
                first_time = datetime.fromisoformat(first_time)
            time_span_hours = (datetime.now() - first_time).total_seconds() / 3600
        else:
            time_span_hours = 0.1
        exploit_rate = (exploits_created / max(0.1, time_span_hours)) * 24

        # Persistence
        persistence = 0.0
        if successful > 0:
            success_times = [h.get("timestamp") for h in history if h.get("success")]
            if len(success_times) >= 2:
                if isinstance(success_times[0], str):
                    success_times = [datetime.fromisoformat(t) for t in success_times]
                persistence = (success_times[-1] - success_times[0]).total_seconds() / 3600

        # Mutation count
        mutation_count = sum(h.get("mutation_count", 0) for h in history)

        metrics = FitnessMetrics(
            agent_id=agent_id,
            success_rate=success_rate,
            exploit_effectiveness=effectiveness,
            persistence_duration_hours=persistence,
            detection_rate=detection_rate,
            trace_cleanliness=100 - detection_rate,
            time_to_compromise_seconds=avg_time,
            resource_usage=50.0,
            mutation_count=mutation_count,
            exploit_generation_rate=exploit_rate,
            total_attempts=total,
            successful_attempts=successful,
            detections=detections,
            exploits_created=exploits_created,
        )

        metrics.compute_overall_fitness(self.parameters.fitness_weights)
        return metrics
