from utils.benchmark import Benchmark
from utils.utils import modular_exponentiation
from utils.period import period
from utils.primes import primes, factorize

from dlog.ph import PohligHellman

from dlog.baby import BabyGiants
from dlog.rho import FloydSolver
from dlog.rho import BrentSolver
from dlog.rho import DistinguishedPointsSolver
from dlog.kangaroo import RhoFourKangaroos

from dlog.test import test_ph

T = [
    #(3, 11, 17, 7), # https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%9F%D0%BE%D0%BB%D0%B8%D0%B3%D0%B0_%E2%80%94_%D0%A5%D0%B5%D0%BB%D0%BB%D0%BC%D0%B0%D0%BD%D0%B0
    #(71, 210, 251, 197), # http://cacr.uwaterloo.ca/hac/about/chap3.pdf
    #(7, 166, 433, 47) # http://www4.ncsu.edu/~clvinzan/437/discretelog.pdf
]

solvers = [BrentSolver, BabyGiants, FloydSolver, DistinguishedPointsSolver, RhoFourKangaroos]

for s in solvers:
    test_ph(s, T, 600)
