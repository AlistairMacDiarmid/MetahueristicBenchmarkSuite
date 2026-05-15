from problems.TSPProblem import TSPProblem
from algorithms.hill_climber import HillClimber
from algorithms.simulated_annealing import SimulatedAnnealing
from core.algorithm_config import AlgorithmConfig
from typing import Optional
import time

class ExperimentRunner:
    def __init__(
        self,
        seeds: list[int],
        num_cities: int,
        algorithm_configs: list[AlgorithmConfig]
    ):
        self.seeds = seeds
        self.num_cities = num_cities
        self.algorithm_configs = algorithm_configs

    def run(self):

        algorithm_costs = {}
        algorithm_runtimes = {}
        algorithm_histories = {}

        best_runs = {}

        results = []

        best_hc_run: Optional[dict] = None
        best_sa_run: Optional[dict] = None

        for config in self.algorithm_configs:
            algorithm_costs[config.name] = []
            algorithm_runtimes[config.name] = []
            algorithm_histories[config.name] = []
            best_runs[config.name] = None

        for seed in self.seeds:
            print(f"\nseed running: {seed}")

            problem = TSPProblem.generate_random(
                num_cities=self.num_cities,
                seed=seed
            )

            initial_route = problem.generate_initial_solution(seed=seed)
            initial_distance = problem.evaluate(initial_route)

            print(f"Initial Distance: {initial_distance:.2f}")

            for config in self.algorithm_configs:
                optimiser = config.algorithm_class(
                    seed = seed,
                    **config.parameters
                )

                start_time = time.perf_counter()

                result = optimiser.optimise(problem)

                run_time = time.perf_counter() - start_time

                result.runtime_seconds = run_time

                algorithm_costs[config.name].append(result.best_cost)
                algorithm_runtimes[config.name].append(result.runtime_seconds)
                algorithm_histories[config.name].append(result.history)

                print(f"{config.name} best distance: {result.best_cost:.2f}")
                print(f"{config.name} runtime: {run_time:.4f}")

                results.append({
                    "seed": seed,
                    "algorithm": config.name,
                    "best_cost": result.best_cost,
                    "runtime_seconds": result.runtime_seconds,
                    **config.parameters
                })

                current_best = best_runs[config.name]

                if current_best is None or result.best_cost < current_best["result"].best_cost:
                    best_runs[config.name] = {
                        "seed": seed,
                        "problem": problem,
                        "initial_route": initial_route,
                        "initial_distance": initial_distance,
                        "result": result,
                    }

        return {
            "results": results,
            "algorithm_costs": algorithm_costs,
            "algorithm_runtimes": algorithm_runtimes,
            "algorithm_histories": algorithm_histories,
            "best_runs": best_runs
        }