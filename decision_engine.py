# src/evolution/decision_engine.py

"""Autonomous evolution decision engine."""

import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

from src.evolution.parameters import EvolutionParameters
from src.evolution.fitness import FitnessMetrics, FitnessCalculator


class DecisionType(Enum):
    """Types of evolution decisions."""

    MUTATE = "mutate"
    PROMOTE = "promote"
    CULL = "cull"
    CREATE_NEW = "create_new"
    ROTATE = "rotate"
    ADJUST_MUTATION_RATE = "adjust_mutation_rate"
    NO_ACTION = "no_action"


@dataclass
class Decision:
    """A decision made by Red supervisor."""

    type: DecisionType
    agent_id: Optional[str]
    reason: str
    parameters: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)


class DecisionEngine:
    """
    Red's decision engine — evaluates fitness and makes evolution decisions.

    This is the core regulatory mechanism that controls how the population evolves.
    """

    def __init__(self, parameters: EvolutionParameters):
        self.parameters = parameters
        self.fitness_calculator = FitnessCalculator(parameters)
        self._last_mutation_time: Dict[str, datetime] = {}
        self._generation_start_time: datetime = datetime.now()

    def evaluate_agent(self, agent_id: str, history: List[Dict]) -> FitnessMetrics:
        """Evaluate a single agent's fitness."""
        return self.fitness_calculator.calculate(agent_id, history)

    def evaluate_population(self, agents: List[Dict]) -> List[FitnessMetrics]:
        """Evaluate entire population."""
        results = []
        for agent in agents:
            metrics = self.evaluate_agent(agent["id"], agent.get("history", []))
            results.append(metrics)

        results.sort(key=lambda x: x.overall_fitness, reverse=True)
        return results

    def decide_for_agent(self, agent_id: str, metrics: FitnessMetrics,
                         agent_history: List[Dict]) -> Decision:
        """Make a decision for a single agent based on its fitness."""

        # Check for starvation
        if self._is_starving(agent_history):
            return Decision(
                type=DecisionType.CULL,
                agent_id=agent_id,
                reason=f"No success in {self.parameters.starvation_days} days",
            )

        # Check consecutive failures
        consecutive_failures = self._get_consecutive_failures(agent_history)
        if consecutive_failures >= self.parameters.max_consecutive_failures:
            return Decision(
                type=DecisionType.MUTATE,
                agent_id=agent_id,
                reason=f"{consecutive_failures} consecutive failures",
                parameters={"mutation_intensity": min(100, consecutive_failures * 10)},
            )

        # Check time since last mutation
        if agent_id in self._last_mutation_time:
            hours_since = (datetime.now() - self._last_mutation_time[agent_id]).total_seconds() / 3600
            if hours_since < self.parameters.min_time_between_mutations_hours:
                return Decision(
                    type=DecisionType.NO_ACTION,
                    agent_id=agent_id,
                    reason=f"Too soon since last mutation ({hours_since:.1f} hours ago)",
                )

        # Fitness-based decisions
        if metrics.overall_fitness < self.parameters.fitness_threshold_cull:
            return Decision(
                type=DecisionType.CULL,
                agent_id=agent_id,
                reason=f"Fitness {metrics.overall_fitness:.1f} below cull threshold {self.parameters.fitness_threshold_cull}",
            )

        if metrics.overall_fitness < self.parameters.fitness_threshold_keep:
            self._last_mutation_time[agent_id] = datetime.now()
            return Decision(
                type=DecisionType.MUTATE,
                agent_id=agent_id,
                reason=f"Fitness {metrics.overall_fitness:.1f} below keep threshold",
                parameters={"mutation_intensity": 30},
            )

        if metrics.overall_fitness >= self.parameters.fitness_threshold_promote:
            return Decision(
                type=DecisionType.PROMOTE,
                agent_id=agent_id,
                reason=f"Fitness {metrics.overall_fitness:.1f} above promote threshold",
                parameters={"preserve": True},
            )

        # Check generation age
        if self._is_generation_too_old():
            return Decision(
                type=DecisionType.ROTATE,
                agent_id=None,
                reason=f"Generation age exceeded {self.parameters.generation_max_age_hours} hours",
            )

        return Decision(
            type=DecisionType.NO_ACTION,
            agent_id=agent_id,
            reason="Fitness acceptable, no action needed",
        )

    def decide_population(self, agents: List[Dict]) -> List[Decision]:
        """Make decisions for entire population."""
        decisions = []
        metrics_list = self.evaluate_population(agents)

        # Individual decisions
        for metrics in metrics_list:
            agent = next((a for a in agents if a["id"] == metrics.agent_id), None)
            if agent:
                decision = self.decide_for_agent(metrics.agent_id, metrics, agent.get("history", []))
                if decision.type != DecisionType.NO_ACTION:
                    decisions.append(decision)

        # Check population size constraints
        active_agents = [a for a in agents if a.get("active", True)]
        if len(active_agents) < self.parameters.population_min:
            decisions.append(Decision(
                type=DecisionType.CREATE_NEW,
                agent_id=None,
                reason=f"Population below minimum ({len(active_agents)} < {self.parameters.population_min})",
                parameters={"count": self.parameters.population_min - len(active_agents)},
            ))

        elif len(active_agents) > self.parameters.population_max:
            lowest = sorted(metrics_list, key=lambda x: x.overall_fitness)[:len(active_agents) - self.parameters.population_max]
            for low_metrics in lowest:
                decisions.append(Decision(
                    type=DecisionType.CULL,
                    agent_id=low_metrics.agent_id,
                    reason=f"Population exceeds maximum, culling lowest fitness",
                ))

        return decisions

    def select_parents(self, agents: List[Dict], metrics_list: List[FitnessMetrics],
                       count: int) -> List[Dict]:
        """Select parent agents for reproduction using fitness-proportionate selection."""
        if not agents or not metrics_list:
            return []

        fitnesses = [m.overall_fitness for m in metrics_list]
        min_fitness = min(fitnesses)
        adjusted = [max(0.1, f - min_fitness + 1) for f in fitnesses]

        pressure = self.parameters.selection_pressure
        adjusted = [f ** pressure for f in adjusted]

        total = sum(adjusted)
        if total == 0:
            return agents[:count]

        probabilities = [f / total for f in adjusted]

        parents = []
        for _ in range(min(count, len(agents))):
            idx = random.choices(range(len(agents)), weights=probabilities)[0]
            parents.append(agents[idx])

        return parents

    def _is_starving(self, history: List[Dict]) -> bool:
        """Check if agent is starving (no success for too long)."""
        if not history:
            return False

        successes = [h for h in history if h.get("success", False)]
        if not successes:
            first = history[0].get("timestamp", datetime.now())
            if isinstance(first, str):
                first = datetime.fromisoformat(first)
            return (datetime.now() - first).days >= self.parameters.starvation_days

        last_success = max(
            (s.get("timestamp") for s in successes),
            default=datetime.now()
        )
        if isinstance(last_success, str):
            last_success = datetime.fromisoformat(last_success)
        return (datetime.now() - last_success).days >= self.parameters.starvation_days

    def _get_consecutive_failures(self, history: List[Dict]) -> int:
        """Count consecutive failures from end of history."""
        consecutive = 0
        for event in reversed(history):
            if event.get("success", False):
                break
            consecutive += 1
        return consecutive

    def _is_generation_too_old(self) -> bool:
        """Check if current generation has exceeded max age."""
        age_hours = (datetime.now() - self._generation_start_time).total_seconds() / 3600
        return age_hours > self.parameters.generation_max_age_hours

    def reset_generation_timer(self) -> None:
        """Reset the generation timer."""
        self._generation_start_time = datetime.now()

    def get_population_stats(self, metrics_list: List[FitnessMetrics]) -> Dict[str, float]:
        """Get population statistics."""
        if not metrics_list:
            return {"avg": 0, "min": 0, "max": 0, "std": 0}

        fitnesses = [m.overall_fitness for m in metrics_list]
        avg = sum(fitnesses) / len(fitnesses)
        mn = min(fitnesses)
        mx = max(fitnesses)
        variance = sum((f - avg) ** 2 for f in fitnesses) / len(fitnesses)
        std = variance ** 0.5

        return {"avg": avg, "min": mn, "max": mx, "std": std}
