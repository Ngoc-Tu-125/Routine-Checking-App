# Custom list widget
#
# Application: Main Controllers
#
# Create by: Tu Nguyen Ngoc

import shutil
from PyQt6 import QtCore
from PyQt6.QtGui import QBrush, QColor, QIcon, QPixmap, QPainter
from PyQt6.QtWidgets import (QMainWindow, QListWidgetItem, QMessageBox, QDialog, QLabel, QFileDialog,
                             QVBoxLayout, QSizePolicy)
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from views.ui_mainwindow import Ui_MainWindow
from views.dialog import EditRoutineDialog
from database.db import (get_db_connection, get_or_create_daily_task_id, insert_task,
                         update_task, delete_task, delete_daily_task_and_tasks, fetch_tasks_for_date)



class MainController(QMainWindow, Ui_MainWindow):
    routine_count = 0
    routine_types = {'good': 'resources/good_routine_icon.png', 'bad': 'resources/bad_routine_icon.png'}  # Icon paths for routine types
    DEFAULT_AVATAR_PATH = 'resources/default_avatar.png'

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.avatar_label = QLabel(self.frame_avatar)
        self.avatar_label.setGeometry(0, 0, self.frame_avatar.width(), self.frame_avatar.height())
        self.avatar_label.setScaledContents(True)

        # Set default avatar
        self.setAvatarImage(self.DEFAULT_AVATAR_PATH)

        # Get the day
        self.widget_calendar.selectionChanged.connect(self.populate_tasks_for_selected_date)

        # Populate tasks for the current date at startup
        self.populate_tasks_for_selected_date()

        self.widget_calendar.selectionChanged.connect(self.updatePieChart)
        self.updatePieChart()

        self.add_button.clicked.connect(self.addCheckboxItem)
        self.delete_button.clicked.connect(self.deleteSelectedItem)
        self.widget_todolist.itemDoubleClicked.connect(self.editItem)  # Edit on double click
        self.edit_button.clicked.connect(self.editSelected)  # Edit using edit button
        self.delete_all_button.clicked.connect(self.deleteAllItems)
        self.update_avatar_button.clicked.connect(self.chooseAndUpdateAvatar)


    def addCheckboxItem(self):
        selected_date = self.widget_calendar.selectedDate().toString("yyyy-MM-dd")
        conn = get_db_connection()
        daily_task_id = get_or_create_daily_task_id(conn, selected_date)

        MainController.routine_count += 1
        item_text = f"New Routine {MainController.routine_count}"
        item = QListWidgetItem(item_text, self.widget_todolist)
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.CheckState.Unchecked)
        item.setForeground(QBrush(QColor(255, 255, 255)))
        item.setIcon(QIcon(self.routine_types['good']))

        task_id = insert_task(conn, daily_task_id, item_text, 'good', 0)  # Assuming isDone is stored as 0 for False, 1 for True
        item.setData(QtCore.Qt.ItemDataRole.UserRole, task_id)
        conn.close()

        # Update the piece chart
        self.updatePieChart()

    def editItem(self, item):
        self.editRoutine(item)

        # Update the piece chart
        self.updatePieChart()

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

            conn = get_db_connection()
            task_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
            is_done = item.checkState() == QtCore.Qt.CheckState.Checked
            update_task(conn, task_id, new_text, new_type, is_done)
            conn.close()

    def deleteSelectedItem(self):
        selected_items = self.widget_todolist.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Selection Required", "Please select a routine to delete.")
            return

        conn = get_db_connection()
        for item in selected_items:
            task_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
            delete_task(conn, task_id)
            row = self.widget_todolist.row(item)
            self.widget_todolist.takeItem(row)
        conn.close()

        # Update the piece chart
        self.updatePieChart()

    def deleteAllItems(self):
        reply = QMessageBox.question(self, 'Delete All Tasks',
                                     'Are you sure you want to delete all tasks for this day?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            selected_date = self.widget_calendar.selectedDate().toString("yyyy-MM-dd")
            conn = get_db_connection()
            delete_daily_task_and_tasks(conn, selected_date)
            conn.close()
            self.widget_todolist.clear()

        # Update the piece chart
        self.updatePieChart()

    def chooseAndUpdateAvatar(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Avatar Image", "",
                                                  "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if fileName:
            # Copy the selected image to DEFAULT_AVATAR_PATH, overwriting the existing file
            shutil.copy(fileName, self.DEFAULT_AVATAR_PATH)
            # Update the avatar display
            self.setAvatarImage(self.DEFAULT_AVATAR_PATH)

    def setAvatarImage(self, imagePath):
        pixmap = QPixmap(imagePath)
        self.avatar_label.setPixmap(pixmap)
        self.avatar_label.setScaledContents(True)

    def populate_tasks_for_selected_date(self):
        """Populate the list widget with tasks for the calendar's selected date."""
        selected_date = self.widget_calendar.selectedDate().toString("yyyy-MM-dd")
        conn = get_db_connection()
        tasks = fetch_tasks_for_date(conn, selected_date)
        conn.close()

        self.widget_todolist.clear()  # Clear existing items
        for task_id, name, type_of_task, is_done in tasks:
            item = QListWidgetItem(name, self.widget_todolist)
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.CheckState.Checked if is_done else QtCore.Qt.CheckState.Unchecked)
            item.setForeground(QBrush(QColor(255, 255, 255)))
            item.setIcon(QIcon(self.routine_types[type_of_task]))
            item.setData(QtCore.Qt.ItemDataRole.UserRole, task_id)  # Store the task ID for later reference

        # Update the piece chart
        self.updatePieChart()

    def updatePieChart(self):
        selected_date = self.widget_calendar.selectedDate().toString("yyyy-MM-dd")
        conn = get_db_connection()
        tasks = fetch_tasks_for_date(conn, selected_date)
        conn.close()

        good_count = sum(1 for _, _, type_of_task, is_done in tasks if type_of_task == 'good')
        bad_count = sum(1 for _, _, type_of_task, is_done in tasks if type_of_task == 'bad')

        if good_count == 0 and bad_count == 0:
            good_count = 1  # Set to 1 if there are no good tasks
            bad_count = 1  # Set to 1 if there are no good tasks

        series = QPieSeries()
        series.append("Good Routines", good_count)
        series.append("Bad Routines", bad_count)
        series.setLabelsVisible(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Good vs Bad Routines for " + selected_date)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)

        # This will make the QChartView expand to fill available space
        chartView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Assuming self.widget_piece_chart is the container for the QChartView
        if self.widget_piece_chart.layout() is None:
            # If there is no layout, set one
            self.widget_piece_chart.setLayout(QVBoxLayout())

        # Clear existing widgets in the layout
        while self.widget_piece_chart.layout().count():
            child = self.widget_piece_chart.layout().takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add the chart view to the layout
        self.widget_piece_chart.layout().addWidget(chartView)

        # Reapply the layout to ensure the chart view is resized
        self.widget_piece_chart.layout().activate()




