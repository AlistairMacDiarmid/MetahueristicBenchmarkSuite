from problems.TSPProblem import TSPProblem
from algorithms.hill_climber import HillClimber
from algorithms.simulated_annealing import SimulatedAnnealing
import time

class ExperimentRunner:
    def __init__(
        self,
        seeds: list[int],
        num_cities: int,
        max_iterations: int,
        neighbour_strategy: str = "two_opt",
        initial_temperature: float = 1000.0,
        cooling_rate: float = 0.995,
        min_temperature: float = 0.001
    ):
        self.seeds = seeds
        self.num_cities = num_cities
        self.max_iterations = max_iterations
        self.neighbour_strategy = neighbour_strategy
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature

    def run(self):
        hc_costs = []
        sa_costs = []

        hc_runtimes = []
        sa_runtimes = []

        hc_histories = []
        sa_histories = []

        results = []

        best_hc_run = None
        best_sa_run = None

        for seed in self.seeds:
            print(f"\nseed running: {seed}")

            problem = TSPProblem.generate_random(
                num_cities=self.num_cities,
                seed=seed
            )

            initial_route = problem.generate_initial_solution(seed=seed)
            initial_distance = problem.evaluate(initial_route)

            hill_climber = HillClimber(
                max_iterations=self.max_iterations,
                seed=seed,
                neighbour_strategy=self.neighbour_strategy
            )

            hc_start = time.perf_counter()
            hc_result = hill_climber.optimise(problem)
            hc_runtime = time.perf_counter() - hc_start

            simulated_annealing = SimulatedAnnealing(
                max_iterations=self.max_iterations,
                seed=seed,
                neighbour_strategy=self.neighbour_strategy,
                initial_temperature=self.initial_temperature,
                cooling_rate=self.cooling_rate,
                min_temperature=self.min_temperature
            )

            sa_start = time.perf_counter()
            sa_result = simulated_annealing.optimise(problem)
            sa_runtime = time.perf_counter() - sa_start

            hc_costs.append(hc_result["best_cost"])
            sa_costs.append(sa_result["best_cost"])

            hc_runtimes.append(hc_runtime)
            sa_runtimes.append(sa_runtime)

            hc_histories.append(hc_result["history"])
            sa_histories.append(sa_result["history"])

            results.append({
                "seed": seed,
                "algorithm": "HillClimber",
                "best_cost": hc_result["best_cost"],
                "iterations": self.max_iterations,
                "neighbour_strategy": self.neighbour_strategy,
                "initial_temperature": "",
                "cooling_rate": "",
                "min_temperature": "",
                "runtime_seconds": hc_runtime
            })

            results.append({
                "seed": seed,
                "algorithm": "SimulatedAnnealing",
                "best_cost": sa_result["best_cost"],
                "iterations": self.max_iterations,
                "neighbour_strategy": self.neighbour_strategy,
                "initial_temperature": self.initial_temperature,
                "cooling_rate": self.cooling_rate,
                "min_temperature": self.min_temperature,
                "runtime_seconds": sa_runtime
            })

            print(f"Initial Distance: {initial_distance:.2f}")
            print(f"HC Best Distance: {hc_result['best_cost']:.2f}")
            print(f"HC runtime: {hc_runtime:.4f}s")
            print(f"SA Best Distance: {sa_result['best_cost']:.2f}")
            print(f"SA runtime: {sa_runtime:.4f}s")

            if best_hc_run is None or hc_result["best_cost"] < best_hc_run["result"]["best_cost"]:
                best_hc_run = {
                    "seed": seed,
                    "problem": problem,
                    "initial_route": initial_route,
                    "initial_distance": initial_distance,
                    "result": hc_result,
                    "runtime_seconds": hc_runtime
                }

            if best_sa_run is None or sa_result["best_cost"] < best_sa_run["result"]["best_cost"]:
                best_sa_run = {
                    "seed": seed,
                    "problem": problem,
                    "initial_route": initial_route,
                    "initial_distance": initial_distance,
                    "result": sa_result,
                    "runtime_seconds": sa_runtime
                }

        return {
            "results": results,
            "hc_costs": hc_costs,
            "sa_costs": sa_costs,
            "hc_runtimes": hc_runtimes,
            "sa_runtimes": sa_runtimes,
            "hc_histories": hc_histories,
            "sa_histories": sa_histories,
            "best_hc_run": best_hc_run,
            "best_sa_run": best_sa_run
        }