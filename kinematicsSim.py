from components import Body, 
import numpy as np
from scipy.optimize import least_squares

SOLVER = least_squares


def kinematicsSim(frontSusp:  ):


    frontSuspension = np.array([
        [x1, y1, z1],
        [x2, y2, z2],
        []
    ])

    def residuals(x):
        pass



    n = 20

    for step in range(n):

        sol = 


if __name__ == "__main__":
    kinematicsSim()