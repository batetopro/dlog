import threading
import random

from utils.utils import modular_exponentiation, modinv
from base import Solver, partition
from utils.marker import Marker


MAX_POINTS = 20000000
HISTORY = 3


class RhoFinder(threading.Thread):
    name = "Rho Finder"

    g = 0
    h = 0
    p = 0
    q = 0

    solved = False
    parent = None
    partitions = 32
    rules = []

    def build_rules(self):
        rules = [(1, 0), (0, 1), (1, 1), (2, 0), (2, 2), (0, 2), (2, 1), (1, 2)]
        for i in range(rules.__len__(), self.partitions):
            rules.append((random.randint(0, self.q - 1), random.randint(0, self.q - 1)))

        result = []
        for rule in rules:
            a = modular_exponentiation(self.g, rule[0], self.p)
            b = modular_exponentiation(self.h, rule[1], self.p)
            r = ((a * b) % self.p, rule[0], rule[1])
            result.append(r)

        self.rules = result

    def shuffle_rules(self):
        for i, rule in enumerate(self.rules):
            swapi = random.randrange(i, len(self.rules))
            self.rules[i], self.rules[swapi] = self.rules[swapi], self.rules[i]

    def info(self):
        print "----------"
        print self.name + " Daemon"
        print "----------"
        print "g = ", self.g
        print "h = ", self.h
        print "p = ", self.p
        print "q = ", self.q
        print "----------"
        print self.rules
        print "----------"

    def solve(self, g, h, p, q, parent):
        self.parent = parent
        self.g = g
        self.h = h
        self.p = p
        self.q = q
        self.build_rules()

    def walk(self, x, a, b):
        index = partition(x, self.partitions)
        rule = self.rules[index]

        if index == 0:
            x = modular_exponentiation(x, 2, self.p)
            a = (2 * a) % self.q
            b = (2 * b) % self.q
        else:
            x = (x * rule[0]) % self.p
            a = (a + rule[1]) % self.q
            b = (b + rule[2]) % self.q

        return x, a, b

    def run(self):
        pass

    def kill(self):
        self.solved = True


class FloydFinder(RhoFinder):
    name = "Floyd Cycle Finder"

    def run(self):
        while not self.solved:
            self.build_rules()
            self.shuffle_rules()

            a1 = random.randint(0, self.q-1)
            b1 = random.randint(0, self.q-1)
            x1 = (modular_exponentiation(self.g, a1, self.p) * modular_exponentiation(self.h, b1, self.p)) % self.p
            x2, a2, b2 = self.walk(x1, a1, b1)

            while x1 != x2 or not self.solved:
                x1, a1, b1 = self.walk(x1, a1, b1)
                x2, a2, b2 = self.walk(x2, a2, b2)
                x2, a2, b2 = self.walk(x2, a2, b2)

                if x1 == x2:
                    if self.solved:
                        break

                    db = (b1 - b2) % self.q
                    if db == 0:
                        break

                    try:
                        result = (modinv(db, self.q) * (a2 - a1)) % self.q
                        self.parent.resolve(result)
                    finally:
                        break


class BrentFinder(RhoFinder):
    name = "Brent Cycle Finder"

    def run(self):
        while not self.solved:
            self.build_rules()
            self.shuffle_rules()

            a1 = random.randint(0, self.q - 1)
            b1 = random.randint(0, self.q - 1)
            x1 = (modular_exponentiation(self.g, a1, self.p) * modular_exponentiation(self.h, b1, self.p)) % self.p
            x2, a2, b2 = x1, a1, b1 #self.walk(x1, a1, b1)

            steps_taken = 0
            step_limit = 2

            while x1 != x2 or not self.solved:
                x2, a2, b2 = self.walk(x2, a2, b2)
                steps_taken += 1

                if x1 == x2:
                    if self.solved:
                        break

                    db = (b1 - b2) % self.q
                    if db == 0:
                        break

                    try:
                        result = (modinv(db, self.q) * (a2 - a1)) % self.q
                        self.parent.resolve(result)
                    finally:
                        break

                if steps_taken == step_limit:
                    steps_taken = 0
                    step_limit *= 2
                    x1, a1, b1 = x2, a2, b2


class DistinguishedPointsFinder(RhoFinder):
    name = "Distinguished Points Finder"
    hits = {}
    marker = None

    def run(self):
        self.marker = Marker(self.g, self.h, self.p, self.q)
        while not self.solved:
            self.build_rules()
            self.shuffle_rules()

            a = random.randint(0, self.q - 1)
            b = random.randint(0, self.q - 1)

            x = (modular_exponentiation(self.g, a, self.p) * modular_exponentiation(self.h, b, self.p)) % self.p

            history = []
            self.hits = {}

            while not self.solved:
                if self.marker.distinguish(x, a, b):
                    if self.solved or history.__len__() > 1:
                        break

                    if x not in self.hits:
                        if self.hits.__len__() < MAX_POINTS:
                            self.hits[x] = (a, b)
                    else:
                        hit = self.hits[x]
                        a2, b2 = hit[0], hit[1]

                        db = (b - b2) % self.q

                        if db == 0:
                            break

                        try:
                            result = (modinv(db, self.q) * (a2 - a)) % self.q
                            self.parent.resolve(result)
                        finally:
                            break

                '''
                cycle = False
                for e in history:
                    if e[0] == a and e[1] == b:
                        cycle = True
                if cycle: break
                '''
                history.append((a, b))

                x, a, b = self.walk(x, a, b)

                if history.__len__() - 1 > HISTORY:
                    history.pop(0)


class RhoSolver(Solver):
    name = "Rho Solver"
    connections = 1
    finder = None
    clients = []
    result = None

    def resolve(self, result):
        self.result = result
        for c in self.clients:
            c.kill()

    def start(self):
        for c in self.clients:
            c.start()

        for c in self.clients:
            c.join()

    def find(self, g, h, p, q, w=None):
        self.clients = []
        self.result = None

        for k in range(self.connections):
            f = self.finder()
            f.solve(g, h, p, q, self)
            self.clients.append(f)

        self.start()

        return self.result


class FloydSolver(RhoSolver):
    name = "Floyd Rho Solver"
    finder = FloydFinder


class BrentSolver(RhoSolver):
    name = "Brent Rho Solver"
    finder = BrentFinder


class DistinguishedPointsSolver(RhoSolver):
    name = "Distinguished Points Solver"
    finder = DistinguishedPointsFinder
