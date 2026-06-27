from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import hashlib


load_dotenv()


KEY = os.getenv("SECRET_KEY").encode()


cipher = Fernet(
    Fernet.generate_key()
)



def encrypt_file(data: bytes):

    encrypted = cipher.encrypt(data)

    return encrypted



def decrypt_file(data: bytes):

    decrypted = cipher.decrypt(data)

    return decrypted



def generate_hash(data: bytes):

    return hashlib.sha256(data).hexdigest()
