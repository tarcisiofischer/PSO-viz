from matplotlib.backends.qt_compat import QtWidgets

from .controller import setup_application_callbacks
from .model import PSOModelSetup
from .view import PSOApplicationWindow


def open_gui_for_problem(problem):
    qapp = QtWidgets.QApplication([])
    model = PSOModelSetup(problem)
    app = PSOApplicationWindow(problem)
    setup_application_callbacks(model, app)
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()
