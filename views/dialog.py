# Dialog
#
# Application: Routine Checking App
#
# Create by: Tu Nguyen Ngoc

from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox, QVBoxLayout, QPushButton


class EditRoutineDialog(QDialog):
    def __init__(self, text, routine_type, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Routine")

        self.lineEdit = QLineEdit(text)
        self.comboBox = QComboBox()
        self.comboBox.addItems(["good", "bad"])
        self.comboBox.setCurrentText(routine_type)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.saveButton)
        self.setLayout(layout)

    def routineDetails(self):
        return self.lineEdit.text(), self.comboBox.currentText()