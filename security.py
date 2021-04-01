import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import random
import string


class Security:
    def __init__(self):
        self.public_key = 'bw4NsfwqNeFGgHBS3YGeAvrJ8ZqZEkk079CHh8VM8-w='
        self.client_public_key = ""
        self.private_key = self.get_key()
        self.client_private_key = ""

    def encrypt(self, message, key):
        """
        This function encrypt the message with a given key
        :param message: the message to encrypt
        :param key: the key to encrypt with
        :return: the encrypted message
        """
        f = Fernet(key)
        return f.encrypt(message)  # Encrypt the bytes. The returning object is of type bytes

    def decrypt(self, data=None):
        """
        The function self.decrypt the encrypted message
        :param data: the message to self.decrypt
        :param key: the key to self.decrypt with
        :return: the self.decrypted message
        """
        return Fernet(self.private_key.encode()).decrypt(data)

    def get_key(self):
        """
        The function generate new key
        :return: the key
        """
        password = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(24)])
        password_provided = password  # This is input in the form of a string
        password = password_provided.encode()  # Convert to type bytes
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )

        key = base64.urlsafe_b64encode(kdf.derive(password))

        return key.decode()  # Can only use kdf once

    def get_send_keys(self, connection):
        """
        The function handle the keys transfer from the server
        :param connection: The connection
        :return: Nothing important
        """

        self.client_public_key = self.decrypt(connection.recv(2048)).decode()  # the client's public key

        # send the server private key encrypted by the client's public key
        send_private_key = self.encrypt(self.private_key.encode(), self.client_public_key)

        connection.sendall(send_private_key)

        self.client_private_key = self.decrypt(connection.recv(2048)).decode()
