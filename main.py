import csv
import numpy as np

from experiments.experiment_runner import ExperimentRunner

from algorithms.hill_climber import HillClimber
from algorithms.simulated_annealing import SimulatedAnnealing

from core.algorithm_config import AlgorithmConfig

from visualisation.tsp_plot import (
    plot_route,
    plot_mean_convergence,
    plot_boxplots,
    plot_violinplots
)


def save_results_to_csv(results: list[dict], output_path: str):
    fieldnames = sorted({
        key
        for row in results
        for key in row.keys()
    })

    with open(output_path, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)


def print_summary_statistics(
    algorithm_costs: dict,
    algorithm_runtimes: dict
):
    print("\nSummary Statistics")

    for algorithm_name in algorithm_costs:
        costs = algorithm_costs[algorithm_name]
        runtimes = algorithm_runtimes[algorithm_name]

        print(f"\n{algorithm_name}")

        print(f"Mean Cost: {np.mean(costs):.2f}")
        print(f"Std Cost:  {np.std(costs):.2f}")
        print(f"Best Cost: {np.min(costs):.2f}")
        print(f"Worst Cost:{np.max(costs):.2f}")

        print(f"Mean Runtime: {np.mean(runtimes):.4f}s")


def main():
    seeds = [16, 27, 28, 67, 69, 300, 420, 710, 1337, 12345]

    algorithm_configs = [
        AlgorithmConfig(
            name="HillClimber",
            algorithm_class=HillClimber,
            parameters={
                "max_iterations": 10000,
                "neighbour_strategy": "two_opt"
            }
        ),

        AlgorithmConfig(
            name="SimulatedAnnealing",
            algorithm_class=SimulatedAnnealing,
            parameters={
                "max_iterations": 10000,
                "neighbour_strategy": "two_opt",
                "initial_temperature": 1000.0,
                "cooling_rate": 0.995,
                "min_temperature": 0.001
            }
        )
    ]

    runner = ExperimentRunner(
        seeds=seeds,
        num_cities=20,
        algorithm_configs=algorithm_configs
    )

    experiment_data = runner.run()

    results = experiment_data["results"]

    algorithm_costs = experiment_data["algorithm_costs"]
    algorithm_runtimes = experiment_data["algorithm_runtimes"]
    algorithm_histories = experiment_data["algorithm_histories"]

    best_runs = experiment_data["best_runs"]

    save_results_to_csv(
        results,
        output_path="results/tsp_results.csv"
    )

    print_summary_statistics(
        algorithm_costs,
        algorithm_runtimes
    )


    for algorithm_name, run_data in best_runs.items():
        plot_route(
            run_data["problem"].cities,
            run_data["result"].best_solution,
            seed=run_data["seed"],
            title=f"{algorithm_name} Best Route - Distance: {run_data['result'].best_cost:.2f}"
        )

    mean_histories = {}
    for algorithm_name in algorithm_histories:
        mean_histories[algorithm_name] = np.mean(
            algorithm_histories[algorithm_name],
            axis=0
        )

    hc_mean = mean_histories["HillClimber"]
    sa_mean = mean_histories["SimulatedAnnealing"]

    plot_mean_convergence(
        hc_mean,
        sa_mean,
        title="Mean Convergence Across Seeds"
    )

    plot_boxplots(
        algorithm_costs["HillClimber"],
        algorithm_costs["SimulatedAnnealing"],
        algorithm_runtimes["HillClimber"],
        algorithm_runtimes["SimulatedAnnealing"]
    )

    plot_violinplots(
        algorithm_costs["HillClimber"],
        algorithm_costs["SimulatedAnnealing"],
        algorithm_runtimes["HillClimber"],
        algorithm_runtimes["SimulatedAnnealing"]
    )


if __name__ == "__main__":
    main()