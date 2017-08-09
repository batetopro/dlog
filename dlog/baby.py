from utils.utils import modular_exponentiation
from dlog.base import Solver


class BabyGiants(Solver):
    name = "BabyGiants"

    def find(self, g, h, p, q, w=None):
        baby = dict()
        for i in range(w):
            baby[modular_exponentiation(g,i,p)] = i

        step = modular_exponentiation(g, q-w, p)
        for i in range(w):
            giant = (h * modular_exponentiation(step, i, p)) % p
            if giant in baby:
                return (i * w + baby[giant]) % p
