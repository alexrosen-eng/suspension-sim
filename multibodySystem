import numpy as np
import csv
from components import Body, Point, DistanceConstraint

class MultibodySystem:

    def __init__(self) -> None:
        self.bodies = []
        self.points = []
        self.constraints = []

    def add_body(self, body):
        self.bodies.append(body)

    def add_constraint(self,constraint):
        self.bodies.append(constraint)

    def residuals(self):
        return np.array([c.residual() for c in self.constraints])
    

# def buildSystem():
             
#     system = MultibodySystem()

#     chassis = Body("chassis")
#     fucaChassicPoint = Point([1,0,0])


#     upright = Body("upright")
#     FUCA = Body("FUCA")
#     FLCA = Body("FLCA")
