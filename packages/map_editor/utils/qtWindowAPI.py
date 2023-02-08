from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog
import os


class QtWindowAPI:
    def __init__(self, cur_dir: str):
        self.dir = cur_dir

    def get_dir(self, parent: QtWidgets.QWidget, info: str = "") -> str:
        return QFileDialog.getExistingDirectory(parent, f"Select a folder to {info} the map",
                                                self.dir,
                                                options=QFileDialog.DontUseNativeDialog | QFileDialog.ShowDirsOnly)

    def create_file_name(self, parent: QtWidgets.QWidget,
                         info: str = "filename") -> str:
        if "SNAP" in os.environ:
            return QFileDialog.getSaveFileName(parent, f"Select {info} to save",
                                               self.dir, options=QtWidgets.QFileDialog.DontUseNativeDialog)[0]
        else:
            dialog = QInputDialog()
            dialog.resize(600, 150)
            text, ok = dialog.getText(parent, "Input data",
                                      f"Select {info} to save")
            if ok:
                return os.path.join(self.dir, text)
