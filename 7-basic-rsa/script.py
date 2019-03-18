import argparse
from publickeysystem import encrypt_pipeline, decrypt_pipeline
import textwrap

def print_digit(x):
    x = textwrap.wrap(x, width=64)
    for i in x:
        print("  ", i)


def read_file(path):
    with open(path, 'rb') as f:
        file_size = f.seek(0, 2)
        f.seek(0)
        return f.read(file_size).decode('utf8')


def run(args):

    # -------------------
    # VERIFY ARGUMENTS
    # -------------------

    if args.a.lower() not in ["encrypt", "decrypt"]:
        print("You must specify which action (encrypt/decrypt)")
        return

    f, e_or_d, start, end = None, None, None, None
    N, n, x, y = None, None, None, None

    try:
        N = int(read_file(args.N))
        n = int(read_file(args.i))
    except:
        print("Something went wrong.")
        print("Please check your file paths, and/or the content of your file/s.")
        return

    x = read_file(args.x)

    if args.a.lower() == "encrypt":

        print("Encrypting...")
        f = encrypt_pipeline
        e_or_d = "Private exponent"
        start = "Plaintext"
        end = "Ciphertext"

    else: #decrypt

        try:
            int(x)
        except:
            print("Your ciphertext must be a decimal integer.")

        print("Decrypting...")
        f = decrypt_pipeline
        e_or_d = "Private exponent"
        start = "Ciphertext"
        end = "Plaintext"

    # -------------------
    # ENCRYPT OR DECRYPT
    # -------------------

    try:
        y = f(x, n, N)
    except:
        print("Something went wrong during the process")

    # -------------------
    # PRINT RESULT
    # -------------------

    print("\nN = ")
    print_digit(str(N))

    print("\n", e_or_d, " = ")
    print_digit(str(n))


    print("\n", start, " = ")
    print_digit(str(x))

    print()
    print("-------------------")
    print(" RESULT ")
    print("-------------------")

    print("\n", end, " = ")
    print_digit(y)
    print()


if __name__ == "__main__":

    # -------------------
    # PARSE ARGUMENT
    # -------------------
    parser = argparse.ArgumentParser(description="a pipeline using basic RSA encryption and decryption.\
        A modified PKCS v1.5 is applied to the short secret message prior to RSA encry!ption and upon decryption,\
        the plaintext recovered is assumed to have a modified PKCS 1 v1.5 format.. \
        IMPORTANT: PKCS v1.5 is severely broken in the real world and should be really used!\
        ")

    parser.add_argument("-a", dest="a",
        help="encrypt/decrypt", required=True)

    parser.add_argument("-x", dest="x",
        help="Path to the string you want to decrypt or encrypt", required=True)

    parser.add_argument("-N", dest="N",
        help="Path were N is stored", required=True)

    parser.add_argument("-i", dest="i",
        help="Path were e or d is stored", required=True)

    args = parser.parse_args()
    run(args)


