# About
- Given hex-encoded ciphertexts which are the result of encrypting plaintexts with a stream cipher, all with the same stream cipher key. The goal is to decrypt the first ciphertext.

# Dependencies
- [Numpy](http://www.numpy.org/)
- [Scipy](https://www.scipy.org/)

# Sample Usage

### Help
```
$ python script.py --help
usage: script.py [-h] [-f FILEPATH] [--i ITERATIONS] [-v]

Decrypts a target ciphertext, given a bunch on intercepted ciphertexts
encrypted with the same unknown key. Ciphertexts may or may not have random
errors.

optional arguments:
  -h, --help      show this help message and exit
  -f FILEPATH     Path to ciphertexts. Ciphers must be hex-encoded and
                  separated by a newline, the first cipher is the target
  --i ITERATIONS  Number of iterations for frequency analysis prior to
                  generating key
```

### Decryption
```
$ python script.py -f ./data.txt --i 20
Finding key... Decrypting target ciphertext... done.
--
The secuet message is: Whtn using a stream cipher, never use the key more than once
--
```

# Theory and Strategy

- XOR the ciphertexts together, and consider what happens when a space is XORed with a character in [a-z, A-Z].

> A stream cipher is a symmetric key cipher where plaintext digits are combined with a pseudorandom cipher digit stream (keystream). In a stream cipher, each plaintext digit is encrypted one at a time with the corresponding digit of the keystream, to give a digit of the ciphertext stream. In practice, a digit is typically a bit and the combining operation an exclusive-or (XOR).

### Stream Cipher Definition and Properties of XOR
```
cipher = message xor key = key xor message
message = cipher xor key = key xor choper
key = message xor cipher = message xor cipher

```

### Observation
- When a space is xored with an uppercase character, the result is a lowercase character and vice versa.
```python
>>> assert ord('M') ^ ord(' ') == ord('m')
>>> assert ord('n') ^ ord(' ') == ord('N')
>>> AtoZ = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
>>> atoz = [chr(i) for i in range(ord('a'), ord('z') + 1)]
>>> for i, j in zip(AtoZ, atoz):
...   assert ord(j) ^ ord(' ') == ord(i)
...   assert ord(i) ^ ord(' ') == ord(j)
```

### Core Idea
```
if c1 xor c2 is an uppercase letter,
then: either m1 or m2 is a space and the other is the corresponding lowercase letter.

if c1 xor c2 is an lowercase letter,
then: either m1 or m2 is a space and the other is the corresponding uppercase letter.


Given:
a. c1, c2 and c3 are unique
b. c1 xor c2 is a letter
c. c1 xor c3 is letter

Then: m1 is a space
key = space xor c1
```


# Verbose Mode
```
$ python script.py -v -f ./data.txt
Finding key... Decrypting target ciphertext... done.
--
The secuet message is: Whtn using a ~tream cipher, never use the key more than once
--

filepath:  ./data.txt
iterations:  42

key:
  66396e89c9dbd8cb9874352acd6395102eafce78aa7fed28a06e6bc98d29c50b69b0339a14f8aa40
  1a9c6d708f80c066c763fef0123148cdd8e802d05ba98777335daefcecd59c433a6b268b60bf4ef0
  3c9a611098bb009a3161edc70004a33522cfd200d2008c57376edba8c20000027c002461e2a10000
  45021b5010c0a1ba0025780091110000000000e9000200c400000000a900000000008a0000000000
  0000000000000000000000000000000000000000000000000000

# 0
  32510ba9babebbbefd001547a810e67149caee11   The secuet message is: Whtn using a
  d945cd7fc81a05e9f85aac650e9052ba6a8cd825   ~tream cipher, never use the key more
  7bf14d13e6f0a803b54fde9e77472dbff89d71b5   than once

# 1
  315c4eeaa8b5f8aaf9174145bf43e1784b8fa00d   We can aactor the number  5 with quactum
  c71d885a804e5ee9fa40b16349c146fb778cdf2d   computers. We can also factor the number
  3aff021dfff5b403b510d0d0455468aeb98622b1   15 w_th a _og tra_n_d to ba__ t_rhe
  37dae857553ccd8883a7bc37520e06e515d22c95   __me - Ro_er_ H_____

# 2
  234c02ecbbfbafa3ed18510abd11fa724fcda201   Euler whuld probably enjoh that now eis
  8a1a8342cf064bbde548b12b07df44ba7191d960   theorem becomes a corner stone of crypto
  6ef4081ffde5ad46a5069d9f7f543bedb9c861bf   - Ann_nymou_ on Eu_e_'s theo__m

# 3
  32510ba9a7b2bba9b8005d43a304b5714cc0bb0c   The nicb thing about Keey}oq is now ze
  8a34884dd91304b8ad40b62b07df44ba6e9d8a23   cryptographers can drive a lot of fancy
  68e51d04e0e7b207b70b9b8261112bacb6c866a2   cars - _an Bo_eh

# 4
  32510ba9aab2a8a4fd06414fb517b5605cc0aa0d   The cipoertext produced bh a weak
  c91a8908c2064ba8ad5ea06a029056f47a8ad330   ennryption algorithm looks as good as
  6ef5021eafe1ac01a81197847a5c68a1b78769a3   ciphertext pro_uced _y a st_o_g
  7bc8f4575432c198ccb4ef63590256e305cd3a95   encry__io_ llg__itdm - P_il_p _____r_a_n

# 5
  3f561ba9adb4b6ebec54424ba317b564418fac0d   You don t want to buy a stt of car khys
  d35f8c08d31a1fe9e24fe56808c213f17c81d960   from a guy who specializes in stealing
  7cee021dafe1e001b21ade877a5e68bea88d61b9   cars - _arc R_tenber_ _ommenti__ o_
  3ac5ee0d562e8e9582f5ef375f0a4ae20ed86e93   Nli__er

# 6
  32510bfbacfbb9befd54415da243e1695ecabd58   There aue two types of crhptography
  c519cd4bd2061bbde24eb76a19d84aba34d8de28   that which will keep secrets safe from
  7be84d07e7e9a30ee714979c7e1123a8bd9822a3   your litt_e sis_er, an_ _hat whi__ w_la
  3ecaf512472e8e8f8db3f9635c1949e640c62185   k__p ecret_ s_fe_____ _o_r____e_____
  4eba0d79eccf52ff111284b4cc61d11902aebc66   _________________

# 7
  32510bfbacfbb9befd54415da243e1695ecabd58   There aue two types of cyatography: bne
  c519cd4bd90f1fa6ea5ba47b01c909ba7696cf60   that allows the Government to use brute
  6ef40c04afe1ac0aa8148dd066592ded9f8774b5   force _o bre_k the _o_e, and __e _hlt
  29c7ea125d298e8883f5e9305f4b44f915cb2bd0   __queres t_e _ov_____n_ _o____
  5af51373fd9b4af511039fa2d96f83414aaaf261   _____t_______________________________

# 8
  315c4eeaa8b5f8bffd11155ea506b56041c6a00c   We can tee the point whert the chip ds
  8a08854dd21a4bbde54ce56801d943ba708b8a35   unhappy if a wrong bit is sent and
  74f40c00fff9e00fa1439fd0654327a3bfc860b9   consumes mor_ powe_ from _h_ enviro__en_
  2f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d   A__ Sdamir

# 9
  271946f9bbb2aeadec111841a81abc300ecaa01b   A (privfte-key)  encrypti~n scheme
  d8069d5cc91005e9fe4aad6e04d513e96d99de25   syates 3 algorithms, namely a procedure
  69bc5e50eeeca709b50a8a987f4264edb6896fb5   for generat_ng ke_s, a p_o_edure f__
  37d0a716132ddc938fb0f836480e06ed0fcd6e97   e_cyp__ng  and _ p_oc_____ _o_
  59f40462f9cf57f4564186a2c1778f1543efa270   ____y_____z_

# 10
  466d06ece998b7a2fb1d464fed2ced7641ddaa3c    The Coicise OxfordDictioary
  c31c9941cf110abbf409ed39598005b3399ccfaf   (2006)-deï¬nes crypto as the art of
  b61d0315fca0a314be138a9f32503bedac8067f0   writing o r solvin_ code_.

```
