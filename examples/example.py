import pso_viz


class MyProblem:
    def fitness(self, X):
        return [(1.0 - X[0])**2 + 100. * (X[1] - X[0]**2)**2]

    def get_bounds(self):
        return ([-2, -1], [2, 5])


pso_viz.open_gui_for_problem(MyProblem())
