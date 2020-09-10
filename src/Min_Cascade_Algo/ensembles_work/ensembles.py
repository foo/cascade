import random as rd
from representation import graph, phase
import itertools


class Ensembles:

    def __init__(self, k, l, ending_percentage_to_retain, choose_mod="random"):
        self.k = k
        self.l = l
        self.phase = phase.RandomPhase(self.k, self.l)
        self.list_ensembles = self.phase.get_some_state(choose_mod, ending_percentage_to_retain)
        self.prime_partitions = []

    def find_prime_partition_number(self, c1, c2):

        if sum(c1) != sum(c2):
            print("clusters have different sizes    c1: ", sum(c1), "  c2: ", sum(c2))
            return

        if len(c2) == 0:
            return 1
        partition_number = 0
        perm = [0]
        tmp_c1 = []
        i_c1 = 0
        length_c1 = len(c1)
        length_c2 = len(c2)
        c2_counter = c2[perm[0]]

        continue_search = True
        while continue_search:
            #print(partition_number)
            if sum(tmp_c1) < c2_counter:
                tmp_c1.append(c1[i_c1])
                i_c1 += 1
                #print("c1 ", i_c1)

            elif sum(tmp_c1) > c2_counter:
                #print(perm)
                if perm[-1] == length_c2-1: #To finish
                    return
                else:
                    c2_counter -= c2[perm[-1]]
                    perm[-1] += 1
                    c2_counter += c2[perm[-1]]

            elif sum(tmp_c1) == c2_counter:
                partition_number += self.find_prime_partition_number(
                    c1[i_c1:], [c2[item] for item in [index for index in range(length_c2) if index not in perm]])
                if perm[-1] >= length_c2 - 1:
                    c2_counter -= c2[perm[-1]]
                    del perm[-1]
                    tmp_c1.clear()
                    i_c1 = 0
                    if len(perm) == 0:
                        return partition_number
                    else:
                        c2_counter -= c2[perm[-1]]
                        perm[-1] = perm[-1] + 1
                        c2_counter += c2[perm[-1]]
                else:
                    c2_counter -= c2[perm[-1]]
                    perm[-1] = perm[-1] + 1
                    c2_counter += c2[perm[-1]]

        return partition_number
