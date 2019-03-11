from helpers import parse_text, byteslist_fromhex
from manytimepad import find_key, decode
import argparse
import textwrap


if __name__ == "__main__":

    # -------------------
    # PARSE ARGUMENT
    # -------------------
    parser = argparse.ArgumentParser(description="Decrypts a target ciphertext, \
        given a bunch on intercepted ciphertexts encrypted with the same unknown key. \
        Ciphertexts may or may not have random errors.")

    parser.add_argument("-f", dest="filepath",
        help="Path to ciphertexts. Ciphers must be hex-encoded and separated by a newline,\
              the first cipher is the target")

    parser.add_argument("--i", dest="iterations", type=int, default=42,
        help="Number of iterations for frequency analysis prior to generating key" )

    parser.add_argument('-v', dest="verbose", action='store_true', default=False,
                    help='Display more information')

    args = parser.parse_args()

    # --------------------
    # FIND KEY AND DECRYPT
    # --------------------
    cipherstrings = parse_text(args.filepath)
    ciphers = byteslist_fromhex(cipherstrings)

    print("Finding key... ", end="")
    key = find_key(ciphers, iterations=args.iterations)

    print("Decrypting target ciphertext...", end="")
    message = decode(ciphers[0], key)

    print(" done.")
    print("--")
    print(message)
    print("--")

    # --------------------
    # DISPLAY MORE INFORMATION
    # --------------------
    n = 40
    if args.verbose is True:
        print()
        print("filepath: ", args.filepath)
        print("iterations: ", args.iterations)

        print()
        print("key:")
        ks = textwrap.wrap(key.hex(), width=2*n)

        for k in ks:
            print(" ", k)

        for i, cipherstring in enumerate(cipherstrings):
            message = decode(ciphers[i], key)
            ms = textwrap.wrap(message, width=n)
            cs = textwrap.wrap(cipherstring, width=n)

            print()
            print("#", i)

            for c, m in zip(cs, ms):
                print(" ", c, " ", m)
