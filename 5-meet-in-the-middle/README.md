# Meet in the Middle Attack
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
Find x such that g^x mod p = h mod p (g^x is g raised to the power of x)


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

# Idea
- let `B = 2^20` then `B^2 = 2^40`
- then `x= xo * B + x1` where `xo` and `x1` are in `{0, 1, ..., B-1}`
- Then smallest x is `x = 0 * B + O = 0`
- Largest x is `x = B * (B-1) + B - 1 = B^2 - B + B -1 = B^2 - 1 = 2^40 - 1`
- Then:
```
h = g^x
h = g^(xo * B + x1)
h = g^(xo * B) * g^(x1)
h / g^(x1) = g^(xo*B)
h * (g^(-x1) mod p) = (g^B mod p)^xo mod p
h * (g^-1 mod p)^x1 mod p = (g^B mod p)^xo mod p
```
- Find `xo` and `x1` given `g`, `h`, `B`

# Strategy
- Build a hash table key: `h / g^(x1)`, with value `x1` for `x1` in `{ 0, 1, 2, .., 2^20 - 1}`
- For each value `x0` in `{0, 1, 2, ... 20^20 -1}` check if `(g^B)^(x0) mod P` is in hashtable. If it is then you've found `x0` and `x1`
- Return `x = xo * B + x1`

### Modulo Division
```
 (x mod p) / ( y mod p)  = ((x mod p) * (y_inverse mod p)) mod p

```



# Notes
- Work is `2^20` multiplications and `2^20` lookups in the worst case
- If we brute forced it, we would do `2^40` multiplications
- So the work is squareroot of brute force

## Important Optimization
- Careful not to do redundant exponentiations.
``` python

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

### Definition of inverse
```
 Definition of modular inverse in Zp
 y_inverse * y mod P = 1
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

# Test Numbers

```
p = 134078079299425970995740249982058461274793658205923933\
    77723561443721764030073546976801874298166903427690031\
    858186486050853753882811946569946433649006084171

g = 11717829880366207009516117596335367088558084999998952205\
    59997945906392949973658374667057217647146031292859482967\
    5428279466566527115212748467589894601965568

h = 323947510405045044356526437872806578864909752095244\
    952783479245297198197614329255807385693795855318053\
    2878928001494706097394108577585732452307673444020333
```

