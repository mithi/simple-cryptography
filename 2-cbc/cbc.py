from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import modes, Cipher
from cryptography.hazmat.backends import default_backend
from os import urandom
import sys


BLOCKSIZE = 16

def xor(x, y):
    # assert len(x) == len(y)
    a = int.from_bytes(x, "big")
    b = int.from_bytes(y, "big")
    r = a ^ b
    return r.to_bytes(len(x), "big")


def unpad(m):
    pad = m[-1]
    assert 1 <= pad <= 16, "Wrong padding"

    for i in range(1, pad + 1):
        assert m[-i] == pad, "Wrong padding"

    return m[:-pad].decode("utf-8")


def pad(pt):
    pad_size = len(pt) % BLOCKSIZE

    if pad_size != 0:
        pad = [pad_size for i in range(pad_size)]
        pt += bytes(pad)
    else:
        pad = [BLOCKSIZE for i in range(BLOCKSIZE)]
        pt += bytes(pad)
    #assert len(pt) % BLOCKSIZE == 0


def AES_DECRYPT(key):
    cipher = Cipher(AES(key), modes.ECB(), backend=default_backend())
    return cipher.decryptor().update


def AES_ENCRYPT(key):
    cipher = Cipher(AES(key), modes.ECB(), backend=default_backend())
    return cipher.encryptor().update


def encrypt_cbc(pt_string, k_string, blocksize=16):

    pt, k = bytearray(pt_string, 'utf-8'), bytes.fromhex(k_string)
    pad(pt)

    n = len(pt) // BLOCKSIZE
    current = urandom(BLOCKSIZE) #IV
    aes_encrypt = AES_ENCRYPT(k)
    ct = bytearray(current)

    for i in range(n):
        start, end = i*blocksize, (i+1)*blocksize
        m = pt[start:end]
        d = xor(m, current)
        current = aes_encrypt(d)
        ct += current

    return ct.hex()


def decrypt_cbc(ct_string, k_string):

    ct, k = bytes.fromhex(ct_string), bytes.fromhex(k_string)
    assert len(ct) % BLOCKSIZE == 0, "Invalid format"

    n = len(ct) // BLOCKSIZE
    aes_decrypt = AES_DECRYPT(k)
    m = bytearray()

    for i in range(n-1):
        start, mid, end = i*BLOCKSIZE, (i+1)*BLOCKSIZE, (i+2)*BLOCKSIZE
        cx, cy = ct[start:mid], ct[mid:end]
        d = aes_decrypt(cy)
        m += xor(cx, d)

    return unpad(m)


if __name__ == "__main__":

    print()
    print("-------------")
    print("Decrypt or Encrypt using CBC AES (16-byte blocks)")
    print("(Plaintext uses PKCS5 Padding Scheme)")
    print("-------------")

    key = None
    while True:
        key = input("Enter 16 byte hex-encoded key: ")
        try:
            bytes.fromhex(key)
            break
        except:
            print("Invalid key.")

    while True:
        action = input("Enter 1 to decrypt, or 2 to encrypt: ")
        if action not in ["1", "2"]:
            print("Invalid action.")
        else:
            break

    if action=="1":
        cipher = input("Enter hex-encoded cipher to decrypt: ")
        try:
            message = decrypt_cbc(cipher, key)
            print()
            print("Decrypted message: ")
            print(message)
        except:
            print("Unable to decrypt cipher. ")
    else:
        message = input("Enter message in plaintext to encrypt: ")
        try:
            cipher = encrypt_cbc(message, key)
            print()
            print("Encrypted message: ")
            print(cipher)
        except:
            print("Unable to encrypt message. ")

    print()
    x = input("Press any key to exit.")
