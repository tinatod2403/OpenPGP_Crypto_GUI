from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QPushButton, QLabel, QCheckBox, QLineEdit, QComboBox, QRadioButton, QFileDialog


class EncryptorUI(object):

    def __init__(self):
        self.errorLabel = None
        self.data = None

    def setupUi(self, EncryptorWindow):
        # Checkbox - Encrypt
        self.checkbox_encrypt = QCheckBox("Encrypt", EncryptorWindow)
        self.checkbox_encrypt.move(20, 20)

        # Label - Algorithm for Encryption
        self.label_algorithm = QLabel("Algorithm for encryption:", EncryptorWindow)
        self.label_algorithm.move(20, 60)

        # Radio Buttons - Triple DES and CAST5
        self.radio_button_triple_des = QRadioButton("Triple DES", EncryptorWindow)
        self.radio_button_triple_des.move(20, 90)
        self.radio_button_cast5 = QRadioButton("CAST5", EncryptorWindow)
        self.radio_button_cast5.move(20, 110)

        # Dropdown Menu - Public Key
        self.dropdown_public_key = QComboBox(EncryptorWindow)
        self.dropdown_public_key.move(20, 150)
        self.dropdown_public_key.addItem("Public Key 1")
        self.dropdown_public_key.addItem("Public Key 2")

        # Line for separation
        self.line1 = QLabel(EncryptorWindow)
        self.line1.setStyleSheet("background-color: black")
        self.line1.setGeometry(20, 190, 491, 2)

        # Checkbox - Sign
        self.checkbox_sign = QCheckBox("Sign", EncryptorWindow)
        self.checkbox_sign.move(20, 200)

        # Dropdown Menu - Password
        self.dropdown_password = QComboBox(EncryptorWindow)
        self.dropdown_password.move(20, 240)
        self.dropdown_password.addItem("Password 1")
        self.dropdown_password.addItem("Password 2")

        # Text Box - Enter Password for Private Key
        self.textbox_private_key = QLineEdit(EncryptorWindow)
        self.textbox_private_key.move(20, 280)
        self.textbox_private_key.setPlaceholderText("Enter password for private key")

        # Line for separation
        self.line2 = QLabel(EncryptorWindow)
        self.line2.setStyleSheet("background-color: black")
        self.line2.setGeometry(20, 320, 491, 2)

        # Checkbox - Compress
        self.checkbox_compress = QCheckBox("Compress", EncryptorWindow)
        self.checkbox_compress.move(20, 330)

        # Line for separation
        self.line3 = QLabel(EncryptorWindow)
        self.line3.setStyleSheet("background-color: black")
        self.line3.setGeometry(20, 370, 491, 2)

        # Checkbox - Radix-64 Conversion
        self.checkbox_radix64 = QCheckBox("Radix-64 Conversion", EncryptorWindow)
        self.checkbox_radix64.move(20, 380)

        # Line for separation
        self.line4 = QLabel(EncryptorWindow)
        self.line4.setStyleSheet("background-color: black")
        self.line4.setGeometry(20, 420, 491, 2)

        # Label - Choose File to Encrypt
        self.label_choose_file = QLabel("Choose file to encrypt:", EncryptorWindow)
        self.label_choose_file.move(20, 430)

        # Button - Choose File
        self.button_choose_file = QPushButton("Choose File", EncryptorWindow)
        self.button_choose_file.move(20, 460)

        # Label - Choose Output Directory
        self.label_choose_directory = QLabel("Choose output directory:", EncryptorWindow)
        self.label_choose_directory.move(20, 500)

        # Button - Encrypt
        self.button_encrypt = QPushButton("Encrypt", EncryptorWindow)
        self.button_encrypt.move(20, 530)

        # Connect button signals
        self.button_choose_file.clicked.connect(lambda: self.choose_file(EncryptorWindow))
        self.button_encrypt.clicked.connect(lambda: self.encrypt_file(EncryptorWindow))
    #
    def choose_file(self, EncryptorWindow):
        file_dialog = QFileDialog(EncryptorWindow)
        file_path = file_dialog.getOpenFileName(EncryptorWindow, "Choose File")[0]
        print("Selected File:", file_path)

    def encrypt_file(self,EncryptorWindow):
        # Implement the encryption logic here
        pass



