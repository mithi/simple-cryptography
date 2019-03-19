import argparse
from hashlib import sha256
import os
import subprocess

HASHSIZE = 32

class StreamReceiver:

    def __init__(self, path, h, buffersize=1024):
        self.stream = path
        self.buffersize = buffersize
        self.h0 = bytes.fromhex(h)

    # A generator that outputs a stream of bytes as
    # expected by our system
    def output_stream(self):
        with open(self.stream, 'rb') as f:
            n = HASHSIZE + self.buffersize
            for chunk in iter(lambda: f.read(n), ''):
                if len(chunk) == 0: break
                yield chunk

    def write_file(self, path):

        print("h0: ", self.h0.hex())
        print("Verifying...")

        chunksize = self.buffersize + HASHSIZE
        h = self.h0
        gen = self.output_stream()

        with open(path, 'wb') as f:

            for chunk in gen:
                if sha256(chunk).digest() != h:
                    raise ValueError
                h = chunk[-HASHSIZE:]
                f.write(chunk[:self.buffersize])

        print("File created: ", path)


class StreamSender:
    def __init__(self, path, buffersize):
        self.file = path
        self.buffersize = buffersize
        self.hashes = []
        self.h0 = None

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
    # The last hash written would be removed from the list and stored
    # in `self.h0` as this will be distributed to users
    def build_hashes(self):
        print("Writing hash in memory...")
        gen = self.read_block_reverse()
        h = bytes()

        for i in gen:
            h = sha256(i + h).digest()
            self.hashes.append(h)

        self.h0 = self.hashes.pop()

    # A generator that returns a chunk of bytes to be sent inorder
    # the first hash is not written as part of the file.
    # the first chunk is the first block of the file and the second hash
    # the third chunk is the second block of the file and the third hash
    # finally, the last chunk to be returned is the last block of the file
    def read_block_hash(self):
        self.build_hashes()

        with open(self.file, 'rb') as f:
            while True:
                yield f.read(self.buffersize) + self.hashes.pop()
                if len(self.hashes) == 0:
                    yield f.read(self.buffersize)
                    print("Hashes depleted.")
                    break

    def write_file(self, path):

        print("Signing...")
        gen = self.read_block_hash()
        with open(path, 'wb') as f:
            for chunk in gen:
                f.write(chunk)
        print("h0: ", self.h0.hex())
        print("File created: ", path)

    def get_first_hash(self):
        return self.h0.hex()
