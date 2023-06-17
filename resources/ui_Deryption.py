from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog


class DecryptorUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.file_path_input = None
        self.setWindowTitle("Decryptor/Verifier")
        self.resize(531, 700)

    def setupUi(self, DecryptorWindow):
        # Label: "Choose File to Decrypt/Verify"
        choose_file_label = QtWidgets.QLabel("Choose File to Decrypt/Verify", DecryptorWindow)
        choose_file_label.setFont(QtGui.QFont("Arial", 16))
        choose_file_label.setGeometry(20, 20, 491, 30)

        # Line separator
        line = QtWidgets.QFrame(DecryptorWindow)
        line.setGeometry(20, 60, 491, 1)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Label: "Chosen file:"
        chosen_file_label = QtWidgets.QLabel("Chosen file:", DecryptorWindow)
        chosen_file_label.setFont(QtGui.QFont("Arial", 12))
        chosen_file_label.setGeometry(20, 70, 100, 30)

        # Label to display path
        self.file_path_label = QtWidgets.QLabel("", DecryptorWindow)
        self.file_path_label.setFont(QtGui.QFont("Arial", 10))
        self.file_path_label.setGeometry(130, 70, 381, 30)
        self.file_path_label.setWordWrap(True)

        # Button for choosing file
        self.choose_file_button = QtWidgets.QPushButton("Choose File", DecryptorWindow)
        self.choose_file_button.setFont(QtGui.QFont("Arial", 12))
        self.choose_file_button.setGeometry(20, 110, 120, 30)
        self.choose_file_button.clicked.connect(lambda: self.choose_file(DecryptorWindow))

        # Button "Decrypt/Verify"
        self.decrypt_verify_button = QtWidgets.QPushButton("Decrypt/Verify", DecryptorWindow)
        self.decrypt_verify_button.setFont(QtGui.QFont("Arial", 12))
        self.decrypt_verify_button.setGeometry(140, 110, 120, 30)
        self.decrypt_verify_button.setEnabled(False)
        self.decrypt_verify_button.clicked.connect(lambda: self.decrypt_verify_file(DecryptorWindow))

        # Line separator
        line2 = QtWidgets.QFrame(DecryptorWindow)
        line2.setGeometry(20, 160, 491, 1)
        line2.setFrameShape(QtWidgets.QFrame.HLine)
        line2.setFrameShadow(QtWidgets.QFrame.Sunken)

        # Label: "Status"
        status_label = QtWidgets.QLabel("Status", DecryptorWindow)
        status_label.setFont(QtGui.QFont("Arial", 16))
        status_label.setGeometry(20, 170, 491, 30)

        # Line separator
        line3 = QtWidgets.QFrame(DecryptorWindow)
        line3.setGeometry(20, 210, 491, 1)
        line3.setFrameShape(QtWidgets.QFrame.HLine)
        line3.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.decryption_status_label = QtWidgets.QLabel("Decryption status:", DecryptorWindow)
        self.decryption_status_label.setFont(QtGui.QFont("Arial", 12))
        self.decryption_status_label.setGeometry(20, 220, 491, 30)

        palette = self.decryption_status_label.palette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0, 128))
        self.decryption_status_label.setPalette(palette)

        # Label for displaying decryption messages
        self.decryption_message_label = QtWidgets.QLabel("", DecryptorWindow)
        self.decryption_message_label.setFont(QtGui.QFont("Arial", 12))
        self.decryption_message_label.setGeometry(20, 260, 491, 30)
        self.decryption_message_label.setWordWrap(True)

        # Label: "Verification status:"
        self.verification_status_label = QtWidgets.QLabel("Verification status:", DecryptorWindow)
        self.verification_status_label.setFont(QtGui.QFont("Arial", 12))
        self.verification_status_label.setGeometry(20, 300, 491, 30)

        palette = self.decryption_status_label.palette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0, 128))
        self.verification_status_label.setPalette(palette)

        # Label for displaying verification messages
        self.verification_message_label = QtWidgets.QLabel("", DecryptorWindow)
        self.verification_message_label.setFont(QtGui.QFont("Arial", 12))
        self.verification_message_label.setGeometry(20, 340, 491, 30)
        self.verification_message_label.setWordWrap(True)

        self.save_original_button = QtWidgets.QPushButton("Save Original", DecryptorWindow)
        self.save_original_button.setGeometry(20, 400, 120, 30)
        self.save_original_button.setFont(QtGui.QFont("Arial", 12))
        self.save_original_button.clicked.connect(self.save_original)

        # Disable widgets and button initially
        self.disable_widgets()

    def choose_file(self, DecryptorWindow):
        self.file_path_input, _ = QtWidgets.QFileDialog.getOpenFileName(DecryptorWindow, "Choose File")
        self.file_path_label.setText(self.file_path_input)

        if self.file_path_input:
            self.enable_widgets()

    def decrypt_verify_file(self, DecryptorWindow):
        DecryptorWindow.decrypt_verify_file()

    def save_original(self):
        pass

    def enable_widgets(self):
        self.decrypt_verify_button.setEnabled(True)
        self.decryption_message_label.setText("")
        self.verification_message_label.setText("")

    def disable_widgets(self):
        self.decrypt_verify_button.setEnabled(False)
        self.decryption_status_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.verification_status_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")
        self.save_original_button.setEnabled(False)
