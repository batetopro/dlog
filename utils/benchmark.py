import time


class Benchmark:
    def __init__(self, title):
        self.title = title
        self.t = 0
        self.s = 0
        self.prev=0
        self.data = {}

    def __enter__(self):
        self.t = time.time()
        self.s = time.time()
        print self.title
        print "=" * self.title.__len__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        e = time.time()

        print "=" * self.title.__len__()
        print "Run time: ", e - self.s
        print "=" * self.title.__len__()

        if self.data.__len__() == 0:
            return

        marks = [(k, self.data[k]) for k in self.data]
        marks.sort(key=lambda x: x[0])

        times, values = [x[1] for x in marks], [x[0] for x in marks]

        '''
        import matplotlib.pyplot as plt
        plt.plot(times, values, 'ro')
            # ,times, values, 'k')
        plt.title(self.title)
        plt.ylabel("Value")
        plt.xlabel("Time")
        plt.show()
        '''

    def mark(self, i):
        if i == 0: return
        t = time.time()
        self.data[i] = t - self.t
        self.prev = t - self.t
        print i, t - self.t
        self.t = time.time()
