# Main
#
# Application: Routine Checking App
#
# Create by: Tu Nguyen Ngoc


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication
from views.ui_mainwindow import Ui_MainWindow
from controllers.main_controller import MainController
import sys

def main():
    app = QApplication(sys.argv)
    mainWindow = MainController()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
