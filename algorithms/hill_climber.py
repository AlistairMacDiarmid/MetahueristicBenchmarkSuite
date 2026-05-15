import numpy as np
from core.optimisation_result import OptimisationResult


class HillClimber:
    """
    Basic hill climber for minimisation problems.

    Supported neighbour strategies:
    - swap: swaps two cities
    - two_opt: reverses a route segment
    """

    def __init__(
        self,
        max_iterations: int = 1000,
        seed: int | None = None,
        neighbour_strategy: str = "swap"
    ):
        self.max_iterations = max_iterations
        self.seed = seed
        self.neighbour_strategy = neighbour_strategy

    def _swap_neighbour(self, route: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        neighbour = route.copy()

        i, j = rng.choice(len(neighbour), size=2, replace=False)
        neighbour[i], neighbour[j] = neighbour[j], neighbour[i]

        return neighbour

    def _two_opt_neighbour(self, route: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        neighbour = route.copy()

        i, j = sorted(rng.choice(len(neighbour), size=2, replace=False))

        # Reverse the segment between i and j
        neighbour[i:j + 1] = neighbour[i:j + 1][::-1]

        return neighbour

    def _generate_neighbour(self, route: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        if self.neighbour_strategy == "swap":
            return self._swap_neighbour(route, rng)

        if self.neighbour_strategy == "two_opt":
            return self._two_opt_neighbour(route, rng)

        raise ValueError(f"Unknown neighbour strategy: {self.neighbour_strategy}")

    def optimise(self, problem):
        rng = np.random.default_rng(self.seed)

        current_solution = problem.generate_initial_solution(seed=self.seed)
        current_cost = problem.evaluate(current_solution)

        best_solution = current_solution.copy()
        best_cost = current_cost

        history = [best_cost]

        for _ in range(self.max_iterations):
            neighbour = self._generate_neighbour(current_solution, rng)
            neighbour_cost = problem.evaluate(neighbour)

            if neighbour_cost < current_cost:
                current_solution = neighbour
                current_cost = neighbour_cost

                if current_cost < best_cost:
                    best_solution = current_solution.copy()
                    best_cost = current_cost

            history.append(best_cost)

        return OptimisationResult(
            best_solution = best_solution,
            best_cost = best_cost,
            history = history
        )
