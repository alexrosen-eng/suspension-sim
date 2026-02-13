import numpy as np
from mechanism.point import Point
from mechanism.link import Link
from mechanism.suspension import Suspension
from core.solver import Solver
from core.history import History
from visualization.plot2D import Plot2D

# create suspension
sus = Suspension()

# Ground Point (fixed)
p_ground = Point("ground", [0, 0, 0], fixed=True)

# Moving Point
p_free = Point("free", [1,0,0])


# Add to mechanism
sus.add_point(p_ground)
sus.add_point(p_free)

# Link between them
link = Link(p_ground, p_free)
sus.add_link(link)


#create solver
solver = Solver(sus)
hist = History(sus)

# Simulation Loop
n_steps = 50

for step in range(n_steps):

    # move ground up slightly
    p_ground.position = np.array([0, step*0.02, 0])

    # Solve new config.
    solver.solve()
    hist.record()

    print("Step:", step)
    print("Ground:", p_ground.position)
    print("Free:", p_free.position)
    print()


p_free_traj = hist.get_point_trajectory("free")
p_ground_traj = hist.get_point_trajectory("ground")
x_vals = p_free_traj[:,0]
y_vals = p_free_traj[:,1]
x = p_ground_traj[:,0]
y = p_ground_traj[:,1]

# simple plot
import matplotlib.pyplot as plt
plt.plot(x_vals, y_vals)
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Trajectory of free point")
plt.show()