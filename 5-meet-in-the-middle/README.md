# About
> The meet-in-the-middle attack (MITM) is a generic space–time tradeoff cryptographic attack against encryption schemes which rely on performing multiple encryption operations in sequence. The MITM attack is the primary reason why Double DES is not used and why a Triple DES key (168-bit) can be bruteforced by an attacker with 2^56 space and 2^112 operations

- This script illustrates how we can use MITM to solve a specific discrete log problem
square-root of the operations of the simplest brute force attack.

# Task
- Given prime `p`
- then `Zp* = {1, 2, 3, ..., p-1}`
- let `g` and `h` be elements in `Zp*` such that
- such that `h mod p = g^x mod p` where ` 0 < x < 2^40`
- find `x` given `h`, `g`, and `p`

# Dependency
- [gmpy2](https://gmpy2.readthedocs.io/en/latest/mpz.html)

## Sample Usage

```
$ python mitm.py

Given p, g, and h, such that p is prime, and both g and h is less than p
Find x such that g^x mod p = h (g^x is g raised to the power of x)


p =
  13407807929942597099574024998205
  84612747936582059239337772356144
  37217640300735469768018742981669
  03427690031858186486050853753882
  811946569946433649006084171

g =
  11717829880366207009516117596335
  36708855808499999895220559997945
  90639294997365837466705721764714
  60312928594829675428279466566527
  115212748467589894601965568

h =
  32394751040504504435652643787280
  65788649097520952449527834792452
  97198197614329255807385693795855
  31805328789280014947060973941085
  77585732452307673444020333

finding x...
x =  375374217830
```

# The Attack

## Core Idea
- let `B = 2^20` then `B^2 = 2^40`
- then `x= xo * B + x1` where `xo` and `x1` are in `{0, 1, ..., B-1}`
- Then smallest `x` is `x = 0 * B + O = 0`
- and the largest `x` is `x = B * (B-1) + B - 1 = B^2 - B + B -1 = B^2 - 1 = 2^40 - 1`
- Then:
```
h = g^x
h = g^(xo * B + x1)
h = g^(xo * B) * g^(x1)
h / g^(x1) = g^(xo*B)
```
- Find `xo` and `x1` given `g`, `h`, `B`

## Strategy
- Build a hash table key: `h / g^(x1)`, with value `x1` for `x1` in `{ 0, 1, 2, .., 2^20 - 1}`
- For each value `x0` in `{0, 1, 2, ... 20^20 -1}` check if `(g^B)^(x0) mod P` is in hash table. If it is then you've found `x0` and `x1`
- Return `x = xo * B + x1`

### Observations
- Work is `2^20` multiplications and `2^20` lookups in the worst case
- If we attack it by bruteforce , we would do `2^40` multiplications
- So the work is squareroot of brute force

# Notes

### Modulo Division
```
 (x mod p) / ( y mod p)  = ((x mod p) * (y_inverse mod p)) mod p

```

## Optimization
- Be smart. Do not do redundant exponentiations.
```python

# Efficient
gB = g**B % p
z = h
print(x, z)
for x in range(1, n):
    z = z*gB % p
    print(x, z)

# Inefficient
for x in range(n):
    y = g**(B*x)
    z = h*y % p
    print(x, z)
```

### Modular Inverse
```

 y_inverse * y mod p = 1
```

### Inverse of  `x` in `Zp*`
```
Given p is prime,
then for every element x in set Zp* = {1, ..., p - 1}
the element x is invertible (there exist an x_inverse such that:
x_inverse * x mod p = 1

The following is true (according to Fermat's 1640)

x^(p - 1) mod  = 1
x ^ (p - 2) * x mod p = 1
x_inverse = x^(p-2)

 ```

