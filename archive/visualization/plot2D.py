import matplotlib.pyplot as plt

class Plot2D:

    def __init__(self, mechanism):
        self.mechanism = mechanism
        self.fig, self.ax = plt.subplots()

    def update(self):
        self.ax.clear()

        # plot points
        for p in self.mechanism.points:
            x, y, z = p.position
            self.ax.scatter(x, y)

        # plot links
        for c in self.mechanism.constraints:
            if hasattr(c, "p1"):
                xs = [c.p1.position[0], c.p2.position[0]]
                ys = [c.p1.position[1], c.p2.position[1]]
                self.ax.plot(xs, ys)

        self.ax.set_aspect("equal")
        plt.pause(0.01)