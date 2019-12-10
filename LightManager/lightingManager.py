from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from functools import partial
import pymel.core as pm


class LightManager(QtWidgets.QDialog):
    lightTypes = {
        "Point Light": pm.pointLight,
        "Spot Light": pm.spotLight,
        "Directional Light": pm.directionalLight,
        "Area Light": partial(pm.shadingNode, 'areaLight', asLight=True),
        "Volume Light": partial(pm.shadingNode, 'volumeLight', asLight=True)
    }

    def __init__(self):
        super(LightManager, self).__init__()
        self.setWindowTitle('Lighting Manager')
        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QGridLayout(self)

        self.lightTypeCB = QtWidgets.QComboBox()
        for lightType in sorted(self.lightTypes):
            self.lightTypeCB.addItem(lightType)
        layout.addWidget(self.lightTypeCB, 0, 0)

        create_button = QtWidgets.QPushButton('Create')
        create_button.clicked.connect(self.create_light)
        layout.addWidget(create_button, 0, 1)
        # row 0 column 1

        scroll_widget = QtWidgets.QWidget()
        scroll_widget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scroll_widget)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area, 1, 0, 1, 2)

    def create_light(self):
        light_type = self.lightTypeCB.currentText()
        func = self.lightTypes[light_type]

        light = func()

        widget = LightWidget(light)
        self.scrollLayout.addWidget(widget)


class LightWidget(QtWidgets.QWidget):
    def __init__(self, light):
        super(LightWidget, self).__init__()
        if isinstance(light, str):
            light = pm.PyNode(light)

        self.light = light
        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QGridLayout(self)

        self.name = QtWidgets.QCheckBox(str(self.light.getTransform()))
        self.name.setChecked(self.light.visibility.get())
        self.name.toggled.connect(lambda val: self.light.getTransform().visibility.set(val))
        # def setLightVisibility(val):
        #     self.light.visibility.set(val)

        layout.addWidget(self.name, 0, 0)


def showUI():
    ui = LightManager()
    ui.show()
    return ui

