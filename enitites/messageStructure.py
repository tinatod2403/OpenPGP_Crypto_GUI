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
    message = {
        "data": data,
        "timestamp": timestamp,
        "message_digest": message_digest,
        "sender_key_id": sender_key_id,
        "recipient_key_id": recipient_key_id
    }

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
