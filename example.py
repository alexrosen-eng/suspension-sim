from components import Frame, Body, SphericalJoint, MultibodySystem
from kinematicsSim import kinematicsSim
import numpy as np
from scipy.spatial.transform import Rotation

# Four Bar Linkage Example

#%% 
# Define Bodies and frames

ground = Body("ground", [0,0,0], [1,0,0,0], free=False)
ground_f1 = Frame([1,1,0])
ground_f2 = Frame([9,1,0])
ground.addFrame(ground_f1)
ground.addFrame(ground_f2)

link1 = Body("link1", [1,1,0], [np.cos(np.pi/12), 0,0,np.sin(np.pi/12)], free=False)
link1_f1 = Frame([3,0,0])
link1.addFrame(link1_f1)

#%%
# Apply Motion to body

link1.setMotion