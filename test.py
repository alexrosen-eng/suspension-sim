from components import Body, Frame, SphericalJoint
from multibodySystem import MultibodySystem
import numpy as np



UCA_fore = Frame([10,10,0], [] designVariable=True)
UCA_aft = Frame([])

chassis = Body(
    name="chassis",
    frames=[UCA_fore,
            UCA_aft]
    )

UCA = Body(name="UCA", frames=[UCA_fore, UCA_aft])

vehicle = MultibodySystem()
vehicle.add_body([chassis, UCA])
vehicle.add_constraint([])