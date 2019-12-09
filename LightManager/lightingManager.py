from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import  QtGui
import pymel.core as pm


class LightManager(QtWidgets.Qdialog):
    def __init__(self):
        super(LightManager, self).__init__()

    def show_ui(self):
        ui = LightManager()
        ui.show_ui()
        return ui