from PyQt5 import QtWidgets
from resources.ui_Encrypton import EncryptorUI


class EncryptWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = EncryptorUI()
        self.ui.setupUi(self)
        self.resize(531, 700)


