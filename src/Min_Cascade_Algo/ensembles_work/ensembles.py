import random as rd
from representation import graph, phase


class Ensembles:

    def __init__(self, k, l, ending_percentage_to_retain, choose_mod = "random"):
        self.k = k
        self.l = l
        self.phase = phase.Phase(self.k, self.l)
        self.list_ensembles = self.phase.get_some_state(choose_mod, ending_percentage_to_retain)

