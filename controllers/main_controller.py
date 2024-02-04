# Custom list widget
#
# Application: Main Controllers
#
# Create by: Tu Nguyen Ngoc



from PyQt6 import QtCore
from PyQt6.QtGui import QBrush, QColor, QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QListWidgetItem, QMessageBox, QDialog, QLabel, QFileDialog
from views.ui_mainwindow import Ui_MainWindow
from widgets.custom_list_widget import EditRoutineDialog


class MainController(QMainWindow, Ui_MainWindow):
    routine_count = 0
    routine_types = {'good': 'resources/good_routine_icon.png', 'bad': 'resources/bad_routine_icon.png'}  # Icon paths for routine types

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.add_button.clicked.connect(self.addCheckboxItem)
        self.delete_button.clicked.connect(self.deleteSelectedItem)
        self.widget_todolist.itemDoubleClicked.connect(self.editItem)  # Edit on double click
        self.edit_button.clicked.connect(self.editSelected)  # Edit using edit button

        # Connect the new delete all button
        self.delete_all_button.clicked.connect(self.deleteAllItems)

        # Let's connect a click event on the label to choose an image
        self.update_avatar_button.clicked.connect(self.chooseAndUpdateAvatar)

        # Initialize QLabel inside frame_avatar to hold the avatar image
        self.avatar_label = QLabel(self.frame_avatar)
        self.avatar_label.setGeometry(0, 0, self.frame_avatar.width(), self.frame_avatar.height())
        self.avatar_label.setScaledContents(True)  # Ensure the avatar scales with the label


    def addCheckboxItem(self):
        MainController.routine_count += 1
        item_text = f"New Routine {MainController.routine_count}"
        item = QListWidgetItem(item_text, self.widget_todolist)
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.CheckState.Unchecked)
        item.setForeground(QBrush(QColor(255, 255, 255)))

        # Default to good routine type
        item.setIcon(QIcon(self.routine_types['good']))

    def editItem(self, item):
        self.editRoutine(item)

    def editSelected(self):
        selected_items = self.widget_todolist.selectedItems()
        if selected_items:
            self.editRoutine(selected_items[0])

    def editRoutine(self, item):
        current_text = item.text()
        current_type = "good" if item.icon().cacheKey() == QIcon(self.routine_types['good']).cacheKey() else "bad"
        dialog = EditRoutineDialog(current_text, current_type, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_text, new_type = dialog.routineDetails()
            item.setText(new_text)
            item.setIcon(QIcon(self.routine_types[new_type]))

    def deleteSelectedItem(self):
        selected_items = self.widget_todolist.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Selection Required", "Please select a routine to delete.")
            return
        for item in selected_items:
            row = self.widget_todolist.row(item)
            self.widget_todolist.takeItem(row)

    def deleteAllItems(self):
        self.widget_todolist.clear()

    def chooseAndUpdateAvatar(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Avatar Image", "",
                                                  "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if fileName:
            self.setAvatarImage(fileName)

    def setAvatarImage(self, imagePath):
        # Load and set the avatar image
        pixmap = QPixmap(imagePath)
        self.avatar_label.setPixmap(pixmap)
