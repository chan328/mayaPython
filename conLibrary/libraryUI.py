import pprint

from maya import cmds
import controllerLibrary
from PySide2 import QtWidgets, QtCore, QtGui
reload(controllerLibrary)


class ControllerLibraryUI(QtWidgets.QDialog):
    """
    The ControllerLibraryUI is a dialog that lets us save and import controllers.
    """
    def __init__(self):
        super(ControllerLibraryUI, self).__init__()

        self.setWindowTitle('Controller Library UI')

        # The library variable points to an instance of our controller library
        self.library = controllerLibrary.ControllerLibrary()

        # Every time we create a new instance, we will automatically build our UI and populate it
        self.build_ui()
        self.populate()

    def build_ui(self):
        """
        This method build out the UI
        :return:
        """
        layout = QtWidgets.QVBoxLayout(self)

        # This is a child widgets
        save_widget = QtWidgets.QWidget()
        save_layout = QtWidgets.QHBoxLayout(save_widget)
        layout.addWidget(save_widget)

        self.save_namefield = QtWidgets.QLineEdit()
        save_layout.addWidget(self.save_namefield)

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

        save_button = QtWidgets.QPushButton('save')
        save_button.clicked.connect(self.save)
        save_layout.addWidget(save_button)

        import_button = QtWidgets.QPushButton('Import')
        import_button.clicked.connect(self.load)
        button_layout.addWidget(import_button)

        refresh_button = QtWidgets.QPushButton('Refresh')
        refresh_button.clicked.connect(self.populate)
        button_layout.addWidget(refresh_button)

        close_button = QtWidgets.QPushButton('Close')
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)

    def populate(self):
        self.list_widget.clear()
        self.library.find()

        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.list_widget.addItem(item)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))

    def load(self):
        current_item = self.list_widget.currentItem()

        if not current_item:
            return

        name = current_item.text()
        self.library.load(name)

    def save(self):
        name = self.save_namefield.text()
        if not name.strip():
            cmds.warning("No name input")

        self.library.save(name)
        self.populate()
        self.save_namefield.setText('')


def showUI():
    ui = ControllerLibraryUI()
    ui.show()
    return ui