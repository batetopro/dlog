import utils.benchmark
from utils.benchmark import Benchmark
from utils.primes import is_prime
from utils.period import easy_period, period, period_greedy

factors = [(2, 5), (3, 1), (5, 2), (784004352084511, 1), (1027227490406197, 1), (654902746474663, 1),
           (1036939576553807, 1), (596188499292077, 1),
           (892468311744169, 1), (659631355866083, 1), (957233047034401, 1), (724125034830403, 1),
           (932208036802673, 1), (884513720203747, 1), (669103258616449, 1),
           (706649413290787, 1), (778270471074587, 1), (1039970558488139, 1), (582911323916071, 1),
           (688320490973009, 1), (1084631666707019, 1), (650445618231881, 1),
           (567579678437593, 1), (791412759766441, 1)]
g = 7

'''
with Benchmark("Periods") as bench:
    for f in factors:
        print f[0], period_greedy(g, f[0])
        bench.mark(f[0])
        print f[0], period(g, f[0])
        bench.mark(f[0])

'''
# Proof of correctness of the period finding
with Benchmark("Period checking") as bench:
    for p in range(2,100001):
        if p % 50 == 0:
            bench.mark(p)

        if not is_prime(p):
            continue

        for g in range(2, p):
            p1 = easy_period(g, p)
            p2 = period(g, p)
            p3 = period_greedy(g, p)

            if p1 != p2:
               print "NO: ", g, p, p1, p2

            if p1 != p3:
                print "NO: ", g, p, p1, p3