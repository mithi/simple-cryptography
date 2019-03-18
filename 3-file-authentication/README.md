# About
- A simple file authentication system that simulate how you'd be able to authenticate and play video chunks as they are downloaded without having to wait for the entire file.
![Simple File Authentication System](./data/task.png)

# Sample Usage

### Help
```
$ python script.py -h
usage: script.py [-h] [--i BUFFERSIZE] action src dst

Simple File Authentication System. Authenticate and decode a received byte
stream or sign and write the bytestream to send.

positional arguments:
  action          SIGN/VERIFY, encode to write a bytestream to send, decode to
                  read and verify a bytestream
  src             Path to read bytes
  dst             The path to write bytes

optional arguments:
  -h, --help      show this help message and exit
  --i BUFFERSIZE  Number of bytes per chunk of data (default: 1024 bytes.)
```

### Sign
```
$ python script.py SIGN ./data/video1.mp4 ./data/SIGNED.bin --i 1024
Encoding...
Writing hash in memory...
Done.
Hashes depleted. Writing last byte...
Done.
Final stream encoded in:  ./data/SIGNED.bin
...done.
```

### Verify
```
$ python script.py VERIFY ./data/SIGNED.bin ./data/VERIFED.mp4 --i 1024
Decoding...
Stream verified, decoded written in:  ./data/VERIFED.mp4
...done.
```
