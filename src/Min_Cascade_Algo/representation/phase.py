from representation import graph
from algos import cascade_calculation
import inputs
import matplotlib.pyplot as plt
import numpy as np


class Phase:

    def __init__(self, k, l):
        self.k = k
        self.l = l
        self.cascade_costs = []
        self.g = graph.Graph(self.k, self.l)
        self.history = [self.g.to_string()]


    def start_phase(self, choose_mode):

        can_phase_continue = True
        while can_phase_continue:
            self.g.comps_to_merge = self.g.next_request(choose_mode)
            is_cascade_possible, new_graph, cascade_cost = cascade_calculation.Calculation.possible_cascade(self.g)
            can_phase_continue = is_cascade_possible == 1
            if can_phase_continue:
                self.g.actualisation(new_graph)
                self.cascade_costs.append(cascade_cost)
                self.history.append(self.g.to_string())

        # for s in self.history:
        #     print(s)
        # print("phase stopped after ", len(self.cascade_costs), " cascades.")

    def show_costs(self):
        ar = np.asarray(self.cascade_costs)
        plt.plot(ar)
        plt.title("cascade costs within a phase, with: k = " + str(self.k) + ",  l = " + str(self.l) + "\n number of cascades = " + str(len(ar)))
        plt.show()






