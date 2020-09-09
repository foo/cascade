from representation import graph
from algos import cascade_calculation
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import copy
from itertools import groupby

class Phase:

    def __init__(self, k, l, choose_mode="classic"):
        self.k = k
        self.l = l
        self.cascade_costs = []

        # maciek: I don't use g in max_phase (local variable in recursive function instead)
        self.g = graph.Graph(self.k, self.l)
        self.history = ""
        self.choose_mode = choose_mode
        self.moves = []

        # ----------------------for experiments ---------------
        self.cascade_number = 0
        for i in range(k * l):
            self.moves.append([])
        self.sizes = []
        for i in range(k * l):
            self.sizes.append([])
        self.max_ratio = 0
    
    def max_phase(self, k, l):
        configuration = graph.Graph(k, l)

        configuration.comps_to_merge = self.first_request(configuration)
        max_cost = self.max_phase_aux(configuration)
        print("max_cost", max_cost)
        return max_cost
    
    # the first request is between arbitrary nodes of different clusters
    def first_request(self, configuration):
        node_list = configuration.get_id_list()
        nodes_cluster1 = node_list[0]
        nodes_cluster2 = node_list[1]
        return [nodes_cluster1[0], nodes_cluster2[0]]

    # returns a list of all component id pairs (only pairs that matters)
    def all_requests(self, configuration):
        requests = []
        node_list = configuration.get_id_list()
       
        # todo: all pairs of clusters should be unique (now we consider each pair twice)
        for idc1, cluster1 in configuration.cluster_list:
            for idc2, cluster2 in configuration.cluster_list:
                if not cluster1 == cluster2:
                    comps1 = cluster1.comp_list
                    comps2 = cluster2.comp_list

                    comps1unique = comps1
                    comps2unique = comps2

                    for i in comps1unique:
                        for j in comps2unique:
                            requests.append([i.id, j.id])

        print("requests ", requests)
        return requests


    def max_phase_aux(self, configuration):

        print("max_phase")
        # apply the current request

        print("current request")
        print(configuration.comps_to_merge)
        print("ids")
        print(configuration.to_string_ids())
 
        is_cascade_possible, graph_changes = cascade_calculation.Calculation.possible_cascade(configuration)

        print("can continue?")
        can_phase_continue = is_cascade_possible == 1
        if not can_phase_continue:
            return 0

        configuration.apply_cascade(graph_changes)

 
        current_request_cost = configuration.get_last_cascade_cost()
        self.cascade_number += 1
        self.cascade_costs.append(current_request_cost)


        # add recursive cost of maximum of next costs

        requests = self.all_requests(configuration)
        assert(not requests == [])

        print("requests r")
        print(requests)

        max_remaining_cost = 0
        max_cost_branch = None

        # comment about branches
        for r in requests:
            print("consider request ", r)
            configuration_branch = copy.deepcopy(configuration)
            configuration_branch.comps_to_merge = r

            branch_cost = self.max_phase_aux(configuration_branch)
            print("current_cost ", current_request_cost)
            print("branch_cost ", branch_cost)

            if max_remaining_cost <= branch_cost:
                max_remaining_cost = branch_cost
                max_cost_branch = configuration_branch
        
        # glue the history
        print("max rem", max_remaining_cost)

        assert(not (max_cost_branch == None))
        return max_remaining_cost + current_request_cost

    def start_phase(self):

        self.g.comps_to_merge = self.g.next_request(self.choose_mode)
        self.history += self.g.to_string(self.g.comps_to_merge) + '\n'

        can_phase_continue = True
        while can_phase_continue:

            is_cascade_possible, graph_changes = cascade_calculation.Calculation.possible_cascade(self.g)
            can_phase_continue = is_cascade_possible == 1
            if can_phase_continue:
                self.g.apply_cascade(graph_changes)

                self.cascade_number += 1
                self.cascade_costs.append(self.g.get_last_cascade_cost())

                self.g.comps_to_merge = self.g.next_request(self.choose_mode)
                self.history += "cascade cost: " + str(self.g.get_last_cascade_cost()) + '\n\n' + str(self.g.to_string(self.g.comps_to_merge)) + '\n'

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
