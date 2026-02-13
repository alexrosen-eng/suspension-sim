import numpy as np

class Point:

    def __init__(self, name, position, fixed=False):
        self.name = name
        self.position = np.array(position, dtype=float)
        self.fixed = fixed

    def set_position(self, new_pos):
        if not self.fixed:
            self.position = np.array(new_pos, dtype=float)