import numpy as np
from core.optimisation_result import OptimisationResult

class SimulatedAnnealing:


    def __init__(
        self,
        max_iterations: int = 1000,
        seed: int | None = None,
        neighbour_strategy: str = "two_opt",
        initial_temperature: float = 1000.0,
        cooling_rate: float = 0.995,
        min_temperature: float = 0.001
    ):
        self.max_iterations = max_iterations
        self.seed = seed
        self.neighbour_strategy = neighbour_strategy
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature


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

        temperature = self.initial_temperature
        history = [best_cost]

        for _ in range(self.max_iterations):
            neighbour = self._generate_neighbour(current_solution, rng)
            neighbour_cost = problem.evaluate(neighbour)

            delta = neighbour_cost - current_cost

            if delta < 0:
                current_solution = neighbour
                current_cost = neighbour_cost
            else:
                acceptance_probability = np.exp(-delta / temperature)

                if rng.random() < acceptance_probability:
                    current_solution = neighbour
                    current_cost = neighbour_cost

            if current_cost < best_cost:
                best_solution = current_solution.copy()
                best_cost = current_cost

            temperature *= self.cooling_rate
            temperature = max(temperature, self.min_temperature)

            history.append(best_cost)

        return OptimisationResult(
            best_solution=best_solution,
            best_cost=best_cost,
            history=history
        )



