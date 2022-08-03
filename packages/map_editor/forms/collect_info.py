from PyQt5.QtWidgets import *
import sys

class Collect_Info(QDialog):

	def __init__(self):
		super(Collect_Info, self).__init__()

		self.setWindowTitle("Init information")

		self.setGeometry(100, 100, 500, 550)

		self.formGroupBox = QGroupBox("Form 1")

		self.size_width = QSpinBox()

		self.size_height = QSpinBox()

		self.crossroad_count = QSpinBox()

		self.road_length = QSpinBox()

		self.save_path = QLineEdit()

		self.watchtowers = QCheckBox()

		self.createForm()

		self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

		error_dialog = QtWidgets.QErrorMessage()
		error_dialog.showMessage('Oh no!')

		self.buttonBox.accepted.connect(self.getInfo)

		self.buttonBox.rejected.connect(self.reject)

		mainLayout = QVBoxLayout()

		mainLayout.addWidget(self.formGroupBox)

		mainLayout.addWidget(self.buttonBox)

		self.setLayout(mainLayout)

	def showError(self):
		button = QMessageBox.critical(
			self,
			"Error",
			"Incorrect input data.",
			buttons=QMessageBox.Discard | QMessageBox.NoToAll | QMessageBox.Ignore,
			defaultButton=QMessageBox.Discard,
		)

		if button == QMessageBox.Discard:
			print("Discard!")
		elif button == QMessageBox.NoToAll:
			print("No to all!")
		else:
			print("Ignore!")

	def checkCorrectnessOfData(self):
		if self.size_width < 3 or self.size_width > 10:
			self.showError()

	def getInfo(self):

		# printing the form information
		print("Width : {0}".format(self.size_width.text()))
		print("Height : {0}".format(self.size_height.text()))
		print("Crossroads count : {0}".format(self.crossroad_count.text()))
		print("Road length : {0}".format(self.road_length.text()))
		print("Path : {0}".format(self.save_path.text()))
		print("Watchtowers: {0}".format(self.watchtowers.isChecked()))

		self.close()

	def createForm(self):

		layout = QFormLayout()

		layout.addRow(QLabel("Width"), self.size_width)

		layout.addRow(QLabel("Height"), self.size_height)

		layout.addRow(QLabel("Crossroad count"), self.crossroad_count)

		layout.addRow(QLabel("Road length"), self.road_length)

		layout.addRow(QLabel("Path"), self.save_path)

		layout.addRow(QLabel("Generate watchtowers"), self.watchtowers)

		self.formGroupBox.setLayout(layout)


# main method
if __name__ == '__main__':

	# create pyqt5 app
	app = QApplication(sys.argv)

	# create the instance of our Window
	window = Collect_Info()

	# showing the window
	window.show()

	# start the app
	sys.exit(app.exec())
