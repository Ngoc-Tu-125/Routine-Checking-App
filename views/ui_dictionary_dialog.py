# Form implementation generated from reading ui file 'ui\qt_dictionary_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.6.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIcon, QColor, QPalette, QLinearGradient, QBrush
from views.utils import resource_path


class Ui_DictionaryDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(691, 694)

        # Create a gradient for the background (left to right)
        gradient = QLinearGradient(0, 0, Dialog.width(), 0)
        gradient.setColorAt(0, QColor(180, 180, 180))  # Start color (gray)
        gradient.setColorAt(1, QColor(250, 250, 250))  # End color (light gray)

        # Set the background gradient for the entire main window
        palette = QPalette()
        palette.setBrush(QtGui.QPalette.ColorRole.Window, QBrush(gradient))
        Dialog.setPalette(palette)

        self.tableWidget = QtWidgets.QTableWidget(parent=Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 671, 674))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.setColumnWidth(0, 200)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.setColumnWidth(1, 400)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.setColumnWidth(2, 60)
        self.widget = QtWidgets.QWidget(parent=Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 681, 46))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_button = QtWidgets.QPushButton(parent=self.widget)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.delete_button = QtWidgets.QPushButton(parent=self.widget)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        self.delete_all_button = QtWidgets.QPushButton(parent=self.widget)
        self.delete_all_button.setObjectName("delete_all_button")
        self.horizontalLayout.addWidget(self.delete_all_button)
        self.move_up_button = QtWidgets.QPushButton(parent=self.widget)
        self.move_up_button.setObjectName("move_up_button")
        self.horizontalLayout.addWidget(self.move_up_button)
        self.move_down_button = QtWidgets.QPushButton(parent=self.widget)
        self.move_down_button.setObjectName("move_down_button")
        self.horizontalLayout.addWidget(self.move_down_button)
        self.import_button = QtWidgets.QPushButton(parent=self.widget)
        self.import_button.setObjectName("import_button")
        self.horizontalLayout.addWidget(self.import_button)
        self.export_button = QtWidgets.QPushButton(parent=self.widget)
        self.export_button.setObjectName("export_button")
        self.horizontalLayout.addWidget(self.export_button)
        self.close_button = QtWidgets.QPushButton(parent=self.widget)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dictionary"))
        Dialog.setWindowIcon(QIcon(resource_path("resources/dictionary_icon.png")))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Description"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Type"))
        self.add_button.setText(_translate("Dialog", "Add"))
        self.delete_button.setText(_translate("Dialog", "Delete"))
        self.delete_all_button.setText(_translate("Dialog", "Delete All"))
        self.move_up_button.setText(_translate("Dialog", "Move Up"))
        self.move_down_button.setText(_translate("Dialog", "Move Down"))
        self.import_button.setText(_translate("Dialog", "Import"))
        self.export_button.setText(_translate("Dialog", "Export"))
        self.close_button.setText(_translate("Dialog", "Close"))
