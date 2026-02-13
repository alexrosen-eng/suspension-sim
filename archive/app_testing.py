import sys
import numpy as np
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer
import pyqtgraph.opengl as gl
from scipy.optimize import least_squares

class Mechanism3DSimulator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Mechanism Simulator")
        self.setGeometry(100, 100, 900, 600)
        self.central = QtWidgets.QWidget()
        self.setCentralWidget(self.central)

        # Main layout
        main_layout = QtWidgets.QHBoxLayout()
        self.central.setLayout(main_layout)

        # Left panel: inputs
        input_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(input_layout)

        # Link length input
        input_layout.addWidget(QtWidgets.QLabel("Link length L1:"))
        self.l1_input = QtWidgets.QLineEdit("1.0")
        input_layout.addWidget(self.l1_input)

        # Steps input
        input_layout.addWidget(QtWidgets.QLabel("Number of steps:"))
        self.steps_input = QtWidgets.QLineEdit("100")
        input_layout.addWidget(self.steps_input)

        # Simulate button
        self.simulate_btn = QtWidgets.QPushButton("Simulate")
        self.simulate_btn.clicked.connect(self.simulate)
        input_layout.addWidget(self.simulate_btn)

        # Right panel: 3D view
        self.view = gl.GLViewWidget()
        self.view.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        self.view.opts['distance'] = 5
        self.view.opts['elevation'] = 20
        self.view.opts['azimuth'] = 30
        main_layout.addWidget(self.view)

        # Axes
        axes = gl.GLAxisItem()
        axes.setSize(2, 2, 2)
        self.view.addItem(axes)

        # Scatter plots for points
        self.p1_sp = gl.GLScatterPlotItem(size=10, color=(1, 0, 0, 1))
        self.p2_sp = gl.GLScatterPlotItem(size=10, color=(0, 0, 1, 1))
        self.view.addItem(self.p1_sp)
        self.view.addItem(self.p2_sp)

        # Line (link)
        self.link_line = gl.GLLinePlotItem(width=2, color=(1, 1, 1, 1), antialias=True)
        self.view.addItem(self.link_line)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.current_step = 0

    def solver(self, L1, n_steps):
        """
        Simple 3D solver: p1 moves along a trajectory,
        p2 is solved using least_squares to satisfy the link length.
        """
        p1_hist = []
        p2_hist = []
        x_guess = np.array([0.5, 0.5, 0.0])

        for t in range(n_steps):
            # Example motion of p1: moves in Y and Z
            p1 = np.array([0.0, 1.0 - (1/n_steps)*t, 0])
            #0.5 * np.sin(2*np.pi*t/n_steps)

            def eq(vars, p1):
                x2, y2, z2 = vars
                dx = x2 - p1[0]
                dy = y2 - p1[1]
                dz = z2 - p1[2]
                # Constraint: distance = L1, keep z2 free for demonstration
                return np.array([dx**2 + dy**2 + dz**2 - L1**2, y2 - 0.0, z2 - 0.0])

            sol = least_squares(eq, x_guess, args=(p1,))
            x2, y2, z2 = sol.x
            p1_hist.append(p1)
            p2_hist.append([x2, y2, z2])
            x_guess = sol.x

        return np.array(p1_hist), np.array(p2_hist)

    def simulate(self):
        L1 = float(self.l1_input.text())
        n_steps = int(self.steps_input.text())
        self.p1_hist, self.p2_hist = self.solver(L1, n_steps)
        self.current_step = 0
        self.timer.start(50)

    def update_animation(self):
        if self.current_step >= len(self.p1_hist):
            self.timer.stop()
            return

        p1 = self.p1_hist[self.current_step]
        p2 = self.p2_hist[self.current_step]

        # Update points
        self.p1_sp.setData(pos=np.array([p1]))
        self.p2_sp.setData(pos=np.array([p2]))

        # Update link line
        self.link_line.setData(pos=np.array([p1, p2]), width=2, antialias=True)

        self.current_step += 1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mechanism3DSimulator()
    window.show()
    sys.exit(app.exec())
