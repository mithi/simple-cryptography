def truncate(a, b):
    n = min(len(a), len(b))
    return a[:n], b[:n]


def truncate3(a, b, c):
    n = min(len(a), len(b), len(c))
    return a[:n], b[:n], c[:n]


def xor(x, y):
    # assert len(x) == len(y)
    a = int.from_bytes(x, "big")
    b = int.from_bytes(y, "big")
    return (a ^ b).to_bytes(len(x), "big")


# Expects a textfile containing
# ciphertexts separated by new lines
# Returns a tuple
# - a list of strings (each cipher)
# - a string (the first cipher)
def parse_text(filepath):
    texts = []
    with open(filepath) as f:
        for line in f:
            s = line.strip(' \t\n\r')
            if s != '': texts.append(s)

    return texts


# Expects a list of strings representing
# byte in hex representation
# Returns the corresponding list the actual bytes
# represented by each string
def byteslist_fromhex(hexlist):
    byteslist = []
    for h in hexlist:
        byteslist.append(bytes.fromhex(h))
    return byteslist

