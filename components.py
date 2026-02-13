import numpy as np
from numpy.typing import NDArray


class Point:

    def __init__(self, position, body=False, fixed=False):
        self.position = position
        self.body = body
        self.fixed = fixed



class Body:

    """
    Docstring for Body

    Creates a body object, which is just a collection of points attached to the body
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.points = []

    def addPoint(self, point):
        self.points.append(point)
        point.body = self # assign the associated body to the point as well



class DistanceConstraint:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2
        self.length = np.linalg.norm(p2.position - p1.position) # taking the length from the initial point definitions to get correct length

    def residual(self) -> float:
        """
        Docstring for residual
        
        :param self: Description

        Defines the difference in the current length and the current length between points
        """
        return float(np.linalg.norm(self.p2.position - self.p1.position) - self.length)