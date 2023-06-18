import json

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QLabel, QCheckBox, QLineEdit, QComboBox, QRadioButton, QFileDialog


class EncryptorUI(object):

    def __init__(self):
        self.directory_path_output = None
        self.dataPrivateKeys = None
        self.dataPublicKeys = None
        self.file_path_input = None




    def setupUi(self, EncryptorWindow):
        self.EncryptorWindow=EncryptorWindow
        # Checkbox - Encrypt
        self.checkbox_encrypt = QCheckBox("Encrypt/Sign", EncryptorWindow)
        self.checkbox_encrypt.setFont(QtGui.QFont("Arial", 12))
        self.checkbox_encrypt.move(20, 20)

        # Label - Algorithm for Encryption
        self.label_algorithm = QLabel("Algorithm for encryption:", EncryptorWindow)
        self.label_algorithm.setFont(QtGui.QFont("Arial", 12))
        self.label_algorithm.move(20, 60)

        # Radio Buttons - Triple DES and CAST5
        self.radio_button_triple_des = QRadioButton("AES128", EncryptorWindow)
        self.radio_button_triple_des.setFont(QtGui.QFont("Arial", 12))
        self.radio_button_triple_des.move(20, 90)
        self.radio_button_triple_des.setChecked(True)
        self.radio_button_triple_des.setEnabled(False)
        self.radio_button_cast5 = QRadioButton("CAST5", EncryptorWindow)
        self.radio_button_cast5.setFont(QtGui.QFont("Arial", 12))
        self.radio_button_cast5.move(20, 110)
        self.radio_button_cast5.setEnabled(False)  # Initially disabled

        # Dropdown Menu - Public Key
        self.dropdown_public_key = QComboBox(EncryptorWindow)
        self.dropdown_public_key.setFont(QtGui.QFont("Arial", 12))
        self.dropdown_public_key.move(20, 150)
        with open('publicKeyRing.json', 'r') as file:
            self.dataPublicKeys = json.load(file)
            for item in self.dataPublicKeys:
                key = list(item.keys())[0]
                self.dropdown_public_key.addItem(key)
        self.dropdown_public_key.setEnabled(False)  # Initially disabled

        # Line for separation
        self.line1 = QLabel(EncryptorWindow)
        self.line1.setStyleSheet("background-color: black")
        self.line1.setGeometry(20, 190, 491, 2)

        # Checkbox - Sign
        self.checkbox_sign = QCheckBox("Sign", EncryptorWindow)
        self.checkbox_sign.setFont(QtGui.QFont("Arial", 12))
        self.checkbox_sign.move(20, 200)

        # Dropdown Menu - Password
        self.dropdown_privateKey = QComboBox(EncryptorWindow)
        self.dropdown_privateKey.setFont(QtGui.QFont("Arial", 12))
        self.dropdown_privateKey.move(20, 240)
        with open('privateKeyRing.json', 'r') as file:
            self.dataPrivateKeys = json.load(file)
            for item in self.dataPrivateKeys:
                key = list(item.keys())[0]
                self.dropdown_privateKey.addItem(key)
        self.dropdown_privateKey.setEnabled(False)  # Initially disabled

        # Text Box - Enter Password for Private Key
        self.textbox_password = QLineEdit(EncryptorWindow)
        self.textbox_password.setFont(QtGui.QFont("Arial", 12))
        self.textbox_password.move(20, 280)
        self.textbox_password.setPlaceholderText("Enter password for private key")
        self.textbox_password.setEnabled(False)

        # Line for separation
        self.line2 = QLabel(EncryptorWindow)
        self.line2.setStyleSheet("background-color: black")
        self.line2.setGeometry(20, 320, 491, 2)

        # Checkbox - Compress
        self.checkbox_compress = QCheckBox("Compress", EncryptorWindow)
        self.checkbox_compress.setFont(QtGui.QFont("Arial", 12))
        self.checkbox_compress.move(20, 330)

        # Line for separation
        self.line3 = QLabel(EncryptorWindow)
        self.line3.setStyleSheet("background-color: black")
        self.line3.setGeometry(20, 370, 491, 2)

        # Checkbox - Radix-64 Conversion
        self.checkbox_radix64 = QCheckBox("Radix-64 Conversion", EncryptorWindow)
        self.checkbox_radix64.setFont(QtGui.QFont("Arial", 12))
        self.checkbox_radix64.move(20, 380)

        # Line for separation
        self.line4 = QLabel(EncryptorWindow)
        self.line4.setStyleSheet("background-color: black")
        self.line4.setGeometry(20, 420, 491, 2)

        # Label - Choose File to Encrypt
        self.label_choose_file = QLabel("Choose file to encrypt:", EncryptorWindow)
        self.label_choose_file.setFont(QtGui.QFont("Arial", 12))
        self.label_choose_file.move(20, 430)

        # Button - Choose File
        self.button_choose_file_input = QPushButton("Choose File", EncryptorWindow)
        self.button_choose_file_input.setFont(QtGui.QFont("Arial", 12))
        self.button_choose_file_input.move(20, 460)

        # Label - Choose Output Directory
        self.label_choose_directory = QLabel("Choose output directory:", EncryptorWindow)
        self.label_choose_directory.setFont(QtGui.QFont("Arial", 12))
        self.label_choose_directory.move(20, 500)

        # Button - Encrypt
        self.button_choose_file_output = QPushButton("Choose File", EncryptorWindow)
        self.button_choose_file_output.setFont(QtGui.QFont("Arial", 12))
        self.button_choose_file_output.move(20, 530)

        self.encrypt_sign = QPushButton("Encrypt", EncryptorWindow)
        self.encrypt_sign.setFont(QtGui.QFont("Arial", 12))
        self.encrypt_sign.move(20, 560)
        self.encrypt_sign.setEnabled(False)

        self.label_selected_file_input = QLabel("", EncryptorWindow)
        self.label_selected_file_input.setFont(QtGui.QFont("Arial", 12))
        self.label_selected_file_input.move(120, 460)
        self.label_selected_file_input.setFixedWidth(500)
        self.label_selected_file_input.setStyleSheet("color: blue;")

        # Label - Selected Output Directory
        self.label_selected_directory_output = QLabel("", EncryptorWindow)
        self.label_selected_directory_output.setFont(QtGui.QFont("Arial", 12))
        self.label_selected_directory_output.move(120, 530)
        self.label_selected_directory_output.setFixedWidth(500)
        self.label_selected_directory_output.setStyleSheet("color: blue;")

        self.errorLabel = QLabel("", EncryptorWindow)
        self.errorLabel.setFont(QtGui.QFont("Arial", 12))
        self.errorLabel.setStyleSheet("color: red;")
        self.errorLabel.move(20, 600)
        self.errorLabel.setFixedWidth(500)

        self.successLabel = QLabel("", EncryptorWindow)
        self.successLabel.setFont(QtGui.QFont("Arial", 12))  # Increase the font size to 16
        self.successLabel.setStyleSheet("color: green;")
        self.successLabel.setGeometry(20, 600, 500, 100)  # Adjust the geometry to set the desired width and height

        self.button_choose_file_input.clicked.connect(lambda: self.choose_file_input(EncryptorWindow))
        self.button_choose_file_output.clicked.connect(lambda: self.choose_directory_output(EncryptorWindow))
        self.encrypt_sign.clicked.connect(self.checkInputEmpty)

        # Connect checkbox signal
        self.checkbox_encrypt.stateChanged.connect(self.toggle_encrypt_options)
        self.checkbox_sign.stateChanged.connect(self.toggle_sign_options)

        self.checkbox_encrypt.stateChanged.connect(self.toggle_encrypt_decript_options)
        self.checkbox_sign.stateChanged.connect(self.toggle_encrypt_decript_options)

        self.back_button = QtWidgets.QPushButton("Back", EncryptorWindow)
        self.back_button.setStyleSheet("background-color: black; color: white;")
        self.back_button.setFont(QtGui.QFont("Arial", 12))
        self.back_button.setGeometry(430, 640, 90, 30)

        self.back_button.clicked.connect(lambda: self.backtoStart(EncryptorWindow))

    def backtoStart(self, EncryptorWindow):
        from controllers.start_menu import StartMenu
        EncryptorWindow.hide()
        startMenu = StartMenu()
        startMenu.exec_()

    def toggle_encrypt_options(self, state):
        encrypt_enabled = state == QtCore.Qt.Checked
        self.radio_button_triple_des.setEnabled(encrypt_enabled)
        self.radio_button_cast5.setEnabled(encrypt_enabled)
        self.dropdown_public_key.setEnabled(encrypt_enabled)

    def toggle_sign_options(self, state):
        sign_enabled = state == QtCore.Qt.Checked
        self.textbox_password.setEnabled(sign_enabled)
        self.dropdown_privateKey.setEnabled(sign_enabled)

    def choose_file_input(self, EncryptorWindow):
        file_dialog_input = QFileDialog(EncryptorWindow)
        self.file_path_input = file_dialog_input.getOpenFileName(EncryptorWindow, "Choose File")[0]
        self.label_selected_file_input.setText(self.file_path_input)

    def choose_directory_output(self, EncryptorWindow):
        file_dialog_output = QFileDialog(EncryptorWindow)
        self.directory_path_output = file_dialog_output.getExistingDirectory(EncryptorWindow, "Choose Directory")
        self.label_selected_directory_output.setText(self.directory_path_output)

    def toggle_encrypt_decript_options(self, state):
        encrypt_enabled = state == QtCore.Qt.Checked
        self.encrypt_sign.setEnabled(encrypt_enabled)

    def checkInputEmpty(self):
        if self.checkbox_sign.isChecked():
            if self.textbox_password.text() == "":
                self.errorLabel.setText("Missing password for private key.")
                return

        if self.file_path_input is None:
            self.errorLabel.setText("Missing input file.")
            return

        if self.directory_path_output is None:
            self.errorLabel.setText("Missing output directory.")
            return

        self.errorLabel.setText("")
        self.EncryptorWindow.getDataAndStartEncrypt()
