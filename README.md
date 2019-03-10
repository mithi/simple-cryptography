# About 
- Python scripts that illustrate basic cryptography concepts based on Coursera Standford Cryptography I course and more
- Currently, in the process of being migrated from my [Algorithm Playground repository](https://github.com/mithi/algorithm-playground/tree/master/fifty-days/crypto)

### 1. Many Time Pad
- This script will be able to decrypt a target ciphertext, given a bunch on intercepted ciphertexts encrypted with the same key (which may or may not have random errors). A stream cipher key should never be used more than once. 

### 2. Cipher Block Chaining (CBC) 
-  This script implements CBC (with random IV) mode of encryption and decryption using AES block ciphers with PKS5 padding scheme. You'll be able to encrypt or decrypt a text given a key.

### 3. Randomized Counter Mode
- This script implements CTR (with random IV) mode of encryption and decryption using built-in AES block ciphers functions. You'll be able to encrypt and decrypt a text given a key.

### 4. Simple File Authentication with SHA256
- This script implements a simple file authentication system that simulate how you'd be able to authenticate and play video chunks as they are downloaded without having to wait for the entire file. 

### 5. Padding Oracle Attack 
- This script illustrates how you'd be able to decrypt an intercepted ciphertext if the receiver reveals whether a sent ciphertext is of valid format or not.
  
### 6.  Meet In the Middle Approach 
- This script computes the discrete log modulo a prime `p`. Given `g` and `h` that are values between `1` and `p-1`, the goal is to find the value `x` between `0` and `2^40` (More than a trillion) such that `h mod p = g^x mod p`as quickly as I know in python. Instead of using brute-force which takes `2^40` iterations worst-case, the over all worst-case using this approach is `2^20` iterations which is square-root of brute-force. 
 
### 7. Factoring Challenges
- RSA can be broken when the public modulus `N` is generated incorrectly.  These scripts illustrates how you'd be able to factor `N` when `p` and `q` are close to each other. 

 ### 8. Basic Textbook RSA Decryption
 - This script uses the information from factoring `N` to decrypt a short secret message that is encoded using PKCS v1.5 before textbook RSA function was applied. 
 
# References
- [A Graduate Course in Applied Cryptography by Dan Boneh and Victor Shoup ](https://toc.cryptobook.us/)
- [Crypto 101 by Laurens Van Houtven](https://www.crypto101.io/)
- [Crypto Pals Crypto Challenges](https://cryptopals.com/)
