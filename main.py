from problems.TSPProblem import TSPProblem
from algorithms.hill_climber import HillClimber
from visualisation.tsp_plot import plot_route, plot_convergence


def main():

    seed = 28
    num_cities = 20
    problem = TSPProblem.generate_random(num_cities=num_cities, seed=seed)

    initial_route = problem.generate_initial_solution(seed=seed)
    initial_distance = problem.evaluate(initial_route)

    optimiser = HillClimber(max_iterations=1000, seed = seed, neighbour_strategy="two_opt")
    result = optimiser.optimise(problem)

    print("Initial distance:")
    print(initial_distance)

    print("\nBest distance:")
    print(result["best_cost"])

    print("\nBest route:")
    print(result["best_solution"])

    plot_route(
        problem.cities,
        initial_route,
        seed=seed,
        title=f"Initial TSP Route - Distance: {initial_distance:.2f}"

    )

    plot_route(
        problem.cities,
        result["best_solution"],
        seed=seed,
        title=f"Optimised TSP Route - Distance: {result['best_cost']:.2f}"
    )

    plot_convergence(result["history"], seed = seed)


if __name__ == "__main__":
    main()