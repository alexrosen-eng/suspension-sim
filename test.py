from components import Body, Point, DistanceConstraint
from multi
import numpy as np

import os
print(os.getcwd())

FUCA_fore = Point(np.array([10,10,0]), designVariable=True)

chassis = Body(
    name="chassis",
    points=[FUCA_fore]
    )