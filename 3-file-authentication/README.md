# About
- A simple file authentication system that simulate how you'd be able to authenticate and play video chunks as they are downloaded without having to wait for the entire file.
![Simple File Authentication System](./data/task.png)

# Sample Usage

### Help
```
$ python script.py -h
usage: script.py [-h] [-act ACTION] [-src SRC] [-dst DST] [--i BUFFERSIZE]

Simple File Authentication System. Authenticate and decode a received byte
stream or encode and write the bytestream to send.

optional arguments:
  -h, --help      show this help message and exit
  -act ACTION     ENCODE/DECODE, encode to write a bytestream to send, decode
                  to read and verify a bytestream
  -src SRC        The path to read bytes
  -dst DST        The path to write bytes
  --i BUFFERSIZE  Number of bytes per chunk of data
```

### Encoding
```
$ python script.py -act ENCODE -src ./data/video1.mp4 -dst ./data/encoded1.bin --i 1024
Encoding...
Writing hash in:  ./data/video1.mp4hash ...
All hashes written in:  ./data/video1.mp4hash
Deleting hash file...
Final stream encoded in:  ./data/encoded1.bin
...done.
```

### Decoding
```
$ python script.py -act DECODE -src ./data/encoded1.bin -dst ./data/video1copy.mp4 --i 1024
Decoding...
Stream verified, decoded written in:  ./data/video1copy.mp4
...done.
```
