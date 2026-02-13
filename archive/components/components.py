import numpy as np
from numpy.typing import NDArray

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # needed for 3D plots

class Tire:
    """
    Generates a tire object
    ALL UNITS IN in.
    """

    def __init__(self, OD: int, ID: int, width: int) -> None:
        self.OD = OD
        self.ID = ID
        self.width = width

    def pointCloud(self, n: int = 100) -> NDArray[np.float64]:
        """
        pointCloud returns a point cloud array representing the tire
        Revolves an ellipse about the z axis
        
        :param self: Object name
        :param n: Description
        :type n: int
        :return: Description
        :rtype: NDArray[float64]
        """

        def Rz(theta):
            return np.array([[np.cos(theta), -np.sin(theta), 0],
                            [np.sin(theta), np.cos(theta), 0],
                            [0, 0, 1]])

        center = np.mean([self.OD/2, self.ID/2])

        a = self.OD/2 - center
        b = self.width/2
        dx = center

        e = np.zeros((n,3))
        pc = np.zeros((n**2, 3))
        
        # First we are going to create a 2D point cloud in XZ plane 
        # representing the ellipse
        for i,phi in enumerate(np.linspace(0, 2*np.pi, n)):
            e[i] = np.array([
                        a * np.cos(phi) + dx,
                        0,
                        b * np.sin(phi)
                        ])
        
        # Next we are going to rotate that ellipse n times to form the ellipsoid torus
        for j,theta in enumerate(np.linspace(0, 2*np.pi, n)):
            rot = (Rz(theta) @ e.T).T
            pc[j*n:(j+1)*n, :] = rot

        return pc
    
    def plot(self, n: int = 50, surface: bool = False, title: str = "3D Tire Point Cloud") -> None:
        """
        Plots the tire in 3D using the point cloud.

        :param n: number of points for the point cloud
        :param surface: if True, plot surface; else scatter
        :param title: plot title
        """

        pc = self.pointCloud(n)

        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111, projection='3d')

        x = pc[:,0]
        y = pc[:,1]
        z = pc[:,2]

        if surface:
            grid_n = int(np.sqrt(pc.shape[0]))
            X = x.reshape(grid_n, grid_n)
            Y = y.reshape(grid_n, grid_n)
            Z = z.reshape(grid_n, grid_n)
            ax.plot_surface(X, Y, Z, rstride=1, cstride=1, color='lightgray', edgecolor='k', alpha=0.7)
        else:
            ax.scatter(x, y, z, s=2, c='blue', alpha=0.6)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(title)

        # make axes equal
        self._set_axes_equal(ax)

        # initial view
        ax.view_init(elev=30, azim=45)
        plt.show()

    @staticmethod
    def _set_axes_equal(ax):
        """
        Sets 3D axes to equal scale.
        """
        x_limits = ax.get_xlim3d()
        y_limits = ax.get_ylim3d()
        z_limits = ax.get_zlim3d()

        x_range = x_limits[1] - x_limits[0]
        y_range = y_limits[1] - y_limits[0]
        z_range = z_limits[1] - z_limits[0]

        max_range = max(x_range, y_range, z_range)

        x_mid = np.mean(x_limits)
        y_mid = np.mean(y_limits)
        z_mid = np.mean(z_limits)

        ax.set_xlim3d([x_mid - max_range/2, x_mid + max_range/2])
        ax.set_ylim3d([y_mid - max_range/2, y_mid + max_range/2])
        ax.set_zlim3d([z_mid - max_range/2, z_mid + max_range/2])

class ControlArm:
    def __init__(self, inboardFore: NDArray[np.float64], inboardAft: NDArray[np.float64], outboard: NDArray[np.float64]) -> None:
        self.inboardFore = inboardFore
        self.inboardAft = inboardAft
        self.outboard = outboard

    def inboardPoints(self) -> NDArray[np.float64]:
        return(
            np.array([
                self.inboardFore,
                self.inboardAft
            ])
        )
    
    def outboardPoints(self) -> NDArray[np.float64]:
        return(
            np.array([
                self.outboard
            ])
        )
    
class Rod:
    def __init__(self, inboard, outboard ) -> None:
        self.inboard = inboard
        self.outboard = outboard

    def