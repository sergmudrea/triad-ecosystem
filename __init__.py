# src/__init__.py

"""TRIAD Ecosystem - Self-evolving autonomous cyber ecosystem."""

__version__ = "2.0.0"
__author__ = "Z3R0"
__license__ = "MIT"

from src.core.meta_memory import MetaMemory
from src.core.replicator import ReplicationEngine
from src.agents.black_agent import BlackAgent
from src.agents.red_agent import RedAgent
from src.agents.blue_agent import BlueAgent
from src.evolution.parameters import EvolutionParameters

__all__ = [
    "MetaMemory",
    "ReplicationEngine",
    "BlackAgent",
    "RedAgent",
    "BlueAgent",
    "EvolutionParameters",
]
