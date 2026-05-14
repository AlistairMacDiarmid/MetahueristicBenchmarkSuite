import matplotlib.pyplot as plt
import numpy as np


def plot_route(cities: np.ndarray, route: np.ndarray, seed: int, title: str = "TSP Route"):
    ordered_cities = cities[route]
    closed_route = np.vstack((ordered_cities, ordered_cities[0]))

    plt.figure(figsize=(10, 10))

    plt.plot(
        closed_route[:, 0],
        closed_route[:, 1],
        marker="o",
        markersize=8,
        linewidth=1.5,
        color="red"
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