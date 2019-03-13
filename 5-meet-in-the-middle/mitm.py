from gmpy2 import mpz
from gmpy2 import t_mod, invert, powmod, add, mul, is_prime
import textwrap

p_string = '13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171'
g_string = '11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568'
h_string = '3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333'


def pretty_print(x):
    x = textwrap.wrap(x, width=32)
    for i in x:
        print(" ",i)
    print()


def build_table(h, g, p, B):
    table, z = {}, h
    g_inverse = invert(g, p)
    table[h] = 0
    for x1 in range(1, B):
        z = t_mod(mul(z, g_inverse), p)
        table[z] = x1
    return table


def lookup(table, g, p, B):
    gB, z = powmod(g, B, p), 1
    for x0 in range(B):
        if z in table:
            x1 = table[z]
            return x0, x1
        z = t_mod(mul(z, gB), p)
    return None, None


def find_x(h, g, p, B):
    table = build_table(h, g, p, B)
    x0, x1 = lookup(table, g, p, B)
    # assert x0 != None and x1 != None
    Bx0 = mul(x0, B)
    x = add(Bx0, x1)
    # print(x0, x1)
    return x


def run(p_string, g_string, h_string):

    p = mpz(p_string)
    g = mpz(g_string)
    h = mpz(h_string)
    B = mpz(2) ** mpz(20)

    assert is_prime(p)
    assert g < p
    assert h < p

    x = find_x(h, g, p, B)

    assert h == powmod(g, x, p)
    return x


if __name__=="__main__":

    print()
    print("Given p, g, and h, such that p is prime, and both g and h is less than p")
    print("Find x such that g^x mod p = h", end="")
    print("where g^x is g raised to the power of x \n")

    print()
    print("p = ")
    pretty_print(p_string)

    print("g = ")
    pretty_print(g_string)

    print("h = ")
    pretty_print(h_string)

    print("finding x...")

    x = run(p_string, g_string, h_string)

    print("x = ", x)
    print()
