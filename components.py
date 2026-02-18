import numpy as np
from numpy.typing import NDArray


class Frame:
    """
    Point creates a frame to define in the simulation.

    position: [NDArray] to define the initial position
    orientation: [NDArray] to define the orientation of the frame
    designVariable: [bool] Add the frame as a design variable in optimizers
    """

    def __init__(self, position: NDArray[np.float64] | list, orientation: NDArray[np.float64] | list, designVariable = False):
        self.position = np.asarray(position, dtype=float)
        self.orientation = np.asarray(orientation, dtype=float)
        self.designVariable = designVariable



class Body:

    """
    Docstring for Body

    Creates a body object, which is just a collection of frames attached to the body
    """

    def __init__(self, name: str, frames: list) -> None:
        self.name = name
        self.frames = []

    def addPoint(self, frame):
        self.frames.append(frame)
        frame.body = self # assign the associated body to the frame as well



class SphericalJoint:
    def __init__(self, p1: Frame, p2: Frame) -> None:
        self.p1 = p1
        self.p2 = p2
        self.length = np.linalg.norm(p2.position - p1.position) # taking the length from the initial frame definitions to get correct length

    def residual(self) -> float:
        """
        Docstring for residual
        
        :param self: Description

        Defines the difference in the current length and the current length between frames
        """
        return float(np.linalg.norm(self.p2.position - self.p1.position) - self.length)