from authentication import StreamSender, StreamReceiver
import argparse

if __name__ == "__main__":

    # -------------------
    # PARSE ARGUMENT
    # -------------------
    parser = argparse.ArgumentParser(description="Simple File Authentication System. \
        Authenticate and decode a received byte stream \
        or encode and write the bytestream to send.")

    parser.add_argument("-act", dest="action",
        help="ENCODE/DECODE, encode to write a bytestream to send, \
            decode to read and verify a bytestream")

    parser.add_argument("-src", dest="src",
        help="The path to read bytes")

    parser.add_argument("-dst", dest="dst",
        help="The path to write bytes")

    parser.add_argument("--i", dest="buffersize", type=int, default=1024,
        help="Number of bytes per chunk of data" )


    args = parser.parse_args()

    if args.action.lower() == "encode":
        print("Encoding...")
        sender = StreamSender(path=args.src, buffersize=args.buffersize)
        sender.write_file(path=args.dst)
        print("...done.")

    elif args.action.lower() == "decode":
        print("Decoding...")
        receiver = StreamReceiver(path=args.src, buffersize=args.buffersize)
        receiver.write_file(path=args.dst)
        print("...done.")
    else:
        print("Invalid action. Try ENCODE or DECODE next time")







