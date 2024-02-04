# Main
#
# Application: Routine Checking App
#
# Create by: Tu Nguyen Ngoc


import sys
from PyQt6.QtWidgets import QApplication
from controllers.main_controller import MainController
from database.db import initialize_database

def main():
    # Initialize the database
    initialize_database()

    app = QApplication(sys.argv)
    mainWindow = MainController()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
