# src/evolution/reporting.py

"""Evolution reporting and report generation."""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional


@dataclass
class EvolutionReport:
    """Complete evolution report."""

    generation: int
    duration_hours: float
    population_stats: Dict[str, float]
    fitness_stats: Dict[str, float]
    diversity_stats: Dict[str, float]
    successful_promotions: int
    total_mutations: int
    elite_agents: List[str]
    recommendations: List[str]
    timestamp: str


class ReportGenerator:
    """Generates comprehensive evolution reports."""

    def __init__(self, memory):
        self.memory = memory

    async def generate_report(self) -> EvolutionReport:
        """Generate current evolution state report."""
        state = await self.memory.get("evolution:state") or {}
        params = await self.memory.get("evolution:parameters") or {}

        # Get fitness history
        fitness_keys = await self.memory.search("fitness:")
        fitness_values = []
        for key in fitness_keys[-100:]:
            val = await self.memory.get(key)
            if val and isinstance(val, (int, float)):
                fitness_values.append(val)
            elif val and isinstance(val, dict):
                fitness_values.append(val.get("overall_fitness", 0))

        # Calculate statistics
        avg_fitness = sum(fitness_values) / len(fitness_values) if fitness_values else 0
        max_fitness = max(fitness_values) if fitness_values else 0
        min_fitness = min(fitness_values) if fitness_values else 0

        if len(fitness_values) > 1:
            variance = sum((f - avg_fitness) ** 2 for f in fitness_values) / len(fitness_values)
            std_fitness = variance ** 0.5
        else:
            std_fitness = 0

        # Get technique diversity
        all_techniques = set()
        tech_keys = await self.memory.search("technique:")
        for key in tech_keys:
            tech = await self.memory.get(key)
            if tech and isinstance(tech, dict):
                all_techniques.add(tech.get("name", "unknown"))
        technique_diversity = len(all_techniques)

        # Get elite agents
        elite_agents = state.get("elite_agents", [])

        report = EvolutionReport(
            generation=state.get("generation", 0),
            duration_hours=state.get("duration_hours", 0.0),
            population_stats={
                "total": state.get("population_size", 0),
                "min_allowed": params.get("population_min", 5),
                "max_allowed": params.get("population_max", 20),
            },
            fitness_stats={
                "average": round(avg_fitness, 1),
                "maximum": round(max_fitness, 1),
                "minimum": round(min_fitness, 1),
                "std_dev": round(std_fitness, 1),
            },
            diversity_stats={
                "technique_count": technique_diversity,
                "fitness_variance": round(std_fitness, 1),
                "genome_variance": 0,
            },
            successful_promotions=state.get("promotions", 0),
            total_mutations=state.get("mutations", 0),
            elite_agents=elite_agents[:5],
            recommendations=self._generate_recommendations(
                avg_fitness, std_fitness, technique_diversity
            ),
            timestamp=datetime.now().isoformat(),
        )

        return report

    def _generate_recommendations(self, avg_fitness: float, std_fitness: float,
                                  technique_count: int) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        if avg_fitness < 30:
            recommendations.append("Increase mutation rate to escape local optimum")
        elif avg_fitness > 70:
            recommendations.append("Decrease mutation rate to exploit current optimum")

        if std_fitness < 10:
            recommendations.append("Low fitness diversity — increase immigrant rate")
        elif std_fitness > 40:
            recommendations.append("High fitness variance — increase elitism count")

        if technique_count < 20:
            recommendations.append("Low technique diversity — enable exploit fuzzing")

        if not recommendations:
            recommendations.append("Evolution progressing normally")

        return recommendations

    async def save_report(self, report: EvolutionReport, filename: Optional[str] = None) -> str:
        """Save report to file."""
        if not filename:
            filename = f"evolution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, "w") as f:
            json.dump(asdict(report), f, indent=2)

        print(f"📄 Report saved to {filename}")
        return filename

    async def print_report(self, report: EvolutionReport) -> None:
        """Pretty print report to console."""
        print("\n" + "=" * 60)
        print(f"📊 EVOLUTION REPORT - Generation {report.generation}")
        print("=" * 60)

        print("\n📈 FITNESS STATISTICS:")
        print(f"   Average: {report.fitness_stats['average']:.1f}")
        print(f"   Maximum: {report.fitness_stats['maximum']:.1f}")
        print(f"   Minimum: {report.fitness_stats['minimum']:.1f}")
        print(f"   Std Dev: {report.fitness_stats['std_dev']:.1f}")

        print("\n👥 POPULATION:")
        print(f"   Total: {report.population_stats['total']}")
        print(f"   Range: {report.population_stats['min_allowed']} - {report.population_stats['max_allowed']}")

        print("\n🔄 EVOLUTION METRICS:")
        print(f"   Promotions: {report.successful_promotions}")
        print(f"   Mutations: {report.total_mutations}")
        print(f"   Technique Diversity: {report.diversity_stats['technique_count']}")

        if report.recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for rec in report.recommendations:
                print(f"   → {rec}")

        print("=" * 60 + "\n")
