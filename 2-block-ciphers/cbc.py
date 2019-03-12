from os import urandom
from helpers import xor, AES_DECRYPT, AES_ENCRYPT

BLOCKSIZE = 16

def unpad(m):
    pad = m[-1]
    assert 1 <= pad <= 16, "Wrong padding"

    for i in range(1, pad + 1):
        assert m[-i] == pad, "Wrong padding"

    return m[:-pad].decode("utf-8")


def pad(pt):
    pad_size = BLOCKSIZE - (len(pt) % BLOCKSIZE)

    if pad_size != 0:
        pad = [pad_size for i in range(pad_size)]
        pt += bytes(pad)
    else:
        pad = [BLOCKSIZE for i in range(BLOCKSIZE)]
        pt += bytes(pad)
    #assert len(pt) % BLOCKSIZE == 0


def encrypt_cbc(pt_string, k_string, blocksize=16):

    pt, k = bytearray(pt_string, 'utf-8'), bytes.fromhex(k_string)
    pad(pt)
    print(pt)
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

    print(len(ct))
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
