import matplotlib.pyplot as plt
import numpy as np


def plot_route(cities: np.ndarray, route: np.ndarray, seed: int, title: str = "TSP Route"):
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


def plot_convergence_comparison(
    hc_history: list[float],
    sa_history: list[float],
    title: str = "Convergence Comparison"
):
    plt.figure(figsize=(10, 10))

    plt.plot(hc_history, label="Hill Climber")
    plt.plot(sa_history, label="Simulated Annealing")

    plt.title(title)
    plt.xlabel("iteration")
    plt.ylabel("best distance (cost)")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_mean_convergence(
    mean_hc_history: np.ndarray,
    mean_sa_history: np.ndarray,
    title: str = "Mean Convergence Comparison"
):
    plt.figure(figsize=(10, 10))

    plt.plot(mean_hc_history, label="Hill Climber")
    plt.plot(mean_sa_history, label="Simulated Annealing")

    plt.title(title)
    plt.xlabel("iteration")
    plt.ylabel("mean best distance (cost)")
    plt.grid(True)
    plt.legend()

    plt.show()

def plot_boxplots(
    hc_costs: list[float],
    sa_costs: list[float],
    hc_runtimes: list[float],
    sa_runtimes: list[float]
):

    #cost distribution
    plt.figure(figsize=(8, 6))
    plt.boxplot(
        [hc_costs, sa_costs],
        tick_labels=["Hill Climber", "Simulated Annealing"]
    )
    plt.title("Final Cost Distribution Across Seeds")
    plt.ylabel("best distance (cost)")
    plt.grid(True)
    plt.show()


    #runtime distribution
    plt.figure(figsize=(8, 6))
    plt.boxplot(
        [hc_runtimes, sa_runtimes],
        tick_labels=["Hill Climber", "Simulated Annealing"]
    )
    plt.title("Runtime Distribution Across Seeds")
    plt.ylabel("runtime (seconds)")
    plt.grid(True)
    plt.show()

def plot_violinplots(
    hc_costs: list[float],
    sa_costs: list[float],
    hc_runtimes: list[float],
    sa_runtimes: list[float]
):

    #cost violin plot

    plt.figure(figsize=(8, 6))

    plt.violinplot(
        [hc_costs, sa_costs],
        showmeans=True,
        showmedians=True
    )

    plt.xticks([1, 2], ["Hill Climber", "Simulated Annealing"])

    plt.title("Cost Distribution Density Across Seeds")
    plt.ylabel("best distance (cost)")
    plt.grid(True)

    plt.show()

    #runtime violin plot
    plt.figure(figsize=(8, 6))
    plt.violinplot(
        [hc_runtimes, sa_runtimes],
        showmeans=True,
        showmedians=True
    )
    plt.xticks([1, 2], ["Hill Climber", "Simulated Annealing"])
    plt.title("Runtime Distribution Density Across Seeds")
    plt.ylabel("runtime (seconds)")
    plt.grid(True)

    plt.show()