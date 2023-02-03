from PyQt5 import QtCore
from typing import Dict, Any, List
from PyQt5.QtWidgets import QDialog, QGroupBox, QDialogButtonBox, QFormLayout, \
    QVBoxLayout, \
    QLineEdit, QLabel, QFrame, QComboBox

from utils.constants import TILES, RELATIVE_TO, FRAME, FORM_DICT


class EditObject(QDialog):
    get_info = QtCore.pyqtSignal(object)

    def __init__(self, layer_name: str, name: str, config: Dict[str, Any],
                 frame: Dict[str, Any], is_draggable: bool, frames: List[str]):
        super(EditObject, self).__init__()
        self.float_formatting = 5
        self.info = {"types": {}}
        self.layer_name = layer_name
        self.info_send = {"name": name, "layer_name": layer_name,
                          "new_config": {}, "is_draggable": is_draggable,
                          FRAME: {},
                          "is_valid": True,
                          "remove": False
                          }
        self.name = name
        self.is_draggable = is_draggable
        self.info_send["new_config"] = config
        self.info_send[FRAME] = frame
        self.frames = frames
        self.setWindowTitle("Edit object")
        self.formGroupBox = QGroupBox(f"Object: {name}")
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.addButton("Remove", QDialogButtonBox.ActionRole)
        self.buttonBox.accepted.connect(self.send_info)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.clicked.connect(self.remove_elem)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.formGroupBox)
        main_layout.addWidget(self.buttonBox)
        self.create_form(config, frame)
        self.setLayout(main_layout)

    def remove_elem(self, e):
        if e.text() == "Remove":
            self.info_send["remove"] = True
            self.get_info.emit(self.info_send)
            self.close()

    def send_info(self) -> None:
        try:
            for frame_key in self.info_send[FRAME]:
                list_for_edit = [frame_key]  if frame_key == RELATIVE_TO else self.info_send[FRAME][frame_key]
                for frame_val in list_for_edit:
                    if isinstance(self.info_send[FRAME][frame_key], dict):
                        row_name = f"{frame_key}.{frame_val}"
                        self.info_send[FRAME][frame_key][frame_val] = \
                            (self.info["types"][row_name])(self.info[row_name].text())
                    elif isinstance(self.info[frame_key], QComboBox):
                        self.info_send[FRAME][frame_key] = self.info[frame_key].currentText()
                    else:
                        self.info_send[FRAME][frame_key] = (
                            self.info["types"][frame_key])(
                            self.info[frame_key].text())
            for key in self.info_send["new_config"]:
                if self.info["types"][key] == dict or self.info["types"][key] == list:
                    val = eval(self.info[key].text())
                elif isinstance(self.info[key], QComboBox):
                    val = self.info[key].currentText()
                else:
                    val = (self.info["types"][key])(self.info[key].text())
                self.info_send["new_config"][key] = val
        except ValueError:
            self.info_send["is_valid"] = False
        except SyntaxError:
            self.info_send["is_valid"] = False
        self.get_info.emit(self.info_send)
        self.close()

    def create_form(self, config: Dict[str, Any], frame: Dict[str, Any]) -> None:
        layout = QFormLayout()

        for key in config:
            # dropdown lists of types
            if self.layer_name in FORM_DICT and key in FORM_DICT[self.layer_name].keys():
                combobox = QComboBox()
                combobox.addItems(FORM_DICT[self.layer_name][key])
                combobox.setCurrentText(config[key])
                self.info[key] = combobox
                self.info["types"][key] = type(config[key])
                layout.addRow(QLabel(key), combobox)
            else:
                # other types
                edit = QLineEdit(self)
                self.info[key] = edit
                self.info["types"][key] = type(config[key])
                # set digit accuracy
                if not isinstance(config[key], float):
                    edit.setText(str(config[key]))
                else:
                    edit.setText(f'{config[key]:.{self.float_formatting}f}')
                # tile identifiers must not be changed
                if self.layer_name == TILES and (key == "i" or key == "j"):
                    edit.setDisabled(True)
                layout.addRow(QLabel(key), edit)
        layout.addWidget(QHLine())
        for frame_key in frame:
            # dropdown lists of objects names
            if frame_key == RELATIVE_TO:
                if self.is_draggable:
                    combobox = QComboBox()
                    combobox.addItems(self.frames)
                    combobox.setCurrentText(frame[frame_key])
                    self.info[frame_key] = combobox
                    self.info["types"][frame_key] = type(self.info[frame_key])
                    layout.addRow(QLabel(frame_key), combobox)
                    list_for_edit = []
                else:
                    list_for_edit = [frame_key]
            else:
                list_for_edit = frame[frame_key]
            for frame_val in list_for_edit:
                edit = QLineEdit(self)
                if not isinstance(frame[frame_key], dict):
                    row_name = frame_key
                    val = frame[frame_key]
                else:
                    row_name = f"{frame_key}.{frame_val}"
                    val = frame[frame_key][frame_val]
                self.info["types"][row_name] = type(val)
                self.info[row_name] = edit
                if not isinstance(val, float):
                    edit.setText(str(val))
                else:
                    edit.setText(f'{val:.{self.float_formatting}f}')
                # cannot edit frames of non-draggable objects
                if not self.is_draggable:
                    edit.setDisabled(True)
                layout.addRow(QLabel(row_name), edit)
        self.formGroupBox.setLayout(layout)


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
