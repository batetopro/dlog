class Marker:
    mask = 0

    def __init__(self, g, h, p, q):
        self.g = g
        self.h = h
        self.p = p
        self.q = q

    '''
    m = int(pow(2, int(p.bit_length() - math.floor(math.log(MAX_POINTS / 3, 2)) + 1)))
    self.mask = m
    if self.mask < 0:
        self.mask = 0


    if self.mask > 0 and not (x & self.mask) == self.mask:
        return False
    '''

    def distinguish(self, x, a, b):
        return True

