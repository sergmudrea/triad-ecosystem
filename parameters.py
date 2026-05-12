# src/evolution/parameters.py

"""Evolution parameter presets."""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List


@dataclass
class EvolutionParameters:
    """Master evolution configuration — defined and enforced by Red Supervisor."""

    # Mutation parameters
    mutation_rate_min: float = 5.0
    mutation_rate_max: float = 30.0
    mutation_rate_initial: float = 15.0
    mutation_rate_dynamic: bool = True
    mutation_increase_on_failure: float = 10.0

    # Fitness thresholds
    fitness_threshold_keep: float = 30.0
    fitness_threshold_promote: float = 70.0
    fitness_threshold_cull: float = 15.0
    fitness_weights: Dict[str, float] = field(default_factory=lambda: {
        "success_rate": 0.4,
        "stealth": 0.2,
        "speed": 0.15,
        "adaptability": 0.15,
        "resource_usage": 0.1,
    })

    # Population control
    population_min: int = 5
    population_max: int = 20
    elitism_count: int = 3
    selection_pressure: float = 3.0

    # Time-based parameters
    generation_max_age_hours: int = 168
    starvation_days: int = 30
    max_consecutive_failures: int = 5
    min_time_between_mutations_hours: int = 2

    # Exploit creation
    exploit_creation_threshold: float = 60.0
    exploit_creation_rate_max_per_day: int = 3
    exploit_fuzzing_enabled: bool = True
    exploit_fuzzing_iterations: int = 100

    # Evolution strategy
    adaptive_mutation: bool = True
    crossover_enabled: bool = True
    crossover_rate: float = 40.0
    immigrant_rate: float = 10.0

    # Memory optimization
    memory_optimization_interval_minutes: int = 10
    encryption_rotation_minutes: int = 60
    deduplication_enabled: bool = True
    compression_enabled: bool = True
    auto_prune_ttl_hours: int = 24

    # Replication
    replication_timeout_seconds: int = 30
    replication_retry_count: int = 3
    broadcast_all_optimizations: bool = True

    # Safety
    max_risk_score_allowed: float = 70.0
    sandbox_only: bool = True
    require_auth_for_targets: bool = True

    # Novelty search
    novelty_enabled: bool = True
    novelty_weight: float = 0.3
    novelty_archive_size: int = 100
    novelty_k_nearest: int = 15

    # MAP-Elites
    map_elites_enabled: bool = True
    map_elites_resolution: List[int] = field(default_factory=lambda: [20, 20])

    # Coevolution
    coevolution_enabled: bool = True
    coevolution_round_interval_seconds: int = 300

    def to_dict(self) -> Dict[str, Any]:
        """Convert parameters to dictionary."""
        return asdict(self)

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update parameters from dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def validate(self) -> List[str]:
        """Validate parameters, return list of errors."""
        errors = []

        if self.mutation_rate_min < 0 or self.mutation_rate_min > 100:
            errors.append("mutation_rate_min must be between 0 and 100")

        if self.mutation_rate_max < self.mutation_rate_min:
            errors.append("mutation_rate_max must be >= mutation_rate_min")

        if self.fitness_threshold_cull >= self.fitness_threshold_keep:
            errors.append("cull threshold must be less than keep threshold")

        if self.fitness_threshold_keep >= self.fitness_threshold_promote:
            errors.append("keep threshold must be less than promote threshold")

        weight_sum = sum(self.fitness_weights.values())
        if abs(weight_sum - 1.0) > 0.01:
            errors.append(f"Fitness weights must sum to 1.0 (currently {weight_sum})")

        if self.population_min < 1:
            errors.append("population_min must be at least 1")

        if self.population_max < self.population_min:
            errors.append("population_max must be >= population_min")

        if self.selection_pressure < 1 or self.selection_pressure > 10:
            errors.append("selection_pressure must be between 1 and 10")

        return errors


# Evolution presets
AGGRESSIVE_PARAMETERS = EvolutionParameters(
    mutation_rate_min=20.0,
    mutation_rate_max=60.0,
    population_min=10,
    population_max=30,
    selection_pressure=5.0,
    elitism_count=1,
    novelty_weight=0.1,
)

CONSERVATIVE_PARAMETERS = EvolutionParameters(
    mutation_rate_min=2.0,
    mutation_rate_max=10.0,
    mutation_rate_initial=5.0,
    population_min=3,
    population_max=10,
    selection_pressure=2.0,
    elitism_count=5,
    novelty_weight=0.5,
)

RESEARCH_PARAMETERS = EvolutionParameters(
    mutation_rate_min=10.0,
    mutation_rate_max=50.0,
    mutation_rate_initial=25.0,
    population_min=8,
    population_max=25,
    selection_pressure=4.0,
    elitism_count=2,
    novelty_weight=0.4,
    crossover_rate=60.0,
    immigrant_rate=15.0,
)

DEFAULT_PARAMETERS = EvolutionParameters()
