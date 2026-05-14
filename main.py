import csv
import numpy as np

from experiments.experiment_runner import ExperimentRunner

from visualisation.tsp_plot import (
    plot_route,
    plot_convergence_comparison,
    plot_mean_convergence,
    plot_boxplots,
    plot_violinplots
)


def save_results_to_csv(results: list[dict], output_path: str):
    fieldnames = [
        "seed",
        "algorithm",
        "best_cost",
        "iterations",
        "neighbour_strategy",
        "initial_temperature",
        "cooling_rate",
        "min_temperature",
        "runtime_seconds"
    ]

    with open(output_path, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def print_summary_statistics(
    hc_costs: list[float],
    sa_costs: list[float],
    hc_runtimes: list[float],
    sa_runtimes: list[float]
):
    print("\nSummary Statistics")

    print("\nHill Climber")
    print(f"Mean: {np.mean(hc_costs):.2f}")
    print(f"Std:  {np.std(hc_costs):.2f}")
    print(f"Best: {np.min(hc_costs):.2f}")
    print(f"Worst:{np.max(hc_costs):.2f}")
    print(f"Mean Runtime: {np.mean(hc_runtimes):.4f}s")

    print("\nSimulated Annealing")
    print(f"Mean: {np.mean(sa_costs):.2f}")
    print(f"Std:  {np.std(sa_costs):.2f}")
    print(f"Best: {np.min(sa_costs):.2f}")
    print(f"Worst:{np.max(sa_costs):.2f}")
    print(f"Mean Runtime: {np.mean(sa_runtimes):.4f}s")


def main():
    seeds = [16, 27, 28, 67, 69, 300, 420, 710, 1337, 12345]

    runner = ExperimentRunner(
        seeds=seeds,
        num_cities=20,
        max_iterations=10000,
        neighbour_strategy="two_opt",
        initial_temperature=1000.0,
        cooling_rate=0.995,
        min_temperature=0.001
    )

    experiment_data = runner.run()

    results = experiment_data["results"]

    hc_costs = experiment_data["hc_costs"]
    sa_costs = experiment_data["sa_costs"]

    hc_runtimes = experiment_data["hc_runtimes"]
    sa_runtimes = experiment_data["sa_runtimes"]

    hc_histories = experiment_data["hc_histories"]
    sa_histories = experiment_data["sa_histories"]

    best_hc_run = experiment_data["best_hc_run"]
    best_sa_run = experiment_data["best_sa_run"]

    mean_hc_history = np.mean(hc_histories, axis=0)
    mean_sa_history = np.mean(sa_histories, axis=0)

    print_summary_statistics(
        hc_costs,
        sa_costs,
        hc_runtimes,
        sa_runtimes
    )

    save_results_to_csv(
        results,
        output_path="results/tsp_results.csv"
    )

    plot_route(
        best_hc_run["problem"].cities,
        best_hc_run["result"]["best_solution"],
        seed=best_hc_run["seed"],
        title=f"Best HC TSP Route - Distance: {best_hc_run['result']['best_cost']:.2f}"
    )

    plot_route(
        best_sa_run["problem"].cities,
        best_sa_run["result"]["best_solution"],
        seed=best_sa_run["seed"],
        title=f"Best SA TSP Route - Distance: {best_sa_run['result']['best_cost']:.2f}"
    )

    plot_convergence_comparison(
        hc_history=best_hc_run["result"]["history"],
        sa_history=best_sa_run["result"]["history"],
        title="Best Run Convergence Comparison"
    )

    plot_mean_convergence(
        mean_hc_history,
        mean_sa_history,
        title="Mean Convergence Across Seeds"
    )

    plot_boxplots(
        hc_costs,
        sa_costs,
        hc_runtimes,
        sa_runtimes
    )

    plot_violinplots(
        hc_costs,
        sa_costs,
        hc_runtimes,
        sa_runtimes
    )


if __name__ == "__main__":
    main()