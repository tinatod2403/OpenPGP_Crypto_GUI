import base64
import binascii
import hashlib
import json
import os
import zlib

import rsa
from Crypto.Cipher import CAST, DES3, AES
from Crypto.Random import get_random_bytes
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
        self.message_encrypt = {}
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
        self.isEncrypted = self.ui.checkbox_encrypt.isChecked()
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

                        # print("e")
                        # print(value['public_key'])
                        # is_valid = rsa.verify(data_hash, bytes.fromhex(self.message_sign["messageDigest"]), rsa.PublicKey.load_pkcs1(value['public_key']))
                        #
                        # if is_valid:
                        #     print("Signature is valid.")
                        # else:
                        #     print("Signature is not valid.")

                        message_sign_json = json.dumps(self.message_sign)
                        message_sign_bytes = message_sign_json.encode('utf-8')
                        # padding_length = 8 - (len(message_sign_bytes) % 8)
                        # self.message_sign_bytes = message_sign_bytes + bytes([padding_length]) * padding_length
                        self.message_sign_bytes = message_sign_bytes
                        print(self.message_sign_bytes)
                        self.ui.successLabel.setText("Successfully signed data.")
                    else:
                        self.ui.errorLabel.setText("Password incorect for private key")
                        return
        else:
            message_sign_json = json.dumps(self.message_sign)
            message_sign_bytes = message_sign_json.encode('utf-8')
            self.message_sign_bytes = message_sign_bytes

        file_name = os.path.basename(self.ui.file_path_input)
        self.file_output_directory = os.path.join(self.file_output_directory, file_name + ".sgn")


        if self.isEncrypted:
            if self.ui.radio_button_cast5.isChecked():
                key = get_random_bytes(16)
                cipher = CAST.new(key, CAST.MODE_OPENPGP)
                plaintext = self.message_sign_bytes
                msg = cipher.encrypt(plaintext)
                print("CAST: ", msg)

                self.message_encrypt["message"] = msg.hex()
                self.message_encrypt["sessionKey"] = self.encryptSessionKey(key).hex()
                self.message_encrypt["keyID_recipient"] = self.ui.dropdown_public_key.currentText()

                print(self.message_encrypt)
                message_sign_json = json.dumps(self.message_encrypt)
                self.message_sign_bytes = message_sign_json.encode('utf-8')
                self.ui.successLabel.setText(self.ui.successLabel.text() + "\n" + "Successfully encrypted data using CAST5")

                # eiv = msg[:CAST.block_size + 2]
                # ciphertext = msg[CAST.block_size + 2:]
                # cipher = CAST.new(key, CAST.MODE_OPENPGP, eiv)
                # print("original: ", cipher.decrypt(ciphertext))
            else:
                key = get_random_bytes(32)
                cipher = AES.new(key, AES.MODE_EAX)
                nonce = cipher.nonce
                ciphertext, tag = cipher.encrypt_and_digest(self.message_sign_bytes)
                print("The message is ciphertext:", ciphertext)

                self.message_encrypt["message"] = ciphertext.hex()
                self.message_encrypt["sessionKey"] = self.encryptSessionKey(key).hex()
                self.message_encrypt["keyID_recipient"] = self.ui.dropdown_public_key.currentText()
                self.message_encrypt["nonce"] = nonce.hex()
                print(self.message_encrypt)

                message_sign_json = json.dumps(self.message_encrypt)
                self.message_sign_bytes = message_sign_json.encode('utf-8')
                self.ui.successLabel.setText(self.ui.successLabel.text() + "\n" + "Successfully encrypted data using AES128")

                # cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
                # plaintext = cipher.decrypt(ciphertext)
                # print("The message is plaintext:", plaintext)
                # try:
                #     cipher.verify(tag)
                #     print("The message is authentic:", plaintext)
                # except ValueError:
                #     print("Key incorrect or message corrupted")

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

    def encryptSessionKey(self, sessionKey):
        keyID_recipient = self.ui.dropdown_public_key.currentText()
        # print(keyID_recipient)
        with open('publicKeyRing.json', 'r') as file:
            publicKeyRing = json.load(file)
            for item in publicKeyRing:
                if keyID_recipient in item:
                    public_key_pem = item[keyID_recipient]["public_key"]
        public_key = rsa.PublicKey.load_pkcs1(public_key_pem)
        # print(public_key)
        data = sessionKey
        encrypted_sessionKey = rsa.encrypt(data, public_key)

        return encrypted_sessionKey
