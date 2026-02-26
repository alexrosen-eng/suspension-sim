import numpy as np
from numpy.typing import NDArray
import copy
from scipy.spatial.transform import Rotation


#%%
# Body Class

class Body:

    def __init__(self, name: str, r: NDArray | list, q: NDArray | list, free=False) -> None:
        self.name = name

        self.r = np.asarray(r, dtype=float)
        self.q = np.asarray(q, dtype=float)
        self.free = free
        
        # Create a variable to store the frames associated to the body
        self.frames = [Frame([0,0,0])] # Always set the first frame as the origin
        self.motion = None

    def addFrame(self, frame: Frame) -> None:
        for f in frame:
            f.body = self
            self.frames.append(f)

    def setMotion(self, motion) -> None:
        self.motion = motion
        self.free = False

    def residual(self) -> float:
        return np.dot(self.q, self.q) - 1

#%%
# Frame Class

class Frame:

    def __init__(self, r_local: NDArray | list) -> None:
        self.r_local = np.asarray(r_local, dtype=float)
        self.body = None

    def globalPosition(self) -> NDArray:

        if self.body is None:
            raise RuntimeError(
                "Frame is not attached to a body."
            )
    
        R = Rotation.from_quat(self.body.q).as_matrix()
        return self.body.r + R @ self.r_local

#%%
# Joint Classes

class SphericalJoint:

    def __init__(self, frame1: Frame, frame2: Frame) -> None:
        self.frame1 = frame1
        self.frame2 = frame2
    
    def residual(self) -> NDArray:

        p1 = self.frame1.globalPosition()
        p2 = self.frame2.globalPosition()

        disp_residual = p2 - p1

        return disp_residual.flatten()


class RevoluteJoint:

    def __init__(self, frame1, frame2, AoR: NDArray | list) -> None:
        self.frame1 = frame1
        self.frame2 = frame2
        self.AoR = np.asarray(AoR, dtype=float)

    def residual(self) -> NDArray:
        p1 = self.frame1.globalPosition()
        p2 = self.frame2.globalPosition()

        body1 = self.frame1.body
        body2 = self.frame2.body

        q1 = body1.q
        q2 = body2.q

        disp_residual = (p2 - p1).flatten()

        rot_residual = np.array([
            q1[1]/self.AoR[0] - q1[2]/self.AoR[1], 
            q1[2]/self.AoR[1] - q1[3]/self.AoR[2], 
            q1[1]/self.AoR[0] - q1[3]/self.AoR[3],
            q2[1]/self.AoR[0] - q2[2]/self.AoR[1], 
            q2[2]/self.AoR[1] - q2[3]/self.AoR[2], 
            q2[1]/self.AoR[0] - q2[3]/self.AoR[3],
        ])

        return np.append(disp_residual, rot_residual).flatten()


# WIP:
# class CartesianJoint:

#     def __init__(self, frame1: Frame, frame2: Frame, fixedAxis= NDArray | list) -> None:
#         self.frame1 = frame1
#         self.frame2 = frame2
#         self.fixedAxis = fixedAxis

#     def residual(self) -> NDArray:
#         p1 = self.frame1.globalPosition()
#         p2 = self.frame2.globalPosition()

#         disp_residual = 

#         return np.array([p2[2] - p1[2]]).flatten() # global z axis is locked


#%%
# Multibody System Class

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
            if body.free == False:
                continue
            x.extend(body.r)
            x.extend(body.q)
        return np.array(x)
    
    def unpack(self,x):
        idx = 0
        for body in self.bodies:
            if body.free == False:
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
            Phi.append(body.residual())

        return np.concatenate(Phi)