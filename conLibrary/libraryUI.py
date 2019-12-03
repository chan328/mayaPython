from controllerLibrary import ControllerLibrary
from PySide2 import QtWidgets, QtCore, QtGui


class ControllerLibraryUI(QtWidgets.QDialog):

    def __init__(self):
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle('Controller Library UI')
        self.library = ControllerLibrary()
        self.build_ui()
        self.populate()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        save_widget = QtWidgets.QWidget()
        save_layout = QtWidgets.QHBoxLayout(save_widget)
        layout.addWidget(save_widget)

        self.save_namefield = QtWidgets.QLineEdit()
        save_layout.addWidget(self.save_namefield)

        save_button = QtWidgets.QPushButton('save')
        save_layout.addWidget(save_button)

        size = 64
        buffer = 12
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.list_widget.setIconSize(QtCore.QSize(size, size))
        self.list_widget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.list_widget.setGridSize(QtCore.QSize(size+buffer, size+buffer))
        save_layout.addWidget(self.list_widget)

        button_widget = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_widget)
        layout.addWidget(button_widget)

        import_button = QtWidgets.QPushButton('Import')
        button_layout.addWidget(import_button)

        refresh_button = QtWidgets.QPushButton('Refresh')
        button_layout.addWidget(refresh_button)

        close_button = QtWidgets.QPushButton('Close')
        button_layout.addWidget(close_button)

    def populate(self):
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.list_widget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)


def showUI():
    ui = ControllerLibraryUI()
    ui.show()
    return ui