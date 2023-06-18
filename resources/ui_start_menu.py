from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Start_menu(object):
    def setupUi(self, Start_menu):
        Start_menu.setObjectName("Start_menu")
        Start_menu.resize(531, 700)

        # Add QLabel for the centered title
        self.title_label = QtWidgets.QLabel(Start_menu)
        self.title_label.setGeometry(QtCore.QRect(0, 20, 531, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setObjectName("title_label")
        self.title_label.setText("PGP PROTOCOL")

        font.setPointSize(12)

        self.key_manager = QtWidgets.QPushButton(Start_menu)
        self.key_manager.setGeometry(QtCore.QRect(27, 80, 141, 321))
        self.key_manager.setObjectName("key_manager")
        self.key_manager.setFont(font)

        self.encryptor = QtWidgets.QPushButton(Start_menu)
        self.encryptor.setGeometry(QtCore.QRect(187, 80, 141, 321))
        self.encryptor.setObjectName("encryptor")
        self.encryptor.setFont(font)

        self.decryptor = QtWidgets.QPushButton(Start_menu)
        self.decryptor.setGeometry(QtCore.QRect(347, 80, 141, 321))
        self.decryptor.setObjectName("decryptor")
        self.decryptor.setFont(font)

        self.retranslateUi(Start_menu)
        QtCore.QMetaObject.connectSlotsByName(Start_menu)

    def retranslateUi(self, Start_menu):
        _translate = QtCore.QCoreApplication.translate
        Start_menu.setWindowTitle(_translate("Start_menu", "Dialog"))
        self.key_manager.setText(_translate("Start_menu", "Key manager"))
        self.encryptor.setText(_translate("Start_menu", "encrypt"))
        self.decryptor.setText(_translate("Start_menu", "decrypt"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    font = QtGui.QFont()
    font.setPointSize(12)
    app.setFont(font)

    start_menu = QtWidgets.QDialog()
    ui = Ui_Start_menu()
    ui.setupUi(start_menu)
    start_menu.show()

    sys.exit(app.exec_())
