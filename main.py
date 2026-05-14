from problems.TSPProblem import TSPProblem
from algorithms.hill_climber import HillClimber
from algorithms.simulated_annealing import SimulatedAnnealing
from visualisation.tsp_plot import plot_route, plot_convergence_comparison, plot_mean_convergence
import numpy as np
import csv


def main():
    seeds = [16,27,28,67,69,300,420,710,1337,12345]
    num_cities = 20
    max_iterations = 10000
    initial_temp = 1000
    cooling_rate = 0.995
    min_temp = 0.001

    hc_costs = []
    sa_costs = []
    best_hc_run = None
    best_sa_run = None
    hc_history = []
    sa_history = []
    results = []

    for seed in seeds:
        print(f"\nseed running: {seed}")

        problem = TSPProblem.generate_random(
            num_cities=num_cities,
            seed=seed
        )

        initial_route = problem.generate_initial_solution(seed=seed)
        initial_distance = problem.evaluate(initial_route)

        hill_climber = HillClimber(
            max_iterations=max_iterations,
            seed=seed,
            neighbour_strategy="two_opt"
        )

        hc_result = hill_climber.optimise(problem)

        simulated_annealing = SimulatedAnnealing(
            max_iterations=max_iterations,
            seed=seed,
            neighbour_strategy="two_opt",
            initial_temperature=initial_temp,
            cooling_rate=cooling_rate,
            min_temperature=min_temp
        )

        sa_result = simulated_annealing.optimise(problem)

        hc_costs.append(hc_result["best_cost"])
        sa_costs.append(sa_result["best_cost"])
        hc_history.append(hc_result["history"])
        sa_history.append(sa_result["history"])

        results.append({
            "seed": seed,
            "algorithm": "HillClimber",
            "best_cost": hc_result["best_cost"],
            "iterations": max_iterations,
            "neighbour_strategy": "two_opt",
            "initial_temperature": "",
            "cooling_rate": "",
            "min_temperature": ""
        })
        results.append({
            "seed": seed,
            "algorithm": "SimulatedAnnealing",
            "best_cost": sa_result["best_cost"],
            "iterations": max_iterations,
            "initial_temperature": initial_temp,
            "cooling_rate": cooling_rate,
            "min_temperature": min_temp,
            "neighbour_strategy": "two_opt"
        })

        print(f"Initial Distance: {initial_distance:.2f}")
        print(f"HC Best Distance: {hc_result['best_cost']:.2f}")
        print(f"SA Best Distance: {sa_result['best_cost']:.2f}")

        if best_hc_run is None or hc_result["best_cost"] < best_hc_run["result"]["best_cost"]:
            best_hc_run = {
                "seed": seed,
                "problem": problem,
                "initial_route": initial_route,
                "initial_distance": initial_distance,
                "result": hc_result
            }

        if best_sa_run is None or sa_result["best_cost"] < best_sa_run["result"]["best_cost"]:
            best_sa_run = {
                "seed": seed,
                "problem": problem,
                "initial_route": initial_route,
                "initial_distance": initial_distance,
                "result": sa_result
            }

    mean_hc_history = np.mean(hc_history, axis=0)
    mean_sa_history = np.mean(sa_history, axis=0)

    print("Summary Statistics")
    print("\nHill Climber")
    print(f"Mean: {np.mean(hc_costs):.2f}")
    print(f"Std:  {np.std(hc_costs):.2f}")
    print(f"Best: {np.min(hc_costs):.2f}")
    print(f"Worst:{np.max(hc_costs):.2f}")

    print("\nSimulated Annealing")
    print(f"Mean: {np.mean(sa_costs):.2f}")
    print(f"Std:  {np.std(sa_costs):.2f}")
    print(f"Best: {np.min(sa_costs):.2f}")
    print(f"Worst:{np.max(sa_costs):.2f}")

    plot_route(
        best_hc_run["problem"].cities,
        best_hc_run["result"]["best_solution"],
        seed=best_hc_run["seed"],
        title=f"best HC TSP route - distance: {best_hc_run['result']['best_cost']:.2f}"
    )

    plot_route(
        best_sa_run["problem"].cities,
        best_sa_run["result"]["best_solution"],
        seed=best_sa_run["seed"],
        title=f"best SA TSP route - distance: {best_sa_run['result']['best_cost']:.2f}"
    )

    plot_convergence_comparison(
        hc_history=best_hc_run["result"]["history"],
        sa_history=best_sa_run["result"]["history"],
        title="best run convergence comparison"
    )

    plot_mean_convergence(
        mean_hc_history,
        mean_sa_history,
        title="mean convergence across seeds"
    )

    with open("results/tsp_results.csv", mode="w", newline="") as f:
        fieldnames = [
            "seed",
            "algorithm",
            "best_cost",
            "iterations",
            "neighbour_strategy",
            "initial_temperature",
            "cooling_rate",
            "min_temperature"
        ]

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    main()