from components import Body, Point, DistanceConstraint
from multibodySystem import MultibodySystem
import numpy as np

FUCA_fore = Point([10,10,0], designVariable=True)
UCA_aft = Point([])

chassis = Body(
    name="chassis",
    points=[FUCA_fore]
    )