class BinaryHeap:
    def __init__(self, data, name="Heap"):
        self.n = data.__len__()
        self.data = [name] + data[:]
        i = self.n // 2
        while i > 0:
            self.sift_down(i)
            i -= 1

    def insert(self, element):
        # here we have a lock :)
        self.n += 1
        self.data.append(element)
        self.sift_up(self.n)
        return self.data[1]

    def head(self, delete=True):
        ret = self.data[1]
        if delete:
            self.delete_min()
        return ret

    def delete_min(self):
        val = self.data[1]
        self.data[1] = self.data[self.n]
        self.n -= 1
        self.data.pop()
        self.sift_down(1)
        return val

    def sift_up(self, i):
        if i == 1: return
        i2 = i / 2
        if self.data[i2][0] <= self.data[i][0]: return
        self.data[i2], self.data[i] = self.data[i], self.data[i2]
        self.sift_up(i2)

    def sift_down(self, i):
        while i * 2 <= self.n:
            mc = self.min_child(i)
            if self.data[i][0] >= self.data[mc][0]:
                self.data[mc], self.data[i] = self.data[i], self.data[mc]
            i = mc

    def min_child(self, i=0):
        if i == 0:
            i = self.n

        if i * 2 + 1 > self.n:
            return i * 2
        else:
            if self.data[i * 2] < self.data[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

if __name__ == "__main__":
    import random
    random.seed()

    N = 10
    data = [(random.randint(0, 10), x) for x in range(N)]

    h = BinaryHeap(data)
    h.insert((5, "Heap"))
    print h.n, h.data[0]
    print h.data

    while h.n > 1:
        print h.head(True)