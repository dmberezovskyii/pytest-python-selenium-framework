from cryptography.fernet import Fernet


class Decryption:
    def __init__(self):
        self.fernet = Fernet

    def generate(self):
        key = self.fernet.generate_key().decode('UTF-8').strip()
        return key
