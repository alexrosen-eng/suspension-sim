import numpy as np

class History:
    def __init__(self, suspension):
        self.data = []
        self.suspension = suspension

    def record(self):
        snapshot = {}
        for p in self.suspension.points:
            snapshot[p.name] = p.position.copy()
        self.data.append(snapshot)

    def get_point_trajectory(self, point_name):
        return np.array([snap[point_name] for snap in self.data])