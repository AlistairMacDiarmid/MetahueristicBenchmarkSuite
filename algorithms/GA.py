import numpy as np
from core.optimisation_result import OptimisationResult

class GeneticAlgorithm:

    def __init__(
            self,
            population_size: int = 100,
            generations: int = 300,
            tournament_size: int = 3,
            crossover_rate: float = 0.9,
            mutation_rate: float = 0.1,
            elitism: bool = True,
            seed: int | None = None
    ):
        self.population_size = population_size
        self.generations = generations
        self.tournament_size = tournament_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.seed = seed


    def initialise_population(self, problem, rng: np.random.Generator) -> list[np.ndarray]:
        return [
            problem.generate_initial_solution(seed=int(rng.integers(0,1_000_000)))
            for _ in range(self.population_size)
        ]

    def _tournament_selection(
            self,
            population: list[np.ndarray],
            fitness_value: list[float],
            rng: np.random.Generator) -> np.ndarray:

        selected_indices = rng.choice(
            len(population),
            size=self.tournament_size,
            replace=False
        )

        best_index = min(selected_indices, key=lambda ind: fitness_value[ind])

        return population[best_index].copy()

    def _ordered_crossover(
            self,
            parent_a : np.ndarray,
            parent_b : np.ndarray,
            rng: np.random.Generator
    ) -> np.ndarray:
        size = len(parent_a)
        child  = np.full(size, -1)

        start, end = sorted(rng.choice(size, size=2, replace=False))

        child[start:end + 1] = parent_a[start:end + 1]

        fill_values = [
            city for city in parent_b
            if city not in child
        ]

        fill_index = 0

        for i in range(size):
            if child[i] == -1:
                child[i] = fill_values[fill_index]
                fill_index += 1

        return child

    def _mutate(self, route: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        mutated = route.copy()
        if rng.random() < self.mutation_rate:
            i, j = rng.choice(len(mutated), size=2, replace=False)
            mutated[i], mutated[j] = mutated[j], mutated[i]
        return mutated


    def optimise(self, problem)-> OptimisationResult:
        rng = np.random.default_rng(self.seed)
        population = self.initialise_population(problem, rng)
        fitness_values = [problem.evaluate(route) for route in population]

        best_index = int(np.argmin(fitness_values))
        best_solution = population[best_index].copy()
        best_cost = fitness_values[best_index]

        history = [best_cost]

        for _ in range(self.generations):
            new_population = []

            if self.elitism:
                new_population.append(best_solution.copy())

            while len(new_population) < self.population_size:
                parent_a = self._tournament_selection(population, fitness_values, rng)
                parent_b = self._tournament_selection(population, fitness_values, rng)

                if rng.random() < self.crossover_rate:
                    child = self._ordered_crossover(parent_a, parent_b, rng)
                else:
                    child = parent_a.copy()

                child = self._mutate(child, rng)
                new_population.append(child)

            population = new_population
            fitness_values = [problem.evaluate(route) for route in population]

            generation_best_index = int(np.argmin(fitness_values))
            generation_best_cost = fitness_values[generation_best_index]

            if generation_best_cost < best_cost:
                best_cost = generation_best_cost
                best_solution = population[generation_best_index].copy()

                history.append(best_cost)

        return OptimisationResult(
            best_solution = best_solution,
            best_cost = best_cost,
            history = history
            )