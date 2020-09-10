from representation import graph
from algos import cascade_calculation
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import copy
from itertools import groupby

class MaxPhase:

    def __init__(self, k, l, choose_mode="classic"):
        self.k = k
        self.l = l
        self.cascade_costs = []

        # maciek: I don't use g in max_phase (local variable in recursive function instead)
        # todo: use g to hold most costly phase in the end?
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
    # (in principle, it would be possible to use all_requests that should return the same)
    def first_request(self, configuration):
        node_list = configuration.get_id_list()
        nodes_cluster1 = node_list[0]
        nodes_cluster2 = node_list[1]
        return [nodes_cluster1[0], nodes_cluster2[0]]

    # returns a list of all component id pairs (only pairs that matters)
    def all_requests(self, configuration):
        requests = []
        node_list = configuration.get_id_list()
       
        for idc1, cluster1 in enumerate(configuration.cluster_list):
            for idc2, cluster2 in enumerate(configuration.cluster_list):
                if idc1 < idc2: # consider each pair of clusters once
                    comps1 = cluster1.comp_list
                    comps2 = cluster2.comp_list

                    # enhance the list of components with component sizes
                    comps1sizes = map(lambda c: (c.size, c), comps1)
                    comps2sizes = map(lambda c: (c.size, c), comps2)

                    # sort components by component sizes
                    comps1sort = sorted(comps1sizes, key=lambda c: c[0])
                    comps2sort = sorted(comps2sizes, key=lambda c: c[0])
 
                    # remove duplicate components (of the same size)
                    comps1unique = (groupby(comps1sort, lambda s: s[0]))
                    comps2unique = (groupby(comps2sort, lambda s: s[0]))

                    # all pairs of components (recall these are of different clusters)
                    for key1, group1 in comps1unique:
                        g1 = next(group1)
                        for key2, group2 in comps2unique:
                            g2 = next(group2)
                            requests.append([g1[1].id, g2[1].id])
        return requests

    # todo: memoization
    # but first, rewrite as a function of configuration only,
    # (now is a function of: configuration + request)
    def max_phase_aux(self, configuration):

        # todo: cascade calculation inside the for loop
        # (interface for memoization)
        #
        # use hashable arguments for the function
        # (not objects, but graph.cluster_list (flattened to non-objects in components too))

        # if a cascade is possible, apply it
        is_cascade_possible, graph_changes = cascade_calculation.Calculation.possible_cascade(configuration)
        can_phase_continue = is_cascade_possible == 1
        if not can_phase_continue:
            return 0
        configuration.apply_cascade(graph_changes)
 
        # statistics
        current_request_cost = configuration.get_last_cascade_cost()
        self.cascade_number += 1
        self.cascade_costs.append(current_request_cost)

        # add recursively the cost of maximum successive cascades
        requests = self.all_requests(configuration)
        assert(not requests == [])

        max_remaining_cost = 0
        max_cost_branch = None

        for r in requests:
            # make an independent copy of the current graph (each recursion branch has its own graph)
            configuration_branch = copy.deepcopy(configuration)
            configuration_branch.comps_to_merge = r

            branch_cost = self.max_phase_aux(configuration_branch)

            if max_remaining_cost <= branch_cost:
                max_remaining_cost = branch_cost
                max_cost_branch = configuration_branch
        
        # todo: glue the history

        return max_remaining_cost + current_request_cost

