from utils.benchmark import Benchmark
from utils.period import period
from utils.primes import factorize
from utils.utils import modular_exponentiation, modinv
from utils.crt import easy_crt


class PohligHellman:
    def __init__(self, dlog):
        self.dlog = dlog
        self.verbose = False
        self.bench = None
        self.queries = 0
        self.g = 0

    def prepare(self, g, p):
        q = period(g, p)
        F = factorize(q)
        return q, F

    def debug(self, g, h, p, q, F):
        self.verbose = True

        with Benchmark("Pohlig Hellman") as bench:
            self.bench = bench
            print "g = ", g
            print "h = ", h
            print "p = ", p
            print "q = ", q
            print "F = ", F
            print "-----------"
            result = self.solve(g, h, p, q, F)
            print "PH DLOG = ", result
            print "----------"

        self.verbose = False
        return result

    def find(self, g, h, p, q):
        if self.verbose:
            self.queries += 1
            L = self.dlog.debug(g, h, p, q)
            self.bench.mark(self.queries)
            with open(str(self.g), "a") as f:
                f.write(str(self.queries) + " " + str(self.bench.prev) + "\n")
            return L

        return self.dlog.solve(g, h, p, q)

    def solve(self, g, h, p, q, F):
        self.g = g
        F.sort(key=lambda x: x[0])

        # we have interest in the Group's order
        q = p - 1

        parts = []
        for f in F:
            A = modular_exponentiation(g, q / f[0], p)
            B = modular_exponentiation(h, q / f[0], p)
            levels = [self.find(A, B, p, f[0])]

            gamma = 1
            for j in range(1,f[1]):
                gamma = (gamma * modular_exponentiation(g, levels[j-1] * pow(f[0], j - 1), p)) % p
                P = pow(f[0], j+1)
                B = modular_exponentiation((h * modinv(gamma, p)) % p, q / P, p)
                levels.append(self.find(A, B, p, f[0]))

            flow = sum([l * pow(f[0],k) for k, l in enumerate(levels)])
            parts.append((flow, pow(f[0], f[1])))

        if self.verbose:
            print "CRT ON:"
            print "-----------"
            print parts
            print "-----------"

        return easy_crt(parts)
