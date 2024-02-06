# Custom list widget
#
# Application: Main Controllers
#
# Create by: Tu Nguyen Ngoc

import logging
import shutil
from PyQt6 import QtCore
from PyQt6.QtGui import QBrush, QColor, QIcon, QPixmap, QPainter, QPen, QAction
from PyQt6.QtWidgets import (QMainWindow, QListWidgetItem, QMessageBox, QDialog, QLabel, QFileDialog,
                             QVBoxLayout, QSizePolicy)
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QLineSeries, QDateTimeAxis, QValueAxis, QPieSlice
from views.ui_mainwindow import Ui_MainWindow
from views.dialog import EditRoutineDialog, DictionaryDialog
from views.utils import resource_path
from database.db import (get_db_connection, get_or_create_daily_task_id, insert_task,
                         update_task, delete_task, delete_daily_task_and_tasks, fetch_tasks_for_date)


class MainController(QMainWindow, Ui_MainWindow):
    routine_count = 0
    routine_types = {'good': resource_path('resources/good_routine_icon.png'), 'bad': resource_path('resources/bad_routine_icon.png')}  # Icon paths for routine types
    DEFAULT_AVATAR_PATH = resource_path('resources/default_avatar.png')

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

        # Update chart
        self.widget_calendar.selectionChanged.connect(self.updateLatestChart)
        # Update the piece chart
        self.day_analysis_button.toggled.connect(self.updateLatestChart)
        # Update the line chart
        self.week_analysis_button.toggled.connect(self.updateLatestChart)
        self.updateLatestChart()

        self.add_button.clicked.connect(self.addCheckboxItem)
        self.delete_button.clicked.connect(self.deleteSelectedItem)
        self.widget_todolist.itemDoubleClicked.connect(self.editItem)  # Edit on double click
        self.widget_todolist.itemChecked.connect(self.updateTaskStatus)
        self.edit_button.clicked.connect(self.editSelected)  # Edit using edit button
        self.delete_all_button.clicked.connect(self.deleteAllItems)
        self.update_chart_button.clicked.connect(self.updateLatestChart)
        # Connect the move up and down button signals to the slot methods
        self.move_up_button.clicked.connect(self.moveItemUp)
        self.move_down_button.clicked.connect(self.moveItemDown)

        # Load the custom icons
        closeIconPath = resource_path("resources/close_menubar_icon.png")  # Replace with the path to your close icon
        dictionaryIconPath = resource_path("resources/dictionary_menubar_icon.png")  # Replace with the path to your dictionary icon
        # Set the icons for the actions
        self.action_close.setIcon(QIcon(closeIconPath))
        self.action_dictionary.setIcon(QIcon(dictionaryIconPath))
        # Connect the actions to their respective slots
        self.action_close.triggered.connect(self.close_application)
        self.action_dictionary.triggered.connect(self.open_dictionary)

        # Create the action
        # Load the custom icon
        infoIconPath = resource_path("resources/about_icon.png")  # Adjust the path to where your icon is stored
        infoIcon = QIcon(infoIconPath)

        # Create the action with the custom icon
        self.actionAbout = QAction(infoIcon, "About", self)
        self.menuDetails.addAction(self.actionAbout)
        self.actionAbout.triggered.connect(self.showAboutInfo)

    def showAboutInfo(self):
        # Create a QMessageBox
        aboutBox = QMessageBox()
        aboutBox.setWindowTitle("About")
        aboutBox.setWindowIcon(QIcon(resource_path("resources/window_icon.png")))
        aboutBox.setText("""
        <b>Application Name:</b> Routine Checking App<br>
        <b>Version:</b> 1.0<br>
        <b>Developed by:</b> Nguyen Ngoc Tu<br>
        <b>Description:</b> This app is designed to help you monitor your daily routines and analyze them. It enables you to enhance good habits and reduce bad ones.<br><br>
        Contact: nguyengnoctu1205@gmail.com
        """)

        # Set the icon for the QMessageBox
        customIconPath = resource_path("resources/about_icon.png")  # Replace with the path to your custom icon
        customIcon = QIcon(customIconPath)
        aboutBox.setIconPixmap(customIcon.pixmap(64, 64))  # Set the icon size as needed

        # Show the QMessageBox
        aboutBox.exec()

    def addCheckboxItem(self):
        # Add check box Item
        # Get the data in dictionary first
        dictionary_data = self.dictionary_dialog.load_data()
        # Create and show a dialog to collect new task details
        dialog = EditRoutineDialog("", "good", dictionary_data, self)  # Assuming EditRoutineDialog can be repurposed for adding new tasks
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Get the new task details from the dialog
            item_text, item_type = dialog.routineDetails()

            # Proceed with adding the new task
            selected_date = self.widget_calendar.selectedDate().toString("yyyy-MM-dd")
            try:
                conn = get_db_connection()
                daily_task_id = get_or_create_daily_task_id(conn, selected_date)
            except Exception as e:
                logging.exception("Error adding checkbox item: ")
                QMessageBox.critical(self, "Error", "Connect the database.")
                raise

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
        else:
            pass

    def editItem(self, item):
        self.editRoutine(item)

    def editSelected(self):
        selected_items = self.widget_todolist.selectedItems()
        if selected_items:
            self.editRoutine(selected_items[0])

    def editRoutine(self, item):
        # Get the current data in dictionary first
        dictionary_data = self.dictionary_dialog.load_data()

        current_text = item.text()
        current_type = "good" if item.icon().cacheKey() == QIcon(self.routine_types['good']).cacheKey() else "bad"
        dialog = EditRoutineDialog(current_text, current_type, dictionary_data, self)
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

    def moveItemUp(self):
        currentRow = self.widget_todolist.currentRow()
        if currentRow > 0:
            currentItem = self.widget_todolist.takeItem(currentRow)
            self.widget_todolist.insertItem(currentRow - 1, currentItem)
            self.widget_todolist.setCurrentRow(currentRow - 1)

    def moveItemDown(self):
        currentRow = self.widget_todolist.currentRow()
        if currentRow < self.widget_todolist.count() - 1:
            currentItem = self.widget_todolist.takeItem(currentRow)
            self.widget_todolist.insertItem(currentRow + 1, currentItem)
            self.widget_todolist.setCurrentRow(currentRow + 1)

    def updateTaskStatus(self, item):
        # Update the "is done" status in the database
        task_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
        is_done = item.checkState() == QtCore.Qt.CheckState.Checked

        conn = get_db_connection()
        # Assume update_task_is_done only updates the "is done" status based on the task ID
        self.update_task_is_done(conn, task_id, is_done)
        conn.close()

    def update_task_is_done(self, conn, task_id, is_done):
        # Convert is_done to a format suitable for your database (e.g., int or string)
        is_done_value = 1 if is_done else 0  # Example for a database expecting integers

        # Prepare the SQL query to update the "is done" status
        query = "UPDATE Task SET isDone = ? WHERE id = ?"

        # Execute the query
        cur = conn.cursor()
        cur.execute(query, (is_done_value, task_id))
        conn.commit()

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

    def updateLatestChart(self):
        # Update the piece chart
        self.updatePieChart()
        # Update the line chart
        self.updateLineChart()

    def updatePieChart(self):
        selected_date = self.widget_calendar.selectedDate().toString("yyyy-MM-dd")
        conn = get_db_connection()
        tasks = fetch_tasks_for_date(conn, selected_date)
        conn.close()

        # Filter tasks based on the state of day_analysis_button
        if self.day_analysis_button.is_on():
            # If day_analysis_button is on, only count tasks that are done
            good_count = sum(1 for _, _, type_of_task, is_done in tasks if type_of_task == 'good' and is_done)
            bad_count = sum(1 for _, _, type_of_task, is_done in tasks if type_of_task == 'bad' and is_done)
        else:
            # If day_analysis_button is off, count all tasks regardless of is_done
            good_count = sum(1 for _, _, type_of_task, _ in tasks if type_of_task == 'good')
            bad_count = sum(1 for _, _, type_of_task, _ in tasks if type_of_task == 'bad')

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

        # Determine the date range based on the week_analysis_button state
        if self.week_analysis_button.is_on():  # For 7 days
            dates = [selected_date.addDays(i) for i in range(-3, 4)]  # One week range centered on selected_date
        else:  # For the current month
            start_of_month = QtCore.QDate(selected_date.year(), selected_date.month(), 1)
            end_of_month = QtCore.QDate(selected_date.year(), selected_date.month(), selected_date.daysInMonth())
            dates = [start_of_month.addDays(i) for i in range(end_of_month.day())]  # Entire month

        good_series = QLineSeries()
        bad_series = QLineSeries()

        # Customizations for series
        bad_series.setPen(QPen(QColor(255, 165, 0), 2))

        for date in dates:
            tasks = fetch_tasks_for_date(get_db_connection(), date.toString("yyyy-MM-dd"))

            # Adjust counting logic based on the state of day_analysis_button
            if self.day_analysis_button.is_on():
                good_count = sum(1 for _, _, type_of_task, is_done in tasks if type_of_task == 'good' and is_done)
                bad_count = sum(1 for _, _, type_of_task, is_done in tasks if type_of_task == 'bad' and is_done)
            else:
                good_count = sum(1 for _, _, type_of_task, _ in tasks if type_of_task == 'good')
                bad_count = sum(1 for _, _, type_of_task, _ in tasks if type_of_task == 'bad')

            datetime = QtCore.QDateTime(date, QtCore.QTime(0, 0))
            good_series.append(datetime.toMSecsSinceEpoch(), good_count)
            bad_series.append(datetime.toMSecsSinceEpoch(), bad_count)


        # Setup the chart with the series
        chart = QChart()
        chart.addSeries(good_series)
        chart.addSeries(bad_series)

        # Setup axes
        axisX = QDateTimeAxis()
        axisX.setFormat("MMM d" if not self.week_analysis_button.is_on() else "ddd")  # Month-Day format for month, Day of the week for 7 days
        axisX.setLabelsColor(QColor('white'))

        axisY = QValueAxis()
        axisY.setLabelsColor(QColor('white'))

        chart.setBackgroundBrush(QBrush(QColor(0, 6, 38)))
        chart.addAxis(axisX, QtCore.Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axisY, QtCore.Qt.AlignmentFlag.AlignLeft)

        good_series.attachAxis(axisX)
        good_series.attachAxis(axisY)
        bad_series.attachAxis(axisX)
        bad_series.attachAxis(axisY)

        # Clear the layout and add the new chart
        layout = self.widget_line_chart_7_days.layout()
        self.clearLayout(layout)
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Ensure the widget has a QVBoxLayout
        if self.widget_line_chart_7_days.layout() is None:
            layout = QVBoxLayout(self.widget_line_chart_7_days)
            self.widget_line_chart_7_days.setLayout(layout)
        else:
            self.clearLayout(self.widget_line_chart_7_days.layout())

        # Add the chartView to the layout
        self.widget_line_chart_7_days.layout().addWidget(chartView)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

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



