import binascii
import hashlib
import json
import string
import re
import zlib

import rsa
from PyQt5 import QtWidgets

from resources.ui_Deryption import DecryptorUI


class DecryptorWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = DecryptorUI()
        self.ui.setupUi(self)
        self.resize(531, 700)

        self.message = None

    def decrypt_verify_file(self):
        import base64

        def read_file(file_path):

            try:
                with open(self.ui.file_path_input, 'r') as file:
                    # is able to read RADIX64 and ONLY SIGNED data
                    self.message = file.read()
                    print(self.message)
                    try:
                        # is able to read JSON, so OnlySigned
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

            if "messageDigest" in data_dict:
                # Message is signed

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
                    print("lose")

        file_path = "path_to_your_file"
        read_file(file_path)
