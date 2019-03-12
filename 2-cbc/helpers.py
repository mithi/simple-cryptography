from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import modes, Cipher
from cryptography.hazmat.backends import default_backend


def xor(x, y):
    # assert len(x) == len(y)
    a = int.from_bytes(x, "big")
    b = int.from_bytes(y, "big")
    return (a ^ b).to_bytes(len(x), "big")


def AES_DECRYPT(key):
    cipher = Cipher(AES(key), modes.ECB(), backend=default_backend())
    return cipher.decryptor().update


def AES_ENCRYPT(key):
    cipher = Cipher(AES(key), modes.ECB(), backend=default_backend())
    return cipher.encryptor().update
