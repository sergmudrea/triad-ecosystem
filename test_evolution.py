# tests/test_evolution.py

import pytest
from datetime import datetime, timedelta

from src.evolution.parameters import EvolutionParameters
from src.evolution.fitness import FitnessCalculator, FitnessMetrics
from src.evolution.decision_engine import DecisionEngine, DecisionType


class TestEvolutionParameters:
    def test_default_parameters(self):
        params = EvolutionParameters()
        assert params.mutation_rate_min == 5.0
        assert params.mutation_rate_max == 30.0
        assert params.population_min == 5
        assert params.population_max == 20

    def test_parameter_validation(self):
        params = EvolutionParameters()
        errors = params.validate()
        assert len(errors) == 0

        params.mutation_rate_min = 100
        params.mutation_rate_max = 50
        errors = params.validate()
        assert len(errors) > 0

    def test_parameter_update(self):
        params = EvolutionParameters()
        params.update_from_dict({"mutation_rate_max": 50.0})
        assert params.mutation_rate_max == 50.0

    def test_weights_sum_to_one(self):
        params = EvolutionParameters()
        total = sum(params.fitness_weights.values())
        assert abs(total - 1.0) < 0.01


class TestFitnessCalculator:
    def test_empty_history(self):
        calculator = FitnessCalculator(EvolutionParameters())
        metrics = calculator.calculate("test_id", [])

        assert metrics.agent_id == "test_id"
        assert metrics.overall_fitness == 0.0

    def test_success_history(self):
        calculator = FitnessCalculator(EvolutionParameters())
        history = [
            {"success": True, "detected": False, "technique": "T1059"},
            {"success": True, "detected": False, "technique": "T1003"},
        ]
        metrics = calculator.calculate("test_id", history)

        assert metrics.success_rate == 100.0
        assert metrics.detection_rate == 0.0

    def test_mixed_history(self):
        calculator = FitnessCalculator(EvolutionParameters())
        history = [
            {"success": True, "detected": False},
            {"success": False, "detected": True},
        ]
        metrics = calculator.calculate("test_id", history)

        assert metrics.success_rate == 50.0
        assert metrics.detection_rate == 50.0


class TestDecisionEngine:
    def test_cull_decision(self):
        params = EvolutionParameters()
        params.fitness_threshold_cull = 20.0
        engine = DecisionEngine(params)

        metrics = FitnessMetrics(agent_id="test", overall_fitness=10.0)
        decision = engine.decide_for_agent("test", metrics, [])

        assert decision.type == DecisionType.CULL

    def test_mutate_decision(self):
        params = EvolutionParameters()
        params.fitness_threshold_keep = 30.0
        engine = DecisionEngine(params)

        metrics = FitnessMetrics(agent_id="test", overall_fitness=25.0)
        decision = engine.decide_for_agent("test", metrics, [])

        assert decision.type == DecisionType.MUTATE

    def test_promote_decision(self):
        params = EvolutionParameters()
        params.fitness_threshold_promote = 70.0
        engine = DecisionEngine(params)

        metrics = FitnessMetrics(agent_id="test", overall_fitness=85.0)
        decision = engine.decide_for_agent("test", metrics, [])

        assert decision.type == DecisionType.PROMOTE

    def test_starvation_detection(self):
        params = EvolutionParameters()
        params.starvation_days = 1
        engine = DecisionEngine(params)

        history = [{
            "success": True,
            "timestamp": datetime.now() - timedelta(days=2),
        }]

        metrics = FitnessMetrics(agent_id="test", overall_fitness=50.0)
        decision = engine.decide_for_agent("test", metrics, history)

        assert decision.type == DecisionType.CULL
