from scipy.optimize import least_squares
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

L1 = 1.0


# Initial positons

x0 = np.array([-0.1,0])    # x2, y2

def equality_constraint(vars,p1):
    x2, y2 = vars
    p2 = [x2, y2]

    # distance is constrainted

    eq1 = np.linalg.norm(p1-p2) - L1
    eq2 = y2

    return np.array([eq1, eq2])


# sim loop

n_steps = 100

p1_hist = []
p2_hist = []

x_guess = x0.copy()

for t in range(n_steps):

    p1 = np.array(
        [0, 1 - (1/n_steps) * t]
    )

    sol = least_squares(equality_constraint, x_guess, args=(p1,))

    x2, y2 = sol.x

    # store results

    p1_hist.append(p1)
    p2_hist.append([x2, y2])

    # use previous solution as initial guess for next iteration
    x_guess = sol.x

# convert to arrays for plotting
p1_hist = np.array(p1_hist)
p2_hist = np.array(p2_hist)

