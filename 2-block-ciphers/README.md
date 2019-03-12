# Cipher Block Chaining
I've implemented two block cipher encryption/decryption systems; CBC and CTR mode of operation. We use AES for  decryption and encryption of each 16-byte block. The 16-byte encryption IV is chosen at random and is prepended to the ciphertext. For CBC, PKCS#5/#7 padding scheme is used. Note that for every encryption of the same message and the same key, a different ciphertext is generated, all ciphertext decrypt to the message.

# Theory

- [AES (Advanced Encryption Standard)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [PKCS #5/#7 padding scheme](https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS#5_and_PKCS#7) as described in [RFC 5652](https://tools.ietf.org/html/rfc5652#section-6.3)
```
01
02 02
03 03 03
04 04 04 04
05 05 05 05 05
06 06 06 06 06 06
etc.
```

### CBC

- [Cipher Block Chaining](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_(CBC))
![Cipher Block Chaining](./img/cbc-diagram.png)

```
Properties

Encryption parallelizable:  No
Decryption parallelizable:  Yes
Random read access: Yes
```

### CTR
- [Counter mode with randomized IV](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Counter_(CTR))
![Cipher Block Chaining](./img/cbc-diagram.png)
```
Properties

Encryption parallelizable:  Yes
Decryption parallelizable:  Yes
Random read access: Yes
```
# Dependency
- [pyca/cryptography](https://cryptography.io/en/latest/)

# Sample Usage
```
$ python script.py

-------------
BLOCK CIPHER MODE OF OPERATION
-------------
Enter preferred mode of operation [cbc/ctr]: ctr
Enter hex-encoded key: 36f18357be4dbd77f050515c73fcf9f2
Decrypt or encrypt?[d/e]: d
Enter hex-encoded cipher to decrypt: 69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329

Decrypted message:
CTR mode lets you build a stream cipher from a block cipher.

Press any key to exit.
```

# Test Cases

## CBC
- Key: `140b41b22a29beb4061bda66b6747e14`

### Cipher A
- The following cipher decrypts to `Basic CBC mode encryption needs padding.`
when the key above is used
```
4ca00ff4c898d61e1edbf1800618fb28
28a226d160dad07883d04e008a7897ee
2e4b7465d5290d0c0e6c6822236e1daa
fb94ffe0c5da05d9476be028ad7c1d81
```

### Cipher B
- The following cipher decrypts to `Our implementation uses rand. IV`
when the key above is used.
```
5b68629feb8606f9a6667670b75b38a5
b4832d0f26e1ab7da33249de7d4afc48
e713ac646ace36e872ad5fb8a512428a
6e21364b0c374df45503473c5242a253"
```

## CTR
- Key: `36f18357be4dbd77f050515c73fcf9f2`

### Cipher C
- The following cipher decrypts to `CTR mode lets you build a stream cipher from a block cipher.`
when the key above is used.
```
69dda8455c7dd4254bf353b773304eec
0ec7702330098ce7f7520d1cbbb20fc3
88d1b0adb5054dbd7370849dbf0b88d3
93f252e764f1f5f7ad97ef79d59ce29f
5f51eeca32eabedd9afa9329
```

### Cipher D
- The following cipher decrypts to `Always avoid the two time pad!`
when the key above is used.
```
770b80259ec33beb2561358a9f2dc617
e46218c0a53cbeca695ae45faa8952aa
0e311bde9d4e01726d3184c34451
```
