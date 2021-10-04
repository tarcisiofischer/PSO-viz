import time
import pygmo as pg


class PSOModelSetup:
    def __init__(self, problem):
        self.n_generations = 10
        self.population_size = 5
        self.inertia = 1
        self.cognitive = 1
        self.social = 1
        self.seed = 1
        self.problem = problem


def pso_run(setup, callback):
    population = pg.population(pg.problem(setup.problem), setup.population_size, seed=setup.seed)
    algorithm = pg.algorithm(
        pg.pso(
            gen=1,
            omega=setup.inertia,
            eta1=setup.cognitive,
            eta2=setup.social,
            seed=setup.seed,
            memory=True,
        )
    )
    for i in range(setup.n_generations):
        population = algorithm.evolve(population)
        callback(i, population.get_x())

        # TODO: Make this user configurable
        time.sleep(0.2)
