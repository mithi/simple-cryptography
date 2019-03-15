# About
- Here is a pipeline using basic RSA encryption and decryption. A modified PKCS v1.5 is applied to the short secret message prior to RSA encryption and upon decryption, the plaintext recovered is assumed to have a modified PKCS #1 v1.5 format.

# Our Modified PCKS1.5
```

The size of the message is the RSA Modulus Size:
which in our case is 128 bytes
Minimum required random nonzero bytes is 8.
+------+------------------------------+------+--------------------+
| 0x02 | RANDOM NONZERO BYTES         | 0x00 | MESSAGE IN ASCII   |
+------+------------------------------+------+--------------------+
```

- In PKCS #1 v1.5 mod 2
```
The size of the message is the RSA Modulus Size:
e.g 2048 bits or 256 bytes or
+--------+------------------------------+------+--------------------+
| 0x0002 | RANDOM NONZERO BYTES         | 0x00 | MESSAGE IN ASCII   |
+--------+------------------------------+------+--------------------+
```
- Where there is atleast 8 bytes. So the maximum size of the message must be less than the size of the modulus size minus 11.
- PKCS v1.5 is a specification widely used like in HTTPS but it turns out that this is not semantically secure. You can rean more about the attack on the paper by **Bleichenbacher 1998**
- This is because the attacker can test if the 16 most significant bits are `0x0002`.
- You can learn more [about PKCS1.5 in rfc2313](https://tools.ietf.org/html/rfc2313)


# Sample use

### Help
```
$ python script.py -h
usage: script.py [-h] -a A -x X -N N -i I

a pipeline using basic RSA encryption and decryption. A modified PKCS v1.5 is
applied to the short secret message prior to RSA encry!ption and upon
decryption, the plaintext recovered is assumed to have a modified PKCS 1 v1.5
format.. IMPORTANT: PKCS v1.5 is severely broken in the real world and should
be really used!

optional arguments:
  -h, --help  show this help message and exit
  -a A        encrypt/decrypt, encode to write a bytestream to send, decode to
              read and verify a bytestream
  -x X        Path to the string you want to decrypt or encrypt
  -N N        Path were N is stored
  -i I        Path were e or d is stored
```

### Encrypting
```
$ python script.py -a encrypt -N ./data/N.txt -i ./data/e.txt -x ./data/m.txt
Your ciphertext must be a decimal integer.
Encrypting...


N =
   1797693134862315907729305190789024733617976978942306572734300811
   5773267580550562068698537944921298295958550138753716401571013985
   8647833778606925583497541085196591615128057575940752635007475935
   2887108236499499407718956170543611494748650467110151015639406805
   27540071584560878577663743040086340742855278549092581

 Private exponent  =
   65537

 Plaintext  =
   Factoring lets us break RSA.

-------------------
 RESULT
-------------------

 Ciphertext  =
   2906207161056955868066823385987526234003498180944344556665355223
   4263566105138355743579987671213936541691008572423924732555948601
   2108688269299320138091072797186129048497132969408911802680013038
   4369213290911729579288965572967470444300191046940001266494090932
   1160219830175326092434405290669266160985648937995423
```

# Decrypting
```
$ python script.py -a decrypt -N ./data/N.txt -i ./data/d.txt -x ./data/c.txt
Decrypting...

N =
   1797693134862315907729305190789024733617976978942306572734300811
   5773267580550562068698537944921298295958550138753716401571013985
   8647833778606925583497541085196591615128057575940752635007475935
   2887108236499499407718956170543611494748650467110151015639406805
   27540071584560878577663743040086340742855278549092581

 Private exponent  =
   1590128797899941302944410362238731766907763942037101362915718114
   1513592652158568184727012903658813528491037910547521854815931164
   9996413081859765873862893558666786159443196819394738421950922073
   7709826999634635374410954901130658130263935313668458679622922107
   1755410527734011645528084075140176976118813890397473

 Ciphertext  =
   2209645186741038177630656113488341801741006978789283107173183914
   3676135600120538004282329650473509424343946219751512256465839967
   9428894607645420405815647489880137348641204523252293201764879166
   6640299750918872997169052608322206777160001932926087000957999372
   4077458967773697817571267229951148662959627934791540

-------------------
 RESULT
-------------------

 Plaintext  =
   Factoring lets us break RSA.
```

### Solution to sample problem
```
$ python script2.py
Given:

ciphertext =
   2209645186741038177630656113488341801741006978789283107173183914
   3676135600120538004282329650473509424343946219751512256465839967
   9428894607645420405815647489880137348641204523252293201764879166
   6640299750918872997169052608322206777160001932926087000957999372
   4077458967773697817571267229951148662959627934791540

N =
   1797693134862315907729305190789024733617976978942306572734300811
   5773267580550562068698537944921298295958550138753716401571013985
   8647833778606925583497541085196591615128057575940752635007475935
   2887108236499499407718956170543611494748650467110151015639406805
   27540071584560878577663743040086340742855278549092581

e =
   1797693134862315907729305190789024733617976978942306572734300811
   5773267580550562068698537944921298295958550138753716401571013985
   8647833778606925583497541085196591615128057575940752635007475935
   2887108236499499407718956170543611494748650467110151015639406805
   27540071584560878577663743040086340742855278549092581

And that we know |p - q| < 2 * fourthroot_of(N); therefore:

p =
   1340780792994259709957402499820584612747936582059239337772356144
   3721764030073662768891111614362326998675040546094339320838419523
   375986027530441562135724301

q =
   1340780792994259709957402499820584612747936582059239337772356144
   3721764030073778560980348930557750569660049234002192590823085163
   940025485114449475265364281

And which we can use to compute phi(N) and consequently the d.

phi(N) =
   1797693134862315907729305190789024733617976978942306572734300811
   5773267580550562068698537944921298295958550138753716401571013985
   8647833778606925583497541058380975755242863376792702638595783680
   3299791824651631853247727296108330893274237168395545566438631121
   92450291488028966916159055724074828097964241148004000

d =
   1590128797899941302944410362238731766907763942037101362915718114
   1513592652158568184727012903658813528491037910547521854815931164
   9996413081859765873862893558666786159443196819394738421950922073
   7709826999634635374410954901130658130263935313668458679622922107
   1755410527734011645528084075140176976118813890397473

Finally, the resulting plaintext:

Factoring lets us break RSA.

```

# Theory and Basic RSA
> RSA (Rivest–Shamir–Adleman) is one of the first public-key cryptosystems and is widely used for secure data transmission. The encryption key is public and it is different from the decryption key which is kept secret (private). In RSA, this asymmetry is based on the practical difficulty of the factorization of the product of two large prime number

### Public Key Encryption
- A public-key encryption system is a set of three algorithms (`G`, `E`, `D`), where
- `G()` is a randomized agorithm that outputs a key pair (`pk`, `sk`),
- `E(pk, m)` is a randomized algorithm that takes `m` that is an element of a specified set `M` and outputs `c` which is an element of a specified set `C`
- `D(sk, c)` is a deterministic algorithm that takes `c` which is an element of set `C` and outputs an `m` that is either an element of `M` or something else called a bottom.
- For consistency for every (`pk`, `sk`) pair that is an output of `G()`, then for every `m` in `M`
the following holds.
```
D(sk), E(pk, m)) = m
```

### Secure Trapdoor functions
-  A trapdoor from set `X` to `Y` is a tripple of efficient algorithms (`G`, `F`, `F_inverse`) such that
- `G()` is a randomized algorithm that outputs a key pair (`pk`, `sk`)
- `F(pk, x)` defines a function `Y` to `X`
- `F_inverse(sk, y)`  defines a funtion that inverts `F(pk, x)`
- More precisely, for every (`pk`, `sk`) output by `G()`, every element `x` of set `X` must satisfy the following:
```
F_inverse(sk, F(pk, x)) = x
```
- A trapdoor is secure if `F(pk, x)` is a "one-way" function which means it can easily be evaluated but hard to be inverted without `sk`


### Textbook RSA Public Key Encryption
- `G()` output `pk` = (`N`, `e`) and `sk` = (`p`, `q`, `d`)
- Where `N` is a product of two very large primes `p`, `q`
- and `d` and `e` satisfies the condition `d * e mod phiN = 1` where
`phi(N) = N - p - q + 1`
-  `c = E(m, e) = c^e mod N`
-  `m = D(m, d) = c^d mod N`
- This implementation is not semantically secure and many attacks exist because it the encryption is not randomized.
- NEVER USE TEXTBOOK RSA!

### RSA in practice
- Because RSA is slow, RSA in practice is usually to send a short message which is shared secret key. Once both parties have the secret key, they will use symmetric key encryption-decryption systems
- In practice you have the short message, there will be some preprocessing to the message before encrypting it with the RSA encryption to produce a ciphertext.
