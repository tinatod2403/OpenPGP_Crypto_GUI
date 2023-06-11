from PyQt5 import QtWidgets
import sys
from controllers.start_menu import StartMenu


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    start_menu = StartMenu()
    start_menu.show()

    sys.exit(app.exec_())

