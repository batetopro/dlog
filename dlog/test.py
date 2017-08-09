from utils.benchmark import Benchmark
from utils.utils import modular_exponentiation
from utils.period import period
from utils.primes import primes, factorize
from dlog.ph import PohligHellman


def test_ph(solver, tests, N):
    solver = solver()
    ph = PohligHellman(solver)

    for test in tests:
        g, h, p, a = test
        q, F = ph.prepare(g, p)
        x = ph.debug(g, h, p, q, F)
        if x != a:
            print "FAILED", a
        else:
            print "OK"

    factors = {}
    for n in range(1, N):
        factors[n] = factorize(n)

    with Benchmark(solver.name + " Test") as bench:
        hits = 0
        ctr = 0

        for p in primes(N):
            F = factors[p - 1]

            for g in range(1, p):
                q = period(g, p, F)
                # print "EPOCH (g, p, q) = ", (g, p, q), F

                for h in range(p):
                    m = modular_exponentiation(g, h, p)
                    x = solver.solve(g, m, p, q)
                    check = modular_exponentiation(g, x, p)

                    ctr += 1
                    if m == check:
                        hits += 1
                    elif x is not None:
                        print "ERROR: (p, g, h) = M, Y", p, g, m, h, x

                    if m == 1 and h > 0:
                        break

            bench.mark(p)

        print ctr, hits


def test_dlog(solver, tests, N):
    solver = solver()

    for test in tests:
        g, h, p, q, a = test
        x = solver.debug(g, h, p, q)
        if x != a:
            print "FAILED", a
        else:
            print "OK"

    factors = {}
    for n in range(1, N):
        factors[n] = factorize(n)

    with Benchmark(solver.name + " Test") as bench:
        hits = 0
        ctr = 0

        for p in primes(N):
            # F = factors[p - 1]

            for g in range(1, p):
                q = period(g, p)

                # print "EPOCH (g, p, q) = ", (g, p, q), F

                for h in range(p):
                    m = modular_exponentiation(g, h, p)
                    x = solver.solve(g, m, p, q)
                    check = modular_exponentiation(g, x, p)

                    ctr += 1
                    if m == check:
                        hits += 1
                    elif x is not None:
                        print "ERROR: (p, g, h) = M, Y", p, g, m, h, x

                    if m == 1 and h > 0:
                        break

            bench.mark(p)

        print ctr, hits