# Custom list widget
#
# Application: Main Controllers
#
# Create by: Tu Nguyen Ngoc

import shutil
from PyQt6 import QtCore
from PyQt6.QtGui import QBrush, QColor, QIcon, QPixmap, QPainter, QPen
from PyQt6.QtWidgets import (QMainWindow, QListWidgetItem, QMessageBox, QDialog, QLabel, QFileDialog,
                             QVBoxLayout, QSizePolicy)
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QLineSeries, QDateTimeAxis, QValueAxis, QPieSlice
from views.ui_mainwindow import Ui_MainWindow
from views.dialog import EditRoutineDialog, DictionaryDialog
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

        # Dictionary
        self.dictionary_dialog = DictionaryDialog(self)

        # Set default avatar
        self.setAvatarImage(self.DEFAULT_AVATAR_PATH)

        # Get the day
        self.widget_calendar.selectionChanged.connect(self.populate_tasks_for_selected_date)

        # Populate tasks for the current date at startup
        self.populate_tasks_for_selected_date()

        # Update the piece chart
        self.widget_calendar.selectionChanged.connect(self.updatePieChart)
        self.updatePieChart()

        # Update the line chart
        self.widget_calendar.selectionChanged.connect(self.updateLineChart)
        self.updateLineChart()

        self.add_button.clicked.connect(self.addCheckboxItem)
        self.delete_button.clicked.connect(self.deleteSelectedItem)
        self.widget_todolist.itemDoubleClicked.connect(self.editItem)  # Edit on double click
        self.edit_button.clicked.connect(self.editSelected)  # Edit using edit button
        self.delete_all_button.clicked.connect(self.deleteAllItems)
        self.update_avatar_button.clicked.connect(self.chooseAndUpdateAvatar)

        # Connect the actions to their respective slots
        self.action_close.triggered.connect(self.close_application)
        self.action_dictionary.triggered.connect(self.open_dictionary)

    def addCheckboxItem(self):
        # Create and show a dialog to collect new task details
        dialog = EditRoutineDialog("", "good", self)  # Assuming EditRoutineDialog can be repurposed for adding new tasks
        dictionary_data = self.dictionary_dialog.load_data()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Get the new task details from the dialog
            item_text, item_type = dialog.routineDetails()

            # Check if the name already exists in the dictionary
            if not any(d == item_text for d in dictionary_data):
                # Name does not exist, add it to the dictionary
                dictionary_data[item_text] = {
                    'description': item_text,
                    'type': item_type
                }
                self.dictionary_dialog.save_data(dictionary_data)

            # Proceed with adding the new task
            selected_date = self.widget_calendar.selectedDate().toString("yyyy-MM-dd")
            conn = get_db_connection()
            daily_task_id = get_or_create_daily_task_id(conn, selected_date)

            MainController.routine_count += 1

            # Create and configure the new item with details from the dialog
            item = QListWidgetItem(item_text, self.widget_todolist)
            item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            item.setForeground(QBrush(QColor(255, 255, 255)))
            item.setIcon(QIcon(self.routine_types[item_type]))

            # Insert the new task into the database
            task_id = insert_task(conn, daily_task_id, item_text, item_type, 0)  # Assuming isDone is stored as 0 for False, 1 for True
            item.setData(QtCore.Qt.ItemDataRole.UserRole, task_id)
            conn.close()

            # Update the charts
            self.updatePieChart()
            self.updateLineChart()
        else:
            pass

    def editItem(self, item):
        self.editRoutine(item)

        # Update the piece chart
        self.updatePieChart()

        # Update the line chart
        self.updateLineChart()

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

        # Update the line chart
        self.updateLineChart()

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

        # Create a custom slice for "Good Routines"
        good_slice = QPieSlice("Good Routines", good_count)
        good_slice.setLabelBrush(QBrush(QColor('white')))  # Set label color to white
        series.append(good_slice)

        # Create a custom slice for "Bad Routines"
        bad_slice = QPieSlice("Bad Routines", bad_count)
        bad_slice.setColor(QColor(255, 165, 0))  # Orange-yellow color
        bad_slice.setLabelBrush(QBrush(QColor('white')))  # Set label color to white
        series.append(bad_slice)

        series.setLabelsVisible(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitleBrush(QBrush(QColor('white')))  # Set chart title color to white
        # chart.setTitle("Good vs Bad Routines for " + selected_date)
        chart.legend().setLabelColor(QColor('white'))  # Set legend labels color to white
        chart.legend().setVisible(True)
        chart.legend().setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom)

        # Set the background color of the chart's plot area
        chart.setBackgroundBrush(QBrush(QColor(0, 6, 38)))

        # Update the legend markers with counts
        for marker in chart.legend().markers(series):  # Loop through the markers of the series
            slice = marker.slice()
            if slice is good_slice:
                marker.setLabel(f"Good Routines: {good_count}")  # Set custom text with count
            elif slice is bad_slice:
                marker.setLabel(f"Bad Routines: {bad_count}")  # Set custom text with count



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


    def updateLineChart(self):
        selected_date = self.widget_calendar.selectedDate()
        dates = [selected_date.addDays(i) for i in range(-3, 4)]  # One week range centered on selected_date

        good_series = QLineSeries()
        bad_series = QLineSeries()

        # Change the series color and set the line width
        bad_series.setPen(QPen(QColor(255, 165, 0), 2))

        for date in dates:
            tasks = fetch_tasks_for_date(get_db_connection(), date.toString("yyyy-MM-dd"))
            good_count = sum(1 for _, _, type_of_task, _ in tasks if type_of_task == 'good')
            bad_count = sum(1 for _, _, type_of_task, _ in tasks if type_of_task == 'bad')

            datetime = QtCore.QDateTime(date, QtCore.QTime(0, 0))
            good_series.append(datetime.toMSecsSinceEpoch(), good_count)
            bad_series.append(datetime.toMSecsSinceEpoch(), bad_count)

        chart = QChart()
        chart.addSeries(good_series)
        chart.addSeries(bad_series)

        axisX = QDateTimeAxis()
        axisX.setLabelsColor(QColor('white'))
        axisX.setTickCount(7)
        axisX.setFormat("ddd")  # Day of the week format

        # Set the chart text color to white
        chart.setPlotAreaBackgroundBrush(QBrush(QColor('white')))

        # Customize the Y-axis if needed
        axisY = QValueAxis()
        axisY.setLabelsColor(QColor('white'))

        # Set the background color of the chart to match the widget_piece_chart background
        chart.setBackgroundBrush(QBrush(QColor(0, 6, 38)))

        chart.addAxis(axisX, QtCore.Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axisY, QtCore.Qt.AlignmentFlag.AlignLeft)

        good_series.attachAxis(axisX)
        good_series.attachAxis(axisY)
        bad_series.attachAxis(axisX)
        bad_series.attachAxis(axisY)

        chartView = QChartView(chart)
        chartView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)

        layout = self.widget_line_chart_7_days.layout()
        if layout is None:
            layout = QVBoxLayout(self.widget_line_chart_7_days)
            self.widget_line_chart_7_days.setLayout(layout)
        else:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        layout.addWidget(chartView)

    def close_application(self):
        # This method will be called when the close action is triggered
        self.close()  # This will close the application window

    def open_dictionary(self):
        # This method will be called when the dictionary action is triggered
        self.dictionary_dialog.prepare_dictionary()
        # Show the dialog modally
        result = self.dictionary_dialog.exec()

        # Check the result after the dialog is closed
        if result == QDialog.DialogCode.Accepted:
            print("Dialog accepted, handle the returned data here")
        else:
            pass



