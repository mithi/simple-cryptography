from gmpy2 import mpz
import gmpy2

# --------------------------------------------------
# CHALLENGE ONE
# --------------------------------------------------
def challenge1(N_string):

    A = None
    N = mpz(N_string)

    # Get the ceiling of sqrt(N)
    A, r = gmpy2.isqrt_rem(N)
    if r > 0:
        A += 1

    A_squared_minus_N = A**2 - N
    x = gmpy2.isqrt(A_squared_minus_N)
    p = A - x
    q = A + x

    N_from_pq = gmpy2.mul(p, q)

    assert N == N_from_pq
    return p.digits(), q.digits()


# --------------------------------------------------
# CHALLENGE TWO
# --------------------------------------------------
def challenge2(N_string):

    A = None
    N = mpz(N_string)
    N_times_24 = 24 * N
    # Get the ceiling of sqrt(N)
    A, r = gmpy2.isqrt_rem(N_times_24)
    if r > 0:
        A += 1

    x, r = gmpy2.isqrt_rem(A**2 - N_times_24)

    assert r == 0

    A_minus_x = A - x
    A_plus_x = A + x

    # Case 1
    p, r = gmpy2.f_divmod(A_minus_x, 6)

    if r == 0:
        q, r = gmpy2.f_divmod(A_plus_x, 4)
        if r == 0:
            assert N == p * q
            return p.digits(), q.digits()

    # Case 2
    p, r = gmp2.f_divmod(A_plus_x, 6)

    if r == 0:
        q, r = gmpy2.f_divmod(A_minus_x, 4)
        if r == 0:
            assert N == p * q
            return p.digits(), q.digits()

    return None, None


# --------------------------------------------------
# CHALLENGE THREE
# --------------------------------------------------
def challenge3(N_string):

    N = mpz(N_string)

    start = gmpy2.isqrt(N) + 1
    end = start + mpz(2)**mpz(20)

    for A in range(start, end):
        A_squared_minus_N = A**2 - N
        x, r = gmpy2.isqrt_rem(A_squared_minus_N)
        if r == 0:
            p = A - x
            q = A + x

            if N == gmpy2.mul(p, q):
                return p.digits(), q.digits()

    return None, None
