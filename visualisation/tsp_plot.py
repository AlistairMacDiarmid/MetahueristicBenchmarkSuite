import matplotlib.pyplot as plt
import numpy as np


def plot_route(cities: np.ndarray, route: np.ndarray, seed: int, title: str = "TSP Route"):
    ordered_cities = cities[route]
    closed_route = np.vstack((ordered_cities, ordered_cities[0]))

    plt.figure(figsize=(10, 10))
    plt.plot(closed_route[:, 0], closed_route[:, 1], marker="o", markersize=5, color="red")
    plt.title(f"{title} | Seed = {seed}")
    plt.xlabel("x coordinate")
    plt.ylabel("y coordinate")
    plt.grid(True)
    plt.show()


def plot_convergence(history: list[float], seed: int, title: str = "Hill Climber Convergence"):
    plt.figure(figsize=(10, 10))
    plt.plot(history)
    plt.title(f"{title} | Seed = {seed}")
    plt.xlabel("iteration")
    plt.ylabel("best distance (cost)")
    plt.grid(True)
    plt.show()