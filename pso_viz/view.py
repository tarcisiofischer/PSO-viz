import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, QtGui
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PSOApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, problem):
        super().__init__()

        # TODO: Remove bad dependency
        self._problem = problem

        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.main_layout = QtWidgets.QHBoxLayout(self._main)
        self._setup_left_panel()
        self._setup_right_panel()

    def _setup_left_panel(self):
        self.plot_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.main_layout.addWidget(self.plot_canvas)
        self._plot_axis = self.plot_canvas.figure.subplots()

        # TODO: Remove dependency
        bounds = self._problem.get_bounds()
        # TODO: Make mesh size user-configurable
        x = np.linspace(bounds[0][0], bounds[1][0], 20)
        y = np.linspace(bounds[0][1], bounds[1][1], 20)
        data = np.zeros(shape=(x.size, y.size))
        for i in range(len(x)):
            for j in range(len(y)):
                data[j, i] = self._problem.fitness(np.array([x[i], y[j]]))[0]
        xv, yv = np.meshgrid(x, y)

        self._plot_axis.contourf(xv, yv, data)
        self._point_cloud, = self._plot_axis.plot([], [], 'ro')

        self.navigation_toolbar = NavigationToolbar(self.plot_canvas, self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.navigation_toolbar)

    def _setup_right_panel(self):
        self.right_panel = QtWidgets.QGroupBox()
        self.right_panel_layout = QtWidgets.QFormLayout()
        self.right_panel.setLayout(self.right_panel_layout)
        self.right_panel.setMaximumWidth(300)

        def add_input(name, title):
            setattr(self, f'{name}_label', QtWidgets.QLabel(title))
            setattr(self, f'{name}_input', QtWidgets.QLineEdit())
            getattr(self, f'{name}_input').setValidator(QtGui.QDoubleValidator())
            self.right_panel_layout.addWidget(getattr(self, f'{name}_label'))
            self.right_panel_layout.addWidget(getattr(self, f'{name}_input'))

        def add_button(name, title):
            setattr(self, f'{name}_button', QtWidgets.QPushButton(title))
            self.right_panel_layout.addWidget(getattr(self, f'{name}_button'))

        add_input('gen', 'Generations:')
        add_input('pop_size', 'Population Size:')
        add_input('inertia', 'Inertia:')
        add_input('cog', 'Cognitive:')
        add_input('soc', 'Social:')
        add_input('seed', 'Seed:')
        add_button('run', 'Run')
        self.main_layout.addWidget(self.right_panel)

    def set_run_callback(self, callback):
        self.run_button.clicked.connect(callback)

    def disable_run_button(self):
        self.run_button.setEnabled(False)

    def enable_run_button(self):
        self.run_button.setEnabled(True)

    def set_input_changed_callback(self, input_name, callback):
        getattr(self, f'{input_name}_input').textChanged.connect(callback)

    def set_input_value(self, input_name, input_value):
        getattr(self, f'{input_name}_input').setText(str(input_value))

    def update_canvas(self, point_cloud):
        self._point_cloud.set_data(point_cloud[:, 0], point_cloud[:, 1])
        self._point_cloud.figure.canvas.draw()
        QtWidgets.qApp.processEvents()
