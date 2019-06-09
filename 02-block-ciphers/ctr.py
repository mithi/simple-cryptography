from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import modes, Cipher
from cryptography.hazmat.backends import default_backend
from os import urandom
from math import ceil
from helpers import xor, AES_ENCRYPT


def do_counter_mode(k, iv, x, blocksize, ivsize):

    aes = AES_ENCRYPT(k)
    long_k = bytearray()
    n = ceil(len(x) / blocksize)

    for i in range(0, n):
        c = aes((iv+i).to_bytes(ivsize, "big"))
        long_k += c

    return xor(x, long_k[:len(x)])


def encrypt_ctr(pt_string, key_string, blocksize=16, ivsize=16):
    k = bytes.fromhex(key_string)
    pt = bytes(pt_string, 'utf-8')
    iv_raw = urandom(ivsize)
    iv = int.from_bytes(iv_raw, "big")
    ct_raw = do_counter_mode(k, iv, pt, blocksize, ivsize)
    return iv_raw.hex() + ct_raw.hex()


def decrypt_ctr(ct_string, key_string, blocksize=16, ivsize=16):
    k = bytes.fromhex(key_string)
    c = bytes.fromhex(ct_string)
    iv = int.from_bytes(c[:ivsize], "big")
    msg = do_counter_mode(k, iv, c[ivsize:], blocksize, ivsize)
    return str(msg, 'utf-8')
