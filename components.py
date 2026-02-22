import numpy as np
from numpy.typing import NDArray
import copy
from scipy.spatial.transform import Rotation



class Frame:
    """
    Point creates a frame to define in the simulation.

    position: [NDArray] to define the initial position. [x,y,z] is expected with respect to the global csys
    orientation: [NDArray] to define the orientation of the frame. Uses quaternions [q0, q1, q2, q3]
    designVariable: [bool] Add the frame as a design variable in optimizers

    """

    def __init__(self, r_local, designVariable = False) -> None:
        self.r_local = np.array(r_local, dtype=float)
        self.body = None
        self.designVariable = designVariable

    def globalPosition(self):
        """
        This function finds the global position of the frame 
        """
        if self.body is None:
            raise RuntimeError(
                "Frame is not attached to a body."
            )
    
        R = Rotation.from_quat(self.body.q).as_matrix()
        return self.body.r + R @ self.r_local



class Body:
    """
    Docstring for Body

    Creates a body object, which is just a collection of frames attached to the body
    addFrame: adds frames to the body and associates the body to each frame
    """

    def __init__(self, name: str, r=None, q=None, fixed=False) -> None:
        self.name = name

        # define the position of the body (origin if not defined)
        self.r = np.array(r if r is not None else [0,0,0], dtype=float)
        # define orientation of body (aligned to origin if undefined)
        self.q = np.array(q if q is not None else [1,0,0,0], dtype=float)
        
        self.fixed = fixed
        
        # Create a variable to store the frames associated to the body
        self.frames = []
        self.motion_func = None

    def addFrame(self, frame: NDArray | list):
        for f in frame:
            f.body = self
            self.frames.append(f)

    def setMotion(self, motion_func):
        self.motion_func = motion_func
        self.fixed = True

    




class SphericalJoint:
    def __init__(self, body1: Body, frame1: Frame, body2: Body, frame2: Frame) -> None:
        self.body1 = body1
        self.frame1 = frame1
        self.body2 = body2
        self.frame2 = frame2


    def residual(self):
        p1 = self.frame1.globalPosition()
        p2 = self.frame2.globalPosition()
        return p2 - p1

        
    

class CartesianJoint:

    def __init__(self, body1: Body, frame1: Frame, body2: Body, frame2: Frame) -> None:
        self.body1 = body1
        self.frame1 = frame1
        self.body2 = body2
        self.frame2 = frame2

    def residual(self) -> NDArray:
        p1 = self.frame1.globalPosition()
        p2 = self.frame2.globalPosition()

        return np.array([p2[2] - p1[2]]) # global z axis is locked

class MultibodySystem:
    """
    residual: This is a function to build the residuals of the multibody system.
    The joints each have their own residual method that will be used to add those residuals to the build
    The quaternion residual of constraining the quaternion vector to have a magnitude of one is then added (quaternion normalization)
    """
    def __init__(self) -> None:
        self.bodies = []
        self.joints = []

    def addBody(self, body: list) -> None:
        self.bodies.extend(body)

    def addJoint(self, joint: list) -> None:
        self.joints.extend(joint)

    def pack(self):
        x=[]
        for body in self.bodies:
            if body.fixed:
                continue
            x.extend(body.r)
            x.extend(body.q)
        return np.array(x)
    
    def unpack(self,x):
        idx = 0
        for body in self.bodies:
            if body.fixed:
                continue
            body.r = x[idx:idx+3]
            idx +=3
            body.q = x[idx:idx+4]
            idx += 4

    def residual(self) -> NDArray:

        Phi = [] # residual variable

        # Joint residuals
        for joint in self.joints:
            Phi.append(joint.residual())

        for body in self.bodies:
            Phi.append(np.array([
                np.dot(body.q, body.q) - 1
            ]))

        return np.concatenate(Phi)
    
    def jacobian(self):
        pass

    # def buildConstraints(self):

    #     # Loop through each body
    #     for i in range(len(self.bodies)):

    #         # Loop through each point in each body
    #         for j in range(len(self.bodies[i])):
                

    # def residuals(self):
    #     return np.array([c.residual() for c in self.constraints])