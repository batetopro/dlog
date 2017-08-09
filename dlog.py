from dlog.test import test_dlog

from dlog.baby import BabyGiants
from dlog.rho import FloydSolver
from dlog.rho import BrentSolver
from dlog.rho import DistinguishedPointsSolver
from dlog.kangaroo import RhoFourKangaroos

T = [
    (11, 3, 29, 28, 17),
    (2, 181, 263, 131, 79),
    (5, 17, 23, 22, 7),
    (3, 181, 263, 131, 12),
    (2, 5, 1019, 1018, 10),
    (89, 799, 809, 101, 50)
]

solvers = [BabyGiants, FloydSolver, BrentSolver, DistinguishedPointsSolver, RhoFourKangaroos]

for s in solvers:
    test_dlog(s, T, 600)
