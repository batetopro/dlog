PRIMES = []
PRIMES_MAX = 1
PRIMES_LIMIT = 10 ** 7
        
def primes_init(n):
    global PRIMES_MAX, PRIMES
    if n > PRIMES_MAX:
        if PRIMES.__len__() > PRIMES_LIMIT:
            return

        for p in gen_primes():
            if p <= PRIMES_MAX:
                continue
            if n <= p:
                break
            if PRIMES.__len__() > PRIMES_LIMIT:
                break
            PRIMES.append(p)

        PRIMES_MAX = PRIMES[-1]


def factorize(n):
    # print n
    primes_init(int(n**0.5) + 5)
    meets = []
    for p in PRIMES:
        while n % p == 0:
            meets.append(p)
            n /= p
        if p > n: break
        if n == 0: break

    flow = False
    if n > 1:
        flow = True
        meets.append(n)

    grouped = {}
    for meet in meets:
        if meet not in grouped:
            grouped[meet] = 0
        grouped[meet] += 1

    return [(k,grouped[k]) for k in grouped]


def phi(n, fact=None):
    if fact is None:
        fact = factorize(n)

    up = 1
    down = 1
    for f in fact:
        up *= f[0] - 1
        down *= f[0]

    return (up * n) / down




def is_prime(n, F=None):
    if F is None:
        F = factorize(n)
    return (F.__len__() == 1) and (F[0][1] == 1)


def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in xrange(3, int(n ** 0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = [False] * ((n - i * i - 1) / (2 * i) + 1)
    return [2] + [i for i in xrange(3, n, 2) if sieve[i]]


def gen_primes():
    D = {}
    q = 2
    while True:
        if q not in D:
            yield q
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            # no longer need D[q], free memory
            del D[q]
        q += 1
