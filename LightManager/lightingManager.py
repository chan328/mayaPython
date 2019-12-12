from Qt import QtWidgets, QtCore, QtGui
from functools import partial
import Qt
import logging
from maya import OpenMayaUI as omui

logging.basicConfig()
logger = logging.getLogger('LightingManager')
logger.setLevel(logging.DEBUG)

if Qt.__binding__ == 'PySide2':
    logger.debug('Using Pyside with shiboken')
    from shiboken2 import wrapInstance
elif Qt.__binding__.startwith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
else:
    logger.debug('Using Pyside2 with shiboken')
    from shiboken2 import wrapInstance

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
        self.populate()

    def populate(self):
        while self.scrollLayout.count():
            widget = self.scrollLayout.takeAt(0).widget()
            if widget:
                # takeAt = delete parent
                widget.setVisible(False)
                widget.deleteLater()

        for light in pm.ls(type=["areaLight", "spotLight", "pointLight", "directionalLight", "volumeLight"]):
            self.add_light(light)

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

        refresh_button = QtWidgets.QPushButton('Refresh')
        refresh_button.clicked.connect(self.populate)
        layout.addWidget(refresh_button, 2, 1)

    def create_light(self):
        light_type = self.lightTypeCB.currentText()
        func = self.lightTypes[light_type]

        light = func()
        self.add_light(light)

    def add_light(self, light):
        widget = LightWidget(light)
        self.scrollLayout.addWidget(widget)
        widget.on_solo.connect(self.on_solo)

    def on_solo(self, value):
        light_widgets = self.findChildren(LightWidget)
        for widget in light_widgets:
            if widget != self.sender():
                widget.disable_light(value)


class LightWidget(QtWidgets.QWidget):

    on_solo = QtCore.Signal(bool)

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

        solo_button = QtWidgets.QPushButton('Solo')
        solo_button.setCheckable(True)
        solo_button.toggled.connect(lambda val: self.on_solo.emit(val))
        layout.addWidget(solo_button, 0, 1)

        delete_button = QtWidgets.QPushButton('X')
        delete_button.clicked.connect(self.delete_light)
        delete_button.setMaximumWidth(10)
        layout.addWidget(delete_button, 0, 2)

        intensity = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        intensity.setMinimum(1)
        intensity.setMaximum(1000)
        intensity.setValue(self.light.intensity.get())
        intensity.valueChanged.connect(lambda val: self.light.intensity.set(val))
        layout.addWidget(intensity, 1, 0, 1, 2)

        self.color_button = QtWidgets.QPushButton()
        self.color_button.setMaximumWidth(20)
        self.color_button.setMaximumHeight(20)
        self.set_button_color()
        self.color_button.clicked.connect(self.set_color)
        layout.addWidget(self.color_button, 1, 2)

    def set_color(self):
        light_color = self.light.color.get()
        color = pm.colorEditor(rgbValue=light_color)

        r, g, b, a = [float(c) for c in color.split()]
        color = (r, g, b)

        self.light.color.set(color)
        self.set_button_color(color)

    def set_button_color(self, color=None):
        if not color:
            color = self.light.color.get()

        assert len(color) == 3, "You must provide a list of 3 colors"

        # color = 0~255 float value
        r, g, b = [c*255 for c in color]
        # each value in color multiplying it by 255

        self.color_button.setStyleSheet('background-color: rgba(%s, %s, %s, 1.0)' % (r, g, b))

    def disable_light(self, value):
        self.name.setChecked(not value)

    def delete_light(self):
        # remove light manager
        self.setParent(None)
        self.setVisible(False)
        self.deleteLater()

        pm.delete(self.light.getTransform())


def show_ui():
    ui = LightManager()
    ui.show()
    return ui

