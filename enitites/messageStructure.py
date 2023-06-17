import base64
import binascii
import zlib

from Crypto.Cipher import CAST
import json


def main():
    # Define the session key
    session_key = b'Sixteen byte key'

    # Initialize the CAST5 cipher with the session key
    cipher = CAST.new(session_key, CAST.MODE_ECB)  # Use ECB mode for simplicity, but it's not recommended for general use

    # Message components
    data = "Hello, this is the message content."
    timestamp = "2023-06-14 10:00:00"
    message_digest = "abc123"
    sender_key_id = "ABCDEF123456"
    recipient_key_id = "987654321DEF"

    # Create a dictionary to represent the message components
    message = {}
    message["data"]=b']t\xf9&\x8b\xfc@\xd1W\xab&a\tC\xa8y\x04\xd7dA\xd3\xa8\x8e\x0c%{qA\x92\x06\xf4\xc5\xd2<\xfbZ\x0e\xe8s0R\x8a\x18\xc0_\xbc\xf5\xf5m\x99s\x0c\xc2\x8a\xe7\xc5\xe3\xe8\xbf\xd9K-\xe6\'\xf3\xf8\xa6\xc18\xe2\x88\xb8\xd2\xdf\xbd=\xee(\xa3\xabu<\x9e\xebB\xd3\xe7\xb0+ci\x93*\xa7\xaa$yElB$\xa8C_\x90\x9e\x9f\xcb\xf8\xf0\xa1\xb3\xa1\x11\x19\x96\x10\x0c@s\xcc\x1e\x86\xbc\xa2\x82\xea\x90\xfd<\xbf\xe97T\x99\xc6\xc9\xed\xb5\xbb<\xd7\xfb\xe0\xfe\xd2R\xcdU2\xfc\x13\x88nt[\x8d\xe1\x9fZD\xc6\x0fsI\x16\xd3c\x16"\xa3\x89tV\xebx\x00\xc2\xc6\x1dwd\xf6Jn\x1d\x90>\x19C\x1e\xefj\xa2\'*!\xc4\x10\xe7\xdb\xee\xcdD\x19\xcd\xbe*\xbd@|Q\x92\xeee6\x17\x0b\xc0,#\xd6\xcfr\xe1\xd1t\x95..\x8fw|0h\xb8\x1b\x93\x06\x81\xa1X\xcfkNkS\xc2\xe7O);\xde\x90\xc2\xed'
    message["zoka"] = 234
    # Convert the message dictionary to JSON
    message_json = json.dumps(message)

    # Convert the JSON message to bytes
    message_bytes = message_json.encode('utf-8')

    # Pad the message to a multiple of 8 bytes if needed
    padding_length = 8 - (len(message_bytes) % 8)
    padded_message_bytes = message_bytes + bytes([padding_length]) * padding_length

    # Encrypt the padded message
    encrypted_message = cipher.encrypt(padded_message_bytes)
    asad=message_bytes.decode('utf-8')
    message = json.loads(asad)
    print("Message: ", message)
    print("Message: ",message_bytes)
    compressed_data = zlib.compress(message_bytes)
    print("compressed_data: ", compressed_data)

    try:
        decompressed_data = zlib.decompress(message_bytes)
        print("decompressed_data: ", decompressed_data)
    except zlib.error:
        print("GRESKA")

    radix_encoded_data = base64.b64encode(compressed_data)
    print("radix_encoded_data: ", radix_encoded_data)

    try:
        print("nesto ", base64.b64decode(compressed_data))

    except binascii.Error:
        print("NECE")

if __name__ == '__main__':
    main()
