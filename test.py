from components import Body, Frame, SphericalJoint
from multibodySystem import MultibodySystem
import numpy as np


# Define the points that make up the bodies and the system
chassis_UCA_fore = Frame([10,10,0], designVariable=True)
chassis_UCA_aft = Frame([20,10,0], designVariable=True)

UCA_fore = Frame([10,10,0], designVariable=True)
UCA_aft = Frame([20,10,0], designVariable=True)
UCA_outboard = Frame([15, 20, 0], designVariable=True)


# Define the bodies
chassis = Body(
    name="chassis"
    )
chassis.addFrame([chassis_UCA_fore,
                  chassis_UCA_aft])


UCA = Body(
    name="UCA"
        )
UCA.addFrame([UCA_fore,
              UCA_aft,
              UCA_outboard])


# Define the joints that will link the bodies together

sj_UCA_fore = SphericalJoint(chassis, chassis_UCA_fore,
                            UCA, UCA_fore)

sj_UCA_aft = SphericalJoint(chassis, chassis_UCA_aft,
                            UCA, UCA_aft)


vehicle = MultibodySystem()


