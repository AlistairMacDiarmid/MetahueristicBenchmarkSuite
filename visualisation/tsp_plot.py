import matplotlib.pyplot as plt
import numpy as np


def plot_route(cities: np.ndarray, route: np.ndarray, seed: int, title: str = "TSP route"):
    ordered_cities = cities[route]
    closed_route = np.vstack((ordered_cities, ordered_cities[0]))

    plt.figure(figsize=(10, 10))

    plt.plot(
        closed_route[:, 0],
        closed_route[:, 1],
        color ="steelblue",
        linewidth = 1.25,
        marker = "o",
        markersize = 8,
        markerfacecolor = "red",
        markeredgecolor = "black",
    )

    for i, (x, y) in enumerate(cities):
        plt.text(x + 1, y + 1, str(i), fontsize=9)

    plt.title(f"{title} | Seed = {seed}")
    plt.xlabel("x coordinate")
    plt.ylabel("y coordinate")
    plt.grid(True)
    plt.show()


def plot_mean_convergence(
    mean_histories: dict[str, np.ndarray],
    title: str = "mean convergence across seeds"
):
    plt.figure(figsize=(10, 10))

    for algorithm_name, history in mean_histories.items():
        plt.plot(history, label=algorithm_name)

    plt.title(title)
    plt.xlabel("iteration / generation")
    plt.ylabel("mean best distance (cost)")
    plt.grid(True)
    plt.legend()

    plt.show()

def plot_boxplots(
    algorithm_costs: dict[str, list[float]],
    algorithm_runtimes: dict[str, list[float]]
):
    algorithm_names = list(algorithm_costs.keys())

    cost_data = [algorithm_costs[name] for name in algorithm_names]
    runtime_data = [algorithm_runtimes[name] for name in algorithm_names]

    plt.figure(figsize=(8, 6))
    plt.boxplot(cost_data, tick_labels=algorithm_names)
    plt.title("final cost distribution across seeds")
    plt.ylabel("best distance (cost)")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.boxplot(runtime_data, tick_labels=algorithm_names)
    plt.title("runtime distribution across seeds")
    plt.ylabel("runtime (seconds)")
    plt.grid(True)
    plt.show()

def plot_violinplots(
    algorithm_costs: dict[str, list[float]],
    algorithm_runtimes: dict[str, list[float]]
):
    algorithm_names = list(algorithm_costs.keys())

    cost_data = [algorithm_costs[name] for name in algorithm_names]
    runtime_data = [algorithm_runtimes[name] for name in algorithm_names]

    plt.figure(figsize=(8, 6))
    plt.violinplot(
        cost_data,
        showmeans=True,
        showmedians=True
    )
    plt.xticks(range(1, len(algorithm_names) + 1), algorithm_names)
    plt.title("cost distribution density across seeds")
    plt.ylabel("best distance (cost)")
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.violinplot(
        runtime_data,
        showmeans=True,
        showmedians=True
    )
    plt.xticks(range(1, len(algorithm_names) + 1), algorithm_names)
    plt.title("runtime distribution density across seeds")
    plt.ylabel("runtime (seconds)")
    plt.grid(True)
    plt.show()