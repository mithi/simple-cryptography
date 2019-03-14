import textwrap
from gmpy2 import mpz
import gmpy2
from publickeysystem import encrypt_pipeline, decrypt_pipeline, compute_d, phi

c = "22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540"
e = '65537'
N = "179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581"


def find_pq(N_string):
    # find p an and q such that N = p * q
    # and |p - q| < 2 * fourthroot_of(N)
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


def print_digit(x):
    x = textwrap.wrap(x, width=64)
    for i in x:
        print("  ", i)


def run():

    print("Given:")
    print("\nciphertext = ")
    print_digit(c)

    print("\nN = ")
    print_digit(N)

    print("\ne = ")
    print_digit(N)

    print("\nAnd that we know that |p - q| < 2 * fourthroot_of(N); therefore:")

    p, q = find_pq(N)

    print("\np = ")
    print_digit(p)

    print("\nq = ")
    print_digit(q)

    print("\nAnd which we can use to compute phi(N) and consequently the d.")

    print("\nphi(N) = ")
    print_digit(phi(N, p, q))

    d = compute_d(e, N, p, q)

    print("\nd = ")
    print_digit(d)

    print("\nFinally, the resulting plaintext:")
    print()
    m = decrypt_pipeline(c, d, N)
    print(m)
    print()


if __name__ == "__main__":
    run()

