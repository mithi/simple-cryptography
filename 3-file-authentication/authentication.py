import argparse
from hashlib import sha256
import os

HASHSIZE = 32

class StreamReceiver:

    def __init__(self, path, buffersize=1024):
        self.stream = path
        self.buffersize = buffersize

    # A generator that outputs a stream of bytes as
    # expected by our system
    def output_stream(self):
        with open(self.stream, 'rb') as f:

            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            f.seek(0)
            yield f.read(HASHSIZE)
            chunksize = HASHSIZE + self.buffersize
            while filesize - f.tell() > self.buffersize:
                yield f.read(chunksize)
            yield f.read(self.buffersize)

    def write_file(self, path):
        chunksize = self.buffersize + HASHSIZE
        gen = self.output_stream()
        with open(path, 'wb') as f:
            h = next(gen)
            for chunk in gen:
                if sha256(chunk).digest() != h:
                    print(h.hex())
                    print(sha256(chunk).digest().hex())
                    print(chunk.hex())
                    raise ValueError
                h = chunk[-HASHSIZE:]
                f.write(chunk[:self.buffersize])
        print("Stream verified, decoded written in: ", path)


class StreamSender:
    def __init__(self, path, buffersize):
        self.file = path
        self.hash = path + "hash"
        self.buffersize = buffersize

    # A generator that reads a block of data (size `buffersize` in bytes)
    # at a time, starting from the last block to the first block of the file
    # The last block of the file (which is the first block we read)
    # might be less than the buffersize while all other blocks are exactly
    # of length `buffersize`
    def read_block_reverse(self):

        with open(self.file, 'rb') as f:
            f.seek(0, os.SEEK_END)
            filesize = f.tell()
            firstchunk = filesize % self.buffersize

            if firstchunk != 0:
                f.seek(filesize - firstchunk)
                yield f.read(firstchunk)

            f.seek(-firstchunk-self.buffersize, os.SEEK_END)
            move = -2*self.buffersize

            while True:
                yield f.read(self.buffersize)
                if f.tell() <= self.buffersize: break
                f.seek(move, 1)

    # Given a file, write all the hashes that must be sent so that the
    # receiver can authenticate the file.
    # The first hash is the hash of the last block
    # The second hash is the hash of the the concatenation of the
    # last block and the first hash
    # and so on until the last hash written is the hash of
    # the concatenation of the last block and the second to the last hash
    def write_hash(self):
        gen = self.read_block_reverse()
        h = bytes()

        with open(self.hash, 'wb') as f:
            for i in gen:
                h = sha256(i + h).digest()
                f.write(h)

        print("All hashes written in: ", self.hash)

    # A generator that returns a chunk of bytes to be sent inorder
    # the first chunk is the first hash
    # the second chunk is the first block of the file and the second hash
    # the third chunk is the second block of the file and the third hash
    # finally, the last chunk to be returned is the last block of the file
    def read_block_hash(self):

        with open(self.hash, "rb") as hf:

            move = -2 * HASHSIZE
            hf.seek(0, os.SEEK_END)
            hf.seek(-HASHSIZE, os.SEEK_END)

            yield hf.read(HASHSIZE)

            with open(self.file, 'rb') as f:
                while True:
                    hf.seek(move, 1)
                    yield f.read(self.buffersize) + hf.read(HASHSIZE)
                    if hf.tell() == HASHSIZE:
                        yield f.read(self.buffersize)
                        break

    # Write the total stream of bytes to path
    def write_file(self, path):
        self.write_hash()

        gen = self.read_block_hash()
        with open(path, 'wb') as f:
            for chunk in gen:
                f.write(chunk)
        print("Final stream encoded in: ", path)

    # Verifies if the file and the hash file matches
    def verify_hash(self):

        gen = self.read_block_hash()
        h = next(gen)

        for chunk in gen:
            if sha256(chunk).digest() != h:
                return False
            h = chunk[-HASHSIZE:]
        return True

    # Given the file return the first hash to be sent to the receiver
    def compute_first_hash(self):

        gen = self.read_block_reverse()
        h = bytes()

        for i in gen:
            h = sha256(i + h).digest()
        return h
