import numpy as np

class TSPProblem:
    """
    class to represent and evaluate TSP problem

    class handles the generation of city coordinates, route distance,
    calculations, and the creation of neighbouring solutions for optimisation

    attributes:
        cities (np.ndarray): an array of (x,y) coordinates for each city
        num_cities (int): the number of cities in the problem instance


    """

    def __init__(self, city: np.ndarray):
        """
        initialises the problem with specified city coordinates
        :param city: a numpy array of (x,y) coordinates to represent each city location.
        """
        #store coordinates matrix and derive the problem size
        self.cities = city
        self.num_cities = len(city)

    @staticmethod
    def generate_random(num_cities: int, seed: int = None):
        """
        create a random tsp instance with cities placed in a 2d space.
        :param num_cities: the number of cities in the problem instance to generate
        :param seed: optional seed for reproducibility
        :return: a new instance of tspproblem
        """
        #recommended generator for numpy random operations
        rng = np.random.default_rng(seed)
        #generate coordinates within a 0-100 bounding box
        cities = rng.uniform(low=0, high=100, size=(num_cities,2))
        return TSPProblem(cities)

    def generate_initial_solution(self, seed:int = None):
        """
        generate a random initial solution by randomly shuffling the city indices
        :param seed: optional seed for reproducibility
        :return: a numpy array representing a random perturbation of city indices
        """
        rng = np.random.default_rng(seed)
        #create random path that visits every city once
        return rng.permutation(self.num_cities)

    def evaluate(self, route: np.ndarray) -> float:
        """
        calculate the total Euclidean distance of the provided route.
        :param route: an array of indices representing the order of travel
        :return: the sum of distances between consecutive cities in route
        """
        #reorder city coordinates based on provided route indices
        ordered_cities = self.cities[route]

        closed_route = np.vstack([ordered_cities, ordered_cities[0]])

        #calculate the Euclidean distance between each consecutive point
        #use of diff to compute the difference between adjacent elements along the axis.
        distances = np.sqrt(
            np.sum(
                np.diff(closed_route, axis=0) ** 2,
                axis=1))

        return distances.sum()



