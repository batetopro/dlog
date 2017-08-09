from heap import BinaryHeap
from primes import phi, factorize
from utils import modular_exponentiation


def period_greedy(g, p, F=None):
    '''
    Calculate period of a generator g of group modulo p - prime
    Greedy approach from top starting from phi
    '''
    if F is None:
        F = factorize(phi(p))

    K = reversed(sorted([f[0] for f in F]))
    R = {}
    for f in F:
        R[f[0]] = f[1]

    fi = p-1
    while fi > 0:
        found = False
        for f in K:
            t = R[f]

            c = None

            for j in range(1,t+1):
                if modular_exponentiation(g, fi / pow(f, j), p) == 1:
                    c = j

            if c is not None:
                fi /= pow(f, c)
                found = True
                break

        if not found:
            break

    return fi


def period(g, p, F=None):
    '''
    Calculate period of a generator g of group modulo p - prime
    This uses something like Dijkstra for the factorizations
    '''
    q = p - 1
    if F is None:
        F = factorize(q)

    # print F

    start = {}
    for f in F:
        start[f[0]] = 0

    H = BinaryHeap([(1, start)], "period")
    R = {}
    for f in F:
        R[f[0]] = f[1]

    K = sorted([f[0] for f in F])

    while H.n > 0:
        h = H.head()

        #print h[0]
        if modular_exponentiation(g, h[0], p) == 1:
            return h[0]

        ctr = 0
        for j, k in enumerate(K):
            if h[1][k] == R[k]:
                ctr = j + 1
                break

        for k in range(ctr, K.__len__()):
            f = K[k]
            child = {}
            val = h[0]
            for k in h[1]:
                child[k] = h[1][k]
                if f == k:
                    child[f] += 1
                    if child[f] > R[f]:
                        child = None
                        break
                    val *= f

            if not child: continue

            queued = False
            for k, v in enumerate(H.data):
                if k == 0: continue
                if v[0] == val:
                    queued = True

            if not queued:
                H.insert((val, child))


def easy_period(g, p):
    for k in range(1,p+1):
        if pow(g,k,p) == 1:
            return k
    return -1