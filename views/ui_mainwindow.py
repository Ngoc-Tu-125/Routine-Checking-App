# Form implementation generated from reading ui file 'design_frame\qt_design.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QBrush, QColor, QIcon, QLinearGradient, QPalette
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from views.toggle_switch import ToggleSwitch


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Routine Checking")
        MainWindow.setFixedSize(905, 702)

        # Create a gradient for the background (left to right)
        gradient = QLinearGradient(0, 0, MainWindow.width(), 0)
        gradient.setColorAt(0, QColor(180, 180, 180))  # Start color (gray)
        gradient.setColorAt(1, QColor(250, 250, 250))  # End color (light gray)

        # Set the background gradient for the entire main window
        palette = QPalette()
        palette.setBrush(QtGui.QPalette.ColorRole.Window, QBrush(gradient))
        MainWindow.setPalette(palette)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_button = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_button.setGeometry(QtCore.QRect(20, 100, 121, 541))
        self.frame_button.setStyleSheet("background-color: rgb(0, 6, 38)")
        self.frame_button.setObjectName("frame_button")

        # Vertical layout for top button
        self.widget = QtWidgets.QWidget(parent=self.frame_button)
        self.widget.setGeometry(QtCore.QRect(10, 0, 101, 281))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # Add button
        self.add_button = QtWidgets.QPushButton(parent=self.widget)
        self.add_button.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.add_button.setObjectName("add_button")
        self.verticalLayout.addWidget(self.add_button)

        # Delete button
        self.delete_button = QtWidgets.QPushButton(parent=self.widget)
        self.delete_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.delete_button.setObjectName("delete_button")
        self.verticalLayout.addWidget(self.delete_button)

        # Delete all button
        self.delete_all_button = QtWidgets.QPushButton(parent=self.widget)
        self.delete_all_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.delete_all_button.setObjectName("delete_all_button")
        self.verticalLayout.addWidget(self.delete_all_button)

        # Edit button
        self.edit_button = QtWidgets.QPushButton(parent=self.widget)
        self.edit_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.edit_button.setObjectName("edit_button")
        self.verticalLayout.addWidget(self.edit_button)

        # Analysis button
        self.analysis_button = QtWidgets.QPushButton(parent=self.widget)
        self.analysis_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.analysis_button.setObjectName("analysis_button")
        self.verticalLayout.addWidget(self.analysis_button)

        # Import button
        self.widget1 = QtWidgets.QWidget(parent=self.frame_button)
        self.widget1.setGeometry(QtCore.QRect(10, 410, 101, 111))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.import_button = QtWidgets.QPushButton(parent=self.widget1)
        self.import_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.import_button.setObjectName("import_button")
        self.verticalLayout_2.addWidget(self.import_button)

        # Export button
        self.export_button = QtWidgets.QPushButton(parent=self.widget1)
        self.export_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.export_button.setObjectName("export_button")
        self.verticalLayout_2.addWidget(self.export_button)

        # Frame analysis
        self.frame_analysis = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_analysis.setGeometry(QtCore.QRect(149, 99, 401, 541))
        # self.frame_analysis.setStyleSheet("background-color: rgb(0, 6, 38);")
        self.frame_analysis.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_analysis.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_analysis.setObjectName("frame_analysis")
        self.widget_piece_chart = QtWidgets.QWidget(parent=self.frame_analysis)
        self.widget_piece_chart.setGeometry(QtCore.QRect(10, 0, 381, 231))
        self.widget_piece_chart.setStyleSheet("background-color: rgb(0, 6, 38);")
        self.widget_piece_chart.setObjectName("widget_piece_chart")
        self.widget_line_chart_7_days = QtWidgets.QWidget(parent=self.frame_analysis)
        self.widget_line_chart_7_days.setGeometry(QtCore.QRect(10, 270, 381, 271))
        self.widget_line_chart_7_days.setStyleSheet("background-color: rgb(0, 6, 38);")
        self.widget_line_chart_7_days.setObjectName("widget_line_chart_7_days")

        # Frame to do list
        self.frame_todolist = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_todolist.setGeometry(QtCore.QRect(559, 99, 331, 321))
        self.frame_todolist.setStyleSheet("background-color: rgb(0, 6, 38);")
        self.frame_todolist.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_todolist.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_todolist.setObjectName("frame_todolist")
        # Widget to do list
        self.widget_todolist = QtWidgets.QListWidget(parent=self.frame_todolist)
        self.widget_todolist.setGeometry(QtCore.QRect(10, 10, 311, 301))
        self.widget_todolist.setObjectName("widget_todolist")

        # Frame calendar
        self.frame_calendar = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_calendar.setGeometry(QtCore.QRect(559, 439, 331, 201))
        self.frame_calendar.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_calendar.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_calendar.setObjectName("frame_calendar")
        self.widget_calendar = QtWidgets.QCalendarWidget(parent=self.frame_calendar)
        self.widget_calendar.setGeometry(QtCore.QRect(1, 0, 331, 201))
        self.widget_calendar.setMinimumSize(QtCore.QSize(331, 201))
        self.widget_calendar.setMaximumSize(QtCore.QSize(331, 16777215))
        self.widget_calendar.setStyleSheet("background-color: rgb(0, 6, 38);\n"
"color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(54, 69, 79);\n"
"selection-background-color: rgb(112, 128, 144);\n"
"border-color: rgb(0, 0, 127);\n"
"")
        # Widget calendar
        self.widget_calendar.setObjectName("widget_calendar")
        self.frame_user_info = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_user_info.setGeometry(QtCore.QRect(730, 10, 161, 80))
        self.frame_user_info.setStyleSheet("background-color: rgb(0, 6, 38);")
        self.frame_user_info.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_user_info.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_user_info.setObjectName("frame_user_info")

        # Lable avatar
        self.frame_avatar = QtWidgets.QFrame(parent=self.frame_user_info)
        self.frame_avatar.setGeometry(QtCore.QRect(69, 10, 81, 61))
        self.frame_avatar.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_avatar.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_avatar.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_avatar.setObjectName("frame_avatar")

        # Add the ToggleSwitch
        self.toggle_switch = ToggleSwitch(parent=self.frame_user_info, width=50, height=25, on_color="#2ecc71", off_color="#e74c3c", on_text="", off_text="")
        self.toggle_switch.setGeometry(QtCore.QRect(10, 30, 51, 21))
        self.toggle_switch.set_on_gradient("#3498db", "#2980b9")  # Light to dark blue for "on" state
        self.toggle_switch.set_off_gradient("#95a5a6", "#7f8c8d")  # Light to dark grey for "off" state
        self.toggle_switch.set_handle_shadow("#ffffff", "#cccccc")
        self.toggle_switch.set_text_size(5)
        self.toggle_switch.setObjectName("toggle_switch")

        # Frame app title
        self.frame_app_title = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_app_title.setGeometry(QtCore.QRect(19, 10, 691, 81))
        self.frame_app_title.setStyleSheet("background-color: rgb(0, 6, 38);")
        self.frame_app_title.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_app_title.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_app_title.setObjectName("frame_app_title")
        self.textEdit = QtWidgets.QTextEdit(parent=self.frame_app_title)
        self.textEdit.setGeometry(QtCore.QRect(110, 10, 461, 61))
        self.textEdit.setStyleSheet("font: 28pt \"Rockwell\";")
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu bar
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 905, 22))
        self.menubar.setObjectName("menubar")
        self.menuRoutine_checking = QtWidgets.QMenu(parent=self.menubar)
        self.menuRoutine_checking.setObjectName("menuRoutine_checking")
        self.menuDetails = QtWidgets.QMenu(parent=self.menubar)
        self.menuDetails.setObjectName("menuDetails")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.action_dictionary = QtGui.QAction(parent=MainWindow)
        self.action_dictionary.setObjectName("action_dictionary")
        self.action_close = QtGui.QAction(parent=MainWindow)
        self.action_close.setObjectName("action_close")
        self.menuRoutine_checking.addAction(self.action_dictionary)
        self.menuRoutine_checking.addAction(self.action_close)
        self.menubar.addAction(self.menuRoutine_checking.menuAction())
        self.menubar.addAction(self.menuDetails.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Apply shadow and rounded corners to frame_button
        self.frame_button.setStyleSheet("""
        QFrame#frame_button {
                background-color: rgb(0, 6, 38);
                border-radius: 15px;
        }
        QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;
                font-size: 10pt;
        }
        """)
        shadow_effect_frame_button = QGraphicsDropShadowEffect()
        shadow_effect_frame_button.setBlurRadius(10)
        shadow_effect_frame_button.setXOffset(0)
        shadow_effect_frame_button.setYOffset(5)
        shadow_effect_frame_button.setColor(QColor(0, 0, 0, 150))
        self.frame_button.setGraphicsEffect(shadow_effect_frame_button)

        # Apply shadow and rounded corners to frame_todolist
        self.frame_todolist.setStyleSheet("""
        background-color: rgb(0, 6, 38);
        border-radius: 15px;
        """)
        shadow_effect_frame_todolist = QGraphicsDropShadowEffect()
        shadow_effect_frame_todolist.setBlurRadius(10)
        shadow_effect_frame_todolist.setXOffset(0)
        shadow_effect_frame_todolist.setYOffset(5)
        shadow_effect_frame_todolist.setColor(QColor(0, 0, 0, 150))
        self.frame_todolist.setGraphicsEffect(shadow_effect_frame_todolist)

        # Apply shadow and rounded corners to frame_calendar
        self.frame_calendar.setStyleSheet("""
        background-color: rgb(0, 6, 38);
        border-radius: 5px;
        """)
        shadow_effect_frame_calendar = QGraphicsDropShadowEffect()
        shadow_effect_frame_calendar.setBlurRadius(10)
        shadow_effect_frame_calendar.setXOffset(0)
        shadow_effect_frame_calendar.setYOffset(5)
        shadow_effect_frame_calendar.setColor(QColor(0, 0, 0, 150))
        self.frame_calendar.setGraphicsEffect(shadow_effect_frame_calendar)

        # Apply shadow and rounded corners to frame_user_info
        self.frame_user_info.setStyleSheet("""
        background-color: rgb(0, 6, 38);
        border-radius: 15px;
        """)
        shadow_effect_frame_user_info = QGraphicsDropShadowEffect()
        shadow_effect_frame_user_info.setBlurRadius(10)
        shadow_effect_frame_user_info.setXOffset(0)
        shadow_effect_frame_user_info.setYOffset(5)
        shadow_effect_frame_user_info.setColor(QColor(0, 0, 0, 150))
        self.frame_user_info.setGraphicsEffect(shadow_effect_frame_user_info)

        # Apply shadow and rounded corners to frame_app_title
        self.frame_app_title.setStyleSheet("""
        background-color: rgb(0, 6, 38);
        border-radius: 15px;
        """)
        shadow_effect_frame_app_title = QGraphicsDropShadowEffect()
        shadow_effect_frame_app_title.setBlurRadius(10)
        shadow_effect_frame_app_title.setXOffset(0)
        shadow_effect_frame_app_title.setYOffset(5)
        shadow_effect_frame_app_title.setColor(QColor(0, 0, 0, 150))
        self.frame_app_title.setGraphicsEffect(shadow_effect_frame_app_title)

        # Apply shadow and rounded corners to widget_piece_chart
        self.widget_piece_chart.setStyleSheet("""
            background-color: rgb(0, 6, 38);
            border-radius: 15px;
        """)
        shadow_effect_piece_chart = QGraphicsDropShadowEffect()
        shadow_effect_piece_chart.setBlurRadius(10)
        shadow_effect_piece_chart.setXOffset(0)
        shadow_effect_piece_chart.setYOffset(5)
        shadow_effect_piece_chart.setColor(QColor(0, 0, 0, 150))
        self.widget_piece_chart.setGraphicsEffect(shadow_effect_piece_chart)

        # Apply shadow and rounded corners to widget_line_chart_7_days
        self.widget_line_chart_7_days.setStyleSheet("""
            background-color: rgb(0, 6, 38);
            border-radius: 15px;
        """)
        shadow_effect_line_chart = QGraphicsDropShadowEffect()
        shadow_effect_line_chart.setBlurRadius(15)
        shadow_effect_line_chart.setXOffset(0)
        shadow_effect_line_chart.setYOffset(5)
        shadow_effect_line_chart.setColor(QColor(0, 0, 0, 150))
        self.widget_line_chart_7_days.setGraphicsEffect(shadow_effect_line_chart)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Routine Checking"))
        MainWindow.setWindowIcon(QIcon("resources/window_icon.png"))
        self.add_button.setText(_translate("MainWindow", "Add Routine"))
        self.delete_button.setText(_translate("MainWindow", "Delete Routine"))
        self.edit_button.setText(_translate("MainWindow", "Edit Routine"))
        self.export_button.setText(_translate("MainWindow", "Export"))
        self.import_button.setText(_translate("MainWindow", "Import"))
        self.analysis_button.setText(_translate("MainWindow", "Analysis"))
        self.delete_all_button.setText(_translate("MainWindow", "Delete All"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Rockwell\'; font-size:28pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Segoe UI\'; color:#ffffff;\">Routine Checking App</span></p></body></html>"))
        self.textEdit.setReadOnly(True)
        self.menuRoutine_checking.setTitle(_translate("MainWindow", "Routine checking"))
        self.menuDetails.setTitle(_translate("MainWindow", "Details"))
        self.action_dictionary.setText(_translate("MainWindow", "Dictionary"))
        self.action_close.setText(_translate("MainWindow", "Close"))
