import random
from utils.period import period


def partition(x, partitions):
    # Binary Mask - partitions power of 2
    return x & (partitions-1)


class Solver:
    name = "Abstract"

    result = None

    def __init__(self, seed=42):
        self.seed = long(seed)
        random.seed(seed)

    def find(self, g, h, p, q, w=None):
        return 0

    def solve(self, g, h, p, q, w=None):
        g = g % p
        h = h % p
        if g == 1 or h == 1:
            return 0
        if g == h:
            return 1
        if q == 2:
            return h & 1

        if w is None:
            w = int(float(q) ** 0.5) + 1

        return self.find(g, h, p, q, w)

    def debug(self, g, h, p, q=None, w=None):
        print "-----------"
        print self.name
        print "-----------"
        print "g = ", g
        print "h = ", h
        print "p = ", p
        if q is None:
            q = period(g, p)
        print "q = ", q
        print "w = ", w
        print "-----------"
        dlog = self.solve(g, h, p, q, w)
        print "DLOG ", dlog
        print "-----------"
        return dlog

