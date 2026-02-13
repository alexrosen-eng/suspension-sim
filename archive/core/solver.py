import numpy as np
from scipy.optimize import least_squares

class Solver:

    def __init__(self, suspension):
        self.suspension = suspension

    def solve(self):
        x0 = []
        for p in self.suspension.points:
            if not p.fixed:
                x0.extend(p.position)

        x0 = np.array(x0)


        def residuals(vars):
            i=0
            for p in self.suspension.points:
                if not p.fixed:
                    p.position = vars[i:i+3]
                    i += 3
            return self.suspension.constraints()

        sol = least_squares(residuals, x0)

        return sol