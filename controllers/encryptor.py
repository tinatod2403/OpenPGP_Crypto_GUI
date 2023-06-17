import base64
import hashlib
import json
import os
import zlib

import rsa
from Crypto.Cipher import CAST
from PyQt5 import QtWidgets
from resources.ui_Encrypton import EncryptorUI
from datetime import datetime


class EncryptWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = EncryptorUI()
        self.ui.setupUi(self)
        self.resize(531, 700)

        self.message_sign = {}
        self.message_sign_bytes = None
        self.message_sign_radix64 = None

        self.sessionKey = None
        self.keyID_recipient = None

        self.isSigned = None
        self.isEncrypted = None
        self.isZipped = False
        self.isRadix64 = False
        self.encryptAlgorithm = None
        self.publicKeyEncrypt = None
        self.privateKeySign = None
        self.privateKeyPassword = None

        self.file_output_directory = None

    def getDataAndStartEncrypt(self):
        # self.isEncrypted = self.ui.checkbox_encrypt.isChecked()
        # if self.radio_button_triple_des.isChecked():
        #     self.encryptAlgorithm = "Triple DES"
        # else:
        #     self.encryptAlgorithm = "CAST5"
        # self.publicKeyEncrypt = self.ui.dropdown_public_key.currentText()
        self.isSigned = self.ui.checkbox_sign.isChecked()
        self.privateKeySign = self.ui.dropdown_privateKey.currentText()
        self.privateKeyPassword = self.ui.textbox_password.text()
        self.isZipped = self.ui.checkbox_compress.isChecked()
        self.isRadix64 = self.ui.checkbox_radix64.isChecked()

        self.file_output_directory = self.ui.directory_path_output

        if self.ui.file_path_input is None:
            print("nema datoteke")
        else:
            with open(self.ui.file_path_input, "r") as file:
                self.message_sign["data"] = file.read()
                self.message_sign["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Code for signing
        if self.isSigned:
            data_bytes = self.message_sign["data"].encode('utf-8')

            sha1_hash = hashlib.sha1()
            sha1_hash.update(data_bytes)
            data_hash = sha1_hash.digest()

            for key, item in enumerate(self.ui.dataPrivateKeys):
                key = list(item.keys())[0]
                if key == self.privateKeySign:
                    value = item[key]
                    private_key = value['private_key']
                    self.message_sign["keyID_sender"] = value['public_key_ID']
                    pam_key = self.passwordCorrect(private_key, self.privateKeyPassword)
                    if pam_key is not None:
                        private_key_original = rsa.PrivateKey.load_pkcs1(pam_key)
                        signature = rsa.sign(data_hash, private_key_original, 'SHA-1')
                        self.message_sign["messageDigest"] = signature.hex()

                        message_sign_json = json.dumps(self.message_sign)
                        message_sign_bytes = message_sign_json.encode('utf-8')
                        padding_length = 8 - (len(message_sign_bytes) % 8)
                        self.message_sign_bytes = message_sign_bytes + bytes([padding_length]) * padding_length
                        print(self.message_sign_bytes)
                        self.ui.successLabel.setText("Successfully signed data.")
                    else:
                        self.ui.errorLabel.setText("Password incorect for private key")
                        return

        file_name = os.path.basename(self.ui.file_path_input)
        self.file_output_directory = os.path.join(self.file_output_directory, file_name + ".sgn")

        if self.isZipped:
            asd = "asd"
            asd = 123
            self.message_sign_bytes = zlib.compress(self.message_sign_bytes)
            self.ui.successLabel.setText(self.ui.successLabel.text() + "\n" + "Successfully zipped data")

        if self.isRadix64:
            message_sign_radix64_encode = base64.b64encode(self.message_sign_bytes)
            self.message_sign_radix64 = message_sign_radix64_encode.decode('utf-8')
            self.ui.successLabel.setText(self.ui.successLabel.text() + "\n" + "Successfully converted to radix64")
            with open(self.file_output_directory, "w") as file:
                file.write(self.message_sign_radix64)
                self.ui.successLabel.setText(
                    self.ui.successLabel.text() + "\n" + "Writen to:" + self.file_output_directory)
        else:
            with open(self.file_output_directory, "wb") as file:
                file.write(self.message_sign_bytes)
                self.ui.successLabel.setText(
                    self.ui.successLabel.text() + "\n" + "Writen to:" + self.file_output_directory)

    def passwordCorrect(self, private_key, password):
        password_bytes = password.encode('utf-8')

        sha1_hash = hashlib.sha1()
        sha1_hash.update(password_bytes)
        key = sha1_hash.digest()
        key = key[:16]

        msg = bytes.fromhex(private_key)

        try:
            eiv = msg[:CAST.block_size + 2]
            ciphertext = msg[CAST.block_size + 2:]
            cipher = CAST.new(key, CAST.MODE_OPENPGP, eiv)

            k = cipher.decrypt(ciphertext)

            kljuc = k.decode('utf-8')
            return kljuc
        except ValueError as e:
            return None
