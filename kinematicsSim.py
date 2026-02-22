from components import MultibodySystem, Body, Frame, SphericalJoint, CartesianJoint
import numpy as np
from scipy.optimize import least_squares

SOLVER = least_squares

def heave_motion(step):
        dz = step * 0.1
        r = np.array([0,0,dz])
        q = np.array([1,0,0,0])
        return r,q

def buildSuspension():
        # Define the points that make up the bodies and the system
    chassis_UCA_fore = Frame([10,10,0], designVariable=True)
    chassis_UCA_aft = Frame([20,10,0], designVariable=True)

    UCA_fore = Frame([10,10,0], designVariable=True)
    UCA_aft = Frame([20,10,0], designVariable=True)
    UCA_outboard = Frame([15, 20, 0], designVariable=True)

    world_UCA_outboard = Frame([15, 20, 0], designVariable=True)


    # Define the bodies
    world = Body(
        name="world"
    )
    world.addFrame([Frame([0,0,0]),
                    world_UCA_outboard])

    chassis = Body(
        name="chassis", fixed=True
        )
    chassis.addFrame([chassis_UCA_fore,
                    chassis_UCA_aft])
    chassis.setMotion(heave_motion)


    UCA = Body(
        name="UCA", fixed=False
            )
    UCA.addFrame([UCA_fore,
                UCA_aft,
                UCA_outboard])
    

    sj_UCA_fore = SphericalJoint(chassis, chassis_UCA_fore,
                            UCA, UCA_fore)

    sj_UCA_aft = SphericalJoint(chassis, chassis_UCA_aft,
                                UCA, UCA_aft)
    
    cart_UCA_outboard = CartesianJoint(UCA, UCA_outboard, world, world_UCA_outboard)

    sys = MultibodySystem()
    sys.addBody([world,chassis,UCA])
    sys.addJoint([sj_UCA_aft, sj_UCA_fore, cart_UCA_outboard])

    return(sys)

def apply_motion(sys,step):
    for body in sys.bodies:
        if body.motion_func is not None:
            r_new, q_new = heave_motion(step)
            body.r = r_new
            body.q = q_new

def kinematicsSim(sys, n_steps):

    z_motion = 5
    x0 = sys.pack()
    hist = [x0]

    def residual_fun(x):
        sys.unpack(x)
        return(sys.residual())

    # now we are going to loop through the motion of the specified body (chassis)
    for step in range(n_steps):
        
        apply_motion(sys, step)

        sol = least_squares(residual_fun, x0)
        x0 = sol.x

        hist.append(x0)

    return (hist)
    

#%%
# Plotting function

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

def plot_kinematics(sys, history, frame_names=None):
    """
    Visualize the multibody system frames over time.

    Parameters:
    -----------
    sys : MultibodySystem
        The system object containing bodies and frames
    history : list of np.array
        List of solver state vectors (x) at each timestep
    frame_names : dict
        Optional mapping of frame objects to names for labeling
    """

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Collect colors for each body
    colors = ['red', 'blue', 'green', 'orange', 'purple']

    for b_idx, body in enumerate(sys.bodies):
        if body.fixed:
            continue
        color = colors[b_idx % len(colors)]

        # Collect frame trajectories
        for f in body.frames:
            traj = []
            for x in history:
                sys.unpack(x)
                pos = f.globalPosition()
                traj.append(pos)
            traj = np.array(traj)
            ax.plot(traj[:,0], traj[:,1], traj[:,2], color=color, label=f"{body.name}-{body.frames.index(f)}")

    # Optionally, mark the final position
    for body in sys.bodies:
        for f in body.frames:
            pos = f.globalPosition()
            ax.scatter(pos[0], pos[1], pos[2], color='k', s=20)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Multibody Frame Trajectories")
    ax.legend()
    ax.grid(True)
    ax.view_init(elev=20, azim=-60)
    plt.show()


#%%
# Main loop

if __name__ == "__main__":
    sys = buildSuspension()
    hist = kinematicsSim(sys, 20)
    plot_kinematics(sys, hist)  