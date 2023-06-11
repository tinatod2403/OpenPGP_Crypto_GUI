from PyQt5 import QtWidgets, QtCore

class KeyManagerUI(object):
    dropdown_KeySize = None
    def __init__(self):
        self.backButton = None
        self.error_label = None
        self.dropdown_KeySize = None
        self.dropdown_ALG = None
        self.textbox_Email = None
        self.textbox_Username = None
        self.textbox_Password = None
        self.generate_key_button = None

    def setupUi(self, KeyManagerWindow):
        KeyManagerWindow.setObjectName("KeyManagerWindow")
        KeyManagerWindow.resize(531, 531)
        KeyManagerWindow.setWindowTitle("KEY MANAGER")

        self.textbox_Username = QtWidgets.QLineEdit(KeyManagerWindow)
        self.textbox_Username.setGeometry(200, 50, 200, 30)

        self.textbox_Email = QtWidgets.QLineEdit(KeyManagerWindow)
        self.textbox_Email.setGeometry(200, 100, 200, 30)

        self.dropdown_ALG = QtWidgets.QComboBox(KeyManagerWindow)
        self.dropdown_ALG.setGeometry(200, 150, 200, 30)

        self.dropdown_KeySize = QtWidgets.QComboBox(KeyManagerWindow)
        self.dropdown_KeySize.setGeometry(200, 200, 200, 30)

        self.textbox_Password = QtWidgets.QLineEdit(KeyManagerWindow)
        self.textbox_Password.setGeometry(200, 250, 200, 30)
        self.textbox_Password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.generate_key_button = QtWidgets.QPushButton(KeyManagerWindow)
        self.generate_key_button.setGeometry(200, 300, 200, 30)
        self.generate_key_button.setText("GENERATE KEY")

        self.dropdown_ALG.addItems(["RSA", "DSA + ElGamal"])
        self.dropdown_KeySize.addItems(["1024", "2048"])

        username = QtWidgets.QLabel("Username", KeyManagerWindow)
        username.setGeometry(20, 50, 150, 30)

        email = QtWidgets.QLabel("Email", KeyManagerWindow)
        email.setGeometry(20, 100, 150, 30)

        ALG = QtWidgets.QLabel("Algorithm for asymmetric keys", KeyManagerWindow)
        ALG.setGeometry(20, 150, 150, 30)

        key_size = QtWidgets.QLabel("Key size", KeyManagerWindow)
        key_size.setGeometry(20, 200, 150, 30)

        password = QtWidgets.QLabel("Password", KeyManagerWindow)
        password.setGeometry(20, 250, 150, 30)

        self.error_label = QtWidgets.QLabel("", KeyManagerWindow)
        self.error_label.setGeometry(200, 350, 200, 30)
        self.error_label.setStyleSheet("color: red")

        self.backButton = QtWidgets.QPushButton("Cancel", KeyManagerWindow)
        self.backButton.setGeometry(QtCore.QRect(20, 450, 150, 30))
        self.backButton.setStyleSheet("background-color: black; color: white;")

        self.generate_key_button.clicked.connect(KeyManagerWindow.generate_key)


class KeyManagerWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)

        self.ui = KeyManagerUI()
        self.ui.setupUi(self)
