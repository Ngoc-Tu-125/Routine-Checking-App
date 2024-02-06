# Dialog
#
# Application: Routine Checking App
#
# Create by: Tu Nguyen Ngoc

import json
from views.ui_dictionary_dialog import Ui_DictionaryDialog
from views.utils import resource_path
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QDialog, QLineEdit, QComboBox, QVBoxLayout, QPushButton, QTableWidgetItem,
                             QMessageBox, QFormLayout, QDialogButtonBox, QCompleter)


class EditRoutineDialog(QDialog):
    def __init__(self, text, routine_type, dictionary, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Routine")

        self.dictionary = resource_path('database/dictionary.json')  # Store the dictionary
        self.keys = list(dictionary.keys())  # Get the keys from the dictionary

        self.lineEdit = QLineEdit(text)

        # Create a QCompleter with the keys from the dictionary
        completer = QCompleter(self.keys)
        self.lineEdit.setCompleter(completer)

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

class AddEntryDialog(QDialog):
    def __init__(self, parent=None):
        super(AddEntryDialog, self).__init__(parent)
        self.setWindowTitle("Add New Entry")

        self.nameEdit = QLineEdit(self)
        self.descriptionEdit = QLineEdit(self)
        self.typeCombo = QComboBox(self)
        self.typeCombo.addItem("Good")
        self.typeCombo.addItem("Bad")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Name:", self.nameEdit)
        layout.addRow("Description:", self.descriptionEdit)
        layout.addRow("Type:", self.typeCombo)
        layout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return self.nameEdit.text(), self.descriptionEdit.text(), self.typeCombo.currentText()


class DictionaryDialog(QDialog, Ui_DictionaryDialog):

    DICTIONARY_DATABASE = resource_path('database/dictionary.json')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Connect buttons to their respective slots
        self.add_button.clicked.connect(self.add_entry)
        self.delete_button.clicked.connect(self.delete_entry)
        self.delete_all_button.clicked.connect(self.delete_all_entries)
        self.move_up_button.clicked.connect(self.move_row_up)
        self.move_down_button.clicked.connect(self.move_row_down)
        self.import_button.clicked.connect(self.import_entries)
        self.export_button.clicked.connect(self.export_entries)
        self.close_button.clicked.connect(self.close_dialog)

        # Prepare dictionary
        self.prepare_dictionary()

    def prepare_dictionary(self):
        # Prepare dictionary
        # Load data from JSON file or create an empty dictionary
        self.data = self.load_data()
        # Populate_table
        self.populate_table()
        # Connect the cellChanged signal to handle updates
        self.tableWidget.cellChanged.connect(self.handle_cell_change)

    def populate_table(self):
        self.tableWidget.setRowCount(0)  # Clear the table
        for name, entry in self.data.items():
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem(name))
            self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(entry['description']))
            type_combo = QComboBox()
            type_combo.addItem("Good", "Good")
            type_combo.addItem("Bad", "Bad")
            type_combo.setCurrentText(entry['type'])
            type_combo.currentIndexChanged.connect(lambda index, row=rowPosition: self.on_type_changed(row, index))
            self.tableWidget.setCellWidget(rowPosition, 2, type_combo)

    def add_entry(self):
        dialog = AddEntryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, description, type_value = dialog.getInputs()
            if name in self.data:
                QMessageBox.warning(self, "Error", "An entry with this name already exists.")
                return
            self.data[name] = {'description': description, 'type': type_value}
            self.save_data(self.data)
            self.populate_table()

    def delete_entry(self):
        row = self.tableWidget.currentRow()
        if row >= 0:
            name = self.tableWidget.item(row, 0).text()
            if name in self.data:
                del self.data[name]
                self.save_data(self.data)
                self.populate_table()

    def delete_all_entries(self):
        reply = QMessageBox.question(self, 'Delete all entries', 'Are you sure you want to delete all entries?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.data.clear()
            self.save_data(self.data)
            self.populate_table()

    def save_data(self, data):
        with open(self.DICTIONARY_DATABASE, 'w') as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        try:
            with open(self.DICTIONARY_DATABASE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def move_row_up(self):
        currentRow = self.tableWidget.currentRow()
        if currentRow <= 0:  # Check if it's already at the top or there's no selection
            return

        self.swap_rows(currentRow, currentRow - 1)

    def move_row_down(self):
        currentRow = self.tableWidget.currentRow()
        if currentRow >= self.tableWidget.rowCount() - 1 or currentRow < 0:  # Check if it's at the bottom or there's no selection
            return

        self.swap_rows(currentRow, currentRow + 1)

    def swap_rows(self, row1, row2):
        self.tableWidget.blockSignals(True)
        for column in range(self.tableWidget.columnCount()):
            item1 = self.tableWidget.takeItem(row1, column)
            item2 = self.tableWidget.takeItem(row2, column)

            # Swap items
            self.tableWidget.setItem(row1, column, item2 if item2 else QtWidgets.QTableWidgetItem(""))
            self.tableWidget.setItem(row2, column, item1 if item1 else QtWidgets.QTableWidgetItem(""))

        self.tableWidget.blockSignals(False)
        # After swapping, select the row that has been moved to keep focus consistent
        self.tableWidget.setCurrentCell(row2, 0)

    def handle_cell_change(self, row, column):
        # Prevent recursive calls
        self.tableWidget.blockSignals(True)

        name_item = self.tableWidget.item(row, 0)
        description_item = self.tableWidget.item(row, 1)
        type_widget = self.tableWidget.cellWidget(row, 2)

        name = name_item.text() if name_item else ""
        description = description_item.text() if description_item else ""
        type_value = type_widget.currentText() if type_widget else "Good"

        if name:
            self.data[name] = {'description': description, 'type': type_value}
            self.save_data(self.data)
        else:
            QMessageBox.warning(self, "Warning", "Name cannot be empty.")

        # Unblock signals after changes
        self.tableWidget.blockSignals(False)

    def on_type_changed(self, row, index):
        name_item = self.tableWidget.item(row, 0)
        if name_item is not None:
            name = name_item.text()
            type_widget = self.tableWidget.cellWidget(row, 2)
            type_value = type_widget.currentText()
            # Update your data model
            if name in self.data:
                self.data[name]['type'] = type_value
                self.save_data(self.data)  # Save changes to the file


    def save_after_edit(self):
        self.save_data(self.data)
        QMessageBox.information(self, "Info", "Changes saved successfully.")

    def close_dialog(self):
        # Close the dialog
        self.reject()

    def import_entries(self):
        # This method would be called to import entries from a file
        pass

    def export_entries(self):
        # This method would be called to export entries to a file
        pass
