import random as rd


class Inputs:
    alpha = 0
    k = 0
    l = 0
    sequence = []
    # the next request index that will be received
    t = 0


    @classmethod
    def init(cls, k, l, alpha):
        cls.k = k
        cls.l = l
        cls.alpha = alpha
        cls.t = 0

    # create a length-size random input sequence
    @classmethod
    def create_sequence(cls, length):
        if cls.k * cls.l <= 1:
            print("too few vertices")
            return

        for i in range(length):
            tmp1 = rd.randint(0, cls.k * cls.l)
            tmp2 = rd.randint(0, cls.k * cls.l)
            while tmp2 ==tmp1:
                tmp2 = rd.randint(0, cls.k * cls.l)
            cls.sequence.append([tmp1, tmp2])

    @classmethod
    def next_request(cls):
        if cls.t >= len(cls.sequence):
            return []

        cls.t += 1
        return cls.sequence[cls.t-1]

