from authentication import StreamSender, StreamReceiver
import argparse

if __name__ == "__main__":

    # -------------------
    # PARSE ARGUMENT
    # -------------------
    parser = argparse.ArgumentParser(description="Simple File Authentication System. \
        Authenticate and decode a received byte stream \
        or sign and write the bytestream to send.")

    parser.add_argument("action",  help="SIGN/VERIFY, encode to write a bytestream to send, \
            decode to read and verify a bytestream")

    parser.add_argument('src', help="Path to read bytes")
    parser.add_argument("dst", help="The path to write bytes")

    parser.add_argument("hash", default=None, help="This is NOT need for signing.")

    parser.add_argument("-i", dest="buffersize", type=int, default=1024,
        help="Number of bytes per chunk of data (default: 1024 bytes.)")

    args = parser.parse_args()

    if args.action.lower() == "sign":
        sender = StreamSender(path=args.src, buffersize=args.buffersize)
        sender.write_file(path=args.dst)

    elif args.action.lower() == "verify":
        if args.hash == None: print("Hash not specified. Please specify hash.")
        receiver = StreamReceiver(path=args.src, h= args.hash, buffersize=args.buffersize)
        receiver.write_file(path=args.dst)
    else:
        print("Invalid action. Try SIGN or VERIFY next time")
