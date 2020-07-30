import pulp as p
import numpy as np
from representation import cascade_changes


class Calculation:

    # G is the graph, id1 and id2 are the two component ids to be merged
    @classmethod
    def possible_cascade(cls, g):
        k = g.k
        l = g.l
        id1, id2 = g.comps_to_merge[0], g.comps_to_merge[1]
        Lp_prob = p.LpProblem('cascade', p.LpMinimize)
        belonging_array, sizes, id_array, index1, index2 = g.belonging_array(id1, id2)
        m = len(sizes)

        # creating the variables
        xs = [p.LpVariable("x{0}_{1}".format(i, j), cat="Binary")
              for i in range(m) for j in range(l)]
        xs = np.array(xs)
        xs = xs.reshape((m, l))

        # minimize objective
        objective = p.lpSum([sizes[i] * xs[i, j] * belonging_array[i, j]] for i in range(m) for j in range(l))
        Lp_prob += objective

        # conditions
        # conditions for respecting the sizes of components
        for i in range(l):
            Lp_prob += p.lpSum([sizes[j] * xs[j, i]] for j in range(m)) == k
        # conditions to make sure that any component is in one cluster at the time
        for i in range(m):
            Lp_prob += p.lpSum([xs[i, j]] for j in range(l)) == 1
        # condition to make sure that the two compnents that must merge will be in the same cluster
        for i in range(l):
            Lp_prob += xs[index1, i] == xs[index2, i]
        # solving the problem
        p.PULP_CBC_CMD(msg=0).solve(Lp_prob)

        # Comunicating the results to create a new graph
        if Lp_prob.sol_status != 1:
            return Lp_prob.sol_status, None
        else:
            exchange_list = []
            for i in range(len(belonging_array)):
                for j in range(len(belonging_array[i])):
                    if belonging_array[i][j] == 0:
                        tmp = [j, id_array[i][j]]
                        break
                for k in range(len(xs[i])):
                    if xs[i][k].varValue == 1 and k != j:
                        tmp.insert(1, k)
                        exchange_list.append(tmp)
            cc = cascade_changes.Cascade_Changes(id1, id2, exchange_list)

            return Lp_prob.sol_status, cc

    # @classmethod
    # def closest_to_origin_cascade(cls, g):
    #     k = g.k
    #     l = g.l
    #     id1, id2 = g.comps_to_merge[0], g.comps_to_merge[1]
    #     Lp_prob = p.LpProblem('cascade', p.LpMinimize)
    #
    #     initial_config = g.initial_config
    #     sizes = g.get_sizes()
    #     m = k * l
    #
    #     # creating the variables
    #     xs = [p.LpVariable("x{0}_{1}".format(i, j), cat="Binary")
    #           for i in range(m) for j in range(l)]
    #     xs = np.array(xs)
    #     xs = xs.reshape((m, l))
    #
    #     # minimize objective
    #     objective = p.lpSum([xs[i, j] * initial_config[i, j]] for i in range(m) for j in range(l))
    #     Lp_prob += objective
    #
    #     # conditions
    #     # conditions for respecting the sizes of components
    #     for i in range(l):
    #         Lp_prob += p.lpSum([xs[j, i]] for j in range(m)) == k
    #     # conditions to make sure that any component is in one cluster at the time
    #     for i in range(m):
    #         Lp_prob += p.lpSum([xs[i, j]] for j in range(l)) == 1
    #     # condition to make sure that the two compnents that must merge will be in the same cluster
    #     for i in range(l):
    #         Lp_prob += xs[index1, i] == xs[index2, i]
    #     # solving the problem
    #     p.PULP_CBC_CMD(msg=0).solve(Lp_prob)
    #
    #     # Comunicating the results to create a new graph
    #     if Lp_prob.sol_status != 1:
    #         return Lp_prob.sol_status, None, -1
    #     else:
    #         exchange_list = []
    #         for i in range(len(initial_config)):
    #             for j in range(len(initial_config[i])):
    #                 if initial_config[i][j] == 0:
    #                     tmp = [j, id_array[i][j]]
    #                     break
    #             for k in range(len(xs[i])):
    #                 if xs[i][k].varValue == 1 and k != j:
    #                     tmp.insert(1, k)
    #                     exchange_list.append(tmp)
    #         cc = cascade_changes.Cascade_Changes(id1, id2, exchange_list)
    #
    #         return Lp_prob.sol_status, cc, p.value(Lp_prob.objective)

    @classmethod
    def closest_to_origin_cascade_v2(cls, g):
        k = g.k
        l = g.l
        id1, id2 = g.comps_to_merge[0], g.comps_to_merge[1]
        Lp_prob = p.LpProblem('cascade', p.LpMaximize)
        belonging_array, sizes, comp_sizes, id_array, index1, index2 = g.belonging_array_v2(id1, id2)
        m = len(sizes)

        # creating the variables
        xs = [p.LpVariable("x{0}_{1}".format(i, j), cat="Binary")
              for i in range(m) for j in range(l)]
        xs = np.array(xs)
        xs = xs.reshape((m, l))



        # minimize objective
        objective = p.lpSum([sizes[i, j] * xs[i, j] for i in range(m) for j in range(l)])
        Lp_prob += objective

        # conditions
        # conditions for respecting the sizes of components
        for i in range(l):
            Lp_prob += p.lpSum([comp_sizes[j] * xs[j, i]] for j in range(m)) == k
        # conditions to make sure that any component is in one cluster at the time
        for i in range(m):
            Lp_prob += p.lpSum([xs[i, j]] for j in range(l)) == 1
        # condition to make sure that the two components that must merge will be in the same cluster
        for i in range(l):
            Lp_prob += xs[index1, i] == xs[index2, i]

        # condition on the cost of the cascade
        Lp_prob += p.lpSum([comp_sizes[i] * xs[i, j] * belonging_array[i, j]] for i in range(m) for j in range(l)) <= l*k*np.log(k)

        # solving the problem
        p.PULP_CBC_CMD(msg=0).solve(Lp_prob)

        # Communicating the results to create a new graph
        if Lp_prob.sol_status != 1:
            return Lp_prob.sol_status, None
        else:
            exchange_list = []
            for i in range(len(belonging_array)):
                for j in range(len(belonging_array[i])):
                    if belonging_array[i][j] == 0:
                        tmp = [j, id_array[i][j]]
                        break
                for k in range(len(xs[i])):
                    if xs[i][k].varValue == 1 and k != j:
                        tmp.insert(1, k)
                        exchange_list.append(tmp)
            cc = cascade_changes.Cascade_Changes(id1, id2, exchange_list)

            return Lp_prob.sol_status, cc
