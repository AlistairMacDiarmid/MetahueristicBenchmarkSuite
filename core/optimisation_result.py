from ast import List
from dataclasses import dataclass
import numpy as np


@dataclass
class OptimisationResult:
    best_solution: np.ndarray
    best_cost: float
    history: List[float]
    runtime_seconds: float = 0.0


