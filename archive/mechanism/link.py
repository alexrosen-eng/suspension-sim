import numpy as np

class Link:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.length = np.linalg.norm(self.p2.position - self.p1.position)

    def constraint(self):
        return np.linalg.norm(self.p2.position - self.p1.position) - self.length
    
    