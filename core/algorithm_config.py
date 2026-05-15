from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class AlgorithmConfig:
    name: str
    algorithm_class: Callable
    parameters: dict[str, Any]