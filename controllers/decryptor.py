import base64
import binascii
import hashlib
import json
import string
import re
import zlib

import rsa
from Crypto.Cipher import CAST, AES
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from resources.ui_Deryption import DecryptorUI, PasswordDialog


class DecryptorWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.data_dict = None
        self.ui = DecryptorUI()
        self.ui.setupUi(self)
        self.resize(531, 700)

        self.message = None

    def decrypt_verify_file(self):
        self.ui.disableWarning()
        self.ui.disable_widgets()
        try:
            with open(self.ui.file_path_input, 'r') as file:
                # is able to read RADIX64 and ONLY SIGNED data
                self.message = file.read()
                print(self.message)
                try:
                    # is able to read JSON, so (OnlySigned) or (OnlySigned and Encrypted)
                    data_dict = json.loads(self.message)
                    print("Not Radix64, only signed")
                    print("signed: ", data_dict)
                except:
                    # is NOT able to read JSON, so Radix64
                    self.message = base64.b64decode(self.message)
                    try:
                        self.message = zlib.decompress(self.message)
                        data_dict = json.loads(self.message)
                    except:
                        data_dict = json.loads(self.message)
                    print("RADIX: ", data_dict)

        except UnicodeDecodeError:
            with open(self.ui.file_path_input, 'rb') as file:
                # is able to read binary, COMPRESSED data
                self.message = file.read()
                self.message = zlib.decompress(self.message)
                data_dict = json.loads(self.message)
                print("COMPRESSED: ", data_dict)
        except Exception:
            self.ui.enableWarning("The file has been depricated.")
            return


        if "sessionKey" in data_dict:
            # Message is encrypted
            keyID_recipien = data_dict["keyID_recipient"]
            with open('privateKeyRing.json', 'r') as file:
                privateKeyRing = json.load(file)
                for row, item in enumerate(privateKeyRing):
                    key = list(item.keys())[0]
                    values = item[key]
                    if key == keyID_recipien:
                        private_key = values.get('private_key', '')
            try:
                print(data_dict)
                password_dialog = PasswordDialog()
                password_dialog.setupUI(keyID_recipien)
                password_dialog.exec_()
                private_key = self.decryptPrivateKey(private_key, password_dialog.textbox.text())
                if private_key is None:
                    self.ui.enableWarning("Wrong password")
                    return
                else:
                    self.ui.disableWarning()
                private_key = rsa.PrivateKey.load_pkcs1(private_key)
                session_key = rsa.decrypt(bytes.fromhex(data_dict["sessionKey"]), private_key)

                msg = bytes.fromhex(data_dict["message"])
                print(msg)
                if "nonce" in data_dict:
                    print("tu")
                    cipher = AES.new(session_key, AES.MODE_EAX, nonce=bytes.fromhex(data_dict["nonce"]))
                    data_dict_bytes = cipher.decrypt(msg)
                    print(data_dict_bytes)
                    data_dict = json.loads(data_dict_bytes)
                    self.ui.decryption_message_label.setText("Encryption done using AES128\n" +
                                                             "Decryption succeeded \nMessage for: " + keyID_recipien)
                    self.ui.enable_decrypt()
                else:

                    eiv = msg[:CAST.block_size + 2]
                    ciphertext = msg[CAST.block_size + 2:]
                    cipher = CAST.new(session_key, CAST.MODE_OPENPGP, eiv)
                    data_dict_bytes = cipher.decrypt(ciphertext)
                    print(data_dict_bytes)
                    data_dict = json.loads(data_dict_bytes)
                    self.ui.decryption_message_label.setText("Encryption done using CAST5\n" +
                                                             "Decryption succeeded \nMessage for: " + keyID_recipien)
                    self.ui.enable_decrypt()

            except Exception:
                self.ui.decryption_error_message_label.setText("Decryption failed\nMessage has been depricated")
                self.ui.enable_decrypt()

        if "messageDigest" in data_dict:
            # Message is signed
            print(data_dict["keyID_sender"])
            public_key_ID = data_dict["keyID_sender"]
            with open('privateKeyRing.json', 'r') as file:
                publicKeyRing = json.load(file)
                for key, item in enumerate(publicKeyRing):
                    key = list(item.values())[0]
                    print(public_key_ID)
                    if key['public_key_ID'] == public_key_ID:
                        public_key = key['public_key']

            try:
                public_key = rsa.PublicKey.load_pkcs1(public_key)

                # Verify the signature using the public key
                data_bytes = data_dict["data"].encode('utf-8')

                sha1_hash = hashlib.sha1()
                sha1_hash.update(data_bytes)
                data_hash = sha1_hash.digest()

                is_valid = rsa.verify(data_hash, bytes.fromhex(data_dict["messageDigest"]), public_key)
                self.ui.verification_message_label.setText(
                    "Verification succeeded \nSigner info: " + key['username'] + " " +
                    key['email'] + "\n" + "Signature created on: " + data_dict["timestamp"])
                self.ui.enable_verify()
            except rsa.pkcs1.VerificationError:
                self.ui.verification_error_message_label.setText("Verification failed\nMessage has been depricated")
                self.ui.enable_verify()
        self.data_dict = data_dict




    def decryptPrivateKey(self, privateKey, password):

        print(self.passwordCorrect(privateKey, password))
        privateKey = self.passwordCorrect(privateKey, password)
        return privateKey

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

    def saveOriginalMess(self):
        file_path, _ = QFileDialog.getSaveFileName(None, "Select File","")
        print("Selected File:", file_path)
        with open(file_path, 'w') as file:
            file.write(self.data_dict["data"])
