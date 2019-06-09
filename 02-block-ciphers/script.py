from cbc import encrypt_cbc, decrypt_cbc
from ctr import encrypt_ctr, decrypt_ctr


if __name__ == "__main__":

    print()
    print("------------- ")
    print("BLOCK CIPHER MODE OF OPERATION ")
    print("------------- ")

    mode, key = None, None

    while True:
        mode = input("Enter preferred mode of operation [cbc/ctr]: ").lower()
        if mode not in ["cbc", "ctr"]:
            print("Invalid mode.")
        else:
            break


    while True:
        key = input("Enter hex-encoded key: ")
        try:
            k = bytes.fromhex(key)
            if mode == "cbc" and len(k) != 16:
                print("for CBC mode, key must be 16 bytes. ")
                raise ValueError
            break
        except:
            print("Invalid key.")

    while True:
        action = input("Decrypt or encrypt?[d/e]: ").lower()
        if action not in ["d", "e"]:
            print("Invalid action.")
        else:
            break

    if action == "d":

        cipher = input("Enter hex-encoded cipher to decrypt: ")
        print()

        try:
            message = None
            if mode == "cbc":
                message = decrypt_cbc(cipher, key)
            else:
                message = decrypt_ctr(cipher, key)

            print("Decrypted message: ")
            print(message)
        except:
            print("Unable to decrypt cipher. ")

    else:

        message = input("Enter message in plaintext to encrypt: ")

        try:
            cipher = None
            if mode == "cbc":
                cipher = encrypt_cbc(message, key)
            else:
                cipher = encrypt_ctr(message, key)

            print("Encrypted message: ")
            print(cipher)
        except:
            print("Unable to encrypt message. ")

    print()
    x = input("Press any key to exit. ")
