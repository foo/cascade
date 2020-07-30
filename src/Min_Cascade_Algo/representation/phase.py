from representation import graph
from algos import cascade_calculation
import inputs
import matplotlib.pyplot as plt
import numpy as np
import random as rd


class Phase:

    def __init__(self, k, l):
        self.k = k
        self.l = l
        self.cascade_costs = []
        self.g = graph.Graph(self.k, self.l)
        self.history = []

        # ----------------------for experiments ---------------
        self.cascade_number = 0
        self.moves = []
        for i in range(k * l):
            self.moves.append([])
        self.sizes = []
        for i in range(k * l):
            self.sizes.append([])
        self.max_ratio = 0

    def start_phase(self, choose_mode):

        can_phase_continue = True
        while can_phase_continue:
            self.g.comps_to_merge = self.g.next_request(choose_mode)
            self.history.append(self.g.to_string(self.g.comps_to_merge))
            is_cascade_possible, new_graph = cascade_calculation.Calculation.possible_cascade(self.g)
            can_phase_continue = is_cascade_possible == 1
            if can_phase_continue:
                self.g.apply_cascade(new_graph)
                self.cascade_number += 1
                self.cascade_costs.append(self.g.get_last_cascade_cost())


                # ids = self.g.get_id_list()
                # # for i in range(len(self.moves)):
                # #     self.moves[i].append(0)
                # #     self.sizes[i].append(0)
                # for id in ids:
                #     for i in id:
                #         tmp = self.g.get_comp(i)
                #         if tmp.moves > self.l * np.log2(self.k) * tmp.size:
                #             print("false!! step nb ", self.cascade_number, "      comp size: ", tmp.size)
                #             for h in self.history:
                #                 print(h)
                # self.moves[i][-1] += tmp.moves
                # self.sizes[i][-1] += tmp.size

        # for s in self.history:
        #     print(s)
        # print("phase stopped after ", len(self.cascade_costs), " cascades.")

    # -------------------------------- for Prime Ensembles Tests ------------------------------------

    def get_some_state(self, choose_mode, ending_percentage_to_retain):
        list_historic = []
        can_phase_continue = True
        while can_phase_continue:
            self.g.comps_to_merge = self.g.next_request(choose_mode)
            is_cascade_possible, new_graph = cascade_calculation.Calculation.possible_cascade(self.g)
            can_phase_continue = is_cascade_possible == 1
            if can_phase_continue:
                list_historic.append(self.g.get_sizes_per_clusters())
                self.g.apply_cascade(new_graph)
                self.cascade_number += 1
                # self.history.append(self.g.to_string())
                self.cascade_costs.append(self.g.get_last_cascade_cost())
        nb_elements_to_retain = int(len(list_historic) * ending_percentage_to_retain / 100)
        return rd.choice(list_historic[(len(list_historic) - nb_elements_to_retain):])
