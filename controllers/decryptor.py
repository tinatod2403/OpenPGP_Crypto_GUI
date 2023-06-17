import binascii
import json
import string
import re

from PyQt5 import QtWidgets

from resources.ui_Deryption import DecryptorUI


class DecryptorWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = DecryptorUI()
        self.ui.setupUi(self)
        self.resize(531, 700)

        self.message=None


    def decrypt_verify_file(self):
        import base64

        def read_file(file_path):

            try:
                with open(self.ui.file_path_input, 'r') as file:
                    #is able to read RADIX64 and ONLY SIGNED data
                    self.message = file.read()
                    print(self.message)
                    try:
                        self.message = base64.b64decode(self.message)
                    except binascii.Error:
                        print("NECE")
            except UnicodeDecodeError:
                with open(self.ui.file_path_input, 'rb') as file:
                    # is able to read binary, COMPRESSED data
                    self.message = file.read()
                    print(self.message)

        file_path = "path_to_your_file"
        read_file(file_path)
