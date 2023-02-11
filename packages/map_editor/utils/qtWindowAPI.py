from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog


class QtWindowAPI:
    def __init__(self, cur_dir: str):
        self.dir = cur_dir

    def get_dir(self, parent: QtWidgets.QWidget, info: str = "") -> str:
        return QFileDialog.getExistingDirectory(parent, f"Select a folder to {info} the map",
                                                self.dir,
                                                options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly)
