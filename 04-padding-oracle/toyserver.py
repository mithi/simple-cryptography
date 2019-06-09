from http.server import BaseHTTPRequestHandler, HTTPServer
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers import modes, Cipher
from cryptography.hazmat.backends import default_backend
from os import urandom

HOST_NAME = 'localhost'
PORT_NUMBER = 9000

BLOCKSIZE = 16
KEY_HEXSTRING = "140b41b22a29beb4061bda66b6747e14"
KEY = bytes.fromhex(KEY_HEXSTRING)


def xor(x, y):
    # assert len(x) == len(y)
    a = int.from_bytes(x, "big")
    b = int.from_bytes(y, "big")
    r = a ^ b
    return r.to_bytes(len(x), "big")


def unpad(m):
    pad = m[-1]
    if pad < 1 or pad > 16:
        return 403, None

    for i in range(1, pad + 1):
        if m[-i] != pad:
            return 403, None

    try:
        message = m[:-pad].decode("utf-8")
    except:
        return 404, None

    return 200, message


def AES_DECRYPT(key):
    cipher = Cipher(AES(key), modes.ECB(), backend=default_backend())
    return cipher.decryptor().update


def decrypt_cbc(ct_string):

    ct = bytes.fromhex(ct_string)

    if len(ct) % BLOCKSIZE != 0:
        return 500, None

    n = len(ct) // BLOCKSIZE
    aes_decrypt = AES_DECRYPT(KEY)
    m = bytearray()

    for i in range(n-1):
        start, mid, end = i*BLOCKSIZE, (i+1)*BLOCKSIZE, (i+2)*BLOCKSIZE
        cx, cy = ct[start:mid], ct[mid:end]
        d = aes_decrypt(cy)
        m += xor(cx, d)

    return unpad(m)


class CryptoHandler(BaseHTTPRequestHandler):

    def set_response(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):

        if self.path[:7] != "/po?er=":
            self.set_response(500)

        cipher_string = self.path[7:]
        status_code, message = decrypt_cbc(cipher_string)
        print(message, status_code)

        self.set_response(status_code)

        if message is None:
            self.wfile.write("Bad things happened.".encode('utf-8'))

        self.wfile.write("Message: {}".format(message).encode('utf-8'))


if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), CryptoHandler)

    try:
        print("Serving at", HOST_NAME, ":", PORT_NUMBER)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
print("... Closed server.")
