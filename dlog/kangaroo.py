import threading
import random

from utils.rw import RWLock
from utils.utils import modular_exponentiation, modinv
from dlog.base import Solver, partition
from utils.marker import Marker

MAX_POINTS = 20000000
HISTORY = 3


class Kangaroo(threading.Thread):
    x = 0
    a = 0
    g = 0
    h = 0
    p = 0
    q = 0
    w = 0
    m = 0
    s = 0
    single = False
    history = set()

    name = "Kangaroo"

    rules = []
    partitions = 0
    parent = None
    marker = None

    solved = False

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

    def build_rules(self):
        rules = [1]
        ns = 1.0
        while sum(rules) / ns < self.m:
            n = int(pow(2, ns))
            rules.append(n)
            ns += 1.0

        result = []
        for rule in rules:
            x = modular_exponentiation(self.g, rule, self.p)
            r = (x, rule)
            result.append(r)

        self.rules = result
        self.partitions = result.__len__()

    def shuffle_rules(self):
        for i, rule in enumerate(self.rules):
            swapi = random.randrange(i, len(self.rules))
            self.rules[i], self.rules[swapi] = self.rules[swapi], self.rules[i]

    def solve(self, x, a, g, h, p, q, w, parent):
        self.s = x
        self.x = x
        self.a = a
        self.p = p
        self.q = q
        self.g = g
        self.h = h
        self.w = w
        self.rules = []
        self.parent = parent
        self.marker = Marker(g, h, p, q)

        self.m = int(0.365 * ((2 * w) ** 0.5)) + 1
        self.build_rules()

    def report(self):
        self.wild()
        self.tame()

    def tame(self):
        if not self.marker.distinguish(self.x, self.a, 0):
            return

        try:
            if self.parent.rw is not None:
                self.parent.rw.writer_acquire()

            if self.x in self.parent.hits:
                self.jump()
                return

            if self.parent.hits.__len__() > MAX_POINTS:
                self.kill()
                return

            self.parent.hits[self.x] = self.a

            if self.parent.hits.__len__() % 100000 == 0:
                with open("kangaroo", "a") as f:
                    f.write(str(self.parent.hits.__len__()) + "\n")

        finally:
            if self.parent.rw is not None:
                self.parent.rw.writer_release()

    def wild(self):
        if not self.marker.distinguish(self.x, self.a, 0):
            return

        try:
            if self.parent.rw is not None:
                self.parent.rw.reader_acquire()

            if self.single:
                if self.x in self.history:
                    self.kill()

                self.history.add(self.x)

            if self.x in self.parent.hits:
                a = self.parent.hits[self.x]
                result = (a-self.a) % self.q

                if modular_exponentiation(self.g, result, self.p) != self.h:
                    result = (-a+self.a) % self.q

                if modular_exponentiation(self.g, result, self.p) != self.h:
                    return

                self.parent.resolve(result)
        finally:
            if self.parent.rw is not None:
                self.parent.rw.reader_release()

    def run(self):
        self.shuffle_rules()
        while not self.solved:
            self.walk()

    def kill(self):
        self.solved = True

    def jump(self):
        if self.single:
            self.kill()
        else:
            self.shuffle_rules()
            u = random.randint(1, 2 * self.m)
            self.a = self.a + u
            self.x = (self.x * modular_exponentiation(self.g, u, self.p)) % self.p

    def walk(self):
        part = partition(self.x, self.partitions)
        rule = self.rules[part]
        self.x = (self.x * rule[0]) % self.p
        self.a = (self.a + rule[1]) % self.q
        self.report()


class RhoFourKangaroos(Solver):
    name = "Four Kangaroos Solver"
    connections = 4

    hits = dict()
    rw = None
    clients = []

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

        if w is None:
            w = q

        self.clients = []
        self.rw = RWLock()

        u = int(w / 2)

        t1 = Kangaroo()
        t1.name = "Tame 1"
        t1.solve(modular_exponentiation(g, u, p), u, g, h, p, q, w, self)
        self.clients.append(t1)

        t2 = Kangaroo()
        t2.name = "Tame 2"
        t2.solve(modular_exponentiation(g, u+1, p), u+1, g, h, p, q, w, self)
        self.clients.append(t2)

        w1 = Kangaroo()
        w1.solve(h, 0, g, h, p, q, w, self)
        w1.name = "Wild 1"
        self.clients.append(w1)

        w2 = Kangaroo()
        w2.name = "Wild 2"
        w2.solve(modinv(h, p), 0, g, h, p, q, w, self)
        self.clients.append(w2)

        self.start()

        return self.result