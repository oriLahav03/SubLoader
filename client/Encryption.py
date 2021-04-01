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
        self.server_public_key = 'bw4NsfwqNeFGgHBS3YGeAvrJ8ZqZEkk079CHh8VM8-w='
        self.server_private_key = ''

        self.my_public_key = self.get_key()
        self.my_private_key = self.get_key()

    def encrypt(self, message, key):
        f = Fernet(key)
        return f.encrypt(message)

    def decrypt(self, data=None, key=b'WrongKey'):
        return Fernet(key).decrypt(data)

    def get_key(self):
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

    def send_my_keys(self, conn):
        conn.sendall(self.encrypt(self.my_public_key, self.server_public_key.encode()))
        self.server_private_key = self.decrypt(conn.recv(1024), self.my_public_key.encode())
        conn.sendall(self.encrypt(self.my_private_key, self.server_private_key))
