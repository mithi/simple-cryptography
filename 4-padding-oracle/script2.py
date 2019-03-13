from paddingoracle import PaddingOracle, decode
import textwrap

if __name__ == "__main__":

    print("------------------------------------")
    print("PADDING ORACLE ATTACK!")
    print("------------------------------------")

    print("\nEnter target server address which you know is vulnerable to this kind of attack. \n")
    print("e.g.")
    print("  crypto-class.appspot.com")
    print("  127.0.0.1:9000")

    print("\nWhen a decrypted CBC ciphertext ends in an invalid pad, ", end="")
    print("the web server returns a 403 error code (forbidden request).")
    print("When the CBC padding is valid, but the message is malformed,", end="")
    print("the web server returns a 404 error code (URL not found).\n")

    while True:
        raw = input("Target Website: ").lower()

        print("\nIs this correct?\n")
        print("http://" + raw + "/")
        print()

        valid = input("[y/n]: ")

        if valid.lower() == 'y':
            break

    target = "http://" + raw + "/po?er="

    print("\nWe will be sending arbitary http request to this website of the form:")
    print(target + "ARBITRARY_HEX_ENCODED_CIPHERTEXT_HERE")
    print()


    print("Enter the hex-encoded ciphertext that you want to decode.\n")

    print("We are expecting a string of 128 characters in length,", end="")
    print("which represents a 16-byte initialization vector (IV)")
    print("and three blocks of encrypted message. (16 bytes per block)", end="")
    print("The decrypted message is expected to be in utf-8 with PKCS #5/#7 padding scheme.")
    print()

    while True:

        ciphertext = input("Target Ciphertext: ")

        if len(ciphertext) != 128:
            print("\nCiphertext must be be 128 characters in length.")
            continue
        try:
            bytes.fromhex(ciphertext)
            break
        except:
            print("Your ciphertext must be hex-encoded.")


    print("\n------------------------------------\n")
    print("Target website:", raw)
    print("Format: ", target + "CIPHERTEXT")
    print("Ciphertext: \n")

    c = textwrap.wrap(ciphertext, width=32)
    for i in c:
        print(i)


    raw_decryption = None
    print("\n------------------------------------")
    print("Decrypting... \n")

    try:
        po = PaddingOracle(target)
        raw_decryption = po.decrypt4blocks(ciphertext)
        print("\n...done.")
    except:
        print("Something went wrong. ")

    print("\n------------------------------------")
    print("Your ciphertext decrypted in raw bytes:")
    print(raw_decryption)
    print("\n------------------------------------")
    try:
        message = decode(raw_decryption)
        print("\nHere's the final result:")
        print(message)
    except:
        print("The format of the decrypted message is unexpected.", end="")
        print("The result might be incorrectly padded or a non-utf8 message. \n")

    print("\n------------------------------------")
    input("Press any key to continue.")
