import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

cipher_suite = Fernet(os.getenv("APP_FERNET_KEY"))


def encrypt_password(password):
    encrypted_text = cipher_suite.encrypt(password.encode())
    return encrypted_text


def decrypt_password(encrypted_password):
    decrypted_text = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_text
